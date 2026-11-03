"""Curling stone, revolved from the committee's dimensioned drawing.

Dimensioned by the sheet: total 32, belt Ø47, lower band 8.3, belt 5.5,
stem Ø11, and one 5 mm callout whose datum is ambiguous (neck height or cap
thickness).  The shoulder and cap are interpolated to match the silhouette.
"""

import math

from cadgen import build123d as bd
from cadgen import step

TOTAL_HEIGHT = 32.0
BELT_DIAMETER = 47.0
BASE_RADIUS = 17.5
BELT_Z0 = 8.3
BELT_Z1 = 13.8
STEM_RADIUS = 11.0 / 2
STEM_TOP_Z = 27.0
CAP_RADIUS = 14.5
SHOULDER_TOP_Z = STEM_TOP_Z - 5.0
SAMPLES = 24


def _catmull(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return tuple(
        0.5 * (2 * p1[i] + (-p0[i] + p2[i]) * t
               + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2
               + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3)
        for i in range(2)
    )


def _spline(ctrl, samples=SAMPLES):
    """Catmull-Rom through ctrl, with clamped end tangents."""
    pts = [ctrl[0]] + ctrl + [ctrl[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        for k in range(samples):
            out.append(_catmull(pts[i - 1], pts[i], pts[i + 1], pts[i + 2], k / samples))
    out.append(ctrl[-1])
    return out


def _profile_points():
    r = BELT_DIAMETER / 2
    pts = [(0.0, 0.0), (BASE_RADIUS, 0.0)]

    # Lower bulge: sweeps out early then runs nearly vertical into the belt.
    pts += _spline([
        (BASE_RADIUS, 0.0),
        (BASE_RADIUS + 2.6, 1.3),
        (r - 0.9, 3.6),
        (r - 0.5, 6.4),
        (r - 0.5, BELT_Z0),
    ])

    # The belt itself: the Ø47 running band, flat-sided with crisp edges.
    pts += [(r, BELT_Z0), (r, BELT_Z1), (r - 0.5, BELT_Z1)]

    # Shoulder: stays wide, then drops in fast so the stem reads as exposed.
    pts += _spline([
        (r - 0.5, BELT_Z1),
        (r - 0.8, BELT_Z1 + 2.7),
        (r - 2.6, BELT_Z1 + 4.7),
        (14.0, SHOULDER_TOP_Z - 1.3),
        (7.5, SHOULDER_TOP_Z - 0.3),
        (STEM_RADIUS, SHOULDER_TOP_Z),
    ])

    # Stem, then the handle cap.
    pts += [
        (STEM_RADIUS, STEM_TOP_Z),
        (CAP_RADIUS, STEM_TOP_Z),
        (CAP_RADIUS, TOTAL_HEIGHT),
        (0.0, TOTAL_HEIGHT),
    ]
    return pts


def _stone() -> bd.Shape:
    raw = [(rad, 0.0, z) for rad, z in _profile_points()]
    pts = [p for i, p in enumerate(raw)
           if i == 0 or (p[0] - raw[i - 1][0]) ** 2 + (p[2] - raw[i - 1][2]) ** 2 > 1e-9]
    profile = bd.Face(bd.Polyline(*pts, close=True))
    stone = bd.revolve(profile, axis=bd.Axis.Z, revolution_arc=360.0)
    stone.label = "curling_stone"
    return stone


@step(out="../oldSTEP/curling_stone.step")
def curling_stone():
    return _stone()


if __name__ == "__main__":
    curling_stone()
