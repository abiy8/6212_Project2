
"""
convex_hull_dac.py
Divide-and-conquer convex hull in O(n log n).

Usage (as a library):
    from convex_hull_dac import convex_hull_divide_and_conquer
    hull = convex_hull_divide_and_conquer(points)  # points: Iterable[(x, y)]

Usage (CLI quick demo):
    python convex_hull_dac.py --n 20 --seed 0
"""
from collections import namedtuple
from typing import List, Tuple, Iterable
import random

Point = namedtuple("Point", ["x", "y"])

# ----------------- Geometry primitives -----------------
def _orientation(a: Point, b: Point, c: Point) -> int:
    """
    Return orientation of triplet (a,b,c):
      >0 for counter-clockwise, <0 for clockwise, 0 collinear.
    Uses signed area (cross product) test.
    """
    # Note: Using a robust predicate (exact arithmetic) is recommended for production,
    # but this simple float/integer version is fine for most uses.
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0

# ----------------- Tangent helpers -----------------
def _upper_tangent(left: List[Point], right: List[Point]) -> Tuple[int, int]:
    """Find indices (i, j) of the upper common tangent between two convex hulls (both CCW)."""
    i = max(range(len(left)), key=lambda k: left[k].x)    # rightmost of left
    j = min(range(len(right)), key=lambda k: right[k].x)  # leftmost of right
    changed = True
    while changed:
        changed = False
        # Move i clockwise on left
        while True:
            nxt = (i - 1) % len(left)  # clockwise step on CCW list
            if _orientation(right[j], left[i], left[nxt]) >= 0:
                i = nxt
                changed = True
            else:
                break
        # Move j counter-clockwise on right
        while True:
            nxt = (j + 1) % len(right)
            if _orientation(left[i], right[j], right[nxt]) <= 0:
                j = nxt
                changed = True
            else:
                break
    return i, j

def _lower_tangent(left: List[Point], right: List[Point]) -> Tuple[int, int]:
    """Find indices (i, j) of the lower common tangent between two convex hulls (both CCW)."""
    i = max(range(len(left)), key=lambda k: left[k].x)    # rightmost of left
    j = min(range(len(right)), key=lambda k: right[k].x)  # leftmost of right
    changed = True
    while changed:
        changed = False
        # Move i counter-clockwise on left
        while True:
            nxt = (i + 1) % len(left)
            if _orientation(right[j], left[i], left[nxt]) <= 0:
                i = nxt
                changed = True
            else:
                break
        # Move j clockwise on right
        while True:
            nxt = (j - 1) % len(right)
            if _orientation(left[i], right[j], right[nxt]) >= 0:
                j = nxt
                changed = True
            else:
                break
    return i, j

# ----------------- Merge two hulls -----------------
def _merge_hulls(left: List[Point], right: List[Point]) -> List[Point]:
    """
    Merge two convex hulls (each CCW, not repeating first vertex at end)
    into a single CCW hull.
    """
    if not left:
        return right[:]
    if not right:
        return left[:]
    ui, uj = _upper_tangent(left, right)
    li, lj = _lower_tangent(left, right)

    merged: List[Point] = []
    # Left arc: ui -> li (inclusive), CCW
    k = ui
    merged.append(left[k])
    while k != li:
        k = (k + 1) % len(left)
        merged.append(left[k])
    # Right arc: lj -> uj (inclusive), CCW
    k = lj
    merged.append(right[k])
    while k != uj:
        k = (k + 1) % len(right)
        merged.append(right[k])
    return merged

# ----------------- Base hulls -----------------
def _hull_base(points: List[Point]) -> List[Point]:
    """Return convex hull for up to 3 points in CCW order (no duplicate start/end)."""
    if len(points) <= 1:
        return points[:]
    if len(points) == 2:
        a, b = points
        if a == b:
            return [a]
        return [a, b]
    # 3 points
    a, b, c = points
    o = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    if o > 0:
        return [a, b, c]
    elif o < 0:
        return [a, c, b]
    else:
        # Collinear: keep endpoints only
        pts = sorted(points, key=lambda p: (p.x, p.y))
        return [pts[0], pts[-1]]

# ----------------- Divide & conquer -----------------
def _dac(points_sorted: List[Point]) -> List[Point]:
    if len(points_sorted) <= 3:
        return _hull_base(points_sorted)
    mid = len(points_sorted) // 2
    left = _dac(points_sorted[:mid])
    right = _dac(points_sorted[mid:])
    return _merge_hulls(left, right)

def convex_hull_divide_and_conquer(points: Iterable[Tuple[float, float]]):
    """
    Compute the convex hull of an iterable of (x, y) points.
    Returns a list of Points in CCW order (first vertex not repeated).
    """
    pts = [Point(float(x), float(y)) for (x, y) in points]
    pts.sort(key=lambda p: (p.x, p.y))  # O(n log n)
    return _dac(pts)

# ----------------- CLI demo -----------------
if __name__ == "__main__":
    import argparse, json
    ap = argparse.ArgumentParser(description="Divide-and-conquer convex hull demo.")
    ap.add_argument("--n", type=int, default=20, help="number of random points")
    ap.add_argument("--seed", type=int, default=0, help="random seed")
    ap.add_argument("--dump", action="store_true", help="print hull as JSON list")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    pts = [(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000)) for _ in range(args.n)]
    hull = convex_hull_divide_and_conquer(pts)

    print(f"Generated {args.n} points. Hull has {len(hull)} vertices.")
    if args.dump:
        print(json.dumps([{"x": p.x, "y": p.y} for p in hull], indent=2))
