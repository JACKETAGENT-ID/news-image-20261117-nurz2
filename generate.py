#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261117 (nurz v2 upgrade).

Concept: "One Day, One Bridge" -- a dramatic vertical poster.
Top 2/3: the Kerch Bridge burning at dusk, drones in the sky.
Bottom 1/3: four small captioned vignettes (Hormuz tanker, Shenzhen trio,
Estonia border gate, Japan jets) plus a ticker of the day's other stories.
All facts are the verified events of Tuesday 17 November 2026.
Drawn entirely with PIL primitives; no external images.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = font("DejaVuSans-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_HERO = font("DejaVuSans-Bold.ttf", 30)
F_CAP = font("DejaVuSans-Bold.ttf", 19)
F_CAP2 = font("DejaVuSans.ttf", 19)
F_TICK = font("DejaVuSans-Bold.ttf", 20)

NAVY = (13, 27, 46)
GOLD = (245, 178, 66)
WHITE = (255, 255, 255)
INK = (18, 22, 30)

random.seed(17112026)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        c = lerp(top, bottom, (y - y0) / h)
        img_draw = ImageDraw.Draw(img)
        img_draw.line([(x0, y), (x1, y)], fill=c)


def text_center(d, cx, y, s, f, fill, spacing=0):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)
    return w


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_drone(d, cx, cy, s=1.0):
    """Small quadcopter silhouette."""
    body = (int(26 * s), int(10 * s))
    d.ellipse([cx - body[0] // 2, cy - body[1] // 2,
               cx + body[0] // 2, cy + body[1] // 2], fill=(20, 20, 26))
    arm = int(34 * s)
    for dx in (-1, 1):
        d.line([(cx, cy), (cx + dx * arm, cy - int(14 * s))],
               fill=(20, 20, 26), width=max(2, int(3 * s)))
        rx = cx + dx * arm
        d.line([(rx - int(16 * s), cy - int(16 * s)),
                (rx + int(16 * s), cy - int(16 * s))],
               fill=(40, 40, 48), width=max(2, int(2 * s)))
    d.ellipse([cx - 3, cy + body[1] // 2 - 2, cx + 3, cy + body[1] // 2 + 8],
              fill=(255, 120, 40))


def flame(d, cx, base_y, h, w):
    """Stylised flame: layered triangles + glow dots."""
    for i, (col, hh, ww) in enumerate([
            ((255, 122, 26), h, w),
            ((255, 190, 60), int(h * 0.72), int(w * 0.66)),
            ((255, 235, 150), int(h * 0.45), int(w * 0.38))]):
        pts = [(cx - ww // 2, base_y), (cx + ww // 2, base_y),
               (cx + ww // 6, base_y - hh), (cx - ww // 8, base_y - hh)]
        d.polygon(pts, fill=col)
    for _ in range(6):
        r = random.randint(2, 5)
        ex = cx + random.randint(-w // 2, w // 2)
        ey = base_y - random.randint(0, h)
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 200, 90))


def smoke(img, cx, cy, scale=1.0):
    """Soft grey smoke plume on its own layer, blurred."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    puffs = [(0, 0, 46), (-30, -34, 38), (28, -40, 40), (-8, -72, 34),
             (18, -100, 28), (-22, -118, 24), (4, -140, 20)]
    for dx, dy, r in puffs:
        r = int(r * scale)
        ld.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                   fill=(120, 118, 122, 150))
    layer = layer.filter(ImageFilter.GaussianBlur(14))
    rgba = img.convert("RGBA")
    rgba.alpha_composite(layer)
    img.paste(rgba.convert("RGB"), (0, 0))


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.line([(0, 104), (W, 104)], fill=GOLD, width=4)
    text_center(d, W // 2, 8, "ONE DAY, ONE BRIDGE", F_TITLE, WHITE)
    text_center(d, W // 2, 68, "TUESDAY 17 NOVEMBER 2026", F_DATE, GOLD)

    # ---- Hero: dusk sky over the sea ------------------------------------
    HY0, HY1 = 108, 668
    vgrad(img, (0, HY0, W, HY1), (43, 27, 74), (232, 106, 51))
    # low sun glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W // 2 - 150, 470 - 150, W // 2 + 150, 470 + 150],
               fill=(255, 190, 90, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    # sun disc low on the horizon
    d.ellipse([W // 2 - 62, 470 - 62, W // 2 + 62, 470 + 62],
              fill=(255, 214, 130))
    # sea
    d.rectangle([0, 520, W, HY1], fill=(20, 50, 74))
    for y in range(524, HY1, 14):
        d.line([(0, y), (W, y)], fill=(32, 78, 110), width=2)
    # sun reflection on water
    for i, wdt in enumerate([150, 110, 80, 55, 36]):
        y = 532 + i * 24
        d.line([(W // 2 - wdt // 2, y), (W // 2 + wdt // 2, y)],
               fill=(255, 190, 100), width=5)

    # ---- Kerch Bridge ----------------------------------------------------
    deck_y = 470
    # arch span
    d.arc([90, 300, 934, 640], start=200, end=340, fill=(24, 24, 34), width=14)
    # deck
    d.rectangle([40, deck_y, 984, deck_y + 14], fill=(24, 24, 34))
    # pillars
    for px in (150, 330, 700, 880):
        d.rectangle([px - 9, deck_y + 14, px + 9, 560], fill=(24, 24, 34))
    # suspension cables
    for cx in (210, 300, 390, 640, 730, 820):
        d.line([(cx, deck_y), (cx - 40, 340)], fill=(40, 40, 52), width=3)
    # damaged gap in the deck, right of centre
    gap_x0, gap_x1 = 560, 640
    d.rectangle([gap_x0, deck_y, gap_x1, deck_y + 14], fill=(232, 106, 51))
    # flames + smoke at the gap
    flame(d, 600, deck_y + 6, 120, 90)
    flame(d, 575, deck_y + 6, 80, 55)
    smoke(img, 600, deck_y - 90, 1.15)
    d = ImageDraw.Draw(img)
    # drones in the sky
    for cx, cy, s in [(180, 210, 1.0), (300, 165, 0.8), (850, 190, 1.1),
                      (760, 250, 0.7), (420, 250, 0.65)]:
        draw_drone(d, cx, cy, s)

    # hero caption band
    d.rectangle([0, 592, W, HY1], fill=(10, 16, 28))
    text_center(d, W // 2, 602,
                "KERCH BRIDGE HIT FOR A SECOND DAY", F_HERO, (255, 214, 130))
    text_center(d, W // 2, 636,
                "Ukraine strikes the Crimea link — Russia hits Kyiv bridges",
                F_CAP2, WHITE)

    # ---- Vignette strip: four small stories ------------------------------
    VY0, VY1 = 668, 928
    d.rectangle([0, VY0, W, VY1], fill=(240, 238, 232))
    pw, gap = 244, 16
    panels = [
        ("tanker", "TANKER MINED", "NEAR HORMUZ"),
        ("shenzhen", "XI–TRUMP–PUTIN", "MEET IN SHENZHEN, 19 NOV"),
        ("estonia", "ESTONIA TO SHUT", "RUSSIA BORDER, 1 DEC"),
        ("jets", "JAPAN SCRAMBLES", "JETS OVER RUSSIAN PLANES"),
    ]
    for i, (kind, l1, l2) in enumerate(panels):
        x0 = gap + i * (pw + gap)
        x1 = x0 + pw
        # mini scene
        sy0, sy1 = VY0 + 10, VY0 + 132
        if kind == "tanker":
            d.rectangle([x0, sy0, x1, sy1], fill=(28, 68, 96))
            d.rectangle([x0, sy1 - 34, x1, sy1], fill=(16, 44, 66))
            d.polygon([(x0 + 30, sy1 - 40), (x0 + 214, sy1 - 40),
                       (x0 + 200, sy1 - 12), (x0 + 44, sy1 - 12)],
                      fill=(120, 40, 30))
            d.rectangle([x0 + 90, sy1 - 78, x0 + 120, sy1 - 40],
                        fill=(150, 60, 40))
            flame(d, x0 + 150, sy1 - 78, 46, 40)
            d.ellipse([x0 + 168, sy1 - 108, x0 + 196, sy1 - 80],
                      fill=(200, 200, 200))
        elif kind == "shenzhen":
            d.rectangle([x0, sy0, x1, sy1], fill=(52, 40, 84))
            for bx, bh in [(x0 + 18, 60), (x0 + 66, 92), (x0 + 118, 74),
                           (x0 + 168, 100), (x0 + 208, 58)]:
                d.rectangle([bx, sy1 - bh, bx + 34, sy1], fill=(24, 22, 44))
            for bx, bh in [(x0 + 18, 60), (x0 + 66, 92), (x0 + 118, 74),
                           (x0 + 168, 100), (x0 + 208, 58)]:
                for wy in range(sy1 - bh + 8, sy1 - 6, 12):
                    d.rectangle([bx + 8, wy, bx + 14, wy + 5],
                                fill=(255, 210, 110))
            for fx, col in [(x0 + 46, (200, 60, 60)), (x0 + 122, (40, 90, 200)),
                            (x0 + 198, (240, 240, 240))]:
                d.rectangle([fx - 16, sy0 + 8, fx + 16, sy0 + 30], fill=col)
                d.ellipse([fx - 5, sy0 + 36, fx + 5, sy0 + 46], fill=col)
        elif kind == "estonia":
            d.rectangle([x0, sy0, x1, sy1], fill=(70, 84, 96))
            d.rectangle([x0, sy1 - 30, x1, sy1], fill=(52, 60, 66))
            # gate posts + striped barrier
            d.rectangle([x0 + 24, sy0 + 18, x0 + 36, sy1 - 30], fill=(30, 34, 40))
            d.rectangle([x0 + 208, sy0 + 18, x0 + 220, sy1 - 30],
                        fill=(30, 34, 40))
            for j in range(6):
                col = (220, 60, 50) if j % 2 == 0 else (245, 245, 245)
                bx0 = x0 + 36 + j * 29
                d.rectangle([bx0, sy0 + 34, bx0 + 29, sy0 + 52], fill=col)
            d.rectangle([x0 + 36, sy0 + 52, x0 + 208, sy0 + 60],
                        fill=(30, 34, 40))
            d.polygon([(x0 + 122, sy1 - 118), (x0 + 152, sy1 - 118),
                       (x0 + 152, sy1 - 66), (x0 + 122, sy1 - 66)],
                      fill=(245, 245, 245))
            d.text((x0 + 128, sy1 - 108), "✕", font=F_CAP, fill=(200, 60, 50))
        else:  # jets
            d.rectangle([x0, sy0, x1, sy1], fill=(140, 180, 210))
            for cy in (sy0 + 26, sy0 + 62, sy0 + 96):
                d.ellipse([x0 + 20, cy, x0 + 60, cy + 10], fill=(255, 255, 255))
            # jet silhouette, nose right
            jx, jy = x0 + 122, sy0 + 66
            d.polygon([(jx - 88, jy - 5), (jx + 52, jy - 8), (jx + 88, jy),
                       (jx + 52, jy + 8), (jx - 88, jy + 5)], fill=(40, 48, 58))
            d.polygon([(jx - 22, jy - 6), (jx + 18, jy - 44), (jx + 30, jy - 6)],
                      fill=(40, 48, 58))
            d.polygon([(jx - 22, jy + 6), (jx + 18, jy + 44), (jx + 30, jy + 6)],
                      fill=(40, 48, 58))
            d.polygon([(jx - 88, jy - 5), (jx - 62, jy - 26), (jx - 56, jy - 5)],
                      fill=(40, 48, 58))
            d.line([(jx - 88, jy), (jx - 122, jy)], fill=(230, 230, 230),
                   width=3)
        # captions (line 2 wrapped so nothing overflows its panel)
        text_center(d, (x0 + x1) // 2, sy1 + 8, l1, F_CAP, INK)
        cy = sy1 + 34
        for ln in wrap(d, l2, F_CAP2, pw - 8):
            text_center(d, (x0 + x1) // 2, cy, ln, F_CAP2, INK)
            cy += 24

    # ---- Footer ticker -----------------------------------------------------
    d.rectangle([0, 928, W, H], fill=NAVY)
    d.line([(0, 928), (W, 928)], fill=GOLD, width=3)
    tick = ("ALSO: IRAN DRONE AT US RADAR BASE IN BAHRAIN  •  "
            "UK SANCTIONS 8 ISRAELI BUILDERS  •  HOUTHIS ADVANCE ON ADEN")
    lines = wrap(d, tick, F_TICK, W - 40)
    y = 940
    for ln in lines:
        text_center(d, W // 2, y, ln, F_TICK, (210, 215, 225))
        y += 26

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
