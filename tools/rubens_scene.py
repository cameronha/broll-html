"""Rubens-lite look: hand-drawn scenes -> scenes/rubens-{pitch,crowd,three,reading,pile}.svg

usage: python3 tools/rubens_scene.py
Reference: a digital sketch sheet after Rubens (loose dark pen, real heads, one flat ochre behind).
Unlike the stick looks, every figure here is drawn by hand: contour lines (each drawn twice, a little
apart, like a quick pen), short hatch strokes for shadow, and a loose ochre fill set off register.
Faces are founder-v9 faces redrawn in pen (v9_head for the two pitch characters, face() for everyone else).
person() draws a generic standing body in the founder's coordinates, scaled into place.
Rig groups match the stick scenes.
"""
import math
import os
import random

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, FILL, BG, ACCENT = "#2A2522", "#E3A84B", "#FBFAF6", "#B5452B"
FILL_BG = "#F2DDB6"   # wash color
SKIN = "#F6DDB0"   # face and hand color (a lighter tone separates skin from clothes)
LOOSE = False   # True: the second pen pass is a jittered redraw, not an offset copy
LW = 1.0        # pen weight multiplier; person() sets it to 1/scale so scaled people keep their line weight
CLIPS = [0]
HIP = (760, 606)   # founder hip, the pivot for upper-body posture
HANDS = "nub"   # "library" (fingered poses) or "nub"
WASH = True     # a soft ochre shape behind the people that sways slowly


def pen(d, w=3.2):
    """A contour, drawn twice: the main stroke and a thinner second pass slightly off."""
    st = f'fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"'
    w *= LW
    if LOOSE:       # a quick second look: every point nudged a little, thinner, and an overshoot at the start
        import re
        rnd = random.Random(d)
        d2 = re.sub(r"-?\d+\.?\d*", lambda m: f"{float(m.group()) + rnd.uniform(-2.6, 2.6) * LW:.1f}", d)
        return (f'<path d="{d}" {st} stroke-width="{w * rnd.uniform(0.8, 1.15):.2f}"/>'
                f'<path d="{d2}" {st} stroke-width="{w * 0.45:g}" opacity="0.8"/>')
    return (f'<path d="{d}" {st} stroke-width="{w:g}"/>'
            f'<path d="{d}" {st} stroke-width="{w * 0.5:g}" opacity="0.7" transform="translate({1.6 * LW:g} {-1.2 * LW:g})"/>')


def fine(d, w=1.8):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w * LW:g}" stroke-linecap="round"/>'


def hatch(x, y, n, step, L, dx=0.45, w=1.6):
    """n parallel short strokes from (x, y), stepping right by `step`, each L long and slanted by dx."""
    return fine(" ".join(f"M{x + i * step:.0f} {y:.0f} l{L * dx:.0f} {L:.0f}" for i in range(n)), w)


def denim(d):
    """Trousers: a light all-over hatch, so they read apart from the top in a one-color scene."""
    return f'<path d="{d}" fill="url(#denim)"/>'


def fill(d, dx=7, dy=5):
    return f'<path d="{d}" fill="{FILL}" transform="translate({dx} {dy})"/>'


def blob(d, w):
    """A thick ochre stroke along a limb, off register."""
    return f'<path d="{d}" fill="none" stroke="{FILL}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" transform="translate(7 5)"/>'


def circ(cx, cy, r):
    return f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0"


def oval(cx, cy, rx, ry):
    return f"M{cx - rx} {cy} a{rx} {ry} 0 1 0 {2 * rx} 0 a{rx} {ry} 0 1 0 {-2 * rx} 0"


V9 = {  # the founder-v9 faces, in v9 coordinates: head center, radius, ear, hair, eyes, pupils, lids, brows, nose, mouth
    "customer": dict(c=(255, 405), r=125, ear=(150, 420),
                     hair="M135 380 Q130 270 250 268 Q370 270 378 370 Q330 320 255 330 Q180 335 135 380Z",
                     eyes=[(215, 410, 26, 18), (300, 410, 26, 18)], pupils=[(224, 414, 10), (309, 414, 10)],
                     lids=[(187, 390, 56, 18), (272, 390, 56, 18)],
                     brows=["M187 371 L243 387", "M274 367 L330 353"], nose=(262, 446, 14, 10),
                     mouth="M220 486 Q258 474 300 492", grin=None, shade=(300, 470)),
    "founder": dict(c=(665, 360), r=128, ear=(785, 375),
                    hair="M545 340 Q540 230 660 222 Q790 220 795 330 L770 298 L750 332 L725 288 L700 326 L675 284 L650 320 L620 284 L600 322 L575 294 Z",
                    eyes=[(605, 365, 26, 30), (685, 365, 26, 30)], pupils=[(595, 368, 12), (675, 368, 12)], lids=[],
                    brows=["M580 327 L632 321", "M660 317 L712 323"], nose=(642, 398, 16, 12),
                    mouth=None, grin=("M598 424 Q645 410 708 420 Q694 474 648 476 Q608 472 598 424Z", "M602 426 Q645 413 704 422 L701 436 Q646 428 605 440Z"),
                    shade=(700, 420)),
}


