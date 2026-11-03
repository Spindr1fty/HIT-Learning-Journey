r"""g_mount_b rev 36 -- one-piece full enclosure for the 20 kg wheel servo.

Built around the servo the user measured on 2026-10-24:
    body    40 (long) x 20 (wide) x 40 (tall)
    flange  52 x 20 x 2.66 thick, mounted near the output end
    4 holes Y 26.19 / 74.19   Z 17.675 / 30.325   (48 x 12.65 pattern)

In this bracket's frame (X along the tooth plate, Y across, Z up from the
plate's underside, the servo's output pointing -X):

    body    X -2.50..37.50   Y 30.19..70.19   Z 14..34
    flange  X  4.84.. 7.50   Y 24.19..76.19   Z 14..34

The box encloses it; the BACK is wide open and sized for the FLANGE (52.6 x
20.3), because the flange is wider than the body -- that is what has to pass.
The servo goes in from the back, the flange lands on the two front posts and
4 x M4 through-holes (either direction, nut on whichever side) clamp it.

Two wall versions are exported:
    g_mount_b.step        side walls + top run to the foot's back edge (X 40)
    g_mount_b_short.step  they stop at the servo body's end (X 37.5)

Run (from src/):
    python g_mount_b.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_servo as S  # noqa: E402

# ---------------------------------------------------------------- interface --
# These come from the tooth plate / chassis and must not move.
PLATE_T = 9.0
FOOT_T = 5.0
HOLE_D = 4.5
PLATE_PITCH = 8.196
HOLE_X = [8.0 + k * PLATE_PITCH for k in range(4)]
HOLE_Y, HOLE_Y_TAIL = 19.94, 80.44
FOOT_X = (0.0, 40.0)
FOOT_Y = (12.64, 88.14)   # rev 40: flush with the 4 mm walls
FOOT_CY = 50.19

# ------------------------------------------------------- servo in this frame --
SERVO_X = 37.5
SERVO_Y = 70.19                     # -> body Y 30.19..70.19
SERVO_Z = PLATE_T + FOOT_T + 10.0   # -> body Z 14..34
BODY_X0, BODY_X1 = -2.5, 37.5
BODY_Y0, BODY_Y1 = 30.19, 70.19
BODY_Z0, BODY_Z1 = 14.0, 34.0
FLANGE_X0 = SERVO_X - S.FLANGE_Z1   # 4.84
FLANGE_X1 = SERVO_X - S.FLANGE_Z0   # 7.50
FLANGE_Y0 = FOOT_CY - S.FLANGE_SPAN / 2.0    # 24.19
FLANGE_Y1 = FOOT_CY + S.FLANGE_SPAN / 2.0    # 76.19
SCREW_Y = (FOOT_CY - S.HOLE_DX, FOOT_CY + S.HOLE_DX)   # 26.19 / 74.19
SCREW_Z = (SERVO_Z - S.HOLE_DY, SERVO_Z + S.HOLE_DY)   # 17.675 / 30.325
SCREW_D = 4.5

# ---------------------------------------------------------------------- box --
CLEAR = 0.30                        # pocket clearance (print + burr)
# rev 40: every wall 4 mm (side walls, top plate, front posts).
# The walls sit OUTBOARD of the 8 chassis bolt heads (Ø7 -> they reach
# Y 16.44 / 83.94) and run all the way down onto the foot, so the box is one
# connected piece.  The foot grows 0.3 on each side to stay flush with them.
WALL_T = 4.0
BOX_Y0, BOX_Y1 = 12.64, 88.14             # wall outer faces = foot edges
IN_Y0 = BOX_Y0 + WALL_T                   # 16.64: 0.2 clear of the bolt heads
IN_Y1 = BOX_Y1 - WALL_T                   # 84.14
IN_Z1 = BODY_Z1 + 0.60                    # 34.60: interior ceiling
BOX_Z0 = PLATE_T + FOOT_T                 # 14
BOX_Z1 = IN_Z1 + WALL_T                   # 38.60: top plate 4 mm thick

POST_W = 8.0
# rev 39: posts widened outboard so they connect the walls to the front
POST_Y = ((IN_Y0, SCREW_Y[0] + POST_W / 2.0),        # 16.14 .. 30.19
          (SCREW_Y[1] - POST_W / 2.0, IN_Y1))        # 70.19 .. 84.24
POST_X = (FLANGE_X0 - WALL_T, FLANGE_X0)   # 4 mm posts; flange lands on 4.84
WALL_X0 = 0.0                       # walls start at the foot's front edge

POCKET_DEPTH = 2.5                  # rev 29 feature: ridge relief
POCKET_W = 2.4
POCKET_Z = (SERVO_Z - POCKET_W / 2.0, SERVO_Z + POCKET_W / 2.0)


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _servo_rot():
    return bd.Rot(0, 0, -90) * bd.Rot(90, 0, 0)


def bracket(back_x=FOOT_X[1]):
    part = _box(FOOT_X[0], FOOT_X[1], FOOT_Y[0], FOOT_Y[1],
                PLATE_T, PLATE_T + FOOT_T)

    # front posts: the flange lands on their inner faces
    for y0, y1 in POST_Y:
        part = part + _box(POST_X[0], POST_X[1], y0, y1, BOX_Z0, IN_Z1)

    # side walls (3 mm) -- behind the flange nuts, bottom relieved
    for y0, y1 in ((BOX_Y0, IN_Y0), (IN_Y1, BOX_Y1)):
        part = part + _box(WALL_X0, back_x, y0, y1, BOX_Z0, IN_Z1)

    # top plate, one piece with posts and walls
    part = part + _box(POST_X[0], back_x, BOX_Y0, BOX_Y1, IN_Z1, BOX_Z1)
    part = part.clean()

    # the back is fully open: one interior that clears the flange
    part = part.cut(_box(POST_X[1] - 0.1, back_x + 1.0, IN_Y0, IN_Y1,
                         BOX_Z0, IN_Z1))

    # 4 through holes in the posts (bolt either way round)
    for cy in SCREW_Y:
        for hz in SCREW_Z:
            part = part.cut(
                bd.Pos(POST_X[0] - 0.5, cy, hz) * bd.Rot(0, 90, 0) *
                bd.Cylinder(SCREW_D / 2.0, POST_X[1] + 1.5,
                            align=(bd.Align.CENTER, bd.Align.CENTER,
                                   bd.Align.MIN)))

    # rev 29 ridge relief in the posts' inner faces
    for y0, y1 in POST_Y:
        part = part.cut(_box(POST_X[1] - POCKET_DEPTH, POST_X[1] + 0.5,
                             y0, y1, POCKET_Z[0], POCKET_Z[1]))

    # the 8 plate holes (2 rows x 4)
    for hy in (HOLE_Y, HOLE_Y_TAIL):
        for hx in HOLE_X:
            part = part.cut(bd.Pos(hx, hy, PLATE_T - 1.0) * bd.Cylinder(
                HOLE_D / 2.0, FOOT_T + 2.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    return part.clean()


def reference():
    """Tooth plate + servo + horn, for checking."""
    plate = _box(0.0, 60.0, 0.0, 24.44, 0.0, PLATE_T)
    servo = bd.Pos(SERVO_X, SERVO_Y, SERVO_Z) * _servo_rot() * S.servo_solid()
    horn = bd.Pos(SERVO_X, SERVO_Y, SERVO_Z) * _servo_rot() * S.horn_solid()
    return plate + servo + horn


@step(out="../newSTEP/g_mount_b.step")
def g_mount_b():
    # walls + top run to the foot's back edge (X 40)
    return bracket(FOOT_X[1])


@step(out="../newSTEP/g_mount_b_ref.step")
def g_mount_b_ref():
    return bd.Compound(children=[bracket(FOOT_X[1]), reference()])


if __name__ == "__main__":
    for tag, back in (("A walls->40", FOOT_X[1]),):
        p = bracket(back)
        b = p.bounding_box()
        print(f"{tag}: bbox X {b.min.X:.2f}..{b.max.X:.2f}"
              f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
        print(f"   valid={p.is_valid}  solids={len(p.solids())}"
              f"  vol {p.volume / 1000:.3f} cm3 ({p.volume / 1000 * 1.24:.0f} g)")
    print(f"servo body Y {BODY_Y0}..{BODY_Y1}  flange Y {FLANGE_Y0}..{FLANGE_Y1}"
          f"  X {FLANGE_X0}..{FLANGE_X1}")
    print(f"screws Y {SCREW_Y[0]:.3f} / {SCREW_Y[1]:.3f}"
          f"   Z {SCREW_Z[0]:.3f} / {SCREW_Z[1]:.3f}")
    print(f"interior Y {IN_Y0:.2f}..{IN_Y1:.2f}  Z {BOX_Z0}..{IN_Z1:.2f}"
          f"  (back open)")
