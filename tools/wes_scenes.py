"""The fake podcast, Wes Anderson direction: every beat as a centered tableau -> scenes/wes-*.svg

usage: python3 tools/wes_scenes.py
Built on wes_test.py (border, curtains, Futura, pastel set). Beats with a chapter card are two shots
(wes-cN card + wes-bN set) that tools/wes_build.sh joins with a blurred whip pan.
Titles are cream placards with a navy inner line, Futura caps, centered low (alpha .mov).
"""
import os
from leon_scenes import calm, title_root, NAVY, CREAM, ORANGE, HERE
from linkedin_scenes import rig, g, dashes, building
from investors_scenes import head, bill, GOLD
from podcast_scenes import mic, ring, HOST, GUEST, BOSS
from wes_test import futura, stage_root, border, curtains, PINK, MINT, MUSTARD, card as interview_card, stage as interview_set
import cast_scenes as CS

POWDER = "#BCD6DE"


def chapter(n, name, size=72):
    dur = 1.3
    s = stage_root(dur, MUSTARD)
    s += g("ch", futura(540, 470, f"CHAPTER {n}", 44, NAVY, 14, "500"), (0.05, dur + 1))
    s += g("rule", f'<rect x="390" y="510" width="300" height="6" fill="{NAVY}"/>', (0.05, dur + 1))
    s += g("name", futura(540, 610, name, size, CREAM, 10), (0.05, dur + 1), rig(540, 610, 1, 0.5))
    return s + border() + "</svg>\n"


def plate(gid, x0, y0, x1, y1, body, show, fill=CREAM, line=NAVY):
    return g(gid, f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{fill}"/>'
                  f'<rect x="{x0 + 12}" y="{y0 + 12}" width="{x1 - x0 - 24}" height="{y1 - y0 - 24}" fill="none" stroke="{line}" stroke-width="4"/>' + body,
             show, rig((x0 + x1) / 2, y1, 1, 0.5))


def plant(gid, x, base):
    return g(gid, f'<rect x="{x - 30}" y="{base - 70}" width="60" height="70" fill="{NAVY}"/>'
                  f'<circle cx="{x}" cy="{base - 130}" r="70" fill="#6FA58A"/>', None, rig(x, base, 2, 0.6))


# ---- b-roll ----

def firm():
    dur = 3.3
    s = stage_root(dur, POWDER, MUSTARD)
    s += g("facade", f'<rect x="290" y="200" width="500" height="560" fill="{PINK}"/><rect x="270" y="180" width="540" height="40" fill="{NAVY}"/>'
                     + "".join(f'<rect x="{335 + 115 * c}" y="{380 + 110 * r}" width="70" height="80" fill="{CREAM}" stroke="{NAVY}" stroke-width="6"/>'
                               for r in range(2) for c in range(4) if not (r == 1 and c in (1, 2)))
                     + f'<path d="M460 760 V560 A80 80 0 0 1 620 560 V760 Z" fill="{NAVY}"/>', (0.05, dur + 1))
    s += plate("sign", 320, 245, 760, 345, futura(540, 307, "SERVICES FIRM", 30, NAVY, 6), (0.05, dur + 1))
    s += head(HOST, [(0.5, "neutral"), (1.6, "happy")], (540, 760), 0.4, False, "host", deg=1)
    s += plant("t1", 190, 760) + plant("t2", 890, 760)
    return s + border() + "</svg>\n"


def listens():
    dur = 4.4
    s = stage_root(dur, MINT, MUSTARD)
    s += g("board", f'<rect x="330" y="160" width="420" height="300" fill="{NAVY}"/>' + futura(540, 225, "LISTENERS", 36, CREAM, 12)
                    + f'<rect x="430" y="260" width="220" height="160" fill="{CREAM}"/>', (0.05, dur + 1), rig(540, 460, 1, 0.5))
    for i, (n, t0, t1) in enumerate((("3", 1.6, 2.3), ("9", 2.3, 3.0), ("12", 3.0, dur + 1))):
        s += g(f"n{i}", futura(540, 385, n, 120, ORANGE if n == "12" else NAVY, 4), (t0, t1))
    s += mic("mic", 540, 940, (0.05, dur + 1), 1.0)
    s += plant("p1", 190, 940) + plant("p2", 890, 940)
    return s + border() + "</svg>\n"


