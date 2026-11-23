"""Draw the 22 November 2026 newspaper front page (1024x1024 PNG).

Deterministic: no randomness, no network, no clock. Run twice and the
bytes come out identical.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (247, 240, 220)
INK = (18, 18, 18)
RED = (178, 34, 34)
TEAL = (0, 128, 128)
BLUE = (28, 68, 180)
GOLD = (255, 196, 0)
GREY = (110, 110, 110)
SKY = (183, 222, 240)
SEA = (140, 200, 225)

FONT_FILES = {
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "plain": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}


def load_font(kind, size):
    """Best-effort font load; falls back to the built-in bitmap font."""
    try:
        return ImageFont.truetype(FONT_FILES[kind], size)
    except Exception:
        return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + font.size + 4


def paint_cop_scene(draw, x, y, w, h):
    """Antalya: pale sky, hall blocks, a rejected text, a red cross."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(168, 200, 150))
    for bx, bw, bh in [(18, 52, 42), (88, 46, 30), (150, 58, 48)]:
        draw.rectangle([x + bx, y + h - 42 - bh, x + bx + bw, y + h - 42],
                       fill=(205, 205, 205))
    draw.ellipse([x + w - 68, y + 14, x + w - 14, y + 68], fill=(255, 210, 90))
    px, py = x + w - 168, y + 26
    draw.rectangle([px, py, px + 128, py + 96], fill="white", outline=INK, width=3)
    for i in range(4):
        ly = py + 18 + i * 20
        draw.line([px + 12, ly, px + 116, ly], fill=(120, 120, 120), width=3)
    draw.line([px + 4, py + 2, px + 124, py + 94], fill=RED, width=9)
    draw.line([px + 124, py + 2, px + 4, py + 94], fill=RED, width=9)
    draw.text((x + 10, y + h - 34), "NO DEAL",
              font=load_font("bold", 26), fill=RED)


