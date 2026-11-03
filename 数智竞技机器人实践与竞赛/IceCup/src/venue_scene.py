"""Venue with painted markings and the red/blue zone tints, for review.

`venue.py` is the collision body; this adds the surface graphics on top. The
decals are 0.5 mm plates stacked in three layers (zone tint, lines, house rings)
so overlapping coplanar faces do not z-fight in a render. Drop this whole
compound when exporting to a simulator -- none of it carries physics.

Line widths are the two the user gave (centre 10 mm, dashes 4 mm). The +-275
track edges had no stated width, so they reuse 10 mm. Dash length/pitch are not
recorded anywhere in the DXF, so they are parameters below.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import venue as venue_mod  # noqa: E402
import venue_spec as V  # noqa: E402

DECAL_T = 0.5
SOLID_W = 10.0
DASH_W = 4.0
DASH_ON = 60.0
DASH_OFF = 30.0

TINT_Z = 0.0
LINE_Z = DECAL_T
RING_Z = 2 * DECAL_T

RED = bd.Color(0.78, 0.16, 0.16)
BLUE = bd.Color(0.13, 0.29, 0.65)
WHITE = bd.Color(0.94, 0.94, 0.94)
YELLOW = bd.Color(0.90, 0.76, 0.13)
GREEN = bd.Color(0.18, 0.55, 0.26)

# Outer ring first: what the rules page's scoring diagram reads as gold, then
# green, then a light band, then the red button.
HOUSE_COLORS = (YELLOW, GREEN, WHITE, RED)


def _plate(x0, x1, y0, y1, z, colour, label):
    p = bd.Box(x1 - x0, y1 - y0, DECAL_T, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    p = bd.Pos(x0, y0, z) * p
    p.color = colour
    p.label = label
    return p


def _zone_tints():
    near = V.near_x()
    return [
        _plate(near, V.THROW_LINE_X, 0.0, V.FIELD_HALF_WIDTH, TINT_Z, RED, "zone_red"),
        _plate(near, V.THROW_LINE_X, -V.FIELD_HALF_WIDTH, 0.0, TINT_Z, BLUE, "zone_blue"),
    ]


def _lines():
    h = SOLID_W / 2
    out = [
        _plate(V.near_x(), V.HOUSE_CENTRE_X, -h, h, LINE_Z, WHITE, "line_centre"),
        _plate(V.THROW_LINE_X, V.TRACK_FAR_X, V.TRACK_HALF_WIDTH - h,
               V.TRACK_HALF_WIDTH + h, LINE_Z, WHITE, "line_track_far"),
        _plate(V.THROW_LINE_X, V.TRACK_FAR_X, -V.TRACK_HALF_WIDTH - h,
               -V.TRACK_HALF_WIDTH + h, LINE_Z, WHITE, "line_track_near"),
    ]
    span = V.TRACK_FAR_X - V.THROW_LINE_X
    count = int(span // (DASH_ON + DASH_OFF)) + 1
    for i in range(count):
        x0 = V.THROW_LINE_X + i * (DASH_ON + DASH_OFF)
        x1 = min(x0 + DASH_ON, V.TRACK_FAR_X)
        d = DASH_W / 2
        for sign, tag in ((1, "far"), (-1, "near")):
            y = sign * V.AIM_HALF_WIDTH
            out.append(_plate(x0, x1, y - d, y + d, LINE_Z, WHITE, f"line_aim_{tag}_{i}"))
    return out


def _house():
    radii = sorted(V.HOUSE_RADII, reverse=True)   # outer first, to match HOUSE_COLORS
    rings = []
    for i, r_out in enumerate(radii):
        r_in = radii[i + 1] if i + 1 < len(radii) else 0.0
        ring = bd.Cylinder(r_out, DECAL_T, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        if r_in > 0:
            ring -= bd.Pos(0, 0, -1.0) * bd.Cylinder(
                r_in, DECAL_T + 2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        ring = bd.Pos(V.HOUSE_CENTRE_X, 0, RING_Z) * ring
        ring.color = HOUSE_COLORS[i]
        ring.label = f"house_r{r_out:.0f}"
        rings.append(ring)
    return rings


def _scene() -> bd.Shape:
    parts = [venue_mod.slab(), *_zone_tints(), *_lines(), *_house()]
    for i, y in enumerate(V.RACK_Y_CENTRES):
        platform = venue_mod.rack_platform(y)
        if platform is not None:
            parts.append(platform)
        parts.append(venue_mod.placed_rack(y, "a" if i == 0 else "b"))
    return bd.Compound(children=parts, label="venue_scene")


@step(out="../oldSTEP/venue_scene.step")
def venue_scene():
    return _scene()


if __name__ == "__main__":
    s = venue_scene()
    b = s.bounding_box()
    print(f"scene bbox {b.max.X - b.min.X:.1f} x {b.max.Y - b.min.Y:.1f}"
          f" x {b.max.Z - b.min.Z:.1f} mm")
    print(f"solids={len(s.solids())}  valid={s.is_valid}"
          f"  rings={[f'house_r{r:.0f}' for r in sorted(V.HOUSE_RADII, reverse=True)]}")