def v9_head(who, x, y, k=0.62):
    """A founder-v9 face redrawn in pen: scaled by k and centered on (x, y). Widths are divided by k so lines keep their weight."""
    h = V9[who]
    (cx, cy), r = h["c"], h["r"]
    P = lambda d, w=3.2: pen(d, w / k)
    o = (f'<path d="{circ(*h["ear"], 24)}" fill="{SKIN}" transform="translate({7 / k:g} {5 / k:g})"/>' + f'<path d="{circ(cx, cy, r)}" fill="{SKIN}" transform="translate({7 / k:g} {5 / k:g})"/>'
         + P(circ(*h["ear"], 24)) + fine(f"M{h['ear'][0] - 8} {h['ear'][1] - 10} q10 8 0 22", 2.4 / k)
         + f'<path d="{circ(cx, cy, r)}" fill="{SKIN}"/>'
         + f'<clipPath id="clip-{who}{x}"><path d="{circ(cx, cy, r)}"/></clipPath>'
         + f'<g clip-path="url(#clip-{who}{x})">{hatch(h["shade"][0], h["shade"][1] - 60, 9, 11, 120, 0.35, 2.2 / k)}</g>'
         + P(circ(cx, cy, r)) + f'<path d="{h["hair"]}" fill="{FILL}"/><path d="{h["hair"]}" fill="url(#hair)"/>' + P(h["hair"]))
    for ex, ey, rx, ry in h["eyes"]:
        o += f'<path d="{oval(ex, ey, rx, ry)}" fill="#FFFFFF"/>' + P(oval(ex, ey, rx, ry), 2.6)
    o += "".join(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{INK}"/>' for px, py, pr in h["pupils"])
    for lx, ly, lw, lh in h["lids"]:     # heavy lids: skin over the top half of the eye, with the lid line
        o += f'<rect x="{lx}" y="{ly - 4}" width="{lw}" height="{lh + 4}" fill="{SKIN}"/>' + P(f"M{lx + 2} {ly + lh} Q{lx + lw / 2} {ly + lh - 4} {lx + lw - 2} {ly + lh}", 2.6)
    o += "".join(P(b, 6) for b in h["brows"]) + P(oval(*h["nose"]), 2.4)
    if h["mouth"]:
        o += P(h["mouth"], 4.2)
    if h["grin"]:
        o += f'<path d="{h["grin"][0]}" fill="{ACCENT}"/><path d="{h["grin"][1]}" fill="#FFFFFF"/>' + P(h["grin"][0], 2.8)
    return f'<g transform="translate({x - cx * k:g} {y - cy * k:g}) scale({k:g})">{o}</g>'


# --- hand library: cartoon hands in v9 proportion. Local coords: right hand, wrist at (0, 0), fingers up (-y),
# thumb on the left (-x). place with hand(pose, x, y, deg, k, flip); "grip" has a back part (drawn behind the held
# object) and a front part (the thumb, drawn over it).

def cap(x1, y1, x2, y2, w, lw):
    """An outlined finger: round-ended capsule from (x1, y1) to (x2, y2)."""
    d = f"M{x1:g} {y1:g} L{x2:g} {y2:g}"
    st = 'fill="none" stroke-linecap="round"'
    return f'<path d="{d}" {st} stroke="{INK}" stroke-width="{w + 2 * lw:g}"/><path d="{d}" {st} stroke="{SKIN}" stroke-width="{w:g}"/>'


def palm(d, edge, lw):
    """Palm: ochre fill on the whole shape, pen only on `edge` (left open where fingers join)."""
    return f'<path d="{d}" fill="{SKIN}"/>' + pen(edge, lw)


def hand_parts(pose, lw):
    if HANDS == "nub":      # no fingers: a round end on the sleeve, like the stick figures
        d = circ(0, -16, 20)
        o = f'<path d="{d}" fill="{SKIN}"/>' + pen(d, lw)
        return ("", o) if pose == "grip" else (o, "")
    fingers = lambda tips: "".join(cap(x, -38, tx, ty, 12, lw) for x, (tx, ty) in zip((-15, -5, 5, 15), tips))
    if pose == "open":      # palm out, fingers a little spread
        return (cap(-18, -14, -38, -40, 13, lw) + fingers([(-21, -80), (-6, -88), (8, -86), (22, -76)])
                + palm("M-22 2 L-24 -38 Q-24 -50 -12 -50 L14 -50 Q24 -50 24 -38 L22 2 Z", "M-22 2 L-24 -38 Q-24 -48 -18 -50 M20 -50 Q24 -48 24 -38 L22 2", lw), "")
    if pose == "fist":      # knuckles up, thumb across the front
        d = "M-20 2 L-22 -26 Q-22 -36 -14 -36 Q-9 -44 -4 -36 Q1 -44 6 -36 Q11 -44 16 -36 Q22 -36 22 -26 L20 2 Z"
        return (palm(d, d, lw) + fine("M-4 -36 L-4 -24 M6 -36 L6 -24 M-14 -36 L-14 -26", lw * 0.6) + cap(-18, -12, 6, -20, 12, lw), "")
    if pose == "point":     # fist with the index finger out
        d = "M-20 2 L-22 -26 Q-22 -36 -12 -36 L16 -36 Q22 -36 22 -26 L20 2 Z"
        return (cap(-10, -30, -10, -86, 12, lw) + palm(d, "M-16 -36 Q-22 -36 -22 -26 L-20 2 M20 2 L22 -26 Q22 -36 -4 -36", lw)
                + fine("M6 -36 L6 -24", lw * 0.6) + cap(-18, -12, 6, -20, 12, lw), "")
    if pose == "grip":      # holds an edge: knuckles behind the object, thumb over its front
        d = "M-20 2 L-22 -30 Q-22 -48 -6 -50 L14 -50 Q24 -48 24 -32 L20 2 Z"
        return (palm(d, d, lw) + fine("M2 -50 L4 -40 M13 -50 L14 -40", lw * 0.6), cap(-16, -22, -4, -64, 13, lw))
    raise ValueError(pose)


def hand(pose, x, y, deg, k=1.3, flip=False, part=None):
    back, front = hand_parts(pose, 3.2 / k)
    body = {"back": back, "front": front}.get(part, back + front)
    return f'<g transform="translate({x:g} {y:g}) rotate({deg:g}) scale({k:g})' + (' scale(-1 1)' if flip else '') + f'">{body}</g>'


def group(gid, body, rig=""):
    return f'  <g id="{gid}"{rig} filter="url(#ink)">{body}</g>\n'


def rig(px, py, deg, freq, shape="sine", phase=0):
    return f' data-pivot="{px},{py}" data-deg="{deg}" data-freq="{freq}"' + (f' data-phase="{phase}"' if phase else "") + f' data-shape="{shape}"'


HAIR = {
    "cap": "M-120 -25 Q-125 -135 -5 -137 Q115 -135 123 -35 Q75 -85 0 -75 Q-75 -70 -120 -25Z",
    "side": "M-124 -10 Q-130 -132 0 -138 Q122 -134 126 -10 Q118 -60 70 -78 Q30 -50 -30 -84 Q-96 -76 -124 -10Z",
    "long": "M-132 80 Q-148 -132 0 -140 Q148 -132 132 80 Q120 0 104 -50 Q60 -86 0 -84 Q-60 -86 -104 -50 Q-120 0 -132 80Z",
    "bald": "M-126 10 Q-132 -30 -114 -52 L-100 -20 Q-108 0 -126 10Z M126 10 Q132 -30 114 -52 L100 -20 Q108 0 126 10Z",
}
BROWS = {"neutral": ["M-68 -40 L-18 -42", "M18 -42 L68 -40"], "up": ["M-68 -50 Q-44 -62 -18 -54", "M18 -54 Q44 -62 68 -50"],
         "calm": ["M-66 -42 L-20 -46", "M20 -46 L66 -42"], "doubt": ["M-68 -36 L-18 -30", "M18 -46 L68 -58"]}


def face(x, y, k=0.62, hair="cap", brows="neutral", mouth="smile", look=0, down=0, glasses=False):
    """A v9-style face for anyone: round head, white eyes, bar brows, oval nose. Local v9 units (head radius 125), centered on (x, y)."""
    CLIPS[0] += 1
    P = lambda d, w=3.2: pen(d, w / k)
    ear = (-120, 18) if look >= 0 else (120, 18)
    head = circ(0, 0, 125)
    o = (f'<path d="{circ(*ear, 24)}" fill="{SKIN}" transform="translate({7 / k:g} {5 / k:g})"/><path d="{head}" fill="{SKIN}" transform="translate({7 / k:g} {5 / k:g})"/>'
         + P(circ(*ear, 24)) + f'<path d="{head}" fill="{SKIN}"/>'
         + f'<clipPath id="fc{CLIPS[0]}"><path d="{head}"/></clipPath><g clip-path="url(#fc{CLIPS[0]})">{hatch(40, -60, 9, 11, 120, 0.35, 2.2 / k)}</g>' + P(head))
    hd = HAIR.get(hair, "")
    if hair == "curly":
        hd = " ".join(circ(round(108 * __import__("math").cos(a)), round(-20 + 112 * __import__("math").sin(a)), 30) for a in [3.4 + i * 0.32 for i in range(9)])
    if hair == "bun":
        hd = HAIR["cap"] + " " + circ(0, -150, 42)
    o += f'<path d="{hd}" fill="{FILL}"/><path d="{hd}" fill="url(#hair)"/>' + P(hd)
    for ex in (-42, 43):
        o += f'<path d="{oval(ex, 5, 24, 24)}" fill="#FFFFFF"/>' + P(oval(ex, 5, 24, 24), 2.6) + f'<circle cx="{ex + look * 10}" cy="{8 + down * 9}" r="10" fill="{INK}"/>'
        if down:    # lowered lids when reading
            o += f'<rect x="{ex - 26}" y="-22" width="52" height="24" fill="{SKIN}"/>' + P(f"M{ex - 24} 2 Q{ex} -2 {ex + 24} 2", 2.6)
        if glasses:
            o += P(circ(ex, 5, 36), 2.6)
    if glasses:
        o += P("M-6 2 L7 2", 2.6) + P("M-78 0 L-114 -4" if look >= 0 else "M79 0 L114 -4", 2.6)
    o += "".join(P(b, 6) for b in BROWS[brows]) + P(oval(look * 14, 40, 14, 11), 2.4)
    if mouth == "smile":
        o += P("M-34 72 Q4 98 42 72", 4.2)
    elif mouth == "flat":
        o += P("M-24 82 L32 80", 4.2)
    elif mouth == "small":
        o += P("M-14 80 Q4 88 22 80", 4)
    elif mouth == "o":
        o += f'<path d="{oval(4, 84, 12, 15)}" fill="{INK}"/>'
    elif mouth == "grin":
        g = "M-67 64 Q-20 50 43 60 Q29 114 -17 116 Q-57 112 -67 64Z"
        o += f'<path d="{g}" fill="{ACCENT}"/><path d="M-63 66 Q-20 53 39 62 L36 76 Q-19 68 -60 80Z" fill="#FFFFFF"/>' + P(g, 2.8)
    return f'<g transform="translate({x:g} {y:g}) scale({k:g})">{o}</g>'


# --- bodies, in the founder's coordinates (feet at y 962, body center x ~760, shoulders (690, 372) and (824, 370)) ---

BODY_FILL = ("M724 350 Q696 352 684 376 Q676 400 680 440 Q686 490 694 520 Q690 560 692 604 Q684 690 690 770 Q684 850 664 930 L708 930 "
             "Q722 850 740 770 Q748 690 766 630 Q790 690 796 770 Q812 850 830 930 L870 930 Q850 850 838 770 Q840 690 828 604 "
             "Q826 560 818 520 Q822 490 828 450 Q834 400 824 370 Q806 350 772 348 Z")


def body(top="jacket"):
    """Torso, legs and shoes. top: jacket (hood, open neck, zip, pockets) | sweater (crew neck) | shirt (collar, buttons)."""
    o = (fill(BODY_FILL)
         + denim("M694 610 Q684 690 690 770 Q684 850 664 930 L708 930 Q722 850 740 770 Q748 690 756 616 Z")
         + denim("M778 616 Q790 690 796 770 Q812 850 830 930 L870 930 Q850 850 838 770 Q840 690 826 610 Z")
         + pen("M724 350 Q696 352 684 376 Q676 400 680 440 Q686 490 694 520 Q690 560 692 604")
         + pen("M772 348 Q806 350 824 370 Q834 400 828 450 Q822 490 818 520 Q826 560 828 604"))
    if top == "jacket":
        o += (pen("M712 354 Q746 382 786 350", 2.8) + fine("M718 360 Q748 388 780 358")
              + pen("M738 366 Q738 420 752 470") + pen("M766 366 Q768 420 752 470")
              + pen("M740 366 Q752 380 764 366", 2.4) + fine("M752 474 L754 600", 1.4)
              + pen("M702 530 L726 560", 2.6) + pen("M808 532 L796 562", 2.6))
    elif top == "sweater":
        o += pen("M724 352 Q748 372 772 350", 2.8) + fine("M728 360 Q748 378 768 358") + fine(" ".join(f"M{x} 590 l1 14" for x in range(700, 822, 9)), 1.4)
    elif top == "shirt":
        o += (pen("M724 350 L742 380 L750 362 L758 380 L774 348", 2.6) + fine("M750 384 L752 600", 1.4)
              + "".join(f'<circle cx="{751 + (y - 400) * 0.005:.0f}" cy="{y}" r="{3 * LW:g}" fill="{INK}"/>' for y in range(410, 600, 40))
              + pen("M790 420 L816 420 L814 448 L792 448 Z", 2))
    o += (pen("M692 604 Q760 616 828 604")
          + fine("M690 452 Q700 470 694 492 M820 456 Q812 474 818 494") + hatch(796, 380, 4, 8, 210, 0.04)
          + pen("M694 610 Q684 690 690 770 Q684 850 664 930") + pen("M756 616 Q748 690 740 770 Q722 850 708 930")
          + pen("M778 616 Q790 690 796 770 Q812 850 830 930") + pen("M826 610 Q840 690 838 770 Q850 850 870 930")
          + fine("M694 764 Q714 776 738 764 M798 766 Q818 778 836 766 M712 790 l4 14 M816 792 l4 14") + hatch(842, 640, 3, 7, 240, 0.1)
          + hatch(724, 640, 3, 7, 110, -0.05)
          + pen("M664 926 Q628 936 630 956 Q632 964 650 964 L718 964 Q726 950 708 928") + fine("M636 952 L716 954 M676 934 l6 8 M688 932 l6 8")
          + pen("M830 926 Q818 954 832 964 L906 964 Q912 946 872 928") + fine("M832 952 L904 954 M848 934 l6 8 M860 932 l6 8"))
    return o


def neck():
    return fill("M722 318 L770 314 L772 350 L720 352 Z").replace(FILL, SKIN) + pen("M726 318 Q728 336 724 352") + pen("M766 314 Q768 332 772 348") + hatch(752, 326, 3, 6, 18, 0.2)


def limbfill(d, w=30):
    """Ochre along a limb, in register, so the sleeve hides the body lines behind it."""
    return f'<path d="{d}" fill="none" stroke="{FILL}" stroke-width="{w}" stroke-linecap="round"/>'


def arm_down(side):
    if side == "near":
        return (blob("M700 386 Q680 450 678 540", 40) + limbfill("M700 390 Q682 450 680 540")
                + pen("M688 368 Q664 420 662 480 Q660 520 664 556") + pen("M712 404 Q698 452 694 500 Q692 530 694 552") + hand("fist", 680, 552, 180, 1.0))
    return (blob("M816 386 Q838 450 840 540", 40) + limbfill("M816 390 Q836 450 840 540")
            + pen("M828 366 Q852 420 856 480 Q858 520 852 556") + pen("M806 404 Q820 452 824 500 Q826 530 824 552") + hand("fist", 840, 552, 180, 1.0, flip=True))


def arm_gesture():
    """Near arm up at chest height, open palm toward the left."""
    return (blob("M700 388 Q660 440 652 470 Q620 440 596 420", 40) + limbfill("M700 392 Q664 440 654 470 Q624 446 600 424")
            + pen("M690 372 Q656 410 640 460") + pen("M712 404 Q682 442 666 482")
            + pen("M640 460 Q612 440 592 410") + pen("M666 482 Q632 462 606 430") + hand("open", 598, 418, -50, 1.0))


class place:
    """Scale content drawn in founder coordinates to stand at (cx, feet y) with scale k; sets LW so pen weight holds."""
    def __init__(self, cx, fy, k, weight=1.0):
        self.k, self.dx, self.dy, self.weight = k, cx - 760 * k, fy - 962 * k, weight
    def __enter__(self):
        global LW
        self.old, LW = LW, self.weight / self.k
        return self
    def __exit__(self, *a):
        global LW
        LW = self.old
    def wrap(self, body):
        return f'<g transform="translate({self.dx:g} {self.dy:g}) scale({self.k:g})">{body}</g>'
    def pt(self, x, y):
        return round(self.dx + x * self.k, 1), round(self.dy + y * self.k, 1)


def person(cx, fy, k, top="sweater", arms="down", weight=1.0, **face_kw):
    with place(cx, fy, k, weight) as P:
        o = body(top) + neck() + (arm_gesture() if arms == "gesture" else arm_down("near")) + arm_down("far") + face(752, 240, **face_kw)
        return P.wrap(o)


WASH_D = ("M180 380 Q150 220 330 170 Q470 120 600 190 Q760 110 900 200 Q1010 290 960 470 Q1020 640 940 800 "
          "Q900 930 720 950 L260 950 Q130 900 150 720 Q100 560 180 380 Z")


def wash():
    """Background: a cream wash with a faint ochre copy off register; sways about the frame center."""
    return group("wash", f'<path d="{WASH_D}" fill="{FILL_BG}"/><path d="{WASH_D}" fill="{FILL}" opacity="0.18" transform="translate(9 6)"/>', rig(560, 560, 3, 0.25))


FRAME = {}   # per-scene crop (x, y, size); Cam prefers the full wide frame (2026-10-26)


def zoom(name):
    """data-zoom that fills the frame with FRAME[name]; the floor is not static then, so it scales too."""
    if name not in FRAME:
        return ""
    x, y, size = FRAME[name]
    z = 1080 / size
    return f' data-zoom="{z:.4f},{-x * z:.1f},{-y * z:.1f}"'


def root(name):
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
            f'     data-bg="{BG}" data-variants="3" data-border="0" data-jitter="0" data-shadow="0"{zoom(name)}>\n'
            f'  <!-- Rubens-lite look, {name}: generated by tools/rubens_scene.py -->\n'
            '  <defs><filter id="ink" filterUnits="userSpaceOnUse" x="-100" y="-100" width="1300" height="1300">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="1"/>'
            '<feDisplacementMap in="SourceGraphic" scale="3" xChannelSelector="R" yChannelSelector="G"/></filter>'
            f'<pattern id="denim" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(70)"><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1.3" opacity="0.8"/></pattern>'
            f'<pattern id="hair" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><line x1="0" y1="0" x2="0" y2="5" stroke="{INK}" stroke-width="2.2"/></pattern></defs>\n'] \
        + ([wash()] if WASH else []) + [group("floor", pen("M40 966 Q300 960 560 964 T1040 962", 2.6) + hatch(150, 968, 14, 18, 10, 1.2) + hatch(620, 968, 16, 18, 10, 1.2), "" if name in FRAME else ' data-static="1"')]


