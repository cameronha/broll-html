"""B-roll for "pinky sales" (raw 2026-11-02 15-51-11) -> scenes/pk-*.svg
Times inside each beat are local; windows in videos/pinky.json (raw time = graded time; offset 0).
b1 videos     three video cards pop; a little Pinky peeks into each
b2 calendar   a calendar, mostly empty; "Not dedicated"; videos land on a few days; a light bulb
b3 talks      Cam and a client trade numbered speech bubbles; "Consultative selling"
b4 right      "Right person" (Cam) gets a check; "Right company" (Actionworks building) gets a check
b5 proposal   a huge proposal thuds down; "Great work", "Outcomes"; the page stack grows
b6 passion    Cam excited; a heart flies at the proposal and bounces off; an X; "Doesn't come across"
b7 attach     a video clips onto the proposal; the envelope flies off; "Hey!"
b8 vision     a video window with Cam excited; the client warms up; "Vision", "Powerful"
b9 jump       a proposal video; Pinky jumps into the frame; "Restart?" gets an X; play goes on
b10 views     the envelope flies to a company; a view counter shows 1, then 2
b11 forwarded the counter climbs 2, 5, 12, 20, 30; envelopes fly around the company
b12 profit    coins pile up; "Very profitable"; a check
b13 train     Pinky walks to a camera and sits; "Video proposal"
t1 My secret / weapon (used twice)   t2 I closed / that deal
"""
import os
from leon_scenes import root, calm, robot, check, CREAM, NAVY, ORANGE, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bubble
from teacher2_scenes import steps, window, lines
from nov2_parts import two, cat, video_card, doc, envelope, counter, heart, building, BLUE, WHITE

CLIENT = 5


def videos():
    dur = 4.6
    s = root(dur, "1,0,0")
    for i, (x, y, t, tc) in enumerate(((90, 200, 0.3, 2.9), (560, 160, 0.8, 3.3), (320, 560, 1.3, 3.7))):
        s += g(f"v{i}", video_card(x, y, 420), (t, dur + 1), rig(x + 210, y + 260, 2, 0.7))
        s += g(f"c{i}", cat(x + 380, y + 262, 0.62), (tc, dur + 1), rig(x + 330, y + 262, 4, 1.2))
    s += pill("q", 540, 1010 - 90, "The cat thing", 52, NAVY, CREAM, (1.0, dur + 1))
    return s + "</svg>\n"


def calendar():
    dur = 7.6
    s = root(dur, "1,0,0")
    s += g("cal", f'<rect x="380" y="120" width="620" height="620" rx="20" fill="{WHITE}"/><rect x="380" y="120" width="620" height="100" rx="20" fill="{ORANGE}"/>'
                  f'<rect x="380" y="190" width="620" height="30" fill="{ORANGE}"/>' + label(420, 190, "This month", 52, CREAM)
                  + "".join(f'<rect x="{410 + 118 * c}" y="{250 + 118 * r}" width="96" height="96" rx="10" fill="#EFE6D2"/>' for r in range(4) for c in range(5)),
           (0.05, dur + 1), rig(690, 740, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (1.4, "skeptical"), (5.8, "happy")], (190, 1010), 0.6, False, "cam")
    s += pill("nd", 230, 200, "Not dedicated", 46, NAVY, CREAM, (1.3, dur + 1))
    for i, (r, c, t) in enumerate(((0, 3, 3.5), (2, 1, 4.4), (3, 4, 5.2))):
        x, y = 410 + 118 * c, 250 + 118 * r
        s += g(f"d{i}", video_card(x + 8, y + 18, 80, NAVY), (t, dur + 1), rig(x + 48, y + 96, 4, 1.2))
    s += g("bulb", f'<circle cx="690" cy="860" r="70" fill="{GOLD}"/><rect x="660" y="920" width="60" height="50" rx="8" fill="{NAVY}"/>', (5.8, dur + 1),
           rig(690, 970, 5, 1.3))
    return s + "</svg>\n"


