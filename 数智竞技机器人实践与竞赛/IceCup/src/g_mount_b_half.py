r"""g_mount_b -- four semi-enclosed options, geometry only.

Base part is the current rev55 bracket (open back, arch base).  Each option
adds the minimum needed to read the idea; fasteners are shown as holes, not
modelled.

A  one-piece: two 4 mm strips close the back to 52.6 x 20.6 (flange width)
B  full 3 mm back cover, 24 x 12 wire window, 4 x M3 into corner blocks
C  same cover, 40 x 20 window (servo tail exposed)
D  back stays fully open, two 20 x 12 windows in the side walls

Exports STEP only; renders are done by cadgen snapshot.

Pure ASCII on purpose.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b as M  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "newSTEP"
BACK = M.FOOT_X[1]                    # 40
FLANGE_CLR = 0.30
COVER_T = 3.0
COVER_X0, COVER_X1 = BACK, BACK + COVER_T
COVER_Y0, COVER_Y1 = M.BOX_Y0, M.BOX_Y1
COVER_Z0, COVER_Z1 = M.PLATE_T, M.BOX_Z1     # 9 .. 38.6

WIN_B = (24.0, 12.0)                  # Y, Z
WIN_C = (40.0, 20.0)

BLOCK_T = 4.0
BLOCK_Z = 8.0
BLOCK_YW = M.FLANGE_Y0 - FLANGE_CLR  # 23.89 inner face
BLOCK_YW2 = M.FLANGE_Y1 + FLANGE_CLR  # 76.49
SCREW_D = 3.4


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _cyl_x(x0, x1, cy, cz, dia):
    return bd.Pos((x0 + x1) / 2.0, cy, cz) * bd.Rot(0, 90, 0) * bd.Cylinder(
        dia / 2.0, x1 - x0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))


def base():
    return M.bracket(M.FOOT_X[1])


# ------------------------------------------------------------------ option A --
def option_a():
    p = base()
    y1 = M.FLANGE_Y0 - FLANGE_CLR
    y2 = M.FLANGE_Y1 + FLANGE_CLR
    strips = [
        _box(BACK - BLOCK_T, BACK, M.IN_Y0 - 0.5, y1,
             M.BOX_Z0 - 0.5, M.IN_Z1 + 0.5),
        _box(BACK - BLOCK_T, BACK, y2, M.IN_Y1 + 0.5,
             M.BOX_Z0 - 0.5, M.IN_Z1 + 0.5),
    ]
    p = p.fuse(*strips).clean()
    p.label = "half_A"
    return p


# -------------------------------------------------------------- options B/C --
def _blocks():
    """Four corner blocks in the back opening, 0.3 clear of the flange."""
    out = []
    for y0, y1 in ((M.IN_Y0 - 0.5, BLOCK_YW),
                   (BLOCK_YW2, M.IN_Y1 + 0.5)):
        out.append(_box(BACK - BLOCK_T, BACK, y0, y1,
                        M.BOX_Z0 - 0.5, M.BOX_Z0 + BLOCK_Z))
        out.append(_box(BACK - BLOCK_T, BACK, y0, y1,
                        M.IN_Z1 - BLOCK_Z, M.IN_Z1 + 0.5))
    return out


def _screws():
    ys = ((M.IN_Y0 - 0.5 + BLOCK_YW) / 2.0,
          (BLOCK_YW2 + M.IN_Y1 + 0.5) / 2.0)
    zs = (M.BOX_Z0 + BLOCK_Z / 2.0, M.IN_Z1 - BLOCK_Z / 2.0)
    return [(y, z) for y in ys for z in zs]


def _cover(win):
    plate = _box(COVER_X0, COVER_X1, COVER_Y0, COVER_Y1,
                 COVER_Z0, COVER_Z1)
    wy, wz = win
    plate = plate.cut(_box(COVER_X0 - 1.0, COVER_X1 + 1.0,
                           M.FOOT_CY - wy / 2.0, M.FOOT_CY + wy / 2.0,
                           M.SERVO_Z - wz / 2.0, M.SERVO_Z + wz / 2.0))
    for y, z in _screws():
        plate = plate.cut(_cyl_x(COVER_X0 - 0.5, COVER_X1 + 0.5,
                                 y, z, SCREW_D))
    plate = plate.clean()
    plate.label = "cover"
    return plate


def _base_with_blocks():
    p = base().fuse(*_blocks()).clean()
    for y, z in _screws():
        p = p.cut(_cyl_x(BACK - BLOCK_T - 1.0, BACK + 1.0,
                         y, z, SCREW_D))
    p = p.clean()
    p.label = "bracket"
    return p


def option_b(win=WIN_B):
    p = _base_with_blocks()
    c = _cover(win)
    return bd.Compound(children=[p, c])


def option_b_exploded(win=WIN_B, dx=30.0):
    p = _base_with_blocks()
    c = bd.Pos(dx, 0, 0) * _cover(win)
    return bd.Compound(children=[p, c])


# ------------------------------------------------------------------ option D --
def option_d():
    p = base()
    cuts = [
        _box(12.0, 32.0, M.BOX_Y0 - 1.0, M.IN_Y0 + 1.0, 18.0, 30.0),
        _box(12.0, 32.0, M.IN_Y1 - 1.0, M.BOX_Y1 + 1.0, 18.0, 30.0),
    ]
    p = p.cut(*cuts).clean()
    p.label = "half_D"
    return p


def _report(name, p):
    b = p.bounding_box()
    print(f"{name}: X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}"
          f"  valid={p.is_valid}  solids={len(p.solids())}"
          f"  vol {p.volume / 1000:.3f} cm3")


if __name__ == "__main__":
    parts = [
        ("g_mount_b_half_A", option_a()),
        ("g_mount_b_half_B", option_b()),
        ("g_mount_b_half_B_exploded", option_b_exploded()),
        ("g_mount_b_half_C", option_b(WIN_C)),
        ("g_mount_b_half_D", option_d()),
    ]
    for name, p in parts:
        _report(name, p)
        out = OUT / f"{name}.step"
        print("  step:", bd.export_step(p, str(out)), out)
