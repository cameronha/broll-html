"""B-roll for "Download your LinkedIn connections" (2026-10-16 footage) -> scenes/li-*.svg

usage: python3 tools/linkedin_scenes.py
Reuses the Leon parts (import, not copy). Times in ORIGINAL footage time live in videos/linkedin.json.
t1 hook       "New customers?"
b1 export     a screen of connection cards empties into a CSV file
t2 hours      "24 hours" with a ticking paper clock
b2 crap       Cam, confused, as a pile of paper falls beside him
b3 dump       the files fly into the agent
t3 prompt     the prompt, line by line
b4 lines      lines from Cam to three companies; one goes red with a tick
t4 list       [x] Direct leads  [x] Creative angles
b5 adjacent   a company just outside the market circle lights up
b6 friend     Cam -> someone he knows -> that company
b7 manual     Cam, tired, behind a tall stack of cards
t5 fast       Fast / Efficient / Creative
"""
import os
import cast_scenes as CS
from leon_scenes import (root, title_root, tag, check, robot, tick, seated, desk, standing_cam, cam_head, calm,
                         CAM, CAM_P, CREAM, NAVY, ORANGE, INK, PAPER, HERE, shade)

BLUE = "#8CBDDC"
GREY = "#9AA0A6"


def rig(x, y, deg=4, freq=0.9, shape="sine"):
    return f' data-pivot="{x:.0f},{y:.0f}" data-deg="{deg}" data-freq="{freq}" data-shape="{shape}"'


def g(gid, body, show=None, r=""):
    s = f' data-show="{show[0]:.2f},{show[1]:.2f}"' if show else ""
    return f'  <g id="{gid}"{s}{r}>\n    {body}\n  </g>\n'


def sheet(x, y, rot, fill=CREAM):
    """A paper sheet with three text lines, top-left (x, y), 90 x 116."""
    r = f' transform="rotate({rot} {x + 45} {y + 58})"'
    return (f'<rect x="{x}" y="{y}" width="90" height="116" rx="6" fill="{fill}"{r}/>'
            + "".join(f'<rect x="{x + 14}" y="{y + 22 + 22 * i}" width="{62 - 14 * (i % 2)}" height="8" rx="4" fill="{GREY}"{r}/>' for i in range(4)))


