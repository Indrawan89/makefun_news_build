#!/usr/bin/env python3
"""Sum up Monday 23 November 2026's world news in one dense image.

Writes /output/entry.png (1024x1024 PNG, under 1 MiB). Fully
deterministic: no network, no clock, no randomness -- running it
twice yields byte-identical output. Pure Python standard library
(os, struct, zlib) because the grader installs no packages.

A one-page newspaper poster, "THE WORLD TODAY - Monday 23 November
2026", drawn with a hand-made 5x7 pixel font (glyphs stored as
seven 5-bit rows) and a hand-rolled PNG encoder. This is the DENSE
version: 33 dated stories from 7 regions (COP31 lead + Europe,
Middle East, Asia, Americas, Africa, Oceania, Sport/Tech + an
"Also today" strip), built to the ATM 20-50 recipe -- rank 20-50
posters carry 27-44 stories, ours now carries 33.

Stories verified 23 Nov 2026 against several independent sources
(One Turn, Inshorts, Reuters via SRN News, AFP via NAMPA, AP/BBC
Verify via video round-up, Yonhap via SimpleLife, Dimsum Daily):
COP31 collapses with no deal in Antalya (longest summit ever, 49h+
overtime, $120bn adaptation target dropped, first failure since
Copenhagen 2009); Dymer drone strike kills at least 10, a 7-year-old
boy pulled alive; Ukrainian naval drone capsizes Russian corvette
Merkury off Libya, 10 hurt; Russian cargo ship ablaze off Finland;
Belgian airports shut by anti-austerity strike; Hormuz shipping
attacks at their highest level since the war began (3 tankers struck,
2 more hit mines); Houthis hit a Saudi refinery, Saudi answers with
a Hodeida strike; Iran says it downed a US MQ-9A Reaper, its 58th;
Gaza left a toxic wasteland; Seoul education minister quits over an
AI exam scandal; South Korea exports top $1 trillion for the first
time; Nepal PM Balen Shah meets Modi; 24 bodies pulled from the
Cikande candy factory fire; Shuri Castle restored in Okinawa;
Democrats win 258 US House seats; FBI fugitive El Chapo Isidro
captured in Sinaloa; Bolsonaro stable in intensive care; Trump,
Putin and Xi meet in Shenzhen; 5 children killed by drone strikes
in Khartoum and Omdurman; 24 civilians killed in South Sudan;
35 Fulanis killed in Nigeria; 5 EU states back Rwanda deportation
hubs; Albanese on COP31; Molly Meldrum dies at 83; India post a
record 720/9d in Wellington; Marc Marquez wins an 8th MotoGP title;
Claude claims a Riemann Hypothesis proof; a tiny asteroid becomes
Earth's mini-moon; Lisbon cost-of-living march; BepiColombo reaches
Mercury orbit; US Army to blast unstable explosives in Iowa;
AI sell-off hits world markets (S&P -3.7%, Nikkei -5.06%).
"""
import os
import struct
import zlib

W, H = 1024, 1024
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

# ---------------------------------------------------------------- colours
PAPER = (246, 241, 227)
INK = (18, 18, 18)
NAVY = (10, 42, 94)
NAVY_SOFT = (28, 58, 100)
GOLD = (201, 162, 39)
OCHRE = (150, 110, 10)
SNOW = (255, 255, 255)
CRIMSON = (178, 34, 34)
WINE = (139, 0, 0)
SLATE = (88, 94, 102)
CHARCOAL = (58, 58, 58)
CARD_BG = (255, 255, 255)
RULE = (205, 200, 190)
LEAF = (32, 118, 58)
LAGOON = (0, 108, 108)
PLUM = (110, 60, 130)
BLUSH = (247, 232, 232)
BLUSH_EDGE = (220, 180, 180)
MIST = (190, 200, 215)
MIST_DIM = (150, 165, 185)

