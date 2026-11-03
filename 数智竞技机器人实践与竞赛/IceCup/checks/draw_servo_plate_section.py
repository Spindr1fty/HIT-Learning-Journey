r"""Cross-sections of the servo plate, to settle whether the relief and the rib
are in the wrong places.

Two cuts, both measured off the model rather than read off the source:

    panel A   horizontal cut at Z = 160 (inside the relief band)
              X across, Y down.  Shows the plate, the relief cut into its
              servo-side face, and the rib standing off the back.
    panel B   vertical cut at X = -92 (inside the left relief)
              Z across, Y down.  Shows how tall the relief is and how much
              taller the rib is.

The point of the picture: the rib sits on the OPPOSITE face to the relief, and
directly behind it, so what it does is turn a 3.5 mm web into a 7.5 mm T.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PLATE_Y = (-31.0, -25.0)
RELIEF_Y = (-27.5, -25.0)
RIB_Y = (-35.0, -30.0)
PLATE_X = (-96.25, -24.0)
WIN_X = (-86.5, -45.5)
SLOT_XS = ((-96.25, -86.5), (-45.5, -24.0))
COLLAR_X0 = -27.3
PLATE_Z = (133.0, 187.0)
RELIEF_Z = (158.5, 161.5)
RIB_Z = (152.0, 168.0)
HOLES_X = (-90.25, -41.75)
HOLES_Z = (155.0, 165.0)

C_PLATE = "#d0ebff"
C_RIB = "#c5f6c5"
C_SLOT = "#ffffff"
C_EDGE = "#0b4f8a"


def panel_a(ax):
    ax.set_xlim(-100, -20)
    ax.set_ylim(-38, -23)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("A. Z=160 水平剖（看 X-Y）", fontsize=13, fontweight="bold")

    # the plate body
    ax.add_patch(Rectangle((PLATE_X[0], PLATE_Y[0]),
                           PLATE_X[1] - PLATE_X[0],
                           PLATE_Y[1] - PLATE_Y[0],
                           facecolor=C_PLATE, edgecolor=C_EDGE, lw=1.6))
    # the window is a through hole
    ax.add_patch(Rectangle((WIN_X[0], PLATE_Y[0] - 0.3),
                           WIN_X[1] - WIN_X[0],
                           PLATE_Y[1] - PLATE_Y[0] + 0.6,
                           facecolor="white", edgecolor=C_EDGE, lw=1.2))
    # the two reliefs, cut into the servo-side face
    for x0, x1 in SLOT_XS:
        ax.add_patch(Rectangle((x0, RELIEF_Y[0]), x1 - x0,
                               RELIEF_Y[1] - RELIEF_Y[0],
                               facecolor="white", edgecolor="#e03131", lw=1.2))
    # the ribs, standing off the back, at the same X ranges
    for x0, x1 in SLOT_XS:
        ax.add_patch(Rectangle((x0, RIB_Y[0]), x1 - x0,
                               RIB_Y[1] - RIB_Y[0],
                               facecolor=C_RIB, edgecolor="#2f9e44", lw=1.4))
    # the collar
    ax.add_patch(Rectangle((COLLAR_X0, PLATE_Y[0]), 6.0, 0.9,
                           facecolor="#e9ecef", edgecolor="#868e96", lw=1.2))

    ax.axhline(PLATE_Y[0], color="#868e96", lw=0.8, ls=":")
    ax.text(-99, -36.6, "Y=-35 筋的外表面", fontsize=8.5, color="#2f9e44")
    ax.text(-99, -31.6, "Y=-31 板背面", fontsize=8.5, color=C_EDGE)
    ax.text(-99, -25.6, "Y=-25 贴面（舵机那面）", fontsize=8.5, color=C_EDGE)
    ax.text(-73, -29.4, "让位窗（通）", fontsize=8.5, ha="center")
    ax.text(-91, -26.3, "缝", fontsize=8, ha="center", color="#e03131")
    ax.text(-35, -26.3, "缝", fontsize=8, ha="center", color="#e03131")
    ax.text(-91, -33.2, "筋", fontsize=8.5, ha="center", color="#2f9e44")
    ax.text(-35, -33.2, "筋", fontsize=8.5, ha="center", color="#2f9e44")
    ax.set_xlabel("X", fontsize=9)
    ax.set_ylabel("Y", fontsize=9)


def panel_b(ax):
    ax.set_xlim(-100, -20)
    ax.set_ylim(-38, -25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("B. X=-92 竖向剖（看 Z-Y）", fontsize=13, fontweight="bold")

    # plate body, full height
    ax.add_patch(Rectangle((PLATE_X[0], PLATE_Y[0]),
                           PLATE_X[1] - PLATE_X[0],
                           PLATE_Y[1] - PLATE_Y[0],
                           facecolor=C_PLATE, edgecolor=C_EDGE, lw=1.6))
    ax.set_ylim(-38, -23)
    ax.set_ylabel("Y", fontsize=9)
    ax.set_xlabel("X", fontsize=9)


def main(out):
    fig = plt.figure(figsize=(15, 6.2), dpi=115)
    panel_a(fig.add_axes([0.05, 0.14, 0.60, 0.74]))
    # panel B is a Z-Y view, drawn separately below
    ax2 = fig.add_axes([0.70, 0.14, 0.28, 0.74])
    ax2.set_xlim(-6, 34)
    ax2.set_ylim(-38, -23)
    ax2.set_aspect("auto")
    ax2.axis("off")
    ax2.set_title("B. X=-92 竖向剖（Z-Y 侧视）", fontsize=13, fontweight="bold")

    z0, z1 = 148.0, 176.0
    def zx(z):
        return (z - z0) / (z1 - z0) * 40.0 - 6.0

    # plate body as a horizontal band
    ax2.add_patch(Rectangle((zx(z0), PLATE_Y[0]), 40.0, PLATE_Y[1] - PLATE_Y[0],
                            facecolor=C_PLATE, edgecolor=C_EDGE, lw=1.6))
    # relief band, cut from the servo side
    ax2.add_patch(Rectangle((zx(RELIEF_Z[0]), RELIEF_Y[0]),
                            zx(RELIEF_Z[1]) - zx(RELIEF_Z[0]),
                            RELIEF_Y[1] - RELIEF_Y[0],
                            facecolor="white", edgecolor="#e03131", lw=1.2))
    # rib band, standing off the back
    ax2.add_patch(Rectangle((zx(RIB_Z[0]), RIB_Y[0]),
                            zx(RIB_Z[1]) - zx(RIB_Z[0]),
                            RIB_Y[1] - RIB_Y[0],
                            facecolor=C_RIB, edgecolor="#2f9e44", lw=1.4))
    for z in (RELIEF_Z[0], RELIEF_Z[1], RIB_Z[0], RIB_Z[1]):
        ax2.plot([zx(z), zx(z)], [-24.0, -23.4], color="#495057", lw=0.8)
        ax2.text(zx(z), -23.2, f"{z:.0f}", fontsize=7.5, ha="center",
                 rotation=90, va="top")
    ax2.text(zx(160) - 1, -36.0, "筋 Z 152~168", fontsize=9, color="#2f9e44",
             rotation=90, ha="center")
    ax2.text(zx(160) + 2.5, -36.0, "缝 Z 158.5~161.5", fontsize=9,
             color="#e03131", rotation=90, ha="center")
    ax2.set_title("B. X=-92 处竖向剖（横轴 Z，纵轴 Y）", fontsize=12,
                  fontweight="bold")

    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sec.png")
