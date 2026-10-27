"""B-roll for the Leon "AI agent week" video: five v9 scenes with cast heads -> scenes/leon-{1a,1b,2,3,4}.svg

usage: python3 tools/leon_scenes.py
t1 name      3.45-6.31   paper-tag titles over the footage: Cam / Houser / Actionworks
t2 fde      20.50-24.00  Forward / Deployed / Engineer
t3 week     16.60-19.30  AI / Agent / Week, with the agent
0  map       6.31-9.28   Cam's head hops from Austin to León on a paper map; pin and label drop on "León"
1a talk      9.28-12.66  Cam (p4) at a slide, three listeners react
1b workshop 12.66-15.00  two tables of people on laptops, a sticky-note wall, Cam leading
2  problem  26.08-34.96  the founder (p5) and Cam across a table, her laptop between; he points at her process
3  agent    38.56-43.44  the agent comes up on her screen and ticks off the steps; skeptical -> surprised
4  alone    43.44-47.92  she changes the agent herself, close
"""
import os, re
import cast_scenes as CS

HERE = CS.HERE
PANTS, CREAM, WOOD, NAVY = "#182A46", "#F6EEDC", "#B5835A", "#182A46"
ORANGE = "#DE4A30"                                     # accent = brand-guide red (rev10; was site orange #FF5600)
HER = {"cloth": "#DE4A30", "skin": "#C98E62"}          # p5
CAM = {"cloth": "#5E7A94", "skin": "#F0B98F"}          # p4: chambray shirt like the footage
CAM_P = 10                                             # Cam's head: person 10, a stylized likeness of him (was 4)
HEAD_K = 0.72
BOIL = 1.0                                             # Cam tried 50% and 25%, chose the full v9 boil (2026-10-27)


def shade(c, f=0.82):
    return "#%02X%02X%02X" % tuple(int(int(c[i:i + 2], 16) * f) for i in (1, 3, 5))


def root(dur, zoom):
    CS.DUR = dur
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
            f'     data-bg="#8CBDDC" data-finish="cut" data-variants="3" data-border="0" data-bg-boil="0.5" '
            f'data-zoom="{zoom}" data-dur="{dur}">\n'
            '  <g id="floor" data-static="1">\n'
            '    <rect x="-40" y="746" width="1160" height="380" fill="#6E9FC4"/>\n'
            '    <rect x="-40" y="797" width="1160" height="330" fill="#5A8BB3"/>\n  </g>\n')


# ---- the laptop scenes (2, 3, 4): she sits on the left, Cam across the table on the right, her laptop between ----

def seated(gid, who, right=False):
    """Chair, legs and torso of a person seated in profile. Left person faces right, neck (204, 516); right person mirrored."""
    c, sk = who["cloth"], who["skin"]
    X = (lambda x, w=0: 1080 - x - w) if right else (lambda x, w=0: x)
    return (f'  <g id="{gid}-chair" data-static="1" fill="{CREAM}">\n'
            f'    <rect x="{X(84, 40)}" y="470" width="40" height="320" rx="14" transform="rotate({6 if right else -6} {X(104)} 790)"/>\n'
            f'    <rect x="{X(96, 18)}" y="780" width="18" height="120" rx="6"/>\n'
            f'    <rect x="{X(272, 18)}" y="780" width="18" height="120" rx="6"/>\n'
            f'    <rect x="{X(90, 210)}" y="760" width="210" height="32" rx="12"/>\n  </g>\n'
            f'  <g id="{gid}-body" data-pivot="{X(200)},770" data-deg="{-1 if right else 1}" data-freq="0.4" data-shape="sine">\n'
            f'    <rect x="{X(200, 210)}" y="716" width="210" height="62" rx="30" fill="{PANTS}"/>\n'
            f'    <rect x="{X(360, 58)}" y="730" width="58" height="160" rx="26" fill="{PANTS}"/>\n'
            f'    <ellipse cx="{X(400)}" cy="892" rx="52" ry="20" fill="{CREAM}"/>\n'
            f'    <rect x="{X(108, 190)}" y="512" width="190" height="262" rx="74" fill="{c}"/>\n'
            f'    <rect x="{X(180, 48)}" y="500" width="48" height="40" fill="{sk}"/>\n  </g>\n')


