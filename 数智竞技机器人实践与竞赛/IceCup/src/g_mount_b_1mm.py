"""Whole bracket with EVERY wall reduced to 1 mm, for a fast fit print.

All positions stay identical to the real part -- the 40.5 servo gap, the four
plate holes, the four M4 holes at 48.5 x 10, the flange pocket, the bridge
height -- only the material thickness changes:

    real part          this coupon
    foot  5   ->  1
    post  5   ->  1   (X direction)
    bridge 2  ->  1
    gusset 5  ->  1

Prints in a few minutes and still shows the servo drop-in and every hole.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_mount_b as M  # noqa: E402

W = 1.0                                    # the one thickness
Z_FOOT_TOP = M.PLATE_T + M.FOOT_T          # 14, kept where the servo sits
Z_FOOT_BOT = Z_FOOT_TOP - W                # 13
POCKET_D = 0.6                             # 1.6 in the real part


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def build():
    # foot: 1 mm plate, top face left at Z 14 where the servo sits
    part = _box(M.FOOT_X[0], M.FOOT_X[1], M.FOOT_Y[0], M.FOOT_Y[1],
                Z_FOOT_BOT, Z_FOOT_TOP)
    # posts: 1 mm thick in X, same Y span and same height
    for y0, y1 in (M.POST1_Y, M.POST2_Y):
        part = part + _box(0.0, W, y0, y1, Z_FOOT_BOT, M.POST_TOP)
    # bridge: 1 mm thick, same top height
    part = part + _box(0.0, W, M.POST1_Y[0], M.POST2_Y[1],
                       M.BRIDGE[5] - W, M.BRIDGE[5])
    # gussets: same triangles, 1 mm thick
    for y_edge, sign in ((M.POST1_Y[0], -1.0), (M.POST2_Y[1], 1.0)):
        pts = [(y_edge, Z_FOOT_BOT), (y_edge + sign * M.RIB_LEG, Z_FOOT_BOT),
               (y_edge, Z_FOOT_BOT + M.RIB_LEG)]
        face = bd.Face(bd.Polyline(*[(0.0, y, z) for y, z in pts],
                                   close=True))
        # symmetric extrude then centre on X: the one-sided extrude followed
        # the face normal, which flips with the vertex order, so the front
        # gusset ended up at X -1..0 outside the wall
        prism = bd.extrude(face, amount=W / 2.0, both=True)
        part = part + bd.Pos(W / 2.0, 0.0, 0.0) * prism

    # plate holes: same 2 x 4 rows as the real part
    for hy in M.HOLE_ROWS:
        for hx in M.HOLE_X:
            part = part.cut(bd.Pos(hx, hy, Z_FOOT_BOT - 1.0) * bd.Cylinder(
                M.HOLE_D / 2.0, W + 2.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))

    # four M4 holes, unchanged positions
    for y_c in (M.POST_C1, M.POST_C2):
        for hz in (M.SERVO_Z - 5.0, M.SERVO_Z + 5.0):
            # CENTRE aligned and placed at the wall's mid-thickness: MIN align
            # plus a rotation silently puts the cutter outside the material
            part = part.cut(bd.Pos(W / 2.0, y_c, hz) * bd.Rot(0, 90, 0)
                            * bd.Cylinder(M.SCREW_D / 2.0, W + 4.0,
                                          align=(bd.Align.CENTER,
                                                 bd.Align.CENTER,
                                                 bd.Align.CENTER)))

    # flange ridge pocket on the inner face of each post
    for y0, y1 in (M.POST1_Y, M.POST2_Y):
        part = part.cut(_box(W - POCKET_D, W + 0.5, y0, y1,
                             *M.POCKET_Z))
    return part.clean()


@step(out="../newSTEP/g_mount_b_1mm.step")
def g_mount_b_1mm():
    return build()


if __name__ == "__main__":
    m = g_mount_b_1mm()
    b = m.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3")
    print(f"servo gap {M.POST2_Y[0] - M.POST1_Y[1]:.1f}   "
          f"screw Y {M.POST_C1:.2f}/{M.POST_C2:.2f}   "
          f"Z {M.SERVO_Z - 5:.0f}/{M.SERVO_Z + 5:.0f}")
