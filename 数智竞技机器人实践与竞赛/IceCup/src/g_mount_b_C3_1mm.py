r"""1 mm thin-wall fit-test version of C3 (src/g_mount_b_C3.py).

Purpose: a cheap, fast print that answers the four assembly questions before
the 44.2 g real part is made --
  1. does the servo body + its 52 x 20 flange slide in through the 53 x 21
     rear window, all the way to the front posts?
  2. can a 3 mm hex key reach the four M4 socket heads straight from the rear?
  3. do the eight foot holes (X 19/27/35/43, Y 15.0/85.38) line up with the
     plate underneath, with room for a screwdriver and a washer?
  4. do the mirrored wire windows sit where the cable actually comes out?

WHAT IS 1 mm (only the walls C3 ADDED):
    foot        5   -> 1   (top face stays at Z = 14, so it thins downward)
    rear plate  2.5 -> 1   (X 49..50, thins inward)
    side panels 3   -> 1   (inner faces stay at Y 23.69 / 76.69)
    top cover   3   -> 1   (underside stays at Z = 35, so it thins upward)
No chamfers: a 1 mm chamfer on a 1 mm wall leaves nothing.

WHAT IS STILL SOLID: the imported rev30 front arch (flange posts, top beam,
two triangular ribs).  After the old foot is cut away it is only ~1.7 cm3, and
it is the part that actually clamps the flange -- keeping it solid means the
test piece can really be bolted to the servo.

INTERFACE DIMENSIONS UNCHANGED FROM C3 (these are the point of the test):
    foot outline X 0..50, Y 9.94..90.44, top Z 14
    rear window 60 x 20.4 at Y 20.19..80.19, Z 14..34.4
    side panel inner faces Y 23.19 / 77.19   (flange 52 passes with 1.0/side)
    top cover underside Z 35                 (flange top Z 34 -> 1 mm)
    wire windows X 33..37.5, Z 27..34, left Y 20.0..24.5 / right 75.88..80.38
    eight holes D4.5 at X 19/27/35/43, Y 15.0/85.38

THREE WAYS THE SAMPLE DIFFERS FROM THE REAL PART (documented, not defects):
    - the foot's underside is Z 13 instead of 9: laid on the mounting plate
      the sample stands 4 mm proud.  Hole X/Y positions are unaffected.
    - the rear plate thins inward, so the tail room behind the servo is
      11.5 instead of 10.
    - the roof top is Z 36 instead of 38, so the rev30 top beam sticks 2 mm
      above the roof.  Overall height 25 instead of 29.

Pure ASCII on purpose (cadgen reads model sources without an encoding).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b_C3 as M  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "newSTEP"
W = 1.0                       # the one thickness

# 1 mm wall positions -- every *interface* face keeps its C3 coordinate
FOOT_Z0 = M.FOOT_Z1 - W                    # 13   (top stays 14)
REAR_X0 = M.REAR_X1 - W                    # 49   (outer stays 50)
SIDE_Y = ((M.SIDE_Y[0][1] - W, M.SIDE_Y[0][1]),   # 22.69..23.69
          (M.SIDE_Y[1][0], M.SIDE_Y[1][0] + W))   # 76.69..77.69
TOP_Z1 = M.TOP_Z0 + W                      # 36   (underside stays 35)


def build():
    p = bd.import_step(str(M.BASE))

    # 1) drop the old rev30 foot, keep posts / ribs / top beam
    p = p.cut(M._box(-1.0, 51.0, -1.0, 91.0, 8.9, M.FOOT_Z1)).clean()

    # 2) 1 mm foot, top face still at Z = 14, plus the fusion bosses
    p = p.fuse(M._box(M.X0, M.X1, M.Y0, M.Y1, FOOT_Z0, M.FOOT_Z1))
    bosses = []
    for y0, y1 in M.POST_Y:
        bosses.append(M._box(M.POST_X[0], M.POST_X[1], y0, y1,
                             M.FOOT_Z1 - M.OV, M.FOOT_Z1 + M.OV))
    for y0, y1 in M.RIB_Y:
        bosses.append(M._box(M.RIB_X[0], M.RIB_X[1], y0, y1,
                             M.FOOT_Z1 - M.OV, M.FOOT_Z1 + M.OV))
    p = p.fuse(*bosses).clean()

    # 3) 1 mm rear plate + the same 53 x 21 window
    p = p.fuse(M._box(REAR_X0, M.REAR_X1, M.Y0, M.Y1, M.REAR_Z0, M.REAR_Z1))
    p = p.cut(M._box(REAR_X0 - 1.0, M.REAR_X1 + 1.0, M.WIN_Y0, M.WIN_Y1,
                     M.WIN_Z0, M.WIN_Z1))

    # 4) 1 mm side panels + the same mirrored wire windows
    for y0, y1 in SIDE_Y:
        p = p.fuse(M._box(M.SIDE_X0, M.SIDE_X1, y0, y1,
                          M.SIDE_Z0, M.SIDE_Z1))
    for y0, y1 in M.WIRE_Y:
        p = p.cut(M._box(M.WIRE_X0, M.WIRE_X1, y0, y1, M.WIRE_Z0, M.WIRE_Z1))

    # 5) 1 mm roof, underside still at Z = 35
    p = p.fuse(M._box(M.TOP_X0, M.TOP_X1, M.TOP_Y0, M.TOP_Y1,
                      M.TOP_Z0, TOP_Z1))

    # 6) the same eight foot holes
    for hx in M.HOLE_X:
        for hy in M.HOLE_Y:
            p = p.cut(M._cyl_z(hx, hy, FOOT_Z0 - 1.0, M.FOOT_Z1 + 1.0,
                               M.HOLE_D))

    p = p.clean()
    p.label = "C3_1mm"
    return p


if __name__ == "__main__":
    p = build()
    b = p.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"valid={p.is_valid}  solids={len(p.solids())}"
          f"  vol {p.volume / 1000:.3f} cm3 ({p.volume / 1000 * 1.24:.1f} g PLA)")
    bd.export_step(p, str(OUT / "g_mount_b_C3_1mm.step"))
    print("wrote", OUT / "g_mount_b_C3_1mm.step")
    bd.export_stl(p, str(OUT / "g_mount_b_C3_1mm.stl"),
                  tolerance=0.01, angular_tolerance=0.3)
    print("wrote", OUT / "g_mount_b_C3_1mm.stl")
