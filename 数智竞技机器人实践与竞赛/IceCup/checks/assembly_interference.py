r"""Full pairwise interference matrix for the Z-axis assembly.

Every solid against every other solid, bottom to top, nothing skipped. The
existing checks only looked at the six printed Z parts; the assembly now also
contains the servo reference body, the fork head and the servo mount, and those
are exactly where a clash would hide.

Reports the intersecting volume for all 28 pairs. A pair that merely TOUCHES --
the rail's foot on the plate, the servo flange on its mounting plate -- reports
zero and is listed as "contact", because a shared face is not a clash.

One caution that has bitten this project before: intersect() returns a ShapeList,
not a Shape, so .volume does not exist on it. The old probe used
hasattr(v, "volume") and silently returned 0 for every ShapeList, turning two
real failures into passes. The helper below sums the list instead.
"""

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import z_assembly  # noqa: E402

TOL = 0.05          # mm3 -- below this a pair is touching, not clashing


def volume_of(shape):
    """Total volume of whatever intersect() handed back."""
    if shape is None:
        return 0.0
    if hasattr(shape, "volume"):
        return shape.volume
    total = 0.0
    for item in shape:
        if item is None:
            continue
        total += getattr(item, "volume", 0.0)
    return total


def main():
    asm = z_assembly._assembly()
    parts = [(c.label or f"part{i}", c) for i, c in enumerate(asm.children)]
    print(f"solids in the assembly: {len(parts)}")
    for i, (name, _) in enumerate(parts, 1):
        print(f"  {i}. {name}")
    print()

    clashes = []
    contacts = []
    clear = 0
    for (na, a), (nb, b) in itertools.combinations(parts, 2):
        v = volume_of(a.intersect(b))
        if v > TOL:
            clashes.append((na, nb, v))
            print(f"  CLASH  {na:16} x {nb:16} {v:9.3f} mm3")
        elif v > 0.0:
            contacts.append((na, nb, v))
        else:
            clear += 1

    print()
    print(f"  distinct volumes: {clear}")
    print(f"  touching (0 < v <= {TOL}): {len(contacts)}")
    for na, nb, v in contacts:
        print(f"     {na:16} x {nb:16} {v:9.4f} mm3")
    print(f"  CLASHES: {len(clashes)}")
    for na, nb, v in clashes:
        print(f"     {na} x {nb}: {v:.2f} mm3")
    if clashes:
        print()
        print("  a clash means the STEP is not buildable as modelled")
        return 1
    print()
    print("  no pair shares volume -> the assembly is buildable as modelled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
