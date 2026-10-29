"""B-roll for "The fake podcast" (2025-04-29 footage) -> scenes/pod-*.svg

usage: python3 tools/podcast_scenes.py
Reuses the Leon / LinkedIn / investors / repetition parts. Times in ORIGINAL footage time live in videos/podcast.json.
Cast: p4 = the host (services firm owner), p3 = the guest (middle manager), p6 = the person she introduces.
t1 title     The fake / podcast
b0 firm      the host pops in next to his small "Services firm" building
b1 listens   a podcast mic; the listen counter ticks up to 12
b2 targets   a row of company buildings; red rings land on the ones he wants
b3 invite    host asks the guest onto his podcast; she goes from surprised to happy
t2 special   They feel / special
b4 rapport   host and guest at two mics, a dashed line joins them; her company behind her
b5 ask       "Anyone in your firm I should talk to?"
t3 traits    Careful / Kind / Attentive
b6 intro     guest introduces the host to a third person (dashed lines, one by one)
b7 deals     bills stack up; "$200,000" tag
b8 ads       a tiny "Ads" coin next to a tall "Clients" stack of bills
t4 inventive A new way / to get customers
"""
import os
from leon_scenes import root, title_root, tag, calm, CREAM, NAVY, ORANGE, PAPER, HERE
from linkedin_scenes import rig, g, building, dashes, GREY
from investors_scenes import head, label, bill, GOLD
from repetition_scenes import pill
from report_scenes import centered

HOST, GUEST, BOSS = 4, 3, 6
BLUE = "#8CBDDC"


def mic(gid, x, y, show, k=1.0):
    """x, y = base of the stand."""
    w, h = 110 * k, 190 * k
    grille = "".join(f'<line x1="{x - w / 2 + 14 * k:.0f}" y1="{y - 330 * k + 40 * k + 26 * k * i:.0f}" x2="{x + w / 2 - 14 * k:.0f}" '
                     f'y2="{y - 330 * k + 40 * k + 26 * k * i:.0f}" stroke="{BLUE}" stroke-width="{6 * k:.0f}" stroke-linecap="round"/>' for i in range(5))
    return g(gid, f'<rect x="{x - 10 * k:.0f}" y="{y - 140 * k:.0f}" width="{20 * k:.0f}" height="{140 * k:.0f}" fill="{NAVY}"/>'
                  f'<rect x="{x - 90 * k:.0f}" y="{y - 18 * k:.0f}" width="{180 * k:.0f}" height="{24 * k:.0f}" rx="{12 * k:.0f}" fill="{NAVY}"/>'
                  f'<rect x="{x - w / 2:.0f}" y="{y - 330 * k:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{w / 2:.0f}" fill="{NAVY}"/>' + grille,
             show, rig(x, y, 2, 0.7))


def ring(gid, cx, cy, show, r=70):
    return g(gid, f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ORANGE}" stroke-width="16"/>'
                  f'<circle cx="{cx}" cy="{cy}" r="{r * 0.45:.0f}" fill="none" stroke="{ORANGE}" stroke-width="12"/>', show, rig(cx, cy, 5, 1.1))


# ---- b-roll ----

def firm():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += building("bld", 560, 300, 420, NAVY, (0.05, dur + 1), base=860)
    s += g("sign", f'<rect x="530" y="330" width="360" height="90" rx="12" fill="{ORANGE}"/>' + centered(710, 390, "Services firm", 46, CREAM),
           (0.5, dur + 1), rig(710, 420, 3, 0.8))
    s += head(HOST, [(0.2, "neutral"), (1.4, "happy")], (290, 700), 0.65, True, "host")
    return s + "</svg>\n"


def listens():
    dur = 4.4
    s = root(dur, "1,0,0")
    s += mic("mic", 360, 900, (0.05, dur + 1), 1.4)
    s += g("card", f'<rect x="580" y="300" width="380" height="300" rx="20" fill="#FFFDF6"/>' + centered(770, 370, "Listens", 52, GREY),
           (1.6, dur + 1), rig(770, 600, 2, 0.7))
    for i, (n, t) in enumerate((("3", 1.8), ("9", 2.4), ("12", 3.0))):
        s += g(f"n{i}", centered(770, 540, n, 150, ORANGE if n == "12" else NAVY), (t, [2.4, 3.0, dur + 1][i]))
    return s + "</svg>\n"


def targets():
    dur = 3.6
    s = root(dur, "1,0,0")
    blds = ((80, 170, 380, NAVY), (290, 200, 540, "#5E7A94"), (530, 160, 300, NAVY), (730, 230, 470, "#5E7A94"))
    for i, (x, w, h, f) in enumerate(blds):
        s += building(f"b{i}", x, w, h, f, (0.05 + 0.15 * i, dur + 1), base=900)
    s += ring("r0", 390, 500, (1.2, dur + 1), 90)
    s += ring("r1", 845, 560, (2.2, dur + 1), 90)
    return s + "</svg>\n"