def posed(x, y, lean, bend):
    """Where (x, y) lands after the upper body rotates by `bend` about the hip and the figure shears by `lean` about the feet."""
    a, (hx, hy) = math.radians(bend), HIP
    x, y = hx + (x - hx) * math.cos(a) - (y - hy) * math.sin(a), hy + (x - hx) * math.sin(a) + (y - hy) * math.cos(a)
    return round(x + math.tan(math.radians(lean)) * (y - 962), 1), round(y, 1)


def careless_founder(lean=0, bend=0, head=0, arm2="open"):
    """The pitching founder: open jacket, tablet pushed forward, other palm open.
    lean/bend/head (degrees) give a posture; arm2="down" lets the other arm hang. Pivots follow the posture."""
    T = f"translate(0 962) skewX({lean}) translate(0 -962)"
    U = f"{T} rotate({bend} {HIP[0]} {HIP[1]})"

    def part(gid, body_, px, py, *r, extra=""):
        x, y = posed(px, py, lean, bend)
        return group(gid, f'<g transform="{U}{extra}">{body_}</g>', rig(x, y, *r))

    b = body("jacket")
    g = [group("founder", f'<g transform="{T}"><clipPath id="flo"><rect x="0" y="604" width="1080" height="476"/></clipPath><g clip-path="url(#flo)">{b}</g></g>'
               f'<g transform="{U}"><clipPath id="fup"><rect x="0" y="0" width="1080" height="612"/></clipPath><g clip-path="url(#fup)">{b}</g></g>')]
    g.append(part("arm2", blob("M816 372 Q866 420 870 470 Q890 430 902 384", 46)
                   + pen("M812 368 Q862 410 880 470") + pen("M806 402 Q840 440 852 476")
                   + pen("M880 470 Q902 430 914 396") + pen("M852 476 Q872 432 886 400")
                   + hatch(858, 430, 3, 7, 34, 0.2) + pen("M884 400 L912 400", 2.6) + hand("open", 900, 402, 22, 1.3), 816, 372, 7, 1.1, "sine", 0.25))
    if arm2 == "down":
        g[-1] = part("arm2", arm_down("far"), 816, 372, 2, 0.6, "sine", 0.25)
    tab = (f'<g transform="rotate(-8 480 345)"><rect x="420" y="260" width="122" height="170" rx="10" fill="#FFFFFF"/>'
           + pen("M430 260 L532 260 Q542 260 542 270 L542 420 Q542 430 532 430 L430 430 Q420 430 420 420 L420 270 Q420 260 430 260 Z", 3.4)
           + fine("M432 274 L530 274 L530 414 L432 414 Z", 1.4)
           + f'<rect x="446" y="368" width="18" height="36" fill="{ACCENT}"/><rect x="472" y="344" width="18" height="60" fill="{ACCENT}"/>'
           f'<rect x="498" y="304" width="18" height="100" fill="{ACCENT}"/>' + fine("M440 406 L522 406", 2.4) + '</g>')
    g.append(part("arm", blob("M704 382 Q660 420 632 452 Q600 420 570 390", 46)
                   + pen("M704 364 Q660 400 622 436") + pen("M708 402 Q672 440 642 472")
                   + pen("M622 436 Q590 410 562 378") + pen("M642 472 Q604 432 576 402")
                   + pen("M564 382 L582 404", 2.6) + hatch(640, 444, 4, 7, 26, 0.3) + hand("grip", 578, 394, -78, 1.3, part="back") + tab
                   + hand("grip", 578, 394, -78, 1.3, part="front"), 704, 382, 7, 1.1, "snap"))
    g.append(part("founder-head", neck() + v9_head("founder", 745, 240), 746, 340, -5, 1.1, "snap", extra=f" rotate({head} 746 340)"))
    return g


