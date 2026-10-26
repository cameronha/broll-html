"""Turn found photos + Vision masks into colour paper pieces. No model, no cost.

usage: python3 stylize.py PROJECTDIR SCENE [LOOK]
  PROJECTDIR/scenes.json holds one plan per scene; PROJECTDIR/work/SCENE.jpg (+ SCENE-mask.png)
  LOOK is a key of LOOKS (Actionworks brand colours)
Writes PROJECTDIR/work/LOOK/SCENE/bg.png, piece-NN.png, manifest.json

Scene plan keys:
  mode   "cut"   subject (or whole photo, mask:false) on flat paper, cut into cols x rows
         "plate" one subject piece over the photo's own inpainted background
  motion fall | peel | assemble | stack (cut);  parallax | cross (plate)
  cols, rows, fit, cover, mask, seed, stagger, dir   (all optional)
"""
import json, math, os, random, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

F = 1080                     # square frame
NAVY, CREAM, SKY = (24, 42, 70), (246, 238, 220), (140, 189, 220)
ORANGE, RED, BRIGHT = (237, 114, 57), (222, 74, 48), (255, 86, 0)

# stops: gradient map shadow -> highlight. plate: stops for background plates (contrast with subject).
# dots: halftone ink on paper instead of a gradient.
LOOKS = {
    "navy-sky":    {"stops": [NAVY, SKY, CREAM], "bg": CREAM},
    "navy-orange": {"stops": [NAVY, ORANGE, (255, 222, 196)], "bg": CREAM},
    "red-on-sky":  {"stops": [(150, 40, 24), ORANGE, CREAM], "bg": SKY,
                    "plate": [(52, 88, 128), SKY, CREAM]},
    "dots-pop":    {"dots": (RED, CREAM), "bg": SKY},
    # Gilliam: engraving line art kept as ink, paper inside the figure hand-tinted flat
    "gilliam":     {"ink": NAVY, "tint": CREAM, "bg": ORANGE},
    # WSJ hedcut: stipple dots + fine contour lines in ink on paper
    "hedcut":      {"stipple": NAVY, "paper": CREAM, "bg": SKY},
    # flat poster bands + ink outlines: South Park-ish, hides bad source photos
    "cartoon":     {"bands": [NAVY, RED, ORANGE, (250, 196, 150), CREAM], "lines": NAVY, "bg": SKY,
                    "plate_bands": [(52, 88, 128), (96, 145, 185), SKY, CREAM]},
}
LOOK = LOOKS["red-on-sky"]
CELL, ANGLE = 6.0, math.radians(45)
BORDER = 5


