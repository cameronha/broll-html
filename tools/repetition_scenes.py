"""B-roll for "Repetition" (2026-08-06 footage) -> scenes/rpt-*.svg

usage: python3 tools/repetition_scenes.py
Reuses the Leon / LinkedIn / investors / stupid parts. Times in ORIGINAL footage time live in videos/repetition.json.
t1 great     Company / Career / Brand, as he names them
b1 ways      the same "Big idea" bubble, over and over, in different sizes and colors
b2 once      Cam posts, writes, says it out loud: post card, page, speech bubble
t2 modern    Not how the modern / world works
b3 seven     "Rule of 7": seven speech bubbles pop in, one by one
b4 feed      a crowded feed scrolls; one red card is "your post"
t3 talk      Talk about it / a lot
b5 crowd     more repetition, more people: heads pop in, row by row
"""
import os
import cast_scenes as CS
from leon_scenes import root, title_root, tag, calm, CREAM, NAVY, ORANGE, PAPER, HERE, CAM_P, shade
from linkedin_scenes import rig, g, sheet, GREY
from investors_scenes import head, label, GOLD
from stupid_scenes import bubble
from report_scenes import centered

BLUE = "#5E7A94"


def pill(gid, cx, cy, text, size, fill, ink, show, rot=0):
    from PIL import ImageFont
    from leon_scenes import FONT
    w = ImageFont.truetype(FONT, size).getlength(text) + size * 1.2; h = size * 1.7
    r = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return g(gid, f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h / 2:.0f}" fill="{fill}"{r}/>'
                  f'<path d="M{cx - w * 0.2:.0f} {cy + h / 2 - 4:.0f} L{cx - w * 0.2 + 34:.0f} {cy + h / 2 - 4:.0f} L{cx - w * 0.2 - 6:.0f} {cy + h / 2 + 34:.0f}Z" fill="{fill}"{r}/>'
                  f'<text x="{cx - (w - size * 1.2) / 2:.0f}" y="{cy + size * 0.36:.0f}" font-family="Libre Franklin" font-weight="800" font-size="{size}" fill="{ink}"{r}>{text}</text>',
             show, rig(cx, cy + h / 2, 4, 1.1))


# ---- b-roll ----

def ways():
    dur = 3.6
    s = root(dur, "1,0,0")
    spots = ((300, 300, 70, NAVY, CREAM, -4), (760, 260, 52, ORANGE, CREAM, 3), (540, 520, 96, CREAM, NAVY, 0), (220, 640, 44, GOLD, NAVY, 5),
             (820, 560, 60, BLUE, CREAM, -3), (380, 820, 54, ORANGE, CREAM, 2), (760, 800, 40, NAVY, CREAM, -5), (560, 180, 38, BLUE, CREAM, 4))
    for i, (x, y, sz, f, ink, rot) in enumerate(spots):
        s += pill(f"b{i}", x, y, "Big idea", sz, f, ink, (0.15 + 0.38 * i, dur + 1), rot)
    return s + "</svg>\n"


def once():
    dur = 3.4
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0, "happy"), (2.4, "excited")], (230, 600), 0.5, True, "cam")
    s += g("post", f'<rect x="440" y="200" width="250" height="250" rx="14" fill="#FFFDF6"/><rect x="465" y="225" width="50" height="50" rx="10" fill="#0A66C2"/>'
                   + label(474, 263, "in", 34, CREAM) + "".join(f'<rect x="465" y="{300 + 30 * i}" width="{190 - 40 * (i % 2)}" height="12" rx="6" fill="{GREY}"/>' for i in range(4)),
           (0.3, dur + 1), rig(565, 450, 3, 0.8))
    s += g("page", f'<rect x="740" y="260" width="220" height="290" rx="8" fill="{CREAM}"/>'
                   + "".join(f'<path d="M770 {310 + 34 * i} q30 -12 60 0 t60 0 t40 0" stroke="{NAVY}" stroke-width="6" fill="none" stroke-linecap="round"/>' for i in range(6)),
           (1.5, dur + 1), rig(850, 550, 3, 0.9))
    s += pill("say", 640, 640, "Big idea!", 56, ORANGE, CREAM, (2.4, dur + 1))
    return s + "</svg>\n"


