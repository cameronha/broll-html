"""B-roll for "front page" (website intro; raw 2026-11-02 15-27-42) -> scenes/fp-*.svg
Times inside each beat are local (0 = beat start); beat windows live in videos/frontpage.json (raw time + 324.24).
b1 intro     Cam; "Actionworks"; cards "AI education", "Startup programs"; the robot hops on
b2 region    "Region", "Community", "City" pop; a small skyline; it grows on "grow"
b3 build     blocks stack into a program; an arrow hits the target; a check
b4 cohort    four founders pop in; "Cohort"; they design and build: product box, "Services"
b5 advocate  a timeline; Cam and the robot at "2019"; a dot walks to "ChatGPT 2022"
b6 world     a globe spins: Brazil, India, Korea, Europe, Latin America light up with pins
b7 partners  a government building, an economic development office, Cam; a line joins them
t1 AI-native / founders   t2 Go after / customers   t3 Give me / a ping
"""
import math, os
from leon_scenes import root, calm, robot, check, CREAM, NAVY, ORANGE, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, GOLD
from repetition_scenes import pill
from report_scenes import centered, globe, ortho
from teacher2_scenes import steps
from nov2_parts import two, building, BLUE, WHITE


def intro():
    dur = 4.6
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.5, "happy")], (230, 1010), 0.8, False, "cam")
    s += pill("aw", 540, 170, "Actionworks", 80, NAVY, CREAM, (0.2, dur + 1))
    s += g("c1", f'<rect x="470" y="380" width="520" height="150" rx="18" fill="{WHITE}"/>' + centered(730, 475, "AI education", 60, NAVY), (1.9, dur + 1), rig(730, 530, 2, 0.7))
    s += g("c2", f'<rect x="470" y="580" width="520" height="150" rx="18" fill="{ORANGE}"/>' + centered(730, 675, "Startup programs", 56, CREAM), (3.0, dur + 1), rig(730, 730, 2, 0.7))
    s += steps("bot", lambda x, y: robot(x, y, 2.2), [(1000, 880), (900, 840), (800, 880), (700, 840)], 3.4, 4.3, dur)
    return s + "</svg>\n"


def region():
    dur = 5.6
    s = root(dur, "1,0,0")
    for i, (w, x, t) in enumerate((("Region", 220, 0.2), ("Community", 540, 1.1), ("City", 860, 2.1))):
        s += pill(f"p{i}", x, 170, w, 56, [NAVY, ORANGE, NAVY][i], CREAM, (t, dur + 1))
    small = [(120, 120, 0.3), (270, 90, 0.5), (390, 150, 1.2), (560, 110, 1.4), (700, 170, 2.2), (870, 130, 2.4)]
    for i, (x, h, t) in enumerate(small):                       # the skyline appears, then grows in three steps on "grow"
        for k, (f, a, b) in enumerate(((1.0, t, 4.3), (1.6, 4.3, 4.6 + 0.1 * i), (2.4, 4.6 + 0.1 * i, dur + 1))):
            s += g(f"b{i}_{k}", building(x, 860, 130, h * f, NAVY if i % 2 else "#2C4466", BLUE, 2), (a, b), rig(x + 65, 860, 1, 0.5))
    s += g("arrow", f'<path d="M180 640 L860 330" stroke="{ORANGE}" stroke-width="22" stroke-linecap="round"/><path d="M820 300 L910 310 L860 390Z" fill="{ORANGE}"/>',
           (4.9, dur + 1))
    return s + "</svg>\n"


def build():
    dur = 2.8
    s = root(dur, "1,0,0")
    for i, (c, t) in enumerate(((NAVY, 0.1), (ORANGE, 0.4), (GOLD, 0.7))):
        s += g(f"blk{i}", f'<rect x="{150 + 30 * (i % 2)}" y="{760 - 150 * i}" width="300" height="130" rx="12" fill="{c}"/>', (t, dur + 1), rig(300, 890 - 150 * i, 2, 0.8))
    s += pill("prog", 320, 260, "Program", 56, NAVY, CREAM, (0.9, dur + 1))
    tgt = "".join(f'<circle cx="820" cy="560" r="{r}" fill="{c}"/>' for r, c in ((170, NAVY), (120, CREAM), (70, ORANGE), (25, CREAM)))
    s += g("tgt", tgt, (0.05, dur + 1), rig(820, 730, 1, 0.5))
    for i, (x, y, t) in enumerate(((470, 690, 1.3), (620, 620, 1.45))):
        s += g(f"ar{i}", f'<path d="M{x - 120} {y + 60} L{x} {y}" stroke="{GOLD}" stroke-width="18" stroke-linecap="round"/>', (t, t + 0.15))
    s += g("hit", f'<path d="M560 680 L812 562" stroke="{GOLD}" stroke-width="18" stroke-linecap="round"/><path d="M800 548 L840 560 L808 590Z" fill="{NAVY}"/>', (1.6, dur + 1))
    s += check("ok", 900, 330, 2.1, dur, 90)
    return s + "</svg>\n"


