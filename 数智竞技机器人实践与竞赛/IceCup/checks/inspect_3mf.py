r"""Inspect the four 3MF meshes: bbox, volume, sharp-edge statistics.
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

DESK = Path.home() / "Desktop"


def load_3mf(path):
    z = zipfile.ZipFile(path)
    model = [n for n in z.namelist() if n.endswith(".model")][0]
    root = ET.fromstring(z.read(model))
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    verts, tris = [], []
    base = 0
    for mesh in root.iter("{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}mesh"):
        for v in mesh.iter("{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}vertex"):
            verts.append((float(v.get("x")), float(v.get("y")), float(v.get("z"))))
        for t in mesh.iter("{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangle"):
            tris.append((int(t.get("v1")) + base, int(t.get("v2")) + base,
                         int(t.get("v3")) + base))
        base = len(verts)
    return np.array(verts, float), np.array(tris, int)


def weld(v, t, tol=1e-3):
    key = np.round(v / tol).astype(np.int64)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    vv = v[first]
    return vv, inv[t]


def stats(name):
    v, t = load_3mf(DESK / name)
    v, t = weld(v, t)
    # volume (signed, from triangle soup)
    a = v[t[:, 0]]
    b = v[t[:, 1]]
    c = v[t[:, 2]]
    vol = np.abs(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
    lo, hi = v.min(0), v.max(0)
    # edge -> adjacent faces
    e = np.vstack([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]])
    e.sort(axis=1)
    f = np.tile(np.arange(len(t)), 3)
    order = np.lexsort((e[:, 1], e[:, 0]))
    e = e[order]
    f = f[order]
    same = np.all(e[1:] == e[:-1], axis=1)
    pairs = np.where(same)[0]
    dihed = []
    for i in pairs:
        e0, e1 = e[i], e[i + 1]
        f0, f1 = f[i], f[i + 1]
        n0 = np.cross(v[t[f0, 1]] - v[t[f0, 0]], v[t[f0, 2]] - v[t[f0, 0]])
        n1 = np.cross(v[t[f1, 1]] - v[t[f1, 0]], v[t[f1, 2]] - v[t[f1, 0]])
        n0 /= np.linalg.norm(n0) + 1e-12
        n1 /= np.linalg.norm(n1) + 1e-12
        dihed.append(np.degrees(np.arccos(np.clip(np.dot(n0, n1), -1, 1))))
    dihed = np.array(dihed)
    elen = np.linalg.norm(v[e[pairs, 0]] - v[e[pairs, 1]], axis=1)
    sharp = dihed > 20.0
    print(f"{name}: verts {len(v)} tris {len(t)}  bbox "
          f"{hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f}"
          f"  min {lo.round(2)}  vol {vol/1000:.2f} cm3")
    print(f"   edges with 2 faces: {len(pairs)}, sharp(>20deg): {sharp.sum()}"
          f"  (length>1mm: {(sharp & (elen > 1.0)).sum()})")
    if sharp.sum():
        print(f"   sharp edge length: {np.sort(elen[sharp])[:8].round(2)} ..."
              f" {np.sort(elen[sharp])[-6:].round(2)}")
        h = np.histogram(dihed[sharp], bins=[20, 40, 60, 80, 100, 120, 140, 180])
        print("   dihedral hist:", dict(zip(h[1][:-1].round(0), h[0])))


if __name__ == "__main__":
    for n in ("u_clamp(1).3mf", "base_plate.3mf", "plunger.3mf", "rack.3mf"):
        stats(n)