def pitch():
    s = root("pitch")
    # chair: plain modern chair, seen from the side
    s.append(group("chair", pen("M150 386 Q160 520 172 640 L402 640 M176 658 L168 962 M394 658 L400 962 M160 640 L410 642 L408 660 L172 660 Z")
                   + hatch(178, 646, 12, 19, 10, 0.8)))
    # the skeptic: older man in a sweater, leaning back, arms and legs crossed
    body = (fill("M268 402 Q240 410 226 432 Q220 500 236 560 Q246 610 262 646 L494 640 L486 588 L384 598 Q386 560 388 520 Q394 460 362 418 Q334 404 268 402 Z")
            + fill("M420 640 L474 636 Q480 790 474 932 L426 934 Q424 790 420 640 Z")
            + denim("M386 600 Q440 584 488 588 L494 640 Q380 652 262 646 Q300 630 386 600 Z") + denim("M420 640 L470 640 Q480 790 474 930 L428 930 Q424 790 420 640 Z")
            + pen("M268 402 Q238 408 226 434 Q216 500 236 560 Q248 612 262 646")          # slumped back
            + pen("M264 404 Q300 422 338 402", 2.8) + fine("M270 412 Q300 428 332 410")    # crew neck
            + pen("M336 404 Q368 414 382 448 Q396 488 390 526")                           # near shoulder and upper arm
            + pen("M352 442 Q364 480 362 508") + fine("M372 500 q8 6 10 16 M366 512 q8 2 12 10")
            + pen("M386 506 Q330 496 258 494") + pen("M392 530 Q330 530 252 526")          # lower forearm
            + pen("M232 488 Q290 470 344 452") + pen("M238 518 Q296 500 350 484")          # upper forearm, on top
            + pen("M238 518 Q220 506 232 488") + fine("M262 486 q4 10 0 22 M280 480 q4 10 0 22")   # far elbow, sleeve folds
            + hand("fist", 346, 468, 78, 1.15)
            + hatch(300, 532, 7, 9, 22, 0.2) + hatch(362, 420, 3, 7, 50, 0.15) + hatch(240, 440, 3, 7, 90, 0.05)
            + pen("M258 600 Q320 614 388 598", 2.6) + fine(" ".join(f"M{x} {604 + (x - 258) * -0.02:.0f} l1 14" for x in range(266, 386, 9)), 1.4)  # ribbed hem
            + pen("M386 600 Q440 584 488 588") + pen("M262 646 Q380 652 468 640")          # thigh
            + fine("M410 598 Q426 616 424 640 M446 594 Q458 618 452 640") + hatch(300, 630, 16, 10, 14, 0.4)
            + pen("M420 646 Q412 720 424 800 Q430 870 428 930") + pen("M470 640 Q484 700 478 780 Q472 860 474 930")  # support leg, calf
            + hatch(458, 690, 3, 6, 190, 0.02) + fine("M432 812 Q448 822 468 810 M446 660 L448 900", 1.4)
            + pen("M424 928 Q410 948 418 962 L506 962 Q514 950 496 940 Q480 934 474 928") + fine("M424 954 L504 954"))   # loafer
    s.append(group("customer", body))
    leg = (blob("M490 610 Q530 680 560 756", 44) + denim("M480 584 Q522 630 550 692 Q566 730 566 746 L546 758 Q544 744 536 722 Q520 680 494 630 Z")
           + pen("M480 584 Q522 630 550 692 Q566 730 566 746") + pen("M494 630 Q520 680 536 722 Q544 744 546 758")  # shin, calf
           + pen("M480 584 Q500 600 494 630", 2.6) + hatch(504, 650, 5, 7, 70, 0.4) + fine("M512 640 L548 734", 1.4)
           + pen("M546 754 Q550 792 592 790 Q620 784 606 764 L566 744") + fine("M558 776 L600 776"))
    s.append(group("customer-foot", leg, rig(488, 604, -10, 2.2, "snap")))
    head = (fill("M272 372 L328 368 L332 404 L270 408 Z")
            + pen("M272 374 Q272 392 268 408") + pen("M326 370 Q330 390 334 404") + hatch(276, 382, 6, 8, 18, 0.3)
            + v9_head("customer", 296, 296))
    s.append(group("customer-head", head, rig(300, 392, 4, 0.4)))

    s += careless_founder(lean=-2, bend=5, head=-9, arm2="down")   # pose 6: hip shift, casual
    return "".join(s) + "</svg>\n"


