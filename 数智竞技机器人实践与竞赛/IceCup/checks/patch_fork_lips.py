r"""One-shot patch: add option C (mouth lip flare) to g_fork.py.

Doing this from PowerShell kept tripping over here-string quoting, so it is a
Python script instead. It is idempotent: if LIP_FLARE is already there it does
nothing.
"""

import io
import re
import sys
from pathlib import Path

SRC = Path(r"D:\IceCup\src\g_fork.py")

CONST = """
# C: flare the two lips where the taper meets the mouth. Without this the mouth
# edge is a pair of sharp points the stone's disc can catch on. Cutting them
# back at 45 degrees makes the opening bell out, so the disc rides in.
LIP_FLARE = 4.0
"""

BLOCK = """    # --- flare the mouth lips (option C) -----------------------------------
    # A 45 degree cut at each lip, widening the void as it goes forward. The
    # throat keeps its 44 mm and gains a bell in front of it.
    for sy in (-1.0, 1.0):
        y_in = sy * MOUTH_HALF
        wedge = [(X_MOUTH - LIP_FLARE, y_in),
                 (X_MOUTH + 1.0, y_in),
                 (X_MOUTH + 1.0, y_in + sy * LIP_FLARE)]
        face = bd.Face(bd.Polyline(*[(x, y, 0.0) for x, y in wedge],
                                   close=True))
        head = head.cut(bd.extrude(face, amount=THICK + 4.0, both=True)).clean()

"""


def main():
    text = SRC.read_text(encoding="utf-8")
    if "LIP_FLARE" in text:
        print("already patched, nothing to do")
        return 0

    if "TIP_BEVEL = 2.0" not in text:
        print("FAIL: could not find the TIP_BEVEL line")
        return 1
    text = text.replace("TIP_BEVEL = 2.0", CONST.strip() + "\nTIP_BEVEL = 2.0", 1)

    anchor = "    # --- thin the leading edge (option B) ----------------------------------"
    if anchor not in text:
        print("FAIL: could not find the option-B anchor")
        return 1
    text = text.replace(anchor, BLOCK + anchor, 1)

    SRC.write_text(text, encoding="utf-8")
    print("patched g_fork.py with the lip flare")
    return 0


if __name__ == "__main__":
    sys.exit(main())
