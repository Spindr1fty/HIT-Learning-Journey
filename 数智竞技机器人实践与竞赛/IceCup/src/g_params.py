"""Single source of truth for the gripper: the stone's profile and the fork.

THE IDEA
The stone's handle is a dia 11 stem with a wider disc on top, and under that
disc there is a gap. Measured off the official drawing at 13.9 px/mm:

    base ................ y =  0.0
    widest band, dia 47 .. y = 11.0
    body top (shoulder) .. y = 23.7
    stem exposed, dia 11 . y = 23.7 .. 29.1     <- the drawing's labelled 5 mm
    handle disc .......... y = 29.1 .. 32.0     dia measured at 21.6

So the disc overhangs the stem by 5.3 mm and sits 5.4 mm above the body. A tine
thinner than 5.4 mm, sliding in beside the stem, gets under the disc and the
whole 70 g stone hangs off it. No magnet, no friction grip, no actuator: the
chassis drives forward to insert and reverses to release.

WHAT IS MEASURED AND WHAT IS ASSUMED
  STEM_Y0 / STEM_Y1 ... from the DRAWING'S OWN "5mm" dimension. Trustworthy.
  DISC_DIA ............ measured off the pixels (21.6). NOT a labelled
                        dimension, so it carries maybe +/-1 mm. Calipers please.
  everything about body taper ... eyeballed from the drawing. Only used to
                        check the tine clears the shoulder, so it does not need
                        to be exact.
"""

from math import pi

# --- stone, as drawn -------------------------------------------------------
# Caliper measurements 2026-10-17 replaced the pixel estimates:
#   handle disc dia 18.0  (I had guessed 21.6 -- 3.6 too big)
#   gap under the disc 7.5 (I had guessed 5.4 -- the tines can be much thicker)
#
# The official drawing labels 5 mm near the stem, but the caliper says the gap
# is 7.5. Trust the caliper; the drawing's 5 may measure something else.
STONE_H = 32.0
STONE_DIA = 47.0
STONE_WIDEST_Y = 11.0
STEM_DIA = 9.70         # MEASURED 2026-10-17 (was 11.0 by guess)
DISC_DIA = 18.0          # MEASURED
GAP_UNDER_DISC = 7.5     # MEASURED
DISC_THICK = 2.36        # MEASURED (was 2.9, derived)         # off the drawing, and 32 - 29.1 matches it
STEM_Y1 = STONE_H - DISC_THICK          # 29.1, the disc's underside
BODY_TOP_Y = STEM_Y1 - GAP_UNDER_DISC   # 21.6, where the stem flares out
DISC_BOT_Y = STEM_Y1
FLARE_H = 1.0            # MEASURED: the collar at the stem root is 1 mm tall
FLARE_D = 15.5           # MEASURED: that collar's diameter (was 22 by guess)

# The stone's outline as (radius, height) from the axis, bottom to top. This is
# a reference solid: it exists so the fork can be proved non-interfering, and
# it is never printed.
STONE_PROFILE = (
    (0.0, 0.0),
    (20.0, 0.0),
    (22.8, 1.5),
    (23.5, 4.0),
    (23.5, 11.0),
    (23.2, 13.5),
    (22.0, 17.0),
    (18.0, 19.5),
    (FLARE_D / 2, BODY_TOP_Y),
    (8.0, BODY_TOP_Y + FLARE_H * 0.5),
    (STEM_DIA / 2, BODY_TOP_Y + FLARE_H),
    (STEM_DIA / 2, STEM_Y1),
    (DISC_DIA / 2, STEM_Y1),
    (DISC_DIA / 2, STONE_H),
    (0.0, STONE_H),
)

# --- fork ------------------------------------------------------------------
# The stem is NOT a straight dia 11 cylinder: it flares into the body between
# BODY_TOP_Y and BODY_TOP_Y+FLARE_H, reaching dia 22 at the bottom. A tine sized
# off the "dia 11" number fouls that flare. So the tines ride ABOVE the flare
# and their inner edges clear it.
#
# The disc is only dia 18 now (measured), so its radius is 9.0 and the tine has
# to live between the flare and the rim -- a 3.5 mm wide corridor, not the
# 5.3 mm the pixel estimate implied.
TINE_THICK = 3.5         # vertical; the 7.5 mm gap finally allows a stiff tine
TINE_W = 3.0             # lateral width, inside the disc's dia 18 rim
TINE_Y = 7.2             # lateral centre; set so the inner face clears the
TINE_LEN = 47.0          # reach past the block face
TINE_TIP_RAMP = 8.0      # length of the 45-degree wedge on the tip
TINE_LIP = 1.5           # upturn at the tip so the disc cannot slide off
TINE_LIP_LEN = 3.0

# vertical placement of the tine, measured above the body's top face
TINE_LIFT = 2.1          # underside clears the flare's top by 0.3

# derived clearances, printed by the model for eyeballing
GAP_UNDER_DISC = DISC_BOT_Y - BODY_TOP_Y          # 5.4
TINE_TOP_Y = BODY_TOP_Y + TINE_LIFT + TINE_THICK  # 27.3
CLEAR_TO_DISC = DISC_BOT_Y - TINE_TOP_Y           # 1.8
TINE_INNER_Y = TINE_Y - TINE_W / 2                # 5.7
TINE_OUTER_Y = TINE_Y + TINE_W / 2                # 8.7, 0.3 inside the disc rim
STEM_CLEAR = TINE_INNER_Y - STEM_DIA / 2          # 2.5 on the straight stem
DISC_OVERLAP = DISC_DIA / 2 - TINE_OUTER_Y        # 0.2 inside the rim
# the whole tine sits under the disc, which is what actually carries the stone
FLARE_R = FLARE_D / 2    # collar radius; the tine sits ABOVE the collar

# --- mounting --------------------------------------------------------------
FORK_BODY_X = (21.0, 31.0)   # the block that bolts to the carriage's +X face
FORK_BODY_Y = 30.0
FORK_BODY_Z = 34.0
MOUNT_HOLE_D = 4.5           # M4 CLEARANCE on the fork's side: the screw
                             # passes through the fork and bites the carriage.
                             # Do NOT drill the carriage to 4.5 -- it would
                             # spin. Carriage gets a 3.5 self-tap pilot.
MOUNT_SLOT = 20.0            # vertical slot travel, trims the pick height
MOUNT_HOLE_Y = 10.0          # +/- from the fork's centreline

# The carriage's +X face sits at +21 in the Z-axis module frame (CARR_X_OUT is
# -21 on the other side). Everything here is modelled in that same frame.
CARR_X_OUT = 21.0


def summary():
    return {
        "gap under disc": GAP_UNDER_DISC,
        "tine thickness": TINE_THICK,
        "tine top above body": TINE_TOP_Y,
        "clearance to disc": CLEAR_TO_DISC,
        "stem clearance": STEM_CLEAR,
        "disc overlap": DISC_OVERLAP,
        "tine reach": TINE_LEN,
    }
