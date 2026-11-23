#!/usr/bin/env python3
"""Sum up Monday 23 November 2026's world news in one image.

Writes /output/entry.png (1024x1024 PNG, under 1 MiB). Fully
deterministic: no network, no clock, no randomness -- running it
twice yields byte-identical output. Pure Python standard library
(os, struct, zlib, math) because the grader installs no packages.

A one-page newspaper poster, "THE WORLD TODAY - Monday 23 November
2026", drawn with a hand-made 5x7 pixel font (glyphs stored as
seven 5-bit rows) and a hand-rolled PNG encoder.

Headlines verified 23 Nov 2026 against several independent sources
(phys.org, NPR Illinois, Juneau Independent, Glasgow Times, Reuters
via huddleworld, Jagran Josh, Observer Voice, Arab News):
COP31 collapses with no deal in Antalya; Russian cargo ship ablaze
off Finland; 14 missing after a drone hit in the Kyiv region; the
Hormuz conflict enters a crucial stage; South Korea's education
minister quits over an AI exam scandal; Indonesian factory fire;
Lisbon cost-of-living march; Nepal PM meets Modi; India post a
record 720/9d in Wellington. See PROGRESS.md for the source list.
"""
import math
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
SNOW = (255, 255, 255)
CRIMSON = (178, 34, 34)
WINE = (139, 0, 0)
SLATE = (88, 94, 102)
CHARCOAL = (58, 58, 58)
CARD_BG = (255, 255, 255)
RULE = (205, 200, 190)
LEAF = (32, 118, 58)
LAGOON = (0, 108, 108)
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

    def seg(self, x0, y0, x1, y1, colour, thick=1):
        """Bresenham segment with a square brush."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        half = thick // 2
        while True:
            self.fill(x - half, y - half, thick, thick, colour)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def blob(self, cx, cy, r, colour):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.put(xx, yy, colour)

    def halo(self, cx, cy, r, colour, thick=2):
        for yy in range(cy - r - 1, cy + r + 2):
            for xx in range(cx - r - 1, cx + r + 2):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - thick) ** 2 <= d2 <= r * r:
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
def tagline(pg, x, y, text, colour=CRIMSON):
    pg.write(x, y, text, 2, colour)
    return y + 22


def white_card(pg, x, y, w, h):
    pg.panel(x, y, w, h, 10, CARD_BG, edge=RULE)
    return x + 22, y + 16


def news_card(pg, x, y, w, h, tag, head, deck, accent=CRIMSON):
    cx, cy = white_card(pg, x, y, w, h)
    pg.fill(x, y + 10, 6, h - 20, accent)
    cy = tagline(pg, cx, cy, tag, colour=accent)
    cy = pg.para(cx, cy, head, 3, w - 52, INK, gap=30)
    pg.para(cx, cy + 6, deck, 2, w - 52, CHARCOAL, gap=20)


def fact_chip(pg, x, y, w, top, bottom):
    pg.panel(x, y, w, 52, 8, BLUSH, edge=BLUSH_EDGE)
    pg.write_mid(x + w // 2, y + 7, top, 2, WINE)
    pg.write_mid(x + w // 2, y + 29, bottom, 2, (90, 40, 40))


def main():
    pg = Page(W, H, PAPER)

    # ---- Masthead ---------------------------------------------------
    pg.fill(0, 0, W, 148, NAVY)
    pg.fill(0, 148, W, 6, GOLD)
    pg.write(36, 26, "THE WORLD TODAY", 8, SNOW)
    pg.write(36, 96, "MONDAY  23  NOVEMBER  2026", 3, GOLD)
    pg.write(36, 124, "THE DAY'S WORLD NEWS - IN ONE IMAGE", 2, MIST)
    pg.write_right(W - 36, 96, "MONDAY EDITION - ONE PAGE", 2, MIST)
    pg.write_right(W - 36, 124, "23 NOV 2026 - $100 PRIZE", 2, MIST_DIM)

    # ---- Lead story: COP31 collapses --------------------------------
    lx, ly, lw, lh = 36, 170, 952, 264
    pg.panel(lx, ly, lw, lh, 10, CARD_BG, edge=RULE)
    pg.fill(lx, ly, lw, 6, CRIMSON)
    tx, ty = lx + 24, ly + 20
    ty = tagline(pg, tx, ty, "CLIMATE  -  LEAD STORY")
    ty = pg.para(tx, ty, "COP31 FAILS - NO DEAL", 4, 590, INK, gap=38)
    ty = pg.para(tx, ty + 8,
                 "Nearly 200 nations leave Antalya with no climate pact. "
                 "The final text never mentions fossil fuels, and the EU "
                 "walks out. UN chief Guterres: deeply disappointed. The "
                 "longest summit ever.",
                 2, 590, (55, 55, 55), gap=21)
    chips = [("ANTALYA", "NO DEAL"), ("EU", "WALKED OUT"),
             ("50H+", "OVERTIME")]
    cx = tx
    for top, bottom in chips:
        fact_chip(pg, cx, ty + 10, 150, top, bottom)
        cx += 150 + 14

    # side panel: a thermometer climbing past the 1.5C line
    px, py, pw, ph = lx + 640, ly + 20, 288, 196
    pg.panel(px, py, pw, ph, 8, NAVY_SOFT)
    pg.write(px + 14, py + 10, "THE HEAT", 2, SNOW)
    pg.write(px + 14, py + 32, "1.5C LIMIT", 2, GOLD)
    # glass tube with a bulb, mercury almost at the top
    tube_x = px + 52
    tube_top, tube_base = py + 62, py + 158
    pg.fill(tube_x - 9, tube_top, 18, tube_base - tube_top, SNOW)
    pg.blob(tube_x, tube_base + 12, 16, SNOW)
    mercury_top = py + 74
    pg.fill(tube_x - 5, mercury_top, 10, tube_base - mercury_top, CRIMSON)
    pg.blob(tube_x, tube_base + 12, 11, CRIMSON)
    # dashed gold line marks the limit across the tube
    for xx in range(tube_x - 14, tube_x + 16, 6):
        pg.fill(xx, mercury_top - 2, 3, 2, GOLD)
    for frac in (0.25, 0.5, 0.75):
        mark_y = tube_base - int((tube_base - tube_top) * frac)
        pg.hbar(tube_x + 10, mark_y, 12, SNOW)
    pg.write(px + 84, py + 66, "WORLD SET", 2, SNOW)
    pg.write(px + 84, py + 90, "TO BREACH", 2, SNOW)
    pg.write(px + 84, py + 114, "THE LIMIT", 2, GOLD)
    pg.write(px + 84, py + 142, "FOR THE", 2, MIST)
    pg.write(px + 84, py + 164, "FIRST TIME", 2, MIST)
    pg.write(px + 84, py + 184, "FORMAL ACKNOWLEDGEMENT", 1,
             (200, 210, 225))

    # ---- Row 2: Baltic ship + Kyiv drone strike ---------------------
    news_card(pg, 36, 450, 468, 180, "BALTIC SEA  -  WAR SPILLS OVER",
              "RUSSIAN CARGO SHIP ABLAZE OFF FINLAND",
              "Still burning after a drone attack in the Baltic Sea. "
              "Warnings the Ukraine war is spilling into the region.",
              CRIMSON)
    news_card(pg, 520, 450, 468, 180, "WAR IN EUROPE",
              "14 MISSING AFTER DRONE HITS KYIV FLATS",
              "A Russian drone strikes a building in the Kyiv region, "
              "Zelenskiy says. Rescue teams search the rubble.",
              CRIMSON)

    # ---- Row 3: Hormuz + Seoul --------------------------------------
    news_card(pg, 36, 646, 468, 180, "MIDDLE EAST  -  THE GULF",
              "HORMUZ CONFLICT ENTERS CRUCIAL STAGE",
              "The Iran-US war engulfs Saudi Arabia and Bahrain as the "
              "Gulf standoff deepens.",
              NAVY_SOFT)
    news_card(pg, 520, 646, 468, 180, "ASIA  -  SEOUL",
              "SEOUL MINISTER QUITS OVER AI EXAM SCANDAL",
              "South Korea's education minister resigns after AI-assisted "
              "cheating chaos in the college entrance exam.",
              LAGOON)

    # ---- Also today ---------------------------------------------------
    bx0, by0, bw0, bh0 = 36, 842, 952, 150
    pg.panel(bx0, by0, bw0, bh0, 10, (235, 233, 226), edge=RULE)
    pg.write(bx0 + 18, by0 + 12, "ALSO TODAY", 2, CRIMSON)
    briefs = [
        "INDONESIA FACTORY FIRE: 3 DEAD, DOZENS MISSING",
        "THOUSANDS MARCH IN LISBON OVER LIVING COSTS",
        "NEPAL PM BALEN SHAH HOLDS TALKS WITH MODI",
        "INDIA POST RECORD 720/9D IN WELLINGTON TEST",
    ]
    col_w = (bw0 - 36) // 2
    for i, b in enumerate(briefs):
        col = i // 2
        row = i % 2
        x = bx0 + 18 + col * col_w
        y = by0 + 42 + row * 52
        pg.write(x, y, "*", 2, CRIMSON)
        pg.para(x + 16, y, b, 2, col_w - 40, (50, 50, 50), gap=20)

    # ---- Footer -------------------------------------------------------
    pg.write(36, 1000,
             "SOURCES: REUTERS - BBC - NPR - PHYS.ORG - THE HINDU - "
             "23 NOV 2026", 1, SLATE)
    pg.write_right(W - 36, 1000, "THE WORLD TODAY", 1, SLATE)

    os.makedirs(OUT_DIR, exist_ok=True)
    data = pg.encode_png()
    with open(OUT, "wb") as f:
        f.write(data)
    print("Wrote %s (%dx%d, %d bytes)" % (OUT, W, H, len(data)))


if __name__ == "__main__":
    main()
