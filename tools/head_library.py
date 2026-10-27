"""Cut image-model heads into a head library, and make a check sheet of the cuts on a headless v9 body

usage: python3 tools/head_library.py PERSON SRC_DIR LIB_DIR
SRC_DIR holds p{PERSON}-{expression}.png: the model's edits of the one-person v9 template (1024 px, wall blue
background, orange hoodie). Each head is cut by color: everything in the head box that is not wall blue and not
hoodie orange. Saved as LIB_DIR/p{PERSON}/{expression}.png (1080-px scale) + anchors.json (neck point in the PNG).
The neck point is fixed by the template: the head sits where the template's cartoon head sat.
"""
import glob, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BOX = [(150, 0), (800, 0), (800, 460), (700, 460), (700, 640), (150, 640)]   # head search area, 1080-px coords, minus the waving hand
SEED = (485, 360)                 # a point inside every face (template head centre)
CREAM_BELOW = 500                 # hoodie strings are cream like the eye whites: drop cream only below the chin
NECK = (465, 492)                 # where the head meets the hoodie in the template, 1080-px coords
DROP = [(140, 189, 220), (255, 86, 0), (237, 114, 57), (110, 159, 196)]   # wall, hoodie, hood, floor line
ERODE = 7                         # px; thin lines (hoodie strings touching a beard) narrower than this are cut off the face blob
EXPRS = ["neutral", "happy", "excited", "skeptical", "confused", "tired", "worried", "surprised"]


def cut(path):
    im = Image.open(path).convert("RGB").resize((1080, 1080), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    keep = np.ones(a.shape[:2])
    for c in DROP:
        keep *= np.clip((np.abs(a - c).sum(2) - 45) / 30, 0, 1)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(BOX, fill=255); box = np.asarray(m) / 255
    cream = np.clip((np.abs(a - (246, 238, 220)).sum(2) - 45) / 30, 0, 1)
    keep[CREAM_BELOW:] *= cream[CREAM_BELOW:]
    alpha = Image.fromarray((keep * box * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    # keep only the blob connected to the face centre: drops thin edge lines left from the hoodie and strings
    solid = alpha.point(lambda v: 255 if v > 128 else 0).filter(ImageFilter.MinFilter(ERODE))
    ImageDraw.floodfill(solid, SEED, 128)
    blob = solid.point(lambda v: 255 if v == 128 else 0).filter(ImageFilter.MaxFilter(ERODE))
    al = np.minimum(np.asarray(alpha), np.asarray(blob))
    ys, xs = np.nonzero(al > 128)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    rgba = Image.fromarray(np.dstack([a.astype(np.uint8), al]), "RGBA").crop((x0, y0, x1, y1))
    return rgba, (NECK[0] - x0, NECK[1] - y0)


def main(person, src, lib):
    out = os.path.join(lib, f"p{person}"); os.makedirs(out, exist_ok=True)
    anchors = {}
    for e in EXPRS:
        f = os.path.join(src, f"p{person}-{e}.png")
        if not os.path.exists(f):
            continue
        im, anchor = cut(f)
        im.save(os.path.join(out, f"{e}.png")); anchors[e] = anchor
    json.dump({k: [int(v[0]), int(v[1])] for k, v in anchors.items()}, open(os.path.join(out, "anchors.json"), "w"), indent=1)
    print("cut", len(anchors), "heads ->", out)
    return out, anchors


def check_sheet(out, anchors, body_png, sheet_path):
    """Every head on the headless body, 4 across, plus a dark background copy to show the cut edges."""
    body = Image.open(body_png).convert("RGBA")
    tiles = []
    for e, (ax, ay) in anchors.items():
        fr = body.copy()
        h = Image.open(os.path.join(out, f"{e}.png"))
        fr.alpha_composite(h, (NECK[0] - ax, NECK[1] - ay))
        t = fr.crop((200, 60, 760, 760)).resize((360, 450)).convert("RGB")
        ImageDraw.Draw(t).rectangle([0, 0, 90, 22], fill="white"); ImageDraw.Draw(t).text((6, 5), e, fill="black")
        tiles.append(t)
    sheet = Image.new("RGB", (4 * 365, 2 * 455), "white")
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 4) * 365, (i // 4) * 455))
    sheet.save(sheet_path); print("wrote", sheet_path)


if __name__ == "__main__":
    out, anchors = main(*sys.argv[1:4])
    if len(sys.argv) > 5:
        check_sheet(out, anchors, sys.argv[4], sys.argv[5])
