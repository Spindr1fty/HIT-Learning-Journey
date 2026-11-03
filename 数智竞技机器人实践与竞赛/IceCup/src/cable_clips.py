r"""Cable-retention clip coupon -- four designs on one printable plate.

The user rejected the round posts.  The primary design follows his sketch: a
plan-view J-hook wall (a U with an inward return lip) that a cable bundle is
dropped into from above.  Three alternatives are on the same plate so he can
compare them in SolidWorks / on the bench:

    1  J-hook          plan U + return lip, 18 x 15, 12 tall
    2  snap C-clip     C wall, 6.5 mouth, 11 x 9 pocket, 12 tall
    3  zip-tie eye     flat wall with an 8 x 5 window, 18 x 3, 12 tall
    4  comb            30 x 8 wall with three 4 mm slots, 12 tall

Everything is a vertical wall extruded in Z, so the whole coupon prints
upright with no supports.  The plate is 5 mm thick with its top at Z = 0 and
the material below, matching the chassis convention.

Run (from src/):
    uvx --from "cadgen==0.7.21" python cable_clips.py
writes
    ..\newSTEP\cable_clips_coupon.step
    ..\newSTEP\cable_clips_coupon.stl
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

PLATE_W, PLATE_H, PLATE_T = 170.0, 120.0, 5.0
STEP_OUT = Path(__file__).resolve().parent.parent / "newSTEP" / "cable_clips_coupon.step"
STL_OUT = Path(__file__).resolve().parent.parent / "newSTEP" / "cable_clips_coupon.stl"

ALIGN_MIN = (bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0, align=ALIGN_MIN)


def j_hook():
    """Plan U (18 x 15, wall 2.5) + a thin top wall and a short inner leg.

    The opening is 9 mm wide at the top-left; a cable is dropped in from above
    and the L-shaped return wraps its right side.  Nothing is thicker than the
    2.5 mm wall, so the plan reads like the user's sketch.
    """
    t, h = 2.5, 12.0
    xo, yo = 9.0, 7.5
    part = _box(-xo, xo, -yo, yo, -0.3, h)
    part = part - _box(-xo + t, xo - t, -yo + t, yo + 1.0, -1.0, h + 1.0)
    part = part + _box(2.5, xo - t, 5.0, yo, -0.3, h)      # top return
    part = part + _box(2.5, 5.0, -1.0, 5.0, -0.3, h)       # inner leg
    return part


def snap_c():
    """Plan C, 16 x 14; pocket 11 x 9, mouth 6.5, wall 2.5, 12 tall."""
    t, h = 2.5, 12.0
    xo, yo, px, py, mouth = 8.0, 7.0, 5.5, 4.5, 6.5
    part = _box(-xo, xo, -yo, yo, -0.3, h)
    part = part - _box(-px, px, -py, py, -1.0, h + 1.0)
    part = part - _box(-mouth / 2.0, mouth / 2.0, py, yo + 1.0, -1.0, h + 1.0)
    return part


def zip_eye():
    """Flat wall 18 x 3 x 12 with an 8 x 5 window for a zip tie."""
    w, t, h = 18.0, 3.0, 12.0
    ww, wh, z0 = 8.0, 5.0, 4.0
    part = _box(-w / 2.0, w / 2.0, -t / 2.0, t / 2.0, -0.3, h)
    part = part - _box(-ww / 2.0, ww / 2.0, -t, t, z0, z0 + wh)
    return part


def comb():
    """30 x 8 foot + a 3 mm wall with three 4 mm slots down to Z = 6."""
    w, fd, fh, wt, h, sz = 30.0, 8.0, 2.0, 3.0, 12.0, 6.0
    part = _box(-w / 2.0, w / 2.0, -fd / 2.0, fd / 2.0, -0.3, fh)
    part = part + _box(-w / 2.0, w / 2.0, -wt / 2.0, wt / 2.0, -0.3, h)
    for cx in (-7.0, 0.0, 7.0):
        part = part - _box(cx - 2.0, cx + 2.0, -wt, wt, sz, h + 1.0)
    return part


def plate():
    p = bd.Pos(0, 0, -PLATE_T) * bd.Box(
        PLATE_W, PLATE_H, PLATE_T, align=ALIGN_MIN)
    try:
        p = p.fillet(5.0, p.edges().filter_by(bd.Axis.Z))
    except Exception as exc:
        print("plate corner fillet skipped:", exc)
    return p


def pip(x, y):
    return _box(x - 1.0, x + 1.0, y - 1.0, y + 1.0, -0.3, 1.5)


STATIONS = [
    (j_hook(), 45.0, 90.0, 1),
    (snap_c(), 120.0, 90.0, 2),
    (zip_eye(), 45.0, 35.0, 3),
    (comb(), 125.0, 35.0, 4),
]


def build():
    parts = [plate()]
    for shape, cx, cy, _ in STATIONS:
        parts.append(bd.Pos(cx, cy, 0) * shape)
    pip_rows = [
        [(45.0, 68.0)],
        [(116.0, 68.0), (120.0, 68.0)],
        [(41.0, 16.0), (45.0, 16.0), (49.0, 16.0)],
        [(119.0, 16.0), (123.0, 16.0), (127.0, 16.0), (131.0, 16.0)],
    ]
    for row in pip_rows:
        for x, y in row:
            parts.append(pip(x, y))
    solid = parts[0].fuse(*parts[1:]).clean()
    return solid


def main():
    solid = build()
    b = solid.bounding_box()
    print(f"solid X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}"
          f"  valid={solid.is_valid}  solids={len(solid.solids())}")
    print(f"volume {solid.volume:.1f} mm3"
          f"  ({solid.volume / 1000:.1f} cm3,"
          f" PLA solid {solid.volume / 1000 * 1.24:.0f} g)")
    print("export_step:", bd.export_step(solid, str(STEP_OUT)), STEP_OUT)
    ok = bd.export_stl(solid, str(STL_OUT), tolerance=0.005,
                       angular_tolerance=0.2)
    print("export_stl:", ok, STL_OUT,
          f"{STL_OUT.stat().st_size / 1024:.0f} kB")


if __name__ == "__main__":
    main()
