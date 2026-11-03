"""Involute spur gear demo: module 2, 48 teeth, 100 mm tip diameter.

Tip (outside) diameter is the 100 mm the request names, so pitch diameter is
96 mm and the root circle is 91 mm.
"""

import math

from cadgen import build123d as bd
from cadgen import step

MODULE = 2.0
TEETH = 48
PRESSURE_ANGLE = math.radians(20.0)
TIP_DIAMETER = 100.0
FACE_WIDTH = 12.0
BORE_DIAMETER = 20.0
KEY_WIDTH = 6.0
KEY_DEPTH = 3.5
FLANK_SAMPLES = 28
TIP_SAMPLES = 9


def _involute(angle: float) -> float:
    return math.tan(angle) - angle


def _radii() -> tuple[float, float, float, float]:
    r_pitch = MODULE * TEETH / 2
    r_tip = TIP_DIAMETER / 2
    r_root = r_pitch - 1.25 * MODULE
    r_base = r_pitch * math.cos(PRESSURE_ANGLE)
    return r_pitch, r_tip, r_root, r_base


def _half_angle(r: float, r_base: float) -> float:
    """Half tooth thickness in radians at radius r, tooth centred on +X."""
    alpha = math.acos(max(-1.0, min(1.0, r_base / r)))
    return math.pi / (2 * TEETH) + _involute(PRESSURE_ANGLE) - _involute(alpha)


def _tooth_face(r_tip: float, r_root: float, r_base: float) -> bd.Face:
    rs = [r_root + (r_tip - r_root) * i / (FLANK_SAMPLES - 1)
          for i in range(FLANK_SAMPLES)]
    r_stub = r_root - 1.0
    ht_a = _half_angle(r_tip, r_base)

    polar: list[tuple[float, float]] = [(r_stub, -_half_angle(r_root, r_base))]
    polar += [(r, -_half_angle(r, r_base)) for r in rs]
    polar += [(r_tip, -ht_a + 2 * ht_a * k / TIP_SAMPLES)
              for k in range(1, TIP_SAMPLES)]
    polar += [(r, _half_angle(r, r_base)) for r in reversed(rs)]
    polar.append((r_stub, _half_angle(r_root, r_base)))

    pts = [(r * math.cos(a), r * math.sin(a)) for r, a in polar]
    return bd.Face(bd.Polyline(*pts, close=True))


def _gear() -> bd.Shape:
    _, r_tip, r_root, r_base = _radii()

    tooth = bd.extrude(_tooth_face(r_tip, r_root, r_base), amount=FACE_WIDTH)
    teeth = [bd.Rot(0, 0, i * 360.0 / TEETH) * tooth for i in range(TEETH)]

    body = bd.Cylinder(
        r_root, FACE_WIDTH, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    gear = body.fuse(*teeth)

    bore = bd.Cylinder(
        BORE_DIAMETER / 2,
        FACE_WIDTH + 2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    keyway = bd.Box(
        BORE_DIAMETER / 2 + KEY_DEPTH,
        KEY_WIDTH,
        FACE_WIDTH + 2,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
    )
    gear = gear.cut(bore, keyway)
    gear.label = "spur_gear_m2_z48"
    return gear


@step(out="../oldSTEP/spur_gear.step")
def spur_gear():
    return _gear()


if __name__ == "__main__":
    spur_gear()
