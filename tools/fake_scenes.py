"""B-roll for "Don't fake it on camera" (video 3 of "five different videos to edit") -> scenes/fke-*.svg

usage: python3 tools/fake_scenes.py
Times in ORIGINAL footage time (the five-video file) live in videos/fake.json. Cat at the lower right: titles left, under 500 px wide.
b1 smile     a camera points at Cam; he smiles, drops it, forces it back on (rev2: the tiny sweat drop read as a glitch, removed)
b2 eyes      big eyes for "the algorithm": a robot with a fishing hook dangles a heart
b3 thumb     a thumbnail frame: Cam's face gets more intense; red arrows and "!!!"
b4 mood      first half: Cam amped up, a "Great" check; second half: Cam tired under a rain cloud
b5 feed      the feed scrolls
b6 real      one calm card in the feed: Cam's real face; a heart
t1 fake      Faking it / on camera
t2 mean      Say it / how you mean it
"""
import os
from leon_scenes import root, title_root, tag, calm, robot, check, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, GOLD
from repetition_scenes import pill, card
from report_scenes import centered
from trash_scenes import heart

BLUE = "#5E7A94"


def camera(x, y):
    return (f'<rect x="{x}" y="{y}" width="260" height="170" rx="20" fill="{NAVY}"/><rect x="{x + 30}" y="{y - 30}" width="80" height="40" rx="8" fill="{NAVY}"/>'
            f'<circle cx="{x + 130}" cy="{y + 85}" r="58" fill="{BLUE}"/><circle cx="{x + 130}" cy="{y + 85}" r="30" fill="{NAVY}"/>'
            f'<circle cx="{x + 220}" cy="{y + 30}" r="12" fill="{ORANGE}"/>')


# ---- b-roll ----

def smile():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += g("cam", camera(90, 380), (0.05, dur + 1), rig(220, 550, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (0.5, "happy"), (1.6, "tired"), (2.4, "excited")], (700, 990), 1.0, False, "cam")
    s += g("rec", centered(220, 330, "REC", 44, ORANGE), (0.3, dur + 1))
    return s + "</svg>\n"


def eyes():
    dur = 4.4
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (0.8, "surprised")], (330, 990), 1.0, False, "cam")
    s += g("bot", robot(820, 260, 3.4), (1.6, dur + 1), rig(820, 340, 4, 0.9))
    s += pill("alg", 820, 90, "The algorithm", 46, NAVY, CREAM, (2.1, dur + 1))
    s += g("line", f'<path d="M900 300 L900 560" stroke="{NAVY}" stroke-width="6"/><path d="M900 560 q0 40 -30 40 q-25 0 -25 -25" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>',
           (2.4, dur + 1), rig(900, 300, 5, 0.8))
    s += heart("bait", 870, 630, (2.6, dur + 1), 1.4)
    return s + "</svg>\n"


def thumb():
    dur = 3.4
    s = root(dur, "1,0,0")
    s += g("frame", f'<rect x="120" y="140" width="840" height="560" rx="24" fill="{ORANGE}"/><rect x="150" y="170" width="780" height="500" rx="12" fill="#FFFDF6"/>',
           (0.05, dur + 1), rig(540, 700, 1, 0.5))
    s += head(CAM_P, [(0.05, "happy"), (1.0, "excited"), (2.0, "surprised")], (420, 690), 0.85, False, "cam")
    s += g("ex", centered(250, 330, "!!!", 120, ORANGE), (1.0, dur + 1), rig(250, 340, 8, 1.6))
    for i, (x1, y1, x2, y2, t0) in enumerate(((880, 620, 600, 540, 1.5), (880, 240, 600, 400, 2.0))):
        s += g(f"ar{i}", f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{NAVY}" stroke-width="22" stroke-linecap="round"/><circle cx="{x2}" cy="{y2}" r="22" fill="{NAVY}"/>',
               (t0, dur + 1), rig(x1, y1, 4, 1.0))
    s += pill("tn", 540, 840, "Thumbnail", 56, NAVY, CREAM, (0.3, dur + 1))
    return s + "</svg>\n"


def mood():
    dur = 5.3
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "excited"), (2.5, "tired")], (400, 990), 1.0, False, "cam")
    s += check("ok", 720, 300, 0.9, 1.5, 110)          # check() shows t0..dur+1: dur 1.5 ends it at 2.5
    s += pill("great", 780, 200, "Great", 66, ORANGE, CREAM, (0.9, 2.5))
    s += g("cloud", f'<ellipse cx="420" cy="230" rx="200" ry="90" fill="{GREY}"/><circle cx="330" cy="190" r="90" fill="{GREY}"/><circle cx="480" cy="170" r="110" fill="{GREY}"/>',
           (2.7, dur + 1), rig(420, 320, 2, 0.5))
    for i in range(5):
        x = 300 + 55 * i
        s += g(f"rain{i}", f'<rect x="{x}" y="{340 + 30 * (i % 2)}" width="12" height="50" rx="6" fill="#5A8BB3"/>', (3.0 + 0.1 * i, dur + 1), rig(x, 400, 10, 2.0))
    return s + "</svg>\n"


def feed():
    dur = 3.0
    s = root(dur, "1,0,0")
    n = 6
    for k in range(n):
        dy = -90 * k
        body = "".join(card(90 + 470 * c, 120 + 230 * r + dy + (110 if c else 0)) for r in range(6) for c in range(2))
        s += g(f"feed{k}", body, (dur * k / n, dur * (k + 1) / n if k < n - 1 else dur + 1))
    return s + "</svg>\n"


def real():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += g("post", f'<rect x="170" y="100" width="740" height="720" rx="24" fill="#FFFDF6"/><rect x="200" y="130" width="680" height="520" rx="14" fill="#8CBDDC"/>'
                   + "".join(f'<rect x="210" y="{680 + 34 * i}" width="{560 - 120 * i}" height="14" rx="7" fill="{GREY}"/>' for i in range(3)),
           (0.05, dur + 1), rig(540, 820, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (2.2, "happy")], (540, 650), 0.85, False, "cam")
    s += heart("like", 820, 760, (1.6, dur + 1), 1.6)
    s += pill("real", 300, 120, "Real", 54, ORANGE, CREAM, (2.4, dur + 1), -5)
    return s + "</svg>\n"


# ---- titles (left, narrow: the cat sits at the lower right) ----

def t_fake():
    dur = 2.6
    s = title_root(dur)
    s += tag("fk", "Faking it", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("oc", "on camera", 60, 885, 86, 2, 1.4, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_mean():
    dur = 2.5
    s = title_root(dur)
    s += tag("say", "Say it", 60, 770, 80, -2, 0.05, dur + 1)[0]
    s += tag("mean", "how you mean it", 60, 885, 62, 2, 0.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_fake), ("t2", t_mean), ("b1", smile), ("b2", eyes), ("b3", thumb), ("b4", mood), ("b5", feed), ("b6", real)):
        open(os.path.join(HERE, f"scenes/fke-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/fke-{n}.svg")
