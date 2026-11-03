"""Slide-fit calibration coupon: one rail stub plus three carriage rings.

WHY THIS EXISTS
The full rail is ~107 cm3 and hours of printing, and its fit rests entirely on
one guessed number (SLIDE_CLEAR, currently 0.30 mm per side). Every printer
lands somewhere different. Print this first, try all three rings, and pick the
one that slides with light drag and no rock. Then set SLIDE_CLEAR in z_params
and print the real parts.

WHAT YOU GET
  one 30 x 30 x 60 rail stub, and three sleeves whose bores differ only in
  clearance. Height encodes the clearance so you can tell them apart without
  labels -- measure to confirm:
      height 10 mm -> 0.20 mm per side (bore 30.40)   tightest
      height 14 mm -> 0.30 mm per side (bore 30.60)   current guess
      height 18 mm -> 0.40 mm per side (bore 30.80)   loosest

HOW TO JUDGE
  Slide each sleeve onto the stub. The right one goes on with light, even drag
  along the whole 60 mm and does not rock when you twist it. Too tight: it
  seizes or needs force. Too loose: it rattles and the arm would droop.

Print the stub standing and the rings flat, 0.2 mm layers, same filament and
same profile you will use for the real parts -- otherwise the measurement is
about a different printer setup than the one that matters.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402

STUB_LEN = 30.0                        # 30 mm is plenty to feel drag along
STUB_W = P.RAIL_W                      # 30.0, same section as the real rail
STUB_WALL = 3.0                        # hollow stub: the outside is what matters
RING_OUTER = P.RAIL_W + 2 * P.WALL     # 42.0, same outer AND wall as the real
                                       # carriage, so the ring flexes the same
LEAD_IN = 1.5                          # square counterbore, so a 0.2 ring starts

# (height, clearance per side) -- height is the label
VARIANTS = (
    (8.0, 0.20),
    (10.0, 0.30),
    (12.0, 0.40),
)

GAP = 10.0                             # spacing when laid out for printing


def _stub():
    bar = bd.Pos(-STUB_W / 2, -STUB_W / 2, 0.0) * bd.Box(
        STUB_W, STUB_W, STUB_LEN,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    core = STUB_W / 2 - STUB_WALL
    cavity = bd.Pos(-core, -core, STUB_WALL) * bd.Box(
        2 * core, 2 * core, STUB_LEN,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    return bar.cut(cavity).clean()


def _ring(height, clear):
    """Square bore -- the rail is a 30x30 bar, so a round bore would only
    touch it on four tangent lines and tell you nothing about the real fit."""
    side = STUB_W + 2 * clear           # square bore side
    half = RING_OUTER / 2

    ring = bd.Pos(-half, -half, 0.0) * bd.Box(
        RING_OUTER, RING_OUTER, height,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))

    bore = bd.Pos(-side / 2, -side / 2, -1.0) * bd.Box(
        side, side, height + 2.0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    ring = ring.cut(bore)

    # square counterbore at each face: a 0.2 mm ring has to be able to start
    lead_side = side + 2 * LEAD_IN
    for z0 in (-1.0, height - LEAD_IN):
        lead = bd.Pos(-lead_side / 2, -lead_side / 2, z0) * bd.Box(
            lead_side, lead_side, LEAD_IN + 1.0,
            align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
        ring = ring.cut(lead)

    return ring.clean()


def _coupon_parts():
    """The positioned parts, built ONCE -- the compound and the self-check must
    run on the same solids. Rebuilding them separately is how the check
    reported clashes between parts that were actually 10 mm apart."""
    parts = [_stub()]
    names = ["stub"]
    # Start clear of the STUB's own half-width, not just the ring's.
    x = STUB_W / 2 + GAP + RING_OUTER / 2
    for height, clear in VARIANTS:
        parts.append(bd.Pos(x, 0, 0) * _ring(height, clear))
        names.append(f"ring_{int(round(clear * 100)):03d}")
        x += RING_OUTER + GAP
    return parts, names


def _coupon():
    parts, _ = _coupon_parts()
    coupon = bd.Compound(children=parts)
    coupon.label = "rail_clearance_coupon"
    return coupon


def _check_no_overlap(parts, names):
    """Boolean-intersect every pair; any shared volume is a layout bug."""
    bad = []
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            a, b = parts[i], parts[j]
            ba, bb = a.bounding_box(), b.bounding_box()
            if not (ba.min.X <= bb.max.X and bb.min.X <= ba.max.X
                    and ba.min.Y <= bb.max.Y and bb.min.Y <= ba.max.Y
                    and ba.min.Z <= bb.max.Z and bb.min.Z <= ba.max.Z):
                continue
            hit = a.intersect(b)
            if hit is None:
                continue
            vol = (hit.volume if hasattr(hit, "volume")
                   else sum(getattr(s, "volume", 0.0) for s in hit))
            if vol > 0.001:
                bad.append((names[i], names[j], vol))
    return bad


@step(out="../fitTest/rail_clearance_coupon.step")
def rail_clearance_coupon():
    return _coupon()


if __name__ == "__main__":
    c = rail_clearance_coupon()
    b = c.bounding_box()

    # the SAME positioned solids that ship in the compound
    check_parts, names = _coupon_parts()
    clashes = _check_no_overlap(check_parts, names)

    print(f"coupon: 1 stub + {len(VARIANTS)} rings,"
          f"  solids {len(c.solids())}  valid={c.is_valid}")
    print(f"stub {STUB_W} x {STUB_W} x {STUB_LEN}, hollowed to"
          f" {STUB_WALL} walls")
    print(f"ring outer {RING_OUTER}  walls {(RING_OUTER - STUB_W) / 2:.1f}/side")
    print()
    if clashes:
        print("LAYOUT CLASHES:")
        for a, bb_, vol in clashes:
            print(f"  {a} <-> {bb_}: {vol:.3f} mm3  *** FIX ***")
    else:
        print("layout check: PASS - no two coupon parts share volume")
    print()
    print(f"{'height':>8}{'clear/side':>12}{'bore side':>11}{'judge':>28}")
    for height, clear in VARIANTS:
        tag = ("tightest" if clear == 0.20 else
               "current guess" if clear == 0.30 else "loosest")
        print(f"{height:>8.0f}{clear:>12.2f}{STUB_W + 2 * clear:>11.2f}"
              f"{tag:>28}")
    print()
    print(f"lay-out bbox X {b.max.X - b.min.X:.1f}"
          f"  Y {b.max.Y - b.min.Y:.1f}  Z {b.max.Z - b.min.Z:.1f}")
    vol = c.volume / 1000
    print(f"volume {vol:.1f} cm3  (~{vol * 1.24:.0f} g PLA)")
    print(f"target: the ring that glides with light drag and does not rock")
