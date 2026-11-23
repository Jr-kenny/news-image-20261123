#!/usr/bin/env python3
"""Compose the make.fun news-image-20261123 front page.

Reads the three photographic panels from ../assets/, lays them out as a
1024x1024 newspaper front page with PIL-rendered headlines and captions,
and writes entry.png next to this script. Run: python3 compose.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (12, 12, 12)
RED = (178, 34, 34)
GREY = (90, 86, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_photo(path, tw, th):
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    im = im.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def draw_lines(draw, lines, x, y, fnt, fill, spacing=4, align="left", width=None):
    for line in lines:
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 28  # side margin
    cw = W - 2 * mx  # content width

    # Masthead
    mast = font(SERIF_B, 66)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, 14), title, font=mast, fill=INK)
    d.line([(mx, 92), (W - mx, 92)], fill=INK, width=3)
    d.line([(mx, 97), (W - mx, 97)], fill=INK, width=1)

    # Date, large and clear
    date_f = font(SANS_B, 40)
    date = "MONDAY 23 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, 106), date, font=date_f, fill=RED)
    d.line([(mx, 156), (W - mx, 156)], fill=INK, width=2)

    # Lead photo: COP31 hall
    lead = fit_photo(os.path.join(ASSETS, "media-generation-cop31-hall-0-e23aa213-516a-4a99-889b-f6a6e664d705.webp"), cw, 248)
    page.paste(lead, (mx, 166))
    d.rectangle([mx, 166, mx + cw - 1, 166 + 248 - 1], outline=INK, width=2)

    # Lead headline + deck
    y = 424
    y = draw_lines(d, ["COP31 ENDS WITH NO DEAL"], mx, y, font(SERIF_B, 42), INK, spacing=2)
    y = draw_lines(d, wrap(d, "Climate talks in Antalya close as the longest UN climate "
                         "conference ever, with no agreement reached.", font(SERIF, 20), cw),
                   mx, y + 2, font(SERIF, 20), GREY, spacing=3)
    d.line([(mx, 520), (W - mx, 520)], fill=INK, width=1)

    # Middle row: two photos side by side
    half = (cw - 20) // 2
    left_x = mx
    right_x = mx + half + 20
    py = 530
    ph = 176
    beng = fit_photo(os.path.join(ASSETS, "media-generation-port-strike-dusk-0-ced23741-fd58-4589-80ec-f8615dac5ed0.webp"), half, ph)
    chip = fit_photo(os.path.join(ASSETS, "media-generation-chip-stocks-fall-0-5520f8e3-741a-4795-9e10-60e2253f5bd4.webp"), half, ph)
    page.paste(beng, (left_x, py))
    page.paste(chip, (right_x, py))
    d.rectangle([left_x, py, left_x + half - 1, py + ph - 1], outline=INK, width=2)
    d.rectangle([right_x, py, right_x + half - 1, py + ph - 1], outline=INK, width=2)

    # Middle headlines + decks
    hy = py + ph + 10
    draw_lines(d, wrap(d, "UKRAINE DRONES HIT TWO RUSSIAN SHIPS IN BENGHAZI",
                       font(SERIF_B, 23), half), left_x, hy, font(SERIF_B, 23), INK, spacing=2)
    draw_lines(d, wrap(d, "Kyiv says its sea drones struck two Russian ships in the Libyan port.",
                       font(SERIF, 17), half), left_x, hy + 56, font(SERIF, 17), GREY, spacing=2)
    draw_lines(d, wrap(d, "CHIP STOCKS SLIDE AS AI SPENDING DOUBTS SPREAD",
                       font(SERIF_B, 23), half), right_x, hy, font(SERIF_B, 23), INK, spacing=2)
    draw_lines(d, wrap(d, "Kospi down 3.3%, Samsung down 3.1%, SK Hynix down 2.5% after a Wall Street rout.",
                       font(SERIF, 17), half), right_x, hy + 56, font(SERIF, 17), GREY, spacing=2)
    d.line([(mx, 850), (W - mx, 850)], fill=INK, width=1)

    # Bottom row: two text-only stories
    by = 862
    draw_lines(d, wrap(d, "TRUMP LEANS TO NEW IRAN STRIKES AFTER NEW YEAR",
                       font(SERIF_B, 21), half), left_x, by, font(SERIF_B, 21), INK, spacing=2)
    draw_lines(d, wrap(d, "President says he is inclined to resume strikes if no deal; "
                         "Iran vows to counter the US naval blockade.",
                       font(SERIF, 16), half), left_x, by + 52, font(SERIF, 16), GREY, spacing=2)
    draw_lines(d, wrap(d, "DEMOCRATS CLINCH HISTORIC HOUSE MAJORITY",
                       font(SERIF_B, 21), half), right_x, by, font(SERIF_B, 21), INK, spacing=2)
    draw_lines(d, wrap(d, "At least 258 seats, their largest majority since 1992.",
                       font(SERIF, 16), half), right_x, by + 52, font(SERIF, 16), GREY, spacing=2)

    # Footer strip: two more stories of the day
    d.rectangle([0, 968, W - 1, H - 1], fill=INK)
    foot_f = font(SANS_B, 17)
    foot = "ALSO TODAY:  Magnitude 6.7 earthquake in Peru's Andes  |  Factory fire in Indonesia kills 24"
    d.text(((W - d.textlength(foot, font=foot_f)) / 2, 982), foot, font=foot_f, fill=(247, 243, 234))

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True, compress_level=9)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
