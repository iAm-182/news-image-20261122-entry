#!/usr/bin/env python3
"""news-image-20261122 v1 — early-edition front page for Sunday 22 Nov 2026.

Original newspaper front page drawn with PIL primitives only. No photos,
no downloaded images, no external assets. Every story on the page happened,
or was first reported, on Sunday 22 November 2026 (any time zone), verified
against live reporting on the morning of 22 Nov 2026 (02:30 UTC). Stories
that looked like today's news but were not are named in the DATE CHECK box
at the bottom instead of being printed as news.

Run:  python3 draw.py   ->   writes entry.png (1024x1024) next to this file.
Deterministic: two runs write identical bytes (no randomness, no network,
no timestamps inside the image beyond the fixed edition line).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (24, 24, 24)
RED = (158, 28, 34)
NAVY = (20, 38, 62)
NAVY2 = (14, 30, 50)
GOLD = (184, 134, 42)
GREY = (96, 93, 86)
LINE = (58, 56, 50)
CREAM = (238, 230, 212)
TAN = (214, 198, 160)
WHITE = (250, 248, 242)
SKY = (196, 219, 238)
TEAL = (18, 110, 106)
GREEN = (46, 110, 72)
ORANGE = (222, 110, 20)

F_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, width):
    """Greedy word wrap to the given pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, width, fill=INK, leading=None):
    """Draw wrapped paragraph; return y after the last line."""
    if leading is None:
        leading = int(f.size * 1.28)
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def headline(d, x, y, text, f, width, fill=INK, leading=None):
    return para(d, x, y, text, f, width, fill=fill, leading=leading)


def kicker(d, x, y, text, fill=RED):
    f = font(F_SANS_B, 17)
    d.text((x, y), text.upper(), font=f, fill=fill)
    return y + 24


