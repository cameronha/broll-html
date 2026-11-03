"""Shared parts for the 2026-11-02 batch (front page, sell, trust, pinky).
Titles sit left and a little high (y 560/675): the real cat is center or lower right in these takes."""
from leon_scenes import title_root, tag, robot, CREAM, NAVY, ORANGE, PAPER
from linkedin_scenes import rig, g, GREY
from investors_scenes import label, GOLD
from report_scenes import centered

BLUE = "#8CBDDC"
WHITE = "#FFFDF6"


def two(a, b, dur, t2=1.0, size2=70, y=560):
    s = title_root(dur)
    s += tag("ta", a, 60, y, 80, -2, 0.05, dur + 1)[0]
    if b:
        s += tag("tb", b, 60, y + 115, size2, 2, t2, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def cat(x, y, k=1.0, look=0):
    """Pinky: a white Persian with ginger patches, flat face. (x, y) = bottom center."""
    def P(px, py):
        return f"{x + px * k:.0f} {y + py * k:.0f}"
    e = 10 * k
    return (f'<ellipse cx="{x:.0f}" cy="{y - 90 * k:.0f}" rx="{150 * k:.0f}" ry="{95 * k:.0f}" fill="{WHITE}"/>'           # body
            f'<ellipse cx="{x + 70 * k:.0f}" cy="{y - 120 * k:.0f}" rx="{70 * k:.0f}" ry="{45 * k:.0f}" fill="#E0A060"/>'    # ginger patch
            f'<path d="M{P(-150, -150)} L{P(-125, -250)} L{P(-80, -185)}Z" fill="#E0A060"/>'                               # ears
            f'<path d="M{P(-20, -185)} L{P(10, -255)} L{P(30, -165)}Z" fill="#E0A060"/>'
            f'<circle cx="{x - 65 * k:.0f}" cy="{y - 150 * k:.0f}" r="{88 * k:.0f}" fill="{WHITE}"/>'                       # head
            f'<path d="M{P(-150, -170)} Q{P(-110, -245)} {P(-40, -230)} Q{P(-60, -190)} {P(-100, -175)}Z" fill="#E0A060"/>'  # ginger cap
            f'<circle cx="{x + (-95 + look) * k:.0f}" cy="{y - 150 * k:.0f}" r="{e:.0f}" fill="{NAVY}"/>'
            f'<circle cx="{x + (-40 + look) * k:.0f}" cy="{y - 150 * k:.0f}" r="{e:.0f}" fill="{NAVY}"/>'
            f'<path d="M{P(-75, -125)} L{P(-60, -125)} L{P(-67, -115)}Z" fill="#D88C8C"/>'                                 # nose
            f'<path d="M{P(-85, -105)} Q{P(-67, -95)} {P(-50, -105)}" stroke="{NAVY}" stroke-width="{4 * k:.0f}" fill="none"/>')


def clock(x, y, r, hand_deg):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" stroke="{NAVY}" stroke-width="{r * 0.12:.0f}"/>'
            f'<rect x="{x - 6}" y="{y - r * 0.75:.0f}" width="12" height="{r * 0.75:.0f}" rx="6" fill="{NAVY}" transform="rotate({hand_deg} {x} {y})"/>'
            f'<rect x="{x - 6}" y="{y - r * 0.5:.0f}" width="12" height="{r * 0.5:.0f}" rx="6" fill="{ORANGE}" transform="rotate({hand_deg * 12 % 360 + 90} {x} {y})"/>'
            f'<circle cx="{x}" cy="{y}" r="12" fill="{NAVY}"/>')


def spin_clock(gid, x, y, r, t0, t1, dur, n=8, deg0=0, step=45):
    out = ""
    for i in range(n):
        a = t0 + (t1 - t0) * i / n
        b = t0 + (t1 - t0) * (i + 1) / n if i < n - 1 else dur + 1
        out += g(f"{gid}{i}", clock(x, y, r, deg0 + step * i), (a, b), rig(x, y + r, 2, 0.8))
    return out


def meter(gid, x, y, h, levels, times, dur, color=ORANGE, label_text=None):
    """A vertical gauge that steps to each level (0..1) at each time."""
    out = g(f"{gid}f", f'<rect x="{x}" y="{y}" width="90" height="{h}" rx="45" fill="{WHITE}" stroke="{NAVY}" stroke-width="10"/>', (0.05, dur + 1))
    for i, (lv, t) in enumerate(zip(levels, times)):
        t1 = times[i + 1] if i + 1 < len(times) else dur + 1
        fh = max(20, (h - 20) * lv)
        out += g(f"{gid}{i}", f'<rect x="{x + 10}" y="{y + h - 10 - fh:.0f}" width="70" height="{fh:.0f}" rx="35" fill="{color}"/>', (t, t1))
    if label_text:
        out += g(f"{gid}l", centered(x + 45, y + h + 60, label_text, 44, NAVY), (0.05, dur + 1))
    return out


