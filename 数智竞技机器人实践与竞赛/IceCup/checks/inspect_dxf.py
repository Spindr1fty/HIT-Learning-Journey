r"""Inspect and draw a DXF part, since the file carries almost no dimensions.

Prints entity counts, overall extents, and the largest closed loops, then renders
a plan view PNG so the shape can be read at a glance.
"""

import sys
from collections import Counter
from pathlib import Path

import ezdxf


def main(path, out):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    types = Counter(e.dxftype() for e in msp)
    print(f"file: {Path(path).name}")
    print("entity types:", dict(types))

    # extents of everything
    xs, ys = [], []
    for e in msp:
        try:
            pts = list(e.vertices()) if e.dxftype() == "LWPOLYLINE" else []
        except Exception:
            pts = []
        if pts:
            for p in pts:
                xs.append(p[0])
                ys.append(p[1])
        else:
            for attr in ("dxf.start", "dxf.end", "dxf.center"):
                p = getattr(e.dxf, attr, None)
                if p is not None:
                    xs.append(p[0])
                    ys.append(p[1])
    if xs:
        print(f"extents X {min(xs):.2f} .. {max(xs):.2f}   ({max(xs)-min(xs):.2f})")
        print(f"extents Y {min(ys):.2f} .. {max(ys):.2f}   ({max(ys)-min(ys):.2f})")

    # closed polylines = candidates for the outline
    loops = []
    for e in msp:
        if e.dxftype() == "LWPOLYLINE" and e.closed:
            pts = [(p[0], p[1]) for p in e.vertices()]
            if len(pts) >= 3:
                w = max(p[0] for p in pts) - min(p[0] for p in pts)
                h = max(p[1] for p in pts) - min(p[1] for p in pts)
                loops.append((len(pts), w, h, pts))
    loops.sort(key=lambda t: -(t[1] * t[2]))
    print(f"\nclosed polylines: {len(loops)}")
    for n, w, h, _ in loops[:6]:
        print(f"  {n:4d} pts   {w:8.2f} x {h:8.2f}")

    circles = [e for e in msp if e.dxftype() == "CIRCLE"]
    if circles:
        print(f"\ncircles: {len(circles)}")
        for c in circles[:10]:
            print(f"  dia {2*c.dxf.radius:7.2f} at "
                  f"({c.dxf.center[0]:8.2f}, {c.dxf.center[1]:8.2f})")

    # render
    from ezdxf.addons.drawing import matplotlib as dm
    dm.qsave(msp, out, bg="#FFFFFF", fg="#212529")
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
