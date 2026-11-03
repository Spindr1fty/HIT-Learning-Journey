r"""Four semi-enclosed options on the 3 mm rack bracket.

The user's Desktop assembly g_mount_b.SLDASM references
Desktop/print/g_mount_b_rack_3mm.SLDPRT, i.e. the 3 mm wall version, not the
4 mm rev55.  Apply the same mutations as g_mount_b_3mm_rack.py BEFORE importing
g_mount_b_half, so its module-level constants are computed for 3 mm.

Exports STEP only.

Pure ASCII on purpose.
"""

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

import g_mount_b_half as H  # noqa: E402  (must come after the mutations)

H.BLOCK_T = T
OUT = Path(__file__).resolve().parent.parent / "newSTEP"


if __name__ == "__main__":
    parts = [
        ("g_mount_b_half3_A", H.option_a()),
        ("g_mount_b_half3_B", H.option_b()),
        ("g_mount_b_half3_B_exploded", H.option_b_exploded()),
        ("g_mount_b_half3_C", H.option_b(H.WIN_C)),
        ("g_mount_b_half3_D", H.option_d()),
    ]
    for name, p in parts:
        b = p.bounding_box()
        print(f"{name}: X {b.min.X:.2f}..{b.max.X:.2f}"
              f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
              f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}"
              f"  valid={p.is_valid}  solids={len(p.solids())}"
              f"  vol {p.volume / 1000:.3f} cm3")
        out = OUT / f"{name}.step"
        print("  step:", bd.export_step(p, str(out)), out)
