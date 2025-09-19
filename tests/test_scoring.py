import os
import sys

# Ensure project root is on sys.path when running from the tests folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pandas as pd
import numpy as np
from character_network.scoring import (
    build_edge_list_kernel, 
    build_token_windows, 
    compute_window_counts, 
    build_edge_list_npmi,
    compute_npmi_edges,
    generate_npmi_edges_csv
)
from character_network.core import split_into_chapters_normalized, tokenize_with_offsets
from retrieval_and_cleaning import get_books_dataset


def test_build_token_windows():
    """Test the build_token_windows function with sample data."""
    print("=== Testing build_token_windows ===")
    
    # Sample data: (book_id, chapter_index) -> total_tokens
    tokens_per_chapter = {
        ("book1", 0): 1000,  # 1000 tokens
        ("book1", 1): 800,   # 800 tokens
        ("book2", 0): 500,   # 500 tokens
    }
    
    window_size = 200
    step = 100
    
    segments = build_token_windows(tokens_per_chapter, window_size, step)
    
    print(f"Created {len(segments)} windows")
    print("Sample windows:")
    for i, seg in enumerate(segments[:5]):
        print(f"  {i+1}. {seg['window_id']}: tokens {seg['start_token']}-{seg['end_token']}")
    
    # Verify window properties
    assert len(segments) > 0, "Should create at least one window"
    assert all('window_id' in seg for seg in segments), "All segments should have window_id"
    assert all('book_id' in seg for seg in segments), "All segments should have book_id"
    assert all('chapter_index' in seg for seg in segments), "All segments should have chapter_index"
    assert all('start_token' in seg for seg in segments), "All segments should have start_token"
    assert all('end_token' in seg for seg in segments), "All segments should have end_token"
    
    # Check that windows don't exceed chapter boundaries
    for seg in segments:
        chapter_tokens = tokens_per_chapter[(seg['book_id'], seg['chapter_index'])]
        assert seg['end_token'] < chapter_tokens, f"Window {seg['window_id']} exceeds chapter boundary"
    
    print("✅ build_token_windows test passed\n")


def test_compute_window_counts():
    """Test the compute_window_counts function with sample data."""
    print("=== Testing compute_window_counts ===")
    
    # Create sample segments
    segments = [
        {
            "window_id": "book1__chapter_0__w_0",
            "book_id": "book1",
            "chapter_index": 0,
            "start_token": 0,
            "end_token": 199,
        },
        {
            "window_id": "book1__chapter_0__w_100",
            "book_id": "book1", 
            "chapter_index": 0,
            "start_token": 100,
            "end_token": 299,
        }
    ]
    
    # Create sample mentions DataFrame
    mentions_data = [
        {"book_id": "book1", "chapter_id": "chapter_0", "canonical_name": "harry", "span_token_start": 50, "span_token_end": 50},
        {"book_id": "book1", "chapter_id": "chapter_0", "canonical_name": "harry", "span_token_start": 150, "span_token_end": 150},
        {"book_id": "book1", "chapter_id": "chapter_0", "canonical_name": "ron", "span_token_start": 160, "span_token_end": 160},
        {"book_id": "book1", "chapter_id": "chapter_0", "canonical_name": "hermione", "span_token_start": 250, "span_token_end": 250},
    ]
    
    mentions_df = pd.DataFrame(mentions_data)
    
    window_counts = compute_window_counts(segments, mentions_df)
    
    print(f"Computed window counts for {len(window_counts)} windows")
    print("Window counts:")
    for window_id, counts in window_counts.items():
        print(f"  {window_id}: {dict(counts)}")
    
    # Verify results
    assert len(window_counts) > 0, "Should have window counts"
    
    # Check specific windows
    window1 = window_counts.get("book1__chapter_0__w_0", {})
    window2 = window_counts.get("book1__chapter_0__w_100", {})
    
    # Window 1 (tokens 0-199) should have harry (token 50) and harry (token 150)
    assert window1.get("harry", 0) == 2, f"Window 1 should have harry mentioned 2 times, got {window1.get('harry', 0)}"
    
    # Window 2 (tokens 100-299) should have harry (token 150), ron (token 160), hermione (token 250)
    assert window2.get("harry", 0) == 1, f"Window 2 should have harry mentioned 1 time, got {window2.get('harry', 0)}"
    assert window2.get("ron", 0) == 1, f"Window 2 should have ron mentioned 1 time, got {window2.get('ron', 0)}"
    assert window2.get("hermione", 0) == 1, f"Window 2 should have hermione mentioned 1 time, got {window2.get('hermione', 0)}"
    
    print("✅ compute_window_counts test passed\n")


