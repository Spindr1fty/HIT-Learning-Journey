"""The ice stone as a reference solid, built from primitives.

This is NOT a printed part. It exists so the fork can be proved to catch the
handle without touching anything it should not.

WHY PRIMITIVES, NOT A REVOLVE
The first version revolved the measured outline as one polyline face. That
produces hundreds of narrow facets, and booleans against it went non-physical:
slicing the stone gave a cross-section radius of 35 mm at a height where the
real radius is 18, and the fork's "does it lift the disc" test jumped from no
contact to 96 mm3 between two 0.5 mm steps. A union of cylinders and cones is
exact, boolean-clean, and slightly FATTER than the real stone -- which is the
safe direction for a clearance check.

The taper is approximated in two stages, so the shoulder is a straight cone
where the real stone is a smooth curve. That over-approximates the body: any
fork that clears this clears the real thing.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_params as G  # noqa: E402

BODY_R = G.STONE_DIA / 2          # 23.5
SHOULDER_R = G.STEM_DIA / 2 + 5.5  # 11.0, where the long taper starts
TAPER_TOP_Y = G.BODY_TOP_Y        # 21.6
STEM_TOP_Y = G.STEM_Y1            # 29.1
DISC_R = G.DISC_DIA / 2           # 9.0


def _cyl(r, z0, z1):
    return bd.Pos(0, 0, z0) * bd.Cylinder(
        r, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _cone(r0, r1, z0, z1):
    return bd.Pos(0, 0, z0) * bd.Cone(
        r0, r1, z1 - z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _stone():
    parts = [
        _cyl(BODY_R, 0.0, G.STONE_WIDEST_Y),
        _cone(BODY_R, SHOULDER_R, G.STONE_WIDEST_Y, TAPER_TOP_Y),
        _cone(SHOULDER_R, G.STEM_DIA / 2, TAPER_TOP_Y,
              TAPER_TOP_Y + G.FLARE_H),
        _cyl(G.STEM_DIA / 2, TAPER_TOP_Y + G.FLARE_H, STEM_TOP_Y),
        _cyl(DISC_R, STEM_TOP_Y, G.STONE_H),
    ]
    body = parts[0]
    for p in parts[1:]:
        body = body + p
    body = body.clean()
    body.label = "g_stone"
    return body


@step(out="../newSTEP/g_stone.step")
def g_stone():
    return _stone()


if __name__ == "__main__":
    s = _stone()
    b = s.bounding_box()
    print("REFERENCE ONLY -- do not print this, it is the ice stone")
    print(f"bbox X {b.max.X - b.min.X:.2f}  Y {b.max.Y - b.min.Y:.2f}"
          f"  Z {b.max.Z - b.min.Z:.2f}   valid={s.is_valid}"
          f"  solids={len(s.solids())}")
    print(f"dia {b.max.X - b.min.X:.2f} (official {G.STONE_DIA})"
          f"   height {b.max.Z:.2f} (official {G.STONE_H})")
    print()
    print("simplified profile, bottom to top")
    print(f"  cylinder r {BODY_R:.2f} ......... y 0 .."
          f" {G.STONE_WIDEST_Y:.1f}")
    print(f"  cone     r {BODY_R:.2f} -> {SHOULDER_R:.2f} .. y"
          f" {G.STONE_WIDEST_Y:.1f} .. {TAPER_TOP_Y:.1f}")
    print(f"  cone     r {SHOULDER_R:.2f} -> {G.STEM_DIA / 2:.2f} .. y"
          f" {TAPER_TOP_Y:.1f} .. {TAPER_TOP_Y + G.FLARE_H:.1f}"
          f"   (the flare the tines must clear)")
    print(f"  cylinder r {G.STEM_DIA / 2:.2f} ......... y"
          f" {TAPER_TOP_Y + G.FLARE_H:.1f} .. {STEM_TOP_Y:.1f}")
    print(f"  cylinder r {DISC_R:.2f} ......... y {STEM_TOP_Y:.1f} .."
          f" {G.STONE_H:.1f}   (the handle disc)")
