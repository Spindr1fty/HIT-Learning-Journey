r"""底盘（激光切割件）—— 唯一的权威源。

整合了之前散在 checks/ 里的七八个脚本。现在只保留这一个文件：
  * 外形：10 条线 + 10 段圆弧（从用户的 底盘.dwg 量出来的，已经去重）
  * 32 个轮板孔：4 组 × 8，左右 + 前后双向镜像（板脚外缘与底盘边齐平）
  * 8 个升降机构孔：导轨脚 4 + 齿条脚 4（z_plate 底板取消，直接上底盘）

坐标系（本文件内部一律用它）：
    原点 = 底盘左下角，X 向右 0..210，Y 向上（缺口那侧为前）0..260，mm
输出的 DXF 会平移回用户原 DWG 的坐标（dx = -2.42, dy = -348.76），
这样和原来那张 底盘.dwg 完全对得上。

输出（运行一次全部重出）：
    D:\IceCup\dxf\chassis.dxf          参考图（外形 + 44 个 Ø4.5；切割已放弃）
    D:\IceCup\renders\chassis_top.png  标注图
    stdout                            孔的坐标清单

跑法：
    cd D:\IceCup\src
    python chassis.py
"""

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

import ezdxf

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent.parent
OUT_DXF = ROOT / "dxf" / "chassis.dxf"
OUT_PNG = ROOT / "renders" / "chassis_top.png"

W, H = 210.0, 260.0                     # chassis size
PLATE_T = 6.0                           # final printed plate thickness (PLA)
DXF_DX, DXF_DY = 0.0, 0.0               # 输出的 DXF 直接用本坐标系：
                                        # 原点=底盘左下角，X 向右，Y 向前

# ---------------------------------------------------------------- outline ---
# (x0, y0, x1, y1) in my frame
LINES = [
    (5.00, 260.00, 102.64, 260.00),     # front edge, left of the notch
    (171.35, 260.00, 205.00, 260.00),   # front edge, right of the notch
    (210.00, 5.00, 210.00, 255.00),     # right edge
    (5.00, 0.00, 205.00, 0.00),         # rear edge
    (0.00, 255.00, 0.00, 5.00),         # left edge
    (104.50, 258.74, 111.85, 240.36),   # notch, left slant
    (112.00, 239.61, 112.00, 205.07),   # notch, left wall
    (114.00, 203.07, 160.00, 203.07),   # notch, bottom
    (162.00, 205.07, 162.00, 239.61),   # notch, right wall
    (169.49, 258.74, 162.14, 240.36),   # notch, right slant
]
# (cx, cy, r, a0, a1) degrees, CCW from a0 to a1
ARCS = [
    (5.00, 255.00, 5.0, 90.0, 180.0),       # outer corners R5
    (205.00, 255.00, 5.0, 0.0, 90.0),
    (205.00, 5.00, 5.0, 270.0, 360.0),
    (5.00, 5.00, 5.0, 180.0, 270.0),
    (102.64, 258.00, 2.0, 21.8, 90.0),      # notch corners R2
    (110.00, 239.61, 2.0, 0.0, 21.8),
    (114.00, 205.07, 2.0, 180.0, 270.0),
    (160.00, 205.07, 2.0, 270.0, 360.0),
    (164.00, 239.61, 2.0, 158.2, 180.0),
    (171.35, 258.00, 2.0, 90.0, 158.2),
]

# ------------------------------------------------------- wheel plate holes --
# g_mount_b 底板：40 x 74.5，8 个 Ø4.5 孔（4 x 2），板脚外缘与底盘边齐平。
# 左右用同一块板：右边两块把舵机在板里翻 180° 装，让轴心偏移翻到另一侧，
# 于是四组孔关于 X=105 和 Y=130 都严格镜像。
PLATE_HOLE_X = (8.0, 16.196, 24.392, 32.588)     # 板内坐标
PLATE_Y0, PLATE_Y1 = 12.94, 87.44                # 板脚在板内的 Y 范围
FOOT_TALL = PLATE_Y1 - PLATE_Y0                  # 74.5
SHAFT_PY = 40.19                                 # 舵机轴在板内的 Y（正常装法）
SHAFT_PY_FLIP = 60.19                            # 翻 180° 装时的 Y
WHEEL_Y = {"front": 195.0, "rear": 65.0}
WHEEL_D, WHEEL_T = 54.0, 26.0
SHAFT_PX = -8.15
HOLE_D = 4.5

