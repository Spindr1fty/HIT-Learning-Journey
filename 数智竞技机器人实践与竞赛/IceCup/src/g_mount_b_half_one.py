r"""g_mount_b_rack_3mm -- one-piece semi-closed back, four variants.

Base: the 3 mm rack bracket the user's g_mount_b.SLDASM points at.
The servo (40 x 20 body, 52 x 20 flange) has to slide in from the back, so
the smallest possible one-piece opening is the flange envelope plus 0.3:
52.6 (Y) x 20.6 (Z).  Every variant keeps that window; they differ in how
much structure is added around it.

V1  shallow strips: 3 mm rear strips, flush with X=40
V2  triangular buttresses: 8 mm deep at the bottom, sloping to the top
V3  full rear plate: 3 mm plate at X 40..43 with the flange window
V4  rear hood: V1 + 6 mm rearward roof/side cheeks, bottom open

Pure ASCII on purpose.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b as M  # noqa: E402

# --- same mutations as g_mount_b_3mm_rack.py --------------------------------
T = 3.0
M.WALL_T = T
M.IN_Y0 = M.BOX_Y0 + T
M.IN_Y1 = M.BOX_Y1 - T
M.BOX_Z1 = M.IN_Z1 + T
M.POST_X = (M.FLANGE_X0 - T, M.FLANGE_X0)
M.PLATE_T = 11.0
M.FOOT_T = T
M.LEG_T = T

OUT = Path(__file__).resolve().parent.parent / "newSTEP"

BACK = M.FOOT_X[1]                 # 40
CLR = 0.30
WIN_Y0 = M.FLANGE_Y0 - CLR         # 23.89
WIN_Y1 = M.FLANGE_Y1 + CLR         # 76.49
WIN_Z0 = M.BODY_Z0 - CLR           # 13.70
WIN_Z1 = M.BODY_Z1 + CLR           # 34.30
OV = 0.50                          # fusion overlap

# outer box faces at the back
OY0, OY1 = M.BOX_Y0, M.BOX_Y1      # 12.64 .. 88.14
OZ0, OZ1 = M.PLATE_T, M.BOX_Z1     # 11 .. 37.60
IZ0, IZ1 = M.BOX_Z0, M.IN_Z1       # 14 .. 34.60


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def base():
    return M.bracket(M.FOOT_X[1])


def _strips(depth):
    """Solid rear side webs, outside the 52.6 x 20.6 flange envelope."""
    out = []
    for y0, y1 in ((M.IN_Y0 - OV, WIN_Y0),
                   (WIN_Y1, M.IN_Y1 + OV)):
        out.append(_box(BACK - depth, BACK, y0, y1,
                        IZ0 - OV, IZ1 + OV))
    return out


def v1():
    p = base().fuse(*_strips(T)).clean()
    p.label = "halfone_v1"
    return p


def v2():
    # right triangle in XZ: (32,14) -> (40,14) -> (40,34.6), 8.25 wide.
    # The vertical rear face keeps the 52.6 window; the slope is the brace.
    tris = []
    leg = 8.0
    zb, zt = IZ0 - OV, IZ1 + OV
    for y0, y1 in ((M.IN_Y0 - OV, WIN_Y0),
                   (WIN_Y1, M.IN_Y1 + OV)):
        pts = [(BACK - leg, y0, zb), (BACK, y0, zb), (BACK, y0, zt)]
        face = bd.Face(bd.Wire.make_polygon(pts, close=True))
        tri = bd.extrude(face, amount=(y1 - y0), dir=(0, 1, 0))
        tris.append(tri)
    p = base().fuse(*tris).clean()
    p.label = "halfone_v2"
    return p


def v3():
    plate = _box(BACK - OV, BACK + 3.0, OY0, OY1, OZ0, OZ1)
    p = base().fuse(plate).clean()
    window = _box(BACK - 1.0, BACK + 4.0, WIN_Y0, WIN_Y1,
                  WIN_Z0, WIN_Z1)
    p = p.cut(window).clean()
    p.label = "halfone_v3"
    return p


def v4():
    depth = 6.0
    hood_top = _box(BACK - OV, BACK + depth, OY0, OY1, IZ1, OZ1)
    hood_l = _box(BACK - OV, BACK + depth, OY0, M.IN_Y0, IZ0 - OV, OZ1)
    hood_r = _box(BACK - OV, BACK + depth, M.IN_Y1, OY1, IZ0 - OV, OZ1)
    p = base().fuse(*_strips(T)).fuse(hood_top, hood_l, hood_r).clean()
    p.label = "halfone_v4"
    return p


VARIANTS = [("v1", v1), ("v2", v2), ("v3", v3), ("v4", v4)]


def report(name, p, ref_vol):
    b = p.bounding_box()
    print(f"{name}: bbox X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}  Z {b.min.Z:.2f}..{b.max.Z:.2f}"
          f"  valid={p.is_valid}  solids={len(p.solids())}")
    print(f"   vol {p.volume / 1000:.3f} cm3 ({p.volume / 1000 * 1.24:.1f} g)"
          f"   added {p.volume / 1000 - ref_vol:+.3f} cm3"
          f" ({(p.volume / 1000 - ref_vol) * 1.24:+.1f} g)")


if __name__ == "__main__":
    b0 = base()
    ref = b0.volume / 1000.0
    report("base", b0, ref)
    for name, fn in VARIANTS:
        p = fn()
        report(name, p, ref)
        out = OUT / f"g_mount_b_halfone_{name}.step"
        print("   step:", bd.export_step(p, str(out)), out)
