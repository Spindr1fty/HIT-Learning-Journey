r"""Dimensioned three-view of the reference servo -- to check against the real one.

    python draw_servo_dims.py  ->  renders/servo_dims.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent


class S:  # the numbers from src/g_servo.py (copied, it imports cadgen)
    BODY_X, BODY_Y, BODY_Z = 40.0, 20.0, 40.0
    FLANGE_Z0, FLANGE_Z1 = 30.0, 32.5
    FLANGE_SPAN = 48.5
    FLANGE_TAB_W = 10.0
    HOLE_DX = FLANGE_SPAN / 2.0
    HOLE_DY = FLANGE_TAB_W / 2.0
    SHAFT_D = 5.9
    SHAFT_Z0, SHAFT_Z1 = 40.0, 45.65
    SHAFT_X_OFF = 10.0
    HORN_D, HORN_T = 20.0, 2.5

    @staticmethod
    def hole_centres():
        cx = S.BODY_X / 2.0
        return [(cx + sx * S.HOLE_DX, sy * S.HOLE_DY, S.FLANGE_Z0)
                for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)]

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "servo_dims.png"

BODY = "#e6d8f5"
FLANGE = "#c8e8c8"
RED = "#c92a2a"
GRN = "#2f6f2f"


def dim(ax, p0, p1, text, color=RED, off=0.0):
    ax.annotate("", xy=p0, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.0))
    ax.text((p0[0] + p1[0]) / 2 + off, (p0[1] + p1[1]) / 2, text, fontsize=8.5,
            ha="center", va="bottom", color=color)


def main():
    fig = plt.figure(figsize=(16, 9), dpi=160, facecolor="white")

    # ---------------- top view (X-Y): body 40 x 20, flange 48.5 x 10
    ax = fig.add_axes([0.04, 0.50, 0.28, 0.40])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-14, 62)
    ax.set_ylim(-16, 30)
    ax.add_patch(Rectangle((0, -S.BODY_Y / 2), S.BODY_X, S.BODY_Y,
                           facecolor=BODY, edgecolor="#6b3fa0", lw=1.5))
    ax.add_patch(Rectangle(((S.BODY_X - S.FLANGE_SPAN) / 2, -S.HOLE_DY),
                           S.FLANGE_SPAN, 2 * S.HOLE_DY, facecolor=FLANGE,
                           edgecolor=GRN, lw=1.5, alpha=0.85))
    for x, y, _ in S.hole_centres():
        ax.plot(x, y, "o", ms=3.5, color=GRN)
    ax.add_patch(plt.Circle((S.BODY_X / 2 + S.SHAFT_X_OFF, 0), S.SHAFT_D / 2,
                            color="white", ec=RED, lw=1.2))
    ax.set_title("俯视（沿 Z 看）", fontsize=11, fontweight="bold")
    dim(ax, (0, -S.BODY_Y / 2 - 3.5), (S.BODY_X, -S.BODY_Y / 2 - 3.5),
        f"本体 {S.BODY_X:.1f}")
    dim(ax, ((S.BODY_X - S.FLANGE_SPAN) / 2, S.HOLE_DY + 3),
        ((S.BODY_X + S.FLANGE_SPAN) / 2, S.HOLE_DY + 3),
        f"法兰跨距 {S.FLANGE_SPAN:.1f}", GRN)
    dim(ax, (-4, -S.HOLE_DY), (-4, S.HOLE_DY), f"{2*S.HOLE_DY:.0f}", GRN)

    # ---------------- front view (X-Z): body 40 x 40, flange at Z 30..32.5
    ax = fig.add_axes([0.36, 0.50, 0.28, 0.40])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-14, 62)
    ax.set_ylim(-8, 58)
    ax.add_patch(Rectangle((0, 0), S.BODY_X, S.BODY_Z, facecolor=BODY,
                           edgecolor="#6b3fa0", lw=1.5))
    ax.add_patch(Rectangle(((S.BODY_X - S.FLANGE_SPAN) / 2, S.FLANGE_Z0),
                           S.FLANGE_SPAN, S.FLANGE_Z1 - S.FLANGE_Z0,
                           facecolor=FLANGE, edgecolor=GRN, lw=1.5, alpha=0.85))
    ax.add_patch(Rectangle((S.BODY_X / 2 + S.SHAFT_X_OFF - S.SHAFT_D / 2,
                            S.SHAFT_Z0), S.SHAFT_D, S.SHAFT_Z1 - S.SHAFT_Z0,
                           facecolor="white", edgecolor=RED, lw=1.2))
    ax.add_patch(Rectangle((S.BODY_X / 2 + S.SHAFT_X_OFF - S.HORN_D / 2,
                            S.SHAFT_Z0), S.HORN_D, S.HORN_T, facecolor="none",
                           edgecolor=RED, lw=0.9, ls=(0, (3, 2))))
    dim(ax, (0, -5), (S.BODY_X, -5), f"本体 {S.BODY_X:.1f}")
    dim(ax, (S.BODY_X + 4, 0), (S.BODY_X + 4, S.BODY_Z), f"{S.BODY_Z:.1f}", off=1)
    dim(ax, (0, S.BODY_Z + 4), (S.BODY_X, S.BODY_Z + 4), "400", GRN)
    ax.text(2, S.FLANGE_Z0 + 1.2, f"法兰 Z {S.FLANGE_Z0:.0f}~{S.FLANGE_Z1:.1f}"
            f"（厚 {S.FLANGE_Z1-S.FLANGE_Z0:.1f}）", fontsize=8, color=GRN)
    ax.text(S.BODY_X / 2 + S.SHAFT_X_OFF + 2, S.SHAFT_Z1 + 1,
            f"输出轴 Ø{S.SHAFT_D}，伸出 {S.SHAFT_Z1-S.SHAFT_Z0:.2f}", fontsize=7.5,
            color=RED)
    ax.set_title("正视（沿 Y 看）", fontsize=11, fontweight="bold")

    # ---------------- questions / checklist
    fig.text(0.05, 0.42, "我模型里用的参考舵机尺寸（请你对着实物核一遍，改哪个告诉我）",
             fontsize=13, fontweight="bold", color="#12395e")
    rows = [
        ("本体", "40（X）× 20（Y）× 40（Z）", "DS3218 / MG996R 级标准舵机"),
        ("法兰跨距（4 个安装孔之间的距离）", f"{S.FLANGE_SPAN:.1f}", "★ 你说“法兰和舵机一样宽”，如果跨距其实是 40，那我这整套前面结构都要改"),
        ("法兰厚度（Z 向）", f"{S.FLANGE_TAB_W:.1f}", "我按 10 做的"),
        ("法兰板厚（X 向）", f"{S.FLANGE_Z1-S.FLANGE_Z0:.1f}", "我按 2.5 做的"),
        ("安装孔位置", "±24.25（长向）× ±5.0（宽向）", "★ 如果法兰只有 40 宽，这里必然是 ±16 左右"),
        ("输出轴", f"Ø{S.SHAFT_D}", f"伸出 {S.SHAFT_Z1-S.SHAFT_Z0:.2f}"),
        ("舵盘", f"Ø{S.HORN_D} × {S.HORN_T}", ""),
    ]
    y = 0.36
    for a, b, c in rows:
        fig.text(0.05, y, a, fontsize=9.6, color="#333333")
        fig.text(0.34, y, b, fontsize=9.6, color=RED if "★" in c else "#1a5fb4")
        fig.text(0.60, y, c, fontsize=9.0, color="#666666")
        y -= 0.032

    fig.text(0.05, 0.12, "插不进去的两个可能原因", fontsize=13, fontweight="bold",
             color="#c92a2a")
    fig.text(0.05, 0.07,
             "① 法兰尺寸和我模型不同（你说“法兰和舵机一样宽=40”），而我按 48.5 做的槽 → 法兰过不去。\n"
             "② 口袋只留 0.15 间隙，打印收缩 + 毛刺就塞不进；我把间隙改成 0.30 会顺很多。\n"
             "（我用参考舵机做扫掠：沿 X 从后面推到位的全程 0 干涉；所以卡住的一定是法兰尺寸不同。）",
             fontsize=9.6, color="#333333")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