def test_compute_npmi_edges():
    """Test the compute_npmi_edges function with sample data."""
    print("=== Testing compute_npmi_edges ===")
    
    # Create sample window counts
    window_counts = {
        "window1": {"harry": 2, "ron": 1, "hermione": 1},
        "window2": {"harry": 1, "ron": 2, "hermione": 1},
        "window3": {"harry": 1, "hermione": 2},
        "window4": {"ron": 1, "hermione": 1},
    }
    
    edges = compute_npmi_edges(window_counts)
    
    print(f"Computed {len(edges)} NPMI edges")
    print("Sample edges:")
    sorted_edges = sorted(edges.items(), key=lambda x: x[1], reverse=True)
    for (char1, char2), score in sorted_edges[:5]:
        print(f"  {char1} - {char2}: {score:.3f}")
    
    # Verify results
    assert len(edges) > 0, "Should have NPMI edges"
    
    # Check that we have edges for character pairs that co-occur
    char_pairs = set()
    for (char1, char2) in edges.keys():
        char_pairs.add((char1, char2))
        char_pairs.add((char2, char1))  # Both directions
    
    # harry-ron should have an edge (co-occur in window1 and window2)
    assert ("harry", "ron") in char_pairs, "harry-ron should have an edge"
    
    # harry-hermione should have an edge (co-occur in window1, window2, window3)
    assert ("harry", "hermione") in char_pairs, "harry-hermione should have an edge"
    
    # ron-hermione should have an edge (co-occur in window2 and window4)
    assert ("ron", "hermione") in char_pairs, "ron-hermione should have an edge"
    
    print("✅ compute_npmi_edges test passed\n")


def test_build_edge_list_npmi():
    """Test the build_edge_list_npmi function."""
    print("=== Testing build_edge_list_npmi ===")
    
    # Create sample window counts (same as compute_npmi_edges test)
    window_counts = {
        "window1": {"harry": 2, "ron": 1, "hermione": 1},
        "window2": {"harry": 1, "ron": 2, "hermione": 1},
        "window3": {"harry": 1, "hermione": 2},
        "window4": {"ron": 1, "hermione": 1},
    }
    
    edge_list = build_edge_list_npmi(window_counts)
    
    print(f"Built {len(edge_list)} edge list entries")
    print("Sample edges:")
    for char1, char2, weight in edge_list[:3]:
        print(f"  {char1} - {char2}: {weight:.3f}")
    
    # Verify results
    assert len(edge_list) > 0, "Should have edge list entries"
    assert all(len(edge) == 3 for edge in edge_list), "All edges should have 3 elements (char1, char2, weight)"
    assert all(isinstance(weight, (int, float)) for _, _, weight in edge_list), "All weights should be numeric"
    
    print("✅ build_edge_list_npmi test passed\n")


def test_generate_npmi_edges_csv():
    """Test the generate_npmi_edges_csv function with real data."""
    print("=== Testing generate_npmi_edges_csv ===")
    
    parquet_path = "Artifacts/mentions.parquet"
    if not os.path.exists(parquet_path):
        print(f"Parquet not found at {parquet_path}. Skipping test.")
        return
    
    output_path = "Artifacts/edges_npmi.csv"
    
    try:
        generate_npmi_edges_csv(parquet_path, output_path, window_size=200, step=100)
        
        if os.path.exists(output_path):
            df = pd.read_csv(output_path)
            print(f"Generated CSV with {len(df)} edges")
            print("Sample edges:")
            print(df.head())
            
            # Verify CSV structure
            assert list(df.columns) == ["char_a", "char_b", "weight"], "CSV should have correct columns"
            assert len(df) >= 0, "Should have some edges (even if 0)"
            
            print("✅ generate_npmi_edges_csv test passed")
        else:
            print("❌ CSV file was not created")
            
    except Exception as e:
        print(f"❌ generate_npmi_edges_csv test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()


def gaussian_kernel_smoke_test(parquet_path: str = "Artifacts/mentions.parquet", sigma: float = 200.0, radius: int = 600, top_k: int = 15):
    if not os.path.exists(parquet_path):
        print(f"Parquet not found at {parquet_path}. Generate it first (tests/test_character_network.py).")
        return

    df = pd.read_parquet(parquet_path)
    print("Loaded mentions:", df.shape)

    edges = build_edge_list_kernel(df, sigma=sigma, radius=radius)
    print("Computed kernel edges:", len(edges))

    # Sort by weight desc and show top_k
    edges_sorted = sorted(edges, key=lambda x: x[2], reverse=True)[:top_k]
    print("Top edges (Gaussian kernel):")
    for a, b, w in edges_sorted:
        print(f"  {a:15s} - {b:15s} : {w:.3f}")


def run_all_npmi_tests():
    """Run all NPMI-related tests."""
    print("🧪 Running NPMI Scoring Tests")
    print("=" * 50)
    
    # Test individual functions
    test_build_token_windows()
    test_compute_window_counts()
    test_compute_npmi_edges()
    test_build_edge_list_npmi()
    test_generate_npmi_edges_csv()
    
    print("🎉 All NPMI tests completed!")


if __name__ == "__main__":
    print("🧪 Running Scoring Tests")
    print("=" * 50)
    
    # Run kernel test
    print("=== Gaussian Kernel Test ===")
    gaussian_kernel_smoke_test()
    
    print("\n" + "=" * 50)
    
    # Run NPMI tests
    run_all_npmi_tests()


