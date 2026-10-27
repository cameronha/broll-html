"""Face-style sheet: the skeptic and the founder, head and shoulders, in eight face designs
-> ~/Claude-files/broll-html/27-faces/faces-sheet.jpg

usage: python3 tools/face_styles.py
Everything except the face stays fixed (Rubens-lite pen, light skin, ochre clothes), so the sheet
compares face design only. Ordered from least to most detailed.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubens_scene as R
from rubens_scene import pen, fine, hatch, circ, oval, INK
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Claude-files/broll-html/27-faces")
SKIN = R.SKIN = "#F6DDB0"
SPIKY = "M-120 -20 Q-125 -130 -5 -138 Q125 -140 130 -30 L105 -62 L85 -28 L60 -72 L35 -34 L10 -76 L-15 -40 L-45 -76 L-65 -38 L-90 -66 Z"
HAIR = {"sk": R.HAIR["cap"], "fo": SPIKY}
HEAD = circ(0, 0, 125)
JAW = "M-115 -10 Q-118 -130 0 -132 Q118 -130 115 -10 Q112 60 80 100 Q40 135 0 136 Q-40 135 -80 100 Q-112 60 -115 -10Z"


def dot(x, y, r, c=INK):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{c}"/>'


def solid(d, c):
    return f'<path d="{d}" fill="{c}"/>'


def base(who, L, shape=HEAD, hair=True, shade=True):
    """Ear, skin, side shadow, outline, hatched hair. L = look direction (+1 right, -1 left)."""
    ear = (-120 * L, 18)
    o = solid(circ(*ear, 24), SKIN) + pen(circ(*ear, 24)) + solid(shape, SKIN)
    if shade:
        o += f'<clipPath id="h{who}{abs(hash(shape)) % 9999}"><path d="{shape}"/></clipPath><g clip-path="url(#h{who}{abs(hash(shape)) % 9999})">{hatch(40, -60, 9, 11, 120, 0.35, 2.2)}</g>'
    o += pen(shape)
    if hair:
        o += solid(HAIR[who], R.FILL) + f'<path d="{HAIR[who]}" fill="url(#hair)"/>' + pen(HAIR[who])
    return o


# --- the eight styles; each returns the head in local units (radius 125) ---

def minimal(who, L):
    o = base(who, L, shade=False) + dot(-36 + 16 * L, 6, 9) + dot(40 + 16 * L, 6, 9)
    return o + (pen("M-14 70 L36 62", 4.5) if who == "sk" else pen("M-50 54 Q-6 104 40 54", 4.5))


def ligne(who, L):
    o = base(who, L, shade=False) + dot(-34 + 14 * L, 6, 8) + dot(42 + 14 * L, 6, 8)
    nose = f"M{12 * L} 12 Q{46 * L} 40 {14 * L} 46"
    if who == "sk":
        o += pen("M-60 -30 L-14 -24", 3.4) + pen("M20 -38 L66 -48", 3.4) + pen("M-8 82 Q16 74 40 84", 3.6)
    else:
        o += pen("M-62 -34 Q-38 -46 -14 -38", 3.4) + pen("M20 -40 Q44 -50 66 -38", 3.4) + solid("M-50 66 Q-6 108 34 66 Z", "#FFFFFF") + pen("M-50 66 Q-6 108 34 66 Z", 3.2)
    return o + pen(nose, 3)


def editorial(who, L):
    """Dash eyes, one big nose, heavy brows: the newspaper-cartoon face."""
    o = base(who, L, shade=False)
    nose = f"M{-4 * L} -6 Q{84 * L} 26 {66 * L} 56 Q{44 * L} 76 {0} 58"
    o += pen(f"M{-52 + 10 * L} 4 L{-24 + 10 * L} 4", 5) + pen(f"M{22 + 10 * L} 2 L{50 + 10 * L} 2", 5)
    if who == "sk":
        o += (pen("M-62 -24 L-18 -18", 7) + pen("M18 -30 L62 -44", 7) + fine("M-50 -66 Q0 -76 50 -66 M-40 -82 Q0 -90 40 -82", 2)
              + solid(nose, SKIN) + pen(nose, 3.4) + solid("M-30 70 Q10 56 52 72 Q20 84 -30 70 Z", R.FILL) + f'<path d="M-30 70 Q10 56 52 72 Q20 84 -30 70 Z" fill="url(#hair)"/>'
              + pen("M-6 96 L30 92", 3.6))
    else:
        o += (pen("M-62 -36 Q-40 -50 -18 -40", 7) + pen("M18 -44 Q40 -56 62 -42", 7)
              + solid(nose, SKIN) + pen(nose, 3.4) + solid("M-58 72 Q-10 120 30 74 Z", "#FFFFFF") + pen("M-58 72 Q-10 120 30 74 Z", 3.2))
    return o


def v9(who, L):
    """The current faces: big white eyes, bar brows, oval nose."""
    o = base(who, L)
    for ex in (-42, 43):
        o += solid(oval(ex, 5, 24, 24), "#FFFFFF") + pen(oval(ex, 5, 24, 24), 2.6) + dot(ex + 10 * L, 8, 10)
        if who == "sk":
            o += solid(f"M{ex - 26} -22 L{ex + 26} -22 L{ex + 26} 4 L{ex - 26} 4 Z", SKIN) + pen(f"M{ex - 24} 4 Q{ex} 0 {ex + 24} 4", 2.6)
    o += pen(oval(14 * L, 40, 14, 11), 2.4)
    if who == "sk":
        return o + pen("M-68 -36 L-18 -30", 6) + pen("M18 -46 L68 -58", 6) + pen("M-24 82 Q10 74 36 84", 4.2)
    g = "M-67 64 Q-20 50 43 60 Q29 114 -17 116 Q-57 112 -67 64Z"
    return (o + pen("M-68 -50 Q-44 -62 -18 -54", 6) + pen("M18 -54 Q44 -62 68 -50", 6)
            + solid(g, R.ACCENT) + solid("M-63 66 Q-20 53 39 62 L36 76 Q-19 68 -60 80Z", "#FFFFFF") + pen(g, 2.8))


def geometric(who, L):
    """Bauhaus: a rounded-square head, half-circle eyes, triangle nose, block mouth."""
    sq = "M-110 -120 L110 -120 Q125 -120 125 -105 L125 95 Q125 125 95 125 L-95 125 Q-125 125 -125 95 L-125 -105 Q-125 -120 -110 -120 Z"
    o = base(who, L, sq, hair=False, shade=False)
    o += solid("M-125 -40 L-125 -105 Q-125 -120 -110 -120 L110 -120 Q125 -120 125 -105 L125 -40 L60 -64 L0 -40 L-60 -64 Z" if who == "fo" else "M-125 -50 L-125 -105 Q-125 -120 -110 -120 L110 -120 Q125 -120 125 -105 L125 -50 Z", INK)
    for ex in (-42, 42):
        x = ex + 8 * L
        o += (solid(f"M{x - 22} 4 A22 22 0 0 0 {x + 22} 4 Z", INK) if who == "sk" else solid(circ(x, 4, 20), "#FFFFFF") + pen(circ(x, 4, 20), 3) + dot(x + 8 * L, 6, 9))
    o += solid(f"M{10 * L} 20 L{36 * L} 58 L{0} 58 Z", R.FILL) + pen(f"M{10 * L} 20 L{36 * L} 58 L{0} 58 Z", 3)
    if who == "sk":
        return o + solid("M-34 -32 L4 -26 L4 -18 L-34 -24 Z", INK) + solid("M18 -26 L58 -40 L58 -32 L18 -18 Z", INK) + solid("M-20 82 L40 78 L40 88 L-20 92 Z", INK)
    return o + solid("M-50 76 L40 76 A45 36 0 0 1 -50 76 Z", R.ACCENT) + pen("M-50 76 L40 76 A45 36 0 0 1 -50 76 Z", 3)


def animated(who, L):
    """Feature-animation eyes: tall whites, irises with a highlight, curved lids, soft brows."""
    o = base(who, L)
    for ex in (-40, 42):
        o += solid(oval(ex, 2, 28, 34), "#FFFFFF") + pen(oval(ex, 2, 28, 34), 2.8) + dot(ex + 12 * L, 6, 14) + dot(ex + 12 * L + 5, 0, 4.5, "#FFFFFF")
        if who == "sk":
            o += solid(f"M{ex - 30} -34 L{ex + 30} -34 L{ex + 30} 0 Q{ex} -6 {ex - 30} 0 Z", SKIN) + pen(f"M{ex - 28} 0 Q{ex} -6 {ex + 28} 0", 3.4)
    o += pen(f"M{10 * L} 40 Q{24 * L} 50 {8 * L} 56", 3)
    if who == "sk":
        return o + pen("M-66 -40 Q-40 -38 -14 -32", 7) + pen("M16 -50 Q42 -66 68 -60", 7) + pen("M-20 86 Q8 80 34 88 Q10 94 -20 86", 3.4)
    g = "M-52 70 Q-6 64 40 70 Q30 118 -8 120 Q-46 116 -52 70 Z"
    return (o + pen("M-66 -54 Q-40 -72 -14 -58", 7) + pen("M16 -58 Q42 -74 68 -56", 7)
            + solid(g, R.ACCENT) + solid("M-48 72 Q-6 66 36 72 L33 84 Q-6 78 -45 86 Z", "#FFFFFF") + pen(g, 3))


def detailed(who, L):
    """Closest to the Rubens sheet: a jaw, almond eyes with lids, a modelled nose, lips, lines, stubble."""
    o = base(who, L, JAW)
    for ex in (-42, 40):
        x = ex + 6 * L
        o += (solid(f"M{x - 24} 6 Q{x} -12 {x + 24} 6 Q{x} 18 {x - 24} 6 Z", "#FFFFFF") + pen(f"M{x - 24} 6 Q{x} -12 {x + 24} 6", 3) + fine(f"M{x - 22} 8 Q{x} 18 {x + 22} 8", 1.8)
              + dot(x + 7 * L, 4, 7) + fine(f"M{x - 20} -6 Q{x} -18 {x + 20} -6", 1.6))
        if who == "sk":
            o += solid(f"M{x - 26} 6 Q{x} -16 {x + 26} 6 Q{x} -2 {x - 26} 6 Z", SKIN) + pen(f"M{x - 26} 4 Q{x} -4 {x + 26} 4", 3) + fine(f"M{x - 16} 22 Q{x} 28 {x + 16} 22", 1.6)
    nose = f"M{4 * L} -4 Q{14 * L} 30 {30 * L} 46 Q{18 * L} 58 {-4 * L} 52"
    o += pen(nose, 3) + hatch(-6 if L < 0 else 14, 6, 3, 5, 36, 0.3 * L, 1.6) + fine(f"M{-30 * L} 50 Q{-20 * L} 70 {-26 * L} 86 M{40 * L} 54 Q{48 * L} 70 {40 * L} 88", 1.8)
    if who == "sk":
        o += (pen("M-66 -30 Q-44 -34 -18 -24", 5) + pen("M18 -34 Q44 -50 66 -48", 5) + fine("M-50 -62 Q0 -72 50 -62 M-40 -78 Q0 -86 40 -78", 1.8)
              + pen("M-24 88 Q8 82 38 90", 3.6) + fine("M-18 96 Q8 102 32 96", 1.6)
              + fine(" ".join(f"M{x} {y} l2 8" for x, y in [(-60, 80), (-48, 96), (-30, 108), (-10, 114), (12, 114), (34, 108), (52, 96), (64, 80), (-40, 104), (24, 112)]), 2))
    else:
        g = "M-44 76 Q-4 68 38 76 Q28 112 -6 114 Q-38 110 -44 76 Z"
        o += (pen("M-62 -44 Q-40 -58 -16 -46", 5) + pen("M16 -48 Q40 -60 62 -46", 5) + solid(g, R.ACCENT)
              + solid("M-40 78 Q-4 71 34 78 L32 88 Q-4 82 -38 90 Z", "#FFFFFF") + pen(g, 2.8) + fine("M-56 70 Q-60 82 -52 90 M50 72 Q56 84 48 92", 1.8))
    return o


STYLES = [("1  Minimal: dot eyes, one line", minimal), ("2  Ligne claire (Tintin)", ligne), ("3  Editorial cartoon: big nose", editorial),
          ("4  v9 (now)", v9), ("5  Geometric (Bauhaus)", geometric), ("6  Feature animation", animated), ("7  Detailed sketch (Rubens)", detailed)]


def shoulders(who):
    d = "M-170 300 Q-160 175 -40 160 L40 160 Q160 175 170 300 Z"
    o = solid(d, R.FILL) + f'<path d="{d}" fill="{R.FILL}" transform="translate(7 5)"/>' + pen(d) + solid("M-30 110 L30 110 L32 162 L-32 162 Z", SKIN) + pen("M-30 110 L-32 162 M30 110 L32 162")
    o += pen("M-40 162 Q0 186 40 162", 2.8) if who == "sk" else pen("M-60 166 Q0 200 60 166", 2.8) + pen("M-16 182 L0 260 L16 182")
    return o + hatch(70, 180, 5, 9, 110, 0.05)


def cell(fn):
    head = R.root("faces")[0].replace('width="1080" height="1080" viewBox="0 0 1080 1080"', 'width="600" height="400" viewBox="0 0 600 400"')
    body = "".join(f'<g transform="translate({x} 175) scale(0.78)">{shoulders(w)}{fn(w, L)}</g>' for x, w, L in [(160, "sk", 1), (440, "fo", -1)])
    return head + f'<g filter="url(#ink)">{body}</g></svg>'


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 600, "height": 400}, device_scale_factor=1.5)
        for i, (_, fn) in enumerate(STYLES):
            pg.set_content(f'<body style="margin:0;background:{R.BG}">{cell(fn)}</body>')
            pg.screenshot(path=f"{OUT}/face-{i + 1}.png")
        b.close()
    W, H = 900, 600
    sheet = Image.new("RGB", (2 * W + 10, 4 * (H + 10)), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 34)
    for i, (label, _) in enumerate(STYLES):
        x, y = (i % 2) * (W + 10), (i // 2) * (H + 10)
        sheet.paste(Image.open(f"{OUT}/face-{i + 1}.png").convert("RGB"), (x, y))
        d.text((x + 18, y + 12), label, fill="black", font=f)
    sheet.save(f"{OUT}/faces-sheet.jpg", quality=88)
    print(f"{OUT}/faces-sheet.jpg")
