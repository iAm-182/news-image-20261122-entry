"""Draw the Sunday 22 November 2026 front page: THE WORLD IN ONE DAY.

A PIL-only newspaper front page, 1024x1024, deterministic: the same
bytes every run. Paper (247, 243, 232), ink (22, 28, 38), navy masthead.
44 stories: 2 leads, 3 second-row stories, 1 Formula 1 band, 30 briefs,
7 Saturday scores and 1 Sunday score, plus a DATE CHECK box.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 28, 38)
NAVY = (16, 32, 64)
GOLD = (176, 132, 32)
RED = (178, 34, 34)
TEAL = (0, 122, 110)
LIGHT_GREY = (205, 202, 192)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif_b(s):
    return font("LiberationSerif-Bold.ttf", s)


def serif(s):
    return font("LiberationSerif-Regular.ttf", s)


def serif_i(s):
    return font("LiberationSerif-Italic.ttf", s)


def sans(s):
    return font("LiberationSans-Regular.ttf", s)


def sans_b(s):
    return font("LiberationSans-Bold.ttf", s)


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, width, text, fnt, leading, fill=INK):
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(d, x, y, text, color, size=13):
    """Small-caps section tag; returns the y below it."""
    d.text((x, y), text.upper(), font=sans_b(size), fill=color)
    return y + size + 5


def hline(d, x, y, width, weight=2):
    d.line([(x, y), (x + width, y)], fill=INK, width=weight)
    return y + weight + 6


def ball_icon(d, cx, cy, r):
    """A simple football: circle, centre pentagon, seams out to the edge."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    pts = []
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + 0.42 * r * math.cos(a), cy + 0.42 * r * math.sin(a)))
    d.polygon(pts, outline=INK)
    for px, py in pts:
        d.line([(px, py), (cx + (px - cx) * 2.3, cy + (py - cy) * 2.3)],
               fill=INK, width=1)


def ballot_icon(d, x, y, s=30):
    """A small ballot box with a red tick and a VOTE label."""
    d.rectangle([x, y, x + s, y + s], outline=INK, width=2, fill=WHITE)
    d.line([(x + 4, y + 3), (x + s - 4, y + 3)], fill=INK, width=2)
    d.line([(x + 6, y + s * 0.55), (x + s * 0.42, y + s * 0.80),
            (x + s - 6, y + s * 0.28)], fill=RED, width=3)
    d.text((x + 1, y + s + 2), "VOTE", font=sans_b(10), fill=INK)


