#!/usr/bin/env python3
"""Render the news-image-20261124 entry: one 1024x1024 picture summing up
Tuesday 24 November 2026 in world news.

Layout top to bottom: masthead with the date as the biggest element on the
page, a UTC timeline ribbon, three hero picture cards, six big numbers, ten
minor picture cards in a 5x2 grid, a real world map with numbered pins beside
a numbered index of the remaining stories, a DATE CHECK box quarantining
other days' stories, and a sources footer.

Everything is drawn with Pillow from the data in this file: no network, no
external assets, deterministic output. Run: python3 render.py
Writes entry.png next to this file (1024x1024, under 1 MiB).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
PAPER = (250, 247, 239)   # warm paper
INK = (24, 34, 56)        # near-black navy
NAVY = (26, 40, 70)       # masthead band
NAVY2 = (36, 55, 92)      # dark panel
RED = (176, 38, 28)       # breaking accent
BLUE = (28, 76, 134)      # section blue
TEAL = (13, 104, 104)     # field tag
GREEN = (18, 110, 58)     # markets green
GOLD = (176, 138, 20)     # numbers gold
GOLD_L = (214, 178, 58)   # light gold on navy
GREY = (92, 101, 115)     # secondary text
LIGHT = (224, 216, 198)   # hairlines
SEA = (206, 224, 236)     # ocean on the map
LAND = (196, 198, 168)    # land on the map
WHITE = (255, 255, 255)
CREAM = (240, 233, 216)

# ---------------------------------------------------------------- fonts
def load_font(name, size, subdir="dejavu"):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/%s/%s.ttf" % (subdir, name), size)

def serif_b(size):
    return load_font("DejaVuSerif-Bold", size)

def serif_i(size):
    return load_font("LiberationSerif-Italic", size, "liberation")

def sans(size):
    return load_font("DejaVuSans", size)

def sans_b(size):
    return load_font("DejaVuSans-Bold", size)

# ---------------------------------------------------------------- data
DATE_LINE = "Tuesday 24 November 2026"
COUNT_LINE = "33 STORIES  \u00b7  7 REGIONS  \u00b7  14 FIELDS  \u00b7  ALL FROM THIS TUESDAY"

TIMELINE = [
    ("01:32", "Nepal quake M5.6"),
    ("02:30", "Villavicencio car bomb"),
    ("03:30", "Yemen strike reported"),
    ("04:35", "Tangguh CO2 talks"),
    ("06:43", "Malaysia data-centre order"),
    ("08:18", "Malaysia CCUS roadmap"),
    ("14:00", "Chess Game 1, Geneva"),
]

HEROES = [
    {
        "num": 1, "region": "WAR \u00b7 POLAND / NATO", "tag": "CONFIRMED",
        "source": "Reuters \u00b7 Polish Armed Forces \u00b7 RMF24/PAP",
        "headline": "Russian drone crosses into Poland overnight \u2014 Warsaw calls it likely deliberate",
        "body": ("Geran-5 drone crossed into Poland near Dorohusk overnight "
                 "(23\u219224 Nov), flew ~20 km to Che\u0142m, then turned back. "
                 "Warsaw held fire; sirens in Lublin."),
        "scene": "drone",
    },
    {
        "num": 2, "region": "MARKETS \u00b7 ASIA", "tag": "CONFIRMED",
        "source": "Reuters",
        "headline": "Asia stocks soar as Nvidia\u2019s rebound revives the AI trade",
        "body": ("Taiwan +9.1%, KOSPI +7.5%, Nikkei +4.5% \u2014 Asia\u2019s biggest "
                 "rally in months. Trigger: Jensen Huang\u2019s return as Nvidia "
                 "CEO, announced Mon 23 Nov."),
        "scene": "chart",
    },
    {
        "num": 3, "region": "SPORT \u00b7 GENEVA", "tag": "CONFIRMED",
        "source": "FIDE via ChessBase \u00b7 myKhel",
        "headline": "Gukesh vs Sindarov: the youngest world chess final ever begins today",
        "body": ("Champion D. Gukesh (India, 20) faces challenger Javokhir Sindarov "
                 "(Uzbekistan, 20) in Game 1, 15:00 CET, Geneva. 14 games, "
                 "first to 7.5; $2.5m prize."),
        "scene": "chess",
    },
]

MINORS = [
    {
        "num": 4, "region": "SOUTH KOREA", "field": "SECURITY", "tag": "CONFIRMED",
        "source": "AP \u00b7 Yonhap \u00b7 QNA",
        "headline": "Russian jets trigger air-raid alert on Ulleung",
        "body": "F-15Ks scrambled; ~9,000 told to shelter. Alert lifted in ~5 min.",
        "scene": "jet",
    },
    {
        "num": 5, "region": "PACIFIC", "field": "DIPLOMACY", "tag": "REPORTED",
        "source": "Sydney Morning Herald",
        "headline": "Solomon Islands to end China security pact",
        "body": "Pact with Beijing ends in April; new Australia deal being finalised.",
        "scene": "pacific",
    },
    {
        "num": 6, "region": "CHINA", "field": "SPACE", "tag": "OFFICIAL",
        "source": "CMSA via Xinhua \u00b7 Reuters",
        "headline": "Shenzhou-24 crew named; first Pakistani to Tiangong",
        "body": "Tang Hongbo, Wu Yi, and Pakistan\u2019s Zeeshan Ali. Launch Wed 25 Nov.",
        "scene": "rocket",
    },
    {
        "num": 7, "region": "UKRAINE", "field": "WAR", "tag": "CONFIRMED",
        "source": "Reuters \u00b7 AnewZ",
        "headline": "Zaporizhzhia strike kills 2, injures 22\u201340",
        "body": "2 killed, 22\u201340 hurt incl. children; homes and transport hit.",
        "scene": "citynight",
    },
    {
        "num": 8, "region": "GLOBAL", "field": "CYBER", "tag": "REPORTED",
        "source": "Wall Street Journal",
        "headline": "US probes Iran role in tanker cyberattacks",
        "body": "WSJ: attackers exploited a Fortinet flaw; no Iran link found yet.",
        "scene": "tanker",
    },
    {
        "num": 9, "region": "NEPAL", "field": "DISASTER", "tag": "CONFIRMED",
        "source": "NEMRC \u00b7 USGS \u00b7 EMSC",
        "headline": "M5.6 quake shakes eastern Nepal near Tibet",
        "body": "Taplejung, 07:17 local (01:32 UTC). Felt in India, Bhutan, Bangladesh.",
        "scene": "quake",
    },
    {
        "num": 10, "region": "INDONESIA", "field": "POLITICS", "tag": "CONFIRMED",
        "source": "Reuters",
        "headline": "Indonesia charges ex-police chief with treason",
        "body": "Alleged wiretap of President Prabowo. Announced Mon eve, reported Tue.",
        "scene": "scales",
    },
    {
        "num": 11, "region": "INDONESIA", "field": "DISASTER", "tag": "CONFIRMED",
        "source": "Reuters \u00b7 AP \u00b7 The Guardian",
        "headline": "Cikande fire toll confirmed at 24; ~30 still missing",
        "body": "Fire broke out Sat 21 Nov \u2014 toll of 24 confirmed Tue; search goes on.",
        "scene": "factory",
    },
    {
        "num": 12, "region": "MALAYSIA", "field": "CLIMATE", "tag": "CONFIRMED",
        "source": "Reuters",
        "headline": "Malaysia plans carbon storage hubs worth $41.3bn",
        "body": "3\u20136 hubs, up to $41.32bn by 2050; first injection targeted 2030.",
        "scene": "co2",
    },
    {
        "num": 13, "region": "MALAYSIA", "field": "TRADE", "tag": "OFFICIAL",
        "source": "MITI via Reuters \u00b7 Straits Times",
        "headline": "Malaysia orders data centres to cut off 7 firms",
        "body": "7 entities incl. Megaspeed (Singapore); follows Mon US chip rule.",
        "scene": "servers",
    },
]

NUMBERS = [
    ("+9.1%", "Taiwan stocks \u2014 Tuesday\u2019s biggest Asian jump"),
    ("9,000", "Ulleung islanders told to shelter"),
    ("~50", "energy tankers hit in cyberattacks"),
    ("$41.3bn", "Malaysia carbon-storage plan to 2050"),
    ("24", "Cikande fire dead, confirmed Tuesday"),
    ("20 & 20", "youngest world chess final ever"),
]

INDEX = [
    (14, "LAHJ", "Saudi strike kills or leaves missing 25, injures 6"),
    (15, "VILLAVICENCIO", "Car bomb injures 5\u201323; Mon night Colombia time, first wire reports Tue"),
    (16, "WASHINGTON", "Hegseth yet to approve ~60 Patriot interceptors for Ukraine"),
    (17, "DHAKA", "Ex-PM Hasina plans return from exile on 16 Dec; faces arrest"),
    (18, "ANTALYA", "COP31 fallout: Pacific Elders accuse Australia of betrayal"),
    (19, "SUVA", "Fiji to close all schools 30 Nov\u20134 Dec as El Ni\u00f1o drought deepens"),
    (20, "NEW DELHI", "India captain Gill urges ICC to revisit COVID-era saliva ban"),
    (21, "EUROPE", "Champions League Matchday 5 TONIGHT: Arsenal\u2013Dortmund, Man City\u2013Napoli"),
    (22, "GOA", "IFFI: Ayan Mukerji confirms Brahmastra 2; admits War 2 fell short"),
    (23, "TOKYO", "Japan\u2019s mass-producible quantum nanodiamond sensor boosts signal 55%"),
    (24, "TANGERANG", "ASEAN disaster meeting opens; AHA Centre board session held Tue"),
    (25, "TANGGUH", "Indonesia discusses Tangguh CO2 storage with Japan and China"),
    (26, "ASIA CUP", "India A vs UAE, Rising Stars Asia Cup, live Tue"),
    (27, "HOLLYWOOD", "\u201cThe Social Reckoning\u201d out digitally Tue; home releases follow"),
    (28, "CHRISTCHURCH", "NZ\u2019s Blair Tickner out of 2nd Test vs India (hamstring); Fisher in"),
    (29, "ENTEBBE", "Somalia and Uganda vow joint push against al-Shabaab"),
    (30, "LOS ANGELES", "Ariana Grande teases \u201cEternal Sunshine Tour\u201d project on Peacock"),
    (31, "HAVANA", "WHO chief Tedros tours Cuba hospitals on day 2 of 3-day visit"),
    (32, "NEW YORK", "Fed Dec hike now priced near-certain; 10-year yield 4.94%; gold ~$3,657"),
    (33, "SHARJAH", "Babar Azam hits 86 (51 balls) on ILT20 debut; reported Tue morning"),
]

DATECHECK = ("Left out on purpose \u2014 first reported BEFORE Tuesday: COP31 collapsed "
             "Sun 22 Nov \u00b7 NATO\u2019s AWACS decision Mon 23 Nov \u00b7 Merkury sinking "
             "Sun 22 Nov, Zelensky\u2019s claim Mon 23 Nov \u00b7 missiles fell in Poland "
             "Fri 20 Nov (today: the drone) \u00b7 Nvidia restored Huang Mon 23 Nov \u00b7 "
             "FIFA named Women\u2019s World Cup hosts Mon 23 Nov \u00b7 CrowdStrike\u2013Zscaler "
             "deal Mon 23 Nov \u00b7 measles death in Pennsylvania Mon 23 Nov. "
             "Not yet: Shenzhou-24 launch Wed 25 Nov \u00b7 Trump\u2013Rutte meeting "
             "Wed 25 Nov \u00b7 Solomon\u2013Australia signing Wed 25 Nov \u00b7 "
             "Hasina\u2019s return 16 Dec \u00b7 Estonia border closure 1 Dec.")

SOURCES = ("Sources: Reuters, AP, AFP, Yonhap, FIDE/ChessBase, Sydney Morning Herald, "
           "Xinhua, Wall Street Journal, Financial Times, Times of India, UEFA, JST, "
           "PINA, IANS, ANI, Bollywood Hungama, Sportstar, Media Play News, Forbes "
           "Europe, Shabelle Media, Petromindo, The Kabar News. Every story happened, "
           "or was first reported, on Tuesday 24 November 2026; claims are labelled "
           "and attributed.")

# (number, longitude, latitude, label offset dx, dy for the pin circle)
PINS = [
    (1, 23.8, 51.2, 0, 0),
    (2, 139.7, 35.7, 0, 0),
    (3, 6.1, 46.2, 0, 0),
    (4, 130.9, 37.5, 0, 0),
    (5, 160.0, -9.6, 0, 0),
    (6, 100.3, 40.9, 0, 0),
    (7, 35.2, 47.8, 0, 0),
    (8, 56.3, 26.6, 0, 0),
    (9, 87.9, 27.6, 0, 0),
    (10, 106.8, -6.2, -11, -9),
    (11, 106.1, -6.2, 11, 9),
    (12, 101.7, 3.1, -10, 10),
    (13, 103.8, 1.35, 12, -10),
]

# Coarse continent outlines (lon, lat) for a recognisable world map.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-105, 68),
     (-95, 69), (-85, 66), (-80, 73), (-70, 62), (-60, 58), (-55, 52),
     (-60, 47), (-65, 44), (-70, 42), (-75, 38), (-80, 32), (-81, 26),
     (-84, 30), (-90, 21), (-94, 17), (-97, 16), (-102, 18), (-105, 21),
     (-110, 24), (-114, 29), (-120, 34), (-124, 40), (-124, 48), (-130, 55),
     (-140, 60), (-150, 59), (-158, 58), (-165, 60), (-168, 66)],
    # Greenland
    [(-58, 64), (-48, 60), (-40, 60), (-32, 66), (-22, 70), (-20, 74),
     (-28, 78), (-40, 80), (-52, 78), (-58, 74), (-58, 64)],
    # South America
    [(-80, 9), (-77, 8), (-72, 11), (-64, 10), (-59, 8), (-52, 5),
     (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-38, -15), (-40, -21),
     (-46, -24), (-48, -28), (-53, -33), (-58, -35), (-62, -39), (-65, -41),
     (-66, -45), (-68, -50), (-70, -53), (-73, -50), (-73, -44), (-72, -37),
     (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 2),
     (-80, 9)],
    # Africa
    [(-17, 15), (-16, 11), (-12, 8), (-8, 5), (-2, 5), (4, 6), (8, 4),
     (9, -1), (10, -4), (13, -10), (12, -17), (14, -22), (16, -28),
     (19, -34), (25, -34), (28, -33), (32, -29), (35, -24), (38, -18),
     (40, -14), (42, -11), (46, -10), (51, 11), (48, 11), (44, 11),
     (40, 14), (38, 18), (36, 21), (34, 27), (32, 31), (30, 32), (23, 33),
     (19, 33), (12, 34), (10, 37), (5, 37), (0, 36), (-6, 35), (-10, 31),
     (-15, 27), (-17, 21), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 48), (-1, 49), (1, 51),
     (3, 53), (5, 53), (8, 57), (8, 59), (10, 59), (12, 56), (18, 56),
     (21, 55), (24, 58), (24, 60), (28, 60), (30, 62), (28, 65), (25, 68),
     (22, 70), (18, 69), (14, 66), (12, 62), (8, 62), (5, 60), (5, 58),
     (0, 57), (-3, 58), (-5, 56), (-5, 50), (-8, 48), (-9, 43), (-10, 36)],
    # Asia
    [(30, 36), (33, 36), (36, 36), (38, 38), (41, 41), (43, 42), (46, 43),
     (49, 45), (50, 47), (52, 49), (55, 51), (58, 53), (60, 55), (63, 58),
     (66, 60), (68, 63), (70, 66), (73, 69), (76, 71), (80, 73), (85, 74),
     (90, 75), (95, 76), (100, 76), (105, 77), (110, 76), (115, 73),
     (120, 73), (125, 72), (130, 72), (135, 71), (140, 72), (145, 72),
     (150, 71), (155, 69), (160, 69), (165, 68), (170, 67), (175, 66),
     (178, 65), (178, 62), (173, 62), (170, 60), (166, 60), (162, 57),
     (159, 53), (156, 51), (150, 59), (145, 58), (142, 55), (141, 50),
     (140, 45), (139, 40), (137, 37), (135, 34), (133, 34), (130, 33),
     (129, 32), (127, 34), (126, 38), (124, 40), (122, 39), (120, 34),
     (119, 31), (118, 28), (116, 23), (113, 22), (110, 21), (108, 18),
     (106, 10), (104, 8), (103, 7), (101, 7), (100, 8), (98, 10), (97, 15),
     (94, 17), (92, 21), (90, 22), (88, 21), (86, 20), (84, 19), (80, 15),
     (79, 10), (77, 8), (76, 10), (75, 14), (73, 19), (72, 20), (70, 22),
     (68, 24), (66, 25), (63, 25), (61, 25), (58, 26), (56, 27), (54, 27),
     (52, 27), (50, 29), (48, 30), (46, 29), (44, 29), (42, 30), (40, 31),
     (38, 32), (36, 36), (33, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -27), (114, -31), (115, -34), (118, -35), (121, -34),
     (124, -33), (128, -32), (130, -32), (132, -32), (135, -35), (137, -35),
     (140, -38), (143, -39), (146, -39), (149, -37), (150, -37), (152, -33),
     (153, -30), (153, -27), (151, -24), (150, -22), (148, -20), (146, -19),
     (143, -15), (142, -11), (141, -13), (140, -17), (138, -17), (136, -15),
     (135, -12), (132, -12), (130, -13), (128, -14), (126, -14), (124, -15),
     (122, -17), (120, -19), (117, -20), (114, -22), (113, -22)],
    # Sumatra
    [(95, 5), (97, 3), (99, 1), (101, -1), (103, -3), (104, -5), (106, -6),
     (104, -5), (102, -3), (100, 0), (98, 3), (95, 5)],
    # Borneo
    [(109, 1), (110, 3), (113, 4), (116, 6), (118, 6), (119, 2), (118, -1),
     (117, -3), (115, -4), (112, -3), (110, -2), (109, 1)],
    # New Guinea
    [(131, -1), (134, -2), (137, -3), (140, -3), (143, -4), (146, -6),
     (148, -8), (150, -8), (147, -9), (144, -8), (141, -8), (138, -7),
     (135, -4), (132, -2), (131, -1)],
    # Japan
    [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (139, 36),
     (140, 38), (141, 40), (141, 42), (143, 43), (143, 44), (141, 45),
     (140, 42), (140, 39), (139, 37), (137, 36), (135, 35), (133, 34),
     (131, 33), (130, 31)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 57), (0, 53), (-1, 51),
     (-3, 50), (-5, 50)],
    # Madagascar
    [(44, -16), (47, -15), (49, -16), (50, -18), (49, -21), (47, -24),
     (45, -25), (43, -22), (43, -19), (44, -16)],
    # New Zealand
    [(167, -45), (168, -44), (170, -42), (172, -41), (174, -39), (176, -38),
     (175, -40), (173, -41), (171, -43), (169, -45), (167, -45)],
]

# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, fnt, width):
    """Greedy word wrap; returns the list of lines that fit the width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_text(draw, text, fnt, width, max_lines):
    """Wrap text to at most max_lines; ellipsize the last line if needed."""
    lines = wrap_text(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + " \u2026", font=fnt) > width:
        words = lines[-1].split(" ")
        lines[-1] = " ".join(words[:-1]) if len(words) > 1 else ""
    lines[-1] = (lines[-1] + " \u2026").strip()
    return lines


