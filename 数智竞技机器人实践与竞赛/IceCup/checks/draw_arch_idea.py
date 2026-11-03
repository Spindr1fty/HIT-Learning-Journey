r"""Schematic of the "arch over the rack" idea for g_mount_b, for discussion.

    python draw_arch_idea.py -> renders/g_mount_b_arch_idea.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = r"D:\IceCup\renders\g_mount_b_arch_idea.png"

C_RACK = "#c8ccd2"
C_ARCH = "#f6d7b0"
C_SERVO = "#c9d9e8"
C_DIM = "#5b6773"
C_RED = "#c92a2a"
C_GRN = "#2f6f2f"


def rack_section(ax, x0, y0, w=16.0, h=24.5, teeth=True):
    """Rack cross-section in the X-Z plane: 16 wide, 24.5 tall, teeth on both 16 sides."""
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=C_RACK, edgecolor="k", lw=1.4, zorder=2))
    if teeth:
        # tooth teeth on both X faces, pitch 1.63
        pitch, th = 1.63, 0.6
        n = int(h / pitch)
        for i in range(n):
            yy = y0 + 1.0 + i * pitch
            ax.add_patch(Polygon([[x0, yy], [x0 - th, yy + pitch * 0.3],
                                  [x0 - th, yy + pitch * 0.7], [x0, yy + pitch]],
                                 closed=True, facecolor=C_RACK, edgecolor="k", lw=0.5, zorder=3))
            ax.add_patch(Polygon([[x0 + w, yy], [x0 + w + th, yy + pitch * 0.3],
                                  [x0 + w + th, yy + pitch * 0.7], [x0 + w, yy + pitch]],
                                 closed=True, facecolor=C_RACK, edgecolor="k", lw=0.5, zorder=3))


def main():
    fig = plt.figure(figsize=(16, 9), dpi=130, facecolor="white")

    # ---------- panel 1: cross-section through the rack (X-Z)
    ax = fig.add_axes([0.05, 0.42, 0.42, 0.50])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-38, 44)
    ax.set_ylim(-20, 52)
    ax.set_title("剖面 A-A（横切齿条，X-Z）：拱门 + 一颗通孔螺栓", fontsize=12, fontweight="bold")

    RX, RZ0, RW, RH = -8.0, 6.0, 16.0, 24.5
    rack_section(ax, RX, RZ0, RW, RH)
    ax.text(RX + RW / 2, RZ0 + RH / 2, "齿条\n16 × 24.5", ha="center", va="center", fontsize=9)

    # arch: legs either side, bridge over the top
    LEG_T, GAP, TOP_T = 4.0, 0.3, 5.0
    leg_l = RX - LEG_T - GAP
    leg_r = RX + RW + GAP
    top_z = RZ0 + RH
    ax.add_patch(Rectangle((leg_l, -2.0), LEG_T, top_z + 2.0 + TOP_T,
                           facecolor=C_ARCH, edgecolor="k", lw=1.4, zorder=4))
    ax.add_patch(Rectangle((leg_r, -2.0), LEG_T, top_z + 2.0 + TOP_T,
                           facecolor=C_ARCH, edgecolor="k", lw=1.4, zorder=4))
    ax.add_patch(Rectangle((leg_l, top_z), leg_r + LEG_T - leg_l, TOP_T,
                           facecolor=C_ARCH, edgecolor="k", lw=1.4, zorder=4))
    # bolt through the legs, below the rack
    BZ = -3.5
    ax.plot([leg_l - 4, leg_r + LEG_T + 4], [BZ, BZ], color=C_RED, lw=2.2, zorder=6)
    ax.add_patch(Rectangle((leg_l - 4.5, BZ - 1.9), 2.6, 3.8, facecolor="#e8e8e8",
                           edgecolor=C_RED, lw=1.0, zorder=7))
    ax.add_patch(Rectangle((leg_r + LEG_T + 1.9, BZ - 1.9), 2.6, 3.8, facecolor="#e8e8e8",
                           edgecolor=C_RED, lw=1.0, zorder=7))
    ax.text(0, BZ - 6.0, "M4 通孔 + 螺母（夹紧/预紧）", ha="center", fontsize=9, color=C_RED)

    # servo box on top of the arch
    ax.add_patch(Rectangle((-24, top_z + TOP_T), 48, 20, facecolor=C_SERVO,
                           edgecolor="#6b3fa0", lw=1.3, ls=(0, (5, 3)), zorder=5))
    ax.text(0, top_z + TOP_T + 10, "舵机盒（现有 g_mount_b 的包围盒）", ha="center",
            va="center", fontsize=9, color="#6b3fa0")

    # pinion on one side of the rack
    ax.add_patch(plt.Circle((RX + RW + 6.5, RZ0 + RH * 0.55), 6.5, facecolor="#ffd9a0",
                            edgecolor="k", lw=1.2, zorder=8))
    ax.text(RX + RW + 15.5, RZ0 + RH * 0.55, "小齿轮\n(舵机轴)", fontsize=8.5, va="center")
    ax.add_patch(FancyArrowPatch((RX + RW + 6.5, RZ0 + RH * 0.55),
                                 (RX + RW + 1.0, RZ0 + RH * 0.55),
                                 arrowstyle="-|>", mutation_scale=12, color=C_GRN, lw=1.4, zorder=9))

    # dims
    ax.annotate("", xy=(RX, RZ0 - 2.5), xytext=(RX + RW, RZ0 - 2.5),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
    ax.text(RX + RW / 2, RZ0 - 5.0, "16", ha="center", fontsize=9, color=C_DIM)
    ax.annotate("", xy=(RX - LEG_T - GAP - 1, RZ0), xytext=(RX - LEG_T - GAP - 1, RZ0 + RH),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
    ax.text(RX - LEG_T - GAP - 3.5, RZ0 + RH / 2, "24.5", ha="center", va="center",
            rotation=90, fontsize=9, color=C_DIM)
    ax.text(leg_l - 1.0, RZ0 - 6.5, "腿", ha="center", fontsize=9, color="#a05a00")
    ax.text(leg_r + LEG_T + 1.0, RZ0 - 6.5, "腿", ha="center", fontsize=9, color="#a05a00")

    # ---------- panel 2: side view along the rack (Y-Z)
    ax2 = fig.add_axes([0.52, 0.42, 0.42, 0.50])
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_xlim(-40, 300)
    ax2.set_ylim(-16, 70)
    ax2.set_title("侧视（沿齿条方向 Y-Z）：齿条是固定的导轨，盒沿它走", fontsize=12, fontweight="bold")
    ax2.add_patch(Rectangle((0, 6), 243.3, 24.5, facecolor=C_RACK, edgecolor="k", lw=1.2))
    ax2.text(120, 18, "齿条 243.32 长（齿在两侧 ±X 面，pitch 1.63）",
             ha="center", va="center", fontsize=9)
    # moving bracket
    for y0 in (30, 150):
        ax2.add_patch(Rectangle((y0, -2), 70, 24.5 + 2 + 5 + 20, facecolor=C_ARCH,
                                edgecolor="k", lw=1.1, alpha=0.9))
        ax2.add_patch(plt.Circle((y0 + 70, 18), 6.5, facecolor="#ffd9a0", edgecolor="k", lw=1.0))
    ax2.annotate("", xy=(30, -8), xytext=(150, -8),
                 arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
    ax2.text(90, -12, "两个拱门（或一个更长的拱门）", ha="center", fontsize=9, color=C_DIM)
    ax2.add_patch(FancyArrowPatch((100, 55), (140, 55), arrowstyle="-|>",
                                  mutation_scale=14, color=C_RED, lw=1.8))
    ax2.text(100, 60, "上弦时这里受力 / 后座方向", fontsize=9, color=C_RED)

    fig.suptitle("g_mount_b 底部改成「拱门抱齿条」的方案示意（讨论用，未建模）",
                 fontsize=15, fontweight="bold", y=0.985)
    fig.text(0.05, 0.05,
             "要点：拱门两条腿贴齿条的两个侧面（±X），顶部跨过去；腿下穿一根 M4 通孔螺栓 + 螺母，"
             "用来夹紧或调间隙。\n"
             "好处：齿条的两个侧面变成定位基准，载荷从两侧直接传下去，不再靠一颗『平贴+8 颗螺栓』的接头吃弯矩。",
             fontsize=10, color="#333333")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