def crowd():
    """'he talked to 30 customers': the pitching founder in front of three pale rows of ten."""
    rnd = random.Random(30)
    s = root("crowd")
    s.append('<defs><filter id="pale"><feComponentTransfer>' + "".join(
        f'<feFunc{c} type="linear" slope="0.45" intercept="{0.55 * int(BG[i:i + 2], 16) / 255:.3f}"/>' for c, i in (("R", 1), ("G", 3), ("B", 5))) + '</feComponentTransfer></filter></defs>\n')
    for r, (fy, k, x0) in enumerate([(600, 0.36, 30), (690, 0.42, 0), (790, 0.48, 20)]):
        for half in (0, 1):
            xs = [x0 + 54 + 108 * i for i in range(half * 5, half * 5 + 5)]
            ppl = "".join(person(x, fy, k, rnd.choice(["sweater", "shirt", "jacket"]), weight=0.75,
                                 hair=rnd.choice(["cap", "side", "long", "bald", "curly", "bun"]), brows=rnd.choice(["neutral", "up", "calm"]),
                                 mouth=rnd.choice(["smile", "smile", "flat", "o", "small"]), look=1 if x < 700 else -1) for x in xs)
            s.append(group(f"crowd-{r}{half}", f'<g filter="url(#pale)">{ppl}</g>', rig(sum(xs) / 5, fy, rnd.choice([-1.5, 1.5]), rnd.choice([0.5, 0.7, 0.9]), phase=round(rnd.random(), 2))))
    s += careless_founder()
    return "".join(s) + "</svg>\n"


