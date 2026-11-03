"""Option A: servo sits on top of the 9 mm tooth plate, shaft pointing at the
toothed edge, flange bolted to a vertical wall that stands on a foot.

Plate local frame: X 0..242.7 along the length, Y 0..24.44 across, Z 0..9 thick,
teeth on the Y=0 edge, hole row at Y=19.94.

Reference only (not printed): the plate stub and the servo stand-in.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_servo as S  # noqa: E402

PLATE_L = 242.70
PLATE_W = 24.44
PLATE_T = 9.0
HOLE_Y = 19.94
HOLE_D = 4.5

FOOT_T = 5.0
FOOT_Z0 = PLATE_T
FOOT_Z1 = PLATE_T + FOOT_T
WALL_Y0 = -3.06
WALL_Y1 = 1.94
WALL_T = WALL_Y1 - WALL_Y0

# servo placement: rotated so the shaft points -Y, base at Y=24.44, body centre
# at Z = 24 so the body spans Z 14..34 and sits on the foot.
SERVO_Y = PLATE_W
SERVO_Z = FOOT_Z1 + 10.0
SHAFT_X = S.BODY_X / 2.0 + S.SHAFT_X_OFF      # 30 in the servo's own frame

# flange plane ends up at Y = SERVO_Y - 30 = -5.56
FLANGE_Y = SERVO_Y - S.FLANGE_Z0


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def bracket():
    # foot on the plate's top face, reaching back to the hole row
    foot = _box(-8.0, 48.0, 0.0, PLATE_W, FOOT_Z0, FOOT_Z1)

    # vertical wall pair either side of the servo body, plus a top bridge
    x_hole0 = SHAFT_X - S.HOLE_DX - 2.0       # 3.75
    x_hole1 = SHAFT_X + S.HOLE_DX + 2.0       # 56.25
    left = _box(x_hole0 - 6.0, x_hole0 + 6.0, WALL_Y0, WALL_Y1,
                FOOT_Z1, FOOT_Z1 + 24.0)
    right = _box(x_hole1 - 6.0, x_hole1 + 6.0, WALL_Y0, WALL_Y1,
                 FOOT_Z1, FOOT_Z1 + 24.0)
    bridge = _box(x_hole0 - 6.0, x_hole1 + 6.0, WALL_Y0, WALL_Y1,
                  FOOT_Z1 + 20.0, FOOT_Z1 + 24.0)
    part = foot + left + right + bridge

    # flange slots
    for hx, hy, _ in S.hole_centres():
        cx = hx - S.BODY_X / 2.0 + SHAFT_X
        cz = FOOT_Z1 + 10.0
        hole = bd.Pos(cx, (WALL_Y0 + WALL_Y1) / 2.0, cz - 5.0) * bd.Cylinder(
            S.HOLE_D / 2.0, WALL_T + 2.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        part = part.cut(hole)
        hole2 = bd.Pos(cx, (WALL_Y0 + WALL_Y1) / 2.0, cz + 5.0) * bd.Cylinder(
            S.HOLE_D / 2.0, WALL_T + 2.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        part = part.cut(hole2)

    # plate fixing holes (2 of the 29)
    for px in (20.0, 36.39):
        part = part.cut(bd.Pos(px, HOLE_Y, FOOT_Z0 - 1.0) * bd.Cylinder(
            HOLE_D / 2.0, FOOT_T + 2.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    return part.clean()


def assembly():
    plate = _box(0.0, 60.0, 0.0, PLATE_W, 0.0, PLATE_T)
    servo = bd.Pos(0.0, SERVO_Y, SERVO_Z) * bd.Rot(90, 0, 0) * S.servo_solid()
    horn = bd.Pos(0.0, SERVO_Y, SERVO_Z) * bd.Rot(90, 0, 0) * S.horn_solid()
    return plate + servo + horn + bracket()


@step(out="../newSTEP/g_mount_a.step")
def g_mount_a():
    return assembly()


if __name__ == "__main__":
    m = g_mount_a()
    b = m.bounding_box()
    print(f"bbox X {b.max.X - b.min.X:.2f}  Y {b.max.Y - b.min.Y:.2f}"
          f"  Z {b.max.Z - b.min.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3")
    print()
    print("plate stub X 0..60, Y 0..24.44, Z 0..9")
    print(f"servo base at Y {SERVO_Y:.2f}, body centre Z {SERVO_Z:.2f}")
    print(f"flange plane at Y {FLANGE_Y:.2f}")
    print(f"bracket foot Z {FOOT_Z0:.0f}..{FOOT_Z1:.0f}, wall Y {WALL_Y0:.2f}..{WALL_Y1:.2f}")
    print(f"flange screws 4 x M4 on {S.FLANGE_SPAN} x {S.FLANGE_TAB_W}"
          f"   shaft offset +{S.SHAFT_X_OFF:.0f} from pattern centre")

