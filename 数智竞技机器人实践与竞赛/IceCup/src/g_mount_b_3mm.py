r"""3 mm thin variant of g_mount_b (all walls 3 mm) -- replaces the 2 mm test.

Interface dimensions (servo envelope, flange contact face, 8 chassis holes,
4 flange through-holes, bolt-head clearance) are untouched; every wall/foot is
3 mm so it prints fast and can be tried on the real servo.

    python g_mount_b_3mm.py
writes
    ..\newSTEP\g_mount_b_3mm.step
    C:\Users\Spindrift\Desktop\g_mount_b_3mm.step
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b as M  # noqa: E402

T = 3.0
M.WALL_T = T
M.BOX_Y0 = M.IN_Y0 - T            # 13.64: outer face follows the wall thickness
M.BOX_Y1 = M.IN_Y1 + T            # 87.14
M.FOOT_Y = (M.BOX_Y0, M.BOX_Y1)
M.BOX_Z1 = M.IN_Z1 + T            # 37.60: top plate 3 mm
M.POST_X = (M.FLANGE_X0 - T, M.FLANGE_X0)   # 1.84 .. 4.84
M.PLATE_T = 11.0                  # foot 3 mm: Z 11..14, servo datum stays 14
M.FOOT_T = T

OUT_WORK = Path(__file__).resolve().parent.parent / "newSTEP" / "g_mount_b_3mm.step"
OUT_DESK = Path.home() / "Desktop" / "g_mount_b_3mm.step"

if __name__ == "__main__":
    part = M.bracket()
    b = part.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"valid={part.is_valid}  solids={len(part.solids())}"
          f"  vol {part.volume / 1000:.2f} cm3 ({part.volume / 1000 * 1.24:.0f} g)")
    bd.export_step(part, str(OUT_WORK))
    shutil.copy2(OUT_WORK, OUT_DESK)
    print("wrote", OUT_WORK)
    print("copied to", OUT_DESK)
