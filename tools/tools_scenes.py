"""B-roll for "Use the tools" (2025-04-29 footage) -> scenes/tls-*.svg

usage: python3 tools/tools_scenes.py
Reuses the Leon / LinkedIn / investors / repetition / report parts. Times in ORIGINAL footage time live in videos/tools.json.
t1 title     Don't just read / about AI   (rev2: "Use the tools" did not make sense as a title; rev3: all titles flush right, off the cat)
b1 hype      a "Hype" gauge; the needle swings up; Cam nods ("which I do")
b2 articles  article pages about AI stack up; Cam reads them, gets tired
b3 gloss     a big article page covers the real thing: a robot peeks out behind it
t2 other     Someone else's / perspective
b4 free      AI app tiles pop in, each with a "Free" tag; a "$0" price tag
b5 minutes   a stopwatch: "5 min" of experimenting
t3 play      Actually / play with the tools
b6 fit       a puzzle with one gap; the red "AI" piece drops into it
"""
import os
from leon_scenes import root, title_root, tag, calm, robot, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, GOLD
from repetition_scenes import pill
from report_scenes import centered

BLUE = "#5E7A94"


def page(x, y, w, h, title, rot=0, fill="#FFFDF6"):
    r = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
    lines = "".join(f'<rect x="{x + 30}" y="{y + 120 + 34 * i}" width="{w - 60 - 50 * (i % 3)}" height="12" rx="6" fill="{GREY}"{r}/>'
                    for i in range(int((h - 150) / 34)))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}"{r}/>'
            f'<text x="{x + 30}" y="{y + 80}" font-family="Libre Franklin" font-weight="800" font-size="52" fill="{NAVY}"{r}>{title}</text>' + lines)


# ---- b-roll ----

def hype():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += g("dial", f'<path d="M300 600 A240 240 0 0 1 780 600 Z" fill="#FFFDF6"/>'
                   f'<path d="M300 600 A240 240 0 0 1 380 420 L540 600 Z" fill="{BLUE}"/>'
                   f'<path d="M700 420 A240 240 0 0 1 780 600 L540 600 Z" fill="{ORANGE}"/>' + centered(540, 680, "Hype", 64, NAVY),
           (0.05, dur + 1), rig(540, 600, 1, 0.5))
    for i, (deg, t0, t1) in enumerate(((-60, 0.05, 0.8), (-10, 0.8, 1.5), (55, 1.5, dur + 1))):
        s += g(f"needle{i}", f'<rect x="530" y="400" width="20" height="200" rx="10" fill="{NAVY}" transform="rotate({deg} 540 600)"/>'
                             f'<circle cx="540" cy="600" r="26" fill="{NAVY}"/>', (t0, t1))
    s += head(CAM_P, [(0.05, "neutral"), (2.2, "happy")], (870, 860), 0.55, False, "cam")
    return s + "</svg>\n"


def articles():
    dur = 3.4
    s = root(dur, "1,0,0")
    for i, (x, y, rot, t) in enumerate(((70, 180, -6, 0.1), (230, 140, 4, 0.5), (390, 200, -3, 0.9))):
        s += g(f"p{i}", page(x, y, 360, 460, "AI news", rot), (t, dur + 1), rig(x + 180, y + 460, 2, 0.7))
    s += head(CAM_P, [(0.05, "neutral"), (2.2, "tired")], (900, 900), 0.55, False, "cam")
    return s + "</svg>\n"


def gloss():
    dur = 3.9
    s = root(dur, "1,0,0")
    s += g("bot", robot(700, 420, 4.2), (0.05, 2.3), rig(700, 520, 5, 1.1))
    s += g("bot2", robot(620, 420, 4.6), (2.3, dur + 1), rig(620, 530, 9, 1.6))     # second half: the robot steps out and waves, so the beat keeps moving
    s += g("pg", page(170, 200, 470, 600, "What AI is", -3), (0.05, 2.3), rig(405, 800, 2, 0.6))
    s += g("pg2", page(60, 330, 470, 600, "What AI is", -14), (2.3, dur + 1), rig(295, 930, 2, 0.6))
    s += pill("real", 800, 610, "the real thing", 44, ORANGE, CREAM, (1.6, dur + 1))
    return s + "</svg>\n"


