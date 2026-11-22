#!/usr/bin/env python3
"""Draw a newspaper front page summing up Saturday 21 November 2026.

Six stories, every one verified against reputable outlets (Reuters, AP,
Al Jazeera, The Hindu, The Straits Times) on 21-22 November 2026. The page
is drawn entirely with Pillow: masthead, headlines, decks and six small
flat illustrations. No photographs, no AI images, no network. Output is
deterministic: the same bytes on every run.
"""

import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (248, 243, 232)
INK = (22, 22, 22)
ACCENT = (178, 58, 44)
NAVY = (28, 74, 118)
TEAL = (52, 108, 142)
MUSTARD = (198, 158, 38)
MUTED = (96, 96, 96)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def split_lines(canvas, text, face, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    words = text.split()
    out, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def text_block(canvas, x, y, text, face, width, colour=INK, spacing=None):
    gap = spacing if spacing is not None else int(face.size * 1.3)
    for line in split_lines(canvas, text, face, width):
        canvas.text((x, y), line, font=face, fill=colour)
        y += gap
    return y


def section_head(canvas, x, y, label, size=20):
    face = load(SANS_BOLD, size)
    canvas.text((x, y), label, font=face, fill=ACCENT)
    return y + int(size * 1.55)


def big_headline(canvas, x, y, text, size, width, colour=INK):
    face = load(SERIF_BOLD, size)
    return text_block(canvas, x, y, text, face, width, colour=colour,
                      spacing=int(size * 1.14))


def hline(canvas, x0, y, x1, thick=2, colour=INK):
    canvas.line([(x0, y), (x1, y)], fill=colour, width=thick)


# ---------------------------------------------------------------- art panels

def panel_wanted(d, x0, y0, x1, y1):
    """A wanted poster: star badge, reward, FBI Top 10 tag."""
    d.rectangle([x0, y0, x1, y1], fill=(232, 214, 178),
                outline=INK, width=3)
    d.rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 8], outline=INK, width=2)
    cx = (x0 + x1) // 2
    cy = y0 + 74
    # five-point star badge
    import math
    outer, inner = 52, 21
    pts = []
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        ang = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=MUSTARD, outline=INK, width=2)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=PAPER,
              outline=INK, width=2)
    face = load(SANS_BOLD, 34)
    word = "WANTED"
    d.text((cx - d.textlength(word, font=face) / 2, y0 + 138), word,
           font=face, fill=INK)
    face2 = load(SANS_BOLD, 26)
    reward = "$5,000,000 REWARD"
    d.text((cx - d.textlength(reward, font=face2) / 2, y0 + 182), reward,
           font=face2, fill=ACCENT)
    face3 = load(SANS_BOLD, 20)
    tag = "FBI TOP 10 MOST WANTED"
    d.text((cx - d.textlength(tag, font=face3) / 2, y0 + 218), tag,
           font=face3, fill=INK)


def panel_rubble(d, x0, y0, x1, y1):
    """Broken city blocks under a grey sky, red-cross aid tent."""
    d.rectangle([x0, y0, x1, y1], fill=(62, 66, 76))
    for i in range(14):
        sx = x0 + (i * 53) % (x1 - x0)
        sy = y0 + (i * 41) % (y1 - y0)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 200, 210))
    base = y1 - 8
    # jagged broken towers, kept inside the panel
    pw = x1 - x0
    towers = [(6, 66), (38, 96), (70, 52), (102, 88)]
    for off, th in towers:
        tx = x0 + off
        tw = 26
        top = base - th
        d.polygon([(tx, base), (tx, top + 14), (tx + 8, top),
                   (tx + 16, top + 10), (tx + tw, top + 4),
                   (tx + tw, base)], fill=(38, 38, 46))
        d.rectangle([tx + 5, top + 26, tx + 13, top + 36],
                    fill=(240, 190, 60))
    # smoke
    for sx, sy, r in ((x0 + 40, y0 + 26, 12), (x0 + 90, y0 + 16, 10),
                      (x0 + 120, y0 + 30, 11)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 158))
    # aid tent with red cross, bottom right
    tx0, ty0 = x1 - 84, y1 - 46
    d.polygon([(tx0, ty0 + 38), (tx0 + 42, ty0), (tx0 + 84, ty0 + 38)],
              fill=(250, 250, 250), outline=INK, width=2)
    d.rectangle([tx0 + 34, ty0 + 12, tx0 + 50, ty0 + 28], fill=ACCENT)
    d.rectangle([tx0 + 38, ty0 + 8, tx0 + 46, ty0 + 32], fill=ACCENT)


