r"""Every hole in the servo mount, checked with a probe that can actually tell
material from a void.

The probe is 0.3 mm a side, so a fully buried probe reads 0.027 mm3. The
threshold is a quarter of that. An earlier version used a 0.06 mm probe (volume
0.00022) against a 0.001 threshold, which classified BOTH "inside material" and
"inside a hole" as empty -- it reported PASS while the ribs were capping all
four bolt holes.

This is the check that has to run after ANY feature is added near a hole.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cadgen import build123d as bd  # noqa: E402

import z_servo_mount as SM  # noqa: E402

PROBE = 0.3
THRESH = 0.25 * PROBE ** 3


def material(part, x, y, z):
    p = bd.Pos(x, y, z) * bd.Box(
        PROBE, PROBE, PROBE,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    v = p.intersect(part)
    if v is None:
        return 0.0
    if hasattr(v, "volume"):
        return v.volume
    return sum(getattr(q, "volume", 0.0) for q in v if q is not None)


def main():
    m = SM._cradle()
    ok = True

    print("A. the four servo bolt holes, walked the full Y span")
    for sx in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            hx = SM.HOLE_CX + sx * SM.SERVO_SPAN_L / 2.0
            hz = SM.PINION_Z + sz * SM.SERVO_SPAN_W / 2.0
            ys = (-27, -26, -25, -24, -23, -22.5, -21, -20, -19, -18,
                  -17, -16.5, -15.5, -14.5, -13, -12)
            bad = [y for y in ys if material(m, hx, y, hz) > THRESH]
            state = "THROUGH" if not bad else f"BLOCKED at Y {bad}"
            print(f"   ({hx:7.2f}, {hz:5.1f})  {state}")
            ok = ok and not bad

    print("B. the collar's clamp screw, along X through both ears")
    yc = (SM.TAB_Y[0] + SM.TAB_Y[1]) / 2.0
    bad = [x for x in (-13, -11, -9, -6, -2, 2, 6, 9, 11, 13)
           if material(m, x, yc, SM.PINION_Z) > THRESH]
    print(f"   {'THROUGH' if not bad else 'BLOCKED at X ' + str(bad)}")
    ok = ok and not bad

    print("C. the plate ribs are present, in bands clear of the holes")
    for z in (140.0, 155.0, 165.0, 180.0):
        v = material(m, -60.0, SM.PLAT_Y[1] + 2.0, z)
        tag = "rib" if v > THRESH else "no rib"
        print(f"   Z={z:5.1f}  {tag}")
    # the ribs must NOT be at the hole rows (Z 155 / 165) or they cap the holes
    for z in (155.0, 165.0):
        v = material(m, -60.0, SM.PLAT_Y[1] + 2.0, z)
        if v > THRESH:
            print(f"   FAIL: a rib sits at Z={z}, which is a bolt hole row")
            ok = False

    print()
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
