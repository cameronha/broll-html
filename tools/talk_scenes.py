"""Generate the talk-to-customers v9 scenes "crowd" and "three" (scenes/talk-*.svg).

usage: python3 tools/talk_scenes.py
Crowd figures come from one template (fig) with varied colors. Local figure coords stay positive
(0..200 x 0..450, feet at 100,440) because the cut filter region starts at -50 in local units.
"""
import os, random, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLOTH = ["#DE4A30", "#2F7D5B", "#E9B949", "#7A5BA6", "#C2557A", "#4F9C8C", "#F6EEDC", "#182A46", "#9C6B3E"]
HAIR = ["#182A46", "#3B2416", "#7A3E1E", "#D9A441", "#1E1E1E"]
SKIN = ["#FAC496", "#E7A97C", "#B97A50", "#8A5636"]
PANTS = ["#182A46", "#3B4A5E", "#5A3A28", "#2B2B2B"]


def shade(c, f=0.82):
    return "#" + "".join(f"{int(int(c[i:i + 2], 16) * f):02X}" for i in (1, 3, 5))


def fig(tf, cloth, hair, skin, pants, style, look=4, mouth="line"):
    """One customer, frontal, feet at local (100,440). tf = transform string."""
    e = [
        f'<rect x="58" y="325" width="34" height="118" rx="16" fill="{pants}"/>',
        f'<rect x="108" y="325" width="34" height="118" rx="16" fill="{pants}"/>',
        '<ellipse cx="72" cy="442" rx="30" ry="12" fill="#F6EEDC"/>',
        '<ellipse cx="128" cy="442" rx="30" ry="12" fill="#F6EEDC"/>',
        f'<rect x="8" y="200" width="34" height="132" rx="17" fill="{shade(cloth)}"/>',
        f'<rect x="158" y="200" width="34" height="132" rx="17" fill="{shade(cloth)}"/>',
        f'<circle cx="25" cy="334" r="16" fill="{skin}"/>', f'<circle cx="175" cy="334" r="16" fill="{skin}"/>',
        f'<rect x="22" y="180" width="156" height="170" rx="60" fill="{cloth}"/>',
        f'<rect x="82" y="150" width="36" height="40" fill="{skin}"/>',
        f'<circle cx="100" cy="100" r="78" fill="{skin}"/>',
    ]
    if style == 0:
        e.append(f'<path d="M20 92 Q16 10 100 8 Q184 10 180 92 Q150 50 100 52 Q50 50 20 92Z" fill="{hair}"/>')
    elif style == 1:
        e.append(f'<path d="M18 160 L18 90 Q16 10 100 8 Q184 10 182 90 L182 160 L156 160 L156 80 Q130 52 100 54 Q70 52 44 80 L44 160Z" fill="{hair}"/>')
    elif style == 2:
        e.append(f'<path d="M22 110 Q20 60 44 52 L46 100Z M178 110 Q180 60 156 52 L154 100Z" fill="{hair}"/>')
    else:
        e.append(f'<circle cx="100" cy="16" r="30" fill="{hair}"/>')
        e.append(f'<path d="M20 92 Q16 24 100 22 Q184 24 180 92 Q150 54 100 56 Q50 54 20 92Z" fill="{hair}"/>')
    e += [
        '<ellipse cx="72" cy="96" rx="16" ry="14" fill="#F6EEDC"/>', '<ellipse cx="128" cy="96" rx="16" ry="14" fill="#F6EEDC"/>',
        f'<circle cx="{72 + look}" cy="98" r="7" fill="#182A46"/>', f'<circle cx="{128 + look}" cy="98" r="7" fill="#182A46"/>',
        '<rect x="56" y="70" width="32" height="8" rx="4" fill="#182A46"/>', '<rect x="112" y="70" width="32" height="8" rx="4" fill="#182A46"/>',
        f'<ellipse cx="100" cy="120" rx="10" ry="8" fill="{shade(skin, 0.9)}"/>',
    ]
    e.append('<path d="M84 142 Q100 154 116 142 L114 148 Q100 158 86 148Z" fill="#182A46"/>' if mouth == "smile"
             else '<rect x="88" y="142" width="24" height="7" rx="3" fill="#182A46"/>')
    return "".join(re.sub(r"^<(\w+)", rf'<\1 transform="{tf}"', x) for x in e)


