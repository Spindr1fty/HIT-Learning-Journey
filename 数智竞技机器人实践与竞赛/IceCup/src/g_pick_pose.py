"""Pick pose: the fork with the stone caught on its tines.

Reference only -- the stone is not a printed part. Load this to see whether the
tines really do end up under the handle disc, and use it as the picture that
explains the gripper to anyone who has not read the notes.

Coordinates are the fork's own frame: the tine's underside is Z=0, the mounting
block sits at X 0..10. The stone's axis is placed at the position it reaches
when its body stops against the block -- that stop is what makes the pick
repeatable, so the stone's X is a derived number, not a free choice.

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import g_params as G  # noqa: E402
from g_fork import BLOCK_X, _fork  # noqa: E402
from g_stone import _stone  # noqa: E402

# the stone's base sits this far below the tine plane
STONE_Z = -(G.BODY_TOP_Y + G.TINE_LIFT)
# the body is dia 47, and it is the body -- not the disc -- that reaches the
# block first, so this is where the stone's axis ends up
BODY_R = max(r for r, z in G.STONE_PROFILE)
STONE_X = BLOCK_X[1] + BODY_R


def _assembly():
    fork = _fork()
    fork.label = "g_fork"

    stone = bd.Pos(STONE_X, 0.0, STONE_Z) * _stone()
    stone.label = "g_stone_reference"

    combo = bd.Compound(children=[fork, stone])
    combo.label = "g_pick_pose"
    return combo


@step(out="../newSTEP/g_pick_pose.step")
def g_pick_pose():
    return _assembly()


if __name__ == "__main__":
    # Call the DECORATED function. Calling _assembly() builds the same geometry
    # and silently skips writing the STEP -- the exact trap documented in
    # z_assembly.py, walked into again.
    a = g_pick_pose()
    b = a.bounding_box()
    print("pick pose -- the stone is a REFERENCE body, not a printed part")
    print(f"solids {len(a.solids())}   valid={a.is_valid}")
    print(f"stone axis at X {STONE_X:.2f}, base at Z {STONE_Z:.2f}")
    print(f"bbox X {b.max.X - b.min.X:.1f}  Y {b.max.Y - b.min.Y:.1f}"
          f"  Z {b.max.Z - b.min.Z:.1f}")
    print()
    print("what the picture should show")
    print(f"  tines pass {G.STEM_CLEAR:.1f} mm either side of the stem")
    print(f"  tines sit under the disc, {G.CLEAR_TO_DISC:.2f} mm below it")
    print(f"  the disc overhangs the tines by "
          f"{G.DISC_OVERLAP:.2f} mm at the outer edge")
    print(f"  the stone's body touches the block at X {BLOCK_X[1]:.0f}")
    print()
    print("NOTE the tines are 47 mm cantilevers about 2.5 x 2.6 mm in section,")
    print("so they sag roughly 0.8 mm under the stone. That sag is elastic and")
    print("repeatable, and it only appears AFTER the disc is caught, so it")
    print("affects the lift height but never the insertion clearance.")
