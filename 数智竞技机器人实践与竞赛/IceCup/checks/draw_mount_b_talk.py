r"""Explain the bracket: coordinate axes, faces, part names, and the question.

    python draw_mount_b_talk.py  ->  renders/g_mount_b_talk.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = r"D:\IceCup\renders\g_mount_b_talk.png"

# geometry (from the model, mm)
PLATE_Z0, PLATE_Z1 = 0.0, 9.0        # tooth plate (reference)
FOOT_X0, FOOT_X1 = 0.0, 40.0
FOOT_Y0, FOOT_Y1 = 12.94, 87.44
FOOT_Z0, FOOT_Z1 = 9.0, 14.0         # foot sits on the plate
POST_X0, POST_X1 = 0.0, 5.0          # front posts: 4 through holes + ridge pockets
FLANGE_X0, FLANGE_X1 = 5.0, 7.5      # servo flange
BODY_X0, BODY_X1 = -2.5, 37.5        # servo body
BODY_Y0, BODY_Y1 = 30.19, 70.19
POST1_Y = (21.94, 29.94)
POST2_Y = (70.44, 78.44)
FLANGE_Y = (25.94, 74.44)
BODY_Z0, BODY_Z1 = 14.0, 34.0
FLANGE_Z = (19.0, 29.0)
TOP_Z = 37.0


def triad(ax, x, y, s=10.0):
    ax.annotate("", xy=(x + s, y), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color="#c92a2a", lw=2.0))
    ax.text(x + s + 1.5, y, "X", fontsize=11, color="#c92a2a", va="center")
    ax.annotate("", xy=(x, y + s), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color="#2f6f2f", lw=2.0))
    ax.text(x, y + s + 1.5, "Y", fontsize=11, color="#2f6f2f", ha="center")


def main():
    fig = plt.figure(figsize=(15.0, 13.0), dpi=160, facecolor="white")

    # ------------------------------------------------ panel 1: top view X-Y
    ax = fig.add_axes([0.05, 0.52, 0.42, 0.42])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-20, 62)
    ax.set_ylim(4, 96)
    ax.set_title("俯视（X-Y 平面）：各个面的名字", fontsize=12,
                 fontweight="bold")
    ax.add_patch(Rectangle((FOOT_X0, FOOT_Y0), FOOT_X1 - FOOT_X0,
                           FOOT_Y1 - FOOT_Y0, facecolor="#e8eef5",
                           edgecolor="#12395e", lw=1.6))
    ax.text(20, 8.5, "脚板 foot（8 个 Ø4.5 底盘孔）", fontsize=8.5,
            ha="center", color="#12395e")
    for y0, y1 in (POST1_Y, POST2_Y):
        ax.add_patch(Rectangle((POST_X0, y0), POST_X1 - POST_X0, y1 - y0,
                               facecolor="#ffe0b8", edgecolor="#a05a00", lw=1.4))
    ax.text(2.5, 84, "前立柱\nfront post\n(4 通孔+凸起槽)", fontsize=8,
            ha="center", color="#a05a00")
    ax.add_patch(Rectangle((BODY_X0, BODY_Y0), BODY_X1 - BODY_X0,
                           BODY_Y1 - BODY_Y0, facecolor="none",
                           edgecolor="#6b3fa0", lw=1.6, ls=(0, (5, 3))))
    ax.text(17, 50, "舵机本体\nbody 40×20\n(Z 向 20)", fontsize=8.5,
            ha="center", color="#6b3fa0")
    ax.add_patch(Rectangle((FLANGE_X0, FLANGE_Y[0]), FLANGE_X1 - FLANGE_X0,
                           FLANGE_Y[1] - FLANGE_Y[0], facecolor="#c8e8c8",
                           edgecolor="#2f6f2f", lw=1.2))
    ax.text(6.2, 91, "法兰 flange 48.5 宽", fontsize=8, color="#2f6f2f")
    # side walls (proposed)
    for y0, y1 in ((BODY_Y0 - 0.15, BODY_Y0 - 0.15 - 3.0),
                   (BODY_Y1 + 0.15, BODY_Y1 + 0.15 + 3.0)):
        pass
    ax.annotate("← 后面（开口，舵机从这儿推进）", xy=(41, 50), xytext=(30, 76),
                fontsize=9, color="#c92a2a",
                arrowprops=dict(arrowstyle="->", color="#c92a2a", lw=1.4))
    ax.annotate("前面（法兰压在这儿）", xy=(2, 50), xytext=(-16, 66),
                fontsize=9, color="#a05a00",
                arrowprops=dict(arrowstyle="->", color="#a05a00", lw=1.4))
    triad(ax, -14, 16, 12)
    ax.text(-3, 101, "左面\n左侧壁", fontsize=8, color="#495057")
    ax.text(41, 101, "右面\n右侧壁", fontsize=8, color="#495057")

    # ------------------------------------------------ panel 2: side view X-Z
    ax2 = fig.add_axes([0.52, 0.52, 0.45, 0.42])
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_xlim(-22, 62)
    ax2.set_ylim(-6, 48)
    ax2.set_title("侧视（X-Z 平面，从左边看）：你要的“背面开 + 通孔 + 凸起槽”",
                  fontsize=12, fontweight="bold")
    ax2.add_patch(Rectangle((FOOT_X0, PLATE_Z0), 60, PLATE_Z1, facecolor="#dbe9f7",
                            edgecolor="#12395e", lw=1.2, alpha=0.7))
    ax2.text(30, 4, "齿板（参考）", fontsize=8, ha="center", color="#12395e")
    ax2.add_patch(Rectangle((FOOT_X0, FOOT_Z0), FOOT_X1 - FOOT_X0,
                            FOOT_Z1 - FOOT_Z0, facecolor="#c9d9e8",
                            edgecolor="#12395e", lw=1.4))
    ax2.text(30, 11.5, "脚板", fontsize=8.5, ha="center")
    # front posts
    for y0, y1 in (POST1_Y, POST2_Y):
        pass
    ax2.add_patch(Rectangle((POST_X0, FOOT_Z1), POST_X1 - POST_X0,
                            TOP_Z - FOOT_Z1, facecolor="#ffe0b8",
                            edgecolor="#a05a00", lw=1.4))
    ax2.text(2.5, 33, "前立柱", fontsize=8, ha="center", rotation=90,
             color="#a05a00")
    # servo body + flange
    ax2.add_patch(Rectangle((BODY_X0, BODY_Z0), BODY_X1 - BODY_X0,
                            BODY_Z1 - BODY_Z0, facecolor="#e6d8f5",
                            edgecolor="#6b3fa0", lw=1.6))
    ax2.text(17, 24, "舵机本体 40×20", fontsize=8.5, ha="center",
             color="#6b3fa0")
    ax2.add_patch(Rectangle((FLANGE_X0, FLANGE_Z[0]), FLANGE_X1 - FLANGE_X0,
                            FLANGE_Z[1] - FLANGE_Z[0], facecolor="#c8e8c8",
                            edgecolor="#2f6f2f", lw=1.4))
    ax2.text(6.3, 14.5, "法兰", fontsize=8, color="#2f6f2f")
    # through holes + nut + ridge pocket
    for z in (FLANGE_Z[0] + 2.0, FLANGE_Z[1] - 2.0):
        ax2.add_patch(Rectangle((POST_X0 - 0.5, z - 1.1), 6.0, 2.2,
                                facecolor="white", edgecolor="#c92a2a", lw=1.0))
    ax2.annotate("4 个 Ø4.5 通孔\n（螺栓穿过去）", xy=(2.5, 21), xytext=(-20, 40),
                 fontsize=8.5, color="#c92a2a",
                 arrowprops=dict(arrowstyle="->", color="#c92a2a", lw=1.2))
    ax2.annotate("螺母在法兰后面\n（需要手能伸进去拧）", xy=(9.5, 26), xytext=(14, 42),
                 fontsize=8.5, color="#c92a2a",
                 arrowprops=dict(arrowstyle="->", color="#c92a2a", lw=1.2))
    ax2.annotate("法兰背面 2mm 高的凸起棱\n→ 立柱内面开 2.5 深的让位槽（凸起槽）",
                 xy=(5.1, 20.2), xytext=(11, 6.0), fontsize=8.5, color="#2f6f2f",
                 arrowprops=dict(arrowstyle="->", color="#2f6f2f", lw=1.2))
    # proposed walls
    ax2.add_patch(Rectangle((BODY_X0, BODY_Z1 + 0.15), BODY_X1 - BODY_X0 + 2.5,
                            3.0, facecolor="#f2f2f2", edgecolor="#5b6773",
                            lw=1.4, ls=(0, (4, 3))))
    ax2.text(20, 37.5, "顶板（封死）", fontsize=8.5, ha="center", color="#5b6773")
    ax2.annotate("", xy=(-4, 24), xytext=(-16, 24),
                 arrowprops=dict(arrowstyle="-|>", color="#c92a2a", lw=2.0))
    ax2.text(-17, 25, "舵机从后面推进来 →", fontsize=9, color="#c92a2a")
    ax2.text(40, 24, "后面\n开口", fontsize=9, color="#c92a2a", ha="center")
    triad(ax2, -18, 40, 10)

    # ------------------------------------------------ text block
    fig.text(0.05, 0.44, "我现在的理解（请你逐条确认/纠正）：", fontsize=13,
             fontweight="bold", color="#12395e")
    lines = [
        "1  盒子：底面=脚板、前面=两根立柱、顶面=一块板封死、左右=两块侧壁；"
        "【后面】完全敞开，舵机从后面水平推进去。",
        "2  前面：立柱上开 4 个 Ø4.5 【通孔】（螺栓穿过去 + 螺母拧在法兰内侧），"
        "和 rev29 一样，不是自攻。",
        "3  法兰：压在立柱的内面（后面那一侧），立柱内面开 2.5 深 × 2.4 宽的"
        "【凸起槽】，让法兰背面那条 2mm 高的凸起棱陷进去。",
        "4  舵机本体：被左右侧壁 + 顶板 + 脚板围住，每边 0.15 间隙 → 零框量。",
        "5  装配：从后口推入 → 法兰顶到立柱内面 → 4 颗螺栓从前面穿过立柱和法兰 → "
        "螺母在后面拧紧 → 顶板/侧壁把本体夹住。",
    ]
    y = 0.40
    for ln in lines:
        fig.text(0.05, y, ln, fontsize=10.2, color="#333333")
        y -= 0.033

    fig.text(0.05, 0.20, "需要你回答的 5 个问题：", fontsize=13,
             fontweight="bold", color="#c92a2a")
    qs = [
        "Q1  “后面开”是指整个背面全开（56.5 宽 × 20 高），还是只留“本体 40.3 × 20.3”的口？"
        "如果只留本体口，法兰 48.5 宽过不去，就必须在两侧壁内面开一条通长的法兰槽。",
        "Q2  4 颗螺栓从【前面】穿、螺母在【后面】（法兰内侧、盒子里），手上能伸进去拧吗？"
        "还是反过来（螺栓从后面穿、螺母在前面）？",
        "Q3  “凸起的槽”我理解成 rev29 那个 2.5 深 × 2.4 宽、给法兰背面凸起棱让位的槽 —— 对吗？"
        "还是指左右侧壁里让法兰滑进去的那条通长槽？",
        "Q4  顶板要不要和侧壁/立柱一起封死（一体），还是顶面也留开口？",
        "Q5  左右侧壁的长度：从最前面（X=0）一直到脚板后边（X=40），还是到舵机本体末端（X=37.5）就停？",
    ]
    y = 0.16
    for q in qs:
        fig.text(0.05, y, q, fontsize=10.0, color="#333333", wrap=True)
        y -= 0.032

    fig.savefig(OUT, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
