"""Reference geometry for the XIN YOU 20 kg standard servo, for checking mounts.

The servo's own frame: base face on Z=0, output shaft up +Z, body 40 (X) x 20 (Y)
x 40 (Z). The mounting flange is a 48.5 x 10 plate at Z=30, and the output shaft
sits 10 mm along +X from the hole-pattern centre -- that offset has caused more
rework than anything else on this robot.

Kept ASCII-only: cadgen reads model sources without an encoding declaration.
"""

from cadgen import build123d as bd

BODY_X = 40.0
BODY_Y = 20.0
BODY_Z = 40.0

FLANGE_Z0 = 30.0
FLANGE_Z1 = 32.66          # user-measured flange plate thickness 2.66
FLANGE_SPAN = 52.0         # long direction, user-measured (inner 44 / outer 52)
FLANGE_W = 20.0            # width = body width (user-measured)
HOLE_D = 4.4
HOLE_DX = 24.0             # hole centres: (44+52)/2 = 48 apart
HOLE_DY = 6.325            # hole centres: (6+19.3)/2 = 12.65 apart

SHAFT_D = 5.9
SHAFT_Z0 = 40.0
SHAFT_Z1 = 45.65
SHAFT_X_OFF = 10.0          # +X from the hole-pattern centre

HORN_D = 20.0
HORN_T = 2.5
HORN_TOP = 47.0
BCD = 14.0


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def servo_solid():
    """Fused stand-in for the servo: base at Z=0, shaft up +Z."""
    body = _box(0.0, BODY_X, -BODY_Y / 2.0, BODY_Y / 2.0, 0.0, BODY_Z)
    # one flange plate spanning both tabs; it fuses with the body
    flange = _box((BODY_X - FLANGE_SPAN) / 2.0, (BODY_X + FLANGE_SPAN) / 2.0,
                  -FLANGE_W / 2.0, FLANGE_W / 2.0, FLANGE_Z0, FLANGE_Z1)
    shaft = bd.Pos(BODY_X / 2.0 + SHAFT_X_OFF, 0.0, SHAFT_Z0) * bd.Cylinder(
        SHAFT_D / 2.0, SHAFT_Z1 - SHAFT_Z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return (body + flange + shaft).clean()


def horn_solid():
    return bd.Pos(BODY_X / 2.0 + SHAFT_X_OFF, 0.0, SHAFT_Z0) * bd.Cylinder(
        HORN_D / 2.0, HORN_T,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def hole_centres():
    """The four flange-slot centres, in the servo's own frame, on Z=FLANGE_Z0."""
    cx = BODY_X / 2.0
    return [(cx + sx * HOLE_DX, sy * HOLE_DY, FLANGE_Z0)
            for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)]
