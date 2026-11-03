r"""Naming drawing for the g_mount_b bracket.

Two views of the printable part: plan (looking down Z) and side (looking along
+X). Numbers match the table in the reply.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# --- numbers straight out of src/g_mount_b.py ---
ARM_X = (-30.0, 30.0)
ARM_Y = (-22.0, 24.44)
ARM_Z = (9.0, 14.0)
POST_X = (-30.0, -25.0)
POST_W = 10.0
POST_Y = (-14.03, 38.47)          # hole centres in Y
POST_Z = (12.0, 38.0)
BRIDGE_Z = (36.0, 38.0)
FLANGE_HOLES = [(-14.03, 19.0), (-14.03, 29.0), (38.47, 19.0), (38.47, 29.0)]
PLATE_HOLES = [(8.0, 19.94), (24.39, 19.94)]
PLATE_W = 24.44

C_ARM = "#d0ebff"
C_POST = "#ffd8a8"
C_HOLE = "#ffffff"


def plan(ax):
    ax.set_xlim(-48, 40)
    ax.set_ylim(-36, 60)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("俯视（从上往下看，齿板在下方）", fontsize=12,
                 fontweight="bold")

    # arm
    ax.add_patch(Rectangle((ARM_X[0], ARM_Y[0]), ARM_X[1] - ARM_X[0],
                           ARM_Y[1] - ARM_Y[0], facecolor=C_ARM,
                           ec="#0b4f8a", lw=1.6))
    # posts, seen from above
    for yc in POST_Y:
        ax.add_patch(Rectangle((POST_X[0], yc - POST_W / 2), 5.0, POST_W,
                               facecolor=C_POST, ec="#a05a00", lw=1.3))
    # bridge (dashed, above)
    ax.add_patch(Rectangle((POST_X[0], POST_Y[0] - POST_W / 2), 5.0,
                           POST_Y[1] - POST_Y[0] + POST_W,
                           fill=False, ec="#a05a00", lw=1.0, ls="--"))
    # flange holes
    for hy, hz in FLANGE_HOLES:
        ax.add_patch(Circle((-27.5, hy), 2.2, facecolor=C_HOLE,
                            ec="#a05a00", lw=1.0))
    # plate fixing holes
    for px, py in PLATE_HOLES:
        ax.add_patch(Circle((px, py), 2.25, facecolor=C_HOLE, ec="#0b4f8a",
                            lw=1.0))
    # the tooth plate outline
    ax.add_patch(Rectangle((0.0, 0.0), 34.0, PLATE_W, fill=False,
                           ec="#2f9e44", lw=1.2, ls=":"))
    ax.text(30, PLATE_W / 2, "齿板\n(参考)", fontsize=8, color="#2f9e44",
            ha="center", va="center")

    ax.annotate("① 横臂（底板）", xy=(0, 12), xytext=(-46, 54), fontsize=9.5,
                color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.1))
    ax.annotate("② 前立柱", xy=(-27.5, POST_Y[0]), xytext=(6, -30),
                fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.1))
    ax.annotate("② 后立柱", xy=(-27.5, POST_Y[1]), xytext=(6, 54),
                fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.1))
    ax.annotate("③ 顶梁", xy=(-27.5, 12), xytext=(-46, 34), fontsize=9.5,
                color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.1))
    ax.annotate("④ 法兰孔 4×M4\n(48.5 × 10)", xy=(-27.5, 36.47),
                xytext=(-46, 46), fontsize=9, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))
    ax.annotate("⑤ 齿板固定孔 2×M4\n(间距 16.39)", xy=(16, 19.94),
                xytext=(4, 40), fontsize=9, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))
    ax.annotate("⑦ 横臂悬空段", xy=(0, -18), xytext=(-46, -30), fontsize=9,
                color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))
    ax.annotate("⑥ 舵机让位腔", xy=(-27.5, 12), xytext=(-46, 22), fontsize=9,
                color="#c92a2a",
                arrowprops=dict(arrowstyle="->", color="#c92a2a", lw=1.0))


def side(ax):
    ax.set_xlim(-40, 40)
    ax.set_ylim(-6, 46)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("侧视（沿 +X 看过去）", fontsize=12, fontweight="bold")

    ax.add_patch(Rectangle((ARM_X[0], ARM_Z[0]), ARM_X[1] - ARM_X[0],
                           ARM_Z[1] - ARM_Z[0], facecolor=C_ARM,
                           ec="#0b4f8a", lw=1.5))
    for yc in POST_Y:
        ax.add_patch(Rectangle((yc - POST_W / 2, POST_Z[0]), POST_W,
                               POST_Z[1] - POST_Z[0], facecolor=C_POST,
                               ec="#a05a00", lw=1.2))
    ax.add_patch(Rectangle((POST_Y[0] - POST_W / 2, BRIDGE_Z[0]),
                           POST_Y[1] - POST_Y[0] + POST_W,
                           BRIDGE_Z[1] - BRIDGE_Z[0], facecolor=C_POST,
                           ec="#a05a00", lw=1.2))
    # servo body silhouette
    ax.add_patch(Rectangle((-10, 14), 40, 20, fill=False, ec="#343a40",
                           lw=1.3, ls="--"))
    ax.text(10, 24, "舵机 20 高", fontsize=8.6, ha="center", color="#343a40")
    # tooth plate
    ax.add_patch(Rectangle((24.44, 0), 20, 9, fill=False, ec="#2f9e44",
                           lw=1.2, ls=":"))
    ax.text(34, 4.5, "齿板 9", fontsize=8, color="#2f9e44", ha="center")

    ax.annotate("⑧ 齿板贴合面 (Z=9)", xy=(-20, 9), xytext=(-38, 1),
                fontsize=8.6, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))
    ax.annotate("顶梁 Z 36~38", xy=(-14, 37), xytext=(-38, 43),
                fontsize=8.6, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))


def main(out):
    fig = plt.figure(figsize=(14, 8.0), dpi=115)
    plan(fig.add_axes([0.02, 0.05, 0.48, 0.88]))
    side(fig.add_axes([0.53, 0.05, 0.45, 0.88]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_names.png")
