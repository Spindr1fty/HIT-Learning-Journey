r"""Part / feature map for g_mount_b rev 26.

Every block gets a number, a name and its XYZ range, all read from
src/g_mount_b.py so the labels cannot drift from the model.

Frame: origin = the tooth plate's end, top-face corner; X along the plate,
+Y towards the servo, Z up.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import g_mount_b as M  # noqa: E402
import g_servo as S  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

EDGE = "#1b3b5a"
FILL = "#eaf2fb"
FILL2 = "#cfe0f2"
FILL3 = "#dbe9f7"
REF = "#aab4c0"
DIM = "#495057"
BADGE = "#c92a2a"

Z0 = M.PLATE_T + M.FOOT_T               # 14
PU, PL = M.POST1_Y                      # 21.94, 29.94
QU, QL = M.POST2_Y                      # 70.44, 78.44
BR = M.BRIDGE
RIB_Z0 = Z0 - 0.5                       # gusset base sinks 0.5 into the foot
GUS = M.RIB_LEG                         # 18
BODY_X0 = M.SERVO_X - S.BODY_Z          # -2.5
BODY_Y0 = M.SERVO_CY - S.BODY_X / 2.0   # 30.19
BODY_Y1 = M.SERVO_CY + S.BODY_X / 2.0   # 70.19


def badge(ax, x, y, n, fs=9.0):
    ax.text(x, y, str(n), fontsize=fs, fontweight="bold", color=BADGE,
            ha="center", va="center", zorder=30,
            bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec=BADGE, lw=1.1))


def plate_ref(ax, view):
    if view == "top":
        ax.add_patch(Rectangle((0, 0), 60, M.PLATE_W, facecolor="none",
                               edgecolor=REF, lw=1.0, ls=(0, (4, 3))))
        ax.text(46, -6.5, "齿板（参考）0~60 × 0~24.44", fontsize=7.0,
                color=REF, ha="center")
    else:
        ax.add_patch(Rectangle((0, 0), 60, M.PLATE_T, facecolor="none",
                               edgecolor=REF, lw=1.0, ls=(0, (4, 3))))
        ax.text(48, M.PLATE_T / 2, "齿板（参考）", fontsize=7.2, color=REF,
                ha="center", va="center")


def axes_icon(ax):
    ax.annotate("", xy=(14, -11), xytext=(4, -11),
                arrowprops=dict(arrowstyle="->", color=DIM, lw=1.0))
    ax.text(15, -11, "X", fontsize=8.5, color=DIM, va="center")
    ax.annotate("", xy=(-8, -1), xytext=(0, 4),
                arrowprops=dict(arrowstyle="->", color=DIM, lw=1.0))
    ax.text(-9, -2, "Y", fontsize=8.5, color=DIM, ha="center")
    ax.plot([0], [0], marker="+", ms=10, color=DIM)
    ax.text(1.5, 1.5, "O", fontsize=8.5, color=DIM)


def view_top(ax):
    ax.set_title("俯视（X-Y）", fontsize=12, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    plate_ref(ax, "top")
    ax.add_patch(Rectangle((M.FOOT_X[0], M.FOOT_Y[0]),
                           M.FOOT_X[1] - M.FOOT_X[0],
                           M.FOOT_Y[1] - M.FOOT_Y[0], facecolor=FILL,
                           edgecolor=EDGE, lw=1.5))
    ax.add_patch(Polygon([(0, PU), (M.POST_T, PU), (0, PU - GUS)],
                         facecolor=FILL3, edgecolor=EDGE, lw=1.0, ls=":"))
    ax.add_patch(Polygon([(0, QL), (M.POST_T, QL), (0, QL + GUS)],
                         facecolor=FILL3, edgecolor=EDGE, lw=1.0, ls=":"))
    ax.add_patch(Rectangle((0, PU), M.POST_T, QL - PU, facecolor=FILL2,
                           edgecolor=EDGE, lw=1.3))
    for hy in M.HOLE_ROWS:
        for hx in M.HOLE_X:
            ax.add_patch(Circle((hx, hy), M.HOLE_D / 2, facecolor="white",
                                edgecolor=EDGE, lw=1.1))
    ax.add_patch(Rectangle((BODY_X0, BODY_Y0), S.BODY_Z, BODY_Y1 - BODY_Y0,
                           facecolor="none", edgecolor="#7b9cc0", lw=1.0,
                           ls=(0, (5, 3))))
    ax.text(18, 50, "舵机（参考）\nY 30.19~70.19", fontsize=7.4,
            color="#7b9cc0", ha="center", va="center")

    badge(ax, 32, 86, 1)
    badge(ax, 2.5, 26, 2)
    badge(ax, 2.5, 74, 3)
    badge(ax, 2.5, 50, 4)
    badge(ax, 2.5, 17, 5)
    badge(ax, 2.5, 83, 6)
    badge(ax, 28, 15, 7)
    axes_icon(ax)
    ax.set_xlim(-20, 66)
    ax.set_ylim(-16, 104)


def view_front(ax):
    ax.set_title("正视图（Y-Z，沿 +X 看）", fontsize=12, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((M.FOOT_Y[0], M.PLATE_T),
                           M.FOOT_Y[1] - M.FOOT_Y[0], M.FOOT_T,
                           facecolor=FILL, edgecolor=EDGE, lw=1.5))
    for a, b in ((PU, PL), (QU, QL)):
        ax.add_patch(Rectangle((a, Z0), b - a, M.POST_TOP - Z0,
                               facecolor=FILL2, edgecolor=EDGE, lw=1.3))
    ax.add_patch(Rectangle((BR[2], BR[4]), BR[3] - BR[2], BR[5] - BR[4],
                           facecolor=FILL2, edgecolor=EDGE, lw=1.3))
    ax.add_patch(Polygon([(PU, RIB_Z0), (PU - GUS, RIB_Z0),
                          (PU, RIB_Z0 + GUS)], facecolor=FILL3,
                         edgecolor=EDGE, lw=1.1, ls=":"))
    ax.add_patch(Polygon([(QL, RIB_Z0), (QL + GUS, RIB_Z0),
                          (QL, RIB_Z0 + GUS)], facecolor=FILL3,
                         edgecolor=EDGE, lw=1.1, ls=":"))
    for yc in (M.POST_C1, M.POST_C2):
        for zc in (M.SERVO_Z - 5, M.SERVO_Z + 5):
            ax.add_patch(Circle((yc, zc), M.SCREW_D / 2, facecolor="white",
                                edgecolor=EDGE, lw=1.2))
    ax.add_patch(Rectangle((BODY_Y0, Z0), BODY_Y1 - BODY_Y0, S.BODY_Y,
                           facecolor="none", edgecolor="#7b9cc0", lw=1.0,
                           ls=(0, (5, 3))))
    ax.text(M.SERVO_CY, M.SERVO_Z, "舵机（参考）\nY 30.19~70.19  Z 14~34",
            fontsize=7.6, color="#7b9cc0", ha="center", va="center")

    badge(ax, 60, 11.5, 1)
    badge(ax, 23.0, 15.3, 2)
    badge(ax, 72.0, 15.3, 3)
    badge(ax, 50, 36, 4)
    badge(ax, 17, 18.5, 5)
    badge(ax, 82, 18.5, 6)
    badge(ax, 25.94, 32.8, 8)
    badge(ax, 50, 17.6, 10)
    ax.set_xlim(0, 102)
    ax.set_ylim(4, 44)


def view_side(ax):
    ax.set_title("侧视（X-Z，沿 −Y 看）", fontsize=12, fontweight="bold", pad=8)
    ax.set_aspect("equal")
    ax.axis("off")
    plate_ref(ax, "side")
    ax.add_patch(Rectangle((M.FOOT_X[0], M.PLATE_T),
                           M.FOOT_X[1] - M.FOOT_X[0], M.FOOT_T,
                           facecolor=FILL, edgecolor=EDGE, lw=1.5))
    ax.add_patch(Rectangle((M.POST_X[0], Z0), M.POST_T, M.POST_TOP - Z0,
                           facecolor=FILL2, edgecolor=EDGE, lw=1.4))
    ax.add_patch(Rectangle((M.POST_X[1] - M.POCKET_DEPTH, M.POCKET_Z[0]),
                           M.POCKET_DEPTH, M.POCKET_W, facecolor="white",
                           edgecolor=BADGE, lw=1.1, ls="--"))
    for zc in (M.SERVO_Z - 5, M.SERVO_Z + 5):
        ax.add_patch(Rectangle((0, zc - M.SCREW_D / 2), M.POST_T, M.SCREW_D,
                               facecolor="white", edgecolor=EDGE, lw=1.0))
    ax.add_patch(Rectangle((M.SERVO_X - S.FLANGE_Z1, Z0), S.BODY_Z, S.BODY_Y,
                           facecolor="none", edgecolor="#7b9cc0", lw=1.0,
                           ls=(0, (5, 3))))
    ax.plot([M.SERVO_X - S.FLANGE_Z1] * 2, [M.SERVO_Z - 5, M.SERVO_Z + 5],
            color="#a05a00", lw=3.5, solid_capstyle="butt")
    ax.text(M.SERVO_X - S.FLANGE_Z1 + 2.5, M.SERVO_Z + 6, "舵机法兰（参考）",
            fontsize=7.2, color="#a05a00")
    ax.text(26, Z0 + 5, "舵机本体（参考）", fontsize=7.2, color="#7b9cc0",
            ha="center")
    badge(ax, 20, 11.5, 1)
    badge(ax, 2.5, 33.2, 2)
    badge(ax, 2.5, 19, 8)
    badge(ax, 3.75, 24, 9)
    ax.set_xlim(-10, 64)
    ax.set_ylim(-6, 44)


ROWS = [
    (1, "底脚", f"X {M.FOOT_X[0]:.0f}~{M.FOOT_X[1]:.0f}",
     f"Y {M.FOOT_Y[0]:.2f}~{M.FOOT_Y[1]:.2f}", "Z 9~14",
     "厚 5，坐在齿板上"),
    (2, "前立柱", f"X {M.POST_X[0]:.0f}~{M.POST_X[1]:.0f}",
     f"Y {PU:.2f}~{PL:.2f}", f"Z {Z0:.0f}~{M.POST_TOP:.0f}",
     "5 厚 × 8 宽；朝舵机那面是 X=5"),
    (3, "后立柱", f"X {M.POST_X[0]:.0f}~{M.POST_X[1]:.0f}",
     f"Y {QU:.2f}~{QL:.2f}", f"Z {Z0:.0f}~{M.POST_TOP:.0f}", "与 2 对称"),
    (4, "顶梁", f"X {BR[0]:.0f}~{BR[1]:.0f}",
     f"Y {BR[2]:.2f}~{BR[3]:.2f}", f"Z {BR[4]:.0f}~{BR[5]:.0f}",
     f"厚 {M.BRIDGE_T:.0f}；两柱顶相连"),
    (5, "前三角筋", f"X {M.POST_X[0]:.0f}~{M.POST_X[1]:.0f}",
     f"Y {PU - GUS:.2f}~{PU:.2f}", f"Z {RIB_Z0:.1f}~{RIB_Z0 + GUS:.1f}",
     f"45°，腿 {GUS:.0f}，厚 5，贴前柱外侧"),
    (6, "后三角筋", f"X {M.POST_X[0]:.0f}~{M.POST_X[1]:.0f}",
     f"Y {QL:.2f}~{QL + GUS:.2f}", f"Z {RIB_Z0:.1f}~{RIB_Z0 + GUS:.1f}",
     "与 5 对称"),
    (7, "齿板孔 ×8（2 排）", "X 8.00~32.59",
     f"Y {M.HOLE_Y:.2f} / {M.HOLE_Y_TAIL:.2f}", "Z 9~14 通",
     f"Ø{M.HOLE_D}；X 8.00 / 16.20 / 24.39 / 32.59"),
    (8, "M4 通孔 ×4", "X 0~5（沿 X 打通）",
     f"Y {M.POST_C1:.2f} / {M.POST_C2:.2f}",
     f"Z {M.SERVO_Z - 5:.0f} / {M.SERVO_Z + 5:.0f}",
     f"Ø{M.SCREW_D}；穿柱+法兰，螺母在法兰背面"),
    (9, "法兰凸脊槽 ×2",
     f"X {M.POST_X[1] - M.POCKET_DEPTH:.1f}~{M.POST_X[1]:.0f}"
     f"（深 {M.POCKET_DEPTH:.1f}）",
     "两柱各一段",
     f"Z {M.POCKET_Z[0]:.1f}~{M.POCKET_Z[1]:.1f}",
     f"宽 {M.POCKET_W}；前柱 Y {PU:.2f}~{PL:.2f}，"
     f"后柱 Y {QU:.2f}~{QL:.2f}"),
    (10, "舵机占位（参考）", f"X {BODY_X0:.1f}~{M.SERVO_X:.1f}",
     f"Y {BODY_Y0:.2f}~{BODY_Y1:.2f}", "Z 14~34", "不是零件，是避让空间"),
]


def table(ax):
    ax.axis("off")
    ax.text(0.0, 1.04, "部件 / 特征坐标表（mm，全部从模型读）", fontsize=12,
            fontweight="bold", transform=ax.transAxes)
    xs = [0.00, 0.09, 0.28, 0.48, 0.62, 0.72]
    for x, h in zip(xs, ["#", "名称", "X", "Y", "Z", "说明"]):
        ax.text(x, 0.95, h, fontsize=9.0, fontweight="bold",
                transform=ax.transAxes, color="#0b4f8a")
    for i, row in enumerate(ROWS):
        y = 0.865 - i * 0.084
        for x, cell in zip(xs, row):
            ax.text(x, y, str(cell), fontsize=8.0, transform=ax.transAxes,
                    fontweight="bold" if x == xs[1] else "normal")
        ax.plot([0.0, 1.0], [y - 0.036] * 2, color="#e6eaef", lw=0.6,
                transform=ax.transAxes, clip_on=False)


def main(out):
    print("no | name | X | Y | Z | note")
    for r in ROWS:
        print(" | ".join(str(c) for c in r))
    fig = plt.figure(figsize=(16.5, 10.5), dpi=115, facecolor="white")
    fig.suptitle(f"g_mount_b rev {M.REV} —— 部件编号与坐标（单位 mm）",
                 fontsize=15.5, fontweight="bold", y=0.975)
    view_top(fig.add_axes([0.015, 0.47, 0.29, 0.48]))
    view_front(fig.add_axes([0.35, 0.47, 0.63, 0.48]))
    view_side(fig.add_axes([0.015, 0.02, 0.26, 0.42]))
    table(fig.add_axes([0.30, 0.02, 0.68, 0.42]))
    fig.text(0.015, 0.004, "注：外棱 45°×1 倒角（X=0 前面、底面、孔口不倒）", fontsize=9, color="#495057")
    fig.savefig(out, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../renders/mount_b_parts.png")