def panel_climate(d, x0, y0, x1, y1):
    """A globe beside a clock running past twelve: overtime."""
    d.rectangle([x0, y0, x1, y1], fill=(216, 232, 238))
    cx, cy, r = x0 + 78, y0 + 62, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 130, 190),
              outline=NAVY, width=3)
    d.ellipse([cx - 30, cy - 34, cx - 2, cy - 8], fill=(96, 168, 96))
    d.ellipse([cx + 4, cy + 6, cx + 34, cy + 34], fill=(96, 168, 96))
    d.ellipse([cx - 8, cy - 40, cx + 22, cy - 18], fill=(96, 168, 96))
    # clock, hands past the hour
    kx, ky, kr = x1 - 74, y0 + 62, 46
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=PAPER,
              outline=INK, width=3)
    d.line([(kx, ky), (kx, ky - kr + 8)], fill=INK, width=4)
    d.line([(kx, ky), (kx + kr - 14, ky + 10)], fill=ACCENT, width=4)
    d.ellipse([kx - 4, ky - 4, kx + 4, ky + 4], fill=INK)
    face = load(SANS_BOLD, 22)
    word = "OVERTIME"
    d.text(((x0 + x1) / 2 - d.textlength(word, font=face) / 2, y1 - 34),
           word, font=face, fill=ACCENT)


