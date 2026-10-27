"""B-roll for "Don't ask to meet investors" (2026-08-20 footage) -> scenes/inv-*.svg

usage: python3 tools/investors_scenes.py
Reuses the Leon and LinkedIn parts. Times in ORIGINAL footage time live in videos/investors.json.
t1 psa        PSA / First-time founders
b1 intro      a founder asks Cam for an intro to an investor
t2 customers  Customers / first
b2 pay        three customers, a paper bill pops above each
t3 vibe       2026 / Vibe coding
b3 build      code lines fill a screen, the product stacks up beside it
b4 road       the founder hops down a road past Build and Customers flags; the investor waits at the end
b5 strings    investors close in on the founder, red strings attached
t4 freedom    [x] Autonomy [x] Freedom [x] A business that makes money
b6 beholden   bank, investor, angel pop up, then each gets a red X
b7 money      the founder, happy, beside stacks of coins that grow
t5 before     Before investors: [x] Build something [x] Talk to customers
"""
import os
import cast_scenes as CS
from leon_scenes import root, title_root, tag, check, robot, calm, CREAM, NAVY, ORANGE, INK, PAPER, HERE
from linkedin_scenes import rig, g, dashes, building, GREY

GOLD = "#E9B949"
FOUNDER = 2                                            # the first-time founder: p2, a young man


def head(p, tl, pos, k=0.5, flip=False, gid="h", deg=4):
    return CS.head(p, tl, pos, k, flip, rig(pos[0], pos[1] - 10, deg), gid)


def label(x, y, text, size=40, color=NAVY):
    return f'<text x="{x}" y="{y}" font-family="Libre Franklin" font-weight="800" font-size="{size}" fill="{color}">{text}</text>'


def bill(gid, x, y, show):
    return g(gid, f'<rect x="{x}" y="{y}" width="150" height="80" rx="8" fill="{NAVY}"/>'
                  f'<rect x="{x + 8}" y="{y + 8}" width="134" height="64" rx="5" fill="{CREAM}"/>'
                  f'<circle cx="{x + 75}" cy="{y + 40}" r="24" fill="{GOLD}"/>' + label(x + 62, y + 56, "$", 42),
             show, rig(x + 75, y + 80, 6, 1.2))


def xmark(gid, cx, cy, show, s=70):
    return g(gid, f'<line x1="{cx - s}" y1="{cy - s}" x2="{cx + s}" y2="{cy + s}" stroke="{ORANGE}" stroke-width="26" stroke-linecap="round"/>'
                  f'<line x1="{cx + s}" y1="{cy - s}" x2="{cx - s}" y2="{cy + s}" stroke="{ORANGE}" stroke-width="26" stroke-linecap="round"/>', show)


# ---- b-roll ----

def intro():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("bubble", f'<rect x="90" y="230" width="230" height="110" rx="20" fill="{CREAM}"/>'
                     f'<path d="M180 336 L220 336 L196 380Z" fill="{CREAM}"/>' + label(118, 304, "Intro?", 56), (0.25, dur + 1), rig(205, 340, 3, 0.8))
    s += dashes("ask", (330, 520), (760, 520), (0.9, dur + 1), ORANGE, 10)
    s += g("bag", f'<circle cx="960" cy="760" r="62" fill="{ORANGE}"/><rect x="935" y="680" width="50" height="30" rx="8" fill="{ORANGE}"/>'
                  + label(940, 784, "$", 64, CREAM), None, rig(960, 820, 5, 1.0))
    s += head(FOUNDER, [(0, "excited")], (230, 640), 0.5, True, "founder")
    s += head(10, [(0, "neutral"), (1.6, "skeptical")], (540, 640), 0.5, False, "cam")
    s += head(8, [(0, "neutral")], (850, 640), 0.5, False, "investor")
    return s + "</svg>\n"


def pay():
    dur = 3.0
    s = root(dur, "1,0,0")
    for i, (p, x) in enumerate(((5, 230), (3, 540), (9, 850))):
        s += head(p, [(0, "happy")], (x, 700), 0.45, i == 0, f"cust{i}")
        s += bill(f"bill{i}", x - 75, 300, (0.35 + 0.35 * i, dur + 1))
    return s + "</svg>\n"


