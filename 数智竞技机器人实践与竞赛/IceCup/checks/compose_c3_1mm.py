# -*- coding: utf-8 -*-
"""Compose the C3 1 mm fit-test sheet.  Pure layout, no geometry."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

R = Path(r"D:\IceCup\renders")
OUT = R / "g_mount_b_C3_1mm_sheet.png"

FONT_T = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 46)
FONT_H = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30)
FONT_S = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 24)
FONT_M = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)

CELL_W, CELL_H = 780, 585
GAP = 18
LEFT = 30
TOP = 150

CELLS = [
    ("iso", "C3_1mm_iso.png",
     "1 mm 薄壁试装件：脚板 / 后板 / 侧墙 / 顶盖全 1 mm",
     "11.13 cm3 / 13.8 g PLA（正式件 35.65 / 44.2）"),
    ("rear", "C3_1mm_rear.png",
     "背面：60 x 20.4 窗口，舵机和 52 法兰从这个口进",
     "法兰每边 4 mm、上方 0.4；透窗可见前面 4 个法兰孔"),
    ("front", "C3_1mm_front.png",
     "正面：rev30 前门框保持实心（只占 ~1.7 cm3）",
     "试装件能真的把舵机用 4 x M4 锁上去"),
    ("xray", "C3_1mm_servo_xray.png",
     "舵机 + 4 个 D7 螺栓头 + 3 mm 内六角路径（绿）",
     "裸舵机扫掠 49 位 48 全空；预装螺栓头则过不了，见下"),
    ("sect", "C3_1mm_sec_trans.png",
     "横截面 X=23.19：脚 1 / 墙 1 / 顶 1，顶盖两边各挑 2",
     "墙内面 Y 23.19 / 77.19、顶下沿 Z 35 与正式件同"),
    ("wall", "C3_1mm_sec_wall.png",
     "侧墙剖面 Y=22.69：9 x 7 出线窗一个洞",
     "X 26.5~35.5（侧墙水平居中）、Z 27~34，左右镜像"),
]

FOOT_LINES = [
    "校核（checks/verify_c3_1mm.py，与正式件同基准）：裸舵机插入扫掠 0.5 mm 步长 49 位，只有 dx=0 一处 14.947 mm3",
    "（法兰贴 rev30 立柱，设计如此，正式件同值）；4 个 D7 螺栓头、4 条直 3 mm 内六角、8 孔的 D9 垫圈 / D7 头 / D5 螺丝刀位 全 0 干涉。",
    "侧墙已外移 0.5（内面 23.19 / 77.19、外面 20.19 / 80.19）：法兰侧隙 0.5→1.0 / 边，内六角侧隙 0.75→1.25；",
    "代价是脚板垫圈 D9（外缘 Y 19.5）离墙外面 1.19→0.69，仍不干涉——若挡的是这 8 颗脚螺丝，说一声我改孔不改墙。",
    "螺栓预装在法兰上一起推进去仍过不了（D7 头外缘 22.44 仍越过墙内面），装配顺序不变：先裸舵机、后从后窗穿螺栓。",
    "60 窗口比 53 内腔宽：后板中段不拉侧墙，闭合靠脚板 + 顶盖 + 后板上条/侧条，后封抗扭比 53 窗口弱。",
    "样板差异：脚底 Z=13（放板上高 4 mm，孔 X/Y 不变）、顶面 Z=36（顶梁高 2 mm）、不倒角。PLA 0.2 层、脚板朝下、顶盖开支撑；只验装配不受力。",
]


def main():
    cols, rows = 3, 2
    w = LEFT * 2 + cols * CELL_W + (cols - 1) * GAP
    foot_h = 40 + len(FOOT_LINES) * 34
    h = TOP + rows * (CELL_H + 78) + (rows - 1) * GAP + foot_h

    img = Image.new("RGB", (w, h), (245, 246, 248))
    d = ImageDraw.Draw(img)
    d.text((LEFT, 26), "C3 的 1 mm 试装件 —— 先打这个验装配，再打 44.2 g 正式件",
           font=FONT_T, fill=(20, 24, 32))
    d.text((LEFT, 92), "外形 50 x 80.5 x 25（正式件 50 x 80.5 x 29）；接口尺寸与 C3 完全相同，只把 C3 新加的四面壁减到 1 mm",
           font=FONT_S, fill=(90, 96, 108))

    for i, (tag, fn, cap1, cap2) in enumerate(CELLS):
        cx = LEFT + (i % cols) * (CELL_W + GAP)
        cy = TOP + (i // cols) * (CELL_H + 78 + GAP)
        src = Image.open(R / fn).convert("RGB")
        src = ImageOps.contain(src, (CELL_W, CELL_H))
        px = cx + (CELL_W - src.width) // 2
        py = cy + (CELL_H - src.height) // 2
        d.rectangle((cx - 2, cy - 2, cx + CELL_W + 2, cy + CELL_H + 2),
                    outline=(200, 204, 212), width=2)
        img.paste(src, (px, py))
        d.text((cx, cy + CELL_H + 8), cap1, font=FONT_H, fill=(24, 28, 36))
        d.text((cx, cy + CELL_H + 46), cap2, font=FONT_M, fill=(96, 102, 114))

    fy = TOP + rows * (CELL_H + 78) + (rows - 1) * GAP + 6
    d.line((LEFT, fy, w - LEFT, fy), fill=(190, 194, 202), width=2)
    for k, line in enumerate(FOOT_LINES):
        d.text((LEFT, fy + 14 + k * 34), line, font=FONT_M,
               fill=(60, 66, 78))

    img.save(OUT)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
