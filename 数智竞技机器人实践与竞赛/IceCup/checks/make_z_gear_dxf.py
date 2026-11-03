# -*- coding: utf-8 -*-
"""Build a dimensioned A3 DXF of the printed pinion and rack.

Inputs are the print-ready STEPs.  The pinion outline is rebuilt from the same
z_params constants as the 3D model; the rack outline is taken from an
orthographic projection so the two full-width end slots are represented
exactly as they exist in the STEP.

Run with cadgen + ezdxf:
  uvx --no-config --python 3.13 --from "cadgen==0.7.21" --with "ezdxf==1.4.4" \
      python checks/make_z_gear_dxf.py
"""

import math
import sys
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment

from cadgen import read_step

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import z_params as P  # noqa: E402

STEP_DIR = ROOT / "printSTEP"
OUT_PATH = Path.home() / "Desktop" / "z_gear_2d.dxf"
PREVIEW_PATH = ROOT / "renders" / "_z_gear_dxf_preview.png"

# Sheet (A3 landscape) and view placement, model space millimetres.
SHEET_W, SHEET_H = 420.0, 297.0
RACK_X0 = 25.0
RACK_Y_TIP = 210.0
RACK_LEN = P.RACK_LEN
RACK_HEIGHT = 26.0          # flange back (-98) to tooth tip (-72)
GEAR_CX, GEAR_CY = 75.0, 100.0
SIDE_CX, SIDE_CY = 165.0, 100.0

# Pinion profile, copied point-for-point from z_pinion._gear_profile().
FLANK_PTS = 16
TIP_ARC_PTS = 5
ROOT_ARC_PTS = 4


def gear_outline():
    z = P.PINION_TEETH
    pitch_ang = 2 * math.pi / z
    phase = math.pi / z
    pts = []
    radii = [P.ROOT_R + (P.TIP_R - P.ROOT_R) * k / FLANK_PTS
             for k in range(FLANK_PTS + 1)]
    ha_tip = P.involute_half_angle(P.TIP_R)
    ha_root = P.involute_half_angle(P.ROOT_R)

    for i in range(z):
        centre = i * pitch_ang + phase
        for r in radii:
            ha = P.involute_half_angle(max(r, P.BASE_R))
            pts.append((r * math.cos(centre - ha), r * math.sin(centre - ha)))
        for k in range(1, TIP_ARC_PTS):
            a = centre - ha_tip + 2 * ha_tip * k / TIP_ARC_PTS
            pts.append((P.TIP_R * math.cos(a), P.TIP_R * math.sin(a)))
        for r in reversed(radii):
            ha = P.involute_half_angle(max(r, P.BASE_R))
            pts.append((r * math.cos(centre + ha), r * math.sin(centre + ha)))
        a0 = centre + ha_root
        a1 = centre + pitch_ang - ha_root
        for k in range(1, ROOT_ARC_PTS):
            a = a0 + (a1 - a0) * k / ROOT_ARC_PTS
            pts.append((P.ROOT_R * math.cos(a), P.ROOT_R * math.sin(a)))
    pts.append(pts[0])
    return pts


def sample_edge(edge, n_curve=64):
    if edge.geom_type.name == "LINE":
        return [edge.position_at(0), edge.position_at(1)]
    n = n_curve
    return [edge.position_at(i / (n - 1)) for i in range(n)]


