r"""Check the exported chassis STEP: hole count, positions, diameter.

    uvx ... python verify_chassis_step.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"D:\IceCup\src").resolve()))

from cadgen import build123d as bd  # noqa: E402
import chassis as C  # noqa: E402

STEP = Path(r"D:\IceCup\newSTEP\chassis.step")


def main():
    shape = bd.import_step(str(STEP))
    b = shape.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    cyls = []
    for f in shape.faces():
        try:
            if f.geom_type == bd.GeomType.CYLINDER:
                c = f.geom_adaptor().Cylinder()
                ax = c.Axis().Direction()
                if abs(ax.Z()) > 0.99:
                    loc = c.Location()
                    cyls.append((round(loc.X(), 3), round(loc.Y(), 3),
                                 round(c.Radius(), 3)))
        except Exception:
            pass
    print(f"vertical cylindrical faces: {len(cyls)}")
    expect = {(round(x, 3), round(y, 3)) for x, y, _ in C.all_holes()}
    got = {(x, y) for x, y, r in cyls if abs(r - C.HOLE_D / 2) < 0.01}
    print(f"holes at dia {C.HOLE_D}: got {len(got)}  expected {len(expect)}")
    missing = sorted(expect - got)
    extra = sorted(got - expect)
    print("missing:", missing if missing else "none")
    print("unexpected:", extra if extra else "none")
    radii = sorted({r for _, _, r in cyls})
    print("radii present:", radii)
    print("battery holes present:",
          sorted((x, y) for x, y in got if (x, y) in
                 {(round(a, 3), round(b2, 3)) for a, b2 in C.battery_holes()}))


if __name__ == "__main__":
    main()
