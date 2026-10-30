"""B-roll for "Host a monthly lunch and learn" (video 2 of "five different videos to edit") -> scenes/lnl-*.svg

usage: python3 tools/lunch_scenes.py
Times in ORIGINAL footage time (the five-video file) live in videos/lunch.json. Cat at the lower right: titles left, under 500 px wide.
b1 unsure    a company tower; the boss looks confused; a big "?"
b2 lunch     a "$0" tag ("costs nothing"); a calendar page "Monthly / Lunch & Learn"; a plate
b3 table     three coworkers at a table; one gets a gold star and a robot ("interesting work with AI"); "Here's what I do"
b4 share     a sheet: what works (check), what doesn't (X), tools (wrench); "Shared"
b5 champs    a crowd of small heads; red rings find the champion and a key player
b6 impact    the champion under a spotlight; impact bars grow
b7 nobig     Vision deck / 5-year plan / Tech bet, each crossed out
b8 grass     grass sprouts; coworkers pop up out of it; an up arrow
t1 start     Not sure / where to start?
t2 speed     Everyone / up to speed
"""
import os
from leon_scenes import root, title_root, tag, calm, robot, check, CREAM, NAVY, ORANGE, PAPER, HERE
from linkedin_scenes import rig, g, GREY, building
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bars
from spotlight_scenes import ring, LIGHT

BLUE = "#5E7A94"
GREEN = "#6FA58A"


def star(cx, cy, r):
    import math
    pts = " ".join(f"{cx + (r if i % 2 == 0 else r * 0.45) * math.sin(math.pi * i / 5):.0f},{cy - (r if i % 2 == 0 else r * 0.45) * math.cos(math.pi * i / 5):.0f}"
                   for i in range(10))
    return f'<polygon points="{pts}" fill="{GOLD}"/>'


def sheet_card(x, y, w, h, title, fill="#FFFDF6"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}"/>'
            + centered(x + w / 2, y + 120, title, 44, NAVY)
            + "".join(f'<rect x="{x + 40}" y="{y + 170 + 40 * i}" width="{w - 80 - 40 * (i % 2)}" height="14" rx="7" fill="{GREY}"/>' for i in range(3)))


# ---- b-roll ----

def unsure():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += building("tower", 560, 340, 520, NAVY, (0.05, dur + 1))
    s += head(6, [(0.05, "neutral"), (1.0, "confused")], (280, 990), 0.95, False, "boss")
    s += g("q", centered(730, 200, "?", 200, ORANGE), (1.3, dur + 1), rig(730, 210, 8, 1.2))
    s += g("bot", robot(470, 560, 2.2), (2.2, dur + 1), rig(470, 610, 6, 1.3))
    return s + "</svg>\n"


def lunch():
    dur = 4.4
    s = root(dur, "1,0,0")
    s += g("tag", f'<rect x="90" y="300" width="300" height="160" rx="22" fill="{ORANGE}"/><circle cx="135" cy="380" r="18" fill="{CREAM}"/>'
                  + centered(260, 420, "$0", 110, CREAM), (0.9, dur + 1), rig(240, 460, 5, 1.0))
    s += g("cal", f'<rect x="490" y="160" width="480" height="560" rx="20" fill="#FFFDF6"/><rect x="490" y="160" width="480" height="120" rx="20" fill="{ORANGE}"/>'
                  + centered(730, 245, "Monthly", 64, CREAM) + centered(730, 380, "Lunch &", 70, NAVY) + centered(730, 470, "Learn", 70, NAVY),
           (2.4, dur + 1), rig(730, 720, 2, 0.6))
    s += g("plate", f'<ellipse cx="730" cy="600" rx="140" ry="50" fill="{CREAM}" stroke="{NAVY}" stroke-width="8"/>'
                    f'<path d="M650 590 Q730 520 810 590 Z" fill="{GOLD}"/>', (3.3, dur + 1), rig(730, 650, 4, 1.0))
    return s + "</svg>\n"


def table():
    dur = 3.7
    s = root(dur, "1,0,0")
    for i, (p, x) in enumerate(((2, 210), (5, 540), (3, 870))):
        tl = [(0.05, "neutral")] + ([(1.0, "excited"), (3.0, "happy")] if p == 5 else [(2.8, "happy")])
        s += head(p, tl, (x, 800), 0.6, x > 540, f"h{i}")
    s += g("table", f'<rect x="40" y="790" width="1000" height="44" rx="8" fill="{CREAM}"/><rect x="40" y="834" width="1000" height="16" fill="{NAVY}"/><rect x="90" y="850" width="26" height="230" fill="{NAVY}"/><rect x="964" y="850" width="26" height="230" fill="{NAVY}"/>', (0.05, dur + 1))
    s += g("star", star(540, 400, 60), (1.0, dur + 1), rig(540, 460, 6, 1.2))
    s += g("bot", robot(660, 400, 1.6), (1.5, dur + 1), rig(660, 435, 6, 1.4))
    s += pill("say", 600, 250, "Here's what I do", 50, ORANGE, CREAM, (3.0, dur + 1))
    return s + "</svg>\n"