def arm(gid, who, shoulder, elbow, hand, rig, point=0):
    """point = +1 / -1: a pointing finger to the right / left of the hand."""
    c = shade(who["cloth"])
    tip = (f'    <rect x="{hand[0] + (6 if point > 0 else -40)}" y="{hand[1] - 8}" width="34" height="12" rx="6" fill="{who["skin"]}"/>\n'
           if point else "")
    return (f'  <g id="{gid}-arm" {rig}>\n'
            f'    <line x1="{shoulder[0]}" y1="{shoulder[1]}" x2="{elbow[0]}" y2="{elbow[1]}" stroke="{c}" stroke-width="46" stroke-linecap="round"/>\n'
            f'    <line x1="{elbow[0]}" y1="{elbow[1]}" x2="{hand[0]}" y2="{hand[1]}" stroke="{c}" stroke-width="42" stroke-linecap="round"/>\n'
            f'{tip}'
            f'    <ellipse cx="{hand[0]}" cy="{hand[1] - 2}" rx="22" ry="18" fill="{who["skin"]}"/>\n  </g>\n')


def desk():
    return (f'  <g id="table">\n'
            f'    <rect x="330" y="628" width="420" height="30" rx="8" fill="{WOOD}"/>\n'
            f'    <rect x="352" y="652" width="22" height="248" rx="6" fill="{shade(WOOD)}"/>\n'
            f'    <rect x="706" y="652" width="22" height="248" rx="6" fill="{shade(WOOD)}"/>\n  </g>\n')


# the screen: content is drawn in a local 0..150 square and mapped onto the screen (turned a little toward her)
SCREEN = "matrix(0.96 0.04 0 0.97 452 458)"
SX, SY = 452, 458                                      # screen origin, for rig pivots


def laptop():
    return (f'  <g id="laptop">\n'
            f'    <path d="M400 616 L600 622 L606 634 L394 628Z" fill="#9AA0A6"/>\n'
            f'    <g transform="{SCREEN}">\n'
            f'      <rect x="-9" y="-9" width="168" height="168" rx="10" fill="{NAVY}"/>\n'
            f'      <rect x="0" y="0" width="150" height="150" rx="4" fill="{CREAM}"/>\n    </g>\n  </g>\n')


def on_screen(gid, body, show=None, rig=""):
    s = f' data-show="{show[0]},{show[1]}"' if show else ""
    return f'  <g id="{gid}"{s}{rig}>\n    <g transform="{SCREEN}">{body}</g>\n  </g>\n'


def process(red=True):
    """Her process: four boxes in a chain, the slow one red."""
    out = ['<rect x="16" y="36" width="118" height="5" fill="#9AA0A6"/>']
    for i, x in enumerate((10, 46, 82, 118)):
        out.append(f'<rect x="{x - 6}" y="20" width="32" height="36" rx="5" fill="{"#DE4A30" if red and i == 2 else NAVY}"/>')
    out.append('<rect x="20" y="86" width="110" height="9" rx="4" fill="#9AA0A6"/>'
               '<rect x="20" y="106" width="80" height="9" rx="4" fill="#9AA0A6"/>'
               '<rect x="20" y="126" width="96" height="9" rx="4" fill="#9AA0A6"/>')
    return "".join(out)


def robot(cx=75, cy=78, k=1.0):
    return (f'<rect x="{cx - 26 * k}" y="{cy - 22 * k}" width="{52 * k}" height="{44 * k}" rx="{11 * k}" fill="{ORANGE}"/>'
            f'<circle cx="{cx - 11 * k}" cy="{cy - 2 * k}" r="{6 * k}" fill="{NAVY}"/>'
            f'<circle cx="{cx + 11 * k}" cy="{cy - 2 * k}" r="{6 * k}" fill="{NAVY}"/>'
            f'<rect x="{cx - 2.5 * k}" y="{cy - 38 * k}" width="{5 * k}" height="{16 * k}" fill="{NAVY}"/>'
            f'<circle cx="{cx}" cy="{cy - 40 * k}" r="{7 * k}" fill="#E9B949"/>')


