#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: a one-page newspaper front page
summing up the world news of Wednesday 25 November 2026.

Run: python3 make_image.py  -> writes entry.png (1024x1024, < 1 MiB)
Requires Pillow and the DejaVu fonts shipped with most Linux systems.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (163, 22, 33)
NAVY = (23, 48, 77)
SEA = (31, 78, 121)
GREY = (90, 86, 78)
LIGHT_LINE = (180, 172, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw a wrapped paragraph; returns the y below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading, fill=INK):
    return para(draw, x, y, text, fnt, max_w, leading, fill)


def kicker(draw, x, y, text, fnt=SANS_BOLD, size=17):
    f = font(fnt, size)
    draw.text((x, y), text, font=f, fill=RED)
    return y + size + 8


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_tanker_scene(draw, x0, y0, x1, y1):
    """Simple flat illustration: a tanker crossing a strait, a naval mine
    in the water ahead of it. All shapes, no photos."""
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    # sky band
    draw.rectangle([x0, y0, x1, y0 + 52], fill=(233, 226, 208))
    # sun
    cx, cy, r = x1 - 52, y0 + 30, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 164, 62))
    # distant shore
    draw.polygon([(x0, y0 + 52), (x0 + 90, y0 + 34), (x0 + 170, y0 + 52)],
                 fill=(120, 116, 100))
    # waves (kept clear of the caption strip at the bottom)
    for wy in (y0 + 104, y0 + 144, y0 + 182):
        for wx in range(x0 + 8, x1 - 30, 52):
            draw.arc([wx, wy, wx + 44, wy + 18], 0, 180,
                     fill=(255, 255, 255), width=3)
    # mine: spiked black sphere in the water, far left, clear of caption
    mx, my, mr = x0 + 40, y0 + 128, 15
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        draw.line([(mx + int(mr * 0.8 * math.cos(a)),
                    my + int(mr * 0.8 * math.sin(a))),
                   (mx + int((mr + 12) * math.cos(a)),
                    my + int((mr + 12) * math.sin(a)))],
                  fill=INK, width=3)
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    draw.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(60, 60, 60))
    # tanker: flat hull with containers sitting on its top edge
    hx0, hy0, hx1, hy1 = x0 + 112, y0 + 104, x1 - 14, y0 + 164
    draw.rectangle([hx0, hy0, hx1, hy1], fill=(28, 28, 30))
    draw.polygon([(hx1, hy0), (hx1 + 14, hy0 + 22), (hx1, hy1)],
                 fill=(28, 28, 30))
    draw.rectangle([hx0 + 8, hy0 - 30, hx0 + 96, hy0], fill=(200, 60, 48))
    draw.rectangle([hx0 + 102, hy0 - 30, hx0 + 158, hy0], fill=(232, 164, 62))
    draw.rectangle([hx0 + 164, hy0 - 30, hx0 + 196, hy0], fill=(240, 240, 235))
    # funnel at the stern (right end)
    draw.rectangle([hx1 - 40, hy0 - 52, hx1 - 6, hy0], fill=RED)
    draw.rectangle([hx1 - 40, hy0 - 52, hx1 - 6, hy0 - 38], fill=(240, 240, 235))
    # caption on a clear strip at the bottom of the scene
    draw.text((x0 + 4, y1 - 22), "A tanker in the Strait of Hormuz",
              font=font(SANS, 14), fill=(235, 235, 230))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36                      # side margin
    RX = W - MX                  # right edge

    # ---- masthead ---------------------------------------------------
    d.text((W // 2, 22), "THE WORLD IN ONE DAY",
           font=font(SERIF, 60), fill=INK, anchor="ma")
    d.text((W // 2, 92), "THE DAY'S NEWS  ·  ONE PAGE  ·  ONE PICTURE",
           font=font(SANS_BOLD, 15), fill=GREY, anchor="ma")

    # ---- date banner ------------------------------------------------
    d.rectangle([MX, 122, RX, 168], fill=RED)
    d.text((W // 2, 128), "WEDNESDAY  25  NOVEMBER  2026",
           font=font(SANS_BOLD, 32), fill=(255, 255, 255), anchor="ma")
    rule(d, MX, RX, 180, 3)

    # ---- lead story: Hormuz -----------------------------------------
    y = 196
    y = kicker(d, MX, y, "STRAIT OF HORMUZ  ·  LEAD STORY", size=18)
    y = headline(d, MX, y, "MINES IN THE STRAIT",
                 font(SERIF, 58), 600, 62)
    y = para(d, MX, y + 6,
             "Iran says oil tankers struck mines in the Strait of "
             "Hormuz; maritime monitors say the claim is "
             "unconfirmed. Brent crude holds near $91 a barrel.",
             font(SANS, 20), 600, 27)
    # illustration, right of the lead text
    draw_tanker_scene(d, 668, 196, RX, 424)

    rule(d, MX, RX, 440, 2)

    # ---- two-column row: Ukraine / Solomons -------------------------
    y = 458
    col_w = 452
    # Ukraine (left)
    yy = kicker(d, MX, y, "UKRAINE  ·  RUSSIA")
    yy = headline(d, MX, yy, "Drones hit two refineries deep in Russia",
                  font(SERIF, 30), col_w, 36)
    para(d, MX, yy + 4,
         "Syzran and Kuibyshev plants in Samara hit overnight; "
         "one killed. Putin vows retaliation is \u201cinevitable\u201d.",
         font(SANS, 18), col_w, 24)
    # Solomons (right)
    x2 = MX + col_w + 40
    yy = kicker(d, x2, y, "THE PACIFIC")
    yy = headline(d, x2, yy, "Solomons picks Australia, drops China pact",
                  font(SERIF, 30), col_w, 36)
    para(d, x2, yy + 4,
         "Treaty signed in Canberra: no foreign military bases. "
         "Australia becomes the security partner of choice.",
         font(SANS, 18), col_w, 24)

    rule(d, MX, RX, 652, 2)

    # ---- three-column row: CIA / markets / Senegal ------------------
    y = 670
    c3 = 292
    xs = [MX, MX + c3 + 22, MX + 2 * (c3 + 22)]
    # CIA
    yy = kicker(d, xs[0], y, "TECH  ·  SECURITY", size=16)
    yy = headline(d, xs[0], yy, "Hackers breach CIA open-source system",
                  font(SERIF, 27), c3, 33)
    para(d, xs[0], yy + 4,
         "NYT: the CIA, ODNI and the spy-satellite agency were "
         "hit. No classified data exposed; China suspected.",
         font(SANS, 17), c3, 23)
    # Markets
    yy = kicker(d, xs[1], y, "MARKETS", size=16)
    yy = headline(d, xs[1], yy, "Asia's AI stocks tumble",
                  font(SERIF, 27), c3, 33)
    para(d, xs[1], yy + 4,
         "Kospi \u22126%, Nikkei \u22122.8%, Taiwan \u22126% as the AI "
         "rally fizzles. Nvidia gives back 5.9%.",
         font(SANS, 17), c3, 23)
    # Senegal
    yy = kicker(d, xs[2], y, "SPORT", size=16)
    yy = headline(d, xs[2], yy, "Senegal get their Africa Cup back",
                  font(SERIF, 27), c3, 33)
    para(d, xs[2], yy + 4,
         "Sports court overturns the CAF ruling and restores "
         "Senegal's 1\u20130 final win over Morocco.",
         font(SANS, 17), c3, 23)

    rule(d, MX, RX, 890, 2)

    # ---- also today -------------------------------------------------
    y = 906
    d.text((MX, y), "ALSO TODAY", font=font(SANS_BOLD, 17), fill=RED)
    para(d, MX, y + 26,
         "Houthi drone hits a Riyadh tower, 11 hurt  \u00b7  "
         "Nor'easter threatens the Thanksgiving parade  \u00b7  "
         "Trump pardons turkeys Freedom and Feathers",
         font(SANS, 18), RX - MX, 25)

    # ---- footer -----------------------------------------------------
    d.text((W // 2, 988),
           "Every story happened or was first reported on "
           "Wednesday 25 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
