r"""Make the funnel's flanks run out to the plate's outer edge and come to a point
where they intersect it.

The user's description: the outer edge of the plate stays a straight line, and
the funnel's slanted flank is EXTENDED until it meets that edge. The meeting
point is the sharp lip.

So the plate grows by (X_LIP - X_MOUTH), the void polygon gains two points at
Y = +/-PLATE_HALF on the extended flank, and the old lip-trimming cut goes away.

X_LIP is not free: it is where the flank line crosses Y = PLATE_HALF.
    flank runs from (X_TINE_END, TINE_IN) to (X_MOUTH, MOUTH_HALF)
    the plate's edge is at PLATE_HALF = MOUTH_HALF + 4
    so  X_LIP = X_TINE_END + (PLATE_HALF - TINE_IN) / (MOUTH_HALF - TINE_IN)
                           * (X_MOUTH - X_TINE_END)
"""

import re
import sys
from pathlib import Path

SRC = Path(r"D:\IceCup\src\g_fork.py")

CONST = """
# The funnel's flank is extended past the throat until it crosses the plate's
# outer edge; that crossing is the sharp lip. The outer edge itself stays a
# straight line, exactly as drawn.
X_LIP = 0.0            # filled in by _head() from the flank geometry
"""

BLOCK = '''    # --- extend the flanks out to the plate's edge ------------------------
    # X_LIP is where the flank line crosses Y = PLATE_HALF. The lip is a point,
    # the plate's outer edge stays straight, and the funnel throat is unchanged.
    globals()["X_LIP"] = X_TINE_END + (PLATE_HALF - TINE_IN) / (MOUTH_HALF - TINE_IN) * (X_MOUTH - X_TINE_END)
    x_lip = globals()["X_LIP"]
    plate = _box(PLATE_X[0], x_lip, -PLATE_HALF, PLATE_HALF, 0.0, THICK)

'''


def main():
    text = SRC.read_text(encoding="utf-8")
    if "X_LIP" in text:
        print("already extended, nothing to do")
        return 0

    # 1) plate must reach the lip point, and in Y as well
    old_plate = ("    plate = _box(PLATE_X[0], X_MOUTH, -MOUTH_HALF - 2.0, "
                 "MOUTH_HALF + 2.0,\n                 0.0, THICK)")
    if old_plate not in text:
        print("FAIL: could not find the plate line")
        return 1
    text = text.replace(old_plate, BLOCK.rstrip("\n"), 1)

    # 2) void polygon: replace the two throat points with the two lip points
    old_void = """    void = [
        (X_MOUTH, -MOUTH_HALF),
        (X_TINE_END, -TINE_IN),
        (X_CLOSED, -TINE_IN),
        (X_CLOSED, TINE_IN),
        (X_TINE_END, TINE_IN),
        (X_MOUTH, MOUTH_HALF),
        (X_MOUTH + 12.0, MOUTH_HALF),
        (X_MOUTH + 12.0, -MOUTH_HALF),
    ]"""
    new_void = """    void = [
        (x_lip + 2.0, -PLATE_HALF),
        (x_lip, -PLATE_HALF),
        (X_TINE_END, -TINE_IN),
        (X_CLOSED, -TINE_IN),
        (X_CLOSED, TINE_IN),
        (X_TINE_END, TINE_IN),
        (x_lip, PLATE_HALF),
        (x_lip + 2.0, PLATE_HALF),
    ]"""
    if old_void not in text:
        print("FAIL: could not find the void polygon")
        return 1
    text = text.replace(old_void, new_void, 1)

    # 3) the lip-trimming cut is no longer wanted
    text = re.sub(
        r"    # --- point the two mouth lips.*?"
        r"head = head\.cut\(bd\.extrude\(face, amount=THICK \+ 4\.0, both=True\)\)"
        r"\.clean\(\)\n\n", "", text, flags=re.S)
    text = re.sub(r"# Point the two mouth lips\.\n.*?\nLIP_POINT_LEN = 8\.0\n",
                  "", text, flags=re.S)

    # 4) constants
    text = text.replace("TIP_BEVEL = 2.0", CONST.strip() + "\nTIP_BEVEL = 2.0", 1)

    SRC.write_text(text, encoding="utf-8")
    print("extended the flanks to the plate edge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
