"""Facilitation video, Rubens-lite look: five literal scenes -> scenes/fac-{room,needs,slides,feedback,good}.svg

usage: python3 tools/facilitation_scenes.py
Beats (source seconds in ~/Claude-files/facilitation-edit): room 20-28 "they don't know how to run a room",
needs 34-39 "wildly disparate interests", slides 46-58 "stands in front of a room and shows slides",
feedback 72-77 "the feedback from the two big players", good 77-91 "who is doing this well".
Rule: show the meaning, not the words (no puns on idioms). Reuses rubens_scene's people, pen and wash.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubens_scene as R
from rubens_scene import pen, fine, fill, denim, blob, limbfill, hand, circ, oval, group, rig, INK, FILL, ACCENT

HERE = R.HERE
WHITE = "#FFFFFF"


def mirror(d):
    """Mirror an absolute path about the body's center line (x 760)."""
    nums = iter(re.findall(r"-?\d+\.?\d*", d))
    out, toks = [], re.findall(r"[A-Za-z]|-?\d+\.?\d*", d)
    flip = True
    for t in toks:
        if t.isalpha():
            out.append(t)
            flip = True
        else:
            out.append(f"{1520 - float(t):g}" if flip else t)
            flip = not flip
    return " ".join(out)


def arms_in():
    """Both forearms come in to the lap, nubs together (holding a phone)."""
    near = ("M700 390 Q680 460 700 530 L735 545", "M688 368 Q662 440 676 528 Q690 556 730 562", "M712 404 Q700 460 712 512 L736 528")
    o = ""
    for d0, d1, d2 in (near, tuple(mirror(d) for d in near)):
        o += blob(d0, 40) + limbfill(d0) + pen(d1) + pen(d2)
    return o


def arm_up():
    """Far arm raised straight up (a question nobody takes)."""
    d = "M816 384 Q846 260 852 120"
    return blob(d, 40) + limbfill(d) + pen("M828 366 Q866 260 870 116") + pen("M806 402 Q830 260 834 116") + hand("fist", 852, 110, 0, 1.15)


def zzz(x, y, s=1.0):
    return "".join(pen(f"M{x + i * 22 * s:g} {y - i * 26 * s:g} l{14 * s:g} 0 l{-14 * s:g} {14 * s:g} l{14 * s:g} 0", 2.6) for i in range(3))


def closed_eyes(x=752, y=240, k=0.62):
    """Cover the face's open eyes with lids: skin discs and a downward arc each."""
    o = ""
    for ex in (-42, 43):
        cx, cy = x + ex * k, y + 5 * k
        o += f'<circle cx="{cx:g}" cy="{cy:g}" r="{17 * k / 0.62:g}" fill="{R.SKIN}"/>' + pen(f"M{cx - 13:g} {cy:g} Q{cx:g} {cy + 9:g} {cx + 13:g} {cy:g}", 3)
    return o


def seated(cx, fy, k, top="sweater", act="", **face_kw):
    """A person on a chair: torso to the front, legs to the side (knees toward the trainer on the left).
    act: "" | sleep | phone."""
    if act == "phone":
        face_kw.update(down=1, mouth=face_kw.get("mouth", "flat"))
    if act == "sleep":
        face_kw.update(mouth="small", look=0)
    with R.place(cx, fy, k, 0.8) as P:
        chair = (pen("M600 812 L860 812 M612 812 L604 962 M848 812 L856 962 M852 812 L860 560", 3.4)
                 + f'<path d="M596 802 L862 802 L862 816 L596 816 Z" fill="{WHITE}"/>' + pen("M596 802 L862 802 L862 816 L596 816 Z"))
        thigh = "M630 742 L800 742 L800 804 L630 804 Q600 804 600 774 Q600 742 630 742 Z"
        shin = "M604 780 L650 780 L648 936 L606 936 Z"
        legs = (fill(shin) + denim(shin) + pen("M604 790 L606 936 M650 790 L648 936")
                + pen("M606 962 Q560 962 560 950 Q562 934 606 934 L650 936 L652 962 Z")
                + fill(thigh) + denim(thigh) + pen(thigh))
        clip = f'<clipPath id="seat{R.CLIPS[0]}"><rect x="0" y="0" width="1080" height="606"/></clipPath>'
        arms = arms_in() if act == "phone" else R.arm_down("near") + (arm_up() if act == "hand" else R.arm_down("far"))
        upper = (clip + f'<g clip-path="url(#seat{R.CLIPS[0]})">{R.body(top)}</g>' + R.neck() + arms + R.face(752, 240, **face_kw))
        if act == "phone":
            upper += (f'<rect x="732" y="520" width="56" height="84" rx="8" fill="{INK}"/><rect x="738" y="528" width="44" height="64" rx="4" fill="#9FC3D0"/>'
                      + hand("fist", 730, 566, 180, 1.0) + hand("fist", 790, 566, 180, 1.0))
        if act == "sleep":
            upper += closed_eyes() + zzz(830, 140, 2.0)
        if act == "lost":
            upper += text(800, 120, "?", 110, ACCENT, "middle")
        return P.wrap(chair + f'<g transform="translate(0 150)">{upper}</g>' + legs), P.pt(752, 390)


