from typing import Dict, List, Tuple, Iterable, Optional

import math
from itertools import combinations
from collections import defaultdict
import os
import pandas as pd


def kernel_score_pair(positions_a: List[int], positions_b: List[int], sigma: float = 200.0, radius: int = 600) -> float:
    if not positions_a or not positions_b:
        return 0.0
    i, j = 0, 0
    score = 0.0
    inv_two_sigma_sq = 1.0 / (2.0 * sigma * sigma)
    while i < len(positions_a) and j < len(positions_b):
        a = positions_a[i]
        b = positions_b[j]
        d = abs(a - b)
        if d <= radius:
            score += math.exp(-(d * d) * inv_two_sigma_sq)
        if a < b:
            i += 1
        else:
            j += 1
    return score


def build_token_windows(tokens_per_chapter: Dict[Tuple[str, int], int], window_size: int, step: int) -> List[Dict]:
    segments: List[Dict] = []
    for (book_id, chapter_index), total_tokens in tokens_per_chapter.items():
        start = 0
        while start < total_tokens:
            end = min(start + window_size, total_tokens) - 1
            window_id = f"{book_id}__chapter_{chapter_index}__w_{start}"
            segments.append({
                "window_id": window_id,
                "book_id": book_id,
                "chapter_index": chapter_index,
                "start_token": start,
                "end_token": end,
            })
            if end + 1 >= total_tokens:
                break
            start += step
    return segments


def compute_window_counts(segments: Iterable[Dict], mentions_df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
    by_chapter: Dict[Tuple[str, int], List[Dict]] = defaultdict(list)
    for seg in segments:
        by_chapter[(seg["book_id"], seg["chapter_index"])].append(seg)

    window_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def _chapter_index_from_id(ch_id: str) -> Optional[int]:
        try:
            return int(ch_id.split("_")[-1])
        except Exception:
            return None

    mentions_df = mentions_df.copy()
    mentions_df["chapter_index"] = mentions_df["chapter_id"].map(_chapter_index_from_id)

    for (book_id, chapter_index), group in mentions_df.groupby(["book_id", "chapter_index"], dropna=True):
        segs = by_chapter.get((book_id, int(chapter_index)), [])
        if not segs:
            continue
        for seg in segs:
            s, e = seg["start_token"], seg["end_token"]
            overlaps = group[(group["span_token_end"] >= s) & (group["span_token_start"] <= e)]
            if overlaps.empty:
                continue
            counts = window_counts[seg["window_id"]]
            for name, cnt in overlaps["canonical_name"].value_counts().items():
                counts[name] += int(cnt)

    return window_counts


def compute_npmi_edges(window_counts: Dict[str, Dict[str, int]]) -> Dict[Tuple[str, str], float]:
    char_to_windows: Dict[str, set] = defaultdict(set)
    all_windows = set(window_counts.keys())
    for w_id, counts in window_counts.items():
        for char, c in counts.items():
            if c > 0:
                char_to_windows[char].add(w_id)

    total_windows = max(len(all_windows), 1)
    edges: Dict[Tuple[str, str], float] = {}
    chars = sorted(char_to_windows.keys())
    for a, b in combinations(chars, 2):
        Wa = char_to_windows[a]
        Wb = char_to_windows[b]
        inter = len(Wa & Wb)
        if inter == 0:
            continue
        pa = len(Wa) / total_windows
        pb = len(Wb) / total_windows
        pab = inter / total_windows
        try:
            pmi = math.log(pab / (pa * pb))
            npmi = pmi / (-math.log(pab))
        except (ZeroDivisionError, ValueError):
            continue
        edges[(a, b)] = npmi
    return edges


def build_edge_list_kernel(mentions_df: pd.DataFrame, sigma: float = 200.0, radius: int = 600) -> List[Tuple[str, str, float]]:
    req = {"book_id", "chapter_id", "canonical_name", "span_token_start"}
    if not req.issubset(mentions_df.columns):
        raise ValueError(f"mentions_df missing columns: {req - set(mentions_df.columns)}")

    def _chapter_index_from_id(ch_id: str) -> Optional[int]:
        try:
            return int(ch_id.split("_")[-1])
        except Exception:
            return None

    df = mentions_df.copy()
    df["chapter_index"] = df["chapter_id"].map(_chapter_index_from_id)

    pair_scores: Dict[Tuple[str, str], float] = defaultdict(float)
    for (book_id, ch_idx), g in df.groupby(["book_id", "chapter_index"], dropna=True):
        pos_by_char: Dict[str, List[int]] = defaultdict(list)
        for name, sub in g.groupby("canonical_name"):
            pos = sorted(sub["span_token_start"].astype(int).tolist())
            if pos:
                pos_by_char[name] = pos
        chars = sorted(pos_by_char.keys())
        for a, b in combinations(chars, 2):
            score = kernel_score_pair(pos_by_char[a], pos_by_char[b], sigma=sigma, radius=radius)
            if score > 0:
                pair_scores[(a, b)] += score

    return [(a, b, w) for (a, b), w in pair_scores.items()]


def build_edge_list_npmi(window_counts: Dict[str, Dict[str, int]]) -> List[Tuple[str, str, float]]:
    edges = compute_npmi_edges(window_counts)
    return [(a, b, w) for (a, b), w in edges.items()]


def edges_to_csv(edges: List[Tuple[str, str, float]], out_path: str) -> None:
    df = pd.DataFrame(edges, columns=["char_a", "char_b", "weight"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)


def generate_kernel_edges_csv(parquet_path: str, out_csv: str, sigma: float = 200.0, radius: int = 600) -> None:
    df = pd.read_parquet(parquet_path)
    edges = build_edge_list_kernel(df, sigma=sigma, radius=radius)
    edges_to_csv(edges, out_csv)


def generate_npmi_edges_csv(parquet_path: str, out_csv: str, window_size: int = 200, step: int = 100) -> None:
    df = pd.read_parquet(parquet_path)
    
    # Create tokens_per_chapter dictionary from parquet data
    # Convert chapter_id (string) to chapter_index (int) for compatibility
    tokens_per_chapter = {}
    for (book_id, chapter_id), group in df.groupby(['book_id', 'chapter_id']):
        # Extract chapter index from chapter_id (e.g., "chapter_0" -> 0)
        try:
            chapter_index = int(chapter_id.split('_')[-1])
        except (ValueError, IndexError):
            continue
            
        # Get the maximum span_token_end for this chapter to determine total tokens
        total_tokens = group['span_token_end'].max() + 1 if len(group) > 0 else 0
        tokens_per_chapter[(book_id, chapter_index)] = total_tokens
    
    token_counts = build_token_windows(tokens_per_chapter, window_size=window_size, step=step)
    window_counts = compute_window_counts(token_counts, df)
    edges = build_edge_list_npmi(window_counts)
    edges_to_csv(edges, out_csv)


