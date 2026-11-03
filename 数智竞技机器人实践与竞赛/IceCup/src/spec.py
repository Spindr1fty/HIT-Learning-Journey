"""Rule-frozen dimensions from the HIT curling robot competition sheets."""

# Stone. The *_MEASURED values come from a real stone with a vernier caliper on
# 2026-10-16. The model is deliberately built to the committee's nominal values
# so every clearance that comes out is conservative. The scatter (total height
# +1.6 mm, diameter -1 mm) says this is an injection moulding part, not a
# machined one -- the mechanism has to tolerate that.
STONE_DIAMETER = 47.0
STONE_DIAMETER_MEASURED = 46.0
STONE_HEIGHT = 32.0
STONE_HEIGHT_MEASURED = 33.6
STONE_BODY_HEIGHT = 24.0

# 击球点 / belt centre height above the resting surface. Three sources:
IMPACT_HEIGHT = 12.0                 # rules page, says "approximately"
IMPACT_HEIGHT_FROM_DRAWING = 11.05   # 8.3 + 5.5/2 off the dimensioned drawing
IMPACT_HEIGHT_MEASURED = 10.9        # caliper: belt top 15.6, belt thick 9.4
BELT_TOP_MEASURED = 15.6
BELT_THICKNESS_MEASURED = 9.4

# The three bottom balls sit essentially flush with the base face -- caliper
# jaws would not fit in the gap -- so the base is the height datum.
BALL_PROTRUSION_MEASURED = 0.0

# Stone rack: 305 wide x 305 tall x 60 deep, 3x3 pockets of 80x80, closed at the
# back by a 2 mm acrylic wall. That wall rules out pushing a stone out from
# behind, and leaves 12 mm of fore-aft play for a stone inside a pocket.
RACK_WIDTH = 305.0
RACK_HEIGHT = 305.0
RACK_DEPTH = 60.0
RACK_WALL = 2.0
CELL_SIZE = 80.0
CELLS_PER_AXIS = 3

# 5 stones per team: 2 bottom / 2 middle / 1 top
STONES_PER_TIER = (2, 2, 1)

# Field and robot envelope. FIELD_LENGTH is the rules-page figure; the venue
# drawing measures 2798.75, the gap being an unmeasured white strip (see
# venue_spec.py).
FIELD_LENGTH = 2940.0
FIELD_WIDTH = 1000.0
ROBOT_FOOTPRINT = 350.0
ATTEMPT_TIME_LIMIT_S = 120.0


def wall_thickness(total: float = RACK_WIDTH) -> float:
    return (total - CELLS_PER_AXIS * CELL_SIZE) / (CELLS_PER_AXIS + 1)


def cell_spans(total: float, centered: bool) -> list[tuple[float, float]]:
    """Return the (start, end) of each cell along one rack axis."""
    wall = wall_thickness(total)
    origin = -total / 2 if centered else 0.0
    pitch = CELL_SIZE + wall
    return [(origin + wall + i * pitch, origin + wall + i * pitch + CELL_SIZE)
            for i in range(CELLS_PER_AXIS)]


def cell_centers(total: float, centered: bool) -> list[float]:
    return [(a + b) / 2 for a, b in cell_spans(total, centered)]


def pocket_floor_y() -> float:
    """Y of the back wall's inner face; pockets open toward +Y."""
    return -RACK_DEPTH / 2 + RACK_WALL


def pocket_play() -> float:
    """Fore/aft room a stone has inside a pocket."""
    return RACK_DEPTH - RACK_WALL - STONE_DIAMETER