def flag_icon(d, x, y, w=34, h=18):
    """A chequered flag: 4 by 2 black squares on white, thin border."""
    sq = w // 4
    hh = h // 2
    for r in range(2):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * sq, y + r * hh,
                             x + (c + 1) * sq, y + (r + 1) * hh],
                            fill=(0, 0, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def masthead(d):
    """Navy band: title left, date in gold, edition block right."""
    d.rectangle([0, 0, W, 94], fill=NAVY)
    d.text((MARGIN, 10), "THE WORLD IN ONE DAY", font=serif_b(40),
           fill=WHITE)
    d.text((MARGIN, 58), "SUNDAY \u00b7 22 NOVEMBER 2026",
           font=sans_b(20), fill=GOLD)
    right = ["FULL EDITION \u00b7 DRAWN 19:15 UTC",
             "44 STORIES \u00b7 8 REGIONS",
             "ONE DAY \u00b7 ONE PICTURE"]
    y = 14
    for line in right:
        f = sans(14)
        d.text((W - MARGIN - f.getlength(line), y), line, font=f, fill=WHITE)
        y += 22
    d.rectangle([0, 94, W, 97], fill=GOLD)
    return 106


LEADS = [
    {
        "tag": "Antalya \u00b7 Climate",
        "color": TEAL,
        "head": "COP31 COLLAPSES \u2014 NO DEAL",
        "body": ("After 44 hours of overtime, the longest COP ever, the "
                 "Antalya Pact was rejected. The EU, UK, Panama and the "
                 "Marshall Islands refused a text that never names fossil "
                 "fuels. President Kurum: \u201cthese decisions have not "
                 "been adopted.\u201d Guterres: \u201cdeeply "
                 "disappointed.\u201d"),
    },
    {
        "tag": "Anfield \u00b7 Football",
        "color": RED,
        "head": "LIVERPOOL ROUT UNITED",
        "score": "LIVERPOOL 4 \u2013 0 MAN UTD",
        "scorers": "Szoboszlai 10\u2032 \u00b7 Wirtz 13\u2032 \u00b7 "
                    "Ngumoha 66\u2032 \u00b7 Munoz 82\u2032",
        "note": "Yoro off 8\u2032; Pochettino\u2019s debut ends in a rout.",
    },
]


def lead_row(d, y):
    """Two lead stories side by side; returns the y below the row."""
    col_w = (CW - 24) // 2
    x1, x2 = MARGIN, MARGIN + col_w + 24
    y1 = tag(d, x1, y, LEADS[0]["tag"], LEADS[0]["color"], 13)
    y1 = para(d, x1, y1, col_w, LEADS[0]["head"], serif_b(29), 34)
    y1 = para(d, x1, y1 + 2, col_w, LEADS[0]["body"], serif(15), 19)
    y2 = tag(d, x2, y, LEADS[1]["tag"], LEADS[1]["color"], 13)
    ball_icon(d, x2 + col_w - 18, y2 + 8, 18)
    y2 = para(d, x2, y2, col_w - 48, LEADS[1]["head"], serif_b(29), 34)
    y2 = para(d, x2, y2 + 2, col_w, LEADS[1]["score"], sans_b(17), 22)
    y2 = para(d, x2, y2, col_w, LEADS[1]["scorers"], serif(14), 18)
    y2 = para(d, x2, y2, col_w, LEADS[1]["note"], serif_i(14), 18)
    return max(y1, y2) + 4


SECONDS = [
    {
        "tag": "The Gulf \u00b7 Escalation",
        "color": RED,
        "head": "IRAN HITS US BASES IN BAHRAIN",
        "body": ("The IRGC claims missile and drone strikes on US Patriot "
                 "radars in Bahrain. Bahrain says an industrial site was "
                 "hit and set alight, with no casualties."),
    },
    {
        "tag": "Hong Kong \u00b7 Asia",
        "color": TEAL,
        "head": "HONG KONG VOTES",
        "body": ("856 candidates chase 723 Election Committee seats. A "
                 "record 98.79% of 5,640 voters cast ballots; the count "
                 "finished at 10.15pm."),
        "turnout": 98.79,
    },
    {
        "tag": "Wellington \u00b7 Cricket",
        "color": TEAL,
        "head": "INDIA 720/9 \u2014 A RECORD",
        "body": ("Pant\u2019s 128 and Rahul\u2019s 136 power India to "
                 "720/9 declared \u2014 the highest Test total ever in "
                 "New Zealand, a 352-run lead. Hosts 119/2 at stumps, "
                 "233 behind."),
    },
]


def second_row(d, y):
    """Three stories side by side; returns the y below the row."""
    col_w = (CW - 50) // 3
    bottom = y
    for i, story in enumerate(SECONDS):
        x = MARGIN + i * (col_w + 25)
        yy = tag(d, x, y, story["tag"], story["color"], 12)
        if story.get("turnout") is not None:
            ballot_icon(d, x + col_w - 30, yy - 14)
        yy = para(d, x, yy, col_w, story["head"], serif_b(22), 26)
        yy = para(d, x, yy + 2, col_w, story["body"], serif(14), 17)
        if story.get("turnout") is not None:
            yy += 4
            d.text((x, yy), "TURNOUT 98.79% \u2014 RECORD",
                   font=sans_b(11), fill=INK)
            yy += 15
            d.rectangle([x, yy, x + col_w, yy + 8], fill=LIGHT_GREY)
            fill_w = int(col_w * story["turnout"] / 100.0)
            d.rectangle([x, yy, x + fill_w, yy + 8], fill=TEAL)
            yy += 8
        bottom = max(bottom, yy)
    return bottom + 4


F1 = {
    "tag": "Las Vegas \u00b7 Formula 1",
    "head": "VERSTAPPEN WINS VEGAS THRILLER",
    "body": ("35 lead changes, 352 overtakes: Verstappen beats Norris by "
             "0.639s, Piastri third. His 75th win \u2014 a third on the "
             "Strip."),
}


def f1_band(d, y):
    """Full-width Formula 1 band; returns the y below it."""
    flag_icon(d, MARGIN, y + 2)
    x = MARGIN + 44
    f_tag = sans_b(13)
    d.text((x, y + 3), F1["tag"].upper(), font=f_tag, fill=RED)
    tx = x + f_tag.getlength(F1["tag"].upper() + " \u2014 ")
    d.text((tx, y), F1["head"], font=serif_b(23), fill=INK)
    y = para(d, MARGIN + 44, y + 30, CW - 44, F1["body"], serif(14), 18)
    return y + 2


BRIEFS = [
    ("MEXICO", "Cartel boss \u2018El Chapo Isidro\u2019 seized in Guasave; "
               "11 killed in the raid."),
    ("UKRAINE", "Russian strike on Kryvyi Rih kills two; 60 hurt, six of "
                "them children."),
    ("NATO", "Rutte: alliance will defend \u2018every inch\u2019 of "
            "Poland; council meets Monday."),
    ("KYIV", "Zelensky: no written security guarantees yet; they must "
             "last decades."),
    ("WASHINGTON", "US wants a Ukraine deal by early January, the FT "
                   "reports."),
    ("US SENATE", "Senate rejects a bid to limit Trump\u2019s strikes on "
                  "Iran."),
    ("MARKETS", "S&P 500 falls 3.7% into correction as AI shares sell "
                "off; Nikkei -5.1%."),
    ("BITCOIN", "Bitcoin holds $60,000 after touching a $55,130 low."),
    ("TRADE", "EU and Indonesia sign a trade deal after ten years of "
             "talks."),
    ("GAZA", "Israeli strikes continue; an aid vehicle is hit."),
    ("DENMARK", "Russian attach\u00e9 expelled over an alleged plot."),
    ("GENEVA", "UN talks on AI weapons end with a tentative deal, no "
              "binding rules."),
    ("CYBER", "FBI criminal database hacked, reports say, amid wider "
             "cyber fears."),
    ("INDONESIA", "Factory fire kills three; 36 people missing."),
    ("PERU", "M5.1 aftershock hits Jun\u00edn overnight; Friday\u2019s "
            "quake killed one."),
    ("FINLAND", "Russian cargo ship Sparta II still ablaze off Loviisa; "
               "crew out, tow promised."),
    ("HORMUZ", "Tankers named: Torkel burns at anchor, Arina hit in her "
              "engine room."),
    ("TEHRAN", "Iran shows a new twin-missile launcher; 14 tankers ready "
              "to sail."),
    ("SPORT", "Alcaraz takes the first set 6-2 over Zverev in tonight\u2019s "
             "ATP Finals decider."),
    ("RUGBY", "France thrash Argentina 45-17 to reach the Nations final; "
             "England beat NZ 37-12."),
    ("NHL", "Senators top Kings; Flyers edge Canadiens 4-3; Leafs lose a "
           "ninth straight."),
    ("NCAA", "No. 6 Indiana fall to Washington in overtime; playoff hopes "
            "dented."),
    ("MLS", "Columbus win 3-0 at Miami in the MLS Cup playoffs; Messi in "
           "a throw-in row."),
    ("TECH", "Google unveils Agent Compute Engine; AWS adds GPU "
           "inference."),
    ("TOKYO", "Japan\u2019s GDP slips on weak consumer spending."),
    ("ESTONIA", "Plans to shut its Russian border for at least six "
               "months."),
    ("NIGERIA", "Bayelsa boat accident toll rises to 24; minister orders "
              "a probe."),
    ("SUDAN", "Amnesty: RSF drone strikes that killed 37 civilians are "
            "possible war crimes."),
    ("KENYA", "Floods kill at least six and displace hundreds; Tana River "
             "hardest hit."),
    ("IRAQ", "Fire at a Basra power station kills at least four; 35 hurt."),
]


def brief(d, x, y, width, tag_text, text, fnt, lead):
    """One brief: bold red tag inline, text wrapped with hanging indent."""
    tag_fnt = sans_b(fnt.size)
    prefix = tag_text + " \u2014 "
    pw = tag_fnt.getlength(prefix)
    words = text.split()
    lines, cur, first = [], "", True
    for word in words:
        trial = (cur + " " + word).strip()
        limit = width - pw if first else width
        if fnt.getlength(trial) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            first = False
    if cur:
        lines.append(cur)
    d.text((x, y), prefix, font=tag_fnt, fill=RED)
    d.text((x + pw, y), lines[0], font=fnt, fill=INK)
    y += lead
    for line in lines[1:]:
        d.text((x, y), line, font=fnt, fill=INK)
        y += lead
    return y + 3


def briefs_grid(d, y, size, lead):
    """30 briefs in 3 columns of 10; returns the y below the grid."""
    col_w = (CW - 50) // 3
    fnt = serif(size)
    bottom = y
    for col in range(3):
        x = MARGIN + col * (col_w + 25)
        yy = y
        for tag_text, text in BRIEFS[col * 10:(col + 1) * 10]:
            yy = brief(d, x, yy, col_w, tag_text, text, fnt, lead)
        bottom = max(bottom, yy)
    return bottom


SATURDAY = ["Newcastle 2\u20132 Arsenal", "Man City 1\u20131 Fulham",
            "Chelsea 1\u20134 Leeds", "Bournemouth 2\u20130 Forest",
            "Tottenham 2\u20130 Ipswich", "Coventry 3\u20132 Crystal Palace",
            "Aston Villa 0\u20130 Sunderland"]
SUNDAY = ["Hull 2\u20130 Brighton (McBurnie 90+2\u2032, 90+5\u2032)"]


def scores_strip(d, y):
    """Saturday and Sunday football scores; returns the y below."""
    f_label = sans_b(12)
    f_text = serif(13)
    for label, games in (("SATURDAY", SATURDAY), ("SUNDAY", SUNDAY)):
        prefix = label + " \u2014 "
        pw = f_label.getlength(prefix)
        text = " \u00b7 ".join(games)
        lines = wrap(text, f_text, CW - pw)
        d.text((MARGIN, y), prefix, font=f_label, fill=INK)
        d.text((MARGIN + pw, y), lines[0], font=f_text, fill=INK)
        y += 17
        for line in lines[1:]:
            d.text((MARGIN, y), line, font=f_text, fill=INK)
            y += 17
    return y + 2


DATE_CHECK = ("DATE CHECK \u2014 Every story above happened, or was first "
              "reported, on Sunday 22 November 2026, except the Saturday "
              "scores, labelled as such. Left out on purpose \u2014 not "
              "today\u2019s news: Norway\u2019s oil ruling (13 Nov), "
              "Ghana\u2019s banknotes (12 Nov), Kenya\u2019s Ebola "
              "discharge (11 Nov), the Peru quake (20 Nov), the US "
              "midterms (3 Nov), Lagarde\u2019s ECB term news.")


def date_check_box(d, y):
    """Boxed note on what counts as 22 November news; returns bottom y."""
    fnt = serif(12)
    lines = wrap(DATE_CHECK, fnt, CW - 24)
    box_h = len(lines) * 15 + 14
    d.rectangle([MARGIN, y, MARGIN + CW, y + box_h], outline=INK, width=2)
    yy = y + 7
    for line in lines:
        d.text((MARGIN + 12, yy), line, font=fnt, fill=INK)
        yy += 15
    return y + box_h


def build(brief_size, brief_lead):
    """Lay out the whole page at a given brief size; returns (img, end_y)."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    y = lead_row(d, y)
    y = hline(d, MARGIN, y, CW)
    y = second_row(d, y)
    y = hline(d, MARGIN, y, CW)
    y = f1_band(d, y)
    y = hline(d, MARGIN, y, CW)
    d.text((MARGIN, y), "THE DAY IN BRIEF", font=sans_b(16), fill=NAVY)
    y += 24
    y = briefs_grid(d, y, brief_size, brief_lead)
    y = hline(d, MARGIN, y, CW)
    y = scores_strip(d, y)
    y = date_check_box(d, y + 2)
    return img, y


def render(path="entry.png"):
    """Render, shrinking the brief type until the page fits in 1024px.

    Tries the largest brief type first so the page fills the sheet
    instead of ending in a band of blank paper.
    """
    for size, lead in [(13, 17), (12, 16), (12, 15), (11, 14), (10, 13),
                       (9, 12)]:
        img, end_y = build(size, lead)
        if end_y <= 1020:
            break
    img.save(path)
    print("rendered %s brief=%d/%d final_y=%d" % (path, size, lead, end_y))
    return end_y


if __name__ == "__main__":
    render()
