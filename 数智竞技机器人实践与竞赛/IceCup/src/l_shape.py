"""L bracket: two identical square legs at 90 deg, hole grid on each.

The source (Lshape.dxf) is one 24.40 x 24.40 face with a 3x3 grid at 8.25 mm
pitch, leaving only 3.95 mm from the outer hole rows to either edge. Two 5 mm
legs at 90 deg cannot share that face: a hole 3.95 mm from the bend breaks
through the mating leg, which is 5 mm thick before the fastener head is even
counted.

Clearing a 5 mm leg plus an M4 head needs roughly 5 + 2 + 2 = 9 mm of margin,
so the leg grows to 2*8.25 + 2*9 = 34.5 mm while the 8.25 pitch is kept.

2026-10-17, per the user after handling the first printed article:
- holes enlarged 4.0 -> 4.5 so that plain M4 bolts pass (printed holes come
  out undersize);
- the hole row hugging the bend on EACH leg is removed (6 holes gone): a bolt
  and washer there run into the other leg, they could never be used;
- a 45 deg full-width gusset braces the inner corner: the article snapped
  when flexed because the two 5 mm legs met in a sharp re-entrant corner with
  a layer bond right at the root.
The gusset legs are 7 mm, not more: a taller gusset eats the washer seat of
the next hole row (centres 17.25, an M4 washer reaches 12.75 from the leg
face), so 7 is the largest size that keeps every remaining hole serviceable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import parts_data as P  # noqa: E402

HOLE_DIAMETER = 4.5
PITCH = 8.25
MARGIN = 9.0
LEG = 2 * PITCH + 2 * MARGIN
GUSSET = 7.0
T = P.THICKNESS


def _leg(label, corner_row):
    """One square leg with its 3x3 grid minus the row next to the bend.

    corner_row is the local grid index (0..2) of the row that ends up facing
    the other leg in the finished bracket. The flat leg keeps its low-y rows;
    the up leg is rotated, so for it the bend-adjacent row is index 2.
    """
    pts = [(0.0, 0.0, 0.0), (LEG, 0.0, 0.0), (LEG, LEG, 0.0), (0.0, LEG, 0.0)]
    solid = bd.extrude(bd.Face(bd.Polyline(*pts, close=True)), amount=T)
    solid = bd.Pos(0, 0, -solid.bounding_box().min.Z) * solid

    r = HOLE_DIAMETER / 2
    cutters = [
        bd.Pos(MARGIN + PITCH * i, MARGIN + PITCH * j, -1.0)
        * bd.Cylinder(r, T + 2.0,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for i in range(3) for j in range(3) if j != corner_row
    ]
    solid = solid.cut(*cutters)
    solid.label = label
    return solid


def _bracket():
    flat = _leg("leg_flat", corner_row=0)
    up = bd.Rot(-90, 0, 0) * _leg("leg_up", corner_row=2)
    up = bd.Pos(0, 0, LEG) * up

    # 45 deg brace across the inner corner, full width. Triangular face drawn
    # in the uv plane, turned so the extrusion runs along +X: Rot(0, 90, 0)
    # maps (u, v, w) to (w, v, -u), i.e. v is world Y and -u is world Z.
    tri = [(-T, T), (-T, T + GUSSET), (-(T + GUSSET), T)]
    face = bd.Face(bd.Polyline(*[(u, v, 0.0) for u, v in tri], close=True))
    gusset = bd.Rot(0, 90, 0) * bd.extrude(face, amount=LEG)
    gusset = bd.Pos(-gusset.bounding_box().min.X, 0, 0) * gusset
    gusset.label = "gusset"

    bracket = flat.fuse(up, gusset)
    bracket.label = "l_bracket"
    return bracket


@step(out="../oldSTEP/l_shape.step")
def l_shape():
    return _bracket()


if __name__ == "__main__":
    b = l_shape()
    box = b.bounding_box()
    print(f"leg {LEG}  grid span {2*PITCH}  margin {MARGIN}"
          f"  hole d {HOLE_DIAMETER}  gusset {GUSSET} (45 deg, full width)")
    print(f"bbox {box.max.X:.2f} x {box.max.Y:.2f} x {box.max.Z:.2f}"
          f"  valid={b.is_valid}  solids={len(b.solids())}"
          f"  cyl_faces={sum(1 for f in b.faces() if f.geom_type == bd.GeomType.CYLINDER)}")
    print(f"volume {b.volume/1000:.4f} cm3")
