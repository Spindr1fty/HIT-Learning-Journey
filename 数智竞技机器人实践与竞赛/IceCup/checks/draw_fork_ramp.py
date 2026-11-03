r"""Compare the 8.1 deg fork ramp with a 13 deg one, including the FDM stair
steps each produces at a given layer height.

    python draw_fork_ramp.py  ->  renders/fork_ramp_compare.png
"""

import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "fork_ramp_compare.png"

THICK = 3.5
TIP_EDGE = 0.5
X_LIP = 53.08
X_LIP_END = X_LIP + 1.0
LAYER = 0.2


def ramp_start(angle_deg):
    return X_LIP_END - (THICK - TIP_EDGE) / math.tan(math.radians(angle_deg))


def terrace(ax, angle_deg, color, dz=1.9):
    """Draw the printed staircase of a ramp of the given angle."""
    xs, zs = [], []
    z = TIP_EDGE
    slope = math.tan(math.radians(angle_deg))
    while z < THICK - 1e-9:
        z_next = min(z + LAYER, THICK)
        x_here = X_LIP_END - (z - TIP_EDGE) / slope
        x_next = X_LIP_END - (z_next - TIP_EDGE) / slope
        xs += [x_next, x_next, x_here]
        zs += [z, z_next, z_next]
        z = z_next
    ax.plot(xs, zs, color=color, lw=1.4)


def panel_profile(ax):
    ax.set_title("A) 叉尖斜面：8.1°（现在）vs 13°（方案）", fontsize=12,
                 fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(24, 60)
    ax.set_ylim(-1.2, 6.2)

    for angle, color, dy in ((8.1, "#7a8fa6", 0.0), (13.0, "#c92a2a", 0.0)):
        x0 = ramp_start(angle)
        # material under the ramp
        ax.fill([x0, X_LIP_END, x0], [THICK, TIP_EDGE, THICK],
                color="#dbe9f7" if angle > 10 else "#e9eef4", zorder=2)
        ax.plot([x0, X_LIP_END], [THICK, TIP_EDGE], color=color, lw=2.2,
                zorder=4)
        ax.plot([x0, x0], [THICK, THICK - 0.0], color=color, lw=0.8, ls=":",
                zorder=3)
        terrace(ax, angle, color)
        ax.annotate(f"{angle}°", xy=((x0 + X_LIP_END) / 2, THICK - 0.2),
                    xytext=((x0 + X_LIP_END) / 2, THICK + 1.2),
                    fontsize=11, color=color, ha="center", fontweight="bold")
        ax.annotate("", xy=(x0, THICK + 0.55), xytext=(X_LIP_END, THICK + 0.55),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=1.0))
        ax.text((x0 + X_LIP_END) / 2, THICK + 0.7,
                f"{(X_LIP_END - x0):.1f}", fontsize=8.6, color=color,
                ha="center")
    ax.plot([24, 60], [0, 0], color="#12395e", lw=1.2)
    ax.text(25, 0.15, "叉板底面（贴床）", fontsize=8.2, color="#12395e")
    ax.text(54.4, TIP_EDGE - 0.55, "唇口 0.5", fontsize=8, color="#12395e")
    ax.annotate("灰色阶梯 = 8.1° 在 0.2 层高下的实际打印面\n"
                "红色阶梯 = 13° 的（台阶更小）",
                xy=(46, 1.3), xytext=(24.5, 2.4), fontsize=8.6, color="#495057")
    ax.text(25, 5.6, "（沿 X 方向看，Z 放大显示；单位 mm）", fontsize=8,
            color="#5b6773")


def panel_bars(ax):
    ax.set_title("B) 每层台阶高度（越矮越好）", fontsize=12, fontweight="bold",
                 pad=8)
    layers = [0.20, 0.16, 0.12, 0.08]
    angles = [(8.1, "#7a8fa6"), (13.0, "#c92a2a"), (15.0, "#e07a3f")]
    width = 0.22
    for k, (angle, color) in enumerate(angles):
        vals = [h / math.tan(math.radians(angle)) for h in layers]
        xs = [i + (k - 1) * width for i in range(len(layers))]
        bars = ax.bar(xs, vals, width=width * 0.92, color=color,
                      label=f"{angle}°")
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.03, f"{v:.2f}", ha="center", fontsize=8,
                    color=color)
    ax.set_xticks(range(len(layers)))
    ax.set_xticklabels([f"{h:.2f}" for h in layers])
    ax.set_xlabel("层高 (mm)", fontsize=10)
    ax.set_ylabel("每层水平台阶 (mm)", fontsize=10)
    ax.set_ylim(0, 1.65)
    ax.legend(fontsize=9, frameon=False)
    ax.grid(axis="y", color="#e8edf2", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def main():
    fig = plt.figure(figsize=(16.0, 7.6), dpi=200, facecolor="white")
    panel_profile(fig.add_axes([0.03, 0.10, 0.55, 0.76]))
    panel_bars(fig.add_axes([0.64, 0.16, 0.33, 0.66]))
    fig.suptitle("叉尖斜面：把角度从 8.1° 改到 13°，打印台阶从 1.40mm 降到 0.86mm",
                 fontsize=15.5, fontweight="bold", y=0.965)
    fig.text(0.03, 0.015,
             "斜面越浅，同样的层高在水平方向推进越多，梯田越明显。"
             "改角度只动一个参数（RAMP_ANGLE），叉板厚度、唇口 0.5、齿尖位置都不变；"
             "13° 斜面长 13.0mm（原来 21.1mm），冰壶 47mm 盘照样能骑上去。",
             fontsize=9.6, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