def tick(x, y, s=1.0):
    return (f'<path d="M{x - 11 * s} {y} L{x - 3 * s} {y + 9 * s} L{x + 13 * s} {y - 10 * s}" stroke="{NAVY}" '
            f'stroke-width="{9 * s}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


HER_NECK, CAM_NECK = (204, 516), (876, 516)


def her_head(tl):
    return CS.head(5, tl, HER_NECK, HEAD_K, True, ' data-pivot="204,520" data-deg="3" data-freq="0.5" data-shape="sine"', "her-head")


def cam_head(tl):
    return CS.head(CAM_P, tl, CAM_NECK, HEAD_K, False, ' data-pivot="876,520" data-deg="4" data-freq="0.9" data-shape="sine"', "cam-head")


def her_typing(freq=0.5, deg=2):
    return arm("her", HER, (236, 590), (300, 646), (440, 620),
               f'data-pivot="236,590" data-deg="{deg}" data-freq="{freq}" data-shape="snap"')


def cam_pointing():
    return arm("cam", CAM, (844, 590), (760, 620), (650, 556),
               'data-pivot="844,590" data-deg="5" data-freq="1.2" data-shape="snap"', point=-1)


def across(dur):
    return root(dur, "0.92,43,64") + seated("her", HER) + seated("cam", CAM, True) + desk() + laptop()


def problem():
    dur = 2.56
    s = across(dur) + on_screen("proc", process())
    # the red box pulses while they talk about it
    s += on_screen("pulse", '<rect x="70" y="14" width="44" height="48" rx="8" fill="none" stroke="#DE4A30" stroke-width="5"/>',
                   (0.3, dur + 1), f' data-pivot="{SX + 92},{SY + 40}" data-deg="4" data-freq="1.6" data-shape="snap"')
    s += her_typing() + cam_pointing() + cam_head([(0, "neutral"), (1.0, "happy")])
    s += her_head([(0, "worried"), (0.8, "happy")])
    return s + "</svg>\n"


def agent_scene():
    dur = 2.65
    s = across(dur) + on_screen("proc", process(), (0, 0.4))
    s += on_screen("robot", robot(75, 62), (0.4, dur + 1), f' data-pivot="{SX + 75},{SY + 84}" data-deg="6" data-freq="1.4" data-shape="sine"')
    for i, t in enumerate((1.0, 1.4, 1.8)):
        s += on_screen(f"tick{i}", tick(32 + i * 44, 122), (t, dur + 1))
    s += her_typing(0.4, 1) + cam_pointing() + cam_head([(0, "happy")])
    s += her_head([(0, "skeptical"), (0.7, "surprised")])
    return s + "</svg>\n"


def alone():
    dur = 2.16
    s = root(dur, "1.4,-20,-210") + seated("her", HER) + desk() + laptop()
    s += on_screen("robot", robot(75, 58, 0.9), None, f' data-pivot="{SX + 75},{SY + 80}" data-deg="5" data-freq="1.2" data-shape="sine"')
    s += on_screen("bar", '<rect x="22" y="118" width="106" height="8" rx="4" fill="#9AA0A6"/>')
    for i, (x, t0, t1) in enumerate([(30, 0, 0.5), (55, 0.5, 1.0), (80, 1.0, 1.5), (110, 1.5, dur + 1)]):
        s += on_screen(f"knob{i}", f'<circle cx="{x}" cy="122" r="11" fill="{ORANGE}"/>', (t0, t1))
    s += her_typing(3, 3) + her_head([(0, "neutral"), (0.3, "happy"), (1.4, "excited")])
    return s + "</svg>\n"


# ---- beat 1: the talk and the workshop ----

def listeners(svg, plan):
    """Put cast heads on the talk-three customers. plan = {cust index: (person, timeline)}."""
    for i, (person, tl) in plan.items():
        m = re.search(rf'  <g id="cust{i}"[^>]*>\n    (.*?)\n  </g>\n', svg, flags=re.S)
        body = "".join(re.findall(r"<[^>]+/>", m.group(1))[:10])
        X = float(re.search(r'data-pivot="([\d.]+),', m.group(0)).group(1))
        rig = CS.rig_of(svg, f"cust{i}")
        svg = svg.replace(m.group(0), f'  <g id="cust{i}"{rig}>\n    {body}\n  </g>\n'
                          + CS.head(person, tl, (X - 2, 848 - 275 * 0.82 + 8), 0.47, False, rig, f"cust{i}-head"))
    return svg


def standing_cam(dx=0):
    """Cam standing, frontal body (from the talk-three presenter), pointing up-right; neck at (272 + dx, 546)."""
    c, sk = CAM["cloth"], CAM["skin"]
    x = lambda v: v + dx
    return (f'  <g id="presenter">\n'
            f'    <rect x="{x(222)}" y="720" width="44" height="120" rx="20" fill="{PANTS}"/>\n'
            f'    <rect x="{x(278)}" y="720" width="44" height="120" rx="20" fill="{PANTS}"/>\n'
            f'    <ellipse cx="{x(236)}" cy="842" rx="40" ry="16" fill="{CREAM}"/>\n'
            f'    <ellipse cx="{x(306)}" cy="842" rx="40" ry="16" fill="{CREAM}"/>\n'
            f'    <line x1="{x(200)}" y1="580" x2="{x(190)}" y2="690" stroke="{shade(c)}" stroke-width="40" stroke-linecap="round"/>\n'
            f'    <circle cx="{x(190)}" cy="700" r="20" fill="{sk}"/>\n'
            f'    <rect x="{x(186)}" y="548" width="172" height="200" rx="70" fill="{c}"/>\n'
            f'    <rect x="{x(252)}" y="530" width="40" height="34" fill="{sk}"/>\n  </g>\n'
            f'  <g id="point" data-pivot="{x(340)},584" data-deg="-6" data-freq="1.2" data-shape="snap">\n'
            f'    <line x1="{x(340)}" y1="584" x2="{x(388)}" y2="500" stroke="{shade(c)}" stroke-width="40" stroke-linecap="round"/>\n'
            f'    <line x1="{x(388)}" y1="500" x2="{x(420)}" y2="404" stroke="{shade(c)}" stroke-width="36" stroke-linecap="round"/>\n'
            f'    <circle cx="{x(424)}" cy="394" r="19" fill="{sk}"/>\n'
            f'    <rect x="{x(418)}" y="356" width="12" height="34" rx="6" fill="{sk}" transform="rotate(16 {x(424)} 373)"/>\n  </g>\n')


def talk():
    dur = 1.46
    CS.DUR = dur
    svg = open(os.path.join(HERE, "scenes/talk-three.svg")).read()
    for gid in ("founder2", "pen", "head2"):
        svg = CS.swap_group(svg, gid, "")
    svg = svg.replace("#7A5BA6", CREAM)                  # purple listener -> brand cream (rev10)
    slide = ('  <g id="slide" data-static="1">\n'
             f'    <rect x="360" y="170" width="250" height="180" rx="10" fill="{NAVY}"/>\n'
             f'    <rect x="372" y="182" width="226" height="156" rx="4" fill="{CREAM}"/>\n  </g>\n'
             '  <g id="slide-agent" data-pivot="485,300" data-deg="5" data-freq="1.2" data-shape="sine">\n    '
             + robot(485, 278, 1.7) + '\n  </g>\n')
    svg = svg.replace('  <g id="cust0"', slide + standing_cam() + '  <g id="cust0"', 1)
    svg = svg.replace("</svg>", CS.head(CAM_P, [(0, "excited"), (0.9, "happy")], (276, 546), 0.62, True,
                                        ' data-pivot="272,540" data-deg="4" data-freq="0.9" data-shape="sine"', "cam-head") + "</svg>")
    svg = listeners(svg, {0: (2, [(0, "neutral"), (0.4, "happy")]), 1: (1, [(0, "happy"), (0.6, "excited")]),
                          2: (3, [(0, "neutral"), (0.9, "surprised")])})
    return CS.set_dur(svg)


STICKY = ["#DE4A30", "#E9B949", "#8CBDDC", "#182A46", "#F6EEDC"]   # no peach: it read as orange (rev11)


def pod(gid, x0, people, flip):
    """A table seen from the front with two people behind it, laptops and sticky notes on it.
    people = [(person, cx, cloth, skin, timeline), ...]"""
    out = []
    for i, (person, cx, cloth, skin, tl) in enumerate(people):
        out.append(f'  <g id="{gid}-p{i}" data-pivot="{cx},700" data-deg="{1.2 if i else -1.2}" data-freq="{0.5 + 0.3 * i}" data-shape="sine">\n'
                   f'    <rect x="{cx - 78}" y="560" width="156" height="170" rx="62" fill="{cloth}"/>\n'
                   f'    <rect x="{cx - 18}" y="540" width="36" height="34" fill="{skin}"/>\n  </g>\n')
    out.append(f'  <g id="{gid}-table">\n'
               f'    <rect x="{x0}" y="688" width="400" height="26" rx="8" fill="{WOOD}"/>\n'
               f'    <rect x="{x0 + 14}" y="712" width="372" height="40" fill="{shade(WOOD)}"/>\n'
               f'    <rect x="{x0 + 24}" y="750" width="22" height="150" rx="6" fill="{shade(WOOD, 0.7)}"/>\n'
               f'    <rect x="{x0 + 354}" y="750" width="22" height="150" rx="6" fill="{shade(WOOD, 0.7)}"/>\n')
    for k, (sx, rot) in enumerate(((x0 + 168, -8), (x0 + 196, 6), (x0 + 182, -2))):
        out.append(f'    <rect x="{sx}" y="{676 - k * 3}" width="38" height="14" rx="2" fill="{STICKY[k]}" transform="rotate({rot} {sx + 19} 684)"/>\n')
    out.append('  </g>\n')
    for i, (person, cx, cloth, skin, tl) in enumerate(people):
        # laptop lid toward us, hands on the keys at both sides of it
        out.append(f'  <g id="{gid}-lap{i}">\n'
                   f'    <path d="M{cx - 62} 690 L{cx + 62} 690 L{cx + 54} 616 L{cx - 54} 616Z" fill="#9AA0A6"/>\n'
                   f'    <circle cx="{cx}" cy="652" r="9" fill="#C3C8CD"/>\n  </g>\n')
        out.append(f'  <g id="{gid}-hands{i}" data-pivot="{cx},620" data-deg="2" data-freq="{2.6 + i * 0.4}" data-shape="snap">\n'
                   f'    <line x1="{cx - 66}" y1="600" x2="{cx - 70}" y2="676" stroke="{shade(cloth)}" stroke-width="34" stroke-linecap="round"/>\n'
                   f'    <line x1="{cx + 66}" y1="600" x2="{cx + 70}" y2="676" stroke="{shade(cloth)}" stroke-width="34" stroke-linecap="round"/>\n'
                   f'    <circle cx="{cx - 68}" cy="684" r="15" fill="{skin}"/>\n'
                   f'    <circle cx="{cx + 68}" cy="684" r="15" fill="{skin}"/>\n  </g>\n')
        out.append(CS.head(person, tl, (cx, 548), 0.5, flip,
                           f' data-pivot="{cx},552" data-deg="3" data-freq="{0.6 + 0.2 * i}" data-phase="{0.3 * i}" data-shape="sine"',
                           f"{gid}-head{i}"))
    return "".join(out)


def workshop():
    dur = 1.54
    s = root(dur, "1,0,0")
    board = ['  <g id="board" data-static="1">\n'
             f'    <rect x="300" y="96" width="480" height="250" rx="10" fill="{NAVY}"/>\n'
             f'    <rect x="312" y="108" width="456" height="226" rx="4" fill="{CREAM}"/>\n']
    for r in range(3):
        for c in range(6):
            x, y = 334 + c * 72, 126 + r * 68
            board.append(f'    <rect x="{x}" y="{y}" width="50" height="48" rx="3" fill="{STICKY[(r * 2 + c) % 4]}" '
                         f'transform="rotate({(r * 7 + c * 5) % 9 - 4} {x + 25} {y + 24})"/>\n')
    s += "".join(board) + "  </g>\n"
    s += standing_cam(dx=268)
    s += CS.head(CAM_P, [(0, "excited")], (544, 546), 0.62, True,
                 ' data-pivot="540,540" data-deg="4" data-freq="0.9" data-shape="sine"', "cam-head")
    s += pod("podL", 10, [(9, 110, "#DE4A30", "#B97A50", [(0, "happy")]),
                          (3, 310, "#F6EEDC", "#F2C9A0", [(0, "neutral"), (0.6, "excited")])], True)
    s += pod("podR", 670, [(1, 770, "#182A46", "#7A4A2E", [(0, "confused"), (0.5, "happy")]),
                           (2, 970, "#E9B949", "#B97A50", [(0, "happy")])], False)
    return s + "</svg>\n"


# ---- beat 0: the map ----

def bez(p0, p1, p2, t):
    return tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t ** 2 * c for a, b, c in zip(p0, p1, p2))


