"""B-roll for "Being yourself on camera" (raw take 2026-11-02 15-17-19) -> scenes/cam-*.svg

usage: python3 tools/camera_scenes.py
Times in ORIGINAL footage time live in videos/camera.json. Cat at the lower right: titles left, under 500 px wide.
b1 value     three skill cards with price tags; the robot arrives; the tags drop to $
b2 editing   Cam; a film strip; the robot snips; a stack of finished videos grows
b3 cheaper   "Easier" pill; a price tag $$$$ crossed out, then $
b4 camera    Cam; a camera on "camera"; an audience on "audience"
b5 story     Cam; a speech bubble "Clearly"; a book "Story"
b6 up        bars hold steady ("always powerful"); then an arrow shoots up ("go up")
b7 human     the robot walks toward Cam and stops at a line; Cam smiles; rays shine out
t1 Video editing
t2 Everyone can / make videos
t3 What holds / its value?
t4 Be yourself / on camera
"""
import os
from leon_scenes import root, title_root, tag, calm, robot, check, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bubble, bars

BLUE = "#8CBDDC"


def price(x, y, text, fill=GOLD, ink=NAVY):
    """A hang tag, hole at the left, top-left at (x, y)."""
    return (f'<path d="M{x} {y + 40} L{x + 40} {y} H{x + 200} V{y + 80} H{x + 40} Z" fill="{fill}"/>'
            f'<circle cx="{x + 34}" cy="{y + 40}" r="9" fill="{CREAM}"/>' + label(x + 62, y + 56, text, 44, ink))


def video_card(x, y, w=150, fill=NAVY):
    h = w * 0.62
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="12" fill="{fill}"/>'
            f'<path d="M{x + w * 0.42:.0f} {y + h * 0.28:.0f} L{x + w * 0.64:.0f} {y + h * 0.5:.0f} L{x + w * 0.42:.0f} {y + h * 0.72:.0f}Z" fill="{CREAM}"/>')


def camera(cx, cy, k=1.0):
    return (f'<rect x="{cx - 130 * k}" y="{cy - 80 * k}" width="{260 * k}" height="{170 * k}" rx="{22 * k}" fill="{NAVY}"/>'
            f'<rect x="{cx - 60 * k}" y="{cy - 110 * k}" width="{90 * k}" height="{40 * k}" rx="{8 * k}" fill="{NAVY}"/>'
            f'<circle cx="{cx}" cy="{cy + 5 * k}" r="{60 * k}" fill="{BLUE}"/><circle cx="{cx}" cy="{cy + 5 * k}" r="{30 * k}" fill="{NAVY}"/>'
            f'<circle cx="{cx + 95 * k}" cy="{cy - 50 * k}" r="{12 * k}" fill="{ORANGE}"/>')


# ---- b-roll ----

def value():
    dur = 4.2
    s = root(dur, "1,0,0")
    s += pill("q", 540, 140, "Holds its value?", 60, NAVY, CREAM, (0.05, dur + 1))
    for i, (name, x) in enumerate((("Coding", 90), ("Editing", 400), ("Design", 710))):
        s += g(f"c{i}", f'<rect x="{x}" y="330" width="280" height="200" rx="16" fill="#FFFDF6"/>' + centered(x + 140, 445, name, 52, NAVY),
               (0.2 + 0.25 * i, dur + 1), rig(x + 140, 530, 2, 0.7))
        drop = 3.0 + 0.3 * i
        s += g(f"hi{i}", price(x + 40, 560, "$$$"), (0.5 + 0.25 * i, drop), rig(x + 70, 560, 6, 1.1))
        s += g(f"lo{i}", price(x + 40, 610, "$", CREAM), (drop, dur + 1), rig(x + 70, 610, 6, 1.1))
    s += g("bot", robot(540, 860, 3.2), (2.6, dur + 1), rig(540, 930, 6, 1.2))
    return s + "</svg>\n"


def editing():
    dur = 3.9
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (2.2, "happy")], (230, 1010), 0.8, False, "cam")
    strip = f'<rect x="90" y="150" width="900" height="170" rx="10" fill="{NAVY}"/>' + "".join(
        f'<rect x="{110 + 70 * i}" y="160" width="40" height="22" rx="4" fill="{CREAM}"/><rect x="{110 + 70 * i}" y="288" width="40" height="22" rx="4" fill="{CREAM}"/>'
        for i in range(13))
    s += g("strip", strip + "".join(f'<rect x="{120 + 220 * i}" y="198" width="190" height="74" rx="6" fill="{[BLUE, GOLD, ORANGE, BLUE][i]}"/>' for i in range(4)),
           (0.05, dur + 1), rig(540, 320, 1, 0.5))
    s += g("bot", robot(640, 560, 3.0), (0.6, dur + 1), rig(640, 620, 6, 1.2))
    for i, t0 in enumerate((0.9, 1.5, 2.1)):                  # snips land on the strip
        s += g(f"snip{i}", f'<rect x="{318 + 220 * i}" y="140" width="14" height="190" rx="7" fill="{ORANGE}"/>', (t0, dur + 1))
    for i in range(5):                                         # finished videos stack up
        s += g(f"v{i}", video_card(760 + (i % 2) * 20, 900 - 70 * i, 170, [NAVY, ORANGE][i % 2]), (1.8 + 0.35 * i, dur + 1), rig(840, 1000, 2, 0.9))
    return s + "</svg>\n"


