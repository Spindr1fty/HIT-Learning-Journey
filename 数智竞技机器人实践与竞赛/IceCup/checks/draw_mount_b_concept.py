r"""Concept sketch for the revised g_mount_b, per the user's four answers.

  1. red block = the raised cross arm, servo sits on it
  2. raise it 25 mm above the tooth plate's top face
  3. that arm is bolted to the tooth plate (needs a foot down on the plate)
  4. keep both posts and the top bridge; the posts get a vertical through-bore
     plus a clamp slot, like the Z axis collar

Plan + side, dimensions only, no 3D.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PLATE_W = 24.44
PLATE_T = 9.0
RAISE = 25.0                 # arm height above the plate's top face
ARM_Z0 = PLATE_T + RAISE     # 34
ARM_Z1 = ARM_Z0 + 5.0        # 39
SERVO_H = 20.0
POST_TOP = ARM_Z1 + 26.0     # 65
BRIDGE_T = 2.0
WALL_X = (-30.0, -25.0)
FOOT_Z = (PLATE_T, PLATE_T + 5.0)
SERVO_Y = PLATE_W / 2.0
POST_Y = (-14.03, 38.47)
POST_W = 10.0
BORE = 8.0

C_ARM = "#d0ebff"
C_POST = "#ffd8a8"
C_SERVO = "#e9ecef"
C_BORE = "#ffffff"


def side(ax):
    ax.set_xlim(-46, 44)
    ax.set_ylim(-4, 76)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("侧视：横臂抬到齿板上表面 +25", fontsize=12, fontweight="bold")

    # tooth plate
    ax.add_patch(Rectangle((0, 0), 46, PLATE_T, facecolor="#d3f9d8",
                           ec="#2f9e44", lw=1.4))
    ax.text(30, PLATE_T / 2, "齿板 9", fontsize=8.5, ha="center",
            va="center", color="#2f9e44")

    # foot
    ax.add_patch(Rectangle((WALL_X[0], FOOT_Z[0]), 60, 5.0,
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.4))
    # riser
    ax.add_patch(Rectangle((WALL_X[0], FOOT_Z[1]), 5.0, ARM_Z0 - FOOT_Z[1],
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.4))
    # raised arm
    ax.add_patch(Rectangle((WALL_X[0], ARM_Z0), 60, 5.0, facecolor=C_ARM,
                           ec="#0b4f8a", lw=1.6))
    # servo on the arm
    ax.add_patch(Rectangle((-10, ARM_Z1), 20, SERVO_H, facecolor=C_SERVO,
                           ec="#343a40", lw=1.3))
    ax.text(0, ARM_Z1 + SERVO_H / 2, "舵机", fontsize=8, ha="center",
            va="center")
    # posts + bridge
    for yc in POST_Y:
        ax.add_patch(Rectangle((yc - POST_W / 2, ARM_Z1), POST_W,
                               POST_TOP - ARM_Z1, facecolor=C_POST,
                               ec="#a05a00", lw=1.3, alpha=0.95))
        ax.add_patch(Rectangle((yc - POST_W / 2 + 1, ARM_Z1 + 0.5),
                               POST_W - 2, POST_TOP - ARM_Z1 - 1.0,
                               facecolor="none", ec="#a05a00", lw=0.8,
                               ls=":"))
    ax.add_patch(Rectangle((POST_Y[0] - POST_W / 2, POST_TOP - BRIDGE_T),
                           POST_Y[1] - POST_Y[0] + POST_W, BRIDGE_T,
                           facecolor=C_POST, ec="#a05a00", lw=1.3))

    # dimensions
    for z0, z1, label, x in ((PLATE_T, ARM_Z0, "25", -38),
                             (ARM_Z0, ARM_Z1, "5", -38),
                             (ARM_Z1, ARM_Z1 + SERVO_H, "20", -30)):
        ax.annotate("", xy=(x, z0), xytext=(x, z1),
                    arrowprops=dict(arrowstyle="<->", color="#343a40", lw=0.9))
        ax.text(x - 2.0, (z0 + z1) / 2, label, fontsize=9, rotation=90,
                va="center", ha="right", color="#343a40")

    ax.annotate("① 抬高的横臂\n（红色那块）", xy=(-12, ARM_Z1 - 2),
                xytext=(-44, 60), fontsize=9.5, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.1))
    ax.annotate("② 竖脚（连到齿板）", xy=(1.5, 22), xytext=(14, 62),
                fontsize=9.5, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.1))
    ax.annotate("③ 底脚（4×Ø4.5 穿齿板）", xy=(14, 11.5), xytext=(10, -2),
                fontsize=9, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))
    ax.annotate("④ 柱子（上下贯穿孔+槽）", xy=(-14, 52), xytext=(6, 70),
                fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.1))
    ax.annotate("⑤ 顶梁", xy=(10, POST_TOP - 1), xytext=(20, 70),
                fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))


def plan(ax):
    ax.set_xlim(-46, 40)
    ax.set_ylim(-34, 60)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("俯视（沿 +Z 看下来）", fontsize=12, fontweight="bold")

    # arm
    ax.add_patch(Rectangle((WALL_X[0], -20), 60, PLATE_W + 20,
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.6))
    # posts, with the bore + slot
    for yc in POST_Y:
        ax.add_patch(Rectangle((WALL_X[0], yc - POST_W / 2), 5.0, POST_W,
                               facecolor=C_POST, ec="#a05a00", lw=1.3))
        ax.add_patch(Circle((-27.5, yc), BORE / 2, facecolor=C_BORE,
                            ec="#a05a00", lw=1.1))
        # clamp slot: a thin cut from the bore out through the front face
        ax.plot([-27.5 - BORE / 2, -30.0], [yc - 1.5, yc - 1.5],
                color="white", lw=2.2)
    # plate fixing holes in the foot
    for k in range(4):
        ax.add_patch(Circle((8 + k * 8.196, 19.94), 2.25, facecolor=C_BORE,
                            ec="#0b4f8a", lw=1.0))
    # tooth plate reference
    ax.add_patch(Rectangle((0, 0), 34, PLATE_W, fill=False, ec="#2f9e44",
                           lw=1.2, ls=":"))
    ax.text(24, PLATE_W / 2 + 3, "齿板", fontsize=8, color="#2f9e44")

    ax.annotate("④ 柱子的贯穿孔 + 槽\n（照 Z 轴抱箍的样子）",
                xy=(-27.5, POST_Y[1]), xytext=(-44, 52), fontsize=9,
                color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))
    ax.annotate("③ 4×Ø4.5 齿板孔", xy=(20, 19.94), xytext=(6, 40),
                fontsize=9, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))


def detail(ax):
    ax.set_xlim(-26, 26)
    ax.set_ylim(-26, 26)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("柱子放大（贯穿孔 + 夹紧槽）", fontsize=11, fontweight="bold")
    ax.add_patch(Rectangle((-5, -11), 10, 22, facecolor=C_POST,
                           ec="#a05a00", lw=1.4))
    ax.add_patch(Circle((0, 0), BORE / 2, facecolor=C_BORE, ec="#a05a00",
                        lw=1.2))
    ax.plot([-BORE / 2, -5], [0, 0], color="white", lw=3.0)
    ax.annotate("沿柱长方向贯穿", xy=(5, 0), xytext=(9, 12), fontsize=8.5,
                color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))
    ax.annotate("开口槽（夹紧用）", xy=(-4, 0), xytext=(-24, -18), fontsize=8.5,
                color="#e03131",
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=1.0))


def main(out):
    fig = plt.figure(figsize=(16, 8.6), dpi=115)
    side(fig.add_axes([0.02, 0.06, 0.44, 0.86]))
    plan(fig.add_axes([0.49, 0.06, 0.28, 0.86]))
    detail(fig.add_axes([0.79, 0.06, 0.19, 0.86]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_concept.png")