def targets_set():
    dur = 2.82
    s = stage_root(dur, POWDER, MUSTARD)
    for i, (h, f) in enumerate(((260, PINK), (400, NAVY), (500, "#6FA58A"), (400, NAVY), (260, PINK))):
        s += building(f"b{i}", 125 + 170 * i, 150, h, f, (0.05, dur + 1), base=680)
    s += ring("r0", 370, 400, (0.7, dur + 1), 70)
    s += ring("r1", 710, 400, (1.3, dur + 1), 70)
    return s + border() + "</svg>\n"


def invite():
    dur = 3.4
    s = stage_root(dur, PINK, MUSTARD)
    s += plate("card", 280, 170, 800, 530, futura(540, 270, "YOU ARE INVITED", 34, NAVY, 8, "500")
               + f'<rect x="440" y="300" width="200" height="4" fill="{NAVY}"/>' + futura(540, 380, "TO BE A GUEST ON", 30, NAVY, 6, "500")
               + futura(540, 470, "MY PODCAST", 58, ORANGE, 8), (0.3, dur + 1))
    s += head(HOST, [(0.05, "happy")], (240, 880), 0.5, True, "host", deg=1.5)
    s += head(GUEST, [(0.05, "surprised"), (1.9, "happy")], (840, 880), 0.5, False, "guest", deg=1.5)
    return s + border() + "</svg>\n"


def ask():
    dur = 3.3
    s = stage_root(dur, POWDER, MINT)
    s += plate("q", 150, 190, 930, 440, futura(540, 290, "ANYONE IN YOUR FIRM", 36, NAVY, 5), (0.15, dur + 1))
    s += g("q2", futura(540, 380, "I SHOULD TALK TO?", 36, ORANGE, 5), (1.0, dur + 1))
    s += head(HOST, [(0.05, "happy")], (250, 880), 0.5, True, "host", deg=1.5)
    s += head(GUEST, [(0.05, "neutral"), (2.0, "happy")], (830, 880), 0.5, False, "guest", deg=1.5)
    return s + border() + "</svg>\n"


def intro_set():
    dur = 2.82
    s = stage_root(dur, MINT, MUSTARD)
    s += head(HOST, [(0.05, "happy")], (220, 660), 0.45, True, "host", deg=1.5)
    s += head(GUEST, [(0.05, "happy")], (540, 660), 0.45, False, "guest", deg=1.5)
    s += head(BOSS, [(1.2, "neutral"), (2.0, "happy")], (860, 660), 0.45, False, "boss", deg=1.5)
    s += dashes("l1", (330, 560), (430, 560), (0.4, dur + 1), NAVY, 10)
    s += dashes("l2", (650, 560), (750, 560), (1.4, dur + 1), ORANGE, 10)
    s += g("bench", f'<rect x="130" y="700" width="820" height="30" fill="{CREAM}"/><rect x="130" y="730" width="820" height="10" fill="{NAVY}"/>'
                    f'<rect x="170" y="740" width="24" height="180" fill="{NAVY}"/><rect x="886" y="740" width="24" height="180" fill="{NAVY}"/>', (0.05, dur + 1))
    return s + border() + "</svg>\n"


def deals():
    dur = 3.8
    s = stage_root(dur, PINK, MUSTARD)
    k = 0
    for row, n in enumerate((4, 3, 2, 1)):
        x0 = 540 - (n * 160 - 10) / 2
        for c in range(n):
            s += bill(f"b{k}", x0 + 160 * c, 880 - 90 * row, (0.2 + 0.18 * k, dur + 1)); k += 1
    s += plate("amt", 270, 170, 810, 330, futura(540, 285, "$200,000", 92, NAVY, 6), (2.3, dur + 1))
    return s + border() + "</svg>\n"