def three():
    """'only talked to three customers': the careful founder listens and writes; three people."""
    s = root("three")
    with place(250, 962, 0.95) as P:
        board = (f'<g transform="rotate(8 835 485)"><rect x="790" y="420" width="90" height="130" rx="6" fill="#FFFFFF"/>'
                 + pen("M796 420 L874 420 Q880 420 880 426 L880 544 Q880 550 874 550 L796 550 Q790 550 790 544 L790 426 Q790 420 796 420 Z", 3)
                 + f'<rect x="818" y="410" width="34" height="16" rx="4" fill="{ACCENT}"/>' + pen("M818 410 L852 410 L852 426 L818 426 Z", 2)
                 + fine("M802 452 L866 452 M802 474 L860 474 M802 496 L866 496 M802 518 L846 518", 1.6) + '</g>')
        hold = (blob("M818 386 Q850 440 858 500 Q852 530 838 556", 40) + limbfill("M818 390 Q848 440 854 500 Q850 530 836 556")
                + pen("M826 370 Q856 420 866 500") + pen("M806 404 Q830 450 842 500") + pen("M866 500 Q862 540 848 562") + pen("M842 500 Q836 530 826 556"))
        b = P.wrap(body("shirt") + hold + hand("grip", 836, 560, 0, 1.0, part="back") + board + hand("grip", 836, 560, 0, 1.0, part="front"))
        s.append(group("founder2", b))
        writer = (blob("M700 388 Q680 440 692 480 Q740 496 786 470", 40) + limbfill("M702 392 Q684 440 696 480 Q740 492 784 468")
                  + pen("M690 372 Q668 430 688 484") + pen("M712 404 Q700 440 708 466")
                  + pen("M688 484 Q740 504 790 478") + pen("M708 466 Q744 476 784 458")
                  + hand("fist", 792, 470, 70, 1.0) + pen("M800 450 L824 414", 6) + pen("M824 414 L830 404", 3))
        s.append(group("pen", P.wrap(writer), rig(*P.pt(690, 372), -5, 2.4, "snap")))
        s.append(group("head2", P.wrap(neck() + face(752, 240, hair="side", brows="calm", mouth="small", look=1, glasses=True)), rig(*P.pt(748, 350), 4, 0.9)))
    for i, (cx, kw) in enumerate([(640, dict(arms="gesture", hair="long", mouth="o", brows="up", top="sweater")),
                                  (800, dict(hair="cap", mouth="flat", brows="neutral", top="shirt")),
                                  (960, dict(hair="curly", mouth="smile", brows="neutral", top="sweater"))]):
        s.append(group(f"cust{i}", person(cx, 962, 0.8, look=-1, **kw), rig(cx, 962, [-1.5, 2.0, 1.5][i], [1.1, 0.6, 0.5][i], phase=i * 0.3)))
    return "".join(s) + "</svg>\n"


