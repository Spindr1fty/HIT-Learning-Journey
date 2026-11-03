r"""What a bolt circle diameter is, drawn on the actual servo horn.

BCD (Bolt Circle Diameter) is the diameter of the circle that passes through
the CENTRES of the mounting holes. It is the standard way to specify a bolt
pattern, because one number plus the hole count fully defines it.

For this horn the BCD is 14.4, which means:

    hole centres sit 7.2 mm from the horn's axis
    two OPPOSITE holes are 14.4 mm apart (they lie on a diameter)
    two ADJACENT holes are 14.4 / sqrt(2) = 10.18 mm apart

The trap that cost us two wrong gears: a caliper's inside jaws pushed into two
holes press against the holes' INNER WALLS, so they read the centre distance
MINUS the hole diameter. With a 3.0 hole that is 14.4 - 3.0 = 11.4 -- which is
exactly where the wrong number came from.
"""

import sys
from math import cos, sin, pi, sqrt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BCD = 14.4
HOLE_D = 3.0
HORN_D = 20.0
R = BCD / 2.0

STEEL = "#868e96"
HOLE = "#e03131"
BCD_C = "#1c7ed6"
OK = "#2f9e44"


def main(out):
    fig = plt.figure(figsize=(12.5, 8.6), dpi=120)
    # explicit axes rectangles: plt.subplots would let the drawing span the
    # whole figure and the notes panel would land on top of it
    ax = fig.add_axes([0.01, 0.04, 0.46, 0.88])
    ax.set_xlim(-16, 16)
    ax.set_ylim(-15, 15)
    ax.set_aspect("equal")
    ax.axis("off")

    # the horn itself
    ax.add_patch(Circle((0, 0), HORN_D / 2, facecolor="#e9ecef",
                        edgecolor=STEEL, lw=1.8, zorder=1))
    ax.add_patch(Circle((0, 0), HORN_D / 2, facecolor="none",
                        edgecolor=STEEL, lw=1.8, zorder=3))
    ax.text(0, -HORN_D / 2 - 1.4, "舵盘 Ø20", fontsize=10, ha="center",
            color=STEEL)

    # the bolt circle
    ax.add_patch(Circle((0, 0), R, facecolor="none", edgecolor=BCD_C,
                        lw=1.4, ls=(0, (5, 3)), zorder=4))
    ax.text(0, R + 0.9, "螺栓分布圆 Ø14.4  （BCD）", fontsize=11,
            ha="center", color=BCD_C, fontweight="bold")

    # the four holes
    pts = []
    for k in range(4):
        a = pi / 2 * k
        x, y = R * cos(a), R * sin(a)
        pts.append((x, y))
        ax.add_patch(Circle((x, y), HOLE_D / 2, facecolor="white",
                            edgecolor=HOLE, lw=2.0, zorder=5))
        ax.plot([x], [y], marker="+", color=HOLE, ms=9, mew=1.6, zorder=6)

    # opposite hole distance
    ax.annotate("", xy=(pts[0][0], 0), xytext=(pts[2][0], 0),
                arrowprops=dict(arrowstyle="<->", color=OK, lw=2.2))
    ax.text(0.2, -1.6, "对角孔中心距 = 14.4", fontsize=10.5, color=OK,
            fontweight="bold", ha="center")

    # adjacent hole distance
    ax.annotate("", xy=pts[0], xytext=pts[1],
                arrowprops=dict(arrowstyle="<->", color="#c2255c", lw=1.8))
    ax.text(7.4, 6.4, "相邻孔\n10.18", fontsize=9, color="#c2255c",
            ha="left", va="center")

    # the centre
    ax.plot([0], [0], marker="+", color="#212529", ms=12, mew=1.8, zorder=7)
    ax.plot([-R - 2.4, R + 2.4], [0, 0], color="#adb5bd", lw=0.5, zorder=0)
    ax.plot([0, 0], [-R - 2.4, R + 2.4], color="#adb5bd", lw=0.5, zorder=0)
    ax.annotate("", xy=(0, 0), xytext=(0, R),
                arrowprops=dict(arrowstyle="->", color=BCD_C, lw=1.3))
    ax.text(0.4, R / 2, "7.2", fontsize=9.5, color=BCD_C, va="center")

    # --- notes panel -----------------------------------------------------
    axn = fig.add_axes([0.50, 0.03, 0.49, 0.85])
    axn.axis("off")
    rows = [
        ("BCD 是什么", True, "#212529"),
        ("Bolt Circle Diameter，螺栓分布圆直径。", False, "#212529"),
        ("就是「所有安装孔中心所在的圆」的直径。", False, "#212529"),
        ("", False, "#212529"),
        ("BCD 14.4 意味着", True, "#212529"),
        ("· 每个孔中心离轴心 7.2 mm", False, "#212529"),
        ("· 对角两孔 14.4 mm（正好是一条直径）", False, "#212529"),
        ("· 相邻两孔 14.4 ÷ √2 = 10.18 mm", False, "#212529"),
        ("", False, "#212529"),
        ("为什么容易量错", True, "#e03131"),
        ("卡尺内测量爪插进两个孔，顶住的是", False, "#212529"),
        ("两个孔「相对的内壁」：", False, "#212529"),
        ("    读数 = 孔中心距 − 孔径", False, "#e03131"),
        ("    11.4 = 14.4 − 3.0", False, "#e03131"),
        ("误差刚好等于一个孔径，所以孔越大错越多。", False, "#212529"),
        ("", False, "#212529"),
        ("可靠量法", True, OK),
        ("① 穿两颗 M3 螺丝，量螺杆外侧，再减 3.0", False, OK),
        ("② 用量出来的距离直接做 1:1 纸模板比对", False, OK),
    ]
    y = 1.0
    for text, bold, col in rows:
        axn.text(0, y, text, fontsize=11.5,
                 fontweight="bold" if bold else "normal",
                 color=col, va="top")
        y -= 0.046 if text else 0.028

    fig.suptitle("BCD（螺栓分布圆直径）是什么", fontsize=17,
                 fontweight="bold", y=0.975)
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bcd.png")
