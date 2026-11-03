"""Regenerate src/parts_data.py from the DXFs in dxf/ as idealised geometry.

The drawings share one drafting signature: outlines carry a ~0.3 mm taper and
hole rows carry sub-0.25 mm placement jitter, both confirmed as error. Columns
are pinned to COL_PITCH on a part-wide grid (hole rows are interrupted by
slots, so an index-within-row would be wrong), rows are least-squares fits.

Every part is validated before it is emitted; a fit that does not hold the
holes inside the outline raises instead of writing bad data.

Run:  python src/gen_parts_data.py
"""

import math
import sys
from pathlib import Path

import ezdxf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dxfgeom  # noqa: E402

DXF_DIR = Path(__file__).resolve().parents[1] / "dxf"
OUT = Path(__file__).resolve().parent / "parts_data.py"

# Parts whose X margins the drawing got wrong; symmetrise them.
PARTS = {
    "6circle": ("SIX_CIRCLE", True),
    "8circle": ("EIGHT_CIRCLE", True),
    "Lshape": ("L_SHAPE", False),
    "Moveitem": ("MOVE_ITEM", False),
    "Shortitem": ("SHORT_ITEM", False),
}

COL_PITCH = 8.25
THICKNESS = 5.0
SLOT_WIDTH = 4.5
BIG_HOLE_DIAMETER = 8.0
MAX_FIT_RESIDUAL = 0.30
EDGE_CLEARANCE = 1.5


def _fit_offset(pairs):
    """Offset of  offset + COL_PITCH * index, by least squares."""
    n = len(pairs)
    return (sum(v - COL_PITCH * i for i, v in pairs)) / n


def _cluster(values, gap):
    out, cur = [], [min(values)]
    for v in sorted(values)[1:]:
        if v - cur[-1] > gap:
            out.append(cur)
            cur = []
        cur.append(v)
    out.append(cur)
    return out


def _outline_size(doc, dims):
    """Intended rectangle size, immune to the drawings' slanted edges.

    A bbox inflates the result when an edge is slanted (Shortitem measures
    49.730 x 24.285 but is dimensioned 49.647 x 24.057). Prefer a DIMENSION
    that matches an edge; fall back to the mean of the two like-oriented edges.

    Only LINE-only closed loops qualify as an outline, so the straight sides of
    a slot are never mistaken for a plate edge.
    """
    line_segs = [s for e in doc.modelspace().query("LINE") for s in dxfgeom.segments(e)]
    loops = [lp for lp in dxfgeom.chain_loops(line_segs)
             if len(lp) > 2 and math.dist(lp[0], lp[-1]) < dxfgeom.TOL]
    if not loops:
        return None
    outer = max(loops, key=dxfgeom.area)

    horiz, vert = [], []
    for a, b in zip(outer, outer[1:] + outer[:1]):
        dx, dy = abs(b[0] - a[0]), abs(b[1] - a[1])
        if max(dx, dy) < 1e-6:
            continue
        (horiz if dx >= dy else vert).append(max(dx, dy))
    if not horiz or not vert:
        return None

    def pick(group):
        best, err = None, 0.06
        for d in dims:
            for g in group:
                if abs(d - g) < err:
                    best, err = d, abs(d - g)
        return best if best is not None else sum(group) / len(group)

    return pick(horiz), pick(vert)