def panel_storm(d, x0, y0, x1, y1):
    """Spiral cyclone over a pale sea, coast strip at the bottom."""
    d.rectangle([x0, y0, x1, y1], fill=(210, 228, 236))
    cx, cy = (x0 + x1) // 2 + 24, (y0 + y1) // 2 - 2
    max_r = min((y1 - y0) // 2 - 6, 34)
    step = max(6, max_r // 4)
    for radius in range(max_r, 4, -step):
        start = 210 - radius * 4
        d.arc([cx - radius, cy - radius, cx + radius, cy + radius],
              start, start + 295, fill=TEAL, width=5)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=PAPER,
              outline=TEAL, width=3)
    d.polygon([(x0, y1), (x0, y1 - 18), (x0 + 110, y1 - 30),
               (x0 + 170, y1 - 18), (x0 + 190, y1)],
              fill=(198, 180, 138))
    face = load(SANS_BOLD, 14)
    d.text((x0 + 8, y0 + 4), "BAY OF BENGAL", font=face,
           fill=(38, 78, 108))


def panel_mosquito(d, x0, y0, x1, y1):
    """A big flat mosquito over a pale green field, wings spread."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 236, 214))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 6
    # wings
    d.ellipse([cx - 58, cy - 26, cx - 6, cy - 2], fill=(255, 255, 255),
              outline=(140, 170, 150), width=2)
    d.ellipse([cx + 6, cy - 26, cx + 58, cy - 2], fill=(255, 255, 255),
              outline=(140, 170, 150), width=2)
    # legs
    for lx, ly, dx in ((-22, 8, -28), (-7, 11, -10), (8, 11, 12),
                       (24, 8, 30)):
        d.line([(cx + lx, cy + ly), (cx + lx + dx, cy + 26)],
               fill=INK, width=3)
    # body and head
    d.ellipse([cx - 11, cy - 12, cx + 11, cy + 18], fill=(52, 52, 52))
    d.ellipse([cx - 8, cy - 22, cx + 8, cy - 10], fill=(38, 38, 38))
    d.ellipse([cx - 4, cy - 19, cx - 1, cy - 16], fill=(255, 80, 80))
    d.ellipse([cx + 1, cy - 19, cx + 4, cy - 16], fill=(255, 80, 80))
    # proboscis
    d.line([(cx, cy - 20), (cx + 3, cy - 32)], fill=INK, width=3)
    # stripes
    for sy in (-4, 4, 12):
        d.line([(cx - 10, cy + sy), (cx + 10, cy + sy)],
               fill=(200, 200, 200), width=2)
    face = load(SANS_BOLD, 13)
    d.text((x0 + 8, y1 - 18), "WOLBACHIA", font=face, fill=(40, 90, 50))


def panel_calendar(d, x0, y0, x1, y1):
    """A small calendar page: 2027 header, big 1 January."""
    d.rectangle([x0, y0, x1, y1], fill=(240, 236, 226))
    d.rectangle([x0 + 14, y0 + 8, x1 - 14, y1 - 8], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([x0 + 14, y0 + 8, x1 - 14, y0 + 30], fill=ACCENT)
    face = load(SANS_BOLD, 15)
    word = "2027"
    d.text(((x0 + x1) / 2 - d.textlength(word, font=face) / 2, y0 + 11),
           word, font=face, fill=(255, 255, 255))
    face2 = load(SERIF_BOLD, 22)
    num = "1"
    d.text(((x0 + x1) / 2 - d.textlength(num, font=face2) / 2, y0 + 30),
           num, font=face2, fill=INK)


# ------------------------------------------------------------------- page

def build_page():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    left, right = 30, CANVAS_W - 30

    # masthead
    title_face = load(SERIF_BOLD, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_face)
    d.text(((CANVAS_W - tw) / 2, 22), title, font=title_face, fill=INK)
    hline(d, left, 102, right, 3)
    date_face = load(SANS_BOLD, 27)
    d.text((left, 112), "SATURDAY  ·  21 NOVEMBER 2026", font=date_face,
           fill=ACCENT)
    side_face = load(SANS_BOLD, 21)
    side = "SIX STORIES  ·  ONE DAY"
    d.text((right - d.textlength(side, font=side_face), 116), side,
           font=side_face, fill=INK)
    hline(d, left, 150, right, 2)

    # ---- lead story: Mexico (168..424) ----
    y = 168
    y = section_head(d, left, y, "MEXICO  ·  SECURITY", 20)
    y = big_headline(d, left, y, "MEXICO CAPTURES \u2018EL CHAPO ISIDRO\u2019",
                     36, 560)
    text_block(d, left, y + 8,
               "FBI most-wanted cartel boss Fausto Isidro Meza Flores "
               "seized in a Sinaloa raid on Friday night. Four soldiers "
               "and seven gunmen were killed as cartel roadblocks burned.",
               load(SANS, 22), 560, spacing=29)
    panel_wanted(d, 622, 168, right, 424)
    hline(d, left, 428, right, 2)

    # ---- middle row (440..708): Ukraine | COP31 ----
    y = 440
    half = CANVAS_W // 2
    yy = section_head(d, left, y, "UKRAINE  ·  WAR", 19)
    yy = big_headline(d, left, yy,
                      "MISSILES HIT ZELENSKYY\u2019S HOMETOWN \u2014 THEN "
                      "THE RESCUERS", 27, 464)
    panel_rubble(d, left, yy + 6, left + 150, yy + 102)
    text_block(d, left + 164, yy + 10,
               "A Russian \u2018triple-tap\u2019 strike on Kryvyi Rih kills "
               "a boy of 7 and a paramedic, 20, and wounds 60. Follow-up "
               "missiles hit the rescue crews.",
               load(SANS, 19), 300, spacing=25)
    yy2 = section_head(d, half + 18, y, "CLIMATE  ·  COP31", 19)
    yy2 = big_headline(d, half + 18, yy2, "COP31 RUNS INTO OVERTIME", 27,
                       446)
    panel_climate(d, half + 18, yy2 + 6, right, yy2 + 96)
    text_block(d, half + 18, yy2 + 104,
               "Talks in Antalya miss their Friday deadline with no deal. "
               "The draft drops fossil fuels and a $120bn adaptation "
               "fund.",
               load(SANS, 18), 446, spacing=23)
    hline(d, left, 708, right, 2)

    # ---- bottom row (724..962): three columns ----
    y = 724
    cols = [(left, 311), (left + 326, 311), (left + 652, 311)]
    x, w = cols[0]
    yy = section_head(d, x, y, "INDIA  ·  WEATHER", 18)
    yy = big_headline(d, x, yy, "CYCLONE AKVAN FADES", 25, w)
    panel_storm(d, x, yy + 4, x + w, yy + 68)
    text_block(d, x, yy + 76,
               "Landfall near Gopalpur on Friday; Akvan weakens to a "
               "depression. No major damage; 440,000 moved to safety.",
               load(SANS, 17), w, spacing=21)
    x, w = cols[1]
    yy = section_head(d, x, y, "SCIENCE  ·  HEALTH", 18)
    yy = big_headline(d, x, yy, "MOSQUITOES THAT BEAT DENGUE", 25, w)
    panel_mosquito(d, x, yy + 4, x + w, yy + 68)
    text_block(d, x, yy + 76,
               "Wolbachia mosquitoes cut dengue and chikungunya "
               "infections about 69% in a four-year trial of 5,700 "
               "Brazilian children.",
               load(SANS, 17), w, spacing=21)
    x, w = cols[2]
    yy = section_head(d, x, y, "TRUMP  ·  IRAN", 18)
    yy = big_headline(d, x, yy, "NO IRAN CALL UNTIL NEW YEAR", 25, w)
    panel_calendar(d, x, yy + 4, x + w, yy + 68)
    text_block(d, x, yy + 76,
               "He will not decide on new strikes on Iran until after "
               "the new year, as Israel presses for a joint campaign.",
               load(SANS, 17), w, spacing=21)

    # ---- footer ----
    hline(d, left, 970, right, 2)
    foot = load(SANS, 15)
    line1 = ("Sources: Reuters, AP, Al Jazeera, The Hindu, "
             "The Straits Times, The Times of India.")
    line2 = "Drawn programmatically with Python + PIL; no photographs."
    for i, s in enumerate((line1, line2)):
        sw = d.textlength(s, font=foot)
        d.text(((CANVAS_W - sw) / 2, 978 + i * 19), s, font=foot,
               fill=MUTED)
    return img


def main():
    img = build_page()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
