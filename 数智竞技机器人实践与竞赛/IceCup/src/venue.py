"""Full venue assembly for simulation: playing slab, both stone racks, stones.

Built for collision geometry, not display: the slab is one box, each rack is
the rack solid plus five stone solids. The painted lines are zero thickness and
are deliberately not modelled -- they carry no physics.

Frame: origin at the throw line on the centre line, +X toward the house, +Z up,
playing surface at Z = 0. See venue_spec.py for where each number came from.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import venue_spec as V  # noqa: E402
from rack_loaded import loaded_rack  # noqa: E402

RACK_CENTRE_X = (V.RACK_FACE_X + V.RACK_BACK_X) / 2


def slab() -> bd.Shape:
    """Extrude the T-shaped plan: 550-wide track plus the 1000-wide end zone."""
    plate = bd.extrude(
        bd.Face(bd.Polyline(*[(x, y, 0.0) for x, y in V.plan()], close=True)),
        amount=V.SLAB_THICKNESS,
    )
    box = plate.bounding_box()
    if box.min.Z < -1e-9:
        plate = bd.Pos(0, 0, -box.min.Z) * plate
    plate = bd.Pos(0, 0, -V.SLAB_THICKNESS) * plate
    plate.label = "slab"
    return plate


def rack_platform(y_centre: float) -> bd.Shape | None:
    if V.PLATFORM_HEIGHT <= 0:
        return None
    p = bd.Box(
        (V.RACK_FACE_X - V.RACK_BACK_X) + 2 * V.PLATFORM_CLEARANCE,
        305.0 + 2 * V.PLATFORM_CLEARANCE,
        V.PLATFORM_HEIGHT,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
    )
    p = bd.Pos(V.RACK_BACK_X - V.PLATFORM_CLEARANCE, y_centre, 0.0) * p
    p.label = "platform"
    return p


def placed_rack(y_centre: float, tag: str) -> bd.Shape:
    rack = bd.Rot(0, 0, -90) * loaded_rack()
    rack = bd.Pos(RACK_CENTRE_X, y_centre, V.PLATFORM_HEIGHT) * rack
    rack.label = f"rack_{tag}"
    return rack


def _venue() -> bd.Shape:
    parts = [slab()]
    for i, y in enumerate(V.RACK_Y_CENTRES):
        platform = rack_platform(y)
        if platform is not None:
            parts.append(platform)
        parts.append(placed_rack(y, "a" if i == 0 else "b"))
    return bd.Compound(children=parts, label="venue")


@step(out="../oldSTEP/venue.step")
def venue():
    return _venue()


if __name__ == "__main__":
    v = venue()
    b = v.bounding_box()
    slab_solid = slab()
    want_area = (2 * V.TRACK_HALF_WIDTH * (V.far_x() - V.THROW_LINE_X)
                 + 2 * V.FIELD_HALF_WIDTH * (V.THROW_LINE_X - V.near_x()))
    got_area = slab_solid.volume / V.SLAB_THICKNESS
    print(f"venue bbox {b.max.X - b.min.X:.1f} x {b.max.Y - b.min.Y:.1f}"
          f" x {b.max.Z - b.min.Z:.1f} mm")
    print(f"solids={len(v.solids())}  valid={v.is_valid}"
          f"  platform height={V.PLATFORM_HEIGHT}")
    print(f"plan area  analytic {want_area / 1e6:.4f} m2"
          f"  cad {got_area / 1e6:.4f} m2  delta {abs(got_area - want_area):.3f} mm2")
    print(f"  (track {2 * V.TRACK_HALF_WIDTH:.0f} x "
          f"{V.far_x() - V.THROW_LINE_X:.0f}"
          f"  +  end zone {2 * V.FIELD_HALF_WIDTH:.0f} x "
          f"{V.THROW_LINE_X - V.near_x():.0f})")
