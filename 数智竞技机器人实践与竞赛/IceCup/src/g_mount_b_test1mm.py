"""Fast fit coupon: the WHOLE bracket at 1 mm thick.

Not a flattened plate and not a shell (OCP's offset refused this shape): this
rebuilds the bracket's full side profile -- foot, both posts, top bridge,
gussets -- as a 1 mm slab in X, with the four screw holes drilled through it.
It prints in minutes and lets you check:
  - the 40.5 gap the servo body drops into
  - the four screw hole positions (48.5 apart, 10 apart)
  - the foot's depth and the top bridge height
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_mount_b as M  # noqa: E402

T = 1.0                                   # slab thickness, along X


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def coupon():
    z_foot = M.PLATE_T + M.FOOT_T          # 14
    # foot, posts, bridge: all 1 mm thick in X
    part = _box(0.0, T, M.FOOT_Y[0], M.FOOT_Y[1], M.PLATE_T, z_foot)
    for y0, y1 in (M.POST1_Y, M.POST2_Y):
        part = part + _box(0.0, T, y0, y1, z_foot, M.POST_TOP)
    part = part + _box(0.0, T, M.POST1_Y[0], M.POST2_Y[1],
                       M.BRIDGE[4], M.BRIDGE[5])
    # gussets: flat triangles in the Y-Z plane
    for y_edge, sign in ((M.POST1_Y[0], -1.0), (M.POST2_Y[1], 1.0)):
        poly = [(y_edge, z_foot - 0.5),
                (y_edge + sign * M.RIB_LEG, z_foot - 0.5),
                (y_edge, z_foot - 0.5 + M.RIB_LEG)]
        face = bd.Face(bd.Polyline(*[(0.0, y, z) for y, z in poly],
                                   close=True))
        part = part + bd.extrude(face, amount=T)
    # four screw holes through the slab
    for yc in (M.POST_C1, M.POST_C2):
        for hz in (M.SERVO_Z - 5.0, M.SERVO_Z + 5.0):
            part = part.cut(bd.Pos(-1.0, yc, hz) * bd.Rot(0, 90, 0)
                            * bd.Cylinder(M.SCREW_D / 2.0, T + 2.0,
                                          align=(bd.Align.MIN, bd.Align.CENTER,
                                                 bd.Align.CENTER)))
    return part.clean()


@step(out="../newSTEP/g_mount_b_test1mm.step")
def g_mount_b_test1mm():
    return coupon()


if __name__ == "__main__":
    m = g_mount_b_test1mm()
    b = m.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3")
    print(f"servo gap between posts: {M.POST2_Y[0] - M.POST1_Y[1]:.1f} mm")
