r"""Nut retention: the difference between a pocket that holds and one that only
looks like it holds.

THE PRINCIPLE
A bolt and nut only do their job if they SANDWICH the workpieces between them,
and the nut has to be physically unable to leave its pocket. A straight-sided
pocket that is open on one face satisfies neither: the nut can be walked out of
the open face, and if it goes the joint simply falls apart however tight the
screw was.

THE FIX
Two things, both drawn:
  1. The bolt head and the nut sit on opposite outboard faces of the stack, so
     the material between them is what gets clamped.
  2. The pocket has a LIP. Its opening is narrower than the nut across corners,
     so the nut is pressed in once and thereafter cannot come out. Printed with
     a 0.3 mm interference, the lip flexes over the nut and then traps it.

Panel A shows the failing arrangement, panel B the retained one.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PLATE = "#d0ebff"
PLATE_E = "#0b4f8a"
WORK = "#e9ecef"
WORK_E = "#868e96"
BOLT = "#e8590c"
BOLT_E = "#a33d0b"
NUT = "#2f9e44"
BAD = "#e03131"
GOOD = "#2f9e44"

NUT_AF = 7.2          # nut across flats
NUT_T = 3.2           # nut thickness
LIP_OPEN = 6.0        # lip opening, narrower than the nut


def frame(ax, title, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)


def bolt(ax, x, y0, y1, head_w=12.0, head_h=4.0, up=True):
    ax.plot([x, x], [y0, y1], color=BOLT, lw=5.0, solid_capstyle="butt",
            zorder=7)
    yy = y1 if up else y0 - head_h
    ax.add_patch(Rectangle((x - head_w / 2, yy), head_w, head_h,
                           facecolor=BOLT, edgecolor=BOLT_E, lw=1.2, zorder=8))


def nut(ax, x, y, label=True):
    ax.add_patch(Rectangle((x - NUT_AF / 2, y), NUT_AF, NUT_T,
                           facecolor=NUT, alpha=0.55, edgecolor=GOOD,
                           lw=1.5, zorder=9))
    if label:
        ax.text(x, y + NUT_T / 2, "螺母", fontsize=8, ha="center",
                va="center", color="#1b5e20", zorder=10)


def panel_a(ax):
    frame(ax, "A. 错：开口直壁槽 —— 螺母能被抽出来", (-42, 42), (-26, 40))

    # upper workpiece and the plate with a straight-sided open pocket
    ax.add_patch(Rectangle((-28, 22), 56, 10, facecolor=WORK,
                           edgecolor=WORK_E, lw=1.6))
    ax.text(-25, 27, "导轨脚", fontsize=9, va="center", color=WORK_E)

    ax.add_patch(Polygon([(-30, 10), (-NUT_AF / 2, 10), (-NUT_AF / 2, 10 + NUT_T),
                          (NUT_AF / 2, 10 + NUT_T), (NUT_AF / 2, 10),
                          (30, 10), (30, 22), (-30, 22)],
                         closed=True, facecolor=PLATE,
                         edgecolor=PLATE_E, lw=1.8, zorder=5))
    ax.text(-26, 18, "底板", fontsize=9, va="center", color=PLATE_E)

    nut(ax, 0, 10.0)
    bolt(ax, 0, -18, 10.0)

    ax.annotate("", xy=(0, -6), xytext=(0, 10),
                arrowprops=dict(arrowstyle="->", color=BAD, lw=2.4,
                                ls=(0, (5, 3))))
    ax.text(6, -2, "螺母沿开口方向\n直接退出 → 连接失效", fontsize=10.5,
            color=BAD, fontweight="bold", va="center")
    ax.text(0, -24, "槽是开口的，没有任何东西挡住螺母", fontsize=11.5,
            color=BAD, fontweight="bold", ha="center")


def panel_b(ax):
    frame(ax, "B. 对：带唇口的螺母槽 —— 压进去就出不来", (-42, 42), (-26, 40))

    ax.add_patch(Rectangle((-28, 22), 56, 10, facecolor=WORK,
                           edgecolor=WORK_E, lw=1.6))
    ax.text(-25, 27, "导轨脚", fontsize=9, va="center", color=WORK_E)

    # plate with a nut trap: wide cavity, narrow lip at the bottom opening
    cav_top = 10 + NUT_T + 1.0
    ax.add_patch(Polygon([
        (-30, 10), (-LIP_OPEN / 2, 10), (-LIP_OPEN / 2, 10 + 0.8),
        (-NUT_AF / 2, 10 + 0.8), (-NUT_AF / 2, cav_top),
        (NUT_AF / 2, cav_top), (NUT_AF / 2, 10 + 0.8),
        (LIP_OPEN / 2, 10 + 0.8), (LIP_OPEN / 2, 10),
        (30, 10), (30, 22), (-30, 22)],
        closed=True, facecolor=PLATE, edgecolor=PLATE_E, lw=1.8, zorder=5))
    ax.text(-26, 18, "底板", fontsize=9, va="center", color=PLATE_E)

    nut(ax, 0, 10.8)
    bolt(ax, 0, -18, 10.8)

    ax.annotate("唇口只有 6.0 宽\n比螺母对角 8.3 窄", xy=(LIP_OPEN / 2 + 0.4, 10.4),
                xytext=(16, 2), fontsize=10, color=GOOD,
                arrowprops=dict(arrowstyle="->", color=GOOD, lw=1.4))
    ax.annotate("拧紧 → 螺母被拉进槽里\n顶死在槽顶，四面被壁包住",
                xy=(-NUT_AF / 2 - 0.4, 12.5), xytext=(-40, 33),
                fontsize=10, color=GOOD, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GOOD, lw=1.4))

    ax.text(0, -24, "螺栓头 ↔ 螺母把两层板夹在中间，螺母被唇口卡死",
            fontsize=11.5, color=GOOD, fontweight="bold", ha="center")


def main(out):
    fig = plt.figure(figsize=(16.5, 7.4), dpi=115)
    panel_a(fig.add_axes([0.01, 0.04, 0.48, 0.84]))
    panel_b(fig.add_axes([0.51, 0.04, 0.48, 0.84]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "nut.png")
