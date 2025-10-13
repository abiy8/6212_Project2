
"""
benchmark_convex_hull.py
Benchmarks the D&C convex hull implementation over growing input sizes.
Writes results.csv and (optionally) plots .png files if matplotlib is available.

Usage:
    python benchmark_convex_hull.py
    python benchmark_convex_hull.py --sizes 500 1000 2000 4000 8000 16000 --repeats 3 --seed 42 --plot
"""
import time
import math
import random
import argparse
import csv
from typing import List, Tuple
try:
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

from convex_hull_dac import convex_hull_divide_and_conquer

def random_points(n: int, seed: int) -> List[Tuple[float, float]]:
    rng = random.Random(seed + n)
    return [(rng.uniform(-1e6, 1e6), rng.uniform(-1e6, 1e6)) for _ in range(n)]

def time_run(n: int, repeats: int, seed: int) -> float:
    pts = random_points(n, seed)
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        _ = convex_hull_divide_and_conquer(pts)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", type=int, nargs="*", default=[500, 1000, 2000, 4000, 8000, 16000])
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--plot", action="store_true", help="Emit runtime charts (requires matplotlib)")
    args = ap.parse_args()

    rows = []
    for n in args.sizes:
        avg = time_run(n, args.repeats, args.seed)
        nlogn = n * math.log2(max(n, 2))
        rows.append({"n": n, "avg_seconds": avg, "n_log2_n": nlogn, "seconds_per_nlog2n": avg / nlogn})
        print(f"n={n:6d}  avg={avg:.6f}s  sec/(n log2 n)={avg/nlogn:.3e}")

    # Write CSV
    with open("results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["n", "avg_seconds", "n_log2_n", "seconds_per_nlog2n"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("Wrote results.csv")

    if args.plot and HAVE_MPL:
        import matplotlib.pyplot as plt
        ns = [r["n"] for r in rows]
        avgs = [r["avg_seconds"] for r in rows]
        ratios = [r["seconds_per_nlog2n"] for r in rows]

        plt.figure()
        plt.plot(ns, avgs, marker="o")
        plt.title("D&C Convex Hull Runtime")
        plt.xlabel("n")
        plt.ylabel("seconds")
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.savefig("runtime.png", bbox_inches="tight")
        plt.close()

        plt.figure()
        plt.plot(ns, ratios, marker="o")
        plt.title("Runtime / (n log2 n)")
        plt.xlabel("n")
        plt.ylabel("seconds per (n log2 n)")
        plt.grid(True, linestyle="--", linewidth=0.5)
        plt.savefig("runtime_per_nlogn.png", bbox_inches="tight")
        plt.close()
        print("Wrote runtime.png and runtime_per_nlogn.png")
    elif args.plot and not HAVE_MPL:
        print("matplotlib is not installed; skipping plots.")

if __name__ == "__main__":
    main()