def reading():
    """'they read The Mom Test': the careful founder holds an open book up, studying."""
    s = root("reading")
    with place(540, 962, 1.0) as P:
        arms = (blob("M700 388 Q656 430 640 480 Q632 520 636 550", 40) + limbfill("M700 390 Q658 432 642 482 Q634 520 638 550")
                + pen("M690 368 Q646 410 626 470 Q616 520 622 556") + pen("M712 404 Q676 440 660 484 Q652 520 652 548")
                + blob("M820 388 Q864 430 880 480 Q888 520 884 550", 40) + limbfill("M820 390 Q862 432 878 482 Q886 520 882 550")
                + pen("M830 368 Q874 410 894 470 Q904 520 898 556") + pen("M808 404 Q844 440 860 484 Q868 520 868 548")
                + fine("M640 470 q10 6 14 18 M880 470 q-10 6 -14 18"))
        book = (f'<path d="M760 512 L630 488 L630 642 L760 666 L890 642 L890 488 Z" fill="{ACCENT}"/>' + pen("M760 512 L630 488 L630 642 L760 666 L890 642 L890 488 Z", 3)
                + f'<path d="M760 500 L642 478 L642 630 L760 654 Z" fill="#FFFFFF"/>' + pen("M760 500 L642 478 L642 630 L760 654 Z", 2.6)
                + f'<path d="M760 500 L878 478 L878 630 L760 654 Z" fill="#FFFFFF"/>' + pen("M760 500 L878 478 L878 630 L760 654 Z", 2.6)
                + fine("M660 504 L744 520 M660 528 L738 543 M660 552 L744 567 M660 576 L730 590 M776 520 L860 504 M776 543 L854 528 M776 567 L860 552", 1.6))
        s.append(group("founder2", P.wrap(body("sweater") + arms + hand("grip", 626, 566, 90, 1.0, part="back") + hand("grip", 894, 566, -90, 1.0, flip=True, part="back")
                                         + book + hand("grip", 626, 566, 90, 1.0, part="front") + hand("grip", 894, 566, -90, 1.0, flip=True, part="front"))))
        page = f'<path d="M760 500 L846 486 L846 636 L760 654 Z" fill="#FFFFFF"/>' + pen("M760 500 L846 486 L846 636 L760 654 Z", 2.6) + fine("M776 520 L830 510 M776 543 L826 534", 1.6)
        s.append(group("page", P.wrap(page), rig(*P.pt(760, 576), -22, 1.0, "snap")))
        s.append(group("head2", P.wrap(neck() + face(752, 240, hair="side", brows="calm", mouth="small", down=1, glasses=True)), rig(*P.pt(748, 350), 3, 0.5)))
    return "".join(s) + "</svg>\n"


