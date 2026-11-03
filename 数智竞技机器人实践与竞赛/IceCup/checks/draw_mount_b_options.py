r"""Catalogue of candidate reinforcement placements for g_mount_b.

Top view of the part with six numbered reinforcement options drawn in colour.
The user just has to pick a number.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FOOT = (0.0, 40.0, 3.94, 96.44)
POSTS = [(21.94, 29.94), (70.44, 78.44)]
POST_X = (0.0, 5.0)
HOLES_X = [8.0, 16.196, 24.392, 32.588]
HOLE_Y = 19.94
SERVO = (30.19, 70.19)      # body span in Y

EDGE = "#1b3b5a"
FILL = "#eef4fb"
FILL2 = "#cfe0f2"


def num(ax, x, y, text, colour, size=15):
    ax.text(x, y, text, fontsize=size, fontweight="bold", color="white",
            ha="center", va="center", zorder=20,
            bbox=dict(boxstyle="circle,pad=0.25", fc=colour, ec="white",
                      lw=1.4))


def main(out):
    fig, ax = plt.subplots(figsize=(11.5, 15.0), dpi=115, facecolor="white")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("补强位置选项（俯视）—— 圈号码告诉我", fontsize=16,
                 fontweight="bold", pad=16)

    # base part
    ax.add_patch(Rectangle((FOOT[0], FOOT[2]), FOOT[1] - FOOT[0],
                           FOOT[3] - FOOT[2], facecolor=FILL, edgecolor=EDGE,
                           lw=2.0))
    for y0, y1 in POSTS:
        ax.add_patch(Rectangle((POST_X[0], y0), POST_X[1] - POST_X[0],
                               y1 - y0, facecolor=FILL2, edgecolor=EDGE,
                               lw=1.6))
    ax.add_patch(Rectangle((POST_X[0], POSTS[0][0]), POST_X[1] - POST_X[0],
                           POSTS[1][1] - POSTS[0][0], fill=False,
                           edgecolor="#8fb0d0", lw=1.0, ls="--"))
    ax.add_patch(Rectangle((-10.0, SERVO[0]), 40.0, SERVO[1] - SERVO[0],
                           fill=False, edgecolor="#c92a2a", lw=1.3, ls=":"))
    ax.text(10, (SERVO[0] + SERVO[1]) / 2, "舵机机身（参考）", fontsize=10,
            color="#c92a2a", ha="center")
    for hx in HOLES_X:
        ax.add_patch(Circle((hx, HOLE_Y), 2.25, facecolor="white",
                            edgecolor=EDGE, lw=1.2))

    # --- option 1: outer triangular gussets (current) ---
    for y0, sgn in ((POSTS[0][0], -1), (POSTS[1][1], 1)):
        ax.add_patch(Polygon([(0.0, y0), (5.0, y0),
                              (0.0, y0 + sgn * 18)],
                             facecolor="#74c0fc", edgecolor="#1864ab", lw=1.4,
                             alpha=0.75))
    num(ax, -4.0, 12.0, "1", "#1864ab")
    num(ax, -4.0, 88.0, "1", "#1864ab")

    # --- option 2: inner face blocks (needs servo to move) ---
    for y0, sgn in ((POSTS[0][1], 1), (POSTS[1][0], -1)):
        ax.add_patch(Rectangle((0.0, min(y0, y0 + sgn * 10)), 5.0, 10.0,
                               facecolor="#ffa8a8", edgecolor="#c92a2a",
                               lw=1.4, alpha=0.8))
    num(ax, 2.5, 36.0, "2", "#c92a2a")
    num(ax, 2.5, 64.0, "2", "#c92a2a")

    # --- option 3: rear face (+X) gussets ---
    for y0, y1 in POSTS:
        ax.add_patch(Polygon([(5.0, y0), (5.0, y1), (18.0, y0)],
                             facecolor="#b2f2bb", edgecolor="#2b8a3e", lw=1.4,
                             alpha=0.8))
    num(ax, 12.0, 22.0, "3", "#2b8a3e")

    # --- option 4: skirt around each post root ---
    for y0, y1 in POSTS:
        ax.add_patch(Rectangle((-6.0, y0 - 6.0), 6.0 + 5.0 + 6.0,
                               (y1 - y0) + 12.0, fill=False,
                               edgecolor="#7048e8", lw=2.0, ls="-."))
    num(ax, -9.0, 25.94, "4", "#7048e8")
    num(ax, -9.0, 74.44, "4", "#7048e8")

    # --- option 5: rib along the foot, from a post out to the edge ---
    for y0, y1 in ((POSTS[0][0], FOOT[2]), (POSTS[1][1], FOOT[3])):
        ax.add_patch(Rectangle((0.0, min(y0, y1)), 5.0, abs(y1 - y0),
                               facecolor="#ffd8a8", edgecolor="#a05a00",
                               lw=1.4, alpha=0.85))
    num(ax, 2.5, 9.0, "5", "#a05a00")
    num(ax, 2.5, 91.0, "5", "#a05a00")

    # --- option 6: brace between the two posts, above the servo ---
    ax.add_patch(Rectangle((0.0, POSTS[0][1]), 5.0,
                           POSTS[1][0] - POSTS[0][1], fill=False,
                           edgecolor="#f08c00", lw=2.0, ls=":"))
    num(ax, 2.5, 50.2, "6", "#f08c00")

    # axis hints
    ax.annotate("", xy=(48, 100), xytext=(40, 100),
                arrowprops=dict(arrowstyle="->", color="#343a40", lw=1.6))
    ax.text(50, 100, "X", fontsize=12, va="center", fontweight="bold")
    ax.annotate("", xy=(44, 106), xytext=(44, 100),
                arrowprops=dict(arrowstyle="->", color="#343a40", lw=1.6))
    ax.text(44, 108, "Y", fontsize=12, ha="center", fontweight="bold")

    ax.set_xlim(-22, 56)
    ax.set_ylim(-6, 112)

    legend = [
        ("1", "#1864ab", "立柱外侧（M/N）三角筋 —— 现在这个"),
        ("2", "#c92a2a", "立柱内侧（K/L）方块 —— 需舵机让位才有空间"),
        ("3", "#2b8a3e", "立柱背面（+X）三角筋"),
        ("4", "#7048e8", "立柱根部一圈围裙（四周加宽台）"),
        ("5", "#a05a00", "沿 Y 的竖筋：从立柱一直做到底脚边沿"),
        ("6", "#f08c00", "两根立柱之间加横撑（舵机上方）"),
    ]
    for i, (k, col, text) in enumerate(legend):
        y = -0.02 - i * 0.028
        fig.text(0.08, y, k, fontsize=12, color="white", fontweight="bold",
                 ha="center", va="center",
                 bbox=dict(boxstyle="circle,pad=0.22", fc=col, ec="white"))
        fig.text(0.11, y, text, fontsize=11, va="center")

    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_options.png")
