"""B-roll for "Field report announcement: León" (2026-10-09 footage) -> scenes/rep-*.svg

usage: python3 tools/report_scenes.py
Reuses the Leon / LinkedIn / investors parts; the Austin -> León map is the Leon video's beat0-rev25.mp4 (as a file, in videos/report.json).
t1 announce  Announcing / a cool project
b1 reports   a stack of field reports drops in, "AI Field Report" on top
b2 regions   a globe: CARICOM, Guatemala, Mexico light up, it spins, Southeast Asia lights up (replaces t2)
t3 weeks     2 weeks / in León
b3 people    Entrepreneurs, Investors, Technologists, Business people: heads pop in as he lists them
t4 asks      Who they hire? / Does it grow?
b4 interview Cam and a founder across a table, a phone on the table records
b5 report    transcripts fly into the León report
t5 dm        Know anyone in León? / DM me
"""
import math, os
from PIL import ImageFont
import cast_scenes as CS
from leon_scenes import root, title_root, tag, check, calm, CREAM, NAVY, ORANGE, PAPER, HERE, WOOD, FONT, CAM_P, shade
from linkedin_scenes import rig, g, sheet, GREY
from investors_scenes import head, label, GOLD


def centered(x, y, text, size, color=NAVY):
    return label(round(x - ImageFont.truetype(FONT, size).getlength(text) / 2), y, text, size, color)


def report(gid, x, y, title, band, show, r=""):
    """A report booklet, top-left (x, y), 260 x 340: a colored band, a title, a small bar chart."""
    return g(gid, f'<rect x="{x + 10}" y="{y + 12}" width="260" height="340" rx="10" fill="{shade(CREAM, 0.75)}"/>'
                  f'<rect x="{x}" y="{y}" width="260" height="340" rx="10" fill="#FFFDF6"/>'
                  f'<rect x="{x}" y="{y}" width="260" height="96" rx="10" fill="{band}"/><rect x="{x}" y="{y + 60}" width="260" height="36" fill="{band}"/>'
                  + label(x + 22, y + 66, title, 34, CREAM)
                  + "".join(f'<rect x="{x + 34 + 52 * i}" y="{y + 300 - h}" width="34" height="{h}" rx="4" fill="{ORANGE if i == 3 else NAVY}"/>' for i, h in enumerate((50, 80, 110, 150)))
                  + "".join(f'<rect x="{x + 30}" y="{y + 118 + 20 * i}" width="{200 - 40 * (i % 2)}" height="9" rx="4" fill="{GREY}"/>' for i in range(2)),
             show, r)


# ---- b-roll ----

def reports():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += report("r1", 120, 330, "Mexico", NAVY, (0.1, dur + 1), rig(250, 670, 2, 0.6))
    s += report("r2", 410, 300, "Guatemala", "#5E7A94", (0.45, dur + 1), rig(540, 640, 2, 0.7))
    s += report("r3", 700, 270, "Field Report", ORANGE, (0.8, dur + 1), rig(830, 610, 3, 0.8))
    return s + "</svg>\n"


def people():
    dur = 3.8
    s = root(dur, "1,0,0")
    for i, (p, x, t, word) in enumerate(((5, 140, 0.2, "Entrepreneurs"), (8, 405, 1.4, "Investors"),
                                         (2, 675, 2.2, "Technologists"), (9, 940, 2.9, "Business"))):
        s += head(p, [(t, "neutral"), (t + 0.5, "happy")], (x, 610), 0.46, i < 2, f"p{i}")
        s += g(f"w{i}", centered(x, 790, word, 34), (t, dur + 1), rig(x, 790, 2, 0.7))
    return s + "</svg>\n"


def interview():
    dur = 3.2
    s = root(dur, "1,0,0")
    s += g("count", f'<rect x="260" y="150" width="560" height="104" rx="14" fill="{ORANGE}"/>' + centered(540, 225, "15–30 interviews", 60, CREAM),
           (0.2, dur + 1), rig(540, 254, 2, 0.6))
    s += head(CAM_P, [(0, "happy"), (1.6, "excited")], (340, 610), 0.5, True, "cam")
    s += head(5, [(0, "neutral"), (0.9, "happy")], (740, 610), 0.5, False, "her")
    s += g("table", f'<ellipse cx="540" cy="780" rx="440" ry="90" fill="{shade(WOOD)}"/><ellipse cx="540" cy="766" rx="440" ry="84" fill="{WOOD}"/>')
    s += g("phone", f'<rect x="484" y="700" width="112" height="56" rx="10" fill="{NAVY}"/><rect x="494" y="708" width="92" height="40" rx="6" fill="#2C4366"/>')
    for k in range(4):                                         # the record dot blinks
        s += g(f"rec{k}", f'<circle cx="540" cy="728" r="13" fill="{ORANGE}"/>', (0.8 * k, 0.8 * k + 0.5))
    return s + "</svg>\n"


