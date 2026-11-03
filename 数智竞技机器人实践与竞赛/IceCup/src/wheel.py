"""Drive wheel from Whells.dxf: Ø53.6 x 25.56 wide, Ø5.9 bore.

The drawing also carries a 168.304 x 25.56 rectangle, which is the wheel's
circumference unrolled (pi x 53.6 = 168.30) -- a calculation, not a part, so it
is not built. Bore matches the servo output shaft diameter from Motor.dxf.
Axis runs along Y and the rim rests on z = 0.
"""

from cadgen import build123d as bd
from cadgen import step

RIM_DIAMETER = 53.6
WIDTH = 25.56
BORE_DIAMETER = 5.9


def _wheel():
    disc = bd.Cylinder(RIM_DIAMETER / 2, WIDTH,
                       align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    bore = bd.Cylinder(BORE_DIAMETER / 2, WIDTH + 2.0,
                       align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    wheel = disc.cut(bore.moved(bd.Location((0, 0, -1.0))))
    wheel = bd.Rot(-90, 0, 0) * wheel
    box = wheel.bounding_box()
    wheel = bd.Pos(0, -box.min.Y, -box.min.Z) * wheel
    wheel.label = "wheel"
    return wheel


@step(out="../oldSTEP/wheel.step")
def wheel():
    return _wheel()


if __name__ == "__main__":
    w = wheel()
    b = w.bounding_box()
    solid = (bd.pi * ((RIM_DIAMETER / 2) ** 2 - (BORE_DIAMETER / 2) ** 2) * WIDTH)
    print(f"bbox {b.max.X - b.min.X:.3f} x {b.max.Y - b.min.Y:.3f}"
          f" x {b.max.Z - b.min.Z:.3f}  valid={w.is_valid}")
    print(f"analytic {solid/1000:.4f} cm3  cad {w.volume/1000:.4f} cm3"
          f"  delta {abs(w.volume - solid):.4f} mm3")
