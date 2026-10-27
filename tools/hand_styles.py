"""Hand-style sheet: four poses (open, fist, point, grip a page) in six hand designs
-> ~/Claude-files/broll-html/28-hands/hands-sheet.jpg

usage: python3 tools/hand_styles.py
Everything except the hand stays fixed (Rubens-lite pen, light skin, ochre sleeve), so the sheet
compares hand design only. Ordered from least to most detailed. Hands are drawn wrist at (0, 0),
fingers up, thumb on the left; "grip" returns (back, front) so the page sits between them.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubens_scene as R
from rubens_scene import pen, fine, circ, oval, INK
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Claude-files/broll-html/28-hands")
SKIN = R.SKIN = "#F6DDB0"
POSES = ("open", "fist", "point", "grip")


def solid(d, c=SKIN):
    return f'<path d="{d}" fill="{c}"/>'


def shape(d, w=3.2):
    return solid(d) + pen(d, w)


def nub(pose):
    o = shape(circ(0, -16, 20))
    return (o, "") if pose == "grip" else o


def mitten(pose):
    ball = "M-24 0 L-26 -30 Q-26 -54 0 -54 Q26 -54 26 -30 L24 0 Z"
    if pose == "open":
        return R.cap(-16, -20, -40, -48, 16, 3.2) + shape("M-22 0 L-24 -62 Q-24 -94 0 -94 Q24 -94 24 -62 L22 0 Z")
    if pose == "fist":
        return shape(ball) + R.cap(-18, -14, 6, -24, 14, 3.2)
    if pose == "point":
        return R.cap(-10, -40, -10, -90, 14, 3.2) + shape(ball) + R.cap(-18, -14, 6, -24, 14, 3.2)
    return shape(ball), R.cap(-16, -24, -4, -64, 15, 3.2)


def fingered(n, w, reach, knuckles=True):
    """n outlined fingers of width w; reach scales their length."""
    xs = [(-14 + 28 * i / (n - 1)) for i in range(n)]
    fist = "M-22 0 L-24 -26 Q-24 -42 -10 -42 L10 -42 Q24 -42 24 -26 L22 0 Z"
    marks = lambda: fine(" ".join(f"M{(xs[i] + xs[i + 1]) / 2:.0f} -42 L{(xs[i] + xs[i + 1]) / 2:.0f} -30" for i in range(n - 1)), 1.8) if knuckles else ""

    def draw(pose):
        if pose == "open":
            fs = ""
            for i, x in enumerate(xs):
                a = -0.3 + 0.6 * i / (n - 1)
                L = 50 * reach * (1 - 0.15 * abs(i - (n - 1) / 2) / ((n - 1) / 2))
                fs += R.cap(x, -38, x + L * math.sin(a), -38 - L * math.cos(a), w, 3.2)
            return R.cap(-18, -14, -40, -40, w, 3.2) + fs + shape("M-22 0 L-24 -38 Q-24 -50 -12 -50 L12 -50 Q24 -50 24 -38 L22 0 Z")
        if pose == "fist":
            return shape(fist) + marks() + R.cap(-18, -12, 6, -22, w - 1, 3.2)
        if pose == "point":
            return R.cap(xs[0], -36, xs[0], -36 - 54 * reach, w, 3.2) + shape(fist) + marks() + R.cap(-18, -12, 6, -22, w - 1, 3.2)
        return shape(fist) + marks(), R.cap(-16, -22, -4, -64, w, 3.2)
    return draw


def current(pose):
    back, front = R.hand_parts(pose, 3.2)
    return (back, front) if pose == "grip" else back + front


def gesture(pose):
    """Quick loose strokes: a skin patch, an open palm contour, single-line fingers."""
    R.LOOSE = True
    st = lambda d, w=4.2: pen(d, w)
    if pose == "open":
        o = (solid("M-22 0 L-24 -46 L24 -46 L22 0 Z") + st("M-22 0 Q-26 -24 -22 -46 M22 0 Q26 -24 22 -46")
             + st("M-20 -44 Q-30 -70 -28 -86 M-8 -48 Q-10 -78 -8 -94 M6 -48 Q8 -78 10 -92 M18 -44 Q26 -68 28 -82")
             + st("M-22 -16 Q-36 -26 -44 -46"))
    elif pose in ("fist", "grip"):
        o = solid(oval(0, -24, 25, 26)) + st("M-22 2 Q-30 -30 -18 -46 Q0 -54 18 -46 Q30 -30 22 2") + st("M-14 -46 Q-12 -36 -16 -30 M2 -50 Q4 -40 0 -32 M16 -44 Q16 -36 12 -30", 2.4)
        if pose == "fist":
            o += st("M-22 -8 Q-8 -12 10 -28")
        else:
            o = (o, st("M-18 -20 Q-14 -44 -4 -64"))
    else:
        o = solid(oval(0, -24, 25, 26)) + st("M-22 2 Q-30 -30 -18 -46 Q0 -54 18 -46 Q30 -30 22 2") + st("M-12 -44 Q-14 -70 -10 -92") + st("M-22 -8 Q-8 -12 10 -28")
    R.LOOSE = False
    return o


STYLES = [("1  No hands (nub)", nub), ("2  Mitten", mitten), ("3  Cartoon (3 fingers + thumb)", fingered(3, 18, 0.95, False)),
          ("4  Rounded chunky fingers", fingered(4, 16, 0.75)), ("5  Current library", current), ("6  Gesture sketch", gesture)]

SLEEVE = "M-30 4 L-34 90 L34 90 L30 4 Z"
PAGE = "M-34 -104 L84 -116 L94 -24 L-24 -12 Z"


def one(fn, pose):
    h = fn(pose)
    if pose == "grip":
        back, front = h
        h = back + solid(PAGE, "#FFFFFF") + pen(PAGE, 3) + fine("M-4 -90 L70 -98 M-2 -72 L72 -80 M0 -54 L50 -59", 1.6) + front
    sleeve = solid(SLEEVE, R.FILL) + f'<path d="{SLEEVE}" fill="{R.FILL}" transform="translate(7 5)"/>' + pen(SLEEVE) + pen("M-31 22 L31 22", 2.4)
    return h + sleeve


def cell(fn):
    head = R.root("hands")[0].replace('width="1080" height="1080" viewBox="0 0 1080 1080"', 'width="800" height="300" viewBox="0 0 800 300"')
    body = "".join(f'<g transform="translate({100 + 200 * i} 200) scale(1.45)">{one(fn, p)}</g>' for i, p in enumerate(POSES))
    return head + f'<g filter="url(#ink)">{body}</g></svg>'


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 800, "height": 300}, device_scale_factor=1.5)
        for i, (_, fn) in enumerate(STYLES):
            pg.set_content(f'<body style="margin:0;background:{R.BG}">{cell(fn)}</body>')
            pg.screenshot(path=f"{OUT}/hand-{i + 1}.png")
        b.close()
    W, H = 1200, 450
    sheet = Image.new("RGB", (2 * W + 10, 3 * (H + 10)), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
    for i, (label, _) in enumerate(STYLES):
        x, y = (i % 2) * (W + 10), (i // 2) * (H + 10)
        sheet.paste(Image.open(f"{OUT}/hand-{i + 1}.png").convert("RGB"), (x, y))
        d.text((x + 18, y + 12), label, fill="black", font=f)
    sheet.save(f"{OUT}/hands-sheet.jpg", quality=88)
    print(f"{OUT}/hands-sheet.jpg")
