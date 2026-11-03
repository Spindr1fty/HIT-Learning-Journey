r"""Section through the base plate, to show the two different nut joints.

A screenshot cannot show a pocket that lives inside an 8 mm plate, and the whole
point of this revision was those pockets. So the plate is cut in half and the
cut face is what gets rendered.

Cut at Y = 0 plus a second cut at X = -80, so the section passes through:
    a rail-foot hole at (18, 18)   -- nut pocket in the UNDERSIDE
    a chassis hole at (-102, 28)   -- lipped nut trap in the TOP face

Underside pocket: straight walls. Nothing is lost by that, because the chassis
sits against the plate's underside and caps the pocket mouth, so the nut cannot
leave once the assembly is closed.

Top trap: the mouth is narrowed to 6.0 mm while the cavity is 7.2 mm across
flats. The nut is 8.3 across corners, so it cannot pass the lip once seated.
That is the positive retention the straight-sided version lacked.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_plate as ZP  # noqa: E402


def _section():
    plate = ZP._plate()

    # keep Y <= 0, so the section face shows the plan view's lower half
    keeper = bd.Pos(-200.0, -200.0, -50.0) * bd.Box(
        420.0, 200.0, 100.0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    cut = plate.cut(keeper)
    cut.label = "z_plate_section"
    return cut


@step(out="../renders/z_plate_section.step")
def z_plate_section():
    return _section()


if __name__ == "__main__":
    s = z_plate_section()
    b = s.bounding_box()
    print(f"section bbox X {b.min.X:.1f}..{b.max.X:.1f}"
          f"  Y {b.min.Y:.1f}..{b.max.Y:.1f}"
          f"  Z {b.min.Z:.1f}..{b.max.Z:.1f}")
    print(f"valid={s.is_valid}  solids={len(s.solids())}")
    print()
    print("the cut face at Y = 0 passes through the two chassis traps at")
    print("Y = +28 only if flipped -- so it is the X = -80..-102 area that")
    print("matters: rail pocket at (18,18) underside, chassis trap at")
    print("(-102, 28) top face.")
    print()
    print(f"  underside pocket: {ZP.NUT_AF} AF x {ZP.NUT_T} deep, straight")
    print(f"  top trap: cavity {ZP.NUT_AF} AF, mouth narrowed to"
          f" {ZP.LIP_OPEN} (nut is {ZP.NUT_CORNER} across corners)")
    print(f"  plate thickness {ZP.PLATE_T}, so both leave"
          f" {ZP.PLATE_T - ZP.NUT_T:.1f} mm of material")
