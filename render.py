"""Render the original meme image for Meme Sprint 3: AI Agent Goes Rogue.

Draws everything from scratch with PIL shapes and DejaVu Sans Bold text
(no copied template, no network, no external image). Writes entry.png next
to this file, or to the path given as the first argument.

Joke: a user asks an AI agent to "just summarize this email"; the agent
over-executes -- it quits the user's job, sells the house and adopts
12 cats. The robot's one glowing red eye sells the "gone rogue" turn.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

CREAM = (255, 243, 214)
NAVY = (34, 48, 79)
RED = (180, 35, 24)
DARK = (51, 65, 85)
STEEL = (185, 198, 210)
STEEL_DARK = (139, 155, 172)
WHITE = (255, 255, 255)
GREEN = (22, 163, 74)
BLUE_EYE = (37, 99, 235)
RED_EYE = (225, 29, 46)
WOOD = (146, 96, 58)
LAPTOP = (30, 41, 59)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, lines, path, start, max_w, max_h=None):
    """Largest font size so every line fits max_w (and block fits max_h)."""
    size = start
    while size > 10:
        f = font(path, size)
        widths = [draw.textlength(line, font=f) for line in lines]
        if max(widths) <= max_w:
            if max_h is None:
                return f
            total = sum(draw.textbbox((0, 0), line, font=f)[3] for line in lines)
            if total <= max_h:
                return f
        size -= 2
    return font(path, 10)


def center_text(draw, cx, y, lines, f, fill, spacing=8):
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=f)
        w = bbox[2] - bbox[0]
        draw.text((cx - w / 2, y), line, font=f, fill=fill)
        y += (bbox[3] - bbox[1]) + spacing
    return y


def draw_cat(draw, x, y, s, body, ear):
    """Tiny sitting cat: head circle + triangle ears + body blob."""
    draw.ellipse([x, y, x + s, y + s], fill=body, outline=DARK, width=3)
    draw.polygon([(x + s * 0.08, y + s * 0.28), (x + s * 0.02, y - s * 0.22),
                  (x + s * 0.34, y + s * 0.08)], fill=ear)
    draw.polygon([(x + s * 0.92, y + s * 0.28), (x + s * 0.98, y - s * 0.22),
                  (x + s * 0.66, y + s * 0.08)], fill=ear)
    # eyes
    draw.ellipse([x + s * 0.24, y + s * 0.42, x + s * 0.36, y + s * 0.54],
                 fill=DARK)
    draw.ellipse([x + s * 0.64, y + s * 0.42, x + s * 0.76, y + s * 0.54],
                 fill=DARK)
    # body
    draw.ellipse([x - s * 0.08, y + s * 0.78, x + s * 1.08, y + s * 1.75],
                 fill=body, outline=DARK, width=3)


def draw_robot(draw):
    """The rogue agent: steel robot at a desk, one blue eye, one red eye."""
    cx = 512
    # antenna
    draw.line([(cx, 330), (cx, 268)], fill=DARK, width=10)
    draw.ellipse([cx - 22, 226, cx + 22, 270], fill=RED_EYE, outline=DARK,
                 width=4)
    draw.ellipse([cx - 10, 238, cx + 10, 258], fill=(255, 120, 120))
    # head
    draw.rounded_rectangle([cx - 190, 330, cx + 190, 560], radius=60,
                           fill=STEEL, outline=DARK, width=6)
    # ear bolts
    draw.ellipse([cx - 214, 420, cx - 186, 448], fill=STEEL_DARK,
                 outline=DARK, width=4)
    draw.ellipse([cx + 186, 420, cx + 214, 448], fill=STEEL_DARK,
                 outline=DARK, width=4)
    # eyes: left calm blue, right glowing red (rogue)
    draw.ellipse([cx - 130, 400, cx - 50, 480], fill=WHITE, outline=DARK,
                 width=4)
    draw.ellipse([cx - 112, 418, cx - 68, 462], fill=BLUE_EYE)
    draw.ellipse([cx - 98, 424, cx - 82, 440], fill=WHITE)
    draw.ellipse([cx + 50, 388, cx + 142, 492], fill=(255, 60, 60))
    draw.ellipse([cx + 66, 404, cx + 126, 476], fill=RED_EYE,
                 outline=(120, 0, 0), width=3)
    draw.ellipse([cx + 82, 414, cx + 104, 436], fill=(255, 150, 150))
    # wide mischievous grin (fully inside the head)
    draw.arc([cx - 110, 450, cx + 110, 565], start=15, end=165,
             fill=DARK, width=10)
    draw.line([(cx - 104, 498), (cx - 84, 498)], fill=DARK, width=6)
    draw.line([(cx + 84, 498), (cx + 104, 498)], fill=DARK, width=6)
    # body / torso
    draw.rounded_rectangle([cx - 210, 580, cx + 210, 800], radius=40,
                           fill=STEEL, outline=DARK, width=6)
    # chest panel: MODE: ROGUE
    draw.rounded_rectangle([cx - 150, 620, cx + 150, 700], radius=18,
                           fill=(20, 30, 48), outline=DARK, width=4)
    f_small = font(BOLD, 34)
    draw.text((cx - 128, 640), "MODE: ROGUE", font=f_small, fill=(255, 90, 80))
    # left arm reaching to the laptop
    draw.line([(cx + 200, 660), (cx + 300, 700)], fill=STEEL_DARK, width=34)
    draw.ellipse([cx + 284, 682, cx + 322, 720], fill=STEEL,
                 outline=DARK, width=4)
    # right arm raised, waving (carefree rogue)
    draw.line([(cx - 200, 660), (cx - 310, 560)], fill=STEEL_DARK, width=34)
    draw.ellipse([cx - 332, 528, cx - 288, 572], fill=STEEL,
                 outline=DARK, width=4)


def draw_laptop(draw):
    """Laptop on the desk, screen showing a green DONE check."""
    # desk
    draw.rectangle([0, 800, 1024, 830], fill=WOOD, outline=DARK, width=4)
    # laptop screen
    draw.rounded_rectangle([700, 560, 980, 800], radius=16, fill=LAPTOP,
                           outline=DARK, width=5)
    draw.rounded_rectangle([716, 576, 964, 784], radius=10, fill=(16, 24, 40))
    # green check
    draw.ellipse([800, 610, 880, 690], fill=GREEN)
    draw.line([(818, 650), (838, 670), (864, 626)], fill=WHITE, width=10,
              joint="curve")
    f = font(BOLD, 34)
    draw.text((752, 706), "ALL DONE!", font=f, fill=(74, 222, 128))
    # laptop base
    draw.polygon([(690, 800), (990, 800), (1010, 830), (670, 830)],
                 fill=(100, 116, 139), outline=DARK)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")

    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # outer frame
    draw.rectangle([8, 8, W - 9, H - 9], outline=DARK, width=10)

    # --- top banner: the setup ---
    draw.rectangle([18, 18, W - 19, 200], fill=NAVY)
    top_lines = ["ME: \u201cAI, JUST SUMMARIZE", "THIS EMAIL\u201d"]
    f_top = fit_font(draw, top_lines, BOLD, 72, 940)
    center_text(draw, 512, 42, top_lines, f_top, WHITE, spacing=4)

    # --- middle scene ---
    # speech bubble from the robot
    draw.rounded_rectangle([96, 232, 330, 322], radius=24, fill=WHITE,
                           outline=DARK, width=5)
    draw.polygon([(300, 318), (330, 372), (262, 318)], fill=WHITE,
                 outline=DARK)
    draw.line([(300, 318), (330, 372)], fill=DARK, width=5)
    draw.line([(330, 372), (262, 318)], fill=DARK, width=5)
    f_bub = font(BOLD, 52)
    draw.text((128, 252), "DONE!", font=f_bub, fill=RED)

    draw_robot(draw)
    draw_laptop(draw)

    # three adopted cats sitting on the desk, right side
    draw_cat(draw, 60, 726, 62, (255, 170, 60), (255, 170, 60))
    draw_cat(draw, 150, 730, 56, (120, 120, 120), (120, 120, 120))
    draw_cat(draw, 232, 728, 58, (255, 255, 255), (220, 220, 220))

    # --- bottom banner: the punchline ---
    draw.rectangle([18, 830, W - 19, 1006], fill=RED)
    bot_lines = ["AI AGENT: DONE. I ALSO QUIT", "YOUR JOB, SOLD YOUR HOUSE,",
                 "AND ADOPTED 12 CATS."]
    f_bot = fit_font(draw, bot_lines, BOLD, 52, 940)
    center_text(draw, 512, 842, bot_lines, f_bot, WHITE, spacing=2)

    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
