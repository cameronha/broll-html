"""B-roll for "Chief Taking the Trash Out Officer" (2026-08-11 footage) -> scenes/trash-*.svg

usage: python3 tools/trash_scenes.py
Reuses the Leon / LinkedIn / investors parts. Times in ORIGINAL footage time live in videos/trash.json.
b0 met       Cam meets a CEO across the frame; a "CEO" tag drops on him
t1 title     Chief / Taking the Trash Out / Officer
b1 linkedin  a leader posts thoughts; like counters pop
b2 trash     the CEO carries a trash bag to the bin, step by step; the lid flips
b3 loyalty   the CEO with his badge, the team turns happy, hearts pop on "loyalty"
t2 work      The unglamorous stuff / is part of the work
b4 badge     a name badge: "CEO" is struck out, "Chief Taking the Trash Out Officer" appears
"""
import os
import cast_scenes as CS
from leon_scenes import root, title_root, tag, calm, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P, shade
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, GOLD

CEO = 9


def heart(gid, x, y, show, s=1.0):
    return g(gid, f'<path d="M{x} {y + 30 * s:.0f} C{x - 50 * s:.0f} {y - 10 * s:.0f} {x - 20 * s:.0f} {y - 40 * s:.0f} {x} {y - 14 * s:.0f} '
                  f'C{x + 20 * s:.0f} {y - 40 * s:.0f} {x + 50 * s:.0f} {y - 10 * s:.0f} {x} {y + 30 * s:.0f}Z" fill="{ORANGE}"/>',
             show, rig(x, y + 30 * s, 6, 1.4))


def bag(x, y):
    """A black trash bag, center-bottom at (x, y)."""
    return (f'<path d="M{x - 70} {y} Q{x - 90} {y - 90} {x - 30} {y - 120} L{x + 30} {y - 120} Q{x + 90} {y - 90} {x + 70} {y}Z" fill="#2B2F36"/>'
            f'<path d="M{x - 26} {y - 118} L{x - 40} {y - 160} L{x} {y - 132} L{x + 40} {y - 160} L{x + 26} {y - 118}Z" fill="#2B2F36"/>')


def bin_(x, base, lid_open):
    body = f'<path d="M{x - 100} {base - 240} L{x + 100} {base - 240} L{x + 80} {base} L{x - 80} {base}Z" fill="{NAVY}"/>' + "".join(
        f'<rect x="{x - 50 + 40 * i}" y="{base - 210}" width="14" height="180" rx="7" fill="#2C4366"/>' for i in range(3))
    lid = (f'<rect x="{x - 112}" y="{base - 270}" width="224" height="34" rx="10" fill="{NAVY}"/>' if not lid_open else
           f'<rect x="{x - 112}" y="{base - 270}" width="224" height="34" rx="10" fill="{NAVY}" transform="rotate(-60 {x - 112} {base - 236})"/>')
    return body + lid


# ---- b-roll ----

