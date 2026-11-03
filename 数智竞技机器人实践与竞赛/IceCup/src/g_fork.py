r"""Funnel gripper head: the part that actually touches the stone.

WHY A FUNNEL
The stone's handle is an 11 mm stem under an 18 mm disc. Two parallel tines
leave a 12.6 mm gap, so they only work if the robot is aligned to the stone
within +/-0.8 mm. The opponent drops the stone anywhere in an 80 mm cell, i.e.
+/-16.5 mm off centre. So the parallel version misses most of the time.

The funnel has a 48 mm mouth that closes to the same 12.6 mm gap over 30 mm of
travel. Whatever the stone's offset, the sloped walls walk it to the middle on
the way in. The stone sits on three ball transfers and slides easily, which is
what makes this work at all.

LAYOUT, fork frame, X forward, Z up, tine underside at Z=0

        plan view
                      48 wide mouth
              \                        /
               \   ___tines___        /
                \ | closed end |      /
        ----------+--------------+----+------> X
       -12       0             12   42

    X = -12..-4   back plate, bolts to a bracket (2 x dia 4.5 for M4)
    X =   0.. 12  the two tines, Y = +/-6.3..8.7, so the gap is 12.6
    X =  12.. 42  funnel walls, Y widening from 6.3 to 24
    X =   0       closed end: the stem stops here, so the pick depth repeats

The head is 3.5 mm thick because it has to pass under the 18 mm disc with 1.9 mm
of clearance to spare. It is deliberately NOT modelled with any mounting that
depends on chassis height -- that is a separate bracket.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from math import radians, tan
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_params as G  # noqa: E402

# --- working end -----------------------------------------------------------
THICK = G.TINE_THICK          # 3.5, fits the 7.5 gap under the disc
TINE_IN = G.TINE_INNER_Y      # 6.3
TINE_OUT = G.TINE_OUTER_Y     # 8.7
X_CLOSED = 0.0
# The parallel section has to be long enough that the whole 9.7 mm stem ends up
# inside it. Inside the cell the stem can sit at most X = 26.5 on this part, so
# the slot has to START beyond 26.5 + 4.85 = 31.35 or the stem stays in the taper
# and never gets centred. 32 it is.
X_TINE_END = 33.0
MOUTH_HALF = 22.0             # mouth narrowed 48 -> 44; capture is then +/-17.15, still clear of the +/-16.5 worst case
X_MOUTH = 49.0             # mouth position; taper length = X_MOUTH - X_TINE_END
# The two outer corners of the mouth are chamfered so the arms come to a tapered
# nose rather than a square 18 mm edge. That lets them slip under the stone's
# disc instead of catching its rim.
# B: instead of chamfering in plan, thin the leading edge in THICKNESS so the
# arms present a wedge to the 7.5 mm gap under the stone's disc. The bevel runs
# across the full width and fades back, leaving the lifting faces untouched.
# Point the two mouth lips. The plate's edge is at Y +/-26 and the throat at
# +/-22, so each lip is a 4 mm strip. Cutting a diagonal back from that strip's
# front leaves a point at (X_MOUTH, +/-22) for the disc to ride onto.
LIP_POINT_LEN = 8.0
# The funnel's flank is extended past the throat until it crosses the plate's
# outer edge; that crossing is the sharp lip. The outer edge itself stays a
# straight line, exactly as drawn.
PLATE_HALF = 26.0      # the plate's outer edge, Y +/- 26
X_LIP = 0.0            # filled in by _head() from the flank geometry
TIP_BEVEL = 2.0
TIP_EDGE = 0.5            # thickness left at the very lip
# Angle of the tip ramp the stone rides up. 8.1 deg is the as-designed value
# (lip to X_TINE_END over 3.0 mm of drop). A steeper ramp prints with much
# smaller stair steps: 0.2 mm layers leave 1.40 mm steps at 8.1 deg but only
# 0.86 mm at 13 deg.
RAMP_ANGLE = 8.1

# --- back plate, for whatever bracket the chassis ends up needing ----------
PLATE_X = (-12.0, -4.0)
PLATE_HALF_Y = 20.0
PLATE_Z = (0.0, 26.0)
PLATE_HOLE_D = 4.5            # M4 clearance
PLATE_HOLE_Y = 12.0
PLATE_HOLE_Z = 13.0


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _head():
    # the working plate, from behind the closed end to past the mouth
    # --- extend the flanks out to the plate's edge ------------------------
    # X_LIP is where the flank line crosses Y = PLATE_HALF. The lip is a point,
    # the plate's outer edge stays straight, and the funnel throat is unchanged.
    globals()["X_LIP"] = X_TINE_END + (PLATE_HALF - TINE_IN) / (MOUTH_HALF - TINE_IN) * (X_MOUTH - X_TINE_END)
    x_lip = globals()["X_LIP"]
    plate = _box(PLATE_X[0], x_lip, -PLATE_HALF, PLATE_HALF, 0.0, THICK)

    # the funnel void: a U cut through the plate, open at the front.
    # The parallel section has to reach back to X_CLOSED, otherwise the material
    # between X=0 and X=12 stays solid and the stem is buried in it -- that cost
    # 332 mm3 of interference before the check caught it.
    void = [
        (x_lip + 2.0, -PLATE_HALF),
        (x_lip, -PLATE_HALF),
        (X_TINE_END, -TINE_IN),
        (X_CLOSED, -TINE_IN),
        (X_CLOSED, TINE_IN),
        (X_TINE_END, TINE_IN),
        (x_lip, PLATE_HALF),
        (x_lip + 2.0, PLATE_HALF),
    ]
    face = bd.Face(bd.Polyline(*[(x, y, 0.0) for x, y in void], close=True))
    # Extrude BOTH ways. A plain extrude follows the face's normal, which for
    # this winding points at -Z, so the cutter ended up entirely below the plate
    # and cut nothing -- the funnel looked fine in the source and in the volume
    # print, and only the stone intersection exposed it. both=True removes the
    # dependency on winding order.
    cutter = bd.extrude(face, amount=THICK + 4.0, both=True)
    head = plate.cut(cutter).clean()

    # back plate, standing up behind the tines
    back = _box(PLATE_X[0], PLATE_X[1], -PLATE_HALF_Y, PLATE_HALF_Y,
                PLATE_Z[0], PLATE_Z[1])
    head = (head + back).clean()

    # --- thin the leading edge (option B) ----------------------------------
    # The bevel now runs the WHOLE funnel, not just the last few millimetres:
    # from the full 3.5 thickness at the slot's start it ramps down to a 0.5 mm
    # edge at the lip point. The stone's disc rides up one continuous ~8.5 degree
    # ramp instead of meeting a step. The tines start at X_TINE_END and keep their
    # full height, so the lifting face is untouched.
    ramp_run = (THICK - TIP_EDGE) / tan(radians(RAMP_ANGLE))
    x_ramp0 = x_lip + 1.0 - ramp_run
    pts = [(x_ramp0, THICK),
           (x_lip + 1.0, THICK),
           (x_lip + 1.0, TIP_EDGE)]
    prof = bd.Face(bd.Polyline(*[(x, 0.0, z) for x, z in pts], close=True))
    head = head.cut(bd.extrude(prof, amount=MOUTH_HALF + 4.0, both=True)).clean()


    # M4 clearance holes through the back plate, along X
    holes = [
        bd.Pos(PLATE_X[0] - 1.0, sy * PLATE_HOLE_Y, PLATE_HOLE_Z)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(PLATE_HOLE_D / 2.0, PLATE_X[1] - PLATE_X[0] + 2.0,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for sy in (-1.0, 1.0)
    ]
    head = head.cut(*holes).clean()

    head.label = "g_fork"
    return head


@step(out="../newSTEP/g_fork.step")
def g_fork():
    return _head()


if __name__ == "__main__":
    f = g_fork()
    b = f.bounding_box()
    print(f"bbox X {b.max.X - b.min.X:.2f}  Y {b.max.Y - b.min.Y:.2f}"
          f"  Z {b.max.Z - b.min.Z:.2f}   valid={f.is_valid}"
          f"  solids={len(f.solids())}")
    print(f"volume {f.volume / 1000:.3f} cm3"
          f"   ({f.volume / 1000 * 1.24:.0f} g PLA)")
    print()
    print("funnel")
    print(f"  mouth ............ {2 * MOUTH_HALF:.1f} mm wide")
    print(f"  closes to ........ {2 * TINE_IN:.1f} mm over"
          f" {X_MOUTH - X_TINE_END:.0f} mm of travel")
    print(f"  capture .......... +/-{MOUTH_HALF - G.STEM_DIA / 2:.1f} mm"
          f"   (stone can sit +/-16.5 off centre in an 80 cell)")
    print(f"  tine thickness ... {THICK:.1f} mm"
          f"   gap under the disc {G.GAP_UNDER_DISC:.1f}")
    print(f"  tine top to disc . {G.GAP_UNDER_DISC - THICK:.2f} mm")
    print(f"  stem clearance ... {TINE_IN - G.STEM_DIA / 2:.2f} mm per side")
    print(f"  disc overlap ..... {G.DISC_DIA / 2 - TINE_OUT:.2f} mm at the rim")
    print()
    print("back plate")
    print(f"  X {PLATE_X}  Y +/-{PLATE_HALF_Y}  Z {PLATE_Z}")
    print(f"  2 x dia {PLATE_HOLE_D} M4 clearance at Y"
          f" +/-{PLATE_HOLE_Y}, Z {PLATE_HOLE_Z}")
