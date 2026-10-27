"""Classical figures cut as a Baroque woodcut (after Jegher/Rubens) -> still PNG

usage: python3 tools/classical_scene.py OUT.png
The scene is a list of parts (filled shapes) and ink strokes (details). It renders twice at 2x:
an ink pass (outlines + details) and a data pass where each part's fill encodes its hatch angle (R),
its curve (G) and its tone (B). Hatch lines run at the part's angle and bow by sqrt(distance to the
edge), so on a limb they wrap across it like the cross-contour lines in the reference.
"""
import math, os, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import woodcut as W

ITEMS = []
SP = 9
SKIN, CLOTH, HAIR = 0.74, 0.88, 0.42


def part(d, tone, ang, bend=0.4):
    ITEMS.append(("part", d, tone, ang % 180, bend))


def ink(d, w=3):
    ITEMS.append(("ink", d, w))


def spline(pts, n=12):
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p[i][j] + (-p[i - 1][j] + p[i + 1][j]) * t
                                    + (2 * p[i - 1][j] - 5 * p[i][j] + 4 * p[i + 1][j] - p[i + 2][j]) * t * t
                                    + (-p[i - 1][j] + 3 * p[i][j] - 3 * p[i + 1][j] + p[i + 2][j]) * t ** 3) for j in range(3)))
    return out + [pts[-1]]


def tube(pts, tone=SKIN, bend=0.6):
    """A limb through (x, y, width) points with round ends; hatch runs across its axis."""
    s = spline(pts)
    L, R, nrm = [], [], []
    for i, (x, y, w) in enumerate(s):
        a, b = s[max(i - 1, 0)], s[min(i + 1, len(s) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        g = math.hypot(tx, ty) or 1
        nx, ny = -ty / g, tx / g
        L.append((x + nx * w / 2, y + ny * w / 2)); R.append((x - nx * w / 2, y - ny * w / 2)); nrm.append((nx, ny, tx / g, ty / g))

    def cap(i, sgn):
        x, y, w = s[i]; nx, ny, tx, ty = nrm[i]
        return [(x + w / 2 * (sgn * nx * math.cos(f) + sgn * tx * math.sin(f)), y + w / 2 * (sgn * ny * math.cos(f) + sgn * ty * math.sin(f)))
                for f in np.linspace(0, math.pi, 9)]
    poly = L + cap(-1, 1)[1:-1] + R[::-1] + cap(0, -1)[1:-1]
    part("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + " Z", tone,
         math.degrees(math.atan2(pts[-1][1] - pts[0][1], pts[-1][0] - pts[0][0])) + 90, bend)


def curls(cx, cy, rx, ry, n, r=9, seed=1):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        a, k = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0, 1))
        x, y = cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)
        ink(f"M{x - r:.0f} {y:.0f} a{r} {r} 0 1 1 {r * 1.3:.0f} {r * 0.9:.0f} q-6 2 -8 -5", 2.6)


def cloud(x0, x1, y, h, n):
    pts = [(x0 + (x1 - x0) * i / n, y - h * math.sin(math.pi * i / n) ** 0.7) for i in range(n + 1)]
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for a, b in zip(pts, pts[1:]):
        r = math.hypot(b[0] - a[0], b[1] - a[1]) * 0.56
        d += f" A{r:.0f} {r:.0f} 0 0 1 {b[0]:.0f} {b[1]:.0f}"
    part(d + f" Q{(x0 + x1) / 2:.0f} {y + 14} {x0:.0f} {y} Z", 0.97, 0, 0)


def leaf(x, y, deg, ln, w=0.32):
    a = math.radians(deg); tx, ty = x + ln * math.cos(a), y + ln * math.sin(a)
    nx, ny = -math.sin(a) * ln * w, math.cos(a) * ln * w
    mx, my = (x + tx) / 2, (y + ty) / 2
    part(f"M{x:.0f} {y:.0f} Q{mx + nx:.0f} {my + ny:.0f} {tx:.0f} {ty:.0f} Q{mx - nx:.0f} {my - ny:.0f} {x:.0f} {y:.0f} Z", 0.7, deg + 60, 0.2)
    ink(f"M{x:.0f} {y:.0f} L{tx:.0f} {ty:.0f}", 2)


