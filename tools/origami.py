"""Origami character system: one skeleton, three renderers (A flat, B sculptural, C hybrid modernist).

usage: python3 tools/origami.py        -> scenes/origami-A.svg, origami-B.svg, origami-C.svg

Proportions (standing figure, v10 coordinates, rendered with data-zoom 0.95,48,-12):
  height 774 (head top 186 -> sole 960); head 92 x 116 (~1/6.7 of height); shoulder width ~160;
  upper arm 150, forearm 125 (width 34 -> 26); leg 330 (width 52 -> 40).
Joints are listed per character below (SKELETONS); every limb is a quad built from its two joints
and a start/end width, so a new pose is a new joint table, not a new drawing.
Pieces (top-level <g id>) follow the rig: body groups, a head on a neck pivot, the pitching arm on a
shoulder pivot, the crossed foot on a knee pivot. Sub-parts are <g data-part> (not separate pieces).
"""
import math, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# palette: (light, mid, dark) per material
PAL = {
    "orange": ("#F2925E", "#E8692E", "#BF4D1C"),
    "red":    ("#E06A55", "#C8402F", "#9C2E20"),
    "slate":  ("#86A0A0", "#5F7A7A", "#435A5B"),
    "cream":  ("#FBF8F2", "#EFE9DD", "#D8D0C1"),
    "navy":   ("#3A4D72", "#22314D", "#141F35"),
    "skin":   ("#F4CBA9", "#E6AE86", "#C98F68"),
    "hair":   ("#2E3648", "#1E2433", "#121722"),
    "shoe":   ("#5A4334", "#3B2A20", "#271A13"),
}

SKELETONS = {
    "founder": dict(head=(748, 250), tilt=-10, neck=((752, 294), (752, 340)),
                    torso=[(672, 336), (836, 350), (850, 470), (836, 628), (704, 628), (690, 500)],
                    hood=[(716, 322), (800, 326), (808, 354), (760, 372), (712, 352)],
                    arm_near=((690, 365), (590, 478), (494, 400)), arm_far=((834, 362), (910, 490), (838, 582)),
                    hand_near=[(466, 372), (496, 368), (502, 402), (474, 408)], hand_far=[(812, 566), (840, 578), (830, 604), (806, 592)],
                    leg_near=((740, 612), (705, 772), (670, 932)), leg_far=((796, 610), (838, 772), (880, 932)),
                    shoe_near=[(600, 934), (684, 928), (694, 956), (596, 960)], shoe_far=[(842, 934), (910, 930), (926, 956), (838, 960)]),
    "customer": dict(head=(238, 380), tilt=-14, neck=((242, 426), (242, 476)),
                     torso=[(178, 478), (300, 466), (338, 560), (342, 742), (196, 746), (186, 600)],
                     upper_l=((190, 484), (200, 606)), upper_r=((312, 476), (322, 598)),
                     fore_under=((196, 612), (330, 604)), fore_top=((186, 602), (326, 584)),
                     hand_l=[(172, 600), (196, 596), (198, 622), (174, 624)], hand_r=[(318, 572), (346, 568), (348, 594), (322, 598)],
                     leg_low=((250, 745), (440, 766), (424, 930)), leg_top=((270, 724), (466, 732), (534, 856)),
                     shoe_low=[(396, 928), (452, 924), (470, 946), (392, 950)], shoe_top=[(508, 848), (560, 840), (586, 868), (518, 876)]),
}

# head outline, local coords, facing left (nose at -x), 92 x 116
HEAD = [(-28, -58), (30, -56), (46, -16), (42, 26), (20, 54), (-14, 58), (-38, 36), (-44, 18), (-54, 4), (-44, -20)]
HAIR = [(-32, -60), (32, -58), (48, -16), (44, 22), (30, 12), (24, -30), (-8, -38), (-40, -28)]


