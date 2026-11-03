"""Read-only audit of project DXF files: profile closure, units, patterns.

Run:  python checks/dxf_report.py [dxf/*.dxf]
"""

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import ezdxf

UNITS = {0: "unitless", 1: "inches", 2: "feet", 4: "mm", 5: "cm", 6: "m", 7: "km"}


def _shoelace(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1]
                   - pts[(i + 1) % len(pts)][0] * pts[i][1]
                   for i in range(len(pts)))) / 2


def _closed_from_segments(segs, tol=1e-4):
    """Do undirected segments form one closed loop? Returns (ok, chain_len)."""
    if not segs:
        return False, 0
    key = lambda p: (round(p[0] / tol), round(p[1] / tol))
    deg = defaultdict(int)
    for a, b in segs:
        deg[key(a)] += 1
        deg[key(b)] += 1
    even = all(d == 2 for d in deg.values())
    return even and len(deg) == len(segs), len(segs)


def report(path: Path) -> None:
    doc = ezdxf.readfile(path)
    ms = doc.modelspace()
    ents = list(ms)
    counts = Counter(e.dxftype() for e in ents)

    print("=" * 78)
    print(f"{path.name}   {path.stat().st_size} bytes   dxf={doc.dxfversion}")
    insu = doc.header.get("$INSUNITS", 0)
    print(f"  units={insu} ({UNITS.get(insu, '?')})   layers={len(list(doc.layers))}"
          f"   entities={len(ents)}")
    print(f"  types: {dict(counts)}")

    hs = doc.header
    if "$EXTMIN" in hs:
        a, b = hs["$EXTMIN"], hs["$EXTMAX"]
        print(f"  header extents {a[0]:.2f},{a[1]:.2f} .. {b[0]:.2f},{b[1]:.2f}"
              f"  = {b[0]-a[0]:.3f} x {b[1]-a[1]:.3f}")

    # --- circles ---
    circles = [(e.dxf.center.x, e.dxf.center.y, e.dxf.radius, e.dxf.layer)
               for e in ms.query("CIRCLE")]
    if circles:
        byr = defaultdict(list)
        for x, y, r, l in circles:
            byr[round(r, 3)].append((x, y))
        print(f"  CIRCLE x{len(circles)}  radii: "
              + ", ".join(f"R{r}({len(v)})" for r, v in sorted(byr.items())))
        conc = defaultdict(list)
        for x, y, r, _ in circles:
            conc[(round(x, 2), round(y, 2))].append(r)
        multi = {k: v for k, v in conc.items() if len(v) > 1}
        if multi:
            print(f"    concentric sets: {len(multi)} -> "
                  + "; ".join(f"({k[0]},{k[1]}) R{sorted(v)}" for k, v in list(multi.items())[:6]))
        for r, pts in sorted(byr.items()):
            xs = sorted(p[0] for p in pts)
            ys = sorted(p[1] for p in pts)
            print(f"    R{r}: n={len(pts)}  x[{xs[0]:.2f}..{xs[-1]:.2f}]"
                  f"  y[{ys[0]:.2f}..{ys[-1]:.2f}]")

    # --- arcs ---
    arcs = [(e.dxf.center.x, e.dxf.center.y, e.dxf.radius,
             e.dxf.start_angle, e.dxf.end_angle) for e in ms.query("ARC")]
    if arcs:
        print(f"  ARC x{len(arcs)}  radii={sorted(set(round(a[2],3) for a in arcs))}")
        full = [a for a in arcs if abs((a[4] - a[3]) % 360 - 360) < 1e-6]
        if full:
            print(f"    {len(full)} of them are full 360 deg (act as circles)")

    # --- polylines ---
    for e in ms.query("LWPOLYLINE"):
        pts = [(p[0], p[1]) for p in e.get_points()]
        bulges = [p[4] for p in e.get_points("xyseb")] if len(pts) else []
        closed = bool(e.closed)
        area = _shoelace(pts) if len(pts) > 2 else 0.0
        has_arc = any(abs(b) > 1e-9 for b in bulges) if bulges else False
        print(f"  LWPOLY n={len(pts):3} closed={closed} arc_segs={has_arc}"
              f"  area={area:.2f}  bbox={_bbox(pts)}")

    for e in ms.query("POLYLINE"):
        try:
            pts = [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices]
        except Exception:
            pts = []
        print(f"  POLYLINE n={len(pts)} closed={bool(e.is_closed)} bbox={_bbox(pts)}")

    # --- lines: do they close? ---
    lines = [(e.dxf.start.x, e.dxf.start.y, e.dxf.end.x, e.dxf.end.y, e.dxf.layer)
             for e in ms.query("LINE")]
    if lines:
        segs = [((a, b), (c, d)) for a, b, c, d, _ in lines]
        ok, n = _closed_from_segments(segs)
        print(f"  LINE x{len(lines)}  form one closed loop: {ok}")
        for a, b, c, d, l in sorted(lines, key=lambda t: -math.dist(t[:2], t[2:4]))[:6]:
            print(f"    ({a:8.3f},{b:8.3f})->({c:8.3f},{d:8.3f})  len={math.dist((a,b),(c,d)):8.3f}")
        if len(lines) > 6:
            print(f"    ... {len(lines)-6} more")

    # --- dimensions ---
    dims = []
    for e in ms.query("DIMENSION"):
        m = getattr(e.dxf, "actual_measurement", None)
        if m is not None:
            dims.append(round(m, 3))
    if dims:
        print(f"  DIMENSION values: {sorted(set(dims))}")

    # --- text ---
    txt = [e.dxf.text for e in ms.query("TEXT MTEXT")]
    if txt:
        print(f"  TEXT: {txt[:12]}")


def _bbox(pts):
    if not pts:
        return "n/a"
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return f"{max(xs)-min(xs):.3f}x{max(ys)-min(ys):.3f}"


if __name__ == "__main__":
    files = [Path(a) for a in sys.argv[1:]] or sorted((Path(__file__).resolve().parents[1] / "dxf").glob("*.dxf"))
    for f in files:
        try:
            report(f)
        except Exception as exc:
            print(f"{f.name}: FAILED {type(exc).__name__}: {exc}")
