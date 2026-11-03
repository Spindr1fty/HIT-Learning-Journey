r"""Clean concept drawing for g_mount_b, version 3.

Deliberately sparse: two views, dimension lines only, no callout arrows.
The five part names are given in the reply, not on the drawing.
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
POST_TOP = ARM_Z1 + 26.0          # 65
BRIDGE_T = 2.0
X0, X1 = -30.0, 30.0
POST_Y = (-14.03, 38.47)
POST_W = 10.0
SLOT_Z = (44.0, 54.0)
SLOT_D = 4.5
BODY_Y = (-10.0, 40.0)

C_ARM = "#cfe4ff"
C_POST = "#ffd8a8"
C_SERVO = "#e9ecef"
C_PLATE = "#d3f9d8"
C_HOLE = "#ffffff"
DIM = "#495057"


def dimv(ax, x, z0, z1, label, side="right"):
    ax.annotate("", xy=(x, z0), xytext=(x, z1),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.0))
    ax.text(x + (1.6 if side == "right" else -1.6), (z0 + z1) / 2, label,
            fontsize=10.5, rotation=90, va="center",
            ha="left" if side == "right" else "right", color=DIM)


def dimh(ax, y0, y1, z, label):
    ax.annotate("", xy=(y0, z), xytext=(y1, z),
                arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.0))
    ax.text((y0 + y1) / 2, z + 1.6, label, fontsize=10.5, ha="center",
            va="bottom", color=DIM)


def side(ax):
    ax.set_xlim(-52, 62)
    ax.set_ylim(-8, 76)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("侧视", fontsize=15, fontweight="bold", pad=14)

    ax.add_patch(Rectangle((0, 0), 58, PLATE_T, facecolor=C_PLATE,
                           ec="#2f9e44", lw=1.6))
    ax.add_patch(Rectangle((X0, PLATE_T), X1 - X0, 5.0, facecolor=C_ARM,
                           ec="#0b4f8a", lw=1.6))
    ax.add_patch(Rectangle((X0, PLATE_T + 5.0), 5.0, RAISE - 5.0,
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.6))
    ax.add_patch(Rectangle((X0, ARM_Z0), X1 - X0, 5.0, facecolor=C_ARM,
                           ec="#0b4f8a", lw=1.8))
    ax.add_patch(Rectangle((-20, ARM_Z1), 40, SERVO_H, facecolor=C_SERVO,
                           ec="#343a40", lw=1.6))
    for yc in POST_Y:
        ax.add_patch(Rectangle((yc - POST_W / 2, ARM_Z1), POST_W,
                               POST_TOP - ARM_Z1, facecolor=C_POST,
                               ec="#a05a00", lw=1.6))
        for hz in SLOT_Z:
            ax.add_patch(Rectangle((yc - SLOT_D / 2, hz - 1.6), SLOT_D, 3.2,
                                   facecolor=C_HOLE, ec="#a05a00", lw=1.0))
    ax.add_patch(Rectangle((POST_Y[0] - POST_W / 2, POST_TOP - BRIDGE_T),
                           POST_Y[1] - POST_Y[0] + POST_W, BRIDGE_T,
                           facecolor=C_POST, ec="#a05a00", lw=1.6))

    dimv(ax, X1 + 8, PLATE_T, ARM_Z0, "25")
    dimv(ax, X1 + 8, ARM_Z0, ARM_Z1, "5")
    dimv(ax, X1 + 20, ARM_Z1, ARM_Z1 + SERVO_H, "20")
    dimv(ax, X1 + 20, ARM_Z1 + SERVO_H, POST_TOP, "6")
    dimh(ax, POST_Y[0], POST_Y[1], POST_TOP + 9, "52.5")


def plan(ax):
    ax.set_xlim(-52, 62)
    ax.set_ylim(-40, 58)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("俯视", fontsize=15, fontweight="bold", pad=14)

    ax.add_patch(Rectangle((X0, -20), X1 - X0, PLATE_W + 20,
                           facecolor=C_ARM, ec="#0b4f8a", lw=1.8))
    ax.add_patch(Rectangle((-40, BODY_Y[0]), 40, BODY_Y[1] - BODY_Y[0],
                           fill=False, ec="#343a40", lw=1.4, ls="--"))

    for yc in POST_Y:
        inward = 1.0 if yc < 0 else -1.0
        ax.add_patch(Rectangle((X0, yc - POST_W / 2), 5.0, POST_W,
                               facecolor=C_POST, ec="#a05a00", lw=1.6))
        for dz in (-5.0, 5.0):
            yy = yc + dz
            ax.add_patch(Circle((X0 + 2.5, yy), SLOT_D / 2, facecolor=C_HOLE,
                                ec="#a05a00", lw=1.2))
            ax.add_patch(Rectangle((X0 + 2.5, yy - SLOT_D / 2),
                                   5.0 if inward > 0 else 0.0, SLOT_D,
                                   facecolor=C_HOLE, ec="none"))
            if inward > 0:
                ax.add_patch(Rectangle((X0, yy - SLOT_D / 2), 2.5, SLOT_D,
                                       facecolor=C_HOLE, ec="none"))
            else:
                ax.add_patch(Rectangle((X0 + 5.0, yy - SLOT_D / 2), 2.5,
                                       SLOT_D, facecolor="none", ec="none"))
                ax.add_patch(Rectangle((X0 + 2.5, yy - SLOT_D / 2), 2.5,
                                       SLOT_D, facecolor=C_HOLE, ec="none"))

    for k in range(4):
        ax.add_patch(Circle((8 + k * 8.196, 19.94), 2.25, facecolor=C_HOLE,
                            ec="#0b4f8a", lw=1.2))

    ax.add_patch(Rectangle((2, 0), 40, PLATE_W, fill=False, ec="#2f9e44",
                           lw=1.4, ls=":"))
    dimh(ax, -20, 24.44, -30, "44.44")
    dimh(ax, 8, 32.6, 34, "24.6")


def main(out):
    fig = plt.figure(figsize=(13.5, 8.2), dpi=120, facecolor="white")
    side(fig.add_axes([0.02, 0.04, 0.50, 0.90]))
    plan(fig.add_axes([0.54, 0.04, 0.44, 0.90]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "mount_b_clean.png")