# (name, side, front/rear, servo_flipped)  -- 对角相同，保证双向镜像
WHEEL_CORNERS = (
    ("左前", "L", "front", False),
    ("右前", "R", "front", True),
    ("左后", "L", "rear", True),
    ("右后", "R", "rear", False),
)

# ------------------------------------------------------------ Z-axis holes --
# 来自 z_plate.py（底板取消后，导轨脚和齿条脚直接上底盘）
#   导轨脚 4 x Ø4.5 @ (±18, ±18)      36 x 36
#   齿条脚 4 x Ø4.5 @ (-96/-84, ±14)  12 x 28，距导轨轴心 90
RAIL_PAT = [(x, y) for x in (-18.0, 18.0) for y in (-18.0, 18.0)]
RACK_PAT = [(x, y) for x in (-96.0, -84.0) for y in (-14.0, 14.0)]
Z_X0, Z_Y0 = 68.0, 235.0        # 导轨轴心；导轨脚 50x50 前缘正好顶到底盘前边
RAIL_FOOT, RACK_FOOT = 50.0, (44.0, 32.0)   # 转 90° 后的外形


# ------------------------------------------------------ battery box holes --
# Measured base plate: 90.3 x 36.2 x 5.5, four dia 4.0 through holes at
# (X +-39.95, Y +-8.00) about the plate's centre (X along the 90.3 edge).
# On the chassis: box centred at (105, 46) with its long edge along X, holes
# opened at dia 4.5 so the bolts get 0.5 of assembly slack.
# The launcher's base plate (base_plate.3mf, 99 x 252) is bolted onto the SAME
# 16 screws as the right-front and right-rear wheel brackets (checked: its own
# 16 holes sit within 0.015 mm of those), so it owns the right half X 111..210.
# The battery box therefore moved to the left-middle strip and is turned 90 deg:
# its long 90.3 edge now runs along Y.
BATT_CENTRE = (75.0, 65.0)
BATT_L, BATT_W = 90.3, 36.2          # long edge along the box's local X
BATT_ROT90 = True                    # long edge along the chassis Y
BATT_HOLE_DX, BATT_HOLE_DY = 39.95, 8.0   # along the long / short edge


def battery_holes():
    cx, cy = BATT_CENTRE
    dx, dy = ((BATT_HOLE_DY, BATT_HOLE_DX) if BATT_ROT90
              else (BATT_HOLE_DX, BATT_HOLE_DY))
    return [(cx + sx * dx, cy + sy * dy)
            for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)]


def battery_outline():
    cx, cy = BATT_CENTRE
    hx, hy = ((BATT_W / 2.0, BATT_L / 2.0) if BATT_ROT90
              else (BATT_L / 2.0, BATT_W / 2.0))
    return (cx - hx, cy - hy, cx + hx, cy + hy)


# launcher base plate footprint (base_plate.3mf), for reference on the drawing
BASE_PLATE_BOX = (111.0, 4.0, 210.0, 256.0)


# ------------------------------------------- cable routing features (2026-10-24) --
# The plate grows only where nothing can hit it: a rear strip and two small
# ears between the wheels (the wheels sit at X -34.15..-8.15 and 218.15..244.15,
# Y 38..92 and 168..222).  NOTHING moves: the frame and all 44 mounting holes
# stay exactly where they were.  The two front strips were dropped on
# 2026-10-24 -- the right one sits in front of the launcher base (Y 256) and
# the arm's sweep is still a placeholder, so it is not worth the risk.
EXT = 20.0                                  # growth per side
EXT_RECTS = [                               # (x0, y0, x1, y1) added to the plate
    (0.0, -EXT, W, 0.0),                    # rear strip
    (-EXT, 105.0, 0.0, 155.0),              # left ear, between the wheels
    (W, 105.0, W + EXT, 155.0),             # right ear, between the wheels
]
SQ = 14.0                                   # square pass-through hole
SQ_POS = [                                  # centres
    (55.0, -10.0), (105.0, -10.0), (155.0, -10.0),
    (-10.0, 118.0), (-10.0, 142.0),
    (W + 10.0, 118.0), (W + 10.0, 142.0),
]
# 2026-10-24 evening: the round posts were rejected.  Three flat zip-tie eyes
# instead: an 18 x 3 wall, 12 tall, with an 8 x 5 window through the 3 mm
# thickness for a standard cable tie.  The wall's long axis follows the cable,
# so the tie loops around the bundle through the window.
EYE_L, EYE_T, EYE_H = 18.0, 3.0, 12.0
EYE_WIN_L, EYE_WIN_Z0, EYE_WIN_H = 8.0, 4.0, 5.0
EYE_POS = [                                 # (cx, cy, long axis along Y)
    (48.0, 60.0, True),                     # left lane, rear
    (48.0, 175.0, True),                    # left lane, front
    (102.0, 120.0, True),                   # lane between battery and launcher
]


