"""Z-axis module parts layout (rack + pinion + printed guide) — final.

Arrangement (rack-railway style):
    rack(fixed) | pinion | arm | carriage | rail(fixed)
The arm ends at the pinion's axle and sits in a different Z-plane than the
gear, so it never crosses the rack. The rack is the outermost part.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FIXED = "#868e96"
MOVE = "#f08c00"
RACK = "#e8590c"
GEAR = "#1c7ed6"
SERVO = "#343a40"
SW = "#2f9e44"
GRIP = "#9c36b5"

RAIL_X = (-15, 15)
CARR_X = (-23, 23)
GEAR_C = (-75, 178)
GEAR_R = 15
RACK_FACE = -90          # rack teeth face, touching the pinion
RACK_X = (-106, -90)


def frame(ax, title, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13.5, fontweight="bold", pad=8)


def leader(ax, text, xy, tx, ty, color, fontsize=10, ha="left"):
    ax.annotate(text, xy=xy, xytext=(tx, ty), fontsize=fontsize,
                color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=1.0,
                                shrinkA=0, shrinkB=2))


def panel_a(ax):
    frame(ax, "A. 装配正视图（从车的侧面看）", (-200, 118), (-45, 335))

    # ① rail — FIXED
    ax.add_patch(Rectangle((RAIL_X[0], 0), 30, 300, facecolor=FIXED, alpha=0.55,
                           edgecolor="#495057", lw=1.4, zorder=2))
    ax.text(0, -40, "① 导轨（固定）", fontsize=11, ha="center", color="#495057")

    # ② rack bar — FIXED, outermost
    ax.add_patch(Rectangle((RACK_X[0], 30), 16, 240, facecolor=RACK, alpha=0.18,
                           edgecolor=RACK, lw=1.6, zorder=2))
    for k in range(29):                      # teeth: 6 mm long, facing +X
        ax.add_patch(Rectangle((RACK_FACE, 34 + k * 8.3), 6, 4.1,
                               facecolor=RACK, edgecolor="none", zorder=3))

    # ③ carriage — MOVING
    ax.add_patch(Rectangle((CARR_X[0], 148), 46, 58, facecolor=MOVE, alpha=0.32,
                           edgecolor=MOVE, lw=2.4, zorder=5))
    ax.text(0, 177, "③", fontsize=14, fontweight="bold", color="#a15c00",
            ha="center", va="center", zorder=11)

    # arm
    ax.add_patch(Rectangle((-75, 168), 52, 20, facecolor=MOVE, alpha=0.26,
                           edgecolor=MOVE, lw=1.5, zorder=4))
    ax.text(-49, 178, "悬臂", fontsize=9.5, color="#a15c00", ha="center",
            va="center", zorder=6)

    # ④ pinion
    ax.add_patch(Circle(GEAR_C, GEAR_R, facecolor="white", edgecolor=GEAR,
                        lw=2.6, zorder=7))
    ax.add_patch(Circle(GEAR_C, 3.4, facecolor=GEAR, edgecolor="none", zorder=8))

    # ⑤ servo — coaxial, in another plane
    ax.add_patch(Circle(GEAR_C, 23, facecolor="none", edgecolor=SERVO,
                        lw=1.3, ls=(0, (5, 4)), zorder=6))

    # ⑧ gripper interface
    ax.add_patch(Rectangle((23, 160), 62, 36, facecolor=GRIP, alpha=0.28,
                           edgecolor=GRIP, lw=1.8, zorder=5))

    # ⑦ limit switches — FIXED
    for h, name in ((32.2, "下层"), (128.5, "中层"), (224.8, "上层")):
        ax.add_patch(Rectangle((30, h - 5.2), 14, 10.4, facecolor=SW, alpha=0.9,
                               edgecolor="none", zorder=5))
        ax.text(50, h, f"{name} {h:.0f}", fontsize=10, color=SW, va="center")

    # stroke
    ax.add_patch(FancyArrowPatch((96, 60), (96, 275), arrowstyle="<->",
                                 mutation_scale=13, color="#212529", lw=1.5))
    ax.text(103, 168, "行程\n230", fontsize=10.5, va="center")

    # motion arrows
    ax.annotate("", xy=(0, 130), xytext=(0, 110),
                arrowprops=dict(arrowstyle="->", color=MOVE, lw=2))
    ax.annotate("", xy=(0, 264), xytext=(0, 284),
                arrowprops=dict(arrowstyle="->", color=MOVE, lw=2))

    # ---- labels, pushed clear to the left margin ----
    leader(ax, "② 齿条\n（固定）", (-98, 268), -198, 300, RACK)
    leader(ax, "④ 齿轮\n（装在悬臂末端）", (-84, 196), -198, 232, GEAR)
    leader(ax, "⑤ 舵机 + ⑥ 座\n（同轴，在齿轮后面）", (-96, 162), -198, 150, SERVO)
    leader(ax, "③ 滑块上下走", (-24, 206), -198, 88, "#a15c00", ha="left")
    leader(ax, "⑦ 限位开关 ×3（固定）", (37, 230), 62, 292, SW)
    leader(ax, "⑧ 取壶机构接口", (54, 162), 62, 118, GRIP)


def panel_b(ax):
    frame(ax, "B. 俯视剖面（与 A 同一 X 坐标）", (-125, 45), (-50, 50))

    ax.add_patch(Rectangle((RAIL_X[0], -15), 30, 30, facecolor=FIXED, alpha=0.55,
                           edgecolor="#495057", lw=1.5, zorder=2))
    ax.text(0, 0, "导轨", fontsize=8.5, ha="center", va="center")

    ax.add_patch(Rectangle((CARR_X[0], -23), 46, 46, facecolor=MOVE, alpha=0.22,
                           edgecolor=MOVE, lw=2.2, zorder=3))
    ax.add_patch(Rectangle((-15.3, -15.3), 30.6, 30.6, facecolor="white",
                           edgecolor=MOVE, lw=0.9, ls=":", zorder=4))
    ax.text(0, 32, "滑块四面包住导轨", fontsize=10, color=MOVE, ha="center")

    ax.add_patch(Rectangle((RACK_X[0], -14), 16, 28, facecolor=RACK, alpha=0.18,
                           edgecolor=RACK, lw=1.6, zorder=3))
    for k in range(7):
        ax.add_patch(Rectangle((RACK_FACE, -12 + k * 4), 6, 2.6,
                               facecolor=RACK, edgecolor="none", zorder=4))

    ax.add_patch(Circle((GEAR_C[0], 0), GEAR_R, facecolor="white",
                        edgecolor=GEAR, lw=2.4, zorder=6))
    ax.add_patch(Circle((GEAR_C[0], 0), 3.4, facecolor=GEAR, zorder=7))

    ax.annotate("配合间隙 0.25mm", xy=(-15.2, 10), xytext=(-6, 42),
                fontsize=9.5, color="#e03131",
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=1.1))
    ax.text(-62, -40, "悬臂与齿轮错开一个平面 → 不碰齿条", fontsize=10,
            ha="center", color="#a15c00")


PARTS = [
    ("①", "导轨", "固定。方 30×30，四面给滑块做导向"),
    ("②", "齿条", "固定，单独一件，装在导轨外侧（模数 2，长约 250）"),
    ("③", "滑块", "上下运动。四面抱住导轨，带一条悬臂伸到齿轮轴"),
    ("④", "齿轮", "装在悬臂末端（模 2 / 15 齿 / 节圆 Ø30）"),
    ("⑤", "舵机", "和齿轮同轴，装在滑块背面 —— 所以舵机线是活动的"),
    ("⑥", "舵机座", "带腰形槽，用来微调齿条啮合间隙"),
    ("⑦", "限位开关 ×3", "固定在导轨上；挡块随滑块，碰到目标层就停"),
    ("⑧", "取壶机构接口", "滑块前端。夹爪 / 电磁铁装这里，后期可换"),
]


def main(out):
    fig = plt.figure(figsize=(17.5, 10.5), dpi=110)
    panel_a(fig.add_axes([0.015, 0.08, 0.38, 0.78]))
    panel_b(fig.add_axes([0.44, 0.60, 0.33, 0.30]))

    fig.suptitle("Z 轴模块 · 零件清单（方案 C：齿条 + 齿轮 + 限位开关）",
                 fontsize=16, fontweight="bold", y=0.975)

    axp = fig.add_axes([0.42, 0.04, 0.56, 0.50])
    axp.axis("off")
    axp.text(0.0, 1.0, "零件清单", fontsize=13, fontweight="bold", va="top")
    for i, (n, name, desc) in enumerate(PARTS):
        y = 0.83 - i * 0.115
        axp.text(0.005, y, n, fontsize=13, fontweight="bold", va="center")
        axp.text(0.045, y, name, fontsize=12, fontweight="bold", va="center")
        axp.text(0.215, y, desc, fontsize=11, va="center", color="#343a40")

    axp.text(0.0, 0.83 - 8 * 0.115 - 0.01,
             "注意：齿轮齿条不自锁 —— 断电时滑块会自由下落。\n"
             "可加一根拉簧配重抵消自重，既省舵机电流也防掉壶。",
             fontsize=11.5, color="#c92a2a", va="top")

    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "z_axis_parts.png")
