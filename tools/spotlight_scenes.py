"""B-roll for "The spotlight effect" (2025-04-24 footage) -> scenes/spt-*.svg

usage: python3 tools/spotlight_scenes.py
Reuses the Leon / LinkedIn / investors / slop / repetition / report parts. Times in ORIGINAL footage time live in videos/spotlight.json.
o1 wrinkle   (alpha, over the footage) a red ring around the shirt wrinkle Cam points at ("Look right here")
t1 title     The spotlight / effect
b1 stage     Cam under a spotlight; a framed photo of him drops in
b2 flaw      a magnifying glass on his photo; a red ring on one tiny spot
b3 hung      Cam worried; little red rings pop in all around him
b4 crowd     a crowd watches a video and smiles; nobody looks at the flaw
b5 hair      Cam with one hair out of place, a crooked collar; red rings
t2 only      No one notices / Only you
b6 ship      a video card, a "Publish" button gets pressed, the next card slides in
"""
import os
from leon_scenes import root, title_root, tag, calm, shade, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, GOLD
from slop_scenes import button
from repetition_scenes import pill
from report_scenes import centered

BLUE = "#5E7A94"
LIGHT = "#FFF4C7"
SHIRT = "#C9737A"


def ring(gid, cx, cy, r, show, w=12):
    """A hand-drawn red ring: a slightly open loop that overshoots its start."""
    d = (f"M{cx + r * 0.95:.0f} {cy - r * 0.25:.0f} C{cx + r * 1.05:.0f} {cy + r * 0.8:.0f} {cx - r * 0.7:.0f} {cy + r * 1.1:.0f} "
         f"{cx - r:.0f} {cy + r * 0.1:.0f} C{cx - r * 1.1:.0f} {cy - r * 0.9:.0f} {cx + r * 0.6:.0f} {cy - r * 1.15:.0f} {cx + r * 1.05:.0f} {cy - r * 0.05:.0f}")
    return g(gid, f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="{w}" stroke-linecap="round"/>', show, rig(cx, cy + r, 3, 0.8))


def photo(x, y, w, h, k, flip=False):
    """A framed photo of Cam: navy frame, cream mat, his head inside. Returns (frame body, head)."""
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{NAVY}"/><rect x="{x + 18}" y="{y + 18}" width="{w - 36}" height="{h - 36}" fill="{CREAM}"/>'
    return body


def video_card(x, y, w=380, h=240, fill="#FFFDF6"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{NAVY}"/><rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 70}" rx="8" fill="{BLUE}"/>'
            f'<path d="M{x + w / 2 - 26:.0f} {y + 60} L{x + w / 2 + 34:.0f} {y + 99} L{x + w / 2 - 26:.0f} {y + 138} Z" fill="{CREAM}"/>'
            f'<rect x="{x + 24}" y="{y + h - 38}" width="{w - 48}" height="10" rx="5" fill="{CREAM}"/><rect x="{x + 24}" y="{y + h - 38}" width="{(w - 48) * 0.35:.0f}" height="10" rx="5" fill="{ORANGE}"/>')


# ---- overlay on the footage ----

def wrinkle():
    dur = 2.2
    s = title_root(dur)
    return s + ring("r", 470, 640, 85, (0.05, dur + 1), 14) + "</svg>\n"


# ---- b-roll ----

def stage():
    dur = 3.5
    s = root(dur, "1,0,0")
    s += g("beam", f'<path d="M470 0 H610 L860 900 H220 Z" fill="{LIGHT}" opacity="0.85"/>', (0.05, dur + 1))
    s += g("pool", f'<ellipse cx="540" cy="900" rx="330" ry="60" fill="{LIGHT}"/>', (0.05, dur + 1))
    s += head(CAM_P, [(0.05, "neutral"), (2.0, "surprised")], (540, 880), 0.6, False, "cam")
    s += g("ph", photo(760, 260, 220, 270, 0.3) + label(800, 470, "you", 44, NAVY), (1.4, dur + 1), rig(870, 530, 4, 0.9))
    return s + "</svg>\n"


def flaw():
    dur = 3.1
    s = root(dur, "1,0,0")
    s += g("frame", photo(260, 160, 560, 680, 0), (0.05, dur + 1), rig(540, 840, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral")], (540, 790), 0.95, False, "cam", deg=1)
    s += g("glass", f'<circle cx="610" cy="640" r="110" fill="none" stroke="{NAVY}" stroke-width="26"/>'
                    f'<rect x="685" y="715" width="40" height="190" rx="18" fill="{NAVY}" transform="rotate(-45 705 810)"/>', (0.6, dur + 1), rig(660, 790, 5, 0.9))
    s += ring("spot", 600, 630, 34, (1.4, dur + 1), 10)
    return s + "</svg>\n"


def hung():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "worried"), (1.6, "tired")], (540, 820), 0.75, False, "cam")
    for i, (x, y, r) in enumerate(((240, 260, 50), (830, 300, 42), (200, 620, 36), (880, 640, 48), (420, 160, 30), (680, 150, 38))):
        s += ring(f"r{i}", x, y, r, (0.3 + 0.3 * i, dur + 1), 9)
    return s + "</svg>\n"


