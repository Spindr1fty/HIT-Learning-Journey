"""What the venue geometry demands of the picker.

Works out, in venue coordinates, where all nine stones of each rack actually
are, then checks those against the 350 mm robot footprint and the field edge.

Run:  python checks/pick_envelope.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import spec  # noqa: E402
import venue_spec as V  # noqa: E402

RACK_CENTRE_X = (V.RACK_FACE_X + V.RACK_BACK_X) / 2
LOCAL_XS = spec.cell_centers(spec.RACK_WIDTH, centered=True)
LOCAL_ZS = [lo for lo, _ in spec.cell_spans(spec.RACK_HEIGHT, centered=False)]
TIER = ("low", "mid", "top")

STONE_X = RACK_CENTRE_X + spec.pocket_floor_y() + spec.STONE_DIAMETER / 2
PLAY = spec.pocket_play()


def positions(y_centre):
    """(label, X, Y, Z) of every stone centre in the venue frame, all 9 cells."""
    return [
        (f"{TIER[row]}-col{col + 1}", STONE_X, y_centre - lx,
         floor + spec.STONE_HEIGHT / 2)
        for row, floor in enumerate(LOCAL_ZS)
        for col, lx in enumerate(LOCAL_XS)
    ]


def main():
    print("=== stone centres in venue frame ===")
    print(f"rack face X={V.RACK_FACE_X}   stone centre X={STONE_X:.1f} (against back"
          f" wall) .. {STONE_X + PLAY:.1f} (against front)   fore/aft play {PLAY} mm")
    half = spec.ROBOT_FOOTPRINT / 2
    for y_centre in V.RACK_Y_CENTRES:
        print(f"\n  rack at Y={y_centre:+.0f}:")
        for label, _, y, z in positions(y_centre):
            over = abs(y) + half - V.FIELD_HALF_WIDTH
            print(f"    {label:10} Y={y:8.2f}  Z={z:7.2f}"
                  + (f"   << body overhangs edge by {over:.1f} mm" if over > 0 else ""))

    z_all = [z for y in V.RACK_Y_CENTRES for _, _, _, z in positions(y)]
    z_top = max(z + spec.STONE_HEIGHT / 2 for z in z_all)
    cols = sorted({round(abs(y), 2) for _, _, y, _ in positions(V.RACK_Y_CENTRES[0])})

    print("\n=== mechanism travel demanded ===")
    print(f"Z  stone centre {min(z_all):.2f} .. {max(z_all):.2f},"
          f"  stone top max {z_top:.2f}")
    print(f"   lift stroke {z_top - min(z_all):.1f} mm"
          f"  (+ same again per mm of platform height, now {V.PLATFORM_HEIGHT})")
    print(f"Y  outer {cols[-1]:.2f} / middle {cols[1]:.2f} / inner {cols[0]:.2f},"
          f"  column pitch {cols[1] - cols[0]:.2f} mm")
    print(f"X  gripper must reach past the rack face by "
          f"{V.RACK_FACE_X - (STONE_X + PLAY):.1f} .. "
          f"{V.RACK_FACE_X - STONE_X:.1f} mm")

    side = (spec.CELL_SIZE - spec.STONE_DIAMETER) / 2
    side_meas = (spec.CELL_SIZE - spec.STONE_DIAMETER_MEASURED) / 2
    head = spec.CELL_SIZE - spec.STONE_HEIGHT
    print("\n=== will a gripper fit the cell opening ===")
    print(f"rack grid: wall {spec.wall_thickness():.2f} mm,"
          f" column pitch {spec.CELL_SIZE + spec.wall_thickness():.2f} mm")
    print(f"opening {spec.CELL_SIZE} x {spec.CELL_SIZE}, stone"
          f" Ø{spec.STONE_DIAMETER} x {spec.STONE_HEIGHT}")
    print(f"   per-side clearance {side:.1f} mm nominal"
          f"  ({side_meas:.1f} mm against the measured Ø46 stone)")
    print(f"   headroom above stone {head:.1f} mm -> gripper body can sit over the"
          f" stone and drop its fingers {spec.STONE_HEIGHT} mm")

    print("\n=== can the chassis centre itself on each column ===")
    found = False
    for y_centre in V.RACK_Y_CENTRES:
        for label, _, y, _ in positions(y_centre):
            over = abs(y) + half - V.FIELD_HALF_WIDTH
            if over > 0:
                found = True
                print(f"   {label} at Y={y:.2f}: centring the {spec.ROBOT_FOOTPRINT:.0f}"
                      f" mm body there puts it {over:.1f} mm past the field edge"
                      f" (|Y|<={V.FIELD_HALF_WIDTH}, no wall)")
    if not found:
        print("   every column is reachable without the body leaving the field")

    print("\n=== pusher contact height (three sources disagree) ===")
    band = [spec.IMPACT_HEIGHT_MEASURED, spec.IMPACT_HEIGHT_FROM_DRAWING,
            spec.IMPACT_HEIGHT]
    print(f"   measured {band[0]:.2f} / from drawing {band[1]:.2f}"
          f" / rules page {band[2]:.1f}   spread {max(band) - min(band):.2f} mm")
    print(f"   -> design the blade for {min(band) - 0.5:.1f} .. {max(band) + 0.5:.1f} mm"
          f" of adjustment, and make it narrower than the"
          f" {spec.BELT_THICKNESS_MEASURED:.1f} mm measured belt")
    print(f"   robot footprint {spec.ROBOT_FOOTPRINT:.0f} mm across a"
          f" {V.FIELD_HALF_WIDTH * 2:.0f} mm field"
          f" = {spec.ROBOT_FOOTPRINT / (2 * V.FIELD_HALF_WIDTH):.0%} of the width")


if __name__ == "__main__":
    main()
