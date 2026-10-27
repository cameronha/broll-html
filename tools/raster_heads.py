"""v9 bodies (SVG) + image-model heads (raster) -> scenes/v9-rubens-{tag}.svg

usage: python3 tools/raster_heads.py GEN.png TAG
GEN.png is the image model's edit of the v9 still (1024 px, faces replaced). Each head is cut with a polygon,
the wall blue and the body colors inside it are made transparent, and the cut goes into the head's rig group
as an <image>, so the rig turns it at the old pivot and svgpieces gives it the cut-paper edge and boil.
"""
import base64, io, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_PX = 1024
ZOOM = (1, 0, 0)              # the still sent to the model was rendered without data-zoom
HEADS = {   # group id -> polygon in GEN pixels
    "customer-head": [(80, 250), (110, 170), (200, 158), (280, 162), (332, 200), (350, 260), (348, 450), (332, 540),
                      (270, 562), (210, 552), (150, 470), (85, 400)],
    "founder-head": [(478, 280), (490, 170), (560, 92), (680, 82), (790, 118), (842, 220), (836, 330), (812, 420),
                     (760, 452), (700, 484), (640, 484), (600, 432), (562, 332), (548, 296)],
}
DROP = [(140, 189, 220), (47, 125, 91), (255, 86, 0), (237, 114, 57)]   # wall, sweater, hoodie x2 (not cream: the eye whites are cream)


def cut(gen, poly):
    a = np.asarray(gen).astype(float)
    keep = np.ones(a.shape[:2])
    for c in DROP:
        keep *= np.clip((np.abs(a - c).sum(2) - 40) / 30, 0, 1)
    m = Image.new("L", gen.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    alpha = (keep * np.asarray(m) / 255 * 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.MedianFilter(5)))
    rgba = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    box = (min(xs), min(ys), max(xs), max(ys))
    buf = io.BytesIO(); rgba.crop(box).save(buf, "PNG")
    return box, base64.b64encode(buf.getvalue()).decode()


def to_svg(x, y):
    k = 1080 / GEN_PX
    return (x * k - ZOOM[1]) / ZOOM[0], (y * k - ZOOM[2]) / ZOOM[0]


def main(gen_path, tag):
    gen = Image.open(gen_path).convert("RGB").resize((GEN_PX, GEN_PX))
    svg = open(os.path.join(HERE, "scenes/founder-v9.svg")).read()
    for gid, poly in HEADS.items():
        (x0, y0, x1, y1), b64 = cut(gen, poly)
        sx0, sy0 = to_svg(x0, y0); sx1, sy1 = to_svg(x1, y1)
        img = f'<image href="data:image/png;base64,{b64}" x="{sx0:.1f}" y="{sy0:.1f}" width="{sx1 - sx0:.1f}" height="{sy1 - sy0:.1f}"/>'
        svg = re.sub(rf'(<g id="{gid}"[^>]*>).*?(\n  </g>)', lambda m: m.group(1) + img + m.group(2), svg, count=1, flags=re.S)
    out = os.path.join(HERE, f"scenes/v9-rubens-{tag}.svg")
    open(out, "w").write(svg)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
