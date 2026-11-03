"""Independent analytic check of every generated part.

Recomputes each volume from parts_data with elementary geometry (shoelace
outline minus hole and slot areas) and compares against what the CAD kernel
produced. A mismatch means the model does not say what the data says.

Run under cadgen's environment:
  uvx --no-config --python 3.13 --from "cadgen==0.7.21" python checks/verify_parts.py
"""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cadgen import build123d as bd  # noqa: E402

import parts_data as P  # noqa: E402

TOL_MM3 = 1e-4


def _shoelace(pts):
    n = len(pts)
    return abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
                   for i in range(n))) / 2


def _removed_area(holes, slots):
    a = sum(math.pi * r * r for _, _, r in holes)
    for x0, y0, x1, y1, w in slots:
        a += abs(x1 - x0) * w + math.pi * (w / 2) ** 2
    return a


def _report(name, solid, want, extra=""):
    delta = abs(solid.volume - want)
    ok = delta < TOL_MM3 and solid.is_valid
    box = solid.bounding_box()
    cyl = sum(1 for f in solid.faces() if f.geom_type == bd.GeomType.CYLINDER)
    print(f"{name:13s} {'OK  ' if ok else 'FAIL'}  "
          f"{box.max.X-box.min.X:8.3f} x {box.max.Y-box.min.Y:7.3f} x "
          f"{box.max.Z-box.min.Z:5.3f}  cyl={cyl:2}  "
          f"vol {solid.volume/1000:8.4f} vs {want/1000:8.4f} cm3  "
          f"delta {delta:8.5f} mm3 {extra}")
    return 0 if ok else 1


def main():
    from eight_circle import eight_circle
    from move_item import move_item
    from short_item import short_item
    from six_circle import six_circle

    fails = 0
    for name, fn, data in [
        ("six_circle", six_circle, P.SIX_CIRCLE),
        ("eight_circle", eight_circle, P.EIGHT_CIRCLE),
        ("move_item", move_item, P.MOVE_ITEM),
        ("short_item", short_item, P.SHORT_ITEM),
    ]:
        want = ((_shoelace(data["outline"]) - _removed_area(data["holes"], data["slots"]))
                * P.THICKNESS)
        expect_cyl = len(data["holes"]) + 2 * len(data["slots"])
        solid = fn()
        fails += _report(name, solid, want,
                         f"(expect {len(data['holes'])}h+{len(data['slots'])}s)")
        got = sum(1 for f in solid.faces() if f.geom_type == bd.GeomType.CYLINDER)
        if got != expect_cyl:
            print(f"              !! cylinder faces {got} != expected {expect_cyl}")
            fails += 1

    from wheel import BORE_DIAMETER, RIM_DIAMETER, WIDTH, wheel
    want = math.pi * ((RIM_DIAMETER / 2) ** 2 - (BORE_DIAMETER / 2) ** 2) * WIDTH
    fails += _report("wheel", wheel(), want)

    import l_shape as L
    br = L.l_shape()
    # Each leg keeps a 2x3 grid (the bend-adjacent row is gone), and the two
    # legs of LEG x LEG x T intersect in a LEG x T x T corner slab that
    # carries no hole (nearest remaining row is 17.25 from the outer edge,
    # T is 5). The 45 deg gusset adds half a GUSSET-square over the width.
    leg = (L.LEG ** 2 - 6 * math.pi * (L.HOLE_DIAMETER / 2) ** 2) * P.THICKNESS
    want = (2 * leg - L.LEG * P.THICKNESS ** 2
            + 0.5 * L.GUSSET ** 2 * L.LEG)
    fails += _report("l_shape", br, want, f"solids={len(br.solids())}")

    import servo_clip as S
    br = S.servo_clip()
    wx0, wy0, wx1, wy1 = S.WINDOW
    want = ((_shoelace(S.OUTLINE) - (wx1 - wx0) * (wy1 - wy0)
             - len(S.holes()) * math.pi * (S.HOLE_DIAMETER / 2) ** 2)
            * S.THICKNESS)
    fails += _report("servo_clip", br, want, "(1 window)")
    got = sum(1 for f in br.faces() if f.geom_type == bd.GeomType.CYLINDER)
    if got != len(S.holes()):
        print(f"              !! cylinder faces {got} != expected {len(S.holes())}")
        fails += 1

    print(f"\nFAILURES: {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
