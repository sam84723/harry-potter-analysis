import os
import argparse
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from frequency_analysis_constants import CHARACTER_HOUSES, MAIN_CHARACTERS
from .graph_analysis import (
    community_spring_layout, 
    detect_communities, 
    analyze_communities,
    print_community_analysis,
    print_network_metrics,
    create_community_visualization
)


def get_house_colors():
    """Return house color mapping for visualization."""
    return {
        'gryffindor': '#DC143C',      # Crimson red
        'slytherin': '#2F4F2F',       # Dark green
        'ravenclaw': '#4169E1',       # Royal blue
        'hufflepuff': '#DAA520',      # Goldenrod
        'unknown': '#808080'          # Gray for unknown/no house
    }


def apply_minimum_distance(pos, min_distance=0.3):
    """Apply minimum distance constraint to prevent overlapping nodes."""
    import numpy as np
    
    positions = list(pos.values())
    n_nodes = len(positions)
    
    if n_nodes < 2:
        return pos
    
    # Convert to numpy array for easier manipulation
    pos_array = np.array(positions)
    
    # Iteratively adjust positions to maintain minimum distance
    max_iterations = 50
    for iteration in range(max_iterations):
        moved = False
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                # Calculate distance between nodes i and j
                dist = np.linalg.norm(pos_array[i] - pos_array[j])
                
                if dist < min_distance:
                    # Move nodes apart
                    direction = pos_array[i] - pos_array[j]
                    if np.linalg.norm(direction) > 0:
                        direction = direction / np.linalg.norm(direction)
                        move_distance = (min_distance - dist) / 2
                        pos_array[i] += direction * move_distance
                        pos_array[j] -= direction * move_distance
                        moved = True
        
        if not moved:
            break
    
    # Update the position dictionary
    for i, node in enumerate(pos.keys()):
        pos[node] = (pos_array[i][0], pos_array[i][1])
    
    return pos




