r"""Sketch of the proposed Z-module fix: rack extended to 320, a top cap tying
rack + rail, and a back spine on the rack.

    python draw_z_proposal.py   ->  renders/z_topcap_proposal.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import z_params as P  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = Path(r"D:\IceCup\renders\z_topcap_proposal.png")

RAIL_X = (-P.RAIL_W / 2, P.RAIL_W / 2)          # -15 .. 15
RACK_BODY_X = P.RACK_BODY_X                     # -96.5 .. -76.5
RACK_TIP_X = P.RACK_PITCH_X + P.MODULE          # -72
FOOT_TOP = 8.0
RACK_OLD_TOP = P.RACK_LEN                       # 251.3
RACK_NEW_TOP = P.RAIL_LEN                       # 320
CAP_T = 8.0
CAP_Z0 = RACK_NEW_TOP
CAR_TOP = P.Z_MAX + P.CARRIAGE_LEN / 2          # 305
NEED_TOP = P.Z_MAX + P.ROOT_R                   # 290.5
SPINE_X = (-116.5, -96.5)
SPINE_Y_HALF = 3.0

C_RAIL, C_RACK, C_PIN, C_CAR, C_CAP, C_SPN = (
    "#c9d9e8", "#dbe9f7", "#c92a2a", "#ffe9c7", "#2f6f2f", "#a05a00")


def side(ax):
    ax.set_title("A) 侧视（X-Z 平面）", fontsize=12, fontweight="bold", pad=6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-128, 44)
    ax.set_ylim(-14, 344)

    # rail (hollow)
    ax.add_patch(Rectangle((RAIL_X[0], FOOT_TOP), 30, P.RAIL_LEN - FOOT_TOP,
                           facecolor=C_RAIL, edgecolor="#12395e", lw=1.4, zorder=3))
    ax.add_patch(Rectangle((-12.5, 13), 25, P.RAIL_LEN - 30, facecolor="white",
                           edgecolor="#12395e", lw=0.7, ls=(0, (4, 2)), zorder=4))
    ax.add_patch(Rectangle((-25, 0), 50, FOOT_TOP, facecolor=C_RAIL,
                           edgecolor="#12395e", lw=1.4, zorder=3))
    ax.text(0, P.RAIL_LEN / 2, "导轨\n30×30×320\n空心", ha="center", va="center",
            fontsize=8.5, color="#12395e", zorder=6)

    # rack body + teeth band
    ax.add_patch(Rectangle((RACK_BODY_X[0], 0), 20, RACK_NEW_TOP,
                           facecolor=C_RACK, edgecolor="#12395e", lw=1.4, zorder=3))
    # schematic teeth: zig-zag band, visual pitch only
    zp = 10.0
    xs, zs = [], []
    z = 0.0
    k = 0
    while z < RACK_NEW_TOP:
        xs += [RACK_BODY_X[1], RACK_TIP_X, RACK_TIP_X, RACK_BODY_X[1]]
        zs += [z, z + zp * 0.25, z + zp * 0.5, z + zp * 0.5]
        z += zp * 0.5
        k += 1
    ax.plot(xs, zs, color="#12395e", lw=0.8, zorder=5)
    ax.add_patch(Rectangle((SPINE_X[0], FOOT_TOP), SPINE_X[1] - SPINE_X[0],
                           RACK_NEW_TOP - FOOT_TOP, facecolor="#f2e2cf",
                           edgecolor=C_SPN, lw=1.3, zorder=2))
    ax.add_patch(Rectangle((RACK_BODY_X[0] - 7.5, 0), 7.5 + 20, FOOT_TOP,
                           facecolor=C_RACK, edgecolor="#12395e", lw=1.2, zorder=3))
    ax.text(SPINE_X[0] - 3.5, 170, "新加背筋\n6×20×312", fontsize=8, color=C_SPN,
            ha="center", va="center", rotation=90, zorder=7)
    ax.text(-87, RACK_NEW_TOP - 24, "齿条（加长到 320）", fontsize=8, color="#12395e",
            ha="center", zorder=7)

    # missing-tooth zone of the OLD rack
    ax.add_patch(Rectangle((RACK_BODY_X[1], RACK_OLD_TOP), 4.5,
                           NEED_TOP + 4 - RACK_OLD_TOP, facecolor="none",
                           edgecolor="#c92a2a", lw=1.0, ls=(0, (3, 2)), hatch="///",
                           zorder=6))
    ax.plot([RACK_TIP_X, RACK_TIP_X + 22], [RACK_OLD_TOP] * 2, color="#c92a2a",
            lw=1.0, ls=(0, (5, 3)), zorder=6)
    ax.text(RACK_TIP_X + 24, RACK_OLD_TOP, "旧齿条顶 251.3", fontsize=8,
            color="#c92a2a", va="center")
    ax.text(RACK_TIP_X + 3, 272, "缺齿区\n≈44", fontsize=8, color="#c92a2a",
            va="center")

    # carriage at both ends of the stroke
    for zc, tag in ((P.Z_MIN, "下限位"), (P.Z_MAX, "上限位")):
        ax.add_patch(Rectangle((-21, zc - 30), 42, 60, facecolor=C_CAR,
                               edgecolor="#a05a00", lw=1.1, alpha=0.75, zorder=4))
        ax.text(6, zc + 20, f"滑块\n{tag}", fontsize=7.5, color="#a05a00",
                ha="center", zorder=8)
        ax.add_patch(Circle((P.PINION_X, zc), P.TIP_R, facecolor="none",
                            edgecolor=C_PIN, lw=1.1, ls=(0, (3, 2)), zorder=8))
        ax.add_patch(Rectangle((-56, zc - 4), 35, 8, facecolor="#eadcf7",
                               edgecolor="#6b3fa0", lw=1.0, zorder=4))
    ax.add_patch(Circle((P.PINION_X, P.Z_MAX), P.PITCH_R, facecolor="none",
                        edgecolor=C_PIN, lw=1.6, zorder=9))
    ax.text(P.PINION_X - 2, P.Z_MAX + 24, f"齿轮 R{P.PITCH_R:.0f}", fontsize=8,
            color=C_PIN, ha="center")
    ax.annotate("", xy=(-40, P.Z_MIN - 30), xytext=(-40, P.Z_MAX + 30),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(-38, (P.Z_MIN + P.Z_MAX) / 2, f"行程 {P.STROKE:.0f}",
            fontsize=8, color="#5b6773", rotation=90, va="center")

    # TOP CAP
    ax.add_patch(Rectangle((SPINE_X[0] - 2, CAP_Z0), 30 + abs(SPINE_X[0]) + 2,
                           CAP_T, facecolor="#d8f0d8", edgecolor=C_CAP, lw=1.8,
                           zorder=10))
    ax.add_patch(Rectangle((-12.5, CAP_Z0 - 20), 25, 20, facecolor="#eef8ee",
                           edgecolor=C_CAP, lw=1.0, ls=(0, (3, 2)), zorder=9))
    for x in (-90, -84, -6, 6):
        ax.plot([x], [CAP_Z0 + CAP_T / 2], marker="o", ms=3.2, color="#12395e",
                zorder=11)
    ax.text(-45, CAP_Z0 + CAP_T + 8, "顶盖 8 厚：2×M4 打进齿条（X 向长圆）"
            " ＋ 2×M4 打导轨顶（顶部改实心）", fontsize=8.2, color=C_CAP,
            ha="center", zorder=11)
    ax.annotate("", xy=(30, CAP_Z0), xytext=(30, CAR_TOP),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=0.9))
    ax.text(32, (CAP_Z0 + CAR_TOP) / 2, "15", fontsize=8, color="#5b6773",
            va="center")

    # limit switch seat
    ax.add_patch(Rectangle((-70, CAP_Z0 + CAP_T), 16, 6, facecolor="#f0e0f0",
                           edgecolor="#6b3fa0", lw=1.0, zorder=10))
    ax.text(-62, CAP_Z0 + CAP_T + 9, "上限位开关", fontsize=7.5, color="#6b3fa0",
            ha="center", zorder=11)

    # dimensions
    ax.annotate("", xy=(34, 0), xytext=(34, RACK_NEW_TOP),
                arrowprops=dict(arrowstyle="<->", color="#12395e", lw=0.9))
    ax.text(36, RACK_NEW_TOP / 2, "320", fontsize=9, color="#12395e",
            va="center")
    ax.annotate("", xy=(-122, 0), xytext=(-122, CAP_Z0 + CAP_T),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=0.9))
    ax.text(-120, (CAP_Z0 + CAP_T) / 2, "总高\n328", fontsize=8,
            color="#5b6773", va="center")


def section(ax):
    ax.set_title("B) 齿条截面（X-Y）：加背筋后刚度 ×5", fontsize=12,
                 fontweight="bold", pad=6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-128, 14)
    ax.set_ylim(-26, 26)

    # existing section
    ax.add_patch(Rectangle((RACK_BODY_X[0], -8), 20, 16, facecolor=C_RACK,
                           edgecolor="#12395e", lw=1.3))
    ax.add_patch(Rectangle((RACK_BODY_X[1], -8), 4.5, 16, facecolor="#eef4fb",
                           edgecolor="#12395e", lw=1.0, hatch="///"))
    ax.text(-86, -19, "现状", fontsize=8.5, ha="center")
    ax.text(-86, 19, "I ≈ 1.2×10⁴ mm⁴", fontsize=8, ha="center", color="#12395e")

    # proposed T section
    ax.add_patch(Rectangle((SPINE_X[0], -SPINE_Y_HALF), 20, 2 * SPINE_Y_HALF,
                           facecolor="#f2e2cf", edgecolor=C_SPN, lw=1.3))
    ax.add_patch(Rectangle((RACK_BODY_X[0], -8), 20, 16, facecolor=C_RACK,
                           edgecolor="#12395e", lw=1.3))
    ax.add_patch(Rectangle((RACK_BODY_X[1], -8), 4.5, 16, facecolor="#eef4fb",
                           edgecolor="#12395e", lw=1.0, hatch="///"))
    ax.text(-86, -19, "加背筋 6×20", fontsize=8.5, ha="center", color=C_SPN)
    ax.text(-86, 19, "I ≈ 6×10⁴ mm⁴  (×5)", fontsize=8, ha="center",
            color=C_SPN)
    ax.annotate("", xy=(RACK_TIP_X, 22), xytext=(RACK_BODY_X[0], 22),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=0.8))
    ax.text(-86, 23.5, "20", fontsize=7.5, ha="center", color="#5b6773")


def plan(ax):
    ax.set_title("C) 顶盖俯视", fontsize=12, fontweight="bold", pad=6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-124, 30)
    ax.set_ylim(-30, 30)

    ax.add_patch(Rectangle((SPINE_X[0] - 2, -22), SPINE_X[1] - SPINE_X[0] + 2, 44,
                           facecolor="none", edgecolor=C_CAP, lw=1.6))
    ax.add_patch(Rectangle((RACK_BODY_X[0], -8), 20, 16, facecolor=C_RACK,
                           edgecolor="#12395e", lw=1.1))
    ax.add_patch(Rectangle((-15, -15), 30, 30, facecolor=C_RAIL,
                           edgecolor="#12395e", lw=1.1))
    ax.add_patch(Rectangle((-12.5, -12.5), 25, 25, facecolor="white",
                           edgecolor="#12395e", lw=0.8, ls=(0, (3, 2))))
    ax.text(0, 0, "内腔 25×25\n盖板塞子插入 20 深", fontsize=7.5, ha="center",
            va="center", color="#12395e")
    for x in (-90, -84):
        ax.add_patch(plt.matplotlib.patches.FancyBboxPatch(
            (x - 2.2, -14), 4.4, 28, boxstyle="round,pad=0,rounding_size=2.2",
            facecolor="none", edgecolor="#c92a2a", lw=1.1, ls=(0, (3, 2))))
    for x in (-6, 6):
        ax.add_patch(Circle((x, 0), 2.2, facecolor="none", edgecolor="#12395e",
                            lw=1.1))
    ax.text(-87, 26, "2×M4 长圆孔（±3，保留啮合距调整）", fontsize=7.6,
            color="#c92a2a", ha="center")
    ax.text(0, 26, "2×M4", fontsize=7.6, color="#12395e", ha="center")
    ax.text(-62, 0, "齿条齿", fontsize=8, color="#5b6773", ha="center")


def main():
    fig = plt.figure(figsize=(16.5, 11.2), dpi=120, facecolor="white")
    ax1 = fig.add_axes([0.03, 0.04, 0.44, 0.86])
    ax2 = fig.add_axes([0.52, 0.56, 0.45, 0.30])
    ax3 = fig.add_axes([0.52, 0.06, 0.45, 0.44])
    side(ax1)
    section(ax2)
    plan(ax3)
    fig.suptitle("Z 模块改法（方案示意，单位 mm）：齿条加长到 320 ＋ 顶盖把齿条和导轨连成刚架",
                 fontsize=15, fontweight="bold", y=0.975)
    fig.text(0.03, 0.015,
             "齿条加长后 320 全高有齿 → 齿轮走满 80~275 全程咬合；顶盖在 Z 320~328，"
             "滑块最高 305，留 15mm；齿条齿尖上方留 1mm 让位。",
             fontsize=9.5, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
