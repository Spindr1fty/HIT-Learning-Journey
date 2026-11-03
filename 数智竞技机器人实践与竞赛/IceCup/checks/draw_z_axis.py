"""Draw the Z-axis mechanism options for the IceCup robot.

Panel A: what a crank-slider looks like.
Panel B: why the crank-slider does not fit vertically.
Panel C: the rack + pinion alternative.

Output: a single PNG. Chinese labels use Microsoft YaHei.
"""

import io
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Arc

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

TABLE = "#c9d6e3"      # table fill
RAIL = "#8a9bb0"
CRANK = "#e8590c"      # orange
ROD = "#1c7ed6"        # blue
OK = "#2f9e44"         # green
BAD = "#e03131"        # red
MAST = "#495057"


def panel_frame(ax, title, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)


def draw_table(ax, x0, x1, y=0.0):
    """Table surface as a thick line with a hatched block below."""
    ax.add_patch(Rectangle((x0, y - 40), x1 - x0, 40, facecolor=TABLE,
                           edgecolor="none", zorder=0))
    ax.plot([x0, x1], [y, y], color="#495057", lw=2.5, zorder=1)
    ax.text(x1, y - 22, "台面", ha="right", va="top", fontsize=9, color="#495057")


# ----------------------------------------------------------------------------
# Panel A — crank-slider, what it looks like
# ----------------------------------------------------------------------------
R = 115.0
L = 300.0


def slider_y(theta_deg):
    import math
    t = math.radians(theta_deg)
    return R * math.cos(t) + math.sqrt(L * L - (R * math.sin(t)) ** 2)


def crank_pin(theta_deg):
    import math
    t = math.radians(theta_deg)
    return R * math.sin(t), R * math.cos(t)


def panel_a(ax):
    panel_frame(ax, "A. 曲柄连杆：机构长这样", (-230, 260), (-230, 500))
    draw_table(ax, -230, 260)

    # crank circle
    ax.add_patch(Circle((0, 0), R, fill=False, ec=CRANK, lw=1.2, ls=(0, (4, 3)), zorder=2))
    ax.plot(0, 0, "o", color="#343a40", ms=5, zorder=3)
    ax.text(8, -18, "曲柄中心\n（舵机轴）", fontsize=8.5, color="#343a40", va="top")

    for th, lbl in ((0, "0°"), (90, "90°"), (180, "180°")):
        px, py = crank_pin(th)
        sy = slider_y(th)
        ax.plot([0, px], [0, py], color=CRANK, lw=3.5, solid_capstyle="round", zorder=3)
        ax.plot([px, 0], [py, sy], color=ROD, lw=2.2, zorder=3)
        ax.plot(0, sy, "s", color=ROD, ms=7, zorder=4)
        ax.text(px + 14, py, lbl, fontsize=9, color=CRANK, fontweight="bold")
        ax.text(20, sy, f"{sy:.0f}", fontsize=9, color=ROD, va="center")

    # slider guide
    ax.plot([0, 0], [160, 440], color=RAIL, lw=1.0, ls=":", zorder=1)
    ax.text(-150, 300, "滑块\n（立柱）", fontsize=9, color=ROD, ha="center")

    # travel dimension
    ax.add_patch(FancyArrowPatch((150, slider_y(180)), (150, slider_y(0)),
                                 arrowstyle="<->", mutation_scale=12, color=ROD, lw=1.4))
    ax.text(158, (slider_y(0) + slider_y(180)) / 2, "行程\n230", fontsize=9, color=ROD, va="center")

    ax.text(-220, 470, f"曲柄半径 R={R:.0f}    连杆 L={L:.0f}", fontsize=10,
            fontweight="bold", color="#212529")


