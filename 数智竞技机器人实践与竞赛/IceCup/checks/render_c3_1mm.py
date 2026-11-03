r"""Export render-only compounds for the 1 mm C3 fit-test piece.

  _C3_1mm_render.step        the sample alone
  _C3_1mm_servo_render.step  sample + servo body/flange/shaft + horn, plus
                             the four M4 socket heads and the hex key path,
                             so the fit can be judged from a snapshot

Run:  cd src && uvx ... python ../checks/render_c3_1mm.py
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b_C3_1mm as T   # noqa: E402
import g_mount_b as B          # noqa: E402
import g_servo as S            # noqa: E402

OUT = SRC.parent / "newSTEP"
HOLES = ((25.94, 19.0), (25.94, 29.0), (74.44, 19.0), (74.44, 29.0))


def cyl_x(x0, x1, cy, cz, dia):
    return bd.Pos((x0 + x1) / 2.0, cy, cz) * bd.Rot(0, 90, 0) * bd.Cylinder(
        dia / 2.0, x1 - x0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))


def main():
    part = T.build()
    bd.export_step(part, str(OUT / "_C3_1mm_render.step"))
    print("wrote", OUT / "_C3_1mm_render.step")

    servo = bd.Pos(B.SERVO_X, B.SERVO_Y, B.SERVO_Z) * B._servo_rot() * \
        S.servo_solid()
    horn = bd.Pos(B.SERVO_X, B.SERVO_Y, B.SERVO_Z) * B._servo_rot() * \
        S.horn_solid()
    heads = None
    for cy, cz in HOLES:
        h = cyl_x(7.5, 11.5, cy, cz, 7.0)
        heads = h if heads is None else heads + h
    key = cyl_x(11.5, 62.0, HOLES[1][0], HOLES[1][1], 3.0)

    comp = bd.Compound(children=[part, servo.clean(), horn, heads.clean(),
                                 key])
    bd.export_step(comp, str(OUT / "_C3_1mm_servo_render.step"))
    print("wrote", OUT / "_C3_1mm_servo_render.step")


if __name__ == "__main__":
    main()
