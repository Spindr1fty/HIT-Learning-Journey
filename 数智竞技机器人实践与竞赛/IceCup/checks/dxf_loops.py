"""Assemble LINE+ARC+POLYLINE segments into closed loops per DXF.

A part profile is only extrudable if its boundary chains into a closed loop.
Lines alone are not enough: rounded corners and slots come from ARC entities,
so both must be walked together.
"""

import math
import sys
from collections import defaultdict
from pathlib import Path

import ezdxf

TOL = 0.05


def _k(p):
    return (round(p[0] / TOL), round(p[1] / TOL))


def _arc_pts(c, r, a0, a1, n=24):
    # DXF angles are CCW from start to end.
    while a1 < a0:
        a1 += 360.0
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _segments(e):
    t = e.dxftype()
    if t == "LINE":
        yield [(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)]
    elif t == "ARC":
        yield _arc_pts((e.dxf.center.x, e.dxf.center.y), e.dxf.radius,
                       e.dxf.start_angle, e.dxf.end_angle)
    elif t == "LWPOLYLINE":
        pts = [(p[0], p[1]) for p in e.get_points()]
        bulges = [p[4] for p in e.get_points("xyseb")]
        for i in range(len(pts) - (0 if e.closed else 1)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            bg = bulges[i]
            if abs(bg) > 1e-9:
                yield _bulge_pts(a, b, bg)
            else:
                yield [a, b]


def _bulge_pts(a, b, bulge):
    theta = 4 * math.atan(bulge)
    chord = math.dist(a, b)
    r = chord / (2 * math.sin(abs(theta) / 2))
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    nx, ny = -(b[1] - a[1]) / chord, (b[0] - a[0]) / chord
    sign = 1 if theta > 0 else -1
    cx = mid[0] + nx * sign * (r * math.cos(abs(theta) / 2))
    cy = mid[1] + ny * sign * (r * math.cos(abs(theta) / 2))
    a0 = math.degrees(math.atan2(a[1] - cy, a[0] - cx))
    a1 = math.degrees(math.atan2(b[1] - cy, b[0] - cx))
    if theta > 0 and a1 < a0:
        a1 += 360
    if theta < 0 and a1 > a0:
        a1 -= 360
    return _arc_pts((cx, cy), r, a0, a1)


def _chain(segs):
    """Group segments into loops by walking shared endpoints."""
    adj = defaultdict(list)
    for i, s in enumerate(segs):
        adj[_k(s[0])].append((i, "fwd"))
        adj[_k(s[-1])].append((i, "rev"))
    used, loops = set(), []
    for start in range(len(segs)):
        if start in used:
            continue
        chain, cur, origin = [], _k(segs[start][0]), _k(segs[start][0])
        idx, direction = start, "fwd"
        while True:
            used.add(idx)
            seg = segs[idx]
            chain.extend(seg if direction == "fwd" else list(reversed(seg)))
            tip = _k(chain[-1])
            nxt = [(i, d) for i, d in adj[tip] if i not in used]
            if not nxt:
                break
            idx, direction = nxt[0]
            if _k(chain[-1]) == origin and len(chain) > 2:
                break
        loops.append(chain)
    return loops


def _area(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1]
                   - pts[(i + 1) % len(pts)][0] * pts[i][1]
                   for i in range(len(pts)))) / 2


def report(path: Path) -> None:
    doc = ezdxf.readfile(path)
    ms = doc.modelspace()
    segs = [s for e in ms if e.dxftype() in ("LINE", "ARC", "LWPOLYLINE")
            for s in _segments(e)]
    loops = _chain(segs)

    print("=" * 74)
    print(f"{path.name}: {len(segs)} segments -> {len(loops)} chain(s)")
    for i, lp in enumerate(loops):
        xs = [p[0] for p in lp]
        ys = [p[1] for p in lp]
        closed = math.dist(lp[0], lp[-1]) < TOL
        print(f"  loop {i}: pts={len(lp):4} closed={closed} "
              f"area={_area(lp):9.2f}  "
              f"bbox {max(xs)-min(xs):8.3f} x {max(ys)-min(ys):8.3f}")
        if not closed:
            print(f"         gap: ({lp[0][0]:.3f},{lp[0][1]:.3f}) .. "
                  f"({lp[-1][0]:.3f},{lp[-1][1]:.3f})  "
                  f"= {math.dist(lp[0], lp[-1]):.3f} mm open")


if __name__ == "__main__":
    files = ([Path(a) for a in sys.argv[1:]]
             or sorted((Path(__file__).resolve().parents[1] / "dxf").glob("*.dxf")))
    for f in files:
        try:
            report(f)
        except Exception as exc:
            print(f"{f.name}: FAILED {type(exc).__name__}: {exc}")
