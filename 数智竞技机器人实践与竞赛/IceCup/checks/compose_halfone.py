from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

R = Path(r"D:\IceCup\renders")
OUT = R / "g_mount_b_halfone_options.png"

FONT_T = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 52)
FONT_H = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 38)
FONT_S = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 26)
FONT_M = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 24)
FONT_R = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 28)

COLS = [
    {
        "tag": "V1",
        "name": "浅收口",
        "desc": "两条 3 mm 竖筋，背面齐平",
        "stats": ["+1.04 cm³ / +1.3 g", "总 33.46 cm³ / 41.5 g",
                  "长度 40（不变）", "抗扭  ★★"],
        "iso": "g_mount_b_halfone_v1_iso.png",
        "back": "g_mount_b_halfone_v1_90_0.png",
    },
    {
        "tag": "V2",
        "name": "三角撑收口",
        "desc": "竖筋内侧加 8 mm 三角撑",
        "stats": ["+1.39 cm³ / +1.7 g", "总 33.81 cm³ / 41.9 g",
                  "长度 40（不变）", "抗扭  ★★★"],
        "iso": "g_mount_b_halfone_v2_iso.png",
        "back": "g_mount_b_halfone_v2_90_0.png",
    },
    {
        "tag": "V3",
        "name": "全背板开窗",
        "desc": "3 mm 整背板，只留法兰窗",
        "stats": ["+2.94 cm³ / +3.6 g", "总 35.35 cm³ / 43.8 g",
                  "长度 43（+3）", "抗扭  ★★★★"],
        "iso": "g_mount_b_halfone_v3_iso.png",
        "back": "g_mount_b_halfone_v3_90_0.png",
    },
    {
        "tag": "V4",
        "name": "后檐收口",
        "desc": "背口外再加 6 mm 后檐（顶+两侧）",
        "stats": ["+3.16 cm³ / +3.9 g", "总 35.58 cm³ / 44.1 g",
                  "长度 46（+6）", "抗扭  ★★★☆"],
        "iso": "g_mount_b_halfone_v4_iso.png",
        "back": "g_mount_b_halfone_v4_90_0.png",
    },
]


def crop_white(im, margin=18):
    im = im.convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        im = im.crop((max(0, x0 - margin), max(0, y0 - margin),
                      min(im.width, x1 + margin), min(im.height, y1 + margin)))
    return im


def fit(im, w, h):
    im = crop_white(im)
    im = ImageOps.contain(im, (w, h), Image.LANCZOS)
    return im


def main():
    W = 2880
    M = 44
    GUTTER = 76
    GAP = 18
    cw = (W - 2 * M - GUTTER - 3 * GAP) // 4

    TITLE_H = 176
    HEAD_H = 128
    ROW1_H = 470
    ROW2_H = 410
    STATS_H = 200

    H = M + TITLE_H + HEAD_H + ROW1_H + ROW2_H + STATS_H + M
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)

    # title
    d.text((M, 34), "g_mount_b 3 mm 底座：四种一体式半封口", font=FONT_T,
           fill=(20, 20, 20))
    d.text((M, 108),
           "舵机+法兰从背面推进 → 一体件的开口不能小于 52.6 × 20.6；"
           "四个方案都保留这个法兰窗，差别在窗口周围加多少料。",
           font=FONT_S, fill=(60, 60, 60))

    y0 = M + TITLE_H
    # row labels
    d.text((M - 4, y0 + HEAD_H + ROW1_H // 2 - 16), "立体",
           font=FONT_R, fill=(90, 90, 90))
    d.text((M - 4, y0 + HEAD_H + ROW1_H + ROW2_H // 2 - 16), "背面",
           font=FONT_R, fill=(90, 90, 90))

    for i, c in enumerate(COLS):
        x = M + GUTTER + i * (cw + GAP)
        # header
        d.text((x, y0 + 4), c["tag"], font=FONT_H, fill=(200, 50, 40))
        tw = d.textlength(c["tag"], font=FONT_H)
        d.text((x + tw + 14, y0 + 12), c["name"], font=FONT_H,
               fill=(20, 20, 20))
        d.text((x, y0 + 62), c["desc"], font=FONT_S, fill=(70, 70, 70))
        d.line([(x, y0 + HEAD_H - 10), (x + cw, y0 + HEAD_H - 10)],
               fill=(210, 210, 210), width=2)

        # iso
        im = fit(Image.open(R / c["iso"]), cw, ROW1_H - 16)
        canvas.paste(im, (x + (cw - im.width) // 2,
                          y0 + HEAD_H + (ROW1_H - im.height) // 2))

        # back
        im2 = fit(Image.open(R / c["back"]), cw, ROW2_H - 12)
        canvas.paste(im2, (x + (cw - im2.width) // 2,
                           y0 + HEAD_H + ROW1_H + (ROW2_H - im2.height) // 2))

        # stats
        sy = y0 + HEAD_H + ROW1_H + ROW2_H + 18
        d.rectangle([x, sy - 6, x + cw, sy + STATS_H - 54],
                    fill=(247, 248, 250), outline=(225, 227, 230), width=1)
        for j, line in enumerate(c["stats"]):
            d.text((x + 14, sy + 6 + j * 34), line, font=FONT_M,
                   fill=(45, 45, 45))

    # footer
    d.text((M, H - 58),
           "体积/重量按 PLA 1.24 g/cm³；基准 32.41 cm³ / 40.2 g；"
           "四个方案的背面窗口均为 52.6 × 20.6（法兰 52 × 20 + 0.3 间隙）。"
           "抗扭星级为定性排序，未做 FEA。",
           font=FONT_M, fill=(90, 90, 90))

    canvas.save(OUT)
    print("saved", OUT, canvas.size)


if __name__ == "__main__":
    main()
