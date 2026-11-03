r"""Detail drawing: how the top cap is fixed to the RACK.

    python draw_z_cap_rack.py  ->  renders/z_cap_rack_detail.png
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
OUT = ROOT / "renders" / "z_cap_rack_detail.png"

# geometry
RACK_TOP = 320.44
PLATE_T = 8.0
CAP_TOP = RACK_TOP + PLATE_T
PLATE_Y = 21.2
RACK_Y = 8.0
RACK_X = (-96.5, -76.5)
RACK_TIP = -72.0
M4_X = -86.5
M4_Y = 5.0
M4_SLOT = 10.6            # dia 4.6 + 6 mm travel
M4_D = 4.6
PILOT = 3.6
PILOT_DEPTH = 10.0
SCREW_L = 20.0
HEAD_D, HEAD_T = 7.0, 4.0
WASHER_D, WASHER_T = 9.0, 1.0
RELIEF = (-77.5, -70.5)

C_CAP, C_RACK, C_SCREW, C_DIM = "#d8f0d8", "#dbe9f7", "#c92a2a", "#5b6773"


def yz_section(ax):
    ax.set_title("A) 过 M4 轴线剖开（Y-Z 剖面，X = −86.5）", fontsize=12,
                 fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-26, 26)
    ax.set_ylim(304, 340)

    # rack
    ax.add_patch(Rectangle((-RACK_Y, 304), 2 * RACK_Y, RACK_TOP - 304,
                           facecolor=C_RACK, edgecolor="#12395e", lw=1.4))
    ax.text(0, 308, "齿条（顶部 Y ±8 平面）", fontsize=8, ha="center",
            color="#12395e")
    # pilot holes
    for y in (-M4_Y, M4_Y):
        ax.add_patch(Rectangle((y - PILOT / 2, RACK_TOP - PILOT_DEPTH),
                               PILOT, PILOT_DEPTH, facecolor="white",
                               edgecolor=C_SCREW, lw=1.0, zorder=5))
    # plate with the two slots cut
    spans = [(-PLATE_Y, -M4_Y - M4_D / 2), (-M4_Y + M4_D / 2, M4_Y - M4_D / 2),
             (M4_Y + M4_D / 2, PLATE_Y)]
    for y0, y1 in spans:
        ax.add_patch(Rectangle((y0, RACK_TOP), y1 - y0, PLATE_T,
                               facecolor=C_CAP, edgecolor="#2f6f2f", lw=1.5,
                               zorder=6))
    ax.text(-19, RACK_TOP + 3, "盖板\n8 厚", fontsize=8, ha="center",
            va="center", color="#2f6f2f", zorder=8)
    # screws: shank + head + washer
    for y in (-M4_Y, M4_Y):
        ax.add_patch(Rectangle((y - 2.0, RACK_TOP - PILOT_DEPTH + 1.0), 4.0,
                               CAP_TOP - RACK_TOP + PILOT_DEPTH - 1.0,
                               facecolor="#f7d9d9", edgecolor=C_SCREW, lw=1.0,
                               zorder=9))
        ax.add_patch(Rectangle((y - WASHER_D / 2, CAP_TOP), WASHER_D, WASHER_T,
                               facecolor="#eeeeee", edgecolor=C_SCREW, lw=0.9,
                               zorder=9))
        ax.add_patch(Rectangle((y - HEAD_D / 2, CAP_TOP + WASHER_T), HEAD_D,
                               HEAD_T, facecolor="#f7d9d9", edgecolor=C_SCREW,
                               lw=1.1, zorder=9))
    ax.annotate("M4×20：头部 + 垫圈压住盖板上面，\n杆穿过 8mm 板，拧进齿条顶面\n"
                "10mm 深 Ø3.6 底孔（自攻）",
                xy=(M4_Y + 2.5, CAP_TOP + 2), xytext=(3, 334),
                fontsize=8.6, color=C_SCREW,
                arrowprops=dict(arrowstyle="->", color=C_SCREW, lw=0.9))
    ax.annotate("长圆孔 ±3（板厚方向看不见，\n沿 X 方向才是长圆）",
                xy=(-M4_Y - 2.3, RACK_TOP + 4), xytext=(-25, 328),
                fontsize=8.2, color="#2f6f2f",
                arrowprops=dict(arrowstyle="->", color="#2f6f2f", lw=0.9))
    ax.annotate("", xy=(-23, RACK_TOP), xytext=(-23, CAP_TOP),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.text(-21.5, (RACK_TOP + CAP_TOP) / 2, "8", fontsize=8.5, color=C_DIM,
            va="center")
    ax.annotate("", xy=(12, RACK_TOP - PILOT_DEPTH), xytext=(12, RACK_TOP),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.9))
    ax.text(13, RACK_TOP - PILOT_DEPTH / 2, "10", fontsize=8.5, color=C_DIM,
            va="center")


def plan(ax):
    ax.set_title("B) 俯视（X-Y）：盖板压在齿条顶面，2 个长圆孔沿 X 滑 ±3",
                 fontsize=12, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-106, -60)
    ax.set_ylim(-26, 26)

    ax.add_patch(Rectangle((-100, -PLATE_Y), 30, 2 * PLATE_Y,
                           facecolor=C_CAP, edgecolor="#2f6f2f", lw=1.8))
    ax.add_patch(Rectangle((RACK_X[0], -RACK_Y), 20, 2 * RACK_Y,
                           facecolor="#c9d9e8", edgecolor="#12395e", lw=1.0,
                           ls=(0, (4, 2))))
    ax.add_patch(Rectangle((RACK_X[1], -RACK_Y), RACK_TIP - RACK_X[1],
                           2 * RACK_Y, facecolor="#eef4fb", edgecolor="#12395e",
                           lw=0.8, hatch="///"))
    ax.text(-86.5, 0, "齿条顶面 20 × 16\n（在盖板下面）", fontsize=8,
            ha="center", va="center", color="#12395e")
    for y in (-M4_Y, M4_Y):
        ax.add_patch(FancyBboxPatch((M4_X - M4_SLOT / 2, y - M4_D / 2),
                                    M4_SLOT, M4_D,
                                    boxstyle="round,pad=0,rounding_size=2.3",
                                    facecolor="white", edgecolor=C_SCREW,
                                    lw=1.3, zorder=6))
        ax.add_patch(Circle((M4_X, y), PILOT / 2, facecolor="none",
                            edgecolor="#12395e", lw=0.9, ls=(0, (2, 2)),
                            zorder=7))
        ax.plot([M4_X], [y], marker="+", ms=7, color=C_SCREW, zorder=8)
    ax.annotate("", xy=(M4_X - 5.3, 12.5), xytext=(M4_X + 5.3, 12.5),
                arrowprops=dict(arrowstyle="<->", color=C_SCREW, lw=1.0))
    ax.text(M4_X, 14.5, "孔心可移动 ±3（调齿轮/齿条啮合距）", fontsize=8.2,
            ha="center", color=C_SCREW)
    ax.annotate("", xy=(M4_X + 5.3, -12.5), xytext=(M4_X - 5.3, -12.5),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
    ax.text(M4_X, -15.5, "长圆总长 10.6（Ø4.6）", fontsize=8.2, ha="center",
            color=C_DIM)
    ax.text(-99, 18, "盖板", fontsize=8.5, color="#2f6f2f")
    ax.text(-70, 18, "齿条齿", fontsize=8, color="#12395e")
    ax.text(-70, -21.5, "齿尖上方 2mm 让位", fontsize=7.8, color="#5b6773")


def main():
    fig = plt.figure(figsize=(14.6, 8.6), dpi=200, facecolor="white")
    yz_section(fig.add_axes([0.04, 0.12, 0.42, 0.74]))
    plan(fig.add_axes([0.52, 0.12, 0.42, 0.74]))
    fig.suptitle("顶盖和齿条怎么连：2 颗 M4 从盖板上面往下拧进齿条顶面",
                 fontsize=16, fontweight="bold", y=0.955)
    fig.text(0.04, 0.015,
             "装配顺序：① 齿条脚 4 颗 M4 照旧打到基板（先别拧死）→ 调好齿轮/齿条啮合中心距 → 拧紧；"
             "② 盖板扣到导轨顶，两颗 M3 紧定把盖板锁在导轨上（导轨不动）；"
             "③ 把 2 颗 M4×20 从盖板上面穿过长圆孔拧进齿条顶面的 Ø3.6 底孔（齿条重打时预留）。"
             "长圆 ±3 就是给第①步调啮合距留的余量——底部滑多少，顶部就能跟着滑多少。",
             fontsize=9.4, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
