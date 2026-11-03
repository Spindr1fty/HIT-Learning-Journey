# Annotate g_mount_b with feature names and dimensions.
# ASCII only in code; Chinese labels come from Unicode escapes / font file.

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\IceCup")
OUT = ROOT / "renders" / "g_mount_b_annotated.png"
ISO = ROOT / "renders" / "g_mount_b_iso.png"
FRONT = ROOT / "renders" / "g_mount_b_front.png"
TOP = ROOT / "renders" / "g_mount_b_top.png"
LEFT = ROOT / "renders" / "g_mount_b_left.png"

# Feature data from src/g_mount_b.py
FEATURES = [
    # (label, detail)
    ("\u5e95\u677f FOOT", "40 \u00d7 92.5 \u00d7 5 mm  Z=9..14"),
    ("\u7acb\u67f1 POST 1", "Y 21.94..29.94  \u5bbd 8  \u9ad8 23"),
    ("\u7acb\u67f1 POST 2", "Y 70.44..78.44  \u5bbd 8  \u9ad8 23"),
    ("\u6865 BRIDGE", "Z 35..37  \u539a 2  \u8de8 40.5"),
    ("\u5b89\u88c5\u5b54 4\u00d7", "\u00d84.5  \u95f4\u8ddd 8.196  Y=19.94"),
    ("\u87ba\u9489\u5b54 4\u00d7", "\u00d84.5 \u901a\u5b54  Z=19 / 29"),
    ("\u52a0\u5f3a\u7b4b GUSSET", "\u817f 18  \u539a 5  45\u00b0"),
    ("\u5185\u4fa7\u53e3 POCKET", "\u6df1 1.6  \u9ad8 2.4  \u88c5\u8235\u673a\u51f8\u53f0"),
]


def font(size: int):
    for p in (
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def dim_h(draw, x0, x1, y, text, f, color=(30, 30, 30), tick=8):
    draw.line([(x0, y), (x1, y)], fill=color, width=2)
    for x in (x0, x1):
        draw.line([(x, y - tick), (x, y + tick)], fill=color, width=2)
    tw = draw.textlength(text, font=f)
    tx = (x0 + x1) / 2 - tw / 2
    ty = y - f.size - 4
    draw.rectangle([tx - 4, ty - 2, tx + tw + 4, ty + f.size + 2], fill=(255, 255, 255, 200))
    draw.text((tx, ty), text, font=f, fill=color)


def dim_v(draw, y0, y1, x, text, f, color=(30, 30, 30), tick=8):
    draw.line([(x, y0), (x, y1)], fill=color, width=2)
    for y in (y0, y1):
        draw.line([(x - tick, y), (x + tick, y)], fill=color, width=2)
    tw = draw.textlength(text, font=f)
    tx = x + 6
    ty = (y0 + y1) / 2 - f.size / 2
    draw.rectangle([tx - 4, ty - 2, tx + tw + 4, ty + f.size + 2], fill=(255, 255, 255, 200))
    draw.text((tx, ty), text, font=f, fill=color)


def leader(draw, xy, text_xy, text, f, color=(180, 40, 40)):
    draw.line([xy, text_xy], fill=color, width=2)
    r = 3
    draw.ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=color)
    tw = draw.textlength(text, font=f)
    x, y = text_xy
    draw.rectangle([x - 2, y - 2, x + tw + 4, y + f.size + 2], fill=(255, 255, 255, 230))
    draw.text((x, y), text, font=f, fill=color)