def cohort():
    dur = 6.2
    s = root(dur, "1,0,0")
    for i, (p, x, t) in enumerate(((2, 150, 0.2), (5, 330, 0.45), (8, 510, 0.7), (3, 690, 0.95))):
        s += head(p, [(t, "neutral"), (3.4 + 0.2 * i, "happy")], (x, 1010), 0.42, i % 2 == 1, f"f{i}")
    s += pill("co", 420, 170, "Cohort", 64, NAVY, CREAM, (2.2, dur + 1))
    s += pill("de", 830, 170, "Design", 52, ORANGE, CREAM, (3.5, dur + 1))
    s += g("box", f'<path d="M700 520 L860 450 L1020 520 L860 590Z" fill="{GOLD}"/><path d="M700 520 L860 590 L860 760 L700 690Z" fill="{ORANGE}"/>'
                  f'<path d="M1020 520 L860 590 L860 760 L1020 690Z" fill="#B53A26"/>', (3.9, dur + 1), rig(860, 760, 3, 1.0))
    s += pill("pr", 860, 360, "Products", 48, NAVY, CREAM, (4.3, dur + 1))
    s += pill("sv", 860, 850, "Services", 48, NAVY, CREAM, (5.1, dur + 1))
    return s + "</svg>\n"


def advocate():
    dur = 4.8
    s = root(dur, "1,0,0")
    s += g("line", f'<rect x="80" y="700" width="920" height="16" rx="8" fill="{NAVY}"/>', (0.05, dur + 1))
    s += head(CAM_P, [(0.05, "happy"), (2.0, "excited")], (220, 650), 0.5, False, "cam")
    s += g("bot", robot(400, 560, 2.2), (0.3, dur + 1), rig(400, 620, 6, 1.3))
    s += g("y19", f'<circle cx="300" cy="708" r="26" fill="{ORANGE}"/>' + centered(300, 820, "2019", 70, ORANGE), (1.6, dur + 1), rig(300, 820, 3, 0.9))
    s += steps("dot", lambda x, y: f'<circle cx="{x}" cy="{y}" r="20" fill="{GOLD}"/>', [(330 + 90 * i, 708) for i in range(6)], 2.0, 3.6, dur,
               r=lambda x, y: rig(x, y, 1, 0.5))
    s += g("y22", f'<circle cx="840" cy="708" r="26" fill="{NAVY}"/><rect x="680" y="440" width="320" height="140" rx="16" fill="{WHITE}"/>'
                  + centered(840, 500, "ChatGPT", 54, NAVY) + centered(840, 560, "2022", 44, GREY) + centered(840, 820, "later", 56, NAVY),
           (3.8, dur + 1), rig(840, 708, 3, 0.9))
    return s + "</svg>\n"


