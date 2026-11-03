r"""Funnel gripper, simplified: the stem is the only thing that matters.

Earlier versions drew the stone's whole body in plan, which overlaps the funnel
and makes it look like a collision. It is not: the fork works at the STEM's
height, well above the body's shoulder. So these panels show only the stem and a
faint disc, which is all the fork can actually touch.

Frame: the CELL is centred on the origin and the fork's centreline is y=0. The
robot lines up on the cell, so a stone the opponent placed off-centre is the
error the fork has to swallow.

Panel A  two parallel tines, gap 12.6 for an 11 mm stem -> +/-0.8 mm. The stone
         is 16.5 mm off, so the stem passes outside the tines. Miss.
Panel B  a funnel. Mouth 44 mm closing to 12.6 mm over 30 mm. The stone gets
         shoved to the middle on the way in. It rides on ball transfers, so it
         slides instead of jamming.
Panel C  front view: the tines run under the dia 18 disc, 0.8 mm clear of the
         stem on each side, 1.9 mm clear of the disc above.

The fork's parts are drawn in its own frame: closed end at x=0, tines to x=12,
funnel mouth at x=42. It drives in +X.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

CELL = 80.0
HALF = CELL / 2
STEM_R = 5.5
DISC_R = 9.0
OFF = 16.5

TINE_IN = 6.3
TINE_OUT = 8.7
MOUTH = 22.0
X_CLOSED = 0.0
X_TIP = 12.0
X_MOUTH = 42.0

FORK = "#1c7ed6"
FORK_EDGE = "#0b4f8a"
BAD = "#e03131"
GOOD = "#2f9e44"
STEEL = "#495057"


def frame(ax, title, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=14.5, fontweight="bold", pad=10)


def cell(ax):
    ax.plot([-HALF, HALF, HALF, -HALF, -HALF],
            [-HALF, -HALF, HALF, HALF, -HALF],
            color="#ced4da", lw=1.8, ls=(0, (7, 5)), zorder=1)


def stem(ax, y, ghost=False, colour=STEEL):
    style = dict(facecolor="none" if ghost else colour,
                 alpha=0.25 if ghost else 0.85,
                 edgecolor=colour,
                 lw=1.6 if ghost else 1.8,
                 ls=(0, (4, 3)) if ghost else "-",
                 zorder=6)
    ax.add_patch(Circle((0, y), STEM_R, **style))
    ax.add_patch(Circle((0, y), DISC_R, facecolor="none",
                        edgecolor=colour, alpha=0.30 if ghost else 0.55,
                        lw=1.2, ls=(0, (2, 3)) if ghost else ":", zorder=5))


def tine_pair(ax, x0, x1):
    for sy in (-1, 1):
        lo, hi = sorted((sy * TINE_IN, sy * TINE_OUT))
        ax.add_patch(Rectangle((x0, lo), x1 - x0, hi - lo,
                               facecolor=FORK, alpha=0.85,
                               edgecolor=FORK_EDGE, lw=1.4, zorder=4))


def panel_a(ax):
    frame(ax, "A. 两片平行叉齿 —— 抓空", (-14, 62), (-34, 34))
    cell(ax)

    # the shank coming in from outside the cell
    ax.add_patch(Rectangle((-14, -10.5), 14, 21, facecolor=FORK, alpha=0.35,
                           edgecolor=FORK_EDGE, lw=1.4, zorder=3))
    tine_pair(ax, X_CLOSED, X_TIP)

    stem(ax, OFF, ghost=True, colour=BAD)
    ax.annotate("", xy=(0, OFF - STEM_R), xytext=(0, TINE_IN),
                arrowprops=dict(arrowstyle="<->", color=BAD, lw=2.2))
    ax.text(2, (OFF - STEM_R + TINE_IN) / 2,
            f"杆在这里\n超出叉齿 10.2", fontsize=10.5,
            color=BAD, fontweight="bold", va="center")

    ax.annotate("", xy=(X_TIP + 6, 0), xytext=(X_TIP + 6, OFF),
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1.4,
                                ls=(0, (4, 3))))
    ax.text(X_TIP + 8, OFF / 2, "擦肩而过", fontsize=10, color=BAD)

    ax.text(HALF / 2, -30, "叉齿内间距 12.6，杆 11  ->  容差 ±0.8 mm\n"
                           "壶偏了 16.5 mm  ",
            fontsize=11, color=BAD, fontweight="bold", ha="center")


def panel_b(ax):
    frame(ax, "B. 喇叭漏斗 —— 兜进来、自己滑到中间", (-14, 62), (-34, 34))
    cell(ax)

    ax.add_patch(Rectangle((-14, -10.5), 14, 21, facecolor=FORK, alpha=0.35,
                           edgecolor=FORK_EDGE, lw=1.4, zorder=3))
    tine_pair(ax, X_CLOSED, X_TIP)
    for sy in (-1, 1):
        ax.plot([X_TIP, X_MOUTH], [sy * TINE_IN, sy * MOUTH],
                color=FORK_EDGE, lw=4.0, solid_capstyle="round", zorder=4)

    # closed end
    ax.plot([X_CLOSED, X_CLOSED], [-TINE_OUT, TINE_OUT],
            color=FORK_EDGE, lw=4.0, solid_capstyle="round", zorder=5)

    stem(ax, OFF, ghost=True, colour="#adb5bd")
    stem(ax, 0.0, colour=GOOD)

    ax.add_patch(FancyArrowPatch((0, OFF - STEM_R), (0, STEM_R + 0.5),
                                 arrowstyle="->", mutation_scale=20,
                                 color=GOOD, lw=2.6,
                                 connectionstyle="arc3,rad=0.3"))
    ax.text(-11, OFF / 2 + 4, "被斜壁推回中心", fontsize=10.5, color=GOOD,
            fontweight="bold", va="center")

    ax.annotate("", xy=(X_MOUTH, -MOUTH - 6), xytext=(X_MOUTH, MOUTH + 6),
                arrowprops=dict(arrowstyle="<->", color=GOOD, lw=1.8))
    ax.text(X_MOUTH - 2, 0, f"口宽\n{2 * MOUTH:.0f}", fontsize=10.5,
            color=GOOD, fontweight="bold", va="center", ha="right")

    ax.text(HALF / 2, -30, f"口宽 44 让杆进得来  ->  容差 ±"
                           f"{MOUTH - STEM_R:.0f} mm\n"
                           f"闭合端顶住杆，深度每次一样",
            fontsize=11, color=GOOD, fontweight="bold", ha="center")


def panel_c(ax):
    frame(ax, "C. 正视：叉齿从盘下穿过", (-30, 30), (-7, 38))

    ax.add_patch(Rectangle((-23.5, 0), 47, 21.6, facecolor="#c8a06a",
                           alpha=0.28, edgecolor="#8a6a3a", lw=1.2))
    ax.text(0, 6, "壶身 Ø47", fontsize=9, ha="center", color="#8a6a3a")
    ax.add_patch(Rectangle((-STEM_R, 21.6), 2 * STEM_R, 7.5,
                           facecolor="#c8a06a", alpha=0.55,
                           edgecolor="#8a6a3a", lw=1.3))
    ax.add_patch(Rectangle((-DISC_R, 29.1), 2 * DISC_R, 2.9,
                           facecolor="#c8a06a", alpha=0.85,
                           edgecolor="#8a6a3a", lw=1.6))
    ax.text(0, 30.5, "盘 Ø18", fontsize=9, ha="center", color="#8a6a3a")

    for sy in (-1, 1):
        lo, hi = sorted((sy * TINE_IN, sy * TINE_OUT))
        ax.add_patch(Rectangle((lo, 23.7), hi - lo, 3.5,
                               facecolor=FORK, alpha=0.9,
                               edgecolor=FORK_EDGE, lw=1.5, zorder=5))
    ax.text(-17, 25.45, "叉齿", fontsize=10.5, color=FORK_EDGE,
            fontweight="bold", va="center")

    ax.annotate("", xy=(TINE_IN, 27.2), xytext=(TINE_IN, 29.1),
                arrowprops=dict(arrowstyle="<->", color=GOOD, lw=1.5))
    ax.text(TINE_IN + 1.0, 28.1, "1.9", fontsize=9, color=GOOD, va="center")
    ax.annotate("", xy=(STEM_R, 23.7), xytext=(TINE_IN, 23.7),
                arrowprops=dict(arrowstyle="<->", color=BAD, lw=1.5))
    ax.text(5.9, 21.8, "0.8", fontsize=9, color=BAD, ha="center")

    ax.text(0, -4, "杆两侧各 0.8，叉齿整条压在盘下", fontsize=10.5,
            ha="center")


def main(out):
    fig = plt.figure(figsize=(18.5, 7.8), dpi=110)
    panel_a(fig.add_axes([0.008, 0.10, 0.29, 0.76]))
    panel_b(fig.add_axes([0.335, 0.10, 0.29, 0.76]))
    panel_c(fig.add_axes([0.685, 0.26, 0.30, 0.50]))

    fig.suptitle("取壶托叉：平行叉齿  ->  喇叭漏斗", fontsize=17,
                 fontweight="bold", y=0.97)

    axn = fig.add_axes([0.685, 0.03, 0.30, 0.18])
    axn.axis("off")
    rows = [("为什么能行", True, "#212529"),
            ("壶底是 3 颗万向滚珠，横向一拨就滑过去", False, "#212529"),
            ("漏斗在杆的高度，从壶身上方掠过，不碰壶身", False, "#212529"),
            ("所以不用视觉，机械自己找正", False, GOOD)]
    for i, (t, bold, col) in enumerate(rows):
        axn.text(0, 1.0 - i * 0.26, t, fontsize=11,
                 fontweight="bold" if bold else "normal", color=col, va="top")

    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "funnel.png")
