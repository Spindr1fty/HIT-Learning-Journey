"""Rack loaded with one team's 5 stones in a 2 / 2 / 1 tier arrangement.

The opponent chooses which cells are filled, so this is one representative
arrangement; the picker must handle all nine cells regardless. Each stone is
drawn resting against the 2 mm back wall, which is the rear-most of the 12 mm
of fore-aft play a stone has inside a pocket.
"""

from cadgen import build123d as bd
from cadgen import step

import spec
from curling_stone import curling_stone
from stone_rack import stone_rack

# (column, row) into the 3x3 grid, row 0 = 底层
FILLED_CELLS = ((0, 0), (2, 0), (0, 1), (1, 1), (2, 2))


def loaded_rack():
    xs = spec.cell_centers(spec.RACK_WIDTH, centered=True)
    floors = [lo for lo, _ in spec.cell_spans(spec.RACK_HEIGHT, centered=False)]
    stone = curling_stone()
    stone_y = spec.pocket_floor_y() + spec.STONE_DIAMETER / 2
    parts = [stone_rack()]
    for col, row in FILLED_CELLS:
        placed = bd.Pos(xs[col], stone_y, floors[row]) * stone
        placed.label = f"stone:c{col + 1}r{row + 1}"
        parts.append(placed)
    return bd.Compound(children=parts, label="rack_loaded")


@step(out="../oldSTEP/rack_loaded.step")
def rack_loaded():
    return loaded_rack()


if __name__ == "__main__":
    rack_loaded()
