r"""Remove option C (the mouth lip flare), keep option B (the thickness bevel).

The user liked B's slope and does not want the lips flared.
"""

import re
import sys
from pathlib import Path

SRC = Path(r"D:\IceCup\src\g_fork.py")


def main():
    text = SRC.read_text(encoding="utf-8")
    if "LIP_FLARE" not in text:
        print("C is already gone, nothing to do")
        return 0

    # drop the flaring loop
    text = re.sub(
        r"    # --- flare the mouth lips \(option C\).*?"
        r"head = head\.cut\(bd\.extrude\(face, amount=THICK \+ 4\.0, both=True\)\)"
        r"\.clean\(\)\n\n",
        "", text, flags=re.S)

    # drop the constants
    text = re.sub(r"# C: flare the two lips.*?\nLIP_FLARE = 4\.0\n", "", text,
                  flags=re.S)

    if "LIP_FLARE" in text:
        print("FAIL: something called LIP_FLARE survived")
        return 1

    SRC.write_text(text, encoding="utf-8")
    print("removed option C; option B left in place")
    return 0


if __name__ == "__main__":
    sys.exit(main())
