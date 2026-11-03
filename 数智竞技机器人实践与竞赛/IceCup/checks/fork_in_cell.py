r"""Does the fork head actually fit inside a cell?

Cell, measured on the rack: 80 wide x 80 high x 60 deep, with a 2 mm acrylic
back panel, so only 58 mm of depth is usable.

The head has to enter the cell from the front, slide its two arms under the
stone's disc, and stop with the stem against the closed end. Three numbers
decide whether that is possible:

  width   the head must pass the 80 mm cell mouth beside the 47 mm stone
  height  the head must pass the 80 mm cell mouth
  reach   the tip has to get far enough in to reach the stem, wherever the
          stone happens to sit in its 11 mm of fore-and-aft play

The head being LONGER than the cell is not a failure: the back of the head just
stays outside the cell, which is where the carriage is anyway.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import g_params as G  # noqa: E402
import g_fork as F  # noqa: E402

CELL_W = 80.0
CELL_H = 80.0
CELL_D = 60.0
BACK_PANEL = 2.0
USABLE_D = CELL_D - BACK_PANEL          # 58

HEAD_W = 2 * (F.MOUTH_HALF + 2.0)       # the plate is mouth + 2 either side
HEAD_L = F.X_MOUTH - F.PLATE_X[0]
HEAD_T = F.THICK

# where the stone's stem can sit, measured from the cell's front face:
# the stone is 47 across and cannot pass the back panel
# The STEM's depth depends on where the whole STONE sits, so it is the stone's
# 47 mm body that sets it, not the 18 mm handle disc. Using the disc here gave a
# nonsense 9..49 range.
STONE_DIA = 47.0
STEM_MIN = STONE_DIA / 2.0                        # 23.5, stone at the front
STEM_MAX = USABLE_D - STONE_DIA / 2.0             # 34.5, stone at the back
TIP_REACH = F.X_MOUTH - F.PLATE_X[1]              # tip ahead of the back plate


def main():
    ok = True
    print(f"cell usable depth {USABLE_D:.0f} mm"
          f"   stone stem sits {STEM_MIN:.1f} .. {STEM_MAX:.1f} mm in")
    print()
    print(f"head  width {HEAD_W:.0f}   length {HEAD_L:.0f}   thick {HEAD_T:.1f}")
    print()

    # width: does the head pass the cell mouth beside the stone?
    clear_w = (CELL_W - HEAD_W) / 2.0
    good = clear_w > 0
    print(f"width   {HEAD_W:.0f} vs {CELL_W:.0f} cell   ->  {clear_w:.1f} mm"
          f" either side  {'OK' if good else 'TOO WIDE'}")
    ok = ok and good

    # height
    clear_h = (CELL_H - HEAD_T) / 2.0
    print(f"height  {HEAD_T:.1f} vs {CELL_H:.0f} cell  ->  {clear_h:.1f} mm"
          f" either side  {'OK' if clear_h > 0 else 'TOO TALL'}")
    ok = ok and clear_h > 0

    # reach: the arms start at the tip, so the head reaches STEM_MIN whatever
    # the stone's depth. What matters is that the tip gets past the stem.
    print()
    print(f"reach   tip is {TIP_REACH:.0f} mm ahead of the back plate")
    print(f"        the arms run from the tip back to X {F.X_TINE_END:.0f},")
    print(f"        so they cover the stem for {F.X_MOUTH - F.X_TINE_END:.0f}"
          f" mm of travel")
    arm_len = F.X_MOUTH - F.X_CLOSED
    print(f"        total arm length (mouth to closed end) {arm_len:.0f} mm")
    print(f"        stem can sit {STEM_MIN:.1f}..{STEM_MAX:.1f} mm in,"
          f" arm covers 0..{arm_len:.0f}  ->  {'OK' if arm_len >= STEM_MAX else 'SHORT'}")

    print()
    print(f"head length {HEAD_L:.0f} vs usable depth {USABLE_D:.0f}"
          f"  ->  the back of the head stays {HEAD_L - USABLE_D:.0f} mm"
          f" outside the cell at worst (that is normal)")
    print()
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