def eye_rect(cx, cy, along_y=True):
    if along_y:
        return (cx - EYE_T / 2.0, cy - EYE_L / 2.0,
                cx + EYE_T / 2.0, cy + EYE_L / 2.0)
    return (cx - EYE_L / 2.0, cy - EYE_T / 2.0,
            cx + EYE_L / 2.0, cy + EYE_T / 2.0)


def zmap(x, y):
    """z_plate 坐标 -> 底盘坐标（模块整体转 90°：叉子朝 +Y）。"""
    return (Z_X0 - y, Z_Y0 + x)


def wheel_group(side, wy, flipped):
    """-> (plate->chassis 映射, 轮子 X 范围, 板脚 X/Y 范围)."""
    s = SHAFT_PY_FLIP if flipped else SHAFT_PY
    if side == "L":
        ox = 0.0                    # 板脚外缘贴底盘左边
        oy = wy - s
        mp = lambda px, py: (ox + px, oy + py)          # noqa: E731
        return mp, (-SHAFT_PX - WHEEL_T, -SHAFT_PX)
    oxr = W                        # 板脚外缘贴底盘右边
    oyr = wy + s
    mp = lambda px, py: (oxr - px, oyr - py)            # noqa: E731
    return mp, (W + SHAFT_PX, W + SHAFT_PX + WHEEL_T)


def wheel_groups():
    out = []
    for name, side, pos, flipped in WHEEL_CORNERS:
        wy = WHEEL_Y[pos]
        mp, xr = wheel_group(side, wy, flipped)
        fx0, fy0 = mp(0.0, PLATE_Y0)
        fx1, fy1 = mp(40.0, PLATE_Y1)
        out.append({
            "name": name, "map": mp, "wheel_x": xr, "wheel_y": wy,
            "flipped": flipped,
            "foot": (min(fx0, fx1), min(fy0, fy1),
                     max(fx0, fx1), max(fy0, fy1)),
            "holes": [mp(hx, hy) for hx in PLATE_HOLE_X
                      for hy in (19.94, 80.44)],
        })
    return out


def z_holes():
    return [zmap(*p) for p in RAIL_PAT + RACK_PAT]


def all_holes():
    h = [(x, y, "WHEEL") for g in wheel_groups() for x, y in g["holes"]]
    h += [(x, y, "Z") for x, y in z_holes()]
    h += [(x, y, "BATT") for x, y in battery_holes()]
    return h


# ----------------------------------------------------------------- output ---
def write_dxf():
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for x0, y0, x1, y1 in LINES:
        msp.add_line((x0 + DXF_DX, y0 + DXF_DY), (x1 + DXF_DX, y1 + DXF_DY))
    for cx, cy, r, a0, a1 in ARCS:
        msp.add_arc((cx + DXF_DX, cy + DXF_DY), r, a0, a1)
    doc.layers.add("WHEEL", color=4)
    doc.layers.add("Z", color=2)
    doc.layers.add("BATT", color=6)
    for x, y, layer in all_holes():
        msp.add_circle((x + DXF_DX, y + DXF_DY), HOLE_D / 2.0,
                       dxfattribs={"layer": layer})
    doc.saveas(str(OUT_DXF))
    print(f"wrote {OUT_DXF}   ({len(all_holes())} holes)")


