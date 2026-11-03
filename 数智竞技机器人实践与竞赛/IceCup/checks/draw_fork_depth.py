r"""Why a 21 mm working end fixes the fork: depth budget picture.

    python draw_fork_depth.py  ->  renders/fork_depth_budget.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(r"D:\IceCup\renders\fork_depth_budget.png")

CELL = 58.0
STONE_D = 47.0
STEM_FWD = 23.5
STEM_BACK = 35.0
L_OLD = 54.0
L_NEW = 21.0


def frame(ax, title):
    ax.set_xlim(-3, 100)
    ax.set_ylim(-4.4, 6.4)
    ax.axis("off")
    ax.set_title(title, fontsize=12.5, fontweight="bold", pad=6)
    ax.add_patch(Rectangle((0, 5.3), CELL, 0.9, facecolor="#dbe9f7",
                           edgecolor="#12395e", lw=1.2))
    ax.add_patch(Rectangle((CELL, 5.3), 2.0, 0.9, facecolor="#c92a2a",
                           edgecolor="#c92a2a", lw=1.2, hatch="//"))
    ax.text(CELL / 2, 5.75, "格子内深 58", fontsize=8.5, ha="center",
            va="center", color="#12395e")
    ax.text(CELL + 3.4, 5.75, "亚克力背板", fontsize=8, va="center",
            color="#c92a2a")
    # stone body outlines at both extremes, stem mark at the centre
    for d, lab in ((STEM_FWD, "壶最靠前"), (STEM_BACK, "壶最靠后")):
        ax.add_patch(Rectangle((d - STONE_D / 2, 3.1), STONE_D, 1.4,
                               facecolor="none", edgecolor="#a8adb5", lw=1.0,
                               ls=(0, (4, 3))))
        ax.plot([d, d], [2.7, 4.6], color="#6b7280", lw=2.4)
        ax.text(d, 4.85, f"{lab}\n{d:.0f}", fontsize=7.4, ha="center",
                va="bottom", color="#5b6773")


def old(ax):
    frame(ax, f"现在：叉头 {L_OLD:.0f}  —— 叉尖先撞背板")
    d0 = CELL - L_OLD                      # 4
    ax.add_patch(Rectangle((d0, 0.9), L_OLD, 0.8, facecolor="#f7d9d9",
                           edgecolor="#c92a2a", lw=1.4))
    ax.plot([d0, d0], [0.55, 2.0], color="#c92a2a", lw=2.2)
    ax.text(d0 - 1.2, 0.3, "闭合端 4", fontsize=7.6, ha="left", color="#c92a2a")
    ax.text(d0 + L_OLD / 2, 1.3, f"叉头 {L_OLD:.0f}（插到 58 就停了）",
            fontsize=8.6, ha="center", va="center", color="#c92a2a")
    for y, d in ((-0.6, STEM_FWD), (-1.7, STEM_BACK)):
        ax.annotate("", xy=(d0, y), xytext=(d, y),
                    arrowprops=dict(arrowstyle="<->", color="#c92a2a", lw=1.1))
        ax.text((d0 + d) / 2, y - 0.45, f"手柄离闭合端 {d - d0:.0f}",
                fontsize=8, ha="center", color="#c92a2a")
    ax.text(-1, -3.6, "叉尖顶到 58 就进不去了 → 手柄永远到不了闭合端，壶只搭在漏斗口上。",
            fontsize=9, color="#495057", va="top")


def new(ax):
    frame(ax, f"改后：叉头 {L_NEW:.0f}  —— 手柄被顶到闭合端，再往外推壶")
    d0 = STEM_BACK                         # the stone gets pushed to the back
    ax.add_patch(Rectangle((d0, 0.9), L_NEW, 0.8, facecolor="#c8e8c8",
                           edgecolor="#2f6f2f", lw=1.4))
    ax.plot([d0, d0], [0.55, 2.0], color="#2f6f2f", lw=2.2)
    ax.text(d0 - 1.2, 0.3, "闭合端 = 手柄", fontsize=7.6, ha="left",
            color="#2f6f2f")
    ax.text(d0 + L_NEW / 2, 1.3, f"叉头 {L_NEW:.0f}", fontsize=8.6,
            ha="center", va="center", color="#2f6f2f")
    ax.annotate("", xy=(CELL, 2.2), xytext=(d0 + L_NEW, 2.2),
                arrowprops=dict(arrowstyle="<->", color="#2f6f2f", lw=1.0))
    ax.text((d0 + L_NEW + CELL) / 2, 2.35, "余 2", fontsize=8, ha="center",
            color="#2f6f2f")
    ax.plot([STEM_FWD, STEM_FWD], [2.7, 4.6], color="#c8c8c8", lw=2.4)
    ax.text(STEM_BACK + 2.0, 2.9, "壶被推到格子最里（手柄 = 闭合端）", fontsize=8.2,
            color="#2f6f2f", va="bottom")
    ax.text(-1, -3.6,
            "手柄每次都被推到闭合端 → 壶居中在叉头上；叉尖最深 56，离背板还有 2。",
            fontsize=9, color="#495057", va="top")


def main():
    fig = plt.figure(figsize=(16.0, 7.6), dpi=200, facecolor="white")
    old(fig.add_axes([0.04, 0.55, 0.92, 0.36]))
    new(fig.add_axes([0.04, 0.09, 0.92, 0.36]))
    fig.suptitle("取壶叉深度预算：格子内深 58、手柄深度 23.5~35 → 叉头必须 ≤ 23.5",
                 fontsize=14.5, fontweight="bold", y=0.965)
    fig.text(0.04, 0.015,
             "托架不用改：勾取点（闭合端）在安装块前面 12mm，由托架位置决定；缩短叉头只是把"
             "“超出勾取点的部分”从 54 减到 21，勾取点相对机器一点没动，安装孔仍是原来的 2×M4（Y±12，Z13）。",
             fontsize=9.4, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
