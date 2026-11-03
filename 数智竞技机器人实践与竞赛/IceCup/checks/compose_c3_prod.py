# -*- coding: utf-8 -*-
"""Compose the C3 production-part sheet.  Pure layout, no geometry."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

R = Path(r"D:\IceCup\renders")
OUT = R / "g_mount_b_C3_prod_sheet.png"

FONT_T = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 46)
FONT_H = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30)
FONT_S = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 24)
FONT_M = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)

CELL_W, CELL_H = 780, 585
GAP = 18
LEFT = 30
TOP = 150

CELLS = [
    ("iso", "C3_prod_iso.png",
     "成品 C3：脚 5 / 墙 3 / 顶 3 / 后 2.5，不是全 5 mm",
     "35.65 cm3 / 44.2 g PLA（含 1 mm 倒角）"),
    ("rear", "C3_prod_rear.png",
     "背面：60 x 20.4 窗口，法兰每边 4 mm",
     "透窗可见前面 4 个法兰孔 = 一条直线"),
    ("front", "C3_prod_front.png",
     "正面：rev30 前门框原样，立柱 5 厚、4 法兰孔",
     "舵机法兰贴立柱内面 X=5，4 x M4 对锁"),
    ("sec", "C3_prod_sec.png",
     "横截面 X=23.19：脚 5 / 墙 3 / 顶 3 一眼看清",
     "墙内面 23.19/77.19、顶下沿 35、后板 2.5"),
]

FOOT_LINES = [
    "厚度清单：脚板 5（Z 9~14）；侧墙 3（内面 Y 23.19 / 77.19）；顶盖 3（Z 35~38）；后板 2.5（X 47.5~50）；rev30 立柱 5、顶梁 3。",
    "侧墙做不到 5：往外厚外面到 18.19，压脚板 D9 垫圈（外缘 19.5）；往内厚内面过 23.69，法兰侧隙就不足 0.5。上限约 3.5~3.7。",
    "顶盖 5 则顶面 38→40（比顶梁高 2）或下沿 35→33 顶到法兰（法兰顶 34）；后板 5 则尾后余量 10→7.5 或总长 50→52.5。都要动包络。",
    "想加厚说一声：侧墙 3.5 是一句话的事；再厚必须挪脚孔或三角筋。校核（checks/verify_c3_1mm.py）：裸舵机扫掠 48/49 全空、",
    "dx=0 14.947 mm3（法兰贴立柱）；螺栓头 / 直内六角 / 8 孔垫圈·头·螺丝刀 全 0 干涉。",
    "打印：PLA、0.2 层、脚板朝下；顶盖下沿 Z=35 是大悬空，要开支撑；侧墙 / 后板竖直自支撑。倒角 9 条选中 2 条拒绝（与初版同）。",
    "装配顺序：先推裸舵机到位 → 后窗穿 4 x M4（螺母在前面 X=0）→ 拧 8 颗脚螺丝（安装板需 >=90.44 宽、按 X 19/27/35/43 重打孔）。",
]


def main():
    cols, rows = 2, 2
    w = LEFT * 2 + cols * CELL_W + (cols - 1) * GAP
    foot_h = 40 + len(FOOT_LINES) * 34
    h = TOP + rows * (CELL_H + 78) + (rows - 1) * GAP + foot_h

    img = Image.new("RGB", (w, h), (245, 246, 248))
    d = ImageDraw.Draw(img)
    d.text((LEFT, 26), "C3 成品件 —— 35.65 cm3 / 44.2 g PLA",
           font=FONT_T, fill=(20, 24, 32))
    d.text((LEFT, 92), "外形 50 x 80.5 x 29；接口尺寸与 1 mm 试装件相同，只差壁厚",
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
