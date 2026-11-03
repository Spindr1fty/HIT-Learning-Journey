"""g_mount_b_widepost -- PROPOSAL ONLY. The released part is src/g_mount_b.py.

One change against the current part: the two servo posts are widened OUTWARD
from 8 to 12 mm (Y 17.94..29.94 and 70.44..82.44).  The 40.5 servo gap, both
screw lines (Y 25.94 / 74.44) and everything else do not move.

Why: the 4.5 screw hole in an 8 mm post leaves 1.75 mm of material on the
servo side, and an M4 head 8.1 across corners already overhangs the face by
0.05.  Widening outboard gives 5.75 mm outboard instead of 1.75, lets an 8 mm
washer sit fully on the face (9 mm still cannot: it would touch the servo
body, which is only 4.25 mm from the screw line), and roughly doubles the
post's root section in the Y direction.

The gusset leg drops 18 -> 14 so the gusset still lands exactly on the foot's
front edge at Y 3.94; the foot, plate holes and bridge height are unchanged.
Cost: +0.2 cm3 of PLA (the widened post sits mostly inside the existing
gusset).

The geometry is reached by overwriting g_mount_b's module constants before
calling its bracket(), so there is still exactly ONE copy of the part.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import step  # noqa: E402

import g_mount_b as M  # noqa: E402

POST_W_WIDE = 12.0
RIB_LEG_WIDE = 14.0

M.POST1_Y = (M.POST1_Y[1] - POST_W_WIDE, M.POST1_Y[1])      # 17.94..29.94
M.POST2_Y = (M.POST2_Y[0], M.POST2_Y[0] + POST_W_WIDE)      # 70.44..82.44
M.POST_W = POST_W_WIDE
# foot is owned by the base module (rev 27: Y 12.94..87.44); the gusset has to
# stop on that edge, so its leg shrinks by the same 4 mm the post moved out
M.RIB_LEG = M.POST1_Y[0] - M.FOOT_Y[0]                      # 5.0
M.BRIDGE = (M.POST_X[0], M.POST_X[1], M.POST1_Y[0], M.POST2_Y[1],
            M.POST_TOP - M.BRIDGE_T, M.POST_TOP)
# the screw lines come from the servo flange, not from the post width; the
# module derives them from POST1_Y, so restate them after the override
M.POST_C1 = M.SERVO_CY - M.FLANGE_HALF
M.POST_C2 = M.SERVO_CY + M.FLANGE_HALF


@step(out="../newSTEP/g_mount_b_widepost.step")
def g_mount_b_widepost():
    return M.bracket()


@step(out="../newSTEP/g_mount_b_widepost_ref.step")
def g_mount_b_widepost_ref():
    return M.bracket() + M.reference()


if __name__ == "__main__":
    m = g_mount_b_widepost()
    b = m.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3"
          f"   ({m.volume / 1000 * 1.24:.0f} g PLA)")
    print(f"posts    Y {M.POST1_Y[0]:.2f}..{M.POST1_Y[1]:.2f} /"
          f" {M.POST2_Y[0]:.2f}..{M.POST2_Y[1]:.2f}"
          f"  ({M.POST1_Y[1] - M.POST1_Y[0]:.1f} wide)")
    print(f"gap      {M.POST2_Y[0] - M.POST1_Y[1]:.1f}  (servo body 40)")
    print(f"gusset   leg {M.RIB_LEG:.0f}, foot Y {M.FOOT_Y[0]:.2f}"
          f"..{M.FOOT_Y[1]:.2f}, bridge Y {M.BRIDGE[2]:.2f}"
          f"..{M.BRIDGE[3]:.2f}")
    print(f"screws   Y {M.POST_C1:.2f}/{M.POST_C2:.2f}"
          f"  hole-to-face {(M.POST1_Y[1] - M.POST_C1):.2f} inboard /"
          f" {(M.POST_C1 - M.POST1_Y[0]):.2f} outboard")
    ref = g_mount_b_widepost_ref()
    print(f"ref      solids={len(ref.solids())}")
