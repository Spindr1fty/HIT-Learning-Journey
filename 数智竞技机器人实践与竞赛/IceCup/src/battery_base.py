r"""Battery-box base plate, re-drawn from the photos + caliper numbers.

The real part (a black printed battery holder) has a flat base plate
90.3 x 36.2 with FOUR M4 through holes, two at each end. Numbers the user
gave:

    base            90.3 long x 36.2 wide
    box body        62.3 long
    base -> box     ~20 (the end walls flare down to the base)
    hole edge -> end of base          3.2
    hole edge -> long side of base    8.44   (inconsistent, see below)
    hole -> hole, same end            12

The three hole numbers cannot all be true at once:
    if the pair is 12 apart (centres), the centre sits (36.2-12)/2 = 12.1
    from a long side, so the hole EDGE is 12.1-2.25 = 9.85, not 8.44.
    if the edge distance really is 8.44, the pair is 36.2-2*(8.44+2.25)=14.82.
So this model uses the 12 mm pair (a hole-to-hole measurement is the most
reliable) and the 3.2 mm end distance, symmetric about the centre line:

    holes at X = +-(90.3/2 - 3.2 - 2.25) = +-39.70,  Y = +-6.00

Print it, drop it on the real box, and the truth comes out in one minute.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

BASE_L = 90.3
BASE_W = 36.2
BASE_T = 5.5             # measured with the depth rod
CORNER_R = 3.0

HOLE_D = 4.0             # measured: the base's own through holes are dia 4.0
HOLE_EDGE_END = 3.2      # given: hole edge -> end of base
HOLE_Y = 8.0             # measured: same-end pair INNER edges 12 apart,
                         # with dia 4.0 holes -> 16.0 centre to centre
HOLE_X = BASE_L / 2 - HOLE_EDGE_END - HOLE_D / 2.0      # 39.95


def _plate():
    plate = bd.Pos(-BASE_L / 2, -BASE_W / 2, 0) * bd.Box(
        BASE_L, BASE_W, BASE_T,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    if CORNER_R > 0:
        vertical = plate.edges().filter_by(bd.Axis.Z)
        plate = bd.fillet(vertical, CORNER_R)

    holes = [
        bd.Pos(sx * HOLE_X, sy * HOLE_Y, -1.0) * bd.Cylinder(
            HOLE_D / 2.0, BASE_T + 2.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)
    ]
    plate = plate.cut(*holes).clean()
    plate.label = "battery_base"
    return plate


@step(out="../newSTEP/battery_base.step")
def battery_base():
    return _plate()


if __name__ == "__main__":
    p = battery_base()
    b = p.bounding_box()
    print(f"base {b.max.X - b.min.X:.2f} x {b.max.Y - b.min.Y:.2f}"
          f" x {b.max.Z - b.min.Z:.2f}  valid={p.is_valid}"
          f"  volume {p.volume / 1000:.3f} cm3")
    print(f"holes dia {HOLE_D} at X +-{HOLE_X:.2f}  Y +-{HOLE_Y:.2f}")
    print(f"  pair spacing {2 * HOLE_Y:.1f}   end spacing {2 * HOLE_X:.1f}"
          f"   edge->end {HOLE_EDGE_END:.2f}"
          f"   edge->long side {BASE_W / 2 - HOLE_Y - HOLE_D / 2:.2f}")
