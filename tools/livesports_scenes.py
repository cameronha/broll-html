"""B-roll for "live sports" (raw 2026-11-02 15-13-48; graded file offset 539.92) -> scenes/ls-*.svg
First video with STAGED scenes (full bodies in a place, no labels) at the story moments, and a different ground per beat.
Local beat times; windows in videos/livesports.json (graded time = 539.5 + audio time).
b1 stands    STAGED  Cam in a row of fans at the Texas game; the fans cheer
b2 tv        STAGED  Cam on the couch, a game on TV
b3 feeds     navy    four people, each a phone with a different thing; the things change
b4 wall      STAGED  the whole stand, everyone the same way; a TEXAS banner drops
b5 nophone   blue    a phone gets an X; fans look up
b6 friends   cream   an old TV, six friends on a couch; "Finale"; 2004
b7 sets      cream   ten TV sets: three show the same show, "30%"; then every set shows a different thing
b8 five      STAGED  Cam and a fan high-five
t1 In the / moment      t2 Go see / live sports
"""
import os
import numpy as np
from PIL import Image
import cast_scenes as CS
from leon_scenes import calm, shade, robot, CREAM, NAVY, ORANGE, HERE, CAM_P, CAM
from linkedin_scenes import rig, g
from investors_scenes import head, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from nov2_parts import two, BLUE, WHITE
from staged_test import person, limb

TEX = "#BF5700"            # Texas burnt orange (the fans' shirts; set dressing, not a brand color)
WOOD, GREEN, STAND = "#B5835A", "#4F8F5B", "#27406A"
FANS = [1, 2, 3, 5, 9, 6, 8]


def skin(p):
    im = np.asarray(Image.open(os.path.join(CS.LIB, f"p{p}", "neutral.png")).convert("RGBA")).astype(float)
    h, w = im.shape[:2]
    box = im[int(h * .5):int(h * .62), int(w * .4):int(w * .6)].reshape(-1, 4)
    r, gr, b = np.median(box[box[:, 3] > 200][:, :3], axis=0)
    return "#%02X%02X%02X" % (int(r), int(gr), int(b))


SKIN = {p: skin(p) for p in FANS}
SKIN[CAM_P] = CAM["skin"]


def root(dur, bg=BLUE, floor=None):
    """floor = (y, color, color2) or None. A different ground per beat gives each cut a new picture."""
    CS.DUR = dur
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
         f'     data-bg="{bg}" data-finish="cut" data-variants="3" data-border="0" data-bg-boil="0.5" data-zoom="1,0,0" data-dur="{dur}">\n')
    if floor:
        y, c1, c2 = floor
        s += (f'  <g id="floor" data-static="1">\n    <rect x="-40" y="{y}" width="1160" height="{1130 - y}" fill="{c1}"/>\n'
              f'    <rect x="-40" y="{y + 50}" width="1160" height="{1080 - y}" fill="{c2}"/>\n  </g>\n')
    return s


UP_L, UP_R = ((-62, -30), (-18, -84), True), ((62, -30), (18, -84), True)
DN_L, DN_R = ((-10, 64), (-4, 56)), ((10, 64), (4, 56))


def fan(gid, p, cx, ground, s, tl, flip, up=True, cloth=TEX, arms=None):
    a = arms or ((UP_L, UP_R) if up else (DN_L, DN_R))
    return person(gid, cx, ground, s, cloth, SKIN[p], a[0], a[1], p, tl, flip, legs=False)


def far_stand(y0=250, y1=600):
    """The far side of the stadium: a navy tier full of small fans (dots), two light towers."""
    s = f'<path d="M-40 {y0 + 60} L1120 {y0} L1120 {y1} L-40 {y1}Z" fill="{STAND}"/>'
    k = 0
    for r in range(7):
        for c in range(27):
            x, y = 10 + c * 41 + (r % 2) * 20, y0 + 96 + r * 36 - c * 2
            if y < y1 - 24:
                s += f'<circle cx="{x}" cy="{y}" r="11" fill="{(TEX, CREAM, TEX, GOLD, TEX, "#8CBDDC")[k % 6]}"/>'
                k += 1
    for x in (150, 930):
        s += (f'<rect x="{x - 8}" y="{y0 - 170}" width="16" height="230" fill="{NAVY}"/>'
              f'<rect x="{x - 70}" y="{y0 - 210}" width="140" height="60" rx="8" fill="{NAVY}"/>'
              + "".join(f'<circle cx="{x - 46 + i * 31}" cy="{y0 - 180}" r="10" fill="{CREAM}"/>' for i in range(4)))
    return s


