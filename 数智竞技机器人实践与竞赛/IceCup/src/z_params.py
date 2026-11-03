"""Shared parameters for the Z-axis module (rack + pinion + printed guide).

Everything is derived from a handful of numbers below. Change MODULE or
PINION_TEETH and every part follows -- the rack length, the centre distance
and the carriage travel all recompute.

Layout, in the module's own frame (Z is up, the arm reaches toward -X):

    rack(fixed) | pinion | arm | carriage | rail(fixed)
      X<-91       -61           0        +15

Y is the pinion's axis. The arm and the pinion share one axle but sit at
different Y, which is what keeps the arm clear of the rack.
"""

from math import cos, pi, radians, sqrt, tan

# ---------------------------------------------------------------- gear train
MODULE = 2.0                 # tooth size; FDM-friendly at 0.4 mm nozzle
PINION_TEETH = 18            # 18 teeth -> pitch dia 36, 113 mm per revolution
PRESSURE_ANGLE = 20.0        # degrees, standard

PITCH_R = MODULE * PINION_TEETH / 2.0                     # 18.000
TIP_R = PITCH_R + MODULE                                  # 20.000
ROOT_R = PITCH_R - 1.25 * MODULE                          # 15.500
BASE_R = PITCH_R * cos(radians(PRESSURE_ANGLE))           # 16.914
CIRCULAR_PITCH = pi * MODULE                              # 6.2832
PER_REV = 2 * pi * PITCH_R                                # 113.097 mm travel/rev

# ---------------------------------------------------------------- travel
STROKE = 195          # = Z_MAX - Z_MIN; the fork only needs 172
CARRIAGE_LEN = 60.0          # bearing length; >= 2x the rail width
RAIL_W = 30.0                # rail cross-section, square
RAIL_LEN = 320.0             # >= STROKE + CARRIAGE_LEN + margins
RACK_TEETH = 51              # 51 * 6.2832 = 320.4 mm: covers the whole
                             # 80..275 travel (old 40 left 44 mm toothless)
RACK_LEN = 320.0      # == RAIL_LEN, so the two uprights are flush.
                      # 51 teeth x 6.2832 = 320.44 would stand 0.44 proud;
                      # the top tooth's root ends at Z 319.4, so the trim is free.

# The carriage runs Z_MIN..Z_MAX (its centre). Bottom and top leave the
# carriage fully on the rail.
Z_MIN = 80.0          # raised from 45. The fork plate hangs 74 mm below the pinion centre, so the old bottom stop drove it 29 mm into the 8 mm base plate. Carriage bottom is then at Z 50 and the plate clears by 6 mm.
Z_MAX = Z_MIN + STROKE                          # 275.0
# Why 15 and not 5: the base plate's top face is Z=0 and the rail's foot sits
# ON it, 8 mm tall. The carriage must clear that foot at the bottom of travel.

# Every part is modelled in this one module frame, so importing all the STEPs
# into one viewer shows the assembled fit. Origin: rail axis, Z=0 at the top of
# the foot at Z=0. The park pose is FIXED at 160, NOT the middle of the stroke:
# every part is modelled in this frame, so tying it to (Z_MIN+Z_MAX)/2 meant that
# raising the bottom stop moved the whole module 17.5 mm and silently broke the
# assembly's absolute placements. 160 sits inside the 80..275 travel.
Z_COMMISSION = 160.0
PINION_Z = Z_COMMISSION
CARRIAGE_Z0 = Z_COMMISSION - CARRIAGE_LEN / 2.0  # 130.0, carriage local Z=0

# ---------------------------------------------------------------- clearances
SLIDE_CLEAR = 0.30           # per side, carriage bore vs rail (FDM measured)
BACKLASH = 0.30              # total circumferential play across the pair
                             # (0.15 per flank each). Zero-backlash teeth
                             # bind on a printed pair; 0.3 is the usual trim.
