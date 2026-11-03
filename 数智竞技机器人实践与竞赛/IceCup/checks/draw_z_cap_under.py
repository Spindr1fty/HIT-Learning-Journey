r"""The two details on the cap's underside: the tooth relief slot and the
through-holes.

    python draw_z_cap_under.py  ->  renders/z_cap_under.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "z_cap_under.png"

PLATE_X = (-104.0, 21.2)
HALF_Y = 21.2
RACK_TOP = 320.44
DOWN = 306.44
RAIL_SOCKET = 30.4
RAIL_OUT = 42.4
CUFF_X = (-104.0, -73.0)
CUFF_WALL = 3.8
CUFF_Y = (8.3, 13.3)
GRUB_AT_X = (-90.0, -80.0)
RELIEF = (-77.5, -70.5)
RELIEF_D = 2.0

C_PLATE, C_WALL, C_HOLE, C_DIM = "#d8f0d8", "#bfe3bf", "#c92a2a", "#5b6773"


def bottom_view(ax):
    ax.set_title("A) 仰视（从下往上看盖板底面）", fontsize=12, fontweight="bold",
                 pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-112, 96)
    ax.set_ylim(-30, 28)

    ax.add_patch(Rectangle((PLATE_X[0], -HALF_Y), PLATE_X[1] - PLATE_X[0],
                           2 * HALF_Y, facecolor=C_PLATE, edgecolor="#2f6f2f",
                           lw=1.8))
    ax.add_patch(Rectangle((-RAIL_SOCKET / 2, -RAIL_SOCKET / 2), RAIL_SOCKET,
                           RAIL_SOCKET, facecolor="white", edgecolor="#2f6f2f",
                           lw=1.4))
    ax.text(0, 0, "导轨方孔 30.4", fontsize=8, ha="center", va="center",
            color="#2f6f2f")
    for y0, y1 in ((CUFF_Y[0], CUFF_Y[1]), (-CUFF_Y[1], -CUFF_Y[0])):
        ax.add_patch(Rectangle((CUFF_X[0], y0), CUFF_X[1] - CUFF_X[0],
                               y1 - y0, facecolor=C_WALL, edgecolor="#2f6f2f",
                               lw=1.2))
    ax.add_patch(Rectangle((CUFF_X[0], -CUFF_Y[1]), CUFF_WALL, 2 * CUFF_Y[1],
                           facecolor=C_WALL, edgecolor="#2f6f2f", lw=1.2))
    ax.add_patch(Rectangle((CUFF_X[0] + CUFF_WALL, -CUFF_Y[0]),
                           CUFF_X[1] - CUFF_X[0] - CUFF_WALL, 2 * CUFF_Y[0],
                           facecolor="white", edgecolor="#2f6f2f", lw=1.0,
                           ls=(0, (3, 2))))
    ax.text(-86, 3.2, "齿条块 27.2×16.6", fontsize=8, ha="center",
            color="#12395e")
    ax.text(-86, -3.2, "（沿 X 可滑 ±3）", fontsize=7.6, ha="center",
            color="#12395e")
    # relief slot (only across the pocket, Y +-8.3)
    ax.add_patch(Rectangle((RELIEF[0], -CUFF_Y[0]), RELIEF[1] - RELIEF[0],
                           2 * CUFF_Y[0], facecolor="#f4d6d6", edgecolor=C_HOLE,
                           lw=1.5, hatch="///"))
    for gx in GRUB_AT_X:
        ax.plot([gx], [(CUFF_Y[0] + CUFF_Y[1]) / 2], marker="o", ms=5,
                mfc="white", mec=C_HOLE, mew=1.3)
    ax.plot([RAIL_OUT / 2 + 0.6], [0], marker="o", ms=5, mfc="white",
            mec="#12395e", mew=1.3)
    ax.plot([0], [RAIL_OUT / 2 + 0.6], marker="o", ms=5, mfc="white",
            mec="#12395e", mew=1.3)

    # leader labels into the right margin
    ax.annotate("① 齿尖让位槽\n   宽 7 × 深 2，只开在齿条块宽度内\n"
                "   齿顶比齿条顶面高 0.6，平贴会压到齿",
                xy=(RELIEF[1], 5.5), xytext=(27, 20), fontsize=8.6,
                color=C_HOLE, va="center",
                arrowprops=dict(arrowstyle="->", color=C_HOLE, lw=0.9))
    ax.annotate("② 齿条箍 2× M3（通孔）\n   紧定穿过 5 壁，顶住齿条侧面",
                xy=(-80, (CUFF_Y[0] + CUFF_Y[1]) / 2), xytext=(27, 3),
                fontsize=8.6, color=C_HOLE, va="center",
                arrowprops=dict(arrowstyle="->", color=C_HOLE, lw=0.9))
    ax.annotate("③ 导轨箍 2× M3（通孔）\n   +X / +Y 面各一颗",
                xy=(RAIL_OUT / 2 + 0.6, 0), xytext=(27, -16), fontsize=8.6,
                color="#12395e", va="center",
                arrowprops=dict(arrowstyle="->", color="#12395e", lw=0.9))
    ax.annotate("", xy=(PLATE_X[0], -26), xytext=(PLATE_X[1], -26),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.text((PLATE_X[0] + PLATE_X[1]) / 2, -24, "125.2", fontsize=8.5,
            ha="center", color=C_DIM)


def section(ax):
    ax.set_title("B) X = −74 竖剖：让位槽和齿尖", fontsize=12,
                 fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-26, 26)
    ax.set_ylim(303, 334)

    # cuff walls attached to the plate
    for y0, y1 in ((CUFF_Y[0], CUFF_Y[1]), (-CUFF_Y[1], -CUFF_Y[0])):
        ax.add_patch(Rectangle((y0, DOWN), y1 - y0, RACK_TOP - DOWN,
                               facecolor=C_WALL, edgecolor="#2f6f2f", lw=1.3))
    # plate: underside at 320.44 outside the pocket, stepped up 2 mm inside it
    ax.add_patch(Rectangle((-HALF_Y, RACK_TOP), CUFF_Y[0] + HALF_Y,
                           RACK_TOP + 8 - RACK_TOP,
                           facecolor=C_PLATE, edgecolor="#2f6f2f", lw=1.4))
    ax.add_patch(Rectangle((-CUFF_Y[0], RACK_TOP), 2 * CUFF_Y[0],
                           RACK_TOP + 8 - RACK_TOP, facecolor=C_PLATE,
                           edgecolor="#2f6f2f", lw=1.4))
    ax.add_patch(Rectangle((CUFF_Y[0], RACK_TOP + RELIEF_D),
                           HALF_Y - CUFF_Y[0],
                           (RACK_TOP + 8) - (RACK_TOP + RELIEF_D),
                           facecolor=C_PLATE, edgecolor="#2f6f2f", lw=1.4))
    # the 2 mm step
    ax.plot([-CUFF_Y[0], -CUFF_Y[0]], [RACK_TOP, RACK_TOP + RELIEF_D],
            color=C_HOLE, lw=1.6)
    ax.plot([CUFF_Y[0], CUFF_Y[0]], [RACK_TOP, RACK_TOP + RELIEF_D],
            color=C_HOLE, lw=1.6)
    ax.plot([-CUFF_Y[0], CUFF_Y[0]], [RACK_TOP + RELIEF_D] * 2, color=C_HOLE,
            lw=1.6)
    ax.text(0, RACK_TOP + 5.0, "盖板（让位段只有 6 厚）", fontsize=8.2,
            ha="center", color="#2f6f2f")
    # rack with teeth
    ax.add_patch(Rectangle((-8, 306), 16, RACK_TOP - 306,
                           facecolor="#dbe9f7", edgecolor="#12395e", lw=1.3))
    ax.add_patch(Rectangle((-8, RACK_TOP - 3.2), 16, 3.2, facecolor="#eef4fb",
                           edgecolor="#12395e", lw=0.9, hatch="///"))
    ax.text(0, 310, "齿条", fontsize=8.5, ha="center", color="#12395e")
    ax.annotate("", xy=(-14, RACK_TOP), xytext=(-14, RACK_TOP + RELIEF_D),
                arrowprops=dict(arrowstyle="<->", color=C_HOLE, lw=1.2))
    ax.text(-13, RACK_TOP + 1.0, "2", fontsize=9, color=C_HOLE, va="center")
    ax.text(0, RACK_TOP + 1.0, "齿顶 320.44", fontsize=8, ha="center",
            color="#12395e", va="center")
    ax.text(-11.5, 318, "箍壁", fontsize=8, rotation=90, ha="center",
            va="center", color="#2f6f2f")


def main():
    fig = plt.figure(figsize=(16.4, 8.2), dpi=200, facecolor="white")
    bottom_view(fig.add_axes([0.02, 0.06, 0.60, 0.78]))
    section(fig.add_axes([0.66, 0.10, 0.30, 0.70]))
    fig.suptitle("盖板底面两处细节：① 齿尖让位槽   ②③ M3 都是通孔",
                 fontsize=16, fontweight="bold", y=0.955)
    fig.text(0.02, 0.012,
             "让位槽为什么必需：齿条共 51 齿，最后一齿的齿根会突出齿条顶面约 0.6mm；"
             "盖板底面平贴 320.44 就会压在齿尖上，装配顶不到底还会压坏齿。"
             "所以盖板在齿尖那一段抬高 2mm（X −77.5~−70.5，只开在齿条块 Y ±8.3 以内，"
             "避免把箍壁从盖板上切掉）。M3 孔已改通孔：紧定螺钉穿过 5mm 壁直接顶住齿条/导轨。",
             fontsize=9.6, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
