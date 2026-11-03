r"""Check the two fork-head tips: are the lips pointed to the plate's edge, and
does option B's thickness slope survive?

Run after any change to the mouth geometry.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cadgen import build123d as bd  # noqa: E402

import g_fork as F  # noqa: E402


def main():
    m = F._head()

    def solid(x, y, z):
        p = bd.Pos(x, y, z) * bd.Box(
            0.1, 0.1, 0.1,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        v = p.intersect(m)
        if v is None:
            return 0.0
        if hasattr(v, "volume"):
            return v.volume
        return sum(getattr(q, "volume", 0.0) for q in v if q is not None)

    print("lip taper: near the plate's edge (Y -25.5), walked along X")
    for x in (36.0, 38.0, 40.0, 42.0, 44.0, 46.0):
        v = solid(x, -25.5, 1.0)
        print(f"   X={x:5.1f}  {'material' if v > 0.0005 else 'cut away'}")

    print()
    print("option B slope: inboard (Y -20), walked along Z")
    for x in (38.0, 41.0, 44.0, 47.0, 49.0):
        zs = [z for z in (0.4, 1.2, 1.9, 2.5, 3.1) if solid(x, -20.0, z) > 0.0005]
        top = max(zs) if zs else 0.0
        print(f"   X={x:5.1f}  thickness top about {top:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
