r"""Labelled isometric drawing of g_mount_b v3, with an XYZ triad.

Everything in the part is a box, so a small hand-rolled isometric renderer gives
a cleaner, fully labelled picture than a shaded STEP snapshot.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

K = 0.8660254          # cos 30
H = 0.5                # sin 30


def proj(x, y, z):
    """Isometric projection, viewed from (+X, -Y, +Z)."""
    return ((x - y) * K, (x + y) * H * 0.0 + z + (x * 0.0) + (y * 0.0) + 0.0
            + (x * 0.0))


def iso(x, y, z):
    # u grows to the upper-right with +X, to the upper-left with +Y
    u = (x - y) * K
    v = (x + y) * H * 0.0 + z - (x + y) * 0.0
    v = z + (x + y) * 0.0
    # tilt the plan so we see it: compress Z and slant X,Y
    return (u, v)


def p(x, y, z):
    # standard isometric: +X to the lower-right, +Y to the lower-left, +Z up
    return ((x - y) * K, z - (x + y) * H)


C_TOP = "#d8e6f5"
C_RIGHT = "#b8cde3"
C_LEFT = "#9fb8d1"
C_EDGE = "#2b3a4a"

PARTS = [
    # name, x0, x1, y0, y1, z0, z1, colour-ish
    ("齿板（参考）", 0.0, 60.0, 0.0, 24.44, 0.0, 9.0, "plate"),
    ("① 底脚", -30.0, 30.0, -20.0, 24.44, 9.0, 14.0, "part"),
    ("② 竖脚", -30.0, -25.0, -20.0, 24.44, 14.0, 34.0, "part"),
    ("③ 横臂", -30.0, 30.0, -20.0, 24.44, 34.0, 39.0, "part"),
    ("④ 前立柱", -30.0, -25.0, -17.03, -7.03, 39.0, 65.0, "part"),
    ("⑤ 后立柱", -30.0, -25.0, 31.47, 41.47, 39.0, 65.0, "part"),
    ("⑥ 顶梁", -30.0, -25.0, -17.03, 41.47, 63.0, 65.0, "part"),
    ("舵机（参考）", -40.0, 0.0, -7.78, 32.22, 39.0, 59.0, "servo"),
]

COLOURS = {
    "plate": ("#d3f9d8", "#a9e3b8", "#8ccfa0", "#2f9e44"),
    "part": ("#eef3fa", "#d5e2f0", "#b9cde3", "#2b3a4a"),
    "servo": ("#f1f3f5", "#dee2e6", "#ced4da", "#495057"),
}


def draw_box(ax, x0, x1, y0, y1, z0, z1, kind, alpha=1.0):
    top, right, left, edge = COLOURS[kind]
    # +Z face
    ax.add_patch(Polygon([p(x0, y0, z1), p(x1, y0, z1),
                          p(x1, y1, z1), p(x0, y1, z1)],
                         facecolor=top, edgecolor=edge, lw=1.1, alpha=alpha,
                         zorder=2))
    # +X face
    ax.add_patch(Polygon([p(x1, y0, z0), p(x1, y1, z0),
                          p(x1, y1, z1), p(x1, y0, z1)],
                         facecolor=right, edgecolor=edge, lw=1.1, alpha=alpha,
                         zorder=3))
    # -Y face
    ax.add_patch(Polygon([p(x0, y0, z0), p(x1, y0, z0),
                          p(x1, y0, z1), p(x0, y0, z1)],
                         facecolor=left, edgecolor=edge, lw=1.1, alpha=alpha,
                         zorder=4))


def main(out):
    fig, ax = plt.subplots(figsize=(14.5, 11.0), dpi=115)
    ax.set_aspect("equal")
    ax.axis("off")

    # draw from back to front so overlaps look right
    order = [7, 5, 4, 6, 1, 2, 3, 0]
    for i in order:
        name, x0, x1, y0, y1, z0, z1, kind = PARTS[i]
        draw_box(ax, x0, x1, y0, y1, z0, z1, kind,
                 alpha=0.92 if kind == "part" else 0.55)

    # XYZ triad at the plate's near corner
    ox, oy, oz = 0.0, 0.0, 0.0
    L = 34.0
    for vec, label, col in (((L, 0, 0), "X  （齿板长边）", "#c92a2a"),
                            ((0, L, 0), "Y  （齿板宽度）", "#2b8a3e"),
                            ((0, 0, L), "Z  （向上）", "#1864ab")):
        ax.annotate("", xy=p(ox + vec[0], oy + vec[1], oz + vec[2]),
                    xytext=p(ox, oy, oz),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4,
                                    mutation_scale=18), zorder=9)
        tx, ty = p(ox + vec[0] * 1.18, oy + vec[1] * 1.18, oz + vec[2] * 1.18)
        ax.text(tx, ty, label, fontsize=11, color=col, ha="center",
                va="center", zorder=9, fontweight="bold")
    ax.plot(*p(ox, oy, oz), marker="o", ms=5, color="#343a40", zorder=9)

    # part labels
    labels = [
        ("齿板（参考）9 厚", p(50, 12, 4.5), (112, -70)),
        ("① 底脚  4×Ø4.5", p(22, 22, 11.5), (106, -34)),
        ("② 竖脚", p(-27.5, 20, 24), (-124, -30)),
        ("③ 横臂  Z 34~39", p(18, -18, 36.5), (118, 34)),
        ("④ 前立柱（开口槽）", p(-27.5, -12, 58), (-128, 92)),
        ("⑤ 后立柱（开口槽）", p(-27.5, 36.5, 58), (44, 112)),
        ("⑥ 顶梁", p(-27.5, 10, 64.5), (-36, 118)),
        ("舵机（参考，轴朝外）", p(-38, 12, 49), (-130, 40)),
    ]
    for text, xy, xytext in labels:
        ax.annotate(text, xy=xy, xytext=xytext, fontsize=10.5,
                    color="#212529",
                    arrowprops=dict(arrowstyle="-", color="#868e96", lw=1.0,
                                    shrinkA=2, shrinkB=3),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              ec="#dee2e6", lw=0.8, alpha=0.92), zorder=10)

    # dimension callouts
    ax.annotate("", xy=p(-30, -26, 9), xytext=p(-30, -26, 34),
                arrowprops=dict(arrowstyle="<->", color="#a05a00", lw=1.3),
                zorder=9)
    ax.text(*p(-30, -30, 21.5), "25", fontsize=12, color="#a05a00",
            ha="center", fontweight="bold", zorder=9)

    ax.set_xlim(-150, 155)
    ax.set_ylim(-92, 132)
    ax.set_title("g_mount_b 第三版：各部件名称与坐标轴", fontsize=16,
                 fontweight="bold", pad=18)
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_iso.png")
