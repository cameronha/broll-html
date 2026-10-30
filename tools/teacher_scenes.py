"""B-roll for "The tool is the teacher" (video 4 of "five different videos to edit") -> scenes/tch-*.svg

usage: python3 tools/teacher_scenes.py
Times in ORIGINAL footage time (the five-video file) live in videos/teacher.json. Cat at the lower right: titles left, under 500 px wide.
b1 teach     Cam at an "AI 101" board; three coworkers pop up to learn
b2 ask       (rev2: the robot arrow no longer starts inside the head) a coworker with a question; the arrow to Cam gets an X; the arrow to the robot lands
b3 dumb      a chat: "Dumb question?"; the robot answers; a check; "Totally fine"
b4 manual    a remote full of buttons; a thick manual drops in; Cam gets tired
b5 teacher   the robot in a graduation cap; Cam asks, gets an answer, a check
b6 accurate  a sheet of answers: one X, then checks down the rest
b7 toolbox   (rev2: the robot sits in front of the handle, face showing) the robot drops into a red toolbox; "Your toolbox"
t1 tool      The tool is / the teacher
t2 ask       Ask AI / for the answers
"""
import os
from leon_scenes import root, title_root, tag, calm, robot, check, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bubble

BLUE = "#5E7A94"


def arrow(x1, y1, x2, y2, c=NAVY):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="20" stroke-linecap="round"/><circle cx="{x2}" cy="{y2}" r="20" fill="{c}"/>'


def cap(cx, top):
    """A graduation cap; the board's front point at (cx, top)."""
    return (f'<rect x="{cx - 90}" y="{top + 40}" width="180" height="60" rx="10" fill="{NAVY}"/>'
            f'<polygon points="{cx},{top - 20} {cx + 190},{top + 40} {cx},{top + 100} {cx - 190},{top + 40}" fill="{NAVY}"/>'
            f'<path d="M{cx} {top + 40} L{cx + 160} {top + 55} L{cx + 160} {top + 140}" stroke="{GOLD}" stroke-width="10" fill="none"/>'
            f'<circle cx="{cx + 160}" cy="{top + 150}" r="16" fill="{GOLD}"/>')


# ---- b-roll ----

def teach():
    dur = 4.2
    s = root(dur, "1,0,0")
    s += g("board", f'<rect x="470" y="110" width="540" height="340" rx="16" fill="{NAVY}"/>' + centered(740, 320, "AI 101", 120, CREAM),
           (0.05, dur + 1), rig(740, 450, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (1.4, "happy")], (250, 1000), 1.0, False, "cam")
    for i, (p, x, t0) in enumerate(((2, 590, 1.2), (5, 770, 1.6), (3, 950, 2.0))):
        s += head(p, [(t0, "neutral"), (t0 + 1.2, "happy")], (x, 1010), 0.45, True, f"h{i}")
    return s + "</svg>\n"


def ask():
    dur = 4.25
    s = root(dur, "1,0,0")
    s += head(2, [(0.05, "confused"), (3.3, "happy")], (260, 1000), 0.9, False, "co")
    s += g("q", centered(260, 330, "?", 180, ORANGE), (0.3, dur + 1), rig(260, 340, 8, 1.2))
    s += head(CAM_P, [(0.05, "neutral"), (1.6, "skeptical")], (830, 560), 0.5, True, "cam")
    s += g("a1", arrow(450, 560, 650, 430), (0.7, dur + 1), rig(450, 560, 3, 0.8))
    s += xmark("no", 560, 470, (1.8, dur + 1), 60)
    s += g("bot", robot(830, 820, 3.6), (2.9, dur + 1), rig(830, 900, 6, 1.2))
    s += g("a2", arrow(520, 720, 690, 800, ORANGE), (3.1, dur + 1), rig(520, 720, 3, 0.8))
    return s + "</svg>\n"


def dumb():
    dur = 3.45
    s = root(dur, "1,0,0")
    s += g("win", '<rect x="110" y="110" width="860" height="640" rx="24" fill="#FFFDF6"/>', (0.05, dur + 1), rig(540, 750, 1, 0.5))
    s += bubble("q", 400, 160, 520, 120, "Dumb question?", 52, (0.2, dur + 1))
    s += g("bot", robot(230, 480, 2.6), (0.9, dur + 1), rig(230, 540, 6, 1.2))
    s += bubble("a", 340, 420, 580, 120, "Sure! Here's how", 52, (1.2, dur + 1), (-1, 1))
    s += check("ok", 860, 600, 1.9, dur, 90)
    s += pill("fine", 540, 880, "Totally fine", 66, ORANGE, CREAM, (2.4, dur + 1))
    return s + "</svg>\n"


