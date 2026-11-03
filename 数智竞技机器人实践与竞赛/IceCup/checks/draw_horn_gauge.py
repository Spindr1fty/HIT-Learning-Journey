r"""Print-at-100% template for identifying the servo horn's bolt circle.

Laying the real horn on a 1:1 print is far more reliable than reading calipers
off a photo: there is no reading error, no edge-vs-centre ambiguity, and the
scale bar proves the printer did not rescale the page.

Four candidate bolt circles are drawn side by side, each with the horn's 20 mm
outline. Put the horn on each panel, look through the holes, and see which one
lines up. The answer is the panel whose four holes sit exactly under the horn's
four.

Every dimension is millimetres and the figure is sized so that 1 mm on paper is
1 mm in the file, so it must be printed at 100% (not "fit to page").
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HORN_D = 20.0
HORN_HOLE_D = 2.5          # the horn's own tapped hole for an M3 screw
CANDIDATES = (11.4, 13.0, 14.4, 16.0)
PITCH = 34.0               # spacing between the panels, mm
WIDTH_MM = PITCH * len(CANDIDATES) + 8.0
HEIGHT_MM = 62.0


def main(out):
    fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH_MM)
    ax.set_ylim(0, HEIGHT_MM)
    ax.set_aspect("equal")
    ax.axis("off")

    for i, bcd in enumerate(CANDIDATES):
        cx = 4.0 + PITCH * i + PITCH / 2.0 - 6.0
        cy = 38.0

        ax.add_patch(Circle((cx, cy), HORN_D / 2.0, facecolor="none",
                            edgecolor="#868e96", lw=0.6, ls=(0, (2, 1.5))))
        r = bcd / 2.0
        for k in range(4):
            a = 3.141592653589793 / 2.0 * k
            hx = cx + r * __import__("math").cos(a)
            hy = cy + r * __import__("math").sin(a)
            ax.add_patch(Circle((hx, hy), HORN_HOLE_D / 2.0,
                                facecolor="none", edgecolor="#e03131", lw=0.8))
        # crosshair
        ax.plot([cx - 12, cx + 12], [cy, cy], color="#adb5bd", lw=0.3)
        ax.plot([cx, cx], [cy - 12, cy + 12], color="#adb5bd", lw=0.3)

        ax.text(cx, cy - 15.0, f"BCD {bcd}", fontsize=7,
                ha="center", va="top", fontweight="bold")

    # a 50 mm scale bar -- if this does not measure 50 mm, the print is scaled
    y0 = 8.0
    ax.plot([6, 56], [y0, y0], color="#212529", lw=1.2)
    for x in (6, 56):
        ax.plot([x, x], [y0 - 1.5, y0 + 1.5], color="#212529", lw=1.2)
    ax.text(31, y0 + 3.0, "50 mm 校准条", fontsize=7, ha="center")
    ax.text(31, y0 - 5.5,
            "打印后先量这条线。不是 50mm 就是打印被缩放了，模板无效。",
            fontsize=6, ha="center", color="#e03131")

    ax.text(WIDTH_MM / 2.0, HEIGHT_MM - 3.0,
            "舵盘孔距 1:1 模板  ——  必须 100% 打印，不要「适应页面」",
            fontsize=7.5, ha="center", va="top", fontweight="bold")

    fig.savefig(out, facecolor="white")
    print(f"wrote {out}  ({WIDTH_MM:.0f} x {HEIGHT_MM:.0f} mm at 100%)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "horn_gauge.svg")
