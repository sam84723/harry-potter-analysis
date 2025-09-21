
"""
Graph Analysis Algorithms
========================

This module contains algorithms for analyzing character networks,
including community detection, layout algorithms, and network metrics.

Usage:
    from character_network.graph_analysis import detect_communities, community_spring_layout
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from frequency_analysis_constants import CHARACTER_HOUSES, MAIN_CHARACTERS

# Community detection algorithms
try:
    import networkx.algorithms.community as nx_comm
    COMMUNITY_AVAILABLE = True
except ImportError:
    COMMUNITY_AVAILABLE = False


def community_spring_layout(G, communities=None, k=1, iterations=50, scale=1):
    """
    Spring layout with community-aware positioning.
    
    This layout algorithm groups nodes by community while maintaining
    the force-directed properties of spring layout.
    
    Args:
        G: NetworkX graph
        communities: Dictionary mapping community names to lists of nodes, or list of communities.
                    If None, uses house information as communities.
        k: Optimal distance between nodes (spring layout parameter)
        iterations: Number of iterations for spring layout
        scale: Scale factor for the layout
        
    Returns:
        Dictionary mapping nodes to (x, y) positions
    """
    if communities is None:
        # Use house information as communities
        communities = {}
        for node in G.nodes():
            house = CHARACTER_HOUSES.get(node, 'unknown')
            if house not in communities:
                communities[house] = []
            communities[house].append(node)
    elif isinstance(communities, list):
        # Convert list of communities to dictionary format
        communities_dict = {}
        for i, community in enumerate(communities):
            communities_dict[f'community_{i}'] = list(community)
        communities = communities_dict
    
    # Get base spring layout
    pos = nx.spring_layout(G, k=k, iterations=iterations, scale=scale)
    
    # Adjust positions to group communities
    community_centers = {}
    for community, nodes in communities.items():
        if len(nodes) > 0:
            # Calculate community center
            community_pos = [pos[node] for node in nodes]
            center_x = np.mean([p[0] for p in community_pos])
            center_y = np.mean([p[1] for p in community_pos])
            community_centers[community] = (center_x, center_y)
    
    # Arrange communities in a circle
    if len(community_centers) > 1:
        community_names = list(community_centers.keys())
        n_communities = len(community_names)
        
        # Calculate positions for community centers in a circle
        for i, community in enumerate(community_names):
            angle = 2 * np.pi * i / n_communities
            radius = scale * 1.5  # Distance from center
            center_x = radius * np.cos(angle)
            center_y = radius * np.sin(angle)
            
            # Move all nodes in this community relative to their new center
            old_center = community_centers[community]
            offset_x = center_x - old_center[0]
            offset_y = center_y - old_center[1]
            
            for node in communities[community]:
                if node in pos:
                    pos[node] = (pos[node][0] + offset_x, pos[node][1] + offset_y)
    
    return pos


def detect_communities(G, method='louvain'):
    """
    Detect communities in the graph using various algorithms.
    
    Args:
        G: NetworkX graph
        method: Community detection method ('louvain', 'label_propagation', 'greedy_modularity')
        
    Returns:
        List of communities (each community is a set of nodes), or None if detection fails
    """
    if not COMMUNITY_AVAILABLE:
        print("Community detection not available. Install networkx with community algorithms.")
        return None
    
    if method == 'louvain':
        try:
            communities = nx_comm.louvain_communities(G, weight='weight')
            return list(communities)
        except:
            print("Louvain algorithm failed, trying label propagation...")
            method = 'label_propagation'
    
    if method == 'label_propagation':
        try:
            communities = nx_comm.label_propagation_communities(G)
            return list(communities)
        except:
            print("Label propagation failed, trying greedy modularity...")
            method = 'greedy_modularity'
    
    if method == 'greedy_modularity':
        try:
            communities = nx_comm.greedy_modularity_communities(G, weight='weight')
            return list(communities)
        except:
            print("All community detection methods failed.")
            return None
    
    return None


def calculate_network_metrics(G):
    """
    Calculate various network metrics for the graph.
    
    Args:
        G: NetworkX graph
        
    Returns:
        Dictionary containing network metrics
    """
    metrics = {}
    
    # Basic metrics
    metrics['num_nodes'] = G.number_of_nodes()
    metrics['num_edges'] = G.number_of_edges()
    metrics['density'] = nx.density(G)
    
    # Connectivity metrics
    if nx.is_connected(G):
        metrics['diameter'] = nx.diameter(G)
        metrics['radius'] = nx.radius(G)
        metrics['average_path_length'] = nx.average_shortest_path_length(G, weight='weight')
    else:
        # For disconnected graphs, calculate for largest component
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        metrics['diameter'] = nx.diameter(subgraph)
        metrics['radius'] = nx.radius(subgraph)
        metrics['average_path_length'] = nx.average_shortest_path_length(subgraph, weight='weight')
        metrics['largest_component_size'] = len(largest_cc)
    
    # Centrality metrics
    if G.number_of_nodes() > 0:
        metrics['degree_centrality'] = nx.degree_centrality(G)
        metrics['betweenness_centrality'] = nx.betweenness_centrality(G, weight='weight')
        metrics['closeness_centrality'] = nx.closeness_centrality(G, distance='weight')
        
        # Find most central nodes
        metrics['most_central_degree'] = max(metrics['degree_centrality'].items(), key=lambda x: x[1])
        metrics['most_central_betweenness'] = max(metrics['betweenness_centrality'].items(), key=lambda x: x[1])
        metrics['most_central_closeness'] = max(metrics['closeness_centrality'].items(), key=lambda x: x[1])
    
    # Clustering
    metrics['average_clustering'] = nx.average_clustering(G, weight='weight')
    metrics['transitivity'] = nx.transitivity(G)
    
    return metrics


def analyze_communities(G, method='louvain'):
    """
    Comprehensive community analysis of the graph.
    
    Args:
        G: NetworkX graph
        method: Community detection method
        
    Returns:
        Dictionary containing community analysis results
    """
    results = {}
    
    # Detect communities
    communities = detect_communities(G, method=method)
    if communities is None:
        return None
    
    results['communities'] = communities
    results['num_communities'] = len(communities)
    results['method'] = method
    
    # Calculate modularity
    if COMMUNITY_AVAILABLE:
        try:
            results['modularity'] = nx_comm.modularity(G, communities, weight='weight')
        except:
            results['modularity'] = None
    
    # Analyze each community
    results['community_stats'] = []
    for i, community in enumerate(communities):
        community_subgraph = G.subgraph(community)
        stats = {
            'id': i + 1,
            'size': len(community),
            'density': nx.density(community_subgraph),
            'nodes': sorted(list(community))
        }
        
        # Add house information for each character
        stats['houses'] = {}
        for node in community:
            house = CHARACTER_HOUSES.get(node, 'unknown')
            if house not in stats['houses']:
                stats['houses'][house] = 0
            stats['houses'][house] += 1
        
        results['community_stats'].append(stats)
    
    return results


def print_community_analysis(analysis_results):
    """
    Print formatted community analysis results.
    
    Args:
        analysis_results: Results from analyze_communities()
    """
    if analysis_results is None:
        print("Community analysis failed")
        return
    
    print(f"\nCOMMUNITY ANALYSIS ({analysis_results['method'].upper()})")
    print("=" * 50)
    print(f"Number of communities found: {analysis_results['num_communities']}")
    
    if analysis_results['modularity'] is not None:
        print(f"Modularity: {analysis_results['modularity']:.3f}")
    
    for stats in analysis_results['community_stats']:
        print(f"\nCommunity {stats['id']} ({stats['size']} characters):")
        print(f"  Density: {stats['density']:.3f}")
        print(f"  House distribution: {stats['houses']}")
        print("  Characters:")
        for char in stats['nodes']:
            house = CHARACTER_HOUSES.get(char, 'unknown')
            print(f"    - {char} ({house})")


def print_network_metrics(metrics):
    """
    Print formatted network metrics.
    
    Args:
        metrics: Results from calculate_network_metrics()
    """
    print(f"\nNETWORK METRICS")
    print("=" * 30)
    print(f"Nodes: {metrics['num_nodes']}")
    print(f"Edges: {metrics['num_edges']}")
    print(f"Density: {metrics['density']:.3f}")
    print(f"Average clustering: {metrics['average_clustering']:.3f}")
    print(f"Transitivity: {metrics['transitivity']:.3f}")
    
    if 'largest_component_size' in metrics:
        print(f"Largest component: {metrics['largest_component_size']} nodes")
    
    print(f"Diameter: {metrics['diameter']}")
    print(f"Radius: {metrics['radius']}")
    print(f"Average path length: {metrics['average_path_length']:.3f}")
    
    print(f"\nMost central nodes:")
    print(f"  Degree: {metrics['most_central_degree'][0]} ({metrics['most_central_degree'][1]:.3f})")
    print(f"  Betweenness: {metrics['most_central_betweenness'][0]} ({metrics['most_central_betweenness'][1]:.3f})")
    print(f"  Closeness: {metrics['most_central_closeness'][0]} ({metrics['most_central_closeness'][1]:.3f})")


def create_community_visualization(G, communities, out_png=None, show=True, show_labels=True):
    """
    Create a visualization of the graph with communities highlighted.
    
    Args:
        G: NetworkX graph
        communities: List of communities (sets of nodes)
        out_png: Optional output PNG path
        show: Whether to display the plot
        show_labels: Whether to show character labels on nodes
    """
    plt.figure(figsize=(20, 16))
    
    # Use community layout
    pos = community_spring_layout(G, communities=communities, k=2.0, iterations=100, scale=2)
    
    # Color nodes by community
    colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
    node_colors = {}
    
    for i, community in enumerate(communities):
        for node in community:
            node_colors[node] = colors[i]
    
    # Draw the graph
    nx.draw_networkx_nodes(G, pos, 
                          node_color=[node_colors.get(node, 'gray') for node in G.nodes()],
                          node_size=200, alpha=0.8)
    
    # Draw edges with reduced opacity
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.5)
    
    # Add labels for all characters (if enabled)
    if show_labels:
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=6, font_weight='normal')
    
    plt.title(f'Character Network Communities', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

    if out_png:
        import os
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=300, bbox_inches='tight')
        print(f"Community visualization saved to: {out_png}")

    if show:
        plt.show()
    plt.close()


def create_publication_community_visualization(G, communities, out_png=None, show=True, 
                                            title="Character Network Communities",
                                            show_legend=True, figsize=(16, 12)):
    """
    Create a publication-ready community visualization with clean layout and legend.
    
    This function creates a professional visualization suitable for PDF presentations
    with clear community groupings and a comprehensive legend.
    
    Args:
        G: NetworkX graph
        communities: List of communities (sets of nodes)
        out_png: Optional output PNG path
        show: Whether to display the plot
        title: Title for the plot
        show_legend: Whether to show community legend
        figsize: Figure size tuple
    """
    plt.figure(figsize=figsize)
    
    # Use community layout
    pos = community_spring_layout(G, communities=communities, k=2.0, iterations=100, scale=2)
    
    # Color nodes by community
    colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
    node_colors = {}
    
    for i, community in enumerate(communities):
        for node in community:
            node_colors[node] = colors[i]
    
    # Draw the graph
    nx.draw_networkx_nodes(G, pos, 
                          node_color=[node_colors.get(node, 'gray') for node in G.nodes()],
                          node_size=400, alpha=0.8, edgecolors='black', linewidths=0.5)
    
    # Draw edges with reduced opacity
    nx.draw_networkx_edges(G, pos, alpha=0.2, width=0.8, color='gray')
    
    # Add labels for all characters with better positioning
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold', 
                           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.title(title, fontsize=18, fontweight='bold', pad=20)
    plt.axis('off')
    
    # Add community legend if requested
    if show_legend:
        legend_elements = []
        for i, community in enumerate(communities):
            community_name = f"Community {i+1} ({len(community)} chars)"
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=colors[i], markersize=12, 
                                            label=community_name))
        
        # Position legend outside the plot area
        plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), 
                  fontsize=10, frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()

    if out_png:
        import os
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Publication visualization saved to: {out_png}")

    if show:
        plt.show()
    plt.close()


def create_community_summary_table(analysis_results, out_png=None, show=True):
    """
    Create a summary table showing communities and their members.
    
    This creates a clean table visualization suitable for PDF presentations
    showing which characters belong to each community.
    
    Args:
        analysis_results: Results from analyze_communities()
        out_png: Optional output PNG path
        show: Whether to display the plot
    """
    if analysis_results is None:
        print("No analysis results to display")
        return
    
    # Prepare data for table
    table_data = []
    for stats in analysis_results['community_stats']:
        community_id = stats['id']
        characters = sorted(stats['nodes'])
        house_dist = stats['houses']
        
        # Create character list with house info
        char_list = []
        for char in characters:
            house = CHARACTER_HOUSES.get(char, 'unknown')
            char_list.append(f"{char} ({house})")
        
        # Join characters with line breaks for better display
        char_string = "\n".join(char_list)
        
        # Create house distribution string
        house_string = ", ".join([f"{house}: {count}" for house, count in house_dist.items()])
        
        table_data.append([
            f"Community {community_id}",
            f"{stats['size']} characters",
            char_string,
            house_string,
            f"{stats['density']:.3f}"
        ])
    
    # Create table
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=table_data,
                    colLabels=['Community', 'Size', 'Characters', 'House Distribution', 'Density'],
                    cellLoc='left',
                    loc='center',
                    bbox=[0, 0, 1, 1])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Color header row
    for i in range(5):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(5):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
            else:
                table[(i, j)].set_facecolor('white')
    
    plt.title(f'Community Analysis Summary - {analysis_results["method"].upper()}\n'
              f'Modularity: {analysis_results["modularity"]:.3f} | '
              f'Communities: {analysis_results["num_communities"]}', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()

    if out_png:
        import os
        output_dir = os.path.dirname(out_png)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Community summary table saved to: {out_png}")

    if show:
        plt.show()
    plt.close()
