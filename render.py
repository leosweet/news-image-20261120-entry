#!/usr/bin/env python3
"""Render the 20 November 2026 world-news infographic (1024x1024 PNG).

All stories were first reported on Friday 20 November 2026. The image is
drawn entirely with PIL: masthead, six story cards with small pictograms,
and a source footer. No network, no AI generation, fully deterministic.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("NEWS_IMAGE_OUT", "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_KICKER = font("DejaVuSans-Bold.ttf", 21)
F_SUB = font("DejaVuSans.ttf", 19)
F_TAG = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 15)

PAPER = (246, 241, 231)
NAVY = (20, 36, 62)
NAVY_SOFT = (38, 56, 86)
GOLD = (201, 162, 39)
CARD = (255, 255, 255)
CARD_EDGE = (216, 210, 196)
INK = (24, 24, 24)
BODY_INK = (58, 58, 58)
MUTED = (214, 222, 235)

# (tag, colour, headline, summary, pictogram)
STORIES = [
    (
        "WEATHER  ·  INDIA",
        (14, 122, 158),
        "Cyclone Akvan hits India's east coast",
        "Landfall near Gopalpur at noon; 300,000 people moved to "
        "safety and 47 trains cancelled.",
        "cyclone",
    ),
    (
        "CLIMATE  ·  COP31",
        (46, 139, 87),
        "COP31 closes with fossil fuels cut from text",
        "Near-final deal in Antalya drops any phase-out pledge, "
        "drawing anger from nations.",
        "globe",
    ),
    (
        "CULTURE  ·  GAMING",
        (123, 63, 160),
        "GTA VI takes $2.36bn on day one, estimate says",
        "Sensor Tower puts first-day sales at 24.6m copies; "
        "Take-Two has confirmed no figure.",
        "controller",
    ),
    (
        "MARKETS  ·  TECH",
        (176, 58, 48),
        "Wall Street slides 2% as Anthropic IPO debuts",
        "Dow falls 1,101 points; Anthropic closes up 17% in the "
        "largest IPO on record, $107bn raised.",
        "chart",
    ),
    (
        "GULF  ·  ENERGY",
        (178, 118, 20),
        "Iran widens attacks on Gulf tankers",
        "Tehran steps up strikes on shipping as oil prices slide; "
        "the IEA warns of a historic energy threat.",
        "drop",
    ),
    (
        "DIPLOMACY  ·  SHENZHEN",
        (40, 90, 160),
        "Shenzhen summit ends with no breakthrough",
        "Trump, Xi and Putin's peace declaration sidesteps the "
        "wars in Ukraine and Iran.",
        "flags",
    ),
]


def wrap(text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_cyclone(d, cx, cy, colour):
    r = 30
    for k in range(5):
        rr = r * (0.25 + 0.18 * k)
        d.arc(
            [cx - rr, cy - rr, cx + rr, cy + rr],
            start=40 + 55 * k,
            end=300 + 55 * k,
            fill=colour,
            width=4,
        )
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)


def draw_globe(d, cx, cy, colour):
    r = 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    d.ellipse(
        [cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=colour, width=3
    )
    d.line([cx - r, cy, cx + r, cy], fill=colour, width=3)
    d.arc(
        [cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
        start=200,
        end=340,
        fill=colour,
        width=3,
    )
    d.arc(
        [cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
        start=20,
        end=160,
        fill=colour,
        width=3,
    )


def draw_controller(d, cx, cy, colour):
    d.rounded_rectangle(
        [cx - 34, cy - 18, cx + 34, cy + 18], radius=14, outline=colour, width=4
    )
    d.line([cx - 22, cy, cx - 10, cy], fill=colour, width=4)
    d.line([cx - 16, cy - 6, cx - 16, cy + 6], fill=colour, width=4)
    for dx, dy in ((16, -7), (24, 1), (16, 9), (8, 1)):
        d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=colour)


def draw_chart(d, cx, cy, colour):
    bars = [14, 26, 20, 32, 22]
    x0 = cx - 32
    for i, bh in enumerate(bars):
        d.rectangle(
            [x0 + i * 13, cy + 18 - bh, x0 + i * 13 + 8, cy + 18], fill=colour
        )
    d.line([cx - 34, cy - 26, cx - 6, cy - 8, cx + 30, cy - 34], fill=(176, 58, 48), width=4)
    d.polygon(
        [(cx + 30, cy - 34), (cx + 18, cy - 34), (cx + 30, cy - 22)],
        fill=(176, 58, 48),
    )


def draw_drop(d, cx, cy, colour):
    d.pieslice([cx - 20, cy - 6, cx + 20, cy + 34], start=0, end=180, fill=colour)
    d.polygon([(cx - 20, cy + 12), (cx + 20, cy + 12), (cx, cy - 26)], fill=colour)
    d.arc([cx - 34, cy + 22, cx - 8, cy + 40], start=90, end=270, fill=colour, width=3)
    d.arc([cx + 8, cy + 22, cx + 34, cy + 40], start=270, end=90, fill=colour, width=3)


def draw_flags(d, cx, cy, colour):
    for i, c in enumerate(((176, 58, 48), (46, 139, 87), (40, 90, 160))):
        fx = cx - 26 + i * 26
        d.line([fx, cy - 26, fx, cy + 26], fill=colour, width=3)
        d.polygon([(fx, cy - 26), (fx + 20, cy - 19), (fx, cy - 12)], fill=c)


PICTOGRAMS = {
    "cyclone": draw_cyclone,
    "globe": draw_globe,
    "controller": draw_controller,
    "chart": draw_chart,
    "drop": draw_drop,
    "flags": draw_flags,
}


def draw_card(img, d, x, y, w, h, story):
    tag, colour, headline, summary, pic = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=CARD_EDGE, width=1)
    d.rounded_rectangle([x, y, x + 8, y + h], radius=4, fill=colour)
    # Tag chip.
    tw = F_TAG.getlength(tag)
    chip_w = int(tw) + 20
    d.rounded_rectangle(
        [x + 22, y + 16, x + 22 + chip_w, y + 16 + 26], radius=13, fill=colour
    )
    d.text((x + 32, y + 21), tag, font=F_TAG, fill=(255, 255, 255))
    # Pictogram: drawn large on a transparent tile, shrunk, pasted top right
    # in the tag row so it never touches the headline.
    tile = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    PICTOGRAMS[pic](td, 40, 40, colour)
    tile = tile.resize((46, 46), Image.LANCZOS)
    img.paste(tile, (x + w - 58, y + 8), tile)
    # Headline, up to 3 lines.
    lines = wrap(headline, F_HEAD, w - 44)
    ty = y + 54
    for line in lines[:3]:
        d.text((x + 22, ty), line, font=F_HEAD, fill=INK)
        ty += 33
    # Summary, up to 3 lines.
    lines = wrap(summary, F_BODY, w - 44)
    ty = y + 54 + 33 * min(len(wrap(headline, F_HEAD, w - 44)), 3) + 8
    for line in lines[:3]:
        d.text((x + 22, ty), line, font=F_BODY, fill=BODY_INK)
        ty += 26


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=GOLD)
    kicker = "T H E   W O R L D   I N   O N E   P I C T U R E"
    d.text(((W - F_KICKER.getlength(kicker)) / 2, 18), kicker, font=F_KICKER, fill=GOLD)
    title = "FRIDAY 20 NOVEMBER 2026"
    d.text(((W - F_TITLE.getlength(title)) / 2, 48), title, font=F_TITLE, fill=(255, 255, 255))
    sub = "Six stories that defined the day — first reported 20 November 2026"
    d.text(((W - F_SUB.getlength(sub)) / 2, 122), sub, font=F_SUB, fill=MUTED)

    # Story grid: 2 columns x 3 rows.
    margin, gap = 18, 14
    cw = (W - 2 * margin - gap) // 2
    ch = 252
    y0 = 186
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (cw + gap)
        y = y0 + row * (ch + 12)
        draw_card(img, d, x, y, cw, ch, story)

    # Footer.
    d.rectangle([0, H - 52, W, H], fill=NAVY)
    foot = ("Also today: World Children's Day  ·  Sources: The Hindu · News18 · "
            "Reuters · CNA · Indian Express · Japan Times · The Independent")
    d.text(((W - F_FOOT.getlength(foot)) / 2, H - 36), foot, font=F_FOOT, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
