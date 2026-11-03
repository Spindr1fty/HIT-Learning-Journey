r"""Two laser-cut test plates, told apart by their OUTER DIAMETER.

The first version differentiated the two bolt circles with rim notches, which
in the cutter's preview looked like two identical discs with a stray circle.
Physical size cannot be misread, so now:

    horn_BCD140_D40.dxf   BCD 14.0   plate dia 40 mm   (the smaller one)
    horn_BCD144_D48.dxf   BCD 14.4   plate dia 48 mm   (the bigger one)

PLATE CONTENTS
    outer disc ......... the cut outline
    dia 12 centre hole . clears the horn's raised spline boss so the plate
                         lies flat
    four dia 3.5 holes . the bolt circle being tested; M3 screws pass through

Verify the outer diameter in the cutter software before running the job. DXF
R12 carries no unit tag, so a cutter that assumes inches will scale the plate
by 25.4 and it will be obvious immediately.

Output is DXF R12 with only LINE and CIRCLE entities.
"""

import math
import sys
from pathlib import Path

CENTRE_HOLE_D = 12.0
HORN_HOLE_D = 3.5

VERSIONS = (
    ("horn_BCD140_D40", 14.0, 40.0),
    ("horn_BCD144_D48", 14.4, 48.0),
)


def circle(cx, cy, r):
    return ("CIRCLE", [(10, cx), (20, cy), (30, 0.0), (40, r)])


def line(x1, y1, x2, y2):
    return ("LINE", [(10, x1), (20, y1), (30, 0.0),
                     (11, x2), (21, y2), (31, 0.0)])


def build(bcd, plate_d):
    ents = []
    n = 180
    pts = [(plate_d / 2 * math.cos(2 * math.pi * i / n),
            plate_d / 2 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        ents.append(line(x1, y1, x2, y2))

    ents.append(circle(0.0, 0.0, CENTRE_HOLE_D / 2))

    r = bcd / 2
    for k in range(4):
        a = math.pi / 2 * k
        ents.append(circle(r * math.cos(a), r * math.sin(a), HORN_HOLE_D / 2))
    return ents


def write_dxf(path, ents):
    out = ["0\nSECTION\n2\nENTITIES\n"]
    for kind, pairs in ents:
        out.append(f"0\n{kind}\n8\n0\n")
        for code, val in pairs:
            out.append(f"{code}\n{val}\n")
    out.append("0\nENDSEC\n0\nEOF\n")
    Path(path).write_text("".join(out), encoding="ascii")


def preview(folder):
    """Draw both plates so the shapes are known before cutting."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                       "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(1, 2, figsize=(12, 6.4), dpi=110)
    for ax, (name, bcd, plate_d) in zip(axes, VERSIONS):
        ax.set_xlim(-plate_d / 2 - 4, plate_d / 2 + 4)
        ax.set_ylim(-plate_d / 2 - 4, plate_d / 2 + 6)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Circle((0, 0), plate_d / 2, facecolor="#e9ecef",
                            edgecolor="#212529", lw=2.0))
        ax.add_patch(Circle((0, 0), CENTRE_HOLE_D / 2, facecolor="white",
                            edgecolor="#e03131", lw=1.8))
        r = bcd / 2
        for k in range(4):
            a = math.pi / 2 * k
            ax.add_patch(Circle((r * math.cos(a), r * math.sin(a)),
                                HORN_HOLE_D / 2, facecolor="white",
                                edgecolor="#1c7ed6", lw=1.8))
        ax.text(0, -plate_d / 2 - 3.0,
                f"{name}\nBCD {bcd}   外径 Ø{plate_d:.0f}",
                fontsize=12, ha="center", va="top", fontweight="bold")
        ax.set_title(f"外径 Ø{plate_d:.0f}  →  BCD {bcd}", fontsize=13,
                     fontweight="bold")

    fig.suptitle("两块试切板：靠外径区分，一大一小", fontsize=16,
                 fontweight="bold", y=0.97)
    out = folder / "test_plates_preview.png"
    fig.savefig(out, facecolor="white")
    print(f"  preview: {out}")
    return out


def main():
    desktop = Path(r"C:\Users\Spindrift\Desktop")
    if not desktop.is_dir():
        desktop = Path.home() / "Desktop"
    print(f"output folder: {desktop}")
    for name, bcd, plate_d in VERSIONS:
        ents = build(bcd, plate_d)
        path = desktop / f"{name}.dxf"
        write_dxf(path, ents)
        print(f"  {path.name:<24} BCD {bcd:<5} 外径 Ø{plate_d:.0f}"
              f"   {path.stat().st_size} bytes")
    preview(desktop)


if __name__ == "__main__":
    main()
