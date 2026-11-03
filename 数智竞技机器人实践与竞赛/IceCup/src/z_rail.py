"""Z-axis guide rail: 30 x 30 square bar, FIXED to the chassis.

Square rather than round or dovetailed because the carriage wraps it on all
four sides and the only load is the gripper's cantilever. The bearing length
(60 mm) is 2x the section, which is what stops the carriage nodding.

The foot flange has the four datum holes for the whole Z module. The rack
bolts to the same plate but through SLOTS, because the mesh distance has to be
trimmed on the bench.

Print standing up if you can afford the height, or lying down for smoother
bearing faces -- lying down puts the layer lines along the slide instead of
across it, which is what you want.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402

FOOT_Z = 0.0                 # sits ON the base plate, not inside it
FOOT_TOP = 8.0
FOOT_HALF = 25.0             # foot is 50 x 50
FOOT_HOLE_D = 4.5
FOOT_HOLE_AT = 18.0          # +/- in X and Y
TOP_CHAMFER = 1.0

# Hollow the bar: solid would be 288 cm3 of filament for a part that only ever
# carries the gripper's cantilever. A closed box section keeps the four bearing
# faces solid (what actually matters for a slide) and drops ~2/3 of the mass.
CORE_WALL = 2.5
CORE_END_GAP = 5.0


def _rail():
    bar = bd.Pos(-P.RAIL_W / 2, -P.RAIL_W / 2, 0.0) * bd.Box(
        P.RAIL_W, P.RAIL_W, P.RAIL_LEN,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))

    foot = bd.Pos(-FOOT_HALF, -FOOT_HALF, FOOT_Z) * bd.Box(
        2 * FOOT_HALF, 2 * FOOT_HALF, FOOT_TOP - FOOT_Z,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))

    rail = (bar + foot).clean()

    core = P.RAIL_W / 2 - CORE_WALL
    cavity = bd.Pos(-core, -core, CORE_END_GAP) * bd.Box(
        2 * core, 2 * core, P.RAIL_LEN - 2 * CORE_END_GAP,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    rail = rail.cut(cavity)

    holes = [
        bd.Pos(sx * FOOT_HOLE_AT, sy * FOOT_HOLE_AT, FOOT_Z - 1.0)
        * bd.Cylinder(FOOT_HOLE_D / 2, FOOT_TOP - FOOT_Z + 2.0,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for sx in (-1, 1) for sy in (-1, 1)
    ]
    rail = rail.cut(*holes).clean()

    rail.label = "z_rail"
    return rail


@step(out="../newSTEP/z_rail.step")
def z_rail():
    return _rail()


if __name__ == "__main__":
    r = z_rail()
    b = r.bounding_box()
    print(f"rail {P.RAIL_W} x {P.RAIL_W} x {P.RAIL_LEN}"
          f"  foot {2 * FOOT_HALF} x {2 * FOOT_HALF} x {FOOT_TOP - FOOT_Z}")
    print(f"bbox X {b.max.X - b.min.X:.3f}  Y {b.max.Y - b.min.Y:.3f}"
          f"  Z {b.max.Z - b.min.Z:.3f}  valid={r.is_valid}"
          f"  solids={len(r.solids())}")
    print(f"carriage travel Z {P.Z_MIN}..{P.Z_MAX}"
          f"  (carriage half length {P.CARRIAGE_LEN / 2})")
    print(f"clearance to foot at bottom: {P.Z_MIN - P.CARRIAGE_LEN / 2 - FOOT_TOP:.2f} mm")
    print(f"rail top margin over carriage: "
          f"{P.RAIL_LEN - (P.Z_MAX + P.CARRIAGE_LEN / 2):.2f} mm")
    print(f"volume {r.volume / 1000:.3f} cm3")
