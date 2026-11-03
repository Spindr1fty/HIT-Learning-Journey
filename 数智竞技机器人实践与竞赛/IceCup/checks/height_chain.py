r"""Height-chain check for the Z axis: does the fork reach every cell, and does
anything hit the base plate at the bottom stop?

Two things have to hold at the same time and they pull opposite ways:

  bottom stop   the fork plate hangs 74 mm below the pinion centre, so the
                pinion must not go below 74 or the plate enters the 8 mm base
  top stop      the tines have to reach under the top cell's stone disc, which
                is 220.6 mm above the table

The old bottom stop was Z 45 and the assembly never checked the first condition
-- the plate went 29 mm into the base.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import z_params as P  # noqa: E402

PLATE_BELOW_PINION = 160.0 - 86.0      # fork plate bottom, module frame
TINE_BELOW_PINION = 160.0 - 110.0      # tines, fork bolts at Z 123
CELL_FLOORS = (19.0, 107.0, 191.0)     # measured on the rack
DISC_UNDER = 29.64                     # cell floor to the stone disc's underside


def main():
    print(f"Z_MIN {P.Z_MIN:.0f}   Z_MAX {P.Z_MAX:.0f}"
          f"   stroke {P.Z_MAX - P.Z_MIN:.0f}")
    print()
    print("bottom stop")
    plate = P.Z_MIN - PLATE_BELOW_PINION
    print(f"  pinion Z {P.Z_MIN:.0f} -> fork plate bottom Z {plate:+.1f}")
    ok_bottom = plate > 0.0
    print(f"  {'clears the base plate' if ok_bottom else 'DRIVES INTO THE BASE'}")
    print()
    print("reach")
    lo = P.Z_MIN - TINE_BELOW_PINION
    hi = P.Z_MAX - TINE_BELOW_PINION
    need_lo = CELL_FLOORS[0] + DISC_UNDER
    need_hi = CELL_FLOORS[-1] + DISC_UNDER
    print(f"  tines span {lo:.1f} .. {hi:.1f}")
    print(f"  needed    {need_lo:.1f} .. {need_hi:.1f}")
    ok_reach = lo <= need_lo and hi >= need_hi
    print(f"  {'all three cells reachable' if ok_reach else 'UNREACHABLE CELL'}")
    print()
    print(f"  stroke available {P.Z_MAX - P.Z_MIN:.0f}, needed"
          f" {need_hi - need_lo:.0f}")
    print()
    print("RESULT:", "PASS" if ok_bottom and ok_reach else "FAIL")
    return 0 if ok_bottom and ok_reach else 1


if __name__ == "__main__":
    sys.exit(main())
