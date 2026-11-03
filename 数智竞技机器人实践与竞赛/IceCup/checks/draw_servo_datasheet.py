r"""Dimensioned data sheet for the 20 kg servo, assembled from:
  - dxf/Motor.dxf        : body 40 x 20 x 40, output shaft dia 5.9
  - the user's calipers  : flange, neck, shaft lengths, hole pattern
  - the horn drawing     : dia 20 x 2.5, 4 x M3 on BCD 14, 25T spline

Coordinates here: standing on its base, shaft up, body 40 (X) x 20 (Y) x 40 (Z).
The output shaft is NOT on the hole-pattern centre -- it sits 10 mm along +X from
it, which is the single dimension that has caused the most rework.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# --- data ---
BODY_X = 40.0
BODY_Y = 20.0
BODY_Z = 40.0
TOTAL_Z = 45.65
FLANGE_Z0 = 30.0
FLANGE_Z1 = 32.5
NECK_TOP = 40.0
HOLE_SPAN = 48.5
HOLE_GAP = 10.0
HOLE_D = 4.4
SHAFT_D = 5.9
SHAFT_X_OFF = 10.0          # shaft axis is +10 X from the hole-pattern centre
HORN_D = 20.0
HORN_T = 2.5
HORN_TOP = 47.0             # 7.0 above the body top
BCD = 14.0

C_BODY = "#d0ebff"
C_FLG = "#ffe8cc"
C_SHAFT = "#e9ecef"


def view_front(ax):
    ax.set_xlim(-20, 62)
    ax.set_ylim(-12, 56)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("正视图（看 40×45.65 面）", fontsize=11, fontweight="bold")

    ax.add_patch(Rectangle((0, 0), BODY_X, BODY_Z, facecolor=C_BODY,
                           ec="#0b4f8a", lw=1.6))
    # flange
    fx0 = (BODY_X - HOLE_SPAN) / 2.0
    ax.add_patch(Rectangle((fx0, FLANGE_Z0), HOLE_SPAN, FLANGE_Z1 - FLANGE_Z0,
                           facecolor=C_FLG, ec="#a05a00", lw=1.4))
    # neck above the flange
    ax.add_patch(Rectangle((10, FLANGE_Z1), 20, NECK_TOP - FLANGE_Z1,
                           facecolor=C_BODY, ec="#0b4f8a", lw=1.2))
    # shaft
    sx = BODY_X / 2 + SHAFT_X_OFF
    ax.add_patch(Rectangle((sx - SHAFT_D / 2, NECK_TOP), SHAFT_D,
                           TOTAL_Z - NECK_TOP, facecolor=C_SHAFT,
                           ec="#495057", lw=1.2))
    ax.plot([sx - 9, sx - 9], [0, TOTAL_Z], color="#e03131", lw=0.8, ls=":")
    ax.plot([BODY_X / 2, BODY_X / 2], [0, TOTAL_Z], color="#2f9e44", lw=0.8, ls=":")

    # dims
    def dim(x0, y0, x1, y1, label, off=0.0, vertical=False):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="<->",
                                     mutation_scale=8, color="#343a40", lw=0.8))
        ax.text((x0 + x1) / 2 + (off if not vertical else 0),
                (y0 + y1) / 2 + (off if vertical else 0), label,
                fontsize=8.4, color="#343a40",
                ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.5))

    dim(0, -5, BODY_X, -5, "40")
    dim(40 + 5, 0, 40 + 5, BODY_Z, "40", off=2.0, vertical=True)
    dim(40 + 11, 0, 40 + 11, TOTAL_Z, "45.65", off=3.5, vertical=True)
    dim(fx0 - 5, FLANGE_Z0, fx0 - 5, FLANGE_Z1, "2.5", off=2.5, vertical=True)
    dim(40 + 18, NECK_TOP, 40 + 18, TOTAL_Z, "5.65", off=3.0, vertical=True)
    ax.annotate("法兰下表面 30.0", xy=(fx0, FLANGE_Z0), xytext=(-18, 26),
                fontsize=8, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=0.9))
    ax.annotate("轴心在孔排中心 +10", xy=(sx, 44), xytext=(sx + 6, 52),
                fontsize=8, color="#e03131",
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=0.9))
    ax.annotate("本体颈 20 宽", xy=(20, 36), xytext=(0, 46),
                fontsize=8, color="#0b4f8a",
                arrowprops=dict(arrowstyle="->", color="#0b4f8a", lw=0.9))


def view_top(ax):
    ax.set_xlim(-20, 62)
    ax.set_ylim(-22, 30)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("俯视 / 法兰孔位（48.5 × 10）", fontsize=11, fontweight="bold")

    ax.add_patch(Rectangle((0, 0), BODY_X, BODY_Y, facecolor=C_BODY,
                           ec="#0b4f8a", lw=1.6))
    fx0 = (BODY_X - HOLE_SPAN) / 2.0
    fy0 = (BODY_Y - HOLE_GAP) / 2.0
    ax.add_patch(Rectangle((fx0, fy0), HOLE_SPAN, HOLE_GAP, facecolor=C_FLG,
                           ec="#a05a00", lw=1.2, alpha=0.8))
    for hx in (fx0, fx0 + HOLE_SPAN):
        for hy in (fy0, fy0 + HOLE_GAP):
            ax.add_patch(Circle((hx, hy), HOLE_D / 2, facecolor="white",
                                ec="#a05a00", lw=1.1))
    # open slots: the flange is U shaped, so the holes break out sideways
    ax.plot([fx0, fx0], [fy0, fy0 + HOLE_GAP], color="white", lw=2.6)
    ax.plot([fx0 + HOLE_SPAN, fx0 + HOLE_SPAN], [fy0, fy0 + HOLE_GAP],
            color="white", lw=2.6)
    sx = BODY_X / 2 + SHAFT_X_OFF
    ax.add_patch(Circle((sx, BODY_Y / 2), SHAFT_D / 2, facecolor=C_SHAFT,
                        ec="#495057", lw=1.2))
    ax.plot([sx], [BODY_Y / 2], marker="+", ms=9, color="#e03131")
    ax.annotate("", xy=(BODY_X / 2, BODY_Y / 2), xytext=(sx, BODY_Y / 2),
                arrowprops=dict(arrowstyle="<->", color="#e03131", lw=1.0))
    ax.text((BODY_X / 2 + sx) / 2, BODY_Y / 2 + 3.5, "10", fontsize=8.4,
            color="#e03131", ha="center")
    ax.text(BODY_X / 2 - 2, BODY_Y / 2 - 6, "孔排中心", fontsize=7.6,
            color="#2f9e44", ha="center")
    ax.text(sx + 3, BODY_Y / 2 + 6, "轴心", fontsize=8, color="#e03131")
    ax.annotate("4 × Ø4.4 开口槽", xy=(fx0, fy0), xytext=(-18, 24),
                fontsize=8, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=0.9))


def view_horn(ax):
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("舵盘 Ø20 × 2.5（BCD 14，25T 花键）", fontsize=11,
                 fontweight="bold")
    ax.add_patch(Circle((0, 0), HORN_D / 2, facecolor="#f8f9fa",
                        ec="#495057", lw=1.5))
    ax.add_patch(Circle((0, 0), SHAFT_D / 2, facecolor=C_SHAFT,
                        ec="#e03131", lw=1.2))
    ax.text(0, -1.2, "Ø5.9\n25T", fontsize=7, ha="center", color="#e03131")
    import math
    for k in range(4):
        a = math.radians(45 + 90 * k)
        hx, hy = BCD / 2 * math.cos(a), BCD / 2 * math.sin(a)
        ax.add_patch(Circle((hx, hy), 1.6, facecolor="white", ec="#a05a00",
                            lw=1.1))
    ax.add_patch(Circle((0, 0), BCD / 2, fill=False, ec="#a05a00", lw=0.7,
                        ls=":"))
    ax.annotate("", xy=(-BCD / 2, 0), xytext=(BCD / 2, 0),
                arrowprops=dict(arrowstyle="<->", color="#a05a00", lw=0.9))
    ax.text(0, 3.0, "BCD 14", fontsize=8, ha="center", color="#a05a00")
    ax.text(0, -12.5, "4 × Ø2.55 穿 M3", fontsize=8, ha="center",
            color="#a05a00")


def main(out):
    fig = plt.figure(figsize=(15, 10.5), dpi=115)
    view_front(fig.add_axes([0.04, 0.52, 0.42, 0.40]))
    view_top(fig.add_axes([0.52, 0.52, 0.42, 0.40]))
    view_horn(fig.add_axes([0.04, 0.04, 0.34, 0.38]))

    ax = fig.add_axes([0.42, 0.04, 0.56, 0.38])
    ax.axis("off")
    rows = [
        ("本体", "40 × 20 × 40"),
        ("总高（含轴）", "45.65"),
        ("法兰", "上表面 32.5 / 下表面 30.0，厚 2.5，宽 48.5"),
        ("法兰孔", "4 × Ø4.4 开口槽，孔距 48.5 × 10"),
        ("本体颈", "法兰上 7.5 高，20 宽"),
        ("输出轴", "Ø5.9，25T 花键，露出 5.65"),
        ("★ 轴心偏移", "比法兰孔排中心偏 +10（X 向）"),
        ("舵盘", "Ø20 × 2.5，4 × M3 在 BCD 14，顶面高出本体 7.0"),
        ("力矩", "20 kg·cm"),
        ("速度", "0.16 s / 60° @ 6V，360° 连续"),
        ("工作电压", "5V（逻辑）/ 6~6.8V（动力）"),
    ]
    ax.text(0.0, 1.02, "舵机数据汇总", fontsize=13, fontweight="bold",
            transform=ax.transAxes)
    for i, (k, v) in enumerate(rows):
        y = 0.93 - i * 0.075
        ax.text(0.0, y, k, fontsize=9.5, transform=ax.transAxes,
                fontweight="bold", color="#0b4f8a")
        ax.text(0.22, y, v, fontsize=9.5, transform=ax.transAxes)
    ax.text(0.0, 0.93 - len(rows) * 0.075 - 0.02,
            "数据来源：dxf/Motor.dxf（40×20×40 + 轴 Ø5.9）"
            " + 用户卡尺实测（法兰/颈/轴长/孔距）+ 舵盘图纸",
            fontsize=8, transform=ax.transAxes, color="#868e96")

    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "servo_datasheet.png")