def building(gid, x, w, h, fill=NAVY, show=None, base=746):
    win = "".join(f'<rect x="{x + 14 + c * (w - 28) / 3:.0f}" y="{base - h + 20 + r * 40}" width="{(w - 28) / 3 - 10:.0f}" height="22" rx="3" fill="{CREAM}"/>'
                  for r in range(int((h - 40) / 40)) for c in range(3))
    return g(gid, f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="6" fill="{fill}"/>' + win, show)


def dashes(gid, a, b, show, color=NAVY, width=8):
    return g(gid, f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{color}" stroke-width="{width}" '
                  f'stroke-dasharray="18 14" stroke-linecap="round"/>', show)


# ---- b-roll ----

def export():
    """A screen of 9 connection cards; the cards drop out one by one and a CSV file pops up."""
    dur = 3.3                                              # rev2: about 1 s longer per beat (Cam: "too briefly")
    s = root(dur, "1,0,0")
    s += g("screen", f'<rect x="150" y="120" width="780" height="600" rx="18" fill="{NAVY}"/>'
                     f'<rect x="174" y="144" width="732" height="552" rx="8" fill="{CREAM}"/>'
                     f'<rect x="500" y="720" width="80" height="60" fill="{NAVY}"/><rect x="420" y="770" width="240" height="24" rx="10" fill="{NAVY}"/>')
    people = [1, 2, 3, 5, 9, 7, 4, 6, 8]
    for i, p in enumerate(people):
        cx, cy = 290 + (i % 3) * 250, 230 + (i // 3) * 170
        gone = 0.9 + 0.08 * i
        s += g(f"card{i}", f'<rect x="{cx - 105}" y="{cy - 70}" width="210" height="150" rx="10" fill="#FFFDF6"/>'
                           f'<rect x="{cx - 10}" y="{cy + 40}" width="100" height="10" rx="5" fill="{GREY}"/>', (0, gone))
        s += CS.head(p, [(0, "neutral")], (cx - 52, cy + 66), 0.2, False, "", f"face{i}").replace(f'data-show="0,{CS.DUR + 1}"', f'data-show="0,{gone:.2f}"')
    s += g("csv", f'<rect x="410" y="250" width="260" height="336" rx="14" fill="#FFFDF6"/>'
                  + "".join(f'<rect x="450" y="{300 + 40 * i}" width="{180 - 40 * (i % 2)}" height="16" rx="8" fill="{GREY}"/>' for i in range(4))
                  + f'<rect x="420" y="480" width="200" height="80" rx="10" fill="{ORANGE}"/>'
                  f'<text x="452" y="540" font-family="Libre Franklin" font-weight="800" font-size="60" fill="{CREAM}">CSV</text>',
           (1.75, dur + 1), rig(540, 590, 4, 1.4))
    return s + "</svg>\n"


def crap():
    """Cam (standing, left) looks at a pile of paper that keeps falling beside him."""
    dur = 3.2
    CS.DUR = dur
    s = root(dur, "1,0,0") + standing_cam()
    s += CS.head(CAM_P, [(0, "confused"), (1.3, "tired")], (276, 546), 0.62, True, rig(272, 540), "cam-head")
    import random
    rnd = random.Random(7)
    for i in range(16):                                   # each sheet: one high frame, then it lands on the pile
        x, y, rot = 560 + rnd.randint(0, 300), 640 - (i // 4) * 52 - rnd.randint(0, 20), rnd.randint(-28, 28)
        t = 0.1 * i
        s += g(f"fall{i}", sheet(x, y - 240, rot + 20), (t, t + 0.08))
        s += g(f"sheet{i}", sheet(x, y, rot), (t + 0.08, dur + 1))
    return s + "</svg>\n"


def dump():
    """The files fly into the agent, which bobs as it eats them."""
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("agent", robot(700, 470, 5.2), None, rig(700, 560, 5, 1.4))
    for k in range(6):                                    # 6 sheets, each hops 5 times toward the agent's face
        t0 = 0.12 + 0.28 * k
        x0, y0 = 70 + 40 * (k % 2), 620 - 60 * (k % 3)
        for j in range(5):
            f = j / 5
            x, y = x0 + (600 - x0) * f, y0 + (420 - y0) * f - 80 * (1 - (2 * f - 1) ** 2)
            s += g(f"f{k}-{j}", sheet(x, y, -20 + 12 * j), (t0 + 0.07 * j, t0 + 0.07 * (j + 1)))
    return s + "</svg>\n"


CAMPOS = (230, 560)


def net_root(dur):
    s = root(dur, "1,0,0")
    return s, CS.head(CAM_P, [(0, "happy")], CAMPOS, 0.5, True, rig(CAMPOS[0], CAMPOS[1] - 10), "cam-head")


def lines():
    """Lines run from Cam to three companies; the middle one turns red and gets a tick. Covers the rev2 flub cut."""
    dur = 2.9
    CS.DUR = dur
    s, head = net_root(dur)
    tops = []
    for i, (x, w, h, t) in enumerate(((560, 150, 420, 0.2), (740, 130, 560, 0.45), (900, 140, 330, 0.7))):
        s += building(f"b{i}", x, w, h, NAVY, (t, dur + 1))
        tops.append(((x + w / 2), 746 - h - 10, t))
    for i, (x, y, t) in enumerate(tops):
        s += dashes(f"l{i}", (CAMPOS[0] + 90, CAMPOS[1] - 120), (x, y), (t + 0.1, dur + 1))
    x, y, _ = tops[1]
    s += dashes("hot", (CAMPOS[0] + 90, CAMPOS[1] - 120), (x, y), (1.3, dur + 1), ORANGE, 12)
    s += g("tick", f'<circle cx="{x:.0f}" cy="{y - 50:.0f}" r="40" fill="{ORANGE}"/>' + tick(x, y - 50, 2.0).replace(NAVY, CREAM),
           (1.5, dur + 1), rig(x, y - 10, 6, 1.2))
    return s + head + "</svg>\n"


def market(stage, dur):
    """stage 1: a company just outside the market circle lights up. stage 2: Cam -> a friend -> that company."""
    CS.DUR = dur
    s, head = net_root(dur)
    s += g("market", f'<ellipse cx="820" cy="560" rx="230" ry="330" fill="{CREAM}"/>'
                     f'<text x="700" y="290" font-family="Libre Franklin" font-weight="800" font-size="46" fill="{NAVY}">Market</text>')
    for i, (x, h) in enumerate(((680, 300), (800, 380), (900, 260))):
        s += building(f"in{i}", x, 90, h, NAVY)
    adj = (470, 120, 300)                                  # the adjacent company, outside the circle
    s += building("adj", adj[0], adj[1], adj[2], NAVY, (0, 0.7 if stage == 1 else 0))
    s += building("adj-hot", adj[0], adj[1], adj[2], ORANGE, (0.7 if stage == 1 else 0, dur + 1))
    if stage == 2:
        fx, fy = 530, 446                                  # the friend stands on the adjacent company's roof line
        s += dashes("l1", (CAMPOS[0] + 90, CAMPOS[1] - 100), (fx - 40, fy - 40), (0.2, dur + 1))
        s += CS.head(9, [(0.5, "happy")], (fx, fy), 0.4, False, rig(fx, fy - 10), "friend").replace(
            f'data-show="0.5,{dur + 1}"', f'data-show="0.50,{dur + 1:.2f}"')
        s += dashes("l2", (fx + 60, fy - 60), (700, 470), (1.1, dur + 1), ORANGE, 12)
        s += g("pop", f'<circle cx="640" cy="560" r="34" fill="{ORANGE}"/>' + tick(640, 560, 1.7).replace(NAVY, CREAM), (1.4, dur + 1), rig(640, 590, 6, 1.2))
    return s + head + "</svg>\n"


def manual():
    """Cam, tired, across the table from a stack of contact cards taller than he is."""
    dur = 3.2
    CS.DUR = dur
    s = root(dur, "0.92,43,64") + seated("cam", CAM, True) + desk()
    for i in range(22):
        y = 610 - 22 * i
        s += g(f"card{i}", f'<rect x="{430 + (i * 37) % 23 - 11}" y="{y}" width="200" height="20" rx="4" '
                           f'fill="{"#FFFDF6" if i % 2 else CREAM}" stroke="{GREY}" stroke-width="2"/>', (0.04 * i, dur + 1))
    s += cam_head([(0, "tired")])
    return s + "</svg>\n"


# ---- titles (transparent, over the footage) ----

def t_hook():
    dur = 2.8
    s = title_root(dur)
    g1, w = tag("new", "New", 60, 760, 110, -3, 0.1, dur + 1, ORANGE, PAPER); s += g1
    s += tag("cust", "customers?", 60 + w + 20, 770, 110, 2, 0.35, dur + 1)[0]
    return s + "</svg>\n"


def t_hours():
    dur = 2.4
    s = title_root(dur)
    cx, cy = 150, 860
    s += g("clock", f'<circle cx="{cx}" cy="{cy}" r="92" fill="{NAVY}"/><circle cx="{cx}" cy="{cy}" r="74" fill="{CREAM}"/>'
                    f'<rect x="{cx - 5}" y="{cy - 44}" width="10" height="48" rx="5" fill="{NAVY}"/>', (0.05, dur + 1))
    s += g("hand", f'<rect x="{cx - 4}" y="{cy - 64}" width="8" height="66" rx="4" fill="{ORANGE}" transform="rotate(40 {cx} {cy})"/>',
           (0.05, dur + 1), rig(cx, cy, 60, 0.8, "snap"))
    s += tag("hrs", "24 hours", 270, 800, 110, -2, 0.1, dur + 1)[0]
    return s + "</svg>\n"


def t_prompt():
    dur = 9.4
    s = title_root(dur)
    s += tag("p0", "“I need new customers.", 40, 650, 58, -2, 0.3, dur + 1)[0]
    s += tag("p1", "Go through my connections.", 70, 760, 58, 1, 3.7, dur + 1)[0]
    s += tag("p2", "Who should I reach out to?”", 40, 870, 58, -1, 7.8, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_list():
    dur = 5.4                                              # rev2: starts at 47.0, after the b-roll that covers the cut
    s = title_root(dur)
    s += check("c1", 52, 780, 0.1, dur) + tag("i1", "Direct leads", 128, 768, 70, 1, 0.1, dur + 1)[0]
    s += check("c2", 52, 896, 4.2, dur) + tag("i2", "Creative angles", 128, 884, 70, -1, 4.2, dur + 1)[0]
    return s + "</svg>\n"


def t_fast():
    dur = 3.6
    s = title_root(dur)
    for gid, word, x, y, rot, t0, fill in (("fast", "Fast", 60, 712, -3, 0.6, INK), ("eff", "Efficient", 120, 812, 2, 1.2, INK),
                                          ("cre", "Creative", 70, 912, -2, 2.7, ORANGE)):
        s += tag(gid, word, x, y, 80, rot, t0, dur + 1, fill, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_hook), ("t2", t_hours), ("t3", t_prompt), ("t4", t_list), ("t5", t_fast),
                 ("b1", export), ("b2", crap), ("b3", dump), ("b4", lines), ("b5", lambda: market(1, 2.9)), ("b6", lambda: market(2, 3.3)),
                 ("b7", manual)):
        open(os.path.join(HERE, f"scenes/li-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/li-{n}.svg")