def map_scene():
    """Cam's head hops from Austin to León like a board-game piece; a pin and a label drop on "León"."""
    from paper_map import PaperMap
    dur = 2.13
    s = root(dur, "1,0,0").split('  <g id="floor"')[0]          # the sea is the background; no floor
    m = PaperMap((-101.65, 24.5), 40)
    s += ('  <g id="map" data-static="1">\n    '
          + m.land("United States of America", "#EFE6D2") + m.state("Texas", "#F6D9A8")
          + "".join(m.land(n, "#EFE6D2") for n in ("Guatemala", "Belize", "Cuba"))
          + m.land("Mexico", "#F2C46B") + "\n  </g>\n")
    A, L = m.xy(-97.74, 30.27), m.xy(-101.68, 21.12)
    P1 = (A[0] + 30, (A[1] + L[1]) / 2)
    s += (f'  <g id="austin" data-static="1">\n    <circle cx="{A[0]:.0f}" cy="{A[1]:.0f}" r="11" fill="{NAVY}"/>\n'
          f'    <text x="{A[0] + 20:.0f}" y="{A[1] + 12:.0f}" font-family="Libre Franklin" font-weight="800" font-size="34" fill="{NAVY}">Austin</text>\n  </g>\n')
    for i in range(1, 14):                                     # the trail fills in behind the piece
        x, y = bez(A, P1, L, i / 14)
        s += f'  <g id="dot{i}" data-show="{0.06 * i:.2f},{dur + 1}">\n    <circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{NAVY}"/>\n  </g>\n'
    pin = lambda y0: (f'<path d="M{L[0]:.0f} {y0:.0f} Q{L[0] - 26:.0f} {y0 - 34:.0f} {L[0] - 24:.0f} {y0 - 50:.0f} '
                      f'A25 25 0 1 1 {L[0] + 24:.0f} {y0 - 50:.0f} Q{L[0] + 26:.0f} {y0 - 34:.0f} {L[0]:.0f} {y0:.0f}Z" fill="{ORANGE}"/>'
                      f'<circle cx="{L[0]:.0f}" cy="{y0 - 54:.0f}" r="9" fill="{CREAM}"/>')
    s += f'  <g id="pin-hi" data-show="0.85,0.93">\n    {pin(L[1] - 50)}\n  </g>\n'
    s += f'  <g id="pin" data-show="0.93,{dur + 1}">\n    {pin(L[1])}\n  </g>\n'
    s += (f'  <g id="label" data-show="1.0,{dur + 1}" data-pivot="{L[0] + 40:.0f},{L[1] - 40:.0f}" data-deg="2" data-freq="0.6" data-shape="sine">\n'
          f'    <rect x="{L[0] + 34:.0f}" y="{L[1] - 92:.0f}" width="132" height="58" rx="8" fill="{CREAM}"/>\n'
          f'    <text x="{L[0] + 48:.0f}" y="{L[1] - 49:.0f}" font-family="Libre Franklin" font-weight="800" font-size="40" fill="{NAVY}">León</text>\n  </g>\n')
    # the piece: Cam's head, 9 hops along the trail, then it sits beside the pin
    stops = [bez(A, P1, L, i / 8) for i in range(9)]
    stops[-1] = (L[0] - 92, L[1] + 4)
    for i, (x, y) in enumerate(stops):
        t0, t1 = 0.1 * i, (0.1 * (i + 1) if i < 8 else dur + 1)
        lift = 0 if i in (0, 8) else (16 if i % 2 else 4)
        g = CS.head(CAM_P, [(t0, "excited" if i < 8 else "happy")], (x, y - lift), 0.3, False,
                    f' data-pivot="{x:.0f},{y:.0f}" data-deg="{4 if i == 8 else 0}" data-freq="0.8" data-shape="sine"', f"piece{i}")
        s += g.replace(f'data-show="{t0},{dur + 1}"', f'data-show="{t0:.2f},{t1:.2f}"')
    return s + "</svg>\n"


