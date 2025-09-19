from typing import Dict, List, Tuple, Iterable, Optional, Set
from dataclasses import dataclass

import re
import os
import sys
import pandas as pd


@dataclass
class BookMeta:
    book_id: str
    book_name: str
    total_tokens: int = 0


@dataclass
class Boundary:
    id: str
    start_token: int
    end_token: int
    kind: str


@dataclass
class Character:
    character_id: str
    canonical_name: str
    aliases: List[str]
    match_pattern: str
    compiled_pattern: Optional[re.Pattern] = None


@dataclass
class Mention:
    book_id: str
    character_id: str
    token_idx: int
    span_token_start: int
    span_token_end: int
    surface_form: str
    alias_canonicalized_to: str
    chapter_id: Optional[str] = None
    paragraph_id: Optional[str] = None
    sentence_id: Optional[str] = None


@dataclass
class Segment:
    segment_id: str
    segment_type: str
    book_id: str
    start_token: int
    end_token: int
    token_count: int


def build_canonical_dictionary(raw_characters: Iterable[str], extra_aliases: Dict[str, List[str]]) -> Dict[str, Character]:
    def alias_to_pattern(alias: str) -> str:
        parts = re.split(r"[\s\-_]+", alias.strip().lower())
        parts = [re.escape(p) for p in parts if p]
        if not parts:
            return ""
        sep = r"(?:\s+|[-_])+"
        return sep.join(parts)

    characters: Dict[str, Character] = {}
    for idx, canonical in enumerate(raw_characters):
        canon = canonical.strip().lower()
        alias_list = [canon] + [a.strip().lower() for a in extra_aliases.get(canon, [])]
        patterns = [p for p in (alias_to_pattern(a) for a in alias_list) if p]
        pattern_str = r"\b(?:" + "|".join(patterns) + r")\b"
        compiled = re.compile(pattern_str, flags=re.IGNORECASE)
        characters[canon] = Character(
            character_id=f"char_{idx}",
            canonical_name=canon,
            aliases=alias_list,
            match_pattern=pattern_str,
            compiled_pattern=compiled,
        )
    return characters


def tokenize_text(text: str) -> List[str]:
    return re.findall(r"[A-Za-z]+(?:_[A-Za-z]+)?|\S", text)


def tokenize_with_offsets(text: str) -> Tuple[List[str], List[Tuple[int, int]]]:
    tokens: List[str] = []
    offsets: List[Tuple[int, int]] = []
    for match in re.finditer(r"[A-Za-z]+(?:_[A-Za-z]+)?|\S", text):
        tokens.append(match.group(0))
        offsets.append((match.start(), match.end()))
    return tokens, offsets


def split_into_chapters_normalized(book_text: str) -> List[Dict[str, Optional[str]]]:
    header_pattern = re.compile(
        r"^\s*(?:(CHAPTER\s+[A-Z\- ]+)\s*$\n?|(?:(Chapter\s+\d+)\s*[:\-—]\s*(.+)\s*$))",
        re.MULTILINE
    )

    matches = list(header_pattern.finditer(book_text))
    chapters: List[Dict[str, Optional[str]]] = []

    idx = 0
    if matches:
        first_start = matches[0].start()
        intro_chunk = book_text[:first_start].strip()
        if intro_chunk:
            lines = intro_chunk.split('\n')
            subtitle_line: Optional[str] = None
            rest_start_idx = 0
            for j, ln in enumerate(lines):
                if ln.strip():
                    subtitle_line = ln.strip()
                    rest_start_idx = j + 1
                    break
            remaining = '\n'.join(lines[rest_start_idx:]) if rest_start_idx < len(lines) else ''
            chapters.append({
                "index": idx,
                "title": "CHAPTER ONE",
                "subtitle": subtitle_line,
                "content": remaining
            })
            idx += 1
    else:
        content = book_text.strip()
        chapters.append({
            "index": idx,
            "title": "CHAPTER ONE",
            "subtitle": None,
            "content": content
        })
        return chapters

    for m_idx, m in enumerate(matches):
        end = m.end()
        upper_title = m.group(1)
        numeric_title = m.group(2)
        inline_subtitle = m.group(3)

        title: str
        subtitle: Optional[str] = None

        if numeric_title:
            title = numeric_title.strip()
            subtitle = inline_subtitle.strip() if inline_subtitle else None
            content_start = end
        else:
            title = upper_title.strip() if upper_title else "CHAPTER"
            content_start = end
            after = book_text[content_start:]
            nl_pos = after.find('\n')
            if nl_pos != -1:
                first_line = after[:nl_pos].strip()
                if first_line:
                    subtitle = first_line
                    content_start += nl_pos + 1

        next_start = matches[m_idx + 1].start() if m_idx + 1 < len(matches) else len(book_text)
        content = book_text[content_start:next_start].strip()

        chapters.append({
            "index": idx,
            "title": title,
            "subtitle": subtitle,
            "content": content
        })
        idx += 1

    return chapters