def draw():
    fig = plt.figure(figsize=(13.0, 14.6), dpi=120, facecolor="white")
    ax = fig.add_axes([0.09, 0.05, 0.86, 0.88])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-60, W + 60)
    ax.set_ylim(-16, H + 16)

    # outline
    seg = []
    for x0, y0, x1, y1 in LINES:
        ax.plot([x0, x1], [y0, y1], color="#12395e", lw=2.0, zorder=3,
                solid_capstyle="round")
    for cx, cy, r, a0, a1 in ARCS:
        if a1 < a0:
            a1 += 360.0
        ts = [math.radians(a0 + (a1 - a0) * i / 24) for i in range(25)]
        ax.plot([cx + r * math.cos(t) for t in ts],
                [cy + r * math.sin(t) for t in ts], color="#12395e", lw=2.0,
                zorder=3)
    ax.plot([W / 2, W / 2], [-16, H + 16], color="#c92a2a", lw=0.9,
            ls=(0, (7, 4, 1, 4)), alpha=0.55, zorder=2)
    ax.plot([-60, W + 60], [H / 2, H / 2], color="#2f6f2f", lw=0.9,
            ls=(0, (7, 4, 1, 4)), alpha=0.55, zorder=2)
    ax.text(W / 2 + 2, -12, "X = 105", fontsize=9, color="#c92a2a")
    ax.text(-58, H / 2 + 2, "Y = 130", fontsize=9, color="#2f6f2f")

    # wheels + plates
    for g in wheel_groups():
        fx0, fy0, fx1, fy1 = g["foot"]
        ax.add_patch(Rectangle((fx0, fy0), fx1 - fx0, fy1 - fy0,
                               facecolor="#dbe9f7", edgecolor="#1b3b5a",
                               lw=1.4, alpha=0.85, zorder=5))
        for x, y in g["holes"]:
            ax.add_patch(Circle((x, y), HOLE_D / 2, facecolor="white",
                                edgecolor="#9db4cc", lw=1.1, zorder=7))
        xr = g["wheel_x"]
        ax.add_patch(Rectangle((xr[0], g["wheel_y"] - WHEEL_D / 2),
                               xr[1] - xr[0], WHEEL_D, facecolor="#ffe3e3",
                               edgecolor="#c92a2a", lw=1.3, zorder=6))
        ax.text((xr[0] + xr[1]) / 2, g["wheel_y"] + WHEEL_D / 2 + 2.5,
                f"{g['name']}轮", fontsize=8.2, ha="center", color="#c92a2a")

    # Z module
    ax.add_patch(Rectangle((Z_X0 - RAIL_FOOT / 2, Z_Y0 - RAIL_FOOT / 2),
                           RAIL_FOOT, RAIL_FOOT, facecolor="#e7f5e7",
                           edgecolor="#2f6f2f", lw=1.5, alpha=0.9, zorder=5))
    rw, rh = RACK_FOOT
    ax.add_patch(Rectangle((Z_X0 - rw / 2, Z_Y0 - 90 - rh / 2), rw, rh,
                           facecolor="#ffe8cc", edgecolor="#a05a00", lw=1.4,
                           alpha=0.9, zorder=5))
    for x, y in z_holes():
        ax.add_patch(Circle((x, y), HOLE_D / 2, facecolor="white",
                            edgecolor="#2f6f2f", lw=1.6, zorder=8))
    ax.add_patch(FancyArrowPatch(zmap(0, 0), zmap(58, 0), arrowstyle="-|>",
                                 mutation_scale=13, color="#c92a2a", lw=2.0,
                                 zorder=9))
    ax.text(zmap(30, 0)[0] + 2, zmap(30, 0)[1], "叉子朝前", fontsize=9,
            color="#c92a2a")
    ax.text(Z_X0 + 28, Z_Y0 + 2, f"导轨轴心\n({Z_X0:.0f},{Z_Y0:.0f})",
            fontsize=8.6, color="#2f6f2f")
    ax.text(Z_X0 - 21, Z_Y0 - 90 - 26, "齿条脚", fontsize=8.2, color="#a05a00")
    ax.text(118, 246, "缺口", fontsize=9.5, color="#12395e", ha="left")
    # cable-routing additions
    for ex0, ey0, ex1, ey1 in EXT_RECTS:
        ax.add_patch(Rectangle((ex0, ey0), ex1 - ex0, ey1 - ey0,
                               facecolor="#c8e8c8", edgecolor="#2f6f2f",
                               lw=1.2, alpha=0.55, zorder=4))
    for sx, sy in SQ_POS:
        ax.add_patch(Rectangle((sx - SQ / 2, sy - SQ / 2), SQ, SQ,
                               facecolor="white", edgecolor="#c92a2a",
                               lw=1.6, zorder=8))
    for cx, cy, along_y in EYE_POS:
        ex0, ey0, ex1, ey1 = eye_rect(cx, cy, along_y)
        ax.add_patch(Rectangle((ex0, ey0), ex1 - ex0, ey1 - ey0,
                               facecolor="#ffe0b8", edgecolor="#a05a00",
                               lw=1.2, zorder=9))
        if along_y:
            for wy in (cy - EYE_WIN_L / 2.0, cy + EYE_WIN_L / 2.0):
                ax.plot([ex0, ex1], [wy, wy], color="#a05a00", lw=0.9,
                        ls=(0, (1.5, 1.5)), zorder=10)
        else:
            for wx in (cx - EYE_WIN_L / 2.0, cx + EYE_WIN_L / 2.0):
                ax.plot([wx, wx], [ey0, ey1], color="#a05a00", lw=0.9,
                        ls=(0, (1.5, 1.5)), zorder=10)
    ax.set_xlim(-EXT - 14, W + EXT + 14)
    ax.set_ylim(-EXT - 20, H + EXT + 20)
    bx0, by0, bx1, by1 = battery_outline()
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           facecolor="none", edgecolor="#6b3fa0", lw=1.3,
                           ls=(0, (6, 4)), zorder=6))
    for x, y in battery_holes():
        ax.add_patch(Circle((x, y), HOLE_D / 2, facecolor="white",
                            edgecolor="#6b3fa0", lw=1.6, zorder=8))
    qx0, qy0, qx1, qy1 = BASE_PLATE_BOX
    ax.add_patch(Rectangle((qx0, qy0), qx1 - qx0, qy1 - qy0,
                           facecolor="none", edgecolor="#a05a00", lw=1.2,
                           ls=(0, (2, 3)), zorder=5))
    ax.text((qx0 + qx1) / 2, qy0 + 8,
            "发射机构底板 99×252\n（与右侧 16 个轮板孔共用）",
            fontsize=8.2, ha="center", va="bottom", color="#a05a00", zorder=9)
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2,
            f"电池盒 90.3 × 36.2（长边沿 Y）\n4 × Ø4.5（孔心 ±8 / ±39.95）",
            fontsize=8.4, ha="center", va="center", color="#6b3fa0",
            zorder=9)
    ax.text(5, -33, f"外形 210 × 260（{PLATE_T:.0f} mm PLA），四角 R5，内角 R2",
            fontsize=9, color="#495057")
    ax.text(5, -27, "44 孔（Ø4.5）不动；绿=后边/耳朵加 20；红方框=过线孔；橙条=扎带眼",
            fontsize=9, color="#495057")
    ax.text(W / 2, -10, "", fontsize=1)

    fig.suptitle(f"底盘（{PLATE_T:.0f} mm PLA）—— 44 孔 + 7 个 14×14 过线方孔 + 3 个扎带眼，单位 mm",
                 fontsize=15, fontweight="bold", y=0.965)
    fig.savefig(OUT_PNG, facecolor="white")
    print("wrote", OUT_PNG)


