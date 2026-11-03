r"""Standalone battery-box base: 10 mm boss, open tray (fit-check part).

Same footprint, hole pattern, wall thickness and nut pockets as the integrated
tray on the chassis, but 10 mm tall and with its own 2.5 mm floor, so it can be
printed alone and the real battery box screwed on.

Part frame (long edge = X):
    90.3 x 36.2 outline, 10 tall
    2.5 floor + 2.5 perimeter walls
    4 posts at X +-39.95 / Y +-8.00, flush with the ends
    4 x dia 4.5 through holes
    4 hex nut pockets A/F 7.2 x 3.6 deep, open at the top

The battery box's own 5.5 mm base is the lid; M4 x 10/12 screws go down from
inside the box into the embedded nuts.

Writes STEP + STL to the Desktop.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import chassis as C  # noqa: E402
import chassis_test_b15 as T  # noqa: E402

H = 10.0
FLOOR = 2.5
WALL = T.BOSS_WALL
NUT_AF = T.NUT_AF
NUT_DEPTH = T.NUT_DEPTH
HOLE_D = C.HOLE_D

L, W = C.BATT_L, C.BATT_W
HOLE_X, HOLE_Y = C.BATT_HOLE_DX, C.BATT_HOLE_DY
POST_LONG = T.BOSS_POST_Y[0][1] - T.BOSS_POST_Y[0][0]
POST_SHORT = T.BOSS_POST_X[0][1] - T.BOSS_POST_X[0][0]

X0, X1 = -L / 2.0, L / 2.0
Y0, Y1 = -W / 2.0, W / 2.0
DESK = Path.home() / "Desktop"
STEP_OUT = DESK / "battery_base_10mm.step"
STL_OUT = DESK / "battery_base_10mm.stl"


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def build():
    parts = [_box(X0, X1, Y0, Y1, 0.0, FLOOR)]
    parts += [
        _box(X0, X0 + WALL, Y0, Y1, 0.0, H),
        _box(X1 - WALL, X1, Y0, Y1, 0.0, H),
        _box(X0 + WALL, X1 - WALL, Y0, Y0 + WALL, 0.0, H),
        _box(X0 + WALL, X1 - WALL, Y1 - WALL, Y1, 0.0, H),
    ]
    for sx in (-1.0, 1.0):
        px0 = X0 if sx < 0 else X1 - POST_LONG
        for sy in (-1.0, 1.0):
            cy = sy * HOLE_Y
            parts.append(_box(px0, px0 + POST_LONG,
                              cy - POST_SHORT / 2.0, cy + POST_SHORT / 2.0,
                              0.0, H))

    solid = parts[0].fuse(*parts[1:]).clean()

    cuts = []
    hex2d = bd.RegularPolygon(NUT_AF / math.sqrt(3.0), 6)
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            x, y = sx * HOLE_X, sy * HOLE_Y
            cuts.append(bd.Pos(x, y, -1.0) * bd.Cylinder(
                HOLE_D / 2.0, H + 2.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
            cuts.append(bd.Pos(x, y, H - NUT_DEPTH)
                        * bd.extrude(hex2d, NUT_DEPTH + 0.2))
    solid = solid.cut(*cuts).clean()
    solid.label = "battery_tray_10mm"
    return solid


if __name__ == "__main__":
    p = build()
    b = p.bounding_box()
    print(f"tray {b.max.X - b.min.X:.2f} x {b.max.Y - b.min.Y:.2f}"
          f" x {b.max.Z - b.min.Z:.2f}  valid={p.is_valid}"
          f"  solids={len(p.solids())}")
    print(f"volume {p.volume / 1000:.3f} cm3"
          f"  ({p.volume / 1000 * 1.24:.0f} g PLA)")
    print(f"holes dia {HOLE_D} at X +-{HOLE_X:.2f}  Y +-{HOLE_Y:.2f}")
    print(f"walls {WALL}  floor {FLOOR}  nut pocket A/F {NUT_AF}"
          f" x {NUT_DEPTH} deep")
    print("export_step:", bd.export_step(p, str(STEP_OUT)), STEP_OUT)
    print("export_stl:", bd.export_stl(p, str(STL_OUT), tolerance=0.005,
                                      angular_tolerance=0.2), STL_OUT)
