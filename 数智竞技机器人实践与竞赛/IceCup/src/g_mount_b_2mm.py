r"""Thin 2 mm variant of g_mount_b (rev 39) -- quick print / fit check only.

Everything that touches the servo, the tooth plate or the 4 flange screws keeps
its real size; the enclosure walls and the top plate are thinned to 2 mm so it
prints fast.

    python g_mount_b_2mm.py
writes
    ..\newSTEP\g_mount_b_2mm.step
    C:\Users\Spindrift\Desktop\g_mount_b_2mm.step
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b as M  # noqa: E402

# --- thin EVERYTHING to 2 mm (the foot too).  The foot's bottom moves up to
# Z 12 so the servo's support face stays at Z 14 -- the part then sits 3 mm
# higher than the real one on the tooth plate, which is fine for a fit check.
M.PLATE_T = 12.0
M.FOOT_T = 2.0
M.WALL_T = 2.0
M.IN_Y0 = M.BOX_Y0 + M.WALL_T          # 14.94
M.IN_Y1 = M.BOX_Y1 - M.WALL_T          # 85.44
M.BOX_Z1 = M.IN_Z1 + 2.0               # 36.60 (top plate 2 mm)
M.POST_X = (M.FLANGE_X0 - 2.0, M.FLANGE_X0)   # posts 2 mm thick

OUT_WORK = Path(__file__).resolve().parent.parent / "newSTEP" / "g_mount_b_2mm.step"
OUT_DESK = Path.home() / "Desktop" / "g_mount_b_2mm.step"

if __name__ == "__main__":
    part = M.bracket()
    b = part.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"valid={part.is_valid}  solids={len(part.solids())}"
          f"  vol {part.volume / 1000:.2f} cm3 ({part.volume / 1000 * 1.24:.0f} g PLA)")
    bd.export_step(part, str(OUT_WORK))
    shutil.copy2(OUT_WORK, OUT_DESK)
    print("wrote", OUT_WORK)
    print("copied to", OUT_DESK)
