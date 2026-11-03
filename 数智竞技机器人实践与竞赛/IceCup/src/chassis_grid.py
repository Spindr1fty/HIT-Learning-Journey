r"""试验板：整块底盘按 10 mm 网格打满 Ø4.5 孔。

用途：用户拿实际板子摆件、标记，再告诉我们哪些孔不要了，最后从正式图里删。
所有孔都是 Ø4.5（M4 通孔），网格对齐 (0,0)，离外形轮廓至少 6 mm（孔边到边 >= 3.75）。

输出：
    D:\IceCup\dxf\chassis_grid.dxf          激光切割用（外形 + 网格孔）
    D:\IceCup\renders\chassis_grid.png      带坐标标注的图（方便口头指位置）
    D:\IceCup\newSTEP\chassis_grid_0.4mm.stl
    C:\Users\Spindrift\Desktop\底盘_试验网格_0.4mm.stl

跑法（from src/）：
    python chassis_grid.py [pitch]
"""

import math
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
import ezdxf

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import chassis as C  # noqa: E402
import chassis_stl as S  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent.parent
OUT_DXF = ROOT / "dxf" / "chassis_grid.dxf"
OUT_PNG = ROOT / "renders" / "chassis_grid.png"
OUT_STL = ROOT / "newSTEP" / "chassis_grid_0.4mm.stl"
DESK_STL = Path.home() / "Desktop" / "底盘_试验网格_0.4mm.stl"

PITCH = 10.0
EDGE = 6.0          # min distance hole centre -> outline
THICK = 0.4
W, H = C.W, C.H
DXF_DX, DXF_DY = C.DXF_DX, C.DXF_DY


# ----------------------------------------------------------- geometry utils --
def _seg_dist(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    t = 0.0 if l2 == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / l2))
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))


def _arc_dist(p, cx, cy, r, a0, a1):
    if a1 < a0:
        a1 += 360.0
    ang = math.degrees(math.atan2(p[1] - cy, p[0] - cx)) % 360.0
    if (ang - a0) % 360.0 <= (a1 - a0):
        return abs(math.hypot(p[0] - cx, p[1] - cy) - r)
    ends = [(cx + r * math.cos(math.radians(a)),
             cy + r * math.sin(math.radians(a))) for a in (a0, a1)]
    return min(math.dist(p, e) for e in ends)


def dist_to_outline(p):
    d = min(_seg_dist(p, (x0, y0), (x1, y1)) for x0, y0, x1, y1 in C.LINES)
    for cx, cy, r, a0, a1 in C.ARCS:
        d = min(d, _arc_dist(p, cx, cy, r, a0, a1))
    return d


def _outline_path():
    ring = S.ring()
    if math.dist(ring[0], ring[-1]) > 1e-6:
        ring = ring + [ring[0]]
    return MPath([(x, y) for x, y in ring])


def grid_holes(pitch=PITCH, edge=EDGE):
    poly = _outline_path()
    pts, inside_void, too_close = [], 0, 0
    k = 1
    while k * pitch < W:
        k2 = 1
        while k2 * pitch < H:
            p = (k * pitch, k2 * pitch)
            if not poly.contains_point(p):
                inside_void += 1          # 缺口里面，当然不要
            elif dist_to_outline(p) < edge:
                too_close += 1
            else:
                pts.append(p)
            k2 += 1
        k += 1
    print(f"  grid candidates (k*pitch inside the 210x260 box): "
          f"{inside_void} in the notch, {too_close} too close to an edge,"
          f" {len(pts)} kept")
    return pts


# ------------------------------------------------------------------ outputs --
def write_dxf(holes):
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for x0, y0, x1, y1 in C.LINES:
        msp.add_line((x0 + DXF_DX, y0 + DXF_DY), (x1 + DXF_DX, y1 + DXF_DY))
    for cx, cy, r, a0, a1 in C.ARCS:
        msp.add_arc((cx + DXF_DX, cy + DXF_DY), r, a0, a1)
    doc.layers.add("GRID", color=2)
    for x, y in holes:
        msp.add_circle((x + DXF_DX, y + DXF_DY), C.HOLE_D / 2.0,
                       dxfattribs={"layer": "GRID"})
    doc.saveas(str(OUT_DXF))
    print(f"wrote {OUT_DXF}  ({len(holes)} holes)")


