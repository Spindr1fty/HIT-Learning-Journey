"""Venue geometry from dxf/Place.DXF, in a robot-friendly frame.

Origin = 投壶线 intersected with the centre line. +X runs down the track toward
the house, +Z is up, the playing surface is Z = 0.

Every number is tagged with where it came from:
  dim   = a DIMENSION entity in the drawing (the design intent)
  drawn = measured off the drawn geometry
  rules = the committee rules page
  open  = not settled by the drawing, parameterised below

The drawing's own drafting sloppiness (edges slanted by ~2.5 mm, duplicate
lines disagreeing by 0.4 mm) is normalised to the nominal values, the same way
gen_parts_data.py treats the part drawings.
"""

# --- track, transverse ---
TRACK_HALF_WIDTH = 275.0      # drawn: the two solid longitudinal lines, 550 total
AIM_HALF_WIDTH = 95.0         # dim: 180 between the dashed line and the track edge
AIM_HALF_WIDTH_DRAWN = 97.5   # drawn: where the HIDDEN lines actually sit, 2.5 off
FIELD_HALF_WIDTH = 500.0      # drawn: the 1000.000 cross lines, matches rules

# --- track, longitudinal (X, +ve toward the house) ---
THROW_LINE_X = 0.0            # datum
HOUSE_CENTRE_X = 1680.0       # drawn: a witness line of exactly 1680.000
TRACK_FAR_X = 2000.0          # drawn 1998.75; the 2000-long lines say 2000
RACK_FACE_X = -700.0          # drawn: rack front face, 700 past the throw line
RACK_BACK_X = -760.0          # drawn: 60 deep
FIELD_NEAR_X = -800.0         # drawn: 800-long end zone

# --- house, concentric at (HOUSE_CENTRE_X, 0) ---
HOUSE_RADII = (35.0, 100.0, 165.0, 230.0)   # drawn: uniform 65 ring pitch

# --- the two racks ---
RACK_Y_CENTRES = (250.0, -250.0)   # drawn: symmetric about the centre line
RACK_EDGE_GAP = 40.0               # dim: rack back to the field's near edge

# --- open / parameterised ---
# Rules say 2940 overall; the drawing measures 2800. The 140 mm difference is a
# white strip the user did not measure, and which end it sits on is unknown.
EXTRA_LENGTH = 140.0
EXTRA_AT_FAR_END = False          # False -> hang it off the near (rack) end

# The rack is elevated on a platform that is sized tight to the rack, so the
# robot cannot drive onto it. Its height has not been measured.
PLATFORM_HEIGHT = 0.0
PLATFORM_CLEARANCE = 0.0          # gap between platform edge and rack footprint

# Cosmetic only: the playing surface is one flat slab, confirmed same height
# across the track and the surrounding area, with no walls and no side slope.
SLAB_THICKNESS = 10.0


def near_x() -> float:
    return FIELD_NEAR_X - (0.0 if EXTRA_AT_FAR_END else EXTRA_LENGTH)


def far_x() -> float:
    return TRACK_FAR_X + (EXTRA_LENGTH if EXTRA_AT_FAR_END else 0.0)


# The plan is NOT a uniform rectangle. The two +-500 edges are only 800 long
# (the end zone) while the +-275 track edges run 2000. The step is exactly at
# the throw line, and the house's 460 outer diameter fitting inside the 550
# track confirms the narrow lane is real.
def plan() -> list[tuple[float, float]]:
    return [
        (near_x(), -FIELD_HALF_WIDTH),
        (THROW_LINE_X, -FIELD_HALF_WIDTH),
        (THROW_LINE_X, -TRACK_HALF_WIDTH),
        (far_x(), -TRACK_HALF_WIDTH),
        (far_x(), TRACK_HALF_WIDTH),
        (THROW_LINE_X, TRACK_HALF_WIDTH),
        (THROW_LINE_X, FIELD_HALF_WIDTH),
        (near_x(), FIELD_HALF_WIDTH),
    ]
