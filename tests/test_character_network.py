from collections import defaultdict, Counter
import os
import sys
import pandas as pd

# Ensure project root is on sys.path when running from the tests folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from retrieval_and_cleaning import get_books_dataset
from character_network.core import (
    split_into_chapters_normalized,
    build_canonical_dictionary,
    find_mentions_in_chapter,
    generate_all_mentions_parquet,
)
from frequency_analysis_constants import ALIASES


def build_canon_from_constants():
    extra_aliases = defaultdict(list)
    canonical_set = set()
    for original, replacement in ALIASES:
        canonical_set.add(replacement)
        extra_aliases[replacement].append(original)
    canonical_list = sorted(canonical_set)
    return build_canonical_dictionary(canonical_list, extra_aliases)


def view_mentions_parquet(parquet_path: str, head_n: int = 20) -> None:
    """View the contents of the mentions parquet file as a readable dataframe."""
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Mentions parquet not found: {parquet_path}")
    
    df = pd.read_parquet(parquet_path)
    print(f"Mentions parquet shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst {head_n} rows:")
    print(df.head(head_n))
    
    if 'canonical_name' in df.columns:
        print(f"\nCharacter counts:")
        print(df['canonical_name'].value_counts().head(10))


def count_mentions_per_book(parquet_path: str) -> None:
    """Count mentions per book and per character per book."""
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Mentions parquet not found: {parquet_path}")
    
    df = pd.read_parquet(parquet_path)
    
    if 'book_id' not in df.columns:
        print("No 'book_id' column found in mentions data")
        return
    
    print("=== MENTIONS PER BOOK ===")
    book_counts = df['book_id'].value_counts().sort_index()
    for book_id, count in book_counts.items():
        print(f"Book {book_id}: {count:,} mentions")
    
    print(f"\nTotal mentions across all books: {len(df):,}")
    
    if 'canonical_name' in df.columns:
        print("\n=== TOP CHARACTERS PER BOOK ===")
        for book_id in sorted(df['book_id'].unique()):
            book_df = df[df['book_id'] == book_id]
            top_chars = book_df['canonical_name'].value_counts().head(5)
            print(f"\nBook {book_id} (top 5 characters):")
            for char, count in top_chars.items():
                print(f"  {char}: {count:,} mentions")


def smoke_test_mentions_first_chapter():
    canon_dict = build_canon_from_constants()

    # Focus on a small subset for quick feedback
    focus = {"harry", "ron", "hermione", "dumbledore", "voldemort"}
    subset = {k: v for k, v in canon_dict.items() if k in focus}

    books, names = get_books_dataset()
    for book_name in sorted(names):
        chapters = split_into_chapters_normalized(books[book_name])
        if not chapters:
            print(f"Book: {book_name} -> no chapters detected")
            continue
        mentions = find_mentions_in_chapter(chapters[0], subset, book_id=book_name, chapter_index=0)
        counts = Counter(m.character_id for m in mentions)
        id_to_name = {c.character_id: c.canonical_name for c in subset.values()}
        print(f"Book: {book_name}")
        print(f"  Chapters detected: {len(chapters)}")
        print(f"  First chapter: {chapters[0]['title']} | {chapters[0]['subtitle']}")
        print(f"  Mentions (first chapter): {dict(counts)}")
        print(f"  Mentions by name: {', '.join(f'{id_to_name.get(k, k)}: {v}' for k, v in counts.items())}")


def smoke_test_save_and_view_parquet():
    """Generate mentions.parquet and view its contents."""
    print("=== GENERATING MENTIONS PARQUET ===")
    mentions_path = os.path.join("Artifacts", "mentions.parquet")
    generate_all_mentions_parquet(out_path=mentions_path)
    
    print("\n=== VIEWING MENTIONS PARQUET ===")
    view_mentions_parquet(mentions_path)
    
    print("\n=== COUNTING MENTIONS PER BOOK ===")
    count_mentions_per_book(mentions_path)


if __name__ == "__main__":
    print("=== FIRST CHAPTER MENTIONS TEST ===")
    smoke_test_mentions_first_chapter()
    
    print("\n" + "="*50)
    print("=== PARQUET GENERATION AND VIEWING TEST ===")
    smoke_test_save_and_view_parquet()


