"""Shared builder for flat parts: an outline extruded to thickness, minus holes,
rectangular windows and slotted (obround) cutouts.

Cutters are made to overshoot the slab in Z so the result is always a through
feature regardless of which way the outline's winding sends the extrusion.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402


def _shift_to_origin(outline):
    ox = min(x for x, _ in outline)
    oy = min(y for _, y in outline)
    return ox, oy


def _window_cutters(windows, ox, oy, thickness):
    depth = thickness + 2.0
    return [
        bd.Pos(x0 - ox, y0 - oy, -1.0)
        * bd.Box(x1 - x0, y1 - y0, depth,
                 align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
        for x0, y0, x1, y1 in windows
    ]


def _slot_cutters(slots, ox, oy, thickness):
    """Obround cutters: a bar between two end cylinders, all overshooting in Z."""
    cutters = []
    for x0, y0, x1, y1, width in slots:
        assert abs(y1 - y0) < 1e-6, "only horizontal slots appear in these drawings"
        r = width / 2
        span = x1 - x0
        assert span > 0, "slot end cylinders are reversed"
        depth = thickness + 2.0
        z = -1.0
        cutters.append(
            bd.Pos(x0 - ox, y0 - oy, z)
            * bd.Box(span, width, depth,
                     align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN))
        )
        for cx in (x0 - ox, x1 - ox):
            cutters.append(
                bd.Pos(cx, y0 - oy, z)
                * bd.Cylinder(r, depth,
                              align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            )
    return cutters


def build_flat(outline, holes, slots, thickness, label="flat_part", windows=()):
    ox, oy = _shift_to_origin(outline)

    pts = [(x - ox, y - oy, 0.0) for x, y in outline]
    solid = bd.extrude(bd.Face(bd.Polyline(*pts, close=True)), amount=thickness)
    solid = bd.Pos(0, 0, -solid.bounding_box().min.Z) * solid

    cutters = [
        bd.Pos(cx - ox, cy - oy, -1.0)
        * bd.Cylinder(r, thickness + 2.0,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        for cx, cy, r in holes
    ]
    cutters += _slot_cutters(slots, ox, oy, thickness + 2.0)
    cutters += _window_cutters(windows, ox, oy, thickness)

    solid = solid.cut(*cutters)
    solid.label = label
    return solid