def _find_token_index_for_char(offsets: List[Tuple[int, int]], char_pos: int) -> Optional[int]:
    lo, hi = 0, len(offsets) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        s, e = offsets[mid]
        if s <= char_pos < e:
            return mid
        if char_pos < s:
            hi = mid - 1
        else:
            lo = mid + 1
    return None


def find_mentions_in_text(text: str, characters: Dict[str, Character], book_id: str = "unknown", chapter_id: Optional[str] = None) -> List[Mention]:
    tokens, offsets = tokenize_with_offsets(text)
    mentions: List[Mention] = []

    for canon_name, character in characters.items():
        if character.compiled_pattern is None:
            character.compiled_pattern = re.compile(character.match_pattern, flags=re.IGNORECASE)
        for m in character.compiled_pattern.finditer(text):
            start_char = m.start()
            end_char = m.end()
            start_tok = _find_token_index_for_char(offsets, start_char)
            end_tok = _find_token_index_for_char(offsets, end_char - 1)
            if start_tok is None or end_tok is None:
                continue
            mentions.append(Mention(
                book_id=book_id,
                character_id=character.character_id,
                token_idx=start_tok,
                span_token_start=start_tok,
                span_token_end=end_tok,
                surface_form=m.group(0),
                alias_canonicalized_to=character.canonical_name,
                chapter_id=chapter_id,
            ))
    return mentions


def find_mentions_in_chapter(chapter: Dict[str, Optional[str]], characters: Dict[str, Character], book_id: str, chapter_index: int) -> List[Mention]:
    chapter_id = f"chapter_{chapter_index}"
    content = chapter.get("content", "") or ""
    return find_mentions_in_text(content, characters, book_id=book_id, chapter_id=chapter_id)


def mentions_to_dataframe(mentions: List[Mention]) -> pd.DataFrame:
    rows = []
    for m in mentions:
        rows.append({
            "book_id": m.book_id,
            "chapter_id": m.chapter_id,
            "character_id": m.character_id,
            "canonical_name": m.alias_canonicalized_to,
            "span_token_start": m.span_token_start,
            "span_token_end": m.span_token_end,
            "surface_form": m.surface_form,
        })
    return pd.DataFrame(rows)


def save_mentions_parquet(df: pd.DataFrame, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_parquet(out_path, index=False)


def generate_all_mentions_parquet(out_path: str, focus_characters: Optional[Iterable[str]] = None) -> None:
    # Ensure project root on sys.path for imports when running as a package/module
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    from retrieval_and_cleaning import get_books_dataset
    from frequency_analysis_constants import ALIASES
    from collections import defaultdict

    extra_aliases = defaultdict(list)
    canonical_set = set()
    for original, replacement in ALIASES:
        canonical_set.add(replacement)
        extra_aliases[replacement].append(original)
    canonical_list = sorted(canonical_set)
    canon_dict = build_canonical_dictionary(canonical_list, extra_aliases)

    if focus_characters:
        focus = {c.lower() for c in focus_characters}
        canon_dict = {k: v for k, v in canon_dict.items() if k in focus}

    books, names = get_books_dataset()
    all_mentions: List[Mention] = []
    for book_name in sorted(names):
        chapters = split_into_chapters_normalized(books[book_name])
        for ch in chapters:
            ch_index = ch["index"]
            all_mentions.extend(find_mentions_in_chapter(ch, canon_dict, book_id=book_name, chapter_index=ch_index))

    df = mentions_to_dataframe(all_mentions)
    save_mentions_parquet(df, out_path)