def doc(x, y, w, h, title=None, n=6, fill=WHITE, k0=0):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>'
    yy = y + 40
    if title:
        s += label(x + 30, y + 70, title, 44, NAVY); yy = y + 110
    s += "".join(f'<rect x="{x + 30}" y="{yy + 40 * i}" width="{w - 60 - 60 * ((i + k0) % 3)}" height="14" rx="7" fill="{GREY}"/>'
                 for i in range(n) if yy + 40 * i < y + h - 30)
    return s


def envelope(x, y, w=200, fill=CREAM):
    h = w * 0.62
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="10" fill="{fill}" stroke="{NAVY}" stroke-width="8"/>'
            f'<path d="M{x + 6} {y + 8} L{x + w / 2:.0f} {y + h * 0.58:.0f} L{x + w - 6} {y + 8}" stroke="{NAVY}" stroke-width="8" fill="none"/>')


def video_card(x, y, w=170, fill=NAVY):
    h = w * 0.62
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="12" fill="{fill}"/>'
            f'<path d="M{x + w * 0.42:.0f} {y + h * 0.28:.0f} L{x + w * 0.64:.0f} {y + h * 0.5:.0f} L{x + w * 0.42:.0f} {y + h * 0.72:.0f}Z" fill="{CREAM}"/>')


def tripod_phone(x, y, rec=True):
    """A phone on a tripod; (x, y) = the phone center."""
    return (f'<path d="M{x} {y + 110} L{x - 110} {y + 420} M{x} {y + 110} L{x + 110} {y + 420} M{x} {y + 110} L{x} {y + 420}" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/>'
            f'<rect x="{x - 70}" y="{y - 120}" width="140" height="240" rx="22" fill="{NAVY}"/><rect x="{x - 56}" y="{y - 100}" width="112" height="200" rx="10" fill="{BLUE}"/>'
            + (f'<circle cx="{x + 30}" cy="{y - 70}" r="14" fill="{ORANGE}"/>' if rec else ""))


def dumbbell(x, y, k=1.0):
    return (f'<rect x="{x - 90 * k:.0f}" y="{y - 10 * k:.0f}" width="{180 * k:.0f}" height="{20 * k:.0f}" rx="{8 * k:.0f}" fill="{GREY}"/>'
            f'<rect x="{x - 110 * k:.0f}" y="{y - 50 * k:.0f}" width="{40 * k:.0f}" height="{100 * k:.0f}" rx="{10 * k:.0f}" fill="{NAVY}"/>'
            f'<rect x="{x + 70 * k:.0f}" y="{y - 50 * k:.0f}" width="{40 * k:.0f}" height="{100 * k:.0f}" rx="{10 * k:.0f}" fill="{NAVY}"/>')


def gym(x, y, w=520, h=360):
    """A gym building, (x, y) = bottom-left."""
    return (f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{NAVY}"/>'
            f'<rect x="{x + w * 0.2:.0f}" y="{y - h - 90}" width="{w * 0.6:.0f}" height="110" rx="14" fill="{ORANGE}"/>'
            + centered(x + w / 2, y - h - 10, "GYM", 76, CREAM)
            + "".join(f'<rect x="{x + 40 + 120 * i}" y="{y - h + 50}" width="80" height="90" rx="6" fill="{BLUE}"/>' for i in range(int((w - 40) / 120)))
            + f'<rect x="{x + w / 2 - 60:.0f}" y="{y - 160}" width="120" height="160" rx="8" fill="{BLUE}"/>')


def counter(x, y, value, w=360, word="views"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="130" rx="20" fill="{NAVY}"/>'
            + label(x + 36, y + 92, str(value), 80, CREAM) + label(x + 36 + 52 * len(str(value)) + 20, y + 88, word, 52, GOLD))


def heart(x, y, s=1.0, fill=ORANGE):
    return (f'<path d="M{x} {y + 40 * s:.0f} C{x - 90 * s:.0f} {y - 20 * s:.0f} {x - 50 * s:.0f} {y - 90 * s:.0f} {x} {y - 45 * s:.0f} '
            f'C{x + 50 * s:.0f} {y - 90 * s:.0f} {x + 90 * s:.0f} {y - 20 * s:.0f} {x} {y + 40 * s:.0f}Z" fill="{fill}"/>')


def building(x, y, w, h, fill=NAVY, win=BLUE, cols=3):
    s = f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{fill}"/>'
    ww = (w - 20 * (cols + 1)) / cols
    for r in range(int((h - 40) / 70)):
        for c in range(cols):
            s += f'<rect x="{x + 20 + c * (ww + 20):.0f}" y="{y - h + 30 + 70 * r}" width="{ww:.0f}" height="40" rx="4" fill="{win}"/>'
    return s