def rule(d, x0, y, x1, width=2, fill=LINE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_ballot(d, x, y, s):
    """Simple ballot box with a ballot paper going in."""
    d.rectangle([x, y + s * 0.35, x + s, y + s], fill=NAVY, outline=INK, width=3)
    d.rectangle([x + s * 0.12, y + s * 0.30, x + s * 0.88, y + s * 0.44],
                fill=INK)
    d.polygon([(x + s * 0.30, y), (x + s * 0.62, y),
               (x + s * 0.56, y + s * 0.34), (x + s * 0.36, y + s * 0.34)],
              fill=WHITE, outline=INK)
    d.line([(x + s * 0.40, y + s * 0.08), (x + s * 0.48, y + s * 0.16),
            (x + s * 0.56, y + s * 0.02)], fill=RED, width=4)
    d.text((x + s * 0.30, y + s * 0.58), "VOTE", font=font(F_SANS_B, 22),
           fill=WHITE)


def draw_sun(d, x, y, s):
    """Sun half-hidden behind a cloud: the climate talks drag on."""
    cx, cy, r = x + s * 0.42, y + s * 0.42, int(s * 0.30)
    for dx, dy in [(0, -r - 8), (0, r + 8), (-r - 8, 0), (r + 8, 0)]:
        d.line([(cx + dx * 0.55, cy + dy * 0.55), (cx + dx, cy + dy)],
               fill=ORANGE, width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE, outline=INK,
              width=2)
    d.ellipse([x + s * 0.45, y + s * 0.55, x + s * 1.05, y + s * 0.92],
              fill=WHITE, outline=INK, width=2)
    d.ellipse([x + s * 0.30, y + s * 0.62, x + s * 0.75, y + s * 0.95],
              fill=WHITE, outline=INK, width=2)


def draw_ship(d, x, y, w, h):
    """Cargo ship with smoke and flame, listing in the Gulf of Finland."""
    sea_y = y + h - 18
    d.rectangle([x, sea_y, x + w, sea_y + 14], fill=SKY)
    for i in range(5):
        wx = x + 10 + i * (w // 5)
        d.arc([wx, sea_y - 4, wx + 26, sea_y + 8], 180, 360, fill=NAVY, width=2)
    # hull
    d.polygon([(x + 8, y + h * 0.55), (x + w - 8, y + h * 0.55),
               (x + w - 40, y + h * 0.88), (x + 40, y + h * 0.88)],
              fill=NAVY, outline=INK, width=2)
    d.rectangle([x + 18, y + h * 0.30, x + w - 60, y + h * 0.55],
                fill=RED, outline=INK, width=2)
    d.rectangle([x + w - 58, y + h * 0.18, x + w - 30, y + h * 0.55],
                fill=WHITE, outline=INK, width=2)
    # containers
    for i, col in enumerate([TEAL, GOLD, GREEN]):
        cx = x + 24 + i * 52
        d.rectangle([cx, y + h * 0.34, cx + 46, y + h * 0.52], fill=col,
                    outline=INK, width=2)
    # flame + smoke from the funnel: flame sits on the funnel top,
    # smoke rises just above it
    fx = x + w - 44
    funnel_top = y + h * 0.18
    d.polygon([(fx - 12, funnel_top), (fx, funnel_top - 26),
               (fx + 12, funnel_top)], fill=ORANGE, outline=RED, width=2)
    d.ellipse([fx - 20, funnel_top - 46, fx + 4, funnel_top - 22],
              fill=GREY, outline=INK)
    d.ellipse([fx - 8, funnel_top - 62, fx + 18, funnel_top - 38],
              fill=GREY, outline=INK)


def draw_ball(d, x, y, r):
    d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE, outline=INK, width=3)
    d.polygon([(x, y - r), (x + r * 0.7, y - r * 0.3), (x, y + r * 0.2),
               (x - r * 0.7, y - r * 0.3)], fill=INK)
    d.line([(x, y - r), (x, y + r)], fill=INK, width=2)
    d.line([(x - r, y), (x + r, y)], fill=INK, width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    R = W - M

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((M, 16), "THE WORLD IN ONE DAY", font=font(F_BLACK, 62),
           fill=WHITE)
    d.text((M, 92), "SUNDAY  \u00b7  22 NOVEMBER 2026",
           font=font(F_SANS_B, 32), fill=GOLD)
    d.text((R - tw(d, "EARLY EDITION", font(F_SANS_B, 20)),
            100), "EARLY EDITION", font=font(F_SANS_B, 20), fill=WHITE)
    d.text((R - tw(d, "ONE DAY \u00b7 ONE PICTURE", font(F_SANS, 17)),
            126), "ONE DAY \u00b7 ONE PICTURE", font=font(F_SANS, 17),
           fill=(200, 205, 215))

    # ---- Row 1: Hong Kong (lead) + COP31 --------------------------------
    y = 172
    col_w = (W - 2 * M - 24) // 2
    lx, rx = M, M + col_w + 24

    # Hong Kong, left column
    y1 = kicker(d, lx, y, "Hong Kong \u00b7 Asia")
    y1 = headline(d, lx, y1, "HONG KONG VOTES",
                  font(F_SERIF_B, 44), col_w, leading=48)
    draw_ballot(d, lx + col_w - 92, y1 + 2, 84)
    y1 = para(d, lx, y1 + 6,
              "Polls open at 9am for the Election Committee: 856 candidates "
              "chase 723 seats across 31 subsectors.",
              font(F_SANS, 20), col_w - 100)
    y1 = para(d, lx, y1 + 4,
              "The 1,500-member committee picks the city's next leader and "
              "40 of its lawmakers. Voting runs until 6pm.",
              font(F_SERIF, 20), col_w)

    # COP31, right column
    y2 = kicker(d, rx, y, "Antalya \u00b7 Climate", fill=TEAL)
    y2 = headline(d, rx, y2, "COP31: STILL NO DEAL",
                  font(F_SERIF_B, 40), col_w, leading=44)
    draw_sun(d, rx + col_w - 96, y2 + 2, 88)
    y2 = para(d, rx, y2 + 6,
              "Climate talks drag into Sunday with no final deal. The draft "
              "text says nothing about fossil fuels.",
              font(F_SANS, 20), col_w - 104)
    y2 = para(d, rx, y2 + 4,
              "A third draft is awaited after overnight talks; negotiators "
              "now expect a finish late on Sunday.",
              font(F_SERIF, 20), col_w)

    y = max(y1, y2) + 14
    rule(d, M, y, R)
    y += 10

    # ---- Row 2: Sparta II, full width ------------------------------------
    y = kicker(d, M, y, "Gulf of Finland \u00b7 Developing")
    y = headline(d, M, y, "RUSSIAN CARGO SHIP STILL ABLAZE OFF FINLAND",
                 font(F_SERIF_B, 38), R - M - 300, leading=42)
    ship_y = y - 118
    draw_ship(d, R - 292, ship_y, 284, 118)
    y = para(d, M, y + 4,
             "The Sparta II, hit by two drones on Saturday on its way to "
             "Kaliningrad, drifts ablaze into Finnish waters. Its crew is "
             "evacuated; firefighting goes on off Loviisa. Finland says "
             "Ukraine was likely behind the strike.",
             font(F_SERIF, 20), R - M - 300)
    y += 14
    rule(d, M, y, R)
    y += 10

    # ---- Row 3: football + today -----------------------------------------
    col_w2 = (W - 2 * M - 24) // 2
    lx, rx = M, M + col_w2 + 24
    y3 = y

    # Football, left
    y3l = kicker(d, lx, y3, "Football \u00b7 Saturday's results")
    draw_ball(d, lx + col_w2 - 30, y3l + 12, 20)
    scores = [
        ("Newcastle 2\u20132 Arsenal", "Leaders held; lead stays six"),
        ("Man City 1\u20131 Fulham", "Winless run reaches four games"),
        ("Chelsea 1\u20134 Leeds", "Okafor scores twice at the Bridge"),
        ("Bournemouth 2\u20130 Forest", "Ninth straight win in all games"),
        ("Tottenham 2\u20130 Ipswich", "Williams-Barnett nets on first start"),
    ]
    yy = y3l + 6
    for sc, note in scores:
        d.text((lx, yy), sc, font=font(F_SANS_B, 19), fill=INK)
        yy += 23
        d.text((lx + 12, yy), note, font=font(F_SERIF_I, 17), fill=GREY)
        yy += 22
    y3l = yy

    # Today, right
    y3r = kicker(d, rx, y3, "Today \u00b7 Sunday 22 November", fill=NAVY)
    y3r = headline(d, rx, y3r, "LIVERPOOL v MAN UTD",
                   font(F_SERIF_B, 34), col_w2, leading=38)
    y3r = para(d, rx, y3r + 2,
               "Anfield, 4.30pm. Hull host Brighton at 2pm. Hong Kong polls "
               "close at 6pm; the COP31 draft is awaited in Antalya.",
               font(F_SERIF, 20), col_w2)
    y3r += 6
    rule(d, rx, y3r, R, width=1, fill=GREY)
    y3r += 10
    y3r = para(d, rx, y3r,
               "ALSO TODAY \u2014 Saudi defences deflect a Houthi missile "
               "over western Saudi Arabia; Iran's new internet bill ties "
               "online accounts to real identities; US airlines are warned "
               "of a possible terror threat ahead of Thanksgiving.",
               font(F_SANS, 18), col_w2)

    y = max(y3l, y3r) + 8
    rule(d, M, y, R)
    y += 10

    # ---- Date check box ----------------------------------------------------
    box_top = y
    yy = box_top + 10
    yy = kicker(d, M + 14, yy, "Date check \u2014 read this first", fill=RED)
    yy = para(d, M + 14, yy + 2,
              "Every story above happened, or was first reported, on Sunday "
              "22 November 2026. Left out on purpose \u2014 not today's "
              "news: Norway's oil ruling (13 Nov), Ghana's banknotes "
              "(12 Nov), Kenya's Ebola discharge (11 Nov), the Peru quake "
              "(20 Nov), the US midterms (3 Nov), Lagarde's resignation "
              "(29 Oct).",
              font(F_SANS, 17), R - M - 28)
    box_bottom = yy + 12
    d.rectangle([M, box_top, R, box_bottom], fill=CREAM, outline=LINE,
                width=2)
    # redraw the text on top of the box (it was drawn before the fill)
    yy2 = box_top + 10
    yy2 = kicker(d, M + 14, yy2, "Date check \u2014 read this first",
                 fill=RED)
    para(d, M + 14, yy2 + 2,
         "Every story above happened, or was first reported, on Sunday "
         "22 November 2026. Left out on purpose \u2014 not today's "
         "news: Norway's oil ruling (13 Nov), Ghana's banknotes "
         "(12 Nov), Kenya's Ebola discharge (11 Nov), the Peru quake "
         "(20 Nov), the US midterms (3 Nov), Lagarde's resignation "
         "(29 Oct).",
         font(F_SANS, 17), R - M - 28)
    d.text((M, box_bottom + 6),
           "Drawn early on 22 Nov 2026 (02:30 UTC) \u2014 an early edition; "
           "more of Sunday's news lands later in the day.",
           font=font(F_SANS, 15), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