def extract(name):
    key, symmetrise_x = PARTS[name]
    doc = ezdxf.readfile(DXF_DIR / f"{name}.dxf")
    circles = [(e.dxf.center.x, e.dxf.center.y, e.dxf.radius)
               for e in doc.modelspace().query("CIRCLE")]
    dims = [round(getattr(e.dxf, "actual_measurement", 0.0), 3)
            for e in doc.modelspace().query("DIMENSION")
            if getattr(e.dxf, "actual_measurement", None)]
    loops = [lp for lp in dxfgeom.loops_of(doc) if len(lp) > 2]
    loops.sort(key=dxfgeom.area, reverse=True)
    bx0, by0, bx1, by1 = dxfgeom.bbox(loops[0])

    size = _outline_size(doc, dims)
    if size:
        w, h = size
        print(f"{name:11s} outline from dimensions {w:.3f} x {h:.3f}"
              f"   (bbox was {bx1-bx0:.3f} x {by1-by0:.3f})")
        ox0, oy0, ox1, oy1 = bx0, by0, bx0 + w, by0 + h
    else:
        print(f"{name:11s} outline from bbox {bx1-bx0:.3f} x {by1-by0:.3f} (no dims)")
        ox0, oy0, ox1, oy1 = bx0, by0, bx1, by1

    # Rows by Y gaps; columns by index on one part-wide X grid.
    row_groups = _cluster([c[1] for c in circles], gap=COL_PITCH * 0.6)
    x_ref = min(c[0] for c in circles)
    col_index = {round((c[0] - x_ref) / COL_PITCH) for c in circles}

    # Per-row centre Y, then a least-squares row grid.
    row_centres = [sum(g) / len(g) for g in sorted(row_groups, reverse=True)]
    row0, row_pitch = _fit_offset_and_pitch(list(enumerate(row_centres)))

    pairs = [(round((x - x_ref) / COL_PITCH), x) for x, _, _ in circles]
    col0 = _fit_offset(pairs)
    col_res = _rms(pairs, lambda i: col0 + COL_PITCH * i)

    holes = []
    for x, y, r in circles:
        ci = round((x - x_ref) / COL_PITCH)
        ri = min(range(len(row_centres)), key=lambda i: abs(y - row_centres[i]))
        d = BIG_HOLE_DIAMETER if 2 * r >= 7.5 else 2 * r
        holes.append((col0 + COL_PITCH * ci, row0 + row_pitch * ri, d / 2))

    hx = [h[0] for h in holes]
    if symmetrise_x:
        left = min(hx) - ox0
        x1 = max(hx) + left
    else:
        x1 = ox1

    slots = []
    for lp in loops[1:]:
        sx0, sy0, sx1, sy1 = dxfgeom.bbox(lp)
        w, h = sx1 - sx0, sy1 - sy0
        if max(w, h) / max(min(w, h), 1e-9) < 2.5:
            continue
        r_old = min(w, h) / 2
        cy = (sy0 + sy1) / 2
        slots.append((sx0 + r_old, cy, sx1 - r_old, cy, SLOT_WIDTH))

    _validate(name, ox0, oy0, x1, oy1, holes, slots, col_res, len(col_index))

    print(f"{name:11s} {x1-ox0:8.3f} x {oy1-oy0:7.3f} x {THICKNESS}  "
          f"holes={len(holes):2} slots={len(slots)}  cols={len(col_index)}  rows={len(row_centres)}")
    print(f"            col pitch pinned {COL_PITCH}  residual {col_res:.3f}"
          f"   row pitch {row_pitch:.4f}  first row y {row0:.3f}")
    print(f"            margin  L {min(hx)-ox0:.3f}  R {x1-max(hx):.3f}"
          f"  T {oy1-max(h[1] for h in holes):.3f}  B {min(h[1] for h in holes)-oy0:.3f}")
    for s in slots:
        print(f"            slot ({s[0]:.3f},{s[1]:.3f})-({s[2]:.3f},{s[3]:.3f}) w{s[4]}")

    return {"outline": [(ox0, oy1), (x1, oy1), (x1, oy0), (ox0, oy0)],
            "holes": holes, "slots": slots}


def _fit_offset_and_pitch(pairs):
    n = len(pairs)
    if n < 2:
        return pairs[0][1], 0.0
    sx = sum(i for i, _ in pairs)
    sy = sum(v for _, v in pairs)
    sxx = sum(i * i for i, _ in pairs)
    sxy = sum(i * v for i, v in pairs)
    pitch = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    return (sy - pitch * sx) / n, pitch


def _rms(pairs, model):
    return (sum((v - model(i)) ** 2 for i, v in pairs) / len(pairs)) ** 0.5


def _validate(name, x0, y0, x1, y1, holes, slots, col_res, n_cols):
    problems = []
    if col_res > MAX_FIT_RESIDUAL:
        problems.append(f"column fit residual {col_res:.3f} mm exceeds {MAX_FIT_RESIDUAL}")
    for cx, cy, r in holes:
        if not (x0 + r + EDGE_CLEARANCE <= cx <= x1 - r - EDGE_CLEARANCE
                and y0 + r + EDGE_CLEARANCE <= cy <= y1 - r - EDGE_CLEARANCE):
            problems.append(f"hole ({cx:.2f},{cy:.2f}) R{r} outside outline with "
                            f"{EDGE_CLEARANCE} mm clearance")
    for sx0, sy0, sx1, sy1, w in slots:
        if not (x0 < sx0 and sx1 < x1 and y0 + w / 2 < sy0 < y1 - w / 2):
            problems.append(f"slot ({sx0:.2f},{sy0:.2f})-({sx1:.2f},{sy1:.2f}) escapes outline")
    if problems:
        raise SystemExit(f"{name}: REJECTED\n  " + "\n  ".join(problems))


def main():
    data = {name: extract(name) for name in PARTS}

    lines = ['"""Idealised part geometry derived from dxf/*.dxf by gen_parts_data.py.',
             "",
             "Drafting error in the sources (outline taper, sub-0.25 mm hole jitter) is",
             "removed: columns pinned to 8.25 mm pitch on a part-wide grid, rows",
             "least-squares fitted, big holes normalised to 8 mm, slots to 4.5 mm wide",
             "with matching end radii. Regenerate with gen_parts_data.py.",
             '"""',
             "",
             f"THICKNESS = {THICKNESS}",
             ""]
    for name, (key, _) in PARTS.items():
        d = data[name]
        lines.append(f"{key} = {{")
        lines.append("    'outline': [")
        lines += [f"        ({x:.4f}, {y:.4f})," for x, y in d["outline"]]
        lines += ["    ],", "    'holes': ["]
        lines += [f"        ({x:.4f}, {y:.4f}, {r:.4f})," for x, y, r in d["holes"]]
        lines += ["    ],", "    'slots': ["]
        lines += [f"        ({a:.4f}, {b:.4f}, {c:.4f}, {d:.4f}, {w:.4f}),"
                  for a, b, c, d, w in d["slots"]]
        lines += ["    ],", "}", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
