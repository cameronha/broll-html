"""B-roll for "Slop button" (2026-08-20 footage) -> scenes/slop-*.svg

usage: python3 tools/slop_scenes.py
Reuses the Leon / LinkedIn / investors parts; the paper-pile scene is reused as a file (li-b2) in videos/slop.json.
t1 makers    To the makers of / Gmail
t2 pages     5-page email -> 1 paragraph
b1 spew      the agent spews an endless paper streamer into an inbox
b2 toolbar   an inbox toolbar: Archive, Spam ... and a new red Slop button pops in
b3 press     a big paper hand presses Slop
b4 sender    the sender's email gets a SLOP stamp; the sender looks worried
t3 slop      "Slop."
b5 ideas     four people, light bulbs pop over their heads
t4 help      Help us out, / Gmail.
"""
import os
import cast_scenes as CS
from leon_scenes import root, title_root, tag, robot, calm, CREAM, NAVY, ORANGE, INK, PAPER, HERE, shade
from linkedin_scenes import rig, g, sheet, GREY
from investors_scenes import head, label, GOLD

SKIN = "#F0B98F"


def button(gid, x, y, w, text, fill, ink, show=None, r=""):
    return g(gid, f'<rect x="{x}" y="{y + 10}" width="{w}" height="110" rx="20" fill="{shade(fill, 0.7)}"/>'
                  f'<rect x="{x}" y="{y}" width="{w}" height="110" rx="20" fill="{fill}"/>' + label(x + 34, y + 74, text, 60, ink), show, r)


def inbox(x, y):
    return (f'<rect x="{x}" y="{y}" width="300" height="200" rx="14" fill="{NAVY}"/><rect x="{x + 14}" y="{y + 14}" width="272" height="172" rx="8" fill="{CREAM}"/>'
            f'<path d="M{x + 14} {y + 22} L{x + 150} {y + 120} L{x + 286} {y + 22}" stroke="{NAVY}" stroke-width="12" fill="none" stroke-linejoin="round"/>')


# ---- b-roll ----

def spew():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += g("inbox", inbox(700, 470), None, rig(850, 670, 2, 0.6))
    s += g("agent", robot(230, 470, 4.2), None, rig(230, 560, 6, 1.6))
    for i in range(14):                                    # the streamer of pages unrolls from the agent toward the inbox
        x, y = 330 + 32 * i, 500 + (20 if i % 2 else -10) + 6 * i
        s += g(f"pg{i}", sheet(x, y, -18 + 36 * (i % 2)), (0.15 * i, dur + 1))
    return s + "</svg>\n"


def toolbar(press=False):
    dur = 3.3
    s = root(dur, "1,0,0")
    s += g("bar", f'<rect x="60" y="360" width="960" height="190" rx="24" fill="#FFFDF6"/>')
    s += button("arch", 84, 400, 300, "Archive", CREAM, NAVY)
    s += button("spam", 404, 400, 240, "Spam", NAVY, CREAM)
    if not press:
        s += button("slop0", 674, 400, 220, "Slop", ORANGE, CREAM, (1.4, 1.5), rig(784, 520, 0))
        s += button("slop", 664, 392, 240, "Slop", ORANGE, CREAM, (1.5, dur + 1), rig(784, 520, 3, 1.2))
        s += g("new", f'<rect x="820" y="310" width="140" height="60" rx="10" fill="{GOLD}"/>' + label(842, 354, "NEW", 40), (1.8, dur + 1), rig(890, 370, 5, 1.4))
        return s + "</svg>\n"
    # the press: the hand comes down at 1.0 s, the button sinks, then it springs back with a burst
    s += button("slop", 664, 392, 240, "Slop", ORANGE, CREAM, (0, 1.0))
    s += g("slop-dn", f'<rect x="664" y="414" width="240" height="100" rx="20" fill="{shade(ORANGE, 0.7)}"/>' + label(698, 480, "Slop", 60, CREAM), (1.0, 1.6))
    s += button("slop2", 664, 392, 240, "Slop", ORANGE, CREAM, (1.6, dur + 1), rig(784, 520, 3, 1.2))
    for k, (t0, t1, dy) in enumerate(((0, 0.6, -170), (0.6, 1.0, -60), (1.0, 1.6, 0), (1.6, dur + 1, -140))):
        y = 230 + dy + 170
        s += g(f"hand{k}", f'<rect x="749" y="{y - 260}" width="70" height="230" rx="30" fill="{SKIN}"/>'
                           f'<rect x="736" y="{y - 80}" width="96" height="110" rx="40" fill="{SKIN}"/>'
                           f'<rect x="762" y="{y + 10}" width="44" height="40" rx="20" fill="{SKIN}"/>', (t0, t1))
    for i, (dx, dy) in enumerate(((-150, -60), (160, -50), (-120, 160), (150, 150))):
        s += g(f"burst{i}", f'<line x1="{784 + dx * 0.6:.0f}" y1="{460 + dy * 0.6:.0f}" x2="{784 + dx:.0f}" y2="{460 + dy:.0f}" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/>', (1.05, 1.6))
    return s + "</svg>\n"


