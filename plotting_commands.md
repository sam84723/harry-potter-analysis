# 🎭 Harry Potter Character Network Plotting Commands

## Quick Reference

### Basic Commands
```bash
# Interactive menu (recommended)
py -3 plot_menu.py

# Basic examples
py -3 -m character_network.static_graphs --type main --out Artifacts/main.png
py -3 -m character_network.static_graphs --type all --out Artifacts/all.png
py -3 -m character_network.static_graphs --type matrix --out Artifacts/matrix.png
```

### Graph Types
| Type | Description | Best For |
|------|-------------|----------|
| `main` | Main characters only (18 chars) | Focused analysis |
| `all` | All characters with edges | Complete network view |
| `matrix` | Correlation heatmap | Detailed relationships |

### Features (Use with any graph type)
| Feature | Flag | Description |
|---------|------|-------------|
| House Colors | `--house-colors` | Color nodes by Hogwarts house |
| Edge Weighting | `--weighting kernel/npmi` | Choose edge calculation method |
| Edge Filtering | `--filter 0.3` | Keep top 30% of edges per node |
| Layout | `--layout spring/circular/kamada` | Choose graph layout |
| Spacing | `--min-distance 0.5` | Control node spacing |

### Layout Options
| Layout | Description | Best For |
|--------|-------------|----------|
| `auto` | Automatically choose | Default choice |
| `spring` | Force-directed | General purpose |
| `circular` | Circular arrangement | Many characters |
| `kamada` | Kamada-Kawai | Small graphs |

### Common Examples

#### Main Characters
```bash
# Basic main characters graph
py -3 -m character_network.static_graphs --type main --out Artifacts/main.png

# With house colors
py -3 -m character_network.static_graphs --type main --house-colors --out Artifacts/main_house.png

# With NPMI weighting
py -3 -m character_network.static_graphs --type main --weighting npmi --out Artifacts/main_npmi.png

# With edge filtering (30% of edges per node)
py -3 -m character_network.static_graphs --type main --filter 0.3 --out Artifacts/main_filtered.png
```

#### All Characters
```bash
# Basic all characters graph (circular layout)
py -3 -m character_network.static_graphs --type all --out Artifacts/all.png

# With house colors
py -3 -m character_network.static_graphs --type all --house-colors --out Artifacts/all_house.png

# With edge filtering (20% of edges per node)
py -3 -m character_network.static_graphs --type all --filter 0.2 --out Artifacts/all_filtered.png

# With spring layout
py -3 -m character_network.static_graphs --type all --layout spring --out Artifacts/all_spring.png
```

#### Filtered Graphs (Reduce Clutter)
```bash
# Main characters with 30% edge filtering
py -3 -m character_network.static_graphs --type main --filter 0.3 --out Artifacts/main_filtered_30.png

# All characters with 20% edge filtering
py -3 -m character_network.static_graphs --type all --filter 0.2 --out Artifacts/all_filtered_20.png

# Very sparse graph (10% edges)
py -3 -m character_network.static_graphs --type all --filter 0.1 --out Artifacts/very_sparse.png
```

#### Correlation Matrices
```bash
# All characters matrix
py -3 -m character_network.static_graphs --type matrix --out Artifacts/matrix_all.png

# Main characters matrix
py -3 -m character_network.static_graphs --type matrix --main-only --out Artifacts/matrix_main.png
```

### Advanced Combinations

#### Custom Spacing Experiments
```bash
# Very tight spacing
py -3 -m character_network.static_graphs --type house --min-distance 0.1 --out Artifacts/tight.png

# Very loose spacing
py -3 -m character_network.static_graphs --type house --min-distance 0.8 --out Artifacts/loose.png
```

#### Layout Experiments
```bash
# Try different layouts
py -3 -m character_network.static_graphs --type house --layout spring --out Artifacts/spring.png
py -3 -m character_network.static_graphs --type house --layout circular --out Artifacts/circular.png
py -3 -m character_network.static_graphs --type house --layout kamada --out Artifacts/kamada.png
```

#### Edge Filtering
```bash
# Limit number of edges shown
py -3 -m character_network.static_graphs --type house --top 100 --out Artifacts/house_100.png
py -3 -m character_network.static_graphs --type house --top 50 --out Artifacts/house_50.png
```

### Parameter Reference

| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| `--type` | Graph type | kernel, npmi, house, main, all, filtered, matrix | kernel |
| `--layout` | Layout algorithm | auto, spring, circular, kamada | auto |
| `--top` | Max edges to show | 1-1000+ | 200 |
| `--cutoff` | % edges per node (filtered) | 0.1-1.0 | 0.3 |
| `--min-distance` | Min distance between nodes | 0.1-1.0 | 0.3 |
| `--main-only` | Show only main characters | true/false | false |
| `--out` | Output PNG file | path | (auto-generated) |
| `--no-show` | Don't display plot | true/false | false |

### Tips for Best Results

1. **Start with house graphs** - Great visual appeal and shows all characters
2. **Use filtered graphs** - Reduces clutter in dense networks
3. **Try main characters** - Cleaner, more focused analysis
4. **Experiment with spacing** - Adjust `--min-distance` to prevent overlap
5. **Test different layouts** - Each layout works better for different graph sizes
6. **Use correlation matrices** - For detailed relationship analysis

### Troubleshooting

- **Nodes overlapping?** → Increase `--min-distance`
- **Graph too cluttered?** → Use `--type filtered` or reduce `--top`
- **Too few characters?** → Check if using `--main-only` when you want all characters
- **Layout looks weird?** → Try different `--layout` options