def main():
    iso = Image.open(ISO).convert("RGB")
    front = Image.open(FRONT).convert("RGB")
    top = Image.open(TOP).convert("RGB")
    left = Image.open(LEFT).convert("RGB")

    W, H = 1800, 1280
    canvas = Image.new("RGB", (W, H), (248, 248, 250))
    d = ImageDraw.Draw(canvas, "RGBA")

    f_title = font(36)
    f_h = font(22)
    f_b = font(18)
    f_s = font(15)

    d.text((40, 24), "g_mount_b  \u53d6\u58f6\u673a\u6784 \u5b89\u88c5\u5757 B", font=f_title, fill=(20, 20, 20))
    d.text((40, 72), "rev.7  layout B   |   40 \u00d7 92.5 \u00d7 28 mm   |   21.58 cm\u00b3   |   ~27 g PLA",
           font=f_h, fill=(80, 80, 80))

    # --- hero ISO ---
    hero_w, hero_h = 820, 620
    hero = iso.resize((hero_w, hero_h), Image.Resampling.LANCZOS)
    canvas.paste(hero, (40, 110))
    d.rectangle([40, 110, 40 + hero_w, 110 + hero_h], outline=(180, 180, 180), width=1)

    ox, oy = 40, 110
    # callouts on ISO (approximate screen anchors)
    leader(d, (ox + 220, oy + 480), (ox + 30, oy + 520),
           "\u5e95\u677f FOOT  40\u00d792.5\u00d75", f_b)
    leader(d, (ox + 280, oy + 220), (ox + 500, oy + 80),
           "\u7acb\u67f1 POST  8\u00d75\u00d723", f_b)
    leader(d, (ox + 360, oy + 120), (ox + 560, oy + 40),
           "\u6865 BRIDGE  \u539a 2", f_b)
    leader(d, (ox + 250, oy + 380), (ox + 520, oy + 300),
           "\u5b89\u88c5\u5b54 4\u00d7\u00d84.5  pitch 8.196", f_b)
    leader(d, (ox + 180, oy + 300), (ox + 20, oy + 200),
           "\u87ba\u9489\u5b54 4\u00d7\u00d84.5 \u901a\u5b54", f_b)
    leader(d, (ox + 150, oy + 420), (ox + 20, oy + 360),
           "45\u00b0 \u52a0\u5f3a\u7b4b  \u817f 18", f_b)

    # --- right column: feature list ---
    rx = 900
    d.rectangle([rx, 110, W - 30, 730], fill=(255, 255, 255), outline=(200, 200, 200))
    d.text((rx + 20, 125), "\u90e8\u4ef6\u4e0e\u5c3a\u5bf8", font=f_h, fill=(20, 20, 20))
    y = 170
    for name, detail in FEATURES:
        d.rectangle([rx + 20, y + 4, rx + 28, y + 22], fill=(200, 60, 60))
        d.text((rx + 40, y), name, font=f_b, fill=(20, 20, 20))
        d.text((rx + 40, y + 26), detail, font=f_s, fill=(90, 90, 90))
        y += 68

    # --- bottom: orthographic ---
    by = 750
    d.text((40, by), "\u6295\u5f71\u89c6\u56fe  |  Orthographic", font=f_h, fill=(20, 20, 20))

    # front (Y-Z)
    fw, fh = 700, 420
    front_s = front.resize((fw, fh), Image.Resampling.LANCZOS)
    canvas.paste(front_s, (40, by + 40))
    d.rectangle([40, by + 40, 40 + fw, by + 40 + fh], outline=(180, 180, 180))
    d.text((50, by + 48), "\u524d\u89c6  (Y-Z)", font=f_s, fill=(180, 40, 40))

    # dimension on front-like schematic below/around
    dim_h(d, 50, 50 + 620, by + 40 + fh + 18,
          "\u603b\u957f Y = 92.5  (\u5e95\u677f)", f_s)
    dim_v(d, by + 50, by + 50 + 340, 30,
          "\u603b\u9ad8 Z = 28", f_s)

    # top (X-Y)
    tw, th = 700, 320
    top_s = top.resize((tw, th), Image.Resampling.LANCZOS)
    canvas.paste(top_s, (780, by + 40))
    d.rectangle([780, by + 40, 780 + tw, by + 40 + th], outline=(180, 180, 180))
    d.text((790, by + 48), "\u4fef\u89c6  (X-Y)", font=f_s, fill=(180, 40, 40))
    dim_h(d, 790, 790 + 620, by + 40 + th + 18,
          "\u603b\u5bbd X = 40", f_s)

    # left side view small
    lw, lh = 360, 280
    left_s = left.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(left_s, (780, by + 40 + th + 50))
    d.rectangle([780, by + 40 + th + 50, 780 + lw, by + 40 + th + 50 + lh], outline=(180, 180, 180))
    d.text((790, by + 40 + th + 58), "\u5de6\u89c6  (X-Z)", font=f_s, fill=(180, 40, 40))

    # key dimensions block
    kx, ky = 40, by + 40 + fh + 40
    d.rectangle([kx, ky, 740, ky + 150], fill=(255, 255, 255), outline=(200, 200, 200))
    d.text((kx + 16, ky + 10), "\u5173\u952e\u5c3a\u5bf8\u6e05\u5355", font=f_h, fill=(20, 20, 20))
    lines = [
        "\u5e95\u677f 40 \u00d7 92.5 \u00d7 5    \u7acb\u67f1 5 \u00d7 8 \u00d7 23 \u00d7 2 \u6839    \u6865 \u539a 2  \u5f00\u53e3 21",
        "\u5b89\u88c5\u5b54 4\u00d7\u00d84.5  pitch 8.196  Y=19.94  \u87ba\u9489\u5b54 4\u00d7\u00d84.5  Z=19/29",
        "\u7b4b\u817f 18 \u00d7 \u539a 5   \u5185\u53e3\u53e3 \u6df11.6 \u00d7 \u9ad82.4   \u603b\u5305\u7edc 40\u00d792.5\u00d728",
    ]
    yy = ky + 48
    for ln in lines:
        d.text((kx + 16, yy), ln, font=f_s, fill=(50, 50, 50))
        yy += 28

    canvas.save(OUT)
    print("wrote", OUT, canvas.size)


if __name__ == "__main__":
    main()