# ----------------------------------------------------------------------------
# Panel B — why it does not fit
# ----------------------------------------------------------------------------
def panel_b(ax):
    panel_frame(ax, "B. 为什么装不下：滑块区间对不上", (-260, 300), (-260, 500))
    draw_table(ax, -260, 300)

    # slider range the crank gives
    lo, hi = slider_y(180), slider_y(0)
    ax.add_patch(Rectangle((-70, lo), 140, hi - lo, facecolor=ROD, alpha=0.20,
                           edgecolor=ROD, lw=1.2))
    ax.text(80, (lo + hi) / 2, f"曲柄能给\n{lo:.0f} – {hi:.0f}", fontsize=9, color=ROD, va="center")

    # slider range we need
    need_lo, need_hi = 20, 250
    ax.add_patch(Rectangle((70, need_lo), 140, need_hi - need_lo, facecolor=OK, alpha=0.20,
                           edgecolor=OK, lw=1.2))
    ax.text(-80, (need_lo + need_hi) / 2, f"我们需要\n{need_lo} – {need_hi}",
            fontsize=9, color=OK, va="center", ha="right")

    # the gap
    gap = lo - need_lo
    ax.add_patch(FancyArrowPatch((0, lo), (0, need_lo), arrowstyle="<->",
                                 mutation_scale=13, color=BAD, lw=2.0))
    ax.text(10, (lo + need_lo) / 2, f"差 {gap:.0f} mm", fontsize=11,
            color=BAD, fontweight="bold", va="center")

    # required crank centre
    ax.plot(0, -gap, "x", color=BAD, ms=14, mew=3, zorder=5)
    ax.add_patch(Circle((0, -gap), R, fill=False, ec=BAD, lw=1.4, ls=(0, (4, 3)), zorder=4))
    ax.text(20, -gap, "曲柄中心必须落到这里\n↓ 台面以下 165mm，装不了",
            fontsize=10, color=BAD, fontweight="bold", va="center")

    ax.text(-250, 470, "结论：竖直曲柄连杆的行程中心固定在连杆长度处，\n"
                       "而台面挡住了它的落点。", fontsize=10, color="#212529", va="top")


# ----------------------------------------------------------------------------
# Panel C — rack + pinion
# ----------------------------------------------------------------------------
def panel_c(ax):
    panel_frame(ax, "C. 换方案：齿条 + 齿轮 + 限位开关", (-260, 320), (-260, 500))
    draw_table(ax, -260, 320)

    # mast (moving carriage) from table to top
    ax.add_patch(Rectangle((-40, 0), 44, 250, facecolor=MAST, alpha=0.22,
                           edgecolor=MAST, lw=1.6))
    ax.text(-18, 262, "立柱（上下动）", fontsize=9, color=MAST, ha="center")

    # rack teeth
    for i in range(0, 250, 12):
        ax.plot([4, 14], [i + 6, i + 6], color=MAST, lw=2.4)

    # pinion
    ax.add_patch(Circle((30, 130), 16, facecolor="white", edgecolor=CRANK, lw=2.2, zorder=4))
    ax.plot(30, 130, "o", color=CRANK, ms=4, zorder=5)

    # servo body
    ax.add_patch(Rectangle((52, 110), 62, 40, facecolor="#f1f3f5",
                           edgecolor="#343a40", lw=1.6, zorder=3))
    ax.text(83, 130, "360°\n舵机", fontsize=9, ha="center", va="center", zorder=6)
    ax.plot([30, 52], [130, 130], color="#343a40", lw=1.6, zorder=3)

    # three stone heights
    for h, name in ((32.2, "下"), (128.5, "中"), (224.8, "上")):
        ax.plot([-40, -12], [h, h], color=OK, lw=2.6, solid_capstyle="round", zorder=6)
        ax.plot([-72, -46], [h, h], color="#adb5bd", lw=1.4, zorder=3)
        ax.plot(-74, h, "o", color=OK, ms=5.5, zorder=6)
        ax.text(-86, h, f"{name}层 {h:.0f}", fontsize=9, color=OK,
                ha="right", va="center")

    ax.text(-86, -14, "限位开关 ×3", fontsize=9, color=OK, ha="right", va="top")

    # speed / force notes
    ax.text(140, 230, "齿轮 Ø30\n（周长 94mm）", fontsize=9, color=CRANK, va="top")
    ax.text(140, 150, "速度：\n62 RPM × 94mm\n≈ 98 mm/s\n→ 走完 230mm 用 2.4 秒",
            fontsize=9, color="#212529", va="top")
    ax.text(140, 40, "推力：\n1.86 N·m ÷ 15mm\n≈ 124 N\n（立柱+壶约 5 N）",
            fontsize=9, color=OK, va="top", fontweight="bold")

    ax.text(-250, 470, "位置靠限位开关触发，与电池电压无关。\n"
                       "行程 230mm，2.4 秒走完。",
            fontsize=10, color="#212529", va="top")


def main(out_path):
    fig, axes = plt.subplots(1, 3, figsize=(19.5, 7.6), dpi=110)
    panel_a(axes[0])
    panel_b(axes[1])
    panel_c(axes[2])
    fig.suptitle("冰壶机器人 · 升降立柱（Z 轴）机构方案对比", fontsize=15, fontweight="bold", y=0.97)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out_path, facecolor="white")
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "z_axis_options.png")