def share():
    dur = 4.3
    s = root(dur, "1,0,0")
    s += g("sheet", '<rect x="200" y="120" width="680" height="780" rx="18" fill="#FFFDF6"/>', (0.05, dur + 1), rig(540, 900, 1, 0.5))
    rows = (("What works", 1.2), ("What doesn't", 1.9), ("Which tools", 2.5))
    for i, (t, t0) in enumerate(rows):
        s += g(f"r{i}", label(370, 300 + 210 * i, t, 60, NAVY), (0.3 + 0.2 * i, dur + 1))
    s += check("ok", 250, 240, 1.2, dur, 80)
    s += xmark("no", 290, 490, (1.9, dur + 1), 34)
    s += g("tool", f'<rect x="270" y="680" width="40" height="110" rx="10" fill="{NAVY}" transform="rotate(35 290 735)"/>'
                   f'<circle cx="265" cy="685" r="38" fill="none" stroke="{NAVY}" stroke-width="22"/>', (2.5, dur + 1), rig(290, 790, 6, 1.2))
    s += pill("shared", 760, 860, "Shared", 60, ORANGE, CREAM, (3.4, dur + 1), -6)
    return s + "</svg>\n"


def champs():
    dur = 3.3
    s = root(dur, "1,0,0")
    crowd = ((2, 180, 560), (8, 420, 560), (3, 660, 560), (9, 900, 560), (5, 300, 960), (1, 540, 960), (6, 780, 960))
    for i, (p, x, y) in enumerate(crowd):
        tl = [(0.05, "neutral")] + ([(1.4, "happy")] if p in (5, 9) else [])
        s += head(p, tl, (x, y), 0.6, x > 540, f"h{i}")
    s += ring("c1", 300, 850, 140, (1.2, dur + 1), 12)
    s += pill("champ", 300, 640, "Champion", 46, ORANGE, CREAM, (1.6, dur + 1))
    s += ring("c2", 900, 450, 140, (2.6, dur + 1), 12)
    return s + "</svg>\n"


def impact():
    dur = 4.7
    s = root(dur, "1,0,0")
    s += g("beam", f'<path d="M200 0 H380 L560 760 H20 Z" fill="{LIGHT}" opacity="0.8"/>', (0.4, dur + 1))
    s += head(5, [(0.05, "neutral"), (0.6, "happy"), (3.9, "excited")], (290, 940), 0.9, False, "champ")
    s += bars(580, 740, [120, 200, 300, 420], 2.0, 0.35, NAVY, 80, 24)
    s += g("arrow", f'<path d="M600 300 L900 140" stroke="{ORANGE}" stroke-width="22" stroke-linecap="round"/><path d="M900 140 L840 140 M900 140 L880 196" stroke="{ORANGE}" stroke-width="22" stroke-linecap="round"/>',
           (3.9, dur + 1), rig(750, 300, 4, 1.0))
    return s + "</svg>\n"


def nobig():
    dur = 4.2
    s = root(dur, "1,0,0")
    for i, (t, x, t0, tx) in enumerate((("Vision", 55, 0.3, 1.1), ("Big plan", 395, 1.0, 1.9), ("Tech bet", 735, 2.6, 3.9))):
        s += g(f"c{i}", sheet_card(x, 260, 290, 420, t), (t0, dur + 1), rig(x + 145, 680, 2, 0.7))
        s += xmark(f"x{i}", x + 145, 470, (tx, dur + 1), 110)
    return s + "</svg>\n"


def grass():
    dur = 4.6
    s = root(dur, "1,0,0")
    for i in range(9):
        x = 90 + 112 * i
        s += g(f"bl{i}", f'<path d="M{x - 30} 750 Q{x - 10} 640 {x} 600 Q{x + 6} 660 {x + 14} 690 Q{x + 24} 640 {x + 40} 620 Q{x + 32} 690 {x + 30} 750 Z" fill="{GREEN}"/>',
               (0.2 + 0.15 * i, dur + 1), rig(x, 750, 6, 1.1))
    for i, (p, x, t0) in enumerate(((2, 230, 2.0), (8, 540, 2.6), (3, 850, 3.2))):
        s += head(p, [(t0, "happy")], (x, 760), 0.62, x > 540, f"h{i}")
    s += g("up", f'<path d="M540 260 V90 M470 160 L540 90 L610 160" fill="none" stroke="{ORANGE}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>',
           (3.8, dur + 1), rig(540, 260, 4, 1.0))
    return s + "</svg>\n"


# ---- titles (left, narrow: the cat sits at the lower right) ----

def t_start():
    dur = 2.5
    s = title_root(dur)
    s += tag("ns", "Not sure", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("ws", "where to start?", 60, 885, 66, 2, 0.9, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_speed():
    dur = 2.8
    s = title_root(dur)
    s += tag("ev", "Everyone", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("up", "up to speed", 60, 885, 80, 2, 1.1, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_start), ("t2", t_speed), ("b1", unsure), ("b2", lunch), ("b3", table), ("b4", share),
                 ("b5", champs), ("b6", impact), ("b7", nobig), ("b8", grass)):
        open(os.path.join(HERE, f"scenes/lnl-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/lnl-{n}.svg")
