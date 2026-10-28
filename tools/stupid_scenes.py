"""B-roll for "Asking stupid questions" (2026-08-13 footage) -> scenes/stu-*.svg

usage: python3 tools/stupid_scenes.py
Reuses the Leon / LinkedIn / investors parts. Times in ORIGINAL footage time live in videos/stupid.json.
t1 facil     I facilitate / CEO peer groups
b1 circle    Cam and five CEOs around a round table
b2 growth    three CEOs in front of a rising bar chart
t2 admit     They admit / "I don't know."
b3 vision    early founders under a "Big vision" cloud; they get nervous
t3 scared    Terrified / of looking stupid
b4 ceo       a successful CEO says "I don't know." and smiles
"""
import os
import cast_scenes as CS
from leon_scenes import root, title_root, tag, calm, CREAM, NAVY, ORANGE, INK, PAPER, HERE, WOOD, shade
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, GOLD


def bubble(gid, x, y, w, h, text, size, show, tail=(0, 1)):
    tx, ty = x + w * 0.3, y + h
    return g(gid, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{CREAM}"/>'
                  f'<path d="M{tx:.0f} {ty - 2} L{tx + 50:.0f} {ty - 2} L{tx + 10 + 40 * tail[0]:.0f} {ty + 60}Z" fill="{CREAM}"/>'
                  + label(x + 34, y + h / 2 + size * 0.36, text, size), show, rig(x + w / 2, y + h, 3, 0.8))


def bars(x0, base, heights, t0, step, color=NAVY, w=90, gap=26):
    out = ""
    for i, h in enumerate(heights):
        out += g(f"bar{i}", f'<rect x="{x0 + i * (w + gap)}" y="{base - h}" width="{w}" height="{h}" rx="6" fill="{ORANGE if i == len(heights) - 1 else color}"/>',
                 (t0 + step * i, 99))
    return out


# ---- b-roll ----

def circle():
    dur = 3.0
    s = root(dur, "1,0,0")
    for i, (p, x, y, t) in enumerate(((1, 330, 560, 1.2), (3, 540, 530, 1.6), (9, 750, 560, 2.0))):     # back row, behind the table
        s += head(p, [(0, "neutral"), (t, "happy")], (x, y), 0.36, i == 0, f"back{i}")
    s += g("table", f'<ellipse cx="540" cy="680" rx="380" ry="110" fill="{shade(WOOD)}"/><ellipse cx="540" cy="664" rx="380" ry="104" fill="{WOOD}"/>'
                    + "".join(f'<rect x="{x}" y="{y}" width="70" height="46" rx="4" fill="{CREAM}" transform="rotate({r} {x + 35} {y + 23})"/>'
                              for x, y, r in ((330, 630, -8), (500, 610, 4), (680, 640, -3))))
    s += head(10, [(0, "happy")], (190, 800), 0.44, True, "cam")
    s += head(6, [(0, "neutral"), (1.0, "excited")], (890, 800), 0.44, False, "ceo6")
    return s + "</svg>\n"


def growth():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += bars(250, 600, (120, 190, 270, 360, 460), 0.1, 0.18)
    s += g("arrow", f'<path d="M230 560 L520 420 L640 470 L820 230" stroke="{ORANGE}" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                    f'<path d="M770 220 L850 200 L830 280Z" fill="{ORANGE}"/>', (1.0, dur + 1))
    for i, (p, x) in enumerate(((7, 230), (8, 540), (6, 850))):
        s += head(p, [(0, "happy"), (1.2 + 0.2 * i, "excited")], (x, 790), 0.4, i == 0, f"ceo{i}")
    return s + "</svg>\n"


def vision():
    dur = 3.0
    s = root(dur, "1,0,0")
    cloud = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CREAM}"/>' for cx, cy, r in
                    ((360, 300, 120), (520, 240, 150), (700, 290, 130), (440, 380, 110), (640, 380, 120)))
    s += g("cloud", cloud + label(380, 350, "Big vision", 76), (1.4, dur + 1), rig(540, 460, 2, 0.6))
    for i, (p, x) in enumerate(((1, 260), (2, 540), (3, 820))):
        s += head(p, [(0, "excited"), (2.1 + 0.15 * i, "worried")], (x, 790), 0.42, i == 0, f"f{i}")
    return s + "</svg>\n"


def ceo():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("chart", "".join(f'<rect x="{720 + 70 * i}" y="{700 - h}" width="52" height="{h}" rx="5" fill="{ORANGE if i == 3 else NAVY}"/>'
                            for i, h in enumerate((140, 210, 290, 380))))
    s += bubble("say", 120, 170, 470, 140, "I don’t know.", 64, (2.8, dur + 1))
    s += head(6, [(0, "neutral"), (1.0, "happy"), (2.8, "excited")], (380, 760), 0.58, True, "ceo")
    return s + "</svg>\n"


# ---- titles ----

def t_facil():
    dur = 2.7
    s = title_root(dur)
    s += tag("fac", "I facilitate", 60, 740, 84, -2, 0.5, dur + 1)[0]
    s += tag("peer", "CEO peer groups", 60, 870, 96, 2, 1.8, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_admit():
    dur = 4.5
    s = title_root(dur)
    s += tag("adm", "They admit", 60, 740, 90, -2, 1.7, dur + 1)[0]
    s += tag("idk", "“I don’t know.”", 60, 870, 100, 2, 3.0, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_scared():
    dur = 5.0
    s = title_root(dur)
    s += tag("terr", "Terrified", 60, 740, 100, -3, 0.3, dur + 1)[0]
    s += tag("stup", "of looking stupid", 60, 880, 84, 2, 3.8, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_facil), ("t2", t_admit), ("t3", t_scared), ("b1", circle), ("b2", growth), ("b3", vision), ("b4", ceo)):
        open(os.path.join(HERE, f"scenes/stu-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/stu-{n}.svg")
