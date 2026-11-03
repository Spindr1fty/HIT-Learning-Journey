r"""3 mm thin version of the rack bracket -- for a quick fit test.

    python g_mount_b_3mm_rack.py
writes newSTEP\g_mount_b_rack_3mm.step / .stl and copies them to the Desktop
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b as M  # noqa: E402

T = 3.0
M.WALL_T = T
M.IN_Y0 = M.BOX_Y0 + T
M.IN_Y1 = M.BOX_Y1 - T
M.BOX_Z1 = M.IN_Z1 + T
M.POST_X = (M.FLANGE_X0 - T, M.FLANGE_X0)
M.PLATE_T = 11.0
M.FOOT_T = T
M.LEG_T = T

OUT = Path(__file__).resolve().parent.parent / "newSTEP"

if __name__ == "__main__":
    p = M.bracket()
    print("valid", p.is_valid, "solids", len(p.solids()),
          "vol %.2f cm3 (%.0f g)" % (p.volume / 1000, p.volume / 1000 * 1.24))
    bd.export_step(p, str(OUT / "g_mount_b_rack_3mm.step"))
    bd.export_stl(p, str(OUT / "g_mount_b_rack_3mm.stl"))
    for ext in ("step", "stl"):
        shutil.copy2(OUT / ("g_mount_b_rack_3mm." + ext),
                     Path.home() / "Desktop" / ("g_mount_b_rack_3mm." + ext))
    print("exported + copied to Desktop")
