r"""Wire-exit options for the C body (rear frame + side panels + top cover).

The C body is the one-piece rev30-based design from g_mount_b_desktop_half:
    rear frame X 37.5..40, window 44 x 21
    side panels X 12..40, Z 19..35.5, inner Y +/-23.69
    top cover X 4.5..40, Y +/-20.69..79.69, Z 35..38

The servo cable can leave the body at four places; each option matches one:
    W0 front side gap  cable exits the body side near the front (X ~ 8)
    W1 rear window     cable exits the body tail (X = 37.5)
    W2 top hole        cable exits the body top (X ~ 34, Z = 34)
    W3 side rear       cable exits the body side near the rear (X ~ 34)

W2 cuts a 6 x 12 hole + 1 mm rim in the top cover.
W3 cuts a 4.5 x 7 window in the left side panel.
W0/W1 add no material; they use the existing gaps.

Wire tubes and the servo are render-only; bracket STEPs are exported without
them.  Pure ASCII on purpose.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b_desktop_half as H  # noqa: E402
import g_mount_b as M  # noqa: E402
import g_servo as S  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "newSTEP"
WIRE_R = 2.0


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _seg(p0, p1, r):
    v = bd.Vector(p1) - bd.Vector(p0)
    pl = bd.Plane(origin=p0, z_dir=v.normalized())
    return pl * bd.Cylinder(r, v.length,
                            align=(bd.Align.CENTER, bd.Align.CENTER,
                                   bd.Align.MIN))


def tube(points, r=WIRE_R):
    parts = []
    for a, b in zip(points, points[1:]):
        parts.append(_seg(a, b, r))
        parts.append(bd.Pos(*a) * bd.Sphere(r))
    parts.append(bd.Pos(*points[-1]) * bd.Sphere(r))
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out.clean()


def servo_ref():
    return bd.Pos(M.SERVO_X, M.SERVO_Y, M.SERVO_Z) * M._servo_rot() * (
        S.servo_solid() + S.horn_solid())


def w0_body():
    return H.c()


def w1_body():
    return H.c()


def w2_body():
    p = H.c()
    rim = _box(29.0, 39.0, 42.0, 58.0, 38.0, 39.0)
    p = p.fuse(rim).clean()
    hole = _box(31.0, 37.0, 44.0, 56.0, 34.0, 40.0)
    p = p.cut(hole).clean()
    p.label = "wire_W2"
    return p


def w3_body():
    p = H.c()
    win = _box(33.0, 37.5, 20.0, 24.5, 27.0, 34.0)
    p = p.cut(win).clean()
    p.label = "wire_W3"
    return p


PATHS = {
    "W0": [(8.0, 30.19, 30.0), (8.0, 25.0, 30.0),
           (8.0, 18.0, 30.0), (4.0, 18.0, 29.0)],
    "W1": [(37.5, 50.0, 30.0), (42.0, 50.0, 30.0),
           (48.0, 50.0, 28.0), (55.0, 51.0, 26.0)],
    "W2": [(34.0, 50.0, 34.0), (34.0, 50.0, 38.0),
           (34.0, 50.0, 44.0), (34.0, 51.0, 48.0)],
    "W3": [(34.0, 30.19, 30.0), (34.0, 26.0, 30.0),
           (34.0, 21.0, 30.0), (34.0, 18.0, 30.0),
           (31.0, 18.0, 29.0)],
}
BODIES = [("W0", w0_body), ("W1", w1_body), ("W2", w2_body), ("W3", w3_body)]
TAGS = {"W0": "frontside", "W1": "rear", "W2": "top", "W3": "siderear"}


if __name__ == "__main__":
    for name, fn in BODIES:
        body = fn()
        print(f"{name}: vol {body.volume / 1000:.3f} cm3"
              f"  valid={body.is_valid}  solids={len(body.solids())}")
        out = OUT / f"g_mount_b_wire_{name}_{TAGS[name]}.step"
        print("  bracket:", bd.export_step(body, str(out)), out)

        wire = tube(PATHS[name])
        comp = bd.Compound(children=[body, servo_ref(), wire])
        comp.label = f"wire_{name}_render"
        rout = OUT / f"_wire_{name}_render.step"
        print("  render:", bd.export_step(comp, str(rout)), rout)
