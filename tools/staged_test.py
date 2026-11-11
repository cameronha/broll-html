"""Staged-scene test (2026-11-11): the trust video's gym beat with full bodies in a place, no labels.
Writes scenes/st-wide.svg (Cam at the front desk, the manager points back at the young members)
and scenes/st-close.svg (close shot of the manager).
"""
import os
import cast_scenes as CS
from leon_scenes import root, calm, shade, CREAM, NAVY, ORANGE, HERE, CAM_P, CAM, PANTS

MGR = 9
GOLD, WOOD, WALL, GREY = "#E9B949", "#B5835A", "#A9CDE6", "#3B4A5E"


def limb(a, b, c, w, col, skin, hand=True):
    """Upper arm a->b, forearm b->c, hand at c."""
    s = (f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{col}" stroke-width="{w:.0f}" stroke-linecap="round"/>'
         f'<line x1="{b[0]:.0f}" y1="{b[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="{col}" stroke-width="{w * .9:.0f}" stroke-linecap="round"/>')
    if hand:
        s += f'<circle cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="{w * .5:.0f}" fill="{skin}"/>'
    return s


def person(gid, cx, ground, s, cloth, skin, armL, armR, person_id, tl, flip, legs=True, back="", sway=1, pants=PANTS):
    """Standing frontal person. armL / armR = ((elbow dx, dy), (hand dx, dy), front?) from the shoulder, in body units.
    back = extra shapes drawn behind the torso (a bag). Returns body group + arm groups + head groups."""
    X = lambda v: cx + v * s
    Y = lambda v: ground - v * s
    rig = f' data-pivot="{cx:.0f},{ground:.0f}" data-deg="{sway}" data-freq="0.4" data-shape="sine"'
    out, front = "", ""
    body = back
    if legs:
        body += (f'<rect x="{X(-50):.0f}" y="{Y(124):.0f}" width="{44 * s:.0f}" height="{122 * s:.0f}" rx="{20 * s:.0f}" fill="{pants}"/>'
                 f'<rect x="{X(6):.0f}" y="{Y(124):.0f}" width="{44 * s:.0f}" height="{122 * s:.0f}" rx="{20 * s:.0f}" fill="{pants}"/>'
                 f'<ellipse cx="{X(-36):.0f}" cy="{Y(0):.0f}" rx="{40 * s:.0f}" ry="{16 * s:.0f}" fill="{CREAM}"/>'
                 f'<ellipse cx="{X(34):.0f}" cy="{Y(0):.0f}" rx="{40 * s:.0f}" ry="{16 * s:.0f}" fill="{CREAM}"/>')
    arms = []
    for side, a in ((-1, armL), (1, armR)):
        sh = (X(side * 70), Y(258))
        el = (sh[0] + a[0][0] * s, sh[1] + a[0][1] * s)
        ha = (el[0] + a[1][0] * s, el[1] + a[1][1] * s)
        shape = limb(sh, el, ha, 40 * s, shade(cloth), skin)
        if len(a) > 2 and a[2]:
            arms.append((side, sh, shape + (a[3] if len(a) > 3 else "")))
        else:
            body += shape
    body += (f'<rect x="{X(-86):.0f}" y="{Y(294):.0f}" width="{172 * s:.0f}" height="{200 * s:.0f}" rx="{70 * s:.0f}" fill="{cloth}"/>'
             f'<rect x="{X(-20):.0f}" y="{Y(312):.0f}" width="{40 * s:.0f}" height="{34 * s:.0f}" fill="{skin}"/>')
    out += f'  <g id="{gid}-body"{rig}>{body}</g>\n'
    for side, sh, shape in arms:
        out += (f'  <g id="{gid}-arm{side + 1}" data-pivot="{sh[0]:.0f},{sh[1]:.0f}" data-deg="{-5 * side}" data-freq="1.1" data-shape="snap">'
                f'{shape}</g>\n')
    out += CS.head(person_id, tl, (X(4 if flip else -4), Y(296)), 0.62 * s, flip,
                   f' data-pivot="{cx:.0f},{Y(300):.0f}" data-deg="3" data-freq="0.7" data-shape="sine"', f"{gid}-head")
    return out


def rack(x, y):
    s = f'<rect x="{x}" y="{y}" width="230" height="14" fill="{GREY}"/><rect x="{x}" y="{y + 70}" width="230" height="14" fill="{GREY}"/>'
    s += f'<rect x="{x + 10}" y="{y - 20}" width="14" height="170" fill="{GREY}"/><rect x="{x + 206}" y="{y - 20}" width="14" height="170" fill="{GREY}"/>'
    for i in range(3):
        for r in (0, 70):
            cx = x + 50 + i * 65
            s += (f'<rect x="{cx - 22}" y="{y + r - 30}" width="14" height="30" rx="4" fill="{NAVY}"/>'
                  f'<rect x="{cx + 8}" y="{y + r - 30}" width="14" height="30" rx="4" fill="{NAVY}"/>'
                  f'<rect x="{cx - 10}" y="{y + r - 20}" width="20" height="9" fill="{ORANGE if (i + r) % 2 else GOLD}"/>')
    return s


def room():
    return ('  <g id="room" data-static="1">\n'
            f'    <rect x="-40" y="-40" width="1160" height="700" fill="{WALL}"/>\n'
            f'    <rect x="-40" y="640" width="1160" height="22" fill="{CREAM}"/>\n'
            f'    <rect x="60" y="120" width="330" height="300" rx="6" fill="{CREAM}"/>'
            f'<rect x="78" y="138" width="294" height="264" fill="#CFE4F2"/>'
            f'<path d="M78 330 L190 138 L260 138 L120 402 L78 402Z" fill="#E4F0F8"/>\n'
            f'    {rack(430, 500)}\n  </g>\n')


