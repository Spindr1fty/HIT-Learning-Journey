r"""Two thin gear blanks for a quick bolt-circle fit test, 2 mm thick.

WHY THIN
A full gear is 16 mm thick and takes about 25 minutes. This is a guessing
expedient to find which horn bolt circle is right, so it prints in a couple of
minutes and the screws either go in or they do not.

The 1.2 mm centring recess is deliberately OMITTED: in a 2 mm part it would
leave an 0.8 mm floor and the thing would be floppy. Without it the blank
stands 1.2 mm off the horn on the raised boss, which is fine for checking hole
alignment -- the screws still pass through and reach the horn's threads.

HOW TO TELL THEM APART
The two blanks differ only in hole positions, so they look identical. Each gets
small marker holes inside the rim -- clear at a glance, clear in the slicer,
and clear after printing:

    BCD 14.0  ->  1 marker hole
    BCD 14.4  ->  2 marker holes

Put them on the bed as exported; both are centred on Z = 0.

A 2 mm gear is a gauge, not a part. The real one must be printed at 16 mm so
the tooth flanks carry load and the recess can seat on the horn.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cadgen import build123d as bd  # noqa: E402

import z_params as P  # noqa: E402
import z_pinion as Z  # noqa: E402

DESKTOP = Path(r"C:\Users\Spindrift\Desktop")

THICKNESS = 2.0
HORN_HOLE_D = 3.5
HORN_HOLES = 4
MARK_R = 13.0          # marker radius, clear of both the horn holes and the root
MARK_D = 3.0
MARK_ANGLES = {1: (90.0,), 2: (80.0, 110.0)}

VERSIONS = (
    ("z_pinion_BCD140_t2", 14.0, 1),
    ("z_pinion_BCD144_t2", 14.4, 2),
)


def build(bcd, markers):
    pts = Z._gear_points()
    face = bd.Face(bd.Polyline(*[(x, y, 0.0) for x, y in pts], close=True))
    body = bd.extrude(face, amount=THICKNESS)

    r = bcd / 2.0
    cuts = []
    for k in range(HORN_HOLES):
        a = 2 * math.pi * k / HORN_HOLES
        cuts.append(bd.Pos(r * math.cos(a), r * math.sin(a), -1.0)
                    * bd.Cylinder(HORN_HOLE_D / 2, THICKNESS + 2.0,
                                  align=(bd.Align.CENTER, bd.Align.CENTER,
                                         bd.Align.MIN)))
    for deg in MARK_ANGLES[markers]:
        a = math.radians(deg)
        cuts.append(bd.Pos(MARK_R * math.cos(a), MARK_R * math.sin(a), -1.0)
                    * bd.Cylinder(MARK_D / 2, THICKNESS + 2.0,
                                  align=(bd.Align.CENTER, bd.Align.CENTER,
                                         bd.Align.MIN)))
    return body.cut(*cuts).clean()


def main():
    print(f"desktop: {DESKTOP}")
    for name, bcd, markers in VERSIONS:
        part = build(bcd, markers)
        bb = part.bounding_box()
        cx = -(bb.min.X + bb.max.X) / 2.0
        cy = -(bb.min.Y + bb.max.Y) / 2.0
        cz = -bb.min.Z
        part = bd.Pos(cx, cy, cz) * part          # centre on the plate
        path = DESKTOP / f"{name}.step"
        ok = bd.export_step(part, str(path))
        print(f"  {path.name:<26} BCD {bcd:<5} "
              f"{markers} marker hole{'s' if markers > 1 else ''}"
              f"   {path.stat().st_size // 1024} KB"
              f"{'' if ok else '  EXPORT FAILED'}")
        print(f"     dia {bb.max.X - bb.min.X:.2f}  thickness "
              f"{bb.max.Z - bb.min.Z:.2f}  volume {part.volume / 1000:.3f} cm3"
              f"  valid={part.is_valid}  solids={len(part.solids())}")
    print()
    print("both are 2 mm gauges -- print them fast, screw them onto the horn,")
    print("and whichever one threads in is the real bolt circle")


if __name__ == "__main__":
    main()
