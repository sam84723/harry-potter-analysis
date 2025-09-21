"""
Character Network Animation Module

This module provides functions to create animated character network visualizations
showing the evolution of character relationships over time (by chapter).
"""

import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


def load_mentions_data(mentions_path: str) -> pd.DataFrame:
    """Load mentions data from parquet file."""
    return pd.read_parquet(mentions_path)


def load_edges_data(edges_path: str) -> pd.DataFrame:
    """Load edges data from CSV file."""
    return pd.read_csv(edges_path)


def prepare_chapter_data(mentions_df: pd.DataFrame) -> Dict[str, List[Tuple[str, int]]]:
    """
    Prepare character mentions data organized by chapter.
    
    Returns:
        Dict mapping chapter_id to list of (character, token_position) tuples
    """
    chapter_mentions = defaultdict(list)
    
    for _, row in mentions_df.iterrows():
        chapter_id = row['chapter_id']
        book_id = row['book_id']
        character = row['canonical_name']  # Use canonical_name instead of 'character'
        token_pos = row['span_token_start']  # Use start position
        
        # Create unique chapter identifier combining book and chapter
        unique_chapter_id = f"{book_id}_{chapter_id}"
        chapter_mentions[unique_chapter_id].append((character, token_pos))
    
    # Sort chapters by book and chapter number
    def chapter_sort_key(unique_chapter_id):
        book_id, chapter_id = unique_chapter_id.split('_', 1)
        # Extract book number from filename
        book_num = int(book_id.split()[0])  # "01 Harry Potter..." -> 1
        chapter_num = int(chapter_id.split('_')[1])  # "chapter_0" -> 0
        return (book_num, chapter_num)
    
    sorted_chapters = sorted(chapter_mentions.keys(), key=chapter_sort_key)
    
    return {ch: chapter_mentions[ch] for ch in sorted_chapters}


def build_cumulative_network(chapter_data: Dict[str, List[Tuple[str, int]]], 
                           up_to_chapter: str) -> nx.Graph:
    """
    Build network with all mentions up to and including the specified chapter.
    """
    G = nx.Graph()
    
    # Collect all mentions up to this chapter
    all_mentions = []
    for chapter_id, mentions in chapter_data.items():
        if chapter_id <= up_to_chapter:
            all_mentions.extend(mentions)
    
    if not all_mentions:
        return G
    
    # Add nodes for all characters mentioned so far
    characters = set(char for char, _ in all_mentions)
    G.add_nodes_from(characters)
    
    # Calculate edge weights based on proximity
    char_pairs = defaultdict(list)
    for char, pos in all_mentions:
        char_pairs[char].append(pos)
    
    # Simple proximity scoring: count co-occurrences within 50 tokens
    for char1 in characters:
        for char2 in characters:
            if char1 < char2:  # Avoid duplicates
                weight = 0
                for pos1 in char_pairs[char1]:
                    for pos2 in char_pairs[char2]:
                        if abs(pos1 - pos2) <= 50:  # Within 50 tokens
                            weight += 1
                
                if weight > 0:
                    G.add_edge(char1, char2, weight=weight)
    
    return G


def build_rolling_network(chapter_data: Dict[str, List[Tuple[str, int]]], 
                        current_chapter: str, window_size: int = 3) -> nx.Graph:
    """
    Build network with mentions from the last N chapters (rolling window).
    """
    G = nx.Graph()
    
    # Get list of chapters
    chapters = list(chapter_data.keys())
    current_idx = chapters.index(current_chapter)
    
    # Get window of chapters
    start_idx = max(0, current_idx - window_size + 1)
    window_chapters = chapters[start_idx:current_idx + 1]
    
    # Collect mentions from window
    all_mentions = []
    for chapter_id in window_chapters:
        all_mentions.extend(chapter_data[chapter_id])
    
    if not all_mentions:
        return G
    
    # Add nodes for all characters in window
    characters = set(char for char, _ in all_mentions)
    G.add_nodes_from(characters)
    
    # Calculate edge weights (same as cumulative)
    char_pairs = defaultdict(list)
    for char, pos in all_mentions:
        char_pairs[char].append(pos)
    
    for char1 in characters:
        for char2 in characters:
            if char1 < char2:
                weight = 0
                for pos1 in char_pairs[char1]:
                    for pos2 in char_pairs[char2]:
                        if abs(pos1 - pos2) <= 50:
                            weight += 1
                
                if weight > 0:
                    G.add_edge(char1, char2, weight=weight)
    
    return G


