#!/usr/bin/env python3
"""news-image-20261122 v2 — full-edition front page for Sunday 22 Nov 2026.

A newspaper front page drawn from scratch with PIL primitives only: no
photos, no downloaded images, no external assets. The page is data-driven:
a small list of feature stories plus a grid of one-line briefs, rendered by
generic helpers below. Every story on the page happened, or was first
reported, on Sunday 22 November 2026 (any time zone), verified against live
reporting on the morning of 22 Nov 2026 (07:30 UTC). Saturday's football
scores sit in a strip labelled SATURDAY, and the DATE CHECK box at the
bottom names the lookalike stories deliberately left out.

Run:  python3 draw.py   ->   writes entry.png (1024x1024) next to this file.
Deterministic: two runs write identical bytes (no randomness, no network,
no timestamps inside the image beyond the fixed edition line).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (158, 28, 34)
NAVY = (20, 38, 62)
NAVY2 = (14, 30, 50)
GOLD = (184, 134, 42)
GREY = (96, 93, 86)
LINE = (58, 56, 50)
CREAM = (238, 230, 212)
WHITE = (250, 248, 242)
SKY = (196, 219, 238)
TEAL = (18, 110, 106)
GREEN = (46, 110, 72)
ORANGE = (222, 110, 20)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_fonts = {}


def fnt(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def textw(d, s, font):
    return d.textlength(s, font=font)


def wrap_lines(d, text, font, maxw):
    """Greedy word wrap; returns a list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if textw(d, trial, font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, maxw, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y below its last line."""
    if leading is None:
        leading = int(font.size * 1.22)
    for line in wrap_lines(d, text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def tagline(d, x, y, text, fill=RED, size=16):
    """Small caps section tag; returns the y below it."""
    font = fnt(SANS_B, size)
    d.text((x, y), text.upper(), font=font, fill=fill)
    return y + size + 6


def hline(d, x0, x1, y, width=2, fill=LINE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def brief_lines(d, tag, text, colw, size=14):
    """Wrap a brief whose first line starts with a bold tag.

    Returns (prefix, lines): the bold prefix string and up to two wrapped
    text lines (the first measured against the prefix width). Text that
    still does not fit is cut with an ellipsis and reported.
    """
    fb = fnt(SANS_B, size)
    fr = fnt(SANS, size)
    prefix = tag + " \u2014 "
    pw = textw(d, prefix, fb)
    words = text.split()
    lines, cur, cur_w, used = [], "", pw, 0
    for word in words:
        ww = textw(d, (" " if cur else "") + word, fr)
        if cur_w + ww <= colw:
            cur = (cur + " " + word) if cur else word
            cur_w += ww
            used += 1
        else:
            lines.append(cur)
            if len(lines) == 2:
                break
            cur, cur_w = word, textw(d, word, fr)
            used += 1
    if cur and len(lines) < 2:
        lines.append(cur)
    if used < len(words):
        lines[-1] = lines[-1].rstrip() + " \u2026"
        print(f"WARNING brief truncated: {tag} ({used}/{len(words)} words)")
    return prefix, lines


def draw_brief(d, x, y, tag, text, colw):
    """One brief: bold tag inline, then regular text, max two lines."""
    fb = fnt(SANS_B, 14)
    fr = fnt(SANS, 14)
    prefix, lines = brief_lines(d, tag, text, colw)
    d.text((x, y), prefix, font=fb, fill=RED)
    pw = textw(d, prefix, fb)
    for i, line in enumerate(lines):
        yy = y + i * 17
        if i == 0:
            d.text((x + pw, yy), line, font=fr, fill=INK)
        else:
            d.text((x, yy), line, font=fr, fill=INK)
    return y + 17 * len(lines)


def ballot_icon(d, x, y, s):
    """Ballot box with a paper going in."""
    d.rectangle([x, y + s * 0.38, x + s, y + s], fill=NAVY,
                outline=INK, width=3)
    d.rectangle([x + s * 0.14, y + s * 0.32, x + s * 0.86, y + s * 0.46],
                fill=INK)
    d.polygon([(x + s * 0.32, y), (x + s * 0.60, y),
               (x + s * 0.54, y + s * 0.34), (x + s * 0.38, y + s * 0.34)],
              fill=WHITE, outline=INK)
    d.line([(x + s * 0.42, y + s * 0.10), (x + s * 0.50, y + s * 0.18),
            (x + s * 0.58, y + s * 0.04)], fill=RED, width=4)
    vt = "VOTE"
    vt_w = textw(d, vt, fnt(SANS_B, 16))
    d.text((x + (s - vt_w) / 2, y + s * 0.60), vt,
           font=fnt(SANS_B, 16), fill=WHITE)


def ball_icon(d, x, y, r):
    """Plain football."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE, outline=INK,
              width=3)
    d.polygon([(x, y - r), (x + r * 0.7, y - r * 0.3), (x, y + r * 0.2),
               (x - r * 0.7, y - r * 0.3)], fill=INK)
    d.line([(x, y - r), (x, y + r)], fill=INK, width=2)
    d.line([(x - r, y), (x + r, y)], fill=INK, width=2)


