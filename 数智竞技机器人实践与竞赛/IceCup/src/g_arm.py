"""Swing arm for the launcher, mounted on the servo horn.

Placeholder dimensions -- the user has not fixed the arm's length or sweep yet,
so these are chosen to be plausible and easy to change:

  pivot disc   dia 20 x 5, matching the horn (Ø20 x 2.5) and its 4 x M3 on BCD 14
  bar          12 wide x 45 long from the pivot axis, 5 thick
  pose         pointing +Z at mid-travel

The arm's frame: the horn's axis along X, the horn's face at X = 0, arm body
extending to -X (outboard). Its own local origin is the pivot centre.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_servo as S  # noqa: E402

ARM_T = 5.0                 # along the shaft
PIVOT_D = 20.0              # matches the horn
BAR_W = 12.0
BAR_L = 45.0                # from the pivot axis to the tip
SCREW_D = 3.2               # M3 clearance
HUB_LIP = 2.5               # the arm's hub sits down over the horn
TIP_FILLET = 3.0


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def arm():
    # pivot disc
    hub = _box(-ARM_T, 0.0, -PIVOT_D / 2, PIVOT_D / 2, -PIVOT_D / 2,
               PIVOT_D / 2)
    # bar pointing +Z
    bar = _box(-ARM_T, 0.0, -BAR_W / 2, BAR_W / 2, 0.0, BAR_L)
    part = (hub + bar).clean()

    # round the tip
    tip_edges = [e for e in part.edges()
                 if abs(e.center().Z - BAR_L) < 1e-6 and abs(e.center().X) < 1e-6]
    if tip_edges:
        try:
            part = part.fillet(TIP_FILLET, tip_edges)
        except Exception as exc:
            print("tip fillet skipped:", exc)

    # 4 x M3 on BCD 14, through the hub
    # 4 x M3 clearance, drilled ALONG X through the hub (holes must be parallel
    # to the shaft, not across it)
    import math
    for k in range(4):
        a = math.radians(45 + 90 * k)
        cy = S.BCD / 2.0 * math.cos(a)
        cz = S.BCD / 2.0 * math.sin(a)
        part = part.cut(bd.Pos(-ARM_T - 1.0, cy, cz) * bd.Rot(0, 90, 0)
                        * bd.Cylinder(SCREW_D / 2.0, ARM_T + 2.0,
                                      align=(bd.Align.CENTER, bd.Align.CENTER,
                                             bd.Align.MIN)))
    return part.clean()


@step(out="../newSTEP/g_arm.step")
def g_arm():
    return arm()


if __name__ == "__main__":
    m = g_arm()
    b = m.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3"
          f"   ({m.volume / 1000 * 1.24:.0f} g PLA)")
    print()
    print(f"pivot disc dia {PIVOT_D} x {ARM_T}")
    print(f"bar {BAR_W} wide x {BAR_L} long, {ARM_T} thick")
    print(f"4 x dia {SCREW_D} on BCD {S.BCD} from the horn")