def invite():
    dur = 3.4
    s = root(dur, "1,0,0")
    s += head(HOST, [(0.05, "happy")], (260, 720), 0.5, True, "host")
    s += pill("ask", 540, 300, "Be on my podcast?", 54, ORANGE, CREAM, (0.4, dur + 1))
    s += head(GUEST, [(0.3, "surprised"), (1.9, "happy")], (820, 720), 0.5, False, "guest")
    return s + "</svg>\n"


def rapport():
    dur = 4.2
    s = root(dur, "1,0,0")
    s += building("co", 880, 170, 460, "#5E7A94", (0.05, dur + 1), base=900)
    s += head(HOST, [(0.05, "happy")], (240, 680), 0.55, True, "host")
    s += head(GUEST, [(0.05, "happy"), (2.6, "excited")], (760, 680), 0.55, False, "guest")
    s += mic("m1", 420, 940, (0.05, dur + 1), 0.8)
    s += mic("m2", 660, 940, (0.05, dur + 1), 0.8)
    s += dashes("line", (360, 560), (640, 560), (1.6, dur + 1), ORANGE, 12)
    return s + "</svg>\n"


def ask():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += head(HOST, [(0.05, "happy")], (230, 800), 0.5, True, "host")
    s += pill("q1", 560, 300, "Anyone in your firm", 54, ORANGE, CREAM, (0.2, dur + 1))
    s += pill("q2", 600, 470, "I should talk to?", 54, ORANGE, CREAM, (1.2, dur + 1))
    s += head(GUEST, [(0.05, "neutral"), (2.0, "happy")], (850, 800), 0.5, False, "guest")
    return s + "</svg>\n"


def intro():
    dur = 3.6
    s = root(dur, "1,0,0")
    s += head(HOST, [(0.05, "happy")], (200, 800), 0.5, True, "host")
    s += head(GUEST, [(0.3, "happy")], (540, 520), 0.5, False, "guest")
    s += head(BOSS, [(1.6, "neutral"), (2.6, "happy")], (880, 800), 0.5, False, "boss")
    s += dashes("l1", (300, 650), (440, 470), (0.9, dur + 1), NAVY, 10)
    s += dashes("l2", (640, 470), (780, 650), (1.9, dur + 1), ORANGE, 10)
    return s + "</svg>\n"


def deals():
    dur = 4.7
    s = root(dur, "1,0,0")
    for i in range(8):
        s += bill(f"b{i}", 300 + (i % 2) * 300, 820 - (i // 2) * 100, (0.2 + 0.22 * i, dur + 1))
    s += g("amt", f'<rect x="250" y="230" width="580" height="150" rx="18" fill="{NAVY}"/>' + centered(540, 335, "$200,000", 96, CREAM),
           (2.3, dur + 1), rig(540, 380, 2, 0.6))
    return s + "</svg>\n"


def ads():
    dur = 3.8
    s = root(dur, "1,0,0")
    s += g("coin", f'<circle cx="290" cy="820" r="36" fill="{GOLD}"/>' + centered(290, 834, "$", 40, NAVY), (0.3, dur + 1), rig(290, 856, 6, 1.2))
    s += g("adsl", centered(290, 930, "Ads", 56, NAVY), (0.3, dur + 1))
    for i in range(7):
        s += bill(f"b{i}", 640, 820 - 90 * i, (1.6 + 0.2 * i, dur + 1))
    s += g("cl", centered(715, 990, "Clients", 56, ORANGE), (1.6, dur + 1))
    return s + "</svg>\n"


# ---- titles ----

def t_title():
    dur = 3.0
    s = title_root(dur)
    s += tag("fake", "The fake", 60, 760, 96, -2, 0.15, dur + 1)[0]
    s += tag("pod", "podcast", 60, 890, 110, 2, 0.9, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_special():
    dur = 2.2
    s = title_root(dur)
    s += tag("they", "They feel", 60, 780, 86, -2, 0.05, dur + 1)[0]
    s += tag("sp", "special", 60, 900, 100, 3, 0.55, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_traits():
    dur = 3.6
    s = title_root(dur)
    for i, (w, t) in enumerate((("Careful", 0.1), ("Kind", 1.5), ("Attentive", 2.6))):
        s += tag(f"w{i}", w, 60, 660 + 115 * i, 86, (-1) ** i * 2, t, dur + 1, ORANGE if i == 2 else None, PAPER)[0]
    return s + "</svg>\n"


def t_inventive():
    dur = 3.0
    s = title_root(dur)
    s += tag("new", "A new way", 60, 760, 86, -2, 0.1, dur + 1)[0]
    s += tag("cust", "to get customers", 60, 880, 86, 2, 1.4, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_title), ("t2", t_special), ("t3", t_traits), ("t4", t_inventive),
                 ("b0", firm), ("b1", listens), ("b2", targets), ("b3", invite), ("b4", rapport),
                 ("b5", ask), ("b6", intro), ("b7", deals), ("b8", ads)):
        open(os.path.join(HERE, f"scenes/pod-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/pod-{n}.svg")
