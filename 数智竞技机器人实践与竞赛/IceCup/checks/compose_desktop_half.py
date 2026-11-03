from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

R = Path(r"D:\IceCup\renders")
OUT = R / "g_mount_b_desktop_half_options.png"

FONT_T = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 50)
FONT_H = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 34)
FONT_S = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 24)
FONT_M = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)
FONT_R = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 26)

COLS = [
    {
        "tag": "现状",
        "name": "rev30 鞍座",
        "desc": "桌面 SLDASM 里的原件",
        "stats": ["16.57 cm³ / 20.5 g", "长度 40 / 高 38", "后门、顶、两侧全开",
                  "抗扭  ★"],
        "iso": "g_mount_b_desktop_base_iso.png",
        "top": "g_mount_b_desktop_base_top.png",
    },
    {
        "tag": "A",
        "name": "后门框",
        "desc": "后端加一个 44 × 21 的框，正好在舵机尾部后面",
        "stats": ["+1.09 cm³ / +1.3 g", "总 17.65 cm³ / 21.9 g",
                  "长度 40（不变）", "抗扭  ★★"],
        "iso": "g_mount_b_desktop_A_iso.png",
        "top": "g_mount_b_desktop_A_top.png",
    },
    {
        "tag": "B",
        "name": "后门框 + 后半侧墙",
        "desc": "侧墙从 X=12 起、下沿 Z=19，顶部仍开",
        "stats": ["+3.71 cm³ / +4.6 g", "总 20.28 cm³ / 25.1 g",
                  "长度 40（不变）", "抗扭  ★★★"],
        "iso": "g_mount_b_desktop_B_iso.png",
        "top": "g_mount_b_desktop_B_top.png",
    },
    {
        "tag": "C",
        "name": "后门框 + 侧墙 + 顶盖",
        "desc": "顶盖把前后框连起来；脚板螺丝仍够得到",
        "stats": ["+9.45 cm³ / +11.7 g", "总 26.02 cm³ / 32.3 g",
                  "长度 40（不变）", "抗扭  ★★★★"],
        "iso": "g_mount_b_desktop_C_iso.png",
        "top": "g_mount_b_desktop_C_top.png",
    },
    {
        "tag": "D",
        "name": "半长顶盖",
        "desc": "前顶梁往后延 17.5 mm，后半仍开",
        "stats": ["+2.92 cm³ / +3.6 g", "总 19.49 cm³ / 24.2 g",
                  "长度 40（不变）", "抗扭  ★★"],
        "iso": "g_mount_b_desktop_D_iso.png",
        "top": "g_mount_b_desktop_D_top.png",
    },
]


def crop_white(im, margin=16):
    im = im.convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox
        im = im.crop((max(0, x0 - margin), max(0, y0 - margin),
                      min(im.width, x1 + margin), min(im.height, y1 + margin)))
    return im


def fit(im, w, h):
    return ImageOps.contain(crop_white(im), (w, h), Image.LANCZOS)


def main():
    W = 3400
    M = 40
    GUTTER = 70
    GAP = 16
    cw = (W - 2 * M - GUTTER - 4 * GAP) // 5

    TITLE_H = 190
    HEAD_H = 116
    ROW1_H = 455
    ROW2_H = 430
    STATS_H = 180

    H = M + TITLE_H + HEAD_H + ROW1_H + ROW2_H + STATS_H + M
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)

    d.text((M, 28), "按桌面 g_mount_b.SLDASM 的 rev30 鞍座改：四种半封口",
           font=FONT_T, fill=(20, 20, 20))
    d.text((M, 94),
           "基础件就是桌面装配里的这个：40 × 74.5 × 29，16.57 cm³ / 20.5 g；"
           "不是项目里后来那个盒子。舵机身体 40 × 40 × 20 从后端沿 X 推进，"
           "所以后门框窗口最小 40.5 × 21；这里做成 44 × 21，左右各留 2 mm 走线。",
           font=FONT_S, fill=(60, 60, 60))
    d.text((M, 132),
           "侧墙内面在 Y ±23.69 / 76.69（离法兰边 0.5），从 X=12 起（避开法兰螺母），"
           "下沿 Z=19（避开 8 颗脚板螺丝）；四颗法兰螺栓仍在 X=0~11 原位。",
           font=FONT_S, fill=(60, 60, 60))

    y0 = M + TITLE_H
    d.text((M - 2, y0 + HEAD_H + ROW1_H // 2 - 14), "立体",
           font=FONT_R, fill=(90, 90, 90))
    d.text((M - 2, y0 + HEAD_H + ROW1_H + ROW2_H // 2 - 14), "俯视",
           font=FONT_R, fill=(90, 90, 90))

    for i, c in enumerate(COLS):
        x = M + GUTTER + i * (cw + GAP)
        d.text((x, y0 + 2), c["tag"], font=FONT_H, fill=(200, 50, 40))
        tw = d.textlength(c["tag"], font=FONT_H)
        d.text((x + tw + 12, y0 + 8), c["name"], font=FONT_H,
               fill=(20, 20, 20))
        d.text((x, y0 + 55), c["desc"], font=FONT_S, fill=(70, 70, 70))
        d.line([(x, y0 + HEAD_H - 8), (x + cw, y0 + HEAD_H - 8)],
               fill=(210, 210, 210), width=2)

        im = fit(Image.open(R / c["iso"]), cw, ROW1_H - 14)
        canvas.paste(im, (x + (cw - im.width) // 2,
                          y0 + HEAD_H + (ROW1_H - im.height) // 2))
        im2 = fit(Image.open(R / c["top"]), cw, ROW2_H - 12)
        canvas.paste(im2, (x + (cw - im2.width) // 2,
                           y0 + HEAD_H + ROW1_H + (ROW2_H - im2.height) // 2))

        sy = y0 + HEAD_H + ROW1_H + ROW2_H + 14
        d.rectangle([x, sy - 4, x + cw, sy + STATS_H - 46],
                    fill=(247, 248, 250), outline=(225, 227, 230), width=1)
        for j, line in enumerate(c["stats"]):
            d.text((x + 12, sy + 6 + j * 30), line, font=FONT_M,
                   fill=(45, 45, 45))

    d.text((M, H - 48),
           "体积/重量按 PLA 1.24 g/cm³；抗扭星级是定性排序，未做 FEA。"
           "后门框在 X 37.5~40，离最后一排脚板螺丝头 0.86 mm；窗口 44 × 21。"
           "倒角/圆角还没加；这轮只定“封到哪一档”。",
           font=FONT_M, fill=(90, 90, 90))

    canvas.save(OUT)
    print("saved", OUT, canvas.size)


if __name__ == "__main__":
    main()
