r"""把 g_mount_b 那套倒角套到任意 B-rep 上（STEP，或 3MF 经 mesh2brep 转出来的实体）。

规则（和 docs/chamfer_spec.md 一致）
------------------------------------
* **45° × 1.0 mm** 对称倒角，倒在外部的**凸棱**上
* 不动的：
    1. 圆棱（孔口）
    2. 底面（Z = 模型最低点，留平面贴热床）
    3. 螺丝承压面（--skip-plane x=0 之类指定）
    4. 短于 --min-edge 的碎边
    5. `--min-face-area` 以下的小碎面旁边的棱（网格重建件专用，避开齿纹/圆角碎片）
* 凸/凹判定：棱中点周围垂直棱的圆环打 24 个探针，过半在空气里 = 凸
* 一次倒不全：递归二分；被拒的边按 0.6 / 0.4 / 0.3 倍重试

用法
----
    python chamfer_part.py in.step out.step
    python chamfer_part.py in.step out.step --min-face-area 25 --size 1.0
    python chamfer_part.py in.step out.step --skip-plane x=0 --stl out.stl
    python chamfer_part.py in.step --report

注：输入必须是**素件**（还没倒过角的）。
"""

import argparse
import math
import sys

from cadgen import build123d as bd

CHAMFER = 1.0
MIN_EDGE = 1.0
PROBE_EPS = 0.15
PROBE_RING = 24
RETRY_FRACTIONS = (0.6, 0.4, 0.3)


def _parse_planes(items):
    out = []
    for it in items or []:
        axis, _, val = it.partition("=")
        out.append((axis.strip().lower(), float(val)))
    return out


def _on_plane(mid, planes, tol=1e-3):
    for axis, val in planes:
        if abs({"x": mid.X, "y": mid.Y, "z": mid.Z}[axis] - val) < tol:
            return True
    return False


def _edge_key(e):
    m = e.position_at(0.5)
    return (e.geom_type.name, round(e.length, 2),
            round(m.X, 3), round(m.Y, 3), round(m.Z, 3))


def face_area_map(part):
    """edge key -> smallest area of the faces touching it."""
    out = {}
    for f in part.faces():
        a = f.area
        for e in f.edges():
            k = _edge_key(e)
            if a < out.get(k, 1e18):
                out[k] = a
    return out


def convex_specs(part, bottom_z=None, planes=(), min_edge=MIN_EDGE,
                 min_face_area=0.0):
    fmap = face_area_map(part) if min_face_area > 0 else None
    specs = []
    n_circle = n_bottom = n_plane = n_short = n_concave = n_small = 0
    for e in part.edges():
        if e.geom_type.name == "CIRCLE":
            n_circle += 1
            continue
        m = e.position_at(0.5)
        if bottom_z is not None and m.Z <= bottom_z + 1e-3:
            n_bottom += 1
            continue
        if planes and _on_plane(m, planes):
            n_plane += 1
            continue
        if e.length < min_edge:
            n_short += 1
            continue
        if fmap is not None and fmap.get(_edge_key(e), 0.0) < min_face_area:
            n_small += 1
            continue
        d = bd.Vector(e.tangent_at(0.5)).normalized()
        ref = bd.Vector(0, 0, 1) if abs(d.Z) < 0.9 else bd.Vector(1, 0, 0)
        u = bd.Vector(d.cross(ref)).normalized()
        v = bd.Vector(d.cross(u)).normalized()
        air = 0
        for k in range(PROBE_RING):
            a = 2.0 * math.pi * k / PROBE_RING
            p = m + u * (math.cos(a) * PROBE_EPS) + v * (math.sin(a) * PROBE_EPS)
            if not part.is_inside(p):
                air += 1
        if air > PROBE_RING // 2:
            specs.append((m, d, e))
        else:
            n_concave += 1
    print(f"   edges {len(part.edges())}: candidates {len(specs)} | skipped"
          f" circle {n_circle}, bottom {n_bottom}, plane {n_plane},"
          f" short {n_short}, small-face {n_small}, concave {n_concave}")
    return specs


def _chamfer_set(part, specs, length, fails, done):
    if not specs:
        return part
    try:
        res = bd.chamfer([s[2] for s in specs], length)
    except Exception:
        res = None
    if res is not None and res.is_valid and res.volume < part.volume:
        done.append(len(specs))
        return res
    if len(specs) <= 1:
        fails.append(specs[0])
        return part
    half = len(specs) // 2
    part = _chamfer_set(part, specs[:half], length, fails, done)
    return _chamfer_set(part, specs[half:], length, fails, done)


def chamfer(part, size=CHAMFER, bottom=True, planes=(), min_edge=MIN_EDGE,
            min_face_area=0.0):
    b = part.bounding_box()
    specs = convex_specs(part, bottom_z=(b.min.Z if bottom else None),
                         planes=planes, min_edge=min_edge,
                         min_face_area=min_face_area)
    fails, done = [], []
    out = _chamfer_set(part, specs, size, fails, done)
    for frac in RETRY_FRACTIONS:
        if not fails:
            break
        retry, fails = list(fails), []
        print(f"   retrying {len(retry)} edge(s) at {frac * size:.2f} mm")
        out = _chamfer_set(out, retry, frac * size, fails, done)
    for m, d, e in fails:
        print(f"   refused at ({m.X:7.2f},{m.Y:7.2f},{m.Z:7.2f})  len {e.length:.2f}")
    return out, specs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--size", type=float, default=CHAMFER)
    ap.add_argument("--skip-plane", action="append", default=[],
                    metavar="AXIS=VALUE")
    ap.add_argument("--no-bottom", action="store_true")
    ap.add_argument("--min-edge", type=float, default=MIN_EDGE)
    ap.add_argument("--min-face-area", type=float, default=0.0)
    ap.add_argument("--stl", default=None)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)

    part = bd.import_step(a.src)
    b = part.bounding_box()
    print(f"input  volume {part.volume / 1000:.3f} cm3  faces {len(part.faces())}"
          f"  bbox {b.max.X - b.min.X:.2f} x {b.max.Y - b.min.Y:.2f}"
          f" x {b.max.Z - b.min.Z:.2f}")
    planes = _parse_planes(a.skip_plane)
    if a.report:
        specs = convex_specs(part, bottom_z=(None if a.no_bottom else b.min.Z),
                             planes=planes, min_edge=a.min_edge,
                             min_face_area=a.min_face_area)
        for m, d, e in specs:
            print(f"   ({m.X:7.2f},{m.Y:7.2f},{m.Z:7.2f})  len {e.length:6.2f}")
        return 0
    if not a.dst:
        ap.error("dst is required unless --report")

    out, specs = chamfer(part, a.size, bottom=not a.no_bottom, planes=planes,
                         min_edge=a.min_edge, min_face_area=a.min_face_area)
    ob = out.bounding_box()
    print(f"output volume {out.volume / 1000:.3f} cm3"
          f"  ({(out.volume - part.volume) / 1000:+.3f})  valid {out.is_valid}"
          f"  faces {len(out.faces())}"
          f"  bbox {ob.max.X - ob.min.X:.2f} x {ob.max.Y - ob.min.Y:.2f}"
          f" x {ob.max.Z - ob.min.Z:.2f}")
    bd.export_step(out, a.dst)
    print("wrote", a.dst)
    if a.stl:
        bd.export_stl(out, a.stl, tolerance=0.01, angular_tolerance=0.3)
        print("wrote", a.stl)
    return 0


if __name__ == "__main__":
    sys.exit(main())
