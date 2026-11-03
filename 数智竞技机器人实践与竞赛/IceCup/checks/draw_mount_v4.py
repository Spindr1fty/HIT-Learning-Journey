r"""Labelled isometric picture of the simplified mount (v4).

No STEP, no 3D kernel: every part is a box, drawn in isometric with an XYZ
triad and part names. This is the sheet to review, not a printable model.

Structure (user's description):
  - foot plate: SHORT in X (just the four holes + margin), EXTENDED in Y
  - no riser, no cross arm
  - front post, rear post and top bridge stand directly on the foot, placed in
    Y around the foot's screw-hole row so the servo hangs between them
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

K = 0.8660254
H = 0.5


def p(x, y, z):
    return ((x - y) * K, z - (x + y) * H)


C = {
    "plate": ("#d3f9d8", "#a9e3b8", "#8ccfa0", "#2f9e44"),
    "part": ("#eef3fa", "#d5e2f0", "#b9cde3", "#2b3a4a"),
    "servo": ("#fff3bf", "#ffe8a3", "#f2d98a", "#a05a00"),
}

# --- geometry (all mm) -------------------------------------------------------
PLATE = (0.0, 60.0, 0.0, 24.44, 0.0, 9.0)

FOOT = (0.0, 40.0, -20.0, 52.0, 9.0, 14.0)
HOLE_X = [8.0, 16.196, 24.392, 32.588]
HOLE_Y = 19.94
HOLE_D = 4.5

POST_X = (0.0, 5.0)
POST_Y = ((-10.56, -0.56), (40.44, 50.44))     # outer/inner, clear of the body
POST_Z = (14.0, 40.0)
BRIDGE_Z = (38.0, 40.0)

SERVO_BODY = (-10.0, 30.0, -0.06, 39.94, 14.0, 34.0)
FLANGE_X = 0.0
FLANGE_HOLES = [(-4.31, 19.0), (-4.31, 29.0), (44.19, 19.0), (44.19, 29.0)]


def draw_box(ax, box, kind, lw=1.1, alpha=1.0):
    x0, x1, y0, y1, z0, z1 = box
    top, right, left, edge = C[kind]
    ax.add_patch(Polygon([p(x0, y0, z1), p(x1, y0, z1),
                          p(x1, y1, z1), p(x0, y1, z1)],
                         facecolor=top, edgecolor=edge, lw=lw, alpha=alpha,
                         zorder=2))
    ax.add_patch(Polygon([p(x1, y0, z0), p(x1, y1, z0),
                          p(x1, y1, z1), p(x1, y0, z1)],
                         facecolor=right, edgecolor=edge, lw=lw, alpha=alpha,
                         zorder=3))
    ax.add_patch(Polygon([p(x0, y0, z0), p(x1, y0, z0),
                          p(x1, y0, z1), p(x0, y0, z1)],
                         facecolor=left, edgecolor=edge, lw=lw, alpha=alpha,
                         zorder=4))


def main(out):
    fig = plt.figure(figsize=(15.5, 11.5), dpi=115, facecolor="white")
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.92])
    ax.set_aspect("equal")
    ax.axis("off")

    draw_box(ax, PLATE, "plate", alpha=0.75)
    draw_box(ax, FOOT, "part")
    for y0, y1 in POST_Y:
        draw_box(ax, (POST_X[0], POST_X[1], y0, y1, POST_Z[0], POST_Z[1]), "part")
    draw_box(ax, (POST_X[0], POST_X[1], POST_Y[0][0], POST_Y[1][1],
                  BRIDGE_Z[0], BRIDGE_Z[1]), "part")
    draw_box(ax, SERVO_BODY, "servo", alpha=0.55)

    # plate fixing holes
    for hx in HOLE_X:
        ax.add_patch(Circle(p(hx, HOLE_Y, 14.0), 2.6, facecolor="white",
                            edgecolor="#2b3a4a", lw=1.0, zorder=6))
    # flange slots on the posts' face
    for hy, hz in FLANGE_HOLES:
        ax.add_patch(Circle(p(FLANGE_X, hy, hz), 2.6, facecolor="white",
                            edgecolor="#a05a00", lw=1.0, zorder=6))

    # XYZ triad at the plate's near corner
    L = 30.0
    for vec, label, col in (((L, 0, 0), "X 齿板长边", "#c92a2a"),
                            ((0, L, 0), "Y 齿板宽", "#2b8a3e"),
                            ((0, 0, L), "Z 向上", "#1864ab")):
        ax.annotate("", xy=p(*vec), xytext=p(0, 0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6,
                                    mutation_scale=20), zorder=12)
        tx, ty = p(vec[0] * 1.22, vec[1] * 1.22, vec[2] * 1.22)
        ax.text(tx, ty, label, fontsize=12, color=col, fontweight="bold",
                ha="center", va="center", zorder=12)
    ax.plot(*p(0, 0, 0), marker="o", ms=6, color="#212529", zorder=12)

    labels = [
        ("齿板（参考）9 厚", p(52, 12, 4.5), (74, -54)),
        ("① 底脚  4×Ø4.5\nX 只留孔长，Y 拉长", p(30, 44, 11.5), (78, -8)),
        ("② 前立柱", p(2.5, -10, 30), (-70, -42)),
        ("③ 后立柱", p(2.5, 45, 30), (-62, 26)),
        ("④ 顶梁", p(2.5, 20, 39), (-22, 62)),
        ("舵机（参考）", p(-9, 20, 24), (-72, 2)),
        ("⑤ 法兰开口槽 ×4", p(0, 44.19, 29), (44, 54)),
    ]
    for text, xy, xytext in labels:
        ax.annotate(text, xy=xy, xytext=xytext, fontsize=11,
                    arrowprops=dict(arrowstyle="-", color="#868e96", lw=1.0,
                                    shrinkA=2, shrinkB=4),
                    bbox=dict(boxstyle="round,pad=0.3", fc="white",
                              ec="#dee2e6", lw=0.8, alpha=0.95), zorder=11)

    ax.set_xlim(-165, 175)
    ax.set_ylim(-105, 130)
    ax.set_title("g_mount_b 第四版（只给图）：底脚 + 两根立柱 + 顶梁",
                 fontsize=17, fontweight="bold", pad=16)
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_v4.png")