def rail(y, fill=NAVY, gid="rail"):
    return (f'  <g id="{gid}"><rect x="-40" y="{y}" width="1160" height="{1130 - y}" fill="{fill}"/>'
            f'<rect x="-40" y="{y}" width="1160" height="22" fill="{CREAM}"/></g>\n')


def stands():
    dur = 2.8
    s = root(dur)
    s += f'  <g id="far" data-static="1">\n    {far_stand()}\n    <rect x="-40" y="600" width="1160" height="500" fill="{GREEN}"/>\n  </g>\n'
    s += fan("f0", 2, 150, 1062, 0.88, [(0, "happy"), (1.5, "excited")], True)
    s += person("cam", 410, 1062, 0.88, CAM["cloth"], CAM["skin"], DN_L, ((40, 20), (20, -70), True), CAM_P,
                [(0, "neutral"), (0.7, "surprised"), (1.7, "happy")], True, legs=False)
    s += fan("f1", 1, 670, 1062, 0.88, [(0, "excited")], False)
    s += fan("f2", 9, 930, 1062, 0.88, [(0, "happy"), (1.1, "excited")], False)
    return s + rail(952) + "</svg>\n"


def tv():
    dur = 2.7
    s = root(dur, CREAM, (800, WOOD, shade(WOOD)))
    s += ('  <g id="set" data-static="1">\n'
          f'    <rect x="560" y="330" width="440" height="300" rx="16" fill="{NAVY}"/>'
          f'<rect x="760" y="630" width="40" height="70" fill="{NAVY}"/><rect x="620" y="696" width="320" height="110" rx="10" fill="{shade(WOOD, .7)}"/>\n'
          f'    <rect x="580" y="350" width="400" height="260" fill="{GREEN}"/>'
          + "".join(f'<rect x="{620 + i * 80}" y="350" width="6" height="260" fill="{CREAM}" opacity=".6"/>' for i in range(5))
          + f'<path d="M930 400 L930 480 M910 400 L950 400 M910 400 L910 370 M950 400 L950 370" stroke="{GOLD}" stroke-width="8" fill="none"/>\n  </g>\n')
    for i, (x, y) in enumerate(((640, 540), (720, 470), (800, 420), (880, 400))):          # the ball flies to the posts
        s += g(f"ball{i}", f'<ellipse cx="{x}" cy="{y}" rx="26" ry="16" fill="#7A4A2A" transform="rotate({-30 + i * 8} {x} {y})"/>',
               (0.3 + i * 0.4, 0.7 + i * 0.4 if i < 3 else dur + 1))
    s += g("couch-back", f'<rect x="40" y="610" width="460" height="300" rx="50" fill="{NAVY}"/>', None, rig(270, 910, 0.5, 0.4))
    s += person("cam", 270, 1010, 0.95, CAM["cloth"], CAM["skin"], DN_L, ((30, 50), (40, -20), True,
                f'<rect x="{270 + 66 + 28 + 38 - 12}" y="{1010 - 245 + 47 - 19 - 44}" width="26" height="60" rx="8" fill="{NAVY}"/>'),
                CAM_P, [(0, "neutral"), (1.5, "excited")], True, legs=False)
    s += g("couch-seat", f'<rect x="20" y="900" width="500" height="130" rx="40" fill="{shade(NAVY, 1.35)}"/>'
                         f'<rect x="20" y="800" width="90" height="230" rx="40" fill="{shade(NAVY, 1.35)}"/>'
                         f'<rect x="430" y="800" width="90" height="230" rx="40" fill="{shade(NAVY, 1.35)}"/>')
    return s + "</svg>\n"


