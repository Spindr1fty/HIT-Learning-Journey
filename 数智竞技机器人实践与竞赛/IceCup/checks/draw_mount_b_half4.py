r"""Half-skirt detail: a widened plinth on the -X half of each post root,
with counterbore reliefs so the M4 heads can still seat.

Four small views + notes, so the user can say yes or point at what to change.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

EDGE = "#1b3b5a"
FILL = "#eef4fb"
FILL2 = "#cfe0f2"
PLINTH = "#d0bfff"
RELIEF = "#ffd8a8"

# post: X 0..5, Y 21.94..29.94 (front post); plinth extends -X to -6
POST = (0.0, 5.0, 21.94, 29.94)
PLINTH_X = (-6.0, 5.0)
PLINTH_Z = (14.0, 22.0)
HOLES = [(25.94, 19.0), (25.94, 29.0)]
HEAD_D = 8.5


def front(ax):
    ax.set_title("正视图（Y-Z，看立柱前面）", fontsize=12, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((POST[2], POST[2] * 0), POST[3] - POST[2], 26.0,
                           facecolor=FILL2, edgecolor=EDGE, lw=1.4))
    # plinth outline (wider than post)
    ax.add_patch(Rectangle((POST[2] - 6.0, 0.0), POST[3] - POST[2] + 12.0,
                           8.0, facecolor=PLINTH, edgecolor=EDGE, lw=1.3,
                           alpha=0.85))
    for yc, zc in HOLES:
        ax.add_patch(Circle((yc, zc - 14.0), HEAD_D / 2, facecolor=RELIEF,
                            edgecolor=EDGE, lw=1.1, ls="--"))
    ax.text(25.94, 20.5, "沉孔让位 Ø8.5", fontsize=8.5, ha="center",
            color="#a05a00")
    ax.set_xlim(10, 42)
    ax.set_ylim(-2, 28)
    ax.text(26, -1.0, "宽 = 立柱 8 + 两侧各 6", fontsize=9, ha="center",
            color="#495057")


def side(ax):
    ax.set_title("侧视（X-Z）", fontsize=12, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0.0, 0.0), 5.0, 26.0, facecolor=FILL2,
                           edgecolor=EDGE, lw=1.4))
    # plinth: extends -X, 8 tall, with a step
    ax.add_patch(Rectangle((-6.0, 0.0), 11.0, 8.0, facecolor=PLINTH,
                           edgecolor=EDGE, lw=1.3, alpha=0.85))
    ax.add_patch(Rectangle((-6.0, 8.0), 2.0, 3.0, facecolor=PLINTH,
                           edgecolor=EDGE, lw=1.1, alpha=0.7, ls=":"))
    for yc, zc in (HOLES[0], HOLES[1]):
        ax.add_patch(plt.Rectangle((0.0, zc - HEAD_D / 2), HEAD_D * 0 + 5.0,
                                   HEAD_D, fill=False, ec="#c92a2a", lw=1.0))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-2, 28)
    ax.text(-3, -1.0, "台 6 长 × 8 高", fontsize=9, ha="center",
            color="#495057")


def top(ax):
    ax.set_title("俯视（X-Y）", fontsize=12, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((POST[0], POST[2]), POST[1] - POST[0],
                           POST[3] - POST[2], facecolor=FILL2, edgecolor=EDGE,
                           lw=1.4))
    ax.add_patch(Rectangle((PLINTH_X[0], POST[2] - 6.0),
                           PLINTH_X[1] - PLINTH_X[0],
                           (POST[3] - POST[2]) + 12.0, facecolor=PLINTH,
                           edgecolor=EDGE, lw=1.3, alpha=0.55))
    for yc, zc in HOLES:
        ax.add_patch(Circle((1.0, yc), HEAD_D / 2, facecolor=RELIEF,
                            edgecolor=EDGE, lw=1.0, ls="--"))
    ax.annotate("−X 只有这一半加宽", xy=(-3.0, 25.94), xytext=(-9.0, 34.0),
                fontsize=9, color="#7048e8",
                arrowprops=dict(arrowstyle="->", color="#7048e8", lw=1.1))
    ax.annotate("+X 那一半不动（舵机会撞）", xy=(6.0, 25.94),
                xytext=(9.0, 34.0), fontsize=9, color="#c92a2a",
                arrowprops=dict(arrowstyle="->", color="#c92a2a", lw=1.1))
    ax.set_xlim(-14, 22)
    ax.set_ylim(12, 44)


def iso(ax):
    ax.set_title("立体示意", fontsize=12, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    # crude axonometric of the plinth + post
    K, H = 0.866, 0.5
    def p(x, y, z):
        return ((x - y) * K, z - (x + y) * H)
    # foot slab
    ax.add_patch(plt.Polygon([p(-10, 15, 0), p(10, 15, 0), p(10, 38, 0),
                              p(-10, 38, 0)], facecolor=FILL, edgecolor=EDGE,
                             lw=1.2))
    # plinth
    ax.add_patch(plt.Polygon([p(PLINTH_X[0], POST[2] - 6, PLINTH_Z[1]),
                              p(PLINTH_X[1], POST[2] - 6, PLINTH_Z[1]),
                              p(PLINTH_X[1], POST[3] + 6, PLINTH_Z[1]),
                              p(PLINTH_X[0], POST[3] + 6, PLINTH_Z[1])],
                             facecolor=PLINTH, edgecolor=EDGE, lw=1.3,
                             alpha=0.9))
    # post
    ax.add_patch(plt.Polygon([p(0, POST[2], 26), p(5, POST[2], 26),
                              p(5, POST[3], 26), p(0, POST[3], 26)],
                             facecolor=FILL2, edgecolor=EDGE, lw=1.3))
    ax.add_patch(plt.Polygon([p(0, POST[2], 0), p(5, POST[2], 0),
                              p(5, POST[2], 26), p(0, POST[2], 26)],
                             facecolor="#b8cde3", edgecolor=EDGE, lw=1.2))
    ax.set_xlim(-30, 26)
    ax.set_ylim(-24, 34)


def main(out):
    fig = plt.figure(figsize=(15.0, 9.5), dpi=115, facecolor="white")
    front(fig.add_axes([0.04, 0.10, 0.26, 0.72]))
    side(fig.add_axes([0.34, 0.10, 0.22, 0.72]))
    top(fig.add_axes([0.58, 0.10, 0.20, 0.72]))
    iso(fig.add_axes([0.79, 0.10, 0.19, 0.72]))

    fig.suptitle("方案 4 的一半：立柱根部 −X 半边加宽台（带螺栓让位沉孔）",
                 fontsize=16, fontweight="bold")

    lines = [
        "· 只在立柱 −X 那半边加宽：从立柱前面往 −X 伸 6，两侧各宽出 6",
        "· 台高 8（Z 14~22），上面从台顶斜收到立柱（可做倒角）",
        "· 两个 M4 螺栓头位置挖 Ø8.5 沉孔，螺母仍在柱子后面",
        "· 完全不碰齿板孔（齿板孔从 X=5.75 开始）",
        "· 后立柱做镜像",
    ]
    for i, s in enumerate(lines):
        fig.text(0.06, 0.045 - i * 0.030, s, fontsize=10.5)

    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_half4.png")
