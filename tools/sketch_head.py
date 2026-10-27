"""Rubens-faces sketch look (loose dark pen over a flat ochre shape), one realistic head -> SVG + PNG

usage: python3 tools/sketch_head.py OUT.png
Lines are point lists. sk() smooths them and draws 2 passes with small random offsets, so contours look
searched for, not traced. hatch() fills a polygon with parallel strokes of random length for the shadows.
"""
import math, os, sys
import numpy as np
from playwright.sync_api import sync_playwright

RNG = np.random.default_rng(7)
INK, OCHRE, PAPER = "#2B2420", "#E3A847", "#FBF8F2"
OUT = []


def smooth(p, n=8):
    p = [p[0]] + list(p) + [p[-1]]
    o = []
    for i in range(1, len(p) - 2):
        for k in range(n):
            t = k / n
            o.append(tuple(0.5 * (2 * p[i][j] + (-p[i - 1][j] + p[i + 1][j]) * t + (2 * p[i - 1][j] - 5 * p[i][j] + 4 * p[i + 1][j] - p[i + 2][j]) * t * t
                                  + (-p[i - 1][j] + 3 * p[i][j] - 3 * p[i + 1][j] + p[i + 2][j]) * t ** 3) for j in range(2)))
    return o + [p[-2]]


def sk(pts, w=2.6, passes=2, jit=2.2):
    for k in range(passes):
        q = [(x + RNG.normal(0, jit), y + RNG.normal(0, jit)) for x, y in pts]
        s = smooth(q)
        OUT.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in s)}" fill="none" stroke="{INK}" '
                   f'stroke-width="{w * (1 if k == 0 else 0.6):.1f}" stroke-linecap="round" stroke-linejoin="round" opacity="{0.95 if k == 0 else 0.7}"/>')


def hatch(poly, deg, gap=9, w=1.6):
    a = math.radians(deg); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    proj = [x * nx + y * ny for x, y in poly]
    for c in np.arange(min(proj) + gap / 2, max(proj), gap):
        hits = []
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            p1, p2 = x1 * nx + y1 * ny - c, x2 * nx + y2 * ny - c
            if p1 * p2 < 0:
                t = p1 / (p1 - p2); hits.append((x1 + (x2 - x1) * t) * ux + (y1 + (y2 - y1) * t) * uy)
        hits.sort()
        for s0, s1 in zip(hits[::2], hits[1::2]):
            s0 += RNG.uniform(0, 0.25) * (s1 - s0); s1 -= RNG.uniform(0, 0.25) * (s1 - s0)
            if s1 - s0 > 6:
                x0, y0, x1, y1 = s0 * ux + c * nx, s0 * uy + c * ny, s1 * ux + c * nx, s1 * uy + c * ny
                OUT.append(f'<path d="M{x0:.0f} {y0:.0f} L{x1 + RNG.normal(0, 1.5):.0f} {y1 + RNG.normal(0, 1.5):.0f}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" opacity="0.8"/>')


def curl(x, y, r, w=2.2):
    t = np.linspace(0, 1.7 * math.pi, 10)
    s = RNG.uniform(0.8, 1.2)
    sk([(x + r * s * math.cos(a + 2) * (1 - a / 14), y + r * math.sin(a + 2) * (1 - a / 14)) for a in t], w, 1, 1)