def talks():
    dur = 6.0
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "happy")], (230, 1010), 0.62, False, "cam")
    s += head(CLIENT, [(0.05, "neutral"), (4.0, "happy")], (850, 1010), 0.62, True, "cl")
    s += pill("cs", 540, 150, "Consultative selling", 54, NAVY, CREAM, (1.3, dur + 1))
    for i, (x, t, mine) in enumerate(((110, 2.8, 1), (640, 3.5, 0), (170, 4.2, 1), (700, 4.9, 0))):
        y = 300 + 70 * i
        s += g(f"b{i}", f'<rect x="{x}" y="{y}" width="280" height="110" rx="36" fill="{[WHITE, ORANGE][mine]}"/>'
                        + centered(x + 140, y + 75, str(i + 1), 62, [NAVY, CREAM][mine]), (t, dur + 1), rig(x + 140, y + 110, 3, 1.0))
    return s + "</svg>\n"


def right():
    dur = 5.5
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (0.9, "happy")], (270, 1010), 0.62, False, "cam")
    s += pill("rp", 280, 200, "Right person", 54, NAVY, CREAM, (0.3, dur + 1))
    s += check("k1", 430, 290, 0.9, dur, 90)
    s += g("co", building(640, 880, 340, 470, ORANGE, CREAM, 3), (2.8, dur + 1), rig(810, 880, 1, 0.5))
    s += pill("rc", 810, 300, "Right company", 50, NAVY, CREAM, (3.3, dur + 1))
    s += check("k2", 930, 380, 3.8, dur, 90)
    return s + "</svg>\n"


def proposal():
    dur = 9.3
    s = root(dur, "1,0,0")
    s += head(CLIENT, [(0.05, "neutral"), (2.6, "surprised"), (6.0, "happy")], (190, 1010), 0.55, False, "cl")
    big = doc(380, 140, 600, 760, "Proposal", 0)
    s += g("drop", big.replace('y="140"', 'y="-200"', 1), (2.4, 2.5))
    s += g("prop", big, (2.5, dur + 1), rig(680, 900, 2, 0.6))
    for i in range(12):
        s += g(f"l{i}", f'<rect x="420" y="{290 + 46 * i}" width="{500 - 90 * (i % 3)}" height="16" rx="8" fill="{GREY}"/>', (2.8 + 0.18 * i, dur + 1))
    s += pill("gw", 680, 520, "Great work", 54, ORANGE, CREAM, (4.9, dur + 1))
    s += pill("oc", 700, 700, "Outcomes", 54, NAVY, CREAM, (6.8, dur + 1))
    for i, t in enumerate((8.0, 8.4, 8.8)):                      # "and so on and so on": more pages behind it
        s += g(f"pg{i}", f'<rect x="{390 + 20 * (i + 1)}" y="{900 + 12 * i}" width="600" height="18" rx="6" fill="{[WHITE, CREAM, WHITE][i]}" stroke="{GREY}" stroke-width="3"/>',
               (t, dur + 1))
    return s + "</svg>\n"


def passion():
    dur = 6.4
    s = root(dur, "1,0,0")
    s += g("prop", doc(560, 160, 420, 560, "Proposal", 7), (0.05, dur + 1), rig(770, 720, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (2.8, "excited"), (4.8, "worried")], (230, 1010), 0.66, False, "cam")
    s += pill("ca", 540, 860, "Doesn't come across", 50, NAVY, CREAM, (0.6, dur + 1))
    s += steps("ht", lambda x, y: heart(x, y, 0.9), [(300, 420), (400, 360), (500, 330), (540, 340)], 3.0, 3.9, 3.3, r=lambda x, y: rig(x, y, 5, 1.3))
    s += steps("hb", lambda x, y: heart(x, y, 0.8), [(470, 470), (420, 580)], 4.3, 4.6, dur, r=lambda x, y: rig(x, y, 5, 1.3))
    s += pill("pa", 300, 200, "Passion", 54, ORANGE, CREAM, (3.4, dur + 1))
    s += xmark("x", 770, 440, (4.6, dur + 1), 110)
    return s + "</svg>\n"