def add_rack_projection(msp):
    shape = read_step(STEP_DIR / "z_rack.step")
    visible, _ = shape.project_to_viewport(
        viewport_origin=(0, 0, 100), viewport_up=(0, 1, 0))

    raw_edges = []
    xs, ys = [], []
    for e in visible:
        pts = sample_edge(e)
        rp = [(p.Y, -p.X) for p in pts]       # length horizontal, teeth down
        raw_edges.append((e.geom_type.name, rp))
        xs.extend(p[0] for p in rp)
        ys.extend(p[1] for p in rp)

    mnx, mxx, mny, mxy = min(xs), max(xs), min(ys), max(ys)
    sx = RACK_LEN / (mxx - mnx)
    sy = RACK_HEIGHT / (mxy - mny)

    def place(p):
        return (RACK_X0 + (p[0] - mnx) * sx,
                RACK_Y_TIP + (p[1] - mny) * sy)

    for kind, pts in raw_edges:
        pts = [place(p) for p in pts]
        if kind == "LINE":
            msp.add_line(pts[0], pts[-1],
                         dxfattribs={"layer": "PROFILE"})
        else:
            msp.add_lwpolyline(
                pts, close=math.dist(pts[0], pts[-1]) < 1e-4,
                dxfattribs={"layer": "PROFILE"})


def add_pinion(msp):
    pts = [(GEAR_CX + x, GEAR_CY + y) for x, y in gear_outline()]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "PROFILE"})

    for x, y in ((5.7, 0.0), (0.0, 5.7), (-5.7, 0.0), (0.0, -5.7)):
        msp.add_circle((GEAR_CX + x, GEAR_CY + y), 1.75,
                       dxfattribs={"layer": "PROFILE"})

    msp.add_circle((GEAR_CX, GEAR_CY), 10.1,
                   dxfattribs={"layer": "PROFILE"})
    msp.add_circle((GEAR_CX, GEAR_CY), P.PITCH_R,
                   dxfattribs={"layer": "CENTER"})
    msp.add_circle((GEAR_CX, GEAR_CY), 5.7,
                   dxfattribs={"layer": "CENTER"})

    msp.add_line((GEAR_CX - 23, GEAR_CY), (GEAR_CX + 23, GEAR_CY),
                 dxfattribs={"layer": "CENTER"})
    msp.add_line((GEAR_CX, GEAR_CY - 23), (GEAR_CX, GEAR_CY + 23),
                 dxfattribs={"layer": "CENTER"})
    for x, y in ((5.7, 0.0), (0.0, 5.7), (-5.7, 0.0), (0.0, -5.7)):
        cx, cy = GEAR_CX + x, GEAR_CY + y
        msp.add_line((cx - 3.0, cy), (cx + 3.0, cy),
                     dxfattribs={"layer": "CENTER"})
        msp.add_line((cx, cy - 3.0), (cx, cy + 3.0),
                     dxfattribs={"layer": "CENTER"})


def add_side_view(msp):
    x0, x1 = SIDE_CX - 8.0, SIDE_CX + 8.0
    y0, y1 = SIDE_CY - 20.0, SIDE_CY + 20.0
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       close=True, dxfattribs={"layer": "PROFILE"})
    msp.add_line((SIDE_CX - 23, SIDE_CY), (SIDE_CX + 23, SIDE_CY),
                 dxfattribs={"layer": "CENTER"})

    # left face is the servo-horn face; recess 1.2 deep, holes stop at its floor
    xr = x0 + 1.2
    msp.add_line((xr, SIDE_CY - 10.1), (xr, SIDE_CY + 10.1),
                 dxfattribs={"layer": "HIDDEN"})
    msp.add_line((x0, SIDE_CY - 10.1), (xr, SIDE_CY - 10.1),
                 dxfattribs={"layer": "HIDDEN"})
    msp.add_line((x0, SIDE_CY + 10.1), (xr, SIDE_CY + 10.1),
                 dxfattribs={"layer": "HIDDEN"})
    for dy in (5.7, 0.0, -5.7):
        msp.add_line((xr, SIDE_CY + dy), (x1, SIDE_CY + dy),
                     dxfattribs={"layer": "HIDDEN"})


def add_linear_dim(msp, p1, p2, base, text, angle):
    d = msp.add_linear_dim(
        base=base, p1=p1, p2=p2, angle=angle, text=text,
        dimstyle="EZDXF", override=DIM_STYLE,
        dxfattribs={"layer": "DIM"})
    d.render()


def add_text(msp, text, pos, height=2.5, layer="NOTE",
             align=TextEntityAlignment.LEFT):
    t = msp.add_text(text, height=height,
                     dxfattribs={"style": "CN", "layer": layer})
    t.set_placement(pos, align=align)
    return t


