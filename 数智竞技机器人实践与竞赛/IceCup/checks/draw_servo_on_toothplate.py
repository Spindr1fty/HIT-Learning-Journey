r"""Concept layout: servo fixed to the end of the 9 mm tooth plate, shaft pointing
at the toothed edge, driving a swing arm.

Plate local frame (from the DXF): X 0..242.70 along the length, Y 0..24.44 across,
teeth on the Y=0 edge, mounting holes at Y=19.94.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PLATE_L = 242.70
PLATE_W = 24.44
PLATE_T = 9.0
HOLE_Y = 19.94
TOOTH_H = 4.49
SERVO_X = 40.0
SERVO_Y = 40.0
SERVO_Z = 20.0
FLANGE_FROM_BASE = 30.0
SHAFT_TIP = 45.65
HORN_TOP = 47.0
ARM_PLANE = HORN_TOP

C_PLATE = "#d0ebff"
C_BRACKET = "#ffd8a8"
C_SERVO = "#f8f9fa"


def plan(ax):
    ax.set_xlim(-70, 120)
    ax.set_ylim(-55, 40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("俯视（齿在下方）", fontsize=12, fontweight="bold")

    # plate
    ax.add_patch(Rectangle((0, 0), PLATE_L, PLATE_W, facecolor=C_PLATE,
                           ec="#0b4f8a", lw=1.5))
    # teeth as a saw edge
    n = 40
    xs = [i * PLATE_L / n for i in range(n + 1)]
    for i in range(n):
        ax.plot([xs[i], (xs[i] + xs[i + 1]) / 2, xs[i + 1]],
                [0, -TOOTH_H, 0], color="#0b4f8a", lw=0.7)
    # hole row
    for i in range(15):
        ax.add_patch(Circle((20 + i * 16.39, HOLE_Y), 2.25, facecolor="white",
                            ec="#0b4f8a", lw=0.9))

    # bracket foot on the plate's top face
    ax.add_patch(Rectangle((-8, 0), 44, PLATE_W, facecolor=C_BRACKET,
                           ec="#a05a00", lw=1.3, alpha=0.75))
    # servo body, base at the plate's far edge, extending -Y (toward the teeth)
    ax.add_patch(Rectangle((-8, PLATE_W - SERVO_Y), SERVO_X, SERVO_Y,
                           facecolor=C_SERVO, ec="#343a40", lw=1.4))
    ax.text(12, PLATE_W - SERVO_Y / 2, "舵机\n40×40", fontsize=9, ha="center",
            va="center", color="#343a40")
    # shaft
    sh_y = PLATE_W - FLANGE_FROM_BASE
    ax.add_patch(Circle((12, sh_y), 4.5, facecolor="#ffe066", ec="#a05a00",
                        lw=1.2, alpha=0.9))
    ax.plot([12], [sh_y], marker="+", ms=8, color="#a05a00")
    ax.annotate("", xy=(12, sh_y - 14), xytext=(12, sh_y),
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=1.4))
    ax.text(15, sh_y - 16, "轴 → 朝齿", fontsize=8.6, color="#e03131")

    ax.annotate("齿板 242.70 × 24.44（9 厚）", xy=(120, PLATE_W / 2),
                xytext=(60, 26), fontsize=9, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=0.9))
    ax.annotate("支架底脚（2 × M4 穿齿板孔）", xy=(10, 12), xytext=(-66, 30),
                fontsize=8.6, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=0.9))


def side(ax):
    ax.set_xlim(-60, 60)
    ax.set_ylim(-40, 55)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("侧视（看摆臂的旋转面）", fontsize=12, fontweight="bold")

    # plate cross-section, 9 thick
    ax.add_patch(Rectangle((-5, 0), 70, PLATE_T, facecolor=C_PLATE,
                           ec="#0b4f8a", lw=1.5))
    ax.text(30, PLATE_T / 2, "齿板 9", fontsize=9, va="center",
            color="#0b4f8a")

    # servo standing on the plate, shaft to the left
    ax.add_patch(Rectangle((-5, PLATE_T), SERVO_Y, SERVO_Z, facecolor=C_SERVO,
                           ec="#343a40", lw=1.4))
    ax.text(30, PLATE_T + SERVO_Z / 2, "舵机 20 高", fontsize=8.6,
            ha="center", va="center", color="#343a40")

    # flange plane
    fy = PLATE_T + SERVO_Z
    ax.plot([-5, 35], [fy, fy], color="#a05a00", lw=2.0)
    ax.text(36, fy, "法兰面", fontsize=8, va="center", color="#a05a00")

    # swing arm sweeping
    ax.plot([15], [ARM_PLANE], marker="o", ms=5, color="#e03131")
    for a in (30, 60, 90):
        ax.add_patch(Arc((15, ARM_PLANE), 2 * 26, 2 * 26, theta1=a,
                         theta2=a + 25, color="#e03131", lw=1.3))
    ax.plot([15, 15 + 26], [ARM_PLANE, ARM_PLANE], color="#e03131", lw=2.2)
    ax.text(15 + 20, ARM_PLANE + 4, "摆臂", fontsize=9, color="#e03131")

    ax.annotate("", xy=(-30, ARM_PLANE), xytext=(-30, 0),
                arrowprops=dict(arrowstyle="<->", color="#343a40", lw=0.9))
    ax.text(-32, ARM_PLANE / 2, f"{ARM_PLANE:.0f}", fontsize=8.4, rotation=90,
            va="center", ha="right", color="#343a40")


def main(out):
    fig = plt.figure(figsize=(15, 7.5), dpi=115)
    plan(fig.add_axes([0.03, 0.05, 0.58, 0.86]))
    side(fig.add_axes([0.64, 0.05, 0.34, 0.86]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "servo_on_toothplate.png")