# ---- titles: paper tags over the footage (transparent renders) ----

FONT = "/Library/Fonts/LibreFranklin-ExtraBold.ttf"
AW_RED = "#DE4A30"                                     # brand guide (actionworks-marks skill) mark red
INK, PAPER = NAVY, CREAM                               # brand guide navy and cream (rev10)                     # actionworks.co charcoal and off-white (with ORANGE)


def tag(gid, text, x, y, size, rot, t0, t1, fill=None, ink=None, pop=0.09):
    """One word on a paper tag, top-left near (x, y). It pops in a little big for `pop` s, then settles."""
    from PIL import ImageFont
    fill, ink = fill or INK, ink or PAPER
    tw = ImageFont.truetype(FONT, size).getlength(text)
    w, h = tw + 0.7 * size, 1.32 * size
    cx, cy = x + w / 2, y + h / 2
    out = []
    for k, a, b in ((1.12, t0, t0 + pop), (1.0, t0 + pop, t1)):
        rw, rh, fs = w * k, h * k, size * k
        r = f' transform="rotate({rot} {cx:.0f} {cy:.0f})"'
        out.append(f'  <g id="{gid}-{k}" data-show="{a:.2f},{b:.2f}" data-pivot="{cx:.0f},{cy + rh / 2:.0f}" data-deg="1.5" '
                   f'data-freq="0.5" data-shape="sine">\n'
                   f'    <rect x="{cx - rw / 2:.0f}" y="{cy - rh / 2:.0f}" width="{rw:.0f}" height="{rh:.0f}" rx="{10 * k:.0f}" fill="{fill}"{r}/>\n'
                   f'    <text x="{cx - tw * k / 2:.0f}" y="{cy + 0.36 * fs:.0f}" font-family="Libre Franklin" font-weight="800" '
                   f'font-size="{fs:.0f}" fill="{ink}"{r}>{text}</text>\n  </g>\n')
    return "".join(out), w