WALL = 6.0                   # carriage wall thickness
ARM_Y = (8.0, 20.0)          # arm sits beside the pinion on the +Y side
GEAR_Y = (-8.0, 8.0)         # pinion and rack width, 16 mm
GEAR_W = GEAR_Y[1] - GEAR_Y[0]
SHAFT_D = 5.9                # matches the servo output spline from Motor.dxf

# X stations. CARR_X_OUT is the carriage's outer face; the arm bridges from
# there to the pinion axle. The gap keeps the servo body clear of the carriage.
CARR_X_OUT = -(RAIL_W / 2 + WALL)                 # -21.0
ARM_LEN = 35.0                                    # -21 -> -56
PINION_X = CARR_X_OUT - ARM_LEN                   # -56.0  (arm end / axle)
RACK_PITCH_X = PINION_X - PITCH_R                 # -74.0  (rack pitch line)
RACK_BODY_X = (RACK_PITCH_X - 2.5 - 20.0, RACK_PITCH_X - 2.5)  # -96.5 .. -76.5

# Clearance audit, all with Y kept in mind:
#   pinion spans X -74..-38   carriage spans -21..21   -> 17 mm gap
#   servo  spans X -76.4..-35.6                       -> 14.6 mm gap to carriage
#   rack   sits at Y -8..8, servo at Y -29.7..-10     -> no Y overlap

# ---------------------------------------------------------------- servo body
SERVO_L = 40.7               # across the mounting flanges
SERVO_W = 19.7               # thickness
SERVO_H = 42.9               # along the output shaft
# Y of the body's shaft-side face. The gear's -Y face is at GEAR_Y[0] = -8, so
# this leaves 7 mm for the servo horn and a washer between body and gear.
SERVO_FACE_Y = -15.0
SERVO_Y = (SERVO_FACE_Y - SERVO_W, SERVO_FACE_Y)     # -34.7 .. -15.0
HORN_GAP = GEAR_Y[0] - SERVO_FACE_Y                  # 7.0 mm available


def involute_half_angle(r: float) -> float:
    """Half angular width of a tooth at radius r, for this gear.

    Reduced by half the backlash so the pair has running clearance. The trim is
    applied as a constant angular subtraction, which thins both flanks evenly.
    """
    a_pitch = radians(PRESSURE_ANGLE)
    inv_pitch = tan(a_pitch) - a_pitch
    trim = (BACKLASH / 2.0) / PITCH_R
    if r <= BASE_R:
        return pi / (2 * PINION_TEETH) + inv_pitch - trim
    a_r = _acos_safe(BASE_R / r)
    return (pi / (2 * PINION_TEETH) + inv_pitch
            - (tan(a_r) - a_r) - trim)


def _acos_safe(v: float) -> float:
    from math import acos
    return acos(max(-1.0, min(1.0, v)))


def summary() -> str:
    c = PITCH_R + RACK_PITCH_X * -1 - PITCH_R  # centre distance placeholder
    return (
        f"module {MODULE}  teeth {PINION_TEETH}  pitch R {PITCH_R}\n"
        f"tip R {TIP_R}  root R {ROOT_R}  base R {BASE_R:.3f}\n"
        f"{PER_REV:.2f} mm per pinion revolution\n"
        f"stroke {STROKE}  rail {RAIL_W}x{RAIL_W}x{RAIL_LEN}\n"
        f"carriage centre Z {Z_MIN}..{Z_MAX}  length {CARRIAGE_LEN}\n"
        f"rack {RACK_TEETH} teeth, {RACK_LEN:.2f} mm\n"
        f"pinion X {PINION_X}  rack pitch X {RACK_PITCH_X}"
    )


if __name__ == "__main__":
    print(summary())
    print(f"meshing centre distance = {abs(RACK_PITCH_X - PINION_X):.3f} (== pitch R)")
    print(f"stroke / per-rev = {STROKE / PER_REV:.2f} pinion revolutions")
    print(f"travel speed @62rpm = {62 / 60 * PER_REV:.1f} mm/s"
          f"  -> {STROKE / (62 / 60 * PER_REV):.2f} s for the stroke")
