r"""Semi-closed variants on the ACTUAL Desktop g_mount_b.SLDASM base.

The Desktop assembly imports g_mount_b.step (rev30 saddle), NOT the later box:
    foot    X 0..40, Y 12.94..87.44, Z 9..14
    posts   X 0..5, Y 21.94..29.94 / 70.44..78.44, Z 14..37
    beam    X 0..5, Y 21.94..78.44, Z 35..38
    opening Y 29.94..70.44, Z 14..35  (servo body 40 x 40 x 20 goes through)
    volume 16.569 cm3

Servo body in this frame: X -2.5..37.5, Y 30.19..70.19, Z 14..34.
The servo is pushed in from +X: body through the opening, flange stops on the
front posts.  A rear wall therefore needs a 40.5 x 21 body window.

A  rear portal only (mirror of the front arch at X 37..40)
B  rear portal + two side walls (U tunnel, top open)
C  rear portal + side walls + top cover (box, front shaft + rear body window)
D  half-length top cover only (front beam extended 17.5 mm)

Pure ASCII on purpose.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "newSTEP"
BASE = OUT / "g_mount_b_desktop_base.step"

# --- measured from the Desktop STEP / rev30 drawing --------------------------
X0, X1 = 0.0, 40.0
Y0, Y1 = 12.94, 87.44
Z0, Z1 = 9.0, 38.0
FOOT_TOP = 14.0
POST_X = (0.0, 5.0)
POST_Y = ((21.94, 29.94), (70.44, 78.44))
OPEN_Y = (29.94, 70.44)
OPEN_Z = (14.0, 35.0)
BEAM_Z = (35.0, 38.0)
OV = 0.50

REAR_X = (37.5, 40.0)              # 2.5 mm rear frame, right behind the servo tail
SIDE_T = 3.0
# The flange is 52 wide (Y 24.19..76.19) and is pushed in from +X, so the
# side panels must sit OUTSIDE it: 0.5 clearance each side.
FLANGE_Y = (24.19, 76.19)
SIDE_CLR = 0.50
SIDE_IN_Y = (FLANGE_Y[0] - SIDE_CLR, FLANGE_Y[1] + SIDE_CLR)   # 23.69 / 76.69
SIDE_OUT_Y = (SIDE_IN_Y[0] - SIDE_T, SIDE_IN_Y[1] + SIDE_T)    # 20.69 / 79.69
# Start behind the flange + nut stack (flange back face 7.5; M4 nut ~3.2,
# washer ~1) so the four flange bolts stay accessible.
SIDE_X0 = 12.0
# Start above the 8 foot screws (M4 head + washer top ~18) so the foot
# screws stay accessible; the side panel covers only the upper body sides.
SIDE_Z0 = 19.0
TOP_Z = BEAM_Z

# Rear portal window is 44 x 21, not the bare 40.5 x 21: the extra 2 mm each
# side lets the servo wires come out of the body tail.
REAR_WIN_Y = (28.19, 72.19)
REAR_POST_Y = ((21.94, REAR_WIN_Y[0]), (REAR_WIN_Y[1], 78.44))


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def base():
    return bd.import_step(str(BASE))


def rear_portal(p):
    """Rear arch: 44 x 21 window (2 mm wire clearance each side)."""
    x0, x1 = REAR_X
    parts = [
        _box(x0, x1, y0, y1, FOOT_TOP - OV, Z1) for y0, y1 in REAR_POST_Y
    ]
    parts.append(_box(x0, x1, POST_Y[0][0], POST_Y[1][1],
                      BEAM_Z[0], BEAM_Z[1]))
    return p.fuse(*parts).clean()


def side_walls(p):
    parts = [
        _box(SIDE_X0, REAR_X[1], y0, y1, SIDE_Z0, TOP_Z[0] + OV)
        for y0, y1 in ((SIDE_OUT_Y[0], SIDE_IN_Y[0]),
                       (SIDE_IN_Y[1], SIDE_OUT_Y[1]))
    ]
    return p.fuse(*parts).clean()


def top_cover(p):
    # covers the side walls (and overhangs the two beams by 1.25 each side)
    return p.fuse(_box(POST_X[1] - OV, REAR_X[1], SIDE_OUT_Y[0], SIDE_OUT_Y[1],
                       TOP_Z[0], TOP_Z[1])).clean()


def a():
    p = rear_portal(base())
    p.label = "desktop_A"
    return p


def b():
    p = side_walls(rear_portal(base()))
    p.label = "desktop_B"
    return p


def c():
    p = top_cover(side_walls(rear_portal(base())))
    p.label = "desktop_C"
    return p


def d():
    p = base().fuse(_box(POST_X[1] - OV, 22.0, POST_Y[0][0], POST_Y[1][1],
                         TOP_Z[0], TOP_Z[1])).clean()
    p.label = "desktop_D"
    return p


VARIANTS = [("A", a), ("B", b), ("C", c), ("D", d)]


if __name__ == "__main__":
    ref = base().volume / 1000.0
    print(f"base: vol {ref:.3f} cm3 ({ref * 1.24:.1f} g)")
    for name, fn in VARIANTS:
        p = fn()
        bb = p.bounding_box()
        print(f"{name}: bbox X {bb.min.X:.2f}..{bb.max.X:.2f}"
              f"  Y {bb.min.Y:.2f}..{bb.max.Y:.2f}"
              f"  Z {bb.min.Z:.2f}..{bb.max.Z:.2f}"
              f"  valid={p.is_valid}  solids={len(p.solids())}")
        print(f"   vol {p.volume / 1000:.3f} cm3"
              f" ({p.volume / 1000 * 1.24:.1f} g)"
              f"   added {p.volume / 1000 - ref:+.3f} cm3"
              f" ({(p.volume / 1000 - ref) * 1.24:+.1f} g)")
        out = OUT / f"g_mount_b_desktop_{name}.step"
        print("   step:", bd.export_step(p, str(out)), out)
