r"""Concept drawing (schematic): g_mount_b base -> arch clamped on the rack.

    python draw_arch_concept.py -> renders/g_mount_b_arch_concept.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = r"D:\IceCup\renders\g_mount_b_arch_concept.png"

C_RACK = "#d5d8dc"
C_BOX = "#cfe0f0"
C_ARCH = "#f6d7b0"
C_SERVO = "#3a2a3a"
C_PADDLE = "#bfe6e8"
C_PLUNG = "#f2b8c6"
C_DIM = "#5b6773"
C_RED = "#c92a2a"
C_GRN = "#2f6f2f"


def main():
    fig = plt.figure(figsize=(18, 10), dpi=140, facecolor="white")

    # ================= panel 1: section A-A through the clamp (real scale)
    ax = fig.add_axes([0.03, 0.26, 0.40, 0.62])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-32, 34); ax.set_ylim(-20, 74)
    ax.set_title("① 剖面 A-A（横切 rack，真实比例）：拱门 + M4 通孔螺栓", fontsize=12,
                 fontweight="bold")

    RX, RW, RZ0, RH = -8.0, 16.0, 20.0, 24.5
    ax.add_patch(Rectangle((RX, RZ0), RW, RH, facecolor=C_RACK, edgecolor="k", lw=1.4, zorder=3))
    pitch, th = 1.63, 0.55
    for i in range(int(RH / pitch)):
        zz = RZ0 + 0.4 + i * pitch
        ax.add_patch(Rectangle((RX - th, zz), th, pitch * 0.5, facecolor=C_RACK,
                               edgecolor="k", lw=0.3, zorder=4))
        ax.add_patch(Rectangle((RX + RW, zz), th, pitch * 0.5, facecolor=C_RACK,
                               edgecolor="k", lw=0.3, zorder=4))
    ax.text(RX + RW / 2, RZ0 + RH / 2, "rack\n16 × 24.5", ha="center", va="center",
            fontsize=9, zorder=9)

    LEG_T, TOP_T, GAP = 4.5, 8.0, 0.3
    leg_l, leg_r = RX - LEG_T - GAP, RX + RW + GAP
    top_z = RZ0 + RH
    BOLT_Z = RZ0 - 6.0
    ax.add_patch(Rectangle((leg_l, top_z), leg_r + LEG_T - leg_l, TOP_T,
                           facecolor=C_ARCH, edgecolor="k", lw=1.4, zorder=5))
    for x0 in (leg_l, leg_r):
        ax.add_patch(Rectangle((x0, BOLT_Z - 3.0), LEG_T,
                               top_z + TOP_T - (BOLT_Z - 3.0),
                               facecolor=C_ARCH, edgecolor="k", lw=1.4, zorder=5))
    ax.plot([leg_l - 5, leg_r + LEG_T + 5], [BOLT_Z, BOLT_Z], color=C_RED, lw=2.4, zorder=8)
    ax.add_patch(Rectangle((leg_l - 5.6, BOLT_Z - 2.0), 2.9, 4.0, facecolor="#eeeeee",
                           edgecolor=C_RED, lw=1.0, zorder=9))
    ax.add_patch(Rectangle((leg_r + LEG_T + 2.7, BOLT_Z - 2.0), 2.9, 4.0,
                           facecolor="#eeeeee", edgecolor=C_RED, lw=1.0, zorder=9))
    ax.text(0, BOLT_Z - 5.5, "M4 螺栓 + 螺母（贯穿两腿夹紧）", ha="center",
            fontsize=9.5, color=C_RED)

    ax.add_patch(Rectangle((leg_l, top_z + TOP_T), leg_r + LEG_T - leg_l, 18,
                           facecolor=C_BOX, edgecolor="#12395e", lw=1.4,
                           ls=(0, (5, 3)), zorder=6))
    ax.text(0, top_z + TOP_T + 9, "盒子本体", ha="center",
            va="center", fontsize=9.5, color="#12395e")
    ax.text(leg_l - 1.6, RZ0 + RH / 2, "腿 4.5", fontsize=8.5, color="#a05a00",
            ha="center", va="center", rotation=90)
    ax.text(leg_r + LEG_T + 1.6, RZ0 + RH / 2, "腿 4.5", fontsize=8.5, color="#a05a00",
            ha="center", va="center", rotation=90)
    ax.text(0, top_z + TOP_T / 2, "顶 8", ha="center", va="center", fontsize=8.5,
            color="#a05a00", zorder=10)
    ax.annotate("", xy=(leg_l, RZ0 - 2.2), xytext=(RX, RZ0 - 2.2),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.annotate("", xy=(leg_r + LEG_T, RZ0 - 2.2), xytext=(RX + RW, RZ0 - 2.2),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.text(0, RZ0 - 4.8, "每侧留 0.3 间隙", ha="center", fontsize=8, color=C_DIM)
    ax.text(-30, top_z + TOP_T + 2, "总宽\n25.6\n= 16+2×(0.3+4.5)", fontsize=8.5, color=C_DIM,
            ha="left", va="center")

    # ================= panel 2: schematic plan (X-Y) of the launcher front end
    ax2 = fig.add_axes([0.47, 0.26, 0.51, 0.62])
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_xlim(100, 225); ax2.set_ylim(-30, 275)
    ax2.set_title("② 示意（俯视 X-Y，不按比例）：盒子骑在 rack 前端，挡板伸向 plunger",
                  fontsize=12, fontweight="bold")

    ax2.add_patch(Rectangle((111, 4), 99, 252, facecolor="#f4f7fa", edgecolor="#aab4c0",
                            lw=1.2, ls=(0, (4, 3))))
    ax2.text(118, 268, "base_plate 轮廓", fontsize=8.5, color="#7a8794")

    ax2.add_patch(Rectangle((129, 4), 16, 251.3, facecolor=C_PLUNG, edgecolor="k",
                            lw=1.1, alpha=0.85))
    ax2.text(137, 268, "plunger", fontsize=9, ha="center", color="#8a1f3a")
    ax2.add_patch(Rectangle((172, 12), 16, 243.3, facecolor=C_RACK, edgecolor="k", lw=1.1))
    ax2.text(180, 268, "rack", fontsize=9, ha="center")
    for xx in (176.0, 184.0):
        ax2.add_patch(plt.Circle((xx, 255.3), 2.4, facecolor="white", edgecolor=C_RED, lw=1.2))
    ax2.annotate("前端面螺孔\n（老薄板固定点）", xy=(180, 255.3), xytext=(196, 236),
                 fontsize=8, color=C_RED,
                 arrowprops=dict(arrowstyle="->", color=C_RED, lw=0.9))

    BX0, BY0, BW, BL = 148, 208, 40, 74.5
    ax2.add_patch(Rectangle((BX0, BY0), BW, BL, facecolor=C_BOX, edgecolor="#12395e",
                            lw=1.6, ls=(0, (5, 3)), alpha=0.55, zorder=6))
    ax2.text(BX0 - 34, BY0 + BL + 8, "g_mount_b 盒子\n40 × 74.5（俯视）", fontsize=8.5,
             color="#12395e")
    ax2.add_patch(Rectangle((BX0, BY0), 172 - BX0, BL, facecolor=C_ARCH, edgecolor="k",
                            lw=1.0, alpha=0.9, zorder=7))
    ax2.add_patch(Rectangle((188, BY0), BX0 + BW - 188, BL, facecolor=C_ARCH, edgecolor="k",
                            lw=1.0, alpha=0.9, zorder=7))
    ax2.text(160, BY0 + BL / 2, "左腿\n贴 −X\n齿面", fontsize=7.5, ha="center",
             va="center", zorder=8)
    ax2.text(194, BY0 + BL / 2, "右腿\n贴 +X\n齿面", fontsize=7.5, ha="center",
             va="center", zorder=8)

    ax2.add_patch(Rectangle((BX0 + 14, BY0 + 17), 20, 40, facecolor=C_SERVO, edgecolor="k",
                            lw=0.9, zorder=9))
    ax2.text(BX0 + 24, BY0 + 37, "舵机", fontsize=7.5, color="w", ha="center", va="center",
             rotation=90, zorder=10)
    pivot = (BX0 + 20, BY0 + 20)
    ax2.add_patch(Polygon([[pivot[0], pivot[1]], [pivot[0] - 78, pivot[1] - 26],
                           [pivot[0] - 78, pivot[1] - 52], [pivot[0], pivot[1] - 42]],
                          closed=True, facecolor=C_PADDLE, edgecolor="k", lw=1.0,
                          alpha=0.85, zorder=6))
    ax2.annotate("挡板 91×46，臂长 78\n前端 26×20 钩子 → 卡 plunger",
                 xy=(pivot[0] - 70, pivot[1] - 40), xytext=(104, 150),
                 fontsize=8.5, color="#0e5c60",
                 arrowprops=dict(arrowstyle="->", color="#0e5c60", lw=0.9))

    ax2.add_patch(FancyArrowPatch((180, 120), (180, 160), arrowstyle="-|>",
                                  mutation_scale=14, color=C_RED, lw=1.8))
    ax2.text(184, 128, "rack 前后移动\n（底板立柱舵机）", fontsize=8.5, color=C_RED)
    ax2.add_patch(FancyArrowPatch((137, 120), (137, 160), arrowstyle="-|>",
                                  mutation_scale=14, color=C_GRN, lw=1.8))
    ax2.text(118, 128, "plunger 弹射方向", fontsize=8.5, color=C_GRN)

    # ================= notes
    notes = (
        "还需你给的数据（图上尺寸都能改）：\n"
        "① rack 前端面螺孔：几颗、孔径、离顶面/底面多少？（图上 2 × Ø4.5 只是示意）\n"
        "② 老 g_mount_b 的舵机轴位置：离 rack 顶面多高？轴心离前端面多远？（决定盒子放哪、挡板能不能够到 plunger）\n"
        "③ rack 下方有没有 >=10 mm 空间走 M4 螺栓+螺母？（图上螺栓在 rack 底面以下 6 mm 处）\n"
        "④ 挡板是「竖着放下」（舵机轴水平）还是「横扫」（舵机轴竖直）？plunger 上卡挡板的是槽还是端面？\n\n"
        "结构：脚板 -> 拱门；拱门顶面坐在 rack 顶面上，两条腿沿 rack 两侧齿面下来，\n"
        "M4 螺栓从 rack 下方贯穿两腿、螺母收紧夹死。舵机、法兰 4 孔、背面开口、包围墙全部保留。"
    )
    fig.text(0.03, 0.115, notes, fontsize=10, color="#222222", va="top",
             bbox=dict(boxstyle="round,pad=0.6", fc="#fbf7ef", ec="#d8c9a8"))

    fig.suptitle("g_mount_b 新方案：脚板 -> 拱门抱 rack（概念图，等你确认再建模）",
                 fontsize=16, fontweight="bold", y=0.975)
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
