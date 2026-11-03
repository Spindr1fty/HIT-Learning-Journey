r"""Proposal: the same fork head with a much shorter working end.

Why: the cell is 58 deep (60 minus the 2 mm acrylic back panel) and the stone
(47 dia) can sit anywhere in it, so its handle stem is 23.5..35 from the cell's
mouth. The current head is 54 long from the closed end to the tip, so the tip
reaches the back panel 54 mm after passing the stem -- long before the stem can
reach the closed end. Symptoms: the tip hits the panel first, and the stone
rides near the mouth of the slot (shallow, easy to drop).

Head budget: tip depth = stem depth + head length <= 58  ->  head <= 23.5.
This proposal uses 21.

Nothing else changes: same plate, same 2 x M4 mounting block at X -12..-4
(Y +-12, Z 13), so the bracket bolts on exactly as before -- and the pick point
(the closed end, X=0) stays 12 mm in front of the bracket face, i.e. the same
place relative to the machine as today.

    python g_fork_proposal.py  ->  newSTEP/g_fork_proposal.step
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import g_fork as F  # noqa: E402

# shorten the working end: throat at X 5, funnel reaches the plate's full width
# at X 21 (50.9 deg walls), and the thin leading wedge takes 10 mm (16.7 deg)
F.X_TINE_END = 5.0
F.MOUTH_HALF = F.PLATE_HALF
F.X_MOUTH = 21.0
F.RAMP_ANGLE = 16.7

from cadgen import build123d as bd  # noqa: E402

if __name__ == "__main__":
    head = F._head()
    b = head.bounding_box()
    print(f"proposal head bbox X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"  valid {head.is_valid}  solids {len(head.solids())}"
          f"  volume {head.volume / 1000:.3f} cm3")
    print(f"  working end (closed end -> tip): {b.max.X:.2f}"
          f"   max tip depth in the cell = 35 + {b.max.X:.2f} = {35 + b.max.X:.2f}")
    bd.export_step(head, r"..\newSTEP\g_fork_proposal.step")
    print("wrote ../newSTEP/g_fork_proposal.step")
