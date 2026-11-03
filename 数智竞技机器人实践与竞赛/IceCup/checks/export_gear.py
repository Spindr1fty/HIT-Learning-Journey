r"""Put the gear where the user can get at it: Desktop, as STEP and as DXF.

STEP  for the 3D printer. This is the right way to make it: 16 mm thick, with
      a 1.2 mm centring recess for the horn's outer diameter, in PLA. The tooth
      tips are 1.03 mm wide and carry under 3 N, which PLA handles easily.

DXF   for the laser, if a flat copy is wanted for fit checking or laminating.
      It is the gear's true outline plus the four horn holes, in millimetres,
      at 1:1. Read the caveats below before cutting anything load-bearing.

WHY A LASER-CUT GEAR IS A COMPROMISE
    16 mm thick cannot be cut in one pass, so it has to be laminated from
    5-6 sheets; the teeth then have to line up between layers.
    1.03 mm acrylic teeth are brittle and chip at the tips.
    Laser kerf eats 0.1-0.2 mm per side, which changes tooth thickness and
    therefore the backlash the mesh was designed around.
    The 1.2 mm recess cannot be cut at all in a flat profile.

So: STEP to the printer. DXF only for checking the hole pattern or for a
non-loaded mock-up.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import z_pinion as Z  # noqa: E402

DESKTOP = Path(r"C:\Users\Spindrift\Desktop")


def dxf_gear(path):
    pts = Z._gear_points()
    r_bcd = Z.HORN_BCD / 2.0
    out = ["0\nSECTION\n2\nENTITIES\n"]

    # gear outline as a closed polyline of LINE segments
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        out.append("0\nLINE\n8\nGEAR\n")
        out.append(f"10\n{x1:.4f}\n20\n{y1:.4f}\n30\n0.0\n")
        out.append(f"11\n{x2:.4f}\n21\n{y2:.4f}\n31\n0.0\n")

    # the four horn holes
    for k in range(Z.HORN_HOLES):
        a = 2 * math.pi * k / Z.HORN_HOLES
        cx, cy = r_bcd * math.cos(a), r_bcd * math.sin(a)
        out.append("0\nCIRCLE\n8\nHOLES\n")
        out.append(f"10\n{cx:.4f}\n20\n{cy:.4f}\n30\n0.0\n")
        out.append(f"40\n{Z.HORN_HOLE_D / 2:.4f}\n")

    out.append("0\nENDSEC\n0\nEOF\n")
    Path(path).write_text("".join(out), encoding="ascii")


def main():
    print(f"desktop: {DESKTOP}")

    # STEP for the printer: copy the print-oriented one
    src = Path(__file__).resolve().parent.parent / "printSTEP" / "z_pinion.step"
    dst = DESKTOP / "z_pinion_print.step"
    dst.write_bytes(src.read_bytes())
    print(f"  {dst.name:<22} STEP, for the 3D printer"
          f"   {dst.stat().st_size // 1024} KB")

    # DXF for checking
    dpath = DESKTOP / "z_pinion.dxf"
    dxf_gear(dpath)
    print(f"  {dpath.name:<22} DXF, gear outline + {Z.HORN_HOLES} horn holes"
          f"   {dpath.stat().st_size // 1024} KB")

    pts = Z._gear_points()
    rs = [math.hypot(x, y) for x, y in pts]
    print()
    print("gear (from the same code that builds the solid)")
    print(f"  teeth ......... {Z.P.PINION_TEETH}")
    print(f"  module ........ {Z.P.MODULE}")
    print(f"  tip dia ....... {2 * Z.P.TIP_R:.3f}")
    print(f"  root dia ...... {2 * Z.P.ROOT_R:.3f}")
    print(f"  outline pts ... {len(pts)}")
    print(f"  max radius .... {max(rs):.3f}   min radius {min(rs):.3f}")
    print(f"  thickness ..... {Z.P.GEAR_W}")
    print()
    print(f"  horn holes: {Z.HORN_HOLES} x dia {Z.HORN_HOLE_D}"
          f" on BCD {Z.HORN_BCD}   (r = {Z.HORN_BCD / 2})")
    print(f"  centring recess: dia {Z.HORN_RECESS_D}"
          f" x {Z.HORN_RECESS_DEPTH} deep   <- DXF cannot carry this")


if __name__ == "__main__":
    main()