def create_network_animation(mentions_path: str, 
                           output_path: str,
                           animation_type: str = "cumulative",
                           window_size: int = 3,
                           fps: int = 2,
                           figsize: Tuple[int, int] = (12, 8)) -> None:
    """
    Create an animated network visualization.
    
    Args:
        mentions_path: Path to mentions parquet file
        output_path: Path to save the animation (MP4)
        animation_type: "cumulative" or "rolling"
        window_size: For rolling animation, number of chapters in window
        fps: Frames per second
        figsize: Figure size
    """
    # Load data
    mentions_df = load_mentions_data(mentions_path)
    chapter_data = prepare_chapter_data(mentions_df)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Get all chapters
    chapters = list(chapter_data.keys())
    
    # Pre-compute layout using all data for consistency
    all_mentions = []
    for mentions in chapter_data.values():
        all_mentions.extend(mentions)
    
    all_characters = set(char for char, _ in all_mentions)
    G_full = nx.Graph()
    G_full.add_nodes_from(all_characters)
    
    # Use spring layout for consistent positioning
    pos = nx.spring_layout(G_full, k=1, iterations=50)
    
    def animate(frame):
        ax.clear()
        
        if frame >= len(chapters):
            return
        
        current_chapter = chapters[frame]
        
        # Build network based on type
        if animation_type == "cumulative":
            G = build_cumulative_network(chapter_data, current_chapter)
        else:  # rolling
            G = build_rolling_network(chapter_data, current_chapter, window_size)
        
        if G.number_of_nodes() == 0:
            ax.set_title(f"Chapter {current_chapter} - No characters yet")
            ax.axis('off')
            return
        
        # Draw network
        # Nodes with special coloring for Harry Potter
        node_sizes = [300 for _ in G.nodes()]
        node_colors = []
        for node in G.nodes():
            if 'harry' in node.lower() or 'potter' in node.lower():
                node_colors.append('red')
            else:
                node_colors.append('lightblue')
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.7)
        
        # Edges
        if G.number_of_edges() > 0:
            edges = G.edges()
            weights = [G[u][v]['weight'] for u, v in edges]
            max_weight = max(weights) if weights else 1
            
            # Scale edge widths
            edge_widths = [w / max_weight * 3 for w in weights]
            
            nx.draw_networkx_edges(G, pos, width=edge_widths, 
                                  alpha=0.6, edge_color='gray')
        
        # Labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        # Format chapter info
        book_id, chapter_id = current_chapter.split('_', 1)
        book_num = book_id.split()[0]  # "05 Harry Potter..." -> "05"
        book_title = ' '.join(book_id.split()[1:])  # "05 Harry Potter..." -> "Harry Potter and the Half-Blood Prince.txt"
        book_title = book_title.replace('.txt', '')  # Remove .txt extension
        chapter_num = int(chapter_id.split('_')[1]) + 1  # "chapter_0" -> 1
        
        # Main title
        main_title = f"{animation_type.title()} Character Network"
        
        # Secondary title
        secondary_title = f"Book {book_num}: {book_title} - Chapter {chapter_num}"
        
        # Set titles
        ax.set_title(main_title, fontsize=16, fontweight='bold', pad=20)
        ax.text(0.5, 0.95, secondary_title, transform=ax.transAxes, 
                fontsize=12, ha='center', va='top')
        
        # Window size label (for rolling only)
        if animation_type == "rolling":
            ax.text(0.02, 0.02, f"Window: {window_size} chapters", 
                    transform=ax.transAxes, fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))
        ax.axis('off')
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=len(chapters), 
                                 interval=1000//fps, repeat=True)
    
    # Save animation
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Try ffmpeg first, fall back to Pillow for GIF
    try:
        anim.save(output_path, writer='ffmpeg', fps=fps)
        print(f"Animation saved to: {output_path}")
    except Exception as e:
        print(f"ffmpeg not available: {e}")
        # Fall back to GIF
        gif_path = output_path.replace('.mp4', '.gif')
        anim.save(gif_path, writer='pillow', fps=fps)
        print(f"Animation saved as GIF to: {gif_path}")


def main():
    """Command line interface for creating network animations."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create character network animations")
    parser.add_argument("--mentions", default="Artifacts/mentions.parquet",
                       help="Path to mentions parquet file")
    parser.add_argument("--output", default="Artifacts/network_animation.mp4",
                       help="Output path for animation")
    parser.add_argument("--type", choices=["cumulative", "rolling"], 
                       default="cumulative", help="Animation type")
    parser.add_argument("--window", type=int, default=3,
                       help="Window size for rolling animation")
    parser.add_argument("--fps", type=int, default=2,
                       help="Frames per second")
    
    args = parser.parse_args()
    
    create_network_animation(
        mentions_path=args.mentions,
        output_path=args.output,
        animation_type=args.type,
        window_size=args.window,
        fps=args.fps
    )


if __name__ == "__main__":
    main()
