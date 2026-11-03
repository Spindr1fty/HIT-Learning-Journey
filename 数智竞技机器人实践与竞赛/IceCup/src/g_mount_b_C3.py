r"""C3: the user's four fixes on the rev30 Desktop base.

1) rear plate is now FULL WIDTH (same as the foot) with a 60 x 20.4 window:
   the 52 x 20 servo flange passes with 4 mm each side, and the four D7
   socket heads can ride through with the flange if the bolts are pre-fitted.
2) both side panels go down to the foot (Z = 14), not Z = 19.
3) the foot/box is 10 mm longer at the rear: X 0..50; rear plate 47.5..50.
4) foot is wider: Y 9.94..90.44; 8 screw holes moved to
   X 19 / 27 / 35 / 43, Y 15.0 / 85.38 (clear of ribs and side panels).

Side wire windows are 9 x 7 at X 26.5..35.5 (centred on the panel), Z 27..34,
mirrored left/right.  Top cover is one piece, solid, X 4.5..50.

The rev30 front arch / posts / ribs / top beam are kept.  The old foot is
removed and replaced by the new foot; the posts/ribs sit on fusion bosses.

Pure ASCII on purpose.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import chamfer_part as C  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "newSTEP"
BASE = OUT / "g_mount_b_desktop_base.step"

# --- footprint --------------------------------------------------------------
X0, X1 = 0.0, 50.0
Y0, Y1 = 9.94, 90.44
FOOT_Z0, FOOT_Z1 = 9.0, 14.0
OV = 0.5

# front arch / posts / ribs from rev30
POST_Y = ((21.94, 29.94), (70.44, 78.44))
RIB_Y = ((16.94, 21.94), (78.44, 83.44))
POST_X = (0.0, 5.0)
RIB_X = (5.0, 14.0)

# rear plate
REAR_X0, REAR_X1 = 47.5, 50.0
REAR_Z0, REAR_Z1 = 13.5, 38.0
WIN_Y0, WIN_Y1 = 20.19, 80.19      # 60 wide, centred on the flange (Y 50.19)
WIN_Z0, WIN_Z1 = 14.0, 34.4        # 20.4 high, bottom flush with the foot top

# side panels -- moved 0.5 outward (user 2026-10-27: the walls were crowding
# the flange screws).  Inner faces now 1.0 off the flange edges, was 0.5.
SIDE_X0, SIDE_X1 = 12.0, 50.0
SIDE_Y = ((20.19, 23.19), (77.19, 80.19))
SIDE_Z0, SIDE_Z1 = 13.5, 35.5

# top cover -- outer edges stay flush with the side panels' outer faces
TOP_X0, TOP_X1 = 4.5, 50.0
TOP_Y0, TOP_Y1 = 20.19, 80.19
TOP_Z0, TOP_Z1 = 35.0, 38.0

# wire windows, mirrored -- 9 long, centred on the side panel in X
# (SIDE_X0..SIDE_X1 mid = 31), height unchanged (user 2026-10-27)
WIRE_X0, WIRE_X1 = 26.5, 35.5
WIRE_Z0, WIRE_Z1 = 27.0, 34.0
WIRE_Y = ((20.0, 24.5), (75.88, 80.38))

# new foot holes
HOLE_X = (19.0, 27.0, 35.0, 43.0)
HOLE_Y = (15.0, 85.38)
HOLE_D = 4.5


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _cyl_z(cx, cy, z0, z1, dia):
    return bd.Pos(cx, cy, z0) * bd.Cylinder(
        dia / 2.0, z1 - z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _chamfer(p):
    """1 mm on the new outer edges; the rev30 front arch/ribs keep theirs."""
    yo0, yo1 = TOP_Y0, TOP_Y1          # the walls'/roof's outer faces
    edges = []
    for e in p.edges():
        m = e.position_at(0.5)
        hit = False
        if abs(m.Z - 38.0) < 0.02:
            if (abs(m.Y - yo0) < 0.03 or abs(m.Y - yo1) < 0.03
                    or abs(m.X - 50.0) < 0.03):
                hit = True
        if abs(m.Y - yo0) < 0.03 or abs(m.Y - yo1) < 0.03:
            if (abs(m.X - SIDE_X0) < 0.03 or abs(m.X - 50.0) < 0.03
                    or abs(m.Z - 14.0) < 0.03):
                hit = True
        if abs(m.X - 50.0) < 0.03 and (abs(m.Y - 9.94) < 0.04
                                       or abs(m.Y - 90.44) < 0.04):
            hit = True
        if hit:
            edges.append(e)
    specs = [(e.position_at(0.5),
              bd.Vector(e.tangent_at(0.5)).normalized(), e) for e in edges]
    fails, done = [], []
    out = C._chamfer_set(p, specs, 1.0, fails, done)
    print(f"chamfer: {len(edges)} edges, {len(done)} set(s), {len(fails)} refused")
    return out


def build(chamfer=True):
    p = bd.import_step(str(BASE))

    # 1) remove the old foot (keep posts/ribs starting at Z=14)
    p = p.cut(_box(-1.0, 51.0, -1.0, 91.0, 8.9, 14.0)).clean()

    # 2) new foot + fusion bosses under posts and ribs
    p = p.fuse(_box(X0, X1, Y0, Y1, FOOT_Z0, FOOT_Z1))
    bosses = []
    for y0, y1 in POST_Y:
        bosses.append(_box(POST_X[0], POST_X[1], y0, y1,
                           FOOT_Z1 - OV, FOOT_Z1 + OV))
    for y0, y1 in RIB_Y:
        bosses.append(_box(RIB_X[0], RIB_X[1], y0, y1,
                           FOOT_Z1 - OV, FOOT_Z1 + OV))
    p = p.fuse(*bosses).clean()

    # 3) rear plate and window.  The cut starts AT the plate's inner face:
    #    the 60-wide window is wider than the 53 interior, so extending the
    #    cut forward would shave the side panels' rear ends off for nothing.
    p = p.fuse(_box(REAR_X0, REAR_X1, Y0, Y1, REAR_Z0, REAR_Z1))
    p = p.cut(_box(REAR_X0, REAR_X1 + 1.0, WIN_Y0, WIN_Y1,
                   WIN_Z0, WIN_Z1))

    # 4) side panels + wire windows
    for y0, y1 in SIDE_Y:
        p = p.fuse(_box(SIDE_X0, SIDE_X1, y0, y1, SIDE_Z0, SIDE_Z1))
    for y0, y1 in WIRE_Y:
        p = p.cut(_box(WIRE_X0, WIRE_X1, y0, y1, WIRE_Z0, WIRE_Z1))

    # 5) top cover
    p = p.fuse(_box(TOP_X0, TOP_X1, TOP_Y0, TOP_Y1, TOP_Z0, TOP_Z1))

    # 6) new 8 foot holes
    for hx in HOLE_X:
        for hy in HOLE_Y:
            p = p.cut(_cyl_z(hx, hy, FOOT_Z0 - 1.0, FOOT_Z1 + 1.0, HOLE_D))

    p = p.clean()
    if chamfer:
        p = _chamfer(p)
    p.label = "C3"
    return p


if __name__ == "__main__":
    p = build()
    b = p.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"valid={p.is_valid}  solids={len(p.solids())}"
          f"  vol {p.volume / 1000:.3f} cm3 ({p.volume / 1000 * 1.24:.1f} g)")
    bd.export_step(p, str(OUT / "g_mount_b_C3.step"))
    print("wrote", OUT / "g_mount_b_C3.step")
    bd.export_stl(p, str(OUT / "g_mount_b_C3.stl"), tolerance=0.01, angular_tolerance=0.3)
    print("wrote", OUT / "g_mount_b_C3.stl")
