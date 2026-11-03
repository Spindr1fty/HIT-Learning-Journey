r"""Z-axis base plate, version 4: ten plain through-holes, no nut pockets.

WHY THE POCKETS WENT AWAY
Version 3 put a hex pocket under each rail and rack bolt, on the reasoning that
the nut had to be held because the plate's underside is not reachable once the
plate sits on the chassis. That reasoning was wrong: it only applies if the bolt
stops at the plate. Bolt all the way THROUGH -- rail foot, plate, chassis -- and
the nut lands on the far side of the chassis, where there is plenty of room for
a spanner. Nothing has to be captive, the joint is a real clamp, and the plate
becomes ten holes in a rectangle.

A hex pocket was also physically wrong while it existed: the pockets were drawn
as 7.2 mm squares, and an M4 nut is 7.0 across flats but 8.3 across corners, so
the nut would not have dropped in. The section render caught that one.

JOINTS, all the same shape
    bolt head on top of the rail foot / rack base / plate
    through the plate
    through the chassis
    M4 nut underneath the chassis

So the chassis needs the same ten holes, which are free if it is laser cut.

SCREW LENGTH
    8 (foot or rack base) + 8 (plate) + t (chassis) + 3.2 (nut)
    = 19.2 + t mm. A 25 mm screw covers a chassis up to 5.8 mm thick; the
    current B15 chassis is 8 mm, so the stack is 27.2 and a 30 mm screw would
    stick out 2.8 mm below the nut. If the chassis gets a hex nut pocket in its
    underside (3.6 deep), the stack drops to 23.6 -> M4 x 24.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

PLATE_T = 8.0
PLATE_Y_HALF = 32.0
PLATE_X = (-108.0, 30.0)

HOLE_D = 4.5                      # M4 clearance
RAIL_HOLE_AT = 18.0               # must match z_rail.FOOT_HOLE_AT
# The rack now has a proper foot with four slots, same idea as the rail's foot,
# so the plate carries four matching holes instead of two.
RACK_HOLE_XS = (-96.0, -84.0)     # must match z_rack.FOOT_HOLE_XS
RACK_HOLE_Y = 14.0                # must match z_rack.FOOT_HOLE_Y
CHASSIS_X = (-102.0, 24.0)        # clear of the rail foot, which reaches Y 25
CHASSIS_Y = 28.0

# (x, y, what) -- collected so the printout and the cuts cannot drift apart
HOLES = (
    [((sx * RAIL_HOLE_AT, sy * RAIL_HOLE_AT), "rail foot")
     for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)]
    + [((rx, sy * RACK_HOLE_Y), "rack foot")
       for rx in RACK_HOLE_XS for sy in (-1.0, 1.0)]
    + [((cx, sy * CHASSIS_Y), "chassis")
       for cx in CHASSIS_X for sy in (-1.0, 1.0)]
)


def _through(x, y, dia=HOLE_D):
    """Hole right through the plate."""
    return bd.Pos(x, y, -PLATE_T - 1.0) * bd.Cylinder(
        dia / 2.0, PLATE_T + 2.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _plate():
    plate = bd.Pos(PLATE_X[0], -PLATE_Y_HALF, -PLATE_T) * bd.Box(
        PLATE_X[1] - PLATE_X[0], 2 * PLATE_Y_HALF, PLATE_T,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    plate = plate.cut(*[_through(x, y) for (x, y), _ in HOLES])

    # a nut has to seat flat, so no hole may break into a neighbour or an edge.
    # Check the signed edges, not abs(x): the plate runs from -108 to +30, so an
    # abs() test rejects every hole on the negative side.
    r = HOLE_D / 2.0
    for (x, y), what in HOLES:
        if x - r < PLATE_X[0] or x + r > PLATE_X[1] \
                or y - r < -PLATE_Y_HALF or y + r > PLATE_Y_HALF:
            raise ValueError(f"{what} hole at ({x}, {y}) breaks the plate edge")

    plate.label = "z_plate"
    return plate


@step(out="../newSTEP/z_plate.step")
def z_plate():
    return _plate()


if __name__ == "__main__":
    p = z_plate()
    b = p.bounding_box()
    print(f"plate {PLATE_X[1] - PLATE_X[0]:.0f} x {2 * PLATE_Y_HALF:.0f}"
          f" x {PLATE_T:.0f}   valid={p.is_valid}  solids={len(p.solids())}")
    print(f"volume {p.volume / 1000:.3f} cm3"
          f"   ({p.volume / 1000 * 1.24:.0f} g PLA)")
    print()
    print(f"{len(HOLES)} through-holes, dia {HOLE_D}, no nut pockets")
    for what in ("rail foot", "rack foot", "chassis"):
        xs = sorted({x for (x, _), w in HOLES if w == what})
        ys = sorted({y for (_, y), w in HOLES if w == what})
        n = sum(1 for _, w in HOLES if w == what)
        print(f"  {what:<10} {n} holes   X {xs}   Y {ys}")
    print()
    print(f"chassis must carry the same {len(HOLES)} holes -- free if laser cut")
    print(f"screw length = 8 + {PLATE_T:.0f} + chassis t + 3.2 ="
          f" {8 + PLATE_T + 3.2:.1f} + t mm")
