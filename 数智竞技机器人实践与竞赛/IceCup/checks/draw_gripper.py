"""Gripper concept: a fixed two-tine fork that lifts the stone by its handle disc.

Measured off the official stone drawing (renders/rules_pptx/
stone_32x47_official.png) at 13.9 px/mm:

    stone base ................ y =  0.0
    widest band, dia 47 ....... y = 11.0
    body top (shoulder) ....... y = 23.7
    stem exposed, dia 11 ...... y = 23.7 .. 29.1   (the drawing's 5 mm)
    handle disc, dia ~21.6 .... y = 29.1 .. 32.0

The disc overhangs the stem by (21.6 - 11)/2 = 5.3 mm all round, and under it
sits a 5.4 mm tall gap. That is a pallet: a tine thinner than the gap, sliding
in from the side, takes the whole 70 g stone. No magnet, no jaw closing on a
curved body through a 16.5 mm slot, no actuator at all.

The body's shoulder is a cone that widens downward from the stem to the dia 47
band, so a tine arriving slightly low rides up it -- the part self-guides.

Every panel draws the stone UPRIGHT: x is lateral, y is height. An earlier
version had the profile on its side while the lift arrow pointed up, which made
the drawing contradict itself.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

STONE = "#c8a06a"
STONE_EDGE = "#8a6a3a"
TINE = "#1c7ed6"
TINE_EDGE = "#0b4f8a"
GAP = "#e03131"
OK = "#2f9e44"

PROFILE = [
    (0.0, 20.0), (1.5, 22.8), (4.0, 23.5), (11.0, 23.5), (14.0, 23.2),
    (18.0, 22.0), (21.5, 18.0), (23.7, 11.0), (24.6, 8.0), (25.5, 5.5),
    (29.1, 5.5), (29.1, 10.8), (32.0, 10.8),
]
DISC_T = 2.9
STEM_Y0, STEM_Y1 = 23.7, 29.1
DISC_R = 10.8
STEM_R = 5.5


def frame(ax, title, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=8)


def stone_up(ax, alpha=1.0):
    pts = [(r, y) for y, r in PROFILE]
    pts += [(-r, y) for y, r in reversed(PROFILE)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=STONE, alpha=alpha,
                         edgecolor=STONE_EDGE, lw=1.6, zorder=2))


def panel_a(ax):
    frame(ax, "A. 冰壶真实轮廓（按官方图标定）", (-34, 46), (-5, 40))
    stone_up(ax)

    # the pallet gap, highlighted as a band across the stem
    ax.add_patch(Rectangle((-STEM_R, STEM_Y0), 2 * STEM_R, STEM_Y1 - STEM_Y0,
                           facecolor=GAP, alpha=0.30, edgecolor=GAP,
                           lw=1.3, ls=(0, (3, 2)), zorder=6))
    ax.annotate("★ 托叉入口\n盘下 5.4 mm 空档",
                xy=(5.0, 26.4), xytext=(19.0, 20.0),
                fontsize=10, color=GAP, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GAP, lw=1.4))

    # height dimension lines on the right
    for y, txt in ((0.0, "壶底 0"), (11.0, "最宽 Ø47 @ y=11"),
                   (23.7, "壶身顶 23.7"), (29.1, "柄盘底 29.1"),
                   (32.0, "总高 32")):
        ax.plot([22.5, 30], [y, y], color="#868e96", lw=0.8)
        ax.text(31.0, y, txt, fontsize=8.8, va="center", color="#495057")

    ax.annotate("锥面：走低了自动爬上来",
                xy=(16.0, 21.0), xytext=(-31, 12.5), fontsize=9.5, color=OK,
                arrowprops=dict(arrowstyle="->", color=OK, lw=1.2))
    ax.text(0, 36.5, "Ø47", fontsize=11, color=STONE_EDGE, ha="center",
            fontweight="bold")
    ax.text(-12.5, 26.4, "Ø11 杆", fontsize=9, color=STONE_EDGE, ha="center")
    ax.text(13.0, 33.2, "柄盘 Ø21.6", fontsize=9, color=STONE_EDGE)


def panel_b(ax):
    frame(ax, "B. 侧视：叉齿滑进盘下，然后 Z 轴抬起", (-46, 30), (-5, 42))
    stone_up(ax)

    # tine in the stem band, arriving from -X
    y0 = 24.6
    ax.add_patch(Polygon([(-44, y0), (0.0, y0), (0.0, y0 + 3.5), (-44, y0 + 3.5)],
                         closed=True, facecolor=TINE, alpha=0.55,
                         edgecolor=TINE_EDGE, lw=1.6, zorder=5))
    # wedge tip
    ax.add_patch(Polygon([(0.0, y0), (0.0, y0 + 3.5), (-3.5, y0)],
                         closed=True, facecolor=TINE, alpha=0.55,
                         edgecolor=TINE_EDGE, lw=1.6, zorder=5))

    ax.annotate("", xy=(-2, 26.4), xytext=(-26, 26.4),
                arrowprops=dict(arrowstyle="->", color=TINE_EDGE, lw=2.2))
    ax.text(-14, 27.6, "底盘前进即插入", fontsize=10, color=TINE_EDGE,
            fontweight="bold", ha="center")

    ax.add_patch(FancyArrowPatch((14.0, 34.5), (14.0, 37.5), arrowstyle="->",
                                 mutation_scale=14, color="#212529", lw=2.0))
    ax.text(15.5, 36.0, "Z 轴抬升\n托住柄盘", fontsize=9.5, va="center")

    ax.annotate("尖端 45° 楔形", xy=(-2.0, 24.8), xytext=(-30, 32.5),
                fontsize=9.5, color=OK,
                arrowprops=dict(arrowstyle="->", color=OK, lw=1.2))
    ax.text(-44, 40, "叉齿厚 3.5（空档 5.4）", fontsize=9.5,
            color=TINE_EDGE, fontweight="bold")


def panel_c(ax):
    frame(ax, "C. 俯视：两齿跨过 Ø11 杆", (-17, 17), (-17, 17))

    ax.add_patch(Circle((0, 0), DISC_R, facecolor=STONE, alpha=0.40,
                        edgecolor=STONE_EDGE, lw=1.6))
    ax.add_patch(Circle((0, 0), STEM_R, facecolor="white",
                        edgecolor=STONE_EDGE, lw=1.3, ls=(0, (4, 3))))
    ax.text(0, 0, "Ø11\n杆", fontsize=9, ha="center", va="center")

    for sy in (-1, 1):
        ax.add_patch(Rectangle((-15.5, sy * 7.5 - 2.0), 31, 4.0,
                               facecolor=TINE, alpha=0.60,
                               edgecolor=TINE_EDGE, lw=1.6, zorder=4))
        ax.text(-13.0, sy * 7.5, "齿", fontsize=9.5, color="white",
                ha="center", va="center", zorder=6)

    ax.annotate("", xy=(0.0, 5.5), xytext=(0.0, 10.8),
                arrowprops=dict(arrowstyle="<->", color=GAP, lw=1.3))
    ax.text(-4.5, 8.2, "外伸\n5.3", fontsize=8.5, color=GAP, ha="right")
    ax.text(0, -15.2, "齿占 r=5.5..9.5：既避开杆，又吃到盘",
            fontsize=9.5, ha="center", color=TINE_EDGE)


def main(out):
    fig = plt.figure(figsize=(18, 9.6), dpi=110)
    panel_a(fig.add_axes([0.01, 0.06, 0.30, 0.84]))
    panel_b(fig.add_axes([0.315, 0.06, 0.335, 0.84]))
    panel_c(fig.add_axes([0.68, 0.26, 0.30, 0.46]))

    fig.suptitle("取壶机构（无磁铁方案）：双齿托叉钩住手柄盘下沿",
                 fontsize=16, fontweight="bold", y=0.965)

    axp = fig.add_axes([0.68, 0.04, 0.31, 0.19])
    axp.axis("off")
    notes = [
        ("为什么选这个", True),
        ("· 零执行器：底盘前进即插入，后退即松开", False),
        ("· 不挤 16.5mm 侧缝，不碰壶身曲面", False),
        ("· 锥面自导向，垂直容差约 ±2mm", False),
        ("· 壶靠自重挂在叉上，不靠摩擦夹持", False),
    ]
    for i, (line, bold) in enumerate(notes):
        axp.text(0, 1.0 - i * 0.20, line, fontsize=10.5,
                 fontweight="bold" if bold else "normal",
                 va="top", color="#212529")

    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gripper_concept.png")
