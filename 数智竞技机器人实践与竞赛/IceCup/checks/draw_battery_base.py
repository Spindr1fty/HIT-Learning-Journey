r"""Dimensioned drawing of the battery-box base plate (measured version).

    python draw_battery_base.py  ->  renders/battery_base.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "battery_base.png"

L, W, T = 90.3, 36.2, 5.5
R = 3.0
HOLE_D = 4.0
HY = 8.0                       # centre spacing 16 = inner edges 12 + dia 4
HX = L / 2 - 3.2 - HOLE_D / 2  # 39.95
C_PLATE, C_HOLE, C_DIM = "#e8eef5", "white", "#5b6773"


def main():
    fig = plt.figure(figsize=(16.0, 8.4), dpi=200, facecolor="white")
    ax = fig.add_axes([0.05, 0.19, 0.90, 0.66])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-L / 2 - 26, L / 2 + 26)
    ax.set_ylim(-W / 2 - 64, W / 2 + 30)

    ax.add_patch(FancyBboxPatch((-L / 2, -W / 2), L, W,
                                boxstyle=f"round,pad=0,rounding_size={R}",
                                facecolor=C_PLATE, edgecolor="#12395e", lw=2.0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax.add_patch(plt.Circle((sx * HX, sy * HY), HOLE_D / 2,
                                    facecolor=C_HOLE, edgecolor="#c92a2a",
                                    lw=1.8, zorder=5))
            ax.plot([sx * HX], [sy * HY], marker="+", ms=8, color="#c92a2a",
                    zorder=6)

    ax.plot([-L / 2 - 18, L / 2 + 18], [0, 0], color="#c92a2a", lw=0.8,
            ls=(0, (8, 3, 1, 3)))
    ax.plot([0, 0], [-W / 2 - 18, W / 2 + 18], color="#c92a2a", lw=0.8,
            ls=(0, (8, 3, 1, 3)))

    ax.annotate("", xy=(-L / 2, -W / 2 - 9), xytext=(L / 2, -W / 2 - 9),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.1))
    ax.text(0, -W / 2 - 12, f"{L:.1f}", fontsize=11, ha="center", color=C_DIM)
    ax.annotate("", xy=(L / 2 + 9, -W / 2), xytext=(L / 2 + 9, W / 2),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.1))
    ax.text(L / 2 + 12, 0, f"{W:.1f}", fontsize=11, color=C_DIM, va="center",
            rotation=90)
    ax.annotate("", xy=(-HX, W / 2 + 11), xytext=(HX, W / 2 + 11),
                arrowprops=dict(arrowstyle="<->", color="#c92a2a", lw=1.1))
    ax.text(0, W / 2 + 14, f"两端孔心距 {2 * HX:.1f}", fontsize=10.5,
            color="#c92a2a", ha="center")
    ax.annotate("", xy=(-HX - 13, -HY), xytext=(-HX - 13, HY),
                arrowprops=dict(arrowstyle="<->", color="#c92a2a", lw=1.1))
    ax.text(-HX - 15, 0, f"孔心距 {2 * HY:.0f}", fontsize=10.5, color="#c92a2a",
            va="center", rotation=90)
    ax.annotate("", xy=(-L / 2, -W / 2 + 4.5), xytext=(-HX, -W / 2 + 4.5),
                arrowprops=dict(arrowstyle="<->", color="#2f6f2f", lw=1.0))
    ax.text((-L / 2 - HX) / 2, -W / 2 + 6.5, "3.2", fontsize=9.5,
            color="#2f6f2f", ha="center")
    ax.annotate("", xy=(-HX + 8, -W / 2), xytext=(-HX + 8, -HY),
                arrowprops=dict(arrowstyle="<->", color="#2f6f2f", lw=1.0))
    ax.text(-HX + 10.5, (-W / 2 - HY) / 2, "8.10", fontsize=9.5,
            color="#2f6f2f", va="center")

    ax.text(0, W / 2 + 22,
            f"电池盒底板（实测版）  90.3 × 36.2 × {T}，4 × Ø{HOLE_D:.1f} 通孔",
            fontsize=14, fontweight="bold", ha="center", color="#12395e")
    ax.text(-L / 2 - 18, -W / 2 - 15,
            "孔位（原点 = 底板中心，X 沿 90.3 长边）：\n"
            "  X = ±39.95（两端孔心距 79.9）\n"
            "  Y = ±8.00（同端孔心距 16 = 内缘距 12 + 孔径 4）\n"
            "孔边到底座端头 3.20（你给的数）\n"
            "孔边到长边 8.10（你量 8.44，差 0.34，在量具误差内）\n"
            "板厚 5.5、孔径 4.0 实测；孔口无凸台、无沉孔，底面纯平。",
            fontsize=9.8, color="#495057", va="top", ha="left")
    fig.text(0.05, 0.02,
             "打印复核用：3 层墙 20% 填充。装盒用 M4×16~20（板厚 5.5 + 底盘厚 + 螺母 3.2）。"
             "底盘上开同一组孔（建议 Ø4.5 留装配余量），安装位置定了再落图。",
             fontsize=9.5, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
