"""B-roll for "The tool is the teacher" take 2 (raw 2026-11-02 15-23-49; replaces the 2026-10-30 take) -> scenes/tc2-*.svg

usage: python3 tools/teacher2_scenes.py
Times in ORIGINAL raw-take time live in videos/teacher2.json. Cat at the lower right: titles left, under 500 px wide.
Cam on camera (2026-11-02): the last animations were "ok, not great". So every beat here keeps moving: steps, scrolls, typing.
b1 lead      Cam "AI lead"; coworkers pop in; the robot drops in; lines connect; $ coins rise; "Business value"
b2 history   a timeline (book, bulb, screen, robot) scrolls left; "First time" pill; the robot says "Ask me"
b3 ask       Cam asks "How do I...?"; the robot's answer card fills line by line; a check
b4 swamped   coworkers around Cam; "?" marks fly in one by one and pile up; Cam gets tired
b5 tools     "Ask" header; Claude, ChatGPT, Any AI tool pills pop in; the robot hops along under them
b6 help      a thick HELP binder thuds down; Cam bored; a red X
b7 forums    Forum and Reddit windows pop in and scroll; Cam confused; a tutorial video plays (progress bar)
b8 remind    Cam with a megaphone; coworkers; a sticky note "Ask AI first"; they smile
b9 start     "Won't always work" with an X; a flag "Start here"; the robot walks to the flag
t1 The tool is / the teacher (used twice)
t2 Ask the AI / itself
"""
import os
from leon_scenes import root, title_root, tag, calm, robot, check, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bubble

BLUE = "#8CBDDC"
WHITE = "#FFFDF6"


def steps(gid, body_at, path, t0, t1, dur, r=None):
    """One element walking along `path` (list of (x, y)), one step per position from t0 to t1, then holding."""
    out, n = "", len(path)
    for i, (x, y) in enumerate(path):
        a = t0 + (t1 - t0) * i / max(n - 1, 1)
        b = t0 + (t1 - t0) * (i + 1) / max(n - 1, 1) if i < n - 1 else dur + 1
        out += g(f"{gid}{i}", body_at(x, y), (a, b), rig(x, y + 60, 5, 1.2) if r is None else r(x, y))
    return out


def coin(x, y):
    return f'<circle cx="{x}" cy="{y}" r="34" fill="{GOLD}"/><circle cx="{x}" cy="{y}" r="24" fill="none" stroke="{NAVY}" stroke-width="4"/>' + label(x - 13, y + 15, "$", 42)


def window(x, y, w, h, title, fill=WHITE, bar=NAVY):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}"/><rect x="{x}" y="{y}" width="{w}" height="56" rx="16" fill="{bar}"/>'
            f'<rect x="{x}" y="{y + 36}" width="{w}" height="20" fill="{bar}"/>' + label(x + 24, y + 40, title, 32, CREAM))


def lines(x, y, n, w=300, gap=34, c=GREY, k0=0):
    return "".join(f'<rect x="{x}" y="{y + gap * i}" width="{w - 70 * ((i + k0) % 3)}" height="14" rx="7" fill="{c}"/>' for i in range(n))


# ---- b-roll ----

def lead():
    dur = 5.5
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (2.4, "happy")], (220, 1010), 0.8, False, "cam")
    s += pill("ai", 220, 520, "AI lead", 56, ORANGE, CREAM, (0.2, dur + 1))
    heads = ((2, 640, 1.2), (5, 800, 1.4), (3, 960, 1.6))
    for i, (p, x, t0) in enumerate(heads):
        s += head(p, [(t0, "neutral"), (3.4, "happy")], (x, 1010), 0.4, True, f"co{i}")
    s += steps("bot", lambda x, y: robot(x, y, 3.0), [(800, 120), (800, 230), (800, 330)], 2.2, 2.6, dur)
    for i, (p, x, t0) in enumerate(heads):
        s += g(f"ln{i}", f'<path d="M800 420 L{x} 760" stroke="{NAVY}" stroke-width="10" stroke-dasharray="4 22" stroke-linecap="round"/>', (3.1 + 0.15 * i, dur + 1))
    for i, (p, x, t0) in enumerate(heads):                     # coins rise from each coworker
        s += steps(f"cn{i}", coin, [(x, 700), (x - 20, 600), (x - 40, 500)], 4.5 + 0.12 * i, 4.9 + 0.12 * i, dur)
    s += pill("val", 760, 560, "Business value", 54, NAVY, CREAM, (5.0, dur + 1))
    return s + "</svg>\n"


