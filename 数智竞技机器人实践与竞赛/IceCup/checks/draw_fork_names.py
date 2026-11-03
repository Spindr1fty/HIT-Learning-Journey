r"""Naming sketch for the fork head (g_fork), so we stop talking past each other.

Two views, both measured off src/g_fork.py:

    A  plan view, looking down the Z axis at the working plate
    B  side view, looking along Y, showing the plate thickness and the back plate
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

X_CLOSED = 0.0
X_TINE_END = 12.0
X_MOUTH = 42.0
X_BACK0, X_BACK1 = -12.0, -4.0
MOUTH_HALF = 24.0
TINE_IN = 5.7
PLATE_HALF = 26.0
THICK = 3.5
PLATE_Z = (0.0, 26.0)
C_PLATE = "#d0ebff"
C_VOID = "#ffffff"
C_BACK = "#ffe8cc"


def panel_a(ax):
    ax.set_xlim(-18, 62)
    ax.set_ylim(-32, 32)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("A. 俯视（从 Z 方向看下去）", fontsize=13, fontweight="bold")

    ax.add_patch(Rectangle((X_BACK0, -PLATE_HALF),
                           X_MOUTH - X_BACK0, 2 * PLATE_HALF,
                           facecolor=C_PLATE, edgecolor="#0b4f8a", lw=1.6))
    void = [(X_MOUTH, -MOUTH_HALF), (X_TINE_END, -TINE_IN),
            (X_CLOSED, -TINE_IN), (X_CLOSED, TINE_IN),
            (X_TINE_END, TINE_IN), (X_MOUTH, MOUTH_HALF),
            (X_MOUTH + 6, MOUTH_HALF), (X_MOUTH + 6, -MOUTH_HALF)]
    ax.add_patch(Polygon(void, closed=True, facecolor=C_VOID,
                         edgecolor="#e03131", lw=1.4))
    ax.add_patch(Rectangle((X_BACK0, -20), X_BACK1 - X_BACK0, 40,
                           facecolor=C_BACK, edgecolor="#a05a00", lw=1.8))

    ax.annotate("① 工作板（漏斗板）\n厚 3.5，下面塞进顶盖和壶肩之间的 7.5 空当",
                xy=(-8, 22), xytext=(-16, 31), fontsize=9.5, color="#0b4f8a")
    ax.annotate("② 背板\nX -12~-4，Y ±20，Z 0~26",
                xy=(-8, 0), xytext=(14, 31), fontsize=9.5, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.2))
    ax.annotate("③ 两个安装孔 Ø4.5\nY ±12，Z 13",
                xy=(-8, 12), xytext=(20, 27), fontsize=9, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.0))
    ax.annotate("④ 漏斗嘴（开口）\nX=42，宽 48",
                xy=(45, 18), xytext=(46, 6), fontsize=9.5, color="#e03131")
    ax.annotate("⑤ 锥度段\nX 12→42，收 48→11.4",
                xy=(26, 10), xytext=(30, -20), fontsize=9.5, color="#e03131",
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=1.0))
    ax.annotate("⑥ 平行槽\n宽 11.4，长 12",
                xy=(6, 0), xytext=(20, -28), fontsize=9.5, color="#e03131",
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=1.0))
    ax.annotate("⑦ 封底\nX=0", xy=(0, 0), xytext=(-16, -28), fontsize=9.5,
                color="#e03131",
                arrowprops=dict(arrowstyle="->", color="#e03131", lw=1.0))
    ax.annotate("⑧ 两臂（勾顶盖的部分）\n内面 Y=±5.7，外缘 Y=±8.7 勾住 Ø18 顶盖",
                xy=(30, 6), xytext=(-16, -34), fontsize=9.5, color="#2f9e44")
    ax.set_xlabel("X", fontsize=9)
    ax.set_ylabel("Y", fontsize=9)


def panel_b(ax):
    ax.set_xlim(-16, 48)
    ax.set_ylim(-4, 30)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("B. 侧视（从 Y 方向看）", fontsize=13, fontweight="bold")

    ax.add_patch(Rectangle((X_BACK0, 0), X_MOUTH - X_BACK0, THICK,
                           facecolor=C_PLATE, edgecolor="#0b4f8a", lw=1.6))
    ax.add_patch(Rectangle((X_BACK0, PLATE_Z[0]), X_BACK1 - X_BACK0,
                           PLATE_Z[1] - PLATE_Z[0],
                           facecolor=C_BACK, edgecolor="#a05a00", lw=1.8))
    ax.text(-9, 13, "② 背板", fontsize=9.5, ha="center", color="#a05a00")
    ax.text(20, 5.2, "① 工作板 厚 3.5", fontsize=9.5, color="#0b4f8a")
    ax.set_xlabel("X", fontsize=9)
    ax.set_ylabel("Z", fontsize=9)


def main(out):
    fig = plt.figure(figsize=(15, 7.4), dpi=115)
    panel_a(fig.add_axes([0.03, 0.06, 0.56, 0.80]))
    panel_b(fig.add_axes([0.64, 0.06, 0.34, 0.80]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "fork_names.png")
