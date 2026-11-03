r"""Z-axis top cap, v5: rail collar + rack half-shell + two M4 screws.

Why it exists: the rack is a 320 mm PLA cantilever. Tying its top to the rail
turns the pair into a frame and stops the pinion walking out of mesh. Neither
the rail nor the carriage may be reprinted, so the cap GRIPS the rail instead
of being screwed into it.

    RAIL  collar: 30.4 square socket over the rail's top (0.2 per side), two M3
          grub screws in the +X / +Y walls take up the slack.
    RACK  a half-shell wraps the rack's top block on three sides (Y +- and -X,
          open at +X where the teeth pass), and the plate over it is screwed
          down with two M4 x 20 into the rack's dia 3.6 x 14 pilot holes. The
          M4 slots are 10.6 long in X so the rack can still be trimmed +-3 for
          the meshing centre distance; the pocket is correspondingly 27.2 wide.
          The shell's bottom stops at 306.44, i.e. 1.44 above the carriage.

Interface, module frame (X toward the teeth, Z up):

    rail   30 x 30, top face Z 320.0, solid above Z 315
    rack   top face Z 320.44; body 20 x 16 (X -96.5 .. -76.5, Y +-8); teeth to
           X -72; spine -116.5 .. -96.5 up to Z 300 only; pilots dia 3.6 x 14
           at (X -86.5, Y +-5)
    cap    plate  X -104 .. 21.2, Y +-21.2, Z 320.44 .. 328.44
           collar X +-21.2, Y +-21.2, Z 306.44 .. 320.44, socket 30.4
           shell  X -104 .. -73, Y +-13.3, Z 306.44 .. 320.44,
                  pocket X -100.2 .. -73, Y +-8.3

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

RACK_TOP = 320.0        # rack and rail tops are flush now
PLATE_T = 8.0
PLATE_X = (-104.0, 21.2)
HALF_Y = 21.2

DOWN = 306.44                          # collar / shell bottom (carriage 305)
H = RACK_TOP - DOWN                    # 14.0
M3_PILOT = 2.5
M3_Z = DOWN + H / 2.0                  # 313.44

RAIL_SOCKET = 30.4                     # rail is 30.0
RAIL_OUT = 42.4

SHELL_X = (-104.0, -73.0)
SHELL_WALL = 3.8                       # back wall thickness
SHELL_Y = (8.3, 13.3)                  # inner / outer, rack block is Y +-8

M4_D = 4.6
M4_X = -86.5
M4_Y = 5.0
M4_SLOT_X = 10.6                       # dia + 6 mm of centre-distance trim

RELIEF = (-77.5, -70.5)                # tooth tips are X -76.5 .. -72
RELIEF_D = 2.0


def _box(x0, y0, z0, x1, y1, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(x1 - x0, y1 - y0, z1 - z0,
                                       align=(bd.Align.MIN, bd.Align.MIN,
                                              bd.Align.MIN))


def _obround(xc, yc, z0, length_x, dia, height_z):
    parts = [_box(xc - (length_x - dia) / 2.0, yc - dia / 2.0, z0,
                  xc + (length_x - dia) / 2.0, yc + dia / 2.0, z0 + height_z)]
    for s in (-1.0, 1.0):
        parts.append(bd.Pos(xc + s * (length_x - dia) / 2.0, yc, z0)
                     * bd.Cylinder(dia / 2.0, height_z,
                                   align=(bd.Align.CENTER, bd.Align.CENTER,
                                          bd.Align.MIN)))
    return parts


def _cap():
    plate = _box(PLATE_X[0], -HALF_Y, RACK_TOP, PLATE_X[1], HALF_Y,
                 RACK_TOP + PLATE_T)
    collar = _box(-RAIL_OUT / 2, -RAIL_OUT / 2, DOWN,
                  RAIL_OUT / 2, RAIL_OUT / 2, RACK_TOP)

    shell_walls = []
    for y0, y1 in ((SHELL_Y[0], SHELL_Y[1]), (-SHELL_Y[1], -SHELL_Y[0])):
        shell_walls.append(_box(SHELL_X[0], y0, DOWN, SHELL_X[1], y1, RACK_TOP))
    shell_walls.append(_box(SHELL_X[0], -SHELL_Y[1], DOWN,
                            SHELL_X[0] + SHELL_WALL, SHELL_Y[1], RACK_TOP))

    cap = (plate + collar + shell_walls[0] + shell_walls[1]
           + shell_walls[2]).clean()

    # rail socket
    cap = cap.cut(_box(-RAIL_SOCKET / 2, -RAIL_SOCKET / 2, DOWN,
                       RAIL_SOCKET / 2, RAIL_SOCKET / 2, RACK_TOP + 0.2))

    # relief over the tooth tips (only across the rack block, so the shell
    # walls stay attached to the plate)
    cap = cap.cut(_box(RELIEF[0], -SHELL_Y[0], RACK_TOP - 0.2, RELIEF[1],
                       SHELL_Y[0], RACK_TOP + RELIEF_D))

    # 2 x M4 through-slots into the rack's top
    cutters = []
    for sy in (-1.0, 1.0):
        cutters += _obround(M4_X, sy * M4_Y, RACK_TOP - 1.0, M4_SLOT_X, M4_D,
                            PLATE_T + 2.0)
    cap = cap.cut(*cutters)

    # two M3 through the rail collar walls (+X and +Y)
    grubs = [
        bd.Pos(RAIL_OUT / 2 + 1.0, 0.0, M3_Z)
        * bd.Cylinder(M3_PILOT / 2.0, RAIL_OUT / 2 + 2.0, rotation=(0, 90, 0)),
        bd.Pos(0.0, RAIL_OUT / 2 + 1.0, M3_Z)
        * bd.Cylinder(M3_PILOT / 2.0, RAIL_OUT / 2 + 2.0, rotation=(90, 0, 0)),
    ]
    cap = cap.cut(*grubs).clean()

    cap.label = "z_topcap"
    return cap


@step(out="../newSTEP/z_topcap.step")
def z_topcap():
    return _cap()


if __name__ == "__main__":
    c = z_topcap()
    b = c.bounding_box()
    print(f"cap {b.max.X - b.min.X:.1f} x {b.max.Y - b.min.Y:.1f}"
          f" x {b.max.Z - b.min.Z:.1f}  Z {b.min.Z:.2f}..{b.max.Z:.2f}"
          f"  valid={c.is_valid}  solids={len(c.solids())}")
    print(f"volume {c.volume / 1000:.2f} cm3"
          f"   ({c.volume / 1000 * 1.24:.0f} g at 100% infill)")
    print("rail socket", RAIL_SOCKET, " bottom", DOWN, "(carriage 305)")
    print("rack half-shell X", SHELL_X, " Y walls", SHELL_Y,
          " pocket", SHELL_X[0] + SHELL_WALL, "..", SHELL_X[1])
    print("M4 slots", M4_SLOT_X, "x", M4_D, "at X", M4_X, "Y +-", M4_Y)
