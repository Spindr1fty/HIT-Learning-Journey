r"""Chassis installation layout: everything mounted except the battery box.

    python draw_chassis_layout_all.py  ->  renders/chassis_layout_all.png
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "checks"))

import chassis as C  # noqa: E402
import mesh_chamfer as MC  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = ROOT / "renders" / "chassis_layout_all.png"

C_EDGE = "#12395e"
C_CHASSIS = "#eef4fb"
C_WHEEL = "#f7d9d9"
C_PLATE = "#c9d9e8"
C_Z = "#c8e8c8"
C_LAUNCH = "#ffe0b8"
C_HOLE = "#c92a2a"
C_BATT = "#6b3fa0"


def section_plan(path, z_frac=0.5):
    """Outline polygons of a 3MF mesh at a mid height, back in the file's XY."""
    v, t = MC.load_3mf(Path(path))
    m = MC.clean(v, t)
    lo, hi = m.bounds
    z = lo[2] + (hi[2] - lo[2]) * z_frac
    sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return []
    p2d, to_3d = sec.to_planar()

    def back(coords):
        pts = []
        for x, y in np.array(coords):
            p3 = to_3d @ np.array([x, y, 0.0, 1.0])
            pts.append((p3[0], p3[1]))
        return np.array(pts)

    out = []
    for poly in p2d.polygons_full:
        out.append((back(poly.exterior.coords),
                    [back(h.coords) for h in poly.interiors]))
    return out


def draw_polys(ax, polys, color, ec, lw=1.2, alpha=0.9, holes=False):
    for ext, ints in polys:
        ax.add_patch(Polygon(ext, closed=True, facecolor=color, edgecolor=ec,
                             lw=lw, alpha=alpha, zorder=6))
        if holes:
            for hp in ints:
                ax.add_patch(Polygon(hp, closed=True, facecolor="white",
                                     edgecolor=ec, lw=lw, zorder=7))


