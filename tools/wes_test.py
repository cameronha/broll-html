"""Style test: the podcast "rapport" beat (pod-b4) in a Wes Anderson direction -> scenes/wes-{card,set}.svg

usage: python3 tools/wes_test.py
Changes against v9: one center line (mirror-image staging), a stage border with curtains, pastel set (brand navy
stays the ink, brand red the accent), Futura caps with wide spacing, a chapter card, less boil (calm 0.4).
The whip pan between the two shots is an ffmpeg xfade (slideleft), not part of the rig.
"""
import os
from leon_scenes import calm, NAVY, CREAM, ORANGE, HERE
from linkedin_scenes import rig, g, dashes
from investors_scenes import head
from podcast_scenes import mic, HOST, GUEST
import cast_scenes as CS

PINK, MINT, MUSTARD = "#E8B4AE", "#A9CDB8", "#D9A94A"


def futura(x, y, text, size, color, spacing=8, weight="bold"):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Futura" font-weight="{weight}" font-size="{size}" '
            f'letter-spacing="{spacing}" fill="{color}">{text}</text>')


def stage_root(dur, bg, floor=None):
    CS.DUR = dur
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080"\n'
         f'     data-bg="{bg}" data-finish="cut" data-variants="3" data-border="0" data-bg-boil="0.5" data-zoom="1,0,0" data-dur="{dur}">\n')
    if floor:
        s += (f'  <g id="floor" data-static="1">\n    <rect x="-40" y="640" width="1160" height="40" fill="{MINT}"/>\n'
              f'    <rect x="-40" y="680" width="1160" height="440" fill="{floor}"/>\n  </g>\n')
    return s


def border():
    """A cream frame with a navy inner line: the scene reads as a small stage."""
    return ('  <g id="frame" data-static="1">\n'
            f'    <path d="M0 0H1080V1080H0Z M60 60V1020H1020V60Z" fill="{CREAM}" fill-rule="evenodd"/>\n'
            f'    <rect x="74" y="74" width="932" height="932" fill="none" stroke="{NAVY}" stroke-width="6"/>\n  </g>\n')


def curtains():
    out = ""
    for side, x in (("l", 60), ("r", 1020)):
        sx = 1 if side == "l" else -1
        d = (f"M{x} 60 H{x + sx * 150} C{x + sx * 120} 260 {x + sx * 60} 380 {x + sx * 70} 1020 H{x} Z")
        out += g(f"cur{side}", f'<path d="{d}" fill="{ORANGE}"/>', None)
    out += g("valance", f'<rect x="60" y="60" width="960" height="70" fill="{ORANGE}"/>'
                        + "".join(f'<circle cx="{100 + 80 * i}" cy="130" r="40" fill="{ORANGE}"/>' for i in range(12)), None)
    return out


def card():
    dur = 1.3
    s = stage_root(dur, MUSTARD)
    s += g("ch", futura(540, 470, "CHAPTER TWO", 44, NAVY, 14, "500"), (0.05, dur + 1))
    s += g("rule", f'<rect x="390" y="510" width="300" height="6" fill="{NAVY}"/>', (0.05, dur + 1))
    s += g("name", futura(540, 610, "THE INTERVIEW", 78, CREAM, 10), (0.05, dur + 1), rig(540, 610, 1, 0.5))
    return s + border() + "</svg>\n"


def stage():
    dur = 3.2
    s = stage_root(dur, PINK, MUSTARD)
    s += g("sign", f'<rect x="370" y="200" width="340" height="96" fill="{NAVY}"/>' + futura(540, 264, "ON AIR", 52, CREAM, 14),
           (0.05, dur + 1), rig(540, 200, 1, 0.5))
    s += g("light", f'<circle cx="540" cy="330" r="16" fill="{ORANGE}"/>', (0.6, dur + 1))
    s += head(HOST, [(0.05, "happy")], (300, 640), 0.55, True, "host", deg=1.5)
    s += head(GUEST, [(0.05, "happy"), (1.9, "excited")], (780, 640), 0.55, False, "guest", deg=1.5)
    s += g("table", f'<rect x="200" y="690" width="680" height="34" fill="{CREAM}"/><rect x="200" y="724" width="680" height="10" fill="{NAVY}"/>'
                    f'<rect x="250" y="734" width="24" height="200" fill="{NAVY}"/><rect x="806" y="734" width="24" height="200" fill="{NAVY}"/>', (0.05, dur + 1))
    s += mic("m1", 420, 694, (0.05, dur + 1), 0.62)
    s += mic("m2", 660, 694, (0.05, dur + 1), 0.62)
    s += dashes("line", (400, 455), (680, 455), (1.0, dur + 1), NAVY, 10)
    s += curtains()
    return s + border() + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("card", card), ("set", stage)):
        open(os.path.join(HERE, f"scenes/wes-{n}.svg"), "w").write(calm(f(), 0.4))
        print(f"wrote scenes/wes-{n}.svg")