def cheaper():
    dur = 4.0
    s = root(dur, "1,0,0")
    s += pill("easy", 540, 180, "Easier", 80, NAVY, CREAM, (1.4, dur + 1))
    s += g("tag1", f'<path d="M260 470 L340 390 H820 V550 H340 Z" fill="{GOLD}"/><circle cx="330" cy="470" r="16" fill="{CREAM}"/>'
                   + label(400, 510, "$$$$$", 110, NAVY), (0.05, dur + 1), rig(330, 470, 4, 0.9))
    s += xmark("x", 590, 470, (2.6, dur + 1), 110)
    s += g("tag2", f'<path d="M380 720 L440 660 H700 V780 H440 Z" fill="{ORANGE}"/><circle cx="432" cy="720" r="13" fill="{CREAM}"/>'
                   + label(500, 755, "$", 100, CREAM), (2.9, dur + 1), rig(432, 720, 8, 1.2))
    s += pill("cheap", 540, 920, "Cheaper", 70, ORANGE, CREAM, (3.1, dur + 1))
    return s + "</svg>\n"


def cam_audience():
    dur = 2.9
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.0, "happy")], (270, 1010), 0.85, False, "cam")
    s += g("camr", camera(760, 300, 1.0), (0.5, dur + 1), rig(760, 390, 3, 0.9))
    s += g("ring", f'<circle cx="760" cy="305" r="150" fill="none" stroke="{ORANGE}" stroke-width="14"/>', (0.8, dur + 1))
    for i, (p, x, t0) in enumerate(((2, 590, 1.9), (5, 760, 2.1), (8, 930, 2.3))):
        s += head(p, [(t0, "neutral"), (t0 + 0.4, "happy")], (x, 1010), 0.38, True, f"a{i}")
    return s + "</svg>\n"


def story():
    dur = 3.4
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "happy"), (1.8, "excited")], (270, 1010), 0.85, False, "cam")
    s += bubble("say", 470, 170, 470, 140, "Clearly.", 70, (0.3, dur + 1), (-1, 1))
    s += g("book", f'<rect x="560" y="500" width="380" height="300" rx="12" fill="{ORANGE}"/><rect x="742" y="500" width="16" height="300" fill="{NAVY}"/>'
                   + "".join(f'<rect x="{600 + 200 * c}" y="{560 + 40 * r}" width="{110 - 20 * (r % 2)}" height="12" rx="6" fill="{CREAM}"/>' for c in range(2) for r in range(4)),
           (2.3, dur + 1), rig(750, 800, 3, 0.9))
    s += pill("st", 750, 900, "A good story", 56, NAVY, CREAM, (2.6, dur + 1))
    return s + "</svg>\n"


def up():
    dur = 4.2
    s = root(dur, "1,0,0")
    s += pill("lbl", 540, 140, "Being you on camera", 56, NAVY, CREAM, (0.05, dur + 1))
    s += bars(220, 820, (300, 320, 310, 330), 0.1, 0.15)
    s += g("pow", centered(450, 300, "always powerful", 48, NAVY), (0.6, 3.7))
    s += g("bar5", f'<rect x="684" y="210" width="90" height="610" rx="6" fill="{ORANGE}"/>', (3.75, dur + 1), rig(729, 820, 2, 0.8))
    s += g("arrow", f'<path d="M260 480 L840 230" stroke="{ORANGE}" stroke-width="22" stroke-linecap="round"/><path d="M800 200 L890 210 L840 290Z" fill="{ORANGE}"/>',
           (3.85, dur + 1))
    s += g("base", f'<rect x="180" y="820" width="720" height="14" rx="7" fill="{NAVY}"/>', (0.05, dur + 1))
    return s + "</svg>\n"


def human():
    dur = 6.1
    s = root(dur, "1,0,0")
    rays = "".join(f'<rect x="{300 - 12}" y="330" width="24" height="120" rx="12" fill="{GOLD}" transform="rotate({a} 300 640)"/>' for a in range(-80, 81, 32))
    s += g("rays", rays, (5.0, dur + 1), rig(300, 640, 3, 0.8))
    s += head(CAM_P, [(0.05, "neutral"), (2.9, "happy"), (5.0, "excited")], (300, 1010), 0.9, False, "cam")
    s += g("line", f'<rect x="610" y="330" width="16" height="650" rx="8" fill="{NAVY}"/>', (0.05, dur + 1))
    steps = ((960, 0.05), (880, 0.5), (800, 0.9), (720, 1.3))     # the robot steps in, then stops at the line
    for i, (x, t0) in enumerate(steps):
        t1 = steps[i + 1][1] if i + 1 < len(steps) else dur + 1
        s += g(f"bot{i}", robot(x, 700, 3.2), (t0, t1), rig(x, 770, 6, 1.2))
    s += g("q", centered(740, 520, "?", 120, ORANGE), (2.0, dur + 1), rig(740, 530, 8, 1.2))
    s += pill("you", 300, 200, "You", 70, ORANGE, CREAM, (3.5, dur + 1))
    return s + "</svg>\n"


# ---- titles (left, narrow: the cat sits at the lower right) ----

def two(a, b, dur, t2=1.0, size2=60):
    s = title_root(dur)
    s += tag("ta", a, 60, 770, 80, -2, 0.05, dur + 1)[0]
    if b:
        s += tag("tb", b, 60, 885, size2, 2, t2, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("Video editing", None, 2.3)), ("t2", lambda: two("Everyone can", "make videos", 2.5, 1.0, 70)),
                 ("t3", lambda: two("What holds", "its value?", 2.7, 1.0, 70)), ("t4", lambda: two("Be yourself", "on camera", 3.2, 0.9, 70)),
                 ("b1", value), ("b2", editing), ("b3", cheaper), ("b4", cam_audience), ("b5", story), ("b6", up), ("b7", human)):
        open(os.path.join(HERE, f"scenes/cam-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/cam-{n}.svg")
