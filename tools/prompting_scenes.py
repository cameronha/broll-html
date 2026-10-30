"""B-roll for "PSA: prompting is dead" (video 1 of "five different videos to edit", 2026-10-30 graded export) -> scenes/pmt-*.svg

usage: python3 tools/prompting_scenes.py
Times in ORIGINAL footage time (the five-video file) live in videos/prompting.json. A cat sits at the lower right: titles left, under 500 px wide.
b1 collect   Cam's head; prompt cards stack up; a "My prompts" pill; he gets tired
b2 apply     a "Problem" box; Cam wonders; bubble "AI for this?"; a robot pops up beside the box
b3 create    Cam happy; a light bulb lights over his head; sparks burst ("creativity and imagination")
b4 orgs      three office towers rise; one lit bulb over them goes grey; a red X
b5 perfect   a prompt field rewritten again and again; Cam worried, then tired
t1 dead      Prompting / is dead
t2 bigger    Think / bigger
"""
import os
from PIL import ImageFont
from leon_scenes import FONT, root, title_root, tag, calm, robot, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY, building
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered

BLUE = "#5E7A94"


def card(x, y, n):
    return (f'<rect x="{x}" y="{y}" width="320" height="110" rx="12" fill="#FFFDF6"/>'
            f'<text x="{x + 24}" y="{y + 50}" font-family="Libre Franklin" font-weight="800" font-size="34" fill="{NAVY}">Prompt #{n}</text>'
            f'<rect x="{x + 24}" y="{y + 70}" width="230" height="12" rx="6" fill="{GREY}"/>')


def bulb(cx, cy, lit=True):
    c = GOLD if lit else GREY
    return (f'<circle cx="{cx}" cy="{cy}" r="85" fill="{c}"/><rect x="{cx - 40}" y="{cy + 70}" width="80" height="60" rx="10" fill="{NAVY}"/>'
            f'<rect x="{cx - 30}" y="{cy + 135}" width="60" height="16" rx="8" fill="{NAVY}"/>')


# ---- b-roll ----

def collect():
    dur = 4.1
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.6, "excited"), (2.8, "tired")], (270, 980), 1.0, False, "cam")
    for i in range(5):
        t0 = 0.3 + 0.45 * i
        s += g(f"c{i}", card(600 + (25 if i % 2 else -10), 650 - 105 * i, i + 1), (t0, dur + 1), rig(760, 760 - 105 * i, 3, 0.9))
    s += pill("mine", 760, 110, "My prompts", 50, ORANGE, CREAM, (3.0, dur + 1))
    return s + "</svg>\n"


def apply_():
    dur = 4.2
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.2, "skeptical"), (3.0, "happy")], (270, 980), 1.0, False, "cam")
    s += g("box", f'<rect x="600" y="520" width="340" height="230" rx="18" fill="{NAVY}"/>' + centered(770, 655, "Problem", 60, CREAM),
           (0.3, dur + 1), rig(770, 750, 1, 0.5))
    s += pill("q", 560, 170, "AI for this?", 66, CREAM, NAVY, (1.8, dur + 1))
    s += g("bot", robot(860, 420, 3.2), (2.8, dur + 1), rig(860, 500, 6, 1.2))
    return s + "</svg>\n"


def create():
    dur = 4.6
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (2.0, "happy"), (3.9, "excited")], (540, 1010), 1.0, False, "cam")
    s += g("off", bulb(540, 210, False), (0.4, 2.6), rig(540, 360, 2, 0.6))
    s += g("on", bulb(540, 210, True), (2.6, dur + 1), rig(540, 360, 3, 0.9))
    for i, (x, y, r, f) in enumerate(((330, 160, 26, ORANGE), (760, 140, 22, GOLD), (300, 380, 18, CREAM), (790, 360, 28, ORANGE),
                                      (420, 60, 16, CREAM), (680, 60, 20, ORANGE))):
        s += g(f"sp{i}", f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}"/>', (3.9 + 0.08 * i, dur + 1), rig(x, y + r, 8, 1.6))
    return s + "</svg>\n"


def orgs():
    dur = 4.0
    s = root(dur, "1,0,0")
    for i, (x, w, h, t0) in enumerate(((150, 230, 420, 0.1), (420, 260, 560, 0.4), (720, 220, 380, 0.7))):
        s += building(f"b{i}", x, w, h, NAVY if i != 1 else BLUE, (t0, dur + 1))
    s += g("on", bulb(550, 200, True), (1.5, 2.9), rig(550, 350, 3, 0.9))
    s += g("off", bulb(550, 200, False), (2.9, dur + 1), rig(550, 350, 1, 0.5))
    s += xmark("x", 860, 210, (3.3, dur + 1), 60)
    return s + "</svg>\n"


def perfect():
    dur = 3.7
    s = root(dur, "1,0,0")
    s += g("field", f'<rect x="110" y="200" width="860" height="200" rx="20" fill="#FFFDF6"/><rect x="110" y="200" width="860" height="200" rx="20" fill="none" stroke="{NAVY}" stroke-width="10"/>',
           (0.05, dur + 1), rig(540, 400, 1, 0.5))
    for i, (t, a, b) in enumerate((("Write an email", 0.05, 0.9), ("Write a good email", 0.9, 1.5), ("Write a great email", 1.5, 2.1),
                                   ("Write a GREAT email!", 2.1, 2.7), ("Write a perfect email", 2.7, dur + 1))):
        s += g(f"t{i}", label(160, 320, t, 58, NAVY) + f'<rect x="{172 + ImageFont.truetype(FONT, 58).getlength(t):.0f}" y="268" width="8" height="70" fill="{ORANGE}"/>', (a, b))
    s += head(CAM_P, [(0.05, "neutral"), (1.2, "worried"), (2.8, "tired")], (540, 1010), 0.95, False, "cam")
    return s + "</svg>\n"


# ---- titles (left, narrow: the cat sits at the lower right) ----

def t_dead():
    dur = 2.3
    s = title_root(dur)
    s += tag("pr", "Prompting", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("dead", "is dead", 60, 885, 96, 2, 1.4, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_bigger():
    dur = 2.6
    s = title_root(dur)
    s += tag("th", "Think", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("big", "bigger", 60, 885, 104, 2, 0.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_dead), ("t2", t_bigger), ("b1", collect), ("b2", apply_), ("b3", create), ("b4", orgs), ("b5", perfect)):
        open(os.path.join(HERE, f"scenes/pmt-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/pmt-{n}.svg")
