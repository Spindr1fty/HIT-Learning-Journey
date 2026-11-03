"""Z-axis pinion: module 2, 18 teeth, true involute flanks.

Why a real involute and not a trapezoid: at 18 teeth the tip lands at 1.35 mm
wide, so the flank shape decides whether the tooth survives a stall. A
trapezoid approximation puts the contact stress in the wrong place.

18 teeth is also the practical minimum for a 20 deg full-depth involute
(17 before undercut), which is why the tooth count is not a free choice.

The bore is a clearance hole for the servo spline; the gear bolts to the
servo's round horn, which is far more reliable than trying to print a 25-tooth
spline socket. HORN_BCD / HORN_HOLES must be checked against the horn that
ships with the Xinhui 20KG servo -- change the two constants and rebuild.

NOTE: this file must stay pure ASCII. cadgen reads model scripts with
Path.read_text() and no explicit encoding, so on a GBK Windows box any
non-ASCII byte makes the parser raise "Failed to parse".
"""

import sys
from math import acos, cos, pi, sin
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402

# --- servo horn interface, MEASURED 2026-10-17 ---------------------------
# horn dia 20.0, 4 holes, M3 screws thread in, horn thickness 2.5,
# servo face -> horn top face = 7.0 mm.
#
# HORN_BCD = 14.0, derived from a caliper pair rather than guessed:
#   inner-jaw reading 11.4  = centre distance - hole dia
#   outer-jaw reading 16.62 = centre distance + hole dia
#   -> centre distance = (11.4 + 16.62) / 2 = 14.01
#   -> hole dia        = (16.62 - 11.4) / 2 =  2.61   (an M3 tap hole)
# Two earlier values were wrong: 20.0 (a guess) and 11.4 (the inner-jaw
# reading taken at face value -- that is the centre distance MINUS one hole
# diameter, which is exactly the trap this pair of readings exposes).
HORN_BCD = 14.0
HORN_HOLES = 4         # measured
HORN_HOLE_D = 3.5      # M3 clearance -- the thread is in the metal horn, so
                       # the printed hole must clear the thread, not grip it
HORN_RECESS_D = 20.2   # shallow seat over the horn's OD for concentricity:
                       # 4 M3 screws in 3.5 bores would leave +/-0.25 mm of
                       # play, which is half the radial tooth clearance
HORN_RECESS_DEPTH = 1.2

# NO CENTRE BORE. The spline ends below the horn's top face (the 7.0 mm stack),
# and the horn's top face is exactly where this gear's -Y face sits, so the
# shaft never enters the gear. A bore would anyway leave too little web between
# it and the M3 holes.
BORE_D = 0.0           # zero means "no bore"; kept so the summary still prints

FLANK_PTS = 16       # samples per involute flank
TIP_ARC_PTS = 5      # samples across the tip land
ROOT_ARC_PTS = 4     # samples across the root gap


def _gear_points():
    """Closed 2D outline as a point list: every tooth, involute flanks.

    Split out of _gear_profile so the same numbers can be written to a DXF for
    laser checking without re-deriving them. Two copies of gear maths would
    eventually disagree, and this gear has already been through enough of that.

    PHASE: with 18 teeth the tooth pitch is 20 deg, so teeth sit at i*20 and
    gaps at i*20+10. The mesh point is at 180 deg from the gear centre, where
    180 mod 20 == 0 -- i.e. a TOOTH points straight at the rack and the two
    parts overlap by a whole tooth. Rotating half a tooth puts a GAP there,
    which is what a real rack-and-pinion looks like at some instant.
    """
    z = P.PINION_TEETH
    pitch_ang = 2 * pi / z
    phase = pi / z                       # half a tooth pitch
    pts = []
    radii = [P.ROOT_R + (P.TIP_R - P.ROOT_R) * k / FLANK_PTS
             for k in range(FLANK_PTS + 1)]
    ha_tip = P.involute_half_angle(P.TIP_R)
    ha_root = P.involute_half_angle(P.ROOT_R)

    for i in range(z):
        centre = i * pitch_ang + phase

        for r in radii:                       # left flank, root -> tip
            ha = P.involute_half_angle(max(r, P.BASE_R))
            pts.append((r * cos(centre - ha), r * sin(centre - ha)))

        for k in range(1, TIP_ARC_PTS):       # tip arc, left -> right
            a = centre - ha_tip + 2 * ha_tip * k / TIP_ARC_PTS
            pts.append((P.TIP_R * cos(a), P.TIP_R * sin(a)))

        for r in reversed(radii):             # right flank, tip -> root
            ha = P.involute_half_angle(max(r, P.BASE_R))
            pts.append((r * cos(centre + ha), r * sin(centre + ha)))

        a0 = centre + ha_root                 # root arc into the next tooth
        a1 = centre + pitch_ang - ha_root
        for k in range(1, ROOT_ARC_PTS):
            a = a0 + (a1 - a0) * k / ROOT_ARC_PTS
            pts.append((P.ROOT_R * cos(a), P.ROOT_R * sin(a)))

    return pts


