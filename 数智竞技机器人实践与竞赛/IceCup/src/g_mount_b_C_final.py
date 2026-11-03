r"""Final C: rear frame + both side panels + solid top cover.

Chosen from the C option:
    rear frame X 37.5..40, window 44 x 21
    side panels X 12..40, Z 19..35.5, inner Y +/-23.69
    top cover X 4.5..40, Y 20.69..79.69, Z 35..38
    W3 wire windows on BOTH side panels:
        X 33..37.5, Z 27..34, through the 3 mm walls
        left  Y 20.00..24.50
        right Y 75.88..80.38  (mirror about Y=50.19)

M4 x 12 socket-head bolts go in from the rear, heads inside; nuts on the
front X=0.  A long ball-end 3 mm hex key reaches the heads through the
44 x 21 rear window.

No new chamfers yet (the rev30 base already carries its own 1 mm chamfers).
Pure ASCII on purpose.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b_desktop_half as H  # noqa: E402
import chamfer_part as C  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "newSTEP"


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _chamfer(p):
    """1 mm on the new outer edges only; base chamfers stay as imported."""
    edges = []
    for e in p.edges():
        m = e.position_at(0.5)
        hit = False
        if abs(m.Z - 38.0) < 0.01:
            if (abs(m.Y - 20.69) < 0.02 or abs(m.Y - 79.69) < 0.02
                    or abs(m.X - 40.0) < 0.02):
                hit = True
        if abs(m.Y - 20.69) < 0.02 or abs(m.Y - 79.69) < 0.02:
            if (abs(m.X - 12.0) < 0.02 or abs(m.X - 40.0) < 0.02
                    or abs(m.Z - 19.0) < 0.02):
                hit = True
        if abs(m.X - 40.0) < 0.02 and (abs(m.Y - 21.94) < 0.03
                                       or abs(m.Y - 78.44) < 0.03):
            hit = True
        if hit:
            edges.append(e)
    specs = [(e.position_at(0.5),
              bd.Vector(e.tangent_at(0.5)).normalized(), e) for e in edges]
    fails, done = [], []
    out = C._chamfer_set(p, specs, 1.0, fails, done)
    print(f"chamfer: {len(edges)} edges, {len(done)} set(s), {len(fails)} refused")
    return out


def final(chamfer=True):
    p = H.c()
    cuts = [
        _box(33.0, 37.5, 20.00, 24.50, 27.0, 34.0),   # left W3
        _box(33.0, 37.5, 75.88, 80.38, 27.0, 34.0),   # right W3 (mirror)
    ]
    p = p.cut(*cuts).clean()
    if chamfer:
        p = _chamfer(p)
    p.label = "C_final"
    return p


if __name__ == "__main__":
    p = final()
    b = p.bounding_box()
    print(f"bbox X {b.min.X:.2f}..{b.max.X:.2f}  Y {b.min.Y:.2f}..{b.max.Y:.2f}"
          f"  Z {b.min.Z:.2f}..{b.max.Z:.2f}")
    print(f"valid={p.is_valid}  solids={len(p.solids())}"
          f"  vol {p.volume / 1000:.3f} cm3 ({p.volume / 1000 * 1.24:.1f} g)")
    for ext, fn in (("step", bd.export_step), ("stl", bd.export_stl)):
        out = OUT / f"g_mount_b_C_final.{ext}"
        if ext == "stl":
            ok = fn(p, str(out), tolerance=0.01, angular_tolerance=0.3)
        else:
            ok = fn(p, str(out))
        print(f"{ext}:", ok, out)
