"""Marker stick-figure style: the five talk-to-customers scenes -> scenes/stick-{pitch,crowd,three,reading,swimmer}.svg

usage: python3 tools/stick_scene.py
Look: outlined thin-tube limbs and bodies, oval heads, open mitten hands, solid black foot wedges,
dot eyes and arc mouths, black on warm white, one orange accent per scene. Lines boil through the
#ink filter (svgpieces re-seeds its turbulence per variant). Every scene uses data-zoom 1.2,-90,-108,
so the visible area in scene units is x 75..975, y 90..990; the floor line is static (not zoomed).
Cast: the careless founder (no glasses; pitch, crowd, swimmer) and the careful founder (round glasses;
three, reading). fig() draws any other person at scale s (s=2.3 is about main-character size).
"""
import math
import os, random

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK, PAPER, ORANGE, BG = "#141414", "#FFFFFF", "#ED7239", "#FBF8F2"
LOOK = "stick"      # "stick" = marker tubes on warm white; "sketch" = thin pen line, shirt box, speckled paper; "pictogram" = solid icon figures
GREY = "#A39E96"
CLIPS = 0
FILL, FILL_BG = "#E3A84B", "#F2DDB6"     # ochre look: flat fill behind people (main, background crowd)


def set_look(look):
    """Switch every helper to a look. sketch: single thin navy line, no hands or feet, shirt boxes, grey paper.
    pictogram: solid black limbs and heads, no faces, hands or feet; a paper-colored gap separates overlapping limbs."""
    global LOOK, INK, PAPER, BG, GREY, ORANGE
    LOOK = look
    ORANGE = "#B5452B" if look == "ochre" else "#ED7239"
    INK, PAPER, BG, GREY = {"stick": ("#141414", "#FFFFFF", "#FBF8F2", "#A39E96"), "sketch": ("#1F3647", "#EDEFEC", "#EDEFEC", "#A3AEB6"),
                            "pictogram": ("#141414", "#FFFFFF", "#FBF8F2", "#BDB8B0"),
                            "ochre": ("#2A2522", "#FFFFFF", "#FBFAF6", "#9C948C")}[look]
MITT = "M-9 16 L-11 -6 Q-11 -22 2 -22 Q14 -22 13 -6 L10 16"   # open mitten, local coords, fingers up, wrist open at the bottom
THUMB = "M-11 4 Q-24 2 -24 -12"
FOOT = "M-32 2 Q-30 -12 -10 -13 L20 -10 Q28 -4 24 4 Z"         # toe points left


def tube(d, w=10, line=6, ink=None, gap=False):
    if LOOK == "pictogram":
        W = (w + 2 * line) * 1.8
        under = f'<path d="{d}" fill="none" stroke="{BG}" stroke-width="{W + 16:g}" stroke-linecap="round" stroke-linejoin="round"/>' if gap else ""
        return under + f'<path d="{d}" fill="none" stroke="{ink or INK}" stroke-width="{W:g}" stroke-linecap="round" stroke-linejoin="round"/>'
    if LOOK == "ochre":     # outlined ochre limb, plus a loose fill a little off register
        f, W, lw = FILL_BG if ink else FILL, (w + 2 * line) * 0.85, max(1.6, line * 0.45)
        st = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
        return (f'<path d="{d}" {st} stroke="{f}" stroke-width="{W * 1.25:g}" transform="translate(5 4)"/>'
                f'<path d="{d}" {st} stroke="{ink or INK}" stroke-width="{W + 2 * lw:g}"/><path d="{d}" {st} stroke="{f}" stroke-width="{W:g}"/>')
    if LOOK in ("sketch", "ochre"):
        return f'<path d="{d}" fill="none" stroke="{ink or INK}" stroke-width="{max(2.2, line * 0.75):g}" stroke-linecap="round" stroke-linejoin="round"/>'
    return (f'<path d="{d}" fill="none" stroke="{ink or INK}" stroke-width="{w + 2 * line:g}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-width="{w:g}" stroke-linecap="round" stroke-linejoin="round"/>')