def shrink_to_width(draw, text, fnt, width):
    """Cut text with an ellipsis so it fits one line of the given width."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def tag_color(tag):
    return {"CONFIRMED": TEAL, "OFFICIAL": BLUE, "REPORTED": GOLD}.get(tag, GREY)

# ---------------------------------------------------------------- scenes
# Each scene draws a small recognisable picture inside the given box
# (x0, y0, x1, y1). All pictures are drawn from shapes, no image files.

def scene_drone(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 42, 66))
    # land: Poland (light) left of a dashed border, Ukraine (darker) right
    d.polygon([(x0, y0 + 18), (x0 + 150, y0 + 8), (x0 + 170, y1 - 14),
               (x0 + 120, y1), (x0, y1)], fill=(72, 96, 120))
    d.polygon([(x0 + 150, y0 + 8), (x1, y0 + 22), (x1, y1),
               (x0 + 170, y1 - 14)], fill=(52, 72, 96))
    for yy in range(y0 + 8, y1 - 8, 12):
        d.line([(x0 + 150 + (yy - y0) * 0.12, yy),
                (x0 + 150 + (yy - y0) * 0.12, yy + 6)], fill=GOLD_L, width=2)
    # drone silhouette with a red trail: slim fuselage, swept delta wings
    cx, cy = x0 + 205, y0 + 34
    d.line([(cx - 78, cy + 20), (cx - 8, cy + 2)], fill=RED, width=2)
    d.polygon([(cx - 24, cy - 3), (cx + 24, cy - 2), (cx + 28, cy + 1),
               (cx + 24, cy + 3), (cx - 24, cy + 3)], fill=(28, 28, 28))
    d.polygon([(cx - 6, cy - 2), (cx + 6, cy - 2), (cx + 16, cy - 16),
               (cx + 10, cy - 16)], fill=(28, 28, 28))
    d.polygon([(cx - 6, cy + 2), (cx + 6, cy + 2), (cx + 14, cy + 13),
               (cx + 8, cy + 13)], fill=(28, 28, 28))
    d.polygon([(cx - 22, cy - 2), (cx - 16, cy - 2), (cx - 20, cy - 12),
               (cx - 24, cy - 10)], fill=(28, 28, 28))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    # siren arcs over Lublin
    sx, sy = x0 + 52, y0 + 66
    for r in (10, 18, 26):
        d.arc([sx - r, sy - r, sx + r, sy + r], 200, 340, fill=GOLD_L, width=3)
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=RED)
    d.text((x0 + 10, y1 - 20), "OVERNIGHT MON \u2192 TUE", font=sans_b(12),
           fill=GOLD_L)
    d.text((x1 - 10, y1 - 20), "DOROHUSK \u2022 CHE\u0141M", font=sans_b(11),
           fill=WHITE, anchor="ra")


def scene_chart(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(16, 48, 32))
    for gy in range(y0 + 44, y1 - 16, 14):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(38, 74, 52), width=1)
    pts = [(x0 + 12, y1 - 28), (x0 + 60, y1 - 38), (x0 + 105, y1 - 34),
           (x0 + 150, y1 - 46), (x0 + 195, y1 - 44), (x0 + 240, y1 - 58),
           (x1 - 14, y1 - 64)]
    d.line(pts, fill=(90, 220, 130), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(90, 220, 130))
    d.text((x0 + 12, y0 + 4), "+9.1%", font=sans_b(34), fill=(150, 240, 170))
    d.text((x0 + 128, y0 + 12), "TAIWAN", font=sans_b(12), fill=WHITE)
    d.text((x0 + 12, y1 - 14), "KOSPI +7.5%  \u00b7  NIKKEI +4.5%",
           font=sans_b(11), fill=(190, 220, 200))


def scene_chess(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(58, 40, 28))
    # 8x8 board on the left
    bs = 11
    bx, by = x0 + 10, y0 + 6
    for r in range(8):
        for c in range(8):
            col = (235, 225, 200) if (r + c) % 2 == 0 else (52, 58, 74)
            d.rectangle([bx + c * bs, by + r * bs, bx + (c + 1) * bs,
                         by + (r + 1) * bs], fill=col)
    # two kings facing off on the right
    for kx, col in ((x0 + 138, (235, 225, 200)), (x0 + 178, (20, 20, 20))):
        d.ellipse([kx - 14, y0 + 22, kx + 14, y0 + 50], fill=col,
                  outline=GOLD_L, width=2)
        d.rectangle([kx - 3, y0 + 10, kx + 3, y0 + 24], fill=col)
        d.rectangle([kx - 9, y0 + 15, kx + 9, y0 + 21], fill=col)
    d.text((x0 + 128, y0 + 58), "20  vs  20", font=sans_b(15), fill=WHITE)
    d.text((x0 + 128, y0 + 78), "GAME 1 \u00b7 TODAY", font=sans_b(10),
           fill=GOLD_L)


def scene_jet(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(70, 110, 150))
    d.ellipse([x0 + 130, y0 + 4, x0 + 190, y0 + 40], fill=(235, 240, 245))
    # F-15K silhouette
    d.polygon([(x0 + 14, y0 + 30), (x0 + 90, y0 + 22), (x0 + 150, y0 + 26),
               (x0 + 96, y0 + 34), (x0 + 30, y0 + 38)], fill=(40, 48, 60))
    d.polygon([(x0 + 60, y0 + 22), (x0 + 78, y0 + 8), (x0 + 84, y0 + 24)],
              fill=(40, 48, 60))
    # phone with an emergency alert
    d.rounded_rectangle([x0 + 118, y0 + 12, x0 + 176, y0 + 46],
                        radius=4, fill=(250, 250, 250), outline=RED, width=2)
    d.text((x0 + 147, y0 + 16), "!", font=sans_b(16), fill=RED, anchor="ma")
    d.text((x0 + 147, y0 + 33), "SHELTER", font=sans_b(7), fill=RED,
           anchor="ma")
    d.text((x0 + 10, y1 - 14), "9,000 TOLD TO SHELTER", font=sans_b(9),
           fill=WHITE)


def scene_pacific(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(58, 120, 160))
    # simplified Pacific islands chain
    for ix, iy, r in ((30, 26, 12), (70, 18, 9), (105, 30, 14), (140, 20, 8),
                      (160, 34, 10)):
        d.ellipse([x0 + ix - r, y0 + iy - r, x0 + ix + r, y0 + iy + r],
                  fill=(120, 170, 90))
    # three small flags: Solomon / Australia / China
    for fx, cols in ((x0 + 22, [(0, 110, 60), (250, 210, 60), (200, 30, 30)]),
                     (x0 + 72, [(0, 40, 120), (255, 255, 255)]),
                     (x0 + 122, [(200, 30, 30), (250, 220, 60)])):
        for i, col in enumerate(cols):
            d.rectangle([fx + i * 12, y0 + 8, fx + (i + 1) * 12, y0 + 20],
                        fill=col)
    d.text((x0 + 10, y1 - 14), "PACT ENDS APRIL", font=sans_b(9), fill=WHITE)


def scene_rocket(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 20, 44))
    for sx, sy in ((30, 10), (70, 6), (120, 12), (160, 8), (60, 40), (150, 44)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=WHITE)
    # Long March rocket
    rx = x0 + 42
    d.rectangle([rx, y0 + 10, rx + 16, y0 + 40], fill=(230, 230, 230))
    d.polygon([(rx, y0 + 10), (rx + 8, y0 + 1), (rx + 16, y0 + 10)],
              fill=RED)
    d.polygon([(rx + 2, y0 + 40), (rx + 8, y0 + 48), (rx + 14, y0 + 40)],
              fill=(250, 180, 60))
    # Tiangong station
    d.rectangle([x0 + 100, y0 + 16, x0 + 170, y0 + 24], fill=(180, 190, 205))
    d.rectangle([x0 + 118, y0 + 10, x0 + 152, y0 + 30], fill=(210, 215, 225))
    d.text((x0 + 10, y1 - 14), "LAUNCH WED 25 NOV", font=sans_b(9),
           fill=GOLD_L)


def scene_citynight(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(18, 24, 44))
    for bx, bh, bw in ((8, 26, 26), (40, 34, 22), (68, 20, 30), (104, 30, 24),
                       (134, 22, 28), (164, 28, 18)):
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(44, 52, 74))
        for wy in range(y1 - bh + 4, y1 - 4, 8):
            d.rectangle([x0 + bx + 4, wy, x0 + bx + 10, wy + 4],
                        fill=(250, 210, 90))
    # searchlight beams
    d.polygon([(x0 + 60, y1), (x0 + 120, y0 + 6), (x0 + 132, y0 + 6),
               (x0 + 78, y1)], fill=(250, 220, 120))
    d.text((x0 + 10, y0 + 4), "ZAPORIZHZHIA", font=sans_b(9), fill=WHITE)


def scene_tanker(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 60, 84))
    d.line([(x0, y1 - 12), (x1, y1 - 12)], fill=(90, 140, 180), width=2)
    # tanker hull and containers
    d.polygon([(x0 + 12, y1 - 22), (x0 + 160, y1 - 22), (x0 + 172, y1 - 12),
               (x0 + 6, y1 - 12)], fill=(150, 60, 40))
    for cx in range(x0 + 26, x0 + 150, 22):
        d.rectangle([cx, y1 - 34, cx + 18, y1 - 22], fill=(200, 190, 120))
    d.rectangle([x0 + 150, y1 - 40, x0 + 166, y1 - 22], fill=(220, 220, 220))
    # circuit traces + shield
    d.line([(x0 + 20, y0 + 8), (x0 + 60, y0 + 8), (x0 + 60, y0 + 16)],
           fill=(120, 220, 160), width=2)
    d.ellipse([x0 + 58, y0 + 14, x0 + 64, y0 + 20], fill=(120, 220, 160))
    d.polygon([(x0 + 168, y0 + 6), (x0 + 182, y0 + 12), (x0 + 182, y0 + 22),
               (x0 + 175, y0 + 28), (x0 + 168, y0 + 22), (x0 + 168, y0 + 12)],
              fill=GOLD_L)
    d.text((x0 + 10, y0 + 4), "~50 TANKERS", font=sans_b(9), fill=WHITE)


def scene_quake(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(150, 190, 220))
    # Himalaya ridge
    d.polygon([(x0, y1), (x0 + 40, y0 + 12), (x0 + 80, y1)], fill=(90, 110, 130))
    d.polygon([(x0 + 55, y1), (x0 + 110, y0 + 4), (x0 + 165, y1)],
              fill=(70, 90, 112))
    d.polygon([(x0 + 100, y0 + 4), (x0 + 110, y0 + 4), (x0 + 118, y0 + 16),
               (x0 + 102, y0 + 16)], fill=WHITE)
    # seismograph zigzag
    pts = [(x0 + 8, y1 - 10)]
    for i, dy in enumerate((-14, 10, -22, 16, -8, 6, -16, 12, -6, 4)):
        pts.append((x0 + 8 + (i + 1) * 16, y1 - 10 + dy))
    d.line(pts, fill=RED, width=2)
    d.text((x0 + 10, y0 + 4), "M5.6", font=sans_b(13), fill=INK)


def scene_scales(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(200, 196, 180))
    # police HQ columns
    for cx in range(x0 + 14, x0 + 110, 22):
        d.rectangle([cx, y0 + 8, cx + 10, y1 - 10], fill=(120, 110, 92))
    d.rectangle([x0 + 8, y0 + 4, x0 + 116, y0 + 10], fill=(90, 82, 66))
    # scales of justice
    sx, sy = x0 + 148, y0 + 12
    d.line([(sx, sy), (sx, sy + 26)], fill=INK, width=2)
    d.line([(sx - 18, sy + 4), (sx + 18, sy + 4)], fill=INK, width=2)
    d.polygon([(sx - 24, sy + 18), (sx - 12, sy + 18), (sx - 18, sy + 8)],
              fill=GOLD)
    d.polygon([(sx + 12, sy + 18), (sx + 24, sy + 18), (sx + 18, sy + 8)],
              fill=GOLD)
    d.text((x0 + 10, y1 - 14), "TREASON CHARGE", font=sans_b(9), fill=INK)


def scene_factory(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(52, 44, 40))
    # sawtooth factory roof
    d.polygon([(x0 + 8, y1 - 8), (x0 + 8, y1 - 28), (x0 + 40, y1 - 28),
               (x0 + 40, y1 - 20), (x0 + 72, y1 - 20), (x0 + 72, y1 - 28),
               (x0 + 104, y1 - 28), (x0 + 104, y1 - 8)], fill=(120, 110, 100))
    d.rectangle([x0 + 118, y1 - 34, x0 + 126, y1 - 8], fill=(120, 110, 100))
    # flames
    for fx, fh in ((20, 18), (48, 26), (78, 16)):
        d.polygon([(x0 + fx, y1 - 8), (x0 + fx + 7, y1 - 8 - fh),
                   (x0 + fx + 14, y1 - 8)], fill=(240, 120, 30))
        d.polygon([(x0 + fx + 3, y1 - 8), (x0 + fx + 7, y1 - 8 - fh + 8),
                   (x0 + fx + 11, y1 - 8)], fill=(250, 200, 60))
    d.text((x0 + 10, y0 + 4), "24 DEAD \u00b7 SAT 21 NOV FIRE", font=sans_b(9),
           fill=WHITE)


def scene_co2(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(210, 225, 215))
    # ground layers
    d.rectangle([x0, y0 + 22, x1, y0 + 30], fill=(120, 150, 90))
    d.rectangle([x0, y0 + 30, x1, y1], fill=(150, 120, 90))
    # plant + capture arrows down to storage
    d.rectangle([x0 + 16, y0 + 6, x0 + 52, y0 + 22], fill=(90, 110, 120))
    d.rectangle([x0 + 44, y0 + 2, x0 + 48, y0 + 8], fill=(90, 110, 120))
    for ax in (70, 100, 130):
        d.line([(x0 + ax, y0 + 10), (x0 + ax, y1 - 12)], fill=TEAL, width=2)
        d.polygon([(x0 + ax - 4, y1 - 12), (x0 + ax + 4, y1 - 12),
                   (x0 + ax, y1 - 6)], fill=TEAL)
    d.ellipse([x0 + 140, y1 - 18, x0 + 172, y1 - 6], fill=(60, 90, 110))
    d.text((x0 + 10, y0 + 32), "CO\u2082 STORED UNDERGROUND", font=sans_b(8),
           fill=INK)


def scene_servers(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(26, 32, 44))
    for rx in range(x0 + 10, x1 - 10, 42):
        d.rectangle([rx, y0 + 6, rx + 34, y1 - 8], fill=(48, 58, 76),
                    outline=(90, 100, 120), width=1)
        for ry in range(y0 + 10, y1 - 12, 9):
            d.rectangle([rx + 4, ry, rx + 22, ry + 5], fill=(60, 200, 120))
            d.ellipse([rx + 27, ry + 1, rx + 30, ry + 4], fill=GOLD_L)
    # prohibition sign
    cx, cy = x0 + 158, y0 + 16
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=RED, width=3)
    d.line([(cx - 8, cy + 8), (cx + 8, cy - 8)], fill=RED, width=3)
    d.text((x0 + 10, y1 - 13), "7 FIRMS CUT OFF", font=sans_b(9), fill=WHITE)


SCENES = {
    "drone": scene_drone, "chart": scene_chart, "chess": scene_chess,
    "jet": scene_jet, "pacific": scene_pacific, "rocket": scene_rocket,
    "citynight": scene_citynight, "tanker": scene_tanker,
    "quake": scene_quake, "scales": scene_scales, "factory": scene_factory,
    "co2": scene_co2, "servers": scene_servers,
}


def project(lon, lat, x0, y0, w, h):
    """Equirectangular projection: lon -180..180, lat 84..-56."""
    px = x0 + (lon + 180.0) / 360.0 * w
    py = y0 + (84.0 - lat) / 140.0 * h
    return px, py


def draw_world_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=SEA)
    for poly in CONTINENTS:
        pts = [project(lon, lat, x0, y0, x1 - x0, y1 - y0) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(140, 142, 118))
    for num, lon, lat, dx, dy in PINS:
        px, py = project(lon, lat, x0, y0, x1 - x0, y1 - y0)
        if dx or dy:
            d.line([(px, py), (px + dx, py + dy)], fill=INK, width=1)
            px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=WHITE, width=1)
        d.text((px, py), str(num), font=sans_b(9), fill=WHITE, anchor="mm")

# ---------------------------------------------------------------- build
def build():
    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    heights = {}
    y = 0

    # ---- masthead: kicker, giant date, count line -------------------
    mh = 104
    d.rectangle([0, y, W, y + mh], fill=NAVY)
    d.rectangle([0, y + mh, W, y + mh + 3], fill=GOLD_L)
    d.text((W // 2, y + 5), "THE WORLD ON ONE PAGE", font=sans_b(13),
           fill=GOLD_L, anchor="ma")
    # date: largest element on the page, auto-fit to the canvas width
    size = 72
    while size > 20:
        f_date = serif_b(size)
        if d.textlength(DATE_LINE, font=f_date) <= W - 48:
            break
        size -= 1
    d.text((W // 2, y + 20), DATE_LINE, font=f_date, fill=WHITE, anchor="ma")
    d.text((W // 2, y + 20 + size + 5), COUNT_LINE, font=sans_b(14),
           fill=(220, 220, 220), anchor="ma")
    print("date font size: %d px" % size)
    heights["masthead"] = mh
    y += mh + 4

    # ---- UTC timeline ribbon ----------------------------------------
    uh = 34
    d.rectangle([24, y, W - 24, y + uh], fill=NAVY2)
    col_w = (W - 48) / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = 24 + col_w * i + col_w / 2
        d.text((cx, y + 2), when, font=sans_b(12), fill=GOLD_L, anchor="ma")
        lines = fit_text(d, what, sans(9), col_w - 10, 1)
        d.text((cx, y + 16), lines[0], font=sans(9), fill=WHITE, anchor="ma")
        d.ellipse([cx - 2, y + 28, cx + 2, y + 32], fill=GOLD_L)
    heights["utc"] = uh
    y += uh + 4

    # ---- three hero picture cards ------------------------------------
    hh = 220
    cw = (W - 48 - 2 * 12) // 3
    for i, hero in enumerate(HEROES):
        x0 = 24 + i * (cw + 12)
        x1 = x0 + cw
        d.rectangle([x0, y, x1, y + hh], outline=LIGHT, width=1)
        d.rectangle([x0, y, x1, y + hh], fill=WHITE)
        img_h = 82
        SCENES[hero["scene"]](d, (x0 + 1, y + 1, x1 - 1, y + img_h))
        ty = y + img_h + 6
        d.text((x0 + 10, ty), "%d \u00b7 %s" % (hero["num"], hero["region"]),
               font=sans_b(10), fill=RED)
        d.text((x1 - 10, ty), hero["tag"], font=sans_b(10),
               fill=tag_color(hero["tag"]), anchor="ra")
        ty += 15
        lines = fit_text(d, hero["headline"], serif_b(16), cw - 20, 3)
        ty = draw_wrapped(d, lines, x0 + 10, ty, serif_b(16), INK, 19)
        ty += 3
        lines = fit_text(d, hero["body"], sans(11), cw - 20, 3)
        ty = draw_wrapped(d, lines, x0 + 10, ty, sans(11), INK, 13)
        d.text((x0 + 10, y + hh - 14), hero["source"], font=sans(8),
               fill=GREY)
    heights["heroes"] = hh
    y += hh + 4

    # ---- the day in numbers: six big figures -------------------------
    nh = 56
    d.rectangle([24, y, W - 24, y + nh], fill=CREAM)
    d.text((36, y + 3), "THE DAY IN NUMBERS", font=sans_b(11), fill=NAVY)
    ncol = (W - 48) / 6
    for i, (value, label) in enumerate(NUMBERS):
        cx = 24 + ncol * i + ncol / 2
        d.text((cx, y + 14), value, font=sans_b(24), fill=INK, anchor="ma")
        lines = fit_text(d, label, sans(9), ncol - 12, 2)
        ly = y + 38
        for line in lines:
            d.text((cx, ly), line, font=sans(9), fill=GREY, anchor="ma")
            ly += 9
    heights["numbers"] = nh
    y += nh + 4

    # ---- minor picture cards: 5 x 2 grid ------------------------------
    d.text((28, y), "MORE FROM TUESDAY", font=sans_b(13), fill=NAVY)
    d.line([190, y + 5, W - 28, y + 5], fill=LIGHT, width=1)
    y += 15
    heights["minor_heading"] = 15
    mh_card, gap = 126, 8
    mcw = (W - 48 - 4 * gap) // 5
    for i, minor in enumerate(MINORS):
        col, row = i % 5, i // 5
        x0 = 24 + col * (mcw + gap)
        x1 = x0 + mcw
        y0 = y + row * (mh_card + gap)
        d.rectangle([x0, y0, x1, y0 + mh_card], outline=LIGHT, width=1)
        d.rectangle([x0, y0, x1, y0 + mh_card], fill=WHITE)
        img_h = 50
        SCENES[minor["scene"]](d, (x0 + 1, y0 + 1, x1 - 1, y0 + img_h))
        ty = y0 + img_h + 4
        tagline = "%d \u00b7 %s \u00b7 %s" % (minor["num"], minor["region"],
                                            minor["tag"])
        d.text((x0 + 6, ty), tagline, font=sans_b(8),
               fill=tag_color(minor["tag"]))
        ty += 11
        lines = fit_text(d, minor["headline"], sans_b(11), mcw - 12, 2)
        ty = draw_wrapped(d, lines, x0 + 6, ty, sans_b(11), INK, 13)
        lines = fit_text(d, minor["body"], sans(9), mcw - 12, 2)
        ty = draw_wrapped(d, lines, x0 + 6, ty + 1, sans(9), INK, 11)
        src = shrink_to_width(d, minor["source"], sans(8), mcw - 12)
        d.text((x0 + 6, y0 + mh_card - 11), src, font=sans(8), fill=GREY)
    heights["minor_grid"] = 2 * mh_card + gap
    y += 2 * mh_card + gap + 4

    # ---- world map + numbered index ------------------------------------
    mh2 = 198
    map_w = 470
    d.text((28, y), "WHERE IT HAPPENED", font=sans_b(13), fill=NAVY)
    d.text((24 + map_w + 16, y), "ALSO ON TUESDAY 24 NOVEMBER",
           font=sans_b(13), fill=NAVY)
    my = y + 18
    draw_world_map(d, (24, my, 24 + map_w, my + mh2 - 18))
    ix0 = 24 + map_w + 16
    ix1 = W - 24
    col_w = (ix1 - ix0 - 8) // 2
    f_city = sans_b(9)
    f_item = sans(9)
    for i, (num, city, text) in enumerate(INDEX):
        col, row = i % 2, i // 2
        xx = ix0 + col * (col_w + 8)
        yy = my + row * 18
        label = "%d %s \u2014 " % (num, city)
        label_w = d.textlength(label, font=f_city)
        # wrap the item text: first line shares the row with the label,
        # the second line uses the full column width
        lines, cur, limit, dropped = [], "", col_w - label_w, False
        for word in text.split(" "):
            trial = (cur + " " + word).strip()
            if d.textlength(trial, font=f_item) <= limit:
                cur = trial
            elif len(lines) == 0:
                lines.append(cur)
                cur = word
                limit = col_w
            else:
                lines.append(cur)
                dropped = True
                break
        if cur and len(lines) < 2:
            lines.append(cur)
        if dropped and len(lines) == 2:
            while d.textlength(lines[1] + " \u2026", font=f_item) > col_w:
                lines[1] = " ".join(lines[1].split(" ")[:-1])
            lines[1] = lines[1] + " \u2026"
        d.text((xx, yy), label, font=f_city, fill=RED)
        d.text((xx + label_w, yy), lines[0], font=f_item, fill=INK)
        if len(lines) > 1:
            d.text((xx, yy + 9), lines[1], font=f_item, fill=INK)
    heights["map_index"] = mh2
    y += mh2 + 4

    # ---- date check ------------------------------------------------------
    dh = 56
    d.rectangle([24, y, W - 24, y + dh], outline=RED, width=2)
    d.text((36, y + 3), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
           font=sans_b(12), fill=RED)
    lines = fit_text(d, DATECHECK, sans(9), W - 72, 3)
    if lines and "\u2026" in lines[-1]:
        print("WARNING: DATE CHECK text truncated!")
    draw_wrapped(d, lines, 36, y + 17, sans(9), INK, 12)
    heights["datecheck"] = dh
    y += dh + 4

    # ---- footer: legend + sources ----------------------------------------
    fh = H - y - 2
    d.text((28, y + 2), "CONFIRMED 2+ outlets  \u00b7  OFFICIAL on the record  "
           "\u00b7  REPORTED one outlet", font=sans_b(10), fill=NAVY)
    lines = fit_text(d, SOURCES, sans(9), W - 56, 2)
    draw_wrapped(d, lines, 28, y + 16, sans(9), GREY, 11)
    heights["footer"] = fh
    y += fh

    print("block heights:", heights)
    print("total height used: %d / %d (bottom margin %d px)" % (y, H, H - y))
    assert y <= H, "layout overflow: %d > %d" % (y, H)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote %s (%d bytes, %dx%d)" % (out, size, W, H))
    assert size <= 1048576, "entry.png over 1 MiB!"
    return out


if __name__ == "__main__":
    build()
