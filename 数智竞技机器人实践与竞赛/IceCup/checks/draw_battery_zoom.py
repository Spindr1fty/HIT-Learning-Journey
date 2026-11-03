r"""Zoom on the battery box: which way its 90.3 long edge runs.

    python draw_battery_zoom.py  ->  renders/battery_orientation.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import chassis as C  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "battery_orientation.png"


def main():
    fig = plt.figure(figsize=(11.0, 11.5), dpi=180, facecolor="white")
    ax = fig.add_axes([0.08, 0.10, 0.86, 0.80])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(20, 140)
    ax.set_ylim(-4, 150)

    # neighbours
    for g in C.wheel_groups():
        fx0, fy0, fx1, fy1 = g["foot"]
        ax.add_patch(Rectangle((fx0, fy0), fx1 - fx0, fy1 - fy0,
                               facecolor="#c9d9e8", edgecolor="#12395e",
                               lw=1.2, zorder=2, alpha=0.8))
    ax.add_patch(Rectangle(C.BASE_PLATE_BOX[:2],
                           C.BASE_PLATE_BOX[2] - C.BASE_PLATE_BOX[0],
                           C.BASE_PLATE_BOX[3] - C.BASE_PLATE_BOX[1],
                           facecolor="#ffe0b8", edgecolor="#a05a00", lw=1.4,
                           zorder=2, alpha=0.8))
    ax.add_patch(Rectangle((C.Z_X0 - 22, C.Z_Y0 - 106), 44, 32,
                           facecolor="#f2e2cf", edgecolor="#a05a00", lw=1.2,
                           zorder=2))
    for x, y, _ in C.all_holes():
        ax.add_patch(Circle((x, y), C.HOLE_D / 2, facecolor="white",
                            edgecolor="#8a8f98", lw=0.8, zorder=5))

    bx0, by0, bx1, by1 = C.battery_outline()
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           facecolor="#e6d8f5", edgecolor="#6b3fa0", lw=2.2,
                           zorder=6))
    for x, y in C.battery_holes():
        ax.add_patch(Circle((x, y), 2.25, facecolor="white",
                            edgecolor="#6b3fa0", lw=1.6, zorder=8))
    # 36.2 across X
    ax.annotate("", xy=(bx0, by1 + 6), xytext=(bx1, by1 + 6),
                arrowprops=dict(arrowstyle="<->", color="#6b3fa0", lw=1.6))
    ax.text((bx0 + bx1) / 2, by1 + 8.5, "36.2  ← 沿 X（横向）", fontsize=11,
            ha="center", color="#6b3fa0")
    # 90.3 along Y
    ax.annotate("", xy=(bx1 + 6, by0), xytext=(bx1 + 6, by1),
                arrowprops=dict(arrowstyle="<->", color="#6b3fa0", lw=1.6))
    ax.text(bx1 + 9, (by0 + by1) / 2, "90.3  ← 沿 Y（前后方向）", fontsize=11,
            color="#6b3fa0", va="center", rotation=90)
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2,
            "电池盒 + 主控\n长边沿 Y = 前后\n（现在就是竖着）", fontsize=11,
            ha="center", va="center", color="#6b3fa0")
    # neighbour labels
    ax.text(20, 120, "左后轮板", fontsize=9, color="#12395e")
    ax.text(113, 130, "发射机构底板\n(X 111 起)", fontsize=9, color="#a05a00")
    ax.text(68, 124, "齿条脚\n(Y 129 起)", fontsize=8.5, ha="center",
            color="#a05a00")
    ax.text(20, 8, "X 向右（横向）→\nY 向前 ↑", fontsize=9.5, color="#495057")
    ax.text(80, -1, "4 孔：(67,25.05)(67,104.95)(83,25.05)(83,104.95)",
            fontsize=8.5, ha="center", color="#6b3fa0")
    fig.suptitle("电池盒方向确认：36.2 在 X，90.3 在 Y", fontsize=14,
                 fontweight="bold", y=0.955)
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
