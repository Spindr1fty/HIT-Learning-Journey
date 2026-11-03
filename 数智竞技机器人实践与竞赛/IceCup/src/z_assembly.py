r"""Assembled view of the Z axis with the servo and the gripper head.

Everything is in the Z-axis module frame, the frame all parts were modelled in,
so no placement maths is needed beyond the servo and the gripper, which are
reference bodies drawn from their real dimensions.

    rail, rack, plate, carriage, pinion   real printable parts
    z_servo_mount                         real printable part (collar design)
    servo + shaft + horn                  reference only, 40 x 20 x 40
    g_fork head                           real printable part; its clamp collar
                                          is not modelled yet, so it is shown at
                                          a placeholder working height

The fork's height is a place holder: it hangs D below the carriage centre, and D
depends on the chassis height, which is still unknown. The collar on the servo
mount is what makes the equivalent adjustment possible in reality.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402
import z_servo_mount as SM  # noqa: E402
from g_fork import _head as fork_head  # noqa: E402
from z_carriage import _carriage  # noqa: E402
from z_pinion import _pinion  # noqa: E402
from z_plate import _plate  # noqa: E402
from z_rack import _rack  # noqa: E402
from z_rail import _rail  # noqa: E402

SERVO_BOX = (-86.0, -46.0, -55.0, -15.0, 150.0, 170.0)
FLANGE = (-93.25, -38.75, -25.0, -22.5, 152.0, 168.0)
SHAFT = (-56.0, 160.0)

# The fork bracket hangs off the servo mount's collar and its slots run
# Z 88..136. Put the head's bolts at Z 112 -- mid-travel, so both directions of
# trim stay available on the bench.
FORK_BOLT_Z = 123.0
FORK_HEAD_UP = 13.0             # the head's back-plate holes sit this far up
FORK_BRACKET_FACE_X = 39.3      # the bracket's +X face
FORK_BACK_X = -12.0             # the head's back plate, in its own frame
FORK_DX = FORK_BRACKET_FACE_X - FORK_BACK_X
FORK_DZ = FORK_BOLT_Z - FORK_HEAD_UP


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _servo_ref():
    parts = [
        _box(*SERVO_BOX),
        _box(*FLANGE),
        # shaft, then the disc horn that the gear bolts to
        bd.Pos(SHAFT[0], -15.0, SHAFT[1]) * bd.Rot(-90, 0, 0) * bd.Cylinder(
            2.95, 5.65, align=(bd.Align.CENTER, bd.Align.CENTER,
                               bd.Align.MIN)),
        bd.Pos(SHAFT[0], -10.5, SHAFT[1]) * bd.Rot(-90, 0, 0) * bd.Cylinder(
            10.0, 2.5, align=(bd.Align.CENTER, bd.Align.CENTER,
                              bd.Align.MIN)),
    ]
    body = parts[0]
    for p in parts[1:]:
        body = body + p
    body.label = "servo_reference"
    return body


def _assembly():
    parts = []
    for name, build in (
        ("rail", _rail),
        ("rack", _rack),
        ("plate", _plate),
        ("carriage", _carriage),
        ("pinion", _pinion),
        ("servo_mount", SM._cradle),
    ):
        s = build()
        s.label = name
        parts.append(s)

    parts.append(_servo_ref())

    fork = bd.Pos(FORK_DX, 0.0, FORK_DZ) * fork_head()
    fork.label = "fork_head"
    parts.append(fork)

    combo = bd.Compound(children=parts)
    combo.label = "z_axis_assembly"
    return combo


@step(out="../newSTEP/z_assembly.step")
def z_assembly():
    return _assembly()


if __name__ == "__main__":
    a = z_assembly()
    b = a.bounding_box()
    print(f"solids {len(a.solids())}   valid={a.is_valid}")
    print(f"overall bbox X {b.max.X - b.min.X:.1f}"
          f"  Y {b.max.Y - b.min.Y:.1f}  Z {b.max.Z - b.min.Z:.1f}")
    print(f"frame X {b.min.X:.1f}..{b.max.X:.1f}"
          f"  Y {b.min.Y:.1f}..{b.max.Y:.1f}"
          f"  Z {b.min.Z:.1f}..{b.max.Z:.1f}")
    print()
    print("key positions, module frame")
    print(f"  pinion axis ........ X {P.PINION_X}  Z {P.PINION_Z}")
    print(f"  rack pitch line .... X {P.RACK_PITCH_X}")
    print(f"  centre distance .... {abs(P.RACK_PITCH_X - P.PINION_X):.3f}"
          f"  (pinion pitch radius {P.PITCH_R:.3f})")
    print(f"  servo flange plane . Y {SM.SERVO_FLANGE_Y}")
    print(f"  servo face Y -15, horn top Y -8, gear Y -8..+8")
    print(f"  carriage ........... Z {P.CARRIAGE_Z0:.0f}.."
          f"{P.CARRIAGE_Z0 + P.CARRIAGE_LEN:.0f}")
    print(f"  fork head tines at Z {FORK_DZ:.0f}"
          f"  (bolts at Z {FORK_BOLT_Z:.0f}, slots span 88..136)")
    print(f"  fork head at X {FORK_DX:.1f}..{FORK_DX + 42.0:.1f}")
