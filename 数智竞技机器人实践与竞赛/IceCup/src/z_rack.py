"""Z-axis rack: module 2, 40 teeth, straight-flank (involute of infinite radius).

A rack is what a gear becomes at infinite radius, so the flanks are straight
lines at the pressure angle instead of curves. Tooth thickness at the pitch
line is half the circular pitch, exactly like the pinion, so the pair meshes
on the pitch line at X = RACK_PITCH_X.

The mounting flange is SLOTTED along X. That slot is the only way to set the
meshing centre distance: the pinion rides on the carriage, so its distance to
the rail is fixed by the arm, and the rack has to come to it.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding,
so any non-ASCII byte breaks the parse on a GBK Windows box.
"""

import sys
from math import radians, tan
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402

PRESSURE_TAN = tan(radians(P.PRESSURE_ANGLE))

X_BACK = P.RACK_BODY_X[0]                        # -96.5  back of the body
X_ROOT = P.RACK_BODY_X[1]                        # -76.5  root of the teeth
X_TIP = P.RACK_PITCH_X + P.MODULE                # -72.0  tooth tips

HALF_PITCH = P.CIRCULAR_PITCH / 4.0              # tooth half-thickness at pitch
BACKLASH_HALF = P.BACKLASH / 2.0                 # trim per flank
HALF_TIP = HALF_PITCH - P.MODULE * PRESSURE_TAN - BACKLASH_HALF
HALF_ROOT = HALF_PITCH + 1.25 * P.MODULE * PRESSURE_TAN - BACKLASH_HALF

FLANGE_Z = 0.0                                   # sits ON the base plate
FLANGE_TOP = 8.0

# Proper foot, like the rail's: wide, and four M4 holes instead of two slots.
# It can only grow in -X and +/-Y; the tooth roots start at X_ROOT, so anything
# past that in +X would eat teeth.
FLANGE_X0 = X_BACK - 1.5                         # -98.0, kept for reference
SPINE_X0 = X_BACK - 20.0                         # -116.5 back spine
SPINE_W = 6.0                                    # Y width of the spine
SPINE_TOP = 300.0       # stop below the top: the cap's back wall passes

# Two M4 pilot holes in the TOP face. The cap's plate sits on this face and two
# M4 x 20 screws come down through the cap's slotted holes into these: 8 mm
# through the cap, 12 mm into the rack, so 14 deep leaves 2 mm of spare thread.
# Positions clear the tooth roots (X -76.5) by 10 mm and the back spine by 7 mm.
PILOT_D = 3.6
PILOT_DEPTH = 14.0
PILOT_X = -86.5
PILOT_Y = 5.0
FLANGE_X1 = X_ROOT                               # -76.5
FOOT_X0 = SPINE_X0                               # -116.5, carries the spine
FOOT_X1 = X_ROOT                                 # -76.5, flush with the roots
FOOT_Y_HALF = 22.0                               # was GEAR_W/2 = 8
FOOT_T = 8.0
FOOT_HOLE_XS = (-96.0, -84.0)                    # inside the foot, clear of slots
FOOT_HOLE_Y = 14.0
FOOT_HOLE_D = 4.5

SLOT_LEN = 6.0                                   # X adjustment travel
SLOT_D = 4.5
SLOT_XS = (-96.0, -84.0)                         # moved onto the new foot holes

# Phase the teeth so a TOOTH centre lands exactly on the mesh point's Z. The
# pinion is rotated to present a gap there (see z_pinion), so tooth-in-gap is
# the correct static pose. Without this the pair overlaps by part of a tooth.
_K = round(P.PINION_Z / P.CIRCULAR_PITCH - 0.5)
TOOTH_PHASE = P.PINION_Z - (_K + 0.5) * P.CIRCULAR_PITCH


def _rack_profile():
    """Closed outline in the X-Z plane: body plus one zig-zag tooth edge."""
    pts = [(X_BACK, 0.0), (X_BACK, P.RACK_LEN), (X_ROOT, P.RACK_LEN)]
    for k in range(P.RACK_TEETH - 1, -1, -1):
        zc = (k + 0.5) * P.CIRCULAR_PITCH + TOOTH_PHASE
        pts.append((X_ROOT, zc + HALF_ROOT))
        pts.append((X_TIP, zc + HALF_TIP))
        pts.append((X_TIP, zc - HALF_TIP))
        pts.append((X_ROOT, zc - HALF_ROOT))
    pts.append((X_ROOT, 0.0))
    pts.append(pts[0])
    return bd.Face(bd.Polyline(*[(x, 0.0, z) for x, z in pts], close=True))