def book(x, y):
    return f'<rect x="{x - 60}" y="{y - 80}" width="120" height="160" rx="8" fill="{ORANGE}"/><rect x="{x - 60}" y="{y - 80}" width="18" height="160" fill="{NAVY}"/>'


def bulb(x, y):
    return f'<circle cx="{x}" cy="{y - 20}" r="62" fill="{GOLD}"/><rect x="{x - 30}" y="{y + 36}" width="60" height="50" rx="8" fill="{NAVY}"/>'


def screen(x, y):
    return (f'<rect x="{x - 90}" y="{y - 80}" width="180" height="120" rx="10" fill="{NAVY}"/><rect x="{x - 74}" y="{y - 64}" width="148" height="88" rx="4" fill="{BLUE}"/>'
            f'<rect x="{x - 12}" y="{y + 40}" width="24" height="34" fill="{NAVY}"/><rect x="{x - 60}" y="{y + 70}" width="120" height="16" rx="8" fill="{NAVY}"/>')


def history():
    dur = 3.2
    s = root(dur, "1,0,0")
    icons = (book, bulb, screen, lambda x, y: robot(x, y, 3.0))
    n = 9
    for k in range(n):                                          # the timeline scrolls left in steps, then stops on the robot
        dx = -95 * k
        body = f'<rect x="{0 + dx}" y="636" width="2200" height="16" rx="8" fill="{NAVY}"/>'
        for i, f in enumerate(icons):
            x = 260 + 380 * i + dx
            body += f'<circle cx="{x}" cy="644" r="18" fill="{NAVY}"/>' + f(x, 480)
        t0, t1 = 0.05 + 0.22 * k, (0.05 + 0.22 * (k + 1) if k < n - 1 else dur + 1)
        s += g(f"tl{k}", body, (t0, t1))
    s += pill("first", 680, 820, "First time in history", 56, ORANGE, CREAM, (2.0, dur + 1))
    s += bubble("me", 760, 170, 250, 110, "Ask me", 54, (2.5, dur + 1), (-1, 1))
    return s + "</svg>\n"


def ask():
    dur = 4.3
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (3.5, "happy")], (220, 1010), 0.8, False, "cam")
    s += bubble("q", 90, 170, 420, 120, "How do I...?", 56, (0.25, dur + 1))
    s += g("bot", robot(820, 300, 3.4), (0.6, dur + 1), rig(820, 370, 6, 1.2))
    s += g("card", f'<rect x="520" y="480" width="480" height="430" rx="18" fill="{WHITE}"/>', (1.8, dur + 1), rig(760, 910, 1, 0.5))
    for i in range(4):
        t0 = 2.0 + 0.35 * i
        s += g(f"n{i}", label(560, 562 + 92 * i, f"{i + 1}.", 44, ORANGE) + f'<rect x="620" y="{532 + 92 * i}" width="{300 - 50 * (i % 2)}" height="18" rx="9" fill="{GREY}"/>',
               (t0, dur + 1))
    s += check("ok", 930, 470, 3.5, dur, 70)
    return s + "</svg>\n"