def attach():
    dur = 5.0
    s = root(dur, "1,0,0")
    pack = doc(300, 260, 420, 540, "Proposal", 7)
    s += g("prop", pack, (0.05, 2.4), rig(510, 800, 1, 0.5))
    s += steps("vid", lambda x, y: video_card(x, y, 260), [(760, 120), (680, 200), (600, 230)], 0.9, 1.5, 1.4, r=lambda x, y: rig(x + 130, y + 160, 3, 1.0))
    s += g("clip", f'<rect x="640" y="200" width="30" height="110" rx="15" fill="none" stroke="{GREY}" stroke-width="10"/>', (1.5, 2.4))
    s += pill("inc", 540, 930, "+ a video", 56, ORANGE, CREAM, (1.4, 2.4))
    s += steps("env", lambda x, y: envelope(x, y, 360), [(360, 440), (480, 360), (620, 260), (760, 160)], 2.4, 3.4, dur, r=lambda x, y: rig(x + 180, y + 220, 3, 1.0))
    s += bubble("hey", 160, 640, 300, 130, "Hey!", 80, (3.5, dur + 1), (-1, 1))
    s += head(CAM_P, [(3.4, "excited")], (300, 1060), 0.4, False, "cam")
    return s + "</svg>\n"


def vision():
    dur = 5.8
    s = root(dur, "1,0,0")
    s += g("win", window(80, 130, 620, 470, "Video", WHITE, NAVY), (0.05, dur + 1), rig(390, 600, 1, 0.5))
    s += head(CAM_P, [(0.05, "happy"), (1.8, "excited")], (390, 590), 0.5, False, "cam")
    s += head(CLIENT, [(0.05, "neutral"), (2.0, "happy"), (4.0, "excited")], (850, 1010), 0.62, True, "cl")
    s += pill("vi", 390, 720, "Vision", 60, ORANGE, CREAM, (0.9, dur + 1))
    s += pill("ex", 390, 860, "So excited", 52, NAVY, CREAM, (2.0, dur + 1))
    for i, (x, y, t) in enumerate(((700, 300, 3.0), (760, 220, 3.3), (650, 200, 3.6))):
        s += g(f"sp{i}", f'<path d="M{x} {y - 30} L{x + 9} {y - 9} L{x + 30} {y} L{x + 9} {y + 9} L{x} {y + 30} L{x - 9} {y + 9} L{x - 30} {y} L{x - 9} {y - 9}Z" fill="{GOLD}"/>',
               (t, dur + 1), rig(x, y + 30, 8, 1.6))
    s += pill("pw", 840, 160, "Powerful", 54, GOLD, NAVY, (5.3, dur + 1))
    return s + "</svg>\n"


def jump():
    dur = 6.4
    s = root(dur, "1,0,0")
    s += g("win", window(160, 120, 760, 620, "Proposal video", WHITE, NAVY), (0.05, dur + 1), rig(540, 740, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (1.0, "surprised"), (3.0, "happy")], (430, 735), 0.62, False, "cam")
    s += steps("pk", lambda x, y: cat(x, y, 1.05), [(1060, 1080), (960, 920), (840, 800), (760, 735)], 0.3, 1.0, dur, r=lambda x, y: rig(x - 60, y, 3, 1.1))
    s += g("rs", f'<rect x="250" y="800" width="300" height="110" rx="20" fill="{GREY}"/>' + centered(400, 875, "Restart?", 50, NAVY), (2.6, dur + 1), rig(400, 910, 2, 0.8))
    s += xmark("x", 400, 855, (4.3, dur + 1), 60)
    s += g("play", f'<circle cx="760" cy="855" r="60" fill="{ORANGE}"/><path d="M740 825 L790 855 L740 885Z" fill="{CREAM}"/>', (5.0, dur + 1), rig(760, 915, 4, 1.0))
    return s + "</svg>\n"


def views():
    dur = 6.9
    s = root(dur, "1,0,0")
    s += steps("env", lambda x, y: envelope(x, y, 220) + video_card(x + 50, y + 20, 120, ORANGE), [(80, 600), (220, 500), (360, 420), (500, 380)], 0.1, 1.6, 2.0,
               r=lambda x, y: rig(x + 110, y + 140, 3, 1.0))
    s += g("co", building(620, 880, 340, 560, NAVY, BLUE, 3), (2.8, dur + 1), rig(790, 880, 1, 0.5))
    s += pill("cp", 790, 230, "A company", 50, ORANGE, CREAM, (3.0, dur + 1))
    s += g("v1", counter(120, 300, 1, 400, "view"), (5.2, 5.7), rig(320, 430, 2, 0.8))
    s += g("v2", counter(120, 300, 2, 400, "views"), (5.7, dur + 1), rig(320, 430, 2, 0.8))
    s += pill("us", 320, 560, "Usually", 48, NAVY, CREAM, (5.4, dur + 1))
    return s + "</svg>\n"