def _obround_slot(xc, yc):
    """A slot cutter: a box with a round end at each tip, running along X.

    Width is SLOT_D (M4 clearance); length SLOT_LEN gives the X trim. Four of
    these, on the same pattern as the rail's foot holes, so the rack fixes down
    with four screws just like the rail does.
    """
    depth = FOOT_T + 2.0
    straight = SLOT_LEN - SLOT_D
    z0 = FLANGE_Z - 1.0
    parts = [bd.Pos(xc, yc, z0)
             * bd.Box(straight, SLOT_D, depth,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))]
    for sign in (-1, 1):
        parts.append(bd.Pos(xc + sign * straight / 2, yc, z0)
                     * bd.Cylinder(SLOT_D / 2, depth,
                                   align=(bd.Align.CENTER, bd.Align.CENTER,
                                          bd.Align.MIN)))
    return parts


def _rack():
    body = bd.extrude(_rack_profile(), amount=P.GEAR_W)
    body = bd.Pos(0, -P.GEAR_W / 2.0, 0) * body

    # FOOT. This used to be a narrow 21.5 x 16 flange with two slots, which read
    # as an afterthought next to the rail's 50 x 50 foot. It is now a proper
    # foot: 27.5 wide in X, 44 wide in Y, same 8 mm thickness as the rail's, and
    # four M4 holes on the same +/-18 pattern. It can only grow in -X and +/-Y,
    # because the tooth roots start at X_ROOT and anything past that would eat
    # teeth.
    foot = bd.Pos(FOOT_X0, 0, FLANGE_Z) * bd.Box(
        FOOT_X1 - FOOT_X0, 2 * FOOT_Y_HALF, FOOT_T,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN))

    # BACK SPINE. The rack is a 320 mm PLA cantilever bolted at the bottom; on
    # its own it bends ~2 mm at the tip under a 7 N radial load, which is enough
    # to walk the pinion out of mesh. A 6 x 20 spine turns the section into a T:
    # second moment 1.1e4 -> 5.0e4 mm4, i.e. 4.6x stiffer, for +47 g of PLA.
    spine_top = SPINE_TOP if SPINE_TOP is not None else P.RACK_LEN
    spine = bd.Pos(SPINE_X0, -SPINE_W / 2.0, FLANGE_TOP) * bd.Box(
        X_BACK - SPINE_X0, SPINE_W, spine_top - FLANGE_TOP,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))

    rack = (body + foot + spine).clean()

    pilots = [
        bd.Pos(PILOT_X, sy * PILOT_Y, P.RACK_LEN - PILOT_DEPTH)
        * bd.Cylinder(PILOT_D / 2.0, PILOT_DEPTH + 2.0,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for sy in (-1.0, 1.0)
    ]
    rack = rack.cut(*pilots).clean()

    # The slots stay: they are the only way to trim the centre distance. They
    # are now cut as round-cap obrounds on the rail's own hole pattern.
    cutters = []
    for xc, yc in _foot_holes():
        cutters.extend(_obround_slot(xc, yc))
    rack = rack.cut(*cutters).clean()

    rack.label = "z_rack"
    return rack


def _foot_holes():
    """The four foot holes, for the base plate to match."""
    return [(x, sy * FOOT_HOLE_Y) for x in FOOT_HOLE_XS for sy in (-1.0, 1.0)]


@step(out="../newSTEP/z_rack.step")
def z_rack():
    return _rack()


if __name__ == "__main__":
    r = z_rack()
    b = r.bounding_box()
    print(f"teeth {P.RACK_TEETH}  module {P.MODULE}"
          f"  circular pitch {P.CIRCULAR_PITCH:.4f}")
    print(f"half thickness at pitch {HALF_PITCH:.4f}"
          f"  tip {HALF_TIP:.4f}  root {HALF_ROOT:.4f}")
    print(f"X stations: back {X_BACK}  root {X_ROOT}  tip {X_TIP}")
    print(f"bbox X {b.max.X - b.min.X:.3f}  Y {b.max.Y - b.min.Y:.3f}"
          f"  Z {b.max.Z - b.min.Z:.3f}  valid={r.is_valid}")
    print(f"teeth span Z {P.RACK_LEN:.3f}  (bbox Z should exceed it by the flange)")
    print(f"volume {r.volume / 1000:.3f} cm3  solids {len(r.solids())}")
    print(f"slot travel {SLOT_LEN} mm -> centre distance"
          f" {P.PITCH_R - SLOT_LEN / 2:.2f}..{P.PITCH_R + SLOT_LEN / 2:.2f} mm")
