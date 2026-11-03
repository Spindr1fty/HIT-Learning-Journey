r"""Concept sketch v2 for g_mount_b.

Changes from v1:
  - the posts carry the servo's four flange screws in OPEN SLOTS that face
    inward (toward the servo), so the servo slides in from inside
  - everything else per the four confirmed answers: raised arm at +25, foot
    bolted to the tooth plate, posts and top bridge kept

Plan + side + post detail, no 3D.
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
RAISE = 25.0
ARM_Z0 = PLATE_T + RAISE          # 34
ARM_Z1 = ARM_Z0 + 5.0             # 39
SERVO_H = 20.0
SERVO_TOP = ARM_Z1 + SERVO_H      # 59
FLANGE_HI = ARM_Z1 + 10.0 + 5.0   # 54
FLANGE_LO = ARM_Z1 + 10.0 - 5.0   # 44
POST_TOP = ARM_Z1 + 26.0          # 65
BRIDGE_T = 2.0
WALL_X = (-30.0, -25.0)
FOOT_Z = (PLATE_T, PLATE_T + 5.0)
POST_Y = (-14.03, 38.47)
POST_W = 10.0
HOLE_D = 4.4
SLOT_D = 3.5

C_ARM = "#d0ebff"
C_POST = "#ffd8a8"
C_SERVO = "#e9ecef"
C_HOLE = "#ffffff"


def side(ax):
    ax.set_xlim(-46, 44)
    ax.set_ylim(-4, 76)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("侧视：横臂抬到齿板上表面 +25", fontsize=12, fontweight="bold")

    ax.add_patch(Rectangle((0, 0), 46, PLATE_T, facecolor="#d3f9d8",
                           ec="#2f9e44", lw=1.4))
    ax.text(32, PLATE_T / 2, "齿板 9", fontsize=8.5, ha="center",
            va="center", color="#2f9e44")

    ax.add_patch(Rectangle((WALL_X[0], FOOT_Z[0]), 60, 5.0,
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.4))
    ax.add_patch(Rectangle((WALL_X[0], FOOT_Z[1]), 5.0, ARM_Z0 - FOOT_Z[1],
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.4))
    ax.add_patch(Rectangle((WALL_X[0], ARM_Z0), 60, 5.0, facecolor=C_ARM,
                           ec="#0b4f8a", lw=1.6))
    ax.add_patch(Rectangle((-10, ARM_Z1), 20, SERVO_H, facecolor=C_SERVO,
                           ec="#343a40", lw=1.3))
    ax.text(0, ARM_Z1 + SERVO_H / 2, "舵机", fontsize=8, ha="center",
            va="center")

    # posts with the open slots, seen from the side (slots show as gaps)
    for yc in POST_Y:
        ax.add_patch(Rectangle((yc - POST_W / 2, ARM_Z1), POST_W,
                               POST_TOP - ARM_Z1, facecolor=C_POST,
                               ec="#a05a00", lw=1.3, alpha=0.95))
        for hz in (FLANGE_LO, FLANGE_HI):
            ax.add_patch(Rectangle((yc - POST_W / 2 + 0.6, hz - SLOT_D / 2),
                                   POST_W - 1.2, SLOT_D, facecolor=C_HOLE,
                                   ec="#a05a00", lw=0.8))
    ax.add_patch(Rectangle((POST_Y[0] - POST_W / 2, POST_TOP - BRIDGE_T),
                           POST_Y[1] - POST_Y[0] + POST_W, BRIDGE_T,
                           facecolor=C_POST, ec="#a05a00", lw=1.3))

    for z0, z1, label, x in ((PLATE_T, ARM_Z0, "25", -42),
                             (ARM_Z0, ARM_Z1, "5", -42),
                             (ARM_Z1, ARM_Z1 + SERVO_H, "20", -30)):
        ax.annotate("", xy=(x, z0), xytext=(x, z1),
                    arrowprops=dict(arrowstyle="<->", color="#343a40", lw=0.9))
        ax.text(x - 2.0, (z0 + z1) / 2, label, fontsize=9, rotation=90,
                va="center", ha="right", color="#343a40")

    ax.annotate("① 抬高的横臂", xy=(-14, ARM_Z1 - 2), xytext=(-44, 70),
                fontsize=9.5, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.1))
    ax.annotate("② 竖脚", xy=(1.5, 22), xytext=(16, 70), fontsize=9.5,
                color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.1))
    ax.annotate("③ 底脚（4×Ø4.5）", xy=(14, 11.5), xytext=(10, -2),
                fontsize=9, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))
    ax.annotate("④ 柱子（舵机开口槽）", xy=(-14, FLANGE_HI), xytext=(4, 74),
                fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.1))
    ax.annotate("⑤ 顶梁", xy=(10, POST_TOP - 1), xytext=(22, 74),
                fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))


def plan(ax):
    ax.set_xlim(-46, 42)
    ax.set_ylim(-34, 60)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("俯视（沿 +Z 看下来）", fontsize=12, fontweight="bold")

    ax.add_patch(Rectangle((WALL_X[0], -20), 60, PLATE_W + 20,
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.6))

    # servo footprint between the posts
    ax.add_patch(Rectangle((-40, -10), 40, 40, fill=False, ec="#343a40",
                           lw=1.2, ls="--"))
    ax.text(-20, 10, "舵机 40×40", fontsize=8, ha="center", color="#343a40")

    # posts: open slots face inward
    for yc in POST_Y:
        inward = -1.0 if yc > 0 else 1.0
        ax.add_patch(Rectangle((WALL_X[0], yc - POST_W / 2), 5.0, POST_W,
                               facecolor=C_POST, ec="#a05a00", lw=1.3))
        for dz in (-5.0, 5.0):
            y0 = yc + dz
            # U slot: a round bottom plus a straight cut out to the inner face
            ax.add_patch(Circle((-27.5, y0), HOLE_D / 2, facecolor=C_HOLE,
                                ec="#a05a00", lw=1.0))
            ax.add_patch(Rectangle((-30.0 if inward < 0 else -25.0, y0 - HOLE_D / 2),
                                   5.0, HOLE_D, facecolor=C_HOLE, ec="none"))

    for k in range(4):
        ax.add_patch(Circle((8 + k * 8.196, 19.94), 2.25, facecolor=C_HOLE,
                            ec="#0b4f8a", lw=1.0))

    ax.add_patch(Rectangle((0, 0), 34, PLATE_W, fill=False, ec="#2f9e44",
                           lw=1.2, ls=":"))
    ax.text(24, PLATE_W / 2 + 3, "齿板", fontsize=8, color="#2f9e44")

    ax.annotate("④ 开口槽朝内\n（舵机从里面滑进去）", xy=(-27.5, POST_Y[0]),
                xytext=(-44, -30), fontsize=9, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))
    ax.annotate("③ 4×Ø4.5 齿板孔", xy=(20, 19.94), xytext=(6, 44),
                fontsize=9, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=1.0))


def detail(ax):
    ax.set_xlim(-30, 30)
    ax.set_ylim(-26, 26)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("后柱子放大（俯视）", fontsize=11, fontweight="bold")
    ax.add_patch(Rectangle((-5, -9), 5, 18, facecolor=C_POST,
                           ec="#a05a00", lw=1.4))
    for y0 in (-5, 5):
        ax.add_patch(Circle((-2.5, y0), HOLE_D / 2, facecolor=C_HOLE,
                            ec="#a05a00", lw=1.1))
        ax.add_patch(Rectangle((-30, y0 - HOLE_D / 2), 27.5, HOLE_D,
                               facecolor=C_HOLE, ec="none"))
    ax.annotate("槽从内侧面开出去", xy=(-6, 5), xytext=(-28, 18), fontsize=8.5,
                color="#e03131")
    ax.annotate("舵机在\n这一侧", xy=(-24, -14), xytext=(-26, -24), fontsize=8.5,
                color="#343a40")


def main(out):
    fig = plt.figure(figsize=(16, 8.6), dpi=115)
    side(fig.add_axes([0.02, 0.06, 0.44, 0.86]))
    plan(fig.add_axes([0.49, 0.06, 0.28, 0.86]))
    detail(fig.add_axes([0.80, 0.06, 0.18, 0.86]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_concept2.png")