def add_leader(msp, tip, text_pos, lines, height=2.2):
    msp.add_line(tip, text_pos, dxfattribs={"layer": "DIM"})
    x, y = text_pos
    for i, line in enumerate(lines):
        add_text(msp, line, (x, y - i * (height + 0.8)), height=height)


def add_dimensions(msp):
    x1 = RACK_X0 + RACK_LEN
    y_tip = RACK_Y_TIP
    y_back = y_tip + 24.5
    y_foot = y_tip + RACK_HEIGHT

    add_linear_dim(msp, (RACK_X0, y_tip), (x1, y_tip),
                   (RACK_X0 + RACK_LEN / 2, 196.0), "251.33", 0)
    add_linear_dim(msp, (RACK_X0, y_tip), (RACK_X0, y_back),
                   (16.0, (y_tip + y_back) / 2), "24.50", 90)
    add_linear_dim(msp, (x1, y_tip), (x1, y_foot),
                   (x1 + 22.0, (y_tip + y_foot) / 2), "26.00", 90)
    add_linear_dim(msp, (x1 - 8.0, y_foot), (x1, y_foot),
                   (x1 - 4.0, 242.0), "8.00", 0)

    add_linear_dim(msp, (GEAR_CX, GEAR_CY - 20.0),
                   (GEAR_CX, GEAR_CY + 20.0),
                   (GEAR_CX + 30.0, GEAR_CY), "φ40.00", 90)

    add_linear_dim(msp, (SIDE_CX - 8.0, SIDE_CY + 20.0),
                   (SIDE_CX + 8.0, SIDE_CY + 20.0),
                   (SIDE_CX, SIDE_CY + 28.0), "16.00", 0)
    add_linear_dim(msp, (SIDE_CX - 6.8, SIDE_CY - 8.0),
                   (SIDE_CX + 8.0, SIDE_CY - 8.0),
                   (SIDE_CX + 0.6, SIDE_CY - 24.0), "14.80", 0)

    msp.add_line((RACK_X0, y_tip + 2.0), (x1, y_tip + 2.0),
                 dxfattribs={"layer": "CENTER"})
    add_text(msp, "节线", (RACK_X0 + RACK_LEN * 0.55, y_tip - 4.0),
             height=2.2, layer="DIM")

    add_leader(msp, (x1 - 4.0, y_tip + 16.0), (300.0, 252.0),
               ["2× 开口槽，沿齿深调整量 6", "槽宽 16 贯穿；法兰厚 8"])
    add_leader(msp, (GEAR_CX, GEAR_CY + 5.7), (96.0, 135.0),
               ["4×φ3.5，均布于 φ11.4"])
    add_leader(msp, (GEAR_CX - 7.2, GEAR_CY + 7.2), (18.0, 132.0),
               ["φ20.2 × 1.2 深"])
    add_text(msp, "18齿  m2  α20°", (96.0, 142.0), height=2.4)
    add_text(msp, "侧视（左端为舵盘面）", (SIDE_CX - 18.0, SIDE_CY - 28.0),
             height=2.2)


