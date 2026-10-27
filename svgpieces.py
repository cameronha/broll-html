"""Rasterize a hand-coded SVG scene into paper pieces (one per top-level <g id>).

usage: python3 svgpieces.py scene.svg OUTDIR motion [pivot_x pivot_y hinge_deg]
The SVG is 1080x1080 with data-bg="#rrggbb" on the root. Group order = draw order;
for motion "hinge" the LAST group is the hinged piece, swinging about the pivot.

Optional root attributes:
  data-finish="cut"   cut-paper finish: rough edges, a small shadow under each shape, paper grain
  data-variants="3"   render each piece N times with a different edge seed (edges boil on twos)
  data-border="0"     no white paper border around each piece
  data-zoom="s,tx,ty" scale and move every non-static group (and its pivot); scenery stays full size
  data-bg-boil="0.5"  how much the background boils, 0..1 (default 1): texture warp and scenery-edge change
  data-step="1" data-jitter="0" data-shadow="0"   smooth motion for painted styles (rig motion)
  data-boil-step="4"  frames between edge-seed changes (default 2 = on twos)
Root data-transparent="1": no background in the render (titles to lay over footage; render.py writes ProRes 4444).
Group attribute data-show="t0,t1": draw the group only from t0 to t1 seconds (expression swaps).
Group attribute data-static="1": scenery, flattened into the background (no motion). With data-variants,
the background gets N versions too: scenery edges boil and the paper texture warps ~1.5px in place.
Optional group attributes (motion "rig": every group can swing on its own pivot):
  data-pivot="x,y" data-deg="-12" data-freq="1.1" data-phase="0" data-shape="snap|sine"
"""
import json, os, re, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

CUT = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="cut" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1180" height="1180">
 <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="1" result="n"/>
 <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
 <feDropShadow in="d" dx="2" dy="3" stdDeviation="1.8" flood-color="#182A46" flood-opacity="0.35"/></filter>
<filter id="cutbg" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1180" height="1180">
 <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="1" data-fixed="1" result="a"/>
 <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="1" result="b"/>
 <feComposite in="a" in2="b" operator="arithmetic" k1="0" k2="{K2}" k3="{K3}" k4="0" result="n"/>
 <feDisplacementMap in="SourceGraphic" in2="n" scale="{SC}" xChannelSelector="R" yChannelSelector="G" result="d"/>
 <feDropShadow in="d" dx="2" dy="3" stdDeviation="1.8" flood-color="#182A46" flood-opacity="0.35"/></filter>