def free():
    dur = 3.8
    s = root(dur, "1,0,0")
    tiles = ((260, 260, NAVY), (540, 260, ORANGE), (820, 260, BLUE), (400, 560, GOLD), (680, 560, NAVY))
    for i, (x, y, f) in enumerate(tiles):
        s += g(f"t{i}", f'<rect x="{x - 100}" y="{y - 100}" width="200" height="200" rx="44" fill="{f}"/>'
                        f'<path d="M{x - 50} {y - 30} h100 a20 20 0 0 1 20 20 v50 a20 20 0 0 1 -20 20 h-60 l-30 26 v-26 h-10 a20 20 0 0 1 -20 -20 v-50 a20 20 0 0 1 20 -20 z" fill="{CREAM}"/>',
               (0.1 + 0.3 * i, dur + 1), rig(x, y + 100, 3, 0.8))
        s += pill(f"f{i}", x, y + 130, "Free", 34, CREAM, NAVY, (0.4 + 0.3 * i, dur + 1))
    s += g("price", f'<rect x="420" y="790" width="240" height="130" rx="18" fill="{ORANGE}"/><circle cx="455" cy="855" r="14" fill="{CREAM}"/>'
                    + centered(560, 885, "$0", 84, CREAM), (2.4, dur + 1), rig(540, 920, 6, 1.1))
    return s + "</svg>\n"


def minutes():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("watch", f'<rect x="515" y="190" width="50" height="60" rx="8" fill="{NAVY}"/><circle cx="540" cy="500" r="250" fill="{NAVY}"/>'
                    f'<circle cx="540" cy="500" r="215" fill="#FFFDF6"/>', (0.05, dur + 1), rig(540, 750, 2, 0.6))
    for i, deg in enumerate((0, 60, 120, 180, 240, 300)):          # the hand ticks round, on twos
        t0 = 0.05 + i * dur / 6
        s += g(f"hand{i}", f'<rect x="530" y="330" width="20" height="180" rx="10" fill="{ORANGE}" transform="rotate({deg} 540 500)"/>'
                           f'<circle cx="540" cy="500" r="22" fill="{NAVY}"/>', (t0, t0 + dur / 6 if i < 5 else dur + 1))
    s += pill("min", 540, 870, "5 minutes", 64, ORANGE, CREAM, (0.6, dur + 1))
    return s + "</svg>\n"


def fit():
    dur = 4.0
    s = root(dur, "1,0,0")
    cells = [(c, r) for r in range(3) for c in range(3)]
    body = "".join(f'<rect x="{240 + 205 * c}" y="{160 + 205 * r}" width="195" height="195" rx="14" fill="{[NAVY, BLUE, CREAM][(c + r) % 3]}"/>'
                   for c, r in cells if (c, r) != (1, 1))
    s += g("board", body + centered(540, 830, "your work", 48, NAVY), (0.05, dur + 1), rig(540, 780, 1, 0.5))
    piece = lambda x, y: (f'<rect x="{x}" y="{y}" width="195" height="195" rx="14" fill="{ORANGE}"/>' + centered(x + 97, y + 125, "AI", 84, CREAM))
    s += g("pc0", piece(760, 640), (0.4, 1.6), rig(857, 835, 6, 1.2))
    s += g("pc1", piece(600, 470), (1.6, 2.0))
    s += g("pc2", piece(445, 365), (2.0, dur + 1), rig(542, 560, 2, 0.6))
    return s + "</svg>\n"


# ---- titles ----

def rtag(gid, text, y, size, rot, t0, t1, fill=None, ink=None):
    """A tag set flush right (60 px margin): the cat sits on Cam's lap at the lower left of this take."""
    w = tag(gid, text, 0, y, size, rot, t0, t1, fill, ink)[1]
    return tag(gid, text, 1020 - w, y, size, rot, t0, t1, fill, ink)[0]


def t_title():
    dur = 3.1
    s = title_root(dur)
    s += rtag("read", "Don't just read", 760, 86, -2, 0.15, dur + 1)
    s += rtag("ai", "about AI", 880, 100, 2, 1.2, dur + 1, ORANGE, PAPER)
    return s + "</svg>\n"


def t_other():
    dur = 2.0
    s = title_root(dur)
    s += rtag("some", "Someone else's", 780, 80, -2, 0.05, dur + 1)
    s += rtag("per", "perspective", 890, 90, 2, 0.6, dur + 1, ORANGE, PAPER)
    return s + "</svg>\n"


def t_play():
    dur = 2.9
    s = title_root(dur)
    s += rtag("act", "Actually", 760, 86, -2, 0.1, dur + 1)
    s += rtag("play", "play with the tools", 880, 80, 2, 0.9, dur + 1, ORANGE, PAPER)
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_title), ("t2", t_other), ("t3", t_play),
                 ("b1", hype), ("b2", articles), ("b3", gloss), ("b4", free), ("b5", minutes), ("b6", fit)):
        open(os.path.join(HERE, f"scenes/tls-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/tls-{n}.svg")