def met():
    dur = 2.5
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0, "happy")], (300, 620), 0.55, True, "cam")
    s += head(CEO, [(0, "neutral"), (0.6, "happy")], (780, 620), 0.55, False, "ceo")
    s += tag("ceotag", "CEO", 700, 300, 90, -3, 0.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def linkedin():
    dur = 3.5
    s = root(dur, "1,0,0")
    s += g("post", f'<rect x="420" y="190" width="560" height="560" rx="18" fill="#FFFDF6"/>'
                   f'<rect x="460" y="230" width="70" height="70" rx="12" fill="#0A66C2"/>' + label(474, 284, "in", 46, CREAM)
                   + label(550, 278, "My thoughts on", 40) + label(550, 330, "leadership…", 40)
                   + "".join(f'<rect x="460" y="{390 + 44 * i}" width="{480 - 70 * (i % 3)}" height="16" rx="8" fill="{GREY}"/>' for i in range(7)))
    s += head(2, [(0, "happy"), (1.5, "excited")], (230, 600), 0.5, True, "poster")
    for i, (n, x, y, t) in enumerate((("+12", 470, 760, 0.8), ("+148", 640, 790, 1.5), ("+2.3K", 820, 760, 2.2))):
        s += g(f"like{i}", f'<rect x="{x - 20}" y="{y - 60}" width="{len(n) * 34 + 40}" height="80" rx="40" fill="{ORANGE}"/>' + label(x, y, n, 50, CREAM),
               (t, dur + 1), rig(x + 40, y + 20, 5, 1.3))
    return s + "</svg>\n"


def trash():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("bin", bin_(860, 760, False), (0, 2.3))
    s += g("bin-open", bin_(860, 760, True), (2.3, dur + 1))
    for i in range(6):                                   # the CEO walks the bag to the bin in hops
        t0, t1 = 0.35 * i, (0.35 * (i + 1) if i < 5 else 2.3)
        x = 180 + 90 * i; lift = 14 if i % 2 else 0
        s += head(CEO, [(t0, "happy" if i < 5 else "excited")], (x, 520 - lift), 0.45, True, f"walk{i}").replace(
            f'data-show="{t0},{dur + 1}"', f'data-show="{t0:.2f},{t1:.2f}"')
        s += g(f"bag{i}", bag(x + 120, 690 - lift), (t0, t1))
    s += head(CEO, [(2.3, "excited")], (630, 520), 0.45, True, "done")
    s += g("bag-in", bag(860, 560), (2.3, 2.5))
    for i, (dx, dy) in enumerate(((-120, -40), (120, -50), (0, -130))):
        s += g(f"puff{i}", f'<line x1="{860 + dx * 0.5:.0f}" y1="{460 + dy * 0.5:.0f}" x2="{860 + dx:.0f}" y2="{460 + dy:.0f}" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/>', (2.4, 2.9))
    return s + "</svg>\n"


def loyalty():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += head(CEO, [(0, "happy")], (540, 520), 0.55, False, "ceo")
    s += g("badge", f'<rect x="420" y="700" width="240" height="80" rx="10" fill="{CREAM}"/><rect x="420" y="700" width="240" height="26" rx="10" fill="{ORANGE}"/>'
                    + label(438, 768, "Trash Officer", 34), None, rig(540, 700, 2, 0.6))
    for i, (p, x, y, t) in enumerate(((1, 170, 420, 0.8), (3, 910, 420, 1.0), (5, 220, 820, 1.2), (7, 860, 820, 1.4))):
        s += head(p, [(0, "neutral"), (t, "happy")], (x, y), 0.36, x < 540, f"team{i}")
        s += heart(f"h{i}", x + (70 if x < 540 else -70), y - 150, (2.4 + 0.12 * i, dur + 1), 0.9)
    return s + "</svg>\n"


def badge():
    dur = 3.4
    s = root(dur, "1,0,0")
    s += g("card", f'<rect x="150" y="250" width="780" height="520" rx="26" fill="#FFFDF6"/>'
                   f'<rect x="150" y="250" width="780" height="150" rx="26" fill="{ORANGE}"/><rect x="150" y="350" width="780" height="50" fill="{ORANGE}"/>'
                   + label(220, 350, "HELLO, my title is", 64, CREAM))
    s += g("ceo", label(450, 600, "CEO", 120), (0, 1.6))
    s += g("strike", label(450, 600, "CEO", 120, GREY) + f'<line x1="430" y1="560" x2="700" y2="540" stroke="{ORANGE}" stroke-width="18" stroke-linecap="round"/>', (1.0, 1.6))
    s += g("new", label(200, 520, "Chief Taking the", 76) + label(200, 610, "Trash Out Officer", 76), (1.6, dur + 1), rig(540, 700, 2, 0.6))
    return s + "</svg>\n"


# ---- titles ----

def t_title():
    dur = 2.8
    s = title_root(dur)
    s += tag("chief", "Chief", 60, 680, 84, -3, 0.1, dur + 1)[0]
    s += tag("trash", "Taking the Trash Out", 60, 790, 84, 2, 0.45, dur + 1, ORANGE, PAPER)[0]
    s += tag("off", "Officer", 60, 900, 84, -2, 1.45, dur + 1)[0]
    return s + "</svg>\n"


def t_work():
    dur = 2.9
    s = title_root(dur)
    s += tag("ung", "The unglamorous stuff", 60, 760, 76, -2, 0.4, dur + 1)[0]
    s += tag("part", "is part of the work", 60, 880, 76, 2, 1.7, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_title), ("t2", t_work), ("b0", met), ("b1", linkedin), ("b2", trash), ("b3", loyalty), ("b4", badge)):
        open(os.path.join(HERE, f"scenes/trash-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/trash-{n}.svg")