def ads():
    dur = 3.8
    s = stage_root(dur, POWDER, MUSTARD)
    for side, x in (("l", 300), ("r", 780)):
        s += g(f"ped{side}", f'<rect x="{x - 110}" y="740" width="220" height="30" fill="{NAVY}"/><rect x="{x - 90}" y="770" width="180" height="250" fill="{CREAM}"/>',
               (0.05, dur + 1))
    s += g("adsl", futura(300, 880, "ADS", 40, NAVY, 8), (0.05, dur + 1))
    s += g("cll", futura(780, 880, "CLIENTS", 25, ORANGE, 3), (0.05, dur + 1))
    s += g("coin", f'<circle cx="300" cy="712" r="28" fill="{GOLD}"/>' + futura(300, 724, "$", 32, NAVY, 0), (0.3, dur + 1), rig(300, 740, 4, 1.0))
    for i in range(7):
        s += bill(f"b{i}", 705, 660 - 70 * i, (1.6 + 0.2 * i, dur + 1))
    return s + border() + "</svg>\n"


# ---- titles: placards ----

def placard(lines, y_mid, t0, dur, gid="pl"):
    """lines = [(text, size, color)]; one centered cream placard."""
    w = max(len(t) * (s * 0.72 + 8) for t, s, _ in lines) + 120
    h = sum(s * 1.4 for _, s, _ in lines) + 60
    x0, y0 = 540 - w / 2, y_mid - h / 2
    body, y = "", y0 + 30
    for t, s, c in lines:
        y += s * 1.4
        body += futura(540, round(y - s * 0.4), t, s, c, 8)
    return plate(gid, round(x0), round(y0), round(x0 + w), round(y0 + h), body, (t0, dur + 1))


def t_title():
    dur = 3.0
    return title_root(dur) + placard([("A TRUE STORY", 26, ORANGE), ("THE FAKE PODCAST", 54, NAVY)], 880, 0.15, dur) + "</svg>\n"


def t_special():
    dur = 2.2
    return title_root(dur) + placard([("THEY FEEL", 34, NAVY), ("SPECIAL", 62, ORANGE)], 880, 0.05, dur) + "</svg>\n"


def t_traits():
    dur = 3.6
    s = title_root(dur)
    s += plate("pl", 150, 830, 930, 950, "", (0.05, dur + 1))
    for i, (w, x, t) in enumerate((("CAREFUL", 300, 0.1), ("KIND", 540, 1.5), ("ATTENTIVE", 780, 2.6))):
        s += g(f"w{i}", futura(x, 908, w, 40, ORANGE if i == 2 else NAVY, 6), (t, dur + 1))
    return s + "</svg>\n"


def t_inventive():
    dur = 3.0
    s = title_root(dur)
    s += plate("pl", 200, 790, 880, 1010, futura(540, 870, "A NEW WAY", 34, NAVY, 8), (0.1, dur + 1))
    s += g("cust", futura(540, 955, "TO GET CUSTOMERS", 50, ORANGE, 8), (1.4, dur + 1))
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_title), ("t2", t_special), ("t3", t_traits), ("t4", t_inventive),
                 ("b0", firm), ("b1", listens), ("c2", lambda: chapter("ONE", "THE TARGETS")), ("b2", targets_set),
                 ("b3", invite), ("c4", interview_card), ("b4", interview_set), ("b5", ask),
                 ("c6", lambda: chapter("THREE", "THE INTRODUCTION", 60)), ("b6", intro_set), ("b7", deals), ("b8", ads)):
        open(os.path.join(HERE, f"scenes/wes-{n}.svg"), "w").write(calm(f(), 0.4))
        print(f"wrote scenes/wes-{n}.svg")