def outline_ring(seg=20):
    """Stitch LINES + ARCS into one closed ring (same idea as chassis_stl)."""
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
    fig = plt.figure(figsize=(13.5, 15.5), dpi=170, facecolor="white")
    ax = fig.add_axes([0.06, 0.05, 0.88, 0.88])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-56, 268)
    ax.set_ylim(-44, 292)

    # ---- chassis outline
    for x0, y0, x1, y1 in C.LINES:
        ax.plot([x0, x1], [y0, y1], color=C_EDGE, lw=2.0, zorder=3,
                solid_capstyle="round")
    import math
    for cx, cy, r, a0, a1 in C.ARCS:
        if a1 < a0:
            a1 += 360.0
        ts = [math.radians(a0 + (a1 - a0) * i / 24) for i in range(25)]
        ax.plot([cx + r * math.cos(t) for t in ts],
                [cy + r * math.sin(t) for t in ts], color=C_EDGE, lw=2.0,
                zorder=3)
    # fill with the real outline (notch included)
    from matplotlib.patches import Polygon as MPoly
    ring = outline_ring()
    ax.add_patch(MPoly(np.array(ring), closed=True, facecolor=C_CHASSIS,
                       edgecolor="none", zorder=1))
    # cable-routing growth: rear strip + two ears (dashed = same plane)
    for x0, y0, x1, y1 in C.EXT_RECTS:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0,
                               facecolor=C_CHASSIS, edgecolor="#7fa88a",
                               lw=0.9, ls=(0, (4, 3)), zorder=1.5))

    # ---- wheels + wheel plates
    for g in C.wheel_groups():
        fx0, fy0, fx1, fy1 = g["foot"]
        ax.add_patch(Rectangle((fx0, fy0), fx1 - fx0, fy1 - fy0,
                               facecolor=C_PLATE, edgecolor=C_EDGE, lw=1.2,
                               alpha=0.85, zorder=4))
        ax.text((fx0 + fx1) / 2, (fy0 + fy1) / 2, g["name"], fontsize=9,
                ha="center", va="center", color="#12395e", zorder=9)
        xr = g["wheel_x"]
        wy = g["wheel_y"]
        ax.add_patch(Rectangle((xr[0], wy - C.WHEEL_D / 2),
                               xr[1] - xr[0], C.WHEEL_D,
                               facecolor=C_WHEEL, edgecolor="#c92a2a",
                               lw=1.3, zorder=5))
        ax.text((xr[0] + xr[1]) / 2, wy + C.WHEEL_D / 2 + 4,
                "轮 26×54", fontsize=8, ha="center", color="#c92a2a", zorder=9)

    # ---- Z module (plan)
    # rail 30x30 + foot 50x50
    ax.add_patch(Rectangle((C.Z_X0 - 15, C.Z_Y0 - 15), 30, 30,
                           facecolor=C_Z, edgecolor="#2f6f2f", lw=1.4,
                           zorder=5))
    ax.add_patch(Rectangle((C.Z_X0 - 25, C.Z_Y0 - 25), 50, 50,
                           facecolor="none", edgecolor="#2f6f2f", lw=1.0,
                           ls=(0, (4, 3)), zorder=6))
    ax.text(C.Z_X0, C.Z_Y0, "导轨\n30×30", fontsize=8.5, ha="center",
            va="center", color="#2f6f2f", zorder=9)
    # rack foot + rack mast
    ax.add_patch(Rectangle((C.Z_X0 - 22, C.Z_Y0 - 90 - 16), 44, 32,
                           facecolor="#f2e2cf", edgecolor="#a05a00", lw=1.2,
                           zorder=5))
    ax.add_patch(Rectangle((C.Z_X0 - 8, C.Z_Y0 - 96.5), 16, 20,
                           facecolor=C_Z, edgecolor="#2f6f2f", lw=1.0,
                           zorder=6))
    ax.text(C.Z_X0, C.Z_Y0 - 90 - 6, "齿条脚 44×32", fontsize=8, ha="center",
            color="#a05a00", zorder=9)
    # cap outline (above)
    ax.add_patch(Rectangle((46.8, 131.0), 42.4, 124.4, facecolor="none",
                           edgecolor="#2f6f2f", lw=1.0, ls=(0, (1, 3)),
                           zorder=6))
    ax.text(44, 150, "顶盖（Z 306 以上）", fontsize=8, rotation=90,
            va="center", ha="right", color="#2f6f2f", zorder=9)
    # fork direction
    ax.annotate("", xy=(C.Z_X0, 292), xytext=(C.Z_X0, 262),
                arrowprops=dict(arrowstyle="-|>", color="#c92a2a", lw=2.2))
    ax.text(C.Z_X0 + 3, 285, "叉子朝前", fontsize=9, color="#c92a2a")

    # ---- launcher (base_plate + rack + plunger), real outlines
    for path, zf, col in ((r"C:\Users\Spindrift\Desktop\base_plate.3mf", 0.04, C_LAUNCH),):
        polys = section_plan(path, zf)
        if polys:
            draw_polys(ax, polys, col, "#a05a00", lw=1.1, holes=True)
    ax.text((111 + 210) / 2, 20, "发射机构底板 99×252\n（与右侧 16 个轮板孔共用）",
            fontsize=9, ha="center", va="center", color="#a05a00", zorder=9)

    # ---- holes
    for x, y, layer in C.all_holes():
        col = C_BATT if layer == "BATT" else C_HOLE
        ax.add_patch(Circle((x, y), C.HOLE_D / 2, facecolor="white",
                            edgecolor=col, lw=1.2, zorder=10))
    bx0, by0, bx1, by1 = C.battery_outline()
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           facecolor="#e6d8f5", edgecolor=C_BATT, lw=1.4,
                           zorder=8))
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2,
            "电池盒 + 主控盒\n高 62（总）", fontsize=9, ha="center",
            va="center", color=C_BATT, zorder=11)

    # ---- centre lines + dims
    ax.plot([C.W / 2, C.W / 2], [-44, 292], color=C_HOLE, lw=0.8,
            ls=(0, (8, 3, 1, 3)), alpha=0.5, zorder=2)
    ax.plot([-56, 268], [C.H / 2, C.H / 2], color="#2f6f2f", lw=0.8,
            ls=(0, (8, 3, 1, 3)), alpha=0.5, zorder=2)
    ax.text(C.W / 2 + 2, 266, "X = 105", fontsize=9, color=C_HOLE)
    ax.text(-54, C.H / 2 + 2, "Y = 130", fontsize=9, color="#2f6f2f")
    ax.annotate("", xy=(0, -28), xytext=(C.W, -28),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(C.W / 2, -35, "210（基准轮廓）", fontsize=10, ha="center",
            color="#5b6773")
    ax.annotate("", xy=(-44, 0), xytext=(-44, C.H),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(-50, C.H / 2, "260", fontsize=10, color="#5b6773", va="center",
            rotation=90)

    fig.suptitle("底盘安装布局（电池盒除外）", fontsize=17, fontweight="bold",
                 y=0.975)
    fig.text(0.06, 0.025,
             "实线=底盘 210×260 基准轮廓；虚线绿=后边/两侧各加 20 的走线区（实体里连成一体）；浅蓝=轮板（g_mount_b 底脚 40×74.5）；"
             "红框=车轮 Ø54 × 宽 26（全在底盘外）；绿=升降机构（导轨 30×30 + 导轨脚 50×50 + 齿条脚 44×32）；"
             "橙=发射机构底板 99×252 外形；紫=电池盒 + 主控盒叠装体（总高 62）。",
             fontsize=9.6, color="#495057")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