def title_root(dur):
    CS.DUR = dur
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
            f'     data-bg="#8CBDDC" data-finish="cut" data-variants="3" data-border="0" data-bg-boil="0.5" '
            f'data-zoom="1,0,0" data-dur="{dur}" data-transparent="1">\n')


def title_name():
    """3.45-6.31: "Cam" "Houser" on "Cam Houser", then "Actionworks" on "ActionWorks"."""
    dur = 2.86
    s = title_root(dur)
    g, w = tag("cam", "Cam", 60, 690, 120, -4, 0.11, dur + 1); s += g
    g, _ = tag("houser", "Houser", 60 + w + 24, 700, 120, 2, 0.31, dur + 1); s += g
    g, _ = tag("aw", "Actionworks", 110, 868, 84, -2, 2.08, dur + 1, AW_RED, PAPER); s += g
    return s + "</svg>\n"


def title_fde():
    """20.5-24.0: "Forward" "Deployed" "Engineer", one word at a time as he says it."""
    dur = 3.5
    s = title_root(dur)
    for gid, word, x, y, rot, t0, fill, ink in (("fwd", "Forward", 60, 730, -3, 0.07, INK, PAPER),
                                                ("dep", "Deployed", 130, 836, 2, 0.51, INK, PAPER),
                                                ("eng", "Engineer", 80, 942, -2, 1.11, ORANGE, PAPER)):
        s += tag(gid, word, x, y, 80, rot, t0, dur + 1, fill, ink)[0]
    return s + "</svg>\n"