def line(d, w=6, ink=None):
    w = max(2.2, w * 0.6) if LOOK in ("sketch", "ochre") else w
    return f'<path d="{d}" fill="none" stroke="{ink or INK}" stroke-width="{w:g}" stroke-linecap="round" stroke-linejoin="round"/>'


def shape(d, fill=None, w=6, tf=""):
    fill = fill or PAPER
    w = w * 0.6 if LOOK in ("sketch", "ochre") else w
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{w:g}" stroke-linejoin="round"{f" transform={chr(34)}{tf}{chr(34)}" if tf else ""}/>'


def hand(x, y, deg, flip=False, k=1.5):
    if LOOK not in ("stick", "ochre"):
        return ""
    tf = f"translate({x:g} {y:g}) rotate({deg:g}) scale({k:g})" + (" scale(-1 1)" if flip else "")
    return shape(MITT, FILL if LOOK == "ochre" else None, tf=tf) + f'<path d="{THUMB}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" transform="{tf}"/>'


def foot(x, y, flip=False, k=1.4, ink=None):
    if LOOK not in ("stick", "ochre"):
        return ""
    return f'<path d="{FOOT}" fill="{ink or INK}" transform="translate({x:g} {y:g}) scale({k:g})' + (' scale(-1 1)' if flip else '') + '"/>'


def head(cx, cy, deg, rx=62, ry=56, w=7, ink=None, hair="curly"):
    if LOOK == "pictogram":     # solid head; the paper-colored rim makes the neck gap
        return f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}" fill="{ink or INK}" stroke="{BG}" stroke-width="{max(5, rx * 0.24):.1f}" transform="rotate({deg:g} {cx:g} {cy:g})"/>'
    w = w * 0.65 if LOOK in ("sketch", "ochre") else w
    if LOOK == "ochre":
        rot, f = f'rotate({deg:g} {cx:g} {cy:g})', FILL_BG if ink else FILL
        e = f'cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}"'
        o = f'<ellipse {e} fill="{f}" transform="translate(6 5) {rot}"/><ellipse {e} fill="{f}" stroke="{ink or INK}" stroke-width="{w:g}" transform="{rot}"/>'
        if ink:             # background people stay plain
            return o
        global CLIPS
        CLIPS += 1
        o += (f'<clipPath id="hc{CLIPS}"><ellipse {e} transform="{rot}"/></clipPath>'
              f'<ellipse cx="{cx + rx * 1.05:g}" cy="{cy + ry * 0.3:g}" rx="{rx * 0.75:g}" ry="{ry:g}" fill="url(#hatch)" clip-path="url(#hc{CLIPS})"/>')
        k = rx / 60
        pt = lambda deg_: (cx + rx * math.cos(math.radians(deg_)), cy + ry * math.sin(math.radians(deg_)))
        curl = lambda px, py: line(f"M{px:.0f} {py:.0f} q{-6 * k:.0f} {-16 * k:.0f} {9 * k:.0f} {-15 * k:.0f} q{12 * k:.0f} {4 * k:.0f} {3 * k:.0f} {14 * k:.0f}", 4.5)
        if hair == "curly":         # a row of curls along the crown
            o += "".join(curl(*pt(196 + i * 18.5)) for i in range(9))
        elif hair == "bald":        # tufts over the ears only
            o += "".join(curl(*pt(a)) for a in (168, 184, 200, 340, 356, 12))
        elif hair == "straight":    # a hatched cap with a fringe
            (lx, ly), (rx_, ry_) = pt(188), pt(352)
            cap = f"M{lx:.0f} {ly:.0f} A{rx:g} {ry:g} 0 0 1 {rx_:.0f} {ry_:.0f} Q{cx + rx * 0.2:.0f} {cy - ry * 0.62:.0f} {cx - rx * 0.3:.0f} {cy - ry * 0.5:.0f} Q{cx - rx * 0.7:.0f} {cy - ry * 0.4:.0f} {lx:.0f} {ly:.0f} Z"
            o += (f'<path d="{cap}" fill="{FILL}" stroke="{INK}" stroke-width="{w:g}" transform="translate(0 -4) {rot}"/>'
                  f'<path d="{cap}" fill="url(#hatch)" transform="translate(0 -4) {rot}"/>')
        return o
    return f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}" fill="{PAPER}" stroke="{ink or INK}" stroke-width="{w:g}" transform="rotate({deg:g} {cx:g} {cy:g})"/>'


