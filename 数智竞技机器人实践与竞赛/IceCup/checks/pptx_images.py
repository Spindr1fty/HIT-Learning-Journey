"""Extract every embedded picture from a .pptx, named by slide and order.

Usage:  python pptx_images.py <deck.pptx> <out_dir>
"""

import io
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk(sh.shapes)
            continue
        yield sh


def main(path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    prs = Presentation(path)
    n = 0
    for idx, slide in enumerate(prs.slides, 1):
        k = 0
        for sh in walk(slide.shapes):
            if sh.shape_type != MSO_SHAPE_TYPE.PICTURE:
                continue
            k += 1
            n += 1
            img = sh.image
            ext = img.ext or "png"
            name = f"s{idx:02d}_p{k:02d}.{ext}"
            dest = os.path.join(out_dir, name)
            with io.open(dest, "wb") as fh:
                fh.write(img.blob)
            w_mm = round(sh.width / 914400 * 25.4, 1) if sh.width else None
            h_mm = round(sh.height / 914400 * 25.4, 1) if sh.height else None
            print(f"{name}\tshapecount={k}\tplotted={w_mm}x{h_mm}mm\tbytes={len(img.blob)}")
    print(f"TOTAL {n} pictures -> {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    main(sys.argv[1], sys.argv[2])
