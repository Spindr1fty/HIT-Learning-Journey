"""Concept robot for the HIT curling match, in its own frame.

Origin at the chassis centre on the ground, +X forward (the direction it
pushes a stone), +Z up. Every dimension traces to a constraint:

  footprint 300x300        rules cap the vertical projection at 350x350
  wheel Ø53.6 x 25.56      Whells.dxf, the Mecanum set on hand
  mast stroke 350          208.5 mm of rack travel plus headroom for the
                           unmeasured platform height H (see venue_spec)
  jaw thickness 14         cell gives 16.5 mm per side at Ø47 nominal
  blade top 13             pusher band 10.4-12.5 mm from the three belt-height
                           sources, blade sits across that window

Six DOF total: holonomic base (3), mast Y slide (1), mast Z (1), jaw (1).
No arm, no IK -- the pick is "drive up, straight down, close".
"""

from cadgen import build123d as bd
from cadgen import step

import spec

# --- chassis ---
CHASSIS = 300.0
CHASSIS_T = 5.0
CHASSIS_Z0 = 56.0          # must clear the wheel top at 53.6
WHEEL_D = 53.6
WHEEL_W = 25.56
WHEEL_XY = 120.0
BORE_D = 5.9

# --- mast / head ---
MAST_X = 130.0
MAST_W = 40.0
MAST_STROKE = 350.0
Y_SLIDE_TRAVEL = 100.0
HEAD_W = 90.0
JAW_T = 14.0          # thickness along Y, must fit the 16.5 mm side gap
JAW_L = 40.0          # reach along X; 40 mm past the rack face lands on the
                      # stone centre when the chassis stops 5 mm off the face
JAW_H = 25.0
JAW_OPEN = 62.0       # gap between jaw faces, open
JAW_CLOSED = 45.0     # gap when gripping the Ø46-47 belt

# --- pusher blade ---
BLADE_W = 60.0
BLADE_T = 8.0
BLADE_Z0 = 8.0
BLADE_Z1 = 13.0

def _colors():
    """Built lazily: cadgen forbids touching the kernel at module level."""
    return {
        "grey": bd.Color(0.55, 0.57, 0.60),
        "dark": bd.Color(0.20, 0.20, 0.22),
        "orange": bd.Color(0.85, 0.45, 0.10),
    }


def _box(x0, x1, y0, y1, z0, z1, label, colour=None):
    b = bd.Box(x1 - x0, y1 - y0, z1 - z0,
               align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    b = bd.Pos(x0, y0, z0) * b
    b.color = colour if colour is not None else _colors()["grey"]
    b.label = label
    return b


def _wheel(x, y):
    c = _colors()
    w = bd.Cylinder(WHEEL_D / 2, WHEEL_W,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    w -= bd.Cylinder(BORE_D / 2, WHEEL_W + 2,
                     align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)) \
        .moved(bd.Location((0, 0, -1)))
    w = bd.Rot(-90, 0, 0) * w
    w = bd.Pos(x, y - WHEEL_W / 2, WHEEL_D / 2) * w
    w.color = c["dark"]
    w.label = f"wheel_{x:+.0f}_{y:+.0f}"
    return w


def robot(jaw_gap: float = JAW_OPEN, head_z: float = 128.5,
          blade_folded: bool = False) -> bd.Shape:
    c = _colors()
    parts = [
        _box(-CHASSIS / 2, CHASSIS / 2, -CHASSIS / 2, CHASSIS / 2,
             CHASSIS_Z0, CHASSIS_Z0 + CHASSIS_T, "chassis_plate"),
        _box(-90, -20, -35, 35, CHASSIS_Z0 + CHASSIS_T, CHASSIS_Z0 + CHASSIS_T + 25,
             "battery_box", c["dark"]),
        _box(-15, 60, -35, 20, CHASSIS_Z0 + CHASSIS_T, CHASSIS_Z0 + CHASSIS_T + 15,
             "main_board", c["dark"]),
    ]
    parts += [_wheel(sx * WHEEL_XY, sy * WHEEL_XY) for sx in (1, -1) for sy in (1, -1)]

    # Y slide: a plate the mast rides on, spanning the +-100 travel
    parts.append(_box(MAST_X - 30, MAST_X + 30,
                      -Y_SLIDE_TRAVEL - 40, Y_SLIDE_TRAVEL + 40,
                      CHASSIS_Z0 + CHASSIS_T, CHASSIS_Z0 + CHASSIS_T + 8,
                      "y_slide_rail", c["dark"]))

    z0 = CHASSIS_Z0 + CHASSIS_T + 8
    parts.append(_box(MAST_X - MAST_W / 2, MAST_X + MAST_W / 2,
                      -MAST_W / 2, MAST_W / 2, z0, z0 + MAST_STROKE + 60,
                      "mast_column"))

    # head carriage + two jaws closing along Y
    hz = max(z0, head_z)
    parts.append(_box(MAST_X - 25, MAST_X + 25, -HEAD_W / 2, HEAD_W / 2,
                      hz, hz + 30, "head_carriage", c["orange"]))
    for sign, tag in ((1, "far"), (-1, "near")):
        y_in = sign * jaw_gap / 2
        y_out = y_in + sign * JAW_T
        parts.append(_box(MAST_X + 20, MAST_X + 20 + JAW_L,
                          min(y_in, y_out), max(y_in, y_out),
                          hz - JAW_H, hz, f"jaw_{tag}", c["orange"]))

    # pusher blade on the front face, hung from a bracket off the chassis edge;
    # folded lies flat against the front so it clears the rack face while picking
    parts.append(_box(CHASSIS / 2 - 5, CHASSIS / 2 + 3, -10, 10,
                      BLADE_Z1, CHASSIS_Z0, "blade_bracket", c["dark"]))
    if blade_folded:
        parts.append(_box(CHASSIS / 2, CHASSIS / 2 + BLADE_T,
                          -BLADE_W / 2, BLADE_W / 2, BLADE_Z0, BLADE_Z0 + 40,
                          "push_blade_folded", c["orange"]))
    else:
        parts.append(_box(CHASSIS / 2 - 5, CHASSIS / 2 + BLADE_T,
                          -BLADE_W / 2, BLADE_W / 2, BLADE_Z0, BLADE_Z1,
                          "push_blade", c["orange"]))

    return bd.Compound(children=parts, label="robot")


@step(out="../oldSTEP/robot.step")
def robot_model():
    return robot()


if __name__ == "__main__":
    r = robot_model()
    b = r.bounding_box()
    print(f"footprint {b.max.X - b.min.X:.1f} x {b.max.Y - b.min.Y:.1f} mm"
          f"  (limit {spec.ROBOT_FOOTPRINT})")
    print(f"height {b.max.Z:.1f} mm (unlimited by rules)  solids={len(r.solids())}"
          f"  valid={r.is_valid}")
