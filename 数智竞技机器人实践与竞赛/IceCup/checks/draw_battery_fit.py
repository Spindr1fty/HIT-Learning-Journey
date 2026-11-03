r"""Why the battery box has to stand with its long side along Y.

    python draw_battery_fit.py  ->  renders/chassis_battery_fit.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import chassis as C  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "chassis_battery_fit.png"

L, W = 90.3, 36.2
FREE0, FREE1 = 40.0, 111.0        # free strip between left wheel plates and launcher


def panel(ax, title, ok):
    ax.set_xlim(-8, 220)
    ax.set_ylim(-24, 272)
    ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    # chassis
    ax.add_patch(Rectangle((0, 0), C.W, C.H, facecolor="#eef4fb",
                           edgecolor="#12395e", lw=1.6))
    # left wheel plates (X 0..40) and launcher (X 111..210)
    for y0, y1 in ((17.75, 92.25), (167.75, 242.25)):
        ax.add_patch(Rectangle((0, y0), 40, y1 - y0, facecolor="#c9d9e8",
                               edgecolor="#12395e", lw=1.0))
    ax.add_patch(Rectangle((FREE1, 4), C.W - FREE1, 252, facecolor="#ffe0b8",
                           edgecolor="#a05a00", lw=1.4))
    ax.text((FREE1 + C.W) / 2, 130, "发射机构底板\nX 111~210", fontsize=9.5,
            ha="center", va="center", color="#a05a00")
    # the free strip
    ax.add_patch(Rectangle((FREE0, 4), FREE1 - FREE0, 252, facecolor="#f2fbf2",
                           edgecolor="#2f6f2f", lw=1.2, ls=(0, (5, 3))))
    ax.text((FREE0 + FREE1) / 2, 254, f"空档 {FREE1 - FREE0:.0f}", fontsize=9.5,
            ha="center", color="#2f6f2f")

    if ok:
        cx, cy = C.BATT_CENTRE if hasattr(C, "BATT_CENTRE") else (75, 65)
        ax.add_patch(Rectangle((cx - W / 2, cy - L / 2), W, L,
                               facecolor="#e6d8f5", edgecolor="#6b3fa0",
                               lw=1.8))
        ax.text(cx, cy, "电池盒\n36.2 × 90.3\n（长边沿 Y）", fontsize=10,
                ha="center", va="center", color="#6b3fa0")
        ax.annotate("", xy=(cx - W / 2, cy + L / 2 + 8),
                    xytext=(cx + W / 2, cy + L / 2 + 8),
                    arrowprops=dict(arrowstyle="<->", color="#6b3fa0", lw=1.0))
        ax.text(cx, cy + L / 2 + 11, "36.2", fontsize=9, ha="center",
                color="#6b3fa0")
        ax.annotate("", xy=(cx + W / 2 + 7, cy - L / 2),
                    xytext=(cx + W / 2 + 7, cy + L / 2),
                    arrowprops=dict(arrowstyle="<->", color="#6b3fa0", lw=1.0))
        ax.text(cx + W / 2 + 10, cy, "90.3", fontsize=9, color="#6b3fa0",
                va="center", rotation=90)
        ax.text(110, -14, "36.2 < 71，放得下：左右各留 17", fontsize=10,
                ha="center", color="#2f6f2f", fontweight="bold")
    else:
        cy = 65.0
        x0 = FREE1 - L          # push its right end against the launcher
        ax.add_patch(Rectangle((x0, cy - W / 2), L, W, facecolor="#f7d9d9",
                               edgecolor="#c92a2a", lw=1.8))
        ax.add_patch(Rectangle((x0, cy - W / 2), FREE0 - x0, W,
                               facecolor="#c92a2a", alpha=0.35, zorder=5))
        ax.text(x0 + L / 2, cy + 26, "电池盒 90.3 × 36.2\n（长边沿 X，横着放）",
                fontsize=10, ha="center", color="#c92a2a")
        ax.annotate("", xy=(FREE0, cy - W / 2 - 8), xytext=(FREE1, cy - W / 2 - 8),
                    arrowprops=dict(arrowstyle="<->", color="#2f6f2f", lw=1.0))
        ax.text((FREE0 + FREE1) / 2, cy - W / 2 - 13, "空档只有 71", fontsize=9,
                ha="center", color="#2f6f2f")
        ax.text(110, -14, "90.3 > 71，横着放不进：左端压到左轮板上",
                fontsize=10, ha="center", color="#c92a2a", fontweight="bold")


def main():
    fig = plt.figure(figsize=(13.5, 8.6), dpi=170, facecolor="white")
    panel(fig.add_axes([0.03, 0.08, 0.45, 0.80]), "现在：竖着放（长边沿 Y）", True)
    panel(fig.add_axes([0.52, 0.08, 0.45, 0.80]), "横着放（长边沿 X）", False)
    fig.suptitle("电池盒为什么只能竖着放：左侧空档 71 < 90.3", fontsize=15,
                 fontweight="bold", y=0.965)
    fig.text(0.03, 0.02,
             "左侧空档 = 左轮板右边 X40 → 发射机构底板左边 X111 = 71 mm。"
             "电池盒长边 90.3 横着放不进；短边 36.2 竖着放还有 35 的余量（左右各 17）。",
             fontsize=9.8, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