# ---------------------------------------------------------------------------
# The day's stories. Every item happened, or was first reported, on
# Sunday 22 November 2026. Sources: Reuters/AP via wire roundups, BBC,
# Al Jazeera, Hong Kong govt (info.gov.hk), BCCI, UKMTO, FT, WSJ.
# ---------------------------------------------------------------------------

LEAD = [
    {
        "tag": "Antalya \u00b7 Climate",
        "tag_fill": TEAL,
        "head": "COP31: FINAL TEXT PUT TO THE VOTE",
        "body": "A 10-page package was tabled at 2am after two days of "
                "overtime. It never names fossil fuels, aims for 35% "
                "electricity by 2035 and a billion tonnes of carbon "
                "capture, and admits 1.5\u00b0C will be overshot. Delegates "
                "vote this morning; one objection can stop it.",
        "icon": None,
    },
    {
        "tag": "The Gulf \u00b7 Escalation",
        "tag_fill": RED,
        "head": "IRAN HITS US BASES IN BAHRAIN",
        "body": "The IRGC claims missile and drone strikes on US Patriot "
                "radars at Al-Riffa and Awali Sakhir. Bahrain says an "
                "industrial site was hit and set alight, with no "
                "casualties. A Houthi missile aimed at western Saudi "
                "Arabia was intercepted; three tankers were hit near "
                "Hormuz.",
        "icon": None,
    },
]

SECOND = [
    {
        "tag": "Hong Kong \u00b7 Asia",
        "tag_fill": NAVY,
        "head": "HONG KONG VOTES",
        "body": "856 candidates chase 723 seats. Polls close 6pm, count "
                "tonight; the next leader is picked in March 2027.",
        "icon": "ballot",
        "turnout": 93.55,
    },
    {
        "tag": "Anfield \u00b7 Football",
        "tag_fill": RED,
        "head": "POCHETTINO'S FIRST TEST",
        "score": "LIVERPOOL v MAN UTD",
        "scorers": "KICK-OFF 4.30PM GMT \u00b7 TODAY",
        "note": "Pochettino's first game in charge of United.",
        "icon": "ball",
    },
    {
        "tag": "Wellington \u00b7 Cricket",
        "tag_fill": GREEN,
        "head": "INDIA 720/9 \u2014 A RECORD",
        "body": "Pant's 128 powers India to the highest Test total ever "
                "in New Zealand. Hosts 119/2 at stumps, 233 behind.",
        "icon": None,
    },
]