def add_frame_and_notes(msp):
    msp.add_lwpolyline([(8, 8), (412, 8), (412, 289), (8, 289)],
                       close=True, dxfattribs={"layer": "FRAME"})

    add_text(msp, "Z 轴齿轮 / 齿条 二维图", (18, 276), height=5.0, layer="TITLE")
    add_text(msp, "ICECUP  Z-AXIS PINION & RACK", (18, 269), height=2.6)

    add_text(msp, "技术要求 / NOTES", (218, 188), height=3.4)
    notes = [
        "1. 齿轮：m=2，z=18，α=20°，齿顶φ40，齿根φ31，节圆φ36，齿宽16。",
        "2. 齿条：m=2，z=40，α=20°，节距6.2832，节线长251.327，宽16。",
        "3. 啮合中心距（齿轮轴—齿条节线）=18.000。",
        "4. 齿轮安装：4×φ3.5，BCD φ11.4；φ20.2×1.2沉槽；无中心孔；",
        "   孔从非沉槽面进入，有效深14.8。",
        "5. 齿条法兰厚8；2×开口槽，沿齿深调整量6，槽宽16贯穿。",
        "6. 齿廓为每侧16段折线渐开线；总侧隙0.30；未注公差±0.2。",
        "7. 材料PLA；按A3、1:1打印；单位mm。",
    ]
    y = 181.0
    for line in notes:
        add_text(msp, line, (218, y), height=2.15)
        y -= 6.4

    # title block
    x0, x1, y0, y1 = 270.0, 408.0, 12.0, 48.0
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       close=True, dxfattribs={"layer": "FRAME"})
    for yy in (36.0, 28.0, 20.0):
        msp.add_line((x0, yy), (x1, yy), dxfattribs={"layer": "FRAME"})
    msp.add_line((348.0, y0), (348.0, 36.0), dxfattribs={"layer": "FRAME"})
    add_text(msp, "ICECUP  Z轴传动 / PINION + RACK", (274, 41), height=2.8)
    add_text(msp, "零件：z_pinion 18T + z_rack 40T", (274, 32), height=2.5)
    add_text(msp, "图号 IC-Z-001", (274, 24), height=2.4)
    add_text(msp, "比例 1:1    单位 mm", (274, 16), height=2.4)
    add_text(msp, "材料 PLA", (352, 24), height=2.4)
    add_text(msp, "2026-10-17", (352, 16), height=2.4)


def main():
    doc = ezdxf.new("R2013", setup=True)
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 2
    doc.header["$LTSCALE"] = 0.6
    doc.header["$EXTMIN"] = (0.0, 0.0, 0.0)
    doc.header["$EXTMAX"] = (SHEET_W, SHEET_H, 0.0)
    doc.header["$LIMMIN"] = (0.0, 0.0)
    doc.header["$LIMMAX"] = (SHEET_W, SHEET_H)

    doc.styles.add("CN", font="simhei.ttf")
    doc.layers.add("PROFILE", color=7, lineweight=35)
    doc.layers.add("CENTER", color=1, linetype="CENTER", lineweight=13)
    doc.layers.add("HIDDEN", color=8, linetype="DASHED", lineweight=13)
    doc.layers.add("DIM", color=3, lineweight=13)
    doc.layers.add("NOTE", color=2, lineweight=13)
    doc.layers.add("FRAME", color=8, lineweight=18)
    doc.layers.add("TITLE", color=7, lineweight=18)

    global DIM_STYLE
    DIM_STYLE = {
        "dimtxt": 2.5, "dimasz": 1.6, "dimexe": 1.5, "dimexo": 1.0,
        "dimgap": 0.8, "dimdec": 2, "dimtad": 1, "dimtxsty": "CN",
        "dimclrd": 3, "dimclre": 3, "dimclrt": 3,
    }

    msp = doc.modelspace()
    add_rack_projection(msp)
    add_pinion(msp)
    add_side_view(msp)
    add_dimensions(msp)
    add_frame_and_notes(msp)

    auditor = doc.audit()
    if auditor.has_errors:
        for error in auditor.errors:
            print("AUDIT", error)
    doc.saveas(OUT_PATH)
    print("wrote", OUT_PATH)
    print("entities", len(list(msp)))

    # A dark preview makes the white/coloured layers readable.
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import Frontend, RenderContext
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

        fig = plt.figure(figsize=(16.8, 11.88), dpi=300)
        ax = fig.add_axes((0, 0, 1, 1))
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        ctx = RenderContext(doc)
        Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp, finalize=True)
        ax.set_axis_off()
        PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(PREVIEW_PATH, facecolor="black")
        plt.close(fig)
        print("preview", PREVIEW_PATH)
    except Exception as exc:
        print("preview skipped:", exc)


if __name__ == "__main__":
    main()
