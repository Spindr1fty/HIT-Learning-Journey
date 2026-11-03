r"""Chassis as a printable solid (default 6 mm PLA), exported to STEP + STL.

The geometry comes from src/chassis.py -- the SAME outline and the SAME 44
holes as the reference DXF, so the solid cannot drift from the source data.

    outline: 10 lines + 10 arcs (arcs polygonalised at 20 segments each,
             chord error < 0.002 mm)
    holes  : 32 wheel-plate + 8 Z-axis + 4 battery
    extras : rear strip + two side ears, 7 square pass-through holes,
             3 flat zip-tie eyes (18 x 3 wall, 12 tall, 8 x 5 window)

The plate top is Z = 0 and the material goes DOWN to Z = -thick, as fixed by
the project coordinate system.

Run (from src/):
    uvx --from "cadgen==0.7.21" python chassis_stl.py [thickness]
writes
    ..\newSTEP\chassis.step
    ..\newSTEP\chassis.stl
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import chassis as C  # noqa: E402

THICK = C.PLATE_T
ARC_SEG = 20
STEP_WORK = Path(__file__).resolve().parent.parent / "newSTEP" / "chassis.step"
STL_WORK = Path(__file__).resolve().parent.parent / "newSTEP" / "chassis.stl"


def segments():
    """Every outline piece as a list of (x, y) points, arcs sampled."""
    segs = []
    for x0, y0, x1, y1 in C.LINES:
        segs.append([(x0, y0), (x1, y1)])
    for cx, cy, r, a0, a1 in C.ARCS:
        if a1 < a0:
            a1 += 360.0
        segs.append([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / ARC_SEG)),
                      cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / ARC_SEG)))
                     for i in range(ARC_SEG + 1)])
    return segs


def ring(tol=0.05):   # the stored line ends are rounded to 0.01 mm
    """Stitch the pieces into one closed point ring."""
    segs = segments()
    pts = list(segs.pop(0))
    while segs:
        last = pts[-1]
        for i, s in enumerate(segs):
            if math.dist(s[0], last) < tol:
                pts += s[1:]
                segs.pop(i)
                break
            if math.dist(s[-1], last) < tol:
                pts += s[-2::-1]
                segs.pop(i)
                break
        else:
            raise RuntimeError(f"outline does not close at {last}")
    return pts


def build(thick=THICK):
    pts = ring()
    if math.dist(pts[0], pts[-1]) < 1e-6:
        pts = pts[:-1]
    wire = bd.Wire(bd.Polyline(*pts, close=True).edges())
    face = bd.Face(wire)
    solid = bd.extrude(face, amount=thick)
    b = solid.bounding_box()
    if b.min.Z < -1e-9:                 # ring wound clockwise -> extruded down
        solid = bd.Pos(0, 0, -b.min.Z) * solid
    solid = bd.Pos(0, 0, -thick) * solid      # top face at Z = 0, plate below
    b = solid.bounding_box()
    if abs(b.max.Z) > 1e-6 or abs(b.min.Z + thick) > 1e-6:
        raise RuntimeError(f"unexpected Z range {b.min.Z}..{b.max.Z}")
    top, bot = b.max.Z, b.min.Z
    # grow the plate (solid boolean, so everything stays one solid)
    grown = []
    for x0, y0, x1, y1 in C.EXT_RECTS:
        grown.append(bd.Pos(x0, y0, bot) * bd.Box(
            x1 - x0, y1 - y0, thick,
            align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)))
    solid = solid.fuse(*grown)
    # round mounting holes + square cable pass-through holes
    cutters = [bd.Pos(x, y, bot - 0.1) * bd.Cylinder(
        C.HOLE_D / 2.0, (top - bot) + 0.2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for x, y, _ in C.all_holes()]
    cutters += [bd.Pos(x - C.SQ / 2, y - C.SQ / 2, bot - 0.1) * bd.Box(
        C.SQ, C.SQ, (top - bot) + 0.2,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
        for x, y in C.SQ_POS]
    solid = solid.cut(*cutters).clean()
    # three flat zip-tie eyes on the top face (18 x 3 wall, 8 x 5 window)
    eyes = []
    for cx, cy, along_y in C.EYE_POS:
        x0, y0, x1, y1 = C.eye_rect(cx, cy, along_y)
        wall = bd.Pos(x0, y0, top - 0.2) * bd.Box(
            x1 - x0, y1 - y0, C.EYE_H + 0.2,
            align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
        if along_y:
            win = bd.Pos(cx - C.EYE_T, cy - C.EYE_WIN_L / 2.0,
                         top + C.EYE_WIN_Z0) * bd.Box(
                2.0 * C.EYE_T, C.EYE_WIN_L, C.EYE_WIN_H,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
        else:
            win = bd.Pos(cx - C.EYE_WIN_L / 2.0, cy - C.EYE_T,
                         top + C.EYE_WIN_Z0) * bd.Box(
                C.EYE_WIN_L, 2.0 * C.EYE_T, C.EYE_WIN_H,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
        eyes.append(wall - win)
    solid = solid.fuse(*eyes).clean()
    b = solid.bounding_box()
    print(f"  after cut: Z {b.min.Z:.3f}..{b.max.Z:.3f}"
          f"  solids {len(solid.solids())}")
    return solid


def main():
    thick = float(sys.argv[1]) if len(sys.argv) > 1 else THICK
    solid = build(thick)
    b = solid.bounding_box()
    print(f"solid  X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.3f}..{b.max.Z:.3f}"
          f"   valid={solid.is_valid}  solids={len(solid.solids())}")
    vol = solid.volume
    print(f"volume {vol:.1f} mm3  ({vol / 1000:.1f} cm3,"
          f" PLA solid {vol / 1000 * 1.24:.0f} g)")
    print("export_step:", bd.export_step(solid, str(STEP_WORK)), STEP_WORK)
    ok = bd.export_stl(solid, str(STL_WORK), tolerance=0.005,
                       angular_tolerance=0.2)
    print("export_stl:", ok, STL_WORK, f"{STL_WORK.stat().st_size / 1024:.0f} kB")


if __name__ == "__main__":
    main()
