r"""Draw the holes read straight out of the exported chassis STEP.

Proves what is actually inside newSTEP/chassis.step.

    uvx ... python draw_step_holes.py  ->  renders/chassis_step_holes.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

sys.path.insert(0, str(Path(r"D:\IceCup\src").resolve()))
sys.path.insert(0, str(Path(r"D:\IceCup\checks").resolve()))

from cadgen import build123d as bd  # noqa: E402
import chassis as C  # noqa: E402


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

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(r"D:\IceCup\renders\chassis_step_holes.png")
STEP = Path(r"D:\IceCup\newSTEP\chassis.step")


def step_holes():
    shape = bd.import_step(str(STEP))
    out = []
    for f in shape.faces():
        if f.geom_type != bd.GeomType.CYLINDER:
            continue
        c = f.geom_adaptor().Cylinder()
        if abs(c.Axis().Direction().Z()) > 0.99 and abs(c.Radius() - C.HOLE_D / 2) < 0.01:
            loc = c.Location()
            out.append((loc.X(), loc.Y(), c.Radius()))
    return shape.bounding_box(), out


def main():
    b, holes = step_holes()
    batt = [(round(x, 2), round(y, 2)) for x, y in C.battery_holes()]
    print(f"STEP bbox: {b.min.X:.2f}..{b.max.X:.2f} x {b.min.Y:.2f}..{b.max.Y:.2f}"
          f" x {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"holes in STEP: {len(holes)}")
    for x, y in batt:
        near = min(holes, key=lambda h: (h[0] - x) ** 2 + (h[1] - y) ** 2)
        print(f"  battery hole wanted ({x}, {y})  ->  nearest in STEP "
              f"({near[0]:.2f}, {near[1]:.2f})  d={2 * near[2]:.2f}")

    fig = plt.figure(figsize=(10.5, 12.5), dpi=170, facecolor="white")
    ax = fig.add_axes([0.06, 0.05, 0.88, 0.86])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-24, 234)
    ax.set_ylim(-34, 285)
    ax.add_patch(Polygon(outline_ring(), closed=True, facecolor="#eef4fb",
                         edgecolor="#12395e", lw=1.8, zorder=1))
    for x0, y0, x1, y1 in C.EXT_RECTS:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0,
                               facecolor="#eef4fb", edgecolor="#7fa88a",
                               lw=0.9, ls=(0, (4, 3)), zorder=1.5))
    for x, y, r in holes:
        is_batt = any(abs(x - bx) < 0.2 and abs(y - by) < 0.2 for bx, by in batt)
        ax.add_patch(Circle((x, y), r, facecolor="white",
                            edgecolor="#6b3fa0" if is_batt else "#c92a2a",
                            lw=2.2 if is_batt else 1.2, zorder=6))
        if is_batt:
            ax.add_patch(Circle((x, y), 8, facecolor="none", edgecolor="#6b3fa0",
                                lw=1.0, ls=(0, (2, 2)), zorder=7))
    ax.annotate("电池盒 4 孔（竖放）\n(67,25.05) (67,104.95)\n(83,25.05) (83,104.95)",
                xy=(83, 104.95), xytext=(150, 150), fontsize=10,
                color="#6b3fa0",
                arrowprops=dict(arrowstyle="->", color="#6b3fa0", lw=1.2))
    ax.text(0, 270, "chassis.step 里实际的 44 个 Ø4.5 孔（按文件内容绘制）",
            fontsize=14, fontweight="bold", color="#12395e")
    ax.text(0, -29, "红=轮板 32 + 升降 8；紫=电池盒 4（两两竖直排列，间距 79.9）",
            fontsize=9.5, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
