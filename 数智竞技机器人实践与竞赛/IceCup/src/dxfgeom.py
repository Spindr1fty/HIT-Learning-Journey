"""Shared DXF geometry helpers: segment extraction and closed-loop chaining.

Used by both the audit scripts in checks/ and src/gen_parts_data.py, so loop
detection is defined once.
"""

import math

TOL = 0.05


def _k(p):
    return (round(p[0] / TOL), round(p[1] / TOL))


def _arc_pts(c, r, a0, a1, n=24):
    while a1 < a0:
        a1 += 360.0
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _bulge_pts(a, b, bulge):
    theta = 4 * math.atan(bulge)
    chord = math.dist(a, b)
    r = chord / (2 * math.sin(abs(theta) / 2))
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    nx, ny = -(b[1] - a[1]) / chord, (b[0] - a[0]) / chord
    sign = 1 if theta > 0 else -1
    cx = mid[0] + nx * sign * r * math.cos(abs(theta) / 2)
    cy = mid[1] + ny * sign * r * math.cos(abs(theta) / 2)
    a0 = math.degrees(math.atan2(a[1] - cy, a[0] - cx))
    a1 = math.degrees(math.atan2(b[1] - cy, b[0] - cx))
    if theta > 0 and a1 < a0:
        a1 += 360
    if theta < 0 and a1 > a0:
        a1 -= 360
    return _arc_pts((cx, cy), r, a0, a1)


def segments(entity):
    """Yield each boundary of an entity as a polyline of (x, y) points."""
    t = entity.dxftype()
    if t == "LINE":
        yield [(entity.dxf.start.x, entity.dxf.start.y),
               (entity.dxf.end.x, entity.dxf.end.y)]
    elif t == "ARC":
        yield _arc_pts((entity.dxf.center.x, entity.dxf.center.y), entity.dxf.radius,
                       entity.dxf.start_angle, entity.dxf.end_angle)
    elif t == "LWPOLYLINE":
        pts = [(p[0], p[1]) for p in entity.get_points()]
        bulges = [p[4] for p in entity.get_points("xyseb")]
        span = len(pts) if entity.closed else len(pts) - 1
        for i in range(span):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            yield _bulge_pts(a, b, bulges[i]) if abs(bulges[i]) > 1e-9 else [a, b]


def chain_loops(segs):
    """Group segments into loops by walking shared endpoints."""
    adj = {}
    for i, s in enumerate(segs):
        adj.setdefault(_k(s[0]), []).append((i, "fwd"))
        adj.setdefault(_k(s[-1]), []).append((i, "rev"))

    used, loops = set(), []
    for start in range(len(segs)):
        if start in used:
            continue
        chain = []
        idx, direction = start, "fwd"
        origin = _k(segs[start][0])
        while True:
            used.add(idx)
            seg = segs[idx]
            chain.extend(seg if direction == "fwd" else list(reversed(seg)))
            nxt = [(i, d) for i, d in adj.get(_k(chain[-1]), []) if i not in used]
            if not nxt:
                break
            idx, direction = nxt[0]
            if _k(chain[-1]) == origin and len(chain) > 2:
                break
        loops.append(chain)
    return loops


def loops_of(doc):
    segs = [s for e in doc.modelspace()
            if e.dxftype() in ("LINE", "ARC", "LWPOLYLINE")
            for s in segments(e)]
    return chain_loops(segs)


def area(pts):
    n = len(pts)
    return abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
                   for i in range(n))) / 2


def bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)