def dot(x, y, r=7, ink=None):
    r = r * 0.6 if LOOK in ("sketch", "ochre") else r
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{ink or INK}"/>'


def ring(x, y, r, w=5, ink=None):
    w = w * 0.6 if LOOK in ("sketch", "ochre") else w
    ink = ink or (BG if LOOK == "pictogram" else INK)    # pictogram glasses are light rings on the solid head
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="none" stroke="{ink}" stroke-width="{w:g}"/>'


def box(top, bot, w, ink=None):
    """The shirt box of the sketch look, the solid torso of the pictogram look, nothing in the stick look."""
    (x1, y1), (x2, y2) = top, bot
    if LOOK == "pictogram":
        ex, ey = x2 + (x2 - x1) * 0.5, y2 + (y2 - y1) * 0.5
        return f'<path d="M{x1:g} {y1:g} L{ex:g} {ey:g}" fill="none" stroke="{ink or INK}" stroke-width="{w * 1.25:g}" stroke-linecap="round"/>'
    if LOOK == "ochre":     # shirt: outlined ochre, hatched shadow down one side, open collar
        f, bot = FILL_BG if ink else FILL, y2 + (y2 - y1) * 0.35
        shirt = f"M{x1 - w * 0.6:g} {y1:g} L{x1 + w * 0.6:g} {y1:g} L{x2 + w * 0.48:g} {bot:g} L{x2 - w * 0.48:g} {bot:g} Z"
        o = (f'<path d="{shirt}" fill="{f}" transform="translate(5 4)"/>'
             f'<path d="{shirt}" fill="{f}" stroke="{ink or INK}" stroke-width="{2.6 if not ink else 1.6}" stroke-linejoin="round"/>')
        if not ink:
            o += (f'<path d="M{x1 + w * 0.25:g} {y1 + 6:g} L{x1 + w * 0.56:g} {y1 + 6:g} L{x2 + w * 0.44:g} {bot - 4:g} L{x2 + w * 0.12:g} {bot - 4:g} Z" fill="url(#hatch)"/>'
                  + line(f"M{x1 - w * 0.22:g} {y1:g} L{x1:g} {y1 + w * 0.4:g} L{x1 + w * 0.22:g} {y1:g}", 5))
        return o
    if LOOK not in ("sketch", "ochre"):
        return ""
    quad = f"M{x1 - w / 2:g} {y1:g} L{x1 + w / 2:g} {y1:g} L{x2 + w / 2:g} {y2:g} L{x2 - w / 2:g} {y2:g} Z"
    under = f'<path d="{quad}" fill="{FILL_BG if ink else FILL}" transform="translate(5 4)"/>' if LOOK == "ochre" else ""
    return under + line(f"M{x1 - w / 2:g} {y1:g} L{x1 + w / 2:g} {y1:g} L{x2 + w / 2:g} {y2:g} L{x2 - w / 2:g} {y2:g} Z", 6.5, ink)


def paper():
    """Speckled paper (sketch look only), flattened into the background."""
    if LOOK != "sketch":
        return ""
    import random as _r
    rnd = _r.Random(7)
    flecks = "".join(f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.uniform(0.6, 1.8):.1f}" fill="#8E989E" opacity="{rnd.uniform(0.2, 0.6):.2f}"/>' for _ in range(260))
    grain = ('<filter id="papergrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>'
             '<feColorMatrix type="matrix" values="0 0 0 0 0.3  0 0 0 0 0.33  0 0 0 0 0.36  0 0 0 0.35 0"/></filter>')
    return f'  <g id="paper" data-static="1"><defs>{grain}</defs><rect x="-40" y="-40" width="1160" height="1160" fill="#fff" filter="url(#papergrain)" opacity="0.5"/>{flecks}</g>\n'


