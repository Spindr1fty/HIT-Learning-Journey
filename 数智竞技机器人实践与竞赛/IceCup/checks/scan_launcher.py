r"""Extract circular features (holes / bosses) from the launcher 3MF parts.

    python scan_launcher.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(r"D:\IceCup\src")))
import mesh_chamfer as MC  # noqa: E402

PATHS = [
    Path(r"C:\Users\Spindrift\Desktop\u_clamp.3mf"),
    Path(r"C:\Users\Spindrift\Desktop\打印\base_plate.3mf"),
    Path(r"C:\Users\Spindrift\Desktop\打印\plunger.3mf"),
    Path(r"C:\Users\Spindrift\Desktop\打印\rack.3mf"),
]


def scan(path):
    v, t = MC.load_3mf(path)
    m = MC.clean(v, t)
    lo, hi = m.bounds
    print(f"== {path.name}: size {np.round(hi - lo, 2)}  lo {np.round(lo, 2)}"
          f"  vol {m.volume / 1000:.1f} cm3  tris {len(m.faces)}")
    found = []
    for z in np.arange(lo[2] + 0.5, hi[2], 1.5):
        sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if sec is None:
            continue
        p2d, _ = sec.to_planar()
        for poly in p2d.polygons_full:
            for h in poly.interiors:
                xy = np.array(h.coords)
                d = 2.0 * np.sqrt(abs(h.area) / np.pi)
                if 1.5 < d < 12.0:
                    found.append((round(d, 1), float(xy[:, 0].mean()),
                                  float(xy[:, 1].mean()), float(z)))
    uniq = {}
    for d, x, y, z in found:
        key = (d, round(x / 1.5), round(y / 1.5))
        uniq.setdefault(key, []).append((x, y, z))
    print(f"   circular features merged: {len(uniq)}")
    for (d, _, _), pts in sorted(uniq.items(), key=lambda kv: (kv[0][2], kv[0][1])):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        zs = [p[2] for p in pts]
        print(f"     d~{d:4.1f}  at ({np.mean(xs):7.1f},{np.mean(ys):7.1f})"
              f"  z {min(zs):6.1f}..{max(zs):6.1f}")


if __name__ == "__main__":
    for p in PATHS:
        if p.exists():
            scan(p)
        else:
            print("missing:", p)
