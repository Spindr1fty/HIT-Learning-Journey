r"""Now vs proposed: the servo mount on the vertical rack (g_mount_b), for discussion.

    python draw_arch_now_proposed.py -> renders/g_mount_b_now_vs_arch.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = r"D:\IceCup\renders\g_mount_b_now_vs_arch.png"

C_RACK = "#d8d8d8"
C_PLATE = "#f2f2f2"
C_SERVO = "#3a2a3a"
C_ARM = "#bfe6e8"
C_ARCH = "#f6d7b0"
C_DIM = "#5b6773"
C_RED = "#c92a2a"
C_GRN = "#2f6f2f"


def rack(ax, x0, y0, w=16.0, h=24.5):
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=C_RACK, edgecolor="k", lw=1.3, zorder=2))
    pitch = 1.63
    n = int(h / pitch)
    for i in range(n):
        yy = y0 + 0.6 + i * pitch
        for sign in (0, 1):
            xx = x0 - 0.55 if sign == 0 else x0 + w
            ax.add_patch(Rectangle((xx, yy), 0.55, pitch * 0.55, facecolor=C_RACK,
                                   edgecolor="k", lw=0.4, zorder=3))


def servo(ax, cx, cy):
    ax.add_patch(Rectangle((cx - 20, cy - 10), 40, 20, facecolor=C_SERVO,
                           edgecolor="k", lw=1.0, zorder=6))
    ax.add_patch(Rectangle((cx - 22.5, cy - 2), 5, 4, facecolor="#8a7a8a",
                           edgecolor="k", lw=0.6, zorder=6))


def main():
    fig = plt.figure(figsize=(17, 9), dpi=130, facecolor="white")

    # ---------------- left: NOW (thin plate cantilevered from the carriage)
    ax = fig.add_axes([0.04, 0.10, 0.44, 0.80])
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-30, 70); ax.set_ylim(-40, 150)
    ax.set_title("现在：竖直薄板从滑块上「悬臂」出来", fontsize=13, fontweight="bold")
    rack(ax, 0, 0, 16, 130)
    # carriage block
    ax.add_patch(Rectangle((20, -20), 44, 20, facecolor="#e9e9e9", edgecolor="k", lw=1.1, zorder=4))
    ax.text(42, -10, "滑块", ha="center", va="center", fontsize=9)
    # thin vertical plate standing on the carriage
    ax.add_patch(Rectangle((40, 0), 5, 95, facecolor=C_PLATE, edgecolor="k", lw=1.2, zorder=5))
    ax.text(42.5, 100, "薄板\n(现在这样)", ha="center", fontsize=9, color="#444444")
    servo(ax, 62, 62)
    ax.plot([42.5, 42.5], [62, 62], color="k", lw=0.5)
    # transparent arm on the horn
    ax.add_patch(Rectangle((60, 52), 34, 3.5, facecolor=C_ARM, edgecolor="k", lw=0.8, alpha=0.75, zorder=7))
    ax.add_patch(plt.Circle((82, 53.7), 2.2, facecolor="w", edgecolor="k", lw=0.7, zorder=8))
    ax.text(96, 54, "亚克力摆臂", fontsize=8.5, va="center")
    # moment arrow
    ax.add_patch(FancyArrowPatch((42.5, 20), (42.5, 42), arrowstyle="-|>", mutation_scale=14,
                                 color=C_RED, lw=1.6, zorder=9))
    ax.text(30, 30, "弯矩", fontsize=10, color=C_RED, rotation=90, va="center")
    ax.annotate("载荷 → 薄板根部吃弯矩\n舵机轴随板一起偏",
                xy=(43, 12), xytext=(58, 8), fontsize=9, color=C_RED,
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0))

    # ---------------- right: PROPOSED (arch straddling the rack)
    ax2 = fig.add_axes([0.52, 0.10, 0.44, 0.80])
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_xlim(-30, 70); ax2.set_ylim(-40, 150)
    ax2.set_title("改成：拱门抱住齿条（齿条当导轨/定位基准）", fontsize=13, fontweight="bold")
    rack(ax2, 0, 0, 16, 130)
    GAP, LEG, TOP = 0.3, 4.0, 5.0
    # legs + top bridge
    ax2.add_patch(Rectangle((-LEG - GAP, -30), LEG, 135 + TOP, facecolor=C_ARCH,
                            edgecolor="k", lw=1.2, zorder=5))
    ax2.add_patch(Rectangle((16 + GAP, -30), LEG, 135 + TOP, facecolor=C_ARCH,
                            edgecolor="k", lw=1.2, zorder=5))
    ax2.add_patch(Rectangle((-LEG - GAP, 130), 16 + 2 * LEG + 2 * GAP, TOP, facecolor=C_ARCH,
                            edgecolor="k", lw=1.2, zorder=5))
    ax2.text(-26, 140, "顶部跨过齿条", fontsize=9, ha="left", color="#a05a00")
    # plate / box on the arch (now cantilever length ~0)
    ax2.add_patch(Rectangle((16 + GAP + LEG, 55), 5, 40, facecolor=C_PLATE,
                            edgecolor="k", lw=1.2, zorder=6))
    servo(ax2, 46, 75)
    ax2.add_patch(Rectangle((44, 65), 34, 3.5, facecolor=C_ARM, edgecolor="k", lw=0.8,
                            alpha=0.75, zorder=7))
    # bolt below the rack
    BZ = -22
    ax2.plot([-LEG - GAP - 5, 16 + GAP + LEG + 5], [BZ, BZ], color=C_RED, lw=2.2, zorder=8)
    ax2.add_patch(Rectangle((-LEG - GAP - 5.5, BZ - 2), 2.6, 4, facecolor="#eee",
                            edgecolor=C_RED, lw=1.0, zorder=9))
    ax2.add_patch(Rectangle((16 + GAP + LEG + 2.9, BZ - 2), 2.6, 4, facecolor="#eee",
                            edgecolor=C_RED, lw=1.0, zorder=9))
    ax2.text(-26, BZ - 6, "M4 通孔+螺母：\n只防脱 / 调预紧，不夹死", fontsize=9,
             ha="left", color=C_RED)
    ax2.annotate("两条腿贴齿条两侧\n载荷直接从两侧传下去",
                 xy=(2, 60), xytext=(-26, 90), fontsize=9, color="#a05a00",
                 arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))
    ax2.add_patch(FancyArrowPatch((20, -2), (20, -14), arrowstyle="-|>", mutation_scale=12,
                                  color=C_GRN, lw=1.4))
    ax2.text(24, 20, "齿条固定不动\n(小齿轮带着拱门上下爬)", fontsize=8.5, va="center",
             color=C_GRN)

    fig.suptitle("g_mount_b 挂在竖直齿条上：现在 vs 拱门方案（讨论用，未建模）",
                 fontsize=15, fontweight="bold", y=0.98)
    fig.text(0.04, 0.02,
             "照片里的现状：伺服用两根长螺丝锁在一块竖直薄板上，薄板只靠底部一小块连在滑块上 → 悬臂受力，"
             "上弦/后座时盒子和输出轴一起偏。\n"
             "拱门方案：改由齿条的两个侧面当定位基准，顶部跨过去，腿下穿一颗 M4（只防脱/调间隙，因为齿条是固定导轨，"
             "抱死了滑块就走不动）。",
             fontsize=10, color="#333333")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
