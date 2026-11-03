"""Z-axis carriage: the moving sleeve plus the arm that reaches the pinion.

The sleeve wraps the rail on all four sides with SLIDE_CLEAR per face. Four
sides rather than two because the gripper hangs off the front and would
otherwise nod the carriage off the rail.

The arm sits at Y 8..20, beside the pinion (Y -8..8) and clear of the rack
(Y -8..8). One axle serves both, so the arm's end bore also supports the free
end of the pinion shaft -- the servo bearing alone would be a cantilever.

Local Z runs 0 (sleeve bottom) to CARRIAGE_LEN. Place the part by putting its
Z centre where z_params says.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402

BORE = P.RAIL_W + 2 * P.SLIDE_CLEAR          # 30.6
OUTER = P.RAIL_W + 2 * P.WALL                # 42.0
HALF = OUTER / 2.0

ARM_Z = (18.0, 42.0)                         # arm band inside the sleeve
AXLE_D = 6.2                                 # bore for the pinion shaft end
AXLE_Y = (P.ARM_Y[0] + P.ARM_Y[1]) / 2.0     # 14.0

LIGHTEN_D = 10.0                             # pockets to save filament
LIGHTEN_AT = ((0.0, 0.0,),)

MOUNT_Y = -16.0                              # cradle pilot holes, -X wall
MOUNT_ZS = (12.0, 48.0)                      # local Z, before the shift
MOUNT_HOLE_D = 3.5                           # M4 self-tap pilot, NOT clearance

# --- gripper fork mounting, +X wall --------------------------------------
# M4 again. The fork's side is a 4.5 clearance slot; THIS side is the 3.5 pilot
# the thread bites into. Wall is 5.7 mm, so an M4 x 14 through a 10 mm fork
# block bites 4 mm and leaves 1.7 mm -- enough for the ~1 N the fork carries,
# and it never pokes through into the rail bore.
FORK_MOUNT_Y = 10.0
FORK_MOUNT_Z = 30.0
FORK_PILOT_D = 3.5

# Blind depth for both mounting hole sets. The wall is 5.7 mm and the rail runs
# immediately behind it, so the screw must never break through.
MOUNT_DEPTH = 4.0


def _carriage():
    sleeve = bd.Pos(-HALF, -HALF, 0.0) * bd.Box(
        OUTER, OUTER, P.CARRIAGE_LEN,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    bore = bd.Pos(-BORE / 2, -BORE / 2, -1.0) * bd.Box(
        BORE, BORE, P.CARRIAGE_LEN + 2.0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    sleeve = sleeve.cut(bore)

    # NO ARM. The arm used to reach out to X = -56 to carry the old bolt-on servo
    # cradle. The cradle is now a collar that wraps this sleeve, so the arm is
    # not only unnecessary -- it runs straight through the collar's 6 mm wall and
    # shares 1728 mm3 with it (12 x 12 x 12, exactly one arm cross-section).
    body = sleeve

    # --- mounting holes -------------------------------------------------
    # There are none, and there should not be. An earlier version tried to cut
    # them and failed silently: bd.Cylinder's axis runs along Z, but a wall hole
    # has to run along X, and they were placed at X = +/-22 which is outside the
    # 42 mm sleeve anyway. The part that got printed has no holes at all.
    #
    # That is fine now, because both the servo cradle and the fork hang off a
    # collar that grips the OUTSIDE of this sleeve. Nothing is bolted through
    # these walls, so there is no reason to weaken them.

    body = bd.Pos(0, 0, P.CARRIAGE_Z0) * body
    body.label = "z_carriage"
    return body


@step(out="../newSTEP/z_carriage.step")
def z_carriage():
    return _carriage()


if __name__ == "__main__":
    c = z_carriage()
    b = c.bounding_box()
    print(f"sleeve outer {OUTER}  bore {BORE}  length {P.CARRIAGE_LEN}"
          f"  clear/side {P.SLIDE_CLEAR}")
    print(f"arm Y {P.ARM_Y}  Z {ARM_Z}  reaches X {P.PINION_X}"
          f"  axle bore {AXLE_D} at Y {AXLE_Y}")
    print(f"bbox X {b.max.X - b.min.X:.3f}  Y {b.max.Y - b.min.Y:.3f}"
          f"  Z {b.max.Z - b.min.Z:.3f}  valid={c.is_valid}"
          f"  solids={len(c.solids())}")
    print(f"bearing length / section = {P.CARRIAGE_LEN / P.RAIL_W:.2f}"
          f" (want >= 2)")
    print(f"volume {c.volume / 1000:.3f} cm3")
    print(f"arm clear of pinion? pinion Y {P.GEAR_Y} vs arm Y {P.ARM_Y}"
          f" -> {'yes' if P.ARM_Y[0] >= P.GEAR_Y[1] else 'NO'}")
    print(f"arm clear of rack? rack Y {P.GEAR_Y} -> "
          f"{'yes' if P.ARM_Y[0] >= P.GEAR_Y[1] else 'NO'}")