def swamped():
    dur = 3.1
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.4, "worried"), (2.3, "tired")], (540, 1010), 0.75, False, "cam")
    for i, (p, x, y, t0, fl) in enumerate(((2, 150, 560, 0.1, False), (5, 930, 560, 0.25, True), (8, 150, 1010, 0.4, False), (3, 930, 1010, 0.55, True))):
        s += head(p, [(t0, "confused")], (x, y), 0.36, fl, f"co{i}")
    marks = ((380, 230, 0.8), (700, 200, 1.1), (330, 420, 1.4), (760, 400, 1.7), (540, 140, 2.0), (450, 330, 2.3), (640, 300, 2.5))
    for i, (x, y, t0) in enumerate(marks):                      # each "?" flies in from its coworker side, then sticks
        sx = -80 if x < 540 else 80
        s += g(f"qa{i}", centered(x + sx, y + 60, "?", 110, ORANGE), (t0, t0 + 0.12))
        s += g(f"q{i}", centered(x, y, "?", 110, ORANGE if i % 2 == 0 else NAVY), (t0 + 0.12, dur + 1), rig(x, y, 8, 1.3))
    return s + "</svg>\n"


def tools():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += pill("ask", 540, 170, "Ask", 90, NAVY, CREAM, (0.05, dur + 1))
    names = (("Claude", 300, 0.35), ("ChatGPT", 760, 1.1), ("Any AI tool", 540, 1.75))
    for i, (n, x, t0) in enumerate(names):
        y = 420 if i < 2 else 620
        s += pill(f"p{i}", x, y, n, 66, [ORANGE, BLUE, GOLD][i], [CREAM, NAVY, NAVY][i], (t0, dur + 1), [-3, 3, -2][i])
    s += steps("bot", lambda x, y: robot(x, y, 2.6), [(300, 860), (420, 820), (540, 860), (660, 820), (760, 860)], 0.5, 2.3, dur)
    return s + "</svg>\n"


