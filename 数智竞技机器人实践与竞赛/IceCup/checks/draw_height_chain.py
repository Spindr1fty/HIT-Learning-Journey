r"""Height chain: the one inequality that fixes the chassis and Z-axis heights.

The rack's measured cell floors are at 19 / 107 / 191 mm. The fork's tines must
sit 23.7 mm above each floor, so at 42.7 / 130.7 / 214.7 mm. The Z axis moves
the tines through a 230 mm stroke and the three heights span 172 mm, leaving
58 mm of slack.

Two numbers are still open:

    M   the Z-axis module's datum, i.e. its base plate's top, above the table
    D   how far the tines hang BELOW the carriage's centre

Working the geometry through in the module frame:

    tine, lowest  = 42.7  - M      carriage centre, lowest  = 45
    tine, highest = 214.7 - M      carriage centre, highest = 275
    tine = carriage centre - D

    D - M >= 2.3     so the bottom row can be reached
    D - M <= 60.3    so the top row can be reached

It is not C and M separately that matter -- only (D - M), inside a 58 mm window.
That is exactly the stroke margin, 230 - 172.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

FLOORS = (19.0, 107.0, 191.0)
CELL_H = 80.0
TINE_OFF = 23.7
TINES = tuple(f + TINE_OFF for f in FLOORS)
RACK_TOP = 19.0 + 305.0
MARGIN = 230.0 - (TINES[2] - TINES[0])

STONE = "#c8a06a"
STONE_EDGE = "#8a6a3a"
FORK = "#1c7ed6"
OK = "#2f9e44"


def main(out):
    fig = plt.figure(figsize=(16, 10), dpi=110)
    ax = fig.add_axes([0.04, 0.05, 0.42, 0.83])
    ax.set_xlim(-1.2, 7.6)
    ax.set_ylim(-14, RACK_TOP + 22)
    ax.axis("off")

    # table
    ax.plot([-1.0, 7.4], [0, 0], color="#212529", lw=3.0)
    ax.text(6.9, -7, "台面 0", fontsize=10, ha="right")

    # rack
    ax.add_patch(Rectangle((0.3, FLOORS[0]), 1.5, RACK_TOP - FLOORS[0],
                           facecolor="#f1f3f5", edgecolor="#adb5bd",
                           lw=1.3, ls=(0, (5, 3))))
    for f in FLOORS:
        ax.add_patch(Rectangle((0.3, f), 1.5, CELL_H, facecolor=STONE,
                               alpha=0.20, edgecolor=STONE_EDGE, lw=1.2))
        ax.add_patch(Rectangle((0.55, f), 1.0, 32.0, facecolor=STONE,
                               alpha=0.55, edgecolor=STONE_EDGE, lw=1.0))
        ax.text(1.05, f + 16, "壶", fontsize=8.5, ha="center", va="center",
                color=STONE_EDGE)
        ax.text(1.05, f - 5, f"{f:.0f}", fontsize=8.5, ha="center",
                color="#868e96")
    ax.text(1.05, RACK_TOP + 6, "壶架 305\n(13 埋台下)", fontsize=9,
            ha="center", color="#495057")

    # tine heights
    for t, f in zip(TINES, FLOORS):
        ax.plot([2.3, 3.4], [t, t], color=FORK, lw=3.0,
                solid_capstyle="round")
        ax.text(3.6, t, f"{t:.1f}", fontsize=11, va="center", color=FORK,
                fontweight="bold")
        ax.annotate("", xy=(2.2, f), xytext=(2.2, t),
                    arrowprops=dict(arrowstyle="<->", color="#ced4da", lw=1.0))
    ax.text(3.6, TINES[2] + 10, "托叉高度", fontsize=10, color=FORK,
            fontweight="bold")

    # span bracket
    ax.annotate("", xy=(5.1, TINES[2]), xytext=(5.1, TINES[0]),
                arrowprops=dict(arrowstyle="<->", color=OK, lw=2.4))
    ax.text(5.4, (TINES[0] + TINES[2]) / 2 + 10,
            f"三层跨度\n{TINES[2] - TINES[0]:.0f} mm", fontsize=11.5,
            color=OK, fontweight="bold", va="center")
    ax.text(5.4, (TINES[0] + TINES[2]) / 2 - 22,
            f"行程 230\n余量 {MARGIN:.0f} mm", fontsize=10.5, color=OK,
            va="center")
    fig.suptitle("整车高度尺寸链：D − M 必须落在 2.3 … 60.3 mm",
                 fontsize=17, fontweight="bold", y=0.965)

    # --- notes panel ------------------------------------------------------
    an = fig.add_axes([0.50, 0.52, 0.48, 0.36])
    an.axis("off")
    rows = [
        ("几个符号", True),
        ("C   底盘顶面离台面多高   （还没做，大概 55–60）", False),
        ("M   Z 轴底板顶面离台面多高  ← 你来定，建议 25–35", False),
        ("D   托叉比滑块中心低多少     ← 取 D = M + 30 最省事", False),
        ("", False),
        ("为什么只看 D − M", True),
        ("托叉最低要伸到 42.7，滑块中心最低在 M+45", False),
        ("    42.7 − M ≥ 45 − D   →   D − M ≥ 2.3", False),
        ("托叉最高要伸到 214.7，滑块中心最高在 M+275", False),
        ("    214.7 − M ≤ 275 − D  →   D − M ≤ 60.3", False),
    ]
    for i, (t, bold) in enumerate(rows):
        an.text(0, 1.0 - i * 0.095, t, fontsize=11,
                fontweight="bold" if bold else "normal", va="top",
                color="#212529")

    # --- conclusion -------------------------------------------------------
    ac = fig.add_axes([0.50, 0.06, 0.48, 0.40])
    ac.axis("off")
    ac.text(0, 1.0, "所以底盘影响什么、不影响什么", fontsize=13,
            fontweight="bold", va="top")
    body = [
        ("不影响", OK, "公式里没有 C。底盘多高，只决定你把它装在什么位置。"),
        ("影响", "#e8590c",
         "C 决定 M 能不能取小。M 越小，托叉下垂 D 越短、刚性越好。"),
        ("所以", OK,
         "把 Z 轴底板压低到 25–35 mm（让它在前脸往下探），"
         "托叉下垂就只要 55–65 mm，抱箍竖槽 ±25 吸收误差。"),
    ]
    y = 0.82
    for tag, col, txt in body:
        ac.text(0, y, tag, fontsize=11.5, fontweight="bold", color=col,
                va="top")
        ac.text(0.10, y, txt, fontsize=11, va="top", wrap=True)
        y -= 0.24
    ac.text(0, 0.10, "结论：你今晚把底盘做出来，量个 C 给我；"
                     "M 我建议 30，D = 60。", fontsize=11.5,
            fontweight="bold", color="#212529", va="top")

    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "height_chain.png")
