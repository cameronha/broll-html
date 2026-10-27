"""Background sheet: the pitch scene on eight backgrounds -> ~/Claude-files/broll-html/31-backgrounds/bg-sheet.jpg

usage: python3 tools/bg_styles.py
The figures (v9 faces, nub hands, light skin, ochre clothes, pen) stay fixed; only what sits behind them changes.
Each background is inserted after <defs>, so it draws under the floor and the figures.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubens_scene as R
from rubens_scene import pen, fine, hatch, INK, FILL, ACCENT
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Claude-files/broll-html/31-backgrounds")
SAGE, SKY, CREAM = "#D3DCC8", "#D6E2E3", "#F2DDB6"


def rect(x, y, w, h, c, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'


def card():
    return rect(110, 130, 860, 834, SAGE, 'rx="6"') + rect(118, 136, 860, 834, SAGE, 'rx="6" opacity="0.5"')


def full():
    return rect(0, 0, 1080, 1080, SKY)


def blob():
    d = ("M180 380 Q150 220 330 170 Q470 120 600 190 Q760 110 900 200 Q1010 290 960 470 Q1020 640 940 800 "
         "Q900 930 720 950 L260 950 Q130 900 150 720 Q100 560 180 380 Z")
    return f'<path d="{d}" fill="{CREAM}"/><path d="{d}" fill="{FILL}" opacity="0.18" transform="translate(9 6)"/>'


def sun():
    return f'<circle cx="640" cy="430" r="330" fill="{FILL}" opacity="0.35"/>' + f'<circle cx="648" cy="436" r="330" fill="none" stroke="{ACCENT}" stroke-width="3" opacity="0.5"/>'


def grid():
    lines = " ".join(f"M{x} 0 L{x} 1080" for x in range(0, 1081, 36)) + " " + " ".join(f"M0 {y} L1080 {y}" for y in range(0, 1081, 36))
    return f'<path d="{lines}" stroke="#9FB8C4" stroke-width="1.2" opacity="0.55" fill="none"/>' + f'<path d="M86 0 L86 1080" stroke="{ACCENT}" stroke-width="2" opacity="0.5"/>'


def halftone():
    return ('<defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="3.4" fill="#D9A55A"/></pattern>'
            '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.85" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<mask id="fm"><rect width="1080" height="1080" fill="url(#fade)"/></mask></defs>'
            '<rect width="1080" height="1080" fill="url(#dots)" mask="url(#fm)" opacity="0.6"/>')


def room():
    win = (pen("M440 96 L650 96 L650 250 L440 250 Z", 2.6) + fine("M545 96 L545 250 M440 173 L650 173", 2)
           + hatch(452, 104, 8, 11, 60, 0.5, 1.2) + hatch(560, 184, 7, 11, 56, 0.5, 1.2))
    frame = pen("M80 150 L200 150 L200 280 L80 280 Z", 2.4) + fine("M92 250 L120 210 L146 236 L170 196 L188 250", 1.8)
    plant = (pen("M950 880 L1010 880 L1000 962 L960 962 Z", 2.6) + f'<path d="M950 880 L1010 880 L1000 962 L960 962 Z" fill="{ACCENT}" opacity="0.7" transform="translate(6 4)"/>'
             + pen("M980 880 Q960 800 930 760 M980 880 Q990 790 1020 740 M980 880 Q1000 830 1050 810 M980 880 Q950 840 910 830", 2.4))
    wall = pen("M0 760 L1080 760", 2.2) + hatch(20, 764, 54, 20, 10, 1.4, 1.2)
    return f'<g opacity="0.75">{wall}{win}{frame}</g>' + plant


STYLES = [("1  Plain (now)", lambda: ""), ("2  Color card", card), ("3  Full color", full), ("4  Wash shape", blob),
          ("5  Big circle", sun), ("6  Grid paper", grid), ("7  Halftone fade", halftone), ("8  Line-drawn room", room)]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    base = R.pitch()
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 540, "height": 540})
        for i, (_, fn) in enumerate(STYLES):
            svg = base.replace("</defs>\n", "</defs>\n" + fn(), 1).replace('width="1080" height="1080"', 'width="540" height="540"', 1)
            pg.set_content(f'<body style="margin:0;background:{R.BG}">{svg}</body>')
            pg.screenshot(path=f"{OUT}/bg-{i + 1}.png")
        b.close()
    W = 540
    sheet = Image.new("RGB", (4 * W + 30, 2 * W + 10), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    for i, (label, _) in enumerate(STYLES):
        x, y = (i % 4) * (W + 10), (i // 4) * (W + 10)
        sheet.paste(Image.open(f"{OUT}/bg-{i + 1}.png").convert("RGB"), (x, y))
        d.text((x + 12, y + 8), label, fill="black", font=f)
    sheet.save(f"{OUT}/bg-sheet.jpg", quality=88)
    print(f"{OUT}/bg-sheet.jpg")