def build():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("screen", f'<rect x="80" y="200" width="520" height="400" rx="16" fill="{NAVY}"/><rect x="100" y="220" width="480" height="360" rx="6" fill="{CREAM}"/>'
                     f'<rect x="300" y="600" width="80" height="60" fill="{NAVY}"/><rect x="230" y="650" width="220" height="22" rx="10" fill="{NAVY}"/>')
    for i in range(8):
        w = (300, 220, 340, 180, 260, 320, 200, 280)[i]
        s += g(f"code{i}", f'<rect x="{130 + 40 * (i % 3)}" y="{250 + 38 * i}" width="{w}" height="18" rx="9" fill="{ORANGE if i % 4 == 2 else GREY}"/>', (0.1 + 0.12 * i, dur + 1))
    for i, (w, c) in enumerate(((260, NAVY), (220, ORANGE), (240, CREAM), (180, NAVY), (200, BLUE2), (140, ORANGE))):
        s += g(f"block{i}", f'<rect x="{800 - w / 2:.0f}" y="{690 - 66 * i}" width="{w}" height="58" rx="8" fill="{c}"/>', (1.0 + 0.22 * i, dur + 1))
    return s + "</svg>\n"


BLUE2 = "#5A8BB3"


def road():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("road", f'<path d="M-20 900 C 260 860 300 640 560 640 S 900 520 1100 500 L1100 580 C 900 600 820 720 560 720 S 300 940 -20 980Z" fill="{CREAM}"/>')
    flags = ((300, 760, "Build", NAVY, 0.9), (640, 650, "Customers", ORANGE, 1.7))
    for i, (x, y, text, c, t) in enumerate(flags):
        w = 30 + 24 * len(text)
        s += g(f"flag{i}", f'<rect x="{x - 4}" y="{y - 300}" width="8" height="300" fill="{NAVY}"/>'      # tall: the hopping head passes under the label
                           f'<rect x="{x + 4}" y="{y - 300}" width="{w}" height="62" rx="6" fill="{c}"/>' + label(x + 18, y - 255, text, 40, CREAM),
               (t, dur + 1), rig(x, y, 3, 0.7))
    s += head(8, [(2.4, "happy")], (960, 470), 0.36, False, "investor").replace(f'data-show="2.4,{dur + 1}"', f'data-show="2.40,{dur + 1:.2f}"')
    pts = [(80, 900), (190, 860), (300, 790), (400, 720), (500, 690), (620, 660), (720, 610), (800, 570)]
    for i, (x, y) in enumerate(pts):
        t0, t1 = 0.3 * i, (0.3 * (i + 1) if i < len(pts) - 1 else dur + 1)
        lift = 0 if i in (0, len(pts) - 1) else 18
        s += CS.head(FOUNDER, [(t0, "excited" if i < len(pts) - 1 else "happy")], (x, y - lift), 0.32, True, rig(x, y, 0), f"piece{i}").replace(
            f'data-show="{t0},{dur + 1}"', f'data-show="{t0:.2f},{t1:.2f}"')
    return s + "</svg>\n"


def strings():
    dur = 3.0
    s = root(dur, "1,0,0")
    inv = ((8, (190, 400), False), (7, (890, 400), True), (6, (200, 860), False), (3, (880, 860), True))   # not p4: it reads as Cam
    for i, (p, (x, y), flip) in enumerate(inv):
        t = 0.3 + 0.3 * i
        s += dashes(f"str{i}", (x + (60 if not flip else -60), y - 120), (540, 520), (t + 0.15, dur + 1), ORANGE, 8)
        s += head(p, [(t, "skeptical")], (x, y), 0.4, not flip, f"inv{i}").replace(f'data-show="{t},{dur + 1}"', f'data-show="{t:.2f},{dur + 1:.2f}"')
    s += head(FOUNDER, [(0, "neutral"), (1.0, "worried")], (540, 640), 0.5, False, "founder")
    return s + "</svg>\n"


