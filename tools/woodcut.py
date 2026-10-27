"""Baroque woodcut look (after Jegher's cuts for Rubens) as a post-process on a flat scene -> still PNG

usage: python3 tools/woodcut.py SCENE OUT.png      (SCENE = name in scenes/, e.g. rubens-pitch)
The scene renders flat at 2x. Every pixel gets a distance to the nearest outline, so the hatch lines run
parallel to each shape's edge and wrap the form. Line width follows a darkness map: the fill's own tone plus
shade on edges that face away from a light at the upper left. The darkest areas get a second, crossed set.
"""
import os, re, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER, INK = np.array([239, 231, 218]), np.array([40, 34, 30])
SP = 10          # hatch spacing in 2x pixels
LIGHT = np.array([-0.6, -0.8])   # light comes from the upper left (x, y)


def render(name):
    svg = open(os.path.join(HERE, f"scenes/{name}.svg")).read()
    svg = re.sub(r'  <g id="wash".*\n', "", svg)
    bg = re.search(r'data-bg="(#\w+)"', svg).group(1)
    p = f"/tmp/woodcut-{name}.png"
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        pg.set_content(f'<body style="margin:0;background:{bg}">{svg}</body>')
        pg.screenshot(path=p)
        b.close()
    return np.asarray(Image.open(p).convert("RGB")).astype(float) / 255, np.array([int(bg[i:i + 2], 16) for i in (1, 3, 5)]) / 255


def shift(a, dy, dx, fill):
    out = np.full_like(a, fill)
    h, w = a.shape
    out[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = a[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return out


def distance(inside):
    """Approximate distance to the nearest non-inside pixel (alternating 4/8 erosion gives octagons)."""
    d, cur, i = np.zeros(inside.shape), inside.copy(), 0
    while cur.any() and i < 400:
        n = cur & shift(cur, 1, 0, False) & shift(cur, -1, 0, False) & shift(cur, 0, 1, False) & shift(cur, 0, -1, False)
        if i % 2:
            n &= shift(cur, 1, 1, False) & shift(cur, -1, -1, False) & shift(cur, 1, -1, False) & shift(cur, -1, 1, False)
        cur, i = n, i + 1
        d += cur
    return d


def blur(a, r):
    for _ in range(2):
        for ax in (0, 1):
            c = np.cumsum(np.pad(a, [(r + 1, r)] * 1 + [(0, 0)] if ax == 0 else [(0, 0), (r + 1, r)], mode="edge"), axis=ax)
            a = ((c[2 * r + 1:] - c[:-2 * r - 1]) if ax == 0 else (c[:, 2 * r + 1:] - c[:, :-2 * r - 1])) / (2 * r + 1)
    return a


def woodcut(img, bg):
    H, W, _ = img.shape
    lum = img @ [0.3, 0.59, 0.11]
    ink = lum < 0.33
    back = np.abs(img - bg).sum(2) < 0.06
    figure = ~ink & ~back
    d = blur(distance(figure), 2)
    gy, gx = np.gradient(d)
    g = np.hypot(gx, gy) + 1e-6
    facing = -(gx * LIGHT[0] + gy * LIGHT[1]) / g          # +1 where the edge faces the light
    edge = np.clip(1 - d / 34, 0, 1) ** 1.5
    dark = np.clip(0.9 * (1 - lum) ** 1.6 + edge * (0.34 - 0.32 * facing) + 0.03, 0, 1)
    dark[d > 120] *= 0.6
    v = (d / SP) % 1
    lines = np.abs(v - 0.5) < dark * 0.55
    yy, xx = np.mgrid[0:H, 0:W]
    cross = np.abs(((xx + yy) / (SP * 0.9)) % 1 - 0.5) < np.clip(dark - 0.55, 0, 1) * 1.1
    out = figure & (lines | cross)

    # background: horizontal sky hatching that fades down, ground hatching below the floor line
    wav = yy + 5 * np.sin(xx / 260)
    sky = np.clip(1 - yy / (0.24 * H), 0, 1) ** 1.2 * 0.5
    floor = np.where(back.sum(1) < W * 0.5)[0]
    ground_y = floor.max() if len(floor) else int(0.89 * H)
    ground = np.where(yy > ground_y, 0.3, 0)
    w = np.maximum(sky, ground) * 0.6
    out |= back & (w > 0.14) & (np.abs((wav / (SP * 1.4)) % 1 - 0.5) < w)

    # bold outlines (one pixel thicker)
    fat = ink | shift(ink, 1, 0, False) | shift(ink, 0, 1, False)
    out |= fat
    rgb = np.where(out[..., None], INK, PAPER).astype(np.uint8)
    return Image.fromarray(rgb).resize((W // 2, H // 2), Image.LANCZOS)


if __name__ == "__main__":
    img, bg = render(sys.argv[1])
    woodcut(img, bg).save(sys.argv[2])
    print("wrote", sys.argv[2])
