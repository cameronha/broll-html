"""One grid of the whole head library: a row for each person, a column for each expression.

usage: python3 tools/cast_sheet.py LIB_DIR OUT.jpg
"""
import os, sys
from PIL import Image, ImageDraw

EXPRS = ["neutral", "happy", "excited", "skeptical", "confused", "tired", "worried", "surprised"]
CELL = 200

lib, out = sys.argv[1:3]
people = sorted(d for d in os.listdir(lib) if d.startswith("p") and os.path.isdir(os.path.join(lib, d)))
sheet = Image.new("RGB", (60 + CELL * len(EXPRS), 30 + CELL * len(people)), (140, 189, 220))
d = ImageDraw.Draw(sheet)
for c, e in enumerate(EXPRS):
    d.text((60 + c * CELL + 8, 10), e, fill="black")
for r, p in enumerate(people):
    d.text((10, 30 + r * CELL + CELL // 2), p, fill="black")
    for c, e in enumerate(EXPRS):
        f = os.path.join(lib, p, f"{e}.png")
        if os.path.exists(f):
            h = Image.open(f); h.thumbnail((CELL - 10, CELL - 10))
            sheet.paste(h, (60 + c * CELL + (CELL - h.width) // 2, 30 + r * CELL + (CELL - h.height) // 2), h)
sheet.save(out)
print("wrote", out)
