r"""Face-labelling sheet for g_mount_b: letters on every face so the user can
point at one instead of describing it.

Views: side (X-Z), front (Y-Z), top (X-Y). Letters are placed on the faces.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FOOT = (0.0, 40.0, 3.94, 96.44, 9.0, 14.0)
POSTS = [(21.94, 29.94), (70.44, 78.44)]
POST_X = (0.0, 5.0)
POST_Z = (14.0, 40.0)
BRIDGE_Z = (38.0, 40.0)
HOLES_X = [8.0, 16.196, 24.392, 32.588]
HOLE_Y = 19.94
SCREWS = [(25.94, 19.0), (25.94, 29.0), (74.44, 19.0), (74.44, 29.0)]
BLOCKS = [(3.94, 21.94), (78.44, 96.44)]
BLOCK_H = 8.5

EDGE = "#1b3b5a"
FILL = "#eaf2fb"
FILL2 = "#cfe0f2"
FILL3 = "#dbe9f7"
LBL = "#c92a2a"


def tag(ax, x, y, text, size=13):
    ax.text(x, y, text, fontsize=size, fontweight="bold", color=LBL,
            ha="center", va="center",
            bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=LBL, lw=1.2),
            zorder=10)


def side(ax):
    ax.set_title("侧视（X-Z，沿 −Y 看）", fontsize=13, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    # foot
    ax.add_patch(Rectangle((FOOT[0], FOOT[4]), FOOT[1] - FOOT[0],
                           FOOT[5] - FOOT[4], facecolor=FILL, edgecolor=EDGE,
                           lw=1.6))
    # post
    ax.add_patch(Rectangle((POST_X[0], POST_Z[0]), POST_X[1] - POST_X[0],
                           POST_Z[1] - POST_Z[0], facecolor=FILL2,
                           edgecolor=EDGE, lw=1.4))
    # bridge
    ax.add_patch(Rectangle((POST_X[0], BRIDGE_Z[0]), POST_X[1] - POST_X[0],
                           BRIDGE_Z[1] - BRIDGE_Z[0], facecolor=FILL2,
                           edgecolor=EDGE, lw=1.4))
    # buttress block
    for y0, y1 in BLOCKS:
        pass
    ax.add_patch(Rectangle((-18.0, FOOT[5]), 18.0, BLOCK_H, facecolor=FILL3,
                           edgecolor=EDGE, lw=1.2, ls="--"))

    tag(ax, 20, 11.5, "D")          # foot front face (-Y)
    tag(ax, 20, (FOOT[4] + FOOT[5]) / 2, "E")   # foot front? keep simple
    tag(ax, 2.5, 27, "F")           # post front face (-X)
    tag(ax, 2.5, 39, "I")           # bridge top
    tag(ax, 2.5, 15.5, "G")         # post base
    ax.text(-9, FOOT[5] + BLOCK_H / 2, "方块", fontsize=9, ha="center",
            color="#495057")

    ax.set_xlim(-24, 46)
    ax.set_ylim(6, 44)


def front(ax):
    ax.set_title("正视图（Y-Z，沿 +X 看）", fontsize=13, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((FOOT[2], FOOT[4]), FOOT[3] - FOOT[2],
                           FOOT[5] - FOOT[4], facecolor=FILL, edgecolor=EDGE,
                           lw=1.6))
    for y0, y1 in POSTS:
        ax.add_patch(Rectangle((y0, POST_Z[0]), y1 - y0,
                               POST_Z[1] - POST_Z[0], facecolor=FILL2,
                               edgecolor=EDGE, lw=1.4))
    ax.add_patch(Rectangle((POSTS[0][0], BRIDGE_Z[0]),
                           POSTS[1][1] - POSTS[0][0],
                           BRIDGE_Z[1] - BRIDGE_Z[0], facecolor=FILL2,
                           edgecolor=EDGE, lw=1.4))
    for yc, zc in SCREWS:
        ax.add_patch(plt.Circle((yc, zc), 2.25, facecolor="white",
                                edgecolor=EDGE, lw=1.1))
    for y0, y1 in BLOCKS:
        ax.add_patch(Rectangle((y0, FOOT[5]), y1 - y0, BLOCK_H,
                               facecolor=FILL3, edgecolor=EDGE, lw=1.2,
                               ls="--"))

    tag(ax, 50, 11.5, "D")
    tag(ax, 25.94, 33, "K")     # inside of the front post (facing servo)
    tag(ax, 74.44, 33, "L")
    tag(ax, 12, 18, "M")        # foot region in front of the posts
    tag(ax, 88, 18, "N")        # foot region behind
    tag(ax, 50, 39, "I2")

    ax.set_xlim(0, 100)
    ax.set_ylim(6, 46)


def top(ax):
    ax.set_title("俯视（X-Y）", fontsize=13, fontweight="bold")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((FOOT[0], FOOT[2]), FOOT[1] - FOOT[0],
                           FOOT[3] - FOOT[2], facecolor=FILL, edgecolor=EDGE,
                           lw=1.6))
    for y0, y1 in POSTS:
        ax.add_patch(Rectangle((POST_X[0], y0), POST_X[1] - POST_X[0],
                               y1 - y0, facecolor=FILL2, edgecolor=EDGE,
                               lw=1.3))
    ax.add_patch(Rectangle((POST_X[0], POSTS[0][0]), POST_X[1] - POST_X[0],
                           POSTS[1][1] - POSTS[0][0], fill=False,
                           edgecolor="#7b9cc0", lw=1.0, ls="--"))
    for y0, y1 in BLOCKS:
        ax.add_patch(Rectangle((POST_X[0], y0), 5.0, y1 - y0,
                               facecolor=FILL3, edgecolor=EDGE, lw=1.2,
                               ls="--"))
    for hx in HOLES_X:
        ax.add_patch(plt.Circle((hx, HOLE_Y), 2.25, facecolor="white",
                                edgecolor=EDGE, lw=1.1))

    tag(ax, 20, 50, "A")        # foot top face
    tag(ax, 20, 6.5, "B")       # foot front edge
    tag(ax, 20, 93, "C")        # foot rear edge
    tag(ax, 2.5, 25.94, "E2")   # post front face (X=0)
    tag(ax, 8, 25.94, "F2")     # post rear face (X=5)
    tag(ax, 2.5, 12, "P")       # buttress block front
    tag(ax, 2.5, 87, "Q")       # buttress block rear

    ax.set_xlim(-8, 48)
    ax.set_ylim(0, 100)


def main(out):
    fig = plt.figure(figsize=(15.5, 11.0), dpi=115, facecolor="white")
    top(fig.add_axes([0.03, 0.50, 0.30, 0.46]))
    front(fig.add_axes([0.38, 0.50, 0.58, 0.46]))
    side(fig.add_axes([0.03, 0.04, 0.28, 0.40]))

    ax = fig.add_axes([0.36, 0.04, 0.61, 0.40])
    ax.axis("off")
    rows = [
        ("A", "底脚上表面（Z=14，舵机坐的位置）"),
        ("B", "底脚前边（−Y 那条边）"),
        ("C", "底脚后边（+Y 那条边）"),
        ("D", "底脚前后两个侧面（法线 ±Y 的立面）"),
        ("E2", "立柱前面（X=0，螺丝孔开口这一面）"),
        ("F2", "立柱后面（X=5，螺母这一面）"),
        ("G", "立柱根部（和底脚的交界）"),
        ("I / I2", "顶梁上面 / 下面"),
        ("K / L", "两立柱朝舵机的内侧 Y 面"),
        ("M / N", "底脚上、两柱之间那块面 / 柱外那块面"),
        ("P / Q", "现在两个方块所在的面"),
    ]
    ax.text(0, 1.0, "面编号", fontsize=13, fontweight="bold",
            transform=ax.transAxes)
    for i, (k, v) in enumerate(rows):
        y = 0.90 - i * 0.083
        ax.text(0.02, y, k, fontsize=10.5, transform=ax.transAxes,
                fontweight="bold", color=LBL)
        ax.text(0.09, y, v, fontsize=10, transform=ax.transAxes)

    fig.suptitle("g_mount_b 面的编号（告诉我字母即可）", fontsize=17,
                 fontweight="bold")
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_faces.png")