def pile():
    """'terrible interviews, but at a high volume': the careless founder tops up a tall, leaning stack of interview notes."""
    rnd = random.Random(12)
    s = root("pile")
    sheets = ""
    for i in range(31):
        y, x = 940 - i * 22, 250 + rnd.uniform(-12, 12) + i * 1.6
        sheets += (f'<g transform="rotate({rnd.uniform(-3, 3):.1f} {x + 75:.1f} {y + 9})"><rect x="{x:.1f}" y="{y}" width="150" height="18" rx="2" fill="#FFFFFF"/>'
                   + pen(f"M{x:.1f} {y} l150 0 l0 18 l-150 0 Z", 2.2) + "</g>")
        if i % 5 == 2:
            sheets += f'<rect x="{x + 132:.1f}" y="{y + 3}" width="16" height="12" fill="{ACCENT}"/>'
    s.append(group("stack", sheets + hatch(256, 942, 9, 16, 12, -0.6), rig(325, 960, 1.2, 0.5)))
    with place(630, 962, 1.0) as P:
        hip = (blob("M818 384 Q866 420 880 462 Q868 500 836 520", 40) + limbfill("M818 388 Q862 424 874 462 Q862 498 834 518")
               + pen("M828 368 Q870 410 884 460 Q878 500 836 524") + pen("M808 404 Q846 440 856 462 Q850 488 826 506") + hand("fist", 830, 520, -110, 1.0))
        s.append(group("founder", P.wrap(body("jacket") + hip)))
        note = (f'<g transform="rotate(-14 600 236)"><rect x="548" y="226" width="110" height="18" rx="2" fill="#FFFFFF"/>' + pen("M548 226 l110 0 l0 18 l-110 0 Z", 2.2)
                + f'<rect x="636" y="229" width="14" height="12" fill="{ACCENT}"/></g>')
        up = (blob("M700 384 Q656 330 624 298 Q608 282 600 268", 40) + limbfill("M700 388 Q658 334 626 300 Q612 286 602 272")
              + pen("M688 370 Q646 330 620 296 Q606 280 596 262") + pen("M712 398 Q664 350 636 316 Q622 298 610 280")
              + hand("grip", 602, 274, -40, 1.0, part="back") + note + hand("grip", 602, 274, -40, 1.0, part="front"))
        s.append(group("arm", P.wrap(up), rig(*P.pt(700, 380), -12, 1.2, "snap")))
        s.append(group("founder-head", P.wrap(neck() + v9_head("founder", 745, 240)), rig(*P.pt(746, 340), -4, 1.2, "snap")))
    return "".join(s) + "</svg>\n"


if __name__ == "__main__":
    for name, f in [("pitch", pitch), ("crowd", crowd), ("three", three), ("reading", reading), ("pile", pile)]:
        open(os.path.join(HERE, f"scenes/rubens-{name}.svg"), "w").write(f())
        print(f"wrote scenes/rubens-{name}.svg")
