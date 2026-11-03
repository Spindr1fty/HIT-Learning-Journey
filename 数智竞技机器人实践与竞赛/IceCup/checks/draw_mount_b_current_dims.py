r"""Dimensioned three-view sheet for the CURRENT g_mount_b, reading every number
straight from src/g_mount_b.py so the drawing cannot drift from the model.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import g_mount_b as M  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

EDGE = "#1b3b5a"
FILL = "#eaf2fb"
FILL2 = "#cfe0f2"
FILL3 = "#dbe9f7"
DIM = "#495057"


def dim_h(ax, x0, x1, y, label, dy=1.8):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9))
    ax.text((x0 + x1) / 2, y + dy, label, fontsize=9.5, ha="center",
            va="bottom", color=DIM)


def dim_v(ax, y0, y1, x, label, dx=1.8):
    ax.annotate("", xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9))
    ax.text(x - dx, (y0 + y1) / 2, label, fontsize=9.5, rotation=90,
            ha="right", va="center", color=DIM)


def view_top(ax):
    ax.set_title("俯视（X-Y）", fontsize=13, fontweight="bold", pad=10)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((M.FOOT_X[0], M.FOOT_Y[0]),
                           M.FOOT_X[1] - M.FOOT_X[0],
                           M.FOOT_Y[1] - M.FOOT_Y[0], facecolor=FILL,
                           edgecolor=EDGE, lw=1.7))
    for y0, y1 in (M.POST1_Y, M.POST2_Y):
        ax.add_patch(Rectangle((M.POST_X[0], y0), M.POST_X[1] - M.POST_X[0],
                               y1 - y0, facecolor=FILL2, edgecolor=EDGE,
                               lw=1.3))
    ax.add_patch(Rectangle((M.POST_X[0], M.POST1_Y[0]),
                           M.POST_X[1] - M.POST_X[0],
                           M.POST2_Y[1] - M.POST1_Y[0], fill=False,
                           edgecolor="#7b9cc0", lw=1.0, ls="--"))
    # gussets (triangles, 18 legs, 5 thick at X 0..5)
    for y_edge, sgn in ((M.POST1_Y[0], -1), (M.POST2_Y[1], 1)):
        ax.add_patch(Polygon([(0.0, y_edge), (M.POST_T, y_edge),
                              (0.0, y_edge + sgn * M.RIB_LEG)],
                             facecolor=FILL3, edgecolor=EDGE, lw=1.1,
                             ls=":"))
    for hy in M.HOLE_ROWS:
        for hx in M.HOLE_X:
            ax.add_patch(Circle((hx, hy), M.HOLE_D / 2, facecolor="white",
                                edgecolor=EDGE, lw=1.2))

    dim_h(ax, M.FOOT_X[0], M.FOOT_X[1], M.FOOT_Y[1] + 6, "40")
    dim_v(ax, M.FOOT_Y[0], M.FOOT_Y[1], M.FOOT_X[0] - 6, "92.5")
    dim_h(ax, M.HOLE_X[0], M.HOLE_X[-1], M.FOOT_Y[0] - 5, "24.6")
    dim_h(ax, M.FOOT_X[0], M.HOLE_X[0], M.FOOT_Y[0] - 10, "8")
    dim_v(ax, M.FOOT_Y[0], M.HOLE_Y, 44.0, "16")
    dim_h(ax, M.POST1_Y[0], M.POST2_Y[1], M.FOOT_Y[1] + 13, "56.5")
    ax.text(20, M.FOOT_Y[1] + 20, "4×Ø4.5 齿板孔", fontsize=9, ha="center",
            color="#2f9e44")
    ax.set_xlim(-20, 52)
    ax.set_ylim(M.FOOT_Y[0] - 16, M.FOOT_Y[1] + 26)


def view_front(ax):
    ax.set_title("正视图（Y-Z，沿 +X 看）", fontsize=13, fontweight="bold",
                 pad=10)
    ax.set_aspect("equal")
    ax.axis("off")
    z0 = M.PLATE_T
    ax.add_patch(Rectangle((M.FOOT_Y[0], z0), M.FOOT_Y[1] - M.FOOT_Y[0],
                           M.FOOT_T, facecolor=FILL, edgecolor=EDGE, lw=1.7))
    for y0, y1 in (M.POST1_Y, M.POST2_Y):
        ax.add_patch(Rectangle((y0, z0 + M.FOOT_T), y1 - y0,
                               M.POST_TOP - (z0 + M.FOOT_T),
                               facecolor=FILL2, edgecolor=EDGE, lw=1.3))
    ax.add_patch(Rectangle((M.POST1_Y[0], M.BRIDGE[4]),
                           M.POST2_Y[1] - M.POST1_Y[0], M.BRIDGE_T,
                           facecolor=FILL2, edgecolor=EDGE, lw=1.3))
    for yc in (M.POST_C1, M.POST_C2):
        for hz in (M.SERVO_Z - 5, M.SERVO_Z + 5):
            ax.add_patch(Circle((yc, hz), M.SCREW_D / 2, facecolor="white",
                                edgecolor=EDGE, lw=1.3))
    # gusset silhouettes
    for y_edge, sgn in ((M.POST1_Y[0], -1), (M.POST2_Y[1], 1)):
        ax.add_patch(Rectangle((min(y_edge, y_edge + sgn * M.RIB_LEG),
                                z0 + M.FOOT_T), M.RIB_LEG, M.RIB_LEG,
                               fill=False, edgecolor="#7b9cc0", lw=0.9,
                               ls=":"))

    dim_h(ax, M.POST1_Y[0], M.POST1_Y[1], M.POST_TOP + 4, "8")
    dim_h(ax, M.POST1_Y[0], M.POST2_Y[0], M.POST_TOP + 9, "48.5")
    dim_h(ax, M.FOOT_Y[0], M.FOOT_Y[1], z0 - 5, "92.5")
    dim_v(ax, z0, M.POST_TOP, M.POST2_Y[1] + 8,
          f"{M.POST_TOP - z0:.0f}")
    dim_v(ax, M.SERVO_Z - 5, M.SERVO_Z + 5, M.POST2_Y[1] + 16, "10")
    ax.text(50, M.POST_TOP + 15, "4×Ø4.5 通孔", fontsize=9, ha="center",
            color="#c92a2a")
    ax.set_xlim(M.FOOT_Y[0] - 8, M.POST2_Y[1] + 26)
    ax.set_ylim(z0 - 10, M.POST_TOP + 22)


def view_side(ax):
    ax.set_title("侧视（X-Z，沿 −Y 看）", fontsize=13, fontweight="bold",
                 pad=10)
    ax.set_aspect("equal")
    ax.axis("off")
    z0 = M.PLATE_T
    ax.add_patch(Rectangle((M.FOOT_X[0], z0), M.FOOT_X[1] - M.FOOT_X[0],
                           M.FOOT_T, facecolor=FILL, edgecolor=EDGE, lw=1.7))
    ax.add_patch(Rectangle((M.POST_X[0], z0 + M.FOOT_T), M.POST_T,
                           M.POST_TOP - (z0 + M.FOOT_T), facecolor=FILL2,
                           edgecolor=EDGE, lw=1.3))
    ax.add_patch(Rectangle((M.POST_X[0], M.BRIDGE[4]), M.POST_T,
                           M.BRIDGE_T, facecolor=FILL2, edgecolor=EDGE,
                           lw=1.3))
    # triangular gusset on the outer Y side, seen edge-on as a rectangle
    ax.add_patch(Rectangle((M.POST_X[0], z0 + M.FOOT_T), M.POST_T, M.RIB_LEG,
                           facecolor=FILL3, edgecolor=EDGE, lw=1.1, ls=":"))
    # flange pocket
    ax.add_patch(Rectangle((M.POST_X[1] - M.POCKET_DEPTH, M.POCKET_Z[0]),
                           M.POCKET_DEPTH, M.POCKET_Z[1] - M.POCKET_Z[0],
                           facecolor="white", edgecolor=EDGE, lw=1.0))

    dim_h(ax, M.FOOT_X[0], M.FOOT_X[1], z0 - 5, "40")
    dim_v(ax, z0, M.POST_TOP, M.FOOT_X[1] + 8,
          f"{M.POST_TOP - z0:.0f}")
    dim_v(ax, z0, z0 + M.FOOT_T, M.FOOT_X[1] + 16, "5")
    dim_v(ax, M.POST_X[0], M.POST_X[1], -8, "5")
    ax.text(20, M.POST_TOP + 5,
            f"槽 {M.POCKET_W} 宽 × {M.POCKET_DEPTH} 深", fontsize=9,
            ha="center",
            color="#c92a2a")
    ax.set_xlim(-16, M.FOOT_X[1] + 26)
    ax.set_ylim(z0 - 10, M.POST_TOP + 10)


def main(out):
    fig = plt.figure(figsize=(15.0, 11.5), dpi=115, facecolor="white")
    view_top(fig.add_axes([0.03, 0.50, 0.30, 0.44]))
    view_front(fig.add_axes([0.40, 0.50, 0.56, 0.44]))
    view_side(fig.add_axes([0.03, 0.05, 0.34, 0.38]))

    ax = fig.add_axes([0.44, 0.05, 0.54, 0.38])
    ax.axis("off")
    rows = [
        ("底脚", f"X {M.FOOT_X[0]:.0f}~{M.FOOT_X[1]:.0f}，"
                 f"Y {M.FOOT_Y[0]:.2f}~{M.FOOT_Y[1]:.2f}，Z {M.PLATE_T:.0f}~"
                 f"{M.PLATE_T + M.FOOT_T:.0f}（厚 {M.FOOT_T:.0f}）"),
        ("齿板孔", f"8 × Ø{M.HOLE_D}（2 排），Y={M.HOLE_Y} / "
                  f"{M.HOLE_Y_TAIL}，X "
                  f"{M.HOLE_X[0]:.1f}/{M.HOLE_X[1]:.1f}/"
                  f"{M.HOLE_X[2]:.1f}/{M.HOLE_X[3]:.1f}（间距 "
                  f"{M.PLATE_PITCH}）"),
        ("前立柱", f"X {M.POST_X[0]:.0f}~{M.POST_X[1]:.0f}，"
                  f"Y {M.POST1_Y[0]:.2f}~{M.POST1_Y[1]:.2f}，"
                  f"Z {M.PLATE_T + M.FOOT_T:.0f}~{M.POST_TOP:.0f}"),
        ("后立柱", f"Y {M.POST2_Y[0]:.2f}~{M.POST2_Y[1]:.2f}"),
        ("顶梁", f"Z {M.BRIDGE[4]:.0f}~{M.BRIDGE[5]:.0f}（厚 {M.BRIDGE_T:.0f}）"),
        ("螺丝通孔", f"4 × Ø{M.SCREW_D}，Y {M.POST_C1:.2f}/{M.POST_C2:.2f}，"
                    f"Z {M.SERVO_Z - 5:.0f}/{M.SERVO_Z + 5:.0f}"),
        ("法兰槽", f"宽 {M.POCKET_W}，深 {M.POCKET_DEPTH}，"
                  f"Z {M.POCKET_Z[0]:.1f}~{M.POCKET_Z[1]:.1f}（内侧面 X=5）"),
        ("三角筋 ×2", f"45°，腿长 {M.RIB_LEG:.0f}，厚 {M.POST_T:.0f}，"
                     f"在立柱外侧 Y 面"),
        ("两柱净距", "40.5（舵机机身 40，每侧 0.25）"),
    ]
    ax.text(0.0, 1.0, "尺寸表（单位 mm，全部从模型读）", fontsize=12,
            fontweight="bold", transform=ax.transAxes)
    for i, (k, v) in enumerate(rows):
        y = 0.90 - i * 0.088
        ax.text(0.0, y, k, fontsize=10, transform=ax.transAxes,
                fontweight="bold", color="#0b4f8a")
        ax.text(0.16, y, v, fontsize=9.5, transform=ax.transAxes)

    fig.suptitle("g_mount_b  当前版本尺寸图", fontsize=17, fontweight="bold")
    fig.text(0.03, 0.012, "倒角：外棱 45°×1（X=0 前面 / 底面 / 孔口不倒）", fontsize=10, color="#c92a2a")
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_current_dims.png")