def to_report():
    dur = 3.3
    s = root(dur, "1,0,0")
    for i in range(6):                                         # transcripts pile up on the left, then the report appears
        s += g(f"t{i}", sheet(120 + 40 * (i % 3), 330 + 70 * (i // 3) - 8 * i, -8 + 6 * i), (0.1 + 0.18 * i, dur + 1))
    s += g("arrow", f'<path d="M380 520 L560 520" stroke="{NAVY}" stroke-width="18" stroke-linecap="round"/><path d="M540 486 L600 520 L540 554Z" fill="{NAVY}"/>', (1.3, dur + 1))
    s += report("rep", 650, 340, "León", ORANGE, (1.6, dur + 1), rig(780, 680, 3, 0.8))
    return s + "</svg>\n"


# ---- the globe (orthographic, Natural Earth 50m) ----

CARICOM = ["Antigua and Barbuda", "The Bahamas", "Barbados", "Belize", "Dominica", "Grenada", "Guyana", "Haiti", "Jamaica", "Montserrat",
           "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Suriname", "Trinidad and Tobago"]
SEA = ["Indonesia", "Malaysia", "Thailand", "Vietnam", "Philippines", "Cambodia", "Laos", "Myanmar", "Singapore", "Brunei", "East Timor"]
GC, GR = (540, 470), 380                                      # globe center and radius on the frame


def ortho(lon, lat, c):
    """Orthographic projection about c = (lon0, lat0). Points on the far side are pushed to the rim."""
    l, f, l0, f0 = (math.radians(a) for a in (lon, lat, *c))
    x = math.cos(f) * math.sin(l - l0)
    y = math.cos(f0) * math.sin(f) - math.sin(f0) * math.cos(f) * math.cos(l - l0)
    vis = math.sin(f0) * math.sin(f) + math.cos(f0) * math.cos(f) * math.cos(l - l0) >= 0
    if not vis:
        n = math.hypot(x, y) or 1; x, y = x / n, y / n
    return GC[0] + GR * x, GC[1] - GR * y, vis


def globe(c, fills):
    """One globe frame centered on c; fills = {country: color}, every other country cream."""
    from paper_map import _load
    out = [f'<circle cx="{GC[0]}" cy="{GC[1]}" r="{GR + 10}" fill="{NAVY}"/><circle cx="{GC[0]}" cy="{GC[1]}" r="{GR}" fill="#5E7A94"/>']
    for feat in _load("ne_50m_admin_0_countries.geojson"):
        name, geom = feat["properties"]["ADMIN"], feat["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        d = []
        for poly in polys:
            pts = [ortho(lo, la, c) for lo, la in poly[0]]
            if not any(v for _, _, v in pts):
                continue
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            if max(xs) - min(xs) < 5 and max(ys) - min(ys) < 5 and name not in fills:
                continue
            ring, last = [], None
            for x, y, _ in pts:
                if last is None or abs(x - last[0]) + abs(y - last[1]) > 1.5:
                    ring.append(f"{x:.1f} {y:.1f}"); last = (x, y)
            if len(ring) > 2:
                d.append("M" + " L".join(ring) + "Z")
            elif name in fills:                                  # a tiny island we name: draw a dot so it shows
                d.append(f"M{xs[0] - 5:.1f} {ys[0]:.1f} a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0Z")
        if d:
            out.append(f'<path d="{"".join(d)}" fill="{fills.get(name, "#EFE6D2")}"/>')
    return "".join(out)


def regions():
    """Matches the window 13.7-19.2. Real word times (2026-10-28 check): CARICOM 15.0, Guatemala 16.0, Mexico 16.6, Southeast Asia 17.85.
    A red pin drops on the country he names, so the small ones (Guatemala next to gold Belize) read clearly."""
    dur = 5.5
    s = root(dur, "1,0,0").split('  <g id="floor"')[0]
    A, B = (-78, 14), (112, 6)
    tc, tg, tm, t0s, t1s, ta = 1.3, 2.3, 2.9, 3.3, 4.0, 4.15
    past = lambda names: {n: GOLD for n in names}
    steps = [(0, tc, A, {}), (tc, tg, A, {n: ORANGE for n in CARICOM}),
             (tg, tm, A, {**past(CARICOM), "Guatemala": ORANGE}), (tm, t0s, A, {**past(CARICOM + ["Guatemala"]), "Mexico": ORANGE})]
    done = past(CARICOM + ["Guatemala", "Mexico"])
    n = 8
    for i in range(1, n):                                     # the spin west across the Pacific, eased
        k = (1 - math.cos(math.pi * i / n)) / 2
        steps.append((t0s + (t1s - t0s) * (i - 1) / (n - 1), t0s + (t1s - t0s) * i / (n - 1), (A[0] - (A[0] + 360 - B[0]) * k, A[1] + (B[1] - A[1]) * k), done))
    steps.append((t1s, ta, B, done))
    steps.append((ta, dur + 1, B, {**done, **{x: ORANGE for x in SEA}}))
    for i, (a, b, c, fills) in enumerate(steps):
        s += g(f"globe{i}", globe(c, fills), (a, b))
    for i, (lonlat, c, a, b) in enumerate((((-62.5, 11.5), A, tc, tg), ((-90.3, 15.6), A, tg, tm), ((-102.5, 23.5), A, tm, t0s), ((110, 6), B, ta, dur + 1))):
        x, y, _ = ortho(*lonlat, c)
        s += g(f"pin{i}", f'<path d="M{x:.0f} {y:.0f} Q{x - 22:.0f} {y - 30:.0f} {x - 20:.0f} {y - 44:.0f} A21 21 0 1 1 {x + 20:.0f} {y - 44:.0f} Q{x + 22:.0f} {y - 30:.0f} {x:.0f} {y:.0f}Z" '
                           f'fill="{ORANGE}" stroke="{CREAM}" stroke-width="4"/><circle cx="{x:.0f}" cy="{y - 47:.0f}" r="8" fill="{CREAM}"/>', (a + 0.05, b), rig(x, y, 4, 1.0))
    for i, (word, a, b) in enumerate((("CARICOM", tc, tg), ("Guatemala", tg, tm), ("Mexico", tm, t0s), ("Southeast Asia", ta, dur + 1))):
        w = ImageFont.truetype(FONT, 64).getlength(word) + 60
        s += g(f"name{i}", f'<rect x="{540 - w / 2:.0f}" y="880" width="{w:.0f}" height="100" rx="14" fill="{ORANGE}"/>' + centered(540, 952, word, 64, CREAM),
               (a, b), rig(540, 980, 2, 0.6))
    return s + "</svg>\n"


# ---- titles ----

def t_announce():
    dur = 2.1
    s = title_root(dur)
    s += tag("ann", "Announcing", 60, 760, 84, -2, 0.1, dur + 1)[0]
    s += tag("proj", "a cool project", 60, 880, 84, 2, 0.95, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_regions():
    dur = 5.5
    s = title_root(dur)
    for i, (word, t) in enumerate((("CARICOM", 0.4), ("Guatemala", 2.2), ("Mexico", 2.7), ("Southeast Asia", 3.7))):
        y = 600 + 104 * i
        s += check(f"c{i}", 52, y + 12, t, dur) + tag(f"r{i}", word, 128, y, 62, (-1) ** i * 1.5, t, dur + 1)[0]
    return s + "</svg>\n"


def t_weeks():
    dur = 2.7
    s = title_root(dur)
    s += tag("wk", "2 weeks", 60, 760, 96, -2, 0.7, dur + 1)[0]
    s += tag("le", "in León", 60, 890, 96, 2, 2.15, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_asks():
    dur = 3.8
    s = title_root(dur)
    s += tag("hire", "Who do they hire?", 60, 760, 80, -2, 1.1, dur + 1)[0]
    s += tag("grow", "Does it grow?", 60, 880, 80, 2, 2.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


def t_dm():
    dur = 6.4
    s = title_root(dur)
    s += tag("know", "Know anyone in León?", 60, 760, 76, -2, 1.1, dur + 1)[0]
    s += tag("dm", "DM me", 60, 880, 110, 2, 5.5, dur + 1, ORANGE, PAPER)[0]
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", t_announce), ("t2", t_regions), ("t3", t_weeks), ("t4", t_asks), ("t5", t_dm),
                 ("b1", reports), ("b2", regions), ("b3", people), ("b4", interview), ("b5", to_report)):
        open(os.path.join(HERE, f"scenes/rep-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/rep-{n}.svg")