def title_week():
    """16.6-19.3: "AI Agent Week" on "AI agent week", the agent beside it."""
    dur = 2.7
    s = title_root(dur)
    g, w1 = tag("ai", "AI", 50, 800, 96, -3, 0.1, dur + 1, ORANGE, PAPER); s += g
    g, w2 = tag("agent", "Agent", 50 + w1 + 16, 806, 96, 2, 0.27, dur + 1); s += g
    g, _ = tag("week", "Week", 50 + w1 + w2 + 32, 798, 96, -2, 0.61, dur + 1); s += g
    s += (f'  <g id="week-agent" data-show="0.27,{dur + 1}" data-pivot="{90},{770}" data-deg="8" data-freq="1.4" data-shape="sine">\n    '
          + robot(96, 742, 1.4) + '\n  </g>\n')
    return s + "</svg>\n"


def title_ae():
    """8.9-11.2: "AI Agents" / "for Entrepreneurs", word by word, the first time he says it."""
    dur = 2.3
    s = title_root(dur)
    g, w1 = tag("ai2", "AI", 50, 760, 96, -3, 0.12, dur + 1, ORANGE, PAPER); s += g
    g, _ = tag("agents", "Agents", 50 + w1 + 16, 766, 96, 2, 0.38, dur + 1); s += g
    g, w3 = tag("for", "for", 90, 892, 80, 1, 0.78, dur + 1); s += g
    g, _ = tag("entre", "Entrepreneurs", 90 + w3 + 14, 886, 80, -2, 1.33, dur + 1); s += g
    return s + "</svg>\n"