def beholden():
    dur = 3.3
    s = root(dur, "1,0,0")
    bank = (f'<path d="M80 440 L220 360 L360 440Z" fill="{NAVY}"/><rect x="90" y="440" width="260" height="24" fill="{NAVY}"/>'
            + "".join(f'<rect x="{110 + 60 * i}" y="470" width="34" height="200" fill="{CREAM}"/>' for i in range(4))
            + f'<rect x="80" y="670" width="280" height="30" fill="{NAVY}"/>' + label(160, 420, "Bank", 34, CREAM))
    s += g("bank", bank, (0.3, dur + 1), rig(220, 700, 2, 0.6))
    s += head(8, [(0.8, "neutral")], (560, 680), 0.45, False, "investor").replace(f'data-show="0.8,{dur + 1}"', f'data-show="0.80,{dur + 1:.2f}"')
    s += g("halo", f'<ellipse cx="880" cy="390" rx="90" ry="22" fill="none" stroke="{GOLD}" stroke-width="14"/>', (1.4, dur + 1), rig(880, 400, 6, 1.2))
    s += head(7, [(1.4, "happy")], (880, 680), 0.45, False, "angel").replace(f'data-show="1.4,{dur + 1}"', f'data-show="1.40,{dur + 1:.2f}"')
    for i, (cx, t) in enumerate(((220, 2.1), (560, 2.35), (880, 2.6))):
        s += xmark(f"x{i}", cx, 540, (t, dur + 1))
    return s + "</svg>\n"


def money():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += head(FOUNDER, [(0, "happy"), (1.4, "excited")], (300, 640), 0.55, True, "founder")
    for c, x in enumerate((620, 760, 900)):
        for j in range(4 + 2 * c):
            y = 730 - 34 * j
            s += g(f"coin{c}-{j}", f'<ellipse cx="{x}" cy="{y}" rx="62" ry="20" fill="{shade_gold(j)}"/>'
                                   f'<ellipse cx="{x}" cy="{y - 6}" rx="62" ry="20" fill="{GOLD}"/>', (0.2 + 0.12 * j + 0.15 * c, dur + 1))
    return s + "</svg>\n"


def shade_gold(j):
    return "#C99A2E" if j % 2 else "#B98A22"


# ---- titles ----

def t_psa():
    dur = 3.0
    s = title_root(dur)
    s += tag("psa", "PSA", 60, 700, 130, -3, 0.2, dur + 1, ORANGE, PAPER)[0]
    s += tag("ftf", "First-time founders", 60, 880, 84, 2, 1.4, dur + 1)[0]
    return s + "</svg>\n"


def t_customers():
    dur = 2.0
    s = title_root(dur)
    g1, w = tag("cust", "Customers", 60, 800, 110, -3, 0.6, dur + 1); s += g1
    s += tag("first", "first", 60 + w + 20, 810, 110, 2, 1.2, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_vibe():
    dur = 4.0
    s = title_root(dur)
    s += tag("yr", "2026", 60, 720, 110, -3, 0.4, dur + 1)[0]
    s += tag("vibe", "Vibe coding", 60, 880, 100, 2, 3.0, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_freedom():
    dur = 5.8
    s = title_root(dur)
    for i, (word, t) in enumerate((("Autonomy", 0.3), ("Freedom", 0.8), ("A business that makes money", 1.9))):
        y = 690 + 112 * i
        s += check(f"c{i}", 52, y + 12, t, dur) + tag(f"i{i}", word, 128, y, 64, (1, -1, 1)[i], t, dur + 1, ORANGE if i == 2 else None, PAPER if i == 2 else None)[0]
    return s + "</svg>\n"


def t_before():
    dur = 6.4
    s = title_root(dur)
    s += tag("bi", "Before investors:", 50, 676, 56, -2, 0.3, dur + 1, ORANGE, PAPER)[0]
    s += check("c1", 52, 784, 1.8, dur) + tag("i1", "Build something", 128, 772, 66, 1, 1.8, dur + 1)[0]
    s += check("c2", 52, 896, 3.5, dur) + tag("i2", "Talk to customers", 128, 884, 66, -1, 3.5, dur + 1)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_psa), ("t2", t_customers), ("t3", t_vibe), ("t4", t_freedom), ("t5", t_before),
                 ("b1", intro), ("b2", pay), ("b3", build), ("b4", road), ("b5", strings), ("b6", beholden), ("b7", money)):
        open(os.path.join(HERE, f"scenes/inv-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/inv-{n}.svg")