def crowd():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("screen", video_card(330, 120, 420, 270), (0.05, dur + 1), rig(540, 390, 1, 0.5))
    people = ((1, 200, 700), (5, 400, 700), (9, 680, 700), (2, 880, 700), (6, 300, 950), (8, 540, 950), (3, 780, 950))
    for i, (p, x, y) in enumerate(people):
        t = 0.2 + 0.18 * i
        s += head(p, [(t, "neutral"), (t + 0.9, "happy")], (x, y), 0.36, x < 540, f"p{i}")
    return s + "</svg>\n"


def hair():
    dur = 3.7
    s = root(dur, "1,0,0")
    s += g("shirt", f'<path d="M370 900 L470 840 L540 900 L610 840 L710 900 L760 1080 H320 Z" fill="{SHIRT}"/>'
                    f'<path d="M470 840 L540 900 L500 940 Z" fill="{shade(SHIRT, 0.85)}"/><path d="M610 840 L540 900 L590 930 Z" fill="{shade(SHIRT, 0.85)}" transform="rotate(14 590 880)"/>',
           (0.05, dur + 1), rig(540, 1080, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (2.2, "worried")], (540, 800), 0.75, False, "cam")
    s += g("strand", f'<path d="M570 540 C600 480 560 450 610 400" stroke="#6B4A2E" stroke-width="9" fill="none" stroke-linecap="round"/>', (1.6, dur + 1), rig(570, 540, 8, 1.4))
    s += ring("rc", 620, 930, 60, (0.9, dur + 1), 10)
    s += ring("rh", 595, 460, 70, (2.0, dur + 1), 10)
    return s + "</svg>\n"


def ship():
    dur = 4.4
    s = root(dur, "1,0,0")
    s += g("v1", video_card(150, 200), (0.05, 2.4), rig(340, 440, 2, 0.7))
    s += button("pub", 600, 300, 330, "Publish", ORANGE, CREAM, (0.3, 1.0))
    s += g("pubdown", f'<rect x="600" y="310" width="330" height="110" rx="20" fill="{shade(ORANGE, 0.85)}"/>' + label(634, 384, "Publish", 60, CREAM), (1.0, 1.3))
    s += button("pub2", 600, 300, 330, "Publish", ORANGE, CREAM, (1.3, dur + 1))
    s += g("v1up", video_card(150, 120), (2.4, dur + 1), rig(340, 360, 2, 0.7))
    s += g("live", f'<rect x="170" y="390" width="120" height="50" rx="10" fill="{ORANGE}"/>' + label(186, 428, "Live", 36, CREAM), (1.3, dur + 1))
    s += g("v2", video_card(350, 560) + label(380, 860, "Next one", 44, NAVY), (3.1, dur + 1), rig(540, 800, 3, 0.8))
    return s + "</svg>\n"


# ---- titles ----

def t_effect():
    dur = 2.6
    s = title_root(dur)
    s += tag("the", "The spotlight", 60, 760, 92, -2, 0.1, dur + 1)[0]
    s += tag("eff", "effect", 60, 890, 106, 2, 0.6, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_only():
    dur = 2.4
    s = title_root(dur)
    s += tag("no", "No one notices", 60, 760, 86, -2, 0.05, dur + 1)[0]
    s += tag("you", "Only you", 60, 880, 100, 2, 1.75, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("o1", wrinkle), ("t1", t_effect), ("t2", t_only),
                 ("b1", stage), ("b2", flaw), ("b3", hung), ("b4", crowd), ("b5", hair), ("b6", ship)):
        open(os.path.join(HERE, f"scenes/spt-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/spt-{n}.svg")
