r"""Explanation sheet for the two g_mount_b rev 26 fixes.

Left  : section at Y = 27.5 (through the flange's contact patch) showing the
        flange ridge and the pocket -- before (1.6) and after (2.5).
Right : post front face, showing what the M4 head / washer really has to sit
        on, plus the wide-post proposal (dashed).
Numbers come from src/g_mount_b.py and src/g_servo.py.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import g_mount_b as M  # noqa: E402
import g_servo as S  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

EDGE = "#1b3b5a"
FILL = "#eaf2fb"
FILL2 = "#cfe0f2"
FLG = "#ffe8cc"
RIDGE = "#fa5252"
WIDE = "#7048e8"
DIM = "#495057"
NOTE = "#c92a2a"

Z0 = M.PLATE_T + M.FOOT_T                 # 14
FLG_HI = M.SERVO_X - S.FLANGE_Z0          # 7.5 (flange face away from post)
FLG_LO = M.SERVO_X - S.FLANGE_Z1          # 5.0 (mating face)
RIDGE_X0 = M.POST_X[1] - 2.0              # 3.0
BODY_Y = M.SERVO_CY - S.BODY_X / 2.0      # 30.19, servo body edge


def arrow_h(ax, x0, x1, y, label, color=DIM, fs=8.2, above=True):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="<->",
                                 mutation_scale=7, color=color, lw=0.8))
    ax.text((x0 + x1) / 2.0, y + (0.35 if above else -0.35), label,
            fontsize=fs, ha="center", va="bottom" if above else "top",
            color=color)


def arrow_v(ax, y0, y1, x, label, color=DIM, fs=8.2, left=True):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="<->",
                                 mutation_scale=7, color=color, lw=0.8))
    ax.text(x - (0.35 if left else -0.35), (y0 + y1) / 2.0, label,
            fontsize=fs, rotation=90, ha="right" if left else "left",
            va="center", color=color)


def section(ax, pocket_depth, title, note, note_color):
    ax.set_title(title, fontsize=11.5, fontweight="bold", pad=6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((-11, 0), 11, M.PLATE_T, facecolor=FILL,
                           edgecolor=EDGE, lw=1.1, alpha=0.55))
    ax.add_patch(Rectangle((0, M.PLATE_T), 22, M.FOOT_T, facecolor=FILL,
                           edgecolor=EDGE, lw=1.4))
    ax.add_patch(Rectangle((M.POST_X[0], Z0), M.POST_T, M.POST_TOP - Z0,
                           facecolor=FILL2, edgecolor=EDGE, lw=1.5))
    ax.add_patch(Rectangle((M.POST_X[1] - pocket_depth, M.POCKET_Z[0]),
                           pocket_depth, M.POCKET_W, facecolor="white",
                           edgecolor=EDGE, lw=1.0))
    for zc in (M.SERVO_Z - 5, M.SERVO_Z + 5):
        ax.add_patch(Rectangle((0, zc - M.SCREW_D / 2), M.POST_T, M.SCREW_D,
                               facecolor="white", edgecolor=EDGE, lw=1.0))
    ax.add_patch(Rectangle((FLG_LO, M.SERVO_Z - 5), FLG_HI - FLG_LO, 10,
                           facecolor=FLG, edgecolor=EDGE, lw=1.4))
    ax.add_patch(Rectangle((RIDGE_X0, M.SERVO_Z - 1), 2.0, 2.0,
                           facecolor=RIDGE, edgecolor="#c92a2a", lw=1.0,
                           alpha=0.8))
    # dimensions
    arrow_h(ax, M.POST_X[1] - pocket_depth, M.POST_X[1], 20.6,
            f"{pocket_depth:.1f}", color=DIM)
    arrow_v(ax, M.SERVO_Z - 1, M.SERVO_Z + 1, 1.2, "2.0", color="#c92a2a")
    arrow_h(ax, FLG_LO, FLG_HI, 17.0, "2.5")
    ax.annotate("", xy=(FLG_LO, 26.0), xytext=(9.0, 30.5),
                arrowprops=dict(arrowstyle="->", color=DIM, lw=0.8))
    ax.text(9.2, 30.8, "法兰上表面 = 立柱内侧面\nX = 5.0（贴合）", fontsize=8.0,
            color=DIM, va="bottom")
    ax.text(0.15, 33.2, "顶梁 Z 35~37\n（与柱同宽）", fontsize=7.6, color=DIM)
    ax.text(0.15, Z0 + 0.5, "底脚", fontsize=7.8, color=DIM)
    ax.text(8.0, M.SERVO_Z - 7.5, "法兰", fontsize=7.8, color="#a05a00")
    ax.text(-10.5, 5.0, "齿板", fontsize=7.8, color=DIM)
    ax.text(9.0, Z0 + 0.6, "（舵机本体在 Y>=30.19，本剖切看不到）", fontsize=7.4,
            color=DIM)
    ax.text(11.0, 25.8, note, fontsize=8.8, color=note_color,
            fontweight="bold", va="top")
    ax.set_xlim(-12, 24)
    ax.set_ylim(0, 38)


def face_view(ax):
    ax.set_title("立柱前面（X = 0，Y-Z）：螺丝头 / 垫圈到底坐在什么上面",
                 fontsize=11.2, fontweight="bold", pad=6)
    ax.set_aspect("equal")
    ax.axis("off")
    y0, y1 = M.POST1_Y
    ax.add_patch(Rectangle((y0, Z0), y1 - y0, M.POST_TOP - Z0,
                           facecolor=FILL2, edgecolor=EDGE, lw=1.5))
    ax.add_patch(Rectangle((y0 - 4.0, Z0), 4.0, M.POST_TOP - Z0,
                           facecolor="none", edgecolor=WIDE, lw=1.3,
                           ls=(0, (5, 3))))
    ax.text(y0 - 2.0, Z0 + 1.0, "加宽 4\n(向外)", fontsize=7.6, color=WIDE,
            ha="center", va="bottom")
    ax.plot([BODY_Y] * 2, [Z0, M.POST_TOP], color=NOTE, lw=1.1, ls="--")
    ax.text(BODY_Y + 0.35, Z0 + 1.0, "舵机本体边\nY = 30.19", fontsize=7.6,
            color=NOTE, va="bottom")
    for zc in (M.SERVO_Z - 5, M.SERVO_Z + 5):
        ax.add_patch(Circle((M.POST_C1, zc), M.SCREW_D / 2, facecolor="white",
                            edgecolor=EDGE, lw=1.1))
        ax.add_patch(Circle((M.POST_C1, zc), 8.1 / 2, fill=False,
                            edgecolor="#495057", lw=0.9, ls=(0, (2, 1.6))))
        ax.add_patch(Circle((M.POST_C1, zc), 9.0 / 2, fill=False,
                            edgecolor=NOTE, lw=1.0, ls=":"))
    arrow_h(ax, y0, M.POST_C1, M.POST_TOP - 1.2, "4.00", above=False)
    arrow_h(ax, M.POST_C1, y1, M.POST_TOP - 1.2, "4.00", above=False)
    arrow_h(ax, BODY_Y, M.POST_C1, Z0 + 0.6, "4.25", above=True)
    ax.text(M.POST_C1 + 4.7, M.SERVO_Z + 4.2, "M4 内六角头\nØ8.1（对角）",
            fontsize=7.4, color="#495057", va="bottom")
    ax.annotate("Ø9 垫圈在这边\n会顶到舵机本体", xy=(M.POST_C1 + 4.3, 20.5),
                xytext=(M.POST_C1 - 6.6, 17.4), fontsize=7.6, color=NOTE,
                arrowprops=dict(arrowstyle="->", color=NOTE, lw=0.8))
    ax.annotate("孔边距 1.75\n(舵机侧)", xy=(y1, 23.0),
                xytext=(y1 + 1.2, 24.5), fontsize=7.6, color="#495057",
                arrowprops=dict(arrowstyle="->", color="#495057", lw=0.8))
    ax.set_xlim(y0 - 7, 37)
    ax.set_ylim(Z0 - 2.5, M.POST_TOP + 1)


def table(ax):
    ax.axis("off")
    rows = [
        ("① 法兰槽深", "1.6 → 2.5", "凸脊实测 2.0；Z 轴座同款让位缝就是 2.5"),
        ("② 立柱宽", "8 → 12（只向外）", "孔边距 1.75 → 5.75（外侧）"),
        ("③ 三角筋腿", "18 → 14", "立柱外移后仍落在底脚前边 Y = 3.94"),
        ("④ 其余", "不动", "40.5 净距 / 4×Ø4.5 孔 / 开口 21 / 底脚 / 齿板孔"),
        ("⑤ 代价", "+0.25 cm³", "加宽部分几乎全在现有三角筋里"),
        ("⑥ 垫圈", "最多 Ø8", "Ø9 会顶到舵机本体（本体离螺栓线 4.25）"),
    ]
    ax.text(0.0, 1.00, "rev 26 改动（数字全部从模型/实测读）", fontsize=12,
            fontweight="bold", transform=ax.transAxes)
    for i, (k, v, why) in enumerate(rows):
        y = 0.86 - i * 0.15
        ax.text(0.00, y, k, fontsize=9.4, fontweight="bold",
                transform=ax.transAxes, color="#0b4f8a")
        ax.text(0.20, y, v, fontsize=9.4, transform=ax.transAxes,
                color="#c92a2a", fontweight="bold")
        ax.text(0.52, y, why, fontsize=8.2, transform=ax.transAxes)


def main(out):
    fig = plt.figure(figsize=(15.5, 9.0), dpi=115, facecolor="white")
    fig.suptitle("g_mount_b rev 26：法兰槽加深（已改）+ 立柱加宽（待确认）",
                 fontsize=16, fontweight="bold", y=0.975)
    section(fig.add_axes([0.02, 0.50, 0.44, 0.42]), 1.6,
            "改前：槽深 1.6",
            "凸脊 2.0 > 槽 1.6\n法兰被垫起 0.4 mm\n干涉 4.8 mm³", NOTE)
    section(fig.add_axes([0.50, 0.50, 0.44, 0.42]), M.POCKET_DEPTH,
            f"改后：槽深 {M.POCKET_DEPTH:.1f}", "余量 0.5 mm", "#2f9e44")
    face_view(fig.add_axes([0.03, 0.03, 0.36, 0.40]))
    table(fig.add_axes([0.44, 0.03, 0.54, 0.40]))
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../renders/mount_b_rev26.png")