def scene():
    # sky, clouds, birds, land
    cloud(40, 420, 170, 90, 6); cloud(300, 560, 110, 60, 5); cloud(640, 1040, 150, 70, 7)
    for x, y in [(860, 300), (900, 286), (930, 320)]:
        ink(f"M{x - 12} {y} q6 -8 12 0 q6 -8 12 0", 2.4)
    part("M0 800 Q200 770 420 792 Q640 808 820 780 Q960 764 1080 784 L1080 1080 L0 1080 Z", 0.94, 2, 0)
    for x, y, r in [(600, 776, 20), (624, 768, 24), (650, 778, 18)]:
        part(f"M{x - r} {y + r} Q{x - r - 6} {y - r} {x} {y - r} Q{x + r + 6} {y - r} {x + r} {y + r} Z", 0.66, 80, 0.3)
    part("M0 960 Q300 948 560 962 Q820 972 1080 956 L1080 1080 L0 1080 Z", 0.72, 3, 0)
    for i in range(7):
        leaf(960, 990, -150 + i * 22 + (i % 2) * 6, 80 + 18 * (i % 3))
    for i in range(5):
        leaf(70, 985, -140 + i * 26, 60 + 14 * (i % 2))

    # the skeptic: heavy bald elder with a big beard on a rock, arms crossed, cloth over the lap
    part("M140 990 Q130 860 160 770 Q190 700 250 692 Q320 690 360 730 Q392 800 386 990 Z", 0.6, 30, 0.2)
    ink("M190 800 Q220 840 210 900 M300 760 L330 800", 2.6)
    tube([(430, 715, 52), (426, 840, 46), (418, 950, 36)])
    part("M404 940 L436 940 Q470 958 478 978 L402 980 Z", SKIN, 90, 0.3)
    tube([(470, 722, 58), (478, 840, 48), (482, 950, 38)])
    part("M462 944 L496 944 Q536 960 540 980 L460 982 Z", SKIN, 90, 0.3)
    ink("M520 972 L522 980 M508 968 L510 980", 2)
    part("M216 626 L380 626 Q456 640 494 676 Q510 716 486 748 Q470 760 440 748 Q420 790 424 860 L398 862 Q394 790 404 744 Q320 760 232 744 Q206 690 216 626 Z", CLOTH, 90, 0.5)
    for k in range(5):
        ink(f"M{300 + k * 36} 650 Q{320 + k * 38} 700 {300 + k * 40} 744", 2.4)
    ink("M408 760 Q412 810 410 856", 2.4)
    part("M218 440 Q292 412 362 436 Q394 474 400 548 Q404 620 372 656 Q300 672 232 652 Q204 560 206 488 Q208 452 218 440 Z", SKIN, 0, 0.9)
    ink("M246 604 Q320 634 394 592", 3.2); ink("M314 624 q8 7 16 0", 2.6); ink("M232 470 Q262 500 296 486", 2.6)
    tube([(226, 452, 54), (214, 500, 50), (216, 548, 44)])
    tube([(364, 452, 54), (384, 500, 50), (390, 548, 44)])
    tube([(212, 552, 44), (280, 548, 40), (342, 532, 36)])
    part("M330 514 Q360 506 366 526 Q366 546 344 548 Q328 544 330 514 Z", SKIN, 90, 0.3)
    tube([(394, 546, 44), (330, 530, 40), (262, 520, 36)])
    part("M268 500 Q238 498 236 520 Q238 540 262 540 Q276 536 268 500 Z", SKIN, 90, 0.3)
    ink("M254 508 L240 512 M256 520 L238 524 M258 532 L242 534", 2.2)
    part("M246 312 Q242 254 292 248 Q342 250 340 310 Q340 340 330 352 L256 354 Q248 340 246 312 Z", SKIN, 0, 0.8)
    part("M246 304 Q230 302 232 320 Q236 336 250 334 Z", SKIN, 90, 0.3)
    part("M250 330 Q238 390 262 440 Q286 482 302 488 Q326 466 340 424 Q352 380 338 330 Q330 354 316 358 Q298 348 288 350 Q270 356 258 346 Z", 0.58, 95, 0.1)
    for x0 in range(258, 340, 12):
        ink(f"M{x0} 360 q-6 22 2 44 q8 24 {(300 - x0) * 0.25:.0f} {50 - abs(x0 - 296) * 0.4:.0f}", 2.2)
    ink("M276 348 Q290 336 298 346 Q308 336 322 348", 4)
    curls(238, 290, 10, 22, 4, 7, 3); curls(342, 292, 8, 20, 3, 7, 4)
    ink("M262 296 L286 306 M304 306 L328 294", 5)
    ink("M266 312 Q276 307 286 314 M302 314 Q312 307 322 312", 3); ink("M268 318 L286 318 M304 318 L320 318", 1.8)
    W_DOTS.extend([(281, 312, 4.5), (317, 311, 4.5)])
    ink("M296 306 Q292 322 300 334 Q294 342 284 336", 3)
    ink("M268 276 Q294 268 318 276 M274 288 Q294 282 312 288", 2.2)

    # the founder: young athlete in a draped tunic, steps in and holds up a wax tablet with a chart
    tube([(848, 374, 46), (884, 430, 42), (888, 474, 38)])
    tube([(888, 474, 38), (898, 520, 34), (902, 560, 30)])
    part("M886 556 Q912 550 918 576 Q920 604 904 614 Q888 612 884 590 Z", SKIN, 90, 0.3)
    tube([(724, 740, 60), (714, 850, 50), (728, 958, 36)])
    part("M722 948 Q690 958 676 980 L752 982 L756 950 Z", SKIN, 0, 0.3)
    tube([(816, 740, 62), (826, 850, 50), (830, 958, 36)])
    part("M814 950 Q804 964 800 982 L866 982 L848 950 Z", SKIN, 0, 0.3)
    ink("M700 840 q8 8 16 0 M818 840 q8 8 16 0", 2.2)
    part("M700 546 L834 546 Q854 650 866 764 Q790 784 688 770 Q690 650 700 546 Z", CLOTH, 90, -0.4)
    for k in range(6):
        ink(f"M{714 + k * 24} 560 Q{708 + k * 26} 660 {704 + k * 30} 770", 2.4)
    part("M700 358 Q760 342 840 356 Q870 366 866 400 Q852 470 826 556 L706 560 Q690 480 684 420 Q680 372 700 358 Z", SKIN, 0, 0.9)
    ink("M712 412 Q740 444 768 420 M772 420 Q802 446 834 412", 3)
    ink("M768 436 L766 548 M738 470 Q766 480 794 470 M740 506 Q766 514 792 506", 2.4)
    part("M812 350 L868 374 L800 560 L744 560 Z", CLOTH, 20, -0.3)
    ink("M826 372 L766 556 M846 380 L786 556", 2.4)
    part("M754 296 L750 356 L800 358 L794 292 Z", SKIN, 0, 0.6)
    ink("M792 300 L772 352", 2.4)
    part("M728 196 Q740 170 772 168 Q812 168 822 206 Q828 250 806 282 Q796 300 790 318 L752 318 Q744 308 730 308 "
         "Q716 306 716 296 L712 288 Q716 284 712 278 L716 272 Q706 268 702 262 Q700 256 714 236 Q716 228 722 220 Q722 206 728 196 Z", SKIN, 10, 0.7)
    part("M722 214 Q724 168 772 160 Q826 160 832 214 Q834 262 806 286 Q800 250 786 236 Q760 212 722 214 Z", HAIR, 60, 0.3)
    curls(782, 210, 40, 36, 16, 9, 1)
    part("M778 236 Q798 232 798 252 Q796 270 780 268 Z", SKIN, 90, 0.2)
    ink("M716 226 Q728 220 742 226", 4); ink("M722 236 Q730 231 740 236 M724 241 L738 240", 2.6)
    W_DOTS.append((726, 237, 3.6))
    ink("M712 282 Q720 288 730 282", 2.6)
    tube([(702, 372, 48), (664, 410, 44), (640, 440, 40)])
    tube([(640, 442, 38), (604, 424, 34), (578, 404, 30)])
    part("M466 270 L578 254 L598 404 L486 420 Z", 0.55, 82, 0)
    part("M482 286 L566 274 L582 392 L498 404 Z", 0.93, 82, 0)
    for x, h in [(504, 40), (528, 64), (552, 98)]:
        ink(f"M{x} 392 L{x - 6 * h / 100:.0f} {392 - h}", 13)
    ink("M494 396 L578 384", 3)
    part("M556 372 Q584 366 592 386 Q596 410 576 418 Q556 420 552 400 Z", SKIN, 90, 0.3)
    ink("M556 384 L582 380 M556 396 L586 394 M558 408 L582 408", 2.2)


