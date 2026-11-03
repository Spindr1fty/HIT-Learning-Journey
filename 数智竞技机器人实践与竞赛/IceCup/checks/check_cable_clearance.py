r"""Check that the cable holes / zip-tie eyes do not touch any mounted part.

    python check_cable_clearance.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"D:\IceCup\src").resolve()))
import chassis as C  # noqa: E402

# mounted parts as axis-aligned plan rectangles (x0, y0, x1, y1)
PARTS = []
for g in C.wheel_groups():
    PARTS.append((f"轮板{g['name']}", *g["foot"]))
    xr = g["wheel_x"]
    PARTS.append((f"车轮{g['name']}", xr[0], g["wheel_y"] - C.WHEEL_D / 2,
                  xr[1], g["wheel_y"] + C.WHEEL_D / 2))
PARTS += [
    ("导轨脚", C.Z_X0 - 25, C.Z_Y0 - 25, C.Z_X0 + 25, C.Z_Y0 + 25),
    ("齿条脚", C.Z_X0 - 22, C.Z_Y0 - 106, C.Z_X0 + 22, C.Z_Y0 - 74),
    ("电池盒", *C.battery_outline()),
    ("发射机构底板", *C.BASE_PLATE_BOX),
]
# the notch is a void: (x0, y0, x1, y1) of the hole in the plate
NOTCH = (102.64, 203.07, 171.35, 260.0)


def rect_gap(x, y, r, rect):
    """Distance from a circle (x, y, r) to a rectangle; negative = overlap."""
    x0, y0, x1, y1 = rect
    dx = max(x0 - x, 0.0, x - x1)
    dy = max(y0 - y, 0.0, y - y1)
    d = (dx * dx + dy * dy) ** 0.5
    if d == 0.0:                       # centre inside the rectangle
        inside = min(x - x0, x1 - x, y - y0, y1 - y)
        return -r - inside
    return d - r


def rect_rect_gap(a, b):
    """Distance between two axis-aligned rectangles; negative = overlap."""
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    dx = max(bx0 - ax1, 0.0, ax0 - bx1)
    dy = max(by0 - ay1, 0.0, ay0 - by1)
    if dx == 0.0 and dy == 0.0:
        return -min(min(ax1, bx1) - max(ax0, bx0),
                    min(ay1, by1) - max(ay0, by0))
    return (dx * dx + dy * dy) ** 0.5


def square_gap(x, y, h, rect):
    """Distance from an axis-aligned square (centre x,y, half side h)."""
    return rect_rect_gap((x - h, y - h, x + h, y + h), rect)


def check_eyes():
    print("== 扎带眼（18×3 墙，窗 8×5）")
    bad = 0
    for cx, cy, along_y in C.EYE_POS:
        rect = C.eye_rect(cx, cy, along_y)
        worst = min((rect_rect_gap(rect, rest), pname)
                    for pname, *rest in PARTS)
        gap_notch = rect_rect_gap(rect, NOTCH)
        hole = min((rect_gap(x, y, C.HOLE_D / 2.0, rect),
                    f"孔({x:.1f},{y:.1f})") for x, y, _ in C.all_holes())
        sq = min((rect_rect_gap(rect, (hx - C.SQ / 2.0, hy - C.SQ / 2.0,
                                      hx + C.SQ / 2.0, hy + C.SQ / 2.0)),
                  f"方孔({hx:.0f},{hy:.0f})") for hx, hy in C.SQ_POS)
        note = ""
        for gap, who in ((worst[0], worst[1]), (hole[0], hole[1]),
                         (sq[0], sq[1]), (gap_notch, "缺口")):
            if gap < 0.5:
                note += f"  <-- 太近/干涉：{who} {gap:.2f}"
                bad += 1
        print(f"  ({cx:6.1f},{cy:6.1f}) 墙 X {rect[0]:6.2f}..{rect[2]:6.2f}"
              f"  Y {rect[1]:6.2f}..{rect[3]:6.2f}"
              f"  件 {worst[0]:6.2f} ({worst[1]})"
              f"  孔 {hole[0]:6.2f}  方孔 {sq[0]:6.2f}"
              f"  缺口 {gap_notch:7.2f}{note}")
    print(f"  problems: {bad}\n")
    return bad


def check(items, label, square=False):
    print(f"== {label}")
    bad = 0
    for name, x, y, r in items:
        gapf = (lambda rect: square_gap(x, y, r, rect)) if square \
            else (lambda rect: rect_gap(x, y, r, rect))
        worst = min((gapf(rest), pname) for pname, *rest in PARTS)
        gap_notch = gapf(NOTCH)
        note = ""
        if worst[0] < 0.5:
            note = f"  <-- 太近/干涉：{worst[1]} {worst[0]:.2f}"
            bad += 1
        if gap_notch < 0.5:
            note += f"  <-- 掉进缺口 {gap_notch:.2f}"
            bad += 1
        print(f"  ({x:7.2f},{y:7.2f}) r{r:.1f}  最小间隙 {worst[0]:6.2f}"
              f" ({worst[1]})  缺口 {gap_notch:7.2f}{note}")
    print(f"  problems: {bad}\n")
    return bad


def main():
    bad = 0
    bad += check_eyes()
    bad += check([("方孔", x, y, C.SQ / 2) for x, y in C.SQ_POS],
                 "方孔（方形，半边长）", square=True)
    print("TOTAL problems:", bad)


if __name__ == "__main__":
    main()
