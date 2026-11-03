r"""Dimensioned three-view drawing of g_mount_b rev 13.

Plain orthographic views with dimension lines only: no shading, no callouts,
so every number is readable. Units mm.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# --- geometry ---
FOOT = (0.0, 40.0, 13.94, 82.44, 9.0, 14.0)
POSTS = [(21.94, 29.94), (70.44, 78.44)]
POST_X = (0.0, 5.0)
POST_Z = (14.0, 40.0)
BRIDGE_Z = (38.0, 40.0)
HOLES_X = [8.0, 16.196, 24.392, 32.588]
HOLE_Y = 19.94
PLATE_HOLE_D = 4.5
SCREWS = [(25.94, 19.0), (25.94, 29.0), (74.44, 19.0), (74.44, 29.0)]
SCREW_D = 4.5
POCKET_X = (3.4, 5.0)
POCKET_Z = (23.0, 25.0)
RIBS = [(17.94, 22.44), (77.94, 82.44)]
RIB_LEG = 11.0

EDGE = "#1b3b5a"
FILL = "#e8f1fb"
DIM = "#495057"


def dim_h(ax, x0, x1, y, label, above=True):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9,
                                shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (1.6 if above else -1.6), label, fontsize=9.5,
            ha="center", va="bottom" if above else "top", color=DIM)


def dim_v(ax, y0, y1, x, label, left=True):
    ax.annotate("", xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9,
                                shrinkA=0, shrinkB=0))
    ax.text(x - (1.6 if left else -1.6), (y0 + y1) / 2, label, fontsize=9.5,
            rotation=90, ha="right" if left else "left", va="center", color=DIM)


def view_top(ax):
    ax.set_title("俯视（X-Y）", fontsize=13, fontweight="bold", pad=12)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((FOOT[0], FOOT[2]), FOOT[1] - FOOT[0],
                           FOOT[3] - FOOT[2], facecolor=FILL, edgecolor=EDGE,
                           lw=1.6))
    # posts (hidden under bridge, drawn solid)
    for y0, y1 in POSTS:
        ax.add_patch(Rectangle((POST_X[0], y0), POST_X[1] - POST_X[0],
                               y1 - y0, facecolor="#cfe0f2", edgecolor=EDGE,
                               lw=1.2))
    # bridge outline (on top of posts)
    ax.add_patch(Rectangle((POST_X[0], POSTS[0][0]), POST_X[1] - POST_X[0],
                           POSTS[1][1] - POSTS[0][0], fill=False,
                           edgecolor="#7b9cc0", lw=1.0, ls="--"))
    # ribs
    for y0, y1 in RIBS:
        ax.add_patch(Rectangle((0.0, y0), RIB_LEG, y1 - y0,
                               facecolor="#d7e6f6", edgecolor="#7b9cc0",
                               lw=0.9, ls=":"))
    # plate holes
    for hx in HOLES_X:
        ax.add_patch(Circle((hx, HOLE_Y), PLATE_HOLE_D / 2, facecolor="white",
                            edgecolor=EDGE, lw=1.1))
    # screw holes seen end-on
    for yc, zc in SCREWS:
        pass

    dim_h(ax, FOOT[0], FOOT[1], FOOT[3] + 5.5, "40")
    dim_v(ax, FOOT[2], FOOT[3], FOOT[0] - 5.5, "68.5")
    dim_h(ax, HOLES_X[0], HOLES_X[-1], FOOT[2] - 5.0, "24.6")
    dim_h(ax, FOOT[0], HOLES_X[0], FOOT[2] - 10.0, "8")
    dim_v(ax, FOOT[2], HOLE_Y, 44.0, "6", left=False)
    dim_h(ax, POSTS[0][0], POSTS[1][1], 88.0, "52.5")
    ax.set_xlim(-20, 52)
    ax.set_ylim(0, 96)
    ax.text(20, 92.5, "4×Ø4.5 齿板孔", fontsize=9, color="#2f9e44",
            ha="center")


def view_front(ax):
    ax.set_title("正视图（Y-Z，沿 +X 看）", fontsize=13, fontweight="bold",
                 pad=12)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((FOOT[2], FOOT[4]), FOOT[3] - FOOT[2],
                           FOOT[5] - FOOT[4], facecolor=FILL, edgecolor=EDGE,
                           lw=1.6))
    for y0, y1 in POSTS:
        ax.add_patch(Rectangle((y0, POST_Z[0]), y1 - y0,
                               POST_Z[1] - POST_Z[0], facecolor="#cfe0f2",
                               edgecolor=EDGE, lw=1.2))
    ax.add_patch(Rectangle((POSTS[0][0], BRIDGE_Z[0]),
                           POSTS[1][1] - POSTS[0][0],
                           BRIDGE_Z[1] - BRIDGE_Z[0], facecolor="#cfe0f2",
                           edgecolor=EDGE, lw=1.2))
    for yc, zc in SCREWS:
        ax.add_patch(Circle((yc, zc), SCREW_D / 2, facecolor="white",
                            edgecolor=EDGE, lw=1.2))
    # ribs silhouette
    for y0, y1 in RIBS:
        ax.add_patch(Rectangle((y0, FOOT[5]), y1 - y0, RIB_LEG,
                               facecolor="none", edgecolor="#7b9cc0", lw=0.8,
                               ls=":"))

    dim_h(ax, POSTS[0][0], POSTS[0][1], 44.5, "8")
    dim_h(ax, POSTS[0][0], POSTS[1][0], 50.5, "48.5")
    dim_v(ax, FOOT[4], POST_Z[1], 12.0, "31")
    dim_v(ax, SCREWS[0][1], SCREWS[1][1], 34.0, "10", left=False)
    dim_h(ax, FOOT[2], FOOT[3], 4.0, "68.5", above=False)
    ax.set_xlim(0, 92)
    ax.set_ylim(-2, 56)
    ax.text(52, 53, "4×Ø4.5 通孔", fontsize=9, color="#c92a2a", ha="center")


def view_side(ax):
    ax.set_title("侧视（X-Z，沿 −Y 看）", fontsize=13, fontweight="bold",
                 pad=12)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((FOOT[0], FOOT[4]), FOOT[1] - FOOT[0],
                           FOOT[5] - FOOT[4], facecolor=FILL, edgecolor=EDGE,
                           lw=1.6))
    ax.add_patch(Rectangle((POST_X[0], POST_Z[0]), POST_X[1] - POST_X[0],
                           POST_Z[1] - POST_Z[0], facecolor="#cfe0f2",
                           edgecolor=EDGE, lw=1.2))
    ax.add_patch(Rectangle((POST_X[0], BRIDGE_Z[0]), POST_X[1] - POST_X[0],
                           BRIDGE_Z[1] - BRIDGE_Z[0], facecolor="#cfe0f2",
                           edgecolor=EDGE, lw=1.2))
    # rib
    ax.add_patch(Polygon([(POST_X[1], FOOT[5]), (POST_X[1] + RIB_LEG, FOOT[5]),
                          (POST_X[1], FOOT[5] + RIB_LEG)],
                         facecolor="#d7e6f6", edgecolor="#7b9cc0", lw=1.0))
    # pocket notch on the inner face
    ax.add_patch(Rectangle((POCKET_X[0], POCKET_Z[0]),
                           POCKET_X[1] - POCKET_X[0],
                           POCKET_Z[1] - POCKET_Z[0], facecolor="white",
                           edgecolor=EDGE, lw=1.0))

    dim_h(ax, FOOT[0], FOOT[1], 4.0, "40", above=False)
    dim_v(ax, FOOT[4], POST_Z[1], -6.0, "31")
    dim_v(ax, FOOT[4], FOOT[5], 46.0, "5", left=False)
    dim_v(ax, POST_X[0], POST_X[1], 46.0, "5", left=False)
    ax.set_xlim(-16, 52)
    ax.set_ylim(-2, 46)
    ax.text(20, 43, "槽 2.4 宽 × 1.6 深", fontsize=9, color="#c92a2a",
            ha="center")


def main(out):
    fig = plt.figure(figsize=(15.0, 11.0), dpi=115, facecolor="white")
    view_top(fig.add_axes([0.03, 0.50, 0.44, 0.44]))
    view_front(fig.add_axes([0.52, 0.50, 0.45, 0.44]))
    view_side(fig.add_axes([0.03, 0.03, 0.34, 0.40]))
    fig.suptitle("g_mount_b  第13版  尺寸图（单位 mm）", fontsize=17,
                 fontweight="bold")
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_dims.png")