def check(gid, x, y, t0, dur, size=60):
    """A red check box that appears with a list item."""
    return (f'  <g id="{gid}" data-show="{t0:.2f},{dur + 1}" data-pivot="{x + size / 2:.0f},{y + size:.0f}" data-deg="2" data-freq="0.6" data-shape="sine">\n'
            f'    <rect x="{x}" y="{y}" width="{size}" height="{size}" rx="8" fill="{ORANGE}" transform="rotate(-4 {x + size / 2} {y + size / 2})"/>\n'
            f'    <path d="M{x + size * 0.24:.0f} {y + size * 0.52:.0f} L{x + size * 0.43:.0f} {y + size * 0.7:.0f} L{x + size * 0.78:.0f} {y + size * 0.3:.0f}" '
            f'stroke="{PAPER}" stroke-width="{size * 0.13:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>\n  </g>\n')


def title_needs():
    """32.2-36.9: Growth / Automation / Whatever you need, as he lists them."""
    dur = 4.7
    s = title_root(dur)
    for gid, word, x, y, rot, t0, fill in (("grow", "Growth", 50, 712, -3, 0.14, INK),
                                          ("auto", "Automation", 110, 812, 2, 0.68, INK),
                                          ("what", "Whatever you need", 60, 912, -2, 2.76, ORANGE)):
        s += tag(gid, word, x, y, 68, rot, t0, dur + 1, fill, PAPER)[0]
    return s + "</svg>\n"


def title_leave():
    """39.8-44.0: You'll leave with: [x] An agent that works, [x] Knowledge to improve it."""
    dur = 4.2
    s = title_root(dur)
    s += tag("leave", "You\u2019ll leave with", 50, 676, 52, -2, 0.32, dur + 1, ORANGE, PAPER)[0]
    s += check("chk1", 52, 772, 1.13, dur) + tag("item1", "An agent that works", 128, 760, 66, 1, 1.13, dur + 1)[0]
    s += check("chk2", 52, 884, 2.52, dur) + tag("item2", "Knowledge to improve it", 128, 872, 66, -1, 2.52, dur + 1)[0]
    return s + "</svg>\n"


def thumb():
    """Thumbnail overlay (transparent; laid over a graded footage frame): AI Agent Week / León, México, the agent, a pin."""
    dur = 0.5
    s = title_root(dur)
    sz, gap = 104, 14                                      # one row, centred: measure first, then place
    ws = [tag(f"th-m{i}", w, 0, 0, sz, 0, -1, dur + 1)[1] for i, w in enumerate(("AI", "Agent", "Week"))]
    x = (1080 - sum(ws) - 2 * gap) / 2
    for (gid, word, rot, fill, ink), w in zip((("th-ai", "AI", -3, ORANGE, PAPER), ("th-agent", "Agent", 2, None, None),
                                               ("th-week", "Week", -2, None, None)), ws):
        g, _ = tag(gid, word, x, 690, sz, rot, -1, dur + 1, fill, ink); s += g; x += w + gap
    g, _ = tag("th-leon", "Le\u00f3n, M\u00e9xico", 132, 864, 88, 1, -1, dur + 1); s += g
    x, y = 84, 960                                         # map pin left of the place tag
    s += (f'  <g id="th-pin">\n    <path d="M{x} {y} Q{x - 34} {y - 44} {x - 32} {y - 66} A33 33 0 1 1 {x + 32} {y - 66} '
          f'Q{x + 34} {y - 44} {x} {y}Z" fill="{ORANGE}"/>\n    <circle cx="{x}" cy="{y - 70}" r="12" fill="{CREAM}"/>\n  </g>\n')
    s += '  <g id="th-robot">\n    ' + robot(915, 540, 3.4) + '\n  </g>\n'
    return s + "</svg>\n"


def calm(svg, k=BOIL):
    """Scale the boil: piece jitter (and sheet shake) and how much the cut edges change."""
    svg = re.sub(r'\s(data-bg-boil|data-jitter)="[^"]*"', "", svg, count=2)
    return svg.replace("<svg ", f'<svg data-bg-boil="{0.5 * k}" data-jitter="{k}" ', 1)


if __name__ == "__main__":
    for n, f in (("t1", title_name), ("t2", title_fde), ("t3", title_week), ("t4", title_ae), ("t5", title_needs), ("t6", title_leave), ("thumb", thumb), ("0", map_scene), ("1a", talk), ("1b", workshop), ("2", problem), ("3", agent_scene), ("4", alone)):
        open(os.path.join(HERE, f"scenes/leon-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/leon-{n}.svg")