def cartoon(rgb, bands, lines, lift=0.0):
    """Flatten to a few colour bands, then draw outlines from the smoothed image."""
    w, h = rgb.size
    small = rgb.resize((w // 3, h // 3), Image.LANCZOS)
    for _ in range(3):
        small = small.filter(ImageFilter.MedianFilter(5))
    smooth = small.resize((w, h), Image.BICUBIC).convert("L")
    g = np.asarray(smooth, np.float32) / 255
    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    g = lift + (1 - lift) * np.clip((g - lo) / max(hi - lo, 1e-3), 0, 1)
    idx = np.clip((g * len(bands)).astype(int), 0, len(bands) - 1)
    out = np.array(bands, np.float32)[idx]
    if lines:
        # edges between bands + strong luminance edges, thickened like a marker
        q = Image.fromarray((idx * (255 // len(bands))).astype(np.uint8))
        e = np.maximum(np.asarray(q.filter(ImageFilter.FIND_EDGES), np.float32),
                       np.asarray(smooth.filter(ImageFilter.FIND_EDGES), np.float32) * 2)
        ink = Image.fromarray(((e > 40) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
        ink = np.asarray(ink.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[..., None] / 255
        out = out * (1 - ink) + np.array(lines, np.float32) * ink
    return out


def ink_tint(rgb, ink, tint):
    """Line art: dark strokes -> ink colour, everything else -> flat tint."""
    g = np.asarray(rgb.convert("L"), np.float32)
    k = np.clip((175 - g) / 70, 0, 1)[..., None]
    return np.array(tint, np.float32) * (1 - k) + np.array(ink, np.float32) * k


def paper_mask(img):
    """Mask for a drawing on white paper: flood the paper from the edges, keep the rest."""
    from PIL import ImageOps
    g = img.convert("L")
    sealed = g.filter(ImageFilter.MinFilter(9))           # thicken lines to close gaps
    light = sealed.point(lambda v: 255 if v > 225 else 0)
    light = ImageOps.expand(light, 2, fill=255)
    ImageDraw.floodfill(light, (0, 0), 128)
    bg = np.asarray(light, np.uint8)[2:-2, 2:-2] == 128
    m = Image.fromarray(np.uint8(~bg) * 255).filter(ImageFilter.MinFilter(5))  # undo the thickening
    return m.filter(ImageFilter.GaussianBlur(1))


def hedcut(rgb, ink, paper, cell=4, seed=0):
    """Stipple: error-diffuse darkness on a coarse grid, jitter each dot, add contour lines."""
    w, h = rgb.size
    g = rgb.convert("L").filter(ImageFilter.GaussianBlur(1.5))
    a = np.asarray(g, np.float32) / 255
    lo, hi = np.percentile(a, 2), np.percentile(a, 98)
    a = np.clip((a - lo) / max(hi - lo, 1e-3), 0, 1)
    # local contrast: pull detail out of shadows (backlit photos go solid otherwise)
    big = np.asarray(Image.fromarray(np.uint8(a * 255)).filter(ImageFilter.GaussianBlur(25)), np.float32) / 255
    a = np.clip(0.35 + (a - big) * 2.2 + (big - 0.5) * 0.4, 0, 1)
    gw, gh = w // cell, h // cell
    d = 1 - np.asarray(Image.fromarray(np.uint8(a * 255)).resize((gw, gh), Image.BOX), np.float32) / 255
    d = np.clip(d * 1.1 - 0.1, 0, 1) ** 1.7            # keep highlights clean, like a hedcut
    rng = np.random.default_rng(seed)
    dots = []
    for y in range(gh):                                  # Floyd-Steinberg on the dot grid
        row = d[y]
        for x in range(gw):
            old = row[x]; new = 1.0 if old > 0.5 else 0.0; err = old - new
            if new: dots.append((x, y))
            if x + 1 < gw: row[x + 1] += err * 7 / 16
            if y + 1 < gh:
                if x > 0: d[y + 1, x - 1] += err * 3 / 16
                d[y + 1, x] += err * 5 / 16
                if x + 1 < gw: d[y + 1, x + 1] += err * 1 / 16
    S = 3                                                # draw at 3x, downsample = smooth dots
    canvas = Image.new("L", (w * S, h * S), 0)
    dr = ImageDraw.Draw(canvas)
    r = cell * S * 0.32
    for x, y in dots:
        cx = (x + 0.5 + rng.uniform(-0.3, 0.3)) * cell * S
        cy = (y + 0.5 + rng.uniform(-0.3, 0.3)) * cell * S
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    k = np.asarray(canvas.resize((w, h), Image.LANCZOS), np.float32) / 255
    # contour lines from the smoothed image
    e = np.asarray(g.filter(ImageFilter.GaussianBlur(1)).filter(ImageFilter.FIND_EDGES), np.float32)
    line = np.clip((e - 14) / 20, 0, 1) * 0.85
    k = np.maximum(k, line)[..., None]
    return np.array(paper, np.float32) * (1 - k) + np.array(ink, np.float32) * k


def tone(rgb, contrast=1.0, lift=0.0, stops=None, plate=False):
    """rgb PIL image -> float RGB array in the current LOOK."""
    if "stipple" in LOOK:
        return hedcut(rgb, LOOK["stipple"], LOOK["paper"])
    if "ink" in LOOK:
        return ink_tint(rgb, LOOK["ink"], LOOK["tint"])
    if "bands" in LOOK:
        if plate:
            return cartoon(rgb, LOOK["plate_bands"], None, lift)
        return cartoon(rgb, LOOK["bands"], LOOK["lines"])
    g = np.asarray(rgb.convert("L").filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    lo, hi = np.percentile(g, 2), np.percentile(g, 98)
    g = np.clip((g - lo) / max(hi - lo, 1e-3), 0, 1)
    g = np.clip((g - 0.5) * contrast + 0.5, 0, 1) ** 0.8      # brighter mids
    g = lift + (1 - lift) * g
    stops = stops or LOOK.get("stops")
    if stops:
        st = np.array(stops, np.float32)
        x = g * (len(st) - 1)
        i = np.clip(np.floor(x).astype(int), 0, len(st) - 2)
        f = (x - i)[..., None]
        return st[i] * (1 - f) + st[i + 1] * f
    ink_c, paper_c = (np.array(c, np.float32) for c in LOOK["dots"])
    g = 0.3 + 0.7 * g                                          # lighter dots
    h, w = g.shape
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (x * math.cos(ANGLE) + y * math.sin(ANGLE)) / CELL
    v = (-x * math.sin(ANGLE) + y * math.cos(ANGLE)) / CELL
    d = np.hypot(u - np.round(u), v - np.round(v))
    r = 0.74 * np.sqrt(1 - g)
    ink = np.clip((r - d) * CELL + 0.5, 0, 1)[..., None]
    return paper_c * (1 - ink) + ink_c * ink


def to_rgba(rgb_arr, alpha):
    a = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb_arr.astype(np.uint8), a]), "RGBA")


def bordered(rgb_arr, alpha):
    """Piece with a white scissor-cut paper border around its alpha."""
    a = Image.fromarray((alpha * 255).astype(np.uint8))
    outer = np.asarray(a.filter(ImageFilter.MaxFilter(BORDER * 2 + 1)), np.float32) / 255
    white = np.full_like(rgb_arr, 255)
    m = alpha[..., None]
    return to_rgba(rgb_arr * m + white * (1 - m), outer)


def fill_hole(img, hole):
    """Diffusion inpaint: blur, re-pin known pixels, repeat."""
    arr = np.asarray(img, np.float32)
    known = (1 - hole)[..., None]
    mean = (arr * known).sum((0, 1)) / known.sum()
    out = arr * known + mean * (1 - known)
    for rad in [24] * 20 + [8] * 20:
        b = np.asarray(Image.fromarray(np.uint8(np.clip(out, 0, 255))).filter(
            ImageFilter.GaussianBlur(rad)), np.float32)
        out = arr * known + b * (1 - known)
    return Image.fromarray(np.uint8(np.clip(out, 0, 255)))


def grid_cells(box, cols, rows, rng, tilt=0.12):
    """Polygons for a jagged grid of straight, slightly tilted scissor cuts."""
    x0, y0, x1, y1 = box
    pad = 400
    jx, jy = min(30, (x1 - x0) / cols / 5), min(30, (y1 - y0) / rows / 5)
    vx = [(x0 - pad, 0.0)] + [(x0 + (x1 - x0) * i / cols + rng.uniform(-jx, jx),
                                rng.uniform(-tilt, tilt)) for i in range(1, cols)] + [(x1 + pad, 0.0)]
    hy = [(y0 - pad, 0.0)] + [(y0 + (y1 - y0) * j / rows + rng.uniform(-jy, jy),
                                rng.uniform(-tilt, tilt)) for j in range(1, rows)] + [(y1 + pad, 0.0)]

    def corner(v, h):         # x = a + b*y, y = c + d*x
        (a, b), (c, d) = v, h
        x = (a + b * c) / (1 - b * d)
        return (x, c + d * x)

    return [[corner(vx[i], hy[j]), corner(vx[i + 1], hy[j]),
             corner(vx[i + 1], hy[j + 1]), corner(vx[i], hy[j + 1])]
            for j in range(rows) for i in range(cols)]


def poly_mask(poly):
    m = Image.new("L", (F, F), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m, np.float32) / 255


def save_piece(rgba, out, k, manifest, ox=0, oy=0):
    box = rgba.getchannel("A").getbbox()
    rgba.crop(box).save(os.path.join(out, f"piece-{k:02d}.png"))
    manifest["pieces"].append({"src": f"piece-{k:02d}.png", "x": box[0] - ox, "y": box[1] - oy,
                               "w": box[2] - box[0], "h": box[3] - box[1]})


def place(img, mask, fit, cover):
    """Scale + centre the mask bbox in the frame (or cover the frame). Return framed img, mask."""
    bb = mask.getbbox()
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    s = F / min(img.size) if cover else fit * F / max(bw, bh)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    mask = mask.resize(img.size, Image.LANCZOS)
    cx, cy = (bb[0] + bb[2]) / 2 * s, (bb[1] + bb[3]) / 2 * s
    ox, oy = round(F / 2 - cx), round(F / 2 - cy)
    fi = Image.new("RGB", (F, F), LOOK["bg"]); fi.paste(img, (ox, oy))
    fm = Image.new("L", (F, F), 0); fm.paste(mask, (ox, oy))
    return fi, fm


def load(work, name, use_mask):
    img = Image.open(os.path.join(work, f"{name}.jpg")).convert("RGB")
    if use_mask == "paper":
        return img, paper_mask(img)
    if use_mask:
        return img, Image.open(os.path.join(work, f"{name}-mask.png")).convert("L")
    return img, Image.new("L", img.size, 255)


def cut(work, name, out, plan, manifest):
    rng = random.Random(plan.get("seed", 1))
    img, mask = load(work, name, plan.get("mask", True))
    img, mask = place(img, mask, plan.get("fit", 0.86), plan.get("cover", False))
    t = tone(img, contrast=1.1)
    alpha = np.asarray(mask, np.float32) / 255
    Image.new("RGB", (F, F), LOOK["bg"]).save(os.path.join(out, "bg.png"))
    cells = grid_cells(mask.getbbox(), plan.get("cols", 4), plan.get("rows", 1), rng)
    for k, poly in enumerate(cells, 1):
        a = alpha * poly_mask(poly)
        if a.sum() > 500:
            save_piece(bordered(t, a), out, k, manifest)


def plate(work, name, out, plan, manifest):
    img, mask = load(work, name, True)
    s = F / min(img.size)                          # cover the square; extra is pan room
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    mask = mask.resize(img.size, Image.LANCZOS)
    hole = np.asarray(mask.filter(ImageFilter.MaxFilter(25)), np.float32) / 255
    plate_img = fill_hole(img, (hole > 0.1).astype(np.float32))
    to_rgba(tone(plate_img, contrast=0.8, lift=0.25, stops=LOOK.get("plate"), plate=True),
            np.ones(hole.shape)).save(os.path.join(out, "bg.png"))
    # frame window: centred on the subject, clamped to the photo
    bb = mask.getbbox()
    ox = int(np.clip((bb[0] + bb[2]) / 2 - F / 2, 0, img.width - F))
    oy = int(np.clip((bb[1] + bb[3]) / 2 - F / 2, 0, img.height - F))
    manifest.update(bg_w=img.width, bg_h=img.height, ox=ox, oy=oy)
    alpha = np.asarray(mask, np.float32) / 255
    save_piece(bordered(tone(img, contrast=1.15), alpha), out, 1, manifest, ox, oy)


if __name__ == "__main__":
    proj, scene = sys.argv[1], sys.argv[2]
    look = sys.argv[3] if len(sys.argv) > 3 else "red-on-sky"
    plan = json.load(open(os.path.join(proj, "scenes.json")))[scene]
    LOOK = dict(LOOKS[look], **{k: tuple(plan[k]) for k in ("bg", "tint") if k in plan})
    work = os.path.join(proj, "work")
    out = os.path.join(work, look, scene); os.makedirs(out, exist_ok=True)
    manifest = {"bg": "bg.png", "motion": plan["motion"], "stagger": plan.get("stagger", 0.2),
                "dir": plan.get("dir", 1), "dur": plan.get("dur", 4.5),
                "hinge": plan.get("hinge", [0.5, 18]), "pieces": []}
    (plate if plan["mode"] == "plate" else cut)(work, scene, out, plan, manifest)
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(out)
