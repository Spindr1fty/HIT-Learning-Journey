r"""Why the servo mount cannot be bolted through the carriage, and what a shaft
collar does instead. Two panels only -- the third kept spilling outside its axes
and adding no information the second does not already carry.

Panel A  the obstacle. The carriage is a 42 mm sleeve with a 30.6 mm bore, the
         30 mm rail runs inside it with 0.3 mm of clearance, and the wall is
         5.7 mm. A bolt through that wall would come out inside the bore and
         drive into the rail. There is nowhere for the tip to go and nowhere
         for a nut to sit.
Panel B  the fix: a collar around the OUTSIDE. It never touches the bore. A
         slit on one side with two M4 screws pulling across it squeezes the
         collar onto the carriage. No holes in the carriage at all, so the
         already-printed carriage can be reused as-is.

The collar also slides along the carriage before it is tightened, which gives
the vertical trim for free.
"""

import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUTER = 42.0
BORE = 30.6
RAIL_W = 30.0
WALL = (OUTER - BORE) / 2.0
COLLAR_IN = 42.6
COLLAR_OUT = 56.0
SLIT = 3.2

CARRIAGE_C = "#e9ecef"
CARRIAGE_E = "#868e96"
RAIL_FILL = "#c8a06a"
RAIL_EDGE = "#8a6a3a"
COLLAR_C = "#d0ebff"
SERVO_E = "#0b4f8a"
BAD = "#e03131"
GOOD = "#2f9e44"


def frame(ax, title, lim=38):
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)


def carriage_section(ax):
    ax.add_patch(Rectangle((-OUTER / 2, -OUTER / 2), OUTER, OUTER,
                           facecolor=CARRIAGE_C, edgecolor=CARRIAGE_E,
                           lw=2.0, zorder=3))
    ax.add_patch(Rectangle((-BORE / 2, -BORE / 2), BORE, BORE,
                           facecolor="white", edgecolor=CARRIAGE_E,
                           lw=1.2, ls=(0, (4, 2)), zorder=4))
    ax.add_patch(Rectangle((-RAIL_W / 2, -RAIL_W / 2), RAIL_W, RAIL_W,
                           facecolor=RAIL_FILL, alpha=0.6, edgecolor=RAIL_EDGE,
                           lw=1.8, zorder=5))
    ax.text(0, 0, "导轨\n30×30", fontsize=9.5, ha="center", va="center",
            color=RAIL_EDGE, fontweight="bold", zorder=6)


def panel_a(ax):
    frame(ax, "A. 为什么不能在滑块上打孔穿螺栓")
    carriage_section(ax)

    y = 15.0
    ax.annotate("", xy=(OUTER / 2 + 3, y), xytext=(OUTER / 2 + 24, y),
                arrowprops=dict(arrowstyle="->", color=BAD, lw=2.6))
    ax.add_patch(Rectangle((OUTER / 2 + 4, y - 2.0), 5, 4.0,
                           facecolor=BAD, edgecolor="none", zorder=8))
    ax.text(OUTER / 2 + 26, y + 2.5, "螺栓\n从这里进", fontsize=10.5,
            color=BAD, fontweight="bold", va="bottom")

    ax.annotate("", xy=(OUTER / 2, y), xytext=(RAIL_W / 2, y),
                arrowprops=dict(arrowstyle="<->", color=BAD, lw=2.0))
    ax.text((OUTER / 2 + RAIL_W / 2) / 2, y - 5.5, f"壁只剩 {WALL:.1f}",
            fontsize=10, color=BAD, fontweight="bold", ha="center")

    ax.text(0, -32, "穿过去直接顶到导轨，螺母也没地方放",
            fontsize=12, color=BAD, fontweight="bold", ha="center")


def panel_b(ax):
    frame(ax, "B. 改成抱箍：夹在滑块外面")
    panel_b.ax = ax

    # collar as a ring: outer circle first, the carriage square covers the hole
    ax.add_patch(Circle((0, 0), COLLAR_OUT / 2, facecolor=COLLAR_C,
                        edgecolor=SERVO_E, lw=2.0, zorder=2))
    # the slit, drawn as a notch cut into the ring at the top
    slit_h = (COLLAR_OUT - COLLAR_IN) / 2 + 1.0
    ax.add_patch(Rectangle((-SLIT / 2, COLLAR_IN / 2 - 1.0), SLIT, slit_h,
                           facecolor="white", edgecolor=SERVO_E, lw=1.2,
                           zorder=7))
    carriage_section(ax)

    # two clamp screws straddling the slit
    for x in (-10.0, 10.0):
        ax.plot([x, x], [COLLAR_IN / 2 - 4.0, COLLAR_OUT / 2 + 2.0],
                color=SERVO_E, lw=5.5, solid_capstyle="round", zorder=8)
    ax.text(0, COLLAR_OUT / 2 + 5.0, "拧这两颗 → 抱死",
            fontsize=11, color=SERVO_E, fontweight="bold", ha="center")

    ax.annotate("", xy=(COLLAR_OUT / 2 - 0.5, -20), xytext=(COLLAR_IN / 2, -20),
                arrowprops=dict(arrowstyle="<->", color=SERVO_E, lw=1.4))
    ax.text(COLLAR_OUT / 2 + 1.0, -20, "抱箍\n壁厚 6.7", fontsize=9.5,
            color=SERVO_E, va="center")

    ax.text(0, -32, "不碰孔、不加孔、还能沿滑块上下调位置",
            fontsize=12, color=GOOD, fontweight="bold", ha="center")


def main(out):
    fig = plt.figure(figsize=(15, 7.6), dpi=115)
    panel_a(fig.add_axes([0.02, 0.04, 0.46, 0.80]))
    panel_b(fig.add_axes([0.50, 0.04, 0.46, 0.80]))
    # no suptitle: the two panel titles already say it, and a figure title on
    # this aspect ratio lands on top of them
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "clamp.png")