def v9_groups(*ids):
    src = open(os.path.join(HERE, "scenes/founder-v9.svg")).read()
    return "\n".join(re.search(rf'  <g id="{i}".*?\n  </g>', src, re.S).group(0) for i in ids)


def root(extra=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
            f'     data-bg="#8CBDDC" data-finish="cut" data-variants="3" data-border="0" data-bg-boil="0.5"{extra}>\n')


def floor(y1, y2):
    return (f'  <g id="floor" data-static="1">\n    <rect x="-40" y="{y1}" width="1160" height="{1126 - y1}" fill="#6E9FC4"/>\n'
            f'    <rect x="-40" y="{y2}" width="1160" height="{1126 - y2}" fill="#5A8BB3"/>\n  </g>\n')


def crowd():
    """The v9 founder pitches in front of 30 customers (3 rows of 10)."""
    rnd = random.Random(30)
    Z, TX, TY = 0.68, 300, 150
    out = [root(f' data-zoom="{Z},{TX},{TY}"'), "  <!-- 30 customers, back row first; each group sways a little -->\n", floor(500, 600)]
    rows = [(600, 0.5, 20), (685, 0.58, 75), (775, 0.66, 30)]
    for r, (Y, s, x0) in enumerate(rows):
        xs = [x0 + i * 108 for i in range(10)]
        for half in (0, 1):
            part = xs[half * 5:half * 5 + 5]
            cx = sum(part) / 5
            px, py = (cx - TX) / Z, (Y - TY) / Z
            out.append(f'  <g id="crowd-{r}{half}" data-pivot="{px:.0f},{py:.0f}" data-deg="{rnd.choice([-1.6, 1.6])}" '
                       f'data-freq="{rnd.choice([0.5, 0.7, 0.9])}" data-phase="{rnd.random():.2f}" data-shape="sine">\n    ')
            for X in part:
                k = s / Z
                tf = f"translate({(X - 100 * s - TX) / Z:.1f} {(Y - 440 * s - TY) / Z:.1f}) scale({k:.3f})"
                look = 5 if X < 620 else -5
                out.append(fig(tf, rnd.choice(CLOTH), rnd.choice(HAIR), rnd.choice(SKIN), rnd.choice(PANTS),
                               rnd.randrange(4), look, rnd.choice(["line", "line", "smile"])))
            out.append("\n  </g>\n")
    out.append("  <!-- the v9 founder, unchanged -->\n" + v9_groups("founder", "arm2", "arm", "founder-head") + "\n</svg>\n")
    return "".join(out)