def group(gid, body, rig=""):
    return f'  <g id="{gid}"{rig} filter="url(#ink)">{body}</g>\n'


def rig(px, py, deg, freq, shape="sine", phase=0):
    return f' data-pivot="{px:g},{py:g}" data-deg="{deg:g}" data-freq="{freq:g}"' + (f' data-phase="{phase:g}"' if phase else "") + f' data-shape="{shape}"'


def root(name, floor=True):
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
         f'     data-bg="{BG}" data-variants="3" data-border="0" data-jitter="0" data-shadow="0" data-zoom="1.2,-90,-108">\n'
         f'  <!-- {LOOK} look, {name}: generated by tools/stick_scene.py -->\n'
         '  <defs><filter id="ink" filterUnits="userSpaceOnUse" x="-100" y="-100" width="1300" height="1300">'
         '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="1"/>'
         '<feDisplacementMap in="SourceGraphic" scale="4" xChannelSelector="R" yChannelSelector="G"/></filter>'
         f'<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="6" stroke="{INK}" stroke-width="1.4"/></pattern></defs>\n']
    s.append(paper())
    if floor:
        s.append(group("floor", line("M-20 932 Q300 926 540 930 T1100 928", 8), ' data-static="1"'))
    return s


def fig(x, y, s, mouth="smile", arms="down", look=0, glasses=False, ink=None):
    """Any extra person, standing, feet at (x, y). look shifts the eyes (+ = right). ink=grey for background people."""
    k = ink
    w, ln = 4.2 * s, 2.6 * s
    hy, sh, hip = y - 232 * s, y - 190 * s, y - 100 * s
    o = tube(f"M{x:g} {hip:g} L{x - 16 * s:g} {y - 4 * s:g}", w, ln, k) + tube(f"M{x:g} {hip:g} L{x + 16 * s:g} {y - 4 * s:g}", w, ln, k)
    o += foot(x - 18 * s, y, False, 0.55 * s, k) + foot(x + 18 * s, y, True, 0.55 * s, k)
    o += tube(f"M{x:g} {y - 208 * s:g} L{x:g} {hip:g}", w, ln, k) + box((x, y - 196 * s), (x, y - 140 * s), 21 * s, k)
    right = f"M{x:g} {sh:g} Q{x + 26 * s:g} {y - 150 * s:g} {x + 28 * s:g} {y - 112 * s:g}"
    left = f"M{x:g} {sh:g} Q{x - 26 * s:g} {y - 150 * s:g} {x - 28 * s:g} {y - 112 * s:g}"
    if arms == "gesture":       # left hand up, palm out, toward the left
        left = f"M{x:g} {sh:g} Q{x - 34 * s:g} {y - 150 * s:g} {x - 58 * s:g} {y - 176 * s:g}"
        o += tube(left, w, ln, k, True) + hand(x - 62 * s, y - 186 * s, -50, False, 0.55 * s) + tube(right, w, ln, k, True)
    else:
        o += tube(left, w, ln, k, True) + tube(right, w, ln, k, True)
    o += head(x, hy, 0, 26 * s, 24 * s, 2.8 * s, k, ("curly", "straight", "bald")[int(x / 150) % 3])
    if LOOK == "pictogram":
        return o
    ex, ey = 9 * s, hy - 3 * s
    o += dot(x - ex + look * s, ey, 2.8 * s, k) + dot(x + ex + look * s, ey, 2.8 * s, k)
    if glasses:
        o += ring(x - ex + look * s, ey, 8 * s, 2 * s, k) + ring(x + ex + look * s, ey, 8 * s, 2 * s, k)
    my = hy + 10 * s
    if mouth == "smile":
        o += line(f"M{x - 9 * s + look * s:g} {my:g} Q{x + look * s:g} {my + 8 * s:g} {x + 9 * s + look * s:g} {my:g}", 2.4 * s, k)
    elif mouth == "flat":
        o += line(f"M{x - 7 * s + look * s:g} {my + 2 * s:g} L{x + 7 * s + look * s:g} {my + 2 * s:g}", 2.4 * s, k)
    else:
        o += ring(x + look * s, my + 3 * s, 3.4 * s, 2.2 * s, k)
    return o