def dumbbell(x, y, k=1.0):
    return (f'<rect x="{x - 46 * k:.0f}" y="{y - 7 * k:.0f}" width="{92 * k:.0f}" height="{14 * k:.0f}" fill="{GREY}"/>'
            f'<rect x="{x - 60 * k:.0f}" y="{y - 26 * k:.0f}" width="{22 * k:.0f}" height="{52 * k:.0f}" rx="5" fill="{NAVY}"/>'
            f'<rect x="{x + 38 * k:.0f}" y="{y - 26 * k:.0f}" width="{22 * k:.0f}" height="{52 * k:.0f}" rx="5" fill="{NAVY}"/>')


def wide():
    dur = 4.5
    s = root(dur, "1,0,0") + room()
    # the young members, small, at the back of the room
    DOWN = ((-6, 62), (-2, 56))
    s += person("y0", 440, 790, 0.5, ORANGE, "#C98E62", ((-40, -50), (16, -66), True, dumbbell(440 - 35 - 20 + 8, 790 - 129 + 31 - 33 - 8, 0.5)),
                ((40, -50), (-16, -66), True), 2, [(0, "happy")], True)
    s += person("y1", 585, 790, 0.5, GOLD, "#8A5A3C", ((-6, 62), (-2, 56)), ((44, 10), (10, -70), True,
                f'<rect x="{585 + 35 + 22 + 5 - 13}" y="{790 - 129 + 5 - 35 - 50}" width="26" height="44" rx="5" fill="{NAVY}"/>'), 1, [(0, "excited")], True)
    # Cam, with a gym bag, at the front desk
    bag = (f'<rect x="60" y="760" width="150" height="84" rx="26" fill="{ORANGE}"/><rect x="60" y="792" width="150" height="14" fill="{shade(ORANGE)}"/>'
           f'<path d="M100 762 Q135 700 170 762" stroke="{NAVY}" stroke-width="10" fill="none"/>')
    s += person("cam", 250, 960, 1.15, CAM["cloth"], CAM["skin"], ((-14, 66), (-6, 58)), ((16, 62), (30, -40), True),
                CAM_P, [(0, "neutral"), (2.6, "happy")], True, back=bag)
    # the manager behind the desk: one thumb over his shoulder at the young members, one hand flat on the desk
    s += person("mgr", 880, 960, 1.15, NAVY, "#C99872", ((-50, 40), (-30, -70), True,
                f'<rect x="{880 - 80 - 57 - 34 - 44}" y="{960 - 297 + 46 - 80 - 14}" width="40" height="15" rx="7" fill="#C99872"/>'),
                ((20, 64), (-4, 50)), MGR, [(0, "skeptical"), (2.6, "happy")], False, legs=False)
    s += ('  <g id="desk">\n'
          f'    <rect x="620" y="786" width="520" height="34" rx="8" fill="{CREAM}"/>\n'
          f'    <rect x="640" y="820" width="500" height="400" fill="{WOOD}"/>\n'
          f'    <rect x="640" y="820" width="500" height="26" fill="{shade(WOOD)}"/>\n'
          f'    <rect x="1000" y="716" width="110" height="72" rx="8" fill="{NAVY}"/>\n  </g>\n')
    return s + "</svg>\n"


def close():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += ('  <g id="room" data-static="1">\n'
          f'    <rect x="-40" y="-40" width="1160" height="1200" fill="{WALL}"/>\n'
          f'    {rack(800, 240)}\n  </g>\n')
    s += person("y0", 130, 1012, 0.5, ORANGE, "#C98E62", ((-40, -50), (16, -66), True, dumbbell(130 - 35 - 20 + 8, 1012 - 129 + 31 - 33 - 8, 0.5)),
                ((40, -50), (-16, -66), True), 2, [(0, "happy")], True)
    # the manager, large: shoulders at the frame bottom, open hand raised ("honestly...")
    skin = "#C99872"
    s += (f'  <g id="mgr-body" data-pivot="470,1080" data-deg="1" data-freq="0.4" data-shape="sine">'
          f'<rect x="170" y="790" width="600" height="500" rx="200" fill="{NAVY}"/>'
          f'<rect x="400" y="730" width="140" height="110" fill="{skin}"/></g>\n')
    s += (f'  <g id="mgr-hand" data-pivot="800,1080" data-deg="-4" data-freq="1.1" data-shape="snap">'
          + limb((760, 1120), (850, 1000), (820, 760), 120, shade(NAVY), skin, hand=False)
          + f'<rect x="762" y="560" width="124" height="220" rx="52" fill="{skin}"/>'
          f'<path d="M772 700 L716 640" stroke="{skin}" stroke-width="44" stroke-linecap="round"/></g>\n')
    s += CS.head(MGR, [(0, "skeptical"), (1.8, "happy")], (462, 800), 1.75, False,
                 ' data-pivot="470,800" data-deg="3" data-freq="0.7" data-shape="sine"', "mgr-head")
    s += (f'  <g id="desk"><rect x="-40" y="1010" width="1160" height="120" fill="{WOOD}"/>'
          f'<rect x="-40" y="990" width="1160" height="30" rx="8" fill="{CREAM}"/></g>\n')
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("wide", wide), ("close", close)):
        open(os.path.join(HERE, f"scenes/st-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/st-{n}.svg")
