r"""Drawing of the clamp-on top cap for the Z module (no rail modification).

    python draw_z_topcap.py  ->  renders/z_topcap_drawing.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import z_params as P  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "z_topcap_drawing.png"

# --- geometry (module frame, mm)
RACK_TOP = 320.44           # the (new) rack's top
RAIL_TOP = 320.0
PLATE_T = 8.0
CAP_TOP = RACK_TOP + PLATE_T                 # 328.44
COLLAR_DOWN = 306.44        # carriage top is 305 -> 1.44 clearance
COLLAR_T = RACK_TOP - COLLAR_DOWN            # 14.0
SOCKET = 30.4               # rail 30.0 -> 0.2 per side
COLLAR_OUT = 42.4
PLATE_X = (-100.0, 21.2)
RAIL_X = (-15.0, 15.0)
RAIL_CAV = (-12.5, 12.5)
RAIL_SOLID_FROM = 315.0
RACK_X = (-96.5, -76.5)
RACK_TIP = -72.0
TOOTH_RELIEF = (-77.5, -70.5)
RELIEF_T = 2.0
M4_X = -86.5
M4_Y = 5.0
M4_SLOT = 10.6
M3_Z = COLLAR_DOWN + COLLAR_T / 2            # 313.44

C_CAP, C_RAIL, C_RACK, C_DIM = "#d8f0d8", "#c9d9e8", "#dbe9f7", "#5b6773"


def section_xz(ax):
    ax.set_title("A) X-Z 剖面（Y=0）：盖板抱住导轨顶部，再用 2×M4 压住齿条顶",
                 fontsize=12, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-116, 40)
    ax.set_ylim(286, 342)

    # ---- rail (top part)
    ax.add_patch(Rectangle((RAIL_X[0], 288), 30, RAIL_TOP - 288,
                           facecolor=C_RAIL, edgecolor="#12395e", lw=1.5,
                           zorder=3))
    ax.add_patch(Rectangle((RAIL_CAV[0], 288), 25, RAIL_SOLID_FROM - 288,
                           facecolor="white", edgecolor="#12395e", lw=0.8,
                           ls=(0, (4, 3)), zorder=4))
    ax.text(0, 296, "导轨（顶部 315~320 实心）", fontsize=8, ha="center",
            color="#12395e", zorder=6)

    # ---- rack + teeth
    ax.add_patch(Rectangle((RACK_X[0], 292), 20, RACK_TOP - 292,
                           facecolor=C_RACK, edgecolor="#12395e", lw=1.5,
                           zorder=3))
    ax.add_patch(Rectangle((RACK_X[1], 296), RACK_TIP - RACK_X[1],
                           RACK_TOP - 296, facecolor="#eef4fb",
                           edgecolor="#12395e", lw=0.9, hatch="///", zorder=3))
    ax.text(-86.5, 299, "齿条（新，51 齿）\n顶面 320.44", fontsize=8,
            ha="center", color="#12395e", zorder=6)

    # ---- cap: hanging collar walls + top plate (with tooth relief)
    ax.add_patch(Rectangle((-COLLAR_OUT / 2, COLLAR_DOWN),
                           COLLAR_OUT / 2 - RAIL_X[1], COLLAR_T,
                           facecolor=C_CAP, edgecolor="#2f6f2f", lw=1.7,
                           zorder=7))
    ax.add_patch(Rectangle((RAIL_X[1], COLLAR_DOWN),
                           COLLAR_OUT / 2 - RAIL_X[1], COLLAR_T,
                           facecolor=C_CAP, edgecolor="#2f6f2f", lw=1.7,
                           zorder=7))
    # plate with a 2 mm relief over the tooth tips
    ax.add_patch(Rectangle((PLATE_X[0], RACK_TOP), TOOTH_RELIEF[0] - PLATE_X[0],
                           PLATE_T, facecolor=C_CAP, edgecolor="#2f6f2f",
                           lw=1.7, zorder=8))
    ax.add_patch(Rectangle((TOOTH_RELIEF[1], RACK_TOP),
                           PLATE_X[1] - TOOTH_RELIEF[1], PLATE_T,
                           facecolor=C_CAP, edgecolor="#2f6f2f", lw=1.7,
                           zorder=8))
    ax.add_patch(Rectangle((TOOTH_RELIEF[0], RACK_TOP + RELIEF_T),
                           TOOTH_RELIEF[1] - TOOTH_RELIEF[0], PLATE_T - RELIEF_T,
                           facecolor=C_CAP, edgecolor="#2f6f2f", lw=1.7,
                           zorder=8))

    # ---- M4 through the plate into the rack
    ax.add_patch(Rectangle((M4_X - M4_SLOT / 2, RACK_TOP + 1), M4_SLOT, PLATE_T - 2,
                           facecolor="white", edgecolor="#c92a2a", lw=1.0,
                           ls=(0, (3, 2)), zorder=9))
    ax.plot([M4_X, M4_X], [RACK_TOP - 12, CAP_TOP + 3], color="#c92a2a", lw=1.0,
            ls=(0, (2, 2)), zorder=10)
    ax.annotate("2× M4（长圆 X±3）\n打进齿条顶预留 Ø3.6 底孔",
                xy=(M4_X + 4, CAP_TOP - 4), xytext=(-104, 333),
                fontsize=8.2, color="#c92a2a",
                arrowprops=dict(arrowstyle="->", color="#c92a2a", lw=0.9))

    # ---- M3 grub screws
    ax.plot([COLLAR_OUT / 2 + 3.2, RAIL_X[1] + 0.4], [M3_Z, M3_Z],
            color="#6b3fa0", lw=1.8, zorder=11)
    ax.plot([COLLAR_OUT / 2 + 3.2], [M3_Z], marker="s", ms=4.5,
            color="#6b3fa0", zorder=12)
    ax.annotate("M3 紧定 ×2（+X、+Y 各一颗）\n顶紧导轨侧面，吃掉 0.2 间隙",
                xy=(COLLAR_OUT / 2 + 2, M3_Z + 1), xytext=(COLLAR_OUT / 2 + 12, 322),
                fontsize=8.2, color="#6b3fa0",
                arrowprops=dict(arrowstyle="->", color="#6b3fa0", lw=0.9))

    ax.annotate("抱夹：30.4 方孔套住\n导轨顶部约 13.5mm",
                xy=(10, COLLAR_DOWN + 4), xytext=(COLLAR_OUT / 2 + 9, 300),
                fontsize=8.2, color="#2f6f2f",
                arrowprops=dict(arrowstyle="->", color="#2f6f2f", lw=0.9))
    ax.annotate("齿尖上方留 2mm 让位",
                xy=(-73.0, RACK_TOP + 1.5), xytext=(-52, 335),
                fontsize=8, color="#2f6f2f",
                arrowprops=dict(arrowstyle="->", color="#2f6f2f", lw=0.9))

    # ---- dimensions
    ax.annotate("", xy=(-110, COLLAR_DOWN), xytext=(-110, CAP_TOP),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
    ax.text(-106, (COLLAR_DOWN + CAP_TOP) / 2 - 2, "22（8 板 + 14 抱夹）", fontsize=8.2,
            color=C_DIM, rotation=90, va="center")
    ax.annotate("", xy=(-14, 288.5), xytext=(-14, 305), arrowprops=dict(
        arrowstyle="<->", color="#a05a00", lw=0.9))
    ax.text(-13, 296.5, "滑块顶 305", fontsize=7.5, color="#a05a00")



def top_view(ax):
    ax.set_title("B) 俯视（X-Y）", fontsize=12, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-112, 42)
    ax.set_ylim(-31, 31)

    ax.add_patch(Rectangle((PLATE_X[0], -PLATE_X[1]), PLATE_X[1] - PLATE_X[0],
                           2 * PLATE_X[1], facecolor=C_CAP, edgecolor="#2f6f2f",
                           lw=1.9, zorder=2))
    ax.add_patch(Rectangle((-COLLAR_OUT / 2, -COLLAR_OUT / 2), COLLAR_OUT,
                           COLLAR_OUT, facecolor="#bfe3bf", edgecolor="#2f6f2f",
                           lw=1.2, zorder=3))
    ax.add_patch(Rectangle((-SOCKET / 2, -SOCKET / 2), SOCKET, SOCKET,
                           facecolor="white", edgecolor="#2f6f2f", lw=1.0,
                           ls=(0, (3, 2)), zorder=4))
    ax.text(0, 2, "30.4 方孔\n抱导轨", fontsize=7.6, ha="center", va="center",
            color="#2f6f2f", zorder=5)
    ax.add_patch(Rectangle((RACK_X[0], -8), 20, 16, facecolor="none",
                           edgecolor="#12395e", lw=1.0, ls=(0, (4, 2)),
                           zorder=4))
    ax.text(-86.5, -13.5, "齿条顶面（20×16，在盖板下面）", fontsize=7.6,
            ha="center", color="#12395e")
    for y in (-M4_Y, M4_Y):
        ax.add_patch(FancyBboxPatch((M4_X - M4_SLOT / 2, y - 2.3), M4_SLOT, 4.6,
                                    boxstyle="round,pad=0,rounding_size=2.3",
                                    facecolor="white", edgecolor="#c92a2a",
                                    lw=1.2, zorder=5))
    ax.text(M4_X, -27, "2× M4 长圆（X±3，调齿轮啮合距）", fontsize=8.2,
            color="#c92a2a", ha="center")
    ax.plot([COLLAR_OUT / 2 - 2.5], [0], marker="o", ms=4, color="#6b3fa0",
            zorder=6)
    ax.plot([0], [COLLAR_OUT / 2 - 2.5], marker="o", ms=4, color="#6b3fa0",
            zorder=6)
    ax.text(COLLAR_OUT / 2 + 1, 1, "+X M3", fontsize=7.6, color="#6b3fa0")
    ax.text(1, COLLAR_OUT / 2 + 2.5, "+Y M3", fontsize=7.6, color="#6b3fa0")
    ax.annotate("", xy=(PLATE_X[0], 26), xytext=(PLATE_X[1], 26),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.text((PLATE_X[0] + PLATE_X[1]) / 2, 27.5, "121.2", fontsize=8.5,
            ha="center", color=C_DIM)
    ax.annotate("", xy=(31, -COLLAR_OUT / 2), xytext=(31, COLLAR_OUT / 2),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.text(33, 0, "42.4", fontsize=8.5, color=C_DIM, va="center")


def main():
    fig = plt.figure(figsize=(16.0, 9.4), dpi=200, facecolor="white")
    section_xz(fig.add_axes([0.03, 0.10, 0.52, 0.72]))
    top_view(fig.add_axes([0.58, 0.13, 0.40, 0.62]))
    fig.suptitle("Z 模块顶盖（抱夹式：导轨本体不打孔，只多打这一个小件）",
                 fontsize=16, fontweight="bold", y=0.965)
    fig.text(0.03, 0.015,
             "装法：① 盖板从上方扣到导轨顶，30.4 方孔套住导轨顶部约 13.5mm（单边 0.2 间隙）；"
             "② 拧紧 +X、+Y 两颗 M3 紧定，把盖板锁死在导轨上；③ 从上面打 2×M4 进齿条顶面"
             "（齿条重打时预留 2 个 Ø3.6 底孔），X 向 ±3 长圆用来对齿轮啮合中心距。"
             "盖板底 306.4，滑块最高 305，留 1.4mm。",
             fontsize=9.6, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
