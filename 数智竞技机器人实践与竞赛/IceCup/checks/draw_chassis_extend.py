r"""Proposal: extend the chassis a little for cable pass-through holes + tie posts.

    python draw_chassis_extend.py  ->  renders/chassis_extend_proposal.png
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
OUT = ROOT / "renders" / "chassis_extend_proposal.png"

EXT = 20.0            # how far each side grows
SQ = 14.0             # square pass-through hole
POST_D = 7.0          # cable post diameter
POST_H = 10.0         # cable post height
NOTCH_L, NOTCH_R = 102.64, 171.35     # notch mouth on the front edge

# extensions: (x0, y0, x1, y1) added to the plate
EXT_SOLID = [
    (0.0, -EXT, C.W, 0.0),              # rear strip
    (0.0, C.H, NOTCH_L, C.H + EXT),     # front strip, left of the notch
    (NOTCH_R, C.H, C.W, C.H + EXT),     # front strip, right of the notch
    (-EXT, 105.0, 0.0, 155.0),          # left ear (between the wheels)
    (C.W, 105.0, C.W + EXT, 155.0),     # right ear
]
# square pass-through holes (centres)
SQ_POS = [(55.0, -10.0), (105.0, -10.0), (155.0, -10.0),
          (-10.0, 118.0), (-10.0, 142.0),
          (C.W + 10.0, 118.0), (C.W + 10.0, 142.0),
          (45.0, C.H + 10.0), (192.0, C.H + 10.0)]
# cable posts (top side)
POSTS = [(-10.0, 128.0), (C.W + 10.0, 128.0),
         (25.0, -10.0), (185.0, -10.0), (105.0, -10.0),
         (52.0, 30.0), (52.0, 90.0), (52.0, 200.0),
         (102.0, 120.0), (102.0, 175.0), (68.0, 178.0), (93.5, 60.0)]


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


def main():
    fig = plt.figure(figsize=(13.0, 15.0), dpi=170, facecolor="white")
    ax = fig.add_axes([0.05, 0.20, 0.90, 0.72])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-70, 285)
    ax.set_ylim(-40, 315)

    # wheels (must not be covered by the extension)
    for g in C.wheel_groups():
        xr = g["wheel_x"]
        wy = g["wheel_y"]
        ax.add_patch(Rectangle((xr[0], wy - C.WHEEL_D / 2), xr[1] - xr[0],
                               C.WHEEL_D, facecolor="#f7d9d9",
                               edgecolor="#c92a2a", lw=1.0, alpha=0.55,
                               zorder=1))
    for i, (x0, y0, x1, y1) in enumerate(EXT_SOLID):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="#c8e8c8",
                               edgecolor="#2f6f2f", lw=1.3, zorder=2))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, f"+{EXT:.0f}", fontsize=8.5,
                ha="center", va="center", color="#2f6f2f", zorder=6)
    ax.add_patch(Polygon(outline_ring(), closed=True, facecolor="#eef4fb",
                         edgecolor="#12395e", lw=1.8, zorder=3))

    for x, y in SQ_POS:
        ax.add_patch(Rectangle((x - SQ / 2, y - SQ / 2), SQ, SQ,
                               facecolor="white", edgecolor="#c92a2a", lw=1.8,
                               zorder=8))
    for x, y in POSTS:
        ax.add_patch(Circle((x, y), POST_D / 2, facecolor="#ffe0b8",
                            edgecolor="#a05a00", lw=1.4, zorder=9))
        ax.add_patch(Circle((x, y), 1.25, facecolor="white",
                            edgecolor="#a05a00", lw=0.8, zorder=10))

    ax.text(105, 300, f"底盘加大 + 走线方孔 + 固定柱（建议）", fontsize=15,
            fontweight="bold", ha="center", color="#12395e")
    fig.text(0.05, 0.155, f"绿 = 往外加 {EXT:.0f}：后边整条、前边缺口两侧各一条、左右各一个耳朵卡在两轮之间",
             fontsize=10, color="#2f6f2f")
    fig.text(0.05, 0.115, f"红方框 = {SQ:.0f}×{SQ:.0f} 过线孔 ×{len(SQ_POS)}（端子 5×11 能过，四周留 3）",
             fontsize=10, color="#c92a2a")
    fig.text(0.05, 0.075, f"橙圆 = Ø{POST_D:.0f}×{POST_H:.0f} 走线柱 ×{len(POSTS)}（柱心 Ø2.5 通孔穿扎带）",
             fontsize=10, color="#a05a00")
    fig.text(0.05, 0.035, "粉红 = 轮子位置：左右不能整条加宽，只能做耳朵，否则压到轮子。"
             f"加完外形 {C.W + 2 * EXT:.0f} × {C.H + 2 * EXT:.0f}（限 350×350），轮子仍最外 278.3 × 300",
             fontsize=10, color="#c92a2a")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
