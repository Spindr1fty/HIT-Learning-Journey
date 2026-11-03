r"""Extract the tooth profile vertices from the tooth-plate DXF.

Prints the lines whose Y is in the tooth band so the exact tooth form can be
reconstructed; the mating pinion has to be generated from this, not guessed.
"""

import sys

import ezdxf


def main(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    segs = []
    for e in msp:
        if e.dxftype() != "LINE":
            continue
        x0, y0 = e.dxf.start[0], e.dxf.start[1]
        x1, y1 = e.dxf.end[0], e.dxf.end[1]
        if max(y0, y1) < 216.0:            # tooth band only
            segs.append(((x0, y0), (x1, y1)))

    print(f"tooth-band segments: {len(segs)}")
    xs = [p[0] for s in segs for p in s]
    print(f"X range {min(xs):.2f} .. {max(xs):.2f}")

    # sort by X and print the first few teeth in detail
    segs.sort(key=lambda s: (min(s[0][0], s[1][0]), min(s[0][1], s[1][1])))
    print("\nfirst 12 segments (x0,y0) -> (x1,y1):")
    for (x0, y0), (x1, y1) in segs[:12]:
        print(f"  ({x0:8.3f},{y0:8.3f}) -> ({x1:8.3f},{y1:8.3f})"
              f"   dx {x1-x0:7.3f}  dy {y1-y0:7.3f}")

    # unique vertex chain
    pts = []
    for (x0, y0), (x1, y1) in segs:
        pts.append((round(x0, 3), round(y0, 3)))
        pts.append((round(x1, 3), round(y1, 3)))
    uniq = sorted(set(pts))
    print(f"\nunique vertices: {len(uniq)}")
    print("X spread of vertices:", f"{uniq[0][0]:.2f} .. {uniq[-1][0]:.2f}")
    ytop = {p[1] for p in uniq}
    print("distinct Y values:", sorted(round(y, 3) for y in ytop))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
