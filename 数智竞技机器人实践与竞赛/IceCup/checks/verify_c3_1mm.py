r"""Verify the 1 mm C3 fit-test piece against the servo and the tools.

Checks, in order:
  A  where the rev30 flange holes actually are (measured from the base STEP)
  B  insertion sweep: the servo translated from 60 mm behind the rear plate to
     its final position, in 1 mm steps -- every step must be free of the walls
     C3 added, so the only allowed contact is the rev30 flange/post overlap
  C  four M4 socket heads (D7 x 4) inside the box at the flange holes
  D  a straight 3 mm hex key from the rear window into each socket
  E  eight foot holes: D9 washer + D7 head on the foot, D5 driver from above
  F  the same numbers for the real (3 mm wall) C3 part, for comparison

Run:  cd src && uvx ... python ../checks/verify_c3_1mm.py
Pure ASCII on purpose.
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b_C3 as M          # noqa: E402
import g_mount_b_C3_1mm as T      # noqa: E402
import g_mount_b as B             # noqa: E402
import g_servo as S               # noqa: E402


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def cyl_x(x0, x1, cy, cz, dia):
    return bd.Pos((x0 + x1) / 2.0, cy, cz) * bd.Rot(0, 90, 0) * bd.Cylinder(
        dia / 2.0, x1 - x0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))


def cyl_z(cx, cy, z0, z1, dia):
    return bd.Pos(cx, cy, (z0 + z1) / 2.0) * bd.Cylinder(
        dia / 2.0, z1 - z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))


def servo_at(dx=0.0):
    """The servo in the bracket frame, slid dx mm toward the rear (+X)."""
    s = bd.Pos(B.SERVO_X, B.SERVO_Y, B.SERVO_Z) * B._servo_rot() * \
        S.servo_solid()
    return bd.Pos(dx, 0.0, 0.0) * s


def vol(a, b):
    r = a & b
    return 0.0 if r is None else r.volume


# ---------------------------------------------------------------- A: holes
def flange_holes():
    """Centres of the rev30 flange holes, measured off the imported base.

    Each D4.5 hole through the 5 mm posts comes out of the STEP as two
    half-cylinder faces, and the two holes on one Z level must NOT be merged
    (they are 48.5 apart in Y).  So: bucket the faces by Z centre, then inside
    each bucket merge only Y intervals that touch.
    """
    base = bd.import_step(str(M.BASE))
    buckets = {}
    for f in base.faces():
        if "CYLINDER" not in str(f.geom_type):
            continue
        b = f.bounding_box()
        if b.min.X < -0.2 or b.max.X > 5.2:      # front posts only
            continue
        if not (3.0 < (b.max.Z - b.min.Z) < 6.0):   # D4.5 through a 5 mm post
            continue
        cz = round((b.min.Z + b.max.Z) / 2.0, 3)
        buckets.setdefault(cz, []).append((b.min.Y, b.max.Y))

    holes = []
    for cz, spans in sorted(buckets.items()):
        spans.sort()
        merged = [list(spans[0])]
        for lo, hi in spans[1:]:
            if lo <= merged[-1][1] + 1e-6:
                merged[-1][1] = max(merged[-1][1], hi)
            else:
                merged.append([lo, hi])
        for lo, hi in merged:
            holes.append((round((lo + hi) / 2.0, 3), cz))
            print(f"     hole  Y {(lo+hi)/2:7.3f}  Z {cz:6.3f}"
                  f"  D{hi-lo:.2f}  (Y span {lo:.3f}..{hi:.3f})")
    holes.sort()
    print("A  rev30 flange holes measured from the base, (Y, Z):", holes)
    return holes


def main():
    holes = flange_holes()

    thin = T.build()
    real = M.build(chamfer=False)
    print(f"\n   1 mm sample: vol {thin.volume/1000:.3f} cm3"
          f"  valid={thin.is_valid}  solids={len(thin.solids())}")
    print(f"   real C3 (unchamfered, same check basis):"
          f" vol {real.volume/1000:.3f} cm3  valid={real.is_valid}"
          f"  solids={len(real.solids())}")

    heads = None
    for cy, cz in holes:
        h = cyl_x(7.5, 11.5, cy, cz, 7.0)
        heads = h if heads is None else heads + h
    heads = heads.clean()

    print("\nB  insertion sweep: servo slid in from the rear (+X) to its final"
          "\n   position.  0.5 mm steps over the last 12 mm, 2 mm beyond that.")
    steps = [i * 0.5 for i in range(0, 25)] + [float(i) for i in range(13, 61, 2)]
    for name, p in (("1 mm sample", thin), ("real C3", real)):
        hit = []
        for dx in steps:
            v = vol(p, servo_at(dx))
            if v > 1e-6:
                hit.append((dx, round(v, 3)))
        print(f"   {name}: {len(steps)} positions, {len(hit)} in contact ->"
              f" {hit[:6]}{' ...' if len(hit) > 6 else ''}")
        free = [dx for dx in steps if dx not in [h[0] for h in hit]]
        print(f"        clear all the way in: {len(free)}/{len(steps)}"
              f" positions; contact only at dx="
              f"{sorted({h[0] for h in hit})}"
              f"  (dx=0 is the flange landing on the rev30 posts, by design)")

    print("\nB2 same sweep but with the four M4 bolts PRE-FITTED in the flange"
          "\n   (D7 heads riding behind it).  Only possible if the rear window"
          "\n   is wider than the head pattern: heads span Y 22.44..77.94.")
    for name, p in (("1 mm sample", thin), ("real C3", real)):
        hit = []
        for dx in steps:
            s = servo_at(dx)
            hs = bd.Pos(dx, 0.0, 0.0) * heads
            v = vol(p, s) + vol(p, hs)
            if v > 1e-6:
                hit.append((dx, round(v, 3)))
        print(f"   {name}: {len(hit)} position(s) in contact -> {hit[:8]}"
              f"{' ...' if len(hit) > 8 else ''}")

    print("\nC  four M4 socket heads, D7 x 4, inside at X 7.5..11.5")
    for name, p in (("1 mm", thin), ("C3", real)):
        print(f"   {name}: head overlap {vol(p, heads):.4f} mm3"
              f"   (0 = the heads fit inside the box)")

    print("\nD  straight 3 mm hex key from the rear window into each socket")
    for cy, cz in holes:
        k = cyl_x(9.0, 60.0, cy, cz, 3.0)
        print(f"   hole Y {cy:7.3f} Z {cz:6.3f}:  1 mm {vol(thin, k):.4f}"
              f"   C3 {vol(real, k):.4f}")

    print("\nE  eight foot holes: washer D9x1 + head D7x4 on the foot top,"
          "\n   D5 driver straight down from Z 40")
    tot_w = tot_h = tot_d = 0.0
    for hx in M.HOLE_X:
        for hy in M.HOLE_Y:
            w = cyl_z(hx, hy, 14.0, 15.0, 9.0)
            h = cyl_z(hx, hy, 15.0, 19.0, 7.0)
            d = cyl_z(hx, hy, 19.0, 40.0, 5.0)
            tot_w += vol(thin, w)
            tot_h += vol(thin, h)
            tot_d += vol(thin, d)
    print(f"   1 mm sample: washer {tot_w:.4f}  head {tot_h:.4f}"
          f"  driver {tot_d:.4f} mm3   (all 0 = clear access)")
    tot_w = tot_h = tot_d = 0.0
    for hx in M.HOLE_X:
        for hy in M.HOLE_Y:
            tot_w += vol(real, cyl_z(hx, hy, 14.0, 15.0, 9.0))
            tot_h += vol(real, cyl_z(hx, hy, 15.0, 19.0, 7.0))
            tot_d += vol(real, cyl_z(hx, hy, 19.0, 40.0, 5.0))
    print(f"   real C3    : washer {tot_w:.4f}  head {tot_h:.4f}"
          f"  driver {tot_d:.4f} mm3")

    print("\nF  wall thickness sanity, 1 mm sample")
    b = thin.bounding_box()
    print(f"   bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}"
          f"..{b.max.Y:.2f}  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"   foot top Z {M.FOOT_Z1}  roof underside Z {M.TOP_Z0}"
          f"  side inner Y {M.SIDE_Y[0][1]}/{M.SIDE_Y[1][0]}"
          f"  rear outer X {M.REAR_X1}")
    print(f"   rear window {M.WIN_Y1-M.WIN_Y0:.1f} x"
          f" {M.WIN_Z1-M.WIN_Z0:.1f}   flange {S.FLANGE_SPAN:.0f} x"
          f" {S.FLANGE_W:.0f}")


if __name__ == "__main__":
    main()
