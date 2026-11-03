from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

R = Path(r"D:\IceCup\renders")
W, H = 1200, 900
TITLE_H = 96
PAD = 24

FONT_T = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 44)
FONT_S = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 30)


def sheet(name, items):
    cols, rows = 2, 2
    cw = W + 2 * PAD
    ch = TITLE_H + H + 2 * PAD
    canvas = Image.new("RGB", (cols * cw, rows * ch), "white")
    d = ImageDraw.Draw(canvas)
    for i, (png, title, sub) in enumerate(items):
        x = (i % cols) * cw
        y = (i // cols) * ch
        img = Image.open(R / png).convert("RGB")
        img = img.resize((W, H), Image.LANCZOS)
        canvas.paste(img, (x + PAD, y + TITLE_H + PAD // 2))
        d.rectangle([x + PAD - 1, y + TITLE_H + PAD // 2 - 1,
                     x + PAD + W, y + TITLE_H + PAD // 2 + H],
                    outline=(150, 150, 150), width=2)
        d.text((x + PAD + 4, y + 10), title, font=FONT_T, fill=(20, 20, 20))
        d.text((x + PAD + 4, y + 58), sub, font=FONT_S, fill=(70, 70, 70))
    canvas.save(R / name)
    print("saved", R / name, canvas.size)


sheet("g_mount_b_half_options_iso.png", [
    ("g_mount_b_half_A_iso.png", "A  一体式收口",
     "后口缩到 52.6 × 20.6，舵机仍从后面进"),
    ("g_mount_b_half_B_iso.png", "B  背盖 + 小线口",
     "3 mm 后盖，24 × 12 线口，4 × M3"),
    ("g_mount_b_half_C_iso.png", "C  背盖 + 大窗口",
     "40 × 20 窗口，舵机尾部露出"),
    ("g_mount_b_half_D_iso.png", "D  侧墙开窗",
     "后面仍全开，两侧各 20 × 12 窗（减重）"),
])

sheet("g_mount_b_half_options_detail.png", [
    ("g_mount_b_half_A_right.png", "A  背面",
     "只剩法兰口 52.6 × 20.6"),
    ("g_mount_b_half_B_right.png", "B  背面",
     "24 × 12 线口 + 4 颗 M3"),
    ("g_mount_b_half_C_right.png", "C  背面",
     "40 × 20 大窗 + 4 颗 M3"),
    ("g_mount_b_half_B_exploded_iso.png", "B  爆炸",
     "4 个角块承接后盖，拆盖后舵机照常推进"),
])

sheet("g_mount_b_half3_options_iso.png", [
    ("g_mount_b_half3_A_iso.png", "A  一体式收口（3 mm 基座）",
     "后口缩到 52.6 × 20.6，舵机仍从后面进"),
    ("g_mount_b_half3_B_iso.png", "B  背盖 + 小线口",
     "24 × 12 线口，4 × M3"),
    ("g_mount_b_half3_C_iso.png", "C  背盖 + 大窗口",
     "40 × 20 窗口，舵机尾部露出"),
    ("g_mount_b_half3_D_iso.png", "D  侧墙开窗",
     "后面仍全开，两侧各 20 × 12 窗（减重）"),
])

sheet("g_mount_b_half3_options_detail.png", [
    ("g_mount_b_half3_A_right.png", "A  背面",
     "只剩法兰口 52.6 × 20.6"),
    ("g_mount_b_half3_B_right.png", "B  背面",
     "24 × 12 线口 + 4 颗 M3"),
    ("g_mount_b_half3_C_right.png", "C  背面",
     "40 × 20 大窗 + 4 颗 M3"),
    ("g_mount_b_half3_B_exploded_iso.png", "B  爆炸",
     "4 个角块承接后盖，拆盖后舵机照常推进"),
])