def icon(kind, cx, cy, s=1.0):
    q = lambda v: f"{v * s:.0f}"
    if kind == "cat":
        return (f'<circle cx="{cx}" cy="{cy}" r="{q(46)}" fill="{GOLD}"/><path d="M{cx - 44 * s:.0f} {cy - 18 * s:.0f} L{cx - 36 * s:.0f} {cy - 66 * s:.0f} L{cx - 8 * s:.0f} {cy - 40 * s:.0f}Z '
                f'M{cx + 44 * s:.0f} {cy - 18 * s:.0f} L{cx + 36 * s:.0f} {cy - 66 * s:.0f} L{cx + 8 * s:.0f} {cy - 40 * s:.0f}Z" fill="{GOLD}"/>'
                f'<circle cx="{cx - 16 * s:.0f}" cy="{cy - 6 * s:.0f}" r="{q(6)}" fill="{NAVY}"/><circle cx="{cx + 16 * s:.0f}" cy="{cy - 6 * s:.0f}" r="{q(6)}" fill="{NAVY}"/>')
    if kind == "chart":
        return "".join(f'<rect x="{cx - 50 * s + i * 36 * s:.0f}" y="{cy + 44 * s - h * s:.0f}" width="{q(26)}" height="{q(h)}" fill="{c}"/>'
                       for i, (h, c) in enumerate(((40, NAVY), (64, NAVY), (92, ORANGE))))
    if kind == "robot":
        return robot(cx, cy + 30 * s, 2.0 * s)
    if kind == "heart":
        return (f'<path d="M{cx} {cy + 44 * s:.0f} L{cx - 48 * s:.0f} {cy - 6 * s:.0f} A{q(26)} {q(26)} 0 0 1 {cx} {cy - 26 * s:.0f} '
                f'A{q(26)} {q(26)} 0 0 1 {cx + 48 * s:.0f} {cy - 6 * s:.0f}Z" fill="{ORANGE}"/>')
    if kind == "pizza":
        return (f'<path d="M{cx - 46 * s:.0f} {cy - 40 * s:.0f} L{cx + 46 * s:.0f} {cy - 40 * s:.0f} L{cx} {cy + 50 * s:.0f}Z" fill="{GOLD}"/>'
                f'<rect x="{cx - 50 * s:.0f}" y="{cy - 50 * s:.0f}" width="{q(100)}" height="{q(16)}" rx="{q(8)}" fill="{WOOD}"/>'
                f'<circle cx="{cx - 10 * s:.0f}" cy="{cy - 12 * s:.0f}" r="{q(9)}" fill="{ORANGE}"/><circle cx="{cx + 12 * s:.0f}" cy="{cy + 6 * s:.0f}" r="{q(8)}" fill="{ORANGE}"/>')
    if kind == "note":
        return (f'<rect x="{cx - 4 * s:.0f}" y="{cy - 48 * s:.0f}" width="{q(10)}" height="{q(84)}" fill="{NAVY}"/><ellipse cx="{cx - 16 * s:.0f}" cy="{cy + 36 * s:.0f}" rx="{q(22)}" ry="{q(16)}" fill="{NAVY}"/>'
                f'<path d="M{cx + 6 * s:.0f} {cy - 48 * s:.0f} L{cx + 44 * s:.0f} {cy - 30 * s:.0f} L{cx + 44 * s:.0f} {cy - 8 * s:.0f} L{cx + 6 * s:.0f} {cy - 26 * s:.0f}Z" fill="{NAVY}"/>')
    if kind == "plane":
        return (f'<path d="M{cx - 54 * s:.0f} {cy + 6 * s:.0f} L{cx + 54 * s:.0f} {cy - 40 * s:.0f} L{cx + 10 * s:.0f} {cy + 46 * s:.0f} L{cx - 4 * s:.0f} {cy + 12 * s:.0f}Z" fill="#5E7A94"/>')
    if kind == "couch":
        return (f'<rect x="{cx - 50 * s:.0f}" y="{cy - 24 * s:.0f}" width="{q(100)}" height="{q(44)}" rx="{q(14)}" fill="{ORANGE}"/>'
                f'<rect x="{cx - 60 * s:.0f}" y="{cy - 4 * s:.0f}" width="{q(120)}" height="{q(36)}" rx="{q(12)}" fill="{shade(ORANGE)}"/>')
    if kind == "ball":
        return f'<circle cx="{cx}" cy="{cy}" r="{q(42)}" fill="{CREAM}" stroke="{NAVY}" stroke-width="{q(8)}"/><path d="M{cx - 40 * s:.0f} {cy} L{cx + 40 * s:.0f} {cy} M{cx} {cy - 40 * s:.0f} L{cx} {cy + 40 * s:.0f}" stroke="{NAVY}" stroke-width="{q(7)}"/>'
    return f'<path d="M{cx} {cy - 50 * s:.0f} L{cx + 16 * s:.0f} {cy - 14 * s:.0f} L{cx + 52 * s:.0f} {cy - 12 * s:.0f} L{cx + 24 * s:.0f} {cy + 12 * s:.0f} L{cx + 32 * s:.0f} {cy + 48 * s:.0f} L{cx} {cy + 28 * s:.0f} L{cx - 32 * s:.0f} {cy + 48 * s:.0f} L{cx - 24 * s:.0f} {cy + 12 * s:.0f} L{cx - 52 * s:.0f} {cy - 12 * s:.0f} L{cx - 16 * s:.0f} {cy - 14 * s:.0f}Z" fill="{GOLD}"/>'   # star