def manual():
    dur = 6.0
    s = root(dur, "1,0,0")
    btn = "".join(f'<circle cx="{200 + 60 * (i % 3)}" cy="{330 + 70 * (i // 3)}" r="20" fill="{[CREAM, ORANGE, BLUE][i % 3]}"/>' for i in range(18))
    s += g("remote", f'<rect x="140" y="220" width="240" height="560" rx="40" fill="{NAVY}"/>' + btn, (0.05, dur + 1), rig(260, 780, 2, 0.6))
    s += head(CAM_P, [(0.05, "neutral"), (1.0, "confused"), (4.2, "tired")], (840, 1000), 0.8, True, "cam")
    s += g("book", f'<rect x="410" y="330" width="300" height="420" rx="10" fill="{CREAM}"/><rect x="400" y="310" width="300" height="420" rx="10" fill="{ORANGE}"/>'
                   + centered(550, 470, "MANUAL", 52, CREAM) + f'<rect x="440" y="520" width="220" height="12" rx="6" fill="{CREAM}"/>'
                   + f'<rect x="440" y="560" width="160" height="12" rx="6" fill="{CREAM}"/>', (2.6, dur + 1), rig(550, 730, 3, 0.9))
    s += g("pages", centered(550, 260, "p. 1 of 312", 44, NAVY), (3.6, dur + 1))
    return s + "</svg>\n"


def teacher():
    dur = 4.2
    s = root(dur, "1,0,0")
    s += g("bot", robot(600, 420, 5.0), (0.05, dur + 1), rig(600, 540, 4, 1.0))
    s += g("cap", cap(600, 210), (0.3, dur + 1), rig(600, 300, 3, 0.9))
    s += pill("tch", 600, 660, "The teacher", 60, ORANGE, CREAM, (0.6, dur + 1))
    s += head(CAM_P, [(0.05, "neutral"), (1.5, "skeptical"), (3.1, "happy")], (220, 1010), 0.7, False, "cam")
    s += g("q", centered(400, 820, "?", 130, ORANGE), (1.6, 3.1), rig(400, 830, 8, 1.2))
    s += check("ok", 410, 790, 3.1, dur, 90)
    return s + "</svg>\n"


def accurate():
    dur = 3.25
    s = root(dur, "1,0,0")
    s += g("sheet", '<rect x="200" y="110" width="680" height="800" rx="18" fill="#FFFDF6"/>' + centered(540, 200, "Answers", 60, NAVY),
           (0.05, dur + 1), rig(540, 910, 1, 0.5))
    for i in range(5):
        y = 290 + 120 * i
        s += g(f"l{i}", f'<rect x="260" y="{y}" width="{440 - 60 * (i % 3)}" height="20" rx="10" fill="{GREY}"/>', (0.1 + 0.1 * i, dur + 1))
        if i == 1:
            s += xmark("x", 790, y + 10, (0.6, dur + 1), 44)
        else:
            t0 = 1.5 + 0.3 * (i if i < 1 else i - 1)
            s += check(f"c{i}", 790, y + 10, t0, dur, 70)
    return s + "</svg>\n"


def toolbox():
    dur = 3.35
    s = root(dur, "1,0,0")
    for i, (y, t0) in enumerate(((140, 0.6), (300, 0.8))):
        s += g(f"fall{i}", robot(540, y, 3.0), (t0, t0 + 0.2))   # falls past the handle into the box
    s += g("hdl", f'<rect x="390" y="440" width="300" height="70" rx="30" fill="none" stroke="{NAVY}" stroke-width="26"/>', (0.05, dur + 1))
    s += g("bot", robot(540, 440, 3.0), (1.0, dur + 1), rig(540, 500, 4, 1.0))
    s += g("box", f'<rect x="230" y="520" width="620" height="330" rx="20" fill="{ORANGE}"/><rect x="230" y="600" width="620" height="22" fill="{NAVY}"/>',
           (0.05, dur + 1), rig(540, 850, 1, 0.5))
    s += g("wr", f'<rect x="150" y="300" width="40" height="150" rx="10" fill="{NAVY}" transform="rotate(-30 170 375)"/>'
                 f'<circle cx="130" cy="305" r="42" fill="none" stroke="{NAVY}" stroke-width="22"/>', (0.3, dur + 1), rig(170, 450, 5, 1.0))
    s += pill("yours", 540, 960, "Your toolbox", 60, NAVY, CREAM, (2.3, dur + 1))
    return s + "</svg>\n"


# ---- titles (left, narrow: the cat sits at the lower right) ----

def t_tool():
    dur = 2.7
    s = title_root(dur)
    s += tag("tl", "The tool is", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("tc", "the teacher", 60, 885, 80, 2, 1.1, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_ask():
    dur = 3.0
    s = title_root(dur)
    s += tag("ai", "Ask AI", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("ans", "for the answers", 60, 885, 62, 2, 0.9, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_tool), ("t2", t_ask), ("b1", teach), ("b2", ask), ("b3", dumb), ("b4", manual),
                 ("b5", teacher), ("b6", accurate), ("b7", toolbox)):
        open(os.path.join(HERE, f"scenes/tch-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/tch-{n}.svg")