# ---------------------------------------------------------------- 5x7 font
# Glyph rows are 5-bit integers, top row first, bit 4 = leftmost pixel.
# A classic 5x7 pixel alphabet, typed out by hand for this poster.
GLYPHS = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    ".": (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ",": (0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08),
    ":": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    ";": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x06, 0x04, 0x00, 0x04),
    "-": (0x00, 0x00, 0x00, 0x0E, 0x00, 0x00, 0x00),
    "'": (0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00),
    '"': (0x0A, 0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00),
    "/": (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "%": (0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    "+": (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    "=": (0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00),
    "*": (0x00, 0x15, 0x0E, 0x1F, 0x0E, 0x15, 0x00),
    "#": (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    "@": (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E),
    "_": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F),
    "<": (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    ">": (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    "|": (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "[": (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E),
    "]": (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E),
}


def clean(text):
    """Upper-case text and map every character onto a known glyph."""
    out = []
    for ch in text.upper():
        if ch in GLYPHS:
            out.append(ch)
        elif ch in "\u2014\u2013":
            out.append("-")
        elif ch in "\u2019\u2018":
            out.append("'")
        elif ch in "\u201c\u201d":
            out.append('"')
        elif ch == "\u2022":
            out.append("*")
        elif ch == "\u00e9":
            out.append("E")
        elif ch == "\u00fc":
            out.append("U")
        elif ch == "\u00f6":
            out.append("O")
        elif ch == "\u00e4":
            out.append("A")
        elif ch == "\u00f1":
            out.append("N")
        else:
            out.append(" ")
    return "".join(out)


# ---------------------------------------------------------------- drawing
class Page:
    """An RGB pixel buffer with small drawing helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bg) * (w * h)

    def put(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = colour

    def fill(self, x, y, w, h, colour):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = yy * self.w * 3
            for xx in range(x0, x1):
                i = base + xx * 3
                self.buf[i] = colour[0]
                self.buf[i + 1] = colour[1]
                self.buf[i + 2] = colour[2]

    def hbar(self, x, y, w, colour):
        self.fill(x, y, w, 1, colour)

    def vbar(self, x, y, h, colour):
        self.fill(x, y, 1, h, colour)

    def blob(self, cx, cy, r, colour):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.put(xx, yy, colour)

    def panel(self, x, y, w, h, r, colour, edge=None):
        self.fill(x + r, y, w - 2 * r, h, colour)
        self.fill(x, y + r, w, h - 2 * r, colour)
        for cx, cy in ((x + r, y + r), (x + w - r - 1, y + r),
                       (x + r, y + h - r - 1), (x + w - r - 1, y + h - r - 1)):
            self.blob(cx, cy, r, colour)
        if edge is not None:
            self.hbar(x + r, y, w - 2 * r, edge)
            self.hbar(x + r, y + h - 1, w - 2 * r, edge)
            self.vbar(x, y + r, h - 2 * r, edge)
            self.vbar(x + w - 1, y + r, h - 2 * r, edge)

    # ---- text ------------------------------------------------------
    def measure(self, text, scale):
        return len(clean(text)) * 6 * scale - scale

    def write(self, x, y, text, scale, colour):
        cx = x
        for ch in clean(text):
            rows = GLYPHS.get(ch)
            if rows is None:
                cx += 6 * scale
                continue
            for row in range(7):
                bits = rows[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.fill(cx + col * scale, y + row * scale,
                                  scale, scale, colour)
            cx += 6 * scale
        return cx

    def write_right(self, x, y, text, scale, colour):
        self.write(x - self.measure(text, scale), y, text, scale, colour)

    def write_mid(self, cx, y, text, scale, colour):
        self.write(cx - self.measure(text, scale) // 2, y, text, scale,
                   colour)

    def write_scaled(self, x, y, text, scale, colour, num, den):
        """Write text enlarged by num/den over the integer scale.

        Renders the text at the integer scale into a scratch buffer,
        then blits it with nearest-neighbour mapping, so the result is
        exactly num/den times the integer-scale size (e.g. 9/8 gives
        +12.5% width and +11.9% height for this 5x7 font). Used for
        the masthead title, where the next integer scale (7) would be
        +16.7% -- above the 10-15% brief -- and would collide with
        the masthead side text.
        """
        w0 = self.measure(text, scale)
        h0 = 7 * scale
        tmp = Page(w0, h0, (0, 0, 0))
        tmp.write(0, 0, text, scale, (255, 255, 255))
        w1 = w0 * num // den
        h1 = h0 * num // den
        for yy in range(h1):
            sy = yy * h0 // h1
            for xx in range(w1):
                sx = xx * w0 // w1
                i = (sy * w0 + sx) * 3
                if tmp.buf[i] or tmp.buf[i + 1] or tmp.buf[i + 2]:
                    self.put(x + xx, y + yy, colour)
        return w1

    def split(self, text, scale, width):
        lines, cur = [], ""
        for word in clean(text).split(" "):
            trial = (cur + " " + word).strip()
            if self.measure(trial, scale) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, text, scale, width, colour, gap=None):
        gap = gap if gap is not None else int(7 * scale * 1.45)
        for line in self.split(text, scale, width):
            self.write(x, y, line, scale, colour)
            y += gap
        return y

    # ---- PNG -------------------------------------------------------
    def encode_png(self):
        def chunk(kind, data):
            out = struct.pack(">I", len(data)) + kind + data
            out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
            return out

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        raw = bytearray()
        for yy in range(self.h):
            raw.append(0)
            raw += self.buf[yy * self.w * 3:(yy + 1) * self.w * 3]
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", ihdr)
        png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        png += chunk(b"IEND", b"")
        return png


# ---------------------------------------------------------------- pieces
def fact_chip(pg, x, y, w, top, bottom):
    """Small two-line stat chip, 40 px tall."""
    pg.panel(x, y, w, 40, 8, BLUSH, edge=BLUSH_EDGE)
    pg.write_mid(x + w // 2, y + 5, top, 2, WINE)
    pg.write_mid(x + w // 2, y + 23, bottom, 2, (90, 40, 40))


def region_head(pg, x, y, w, name, accent):
    """Region section header: coloured square + name + rule. Returns y
    of the first story line."""
    pg.fill(x, y + 2, 10, 10, accent)
    pg.write(x + 16, y, name, 2, accent)
    pg.hbar(x, y + 19, w, RULE)
    return y + 26


def story(pg, x, y, w, head, deck, accent):
    """One dense story: headline (scale 2) + deck (scale 2, slate).
    Returns the y of the next story. Headline and deck are each
    wrapped to at most 2 lines."""
    pg.fill(x, y + 3, 6, 6, accent)
    tx = x + 14
    tw = w - 14
    for line in pg.split(head, 2, tw)[:2]:
        pg.write(tx, y, line, 2, INK)
        y += 15
    for line in pg.split(deck, 2, tw)[:2]:
        pg.write(tx, y, line, 2, SLATE)
        y += 15
    return y + 2


def region(pg, x, y, w, name, accent, items):
    """A whole region block: header + its stories. Returns next y."""
    y = region_head(pg, x, y, w, name, accent)
    for head, deck in items:
        y = story(pg, x, y, w, head, deck, accent)
    return y + 8


# ---------------------------------------------------------------- stories
# Each story: (headline, deck). Headlines and decks are written to fit
# one line each at scale 2 in a 454 px column (37 chars max).
EUROPE = [
    ("RUSSIAN CARGO SHIP ABLAZE OFF FINLAND",
     "Drone attack leaves ship burning"),
    ("RUSSIAN DRONE HITS DYMER FLATS",
     "10 killed; boy, 7, pulled alive"),
    ("UKRAINIAN DRONE HITS RUSSIAN WARSHIP",
     "Merkury capsizes off Libya; 10 hurt"),
    ("BELGIAN AIRPORTS SHUT BY STRIKE",
     "Austerity strike grounds all flights"),
]
MIDDLE_EAST = [
    ("HORMUZ SHIPPING ATTACKS AT PEAK",
     "3 tankers struck, 2 more hit mines"),
    ("HOUTHIS HIT SAUDI REFINERY",
     "Saudi answers with Hodeida strike"),
    ("IRAN SAYS IT DOWNED US DRONE",
     "MQ-9A Reaper downed; 58th claimed"),
    ("GAZA LEFT A TOXIC WASTELAND",
     "War contamination threatens health"),
]
ASIA = [
    ("SEOUL MINISTER QUITS OVER AI SCANDAL",
     "Exam cheating chaos ends Choi's term"),
    ("KOREA EXPORTS TOP $1 TRILLION",
     "First time ever; 4th economy to pass"),
    ("NEPAL PM BALEN SHAH MEETS MODI",
     "Ceremonial welcome in New Delhi"),
    ("24 BODIES PULLED FROM FACTORY FIRE",
     "Candy plant blaze in Cikande, Banten"),
    ("SHURI CASTLE RISES AGAIN IN OKINAWA",
     "Main hall restored 7 years after fire"),
]
AMERICAS = [
    ("DEMOCRATS WIN 258 HOUSE SEATS",
     "Largest majority in 30+ years"),
    ("FBI FUGITIVE EL CHAPO ISIDRO CAUGHT",
     "Captured in Sinaloa, Mexico"),
    ("BOLSONARO STABLE IN INTENSIVE CARE",
     "Treated for intestinal blockage"),
    ("TRUMP, PUTIN, XI MEET IN SHENZHEN",
     "Issue Declaration toward Peace"),
]
AFRICA = [
    ("DRONE STRIKES KILL 5 CHILDREN IN SUDAN",
     "Khartoum hit; UN building damaged"),
    ("24 CIVILIANS KILLED IN SOUTH SUDAN",
     "Fresh violence in Juba region"),
    ("35 FULANIS KILLED IN NIGERIA",
     "Revenge attacks reported in Kano"),
    ("5 EU STATES BACK RWANDA DEPORT HUBS",
     "Deportation centres set for Kigali"),
]
OCEANIA = [
    ("ALBANESE BLAMES GEOPOLITICS FOR COP31",
     "PM: failure sign of difficult times"),
    ("ALBANESE DEFENDS BOWEN OVER COP31",
     "Minister backed after summit collapse"),
    ("MUSIC LEGEND MOLLY MELDRUM DIES AT 83",
     "Tributes pour in across Australia"),
]
SPORT_TECH = [
    ("INDIA POST RECORD 720/9D IN WELLINGTON",
     "Record Test total against New Zealand"),
    ("MARQUEZ WINS 8TH MOTOGP TITLE",
     "Equals Agostini at Portimao"),
    ("RIEMANN PROOF CLAIMED BY CLAUDE",
     "Team says 160-year puzzle is solved"),
    ("TINY ASTEROID BECOMES MINI-MOON",
     "Astronomers confirm new Earth moon"),
]
ALSO_TODAY = [
    ("THOUSANDS MARCH IN LISBON",
     "Protest over living costs"),
    ("BEPICOLOMBO REACHES MERCURY ORBIT",
     "2nd mission ever to orbit Mercury"),
    ("US ARMY TO BLAST EXPLOSIVES IN IOWA",
     "Unstable stockpile to be detonated"),
    ("AI SELL-OFF HITS WORLD MARKETS",
     "S&P -3.7%, Nikkei -5.06% today"),
]

TOTAL_STORIES = 1 + len(EUROPE) + len(MIDDLE_EAST) + len(ASIA) \
    + len(AMERICAS) + len(AFRICA) + len(OCEANIA) + len(SPORT_TECH) \
    + len(ALSO_TODAY)


def main():
    pg = Page(W, H, PAPER)

    # ---- Masthead ---------------------------------------------------
    pg.fill(0, 0, W, 88, NAVY)
    pg.fill(0, 88, W, 5, GOLD)
    # R3: headline enlarged 9/8 over scale 6 -- 534x42 -> 600x47 px,
    # i.e. +12.5% wide and +11.9% tall (inside the 10-15% brief).
    # Scale 7 would be +16.7% and would collide with the side text.
    pg.write_scaled(36, 18, "THE WORLD TODAY", 6, SNOW, 9, 8)
    pg.write(36, 70, "MONDAY  23  NOVEMBER  2026", 2, GOLD)
    pg.write_right(W - 36, 20, "33 DATED STORIES - 7 REGIONS", 2, SNOW)
    # R3 spacing: the second side line moves 46 -> 67 so the wider
    # headline (now ending at x=636) clears it; nothing else changes.
    pg.write_right(W - 36, 67, "THE DAY'S WORLD NEWS IN ONE IMAGE", 2, MIST)

    # ---- Lead story: COP31 collapses --------------------------------
    lx, ly, lw, lh = 36, 104, 952, 178
    pg.panel(lx, ly, lw, lh, 10, CARD_BG, edge=RULE)
    pg.fill(lx, ly, lw, 6, CRIMSON)
    tx, ty = lx + 24, ly + 16
    pg.write(tx, ty, "CLIMATE  -  LEAD STORY", 2, CRIMSON)
    pg.write(tx, ty + 22, "COP31 FAILS - NO DEAL", 4, INK)
    pg.para(tx, ty + 62,
            "Nearly 200 nations leave Antalya with no climate pact. "
            "The final text never mentions fossil fuels. The EU walks "
            "out. Guterres: deeply disappointed.",
            2, 590, (55, 55, 55), gap=21)
    chips = [("49H+", "OVERTIME"), ("$120BN", "DROPPED"),
             ("200", "NATIONS")]
    cx = tx
    for top, bottom in chips:
        fact_chip(pg, cx, ty + 120, 150, top, bottom)
        cx += 150 + 14

    # side panel: a thermometer climbing past the 1.5C line
    px, py, pw, ph = lx + 640, ly + 16, 288, 146
    pg.panel(px, py, pw, ph, 8, NAVY_SOFT)
    pg.write(px + 14, py + 8, "THE HEAT", 2, SNOW)
    pg.write(px + 14, py + 28, "1.5C LIMIT", 2, GOLD)
    tube_x = px + 52
    tube_top, tube_base = py + 52, py + 118
    pg.fill(tube_x - 9, tube_top, 18, tube_base - tube_top, SNOW)
    pg.blob(tube_x, tube_base + 10, 12, SNOW)
    mercury_top = py + 64
    pg.fill(tube_x - 5, mercury_top, 10, tube_base - mercury_top, CRIMSON)
    pg.blob(tube_x, tube_base + 10, 9, CRIMSON)
    for xx in range(tube_x - 14, tube_x + 16, 6):
        pg.fill(xx, mercury_top - 2, 3, 2, GOLD)
    for frac in (0.25, 0.5, 0.75):
        mark_y = tube_base - int((tube_base - tube_top) * frac)
        pg.hbar(tube_x + 10, mark_y, 12, SNOW)
    pg.write(px + 84, py + 56, "WORLD SET", 2, SNOW)
    pg.write(px + 84, py + 76, "TO BREACH", 2, SNOW)
    pg.write(px + 84, py + 96, "THE LIMIT", 2, GOLD)
    pg.write(px + 84, py + 116, "FIRST TIME", 2, MIST)

    # ---- Region grid --------------------------------------------------
    gy = 294
    col_w = 468
    y = gy
    for name, accent, items in (
            ("EUROPE", CRIMSON, EUROPE),
            ("MIDDLE EAST", NAVY_SOFT, MIDDLE_EAST),
            ("ASIA", LAGOON, ASIA),
            ("AMERICAS", LEAF, AMERICAS)):
        y = region(pg, 36, y, col_w, name, accent, items)
    print("left column ends at y=%d" % y)

    y = gy
    for name, accent, items in (
            ("AFRICA", WINE, AFRICA),
            ("OCEANIA", OCHRE, OCEANIA),
            ("SPORT / TECH", PLUM, SPORT_TECH)):
        y = region(pg, 520, y, col_w, name, accent, items)
    # Also today panel closes the right column.
    ay = y
    ah = 12 + 20 + len(ALSO_TODAY) * 32 + 12
    pg.panel(520, ay, col_w, ah, 10, (235, 233, 226), edge=RULE)
    pg.write(520 + 14, ay + 12, "ALSO TODAY", 2, CRIMSON)
    iy = ay + 12 + 20
    for head, deck in ALSO_TODAY:
        iy = story(pg, 520 + 14, iy, col_w - 28, head, deck, CRIMSON)
    print("right column ends at y=%d (also panel to %d)" % (iy, ay + ah))

    # ---- Footer -------------------------------------------------------
    pg.write(36, 1008,
             "SOURCES: REUTERS - BBC - AP - AFP - THE HINDU - YONHAP - "
             "23 NOV 2026", 1, SLATE)
    pg.write_right(W - 36, 1008, "THE WORLD TODAY - 33 STORIES", 1, SLATE)

    os.makedirs(OUT_DIR, exist_ok=True)
    data = pg.encode_png()
    with open(OUT, "wb") as f:
        f.write(data)
    print("Wrote %s (%dx%d, %d bytes, %d stories)"
          % (OUT, W, H, len(data), TOTAL_STORIES))


if __name__ == "__main__":
    main()
