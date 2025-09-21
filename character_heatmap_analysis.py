#!/usr/bin/env python3
"""
Character-Specific Heatmap Analysis
===================================

This script creates focused heatmap visualizations showing the top connections
for specific characters, useful for analyzing individual character networks.

Usage: py -3 character_heatmap_analysis.py
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frequency_analysis_constants import CHARACTER_HOUSES

def load_edges_data(edges_file):
    """Load edges data from CSV file."""
    if not os.path.exists(edges_file):
        raise FileNotFoundError(f"Edges file not found: {edges_file}")
    
    df = pd.read_csv(edges_file)
    if df.empty:
        raise ValueError("Edges CSV is empty")
    
    return df

def get_character_connections(df, character_name, top_n=10):
    """Get top N connections for a specific character."""
    # Find all edges involving this character
    char_edges = df[
        (df['char_a'] == character_name) | 
        (df['char_b'] == character_name)
    ].copy()
    
    if char_edges.empty:
        print(f"No connections found for {character_name}")
        return None, None
    
    # Normalize the edges so the character is always in 'char_a' column
    normalized_edges = []
    for _, row in char_edges.iterrows():
        if row['char_a'] == character_name:
            normalized_edges.append({
                'character': character_name,
                'connected_to': row['char_b'],
                'weight': row['weight']
            })
        else:
            normalized_edges.append({
                'character': character_name,
                'connected_to': row['char_a'],
                'weight': row['weight']
            })
    
    # Convert to DataFrame and sort by weight
    connections_df = pd.DataFrame(normalized_edges)
    connections_df = connections_df.sort_values('weight', ascending=False)
    
    # Get top N connections
    top_connections = connections_df.head(top_n)
    
    return top_connections, connections_df

def create_character_heatmap(character_name, connections_df, out_png=None, show=True):
    """Create a focused heatmap for a specific character's connections."""
    if connections_df is None or connections_df.empty:
        print(f"No data to visualize for {character_name}")
        return
    
    # Prepare data for heatmap
    characters = [character_name] + connections_df['connected_to'].tolist()
    weights = [0] + connections_df['weight'].tolist()  # Character's connection to itself is 0
    
    # Create a matrix (1 row, multiple columns)
    matrix = np.array([weights])
    
    # Create the plot
    plt.figure(figsize=(max(12, len(characters) * 1.2), 4))
    
    # Create heatmap
    sns.heatmap(matrix, 
                xticklabels=characters,
                yticklabels=[f"{character_name}'s Connections"],
                annot=True, 
                fmt='.0f',
                cmap='YlOrRd',
                cbar_kws={'label': 'Connection Strength'},
                square=False)
    
    # Customize the plot
    plt.title(f'{character_name.title()}\'s Top {len(connections_df)} Character Connections', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Connected Characters', fontsize=12)
    plt.ylabel('')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Add house colors to character names
    ax = plt.gca()
    for i, char in enumerate(characters):
        house = CHARACTER_HOUSES.get(char, 'unknown')
        color = get_house_color(house)
        ax.get_xticklabels()[i].set_color(color)
        ax.get_xticklabels()[i].set_fontweight('bold')
    
    plt.tight_layout()
    
    if out_png:
        os.makedirs(os.path.dirname(out_png), exist_ok=True)
        plt.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Character heatmap saved to: {out_png}")
    
    if show:
        plt.show()
    else:
        plt.close()

def get_house_color(house):
    """Get color for house."""
    house_colors = {
        'gryffindor': '#DC143C',  # Crimson
        'slytherin': '#2F4F2F',   # Dark green
        'ravenclaw': '#4169E1',   # Royal blue
        'hufflepuff': '#DAA520',  # Goldenrod
        'unknown': '#808080'      # Gray
    }
    return house_colors.get(house.lower(), '#808080')

def create_comparison_heatmap(characters, edges_file, out_png=None, show=True):
    """Create a comparison heatmap showing multiple characters' top connections."""
    df = load_edges_data(edges_file)
    
    # Get data for each character
    char_data = {}
    for char in characters:
        connections, _ = get_character_connections(df, char, top_n=10)
        if connections is not None:
            char_data[char] = connections
    
    if not char_data:
        print("No data found for any of the specified characters")
        return
    
    # Create comparison matrix
    all_connected_chars = set()
    for connections in char_data.values():
        all_connected_chars.update(connections['connected_to'].tolist())
    
    all_connected_chars = sorted(list(all_connected_chars))
    
    # Create matrix
    matrix = np.zeros((len(characters), len(all_connected_chars)))
    
    for i, char in enumerate(characters):
        if char in char_data:
            connections = char_data[char]
            for _, row in connections.iterrows():
                connected_char = row['connected_to']
                if connected_char in all_connected_chars:
                    j = all_connected_chars.index(connected_char)
                    matrix[i, j] = row['weight']
    
    # Create the plot
    plt.figure(figsize=(max(16, len(all_connected_chars) * 0.8), max(8, len(characters) * 1.5)))
    
    sns.heatmap(matrix,
                xticklabels=all_connected_chars,
                yticklabels=[f"{char.title()}'s Connections" for char in characters],
                annot=True,
                fmt='.0f',
                cmap='YlOrRd',
                cbar_kws={'label': 'Connection Strength'},
                square=False)
    
    plt.title('Character Connection Comparison', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Connected Characters', fontsize=12)
    plt.ylabel('')
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if out_png:
        os.makedirs(os.path.dirname(out_png), exist_ok=True)
        plt.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Comparison heatmap saved to: {out_png}")
    
    if show:
        plt.show()
    else:
        plt.close()

def analyze_character_network(character_name, edges_file):
    """Analyze a character's network connections."""
    df = load_edges_data(edges_file)
    connections, all_connections = get_character_connections(df, character_name, top_n=20)
    
    if connections is None:
        return
    
    print(f"\n{character_name.upper()} NETWORK ANALYSIS")
    print("=" * 50)
    print(f"Total connections: {len(all_connections)}")
    print(f"Top 10 connections:")
    print("-" * 30)
    
    for i, (_, row) in enumerate(connections.head(10).iterrows(), 1):
        connected_char = row['connected_to']
        weight = row['weight']
        house = CHARACTER_HOUSES.get(connected_char, 'unknown')
        print(f"{i:2d}. {connected_char:15s} | {weight:8.0f} | {house}")
    
    # Calculate some statistics
    weights = all_connections['weight'].values
    print(f"\nConnection Statistics:")
    print(f"  Strongest connection: {weights.max():.0f}")
    print(f"  Weakest connection: {weights.min():.0f}")
    print(f"  Average connection: {weights.mean():.0f}")
    print(f"  Median connection: {np.median(weights):.0f}")
    
    return connections

def calculate_network_similarity(char1_connections, char2_connections):
    """Calculate Jaccard similarity between two character networks."""
    set1 = set(char1_connections['connected_to'].tolist())
    set2 = set(char2_connections['connected_to'].tolist())
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0

def calculate_expected_connection(network_similarity, char1_avg_weight, char2_avg_weight):
    """Calculate expected connection strength based on network similarity and character importance."""
    # Use a more sophisticated approach that considers:
    # 1. Network similarity (how much their social circles overlap)
    # 2. Character importance (average connection strength)
    # 3. Non-linear scaling for more realistic expectations
    
    # Base expected connection from character importance
    base_expected = (char1_avg_weight + char2_avg_weight) / 2
    
    # Non-linear scaling based on network similarity
    # Low similarity (0.0-0.3): 5-20% of base
    # Medium similarity (0.3-0.7): 20-60% of base  
    # High similarity (0.7-1.0): 60-100% of base
    
    if network_similarity < 0.3:
        # Very different social circles
        similarity_factor = 0.05 + (network_similarity / 0.3) * 0.15  # 5-20%
    elif network_similarity < 0.7:
        # Moderately different social circles
        similarity_factor = 0.20 + ((network_similarity - 0.3) / 0.4) * 0.40  # 20-60%
    else:
        # Similar social circles
        similarity_factor = 0.60 + ((network_similarity - 0.7) / 0.3) * 0.40  # 60-100%
    
    expected_connection = base_expected * similarity_factor
    
    return expected_connection

def find_surprising_connections(edges_file, top_n=3):
    """Find the most surprising character connections based on network similarity."""
    print("\n" + "=" * 60)
    print("SURPRISING CONNECTIONS ANALYSIS")
    print("=" * 60)
    
    df = load_edges_data(edges_file)
    
    # Get all unique characters
    all_chars = sorted(set(df['char_a'].unique()) | set(df['char_b'].unique()))
    
    # Define the trio to exclude from direct analysis
    trio = {"harry", "ron", "hermione"}
    non_trio_chars = [char for char in all_chars if char not in trio]
    
    print(f"Analyzing {len(all_chars)} total characters...")
    print(f"Excluding trio from direct analysis: {len(non_trio_chars)} characters")
    
    # Pre-calculate each character's top 10 connections and average weight
    # Include ALL characters (including trio) for network similarity calculations
    char_networks = {}
    char_avg_weights = {}
    
    for char in all_chars:
        connections, all_connections = get_character_connections(df, char, top_n=10)
        if connections is not None and len(connections) > 0:
            char_networks[char] = connections
            char_avg_weights[char] = all_connections['weight'].mean()
    
    print(f"Found networks for {len(char_networks)} characters")
    
    # Calculate surprise scores for non-trio character pairs only
    surprise_scores = []
    
    for i, char1 in enumerate(non_trio_chars):
        if char1 not in char_networks:
            continue
            
        for j, char2 in enumerate(non_trio_chars):
            if i >= j or char2 not in char_networks:  # Avoid duplicates and missing chars
                continue
            
            # Get actual connection strength
            actual_connection = df[
                ((df['char_a'] == char1) & (df['char_b'] == char2)) |
                ((df['char_a'] == char2) & (df['char_b'] == char1))
            ]
            
            if actual_connection.empty:
                continue
                
            actual_weight = actual_connection['weight'].iloc[0]
            
            # Skip if no actual connection (weight = 0 or very small)
            # Use a small threshold to catch very small weights that might be effectively zero
            if actual_weight <= 0.1:
                continue
            
            # Calculate network similarity
            network_similarity = calculate_network_similarity(
                char_networks[char1], char_networks[char2]
            )
            
            # Calculate expected connection
            expected_weight = calculate_expected_connection(
                network_similarity, 
                char_avg_weights[char1], 
                char_avg_weights[char2]
            )
            
            # Calculate surprise score (actual / expected)
            if expected_weight > 0:
                surprise_score = actual_weight / expected_weight
            else:
                surprise_score = float('inf') if actual_weight > 0 else 0
            
            # Calculate relative surprise (how much above/below expected)
            relative_surprise = (actual_weight - expected_weight) / expected_weight if expected_weight > 0 else 0
            
            surprise_scores.append({
                'char1': char1,
                'char2': char2,
                'actual_weight': actual_weight,
                'expected_weight': expected_weight,
                'network_similarity': network_similarity,
                'surprise_score': surprise_score,
                'relative_surprise': relative_surprise
            })
    
    # Separate HIGH and LOW surprises
    high_surprises = [s for s in surprise_scores if s['relative_surprise'] > 0]
    low_surprises = [s for s in surprise_scores if s['relative_surprise'] < 0]
    
    # Sort each type
    high_surprises.sort(key=lambda x: x['relative_surprise'], reverse=True)
    low_surprises.sort(key=lambda x: x['relative_surprise'])  # Most negative first
    
    print(f"\nFound {len(surprise_scores)} character pairs with connections")
    print(f"  - {len(high_surprises)} surprisingly HIGH connections")
    print(f"  - {len(low_surprises)} surprisingly LOW connections")
    
    print(f"\nTOP {top_n} SURPRISINGLY HIGH CONNECTIONS:")
    print("-" * 80)
    
    for i, result in enumerate(high_surprises[:top_n], 1):
        char1, char2 = result['char1'], result['char2']
        actual = result['actual_weight']
        expected = result['expected_weight']
        similarity = result['network_similarity']
        surprise = result['surprise_score']
        relative = result['relative_surprise']
        
        print(f"{i}. {char1.upper()} ↔ {char2.upper()}")
        print(f"   Actual: {actual:8.2f} | Expected: {expected:8.2f} | Surprise: {surprise:.2f}x")
        print(f"   Network Similarity: {similarity:.3f} | Relative Surprise: {relative:+.1%}")
        print()
    
    print(f"\nTOP 10 SURPRISINGLY LOW CONNECTIONS:")
    print("-" * 80)
    
    for i, result in enumerate(low_surprises[:10], 1):
        char1, char2 = result['char1'], result['char2']
        actual = result['actual_weight']
        expected = result['expected_weight']
        similarity = result['network_similarity']
        surprise = result['surprise_score']
        relative = result['relative_surprise']
        
        print(f"{i}. {char1.upper()} ↔ {char2.upper()}")
        print(f"   Actual: {actual:8.2f} | Expected: {expected:8.2f} | Surprise: {surprise:.2f}x")
        print(f"   Network Similarity: {similarity:.3f} | Relative Surprise: {relative:+.1%}")
        print()
    
    return high_surprises[:top_n] + low_surprises[:top_n]

def main():
    """Main function to generate character-specific heatmaps."""
    print("Character-Specific Heatmap Analysis")
    print("=" * 40)
    
    # Check if edges file exists
    edges_file = "Artifacts/edges_kernel.csv"
    if not os.path.exists(edges_file):
        print(f"ERROR: Edges file not found: {edges_file}")
        print("Please run the pipeline first: py -3 -m character_network.pipeline")
        return
    
    # Characters to analyze
    characters_to_analyze = ["hagrid", "ginny"]
    
    print(f"Analyzing characters: {', '.join(characters_to_analyze)}")
    print()
    
    # Create output directory
    output_dir = "Artifacts/Character_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Analyze each character
    for char in characters_to_analyze:
        print(f"Analyzing {char}...")
        
        # Get connections
        connections, all_connections = get_character_connections(load_edges_data(edges_file), char, top_n=10)
        
        if connections is not None:
            # Create individual heatmap
            out_file = os.path.join(output_dir, f"{char}_connections_heatmap.png")
            create_character_heatmap(char, connections, out_png=out_file, show=False)
            
            # Print analysis
            analyze_character_network(char, edges_file)
        else:
            print(f"No connections found for {char}")
    
    # Create comparison heatmap
    print(f"\nCreating comparison heatmap...")
    comparison_file = os.path.join(output_dir, "hagrid_ginny_comparison.png")
    create_comparison_heatmap(characters_to_analyze, edges_file, out_png=comparison_file, show=False)
    
    # Find surprising connections
    surprising_connections = find_surprising_connections(edges_file, top_n=3)
    
    print(f"\nAnalysis complete! Files saved to: {output_dir}/")
    print("Generated files:")
    for char in characters_to_analyze:
        print(f"  - {char}_connections_heatmap.png")
    print("  - hagrid_ginny_comparison.png")
    print("\nSurprising connections analysis completed!")

if __name__ == "__main__":
    main()