def feeds():
    dur = 6.0
    s = root(dur, NAVY, (900, "#0F1D33", "#0F1D33"))
    A, B, C = ("cat", "chart", "robot", "heart"), ("pizza", "note", "plane", "star"), ("ball", "couch", "cat", "chart")
    for i, (p, x, t) in enumerate(((2, 150, 0.15), (3, 410, 0.9), (CAM_P, 670, 1.9), (5, 930, 2.7))):
        s += head(p, [(max(0.05, t - 0.1), "neutral"), (4.6 + i * 0.1, "tired")], (x, 1040), 0.44, i % 2 == 0, f"h{i}")
        s += g(f"ph{i}", f'<rect x="{x - 96}" y="360" width="192" height="330" rx="26" fill="{WHITE}"/>'
                         f'<rect x="{x - 96}" y="360" width="192" height="44" rx="22" fill="#8CBDDC"/><rect x="{x - 60}" y="640" width="120" height="14" rx="7" fill="#C9CED6"/>',
               (t, dur + 1), rig(x, 690, 1.5, 0.5 + i * 0.1))
        t1, t2 = 3.5 + i * 0.25, 4.7 + i * 0.2
        for k, (kind, a, b) in enumerate(((A[i], t + 0.05, t1), (B[i], t1, t2), (C[i], t2, dur + 1))):
            s += g(f"ic{i}{k}", icon(kind, x, 520, 1.15), (a, b), rig(x, 580, 3, 0.9 + i * 0.1))
    return s + "</svg>\n"


