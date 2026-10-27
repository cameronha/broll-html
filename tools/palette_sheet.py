"""Same v9 scene, colors swapped by role -> labeled contact sheet. usage: python3 tools/palette_sheet.py SCENE.svg OUT.jpg"""
import os, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROLES = {   # v9 color -> role
    "#8CBDDC": "wall", "#6E9FC4": "wall2", "#5A8BB3": "wall3", "#182A46": "navy", "#F6EEDC": "cream",
    "#FF5600": "accent", "#ED7239": "accent2", "#DE4A30": "red", "#B83A24": "red2",
    "#286C4E": "green", "#22603F": "green2", "#2F7D5B": "green3", "#FAC496": "skin", "#EFA877": "skin2"}
PALETTES = {
    "A editorial": dict(wall="#D6CFC2", wall2="#C2B9AA", wall3="#AFA594", navy="#232B36", cream="#EEE7DA", accent="#B5562E", accent2="#A44D2A",
                        red="#7E3A30", red2="#662E26", green="#5E6B4A", green2="#525E40", green3="#6B7856", skin="#EDC9A6", skin2="#DDB28C"),
    "B navy & brass": dict(wall="#9DAAB6", wall2="#8796A4", wall3="#748493", navy="#1C2633", cream="#EDE8DE", accent="#C1913C", accent2="#AE8134",
                           red="#93473A", red2="#7A3A2F", green="#2F4F43", green2="#28443A", green3="#3A5D50", skin="#EDC9A6", skin2="#DDB28C"),
    "C sage & clay": dict(wall="#AEB8A4", wall2="#9AA590", wall3="#87927D", navy="#26302C", cream="#EFEADF", accent="#BC633F", accent2="#A95836",
                          red="#8B3E2E", red2="#723326", green="#2C5D59", green2="#25504C", green3="#376B66", skin="#EDC9A6", skin2="#DDB28C"),
    "D graphite + 1": dict(wall="#D2CEC7", wall2="#BDB8B0", wall3="#A9A49B", navy="#2A2C31", cream="#F1EEE8", accent="#D2532B", accent2="#BC4A27",
                           red="#55585F", red2="#45484E", green="#6E7277", green2="#606469", green3="#7B7F84", skin="#EDC9A6", skin2="#DDB28C"),
}

def variant(svg, pal):
    for hexv, role in ROLES.items():
        for case in (hexv, hexv.lower()):
            svg = svg.replace(case, pal[role])
    return svg

src = open(sys.argv[1]).read()
items = [("current v9", src)] + [(k, variant(src, p)) for k, p in PALETTES.items()]
ims = []
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome"); pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for name, svg in items:
        bg = svg.split('data-bg="', 1)[1].split('"', 1)[0] if 'data-bg="' in svg else "#fff"
        pg.set_content(f'<body style="margin:0;background:{bg}">{svg}</body>'); p = f"/tmp/pal-{len(ims)}.png"; pg.screenshot(path=p)
        im = Image.open(p).convert("RGB").resize((540, 540)); ImageDraw.Draw(im).rectangle([0, 0, 200, 26], fill="white")
        ImageDraw.Draw(im).text((8, 7), name, fill="black"); ims.append(im)
    b.close()
sheet = Image.new("RGB", (550 * 3, 550 * 2), "white")
for i, im in enumerate(ims): sheet.paste(im, ((i % 3) * 550, (i // 3) * 550))
sheet.save(sys.argv[2]); print("wrote", sys.argv[2])