def plot_house_colored_graph(edges_csv: str, top_n: int = 200, out_png: str = None, show: bool = True, layout: str = "auto", min_distance: float = 0.4, main_only: bool = False, filter_percent: float = None) -> None:
    """Plot character network with nodes colored by house."""
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    # Filter to main characters if requested
    if main_only:
        main_chars_set = set(MAIN_CHARACTERS)
        df = df[
            (df['char_a'].isin(main_chars_set)) & 
            (df['char_b'].isin(main_chars_set))
        ]
        if df.empty:
            print("No edges found between main characters")
            return

    # Apply edge filtering if requested
    if filter_percent is not None:
        # For each character, keep only their top connections
        all_chars = set(df['char_a'].unique()) | set(df['char_b'].unique())
        filtered_edges = []
        
        for char in all_chars:
            # Get all edges for this character
            char_edges = df[(df['char_a'] == char) | (df['char_b'] == char)].copy()
            
            if len(char_edges) > 0:
                # Sort by weight and keep top X%
                char_edges = char_edges.sort_values('weight', ascending=False)
                keep_count = max(1, int(len(char_edges) * filter_percent))
                filtered_edges.append(char_edges.head(keep_count))
        
        if filtered_edges:
            df = pd.concat(filtered_edges).drop_duplicates()
        else:
            df = pd.DataFrame()
        
        if df.empty:
            print("No edges after filtering")
            return

    df = df.sort_values("weight", ascending=False).head(top_n)

    G = nx.Graph()
    for _, r in df.iterrows():
        G.add_edge(r['char_a'], r['char_b'], weight=r['weight'])

    if G.number_of_nodes() == 0:
        print("No nodes in graph")
        return

    # Create layout with better spacing
    if layout == "auto":
        # Try multiple layout algorithms and pick the best one
        layouts = {}
        
        # Spring layout with better parameters
        layouts['spring'] = nx.spring_layout(G, k=2.0, iterations=100, seed=42)
        
        # Kamada-Kawai layout (good for small-medium graphs)
        if G.number_of_nodes() < 100:
            try:
                layouts['kamada'] = nx.kamada_kawai_layout(G, scale=2)
            except:
                pass
        
        # Circular layout as fallback
        layouts['circular'] = nx.circular_layout(G, scale=2)
        
        # Choose the best layout (spring is usually good)
        pos = layouts['spring']
        
        # If spring layout is too clustered, try circular
        if G.number_of_nodes() > 20:
            # Check if nodes are too clustered in spring layout
            positions = list(pos.values())
            if positions:
                x_coords = [p[0] for p in positions]
                y_coords = [p[1] for p in positions]
                x_range = max(x_coords) - min(x_coords)
                y_range = max(y_coords) - min(y_coords)
                
                # If the layout is too compact, use circular
                if x_range < 1.5 or y_range < 1.5:
                    pos = layouts['circular']
    else:
        # Manual layout selection
        if layout == "spring":
            pos = nx.spring_layout(G, k=2.0, iterations=100, seed=42)
        elif layout == "circular":
            pos = nx.circular_layout(G, scale=2)
        elif layout == "kamada" and G.number_of_nodes() < 100:
            pos = nx.kamada_kawai_layout(G, scale=2)
        elif layout == "community":
            pos = community_spring_layout(G, k=2.0, iterations=100, scale=2)
        else:
            pos = nx.spring_layout(G, k=2.0, iterations=100, seed=42)

    # Get house colors
    house_colors = get_house_colors()
    
    # Color nodes by house
    node_colors = []
    house_counts = {'gryffindor': 0, 'slytherin': 0, 'ravenclaw': 0, 'hufflepuff': 0, 'unknown': 0}
    
    for node in G.nodes():
        house = CHARACTER_HOUSES.get(node, 'unknown')
        node_colors.append(house_colors[house])
        house_counts[house] += 1

    # Draw the graph
    fig, ax = plt.subplots(figsize=(15, 12))
    
    # Draw edges with better visibility
    if G.number_of_edges() > 0:
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        
        # Better edge scaling: ensure all edges are visible
        if len(set(weights)) > 1:  # If there are different weights
            min_weight, max_weight = min(weights), max(weights)
            # Scale from 0.5 to 4.0, ensuring minimum visibility
            edge_widths = [0.5 + 3.5 * (w - min_weight) / (max_weight - min_weight) for w in weights]
        else:  # If all weights are the same
            edge_widths = [2.0] * len(weights)
        
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7, edge_color='#666666', ax=ax)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, alpha=0.8, ax=ax)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

    # Create legend
    legend_elements = []
    for house, color in house_colors.items():
        if house_counts[house] > 0:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=10, 
                                            label=f'{house.title()} ({house_counts[house]})'))
    
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.title("Character Network - Colored by House", fontsize=16, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def plot_main_characters_graph(edges_csv: str, out_png: str = None, show: bool = True, min_distance: float = 0.3, filter_percent: float = None) -> None:
    """Plot character network with only main characters, using Kamada-Kawai layout."""
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    # Filter to only include edges between main characters
    main_chars_set = set(MAIN_CHARACTERS)
    main_edges = df[
        (df['char_a'].isin(main_chars_set)) & 
        (df['char_b'].isin(main_chars_set))
    ]
    
    if main_edges.empty:
        print("No edges found between main characters")
        return

    # Apply edge filtering if requested
    if filter_percent is not None:
        # For each character, keep only their top connections
        all_chars = set(main_edges['char_a'].unique()) | set(main_edges['char_b'].unique())
        filtered_edges = []
        
        for char in all_chars:
            # Get all edges for this character
            char_edges = main_edges[(main_edges['char_a'] == char) | (main_edges['char_b'] == char)].copy()
            
            if len(char_edges) > 0:
                # Sort by weight and keep top X%
                char_edges = char_edges.sort_values('weight', ascending=False)
                keep_count = max(1, int(len(char_edges) * filter_percent))
                filtered_edges.append(char_edges.head(keep_count))
        
        if filtered_edges:
            main_edges = pd.concat(filtered_edges).drop_duplicates()
        else:
            main_edges = pd.DataFrame()
        
        if main_edges.empty:
            print("No edges after filtering")
            return

    G = nx.Graph()
    for _, r in main_edges.iterrows():
        G.add_edge(r['char_a'], r['char_b'], weight=r['weight'])

    if G.number_of_nodes() == 0:
        print("No main character nodes in graph")
        return

    # Use Kamada-Kawai layout (good for small graphs) with better spacing
    try:
        pos = nx.kamada_kawai_layout(G, scale=4)  # Increased scale
    except:
        # Fallback to spring layout if Kamada-Kawai fails
        pos = nx.spring_layout(G, k=3.0, iterations=200, seed=42)  # Increased k and iterations
    
    # Apply minimum distance constraint to prevent overlapping nodes
    pos = apply_minimum_distance(pos, min_distance=min_distance)

    # Get house colors
    house_colors = get_house_colors()
    
    # Color nodes by house
    node_colors = []
    house_counts = {'gryffindor': 0, 'slytherin': 0, 'ravenclaw': 0, 'hufflepuff': 0, 'unknown': 0}
    
    for node in G.nodes():
        house = CHARACTER_HOUSES.get(node, 'unknown')
        node_colors.append(house_colors[house])
        house_counts[house] += 1

    # Draw the graph
    plt.figure(figsize=(12, 10))
    
    # Draw edges with better visibility
    if G.number_of_edges() > 0:
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        
        # Better edge scaling: ensure all edges are visible
        if len(set(weights)) > 1:  # If there are different weights
            min_weight, max_weight = min(weights), max(weights)
            # Scale from 1.0 to 5.0, ensuring good visibility for main characters
            edge_widths = [1.0 + 4.0 * (w - min_weight) / (max_weight - min_weight) for w in weights]
        else:  # If all weights are the same
            edge_widths = [3.0] * len(weights)
        
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.8, edge_color='#444444')

    # Draw nodes (larger for main characters)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, alpha=0.9)
    
    # Draw labels (larger font for main characters)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Create legend
    legend_elements = []
    for house, color in house_colors.items():
        if house_counts[house] > 0:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=12, 
                                            label=f'{house.title()} ({house_counts[house]})'))
    
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.title("Main Characters Network - Colored by House", fontsize=16, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def plot_all_characters_graph(edges_csv: str, out_png: str = None, show: bool = True, min_distance: float = 0.2, filter_percent: float = None) -> None:
    """Plot character network with ALL characters (no edge filtering)."""
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    # Apply edge filtering if requested
    if filter_percent is not None:
        # For each character, keep only their top connections
        all_chars = set(df['char_a'].unique()) | set(df['char_b'].unique())
        filtered_edges = []
        
        for char in all_chars:
            # Get all edges for this character
            char_edges = df[(df['char_a'] == char) | (df['char_b'] == char)].copy()
            
            if len(char_edges) > 0:
                # Sort by weight and keep top X%
                char_edges = char_edges.sort_values('weight', ascending=False)
                keep_count = max(1, int(len(char_edges) * filter_percent))
                filtered_edges.append(char_edges.head(keep_count))
        
        if filtered_edges:
            df = pd.concat(filtered_edges).drop_duplicates()
        else:
            df = pd.DataFrame()
        
        if df.empty:
            print("No edges after filtering")
            return

    # Use ALL edges, not just top_n
    G = nx.Graph()
    for _, r in df.iterrows():
        G.add_edge(r['char_a'], r['char_b'], weight=r['weight'])

    if G.number_of_nodes() == 0:
        print("No nodes in graph")
        return

    print(f"Total characters in graph: {G.number_of_nodes()}")
    print(f"Total edges in graph: {G.number_of_edges()}")

    # Use circular layout for better distribution of many characters
    pos = nx.circular_layout(G, scale=3)  # Increased scale
    
    # Apply minimum distance constraint to prevent overlapping nodes
    pos = apply_minimum_distance(pos, min_distance=min_distance)  # Smaller min distance for circular layout

    # Get house colors
    house_colors = get_house_colors()
    
    # Color nodes by house
    node_colors = []
    house_counts = {'gryffindor': 0, 'slytherin': 0, 'ravenclaw': 0, 'hufflepuff': 0, 'unknown': 0}
    
    for node in G.nodes():
        house = CHARACTER_HOUSES.get(node, 'unknown')
        node_colors.append(house_colors[house])
        house_counts[house] += 1

    # Draw the graph
    plt.figure(figsize=(16, 14))
    
    # Draw edges with better visibility
    if G.number_of_edges() > 0:
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        
        # Better edge scaling: ensure all edges are visible
        if len(set(weights)) > 1:  # If there are different weights
            min_weight, max_weight = min(weights), max(weights)
            # Scale from 0.3 to 2.0 for many edges
            edge_widths = [0.3 + 1.7 * (w - min_weight) / (max_weight - min_weight) for w in weights]
        else:  # If all weights are the same
            edge_widths = [1.0] * len(weights)
        
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color='#888888')

    # Draw nodes (smaller for many characters)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=200, alpha=0.8)
    
    # Draw labels (smaller font for many characters)
    nx.draw_networkx_labels(G, pos, font_size=6)

    # Create legend
    legend_elements = []
    for house, color in house_colors.items():
        if house_counts[house] > 0:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=10, 
                                            label=f'{house.title()} ({house_counts[house]})'))
    
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.title("All Characters Network - Colored by House", fontsize=16, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def plot_filtered_graph(edges_csv: str, cutoff_percent: float = 0.3, main_only: bool = False, out_png: str = None, show: bool = True, layout: str = "auto", min_distance: float = 0.4) -> None:
    """Plot character network with filtered edges (top X% for each node)."""
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    # Filter to main characters if requested
    if main_only:
        main_chars_set = set(MAIN_CHARACTERS)
        df = df[
            (df['char_a'].isin(main_chars_set)) & 
            (df['char_b'].isin(main_chars_set))
        ]
        if df.empty:
            print("No edges found between main characters")
            return

    # Get all unique characters
    all_chars = set(df['char_a'].unique()) | set(df['char_b'].unique())
    
    # For each character, keep only their top connections
    filtered_edges = []
    
    for char in all_chars:
        # Get all edges for this character
        char_edges = df[(df['char_a'] == char) | (df['char_b'] == char)].copy()
        
        if len(char_edges) > 0:
            # Sort by weight and keep top X%
            char_edges = char_edges.sort_values('weight', ascending=False)
            keep_count = max(1, int(len(char_edges) * cutoff_percent))
            filtered_edges.append(char_edges.head(keep_count))
    
    if filtered_edges:
        filtered_df = pd.concat(filtered_edges).drop_duplicates()
    else:
        filtered_df = pd.DataFrame()
    
    if filtered_df.empty:
        print("No edges after filtering")
        return

    print(f"Original edges: {len(df)}")
    print(f"Filtered edges: {len(filtered_df)}")
    print(f"Reduction: {len(df) - len(filtered_df)} edges removed")

    G = nx.Graph()
    for _, r in filtered_df.iterrows():
        G.add_edge(r['char_a'], r['char_b'], weight=r['weight'])

    if G.number_of_nodes() == 0:
        print("No nodes in graph")
        return

    # Create layout with better spacing
    if layout == "auto":
        if G.number_of_nodes() < 50:
            try:
                pos = nx.kamada_kawai_layout(G, scale=4)  # Increased scale
            except:
                pos = nx.spring_layout(G, k=3.0, iterations=200, seed=42)  # Increased k and iterations
        else:
            pos = nx.spring_layout(G, k=3.0, iterations=200, seed=42)  # Increased k and iterations
    elif layout == "spring":
        pos = nx.spring_layout(G, k=3.0, iterations=200, seed=42)  # Increased k and iterations
    elif layout == "circular":
        pos = nx.circular_layout(G, scale=3)  # Increased scale
    elif layout == "kamada" and G.number_of_nodes() < 100:
        pos = nx.kamada_kawai_layout(G, scale=4)  # Increased scale
    else:
        pos = nx.spring_layout(G, k=3.0, iterations=200, seed=42)  # Increased k and iterations
    
    # Apply minimum distance constraint to prevent overlapping nodes
    pos = apply_minimum_distance(pos, min_distance=min_distance)

    # Get house colors
    house_colors = get_house_colors()
    
    # Color nodes by house
    node_colors = []
    house_counts = {'gryffindor': 0, 'slytherin': 0, 'ravenclaw': 0, 'hufflepuff': 0, 'unknown': 0}
    
    for node in G.nodes():
        house = CHARACTER_HOUSES.get(node, 'unknown')
        node_colors.append(house_colors[house])
        house_counts[house] += 1

    # Draw the graph
    plt.figure(figsize=(14, 12))
    
    # Draw edges with better visibility
    if G.number_of_edges() > 0:
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        
        # Better edge scaling: ensure all edges are visible
        if len(set(weights)) > 1:  # If there are different weights
            min_weight, max_weight = min(weights), max(weights)
            # Scale from 1.0 to 4.0 for filtered edges
            edge_widths = [1.0 + 3.0 * (w - min_weight) / (max_weight - min_weight) for w in weights]
        else:  # If all weights are the same
            edge_widths = [2.5] * len(weights)
        
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7, edge_color='#555555')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=400, alpha=0.8)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Create legend
    legend_elements = []
    for house, color in house_colors.items():
        if house_counts[house] > 0:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=10, 
                                            label=f'{house.title()} ({house_counts[house]})'))
    
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # Dynamic title based on options
    char_type = "Main Characters" if main_only else "All Characters"
    plt.title(f"Filtered {char_type} Network - Top {int(cutoff_percent*100)}% Edges per Node", fontsize=16, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def plot_correlation_matrix(edges_csv: str, main_only: bool = False, out_png: str = None, show: bool = True, show_values: bool = None) -> None:
    """Plot correlation matrix heatmap of character relationships."""
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    # Filter to main characters if requested
    if main_only:
        main_chars_set = set(MAIN_CHARACTERS)
        df = df[
            (df['char_a'].isin(main_chars_set)) & 
            (df['char_b'].isin(main_chars_set))
        ]
        if df.empty:
            print("No edges found between main characters")
            return

    # Get all unique characters
    all_chars = sorted(list(set(df['char_a'].unique()) | set(df['char_b'].unique())))
    
    # Create correlation matrix
    n_chars = len(all_chars)
    corr_matrix = np.zeros((n_chars, n_chars))
    
    # Fill the matrix
    for _, row in df.iterrows():
        i = all_chars.index(row['char_a'])
        j = all_chars.index(row['char_b'])
        corr_matrix[i][j] = row['weight']
        corr_matrix[j][i] = row['weight']  # Make symmetric
    
    # Create heatmap
    plt.figure(figsize=(16, 14))
    
    # Create color map
    im = plt.imshow(corr_matrix, cmap='YlOrRd', aspect='auto')
    
    # Set ticks
    plt.xticks(range(n_chars), all_chars, rotation=45, ha='right')
    plt.yticks(range(n_chars), all_chars)
    
    # Add colorbar
    cbar = plt.colorbar(im, shrink=0.8)
    cbar.set_label('Relationship Strength', rotation=270, labelpad=20)
    
    # Add values to cells if requested
    if show_values is None:
        # Auto-decide: show values for smaller matrices (≤20 characters)
        show_values = n_chars <= 20
    
    if show_values:
        for i in range(n_chars):
            for j in range(n_chars):
                if corr_matrix[i][j] > 0:
                    plt.text(j, i, f'{corr_matrix[i][j]:.1f}', 
                            ha='center', va='center', fontsize=8)
    
    char_type = "Main Characters" if main_only else "All Characters"
    plt.title(f'{char_type} Relationship Matrix', fontsize=16, fontweight='bold')
    plt.xlabel('Characters')
    plt.ylabel('Characters')
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def plot_npmi_graph(edges_csv: str, top_n: int = 200, out_png: str = None, show: bool = True) -> None:
    """Plot NPMI-weighted character network graph."""
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    df = df.sort_values("weight", ascending=False).head(top_n)

    G = nx.Graph()
    for _, r in df.iterrows():
        G.add_edge(r.char_a, r.char_b, weight=float(r.weight))

    pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42)  # Spring layout (force-directed)
    # pos = nx.circular_layout(G)  # Circular layout
    weights = [d['weight'] for _, _, d in G.edges(data=True)]
    wmin, wmax = min(weights), max(weights)
    wscaled = [0.5 + 4 * (w - wmin) / (wmax - wmin + 1e-9) for w in weights]
    offset = 1.0  # increase all edges by 1 px
    wscaled = [w + offset for w in wscaled]

    plt.figure(figsize=(12, 9))
    
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="#E74C3C")  # Red nodes for NPMI
    nx.draw_networkx_edges(G, pos, width=wscaled, edge_color="#555", alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title("Character Network - NPMI Scoring", fontsize=16, fontweight='bold')
    plt.axis("off")
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:  # Only create directory if there's a directory component
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def plot_kernel_graph(edges_csv: str, top_n: int = 200, out_png: str = None, show: bool = True) -> None:
    if not os.path.exists(edges_csv):
        raise FileNotFoundError(f"Edges CSV not found: {edges_csv}")

    df = pd.read_csv(edges_csv)
    if df.empty:
        raise ValueError("Edges CSV is empty")

    df = df.sort_values("weight", ascending=False).head(top_n)

    G = nx.Graph()
    for _, r in df.iterrows():
        G.add_edge(r.char_a, r.char_b, weight=float(r.weight))

    pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42)  # Spring layout (force-directed)
    # pos = nx.circular_layout(G)  # Circular layout
    weights = [d['weight'] for _, _, d in G.edges(data=True)]
    wmin, wmax = min(weights), max(weights)
    wscaled = [0.5 + 4 * (w - wmin) / (wmax - wmin + 1e-9) for w in weights]
    offset = 1.0  # increase all edges by 1 px
    wscaled = [w + offset for w in wscaled]

    plt.figure(figsize=(12, 9))
    
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="#5DADE2")
    nx.draw_networkx_edges(G, pos, width=wscaled, edge_color="#555", alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.axis("off")
    plt.tight_layout()

    if out_png:
        output_dir = os.path.dirname(out_png)
        if output_dir:  # Only create directory if there's a directory component
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Plot character network graphs")
    parser.add_argument("--edges", default=os.path.join("Artifacts", "edges_kernel.csv"))
    parser.add_argument("--type", choices=["main", "all", "matrix", "communities"], default="main", 
                       help="graph type: main (main characters only), all (all characters), matrix (correlation heatmap), or communities (community analysis)")
    parser.add_argument("--weighting", choices=["kernel", "npmi"], default="kernel",
                       help="edge weighting method: kernel (Gaussian) or npmi (Normalized Pointwise Mutual Information)")
    parser.add_argument("--house-colors", action="store_true",
                       help="color nodes by Hogwarts house (Gryffindor, Slytherin, etc.)")
    parser.add_argument("--top", type=int, default=200,
                       help="maximum number of edges to display")
    parser.add_argument("--layout", choices=["auto", "spring", "circular", "kamada", "community"], default="auto",
                       help="layout algorithm: auto, spring, circular, kamada, or community")
    parser.add_argument("--filter", type=float, default=None,
                       help="filter edges: keep only top X%% of edges per node (0.1-1.0, e.g., 0.3 for top 30%%)")
    parser.add_argument("--min-distance", type=float, default=0.3,
                       help="minimum distance between nodes to prevent overlapping (0.1-1.0)")
    parser.add_argument("--main-only", action="store_true",
                       help="for matrix: show only main characters")
    parser.add_argument("--show-values", action="store_true",
                       help="for matrix: show values in heatmap cells")
    parser.add_argument("--no-values", action="store_true",
                       help="for matrix: hide values in heatmap cells")
    parser.add_argument("--algorithm", choices=["louvain", "label_propagation", "greedy_modularity"], 
                       default="louvain", help="community detection algorithm")
    parser.add_argument("--no-labels", action="store_true",
                       help="for communities: hide character labels on nodes")
    parser.add_argument("--out", default="", help="optional PNG output path")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    out_png = args.out if args.out else None
    
    # Determine which edges file to use based on weighting
    if args.weighting == "npmi":
        edges_file = os.path.join("Artifacts", "edges_npmi.csv")
    else:  # kernel
        edges_file = args.edges
    
    # Handle matrix type (correlation heatmap)
    if args.type == "matrix":
        # Determine show_values based on arguments
        show_values = None  # Auto-decide by default
        if args.show_values and args.no_values:
            print("Warning: Both --show-values and --no-values specified. Using --show-values.")
            show_values = True
        elif args.show_values:
            show_values = True
        elif args.no_values:
            show_values = False
        
        plot_correlation_matrix(edges_file, main_only=args.main_only, out_png=out_png, 
                              show=(not args.no_show), show_values=show_values)
    
    # Handle communities type (community analysis)
    elif args.type == "communities":
        # Load graph from edges
        df = pd.read_csv(edges_file)
        if df.empty:
            raise ValueError("Edges CSV is empty")
        
        G = nx.Graph()
        for _, r in df.iterrows():
            G.add_edge(r['char_a'], r['char_b'], weight=r['weight'])
        
        if G.number_of_nodes() == 0:
            print("No nodes in graph")
            return
        
        # Perform community analysis
        analysis_results = analyze_communities(G, method=args.algorithm)
        if analysis_results is None:
            print("Community analysis failed")
            return
        
        # Print results
        print_community_analysis(analysis_results)
        
        # Create visualization
        create_community_visualization(G, analysis_results['communities'], 
                                     out_png=out_png, show=(not args.no_show), 
                                     show_labels=(not args.no_labels))
    
    # Handle graph types (main or all)
    elif args.type == "main":
        if args.house_colors:
            plot_house_colored_graph(edges_file, top_n=args.top, out_png=out_png, show=(not args.no_show), 
                                   layout=args.layout, min_distance=args.min_distance, 
                                   main_only=True, filter_percent=args.filter)
        else:
            plot_main_characters_graph(edges_file, out_png=out_png, show=(not args.no_show), 
                                     min_distance=args.min_distance, filter_percent=args.filter)
    
    elif args.type == "all":
        if args.house_colors:
            plot_house_colored_graph(edges_file, top_n=args.top, out_png=out_png, show=(not args.no_show), 
                                   layout=args.layout, min_distance=args.min_distance, 
                                   main_only=False, filter_percent=args.filter)
        else:
            plot_all_characters_graph(edges_file, out_png=out_png, show=(not args.no_show), 
                                    min_distance=args.min_distance, filter_percent=args.filter)


if __name__ == "__main__":
    main()