def help_files():
    dur = 3.1
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.4, "tired")], (840, 1010), 0.75, True, "cam")
    binder = (f'<rect x="150" y="300" width="460" height="560" rx="16" fill="{NAVY}"/><rect x="190" y="340" width="380" height="480" rx="8" fill="{CREAM}"/>'
              + centered(380, 480, "HELP", 110, NAVY) + lines(230, 560, 6, 300))
    s += g("drop", binder.replace('y="300"', 'y="60"').replace('y="340"', 'y="100"'), (0.6, 0.7))   # one frame high, then the thud
    s += g("bind", binder, (0.7, dur + 1), rig(380, 860, 2, 0.6))
    for i, (x1, y1, x2, y2) in enumerate(((120, 900, 60, 940), (640, 900, 700, 940), (380, 900, 380, 960))):
        s += g(f"dust{i}", f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{GREY}" stroke-width="12" stroke-linecap="round"/>', (0.75, 1.3))
    s += xmark("x", 380, 580, (1.6, dur + 1), 150)
    s += pill("suck", 380, 180, "Help files", 60, ORANGE, CREAM, (0.9, dur + 1))
    return s + "</svg>\n"


def forums():
    dur = 5.2
    s = root(dur, "1,0,0")
    for k in range(6):                                           # both windows scroll while he hunts for the answer
        t0, t1 = 0.3 + 0.5 * k, (0.3 + 0.5 * (k + 1) if k < 5 else dur + 1)
        body = window(60, 110, 470, 400, "Forum") + lines(100, 200 + 0, 8, 360, 34, GREY, k)
        s += g(f"fo{k}", body, (max(t0, 0.3), t1), rig(295, 510, 1, 0.5))
    for k in range(5):
        t0, t1 = 1.1 + 0.5 * k, (1.1 + 0.5 * (k + 1) if k < 4 else dur + 1)
        s += g(f"re{k}", window(560, 160, 470, 400, "Reddit", WHITE, ORANGE) + lines(600, 250, 8, 360, 34, GREY, k + 1), (t0, t1),
               rig(795, 560, 1, 0.5))
    s += head(CAM_P, [(1.5, "confused"), (4.0, "skeptical")], (230, 1010), 0.6, False, "cam")
    tut = window(500, 600, 520, 330, "Tutorial", WHITE, NAVY) + f'<path d="M720 690 L820 760 L720 830Z" fill="{ORANGE}"/>'
    s += g("tut", tut + f'<rect x="530" y="890" width="460" height="14" rx="7" fill="{GREY}"/>', (3.6, dur + 1), rig(760, 930, 1, 0.5))
    for k in range(6):                                           # the progress bar crawls
        a = 3.8 + 0.25 * k
        s += g(f"pb{k}", f'<rect x="530" y="890" width="{40 + 30 * k}" height="14" rx="7" fill="{ORANGE}"/>', (a, a + 0.25 if k < 5 else dur + 1))
    return s + "</svg>\n"


def megaphone(x, y):
    return (f'<path d="M{x} {y - 30} L{x + 160} {y - 90} L{x + 160} {y + 90} L{x} {y + 30} Z" fill="{ORANGE}"/>'
            f'<rect x="{x - 40}" y="{y - 34}" width="50" height="68" rx="10" fill="{NAVY}"/>')


def remind():
    dur = 4.0
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "excited")], (200, 1010), 0.7, False, "cam")
    s += g("mega", megaphone(330, 640), (0.1, dur + 1), rig(330, 640, 6, 1.4))
    for i, (x1, y1, x2, y2, t0) in enumerate(((520, 560, 580, 520, 0.3), (530, 640, 610, 640, 0.5), (520, 720, 580, 760, 0.7))):
        s += g(f"w{i}", f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>', (t0, dur + 1), rig(x1, y1, 8, 1.6))
    for i, (p, x, t0) in enumerate(((2, 690, 0.5), (5, 850, 0.7), (8, 1000, 0.9))):
        s += head(p, [(t0, "neutral"), (3.2, "happy")], (x, 1010), 0.38, True, f"co{i}")
    s += g("note", f'<rect x="600" y="180" width="380" height="300" fill="{GOLD}" transform="rotate(3 790 330)"/>'
                   + centered(790, 310, "Ask AI", 76, NAVY) + centered(790, 400, "first", 76, ORANGE), (2.7, dur + 1), rig(790, 180, 4, 1.0))
    s += g("bot", robot(970, 160, 1.8), (3.3, dur + 1), rig(970, 200, 8, 1.4))
    return s + "</svg>\n"


def start():
    dur = 3.7
    s = root(dur, "1,0,0")
    s += pill("not", 540, 170, "Won't always work", 58, GREY, NAVY, (0.3, dur + 1))
    s += xmark("x", 860, 170, (1.0, dur + 1), 40)
    s += g("path", "".join(f'<rect x="{90 + 90 * i}" y="800" width="54" height="14" rx="7" fill="{NAVY}"/>' for i in range(10)), (0.05, dur + 1))
    s += g("flag", f'<rect x="300" y="420" width="16" height="400" fill="{NAVY}"/><path d="M316 430 L560 490 L316 550Z" fill="{ORANGE}"/>', (2.0, dur + 1),
           rig(308, 820, 4, 1.0))
    s += pill("here", 430, 340, "Start here", 60, NAVY, CREAM, (2.4, dur + 1))
    s += steps("bot", lambda x, y: robot(x, y, 2.6), [(920, 740), (800, 720), (680, 740), (560, 720), (440, 740)], 1.4, 3.2, dur)
    return s + "</svg>\n"


# ---- titles (left, narrow: the cat sits at the lower right) ----

def two(a, b, dur, t2=1.0, size2=70):
    s = title_root(dur)
    s += tag("ta", a, 60, 620, 80, -2, 0.05, dur + 1)[0]
    s += tag("tb", b, 60, 735, size2, 2, t2, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("The tool is", "the teacher", 2.1, 1.0, 60)), ("t2", lambda: two("Ask the AI", "itself", 2.0, 0.6)),
                 ("b1", lead), ("b2", history), ("b3", ask), ("b4", swamped), ("b5", tools), ("b6", help_files), ("b7", forums),
                 ("b8", remind), ("b9", start)):
        open(os.path.join(HERE, f"scenes/tc2-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/tc2-{n}.svg")
