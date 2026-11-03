r"""Chassis, design B15 (user's 2026-10-24 revision).  Sole product source.

TH / CHAMFER select the variant:
    1 mm  test plate  -> Desktop/chassis_1mm.step  (main())
    0.6 mm fit-check  -> Desktop/chassis_fitcheck_0.6.step
    8 mm  production  -> newSTEP/chassis.step      (TH=8, CHAMFER=1)

One continuous 210 x 290 outline: front corner ears (15 mm deep) and a
full-width rear strip (15 mm deep) are part of the boundary, so the old base
R5 front/rear corners are filled and the left/right edges are straight.  The
four outer corners are R5; the front centre keeps the notch and the
launcher/Z-fork space.

Four 22 x 7 wire slots (R3.5) sit at the corners, outside the launcher base
footprint (Y 4..256); the top-right one is moved 4 mm right to (190, 267.5).
The three zip-tie eyes are REMOVED.  Instead there are eight 14 x 2 tie slots
(R1 ends), four pairs with a 6 mm pitch:
    left pair   (8,140) / (14,140)       vertical (14 along Y)
    centre pair (99,140) / (105,140)     vertical
    rear left   (67,-3) / (67,-9)        horizontal (14 along X)
    rear right  (143,-3) / (143,-9)      horizontal
The 44 mounting holes are unchanged.  The right ear root gets an R3 round
only where the user marked green.

Battery boss (1 mm full only): integrated OPEN TRAY, exact battery-box
footprint X 56.9..93.1 / Y 19.9..110.2, 28 tall (Z 0..28).  Perimeter walls
2.5 mm thick + four solid nut posts at the battery holes; the top is open and
the battery box's own 5.5 mm base is the cover.  Four M4 hex-nut pockets
(A/F 7.2, 3.6 deep); the Ø4.5 holes continue down through the posts; short
screws go down from inside the battery box into the embedded nuts.  The 0.6
fit-check has no boss.

Run (from src/):
    uvx --from "cadgen==0.7.21" python chassis_test_b15.py
writes
    C:\Users\Spindrift\Desktop\chassis_1mm.step
    C:\Users\Spindrift\Desktop\chassis_1mm.stl
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import chassis as C  # noqa: E402

TH = 1.0
CHAMFER = 0.5
# four 22 x 7 wire pass-through slots (the top-right one moved right 4 mm)
SLOT_W, SLOT_H, SLOT_R = 22.0, 7.0, 3.5
WIRE_SLOTS = [(24.0, 267.5), (190.0, 267.5),
              (24.0, -7.5), (186.0, -7.5)]
# eight 14 x 2 tie slots, four pairs, pair pitch 6 mm
TIE_L, TIE_W, TIE_R = 14.0, 2.0, 1.0
TIE_SLOTS = [
    (8.0, 140.0, "Y"), (14.0, 140.0, "Y"),       # left pair
    (99.0, 140.0, "Y"), (105.0, 140.0, "Y"),     # centre pair
    (67.0, -3.0, "X"), (67.0, -9.0, "X"),        # rear-left pair
    (143.0, -3.0, "X"), (143.0, -9.0, "X"),      # rear-right pair
]
# battery-box boss: integrated OPEN TRAY (walls + 4 nut posts, no top plate)
BOSS_X0, BOSS_X1 = 56.9, 93.1
BOSS_Y0, BOSS_Y1 = 19.9, 110.2
BOSS_H = 28.0
BOSS_WALL = 2.5
BOSS_POST_X = ((62.0, 72.0), (78.0, 88.0))
BOSS_POST_Y = ((19.9, 31.0), (99.1, 110.2))
NUT_AF = 7.2                 # M4 hex nut across flats, pocket clearance
NUT_DEPTH = 3.6              # pocket depth (nut is 3.2 thick)
# reinforcement ribs (6 mm production only)
RIB_H, RIB_W = 3.0, 8.0      # underside X-brace
ZG_T, ZG_H = 5.0, 25.0       # Z rail foot gussets
LG_T, LG_H = 4.0, 25.0       # launcher-base side gussets
TG_T, TG_H = 3.0, 15.0       # battery-tray outer gussets
DESK = Path.home() / "Desktop"
STEP_OUT = DESK / "chassis_1mm.step"
STL_OUT = DESK / "chassis_1mm.stl"
ALIGN_MIN = (bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0, align=ALIGN_MIN)


def arc(cx, cy, r, a0, a1, seg=24):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / seg)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / seg)))
            for i in range(seg + 1)]


def outline():
    """One closed ring: 210 x 290, front corner ears + full rear strip.

    The ears/rear strip are part of the same boundary, so the base's old R5
    front/rear corners are filled and the left/right edges stay straight.
    The four outer corners are R5; the front ear roots and the front inner
    corners have 2 x 45 chamfers (no sharp 90 there); the right ear root has
    an R3 round where the user marked green; the front centre keeps the notch.
    """
    pts = [(0.0, -10.0), (0.0, 270.0)]
    pts += arc(5, 270, 5, 180, 90)[1:]          # front-left R5
    pts += [(38.0, 275.0), (40.0, 273.0), (40.0, 262.0),
            (42.0, 260.0), (102.64, 260.0)]
    pts += arc(102.64, 258, 2, 90, 21.8)[1:]    # notch, left mouth
    pts += [(111.85, 240.36)]
    pts += arc(110, 239.61, 2, 21.8, 0)[1:]
    pts += [(112.0, 205.07)]
    pts += arc(114, 205.07, 2, 180, 270)[1:]
    pts += [(160.0, 203.07)]
    pts += arc(160, 205.07, 2, 270, 360)[1:]
    pts += [(162.0, 239.61)]
    pts += arc(164, 239.61, 2, 180, 158.2)[1:]
    pts += [(169.49, 258.74)]
    pts += arc(171.35, 258, 2, 158.2, 90)[1:]   # notch, right mouth
    # green-stroke area: R3 round at the right ear root (only this spot)
    pts += [(176.35, 260.0)]
    pts += arc(176.35, 263.0, 3.0, 270, 180)[1:]
    pts += [(173.35, 273.0), (175.35, 275.0), (205.0, 275.0)]
    pts += arc(205, 270, 5, 90, 0)[1:]          # front-right R5
    pts += [(210.0, -10.0)]
    pts += arc(205, -10, 5, 0, -90)[1:]         # rear-right R5
    pts += [(5.0, -15.0)]
    pts += arc(5, -10, 5, 270, 180)[1:]         # rear-left R5
    return pts


def plate():
    pts = outline()
    if (pts[0][0] - pts[-1][0]) ** 2 + (pts[0][1] - pts[-1][1]) ** 2 < 1e-12:
        pts = pts[:-1]
    wire = bd.Wire(bd.Polyline(*pts, close=True).edges())
    solid = bd.extrude(bd.Face(wire), amount=TH)
    b = solid.bounding_box()
    if b.min.Z < -1e-9:
        solid = bd.Pos(0, 0, -b.min.Z) * solid
    return bd.Pos(0, 0, -TH) * solid


def eyes():
    out = []
    for cx, cy, along_y in C.EYE_POS:
        x0, y0, x1, y1 = C.eye_rect(cx, cy, along_y)
        wall = _box(x0, x1, y0, y1, -0.2, C.EYE_H)
        if along_y:
            win = _box(cx - C.EYE_T, cx + C.EYE_T,
                       cy - C.EYE_WIN_L / 2.0, cy + C.EYE_WIN_L / 2.0,
                       C.EYE_WIN_Z0, C.EYE_WIN_Z0 + C.EYE_WIN_H)
        else:
            win = _box(cx - C.EYE_WIN_L / 2.0, cx + C.EYE_WIN_L / 2.0,
                       cy - C.EYE_T, cy + C.EYE_T,
                       C.EYE_WIN_Z0, C.EYE_WIN_Z0 + C.EYE_WIN_H)
        out.append(wall - win)
    return out


def build(with_eyes=True, chamfer=True, with_boss=False, with_ribs=False):
    solid = plate()
    cut = [bd.Pos(x, y, -TH - 0.2) * bd.Cylinder(
        C.HOLE_D / 2.0, TH + 0.4,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for x, y, _ in C.all_holes()]
    for cx, cy in WIRE_SLOTS:
        slot2d = bd.Rectangle(SLOT_W - SLOT_H, SLOT_H)
        slot2d = slot2d + bd.Pos(-(SLOT_W - SLOT_H) / 2.0, 0) * bd.Circle(
            SLOT_R)
        slot2d = slot2d + bd.Pos((SLOT_W - SLOT_H) / 2.0, 0) * bd.Circle(
            SLOT_R)
        cut.append(bd.Pos(cx, cy, -TH - 0.5) *
                   bd.extrude(slot2d, amount=TH + 1.0))
    for cx, cy, axis in TIE_SLOTS:
        if axis == "Y":
            slot2d = bd.Rectangle(TIE_W, TIE_L - 2.0 * TIE_R)
            slot2d = slot2d + bd.Pos(0, TIE_L / 2.0 - TIE_R) * bd.Circle(
                TIE_R)
            slot2d = slot2d + bd.Pos(0, -(TIE_L / 2.0 - TIE_R)) * bd.Circle(
                TIE_R)
        else:
            slot2d = bd.Rectangle(TIE_L - 2.0 * TIE_R, TIE_W)
            slot2d = slot2d + bd.Pos(TIE_L / 2.0 - TIE_R, 0) * bd.Circle(
                TIE_R)
            slot2d = slot2d + bd.Pos(-(TIE_L / 2.0 - TIE_R), 0) * bd.Circle(
                TIE_R)
        cut.append(bd.Pos(cx, cy, -TH - 0.5) *
                   bd.extrude(slot2d, amount=TH + 1.0))
    solid = solid.cut(*cut).clean()
    if with_eyes:
        solid = solid.fuse(*eyes()).clean()
    if with_boss:
        w = BOSS_WALL
        tray = [
            _box(BOSS_X0, BOSS_X0 + w, BOSS_Y0, BOSS_Y1, -0.2, BOSS_H),
            _box(BOSS_X1 - w, BOSS_X1, BOSS_Y0, BOSS_Y1, -0.2, BOSS_H),
            _box(BOSS_X0 + w, BOSS_X1 - w, BOSS_Y0, BOSS_Y0 + w,
                 -0.2, BOSS_H),
            _box(BOSS_X0 + w, BOSS_X1 - w, BOSS_Y1 - w, BOSS_Y1,
                 -0.2, BOSS_H),
        ]
        for px0, px1 in BOSS_POST_X:
            for py0, py1 in BOSS_POST_Y:
                tray.append(_box(px0, px1, py0, py1, -0.2, BOSS_H))
        solid = solid.fuse(*tray).clean()
        boss_cut = []
        for x, y in C.battery_holes():
            boss_cut.append(bd.Pos(x, y, -TH - 0.2) * bd.Cylinder(
                C.HOLE_D / 2.0, TH + BOSS_H + 0.4,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
            hex2d = bd.RegularPolygon(NUT_AF / math.sqrt(3.0), 6)
            boss_cut.append(
                bd.Pos(x, y, BOSS_H - NUT_DEPTH) *
                bd.extrude(hex2d, NUT_DEPTH + 0.2))
        solid = solid.cut(*boss_cut).clean()
    if with_ribs:
        ribs = []
        # 1) underside X-brace between the four wheel inner corners
        dx, dy = 170.0 - 40.0, 167.75 - 92.25
        diag = math.hypot(dx, dy)
        ang = math.degrees(math.atan2(dy, dx))
        for a in (ang, -ang):
            ribs.append(
                bd.Pos(105.0, 130.0, -TH - RIB_H) * bd.Rot(0, 0, a) *
                bd.Box(diag, RIB_W, RIB_H,
                       align=(bd.Align.CENTER, bd.Align.CENTER,
                              bd.Align.MIN)))
        # 2) Z rail-foot side gussets (left / right of the 30x30 rail)
        for x0, x1 in ((53.0, 43.0), (83.0, 93.0)):
            face = bd.Face(bd.Wire(bd.Polyline(
                (x0, 232.5, 0.0), (x0, 232.5, ZG_H), (x1, 232.5, 0.0),
                close=True).edges()))
            ribs.append(bd.extrude(face, amount=ZG_T))
        # 3) launcher-base side gussets (left / front / rear)
        for pts, amount in (
                (((111, 240, 0), (111, 240, LG_H), (107, 240, 0)), 220.0),
                (((120, 256, 0), (120, 256, LG_H), (120, 260, 0)), 80.0),
                (((120, 4, 0), (120, 4, LG_H), (120, 0, 0)), 80.0)):
            face = bd.Face(bd.Wire(bd.Polyline(*pts, close=True).edges()))
            ribs.append(bd.extrude(face, amount=amount))
        # 4) battery-tray outer gussets (4 corners, 10 long x 15 high x 3)
        for cx, sx in ((56.9, -1.0), (93.1, 1.0)):
            for cy, sy in ((19.9, 1.0), (110.2, -1.0)):
                pts = ((cx, cy, 0.0), (cx, cy, TG_H), (cx + sx * TG_T, cy, 0.0))
                face = bd.Face(bd.Wire(bd.Polyline(*pts, close=True).edges()))
                ribs.append(bd.Pos(0, 0, 0) * bd.extrude(face, amount=10.0 * sy))
        solid = solid.fuse(*ribs).clean()
    if chamfer:
        # 0.5 x 45 deg chamfer on the top rim of the four wire slots
        slot_edges = []
        for cx, cy in WIRE_SLOTS:
            x0 = cx - SLOT_W / 2.0 - 0.6
            x1 = cx + SLOT_W / 2.0 + 0.6
            y0 = cy - SLOT_H / 2.0 - 0.6
            y1 = cy + SLOT_H / 2.0 + 0.6
            for e in solid.edges():
                c = e.center()
                if abs(c.Z) < 1e-6 and x0 < c.X < x1 and y0 < c.Y < y1:
                    slot_edges.append(e)
        print(f"  slot top edges for chamfer: {len(slot_edges)}")
        solid = solid.chamfer(CHAMFER, None, slot_edges)
    return solid


def main():
    solid = build(with_eyes=False, chamfer=True, with_boss=True)
    b = solid.bounding_box()
    print(f"solid X {b.min.X:.2f}..{b.max.X:.2f}"
          f"  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.3f}..{b.max.Z:.3f}"
          f"  valid={solid.is_valid}  solids={len(solid.solids())}")
    print(f"volume {solid.volume:.1f} mm3"
          f"  ({solid.volume / 1000:.1f} cm3,"
          f" PLA solid {solid.volume / 1000 * 1.24:.0f} g)")
    print("export_step:", bd.export_step(solid, str(STEP_OUT)), STEP_OUT)
    print("export_stl:", bd.export_stl(solid, str(STL_OUT), tolerance=0.005,
                                      angular_tolerance=0.2), STL_OUT)


if __name__ == "__main__":
    main()
