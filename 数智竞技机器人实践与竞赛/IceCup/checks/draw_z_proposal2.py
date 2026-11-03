r"""Two clean sketches of the proposed Z-module fix.

    python draw_z_proposal2.py
        -> renders/z_proposal_side.png     side view (X-Z)
        -> renders/z_proposal_detail.png   T-section + top-cap plan
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

C_RAIL, C_RACK, C_PIN, C_CAR = "#c9d9e8", "#dbe9f7", "#c92a2a", "#ffe9c7"
C_CAP, C_SPN, C_EDGE = "#d8f0d8", "#f2e2cf", "#12395e"

RACK_X0, RACK_X1 = P.RACK_BODY_X            # -96.5 .. -76.5
RACK_TIP = P.RACK_PITCH_X + P.MODULE        # -72
SPINE_X0 = -116.5
FOOT_T = 8.0
TOP = P.RAIL_LEN                            # 320
CAP_T = 8.0
CAR_HALF = P.CARRIAGE_LEN / 2
CAR_TOP = P.Z_MAX + CAR_HALF                # 305
OLD_RACK_TOP = P.RACK_LEN                   # 251.3
NEED_TOP = P.Z_MAX + P.ROOT_R               # 290.5


# ------------------------------------------------------------------ side view
def side():
    fig = plt.figure(figsize=(9.6, 14.6), dpi=200, facecolor="white")
    ax = fig.add_axes([0.06, 0.045, 0.88, 0.90])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-140, 62)
    ax.set_ylim(-16, 372)

    # ---- rail
    ax.add_patch(Rectangle((-15, FOOT_T), 30, TOP - FOOT_T, facecolor=C_RAIL,
                           edgecolor=C_EDGE, lw=1.6, zorder=3))
    ax.add_patch(Rectangle((-12.5, 13), 25, TOP - 18, facecolor="white",
                           edgecolor=C_EDGE, lw=0.8, ls=(0, (4, 3)), zorder=4))
    ax.add_patch(Rectangle((-25, 0), 50, FOOT_T, facecolor=C_RAIL,
                           edgecolor=C_EDGE, lw=1.6, zorder=3))
    ax.text(0, 175, "导轨 30×30×320\n（空心，壁 2.5）", ha="center", va="center",
            fontsize=9.5, color=C_EDGE, zorder=7)

    # ---- rack body + teeth + foot + spine
    ax.add_patch(Rectangle((RACK_X0, FOOT_T), 20, TOP - FOOT_T, facecolor=C_RACK,
                           edgecolor=C_EDGE, lw=1.6, zorder=3))
    ax.plot([RACK_X0, RACK_X0], [FOOT_T, TOP], color=C_EDGE, lw=1.6, zorder=4)
    # schematic teeth (visual pitch, not to scale)
    zp = 11.0
    z = FOOT_T
    while z < TOP:
        ax.plot([RACK_X1, RACK_TIP, RACK_TIP, RACK_X1],
                [z, z + zp * 0.3, z + zp * 0.6, z + zp * 0.6],
                color=C_EDGE, lw=0.9, zorder=5)
        z += zp * 0.6
    ax.add_patch(Rectangle((-104, 0), 27.5, FOOT_T, facecolor=C_RACK,
                           edgecolor=C_EDGE, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((SPINE_X0, FOOT_T), RACK_X0 - SPINE_X0, TOP - FOOT_T,
                           facecolor=C_SPN, edgecolor="#a05a00", lw=1.4,
                           zorder=2))
    for z in range(30, 315, 45):
        ax.plot([SPINE_X0 + 2, SPINE_X0 + 2], [z, z + 12], color="#a05a00",
                lw=0.8, zorder=3)

    # ---- carriage at both ends + pinion + arm
    for zc, tag in ((P.Z_MIN, "下限位"), (P.Z_MAX, "上限位")):
        ax.add_patch(Rectangle((-21, zc - CAR_HALF), 42, 2 * CAR_HALF,
                               facecolor=C_CAR, edgecolor="#a05a00", lw=1.3,
                               alpha=0.85, zorder=6))
        ax.plot([-21, -21], [zc - CAR_HALF, zc + CAR_HALF], color="#a05a00",
                lw=1.3, zorder=7)
        ax.add_patch(Rectangle((-56, zc - 4.5), 35, 9, facecolor="#eadcf7",
                               edgecolor="#6b3fa0", lw=1.2, zorder=6))
        ax.add_patch(Circle((P.PINION_X, zc), P.TIP_R, facecolor="none",
                            edgecolor=C_PIN, lw=1.2, ls=(0, (3, 2)), zorder=8))
        ax.text(8, zc + CAR_HALF - 8, f"滑块\n{tag}", fontsize=8.5,
                color="#a05a00", ha="center", va="center", zorder=9)
    ax.add_patch(Circle((P.PINION_X, P.Z_MAX), P.PITCH_R, facecolor="none",
                        edgecolor=C_PIN, lw=2.0, zorder=9))
    ax.add_patch(Circle((P.PINION_X, P.Z_MAX), P.ROOT_R, facecolor="none",
                        edgecolor=C_PIN, lw=0.8, ls=(0, (2, 2)), zorder=9))
    ax.annotate("齿轮 R18（齿顶 20 / 齿根 15.5）",
                xy=(P.PINION_X + 6, P.Z_MAX + 14), xytext=(20, 348),
                fontsize=9, color=C_PIN, ha="left",
                arrowprops=dict(arrowstyle="->", color=C_PIN, lw=0.9))

    # ---- old rack top / missing teeth
    ax.add_patch(Rectangle((RACK_X1, OLD_RACK_TOP), RACK_TIP - RACK_X1,
                           NEED_TOP - OLD_RACK_TOP, facecolor="none",
                           edgecolor=C_PIN, lw=1.1, ls=(0, (3, 2)), hatch="///",
                           zorder=9))
    ax.plot([-72, 40], [OLD_RACK_TOP] * 2, color=C_PIN, lw=1.1, ls=(0, (6, 4)),
            zorder=9)
    ax.text(40, OLD_RACK_TOP, "旧齿条顶 251.3", fontsize=9, color=C_PIN,
            va="center")
    ax.annotate("旧版缺齿区（≈44）：齿轮走到 Z275 时齿根已到 290.5",
                xy=(RACK_TIP + 0.5, (OLD_RACK_TOP + NEED_TOP) / 2),
                xytext=(-48, 150), fontsize=8.8, color=C_PIN, rotation=90,
                va="center", ha="center",
                arrowprops=dict(arrowstyle="->", color=C_PIN, lw=0.9,
                                connectionstyle="arc3,rad=0.15"))

    # ---- travel arrow
    ax.annotate("", xy=(-32, P.Z_MIN - CAR_HALF), xytext=(-32, P.Z_MAX + CAR_HALF),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.1))
    ax.text(-30, (P.Z_MIN + P.Z_MAX) / 2, "行程 195", fontsize=9,
            color="#5b6773", rotation=90, va="center")

    # ---- TOP CAP
    ax.add_patch(Rectangle((SPINE_X0 - 1.5, TOP), -(SPINE_X0 - 1.5) + 17, CAP_T,
                           facecolor=C_CAP, edgecolor="#2f6f2f", lw=2.2,
                           zorder=12))
    ax.add_patch(Rectangle((-12.5, TOP - 22), 25, 22, facecolor="#eef8ee",
                           edgecolor="#2f6f2f", lw=1.0, ls=(0, (3, 2)),
                           zorder=11))
    for x in (-90, -84, -6, 6):
        ax.plot([x], [TOP + CAP_T / 2], marker="o", ms=4.5, color="#2f6f2f",
                zorder=13)
    ax.annotate("顶盖 8 厚：2×M4 竖打进食条顶（X 向长圆孔，保留 ±3 啮合距调整）\n"
                "＋ 2×M4 打导轨顶（导轨顶部 25 改实心带底孔）；下方 25×25 塞子插进导轨内腔",
                xy=(-20, TOP + CAP_T), xytext=(-118, TOP + 34), fontsize=9,
                color="#2f6f2f", va="bottom",
                arrowprops=dict(arrowstyle="->", color="#2f6f2f", lw=1.0))
    ax.annotate("", xy=(24, TOP), xytext=(24, CAR_TOP),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(26, (TOP + CAR_TOP) / 2, "15", fontsize=9, color="#5b6773",
            va="center")
    ax.add_patch(Rectangle((-64, TOP + CAP_T), 18, 7, facecolor="#f0e0f0",
                           edgecolor="#6b3fa0", lw=1.1, zorder=12))
    ax.text(-55, TOP + CAP_T + 11, "上限位开关座", fontsize=8.2, color="#6b3fa0",
            ha="center")

    # ---- labels / dims
    ax.text(SPINE_X0 - 8, 190, "新加背筋 6×20×312（T 型截面，刚度 ×5）",
            fontsize=9, color="#a05a00", rotation=90, va="center", ha="center")
    ax.annotate("", xy=(44, 0), xytext=(44, TOP),
                arrowprops=dict(arrowstyle="<->", color=C_EDGE, lw=1.0))
    ax.text(47, TOP / 2, "320（齿条与导轨同高）", fontsize=9, color=C_EDGE,
            rotation=90, va="center")
    ax.annotate("", xy=(-132, 0), xytext=(-132, TOP + CAP_T),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(-134, (TOP + CAP_T) / 2, "总高 328", fontsize=9, color="#5b6773",
            rotation=90, va="center", ha="right")
    ax.text(-118, -12, "底盘 / 底板（Z=0）", fontsize=9, color="#5b6773")

    fig.suptitle("Z 模块改法 · A 侧视", fontsize=15, fontweight="bold", y=0.975)
    fig.savefig(ROOT / "renders" / "z_proposal_side.png", facecolor="white")
    print("wrote", ROOT / "renders" / "z_proposal_side.png")


# ---------------------------------------------------------------- detail views
def detail():
    fig = plt.figure(figsize=(15.5, 6.6), dpi=200, facecolor="white")
    axA = fig.add_axes([0.04, 0.10, 0.42, 0.72])
    axB = fig.add_axes([0.52, 0.10, 0.44, 0.72])

    # ---- A: cross section X-Y
    axA.set_aspect("equal")
    axA.axis("off")
    axA.set_xlim(-132, 12)
    axA.set_ylim(-30, 30)
    axA.set_title("B) 齿条截面（X-Y 俯视）：加背筋后 I ×5", fontsize=12,
                  fontweight="bold", pad=8)
    axA.add_patch(Rectangle((RACK_X0, -8), 20, 16, facecolor=C_RACK,
                            edgecolor=C_EDGE, lw=1.4))
    axA.add_patch(Rectangle((RACK_X1, -8), RACK_TIP - RACK_X1, 16,
                            facecolor="#eef4fb", edgecolor=C_EDGE, lw=1.0,
                            hatch="///"))
    axA.add_patch(Rectangle((SPINE_X0, -3), RACK_X0 - SPINE_X0, 6,
                            facecolor=C_SPN, edgecolor="#a05a00", lw=1.4))
    axA.annotate("", xy=(RACK_X0, 22), xytext=(RACK_TIP, 22),
                 arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=0.9))
    axA.text((RACK_X0 + RACK_TIP) / 2, 24, "24.5（含齿）", fontsize=8.5,
             ha="center", color="#5b6773")
    axA.annotate("", xy=(SPINE_X0, -22), xytext=(RACK_X0, -22),
                 arrowprops=dict(arrowstyle="<->", color="#a05a00", lw=0.9))
    axA.text((SPINE_X0 + RACK_X0) / 2, -25, "背筋深 20", fontsize=8.5,
             ha="center", color="#a05a00")
    axA.text(-86, 10.5, "Y 宽 16", fontsize=8.5, color="#5b6773",
             ha="center")
    axA.text(-106, 8, "现状 I≈1.2×10⁴ mm⁴\n加背筋 I≈6×10⁴ mm⁴",
             fontsize=9, color="#a05a00", ha="center", va="bottom")

    # ---- B: top cap plan
    axB.set_aspect("equal")
    axB.axis("off")
    axB.set_xlim(-126, 34)
    axB.set_ylim(-34, 34)
    axB.set_title("C) 顶盖俯视（Z 320~328）", fontsize=12, fontweight="bold",
                  pad=8)
    axB.add_patch(Rectangle((SPINE_X0 - 2, -22), (17 - SPINE_X0) + 2, 44,
                            facecolor="#f4fbf4", edgecolor="#2f6f2f", lw=1.8))
    axB.add_patch(Rectangle((RACK_X0, -8), 20, 16, facecolor=C_RACK,
                            edgecolor=C_EDGE, lw=1.2))
    axB.add_patch(Rectangle((RACK_X1, -8), RACK_TIP - RACK_X1, 16,
                            facecolor="#eef4fb", edgecolor=C_EDGE, lw=0.8,
                            hatch="///"))
    axB.add_patch(Rectangle((-15, -15), 30, 30, facecolor=C_RAIL,
                            edgecolor=C_EDGE, lw=1.2))
    axB.add_patch(Rectangle((-12.5, -12.5), 25, 25, facecolor="white",
                            edgecolor=C_EDGE, lw=1.0, ls=(0, (3, 2))))
    axB.text(0, 6.5, "导轨顶部 25 高\n改实心", fontsize=8, ha="center",
             va="center", color=C_EDGE)
    axB.text(0, -8.5, "塞子 25×25×20", fontsize=8, ha="center", va="center",
             color=C_EDGE)
    for x in (-90, -84):
        axB.add_patch(FancyBboxPatch((x - 2.4, -15), 4.8, 30,
                                     boxstyle="round,pad=0,rounding_size=2.4",
                                     facecolor="none", edgecolor=C_PIN, lw=1.3,
                                     ls=(0, (3, 2))))
    for x in (-6.5, 6.5):
        axB.add_patch(Circle((x, 0), 2.4, facecolor="none", edgecolor=C_EDGE,
                             lw=1.3))
    axB.text(-87, -27, "2×M4 长圆（±3，调啮合距）", fontsize=8.5, color=C_PIN,
             ha="center")
    axB.text(-6.5, -27, "2×M4", fontsize=8.5, color=C_EDGE, ha="center")
    axB.text(-62, 20, "齿条（X −96.5~−72）", fontsize=8.5, color=C_EDGE,
             ha="center")
    axB.text(-62, -20, "齿尖上方留 1mm 让位", fontsize=8.5, color="#5b6773",
             ha="center")

    fig.suptitle("Z 模块改法 · B 截面 / C 顶盖", fontsize=15, fontweight="bold",
                 y=0.965)
    fig.savefig(ROOT / "renders" / "z_proposal_detail.png", facecolor="white")
    print("wrote", ROOT / "renders" / "z_proposal_detail.png")


if __name__ == "__main__":
    side()
    detail()