def P(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def poly(pts, fill):
    return f'<polygon points="{P(pts)}" fill="{fill}"/>'


def quad(p, q, w1, w2):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    return [(p[0] + nx * w1 / 2, p[1] + ny * w1 / 2), (q[0] + nx * w2 / 2, q[1] + ny * w2 / 2),
            (q[0] - nx * w2 / 2, q[1] - ny * w2 / 2), (p[0] - nx * w1 / 2, p[1] - ny * w1 / 2)]


def mid(a, b, t=0.5):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def head_pts(c, tilt, pts):
    a = math.radians(tilt)
    return [(c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)) for x, y in pts]


class Style:
    """Renderer. limb() and plane() decide how a part is folded."""
    def __init__(self, mode):
        self.m = mode

    def limb(self, p, q, w1, w2, mat):
        L, M, D = PAL[mat]
        qd = quad(p, q, w1, w2)
        if self.m == "A":
            return poly(qd, M)
        if self.m == "B":       # split along the length: lit side and shade side
            a, b = mid(qd[0], qd[3]), mid(qd[1], qd[2])
            return poly([qd[0], qd[1], b, a], L) + poly([a, b, qd[2], qd[3]], D)
        # C: flat limb with a fold triangle at the far joint
        return poly(qd, M) + poly([qd[1], qd[2], mid(qd[2], qd[3], 0.25)], D)

    def joint(self, j, w, mat):
        L, M, D = PAL[mat]
        r = w / 2
        return poly([(j[0] - r, j[1]), (j[0], j[1] - r), (j[0] + r, j[1]), (j[0], j[1] + r)], D if self.m == "B" else M)

    def torso(self, pts, mat, mat2=None):
        L, M, D = PAL[mat]
        top_l, top_r, side_r, bot_r, bot_l, side_l = pts
        if self.m == "A":       # one side plane folded back
            a, b = mid(top_l, top_r, 0.72), mid(bot_l, bot_r, 0.68)
            return poly(pts, M) + poly([a, top_r, side_r, bot_r, b], D)
        if self.m == "B":       # four facets: centre ridge + chest fold
            t, bt = mid(top_l, top_r, 0.52), mid(bot_l, bot_r, 0.5)
            c = mid(t, bt, 0.45)
            return (poly([top_l, t, c, side_l], L) + poly([side_l, c, bt, bot_l], M)
                    + poly([t, top_r, side_r, c], M) + poly([c, side_r, bot_r, bt], D))
        # C: Malevich split, two materials
        t, bt = mid(top_l, top_r, 0.5), mid(bot_l, bot_r, 0.5)
        L2, M2, D2 = PAL[mat2 or mat]
        return poly([top_l, t, bt, bot_l, side_l], M) + poly([t, top_r, side_r, bot_r, bt], M2) + poly([t, mid(t, bt, 0.22), mid(t, top_r, 0.5)], D2)

    def head(self, c, tilt, mood):
        L, M, D = PAL["skin"]
        H = lambda pts: head_pts(c, tilt, pts)
        out = []
        if self.m == "B":       # four facets around the nose ridge, nearly faceless
            o = (-20, 0)
            hp = HEAD
            out += [poly(H([hp[9], hp[8], o, hp[0]]), L), poly(H([hp[8], hp[7], hp[6], o]), M),
                    poly(H([o, hp[6], hp[5], hp[4]]), D), poly(H([o, hp[4], hp[3], hp[2], hp[1], hp[0]]), M)]
        else:
            out.append(poly(H(HEAD), M))
            if self.m == "A":
                out.append(poly(H([(8, -44), (46, -16), (42, 26), (20, 54), (2, 30)]), D))
            else:               # C: split head, front light / back dark
                out.append(poly(H([(0, -57), (30, -56), (46, -16), (42, 26), (20, 54), (0, 57)]), D))
        out.append(poly(H(HAIR), PAL["hair"][1]))
        if self.m == "B":
            out.append(poly(H([(-36, -6), (-20, -8), (-20, -5), (-36, -3)]), PAL["hair"][2]))
            return "".join(out)
        lid = 1.5 if mood == "skeptic" else 3.5
        out.append(poly(H([(-38, -8), (-20, -9), (-20, -9 + lid), (-38, -8 + lid)]), "#141F35"))
        brow = [(-42, -22), (-18, -26), (-18, -22), (-42, -18)] if mood == "skeptic" else [(-42, -20), (-18, -20), (-18, -16), (-42, -16)]
        out.append(poly(H(brow), PAL["hair"][1]))
        mouth = [(-40, 30), (-24, 29), (-24, 32), (-40, 33)] if mood == "skeptic" else [(-42, 27), (-24, 30), (-26, 34), (-40, 31)]
        out.append(poly(H(mouth), "#8E3A26"))
        return "".join(out)

    def shoe(self, pts):
        L, M, D = PAL["cream"]
        a, b = mid(pts[0], pts[1]), mid(pts[3], pts[2])
        return poly(pts, M) + ("" if self.m == "A" else poly([b, pts[2], pts[1], a], D))


