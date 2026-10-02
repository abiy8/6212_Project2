
# Divide-and-Conquer Convex Hull

This repo contains a compact Python implementation of a **divide-and-conquer** convex hull with an optional benchmark script.

## Files
- `convex_hull_dac.py` — Library + small CLI demo.
- `benchmark_convex_hull.py` — Runs timing experiments and writes `results.csv`. Can also output charts (`--plot`).

## Quick Start
```bash
# (Optional) create & activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -U pip
# Only needed for charts in benchmark script:
pip install matplotlib
```

### Demo
```bash
python convex_hull_dac.py --n 20 --seed 0 --dump
```

### Benchmark
```bash
python benchmark_convex_hull.py --sizes 500 1000 2000 4000 8000 16000 --repeats 3 --seed 42 --plot
# outputs:
#  - results.csv
#  - runtime.png
#  - runtime_per_nlogn.png
```

## API
```python
from convex_hull_dac import convex_hull_divide_and_conquer
hull = convex_hull_divide_and_conquer([(0,0), (1,0), (0,1), (1,1)])
# hull is a list of Points (namedtuple with fields x,y) in CCW order.
```
## How to run
git clone https://github.com/abiy8/6212_Project2.git
cd 6212_Project2


## Project context

Computational geometry coursework with a library function, CLI demo, and benchmark script. The stated O(n log n) bound is the intended algorithmic complexity, not an independently proven property of every implementation path. Review checks reproduced nontermination for four collinear points and four identical points (two-second process timeouts). The random CLI demo and a square-input example completed. Degenerate-input handling needs a code fix before broader use; this README-only change leaves it untouched.

## Notes
- Complexity: **O(n log n)** due to initial sort; merge is linear in hull sizes.
- Robustness: For near-collinear cases with floats, consider using exact predicates for orientation if needed.
