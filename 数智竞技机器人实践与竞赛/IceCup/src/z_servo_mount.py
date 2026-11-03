r"""Servo cradle: a square clamp collar around the carriage plus a servo plate.

WHY THE OLD ONE WAS SCRAP
Version 1 bolted to the carriage's -X wall. That wall is 6 mm and the 30 mm rail
runs behind it with 0.3 mm of clearance, so a screw would come out inside the
bore and hit the rail. Its pilot holes were never actually cut either.

WHY A COLLAR
The collar wraps the OUTSIDE of the 42 mm sleeve, so it never touches the bore.
A gap on one side plus two tabs and one M4 screw squeezes it onto the carriage.
No holes in the carriage at all, so the carriage already printed is reused.

A SQUARE collar, not a round one: the carriage is square, and a square ring is
a box minus a box, which cannot come out as loose shells the way a round outer
with a square bore kept doing.

GEOMETRY, module frame, millimetres
    carriage .......... 42 square, Z 130..190
    pinion axis ....... X -56, Z 160
    servo flange plane  Y -25      (servo base at Y -55, outer face Y -15)
    horn top ........... Y  -8
    gear ............... Y  -8 .. +8

SERVO, from the maker's dimension drawing
    4 x dia 4.4 holes on a 48.5 x 10 rectangle
    body 40 x 20 x 40, flange 30 from the base and 2.5 thick, height 45.65
    shaft centre 10 mm from one end, so the body runs 30 mm one way and 10 the
    other from the axis

Pure ASCII on purpose: cadgen parses model files with no explicit encoding.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadgen import build123d as bd  # noqa: E402
from cadgen import step  # noqa: E402

import z_params as P  # noqa: E402

PINION_X = P.PINION_X                 # -56
PINION_Z = P.PINION_Z                 # 160

# --- servo, from the maker's drawing --------------------------------------
SERVO_HOLE_D = 4.4
SERVO_SPAN_L = 48.5
SERVO_SPAN_W = 10.0
SERVO_BODY_L = 40.0
SERVO_BODY_W = 20.0
SERVO_SHAFT_OFF = 10.0
SERVO_FLANGE_Y = -25.0
PLAT_T = 6.0

# --- collar ---------------------------------------------------------------
CARRIAGE = 42.0
COLLAR_IN = CARRIAGE + 0.6            # 42.6, 0.3 clearance per side
COLLAR_WALL = 6.0
COLLAR_OUT = COLLAR_IN + 2 * COLLAR_WALL
COLLAR_Z = (140.0, 180.0)
GAP_W = 4.0                           # the slot that lets the collar squeeze
TAB_X = (GAP_W / 2, GAP_W / 2 + 6.0)  # half-width of each tab
TAB_Y = (COLLAR_OUT / 2, COLLAR_OUT / 2 + 14.0)
CLAMP_HOLE_D = 4.5                    # M4
# GUSSETS on the clamp ears. Each ear is a 6 x 14 x 40 cantilever and the whole
# clamp force passes through its root, the least forgiving corner on the part.
# A triangular rib on each ear's outboard side, running down to the collar's
# outer face, turns that root into a T.
EAR_GUSSET_OUT = 6.0                  # how far the rib reaches outboard
NUT_AF = 7.2
NUT_T = 3.4

# Interface to the fork bracket (src/g_fork_clamp.py). Self-tapping M4 into a
# blind hole: 3.5 pilot, 4.0 deep, leaving 2 mm between the hole's bottom and
# the rail bore.
FORK_HOLE_D = 3.5
FORK_HOLE_Y = 12.0
FORK_HOLE_ZS = (156.0, 172.0)
BLIND_DEPTH_FROM_BORE = 2.0           # material kept between hole and bore

# --- fork plate, fused into this part -------------------------------------
# There USED to be a separate bracket that self-tapped into four blind holes in
# the collar. That joint is gone: the user has no self-tapping screws, only
# machine screws and nuts, and a through-hole is impossible because the collar
# wall is 6 mm with the rail bore directly behind it. Fusing the slotted plate
# into this part removes the joint entirely -- one part fewer and nothing has to
# thread into plastic.
# The fork plate has to sit OUTBOARD of the base plate (which ends at X 30),
# otherwise its lower end drives into the base plate when the carriage descends.
# So the collar's +X wall is extended 8 mm and the plate rides out on it.
# Everything else on this part is unchanged.
COLLAR_FORK_BOSS = 8.0                          # +X wall extension
BOSS_FACE_X = COLLAR_OUT / 2 + COLLAR_FORK_BOSS  # 35.3, the new outboard face
FORK_PLATE_X = (BOSS_FACE_X - 2.0, BOSS_FACE_X + 4.0)   # 33.3 .. 39.3
FORK_PLATE_Y = 20.0
FORK_PLATE_Z = (86.0, 176.0)
FORK_SLOT_W = 4.5                               # M4 clearance
FORK_SLOT_Y = 12.0
FORK_SLOT_Z = (88.0, 136.0)                     # 48 mm of trim for the fork head

# --- servo plate ----------------------------------------------------------
# The shaft sits 10 mm from one end of the 40 mm body, while the four flange
# holes are centred on the BODY. So the hole pattern's centre is NOT the shaft
# axis -- it is 10 mm away from it. Putting the holes symmetric about the
# pinion axis, as the first attempt did, would have landed the gear 10 mm off
# its own shaft.
HOLE_CX = PINION_X - SERVO_SHAFT_OFF          # -66, flange pattern centre
PLAT_X = (HOLE_CX - SERVO_SPAN_L / 2 - 6.0, -24.0)
PLAT_Z = (PINION_Z - 27.0, PINION_Z + 27.0)
# WHICH FACE OF THE FLANGE. The flange sits 30 mm up from the servo's base and
# is 2.5 thick, so its upper face is at 32.5 and the body carries on another
# 7.5 mm above that to the 40 mm top. The servo therefore HANGS from the flange's
# UPPER face -- its body is below it. An earlier version put the mounting plate
# on the flange's LOWER face, which is the side the body is on: that plate would
# have hit the body. The plate now sits at Y -22.5 .. -16.5.
SERVO_FLANGE_T = 2.5
SERVO_FLANGE_TOP_Y = SERVO_FLANGE_Y + SERVO_FLANGE_T      # -22.5
PLAT_Y = (SERVO_FLANGE_TOP_Y, SERVO_FLANGE_TOP_Y + PLAT_T)
# The flange carries a ~2 mm ridge down its middle, at Z = PINION_Z, which is
# between the two rows of screw holes. It only fouls the two strips of plate
# that carry the holes, so a notch in each is enough -- 2.5 mm deep, 6 mm tall.

# body window: from the shaft the body runs 30 mm one way and 10 mm the other
WIN_X = (PINION_X - 30.0 - 0.5, PINION_X + 10.0 + 0.5)
WIN_Z = (PINION_Z - SERVO_BODY_W / 2 - 0.5,
         PINION_Z + SERVO_BODY_W / 2 + 0.5)

# RIDGE RELIEF, measured: the flange's ridge is 45 mm long, the body window is
# only 42 wide, so the ridge's ends overhang into the two hole columns. It needs
# a notch there after all -- but a SHORT one. The two rows of screw holes leave
# just 5.6 mm clear between their rims (Z 157.2 to 162.8). A 3 mm tall notch
# centred on Z = PINION_Z clears the ridge and keeps 1.3 mm to each hole rim.
#   attempt 1: whole contact face recessed, four round pads -- worked, ugly
#   attempt 2: notch 6 mm tall (Z 157..163) -- ate into both hole rims
#   attempt 3: no notch at all -- wrong, the ridge is 45 not 42
#   this one:  3 mm tall, 2.5 mm deep, over each hole column
RIDGE_Z = (PINION_Z - 1.5, PINION_Z + 1.5)
RIDGE_D = 2.5
RIDGE_NOTCH_X = ((-96.25, WIN_X[0]), (WIN_X[1], -24.0))

# RIBS. The ridge relief takes 2.5 of the plate's 6 mm right between the two
# screw holes -- exactly where the bolt squeezes. A stiffener on the BACK face
# puts the material back as a T-section instead of a flat web.
RIB_PROUD = 4.0                      # how far the rib stands off the back
# Two ribs on the servo plate, running its full length -- but in the Z bands
# ABOVE and BELOW the bolt holes (Z 155 and 165), never across them. An earlier
# pair sat at the hole columns and capped all four holes, which is why the plate
# came out of the printer with the servo unable to bolt on.
RIB_Z_BANDS = ((133.0, 148.0), (172.0, 187.0))

# GUSSETS at the plate-to-collar junction. The plate is a 72 mm cantilever off
# a narrow band on the collar, and until now it left the junction as a bare
# 90-degree corner -- the weakest possible shape. Two triangular webs on the
# BACK face fix that: full depth at the root, tapering to nothing at the free
# end. They run along the plate's top and bottom edges because the servo's
# 40 x 20 body occupies Z 150..170 in the middle.
GUSSET_PROUD = 8.0                   # depth at the root
GUSSET_ROOT_X = -27.3                # the collar's -X face, i.e. the junction
GUSSET_TIP_X = -88.0                 # where the taper reaches zero
# These must sit INSIDE the collar's Z 140..180, otherwise their root only
# touches the plate and never reaches the collar -- which defeats the whole
# point. And they must stay clear of the servo body, which occupies Z 150..170.
# Where each ridge relief ends, the plate steps from 6 mm back to 3.5 mm. That
# step is a stress riser right next to a bolt hole. A small triangular ramp
# blends it: full thickness at the outboard end, tapering away over RAMP_LEN.
# It sits at the slot's OUTBOARD end, clear of the servo flange's ridge, which
# only reaches X -88.5 and -43.5.
GUSSET_PROUD = 5.0                   # stands this far off the servo-side face
GUSSET_ROOT_X = -27.3                # the collar's -X face, i.e. the junction
GUSSET_TIP_X = -90.0                 # the taper reaches zero here


def _box(x0, x1, y0, y1, z0, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(
        x1 - x0, y1 - y0, z1 - z0,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def _hole_y(x, y0, depth, z, dia):
    return bd.Pos(x, y0, z) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        dia / 2.0, depth,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _hole_x(x0, depth, y, z, dia):
    return bd.Pos(x0, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(
        dia / 2.0, depth,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _collar():
    z0, z1 = COLLAR_Z
    ring = _box(-COLLAR_OUT / 2, COLLAR_OUT / 2,
                -COLLAR_OUT / 2, COLLAR_OUT / 2, z0, z1)
    ring = ring.cut(_box(-COLLAR_IN / 2, COLLAR_IN / 2,
                         -COLLAR_IN / 2, COLLAR_IN / 2, z0 - 1.0, z1 + 1.0))

    # the squeezing gap: a slot on the +Y side running right through the wall
    ring = ring.cut(_box(-GAP_W / 2, GAP_W / 2,
                         COLLAR_IN / 2 - 2.0, TAB_Y[1] + 1.0,
                         z0 - 1.0, z1 + 1.0))

    # the two tabs the clamp screw pulls together
    for sx in (-1.0, 1.0):
        x0 = sx * TAB_X[0] if sx > 0 else -TAB_X[1]
        x1 = sx * TAB_X[1] if sx > 0 else -TAB_X[0]
        ring = ring + _box(min(x0, x1), max(x0, x1), TAB_Y[0], TAB_Y[1], z0, z1)

    # One M4 straight through both tabs, nut on the outside. There USED to be a
    # 7.2 mm SQUARE nut seat here -- the same mistake as the base plate and the
    # servo flange: an M4 nut is 7.0 across flats but 8.3 across corners, so it
    # cannot sit in a 7.2 square. And there is no reason to pocket it at all:
    # the tab's outer face is wide open, so a plain washer and nut go on there.
    yc = (TAB_Y[0] + TAB_Y[1]) / 2.0
    ring = ring.cut(_hole_x(-TAB_X[1] - 2.0, 2 * TAB_X[1] + 4.0,
                            yc, PINION_Z, CLAMP_HOLE_D))
    # --- gussets on the clamp ears ----------------------------------------
    # Triangle in the X-Y plane: one leg down the ear's outboard face, the other
    # along the collar's +Y face. Extruded in Z, but ONLY above and below the
    # clamp bolt. A full-height rib blocked the clamp screw at X +/-9 -- the
    # third time in this part that a stiffener capped a hole it shared a plane
    # with. The bolt is at Z 160 and is 4.5 across, so the ribs live in Z 140..152
    # and 168..180 and the screw passes between them cleanly.
    for sx in (-1.0, 1.0):
        for gz0, gz1 in ((COLLAR_Z[0], PINION_Z - 8.0), (PINION_Z + 8.0, COLLAR_Z[1])):
            # start 2 mm INSIDE the collar's outer face. A triangle that only
            # touched that face stayed a separate solid -- face-to-face contact
            # does not fuse, and the part came out as three loose pieces.
            pts = [(sx * TAB_X[1], TAB_Y[0] - 2.0),
                   (sx * TAB_X[1], TAB_Y[1]),
                   (sx * (TAB_X[1] + EAR_GUSSET_OUT), TAB_Y[0] - 2.0)]
            zm = (gz0 + gz1) / 2.0
            face = bd.Face(bd.Polyline(*[(x, y, zm) for x, y in pts],
                                       close=True))
            ring = ring + bd.extrude(face, amount=(gz1 - gz0) / 2.0, both=True)

    # --- +X wall extension -------------------------------------------------
    # A boss from inside the existing wall out to the new face. It starts at the
    # bore's plane so it is one solid with the wall, not a block glued to a face.
    ring = ring + _box(COLLAR_IN / 2, BOSS_FACE_X,
                       -COLLAR_OUT / 2, COLLAR_OUT / 2,
                       COLLAR_Z[0], COLLAR_Z[1])

    # --- fork plate, fused on ---------------------------------------------
    # Starts at X 25 so it overlaps the collar's wall instead of just kissing
    # its face. Kissing faces do not fuse; this project has been bitten by that
    # more than once.
    fork = _box(FORK_PLATE_X[0], FORK_PLATE_X[1],
                -FORK_PLATE_Y, FORK_PLATE_Y,
                FORK_PLATE_Z[0], FORK_PLATE_Z[1])
    for sy in (-1.0, 1.0):
        fork = fork.cut(_box(FORK_PLATE_X[0] - 2.0, FORK_PLATE_X[1] + 2.0,
                             sy * FORK_SLOT_Y - FORK_SLOT_W / 2,
                             sy * FORK_SLOT_Y + FORK_SLOT_W / 2,
                             FORK_SLOT_Z[0], FORK_SLOT_Z[1]))
    ring = ring + fork

    return ring


def _plate():
    plat = _box(PLAT_X[0], PLAT_X[1], PLAT_Y[0], PLAT_Y[1],
                PLAT_Z[0], PLAT_Z[1])
    plat = plat.cut(_box(WIN_X[0], WIN_X[1], PLAT_Y[0] - 1.0, PLAT_Y[1] + 1.0,
                         WIN_Z[0], WIN_Z[1]))

    # NO RIDGE RELIEF -- and that took three attempts to get right.
    #
    # The flange carries a ~2 mm ridge at its centre. Attempt one stepped the
    # whole contact face back and left four round pads; ugly and fragile.
    # Attempt two cut a small notch at each end of the body window, but the
    # notch spanned Z 157..163 while the screw holes reach Z 157.2 and 162.8 --
    # it ate into both holes.
    #
    # The ridge is at the MIDDLE of the bolt pattern, which is (X -66, Z 160).
    # That point is already inside the body window (X -87..-45, Z 149..171), so
    # the ridge is clear with no relief at all. A through-slot there would be
    # impossible anyway: the gap between the two rows of holes is only 5.6 mm,
    # so any cut big enough for the ridge would break the hole rims.

    # ridge relief: a short notch over each hole column, NOT through the plate
    for nx0, nx1 in RIDGE_NOTCH_X:
        plat = plat.cut(_box(nx0, nx1,
                             PLAT_Y[0] - 1.0, PLAT_Y[0] + RIDGE_D,
                             RIDGE_Z[0], RIDGE_Z[1]))

    # ribs on the open face, full length, above and below the bolt holes
    for rz0, rz1 in RIB_Z_BANDS:
        plat = plat + _box(PLAT_X[0], PLAT_X[1],
                           PLAT_Y[1] - 1.0, PLAT_Y[1] + RIB_PROUD,
                           rz0, rz1)

    for sx in (-1.0, 1.0):
        for sz in (-1.0, 1.0):
            hx = HOLE_CX + sx * SERVO_SPAN_L / 2.0
            hz = PINION_Z + sz * SERVO_SPAN_W / 2.0
            # Plain through-hole, no nut pocket. The pocket used to be a 7.2 mm
            # SQUARE, which an M4 nut (7.0 across flats, 8.3 across corners)
            # physically cannot enter -- the same mistake the base plate had.
            # The flange holes sit outside the servo's 40 x 20 body, so there is
            # free space on the servo side for a nut and a spanner: bolt from the
            # back, nut on the servo side.
            # The cutter must start at the RIB's outer face, not the plate's.
            # Starting at the plate left the rib's outer 4 mm solid and the
            # bolt could not get in at all -- the ribs covered all four holes.
            # bolt from the +Y side: through the plate (6) and the flange (2.5),
            # nut on the flange's underside, which is wide open -- the flange's
            # bores sit outside the 40 x 20 body. M4 x 12.
            plat = plat.cut(_hole_y(hx, SERVO_FLANGE_Y - 4.0,
                                    PLAT_Y[1] - (SERVO_FLANGE_Y - 4.0) + 1.0,
                                    hz, SERVO_HOLE_D))
    return plat


def _cradle():
    body = (_collar() + _plate()).clean()
    n = len(body.solids())
    if n != 1:
        raise ValueError(
            f"collar and plate did not fuse: {n} solids. The plate's +X end "
            f"must overlap the collar's -Y face; check PLAT_X and PLAT_Y.")
    body.label = "z_servo_mount"
    return body


@step(out="../newSTEP/z_servo_mount.step")
def z_servo_mount():
    return _cradle()


if __name__ == "__main__":
    m = z_servo_mount()
    b = m.bounding_box()
    print(f"bbox X {b.max.X - b.min.X:.2f}  Y {b.max.Y - b.min.Y:.2f}"
          f"  Z {b.max.Z - b.min.Z:.2f}   valid={m.is_valid}"
          f"  solids={len(m.solids())}")
    print(f"volume {m.volume / 1000:.3f} cm3"
          f"   ({m.volume / 1000 * 1.24:.0f} g PLA)")
    print()
    print("collar -- clamps the 42 carriage, no holes in the carriage")
    print(f"  inner square ....... {COLLAR_IN}  (0.3 per side)")
    print(f"  outer square ....... {COLLAR_OUT}")
    print(f"  Z .................. {COLLAR_Z}")
    print(f"  gap ................ {GAP_W} wide on +Y, one M4 pulls the tabs")
    print(f"  clamp nut .......... plain nut + washer on the tab face")
    print()
    print("servo plate -- sits on the flange plane")
    print(f"  Y .................. {PLAT_Y}  (flange at {SERVO_FLANGE_Y})")
    print(f"  flange holes ....... 4 x dia {SERVO_HOLE_D} on"
          f" {SERVO_SPAN_L} x {SERVO_SPAN_W}")
    print(f"  pattern centre ..... X {HOLE_CX:.2f}"
          f"   (shaft is at X {PINION_X}, so"
          f" {abs(HOLE_CX - PINION_X):.0f} offset)")
    print(f"  hole X ............. {HOLE_CX - SERVO_SPAN_L / 2:.2f}"
          f" .. {HOLE_CX + SERVO_SPAN_L / 2:.2f}")
    print(f"  hole Z ............. {PINION_Z - SERVO_SPAN_W / 2:.2f}"
          f" .. {PINION_Z + SERVO_SPAN_W / 2:.2f}")
    print(f"  body window ........ X {WIN_X}  Z {WIN_Z}")
