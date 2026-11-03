"""Dump a .pptx to a UTF-8 text file.

Extracts per slide: text frames (with position), tables, picture counts,
speaker notes, and the deck's slide size. Writes UTF-8 so the caller can read
it without the console's GBK codepage mangling Chinese text.

Usage:  python pptx_dump.py <deck.pptx> <out.txt>
"""

import io
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

EMU_PER_MM = 914400 / 25.4


def mm(v):
    return None if v is None else round(v / EMU_PER_MM, 2)


def walk(shapes, sink, depth=0):
    """Yield shapes, descending into groups."""
    pad = "  " * depth
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            sink.append(f"{pad}[GROUP] {sh.name!r}")
            walk(sh.shapes, sink, depth + 1)
            continue

        left, top = mm(sh.left), mm(sh.top)
        pos = f"@({left},{top})mm" if left is not None else "@(?)"

        if sh.has_text_frame:
            text = "\n".join(p.text for p in sh.text_frame.paragraphs)
            if text.strip():
                sink.append(f"{pad}[TEXT] {sh.name!r} {pos}")
                for line in text.splitlines():
                    sink.append(f"{pad}    {line}")
                sink.append("")

        if getattr(sh, "has_table", False) and sh.has_table:
            tbl = sh.table
            sink.append(
                f"{pad}[TABLE] {sh.name!r} {pos} "
                f"rows={len(tbl.rows)} cols={len(tbl.columns)}"
            )
            for row in tbl.rows:
                cells = [c.text.replace("\n", " / ").strip() for c in row.cells]
                sink.append(f"{pad}    | " + " | ".join(cells) + " |")
            sink.append("")

        if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
            sink.append(f"{pad}[PICTURE] {sh.name!r} {pos}")
            sink.append("")

        if sh.has_chart:
            sink.append(f"{pad}[CHART] {sh.name!r} {pos}")
            sink.append("")


def dump(path, out_path):
    prs = Presentation(path)
    sink = []
    sink.append(f"FILE  : {path}")
    sink.append(f"SLIDES: {len(prs.slides)}")
    sink.append(
        f"SIZE  : {mm(prs.slide_width)} x {mm(prs.slide_height)} mm "
        f"({prs.slide_width} x {prs.slide_height} EMU)"
    )
    sink.append("=" * 72)

    for idx, slide in enumerate(prs.slides, 1):
        sink.append("")
        sink.append(f"########## SLIDE {idx} ##########")
        try:
            sink.append(f"layout: {slide.slide_layout.name}")
        except Exception:
            pass
        sink.append("")
        walk(slide.shapes, sink)

        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text
            if notes.strip():
                sink.append(f"--- NOTES (slide {idx}) ---")
                for line in notes.splitlines():
                    sink.append(f"    {line}")
                sink.append("")

    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sink))

    print(f"wrote {out_path}: {len(sink)} lines, {len(prs.slides)} slides")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    dump(sys.argv[1], sys.argv[2])