def forwarded():
    dur = 10.7
    s = root(dur, "1,0,0")
    s += g("win", window(80, 120, 420, 330, "Video", WHITE, NAVY) + cat(360, 450, 0.62), (0.05, dur + 1), rig(290, 450, 1, 0.5))
    for i, (v, t0) in enumerate(((2, 0.05), (5, 4.4), (12, 5.0), (20, 5.6), (30, 6.1))):
        t1 = (0.05, 4.4, 5.0, 5.6, 6.1, dur + 1)[i + 1]
        s += g(f"n{i}", counter(560, 200, v, 440), (t0, t1), rig(780, 330, 2 + i, 0.9 + 0.1 * i))
    s += pill("wow", 780, 470, "Forwarded", 52, ORANGE, CREAM, (6.6, dur + 1))
    heads = ((2, 160, 0.2), (8, 360, 0.2), (CLIENT, 560, 0.2), (3, 760, 0.2), (9, 960, 0.2))
    for i, (p, x, _) in enumerate(heads):
        s += head(p, [(7.4 + 0.15 * i, "neutral"), (9.4, "happy")], (x, 1010), 0.32, i % 2 == 1, f"h{i}")
    hop = [(120, 680), (330, 640), (530, 680), (730, 640), (930, 680)]
    s += steps("env", lambda x, y: envelope(x - 60, y - 40, 130), hop, 8.2, 10.4, dur, r=lambda x, y: rig(x, y + 40, 4, 1.2))
    return s + "</svg>\n"


def profit():
    dur = 3.4
    s = root(dur, "1,0,0")
    for i in range(9):
        x, y = 300 + 120 * (i % 4) + 60 * (i // 4 % 2), 860 - 70 * (i // 4)
        s += g(f"c{i}", f'<circle cx="{x}" cy="{y}" r="56" fill="{GOLD}"/><circle cx="{x}" cy="{y}" r="40" fill="none" stroke="{NAVY}" stroke-width="5"/>' + label(x - 18, y + 22, "$", 60),
               (0.1 + 0.15 * i, dur + 1), rig(x, y + 56, 6, 1.3))
    s += pill("vp", 540, 220, "Very profitable", 60, NAVY, CREAM, (0.6, dur + 1))
    s += check("ok", 860, 400, 1.8, dur, 110)
    return s + "</svg>\n"


def train():
    dur = 6.4
    s = root(dur, "1,0,0")
    camr = (f'<rect x="760" y="420" width="260" height="170" rx="22" fill="{NAVY}"/><rect x="830" y="390" width="90" height="40" rx="8" fill="{NAVY}"/>'
            f'<circle cx="890" cy="505" r="60" fill="{BLUE}"/><circle cx="890" cy="505" r="30" fill="{NAVY}"/>'
            f'<path d="M890 590 L830 860 M890 590 L950 860" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/>')
    s += g("cam", camr, (0.05, dur + 1), rig(890, 860, 1, 0.5))
    s += pill("tr", 300, 200, "Train your pet", 56, ORANGE, CREAM, (1.5, dur + 1))
    s += steps("pk", lambda x, y: cat(x, y, 1.1, 30), [(160, 900), (260, 880), (360, 900), (460, 880), (560, 900)], 0.6, 3.2, dur, r=lambda x, y: rig(x - 60, y, 3, 1.1))
    for k in range(3):
        s += g(f"rec{k}", f'<circle cx="985" cy="445" r="14" fill="{ORANGE}"/>', (3.4 + 0.6 * k, 3.7 + 0.6 * k))
    s += pill("vp", 700, 330, "Video proposal", 50, NAVY, CREAM, (5.0, dur + 1))
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("My secret", "weapon", 2.4, 0.8)), ("t2", lambda: two("I closed", "that deal", 2.4, 0.6)),
                 ("b1", videos), ("b2", calendar), ("b3", talks), ("b4", right), ("b5", proposal), ("b6", passion), ("b7", attach),
                 ("b8", vision), ("b9", jump), ("b10", views), ("b11", forwarded), ("b12", profit), ("b13", train)):
        open(os.path.join(HERE, f"scenes/pk-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/pk-{n}.svg")