def seven():
    dur = 3.5
    s = root(dur, "1,0,0")
    s += g("rule", f'<rect x="300" y="140" width="480" height="130" rx="18" fill="{NAVY}"/>' + centered(540, 232, "Rule of 7", 80, CREAM), (0.05, dur + 1), rig(540, 270, 2, 0.6))
    for i in range(7):
        x, y = 170 + (i % 4) * 245 + (120 if i >= 4 else 0), 450 + (i // 4) * 230
        s += pill(f"s{i}", x, y, str(i + 1), 64, ORANGE if i == 6 else CREAM, CREAM if i == 6 else NAVY, (0.5 + 0.38 * i, dur + 1))
    return s + "</svg>\n"


def card(x, y, mine=False):
    fill = ORANGE if mine else "#FFFDF6"; ink = CREAM if mine else GREY
    return (f'<rect x="{x}" y="{y}" width="380" height="190" rx="14" fill="{fill}"/><circle cx="{x + 46}" cy="{y + 46}" r="26" fill="{NAVY if not mine else CREAM}"/>'
            + "".join(f'<rect x="{x + 90}" y="{y + 32 + 30 * i}" width="{240 - 50 * (i % 2)}" height="12" rx="6" fill="{ink}"/>' for i in range(4))
            + (label(x + 26, y + 168, "your post", 32, CREAM) if mine else ""))


def feed():
    dur = 3.5
    s = root(dur, "1,0,0")
    n = 7
    for k in range(n):                                      # the feed scrolls up in steps; your post is one card among many
        dy = -70 * k
        body = "".join(card(90 + 470 * c, 120 + 230 * r + dy + (110 if c else 0), mine=(r == 2 and c == 1)) for r in range(6) for c in range(2))
        s += g(f"feed{k}", body, (dur * k / n, dur * (k + 1) / n if k < n - 1 else dur + 1))
    return s + "</svg>\n"


def crowd():
    dur = 3.3
    s = root(dur, "1,0,0")
    s += pill("msg", 540, 200, "Big idea", 64, ORANGE, CREAM, (0.05, dur + 1))
    people = ((1, 200, 520), (3, 420, 520), (5, 660, 520), (9, 880, 520), (2, 300, 800), (6, 540, 800), (8, 780, 800))
    for i, (p, x, y) in enumerate(people):
        t = 0.3 + 0.32 * i
        s += head(p, [(t, "neutral"), (t + 0.4, "happy")], (x, y), 0.36, x < 540, f"p{i}")
    return s + "</svg>\n"


# ---- titles ----

def t_great():
    dur = 3.1
    s = title_root(dur)
    for i, (w, t) in enumerate((("Company", 0.3), ("Career", 1.3), ("Brand", 2.5))):
        s += tag(f"g{i}", w, 60, 660 + 115 * i, 86, (-1) ** i * 2, t, dur + 1, ORANGE if i == 2 else None, PAPER)[0]
    return s + "</svg>\n"


def t_modern():
    dur = 2.5
    s = title_root(dur)
    s += tag("not", "Not how the modern", 60, 760, 80, -2, 0.1, dur + 1)[0]
    s += tag("works", "world works", 60, 880, 80, 2, 1.0, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_talk():
    dur = 3.0
    s = title_root(dur)
    s += tag("talk", "Talk about it", 60, 760, 96, -2, 0.4, dur + 1)[0]
    s += tag("lot", "a lot", 60, 890, 110, 3, 2.6, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_great), ("t2", t_modern), ("t3", t_talk),
                 ("b1", ways), ("b2", once), ("b3", seven), ("b4", feed), ("b5", crowd)):
        open(os.path.join(HERE, f"scenes/rpt-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/rpt-{n}.svg")
