"""Render the 22 November 2026 world-news front page to entry.png.

One 1024x1024 image, 39 stories reported on Sunday 22 November 2026,
grouped by region and field. All text is drawn programmatically with
Pillow from the story lists below, so no lettering can be garbled.
The render is deterministic: fixed palette, fixed fonts, no clock,
no randomness, no network. Running it twice writes identical bytes.
Final layout: balanced two columns, 18px story lines, short labels
in the numbers strip so nothing overflows the page.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 243, 234)
INK = (22, 26, 34)
MUTED = (92, 96, 104)
RULE = (196, 188, 168)
NAVY = (16, 32, 56)
RED = (168, 32, 36)
TEAL = (14, 102, 96)
GOLD = (176, 124, 22)
LEAD_BG = (232, 226, 208)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


LEAD = [
    ("COP31 TALKS COLLAPSE",
     "UN climate summit in Antalya ends with no deal after EU and vulnerable states reject a final draft that never mentions fossil fuels."),
    ("RUSSIA HITS KYIV FLATS",
     "A five-storey block in Dymer is partly destroyed and 14 people are missing after an overnight drone strike north of Kyiv."),
    ("IRAN STRIKES BAHRAIN",
     "Bahrain says Iranian projectiles hit an industrial facility and injured two, as Gulf states condemn the attack."),
]

SECTIONS_LEFT = [
    ("EUROPE & UKRAINE", RED, [
        "Kryvyi Rih missile kills 2, incl. boy, 7; 60 hurt",
        "Russian ship Sparta II burns in Gulf of Finland",
        "UK and EU seal post-Brexit reset deals",
        "France protests enter a sixth Saturday",
        "Turkey seizes last big independent TV channel",
    ]),
    ("ASIA-PACIFIC", TEAL, [
        "Indonesia factory fire: 3 dead, dozens missing",
        "EU and Indonesia sign trade deal after 10 years",
        "South Korea minister quits over AI exam cheating",
        "Japan quake injures 22 in Aichi and Shizuoka",
        "Okinawa reopens restored Shuri Castle hall",
        "China flies 21 sorties in Taiwan patrols",
        "New Zealand election too close to call",
    ]),
    ("AMERICAS", NAVY, [
        "Mexico captures 'El Chapo Isidro'; 11 killed",
        "FBI probes hack of its criminal database",
        "Seattle airport immigration arrests draw outcry",
        "Bolsonaro in intensive care in Brazil",
        "Peru quake: 1 dead, 853 need assistance",
    ]),
]

SECTIONS_RIGHT = [
    ("MIDDLE EAST", GOLD, [
        "Gaza food-aid van strike kills three people",
        "Settlers torch West Bank vehicles; inquiry opens",
        "Eisenkot invites Likud to coalition talks",
        "Basra power-station fire kills four in Iraq",
    ]),
    ("AFRICA", RED, [
        "Nigeria funeral boat capsizes; 24 dead",
        "Drones hit Khartoum, damage UN building",
        "Congo Ebola cases climb to 11,645",
        "South Africa jobless rate rises to 33.7%",
    ]),
    ("ECONOMY & TECHNOLOGY", TEAL, [
        "AI sell-off: S&P 500 falls 3.7% into correction",
        "UN AI-weapons talks end, no binding rules",
        "Iran begins rationing electricity amid crisis",
    ]),
    ("SCIENCE, SPACE & HEALTH", GOLD, [
        "BepiColombo orbits Mercury after 8 years",
        "One-time CRISPR therapy cuts cholesterol 52%",
        "Princess Kate says she is in remission",
    ]),
    ("SPORT & CULTURE", RED, [
        "Verstappen wins chaotic Las Vegas Grand Prix",
        "Leeds stun Chelsea 4-1, first win there since 1999",
        "France rout Argentina 45-17 to reach final",
        "Kansas City win their first NWSL title",
        "200 mascots gather for festival in Saitama",
    ]),
]

NUMBERS = [
    ("186", "drones over Ukraine"),
    ("-3.7%", "S&P 500 AI sell-off"),
    ("11,645", "Ebola cases in Congo"),
    ("8 yrs", "journey to Mercury"),
    ("98.5%", "EU-Indonesia deal"),
]


def draw_section(draw, x, y, width, title, colour, items):
    draw.rectangle([x, y, x + width, y + 26], fill=colour)
    draw.text((x + 10, y + 4), title, font=font(SANS_B, 17), fill=(255, 255, 255))
    y += 32
    for item in items:
        draw.text((x + 4, y), "\u2022", font=font(SANS_B, 18), fill=colour)
        draw.text((x + 22, y), item, font=font(SANS, 18), fill=INK)
        y += 23
    return y + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.text((36, 14), "THE WORLD IN ONE DAY", font=font(SANS_B, 21), fill=(214, 186, 120))
    draw.text((36, 40), "Sunday 22 November 2026", font=font(SERIF_B, 46), fill=(255, 255, 255))
    draw.text((36, 94), "39 stories  \u00b7  every region  \u00b7  one page", font=font(SANS, 16), fill=(196, 208, 224))
    draw.text((812, 48), "22 NOV", font=font(SERIF_B, 34), fill=(255, 255, 255))
    draw.text((812, 86), "2026", font=font(SANS_B, 18), fill=(214, 186, 120))

    # Lead stories
    y = 130
    draw.rectangle([24, y, W - 24, y + 148], fill=LEAD_BG)
    lx = 40
    col_w = 312
    for i, (head, body) in enumerate(LEAD):
        x = lx + i * (col_w + 12)
        draw.text((x, y + 12), head, font=font(SANS_B, 19), fill=RED if i == 0 else INK)
        # wrap body by hand: split into lines of ~34 chars using simple wrap
        words = body.split()
        lines, cur = [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if draw.textlength(trial, font=font(SANS, 15)) > col_w - 6:
                lines.append(cur)
                cur = wd
            else:
                cur = trial
        if cur:
            lines.append(cur)
        by = y + 44
        for line in lines[:5]:
            draw.text((x, by), line, font=font(SANS, 15), fill=(52, 56, 64))
            by += 20
    y += 160

    # Two-column sections
    left_y = y
    for title, colour, items in SECTIONS_LEFT:
        left_y = draw_section(draw, 24, left_y, 484, title, colour, items)
    right_y = y
    for title, colour, items in SECTIONS_RIGHT:
        right_y = draw_section(draw, 524, right_y, 476, title, colour, items)

    # Day in numbers strip
    ny = max(left_y, right_y) + 2
    draw.rectangle([24, ny, W - 24, ny + 58], outline=RULE, width=2)
    draw.text((40, ny + 4), "THE DAY IN NUMBERS", font=font(SANS_B, 13), fill=NAVY)
    nx = 40
    for value, label in NUMBERS:
        draw.text((nx, ny + 20), value, font=font(SERIF_B, 20), fill=RED)
        draw.text((nx, ny + 43), label, font=font(SANS, 9), fill=MUTED)
        nx += 192

    draw.text((24, H - 18), "Sources: AP, Reuters, AFP, Al Jazeera, The Guardian, ESA and national reports of 22 Nov 2026.",
              font=font(SANS, 11), fill=MUTED)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