def three():
    """A careful founder with a clipboard listens to only three customers in an empty room."""
    out = [root(), floor(746, 797)]
    out.append('''  <!-- careful founder: bun, glasses, teal sweater, clipboard -->
  <g id="founder2">
    <rect x="222" y="720" width="44" height="120" rx="20" fill="#182A46"/>
    <rect x="278" y="720" width="44" height="120" rx="20" fill="#182A46"/>
    <ellipse cx="236" cy="842" rx="40" ry="16" fill="#F6EEDC"/>
    <ellipse cx="306" cy="842" rx="40" ry="16" fill="#F6EEDC"/>
    <rect x="186" y="548" width="172" height="200" rx="70" fill="#4F9C8C"/>
    <rect x="252" y="530" width="40" height="34" fill="#FAC496"/>
    <line x1="340" y1="580" x2="362" y2="660" stroke="#41867A" stroke-width="40" stroke-linecap="round"/>
    <rect x="300" y="586" width="96" height="126" rx="8" fill="#B5835A" transform="rotate(8 348 649)"/>
    <rect x="310" y="600" width="76" height="102" rx="3" fill="#F6EEDC" transform="rotate(8 348 649)"/>
    <rect x="322" y="620" width="50" height="7" fill="#182A46" transform="rotate(8 348 649)"/>
    <rect x="322" y="640" width="44" height="7" fill="#182A46" transform="rotate(8 348 649)"/>
    <rect x="322" y="660" width="50" height="7" fill="#182A46" transform="rotate(8 348 649)"/>
    <rect x="330" y="580" width="36" height="14" rx="4" fill="#9AA0A6" transform="rotate(8 348 649)"/>
    <circle cx="372" cy="672" r="20" fill="#FAC496"/>
  </g>
  <g id="pen" data-pivot="206,580" data-deg="-7" data-freq="2.4" data-shape="snap">
    <line x1="206" y1="580" x2="236" y2="670" stroke="#41867A" stroke-width="40" stroke-linecap="round"/>
    <line x1="236" y1="670" x2="318" y2="650" stroke="#41867A" stroke-width="36" stroke-linecap="round"/>
    <rect x="322" y="602" width="10" height="56" rx="4" fill="#182A46" transform="rotate(20 327 630)"/>
    <circle cx="326" cy="646" r="19" fill="#FAC496"/>
  </g>
  <g id="head2" data-pivot="272,540" data-deg="4" data-freq="0.9" data-shape="sine">
    <circle cx="272" cy="368" r="40" fill="#3B2416"/>
    <circle cx="272" cy="450" r="96" fill="#FAC496"/>
    <path d="M176 446 Q172 352 272 350 Q372 352 368 446 Q330 396 272 398 Q214 396 176 446Z" fill="#3B2416"/>
    <circle cx="242" cy="452" r="27" fill="#182A46"/>
    <circle cx="312" cy="452" r="27" fill="#182A46"/>
    <rect x="262" y="444" width="24" height="9" fill="#182A46"/>
    <circle cx="242" cy="452" r="20" fill="#F6EEDC"/>
    <circle cx="312" cy="452" r="20" fill="#F6EEDC"/>
    <circle cx="250" cy="454" r="8" fill="#182A46"/>
    <circle cx="320" cy="454" r="8" fill="#182A46"/>
    <rect x="222" y="410" width="40" height="10" rx="5" fill="#3B2416"/>
    <rect x="292" y="410" width="40" height="10" rx="5" fill="#3B2416"/>
    <ellipse cx="282" cy="482" rx="11" ry="8" fill="#EFA877"/>
    <path d="M262 506 Q282 518 302 506 L300 513 Q282 524 264 513Z" fill="#B83A24"/>
  </g>
''')
    custs = [(660, "#DE4A30", "#182A46", "#E7A97C", "#3B4A5E", 0, "line", -1.5, 0.6, 0.0),
             (800, "#E9B949", "#7A3E1E", "#FAC496", "#182A46", 1, "smile", 2.5, 1.1, 0.3),
             (940, "#7A5BA6", "#1E1E1E", "#8A5636", "#2B2B2B", 2, "line", 1.5, 0.5, 0.6)]
    for i, (X, c, h, sk, p, st, m, deg, fq, ph) in enumerate(custs):
        s, Y = 0.82, 848
        out.append(f'  <g id="cust{i}" data-pivot="{X},{Y}" data-deg="{deg}" data-freq="{fq}" data-phase="{ph}" data-shape="sine">\n    '
                   + fig(f"translate({X - 100 * s:.1f} {Y - 440 * s:.1f}) scale({s})", c, h, sk, p, st, -5, m) + "\n  </g>\n")
    return "".join(out) + "</svg>\n"


for name, f in (("crowd", crowd), ("three", three)):
    open(os.path.join(HERE, f"scenes/talk-{name}.svg"), "w").write(f())
    print("wrote scenes/talk-%s.svg" % name)
