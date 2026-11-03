"""Servo clip plate, 60.400 x 39.000 x 5.0, 18 x dia 4.5 + one through window.

Source: dxf/\u8235\u673a\u5361\u6263.dxf (servo clip). The drawing carries no dimensions and no
text: 9 LINEs and 18 CIRCLEs, all on one continuous layer. Geometry was read
back from coordinates and normalised to the plate's lower-left corner:

    outline            60.400 x 39.000
    through window     42.400 x 23.000, margins L10.0 R8.0 T8.0 B8.0
    hole rows (x2)     7 holes, pitch 8.000, span 48.000, y = 4.25 / 34.75,
                       x = 4.15 + 8k  (row margins L4.15 R8.25)
    side holes (x4)    3.25 from the window edges, +-4.25 about the window
                       centre, 8.5 apart vertically
    holes              all dia 4.5 (R2.25) as drawn, no resizing needed

Idealisation follows the parts_data rules: row pitch pinned to 8.000 (two
columns carried +0.2 of drafting jitter), window height 23.001 -> 23.000, and
a duplicate LINE lying exactly on the bottom edge ignored. The 1 mm X offset
of the window (L10 / R8) and the asymmetric row margins are kept as drawn,
per user decision 2026-10-17; the four side holes are defined off the window,
so they move with it if the window is ever re-centred.

The window is a through-cut and the plate is 5 mm thick, both confirmed by the
user 2026-10-17. The 42.4 x 23.0 opening matches the 40 x 20 servo body
(Motor.dxf) with 1.2 / 1.5 mm side clearance.

Analytic volume: (60.4*39 - 42.4*23 - 18*pi*2.25^2) * 5 = 5470.612 mm3.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

from flatpart import build_flat  # noqa: E402

THICKNESS = 5.0
HOLE_DIAMETER = 4.5
PITCH = 8.0

OUTLINE = [(0.0, 0.0), (60.4, 0.0), (60.4, 39.0), (0.0, 39.0)]
WINDOW = (10.0, 8.0, 52.4, 31.0)

ROW_Y = (4.25, 34.75)
ROW_X0 = 4.15
ROW_COUNT = 7
SIDE_HOLES = [(6.75, 15.25), (6.75, 23.75), (55.65, 15.25), (55.65, 23.75)]


def holes():
    r = HOLE_DIAMETER / 2
    rows = [(ROW_X0 + PITCH * i, y, r) for y in ROW_Y for i in range(ROW_COUNT)]
    return rows + [(x, y, r) for x, y in SIDE_HOLES]


@step(out="../oldSTEP/servo_clip.step")
def servo_clip():
    return build_flat(OUTLINE, holes(), [], THICKNESS, "servo_clip",
                      windows=[WINDOW])


if __name__ == "__main__":
    b = servo_clip()
    box = b.bounding_box()
    print(f"outline {box.max.X - box.min.X:.3f} x {box.max.Y - box.min.Y:.3f}"
          f" x {box.max.Z - box.min.Z:.3f}  holes {len(holes())}"
          f"  window {WINDOW[2] - WINDOW[0]:.1f} x {WINDOW[3] - WINDOW[1]:.1f}")
    print(f"valid={b.is_valid} solids={len(b.solids())} "
          f"cyl_faces={sum(1 for f in b.faces() if f.geom_type == bd.GeomType.CYLINDER)}")
    print(f"volume {b.volume / 1000:.4f} cm3")
