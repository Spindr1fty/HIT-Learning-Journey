r"""Variant of g_fork with the tip ramp at 13 deg instead of 8.1 deg.

    python g_fork_13deg.py   ->  newSTEP/g_fork_13deg.step

Same part, only the ramp angle changes: the ramp gets shorter (21.1 -> 13.0 mm)
so the FDM stair steps on it drop from 1.40 to 0.86 mm at 0.2 mm layers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import g_fork as F  # noqa: E402

F.RAMP_ANGLE = 13.0

from cadgen import build123d as bd  # noqa: E402


if __name__ == "__main__":
    part = F._head()
    b = part.bounding_box()
    print(f"g_fork_13deg  bbox {b.max.X - b.min.X:.2f} x {b.max.Y - b.min.Y:.2f}"
          f" x {b.max.Z - b.min.Z:.2f}  valid={part.is_valid}"
          f"  volume {part.volume / 1000:.3f} cm3")
    bd.export_step(part, r"..\newSTEP\g_fork_13deg.step")
    print("wrote ../newSTEP/g_fork_13deg.step")