def careless_founder(arm_deg=7):
    """The pitching founder from the pitch scene: leans left, tablet out, other palm open."""
    tab = (f'<g transform="rotate(-8 495 415)"><rect x="430" y="330" width="130" height="170" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="8"/>'
           f'<rect x="452" y="430" width="20" height="44" fill="{ORANGE}"/><rect x="482" y="404" width="20" height="70" fill="{ORANGE}"/>'
           f'<rect x="512" y="366" width="20" height="108" fill="{ORANGE}"/>{line("M448 480 L544 480", 5)}</g>')
    return (group("founder", tube("M712 392 Q716 500 738 604") + box((714, 410), (724, 520), 66) + tube("M738 604 L690 842") + foot(686, 848)
                  + tube("M738 604 L800 842") + foot(800, 848))
            + group("arm2", tube("M722 424 Q790 450 806 486 Q830 452 846 418", gap=True) + hand(850, 404, 12, flip=True), rig(722, 424, 7, 1.1, phase=0.25))
            + group("arm", tube("M716 424 Q660 450 640 470 Q596 452 566 420", gap=True) + tab + hand(566, 412, -10), rig(716, 424, arm_deg, 1.1, "snap"))
            + group("founder-head", head(700, 330, 8) + line("M654 298 Q668 286 684 294", 7) + line("M698 292 Q714 282 730 292", 7)
                    + dot(670, 320) + dot(708, 318) + line("M652 350 Q684 382 722 348", 7), rig(712, 392, -5, 1.1, "snap")))


def careful_head(cx, cy, look=0, down=0):
    """The careful founder's head: round glasses, flat attentive brows, small closed mouth."""
    ex = (cx - 18 + look, cx + 18 + look)
    ey = cy - 6 + down
    return (head(cx, cy, 0, hair="straight") + "".join(ring(x, ey, 17, 6) for x in ex) + line(f"M{ex[0] + 17} {ey} L{ex[1] - 17} {ey}", 5)
            + dot(ex[0] + look / 3, ey + down / 3, 6) + dot(ex[1] + look / 3, ey + down / 3, 6)
            + line(f"M{ex[0] - 14} {ey - 30} L{ex[0] + 12} {ey - 32}", 7) + line(f"M{ex[1] - 12} {ey - 32} L{ex[1] + 14} {ey - 30}", 7)
            + line(f"M{cx - 10 + look} {cy + 30} Q{cx + look} {cy + 36} {cx + 10 + look} {cy + 30}", 6))


def pitch():
    s = root("pitch")
    s.append(group("chair", line("M168 470 L190 690 L372 690 M190 690 L182 864 M364 690 L372 864", 22 if LOOK == "pictogram" else 9)))
    # skeptic: leans back, arms crossed, crossed leg bounces
    s.append(group("customer", tube("M262 676 Q330 668 396 660 L392 852") + foot(390, 858) + tube("M286 480 Q276 580 264 676")
                   + box((284, 498), (276, 598), 62) + tube("M276 510 Q236 560 268 586 L318 572", gap=True) + tube("M296 512 Q332 556 300 584 L246 590", gap=True)))
    s.append(group("customer-foot", tube("M398 656 Q440 708 452 772", gap=True) + foot(462, 778, flip=True), rig(398, 656, -10, 2.2, "snap")))
    s.append(group("customer-head", head(282, 420, -10, hair="bald")
                   + line("M248 406 L276 408", 6) + dot(266, 418, 6) + line("M298 404 L326 402", 6) + dot(318, 414, 6)
                   + line("M246 394 L276 394", 7) + line("M300 376 Q316 362 334 370", 7)
                   + line("M264 454 L304 446", 6), rig(284, 476, 4, 0.4)))
    s.append(careless_founder())
    return "".join(s) + "</svg>\n"