def sender():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += g("email", f'<rect x="540" y="230" width="380" height="480" rx="12" fill="#FFFDF6"/>'
                    + "".join(f'<rect x="580" y="{280 + 34 * i}" width="{300 - 60 * (i % 3)}" height="14" rx="7" fill="{GREY}"/>' for i in range(12)))
    s += g("stamp0", f'<rect x="520" y="360" width="420" height="170" rx="16" fill="none" stroke="{ORANGE}" stroke-width="18"/>'
                     + label(560, 480, "SLOP", 120, ORANGE), (0.9, 1.0))
    s += g("stamp", f'<rect x="560" y="380" width="340" height="140" rx="14" fill="none" stroke="{ORANGE}" stroke-width="16"/>'
                    + label(588, 482, "SLOP", 100, ORANGE), (1.0, dur + 1))
    s += head(1, [(0, "happy"), (1.1, "worried")], (270, 640), 0.55, True, "sender")
    return s + "</svg>\n"


def ideas():
    dur = 3.0
    s = root(dur, "1,0,0")
    for i, (p, x) in enumerate(((3, 170), (9, 420), (7, 670), (6, 910))):
        s += head(p, [(0, "neutral"), (0.4 + 0.3 * i, "excited")], (x, 720), 0.4, i < 2, f"p{i}")
        t = 0.4 + 0.3 * i
        s += g(f"bulb{i}", f'<circle cx="{x}" cy="380" r="56" fill="{GOLD}"/><rect x="{x - 24}" y="426" width="48" height="40" rx="8" fill="{GREY}"/>'
                           + "".join(f'<line x1="{x + 80 * dx:.0f}" y1="{380 + 80 * dy:.0f}" x2="{x + 110 * dx:.0f}" y2="{380 + 110 * dy:.0f}" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
                                     for dx, dy in ((-1, 0), (1, 0), (0, -1), (-0.7, -0.7), (0.7, -0.7))),
               (t, dur + 1), rig(x, 460, 6, 1.3))
    return s + "</svg>\n"


# ---- titles ----

def t_makers():
    dur = 2.6
    s = title_root(dur)
    s += tag("to", "To the makers of", 60, 740, 70, -2, 0.05, dur + 1)[0]
    s += tag("gm", "Gmail", 60, 850, 120, 2, 0.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_pages():
    dur = 4.3
    s = title_root(dur)
    s += tag("five", "5-page email", 60, 740, 90, -3, 0.3, dur + 1)[0]
    s += tag("one", "1 paragraph", 60, 880, 90, 2, 3.8, dur + 1, ORANGE, PAPER)[0]
    s += g("strike", f'<line x1="50" y1="800" x2="620" y2="770" stroke="{ORANGE}" stroke-width="16" stroke-linecap="round"/>', (3.8, dur + 1))
    return s + "</svg>\n"


def t_slop():
    dur = 1.6
    s = title_root(dur)
    s += tag("slop", "Slop.", 60, 780, 180, -4, 0.05, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_help():
    dur = 2.9
    s = title_root(dur)
    s += tag("help", "Help us out,", 60, 740, 96, -2, 1.6, dur + 1)[0]
    s += tag("gm2", "Gmail.", 60, 880, 120, 2, 1.9, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_makers), ("t2", t_pages), ("t3", t_slop), ("t4", t_help),
                 ("b1", spew), ("b2", toolbar), ("b3", lambda: toolbar(True)), ("b4", sender), ("b5", ideas)):
        open(os.path.join(HERE, f"scenes/slop-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/slop-{n}.svg")
