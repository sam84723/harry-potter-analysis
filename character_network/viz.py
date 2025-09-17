import os
import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


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
    offset = 1.0  # increase all edges by 2 px
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
    parser.add_argument("--type", choices=["kernel", "npmi"], default="kernel", help="graph type: kernel or npmi")
    parser.add_argument("--top", type=int, default=200)
    parser.add_argument("--out", default="", help="optional PNG output path")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    out_png = args.out if args.out else None
    
    if args.type == "npmi":
        plot_npmi_graph(args.edges, top_n=args.top, out_png=out_png, show=(not args.no_show))
    else:
        plot_kernel_graph(args.edges, top_n=args.top, out_png=out_png, show=(not args.no_show))


if __name__ == "__main__":
    main()