def crowd():
    """'he talked to 30 customers': the pitching founder in front of three rows of ten."""
    rnd = random.Random(30)
    s = root("crowd")
    for r, (y, sc, x0) in enumerate([(560, 0.95, 110), (640, 1.1, 150), (730, 1.25, 100)]):
        for half in (0, 1):
            xs = [x0 + 96 * i for i in range(half * 5, half * 5 + 5)]
            body = "".join(fig(x, y, sc, rnd.choice(["smile", "smile", "flat", "o"]), "down", 3 if x < 700 else -3, ink=GREY) for x in xs)
            s.append(group(f"crowd-{r}{half}", body, rig(sum(xs) / 5, y, rnd.choice([-1.5, 1.5]), rnd.choice([0.5, 0.7, 0.9]), phase=round(rnd.random(), 2))))
    s.append(careless_founder())
    return "".join(s) + "</svg>\n"


def three():
    """'only talked to three customers': the careful founder listens and writes; three people, lots of floor."""
    s = root("three")
    clip = (f'<g transform="rotate(8 340 480)"><rect x="296" y="420" width="88" height="120" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="322" y="410" width="36" height="16" rx="4" fill="{ORANGE}" stroke="{INK}" stroke-width="5"/>'
            + line("M310 450 L366 450 M310 472 L360 472 M310 494 L366 494", 4) + '</g>')
    s.append(group("founder2", tube("M246 392 Q246 500 250 604") + box((246, 410), (248, 520), 66) + tube("M250 604 L214 842") + foot(222, 848, True)
                   + tube("M250 604 L292 842") + foot(300, 848, True)
                   + tube("M252 424 Q300 470 318 520", gap=True) + clip + hand(322, 524, 150, k=1.3)))
    s.append(group("pen", tube("M246 424 Q206 500 270 500 L324 480", gap=True) + hand(330, 470, 60, k=1.3) + line("M336 452 L352 426", 6),
                   rig(246, 424, -6, 2.4, "snap")))
    s.append(group("head2", careful_head(244, 330, look=16), rig(248, 392, 4, 0.9)))
    for i, (x, mouth, arms, deg, fq) in enumerate([(600, "o", "gesture", -1.5, 1.1), (750, "flat", "down", 2.0, 0.6), (900, "smile", "down", 1.5, 0.5)]):
        s.append(group(f"cust{i}", fig(x, 848, 2.05, mouth, arms, -3), rig(x, 848, deg, fq, phase=i * 0.3)))
    return "".join(s) + "</svg>\n"


def reading():
    """'they read The Mom Test': the careful founder holds an open book up, studying."""
    s = root("reading")
    s.append(group("founder2", tube("M525 392 L525 604") + box((525, 410), (525, 520), 66) + tube("M525 604 L495 842") + foot(490, 848)
                   + tube("M525 604 L555 842") + foot(560, 848, True)
                   + tube("M520 424 Q470 470 412 500") + tube("M530 424 Q580 470 638 500")
                   + shape("M525 452 L400 430 L400 592 L525 612 L650 592 L650 430 Z", ORANGE, 7)
                   + shape("M525 440 L410 420 L410 580 L525 600 Z", w=7) + shape("M525 440 L640 420 L640 580 L525 600 Z", w=7)
                   + line("M432 448 L506 460 M432 476 L500 488 M432 504 L506 516 M432 532 L490 542 M548 460 L618 448 M548 488 L612 476", 4)
                   + hand(406, 508, -84, k=1.4) + hand(644, 508, 84, flip=True, k=1.4)))
    s.append(group("page", shape("M525 440 L598 430 L598 588 L525 600 Z", w=6), rig(525, 520, -22, 1.0, "snap")))
    s.append(group("head2", careful_head(525, 330, down=8), rig(525, 392, 3, 0.5)))
    return "".join(s) + "</svg>\n"


