"""Generate entry.png: a newspaper front page summing up 22 Nov 2026.

Run: python3 gen_image.py  -> writes entry.png (1024x1024, PNG, <1 MiB)
Facts used (verified against AP/Reuters/AFP reporting of 22 Nov 2026):
 1. COP31 in Antalya ended Sunday with NO deal: the EU and ~130 nations
    rejected a final text that never mentioned fossil fuels.
 2. A Russian Shahed drone hit a five-storey apartment block in Dymer,
    north of Kyiv, at 5 a.m. Sunday; 14 people were missing, and
    7-year-old David was pulled alive from the rubble after 14 hours.
 3. Suspected Ukrainian sea drones hit the Russian corvette Merkury at
    Benghazi naval base, Libya; it capsized and sank. A second ship
    (a Maltese-flagged commercial vessel) was hit off Benghazi that
    evening.
 4. Democrats won at least 258 US House seats -- their largest majority
    since 1992 -- after Chuck Hubbard beat Rep. Virginia Foxx in North
    Carolina following a recount.
Also: BepiColombo reached Mercury orbit after 8 years (ESA reported a
thruster glitch on Sunday); the search went on at the Fonusa candy
factory in Cikande, Indonesia (3 dead, dozens missing after Saturday's
fire); Peru's Sunday toll from Friday's 6.7 Junin quake: 1 dead,
16 injured, 853 homeless.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (14, 124, 123)
GREY = (90, 90, 90)
LIGHT = (255, 255, 255)
SKY = (186, 220, 240)
SEA = (120, 180, 215)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, x, y, w, h, kicker, kcolor, headline, summary, art):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           outline=INK, width=3, fill=LIGHT)
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=10, fill=kcolor)
    draw.rectangle([x, y + 20, x + w, y + 34], fill=kcolor)
    draw.text((x + 14, y + 7), kicker, font=font(BOLD, 19), fill=LIGHT)
    art(draw, x + 14, y + 48, w - 28, 118)
    ty = y + 178
    for line in wrap_text(draw, headline, font(BOLD, 26), w - 28):
        draw.text((x + 14, ty), line, font=font(BOLD, 26), fill=INK)
        ty += 32
    ty += 4
    for line in wrap_text(draw, summary, font(REG, 19), w - 28):
        draw.text((x + 14, ty), line, font=font(REG, 19), fill=(60, 60, 60))
        ty += 25


def art_cop(draw, x, y, w, h):
    # Antalya coast, conference hall, a pact document stamped NO DEAL
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w - 70, y + 8, x + w - 10, y + 68], fill=(250, 210, 80))
    draw.rectangle([x, y + 88, x + w, y + h], fill=(150, 190, 160))
    for bx in (x + 16, x + 88, x + 160):
        draw.rectangle([bx, y + 58, bx + 52, y + 88], fill=(200, 200, 200))
    # document
    draw.rectangle([x + 250, y + 14, x + 400, y + 104], fill=LIGHT,
                   outline=INK, width=3)
    for i in range(4):
        draw.line([x + 262, y + 30 + i * 14, x + 388, y + 30 + i * 14],
                  fill=GREY, width=3)
    # big red X over the document
    draw.line([x + 250, y + 14, x + 400, y + 104], fill=RED, width=10)
    draw.line([x + 400, y + 14, x + 250, y + 104], fill=RED, width=10)
    draw.text((x + 8, y + 96), "NO DEAL", font=font(BOLD, 20), fill=RED)


def art_dymer(draw, x, y, w, h):
    # five-storey block, middle section collapsed, crane and rubble
    draw.rectangle([x, y, x + w, y + h], fill=(210, 205, 195))
    # standing left part of the block
    draw.rectangle([x + 20, y + 10, x + 170, y + h], fill=(150, 130, 110))
    for r in range(5):
        for c in range(3):
            draw.rectangle([x + 36 + c * 44, y + 20 + r * 20,
                            x + 62 + c * 44, y + 36 + r * 20],
                           fill=(60, 60, 80))
    # standing right part
    draw.rectangle([x + 300, y + 10, x + 420, y + h], fill=(150, 130, 110))
    for r in range(5):
        for c in range(2):
            draw.rectangle([x + 316 + c * 44, y + 20 + r * 20,
                            x + 342 + c * 44, y + 36 + r * 20],
                           fill=(60, 60, 80))
    # collapsed middle: rubble pile
    draw.polygon([(x + 170, y + h), (x + 210, y + 55), (x + 250, y + 40),
                  (x + 300, y + h)], fill=(110, 100, 90))
    draw.polygon([(x + 190, y + h), (x + 230, y + 80), (x + 270, y + h)],
                 fill=(90, 80, 70))
    # smoke
    for cx, cy, r in ((x + 225, y + 22, 16), (x + 245, y + 8, 12),
                      (x + 205, y + 6, 10)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # crane arm reaching over the rubble
    draw.line([x + 380, y + 4, x + 230, y + 30], fill=(220, 170, 20), width=6)
    draw.line([x + 230, y + 30, x + 230, y + 52], fill=INK, width=3)
    draw.rectangle([x + 222, y + 52, x + 238, y + 62], fill=RED)


def art_ship(draw, x, y, w, h):
    # sea, a listing warship with flames, a drone boat on the water
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + 78, x + w, y + h], fill=SEA)
    for i in range(3):
        yy = y + 92 + i * 12
        draw.arc([x + 10 + i * 40, yy, x + 150 + i * 40, yy + 18],
                 0, 180, fill=BLUE, width=3)
    # warship hull, tilted and low in the water
    draw.polygon([(x + 130, y + 62), (x + 330, y + 62), (x + 310, y + 88),
                  (x + 150, y + 88)], fill=(70, 70, 70))
    draw.rectangle([x + 200, y + 30, x + 250, y + 62], fill=(90, 90, 90))
    draw.line([x + 225, y + 30, x + 225, y + 8], fill=INK, width=4)
    # flames on deck
    for fx, fh in ((x + 160, 26), (x + 210, 34), (x + 270, 24)):
        draw.polygon([(fx, y + 62), (fx + 12, y + 62 - fh),
                      (fx + 24, y + 62)], fill=(240, 130, 20))
        draw.polygon([(fx + 5, y + 62), (fx + 12, y + 62 - fh + 10),
                      (fx + 19, y + 62)], fill=(250, 200, 40))
    # smoke column
    for cx, cy, r in ((x + 215, y + 6, 14), (x + 235, y - 4, 10)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(100, 100, 100))
    # small drone boat approaching
    draw.polygon([(x + 360, y + 96), (x + 420, y + 96), (x + 410, y + 108),
                  (x + 370, y + 108)], fill=(40, 40, 40))
    draw.line([x + 388, y + 96, x + 388, y + 82], fill=INK, width=3)
    draw.ellipse([x + 382, y + 76, x + 394, y + 88], fill=RED)


def art_house(draw, x, y, w, h):
    # Capitol dome, ballot box, big 258
    draw.rectangle([x, y, x + w, y + h], fill=(235, 235, 240))
    # dome
    draw.pieslice([x + 150, y + 6, x + 250, y + 86], 180, 360, fill=LIGHT,
                  outline=INK, width=3)
    draw.rectangle([x + 150, y + 46, x + 250, y + 86], fill=LIGHT,
                   outline=INK, width=3)
    draw.line([x + 200, y + 6, x + 200, y - 2], fill=INK, width=3)
    draw.rectangle([x + 120, y + 86, x + 280, y + 100], fill=LIGHT,
                   outline=INK, width=3)
    # columns
    for cx in (x + 130, x + 170, x + 210, x + 250):
        draw.rectangle([cx, y + 100, cx + 12, y + 128], fill=LIGHT,
                       outline=INK, width=2)
    # ballot box
    draw.rectangle([x + 300, y + 60, x + 420, y + 128], fill=(245, 245, 245),
                   outline=INK, width=4)
    draw.rectangle([x + 340, y + 46, x + 380, y + 62], fill=INK)
    draw.line([x + 320, y + 100, x + 345, y + 122], fill=RED, width=7)
    draw.line([x + 345, y + 122, x + 400, y + 70], fill=RED, width=7)
    # big number
    draw.text((x + 16, y + 20), "258", font=font(BOLD, 64), fill=BLUE)
    draw.text((x + 20, y + 92), "SEATS", font=font(BOLD, 20), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.text((512, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 58),
           fill=INK, anchor="ma")
    d.text((512, 88), "SUNDAY, 22 NOVEMBER 2026", font=font(BOLD, 38),
           fill=RED, anchor="ma")
    d.line([40, 140, 984, 140], fill=INK, width=4)
    d.text((512, 150), "Four stories that defined the day — as reported",
           font=font(REG, 22), fill=GREY, anchor="ma")
    # panels 2x2
    pw, ph = 462, 330
    draw_panel(d, 40, 190, pw, ph, "ANTALYA  •  CLIMATE", RED,
               "COP31 collapses: no deal on fossil fuels",
               "The EU and about 130 nations rejected a final text that never "
               "mentioned oil, gas or coal.",
               art_cop)
    draw_panel(d, 522, 190, pw, ph, "DYMER, UKRAINE  •  WAR", TEAL,
               "Drone strike destroys flats; boy, 7, pulled alive",
               "A Shahed drone hit a five-storey block at 5 a.m.; 14 were "
               "missing — David, 7, was pulled alive after 14 hours.",
               art_dymer)
    draw_panel(d, 40, 540, pw, ph, "BENGHAZI  •  WAR AT SEA", BLUE,
               "Russian warship Merkury sunk by sea drones",
               "Two sea drones hit the corvette at Benghazi naval base and it "
               "capsized. A second ship was hit that evening.",
               art_ship)
    draw_panel(d, 522, 540, pw, ph, "WASHINGTON  •  US POLITICS", RED,
               "Democrats win 258 House seats, biggest since 1992",
               "Chuck Hubbard beat Rep. Virginia Foxx in North Carolina after "
               "a recount, sealing the 258-seat majority.",
               art_house)
    # also strip
    d.rectangle([40, 886, 984, 972], fill=INK)
    d.text((512, 890), "ALSO TODAY", font=font(BOLD, 19),
           fill=(255, 200, 60), anchor="ma")
    d.text((512, 912),
           "BepiColombo reaches Mercury after 8 years; ESA reports a thruster glitch",
           font=font(REG, 16), fill=LIGHT, anchor="ma")
    d.text((512, 932),
           "Fonusa candy factory search goes on in Cikande: 3 dead, dozens missing",
           font=font(REG, 16), fill=LIGHT, anchor="ma")
    d.text((512, 952),
           "Peru's Sunday toll from Friday's 6.7 Junin quake: 1 dead, 16 hurt, 853 homeless",
           font=font(REG, 16), fill=LIGHT, anchor="ma")
    d.text((512, 982),
           "Stories as reported on 22 November 2026  •  AP  •  Reuters  •  AFP  •  Al Jazeera",
           font=font(REG, 16), fill=GREY, anchor="ma")
    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