W_DOTS = []


def svg(mode):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080" shape-rendering="{"auto" if mode == "ink" else "crispEdges"}">',
         f'<rect width="1080" height="1080" fill="{"#fff" if mode == "ink" else "rgb(0,0,255)"}"/>']
    for it in ITEMS:
        if it[0] == "part":
            _, d, tone, ang, bend = it
            if mode == "ink":
                s.append(f'<path d="{d}" fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/>')
            else:
                s.append(f'<path d="{d}" fill="rgb({int(ang / 180 * 255)},{int(128 + bend * 60)},{int(tone * 255)})"/>')
        elif mode == "ink":
            s.append(f'<path d="{it[1]}" fill="none" stroke="#000" stroke-width="{it[2]}" stroke-linecap="round" stroke-linejoin="round"/>')
    if mode == "ink":
        s += [f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in W_DOTS]
    return "".join(s) + "</svg>"


def render():
    shots = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        for mode in ("ink", "data"):
            pg.set_content(f'<body style="margin:0">{svg(mode)}</body>')
            p = f"/tmp/classical-{mode}.png"; pg.screenshot(path=p)
            shots.append(np.asarray(Image.open(p).convert("RGB")).astype(int))
        b.close()
    return shots


def cut(inkimg, data):
    H, Wd, _ = data.shape
    ink_m = inkimg.mean(2) < 128
    back = data[..., 1] == 0
    change = np.zeros((H, Wd), bool)
    for dy, dx in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        change |= (np.abs(data - W.shift(data.reshape(H, Wd * 3), dy, dx * 3, 0).reshape(H, Wd, 3)).sum(2) > 6)
    figure = ~back & ~ink_m
    d = W.blur(W.distance(figure & ~change), 2)
    tone, ang, bend = data[..., 2] / 255, data[..., 0] / 255 * math.pi, (data[..., 1] - 128) / 60
    gy, gx = np.gradient(d)
    facing = -(gx * W.LIGHT[0] + gy * W.LIGHT[1]) / (np.hypot(gx, gy) + 1e-6)
    edge = np.clip(1 - d / 32, 0, 1) ** 1.4
    dark = np.clip(0.95 * (1 - tone) ** 1.15 + edge * (0.44 - 0.4 * facing) + 0.02, 0, 1)
    yy, xx = np.mgrid[0:H, 0:Wd]
    u = (-xx * np.sin(ang) + yy * np.cos(ang) + bend * 9 * np.sqrt(d)) / SP
    lines = (np.abs(u % 1 - 0.5) < dark * 0.55) & (dark > 0.1)
    a2 = ang + 0.9
    v = (-xx * np.sin(a2) + yy * np.cos(a2)) / (SP * 1.1)
    cross = np.abs(v % 1 - 0.5) < np.clip(dark - 0.55, 0, 1) * 1.1
    out = figure & (lines | cross)
    w = np.clip(1 - yy / (0.5 * H), 0, 1) ** 1.1 * 0.5
    out |= back & (w > 0.12) & (np.abs(((yy + 5 * np.sin(xx / 260)) / (SP * 1.3)) % 1 - 0.5) < w)
    out |= ink_m | W.shift(ink_m, 1, 0, False)
    rgb = np.where(out[..., None], W.INK, W.PAPER).astype(np.uint8)
    return Image.fromarray(rgb).resize((Wd // 2, H // 2), Image.LANCZOS)


if __name__ == "__main__":
    scene()
    cut(*render()).save(sys.argv[1])
    print("wrote", sys.argv[1])
