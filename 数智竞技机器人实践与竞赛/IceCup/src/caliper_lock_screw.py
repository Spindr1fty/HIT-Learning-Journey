from __future__ import annotations

from cadgen import build123d as bd
from cadgen import step, stl

# Replacement thumb screw for a vernier caliper lock.
# User measured the lost screw: shank dia 2.0, head dia 7.0 -> M2 x 0.4.
# Printed plastic threads wear; field fix only. Major dia is undersized
# so the plastic thread can enter a metal M2 hole.

PITCH = 0.4
MAJOR = 1.92
ROOT_R = 0.82
THREAD_LEN = 5.5
HEAD_D = 7.0
HEAD_H = 2.2
NECK_D = 1.7
NECK_H = 0.25
FLUTES = 10
FLUTE_R = 0.32
CHAMFER = 0.2


def _thread_part() -> bd.Solid:
    z0 = -NECK_H
    z_lo = z0 - THREAD_LEN
    core = bd.Cylinder(ROOT_R, THREAD_LEN).moved(bd.Pos(0, 0, z0 - THREAD_LEN / 2))

    helix = bd.Helix(
        pitch=PITCH,
        height=THREAD_LEN - 2 * CHAMFER,
        radius=ROOT_R,
        center=(0, 0, z_lo + CHAMFER),
    )
    # Rounded ridge (pipe along helix). Frenet frame keeps it on the path.
    thread_h = MAJOR / 2 - ROOT_R
    prof = bd.Circle(radius=thread_h * 0.72).moved(bd.Pos(ROOT_R, 0, z_lo + CHAMFER))
    ridge = bd.sweep(prof, path=helix, is_frenet=True)

    clip = bd.Cylinder(MAJOR / 2 + 0.05, THREAD_LEN).moved(bd.Pos(0, 0, z0 - THREAD_LEN / 2))
    body = core.fuse(ridge)
    body = body.intersect(clip)[0]

    sink = bd.Cone(bottom_radius=MAJOR / 2 + 0.12, top_radius=ROOT_R - 0.18, height=0.5)
    sink = sink.moved(bd.Pos(0, 0, z_lo + 0.1))
    return body.cut(sink)


def caliper_lock_screw() -> bd.Solid:
    head = bd.Cylinder(HEAD_D / 2, HEAD_H)
    rim = list(head.edges().sort_by(bd.Axis.Z))
    head = head.chamfer(CHAMFER, CHAMFER, [rim[0], rim[-1]])

    cutters = []
    for i in range(FLUTES):
        ang = 360.0 * i / FLUTES
        loc = bd.Pos(HEAD_D / 2, 0, HEAD_H / 2) * bd.Rot(Z=ang)
        cutters.append(bd.Cylinder(FLUTE_R, HEAD_H + 2).moved(loc))
    fluted = head.cut(*cutters)
    if not isinstance(fluted, bd.Solid):
        fluted = list(fluted.solids())[0]

    neck = bd.Cylinder(NECK_D / 2, NECK_H).moved(bd.Pos(0, 0, -NECK_H / 2))
    thread = _thread_part()

    solid = fluted.fuse(neck).fuse(thread)
    solid.label = "caliper_lock_screw"
    return solid


@step(out="../printSTEP/caliper_lock_screw.step")
@stl(out="../printSTEP/caliper_lock_screw.stl", mesh_tolerance=6e-3)
def caliper_lock_screw_model():
    return caliper_lock_screw()


if __name__ == "__main__":
    caliper_lock_screw_model()
