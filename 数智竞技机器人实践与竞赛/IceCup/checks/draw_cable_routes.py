r"""Cable routing plan on the chassis (power lines, 5 x 11 mm terminals).

    python draw_cable_routes.py  ->  renders/chassis_cable_routes.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import chassis as C  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "chassis_cable_routes.png"

LANE = 16.0          # lane width reserved for a 5 x 11 terminal bundle
C_TRUNK = "#c92a2a"
C_LEFT = "#2f6f2f"
C_FRONT = "#a05a00"
C_RIGHT = "#6b3fa0"


def outline_ring(seg=20):
    import math as _m
    segs = [[(x0, y0), (x1, y1)] for x0, y0, x1, y1 in C.LINES]
    for cx, cy, r, a0, a1 in C.ARCS:
        if a1 < a0:
            a1 += 360.0
        segs.append([(cx + r * _m.cos(_m.radians(a0 + (a1 - a0) * i / seg)),
                      cy + r * _m.sin(_m.radians(a0 + (a1 - a0) * i / seg)))
                     for i in range(seg + 1)])
    pts = list(segs.pop(0))
    while segs:
        last = pts[-1]
        for i, s in enumerate(segs):
            if _m.dist(s[0], last) < 0.05:
                pts += s[1:]
                segs.pop(i)
                break
            if _m.dist(s[-1], last) < 0.05:
                pts += s[-2::-1]
                segs.pop(i)
                break
        else:
            break
    return pts


def route(ax, pts, color, label, lw=5.0, label_xy=None, rot=0):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
            solid_joinstyle="round", alpha=0.75, zorder=9)
    if label_xy:
        ax.text(label_xy[0], label_xy[1], label, fontsize=9.5, color=color,
                fontweight="bold", rotation=rot, ha="center", va="center",
                zorder=12)


def main():
    fig = plt.figure(figsize=(13.5, 15.0), dpi=170, facecolor="white")
    ax = fig.add_axes([0.06, 0.045, 0.88, 0.86])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-40, 250)
    ax.set_ylim(-28, 288)

    ax.add_patch(Polygon(outline_ring(), closed=True, facecolor="#eef4fb",
                         edgecolor="#12395e", lw=1.8, zorder=1))
    for g in C.wheel_groups():
        fx0, fy0, fx1, fy1 = g["foot"]
        ax.add_patch(Rectangle((fx0, fy0), fx1 - fx0, fy1 - fy0,
                               facecolor="#c9d9e8", edgecolor="#12395e",
                               lw=1.0, zorder=2))
        ax.text((fx0 + fx1) / 2, (fy0 + fy1) / 2, g["name"], fontsize=8.5,
                ha="center", va="center", color="#12395e", zorder=6)
    # launcher plate, Z module, battery stack
    ax.add_patch(Rectangle((111, 4), 99, 252, facecolor="#ffe0b8",
                           edgecolor="#a05a00", lw=1.3, zorder=2))
    ax.text(160, 130, "发射机构底板\n(底下有 10 空隙可走线)", fontsize=9,
            ha="center", va="center", color="#a05a00", zorder=6)
    ax.add_patch(Rectangle((C.Z_X0 - 25, C.Z_Y0 - 25), 50, 50,
                           facecolor="#c8e8c8", edgecolor="#2f6f2f", lw=1.2,
                           zorder=3))
    ax.text(C.Z_X0, C.Z_Y0, "导轨", fontsize=8.5, ha="center", va="center",
            color="#2f6f2f", zorder=6)
    ax.add_patch(Rectangle((C.Z_X0 - 22, C.Z_Y0 - 106), 44, 32,
                           facecolor="#f2e2cf", edgecolor="#a05a00", lw=1.2,
                           zorder=3))
    bx0, by0, bx1, by1 = C.battery_outline()
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           facecolor="#e6d8f5", edgecolor="#6b3fa0", lw=1.6,
                           zorder=3))
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2, "电池盒\n+ 主控\n(H62)", fontsize=9,
            ha="center", va="center", color="#6b3fa0", zorder=6)
    for x, y, layer in C.all_holes():
        ax.add_patch(Circle((x, y), C.HOLE_D / 2, facecolor="white",
                            edgecolor="#8a8f98", lw=0.9, zorder=5))

    # ---- routes
    # trunk: controller -> right gap (X 93..111) -> north and south
    route(ax, [(93, 95), (102, 95), (102, 160), (102, 200)], C_TRUNK,
          "主线（电源）", 6.0, (104, 175), 0)
    # left wheels: along X 42..56 lane
    route(ax, [(52, 20), (52, 95), (60, 100)], C_LEFT, "左后舵机", 5.0, (44, 60), 90)
    route(ax, [(52, 232), (52, 145), (52, 120), (60, 108)], C_LEFT, "左前舵机", 5.0, (44, 180), 90)
    ax.add_patch(Rectangle((46, 141), 6.5, 8, facecolor="#ffffff",
                           edgecolor="#2f6f2f", lw=1.2, ls=(0, (2, 1.5)),
                           zorder=11))
    ax.annotate("齿条脚挡路：\n底边开 12×6 过线槽", xy=(49, 145), xytext=(24, 145),
                fontsize=8.4, color="#2f6f2f", va="center", ha="center",
                arrowprops=dict(arrowstyle="->", color="#2f6f2f", lw=1.0),
                zorder=13)
    # right wheels: under the launcher plate (10 mm gap)
    route(ax, [(196, 20), (196, 60), (225, 60), (225, 240), (196, 240)],
          C_RIGHT, "右侧舵机（走发射底板下 10 空隙）", 5.0, (243, 150), 90)
    # front: Z servo + launcher servos back to the controller
    route(ax, [(102, 200), (68, 200), (68, 262), (68, 232)], C_FRONT,
          "升降舵机", 5.0, (44, 205), 0)
    route(ax, [(120, 240), (120, 200), (102, 200)], C_FRONT, "发射舵机", 5.0,
          (126, 225), 90)

    # ---- suggested tie-down points (3 mm holes, free areas only)
    ties = [(102, 120), (102, 140), (102, 180), (102, 215),
            (52, 30), (52, 60), (52, 90), (52, 200),
            (68, 175), (68, 192), (86, 122), (93.5, 70)]
    for x, y in ties:
        ax.add_patch(Circle((x, y), 2.5, facecolor="none", edgecolor="#111111",
                            lw=1.0, ls=(0, (2, 1.5)), zorder=11))
    ax.text(160, 8, "虚线圈 = 建议加的 Ø3 扎带孔", fontsize=8.5, color="#111111",
            ha="center", zorder=12)

    ax.text(0, 282, "走线安排（端子 5 厚 × 11 宽）", fontsize=15,
            fontweight="bold", color="#12395e")
    ax.text(150, 250, "升降舵机随滑块上下 195 → 用拖链/弹簧软管，\n沿导轨侧面走，顶盖下留回环",
            fontsize=8.6, color="#a05a00", ha="center", va="center", zorder=13)
    ax.text(0, -24,
            "端子要过的通道都 ≥ 12 宽：发射底板下 10 空隙（5 厚端子刚好过，留盘一圈）、"
            "左轮板与电池盒之间 17、电池盒与发射底板之间 18。转弯半径按 ≥ 8 留。",
            fontsize=9, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