def swimmer():
    """'that worked out swimmingly': the careless founder, orange swim cap, front crawl, grinning."""
    s = root("swimmer", floor=False)
    waves = lambda y, x0, x1: "M%d %d " % (x0, y) + " ".join("Q%d %d %d %d" % (x + 25, y - 16, x + 50, y) for x in range(x0, x1, 50))
    s.append(group("far-water", line(waves(560, 60, 360), 5) + line(waves(560, 760, 1000), 5), ' data-static="1"'))
    body = (tube("M640 600 L420 612") + tube("M420 612 L300 588") + tube("M420 612 L300 640") + tube("M630 605 Q560 660 500 650")
            + head(700, 575, 0) + shape("M640 572 Q640 515 700 515 Q760 515 762 570 Z", ORANGE, 7)
            + dot(694, 584) + dot(728, 582) + line("M700 604 Q724 622 750 600", 7))
    s.append(group("swimmer", body, rig(540, 620, 2, 0.9)))
    s.append(group("stroke", tube("M640 592 Q690 470 790 540") + hand(798, 552, 125), rig(640, 592, 32, 1.0)))
    front = (f'<path d="{waves(624, 20, 1060)} L1060 1020 L20 1020 Z" fill="{BG}"/>' + line(waves(624, 20, 1060), 7)
             + line(waves(700, 140, 440), 5) + line(waves(700, 640, 900), 5) + line(waves(780, 300, 700), 5)
             + line("M820 600 L846 584 M830 618 L862 612 M812 584 L826 562", 5))
    s.append(group("water", front, rig(540, 1500, 0.8, 0.9)))
    return "".join(s) + "</svg>\n"


def pile():
    """'terrible interviews, but at a high volume': the careless founder tops up a tall, leaning stack of interview notes."""
    rnd = random.Random(12)
    s = root("pile")
    sheets = ""
    for i in range(28):
        y = 842 - i * 22
        sheets += (f'<rect x="{262 + rnd.uniform(-14, 14) + i * 1.6:.1f}" y="{y}" width="150" height="18" rx="2" fill="{PAPER}" stroke="{INK}" '
                   f'stroke-width="{3 if LOOK in ("sketch", "ochre") else 5}" transform="rotate({rnd.uniform(-3, 3):.1f} {337 + i * 1.6:.1f} {y + 9})"/>')
        if i % 5 == 2:
            sheets += f'<rect x="{392 + i * 1.6:.1f}" y="{y + 3}" width="16" height="12" fill="{ORANGE}"/>'
    s.append(group("stack", sheets, rig(337, 860, 1.2, 0.5)))
    s.append(group("founder", tube("M640 392 Q644 500 660 604") + box((642, 410), (650, 520), 66)
                   + tube("M660 604 L620 842") + foot(616, 848) + tube("M660 604 L712 842") + foot(712, 848)
                   + tube("M652 424 L722 498 L672 560", gap=True)))
    note = (f'<rect x="436" y="262" width="110" height="16" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="{3 if LOOK in ("sketch", "ochre") else 5}" transform="rotate(-14 490 270)"/>'
            f'<rect x="520" y="262" width="14" height="11" fill="{ORANGE}" transform="rotate(-14 490 270)"/>')
    s.append(group("arm", tube("M646 424 Q590 352 532 296", gap=True) + note + hand(534, 300, -40), rig(646, 424, -12, 1.2, "snap")))
    s.append(group("founder-head", head(630, 330, -8) + line("M586 298 Q600 284 616 292", 7) + line("M630 290 Q646 280 662 290", 7)
                   + dot(600, 316) + dot(638, 314) + line("M588 348 Q620 380 656 348", 7), rig(640, 392, -4, 1.2, "snap")))
    return "".join(s) + "</svg>\n"


if __name__ == "__main__":
    for look in ("stick", "sketch", "pictogram", "ochre"):
        set_look(look)
        for name, f in [("pitch", pitch), ("crowd", crowd), ("three", three), ("reading", reading), ("swimmer", swimmer), ("pile", pile)]:
            open(os.path.join(HERE, f"scenes/{look}-{name}.svg"), "w").write(f())
            print(f"wrote scenes/{look}-{name}.svg")