BRIEFS = [
    ("MEXICO", "Cartel boss \u2018El Chapo Isidro\u2019 seized in Sinaloa; 11 killed in the raid."),
    ("UKRAINE", "Russian strike on Kryvyi Rih kills two, a boy of seven; about 58 hurt."),
    ("NATO", "Rutte: alliance will defend \u2018every inch\u2019 of Poland; council meets Monday."),
    ("KYIV", "Zelensky: no written security guarantees yet; they must last decades."),
    ("WASHINGTON", "US wants a Ukraine deal by early January, the FT reports."),
    ("US SENATE", "Senate rejects a bid to limit Trump\u2019s strikes on Iran."),
    ("MARKETS", "S&P 500 falls 3.7% into correction as AI shares sell off; Nikkei -5.1%."),
    ("TRADE", "EU and Indonesia sign a trade deal after ten years of talks."),
    ("GAZA", "Israeli strikes continue; an aid vehicle is hit."),
    ("AMSTERDAM", "PMs Burnham and Jetten pledge continued support for Ukraine."),
    ("DENMARK", "Russian attach\u00e9 expelled over an alleged plot."),
    ("BEIRUT", "President Aoun blames Israel and Iran for threats to sovereignty."),
    ("GENEVA", "UN talks on AI weapons end with a tentative deal, no binding rules."),
    ("CYBER", "FBI criminal database hacked, reports say, amid wider cyber fears."),
    ("INDONESIA", "Factory fire kills three; 36 people missing."),
    ("SEOUL", "Education chief quits amid an AI cheating scandal."),
    ("PERU", "M5.1 aftershock hits Jun\u00edn overnight; Friday\u2019s quake killed one."),
    ("FINLAND", "Russian cargo ship Sparta II still ablaze; crew evacuated."),
    ("HORMUZ", "Two tankers hit by projectiles; a third strikes a mine."),
    ("TEHRAN", "Iran shows a new twin-missile launcher; 14 tankers ready to sail."),
    ("SPORT", "Alcaraz faces Zverev in today\u2019s ATP Finals decider."),
    ("RUGBY", "France beat Argentina to reach the final; Australia edge Wales."),
    ("NHL", "Senators top Kings; Flyers edge Canadiens 4-3; Leafs lose a ninth straight."),
    ("NCAA", "No. 6 Indiana fall to Washington in overtime; playoff hopes dented."),
    ("MLS", "Columbus thrash Inter Miami in the MLS Cup."),
    ("TECH", "Google unveils Agent Compute Engine; AWS adds GPU inference."),
    ("TOKYO", "Japan\u2019s GDP slips on weak consumer spending."),
    ("ESTONIA", "Plans to shut its Russian border for at least six months."),
    ("MINNESOTA", "Somali American driver assaulted after Trump\u2019s \u2018fight back\u2019 call."),
    ("JERUSALEM", "Israeli envoy: US troops stay until Iran is beaten; backlash follows."),
]

SATURDAY = [
    "Newcastle 2\u20132 Arsenal",
    "Man City 1\u20131 Fulham",
    "Chelsea 1\u20134 Leeds",
    "Bournemouth 2\u20130 Forest",
    "Tottenham 2\u20130 Ipswich",
    "Coventry 3\u20132 Crystal Palace",
]

