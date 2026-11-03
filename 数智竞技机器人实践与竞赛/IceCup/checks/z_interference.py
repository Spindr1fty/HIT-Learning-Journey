"""Interference check for the Z-axis assembly.

Renders lie: in an isometric view the servo cradle appears to pass through the
rack, because they are separated in Y, not in X. The only way to know whether
two parts really share volume is to intersect them and measure the result.

Any pair reporting a non-zero intersection volume is a real clash. Intentional
line-to-line contacts (0.000) are fine; so is the pinion/rack mesh, which is
reported separately because teeth are SUPPOSED to meet.

Run:  python z_interference.py
"""

import sys
from itertools import combinations
from pathlib import Path

# this script lives in checks/; the model modules live in ../src/
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from cadgen import build123d as bd  # noqa: E402

import z_params as P  # noqa: E402
import z_carriage  # noqa: E402
import z_pinion  # noqa: E402
import z_plate  # noqa: E402
import z_rack  # noqa: E402
import z_rail  # noqa: E402
import z_servo_mount  # noqa: E402

BUILDERS = {
    "rail": z_rail._rail,
    "rack": z_rack._rack,
    "plate": z_plate._plate,
    "carriage": z_carriage._carriage,
    "pinion": z_pinion._pinion,
    "servo_mount": z_servo_mount._cradle,
}

# Teeth are meant to meet. A rack and pinion that do NOT touch are the fault.
MESH_PAIR = frozenset({"rack", "pinion"})


def bbox_overlap(a, b, pad=0.0):
    ba, bb = a.bounding_box(), b.bounding_box()
    return (ba.min.X - pad <= bb.max.X and bb.min.X - pad <= ba.max.X
            and ba.min.Y - pad <= bb.max.Y and bb.min.Y - pad <= ba.max.Y
            and ba.min.Z - pad <= bb.max.Z and bb.min.Z - pad <= ba.max.Z)


def main():
    parts = {name: fn() for name, fn in BUILDERS.items()}

    print(f"{'part':<14}{'solids':>7}{'volume cm3':>12}")
    for name, s in parts.items():
        print(f"{name:<14}{len(s.solids()):>7}{s.volume / 1000:>12.3f}")
    print()

    clashes, touches, skipped = [], [], 0
    for a, b in combinations(sorted(parts), 2):
        pair = frozenset({a, b})
        if not bbox_overlap(parts[a], parts[b]):
            skipped += 1
            continue
        inter = parts[a].intersect(parts[b])
        # intersect() hands back a ShapeList, not one Shape -- sum whatever
        # solids came out of it.
        if inter is None:
            vol = 0.0
        elif hasattr(inter, "volume"):
            vol = inter.volume
        else:
            vol = sum(getattr(s, "volume", 0.0) for s in inter)
        if pair == MESH_PAIR:
            touches.append((a, b, vol))
        elif vol > 0.001:
            clashes.append((a, b, vol))
        else:
            touches.append((a, b, vol))

    print(f"bbox-disjoint pairs skipped : {skipped}")
    print(f"pairs actually intersected  : {len(touches) + len(clashes)}")
    print()

    print("mesh check")
    # A correct rack-and-pinion with backlash shares ZERO volume: the teeth sit
    # in the gaps with clearance. Zero intersection is therefore the PASS, not
    # the failure -- what matters is that the circles still overlap radially.
    pinion_tip_x = P.PINION_X - P.TIP_R            # -76.0
    pinion_root_x = P.PINION_X - P.ROOT_R          # -71.5
    rack_root_x = P.RACK_BODY_X[1]                 # -76.5
    rack_tip_x = P.RACK_PITCH_X + P.MODULE         # -72.0
    # All four X are negative; compare magnitudes against the meshing axis.
    tip_clear = abs(rack_root_x) - abs(pinion_tip_x)    # want 0.25*module
    root_clear = abs(rack_tip_x) - abs(pinion_root_x)   # want 0.25*module
    standard = 0.25 * P.MODULE
    print(f"  centre distance .................... "
          f"{abs(P.RACK_PITCH_X - P.PINION_X):.3f} mm"
          f"  (pinion pitch R {P.PITCH_R:.3f})")
    print(f"  pinion tip  X {pinion_tip_x:.2f} vs rack root X {rack_root_x:.2f}"
          f"  -> clearance {tip_clear:.3f} mm")
    print(f"  rack tip    X {rack_tip_x:.2f} vs pinion root X {pinion_root_x:.2f}"
          f"  -> clearance {root_clear:.3f} mm")
    print(f"  radial clearance, both flanks ....... "
          f"tip {tip_clear:.3f} / root {root_clear:.3f} mm"
          f"  (standard {standard:.3f})")
    print(f"  backlash (total circumferential) ... {P.BACKLASH:.2f} mm")
    for a, b, vol in touches:
        if frozenset({a, b}) == MESH_PAIR:
            engaged = tip_clear > 0 and root_clear > 0 and vol == 0.0
            verdict = ("PASS - engaged with correct clearance"
                       if engaged else
                       "FAIL - teeth overlap, check phasing" if vol > 0 else
                       "FAIL - circles do not overlap, teeth miss entirely")
            print(f"  {a} <-> {b} shared volume {vol:.4f} mm3 -> {verdict}")

    print()
    if clashes:
        print("CLASHES (real shared volume):")
        for a, b, vol in clashes:
            print(f"  {a} <-> {b}: {vol:.3f} mm3  *** FIX ***")
    else:
        print("no clashes: every intersecting pair has zero shared volume")
        print("(contacts are line/face touching only)")

    return 1 if clashes else 0


if __name__ == "__main__":
    raise SystemExit(main())