def draw(holes, pitch=PITCH):
    fig = plt.figure(figsize=(13.0, 15.2), dpi=120, facecolor="white")
    ax = fig.add_axes([0.08, 0.05, 0.87, 0.87])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-18, W + 18)
    ax.set_ylim(-16, H + 16)
    for x0, y0, x1, y1 in C.LINES:
        ax.plot([x0, x1], [y0, y1], color="#12395e", lw=2.0, zorder=3)
    for cx, cy, r, a0, a1 in C.ARCS:
        if a1 < a0:
            a1 += 360.0
        ts = [math.radians(a0 + (a1 - a0) * i / 24) for i in range(25)]
        ax.plot([cx + r * math.cos(t) for t in ts],
                [cy + r * math.sin(t) for t in ts], color="#12395e", lw=2.0,
                zorder=3)
    # 10 mm grid lines
    for k in range(0, int(W) + 1, int(pitch)):
        ax.plot([k, k], [0, H], color="#eef2f6", lw=0.6, zorder=1)
    for k in range(0, int(H) + 1, int(pitch)):
        ax.plot([0, W], [k, k], color="#eef2f6", lw=0.6, zorder=1)
    for x, y in holes:
        ax.add_patch(plt.Circle((x, y), C.HOLE_D / 2, facecolor="white",
                                edgecolor="#c92a2a", lw=0.9, zorder=4))
    # 50 mm coordinate rulers
    for k in range(0, int(W) + 1, 50):
        ax.text(k, -6, str(k), fontsize=9, ha="center", color="#495057")
        ax.plot([k, k], [-4, 0], color="#495057", lw=0.8)
    for k in range(0, int(H) + 1, 50):
        ax.text(-6, k, str(k), fontsize=9, ha="right", va="center",
                color="#495057")
        ax.plot([-4, 0], [k, k], color="#495057", lw=0.8)
    ax.text(W / 2, -13, "X", fontsize=11, color="#495057")
    ax.text(-14, H / 2, "Y", fontsize=11, color="#495057")
    ax.text(137, 236, "缺口（挖穿）", fontsize=10, color="#12395e",
            ha="center", va="center")

    fig.suptitle(f"底盘试验板：{pitch:.0f}mm 网格 × Ø{C.HOLE_D} 孔，共 "
                 f"{len(holes)} 个（离边 ≥{EDGE:.0f}）",
                 fontsize=14.5, fontweight="bold", y=0.968)
    fig.text(0.08, 0.018,
             "原点 = 底盘左下角，X 向右 0~210，Y 向前 0~260（缺口侧）。"
             "把我标出来的孔号/坐标告给我，我从正式图里删。",
             fontsize=9.2, color="#495057")
    fig.savefig(OUT_PNG, facecolor="white")
    print("wrote", OUT_PNG)


def build_stl(holes, thick=THICK):
    pts = S.ring()
    if math.dist(pts[0], pts[-1]) < 1e-6:
        pts = pts[:-1]
    face = bd.Face(bd.Wire(bd.Polyline(*pts, close=True).edges()))
    solid = bd.extrude(face, amount=thick)
    b = solid.bounding_box()
    if b.min.Z < -1e-9:
        solid = bd.Pos(0, 0, -b.min.Z) * solid
        b = solid.bounding_box()
    cutters = [bd.Pos(x, y, b.min.Z - 0.1) * bd.Cylinder(
        C.HOLE_D / 2.0, (b.max.Z - b.min.Z) + 0.2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for x, y in holes]
    solid = solid.cut(*cutters).clean()
    print(f"solid valid={solid.is_valid}  volume {solid.volume:.0f} mm3")
    bd.export_stl(solid, str(OUT_STL), tolerance=0.005, angular_tolerance=0.2)
    shutil.copy2(OUT_STL, DESK_STL)
    print(f"wrote {OUT_STL}  and {DESK_STL}")


def main():
    pitch = float(sys.argv[1]) if len(sys.argv) > 1 else PITCH
    holes = grid_holes(pitch)
    print(f"grid pitch {pitch} mm, edge clearance {EDGE} mm -> {len(holes)} holes")
    xs = sorted({x for x, _ in holes})
    ys = sorted({y for _, y in holes})
    print(f"  X lines: {xs[0]:.0f}..{xs[-1]:.0f} ({len(xs)}),"
          f"  Y lines: {ys[0]:.0f}..{ys[-1]:.0f} ({len(ys)})")
    write_dxf(holes)
    draw(holes, pitch)
    build_stl(holes)


if __name__ == "__main__":
    main()
