"""Emit print-ready STEPs: one file per part, pre-rotated and sitting on Z=0.

WHY THIS EXISTS
The six parts are modelled in one shared assembly frame, so importing them all
into a slicer scatters them through space at their assembled positions, with
the gear standing on edge and the rail 320 mm tall. That is correct for looking
at the fit and wrong for printing: a slicer needs each part flat on the plate
and oriented so its critical surfaces are in the XY plane.

This script rebuilds every part, applies the print orientation below, drops it
onto Z=0 and centres it in XY, then writes it to ../printSTEP/.

ORIENTATION CHOICES
  plate        as modelled      already flat
  rail         rotate -90 about X   the 320 mm axis lies along Y; the two
                                    bearing faces become top and bottom, and
                                    the layer lines run along the slide
  rack         rotate +90 about X   tooth profile lands in the XY plane, so the
                                    nozzle traces the flanks instead of
                                    stair-stepping them
  carriage     as modelled      the rail bore is already vertical
  pinion       rotate -90 about X   gear axis vertical, i.e. flat on the plate
  servo_mount  as modelled      pocket already opens upward

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import z_carriage  # noqa: E402
import z_pinion  # noqa: E402
import z_plate  # noqa: E402
import z_rack  # noqa: E402
import z_rail  # noqa: E402
import z_servo_mount  # noqa: E402
import g_fork  # noqa: E402
import g_fork_clamp  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "printSTEP"

# H2D build volume, dual-nozzle mode using the left nozzle
BED = (350.0, 320.0, 325.0)

# name -> (builder, rotation or None, note)
JOBS = (
    ("z_plate", z_plate._plate, None,
     "flat as modelled"),
    ("z_rail", z_rail._rail, bd.Rot(0, 90, 0),
     "lying along X, bearing faces up/down"),
    ("z_rack", z_rack._rack, bd.Rot(90, 0, 0),
     "profile in XY, teeth point +X"),
    ("z_carriage", z_carriage._carriage, None,
     "rail bore vertical"),
    ("z_pinion", z_pinion._pinion, bd.Rot(-90, 0, 0),
     "gear axis vertical, flat on plate"),
    # As modelled this part stands with its servo plate VERTICAL, so the four
    # M4 holes run horizontally and bridge across 4.4 mm. They came out of the
    # printer half closed and the servo could not be bolted on. Lay the part on
    # its face instead: the plate's normal becomes vertical and the holes print
    # as clean vertical bores. The collar's bore then lies horizontal and needs
    # support inside it.
    ("z_servo_mount", z_servo_mount._cradle, bd.Rot(90, 0, 0),
     "lying on its servo-side face, bolt holes vertical; support the collar bore"),
    ("g_fork", g_fork._head, None,
     "working plate flat on the bed; support the back plate"),
)


def _place(shape, rot):
    """Apply the print rotation, centre in XY, drop the lowest point onto Z=0."""
    s = rot * shape if rot is not None else shape
    bb = s.bounding_box()
    return bd.Pos(-(bb.min.X + bb.max.X) / 2.0,
                  -(bb.min.Y + bb.max.Y) / 2.0,
                  -bb.min.Z) * s


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"output: {OUT_DIR}")
    print(f"bed {BED[0]:.0f} x {BED[1]:.0f} x {BED[2]:.0f} mm")
    print()
    print(f"{'part':<16}{'X':>8}{'Y':>8}{'Z':>8}   {'fits':>5}  note")
    total = 0.0
    bad = []
    for name, build, rot, note in JOBS:
        shape = _place(build(), rot)
        bb = shape.bounding_box()
        dx = bb.max.X - bb.min.X
        dy = bb.max.Y - bb.min.Y
        dz = bb.max.Z - bb.min.Z
        fits = dx <= BED[0] and dy <= BED[1] and dz <= BED[2]
        if not fits:
            bad.append(name)
        dest = OUT_DIR / f"{name}.step"
        ok = bd.export_step(shape, str(dest))
        total += shape.volume
        print(f"{name:<16}{dx:>8.1f}{dy:>8.1f}{dz:>8.1f}"
              f"   {'yes' if fits else 'NO':>5}  {note}"
              f"{'' if ok else '   EXPORT FAILED'}")
    print()
    print(f"total {total / 1000:.1f} cm3  (~{total / 1000 * 1.24:.0f} g PLA)")
    if bad:
        print(f"DOES NOT FIT: {', '.join(bad)}")
    else:
        print("all parts fit the bed in the orientation given")
    print()
    print("each file is centred in XY and sits on Z=0 -- import all six and")
    print("they land side by side on the plate with no manual arranging")


if __name__ == "__main__":
    main()