</defs></svg><style>svg > g > *{filter:url(#cut)} svg > g[data-static] > *{filter:url(#cutbg)}</style>"""


def fibers(size, rng, n):
    """Short light and dark paper fibers, as a multiplier around 0."""
    fib = Image.new("L", size, 128)
    d = ImageDraw.Draw(fib)
    for _ in range(n):
        x, y, L, t = rng.random() * size[0], rng.random() * size[1], 6 + rng.random() * 22, rng.random() * np.pi
        d.line([(x, y), (x + L * np.cos(t), y + L * np.sin(t))], fill=int(rng.choice([95, 165])), width=1)
    return np.asarray(fib.filter(ImageFilter.GaussianBlur(0.6)), np.float32)[..., None] / 128 - 1


def grain(im, seed, amt=0.07, fib=0.3):
    """Paper texture: fibers plus fine noise, fixed per piece (does not boil)."""
    rng = np.random.default_rng(seed)
    n = Image.fromarray((rng.random(im.size[::-1]) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    n = np.asarray(n, np.float32)[..., None] / 255
    a = np.asarray(im, np.float32)
    a[..., :3] *= (1 - amt + amt * 2 * n) * (1 + fib * fibers(im.size, rng, int(im.size[0] * im.size[1] / 830)))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), im.mode)


def warp(im, seed, amp=1.5):
    """Shift each pixel by a smooth random offset of up to ~amp px (nearest neighbour)."""
    rng = np.random.default_rng(seed)
    h, w = im.size[1], im.size[0]
    def field():
        f = Image.fromarray((rng.random((h, w)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))
        f = np.asarray(f, np.float32)
        return (f - f.mean()) / (f.std() + 1e-6) * amp
    yy, xx = np.mgrid[0:h, 0:w]
    xs = np.clip(np.rint(xx + field()), 0, w - 1).astype(int)
    ys = np.clip(np.rint(yy + field()), 0, h - 1).astype(int)
    return Image.fromarray(np.asarray(im)[ys, xs])


def paper_bg(color):
    """Paper ground: soft mottling. Fibers and grain go on after the scenery is flattened in."""
    im = Image.new("RGB", (1080, 1080), color)
    rng = np.random.default_rng(42)
    m = Image.fromarray((rng.random((1080, 1080)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40))
    m = np.asarray(m, np.float32)[..., None] / 255
    m = (m - m.mean()) / (m.std() + 1e-6)
    a = np.asarray(im, np.float32) * (1 + 0.02 * m)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def attr(svg, name, default=None):
    m = re.search(rf'<svg[^>]*\b{name}="([^"]+)"', svg)
    return m.group(1) if m else default


def main():
    svg_path, out, motion = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    svg = open(svg_path).read()
    zoom = attr(svg, "data-zoom")
    if zoom:
        zs, ztx, zty = (float(x) for x in zoom.split(","))
        svg = re.sub(r'<g id="([^"]+)"(?![^>]*data-static)',
                     rf'<g transform="translate({ztx} {zty}) scale({zs})" id="\1"', svg)
    groups = re.findall(r'<g (?:transform="[^"]*" )?id="([^"]+)"([^>]*)>', svg)
    bg, finish = attr(svg, "data-bg"), attr(svg, "data-finish")
    nvar, border = int(attr(svg, "data-variants", 1)), int(attr(svg, "data-border", 5))
    base = (paper_bg(bg) if finish else Image.new("RGB", (1080, 1080), bg)).convert("RGBA")
    bgs = [base.copy() for _ in range(nvar)]
    manifest = {"bg": "bg.png", "motion": motion, "dur": float(attr(svg, "data-dur", 4.5)), "stagger": 0.3, "dir": 1,
                "variants": nvar, "boil_step": int(attr(svg, "data-boil-step", 2)), "bg_life": finish == "cut", "step": int(attr(svg, "data-step", 2)),
                "jitter": float(attr(svg, "data-jitter", 1)), "transparent": attr(svg, "data-transparent", "0") == "1", "shadow": float(attr(svg, "data-shadow", 0.6)), "pieces": []}
    if len(sys.argv) > 6:
        manifest.update(pivot=[float(sys.argv[4]), float(sys.argv[5])], hinge=[0, float(sys.argv[6])])
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        page = b.new_page(viewport={"width": 1080, "height": 1080})
        bb = float(attr(svg, "data-bg-boil", 1))   # the fixed noise keeps edges rough; only bb of it changes
        cut = CUT.replace("{K2}", str(1 - bb)).replace("{K3}", str(bb)).replace(
            "{SC}", str(round(7 / ((1 - bb) ** 2 + bb ** 2) ** 0.5, 2)))
        page.set_content(f"<style>html,body{{margin:0;background:transparent}}</style>"
                         f"{cut if finish == 'cut' else ''}{svg}")
        for k, (gid, rest) in enumerate(groups, 1):
            page.evaluate("id => document.querySelectorAll('svg > g').forEach(g => "
                          "g.style.display = g.id === id ? '' : 'none')", gid)
            static = 'data-static="1"' in rest
            shots = []
            for v in range(nvar):
                page.evaluate("s => document.querySelectorAll('feTurbulence:not([data-fixed])').forEach(t => "
                              "t.setAttribute('seed', s))", 1 + v * 17)
                tmp = os.path.join(out, "_tmp.png")
                page.screenshot(path=tmp, omit_background=True)
                im = Image.open(tmp).convert("RGBA")
                if border:              # white paper border, like the photo pieces
                    outer = im.getchannel("A").filter(ImageFilter.MaxFilter(border * 2 + 1))
                    paper = Image.new("RGBA", im.size, (255, 255, 255, 0))
                    paper.putalpha(outer)
                    paper.alpha_composite(im)
                    im = paper
                shots.append(grain(im, k) if finish and not static else im)
            if static:
                for v in range(nvar):
                    bgs[v].alpha_composite(shots[v])
                continue
            boxes = [s.getchannel("A").getbbox() for s in shots]
            box = (min(x[0] for x in boxes), min(x[1] for x in boxes),
                   max(x[2] for x in boxes), max(x[3] for x in boxes))
            srcs = []
            for v, s in enumerate(shots):
                srcs.append(f"piece-{k:02d}" + (f"-{v}" if nvar > 1 else "") + ".png")
                s.crop(box).save(os.path.join(out, srcs[-1]))
            p = {"src": srcs[0], "srcs": srcs, "id": gid, "x": box[0], "y": box[1],
                 "w": box[2] - box[0], "h": box[3] - box[1]}
            show = re.search(r'data-show="([^"]+)"', rest)
            if show:
                p["show"] = [float(x) for x in show.group(1).split(",")]
            rig = dict(re.findall(r'data-(pivot|deg|freq|phase|shape)="([^"]+)"', rest))
            if "pivot" in rig:
                px, py = (float(x) for x in rig["pivot"].split(","))
                if zoom:
                    px, py = px * zs + ztx, py * zs + zty
                p["rig"] = {"pivot": [px, py],
                            "deg": float(rig.get("deg", 10)), "freq": float(rig.get("freq", 1)),
                            "phase": float(rig.get("phase", 0)), "shape": rig.get("shape", "snap")}
            manifest["pieces"].append(p)
        os.remove(tmp)
        for v, im in enumerate(bgs):
            im = im.convert("RGB")
            if finish:
                im = grain(im, 0, 0.13, 0.35)       # same fibers in every version...
                if nvar > 1:
                    im = warp(im, 100 + v, 1.5 * bb)          # ...nudged in place, so they boil, not flicker
            im.save(os.path.join(out, f"bg-{v}.png"))
        manifest["bg"], manifest["bgs"] = "bg-0.png", [f"bg-{v}.png" for v in range(nvar)]
        b.close()
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(out)


if __name__ == "__main__":
    main()
