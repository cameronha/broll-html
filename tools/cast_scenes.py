"""v9 scenes with heads from the cast library (image-model heads, SVG bodies), with timed expression swaps
-> scenes/cast-{pitch,interview,closeup}.svg

usage: python3 tools/cast_scenes.py LIB_DIR [pitch interview closeup]
LIB_DIR/p{N}/{expression}.png + anchors.json come from tools/head_library.py. Library heads face left and are
drawn at the v9 founder's head size (k=1). A head = one top-level group per expression, all on the body's pivot
with the body's rig values, each shown only in its time window (data-show), so the face swaps while the head
keeps nodding with the body.
"""
import base64, io, json, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assets", "heads")
DUR = 6.0


def head(person, timeline, neck, k, flip, rig, gid):
    """timeline = [(t0, expression), ...]. Returns one group per entry."""
    anchors = json.load(open(os.path.join(LIB, f"p{person}", "anchors.json")))
    out = []
    for i, (t0, e) in enumerate(timeline):
        t1 = timeline[i + 1][0] if i + 1 < len(timeline) else DUR + 1
        im = Image.open(os.path.join(LIB, f"p{person}", f"{e}.png"))
        ax, ay = anchors[e]
        if flip:                                       # mirror the pixels, not the coordinates: the cut filter's
            im, ax = im.transpose(Image.FLIP_LEFT_RIGHT), im.width - ax   # region is in the piece's own user space
        buf = io.BytesIO(); im.save(buf, "PNG"); b64 = base64.b64encode(buf.getvalue()).decode()
        out.append(f'  <g id="{gid}-{i}"{rig} data-show="{t0},{t1}"><image href="data:image/png;base64,{b64}" '
                   f'x="{neck[0] - ax * k:.1f}" y="{neck[1] - ay * k:.1f}" width="{im.width * k:.1f}" height="{im.height * k:.1f}"/></g>\n')
    return "".join(out)


def rig_of(svg, gid):
    m = re.search(rf'<g id="{gid}"([^>]*)>', svg)
    return " " + " ".join(re.findall(r'data-(?:pivot|deg|freq|phase|shape)="[^"]*"', m.group(1)))


def swap_group(svg, gid, new):
    return re.sub(rf'  <g id="{gid}"[^>]*>.*?\n  </g>\n', lambda m: new, svg, count=1, flags=re.S)


def set_dur(svg, extra=""):
    return svg.replace("<svg ", f'<svg data-dur="{DUR}" {extra}', 1)


def pitch():
    """Founder (p4) pitches the bald skeptic (p8). The skeptic goes from doubt to surprise."""
    svg = open(os.path.join(HERE, "scenes/founder-v9.svg")).read()
    svg = swap_group(svg, "founder-head", head(4, [(0, "excited"), (3.2, "happy")], (645, 492), 1.0, False, rig_of(svg, "founder-head"), "founder-head"))
    svg = swap_group(svg, "customer-head", head(8, [(0, "skeptical"), (3.0, "surprised")], (316, 520), 0.84, True, rig_of(svg, "customer-head"), "customer-head"))
    return set_dur(svg)


def interview():
    """The careful founder (p7, glasses) interviews three customers (p2, p1, p3); each reacts at a different time."""
    svg = open(os.path.join(HERE, "scenes/talk-three.svg")).read()
    svg = swap_group(svg, "head2", head(7, [(0, "neutral"), (2.2, "happy")], (276, 546), 0.62, True, rig_of(svg, "head2"), "head2"))
    plan = {0: (2, [(0, "neutral"), (1.6, "skeptical")]), 1: (1, [(0, "happy"), (3.0, "excited")]),
            2: (3, [(0, "neutral"), (2.4, "confused")])}
    for i, (person, tl) in plan.items():
        m = re.search(rf'  <g id="cust{i}"[^>]*>\n    (.*?)\n  </g>\n', svg, flags=re.S)
        parts = re.findall(r"<[^>]+/>", m.group(1))
        body = "".join(parts[:10])                     # fig(): pants, shoes, arms, hands, torso, neck; the head follows
        X = float(re.search(r'data-pivot="([\d.]+),', m.group(0)).group(1))
        rig = rig_of(svg, f"cust{i}")
        new = (f'  <g id="cust{i}"{rig}>\n    {body}\n  </g>\n'
               + head(person, tl, (X - 2, 848 - 275 * 0.82 + 8), 0.47, False, rig, f"cust{i}-head"))
        svg = svg.replace(m.group(0), new)
    return set_dur(svg)


def closeup():
    """One person (p5) close: neutral, then worried, then surprised. Shows the face detail the wide shots hide."""
    svg = open(os.path.join(HERE, "scenes/founder-v9.svg")).read()
    for gid in ("chair", "customer", "foot", "customer-head", "arm"):
        svg = swap_group(svg, gid, "")
    rig = rig_of(svg, "founder-head")
    svg = swap_group(svg, "founder-head", head(5, [(0, "neutral"), (2.0, "worried"), (4.0, "surprised")], (645, 492), 1.0, False, rig, "founder-head"))
    svg = re.sub(r'data-zoom="[^"]*"', 'data-zoom="1.25,-300,-70"', svg)
    return set_dur(svg)


if __name__ == "__main__":
    want = sys.argv[2:] or ["pitch", "interview", "closeup"]
    for name, f in (("pitch", pitch), ("interview", interview), ("closeup", closeup)):
        if name not in want:
            continue
        open(os.path.join(HERE, f"scenes/cast-{name}.svg"), "w").write(f())
        print("wrote scenes/cast-%s.svg" % name)
