r"""Dump every dimension and text found in a DXF reference drawing.

Used to build a full data sheet for the 20 kg servo from the maker's 3-view
(dxf/Motor.dxf), so nothing has to be re-measured by hand.
"""

import sys
from pathlib import Path

import ezdxf


def main(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    dims = []
    texts = []
    for e in msp:
        t = e.dxftype()
        if t == "DIMENSION":
            try:
                d = e.get_measurement()
            except Exception:
                d = None
            if isinstance(d, (list, tuple)):
                d = tuple(round(v, 3) for v in d)
            elif isinstance(d, float):
                d = round(d, 3)
            dims.append((e.dxf.dimtype & 0x0F, d, e.dxf.get("text", "")))
        elif t in ("TEXT", "MTEXT"):
            s = e.dxf.text if t == "TEXT" else e.plain_text()
            s = s.strip()
            if s:
                texts.append(s)

    print(f"file    : {Path(path).name}")
    print(f"entities: {len(list(msp))}")
    print(f"dimensions: {len(dims)}")
    print()
    print("--- DIMENSIONS (type, value) ---")
    for dimtype, val, txt in dims:
        print(f"  type {dimtype}  value {val}  text {txt!r}")
    print()
    print("--- TEXTS ---")
    for s in texts:
        print(f"  {s!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
