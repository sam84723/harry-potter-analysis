import os
import argparse

# Support both "python -m character_network.pipeline" and
# direct execution "python character_network/pipeline.py"
try:
    from .core import generate_all_mentions_parquet
    from .scoring import generate_kernel_edges_csv, generate_npmi_edges_csv
except ImportError:
    import sys
    # Add project root to sys.path, then import via absolute package path
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    from character_network.core import generate_all_mentions_parquet
    from character_network.scoring import generate_kernel_edges_csv, generate_npmi_edges_csv


def run_pipeline(
    mentions_path: str = os.path.join("Artifacts", "mentions.parquet"),
    edges_kernel_csv: str = os.path.join("Artifacts", "edges_kernel.csv"),
    edges_npmi_csv: str = os.path.join("Artifacts", "edges_npmi.csv"),
    sigma: float = 200.0,
    radius: int = 600,
    window_size: int = 200,
    step: int = 100,
    focus: str = ""
):
    focus_list = None
    if focus.strip():
        focus_list = [x.strip().lower() for x in focus.split(",") if x.strip()]

    generate_all_mentions_parquet(out_path=mentions_path, focus_characters=focus_list)
    print(f"Mentions saved to: {mentions_path}")

    generate_kernel_edges_csv(mentions_path, edges_kernel_csv, sigma=sigma, radius=radius)
    print(f"Kernel edges saved to: {edges_kernel_csv}")
    
    generate_npmi_edges_csv(mentions_path, edges_npmi_csv, window_size=window_size, step=step)
    print(f"NPMI edges saved to: {edges_npmi_csv}")


def main():
    parser = argparse.ArgumentParser(description="Character network pipeline")
    parser.add_argument("--mentions", default=os.path.join("Artifacts", "mentions.parquet"))
    parser.add_argument("--edges-kernel", default=os.path.join("Artifacts", "edges_kernel.csv"))
    parser.add_argument("--edges-npmi", default=os.path.join("Artifacts", "edges_npmi.csv"))
    parser.add_argument("--sigma", type=float, default=200.0)
    parser.add_argument("--radius", type=int, default=600)
    parser.add_argument("--window-size", type=int, default=200, help="window size for NPMI calculation")
    parser.add_argument("--step", type=int, default=100, help="step size for NPMI window sliding")
    parser.add_argument("--focus", type=str, default="", help="comma-separated canonical names")
    args = parser.parse_args()

    run_pipeline(
        mentions_path=args.mentions,
        edges_kernel_csv=args.edges_kernel,
        edges_npmi_csv=args.edges_npmi,
        sigma=args.sigma,
        radius=args.radius,
        window_size=args.window_size,
        step=args.step,
        focus=args.focus,
    )


if __name__ == "__main__":
    main()


