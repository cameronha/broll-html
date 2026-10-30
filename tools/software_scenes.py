"""B-roll for "Building software ain't it" (2026-10-30 footage) -> scenes/sft-*.svg

usage: python3 tools/software_scenes.py
Times in ORIGINAL footage time live in videos/software.json. A cat sits at the lower right of this take: titles stay left and narrow (under 500 px), clear of the cat after the base zoom.
b1 software  a laptop full of code wears a gold crown; the crown falls off and the code goes grey
b2 want      the crown lands on a customer; a thought bubble with a heart ("what customers want")
b3 habits    a customer thinks; a cart fills ("buying habits"); a red "Why?" bubble; a check
t1 know      Know your / customer
t2 aint      Building software / ain't it
"""
import os
from leon_scenes import root, title_root, tag, calm, check, CREAM, NAVY, ORANGE, PAPER, HERE
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, GOLD
from repetition_scenes import pill
from trash_scenes import heart

BLUE = "#5E7A94"
CODE = (ORANGE, GOLD, CREAM, "#8CBDDC")


def crown(cx, by, rot=0, k=1.0):
    """A gold crown, bottom center at (cx, by)."""
    w, h = 170 * k, 110 * k
    x0 = cx - w / 2
    r = f' transform="rotate({rot} {cx:.0f} {by - h / 2:.0f})"' if rot else ""
    d = (f"M{x0:.0f} {by:.0f} L{x0:.0f} {by - h:.0f} L{x0 + w * 0.25:.0f} {by - h * 0.45:.0f} L{cx:.0f} {by - h * 1.15:.0f} "
         f"L{x0 + w * 0.75:.0f} {by - h * 0.45:.0f} L{x0 + w:.0f} {by - h:.0f} L{x0 + w:.0f} {by:.0f} Z")
    return f'<path d="{d}" fill="{GOLD}"{r}/><rect x="{x0:.0f}" y="{by - 22 * k:.0f}" width="{w:.0f}" height="{22 * k:.0f}" fill="{ORANGE}"{r}/>'


def laptop(grey=False):
    lines = "".join(f'<rect x="{350 + 40 * (i % 3)}" y="{330 + 38 * i}" width="{300 - 60 * (i % 4)}" height="16" rx="8" '
                    f'fill="{GREY if grey else CODE[i % 4]}"/>' for i in range(6))
    return (f'<rect x="300" y="280" width="480" height="320" rx="18" fill="{NAVY}"/><rect x="326" y="304" width="428" height="272" rx="8" fill="{BLUE if not grey else "#4A5868"}"/>'
            + lines + f'<path d="M240 600 H840 L800 640 H280 Z" fill="{NAVY}"/>')


# ---- b-roll ----

def software():
    dur = 3.7
    s = root(dur, "1,0,0")
    s += g("lap", laptop(), (0.05, 2.3), rig(540, 640, 1, 0.5))
    s += g("lapg", laptop(True), (2.3, dur + 1), rig(540, 640, 1, 0.5))
    s += g("cr0", crown(540, 282), (0.05, 1.4), rig(540, 282, 3, 0.9))
    for i, (dx, dy, rot) in enumerate(((50, -40, 18), (150, -10, 45), (260, 120, 80), (370, 330, 110))):
        t0 = 1.4 + 0.17 * i
        s += g(f"cr{i + 1}", crown(540 + dx, 282 + dy, rot), (t0, t0 + 0.17))
    s += g("thud", crown(900, 790, 160, 0.9), (2.08, dur + 1), rig(900, 760, 2, 0.6))
    return s + "</svg>\n"


def want():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += head(5, [(0.05, "neutral"), (0.9, "surprised"), (1.6, "happy")], (380, 960), 1.15, False, "cust")
    for i, (y, t0) in enumerate(((90, 0.05), (230, 0.22), (370, 0.39))):
        s += g(f"fall{i}", crown(380, y, 0, 1.0), (t0, t0 + 0.17))
    s += g("cr", crown(380, 580, -8, 1.0), (0.56, dur + 1), rig(380, 580, 3, 0.9))
    s += g("bub", f'<ellipse cx="790" cy="300" rx="190" ry="150" fill="{CREAM}"/><circle cx="630" cy="480" r="30" fill="{CREAM}"/>'
                  f'<circle cx="585" cy="545" r="18" fill="{CREAM}"/>', (1.6, dur + 1), rig(790, 450, 3, 0.8))
    s += heart("h", 790, 290, (1.9, dur + 1), 2.2)
    return s + "</svg>\n"


def habits():
    dur = 4.5
    s = root(dur, "1,0,0")
    s += head(2, [(0.05, "skeptical"), (1.2, "neutral"), (2.4, "confused"), (3.3, "happy")], (290, 960), 1.0, False, "cust")
    s += g("cart", f'<path d="M560 420 H620 L670 680 H930 L970 500 H640" fill="none" stroke="{NAVY}" stroke-width="22" stroke-linejoin="round"/>'
                   f'<circle cx="700" cy="740" r="30" fill="{NAVY}"/><circle cx="900" cy="740" r="30" fill="{NAVY}"/>', (0.9, dur + 1), rig(800, 770, 2, 0.6))
    for i, (x, w, h, f, t0) in enumerate(((680, 80, 110, ORANGE, 1.3), (775, 70, 140, GOLD, 1.6), (860, 70, 90, CREAM, 1.9))):
        s += g(f"box{i}", f'<rect x="{x}" y="{670 - h}" width="{w}" height="{h}" rx="8" fill="{f}"/>', (t0, dur + 1), rig(x + w / 2, 670, 3, 1.0))
    s += pill("why", 780, 270, "Why?", 90, ORANGE, CREAM, (2.4, dur + 1))
    s += check("ok", 240, 330, 3.3, dur, 90)
    return s + "</svg>\n"


# ---- titles (left side: the cat sits at the lower right) ----

def t_know():
    dur = 1.6
    s = title_root(dur)
    s += tag("know", "Know your", 60, 770, 72, -2, 0.05, dur + 1)[0]
    s += tag("cust", "customer", 60, 880, 80, 2, 0.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_aint():
    dur = 2.7
    s = title_root(dur)
    s += tag("bld", "Building", 60, 680, 72, -2, 0.05, dur + 1)[0]
    s += tag("sw", "software", 60, 785, 72, 1, 0.35, dur + 1)[0]
    s += tag("aint", "ain't it", 60, 895, 92, 2, 1.4, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_know), ("t2", t_aint), ("b1", software), ("b2", want), ("b3", habits)):
        open(os.path.join(HERE, f"scenes/sft-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/sft-{n}.svg")