def wall():
    dur = 4.6
    s = root(dur, STAND)
    s += ('  <g id="tiers" data-static="1">\n'
          + "".join(f'    <rect x="-40" y="{y}" width="1160" height="16" fill="{shade(STAND, 1.25)}"/>\n' for y in (120, 180, 240)) + '  </g>\n')
    rows = ((520, (160, 420, 680, 940), (1, 3, 9, 2)), (780, (290, 550, 810), (5, CAM_P, 6)), (1040, (160, 420, 680, 940), (9, 8, 1, 3)))
    k = 0
    for r, (gy, xs, ps) in enumerate(rows):
        for c, (x, p) in enumerate(zip(xs, ps)):
            t = 0.25 + (x / 1080) * 1.5                                   # the cheer runs left to right, like a wave
            cam = p == CAM_P
            s += fan(f"w{k}", p, x, gy, 0.62, [(0, "neutral" if r else "happy"), (t, "excited" if not cam else "happy"), (3.0 + (x / 1080) * 0.8, "excited")],
                     x < 540, cloth=CAM["cloth"] if cam else (TEX, CREAM, TEX, GOLD)[k % 4])
            k += 1
        s += rail(gy - 62, shade(STAND, 0.8), f"rail{r}")[:-1].replace(f'height="{1130 - (gy - 62)}"', 'height="64"') + "\n"
    s += g("banner", f'<rect x="250" y="40" width="580" height="150" rx="10" fill="{CREAM}"/><rect x="250" y="40" width="580" height="22" fill="{TEX}"/>'
                     + centered(540, 158, "TEXAS", 110, TEX), (2.3, dur + 1), rig(540, 40, 2.5, 1.0))
    return s + "</svg>\n"


def nophone():
    dur = 3.5
    s = root(dur, BLUE, (746, "#6E9FC4", "#5A8BB3"))
    s += g("phone", f'<rect x="150" y="200" width="300" height="520" rx="40" fill="{NAVY}"/><rect x="172" y="250" width="256" height="400" rx="8" fill="{CREAM}"/>'
                    + "".join(f'<rect x="196" y="{280 + i * 62}" width="{(200, 150, 180, 120, 190)[i]}" height="24" rx="10" fill="#C9CED6"/>' for i in range(5))
                    + f'<circle cx="300" cy="686" r="16" fill="{CREAM}"/>', (0.1, dur + 1), rig(300, 720, 3, 0.8))
    s += xmark("x", 300, 450, (0.5, dur + 1), 130)
    for i, (p, x, y, t) in enumerate(((1, 640, 640, 1.5), (CAM_P, 880, 560, 1.9), (9, 700, 1010, 2.3), (3, 950, 960, 2.6))):
        s += head(p, [(t, "happy"), (t + 0.5, "excited")], (x, y), 0.46, True, f"u{i}")
    return s + "</svg>\n"


def old_tv(x, y, w=560, h=420):
    return (f'<path d="M{x + w * .35:.0f} {y - 90} L{x + w * .5:.0f} {y + 6} L{x + w * .7:.0f} {y - 110}" stroke="{NAVY}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{WOOD}"/>'
            f'<rect x="{x + 30}" y="{y + 30}" width="{w - 150}" height="{h - 60}" rx="40" fill="#CFE4F2"/>'
            f'<circle cx="{x + w - 62}" cy="{y + 90}" r="30" fill="{NAVY}"/><circle cx="{x + w - 62}" cy="{y + 176}" r="30" fill="{NAVY}"/>'
            + "".join(f'<rect x="{x + w - 96}" y="{y + 240 + i * 26}" width="68" height="10" rx="5" fill="{shade(WOOD, .7)}"/>' for i in range(5))
            + f'<rect x="{x + 60}" y="{y + h}" width="30" height="50" fill="{NAVY}"/><rect x="{x + w - 90}" y="{y + h}" width="30" height="50" fill="{NAVY}"/>')


def friends():
    dur = 4.5
    s = root(dur, CREAM, (800, NAVY, shade(NAVY, .8)))
    s += g("tv", old_tv(90, 300), (0.05, dur + 1), rig(370, 770, 0.8, 0.5))
    s += g("sofa", f'<rect x="150" y="540" width="350" height="70" rx="26" fill="{ORANGE}"/><rect x="134" y="590" width="382" height="60" rx="22" fill="{shade(ORANGE)}"/>', (0.2, dur + 1))
    for i, p in enumerate((3, 9, 5, 2, 1, 6)):
        s += head(p, [(0.35 + i * 0.12, "happy"), (3.3 + i * 0.06, "excited")], (176 + i * 60, 560), 0.17, i < 3, f"fr{i}", deg=3)
    s += pill("fin", 800, 330, "Finale", 70, ORANGE, CREAM, (1.3, dur + 1), 3)
    s += g("cal", f'<rect x="680" y="470" width="300" height="270" rx="14" fill="{WHITE}"/><rect x="680" y="470" width="300" height="70" rx="14" fill="{ORANGE}"/>'
                  f'<circle cx="740" cy="470" r="14" fill="{NAVY}"/><circle cx="920" cy="470" r="14" fill="{NAVY}"/>' + centered(830, 690, "2004", 104, NAVY),
           (2.5, dur + 1), rig(830, 470, 3, 0.9))
    return s + "</svg>\n"