def report():
    print()
    print("wheel plates (chassis frame):")
    for g in wheel_groups():
        fx0, fy0, fx1, fy1 = g["foot"]
        print(f"  {g['name']}: foot X {fx0:6.2f}..{fx1:6.2f}"
              f"  Y {fy0:7.2f}..{fy1:7.2f}"
              f"  wheel Y {g['wheel_y']:5.1f}"
              f"  servo {'flipped' if g['flipped'] else 'normal'}")
    xs = sorted({round(x, 3) for x, y, _ in all_holes() if _ == "WHEEL"})
    ys = sorted({round(y, 3) for x, y, _ in all_holes() if _ == "WHEEL"})
    print(f"  wheel hole X: {xs}")
    print(f"  wheel hole Y: {ys}")
    pts = [(round(x, 3), round(y, 3)) for x, y, _ in all_holes() if _ == "WHEEL"]
    print("  mirror about X=105:", all((round(W - x, 3), y) in pts for x, y in pts),
          "  about Y=130:", all((x, round(H - y, 3)) in pts for x, y in pts))
    print("battery box holes (chassis frame):",
          "  ".join(f"({x:.2f},{y:.2f})" for x, y in battery_holes()))
    bx0, by0, bx1, by1 = battery_outline()
    print(f"  box outline X {bx0:.1f}..{bx1:.1f}  Y {by0:.1f}..{by1:.1f}")
    print("Z module holes (chassis frame):")
    for label, pat in (("rail", RAIL_PAT), ("rack", RACK_PAT)):
        print(f"  {label}: " + "  ".join(
            f"({zmap(*p)[0]:.1f},{zmap(*p)[1]:.1f})" for p in pat))
    print("zip-tie eyes (chassis frame):")
    for cx, cy, along_y in EYE_POS:
        x0, y0, x1, y1 = eye_rect(cx, cy, along_y)
        print(f"  centre ({cx:.1f},{cy:.1f})  wall X {x0:.1f}..{x1:.1f}"
              f"  Y {y0:.1f}..{y1:.1f}  window {EYE_WIN_L:.0f}x{EYE_WIN_H:.0f}")


if __name__ == "__main__":
    write_dxf()
    draw()
    report()