def _gear_profile():
    """Closed 2D face built from _gear_points()."""
    pts = _gear_points()
    pts.append(pts[0])
    return bd.Face(bd.Polyline(*[(x, y, 0.0) for x, y in pts], close=True))


def _pinion():
    blank = bd.extrude(_gear_profile(), amount=P.GEAR_W)

    cutters = []

    if BORE_D > 0.0:
        cutters.append(bd.Pos(0, 0, -1.0) * bd.Cylinder(
            BORE_D / 2, P.GEAR_W + 2.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))

    # centring seat for the horn's OD, cut into the face that lands on the horn
    cutters.append(bd.Pos(0, 0, -1.0) * bd.Cylinder(
        HORN_RECESS_D / 2, HORN_RECESS_DEPTH + 1.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))

    r_bcd = HORN_BCD / 2
    for i in range(HORN_HOLES):
        a = 2 * pi * i / HORN_HOLES
        cutters.append(
            bd.Pos(r_bcd * cos(a), r_bcd * sin(a), -1.0)
            * bd.Cylinder(HORN_HOLE_D / 2, P.GEAR_W + 2.0,
                          align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))

    gear = blank.cut(*cutters)

    # stand the axis up along +Y, gear centred on the origin in Y
    gear = bd.Rot(-90, 0, 0) * gear
    box = gear.bounding_box()
    gear = bd.Pos(0, -(box.min.Y + box.max.Y) / 2, 0) * gear

    # place it at the assembled position: on the axle, mid-stroke
    gear = bd.Pos(P.PINION_X, 0, P.PINION_Z) * gear
    gear.label = "z_pinion"
    return gear


@step(out="../newSTEP/z_pinion.step")
def z_pinion():
    return _pinion()


if __name__ == "__main__":
    g = z_pinion()
    b = g.bounding_box()
    print(f"teeth {P.PINION_TEETH}  module {P.MODULE}")
    print(f"bbox X {b.max.X - b.min.X:.3f}  Y {b.max.Y - b.min.Y:.3f}"
          f"  Z {b.max.Z - b.min.Z:.3f}   valid={g.is_valid}")
    # bbox is NOT the tip diameter: teeth are phased half a pitch off so a GAP
    # faces the rack, which means no tooth sits on the X axis. Z lands on a
    # tooth and does give 2*TIP_R; read that one.
    print(f"tip dia {b.max.Z - b.min.Z:.3f} (Z axis, expect {2 * P.TIP_R:.3f})"
          f"   root dia {2 * P.ROOT_R:.3f}")
    print(f"bbox X {b.max.X - b.min.X:.3f}  (no tooth on X -- phase offset)")
    print(f"volume {g.volume / 1000:.3f} cm3")
    print()
    print("servo horn interface (MEASURED 2026-10-17)")
    print(f"  bolt circle dia ....... {HORN_BCD} mm   ({HORN_HOLES} holes)")
    print(f"  screw clearance bore .. {HORN_HOLE_D} mm  (M3)")
    print(f"  centring recess ....... dia {HORN_RECESS_D}"
          f" x {HORN_RECESS_DEPTH} deep over the horn's OD 20.0")
    print(f"  centre bore ........... "
          f"{'none' if BORE_D <= 0 else f'dia {BORE_D}'}"
          f"  (spline never reaches this face)")
    web = HORN_BCD / 2 - HORN_HOLE_D / 2 - HORN_RECESS_DEPTH * 0 - 0.0
    print(f"  web at the holes ...... "
          f"{HORN_BCD / 2 - HORN_HOLE_D / 2:.2f} mm out from the axis,"
          f" root is at {P.ROOT_R:.2f}")
    print(f"  tooth tip thickness ... "
          f"{2 * P.TIP_R * P.involute_half_angle(P.TIP_R):.3f} mm")
