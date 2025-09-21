#!/usr/bin/env python3
"""
Test script for the new graph analysis module.
This demonstrates the separated algorithmic functionality.
"""

import pandas as pd
import networkx as nx
from character_network.graph_analysis import (
    analyze_communities,
    calculate_network_metrics,
    print_community_analysis,
    print_network_metrics,
    create_community_visualization
)

def test_graph_analysis():
    """Test the graph analysis functions."""
    print("Testing Graph Analysis Module")
    print("=" * 50)
    
    # Load a sample graph
    edges_file = "Artifacts/edges_kernel.csv"
    try:
        df = pd.read_csv(edges_file)
        if df.empty:
            print("ERROR: No edges found in CSV file")
            return
        
        # Create graph
        G = nx.Graph()
        for _, r in df.iterrows():
            G.add_edge(r['char_a'], r['char_b'], weight=r['weight'])
        
        print(f"SUCCESS: Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Test network metrics
        print("\nCalculating network metrics...")
        metrics = calculate_network_metrics(G)
        print_network_metrics(metrics)
        
        # Test community analysis
        print("\nAnalyzing communities...")
        analysis_results = analyze_communities(G, method='louvain')
        if analysis_results:
            print_community_analysis(analysis_results)
            
            # Test visualization
            print("\nCreating community visualization...")
            create_community_visualization(G, analysis_results['communities'], 
                                        out_png="Artifacts/test_communities.png", 
                                        show=False)
            print("SUCCESS: Community visualization saved to Artifacts/test_communities.png")
        else:
            print("ERROR: Community analysis failed")
            
    except FileNotFoundError:
        print(f"ERROR: Edges file not found: {edges_file}")
        print("Please run the pipeline first to generate edges.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_graph_analysis()
