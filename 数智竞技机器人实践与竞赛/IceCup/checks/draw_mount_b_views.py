r""" Three-view drawing of the current g_mount_b (rev 37) with axes and names.

    python draw_mount_b_views.py -> renders/g_mount_b_views.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = r"D:\IceCup\renders\g_mount_b_views.png"

# ---- geometry (mm), straight from src/g_mount_b.py rev 37
PLATE_T, FOOT_T = 9.0, 5.0
FOOT_X, FOOT_Y = (-8.0, 40.0), (12.94, 87.44)
FOOT_Z = (PLATE_T, PLATE_T + FOOT_T)              # 9..14
FLANGE_X0, FLANGE_X1 = 4.84, 7.50
POST_Y = ((22.19, 30.19), (70.19, 78.19))
BOX_Y0, BOX_Y1 = 18.89, 81.49
IN_Y0, IN_Y1 = 23.89, 76.49
WALL_TOP = 34.60
TOP_PLATE = (34.60, 37.30)
WALL_BOTTOM = 18.85
BACK_X = 37.65
SCREW_Y = (26.19, 74.19)
SCREW_Z = (17.675, 30.325)
HOLE_X = [8.0 + k * 8.196 for k in range(4)]
HOLE_Y = (19.94, 80.44)
SERVO_Y = (30.19, 70.19)
SERVO_Z = (14.0, 34.0)
SERVO_X = (-2.5, 37.5)
FLANGE_Y = (24.19, 76.19)
FLANGE_Z = (14.0, 34.0)
NUT_X = (7.24, 10.9)
NUT_Y = ((22.14, 23.89), (76.49, 78.24))
NUT_Z = ((18.85, 21.9), (26.1, 34.6))
RIDGE = (2.34, 5.34, 22.8, 25.2)     # x0,x1,z0,z1 of the ridge pocket
SHAFT = (-8.15, -2.5)

C_EDGE = "#12395e"
C_FOOT = "#dbe9f7"
C_WALL = "#c9d9e8"
C_TOP = "#e8eef5"
C_POST = "#ffe0b8"
C_INTER = "#ffffff"
C_SERVO = "#f2d9f5"
C_DIM = "#5b6773"
C_RED = "#c92a2a"


def axes_triad(ax, x, y, s=9.0, labels=("X", "Y")):
    ax.annotate("", xy=(x + s, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.8))
    ax.text(x + s + 1.2, y, labels[0], fontsize=11, color=C_RED, va="center")
    ax.annotate("", xy=(x, y + s), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color="#2f6f2f", lw=1.8))
    ax.text(x, y + s + 1.2, labels[1], fontsize=11, color="#2f6f2f", ha="center")


def tag(ax, x, y, n, dx=0, dy=0):
    ax.annotate(f"{n}", xy=(x, y), xytext=(x + dx, y + dy), fontsize=10,
                fontweight="bold", color=C_RED, ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=C_RED, lw=1.0),
                arrowprops=dict(arrowstyle="-", color=C_RED, lw=0.8,
                                shrinkA=0, shrinkB=0))


def main():
    fig = plt.figure(figsize=(17, 12.5), dpi=150, facecolor="white")

    # ===== 1. TOP VIEW (X-Y), looking down -Z
    ax = fig.add_axes([0.04, 0.52, 0.44, 0.42])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-24, 60)
    ax.set_ylim(2, 104)
    ax.set_title("① 俯视图（沿 −Z 看，X-Y 平面）", fontsize=12, fontweight="bold")
    # foot
    ax.add_patch(Rectangle((FOOT_X[0], FOOT_Y[0]), FOOT_X[1] - FOOT_X[0],
                           FOOT_Y[1] - FOOT_Y[0], facecolor=C_FOOT,
                           edgecolor=C_EDGE, lw=1.6, zorder=1))
    # walls (seen from above)
    for y0, y1 in ((BOX_Y0, IN_Y0), (IN_Y1, BOX_Y1)):
        ax.add_patch(Rectangle((FOOT_X[0], y0), FOOT_X[1] - FOOT_X[0], y1 - y0,
                               facecolor=C_WALL, edgecolor=C_EDGE, lw=1.2,
                               zorder=2))
    # top plate covering everything
    ax.add_patch(Rectangle((FOOT_X[0], BOX_Y0), FOOT_X[1] - FOOT_X[0],
                           BOX_Y1 - BOX_Y0, facecolor=C_TOP, edgecolor=C_EDGE,
                           lw=1.4, ls=(0, (6, 3)), zorder=3))
    # posts (hidden under the top plate)
    for y0, y1 in POST_Y:
        ax.add_patch(Rectangle((0, y0), FLANGE_X0, y1 - y0, facecolor=C_POST,
                               edgecolor="#a05a00", lw=1.0, ls=(0, (2, 2)),
                               zorder=4))
    # servo + flange (reference)
    ax.add_patch(Rectangle((SERVO_X[0], SERVO_Y[0]),
                           SERVO_X[1] - SERVO_X[0], SERVO_Y[1] - SERVO_Y[0],
                           facecolor="none", edgecolor="#6b3fa0", lw=1.2,
                           ls=(0, (4, 3)), zorder=5))
    ax.add_patch(Rectangle((FLANGE_X0, FLANGE_Y[0]), FLANGE_X1 - FLANGE_X0,
                           FLANGE_Y[1] - FLANGE_Y[0], facecolor=C_SERVO,
                           edgecolor="#6b3fa0", lw=1.4, alpha=0.8, zorder=6))
    # plate holes
    for hy in HOLE_Y:
        for hx in HOLE_X:
            ax.add_patch(Circle((hx, hy), 2.25, facecolor="white",
                                edgecolor=C_RED, lw=1.1, zorder=7))
    # servo screw holes
    for sy in SCREW_Y:
        for sz in SCREW_Z:
            ax.add_patch(Circle((FLANGE_X0 / 2, sy), 2.25, facecolor="none",
                                edgecolor="#a05a00", lw=1.0, ls=(0, (1, 1)),
                                zorder=7))
    axes_triad(ax, -20, 8, 9)
    tag(ax, -4, 50, 1, -14, 12)          # foot
    tag(ax, -4, 20, 2, -16, -8)          # wall
    tag(ax, 16, 50, 3, 0, 16)            # top plate
    tag(ax, 2.4, 26, 4, -10, -14)        # post
    tag(ax, 6.2, 50, 5, 14, 22)          # flange
    tag(ax, 17, 50, 6, 16, 4)            # servo
    tag(ax, HOLE_X[0], HOLE_Y[0], 7, 8, -10)   # plate hole
    tag(ax, 33, 50, 12, 20, -18)         # back opening

    # ===== 2. FRONT VIEW (Y-Z), looking along +X
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.42])
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_xlim(2, 96)
    ax2.set_ylim(-2, 48)
    ax2.set_title("② 主视图（沿 +X 看，Y-Z 平面）", fontsize=12, fontweight="bold")
    # foot
    ax2.add_patch(Rectangle((FOOT_Y[0], FOOT_Z[0]), FOOT_Y[1] - FOOT_Y[0],
                            FOOT_Z[1] - FOOT_Z[0], facecolor=C_FOOT,
                            edgecolor=C_EDGE, lw=1.6))
    # walls
    for y0, y1 in ((BOX_Y0, IN_Y0), (IN_Y1, BOX_Y1)):
        ax2.add_patch(Rectangle((y0, WALL_BOTTOM), y1 - y0,
                                WALL_TOP - WALL_BOTTOM, facecolor=C_WALL,
                                edgecolor=C_EDGE, lw=1.2))
    # top plate
    ax2.add_patch(Rectangle((BOX_Y0, TOP_PLATE[0]), BOX_Y1 - BOX_Y0,
                            TOP_PLATE[1] - TOP_PLATE[0], facecolor=C_TOP,
                            edgecolor=C_EDGE, lw=1.4))
    # interior (opening)
    ax2.add_patch(Rectangle((IN_Y0, FOOT_Z[1]), IN_Y1 - IN_Y0,
                            WALL_TOP - FOOT_Z[1], facecolor=C_INTER,
                            edgecolor=C_EDGE, lw=1.0, ls=(0, (3, 2)), zorder=2))
    # posts
    for y0, y1 in POST_Y:
        ax2.add_patch(Rectangle((y0, FOOT_Z[1]), y1 - y0, WALL_TOP - FOOT_Z[1],
                                facecolor="none", edgecolor="#a05a00", lw=1.2,
                                ls=(0, (2, 2)), zorder=3))
    # servo + flange
    ax2.add_patch(Rectangle((SERVO_Y[0], SERVO_Z[0]), SERVO_Y[1] - SERVO_Y[0],
                            SERVO_Z[1] - SERVO_Z[0], facecolor="none",
                            edgecolor="#6b3fa0", lw=1.0, ls=(0, (4, 3)),
                            zorder=4))
    ax2.add_patch(Rectangle((FLANGE_Y[0], FLANGE_Z[0]),
                            FLANGE_Y[1] - FLANGE_Y[0], FLANGE_Z[1] - FLANGE_Z[0],
                            facecolor=C_SERVO, edgecolor="#6b3fa0", lw=1.4,
                            alpha=0.7, zorder=5))
    # 4 through holes
    for sy in SCREW_Y:
        for sz in SCREW_Z:
            ax2.add_patch(Circle((sy, sz), 2.25, facecolor="white",
                                 edgecolor=C_RED, lw=1.2, zorder=6))
    # nut pockets (hidden)
    for y0, y1 in NUT_Y:
        for z0, z1 in NUT_Z:
            ax2.add_patch(Rectangle((y0, z0), y1 - y0, z1 - z0,
                                    facecolor="none", edgecolor="#2f6f2f",
                                    lw=1.0, ls=(0, (1, 2)), zorder=7))
    axes_triad(ax2, 6, 42, 9, ("Y", "Z"))
    tag(ax2, 50, 10, 1, 0, -7)
    tag(ax2, 21, 30, 2, -14, 8)
    tag(ax2, 50, 36, 3, 0, 8)
    tag(ax2, 50, 24, 8, 0, 14)                 # interior / flange envelope
    tag(ax2, 26.19, 30.325, 9, -12, 10)        # through hole
    tag(ax2, 22.9, 20.0, 10, -13, -2)          # nut pocket
    tag(ax2, 50.19, 24, 5, 16, 0)              # flange

    # ===== 3. SIDE VIEW (X-Z), looking along +Y
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    ax3.set_aspect("equal")
    ax3.axis("off")
    ax3.set_xlim(-18, 48)
    ax3.set_ylim(4, 44)
    ax3.set_title("③ 左视图（沿 +Y 看，X-Z 平面）", fontsize=12, fontweight="bold")
    ax3.add_patch(Rectangle((FOOT_X[0], FOOT_Z[0]), FOOT_X[1] - FOOT_X[0],
                            FOOT_Z[1] - FOOT_Z[0], facecolor=C_FOOT,
                            edgecolor=C_EDGE, lw=1.6))
    ax3.add_patch(Rectangle((FOOT_X[0], WALL_BOTTOM), FOOT_X[1] - FOOT_X[0],
                            WALL_TOP - WALL_BOTTOM, facecolor=C_WALL,
                            edgecolor=C_EDGE, lw=1.2, alpha=0.75))
    ax3.add_patch(Rectangle((FOOT_X[0], TOP_PLATE[0]), FOOT_X[1] - FOOT_X[0],
                            TOP_PLATE[1] - TOP_PLATE[0], facecolor=C_TOP,
                            edgecolor=C_EDGE, lw=1.4))
    # interior from X 4.84 to 37.65
    ax3.add_patch(Rectangle((FLANGE_X0, FOOT_Z[1]), BACK_X - FLANGE_X0,
                            WALL_TOP - FOOT_Z[1], facecolor="white",
                            edgecolor=C_EDGE, lw=1.0, ls=(0, (3, 2)), zorder=2))
    # posts
    for y0, y1 in POST_Y:
        pass
    ax3.add_patch(Rectangle((0, FOOT_Z[1]), FLANGE_X0, WALL_TOP - FOOT_Z[1],
                            facecolor=C_POST, edgecolor="#a05a00", lw=1.2,
                            alpha=0.75, zorder=3))
    # flange
    ax3.add_patch(Rectangle((FLANGE_X0, FLANGE_Z[0]), FLANGE_X1 - FLANGE_X0,
                            FLANGE_Z[1] - FLANGE_Z[0], facecolor=C_SERVO,
                            edgecolor="#6b3fa0", lw=1.4, alpha=0.8, zorder=4))
    # servo body (dashed) + shaft
    ax3.add_patch(Rectangle((SERVO_X[0], SERVO_Z[0]), SERVO_X[1] - SERVO_X[0],
                            SERVO_Z[1] - SERVO_Z[0], facecolor="none",
                            edgecolor="#6b3fa0", lw=1.0, ls=(0, (4, 3)),
                            zorder=5))
    ax3.add_patch(Rectangle((SHAFT[0], 23.05), SHAFT[1] - SHAFT[0], 5.9,
                            facecolor="white", edgecolor="#6b3fa0", lw=1.0,
                            zorder=6))
    # through holes (hidden lines) + ridge pockets + nut pockets
    for sz in SCREW_Z:
        ax3.plot([0, FLANGE_X0], [sz, sz], color=C_RED, lw=0.9, ls=(0, (4, 2)))
    ax3.add_patch(Rectangle((RIDGE[0], RIDGE[2]), RIDGE[1] - RIDGE[0],
                            RIDGE[3] - RIDGE[2], facecolor="none",
                            edgecolor="#2f6f2f", lw=0.9, ls=(0, (1, 2))))
    for z0, z1 in NUT_Z:
        ax3.add_patch(Rectangle((NUT_X[0], z0), NUT_X[1] - NUT_X[0], z1 - z0,
                                facecolor="none", edgecolor="#2f6f2f",
                                lw=0.9, ls=(0, (1, 2))))
    axes_triad(ax3, -14, 8, 9, ("X", "Z"))
    tag(ax3, 16, 11.5, 1, 0, -6)
    tag(ax3, 22, 26, 2, 10, 12)
    tag(ax3, 22, 36, 3, 0, 6)
    tag(ax3, 2.4, 26, 4, -12, 6)
    tag(ax3, 6.2, 20, 5, -14, -6)
    tag(ax3, 30, 24, 8, 0, -10)
    tag(ax3, 8.9, 20.0, 10, 14, -8)      # nut pocket
    tag(ax3, 38.5, 24, 12, 10, 4)        # back opening
    tag(ax3, 3.8, 23.9, 11, -12, -12)    # ridge pocket

    # ===== legend
    fig.text(0.52, 0.44, "部件名称", fontsize=13, fontweight="bold", color="#12395e")
    items = [
        (1, "脚板 foot", "X −8…40，Y 12.94…87.44，Z 9…14（5 厚）"),
        (2, "侧壁 side wall", "5 厚，X −8…40，Z 18.85…34.6（下面留 4.85 给底盘螺栓头）"),
        (3, "顶板 top plate", "2.7 厚，Z 34.6…37.3，横跨整个 Y"),
        (4, "前立柱 front post", "X 0…4.84，Y 22.19…30.19 / 70.19…78.19，Z 14…34.6"),
        (5, "舵机法兰 flange", "52 × 20 × 2.66，X 4.84…7.5（贴立柱内面）"),
        (6, "舵机本体 body", "40 × 20 × 40，Y 30.19…70.19，Z 14…34"),
        (7, "底盘安装孔 ×8", "Ø4.5，X 8/16.196/24.392/32.588，Y 19.94 / 80.44"),
        (8, "内腔 interior", "Y 23.89…76.49，Z 14…34.6（后端敞开）"),
        (9, "法兰通孔 ×4", "Ø4.5，Y 26.19 / 74.19，Z 17.675 / 30.325"),
        (10, "螺母暗袋 ×4", "侧壁内面盲槽 1.75 深，Z 18.85…21.9 / 26.1…34.6"),
        (11, "凸起让位槽 ×2", "立柱内面 2.5 深 × 2.4 高，Z 22.8…25.2"),
        (12, "背面开口", "X 37.65（内腔后端），开口 Y 23.89…76.49 × Z 14…34.6"),
        (13, "输出轴 + 舵盘", "轴 Ø5.9，X −8.15…−2.5；舵盘 Ø20 × 2.5"),
    ]
    y = 0.405
    for n, name, note in items:
        fig.text(0.52, y, f"{n:>2}", fontsize=9.5, fontweight="bold", color=C_RED)
        fig.text(0.545, y, name, fontsize=9.5, color="#1a1a1a")
        fig.text(0.68, y, note, fontsize=8.6, color="#555555")
        y -= 0.0265

    fig.suptitle("轮板舵机支架 g_mount_b rev37 —— 三视图 / 坐标轴 / 部件名称",
                 fontsize=16, fontweight="bold", y=0.975)
    fig.text(0.04, 0.015,
             "坐标系：原点 = 脚板前左下方（齿板底面上表面 Z=0 起）；X 沿齿板方向（右为正），"
             "Y 跨齿板方向（前为正），Z 向上。舵机输出轴朝 −X。",
             fontsize=9.6, color="#333333")
    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
