r"""Sharpen the two mouth lips to points.

The mouth's edge currently ends in a short flat at each lip. The user wants each
lip to come to a point, so the disc can ride onto it instead of catching the
corner.

In plan the plate's edge is at Y +/-26 and the mouth's throat is at +/-22, so
each lip is a 4 mm strip. A diagonal cut from the plate's edge back to the throat
turns that strip's front into a point at (X_MOUTH, +/-22).

This is a PLAN cut only. Option B's thickness bevel on the leading edge stays.
"""

import re
import sys
from pathlib import Path

SRC = Path(r"D:\IceCup\src\g_fork.py")

CONST = """
# Point the two mouth lips. The plate's edge is at Y +/-26 and the throat at
# +/-22, so each lip is a 4 mm strip. Cutting a diagonal back from that strip's
# front leaves a point at (X_MOUTH, +/-22) for the disc to ride onto.
LIP_POINT_LEN = 8.0
"""

BLOCK = '''    # --- point the two mouth lips -----------------------------------------
    for sy in (-1.0, 1.0):
        y_throat = sy * MOUTH_HALF          # 22
        y_edge = sy * (MOUTH_HALF + 2.0)    # 26, the plate's edge
        wedge = [(X_MOUTH, y_throat),
                 (X_MOUTH, y_edge),
                 (X_MOUTH - LIP_POINT_LEN, y_edge)]
        face = bd.Face(bd.Polyline(*[(x, y, 0.0) for x, y in wedge],
                                   close=True))
        head = head.cut(bd.extrude(face, amount=THICK + 4.0, both=True)).clean()

'''


def main():
    text = SRC.read_text(encoding="utf-8")
    if "LIP_POINT_LEN" in text:
        print("already pointed, nothing to do")
        return 0

    anchor = "    # --- thin the leading edge (option B) ----------------------------------"
    if anchor not in text:
        print("FAIL: option-B anchor not found")
        return 1
    text = text.replace(anchor, BLOCK + anchor, 1)

    # constants go just above TIP_BEVEL
    if "TIP_BEVEL = 2.0" not in text:
        print("FAIL: TIP_BEVEL not found")
        return 1
    text = text.replace("TIP_BEVEL = 2.0",
                        CONST.strip() + "\nTIP_BEVEL = 2.0", 1)

    SRC.write_text(text, encoding="utf-8")
    print("pointed the two mouth lips")
    return 0


if __name__ == "__main__":
    sys.exit(main())
