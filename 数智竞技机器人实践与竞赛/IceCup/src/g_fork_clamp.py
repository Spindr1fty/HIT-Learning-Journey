r"""Fork bracket: a plain slotted plate that bolts to the servo mount's collar.

WHY THERE IS NO COLLAR ANY MORE
Version 1 had its own clamp collar. The carriage is only 60 mm long, and the
servo mount's collar already occupies Z 140..180 of it. A second collar at
Z 148..182 overlapped the first by 32 mm -- 40 + 34 = 74 mm of collar on a 60 mm
carriage. Neither could be fitted. The carriage is the scarce resource, so there
is exactly ONE collar, and this part hangs off it.

The first version also buried its slots in the collar: slots ran to Z 160 while
the collar started at 148, so the top 12 mm of travel was inside solid material
and unreachable by a screw.

HOW IT ATTACHES
Four M4 screws through the fixed holes here, into blind self-tapping holes in
the servo mount's collar's +X face. Blind, because the collar's wall is 6 mm and
behind it is the rail bore -- a through-hole would open into the bore and hit the
carriage.

    fixed holes ....... Y +/-12, Z 148 and 172   (into the collar)
    slots ............. Y +/-12, Z 88..136        (48 mm of fork trim)

The fork head's own back plate has 2 x dia 4.5 at Y +/-12, Z 13, so dropping
those onto the slots puts the tines 13 mm above the bolt height and makes the
whole head adjustable.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

# The servo mount's collar outer square is 54.6, so its +X face is at 27.3.
# Sit the bracket against it; the two are separate parts held by screws.
COLLAR_FACE_X = 27.3
BRACKET_T = 6.0
BRACKET_X = (COLLAR_FACE_X, COLLAR_FACE_X + BRACKET_T)
BRACKET_Y_HALF = 20.0
BRACKET_Z = (86.0, 176.0)

HOLD_D = 4.5                      # M4 clearance, into the collar's blind holes
HOLD_Y = 12.0
HOLD_ZS = (156.0, 172.0)          # inside the collar's Z 140..180

SLOT_W = 4.5
SLOT_Y = 12.0
SLOT_Z = (88.0, 136.0)            # all of it below the collar's bottom at 140
SLOT_TRAVEL = SLOT_Z[1] - SLOT_Z[0]


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _through_x(x0, y, z, dia):
    return bd.Pos(x0, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(
        dia / 2.0, BRACKET_T + 4.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _bracket():
    b = _box(BRACKET_X[0], BRACKET_X[1], -BRACKET_Y_HALF, BRACKET_Y_HALF,
             BRACKET_Z[0], BRACKET_Z[1])

    # four fixed screws into the collar
    for sy in (-1.0, 1.0):
        for hz in HOLD_ZS:
            b = b.cut(_through_x(BRACKET_X[0] - 2.0, sy * HOLD_Y, hz, HOLD_D))

    # two vertical slots for the fork head, all below the collar
    for sy in (-1.0, 1.0):
        b = b.cut(_box(BRACKET_X[0] - 2.0, BRACKET_X[1] + 2.0,
                       sy * SLOT_Y - SLOT_W / 2, sy * SLOT_Y + SLOT_W / 2,
                       SLOT_Z[0], SLOT_Z[1]))

    b.label = "g_fork_clamp"
    return b


@step(out="../newSTEP/g_fork_clamp.step")
def g_fork_clamp():
    return _bracket()


if __name__ == "__main__":
    m = g_fork_clamp()
    bb = m.bounding_box()
    print(f"bbox X {bb.max.X - bb.min.X:.2f}  Y {bb.max.Y - bb.min.Y:.2f}"
          f"  Z {bb.max.Z - bb.min.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3"
          f"   ({m.volume / 1000 * 1.24:.0f} g PLA)")
    print()
    print("no collar: it bolts to the servo mount's collar instead")
    print(f"  plate X {BRACKET_X}  Y +/-{BRACKET_Y_HALF}  Z {BRACKET_Z}")
    print(f"  4 fixed holes dia {HOLD_D} at Y +/-{HOLD_Y}, Z {HOLD_ZS}")
    print(f"  2 slots {SLOT_W} wide at Y +/-{SLOT_Y}, Z {SLOT_Z}"
          f"  = {SLOT_TRAVEL:.0f} mm travel")
    print(f"  slot top {SLOT_Z[1]} is below the collar's bottom at 140, so the")
    print(f"  whole travel is usable -- the first version lost 12 mm there")
    print()
    print("the servo mount's collar needs matching blind holes:")
    print(f"  4 x dia 3.5, 4.0 deep, on its +X face at X"
          f" {COLLAR_FACE_X}, Y +/-{HOLD_Y}, Z {HOLD_ZS}")
