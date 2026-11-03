"""Robot parked at its own rack in a picking pose, inside the marked venue.

The chassis stops CLEAR mm off the rack face with the blade folded; the jaws
then reach 40 mm into the cell, which lands on the stone centre when the stone
is resting against the 2 mm back wall. Head is at the middle tier.

This is a pose check, not a kinematic model: nothing here moves.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import robot as R  # noqa: E402
import spec  # noqa: E402
import venue_spec as V  # noqa: E402
from venue_scene import venue_scene  # noqa: E402

CLEAR = 5.0
MIDDLE_TIER_Z = 128.5


def robot_at_rack(rack_y: float = V.RACK_Y_CENTRES[0]) -> bd.Shape:
    body = R.robot(jaw_gap=R.JAW_OPEN, head_z=MIDDLE_TIER_Z + V.PLATFORM_HEIGHT,
                   blade_folded=True)
    body = bd.Rot(0, 0, 180) * body
    body = bd.Pos(V.RACK_FACE_X + CLEAR + R.CHASSIS / 2, rack_y, 0.0) * body
    body.label = "robot_at_rack"
    return body


def _scene() -> bd.Shape:
    return bd.Compound(children=[venue_scene(), robot_at_rack()],
                       label="robot_in_venue")


@step(out="../oldSTEP/robot_in_venue.step")
def robot_in_venue():
    return _scene()


if __name__ == "__main__":
    s = robot_in_venue()
    b = s.bounding_box()
    rb = robot_at_rack().bounding_box()
    front = V.RACK_FACE_X + CLEAR
    print(f"scene bbox {b.max.X - b.min.X:.1f} x {b.max.Y - b.min.Y:.1f}"
          f" x {b.max.Z - b.min.Z:.1f}")
    print(f"chassis front {front:.1f} (clearance {CLEAR} to rack face {V.RACK_FACE_X})")
    stone_x = ((V.RACK_FACE_X + V.RACK_BACK_X) / 2
               + spec.pocket_floor_y() + spec.STONE_DIAMETER / 2)
    print(f"jaw tip {rb.min.X:.1f}  vs stone centre {stone_x:.1f} (against back wall)")
    print(f"robot Y span {rb.min.Y:.1f}..{rb.max.Y:.1f}  (rack at "
          f"{V.RACK_Y_CENTRES[0] - 152.5:.1f}..{V.RACK_Y_CENTRES[0] + 152.5:.1f})")