def sets():
    dur = 5.3
    s = root(dur, CREAM, (880, NAVY, shade(NAVY, .8)))
    kinds = ("cat", "chart", "robot", "heart", "pizza", "note", "plane", "star", "ball", "couch")
    same = (1, 5, 8)
    for i in range(10):
        x, y = 130 + (i % 5) * 205, 330 + (i // 5) * 250
        on = i in same
        s += g(f"tv{i}", f'<rect x="{x - 88}" y="{y - 70}" width="176" height="150" rx="18" fill="{NAVY}"/>'
                         f'<rect x="{x - 72}" y="{y - 56}" width="144" height="110" rx="10" fill="#5E7A94"/>'
                         f'<rect x="{x - 50}" y="{y + 80}" width="100" height="14" rx="6" fill="{NAVY}"/>', (0.05 + i * 0.04, dur + 1), rig(x, y + 90, 1.5 if on else 0.6, 0.8))
        t_frag = 3.3 + i * 0.07
        if on:
            t = 0.35 + same.index(i) * 0.3
            s += g(f"glow{i}", f'<rect x="{x - 72}" y="{y - 56}" width="144" height="110" rx="10" fill="{CREAM}"/>' + icon("couch", x, y, 0.8), (t, t_frag), rig(x, y + 90, 1.5, 0.8))
        s += g(f"frag{i}", f'<rect x="{x - 72}" y="{y - 56}" width="144" height="110" rx="10" fill="{(CREAM, "#8CBDDC", WHITE)[i % 3]}"/>' + icon(kinds[i], x, y, 0.72),
               (t_frag, dur + 1), rig(x, y + 90, 4, 1.0 + (i % 4) * 0.25))
    s += pill("pct", 540, 130, "30%", 96, ORANGE, CREAM, (0.9, 3.3), -2)
    s += pill("same", 540, 800, "Same show", 60, NAVY, CREAM, (2.0, 3.3), 2)
    return s + "</svg>\n"


def five():
    dur = 3.2
    s = root(dur)
    s += f'  <g id="far" data-static="1">\n    {far_stand(120, 560)}\n    <rect x="-40" y="560" width="1160" height="600" fill="{GREEN}"/>\n  </g>\n'
    lo, hi = ((54, -40), (26, -54), True), ((48, -86), (26, -110), True)
    s += person("cam", 330, 1170, 1.2, CAM["cloth"], CAM["skin"], DN_L, hi, CAM_P, [(0, "happy"), (1.0, "excited")], True, legs=False)
    s += person("fan", 750, 1170, 1.2, TEX, SKIN[2], ((-48, -86), (-26, -110), True), DN_R, 2, [(0, "happy"), (0.9, "excited")], False, legs=False)
    for i, (dx, dy) in enumerate(((0, -70), (-56, -44), (56, -44))):
        s += g(f"sp{i}", f'<line x1="{540 + dx * .5:.0f}" y1="{590 + dy * .5:.0f}" x2="{540 + dx:.0f}" y2="{590 + dy:.0f}" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/>',
               (1.0, dur + 1), rig(540, 590, 6, 2.0))
    return s + rail(1010) + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("In the", "moment", 2.5, 0.5)), ("t2", lambda: two("Go see", "live sports", 2.6, 0.45)),
                 ("b1", stands), ("b2", tv), ("b3", feeds), ("b4", wall), ("b5", nophone), ("b6", friends), ("b7", sets), ("b8", five)):
        open(os.path.join(HERE, f"scenes/ls-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/ls-{n}.svg")
