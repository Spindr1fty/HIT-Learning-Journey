r"""Side elevation through the battery / main-controller stack.

Section at X = 75 (through the battery box), horizontal axis = chassis Y,
vertical axis = height above the chassis top face.

    python draw_chassis_heights.py  ->  renders/chassis_heights.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import chassis as C  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "chassis_heights.png"

STACK_H = 62.0       # battery box + main controller, total
bx0, by0, bx1, by1 = C.battery_outline()     # X 56.9..93.1, Y 19.9..110.2


def main():
    fig = plt.figure(figsize=(14.0, 8.4), dpi=200, facecolor="white")
    ax = fig.add_axes([0.07, 0.10, 0.90, 0.78])
    ax.set_xlim(-12, 272)
    ax.set_ylim(-14, 340)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(axis="y", color="#e9eef3", lw=0.8)
    for z in (62, 80, 129, 161, 203, 250, 275, 306, 320):
        ax.text(-8, z, f"{z}", fontsize=8, ha="right", va="center",
                color="#8a8f98")

    # chassis plate (thickness not fixed: draw 5)
    ax.add_patch(Rectangle((0, -5), C.H, 5, facecolor="#dbe9f7",
                           edgecolor="#12395e", lw=1.4))
    ax.text(4, -9.5, "底盘（厚度待定）", fontsize=8.5, color="#12395e")

    # battery + main controller stack
    ax.add_patch(Rectangle((by0, 0), by1 - by0, STACK_H, facecolor="#e6d8f5",
                           edgecolor="#6b3fa0", lw=1.6))
    ax.text((by0 + by1) / 2, STACK_H / 2, f"电池盒 + 主控盒\n总高 {STACK_H:.0f}",
            fontsize=10, ha="center", va="center", color="#6b3fa0")
    ax.annotate("", xy=(by1 + 6, 0), xytext=(by1 + 6, STACK_H),
                arrowprops=dict(arrowstyle="<->", color="#6b3fa0", lw=1.2))
    ax.text(by1 + 9, STACK_H / 2, "62", fontsize=10, color="#6b3fa0",
            va="center")

    # (left wheel plates live at X 0..40, so they are NOT in this section)

    # Z module: rack foot, rack mast, rail, carriage, cap
    ax.add_patch(Rectangle((129, 0), 32, 10, facecolor="#f2e2cf",
                           edgecolor="#a05a00", lw=1.2))
    ax.add_patch(Rectangle((138.5, 0), 20, 300, facecolor="#c8e8c8",
                           edgecolor="#2f6f2f", lw=1.0))
    ax.text(148.5, 240, "齿条\n(Z 0..300)", fontsize=7.6, ha="center",
            va="center", color="#2f6f2f")
    ax.add_patch(Rectangle((220, 0), 30, 320, facecolor="#c8e8c8",
                           edgecolor="#2f6f2f", lw=1.2))
    ax.text(235, 180, "导轨\n30×30\nZ 0..320", fontsize=7.8, ha="center",
            va="center", color="#2f6f2f")
    ax.add_patch(Rectangle((214, 80), 42, 195, facecolor="none",
                           edgecolor="#a05a00", lw=1.1, ls=(0, (4, 3))))
    ax.text(262, 190, "滑块\nZ 80..275", fontsize=7.8, va="center",
            color="#a05a00")
    ax.add_patch(Rectangle((131, 306), 124.4, 22, facecolor="none",
                           edgecolor="#2f6f2f", lw=1.1, ls=(0, (1, 3))))
    ax.text(200, 333, "顶盖 Z 306..328", fontsize=8, ha="center",
            color="#2f6f2f")
    ax.annotate("", xy=(266, -12), xytext=(196, -12),
                arrowprops=dict(arrowstyle="-|>", color="#c92a2a", lw=2.2))
    ax.text(272, -12, "前方 +Y", fontsize=9, color="#c92a2a", va="center")

    ax.set_title("侧视（剖在 X=75，穿过电池盒）：高度方向谁跟谁撞", fontsize=15,
                 fontweight="bold", pad=10)
    ax.set_xlabel("底盘 Y (mm)", fontsize=10)
    fig.text(0.07, 0.025,
             "电池盒+主控盒 62 高，前后 19.9~110.2；其前方最近的件是齿条脚（Y 129 起）——净空 19；"
             "上方没有任何件（升降机构全在 Y≥129，顶盖在 Z306 以上）→ 62 的高完全放得下。",
             fontsize=9.6, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
