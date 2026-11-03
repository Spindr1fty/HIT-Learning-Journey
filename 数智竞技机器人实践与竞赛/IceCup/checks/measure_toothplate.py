r"""Measure the tooth plate: outline, hole row, tooth geometry."""

import sys

import ezdxf


def main(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    lines = [e for e in msp if e.dxftype() == "LINE"]
    circles = [e for e in msp if e.dxftype() == "CIRCLE"]

    xs, ys = [], []
    for e in lines:
        xs += [e.dxf.start[0], e.dxf.end[0]]
        ys += [e.dxf.start[1], e.dxf.end[1]]
    print(f"outline extents  X {min(xs):.2f} .. {max(xs):.2f}"
          f"   ({max(xs)-min(xs):.2f})")
    print(f"                 Y {min(ys):.2f} .. {max(ys):.2f}"
          f"   ({max(ys)-min(ys):.2f})")
    print()

    hx = sorted(c.dxf.center[0] for c in circles)
    hy = [c.dxf.center[1] for c in circles]
    dias = sorted({round(2 * c.dxf.radius, 2) for c in circles})
    print(f"holes {len(circles)}   diameters {dias}")
    if len(hx) > 1:
        gaps = [hx[i + 1] - hx[i] for i in range(len(hx) - 1)]
        print(f"hole pitch  mean {sum(gaps)/len(gaps):.3f}   "
              f"min {min(gaps):.3f}   max {max(gaps):.3f}")
        print(f"hole span   {hx[0]:.2f} .. {hx[-1]:.2f}  ({hx[-1]-hx[0]:.2f})")
    print(f"hole row Y  {min(hy):.2f} .. {max(hy):.2f}")
    print()

    # horizontal lines = the plate's top and bottom edges
    tops = sorted({round(e.dxf.start[1], 2) for e in lines
                   if abs(e.dxf.start[1] - e.dxf.end[1]) < 1e-6})
    print("horizontal line Y values (plate edges + tooth roots):")
    for y in tops:
        print(f"   Y = {y:8.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
