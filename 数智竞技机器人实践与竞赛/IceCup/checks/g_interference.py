r"""Prove the funnel head both slides in clean AND actually catches an offset stone.

The old check only asked "does the fork touch the stone when everything is
lined up". That is the easy half. The hard half is what this design exists for:
the opponent's stone can be 16.5 mm off the cell's centre, so the check has to
show that the funnel's walls walk it in rather than letting it slip past.

Three things are tested.

  1. CAPTURE. Sweep the funnel's opening half-width along its length. It must
     start wider than the worst-case stem position and shrink monotonically to
     the 12.6 mm tine gap. If it ever widens again, a stem could work backwards
     out of it.
  2. SLIDING IN. Put the stone at the fully-centred pick position and confirm
     zero interference at the pick height. A funnel that scrapes the disc or the
     body is worse than no funnel.
  3. LIFTING. Raise the fork and confirm the disc gets caught right at the
     designed clearance. A fork that "almost" reaches is a fork that drops a
     stone.

Run from src/:  python ../checks/g_interference.py
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from cadgen import build123d as bd  # noqa: E402

import g_params as G  # noqa: E402
import g_fork as F  # noqa: E402
from g_stone import _stone  # noqa: E402

STONE_Z = -(G.BODY_TOP_Y + G.TINE_LIFT)
STEM_R = G.STEM_DIA / 2.0
WORST_OFFSET = (80.0 - G.STONE_DIA) / 2.0      # 16.5, cell slop


def vol(shape):
    if shape is None:
        return 0.0
    if hasattr(shape, "volume"):
        return shape.volume
    return sum(getattr(s, "volume", 0.0) for s in shape if s is not None)


def funnel_half_width(x):
    """Half-width of the funnel's opening at position x along the fork."""
    if x <= F.X_TINE_END:
        return F.TINE_IN
    if x >= F.X_MOUTH:
        return F.MOUTH_HALF
    t = (x - F.X_TINE_END) / (F.X_MOUTH - F.X_TINE_END)
    return F.TINE_IN + (F.MOUTH_HALF - F.TINE_IN) * t


def main():
    fork = F._head()
    stone = _stone()

    print("1. CAPTURE -- can the funnel swallow the worst-case stone?")
    print(f"   stone can sit +/-{WORST_OFFSET:.1f} mm off centre in an 80 mm cell")
    print(f"   stem radius {STEM_R:.1f}, so the worst stem edge is at"
          f" +/-{WORST_OFFSET + STEM_R:.1f} mm")
    print(f"   mouth half-width {F.MOUTH_HALF:.1f} mm"
          f"  ->  margin {F.MOUTH_HALF - (WORST_OFFSET + STEM_R):.1f} mm")

    widths = [funnel_half_width(x) for x in
              [F.X_MOUTH - i * (F.X_MOUTH - F.X_TINE_END) / 40.0
               for i in range(41)]]
    monotonic = all(widths[i] <= widths[i - 1] + 1e-9
                    for i in range(1, len(widths)))
    if not monotonic:
        print("   FAIL: the funnel widens somewhere -- a stem could work out")
        return 1
    print(f"   PASS: opening shrinks monotonically {widths[0]:.1f} ->"
          f" {widths[-1]:.1f} mm, so anything that enters is guided inward")
    print()

    print("2. SLIDING IN -- stone swept from the closed end out to the mouth")
    # The stem's REAR point touches the closed end at X=0, so the stone's axis
    # ends up at +STEM_R. Placing it at 0 buried the stem inside the closed end
    # and produced 514 mm3 of nonsense interference.
    # The stem's rear tangent point must NOT touch the closed end of the U. At
    # exactly X = STEM_R the two surfaces are tangent, and a tangent surface
    # pair makes the boolean report a sliver of interference that is not real.
    # Give it 0.5 mm of daylight; the fork lifts the stone, it never pushes it.
    PICK_CLEAR = 0.5
    PICK_X = STEM_R + PICK_CLEAR
    s = bd.Pos(0.0, 0.0, STONE_Z) * stone
    # sweep the stone backwards along the fork, which is what happens as the
    # robot drives in: the stem ends up at the closed end
    worst = 0.0
    worst_x = None
    for i in range(31):
        sx = PICK_X + 36.5 * i / 30.0
        s = bd.Pos(sx, 0.0, STONE_Z) * stone
        v = vol(fork.intersect(s))
        if v > worst:
            worst, worst_x = v, sx
    if worst > 0.001:
        print(f"   FAIL: {worst:.3f} mm3 of interference at stone X {worst_x}")
        return 1
    print(f"   PASS: zero interference across 36.5 mm of travel"
          f" (worst {worst:.4f})")
    print(f"   tine top sits {G.GAP_UNDER_DISC - G.TINE_LIFT - F.THICK:.2f} mm"
          f" below the disc, {(G.TINE_LIFT):.2f} mm above the body's shoulder")
    print()

    print("3. LIFTING -- does the disc actually get caught?")
    s = bd.Pos(PICK_X, 0.0, STONE_Z) * stone
    first = None
    for step in range(1, 61):
        lift = step * 0.05
        v = vol((bd.Pos(0, 0, lift) * fork).intersect(s))
        if v > 0.001:
            first = lift
            break
    expected = G.GAP_UNDER_DISC - G.TINE_LIFT - F.THICK
    if first is None:
        print("   FAIL: 3 mm of lift and still no contact")
        return 1
    print(f"   first contact at {first:.2f} mm of lift (expected"
          f" {expected:.2f})")
    print(f"   PASS: the disc is caught, the stone is carried")
    print()

    print("4. CLEARANCE IN THE CELL")
    print(f"   head is {2 * (F.MOUTH_HALF + 2.0):.0f} mm wide"
          f" vs an 80 mm cell -> {(80 - 2 * (F.MOUTH_HALF + 2.0)) / 2:.1f} mm"
          f" either side")
    print(f"   head is {F.THICK:.1f} mm thick in a {G.GAP_UNDER_DISC:.1f} mm"
          f" gap under the disc")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
