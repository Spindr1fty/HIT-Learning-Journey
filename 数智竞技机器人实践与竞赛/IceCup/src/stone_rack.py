from cadgen import build123d as bd
from cadgen import step

import spec


def pocket_boxes() -> list[bd.Shape]:
    """The nine 80x80 pockets, 58 mm deep, stopped by the 2 mm back wall."""
    xs = spec.cell_centers(spec.RACK_WIDTH, centered=True)
    zs = [lo for lo, _ in spec.cell_spans(spec.RACK_HEIGHT, centered=False)]
    floor = spec.pocket_floor_y()
    depth = (spec.RACK_DEPTH / 2 + 2.0) - floor
    return [
        bd.Pos(x, floor, z)
        * bd.Box(
            spec.CELL_SIZE,
            depth,
            spec.CELL_SIZE,
            align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
        )
        for x in xs
        for z in zs
    ]


def _rack() -> bd.Shape:
    shell = bd.Box(
        spec.RACK_WIDTH,
        spec.RACK_DEPTH,
        spec.RACK_HEIGHT,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    for pocket in pocket_boxes():
        shell = shell - pocket
    shell.label = "stone_rack"
    return shell


@step(out="../oldSTEP/stone_rack.step")
def stone_rack():
    return _rack()


if __name__ == "__main__":
    r = stone_rack()
    print(f"pocket depth {spec.RACK_DEPTH - spec.RACK_WALL} mm, stone dia"
          f" {spec.STONE_DIAMETER} -> fore/aft play {spec.pocket_play()} mm")
    print(f"side clearance {spec.CELL_SIZE} - {spec.STONE_DIAMETER} = "
          f"{spec.CELL_SIZE - spec.STONE_DIAMETER} mm "
          f"= {(spec.CELL_SIZE - spec.STONE_DIAMETER) / 2} mm per side")
    print(f"volume {r.volume / 1000:.2f} cm3  valid={r.is_valid}")