def paint_dymer_scene(draw, x, y, w, h):
    """Dymer: two apartment blocks, a rubble heap, smoke, a crane arm."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 224, 210))
    for bx in (14, 300):
        draw.rectangle([x + bx, y + 12, x + bx + 128, y + h - 8],
                       fill=(150, 122, 88))
        for row in range(4):
            for col in range(3):
                wx = x + bx + 14 + col * 38
                wy = y + 22 + row * 22
                draw.rectangle([wx, wy, wx + 24, wy + 14], fill=(32, 32, 64))
    draw.polygon([(x + 150, y + h - 8), (x + 230, y + 42), (x + 310, y + h - 8)],
                 fill=(96, 84, 72))
    draw.rectangle([x + 218, y + 96, x + 244, y + 116], fill=RED)
    for cx, cy, r in [(240, 34, 16), (262, 24, 13), (222, 26, 11)]:
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(120, 120, 120))
    draw.line([x + 250, y + 22, x + w - 12, y + 6], fill=GOLD, width=6)


def paint_benghazi_scene(draw, x, y, w, h):
    """Benghazi: a burning warship on the water, a small drone boat."""
    sea_top = int(h * 0.60)
    draw.rectangle([x, y, x + w, y + sea_top], fill=SKY)
    draw.rectangle([x, y + sea_top, x + w, y + h], fill=SEA)
    hull_top = sea_top + 4
    draw.polygon([(x + 96, y + hull_top), (x + 330, y + hull_top),
                  (x + 306, y + hull_top + 26), (x + 122, y + hull_top + 26)],
                 fill=(64, 64, 64))
    draw.rectangle([x + 176, y + hull_top - 30, x + 206, y + hull_top],
                   fill=(64, 64, 64))
    for cx, cy, r in [(186, hull_top - 42, 12), (202, hull_top - 50, 9)]:
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(110, 110, 110))
    for fx in (128, 190, 258):
        draw.polygon([(x + fx - 15, y + hull_top), (x + fx, y + hull_top - 30),
                      (x + fx + 15, y + hull_top)], fill=(255, 140, 0))
        draw.polygon([(x + fx - 7, y + hull_top), (x + fx, y + hull_top - 18),
                      (x + fx + 7, y + hull_top)], fill=(255, 220, 0))
    draw.polygon([(x + 352, y + hull_top + 16), (x + 402, y + hull_top + 16),
                  (x + 392, y + hull_top + 28), (x + 362, y + hull_top + 28)],
                 fill=(30, 30, 30))
    draw.ellipse([x + 372, y + hull_top + 2, x + 384, y + hull_top + 14],
                 fill=RED)
    for wy in (int(h * 0.86), int(h * 0.94)):
        for sx in range(0, w, 60):
            draw.arc([x + sx, y + wy - 7, x + sx + 52, y + wy + 8],
                     start=200, end=340, fill=(30, 90, 160), width=3)


def paint_washington_scene(draw, x, y, w, h):
    """Washington: a big 258, a capitol dome, a ballot box with a tick."""
    draw.rectangle([x, y, x + w, y + h], fill=(228, 230, 238))
    draw.text((x + 12, y + 10), "258", font=load_font("bold", 62), fill=BLUE)
    draw.text((x + 16, y + 80), "SEATS", font=load_font("bold", 22), fill=GREY)
    cx, cy = x + 252, y + 52
    draw.pieslice([cx - 44, cy - 38, cx + 44, cy + 38], start=180, end=360,
                  fill="white", outline=INK, width=3)
    draw.rectangle([cx - 50, cy + 34, cx + 50, cy + 44], fill="white",
                   outline=INK, width=3)
    for i in range(5):
        px = cx - 40 + i * 19
        draw.rectangle([px, cy + 46, px + 9, cy + 68], fill="white",
                       outline=INK, width=2)
    draw.rectangle([cx - 54, cy + 70, cx + 54, cy + 79], fill="white",
                   outline=INK, width=3)
    bx, by = x + 330, y + 52
    draw.rectangle([bx, by, bx + 96, by + 64], fill="white", outline=INK, width=3)
    draw.rectangle([bx + 30, by - 14, bx + 66, by], fill=INK)
    draw.line([bx + 14, by + 36, bx + 38, by + 54], fill=RED, width=6)
    draw.line([bx + 38, by + 54, bx + 84, by + 12], fill=RED, width=6)


SCENES = {
    "cop": paint_cop_scene,
    "dymer": paint_dymer_scene,
    "benghazi": paint_benghazi_scene,
    "washington": paint_washington_scene,
}

PANELS = [
    {
        "kicker": "ANTALYA  \u2022  CLIMATE",
        "colour": RED,
        "scene": "cop",
        "headline": "COP31 collapses: no deal on fossil fuels",
        "body": "The EU and about 130 nations rejected a final text that never mentioned oil, gas or coal.",
    },
    {
        "kicker": "DYMER, UKRAINE  \u2022  WAR",
        "colour": TEAL,
        "scene": "dymer",
        "headline": "Drone strike destroys flats; boy, 7, pulled alive",
        "body": "A Shahed drone hit a five-storey block at 5 a.m.; 14 were missing \u2014 David, 7, was pulled alive after 14 hours.",
    },
    {
        "kicker": "BENGHAZI  \u2022  WAR AT SEA",
        "colour": BLUE,
        "scene": "benghazi",
        "headline": "Russian warship Merkury sunk by sea drones",
        "body": "Two sea drones hit the corvette at Benghazi naval base and it capsized. A second ship was hit that evening.",
    },
    {
        "kicker": "WASHINGTON  \u2022  US POLITICS",
        "colour": RED,
        "scene": "washington",
        "headline": "Democrats win 258 House seats, biggest since 1992",
        "body": "Chuck Hubbard beat Rep. Virginia Foxx in North Carolina after a recount, sealing the 258-seat majority.",
    },
]

ALSO_TODAY = [
    "BepiColombo reaches Mercury after 8 years; ESA reports a thruster glitch",
    "Fonusa candy factory search goes on in Cikande: 3 dead, dozens missing",
    "Peru's Sunday toll from Friday's 6.7 Jun\u00edn quake: 1 dead, 16 hurt, 853 homeless",
]


def draw_panel(draw, box, panel):
    """One story card: coloured kicker, picture, headline, body copy."""
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill="white", outline=INK, width=3)
    draw.rounded_rectangle([x, y, x + w, y + 40], radius=10,
                           fill=panel["colour"])
    draw.rectangle([x, y + 26, x + w, y + 40], fill=panel["colour"])
    draw.text((x + 14, y + 7), panel["kicker"],
              font=load_font("bold", 21), fill="white")
    SCENES[panel["scene"]](draw, x + 12, y + 52, w - 24, 124)
    ty = y + 186
    head_font = load_font("bold", 29)
    for line in wrap_text(draw, panel["headline"], head_font, w - 28):
        draw.text((x + 14, ty), line, font=head_font, fill=INK)
        ty += 32
    body_font = load_font("plain", 18)
    for line in wrap_text(draw, panel["body"], body_font, w - 28):
        draw.text((x + 14, ty), line, font=body_font, fill=(40, 40, 40))
        ty += 22


def build_page():
    page = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(page)

    draw_centered(draw, CANVAS // 2, 22, "THE WORLD IN ONE DAY",
                  load_font("bold", 58), INK)
    draw_centered(draw, CANVAS // 2, 92, "SUNDAY, 22 NOVEMBER 2026",
                  load_font("bold", 42), RED)
    draw.line([42, 148, CANVAS - 42, 148], fill=INK, width=4)
    draw_centered(draw, CANVAS // 2, 160,
                  "Four stories that defined the day \u2014 as reported",
                  load_font("plain", 24), GREY)

    margin = 30
    gap = 16
    cw = (CANVAS - 2 * margin - gap) // 2
    ch = 322
    top = 202
    for i, panel in enumerate(PANELS):
        px = margin + (i % 2) * (cw + gap)
        py = top + (i // 2) * (ch + gap)
        draw_panel(draw, (px, py, cw, ch), panel)

    strip_y = top + 2 * ch + gap + 6
    draw.rectangle([margin, strip_y, CANVAS - margin, strip_y + 108], fill=INK)
    draw_centered(draw, CANVAS // 2, strip_y + 8, "ALSO TODAY",
                  load_font("bold", 24), GOLD)
    sy = strip_y + 42
    for line in ALSO_TODAY:
        draw_centered(draw, CANVAS // 2, sy, line,
                      load_font("plain", 19), "white")
        sy += 24
    draw_centered(draw, CANVAS // 2, strip_y + 122,
                  "Stories as reported on 22 November 2026  \u2022  AP  \u2022  Reuters  \u2022  AFP  \u2022  Al Jazeera",
                  load_font("plain", 18), GREY)
    return page


if __name__ == "__main__":
    build_page().save("entry.png", format="PNG")
