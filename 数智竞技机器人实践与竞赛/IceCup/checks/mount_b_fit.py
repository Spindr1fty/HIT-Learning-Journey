r"""Interface / fit check for g_mount_b against the real 20 kg servo.

Everything here is measured from the solids, not from memory.  The point is to
catch what a picture cannot show:

  * does the servo actually CONTACT the bracket where it is meant to?
  * does anything interpenetrate (i.e. would the printed part not assemble)?
  * is there room for the bolt head / nut / washer?
  * does the flange's 2 mm centre ridge fit into the 1.6 mm pocket?

Result classes:
  PASS  hard geometry, must be true
  FAIL  hard geometry is wrong -- the part cannot assemble as drawn
  WARN  a design risk that needs the user to decide, not a fact error

Run:
  uvx --no-config --python 3.13 --from "cadgen==0.7.21" python mount_b_fit.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cadgen import build123d as bd  # noqa: E402

import g_mount_b as M  # noqa: E402
import g_servo as S  # noqa: E402

TOL = 0.005

# --- measured hardware, from PROGRESS.md 10.2 / 12.1 -------------------------
HEAD_AC = 8.1        # M4 socket head across corners
WASHER_D = 9.0
BOLT_LEN = 16.0      # candidate M4x16
NUT_H = 3.2
WASHER_T = 1.5
RIDGE_H = 2.0        # flange centre ridge, user-measured 2 mm
RIDGE_W = 2.0        # ~2 mm wide (the pocket is 2.4)

FAILS = []
WARNS = []


def record(kind, name, detail):
    print(f"  [{kind:<4}] {name:<38} {detail}")
    if kind == "FAIL":
        FAILS.append(name)
    elif kind == "WARN":
        WARNS.append(name)


def check(name, ok, detail):
    record("PASS" if ok else "FAIL", name, detail)


def warn(name, ok, detail):
    record("PASS" if ok else "WARN", name, detail)


def vol(shape):
    try:
        return shape.volume
    except Exception:                      # empty boolean result
        return 0.0


def servo_at(x):
    return (bd.Pos(x, M.SERVO_Y, M.SERVO_Z) * M._servo_rot()
            * S.servo_solid())


def ridge_solid():
    """Flange centre ridge on the flange's UPPER surface (servo Z 32.5).
    Runs along the flange's length, 2 mm tall, 2 mm wide.  It is given nearly
    the full 48.5 span on purpose: the ridge has to cross the two 4 mm wide
    post contact patches, which is where the pocket has to clear it."""
    length = S.FLANGE_SPAN - 2.0
    return bd.Pos(S.BODY_X / 2.0 - length / 2.0, 0.0, S.FLANGE_Z1) * bd.Box(
        length, RIDGE_W, RIDGE_H,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN))


def main():
    part = M.bracket()
    plate = M._box(0.0, 60.0, 0.0, M.PLATE_W, 0.0, M.PLATE_T)
    servo = servo_at(M.SERVO_X)
    ridge = (bd.Pos(M.SERVO_X, M.SERVO_Y, M.SERVO_Z) * M._servo_rot()
             * ridge_solid())

    print("g_mount_b interface report\n")

    # ---- 1. placement --------------------------------------------------
    sx = M.SERVO_X
    flange_upper_x = sx - S.FLANGE_Z1
    flange_lower_x = sx - S.FLANGE_Z0
    post_face = M.POST_X[1]
    print("1. Servo placement  (flange UPPER face is the mounting face)")
    print(f"   SERVO_X                    {sx:.2f}")
    print(f"   flange upper face  X =     {flange_upper_x:.2f}"
          f"   (post inner face X = {post_face:.2f})")
    print(f"   flange lower face  X =     {flange_lower_x:.2f}")
    check("flange sits on the posts", abs(flange_upper_x - post_face) < TOL,
          f"gap {flange_upper_x - post_face:+.3f} mm")
    bb = servo.bounding_box()
    print(f"   servo solid       X {bb.min.X:.2f}..{bb.max.X:.2f}"
          f"  Y {bb.min.Y:.2f}..{bb.max.Y:.2f}"
          f"  Z {bb.min.Z:.2f}..{bb.max.Z:.2f}")

    # ---- 2. interference ----------------------------------------------
    print("\n2. Interference (shared volume must be 0)")
    for label, a, b in (("bracket vs servo", part, servo),
                        ("bracket vs plate", part, plate),
                        ("servo  vs plate", servo, plate)):
        check(label, vol(a & b) < 0.05, f"{vol(a & b):.3f} mm^3")
    ridge_hit = vol(part & ridge)
    need = RIDGE_H + 0.2
    detail = ("clear" if ridge_hit < 0.05 else
              f"{ridge_hit:.2f} mm^3 shared: ridge {RIDGE_H} > pocket"
              f" {M.POCKET_DEPTH}, flange held {RIDGE_H - M.POCKET_DEPTH:.1f}"
              f" mm off; needs >= {need:.1f} deep")
    check("pocket clears the flange ridge", ridge_hit < 0.05, detail)

    # ---- 3. clearances -------------------------------------------------
    print("\n3. Clearances")
    body_y0 = M.SERVO_Y - S.BODY_X
    body_y1 = M.SERVO_Y
    for name, post_y in (("front", M.POST1_Y), ("rear", M.POST2_Y)):
        if name == "front":
            d = abs(body_y0 - post_y[1])
        else:
            d = abs(post_y[0] - body_y1)
        check(f"servo body to {name} post", 0.05 < d < 1.0, f"{d:.3f} mm")
    bridge_under = M.BRIDGE[4]
    body_top = M.SERVO_Z + S.BODY_Y / 2.0
    check("body top to bridge underside",
          abs(bridge_under - body_top - 1.0) < TOL,
          f"{bridge_under - body_top:.3f} mm (OPENING {M.OPENING:.0f}"
          f" - body {S.BODY_Y:.0f})")
    foot_top = M.PLATE_T + M.FOOT_T
    check("body bottom sits on the foot",
          abs((M.SERVO_Z - S.BODY_Y / 2.0) - foot_top) < TOL,
          f"body Z {M.SERVO_Z - S.BODY_Y / 2:.2f} vs foot top {foot_top:.2f}")

    # ---- 4. screws ------------------------------------------------------
    print("\n4. M4 hardware")
    grip = M.POST_T + (S.FLANGE_Z1 - S.FLANGE_Z0)      # post + flange
    tail = BOLT_LEN - grip
    print(f"   grip (post {M.POST_T:.1f} + flange"
          f" {S.FLANGE_Z1 - S.FLANGE_Z0:.1f}) = {grip:.1f} mm")
    print(f"   M4x{BOLT_LEN:.0f} leaves {tail:.1f} mm past the flange"
          f" (nut {NUT_H} + washer {WASHER_T} = {NUT_H + WASHER_T})")
    check("bolt long enough for nut + washer", tail >= NUT_H + WASHER_T + 1.0,
          f"{tail:.1f} mm")
    post_w = M.POST1_Y[1] - M.POST1_Y[0]
    margin_in = M.POST1_Y[1] - (M.POST_C1 + M.SCREW_D / 2.0)
    margin_out = (M.POST_C1 - M.SCREW_D / 2.0) - M.POST1_Y[0]
    print(f"   hole edge to post face: inner {margin_in:.2f} mm,"
          f" outer {margin_out:.2f} mm  (post {post_w:.1f} wide,"
          f" hole at the servo flange line)")
    head_r = HEAD_AC / 2.0
    washer_r = WASHER_D / 2.0
    to_body = body_y0 - M.POST_C1
    check("M4 head clears the servo body", M.POST_C1 + head_r <= body_y0,
          f"head edge {M.POST_C1 + head_r:.2f} vs body {body_y0:.2f}"
          f" ({body_y0 - M.POST_C1 - head_r:+.2f} mm)")
    max_washer = 2.0 * to_body
    print(f"   washer on the post face: room beside the servo body"
          f" {to_body:.2f} mm -> dia <= {max_washer:.1f} (M4 washers are"
          f" 8 or 9)")
    warn("washer supported by the post face",
         WASHER_D <= min(2.0 * to_body, 2.0 * (M.POST_C1 - M.POST1_Y[0])),
         f"{WASHER_D:.1f} washer vs {max_washer:.1f} limit"
         f" -> use dia 8, or no washer")
    for yc in (M.POST_C1, M.POST_C2):
        clear = min(abs(yc - body_y0), abs(yc - body_y1))
        check(f"nut at Y {yc:.2f} clears the servo body", clear > 2.5,
              f"{clear:.2f} mm to the body edge")
    print(f"   nut lands on the flange's lower face X {flange_lower_x:.2f};"
          f" nut {NUT_H} tall -> X {flange_lower_x + NUT_H:.2f}")

    # ---- 5. plate mounting ---------------------------------------------
    print("\n5. Plate mounting (2 x 4 hole rows, rev 29)")
    for hx in M.HOLE_X:
        check(f"plate hole X {hx:.2f} on the plate", 0.0 < hx < 60.0,
              "plate X 0..60 (the real tooth plate is 242.7 long)")
    rows = getattr(M, "HOLE_ROWS", (M.HOLE_Y,))
    for hy in rows:
        label = "head row" if abs(hy - M.HOLE_Y) < 1e-6 else "tail row"
        on_plate = 0.0 < hy < M.PLATE_W
        record("PASS" if on_plate else "WARN",
               f"{label} Y {hy:.2f} on the plate",
               f"plate Y 0..{M.PLATE_W:.2f}"
               + ("" if on_plate else
                  f"; lands {hy - M.PLATE_W:.1f} mm past the plate edge,"
                  f" nothing to bolt to unless another part is there"))
    cant = M.FOOT_Y[1] - M.PLATE_W
    print(f"   info: foot runs {cant:.1f} mm past the plate edge"
          f" (layout B); it only carries the 70 g servo plus handling loads")

    # ---- verdict --------------------------------------------------------
    print()
    if FAILS:
        print(f"RESULT: {len(FAILS)} hard problem(s): {', '.join(FAILS)}")
        return 1
    print(f"RESULT: hard checks PASS, {len(WARNS)} open design risk(s):"
          f" {', '.join(WARNS) if WARNS else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