def world():
    dur = 7.4
    s = root(dur, "1,0,0").split('  <g id="floor"')[0]
    stops = [("Brazil", (-52, -10), 1.6), ("India", (79, 21), 2.6), ("South Korea", (127, 36), 3.6),
             ("Europe", (12, 48), 4.9), ("Latin America", (-70, 0), 6.3)]
    EU = ["France", "Germany", "Spain", "Italy", "Poland", "Netherlands", "Belgium", "Portugal", "Austria", "Czechia", "Hungary",
          "Sweden", "Norway", "Finland", "Denmark", "Romania", "Greece", "Ireland", "United Kingdom", "Switzerland", "Croatia", "Slovakia", "Bulgaria"]
    LA = ["Mexico", "Guatemala", "Colombia", "Peru", "Chile", "Argentina", "Ecuador", "Bolivia", "Venezuela", "Uruguay", "Paraguay",
          "Costa Rica", "Panama", "Honduras", "Nicaragua", "El Salvador", "Dominican Republic"]
    group = {"Brazil": ["Brazil"], "India": ["India"], "South Korea": ["South Korea"], "Europe": EU, "Latin America": LA}
    done, c, t = {}, (-30, 10), 0.0
    s += g("g0", globe(c, {}), (0.0, 0.9))
    t, k = 0.9, 1
    for name, tc, tl in stops:                                    # spin to each place (4 eased steps), then light it
        steps_n = 4
        t_spin0, t_spin1 = t, tl - 0.15
        for i in range(1, steps_n + 1):
            f = (1 - math.cos(math.pi * i / steps_n)) / 2
            dl = ((tc[0] - c[0] + 180) % 360) - 180
            cc = (c[0] + dl * f, c[1] + (tc[1] - c[1]) * f)
            a = t_spin0 + (t_spin1 - t_spin0) * (i - 1) / steps_n
            b = t_spin0 + (t_spin1 - t_spin0) * i / steps_n
            s += g(f"g{k}", globe(cc, done), (a, b)); k += 1
        c = tc
        nxt = [st[2] for st in stops if st[2] > tl]
        end = (nxt[0] - 0.15 - 0.6) if nxt else dur + 1
        lit = {**done, **{n: ORANGE for n in group[name]}}
        s += g(f"g{k}", globe(c, lit), (tl - 0.15, end)); k += 1
        done = {**done, **{n: GOLD for n in group[name]}}
        w = len(name) * 36 + 70
        s += g(f"n{k}", f'<rect x="{540 - w / 2:.0f}" y="880" width="{w:.0f}" height="100" rx="14" fill="{ORANGE}"/>' + centered(540, 952, name, 64, CREAM),
               (tl - 0.1, (nxt[0] - 0.15) if nxt else dur + 1), rig(540, 980, 2, 0.6))
        x, y, _ = ortho(*tc, c)
        s += g(f"pin{k}", f'<path d="M{x:.0f} {y:.0f} Q{x - 22:.0f} {y - 30:.0f} {x - 20:.0f} {y - 44:.0f} A21 21 0 1 1 {x + 20:.0f} {y - 44:.0f} Q{x + 22:.0f} {y - 30:.0f} {x:.0f} {y:.0f}Z" '
                              f'fill="{ORANGE}" stroke="{CREAM}" stroke-width="4"/><circle cx="{x:.0f}" cy="{y - 47:.0f}" r="8" fill="{CREAM}"/>',
               (tl, end), rig(x, y, 4, 1.0))
        t = end
    return s + "</svg>\n"


def partners():
    dur = 3.5
    s = root(dur, "1,0,0")
    gov = (f'<path d="M80 420 L280 320 L480 420Z" fill="{NAVY}"/><rect x="100" y="420" width="360" height="30" fill="{NAVY}"/>'
           + "".join(f'<rect x="{120 + 80 * i}" y="460" width="40" height="230" fill="{WHITE}"/>' for i in range(5))
           + f'<rect x="90" y="690" width="380" height="40" fill="{NAVY}"/>')
    s += g("gov", gov, (0.05, dur + 1), rig(280, 730, 1, 0.5))
    s += pill("gl", 280, 200, "Government", 46, NAVY, CREAM, (0.2, dur + 1))
    s += g("edo", building(600, 730, 300, 380, ORANGE, CREAM, 3), (0.6, dur + 1), rig(750, 730, 1, 0.5))
    s += pill("el", 760, 200, "Economic development", 40, ORANGE, CREAM, (0.8, dur + 1))
    s += head(CAM_P, [(2.2, "happy"), (2.9, "excited")], (540, 1040), 0.5, False, "cam")
    s += g("j1", f'<path d="M280 760 Q400 900 470 900" stroke="{GOLD}" stroke-width="14" fill="none" stroke-linecap="round"/>', (2.6, dur + 1))
    s += g("j2", f'<path d="M750 760 Q680 900 610 900" stroke="{GOLD}" stroke-width="14" fill="none" stroke-linecap="round"/>', (2.75, dur + 1))
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("AI-native", "founders", 2.4, 0.7)), ("t2", lambda: two("Go after", "customers", 2.4, 1.2)),
                 ("t3", lambda: two("Give me", "a ping", 2.6, 0.5)),
                 ("b1", intro), ("b2", region), ("b3", build), ("b4", cohort), ("b5", advocate), ("b6", world), ("b7", partners)):
        open(os.path.join(HERE, f"scenes/fp-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/fp-{n}.svg")
