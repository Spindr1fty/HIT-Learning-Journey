r"""Top view of the cable-clip coupon, drawn from its STL.

    python draw_cable_clips.py  ->  renders/cable_clips_top.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.collections import PolyCollection
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent
STL = ROOT / "newSTEP" / "cable_clips_coupon.stl"
OUT = ROOT / "renders" / "cable_clips_top.png"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def face_colour(z):
    if z > 11.5:
        return "#e39a4f"
    if z > 5.5:
        return "#f4c98f"
    if z > 2.5:
        return "#d9e8f6"
    if z > 1.0:
        return "#bcd6ee"
    if z > -0.5:
        return "#eef4fb"
    return "#f6f8fa"


def main():
    mesh = trimesh.load(str(STL))
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)
    tri = mesh.triangles
    normals = mesh.face_normals
    zmax = tri[:, :, 2].max(axis=1)
    up = normals[:, 2] > 0.5

    fig = plt.figure(figsize=(12.5, 10.2), dpi=160, facecolor="white")
    ax = fig.add_axes([0.05, 0.10, 0.90, 0.78])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-10, 180)
    ax.set_ylim(-14, 138)

    # all triangles: silhouette
    ax.add_collection(PolyCollection(
        tri[:, :, :2], facecolors="#f4f7fa", edgecolors="none"))
    # upward faces, low to high so the highest surface wins
    order = np.argsort(zmax[up])
    tris = tri[up][order]
    cols = [face_colour(z) for z in zmax[up][order]]
    ax.add_collection(PolyCollection(tris[:, :, :2], facecolors=cols,
                                     edgecolors="face", linewidths=0.15))

    # ---- labels
    labels = [
        (45, 109, "① J 形钩", "你画的方案：U 形墙 + 内折钩"),
        (120, 109, "② 卡扣 C", "从上方压入，唇口 6.5"),
        (45, 60, "③ 扎带眼", "墙内 8×5 窗，穿扎带"),
        (125, 50, "④ 梳齿", "分线用，3 个 4 mm 槽"),
    ]
    for x, y, name, sub in labels:
        ax.text(x, y, name, fontsize=13, fontweight="bold", ha="center",
                color="#12395e")
        ax.text(x, y - 4.2, sub, fontsize=8.8, ha="center", color="#495057")

    # ---- cable illustrations
    def cable(x, y, r=4.0):
        ax.add_patch(Circle((x, y), r, facecolor="#d9d9d9",
                            edgecolor="#7a7a7a", lw=1.2, zorder=20))
        ax.add_patch(Circle((x - 1.2, y + 1.2), r * 0.45, facecolor="white",
                            edgecolor="none", alpha=0.55, zorder=21))

    # 1 J-hook: pocket is on the left of the lip
    cable(42.0, 91.0, 4.0)
    # 2 snap C: pocket centre
    cable(120.0, 90.0, 4.0)
    # 3 zip eye: cable above the wall, tie through the window
    cable(45.0, 43.0, 3.2)
    ax.add_patch(FancyBboxPatch((39.0, 35.0), 12.0, 10.0,
                                boxstyle="round,pad=0,rounding_size=3",
                                facecolor="none", edgecolor="#3a3a3a",
                                lw=1.4, ls=(0, (3, 2)), zorder=22))
    # 4 comb: three wires in the slots
    for dx in (-7.0, 0.0, 7.0):
        cable(125.0 + dx, 35.0, 2.0)

    # ---- dimensions / notes
    ax.annotate("", xy=(0, -8), xytext=(170, -8),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(85, -12, "170", fontsize=9.5, ha="center", color="#5b6773")
    ax.annotate("", xy=(176, 0), xytext=(176, 120),
                arrowprops=dict(arrowstyle="<->", color="#5b6773", lw=1.0))
    ax.text(179, 60, "120", fontsize=9.5, va="center", rotation=90,
            color="#5b6773")
    ax.plot([132, 152], [-12, -12], color="#12395e", lw=3.0,
            solid_capstyle="butt")
    ax.text(142, -10.0, "20 mm", fontsize=9, ha="center", color="#12395e")

    fig.suptitle("走线固定件对比 —— 4 种方案（PLA，5 mm 底板，夹子高 12）",
                 fontsize=16, fontweight="bold", y=0.965)
    fig.text(0.05, 0.035,
             "①②④ 线从上方放入；③ 用扎带把线束绑在墙边。"
             "黄色顶面 = Z12 墙顶，浅橙 = 槽/窗内底面，浅蓝 = 底板顶面。",
             fontsize=9.5, color="#495057")
    fig.text(0.05, 0.012,
             "打印：底板贴床，夹子朝上，无支撑；建议先打这个对比件，选定后替换底盘上的 10 根 Ø7 柱。",
             fontsize=9.5, color="#495057")

    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
