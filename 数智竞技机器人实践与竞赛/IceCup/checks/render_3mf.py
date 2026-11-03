r"""Quick iso thumbnails of the four uploaded 3MF parts (matplotlib, no GPU).

    python render_3mf.py            -> renders/upload_4parts.png
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

NS = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"
PARTS = ["u_clamp(1).3mf", "base_plate.3mf", "plunger.3mf", "rack.3mf"]
OUT = Path(r"D:\IceCup\renders\upload_4parts.png")


def load(path):
    z = zipfile.ZipFile(path)
    model = [n for n in z.namelist() if n.endswith(".model")][0]
    root = ET.fromstring(z.read(model))
    verts, tris = [], []
    for mesh in root.iter(NS + "mesh"):
        base = len(verts)
        for v in mesh.iter(NS + "vertex"):
            verts.append((float(v.get("x")), float(v.get("y")), float(v.get("z"))))
        for t in mesh.iter(NS + "triangle"):
            tris.append((int(t.get("v1")) + base, int(t.get("v2")) + base,
                         int(t.get("v3")) + base))
    return np.array(verts, float), np.array(tris, int)


def shade(tris, color=(0.72, 0.78, 0.86)):
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    lights = [np.array([0.55, -0.5, 0.67]), np.array([-0.6, 0.3, 0.45])]
    lam = np.full(len(n), 0.30)
    for l in lights:
        l = l / np.linalg.norm(l)
        lam += 0.45 * np.clip(n @ l, 0, 1)
    lam = np.clip(lam, 0.18, 1.0)
    return np.clip(np.array(color)[None, :] * lam[:, None], 0, 1)


def main():
    fig = plt.figure(figsize=(15, 13.5), dpi=110, facecolor="white")
    for i, name in enumerate(PARTS):
        v, f = load(Path.home() / "Desktop" / name)
        c = v.mean(axis=0)
        v = v - c
        ax = fig.add_subplot(2, 2, i + 1, projection="3d")
        tri = v[f]
        pc = Poly3DCollection(tri, facecolors=shade(tri), edgecolors="none")
        ax.add_collection3d(pc)
        ext = v.max(axis=0) - v.min(axis=0)
        r = float(max(ext)) / 2
        mid = (v.max(axis=0) + v.min(axis=0)) / 2
        ax.set_xlim(mid[0] - r, mid[0] + r)
        ax.set_ylim(mid[1] - r, mid[1] + r)
        ax.set_zlim(mid[2] - r, mid[2] + r)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=24, azim=-58)
        ax.set_axis_off()
        ax.set_title(f"{name.replace('.3mf', '')}\n"
                     f"{ext[0]:.1f} × {ext[1]:.1f} × {ext[2]:.1f} mm, {len(f)} 面",
                     fontsize=11.5)
    fig.suptitle("上传的四个 3MF（原始，未倒角）", fontsize=15, y=0.955)
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    main()