def standing(cx, fy, k, top="sweater", arms="down", **face_kw):
    return R.person(cx, fy, k, top, arms, 0.9, **face_kw)


def screen(x, y, w, h, body=""):
    o = (pen(f"M{x + w / 2} {y + h} L{x + w / 2} 962 M{x + w / 2 - 60} 962 L{x + w / 2} {y + h + 40} L{x + w / 2 + 60} 962")
         + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}"/>' + fill(f"M{x} {y + h} L{x + w} {y + h} L{x + w} {y + h + 6} L{x} {y + h + 6} Z", 6, 6)
         + pen(f"M{x} {y} L{x + w} {y} L{x + w} {y + h} L{x} {y + h} Z", 3.4))
    return o + body


def bullets(x, y, n, w=180, gap=34):
    return "".join(f'<circle cx="{x}" cy="{y + i * gap}" r="5" fill="{INK}"/>' + fine(f"M{x + 16} {y + i * gap} L{x + 16 + w - (i % 3) * 30} {y + i * gap}", 2.4) for i in range(n))


def text(x, y, s, size=34, c=INK, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Helvetica, Arial" font-weight="bold" font-size="{size}" fill="{c}" text-anchor="{anchor}">{s}</text>'


def bubble(hx, hy, icon):
    """Thought bubble above-right of a head at (hx, hy), with an icon drawn around (0, 0)."""
    bx, by = hx + 30, hy - 120
    return (f'<circle cx="{hx + 10}" cy="{hy - 58}" r="6" fill="{WHITE}"/>' + pen(circ(hx + 10, hy - 58, 6), 2.2)
            + f'<circle cx="{hx + 20}" cy="{hy - 78}" r="9" fill="{WHITE}"/>' + pen(circ(hx + 20, hy - 78, 9), 2.2)
            + f'<circle cx="{bx}" cy="{by}" r="46" fill="{WHITE}"/>' + pen(circ(bx, by, 46), 2.6)
            + f'<g transform="translate({bx} {by})">{ICONS[icon]}</g>')


ICONS = {
    "code": pen("M-20 -16 L-34 0 L-20 16 M20 -16 L34 0 L20 16 M6 -20 L-6 20", 3.4),
    "money": text(0, 16, "$", 46, ACCENT, "middle"),
    "law": pen("M0 -26 L0 22 M-14 22 L14 22 M-28 -18 L28 -18 M-28 -18 L-36 2 L-20 2 Z M28 -18 L20 2 L36 2 Z", 2.6),
    "art": f'<path d="{oval(0, 0, 32, 24)}" fill="{FILL}"/>' + pen(oval(0, 0, 32, 24), 2.6) + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>' for x, y, c in [(-14, -8, ACCENT), (2, -12, INK), (16, -4, "#6E9FB3")]),
    "chart": pen("M-28 22 L-28 -24 M-28 22 L30 22", 2.6) + "".join(f'<rect x="{x}" y="{22 - h}" width="10" height="{h}" fill="{ACCENT}"/>' for x, h in [(-20, 14), (-4, 26), (12, 38)]),
}


def wrapup(s):
    return "".join(s) + "</svg>\n"


def room():
    """'They don't know how to run a room': the trainer talks to the slide; hands go up unanswered, people are lost."""
    s = R.root("fac-room")
    s.append(group("screen", screen(60, 250, 300, 200, text(80, 300, "AI TOOLS", 30) + bullets(86, 340, 3))))
    s.append(group("trainer", standing(400, 962, 0.62, "shirt", "gesture", hair="side", brows="neutral", mouth="o", look=-1), rig(400, 962, 1.5, 0.7)))
    back = [(640, "hand", dict(hair="long", brows="up", mouth="o")), (790, "lost", dict(hair="cap", brows="doubt", mouth="flat")),
            (940, "", dict(hair="bald", brows="doubt", mouth="flat", look=-1))]
    front = [(570, "lost", dict(hair="curly", brows="doubt", mouth="small")), (720, "", dict(hair="bun", brows="doubt", mouth="flat", look=1)),
             (880, "hand", dict(hair="side", brows="up", mouth="o")), (1020, "lost", dict(hair="cap", brows="doubt", mouth="flat", look=-1))]
    for row, (fy, k, people) in enumerate([(840, 0.5, back), (962, 0.58, front)]):
        for i, (x, act, kw) in enumerate(people):
            body, _ = seated(x, fy, k, ["sweater", "shirt", "jacket"][(i + row) % 3], act, **kw)
            s.append(group(f"p{row}{i}", body, rig(x, fy, 4 if act == "hand" else 2, 0.6 + 0.2 * i, "sine", 0.3 * i)))
    return wrapup(s)


def needs():
    """'Wildly disparate interests and needs': five attendees, five different thoughts; one slide for all."""
    s = R.root("fac-needs")
    s.append(group("screen", screen(40, 300, 240, 170, text(160, 400, "AI 101", 40, INK, "middle"))))
    s.append(group("trainer", standing(330, 962, 0.6, "shirt", "gesture", hair="side", brows="neutral", mouth="smile", look=-1), rig(330, 962, 1.5, 0.6)))
    icons = ["code", "money", "law", "art", "chart"]
    hairs = ["cap", "long", "bald", "curly", "bun"]
    for i, (icon, hair) in enumerate(zip(icons, hairs)):
        x = 478 + i * 126
        body, (hx, hy) = seated(x, 962, 0.6, ["sweater", "shirt", "jacket"][i % 3], hair=hair, brows=["neutral", "calm", "doubt", "up", "neutral"][i], mouth=["flat", "small", "flat", "smile", "flat"][i], look=-1)
        s.append(group(f"p{i}", body, rig(x, 962, 1.5, 0.6 + 0.1 * i, "sine", 0.2 * i)))
        s.append(group(f"b{i}", bubble(hx, hy, icon), rig(hx, hy - 60, 4, 0.5 + 0.15 * i, "sine", 0.25 * i)))
    return wrapup(s)


def slides():
    """'Stands in front of a room and shows slides': slide 1 of 87, and the room is asleep."""
    s = R.root("fac-slides")
    s.append(group("screen", screen(50, 170, 400, 270, text(80, 225, "AGENDA", 36) + bullets(90, 265, 4, 260) + text(430, 425, "1 / 87", 26, ACCENT, "end"))))
    s.append(group("trainer", standing(470, 962, 0.64, "jacket", "gesture", hair="cap", brows="neutral", mouth="flat", look=-1), rig(520, 962, 1, 0.4)))
    people = [(770, 850, 0.45), (900, 850, 0.45), (1030, 850, 0.45), (700, 962, 0.52), (840, 962, 0.52), (980, 962, 0.52)]
    for i, (x, fy, k) in enumerate(people):
        body, _ = seated(x, fy, k, ["sweater", "shirt", "jacket"][i % 3], "sleep", hair=["long", "bald", "side", "curly", "cap", "bun"][i])
        s.append(group(f"p{i}", body, rig(x, fy, 3, 0.3 + 0.05 * i, "sine", 0.17 * i)))
    return wrapup(s)


def card(x, y, deg, w=140):
    stars = "".join((f'<path d="{star(x + 18 + j * (w - 30) / 4, y + 30, 9)}" fill="{ACCENT}"/>' if j == 0 else "") + pen(star(x + 18 + j * (w - 30) / 4, y + 30, 9), 1.8) for j in range(5))
    return (f'<g transform="rotate({deg} {x + w / 2} {y + 50})"><rect x="{x}" y="{y}" width="{w}" height="100" fill="{WHITE}"/>' + pen(f"M{x} {y} L{x + w} {y} L{x + w} {y + 100} L{x} {y + 100} Z", 2.6)
            + stars + fine(f"M{x + 14} {y + 62} L{x + w - 18} {y + 62} M{x + 14} {y + 80} L{x + w - 46} {y + 80}", 2) + "</g>")


def star(cx, cy, r):
    import math
    pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.sin(i * math.pi / 5), cy - (r if i % 2 == 0 else r * 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def feedback():
    """'The feedback from the two big players, how bad it is': great at building, bad at teaching.
    Two confident figures on a bright launch stage; the wall of one-star training feedback beside them."""
    s = R.root("fac-feedback")
    board = pen("M30 200 L430 200 L430 700 L30 700 Z", 3) + "".join(
        card(46 + (i % 3) * 128, 222 + (i // 3) * 160, [-4, 3, -2, 5, -5, 2, 3, -3, 4][i], 112) for i in range(9))
    s.append(group("board", f'<rect x="30" y="200" width="400" height="500" fill="#E9D6B4"/>' + board))
    light = "".join(f'<path d="M{x - 30} 40 L{x + 30} 40 L{x + 150} 900 L{x - 150} 900 Z" fill="#FFF3C4" opacity="0.75"/>' for x in (680, 900))
    stage = (f'<path d="M500 900 L1060 900 L1060 962 L500 962 Z" fill="{WHITE}"/>' + fill("M500 900 L1060 900 L1060 912 L500 912 Z", 0, 0)
             + pen("M500 900 L1060 900 L1060 962 M500 900 L500 962"))
    sparks = "".join(pen(f"M{x} {y - 16} L{x} {y + 16} M{x - 16} {y} L{x + 16} {y}", 3) for x, y in [(560, 300), (1010, 240), (590, 560), (1030, 520)])
    s.append(group("stage", light + stage + sparks, ' data-static="1"'))
    s.append(group("big1", standing(680, 900, 0.8, "jacket", "gesture", hair="side", brows="up", mouth="grin", look=-1), rig(680, 900, 1.5, 0.6)))
    s.append(group("big2", standing(900, 900, 0.8, "shirt", "down", hair="cap", glasses=True, brows="calm", mouth="smile", look=-1), rig(900, 900, 1, 0.45, "sine", 0.4)))
    return wrapup(s)


def good():
    """'Who is doing this well': a facilitator and a group around a wall of notes; everyone takes part."""
    s = R.root("fac-good")
    notes = ""
    for i in range(14):
        x, y = 90 + (i % 7) * 132 + (i // 7) * 30, 150 + (i // 7) * 120 + (i % 3) * 14
        c = [FILL, "#F6E27A", ACCENT, "#9FC3D0"][i % 4]
        notes += f'<g transform="rotate({[-6, 4, -2, 5, -4, 3, -5][i % 7]} {x + 40} {y + 40})"><rect x="{x}" y="{y}" width="84" height="84" fill="{c}"/>' + fine(f"M{x + 12} {y + 30} L{x + 70} {y + 30} M{x + 12} {y + 50} L{x + 56} {y + 50}", 2) + pen(f"M{x} {y} L{x + 84} {y} L{x + 84} {y + 84} L{x} {y + 84} Z", 2) + "</g>"
    s.append(group("notes", notes))
    people = [(170, 0.7, "sweater", "gesture", dict(hair="curly", mouth="grin", brows="up", look=-1)),
              (330, 0.7, "shirt", "down", dict(hair="long", mouth="smile", look=1)),
              (540, 0.8, "jacket", "gesture", dict(hair="side", mouth="smile", brows="calm", look=-1)),
              (760, 0.7, "sweater", "down", dict(hair="bun", mouth="o", brows="up", look=-1)),
              (920, 0.7, "shirt", "gesture", dict(hair="bald", mouth="grin", look=-1))]
    for i, (x, k, top, arms, kw) in enumerate(people):
        s.append(group(f"p{i}", standing(x, 962, k, top, arms, **kw), rig(x, 962, 2, 0.8 + 0.15 * i, "sine", 0.2 * i)))
    for x in (250, 840):
        s.append(group(f"table{x}", table(x)))
    return wrapup(s)


def table(x):
    """A standing table with an open laptop; the screen shows a chat with the AI."""
    top = f"M{x - 110} 720 L{x + 110} 720 L{x + 110} 736 L{x - 110} 736 Z"
    scr = f"M{x - 62} 620 L{x + 62} 620 L{x + 62} 712 L{x - 62} 712 Z"
    chat = (f'<rect x="{x - 50}" y="632" width="62" height="20" rx="8" fill="#9FC3D0"/><rect x="{x - 14}" y="660" width="66" height="20" rx="8" fill="{FILL}"/>'
            f'<rect x="{x - 50}" y="688" width="48" height="14" rx="6" fill="#9FC3D0"/>')
    return (pen(f"M{x} 736 L{x} 962 M{x - 50} 962 L{x + 50} 962", 3.4) + f'<path d="{top}" fill="{WHITE}"/>' + fill(top, 5, 4) + pen(top)
            + f'<path d="{scr}" fill="{WHITE}"/>' + chat + pen(scr, 3) + pen(f"M{x - 76} 712 L{x + 76} 712 L{x + 70} 720 L{x - 70} 720 Z", 2.6))


if __name__ == "__main__":
    for name, f in [("room", room), ("needs", needs), ("slides", slides), ("feedback", feedback), ("good", good)]:
        open(os.path.join(HERE, f"scenes/fac-{name}.svg"), "w").write(f())
        print(f"wrote scenes/fac-{name}.svg")
