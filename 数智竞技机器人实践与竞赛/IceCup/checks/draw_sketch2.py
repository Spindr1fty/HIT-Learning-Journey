r"""Sketch before modelling: the two joints that still had no answer.

PANEL A  base plate to chassis, WITHOUT drilling.
         The chassis will be laser cut, so its four holes are designed in and
         come free with the cut -- no drill needed. The bolt goes UP from under
         the chassis, through it and through the plate, into a nut sitting in a
         pocket in the plate's TOP face. That pocket is what answers the worry
         about the nut pulling out: tightening drags the nut DOWN into the
         pocket, and the pocket's sides stop it turning. The nut is inside the
         plate's thickness, capped above by the rail foot and below by the
         pocket floor, so the pair cannot be pulled apart.

PANEL B  fork, split version.
         A collar clamps the carriage the same way the servo mount's does. A
         plate hangs off its front with two vertical slots, and the fork head
         bolts onto that plate. Loosen the two bolts, slide the head up or
         down the slots, tighten. That is the +/-25 mm of height trim the
         unknown chassis height demands -- it can be made now and set later.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PLATE = "#d0ebff"
PLATE_E = "#0b4f8a"
RAIL = "#c8a06a"
RAIL_E = "#8a6a3a"
CHASSIS = "#e9ecef"
CHASSIS_E = "#868e96"
BOLT = "#e8590c"
NUT = "#2f9e44"
GOOD = "#2f9e44"
GROUND = "#212529"


def frame(ax, title, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13.5, fontweight="bold", pad=10)


def bolt_head(ax, x, y, w=7.0, h=3.2):
    ax.add_patch(Rectangle((x - w / 2, y), w, h, facecolor=BOLT,
                           edgecolor="#a33d0b", lw=1.2, zorder=9))
    ax.plot([x, x], [y + h, y + h + 12], color=BOLT, lw=4.5,
            solid_capstyle="butt", zorder=8)


def nut(ax, x, y, w=7.2, h=3.2, label=True):
    ax.add_patch(Rectangle((x - w / 2, y), w, h, facecolor=NUT, alpha=0.55,
                           edgecolor=GOOD, lw=1.4, zorder=9))
    if label:
        ax.text(x, y + h / 2, "螺母", fontsize=7.5, ha="center", va="center",
                color="#1b5e20", zorder=10)


def panel_a(ax):
    frame(ax, "A. 底板 ↔ 底盘：不钻孔，螺母藏在底板里", (-46, 46), (-30, 42))

    # sandwich: rail foot / plate / chassis, seen from the side
    ax.add_patch(Rectangle((-30, 18), 60, 8, facecolor=RAIL, alpha=0.6,
                           edgecolor=RAIL_E, lw=1.6))
    ax.text(-27, 22, "导轨脚 8", fontsize=9, va="center", color=RAIL_E)

    ax.add_patch(Rectangle((-34, 10), 68, 8, facecolor=PLATE,
                           edgecolor=PLATE_E, lw=1.8))
    ax.text(-31, 14, "底板 8", fontsize=9, va="center", color=PLATE_E)

    ax.add_patch(Rectangle((-38, 0), 76, 10, facecolor=CHASSIS,
                           edgecolor=CHASSIS_E, lw=1.6))
    ax.text(-35, 5, "底盘（激光切，孔一起切出来）", fontsize=9, va="center",
            color=CHASSIS_E)

    # the nut pocket in the plate's TOP face, then the bolt from below
    ax.add_patch(Rectangle((-3.6, 10), 7.2, 3.6, facecolor="white",
                           edgecolor=GOOD, lw=1.4, ls=(0, (3, 2)), zorder=7))
    nut(ax, 0, 10.0)
    ax.plot([0, 0], [-12, 10], color=BOLT, lw=4.5, solid_capstyle="butt",
            zorder=8)
    ax.add_patch(Rectangle((-3.5, -14.5), 7.0, 3.0, facecolor=BOLT,
                           edgecolor="#a33d0b", lw=1.2, zorder=9))
    ax.annotate("螺栓从下面穿上来", xy=(0, -9), xytext=(-40, -20),
                fontsize=10, color=BOLT, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=BOLT, lw=1.4))

    ax.annotate("", xy=(10, 13.6), xytext=(10, 10.0),
                arrowprops=dict(arrowstyle="->", color=GOOD, lw=1.8))
    ax.text(11.5, 11.8, "拧紧时螺母被\n往下拉进槽里", fontsize=9.5,
            color=GOOD, va="center")

    ax.text(0, -27, "螺母被槽四面包住 → 拔不出来，也不会跟着转",
            fontsize=11, color=GOOD, fontweight="bold", ha="center")


def panel_b(ax):
    frame(ax, "B. 托叉分体：抱箍 + 竖槽板 + 托叉头", (-40, 46), (-34, 34))

    # carriage and its collar, seen from the side
    ax.add_patch(Rectangle((-21, 6), 42, 22, facecolor=CHASSIS,
                           edgecolor=CHASSIS_E, lw=1.8))
    ax.text(0, 17, "滑块", fontsize=9.5, ha="center", color=CHASSIS_E)
    ax.add_patch(Rectangle((-27, 6), 54, 6, facecolor=PLATE,
                           edgecolor=PLATE_E, lw=1.6))
    ax.text(-24, 9, "抱箍", fontsize=8.5, va="center", color=PLATE_E)

    # the vertical slotted plate hanging off the collar's +X side
    ax.add_patch(Rectangle((22, -22), 8, 34, facecolor=PLATE,
                           edgecolor=PLATE_E, lw=1.8))
    for x in (26.0,):
        ax.add_patch(Rectangle((x - 2.0, -16), 4.0, 26, facecolor="white",
                               edgecolor=PLATE_E, lw=1.2, zorder=6))
    ax.text(30, 0, "竖槽板\n±25mm 可调", fontsize=9.5, color=PLATE_E,
            va="center")

    # the fork head bolted to it
    ax.add_patch(Rectangle((12, -26), 16, 14, facecolor="#c8a06a", alpha=0.55,
                           edgecolor=RAIL_E, lw=1.6))
    ax.text(20, -19, "托叉头", fontsize=9, ha="center", va="center",
            color=RAIL_E)
    ax.plot([26, 26], [-20, -20], marker="o", ms=7, color=BOLT, zorder=9)
    ax.text(20, -29, "两颗 M4 穿过竖槽锁紧", fontsize=9, ha="center",
            color=BOLT, fontweight="bold")

    ax.annotate("", xy=(26, 10), xytext=(26, -10),
                arrowprops=dict(arrowstyle="<->", color=GOOD, lw=2.0))
    ax.text(0, -32, "高度现场调 → 底盘多高都能对上", fontsize=11,
            color=GOOD, fontweight="bold", ha="center")


def main(out):
    fig = plt.figure(figsize=(16, 7.6), dpi=115)
    panel_a(fig.add_axes([0.01, 0.04, 0.48, 0.86]))
    panel_b(fig.add_axes([0.51, 0.04, 0.48, 0.86]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sketch.png")