def scene(mode):
    S = Style(mode)
    f, c = SKELETONS["founder"], SKELETONS["customer"]
    bg = {"A": "#E4DED3", "B": "#E7E1D6", "C": "#E9E1CF"}[mode]
    acc2_f = "red" if mode == "C" else None
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
         f'     data-bg="{bg}" data-variants="1" data-border="0" data-step="2" data-jitter="0" data-shadow="0.35" data-zoom="0.95,48,-12">\n'
         f'  <!-- origami {mode}: generated by tools/origami.py (edit the skeleton there, not here) -->\n']
    # scenery
    if mode == "A":
        floor = '<rect x="-40" y="746" width="1160" height="380" fill="#CFC7B9"/><rect x="-40" y="797" width="1160" height="330" fill="#C2B9A9"/>'
    elif mode == "B":           # a folded backdrop: wall and floor each in two planes
        floor = ('<polygon points="560,-40 1120,-40 1120,746 600,746" fill="#DBD4C7"/>'
                 '<polygon points="-40,746 1120,746 1120,1126 -40,1126" fill="#C7BEAE"/><polygon points="600,746 1120,746 1120,1126 380,1126" fill="#B8AE9C"/>')
    else:
        floor = ('<rect x="-40" y="700" width="1160" height="22" fill="#C8402F"/><rect x="-40" y="746" width="1160" height="51" fill="#C9B07E"/>'
                 '<rect x="-40" y="797" width="1160" height="330" fill="#8E9AA6"/>'
                 '<polygon points="540,797 -40,1126 60,1126" fill="#7F8B97"/><polygon points="540,797 1120,1126 1020,1126" fill="#7F8B97"/>')
    o.append(f'  <g id="floor" data-static="1">{floor}</g>\n')
    cr = "navy" if mode == "C" else "cream"
    o.append('  <g id="chair">' + S.limb((150, 482), (126, 780), 40, 40, cr) + poly([(120, 740), (440, 740), (440, 780), (120, 780)], PAL[cr][1])
             + poly([(120, 768), (440, 768), (440, 780), (120, 780)], PAL[cr][2]) + S.limb((150, 780), (150, 940), 18, 16, cr) + S.limb((410, 780), (410, 940), 18, 16, cr) + '</g>\n')
    # customer
    lo, to = c["leg_low"], c["leg_top"]
    o.append('  <g id="customer-legs">' + S.limb(lo[0], lo[1], 48, 44, "navy") + S.joint(lo[1], 44, "navy") + S.limb(lo[1], lo[2], 40, 32, "navy")
             + poly(c["shoe_low"], PAL["shoe"][1]) + '</g>\n')
    tor = S.torso(c["torso"], "cream", "slate") if mode == "C" else S.torso(c["torso"], "slate")
    o.append('  <g id="customer-body">' + tor + poly([(222, 474), (264, 470), (244, 508)], PAL["cream"][0])
              + S.limb(to[0], to[1], 48, 44, "navy")
              + '<g data-part="arms-crossed">' + S.limb(*c["upper_l"], 32, 28, "slate") + S.limb(*c["upper_r"], 32, 28, "slate")
              + S.limb(*c["fore_under"], 24, 22, "slate") + poly(c["hand_l"], PAL["skin"][1])
              + S.limb(*c["fore_top"], 28, 26, "slate") + poly(c["hand_r"], PAL["skin"][1]) + '</g>'
              + S.limb(*c["neck"], 28, 28, "skin") + '</g>\n')
    o.append(f'  <g id="customer-head" data-pivot="242,440" data-deg="3" data-freq="0.4" data-shape="sine">{S.head(c["head"], c["tilt"], "skeptic")}</g>\n')
    o.append(f'  <g id="customer-foot" data-pivot="466,732" data-deg="-9" data-freq="2.2" data-shape="snap">'
             f'{S.limb(to[1], to[2], 40, 30, "navy")}{poly(c["shoe_top"], PAL["shoe"][1])}</g>\n')
    # founder
    ln, lf = f["leg_near"], f["leg_far"]
    an, af = f["arm_near"], f["arm_far"]
    o.append('  <g id="founder"><g data-part="legs">' + S.limb(ln[0], ln[2], 52, 40, "navy") + S.limb(lf[0], lf[2], 52, 40, "navy")
             + S.shoe(f["shoe_near"]) + S.shoe(f["shoe_far"]) + '</g>'
             + '<g data-part="far-arm">' + S.limb(af[0], af[1], 34, 30, "orange") + S.joint(af[1], 30, "orange")
             + S.limb(af[1], af[2], 30, 26, "orange") + poly(f["hand_far"], PAL["skin"][1]) + '</g>'
             + '<g data-part="torso">' + S.torso(f["torso"], "orange", acc2_f) + poly(f["hood"], PAL["orange"][2])
             + poly([(704, 600), (838, 602), (836, 632), (704, 632)], PAL["orange"][2]) + '</g>'
             + S.limb(*f["neck"], 28, 28, "skin") + '</g>\n')
    o.append(f'  <g id="founder-head" data-pivot="752,330" data-deg="-4" data-freq="1.1" data-shape="snap">{S.head(f["head"], f["tilt"], "pitch")}</g>\n')
    tab = ('<g data-part="tablet" transform="rotate(-10 420 380)"><rect x="360" y="300" width="120" height="160" fill="#22314D"/>'
           '<rect x="370" y="310" width="100" height="140" fill="#FBF8F2"/><polygon points="360,300 400,300 360,340" fill="#141F35"/>'
           '<rect x="384" y="404" width="18" height="34" fill="#F2925E"/><rect x="410" y="384" width="18" height="54" fill="#C8402F"/>'
           '<rect x="436" y="350" width="18" height="88" fill="#E8692E"/></g>')
    o.append('  <g id="arm" data-pivot="690,370" data-deg="7" data-freq="1.1" data-shape="snap">'
             f'<g data-part="upper-arm">{S.limb(an[0], an[1], 34, 30, "orange")}{S.joint(an[1], 30, "orange")}</g>'
             f'<g data-part="forearm">{S.limb(an[1], an[2], 30, 26, "orange")}</g>{tab}'
             f'<g data-part="hand">{poly(f["hand_near"], PAL["skin"][1])}</g></g>\n')
    return "".join(o) + "</svg>\n"


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    return [(cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in pts]


def octo(c, r, sx=0.97):
    return [(c[0] + r * sx * math.cos(math.radians(22.5 + 45 * k)), c[1] + r * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]


def big_head(c, r, fold_x):
    """v9-size head: an octagon with its right side folded back (one dark plane)."""
    pts = octo(c, r)            # k=6,7,0,1 are the right-hand corners, top to bottom
    edge = r * math.sin(math.radians(67.5))   # the top and bottom edges are flat at +-edge
    back = [(fold_x, c[1] - edge), pts[6], pts[7], pts[0], pts[1], (fold_x, c[1] + edge)]
    return poly(pts, PAL["skin"][1]) + poly(back, PAL["skin"][2])


def scene_v9():
    """Origami A drawn on the founder-v9 bodies and poses (v9 coordinates, big heads)."""
    S = Style("A")
    nv, sl, og, sk = PAL["navy"], PAL["slate"], PAL["orange"], PAL["skin"]
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
         '     data-bg="#E4DED3" data-variants="1" data-border="0" data-step="2" data-jitter="0" data-shadow="0.35" data-zoom="0.95,35,-12">\n'
         '  <!-- origami A on the founder-v9 proportions: generated by tools/origami.py (scene_v9) -->\n'
         '  <g id="floor" data-static="1"><rect x="-40" y="746" width="1160" height="380" fill="#CFC7B9"/>'
         '<rect x="-40" y="797" width="1160" height="330" fill="#C2B9A9"/></g>\n']
    cr = PAL["cream"]
    o.append('  <g id="chair">' + poly(quad((140, 486), (118, 776), 44, 44), cr[1]) + poly(quad((149, 772), (149, 940), 18, 16), cr[1])
             + poly(quad((409, 772), (409, 940), 18, 16), cr[1]) + poly([(120, 740), (440, 740), (440, 780), (120, 780)], cr[1])
             + poly([(120, 768), (440, 768), (440, 780), (120, 780)], cr[2]) + '</g>\n')
    # customer: leaning back, arms crossed (torso rotated -10 about the hip, like v9)
    torso = rot([(232, 520), (300, 520), (360, 584), (360, 700), (322, 750), (208, 750), (170, 700), (170, 584)], -10, 265, 750)
    fold = rot([(312, 520), (360, 584), (360, 700), (322, 750), (300, 750)], -10, 265, 750)
    o.append('  <g id="customer">' + poly(quad((240, 722), (452, 722), 64, 62), nv[1]) + poly(quad((441, 712), (441, 905), 62, 58), nv[1])
             + poly(quad((200, 575), (196, 655), 50, 46), sl[2]) + poly(torso, sl[1]) + poly(fold, sl[2])
             + poly([(234, 512), (284, 506), (262, 548)], cr[0])
             + poly(quad((330, 560), (352, 648), 50, 46), sl[1]) + S.joint((352, 648), 46, "slate")
             + poly(quad((352, 650), (215, 628), 48, 44), sl[1]) + poly([(190, 616), (212, 604), (232, 620), (224, 642), (198, 640)], sk[1])
             + poly(quad((196, 660), (335, 622), 48, 44), sl[2]) + poly([(330, 604), (356, 606), (362, 628), (344, 638), (326, 628)], sk[1])
             + '</g>\n')
    o.append('  <g id="foot" data-pivot="425,925" data-deg="-14" data-freq="2.6" data-shape="snap">'
             + poly([(398, 918), (420, 892), (500, 892), (526, 914), (516, 932), (402, 932)], PAL["shoe"][1])
             + poly([(398, 930), (526, 930), (524, 940), (400, 940)], PAL["shoe"][2]) + '</g>\n')
    hc = (255, 405)
    o.append('  <g id="customer-head" data-pivot="265,540" data-deg="5" data-freq="0.4" data-shape="sine">'
             + poly([(126, 404), (150, 392), (162, 420), (148, 444)], sk[2]) + big_head(hc, 125, 300)
             + poly([(135, 380), (150, 300), (250, 268), (350, 290), (378, 370), (330, 326), (255, 330), (180, 338)], PAL["hair"][1])
             + poly([(190, 386), (242, 392), (242, 400), (190, 394)], PAL["hair"][1])
             + poly([(276, 370), (330, 354), (332, 362), (278, 378)], PAL["hair"][1])
             + poly([(203, 412), (227, 412), (215, 420)], "#141F35") + poly([(288, 412), (312, 412), (300, 420)], "#141F35")
             + poly([(262, 436), (250, 458), (274, 458)], sk[2])
             + poly([(226, 486), (296, 480), (296, 488), (226, 494)], "#8E3A26") + '</g>\n')
    # founder: v9 hoodie block rotated -10 about (740,770)
    body = rot([(640, 478), (840, 478), (880, 520), (872, 600), (860, 720), (820, 770), (660, 770), (620, 720), (608, 600), (600, 520)], -10, 740, 770)
    side = rot([(800, 478), (840, 478), (880, 520), (872, 600), (860, 720), (820, 770), (790, 770)], -10, 740, 770)
    hood = rot([(612, 488), (700, 456), (808, 476), (790, 520), (710, 540), (630, 522)], -10, 740, 770)
    strings = "".join(poly(rot(quad((x, 505), (x, 585), 10, 10), -10, 740, 770), cr[0]) for x in (695, 735))
    o.append('  <g id="founder">'
             + poly(rot(quad((694, 730), (694, 930), 68, 62), 6, 694, 730), nv[1]) + poly(rot(quad((784, 730), (784, 930), 68, 62), -3, 784, 730), nv[1])
             + "".join(poly([(x - 66, 940), (x - 48, 914), (x + 40, 912), (x + 66, 936), (x + 56, 954), (x - 60, 954)], cr[1])
                       + poly([(x - 66, 950), (x + 66, 950), (x + 64, 962), (x - 64, 962)], PAL["red"][1]) for x in (660, 800))
             + poly(body, og[1]) + poly(side, og[2]) + poly(hood, og[2]) + strings + '</g>\n')
    o.append('  <g id="arm2" data-pivot="812,515" data-deg="7" data-freq="1.1" data-phase="0.25" data-shape="sine">'
             + poly(quad((812, 515), (878, 612), 58, 54), og[2]) + S.joint((878, 612), 54, "orange")
             + poly(quad((878, 612), (930, 528), 52, 48), og[2])
             + poly(rot([(910, 474), (952, 474), (958, 526), (936, 540), (908, 524)], 14, 932, 520), sk[1])
             + poly([(890, 500), (908, 508), (902, 528)], sk[1]) + '</g>\n')
    tab = ('<g data-part="tablet" transform="rotate(-6 425 383)"><rect x="355" y="290" width="140" height="186" fill="#22314D"/>'
           '<rect x="367" y="302" width="116" height="162" fill="#FBF8F2"/><polygon points="355,290 400,290 355,335" fill="#141F35"/>'
           '<rect x="382" y="414" width="22" height="38" fill="#F2925E"/><rect x="413" y="388" width="22" height="64" fill="#C8402F"/>'
           '<rect x="444" y="346" width="22" height="106" fill="#E8692E"/></g>')
    o.append('  <g id="arm" data-pivot="598,560" data-deg="9" data-freq="1.1" data-shape="snap">'
             f'<g data-part="upper-arm">{poly(quad((598, 560), (505, 588), 60, 56), og[1])}{S.joint((505, 588), 56, "orange")}</g>'
             f'<g data-part="forearm">{poly(quad((505, 588), (495, 500), 54, 50), og[1])}</g>{tab}'
             f'<g data-part="hand">{poly([(474, 440), (510, 436), (516, 474), (496, 492), (474, 480)], sk[1])}'
             f'{poly([(466, 420), (484, 438), (472, 452)], sk[1])}</g></g>\n')
    fc = (665, 360)
    o.append('  <g id="founder-head" data-pivot="700,490" data-deg="-5" data-freq="1.1" data-shape="snap">'
             + poly([(772, 360), (800, 352), (808, 386), (784, 400)], sk[2]) + big_head(fc, 128, 715)
             + poly([(545, 340), (556, 268), (612, 228), (700, 220), (770, 240), (795, 330), (770, 298), (750, 332), (725, 288), (700, 326),
                     (675, 284), (650, 320), (620, 284), (600, 322), (575, 294)], PAL["hair"][1])
             + poly([(578, 326), (630, 316), (632, 326), (580, 336)], PAL["hair"][1]) + poly([(660, 318), (712, 322), (710, 332), (658, 328)], PAL["hair"][1])
             + poly([(594, 368), (605, 359), (616, 368), (605, 377)], "#141F35") + poly([(674, 368), (685, 359), (696, 368), (685, 377)], "#141F35")
             + poly([(642, 386), (630, 408), (654, 408)], sk[2])
             + poly([(602, 426), (702, 420), (660, 462)], "#8E3A26") + poly([(612, 427), (692, 422), (686, 432), (618, 436)], cr[0]) + '</g>\n')
    return "".join(o) + "</svg>\n"


for m in "ABC":
    open(os.path.join(HERE, f"scenes/origami-{m}.svg"), "w").write(scene(m))
    print(f"wrote scenes/origami-{m}.svg")
open(os.path.join(HERE, "scenes/origami-A-v9.svg"), "w").write(scene_v9())
print("wrote scenes/origami-A-v9.svg")