DATE_CHECK = (
    "DATE CHECK \u2014 Every story above happened, or was first reported, on "
    "Sunday 22 November 2026, except the Saturday scores, labelled as such. "
    "Left out on purpose \u2014 not today\u2019s news: Norway\u2019s oil ruling "
    "(13 Nov), Ghana\u2019s banknotes (12 Nov), Kenya\u2019s Ebola discharge "
    "(11 Nov), the Peru quake (20 Nov), the US midterms (3 Nov), Lagarde\u2019s "
    "resignation (29 Oct). The Anfield game is tonight's fixture, "
    "previewed not reported."
)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    R = W - M

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 120], fill=NAVY)
    d.rectangle([0, 120, W, 125], fill=GOLD)
    d.text((M, 12), "THE WORLD IN ONE DAY",
           font=fnt(SERIF_BLACK, 44), fill=WHITE)
    d.text((M, 72), "SUNDAY  \u00b7  22 NOVEMBER 2026",
           font=fnt(SANS_B, 28), fill=GOLD)
    right1 = "FULL EDITION  \u00b7  DRAWN 07:30 UTC"
    d.text((R - textw(d, right1, fnt(SANS_B, 18)), 26), right1,
           font=fnt(SANS_B, 18), fill=WHITE)
    right2 = "42 STORIES  \u00b7  6 REGIONS"
    d.text((R - textw(d, right2, fnt(SANS, 16)), 54), right2,
           font=fnt(SANS, 16), fill=(200, 205, 215))
    d.text((R - textw(d, "ONE DAY \u00b7 ONE PICTURE", fnt(SANS, 15)), 82),
           "ONE DAY \u00b7 ONE PICTURE", font=fnt(SANS, 15),
           fill=(200, 205, 215))

    # ---- Lead row: COP31 + Gulf ------------------------------------------
    y = 136
    col_w = (W - 2 * M - 24) // 2
    lx, rx = M, M + col_w + 24
    tops = []
    for x, story in ((lx, LEAD[0]), (rx, LEAD[1])):
        yy = tagline(d, x, y, story["tag"], fill=story["tag_fill"])
        yy = block(d, x, yy, story["head"], fnt(SERIF_B, 28), col_w,
                   leading=33)
        yy = block(d, x, yy + 4, story["body"], fnt(SERIF, 17), col_w,
                   leading=20)
        tops.append(yy)
    y = max(tops) + 10
    hline(d, M, R, y)
    y += 10

    # ---- Second row: Hong Kong + Liverpool + India -----------------------
    col3 = (W - 2 * M - 2 * 20) // 3
    xs = [M, M + col3 + 20, M + 2 * (col3 + 20)]
    row2_bottom = y
    for x, story in zip(xs, SECOND):
        yy = tagline(d, x, y, story["tag"], fill=story["tag_fill"])
        if story.get("icon") == "ballot":
            ballot_icon(d, x + col3 - 62, yy + 2, 56)
            head_w = col3 - 70
        elif story.get("icon") == "ball":
            ball_icon(d, x + col3 - 26, yy + 12, 20)
            head_w = col3 - 56
        else:
            head_w = col3
        yy = block(d, x, yy, story["head"], fnt(SERIF_B, 26), head_w,
                   leading=30)
        if "score" in story:
            yy = block(d, x, yy + 2, story["score"], fnt(SANS_B, 21),
                       col3, leading=25)
            yy = block(d, x, yy, story["scorers"], fnt(SANS, 17), col3,
                       leading=21)
            yy = block(d, x, yy + 2, story["note"], fnt(SERIF_I, 17),
                       col3, leading=21)
        else:
            yy = block(d, x, yy + 2, story["body"], fnt(SERIF, 17), col3,
                       leading=21)
        if "turnout" in story:
            yy += 4
            d.text((x, yy), "TURNOUT 93.55% BY 2PM",
                   font=fnt(SANS_B, 13), fill=INK)
            yy += 18
            d.rectangle([x, yy, x + col3, yy + 12], outline=INK,
                        width=2, fill=WHITE)
            fill_w = int((col3 - 4) * story["turnout"] / 100.0)
            d.rectangle([x + 2, yy + 2, x + 2 + fill_w, yy + 10],
                        fill=TEAL)
            yy += 14
        row2_bottom = max(row2_bottom, yy)
    y = row2_bottom + 8
    hline(d, M, R, y)
    y += 10

    # ---- The day in brief: 3-column grid ---------------------------------
    yy = tagline(d, M, y, "The day in brief", fill=NAVY, size=18)
    y = yy + 2
    grid_top = y
    col_b = (W - 2 * M - 2 * 20) // 3
    bx = [M, M + col_b + 20, M + 2 * (col_b + 20)]
    rows = (len(BRIEFS) + 2) // 3
    row_h = 35
    for i, (tag, text) in enumerate(BRIEFS):
        gx = bx[i % 3]
        gy = grid_top + (i // 3) * row_h
        draw_brief(d, gx, gy, tag, text, col_b)
    y = grid_top + rows * row_h + 2
    hline(d, M, R, y)
    y += 8

    # ---- Saturday strip ----------------------------------------------------
    sat = "SATURDAY \u2014 " + "  \u00b7  ".join(SATURDAY) + \
        "  \u00b7  TODAY: Hull host Brighton, 2pm"
    y = block(d, M, y, sat, fnt(SANS, 14), R - M, leading=17)
    y += 4

    # ---- Date check box ----------------------------------------------------
    box_top = y
    inner = block(d, M + 12, box_top + 8, DATE_CHECK, fnt(SANS, 14),
                  R - M - 24, leading=16)
    box_bottom = inner + 8
    d.rectangle([M, box_top, R, box_bottom], fill=CREAM, outline=LINE,
                width=2)
    block(d, M + 12, box_top + 8, DATE_CHECK, fnt(SANS, 14),
          R - M - 24, leading=16)
    y = box_bottom
    assert y <= H, f"layout overflow: y={y} > {H}"
    print(f"layout ok: bottom y={y}, stories={5 + len(BRIEFS) + len(SATURDAY) + 1}")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