def head():
    # flat ochre shape behind, a little off the drawing
    OUT.append(f'<path d="M300 1080 Q250 860 330 780 Q380 700 420 640 Q360 520 380 380 Q410 210 540 190 Q690 190 720 300 '
               f'Q760 420 740 500 Q760 620 640 730 Q800 760 880 860 Q930 960 920 1080 Z" fill="{OCHRE}" transform="translate(-14 10)"/>')
    # skull, forehead, brow, nose, beard silhouette
    sk([(420, 520), (392, 430), (396, 330), (440, 250), (520, 206), (600, 210), (650, 248), (674, 300), (684, 352), (694, 380)], 3.2)
    sk([(694, 380), (686, 400), (690, 418), (704, 444), (722, 470), (712, 486), (692, 490)], 3)
    sk([(690, 490), (672, 484), (660, 474)], 2.4)
    sk([(694, 488), (680, 492)], 2.4, 1)
    sk([(706, 500), (726, 520), (730, 560), (722, 610), (700, 660), (660, 700), (612, 724), (566, 716), (520, 690), (484, 640), (462, 590)], 2.8)
    # ear
    sk([(440, 420), (418, 404), (404, 420), (406, 460), (420, 494), (440, 504), (452, 490)], 2.8)
    sk([(426, 430), (420, 450), (430, 476)], 2, 1)
    # brows (knitted), eyes, lids, bags
    sk([(500, 380), (530, 372), (566, 378), (600, 396)], 5, 2, 1.5)
    sk([(636, 398), (660, 382), (690, 376)], 4.4, 2, 1.5)
    sk([(626, 394), (632, 376), (628, 360)], 2, 1)
    sk([(616, 392), (620, 372)], 1.8, 1)
    sk([(526, 420), (548, 408), (574, 410), (596, 422)], 2.8)
    sk([(530, 424), (556, 430), (588, 426)], 1.8)
    sk([(536, 438), (562, 446), (590, 438)], 1.6, 1)
    OUT.append(f'<ellipse cx="572" cy="418" rx="8" ry="7" fill="{INK}"/>')
    sk([(652, 420), (668, 410), (684, 414)], 2.4)
    sk([(656, 428), (674, 428)], 1.6, 1)
    OUT.append(f'<ellipse cx="676" cy="419" rx="5" ry="6" fill="{INK}"/>')
    # nose wing, cheek
    sk([(644, 440), (652, 470), (664, 480)], 2, 1)
    sk([(640, 484), (652, 486), (664, 482)], 2.2)
    sk([(580, 470), (604, 486)], 1.6, 1)
    # forehead wrinkles
    for y, x0, x1 in [(300, 520, 640), (322, 510, 650), (344, 540, 640)]:
        sk([(x0, y + 4), ((x0 + x1) / 2, y - 6), (x1, y + 2)], 1.8, 1)
    # mustache, lip, beard strands
    sk([(560, 512), (600, 498), (640, 494), (680, 496), (708, 504), (730, 530)], 2.6)
    sk([(600, 512), (640, 514), (690, 516)], 2, 1)
    sk([(640, 540), (668, 548), (692, 540)], 2.6)
    sk([(652, 552), (672, 556)], 1.8, 1)
    for i in range(18):
        x = 480 + i * 13 + RNG.normal(0, 4)
        y0 = 500 + abs(x - 620) * 0.25 + (40 if 600 < x < 710 else 0)
        sk([(x, y0), (x + RNG.normal(0, 8), y0 + 60), (x * 0.9 + 58 + RNG.normal(0, 10), y0 + 120 + RNG.uniform(0, 70))], 1.8, 1, 3)
    for x, y in [(560, 690), (600, 712), (640, 700), (520, 660), (680, 660)]:
        curl(x, y, 9)
    # hair fringe: curls around the back and over the ear
    for x, y in [(400, 360), (392, 392), (404, 330), (420, 300), (446, 284), (470, 400), (456, 360)]:
        curl(x, y, 12, 2.4)
    # shadows: back of skull, eye socket, under the cheekbone, temple
    hatch([(398, 330), (440, 252), (470, 236), (440, 330), (430, 420), (408, 440)], 60, 8)
    hatch([(520, 384), (600, 398), (606, 420), (540, 410)], 30, 6, 1.4)
    hatch([(470, 470), (560, 470), (590, 500), (520, 520), (472, 520)], 50, 8)
    hatch([(600, 230), (650, 250), (672, 300), (640, 290)], -30, 8, 1.3)
    # neck and robe
    sk([(470, 640), (476, 700), (460, 770)], 2.6)
    sk([(650, 700), (680, 760)], 2.6)
    sk([(330, 1080), (330, 940), (380, 840), (460, 770), (560, 800), (680, 760), (800, 820), (880, 920), (900, 1080)], 3)
    sk([(460, 770), (520, 880), (580, 1080)], 2.4)
    sk([(680, 760), (650, 880), (640, 1080)], 2.4)
    for k in range(5):
        sk([(400 + k * 22, 860 + k * 8), (440 + k * 24, 960), (450 + k * 24, 1080)], 1.6, 1, 3)
    hatch([(470, 780), (560, 800), (600, 900), (520, 900)], 70, 9)
    hatch([(690, 770), (800, 820), (860, 900), (700, 900)], -60, 10)


def page():
    head()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">'
            f'<rect width="1080" height="1080" fill="{PAPER}"/>' + "".join(OUT) + "</svg>")


if __name__ == "__main__":
    out = sys.argv[1]
    svg = page()
    open(out.replace(".png", ".svg"), "w").write(svg)
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1080})
        pg.set_content(f'<body style="margin:0">{svg}</body>'); pg.screenshot(path=out); b.close()
    print("wrote", out)
