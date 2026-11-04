#!/usr/bin/env python3
# Photo b-roll experiment: same four photos, same 15 s of voice, one treatment per clip.
# usage: photo_test.py OUTDIR
import math, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from pathlib import Path

OUT = Path(sys.argv[1]); SRC = OUT / "src"
FOOT = str(Path("~/3 day startup Dropbox/Cam Houser/My Mac (Cameron’s MacBook Air)/Downloads/five different videos to edit - 1080WebShareName.mov").expanduser())
T0, DUR, FPS, S = 54.8, 15.0, 24, 1080
N = int(DUR * FPS)
NAVY, CREAM, RED, BLUE = "#182A46", "#F6EEDC", "#DE4A30", "#8CBDDC"
# name, start, end, focus x, focus y, print shape, tilt, cutout ground
PH = [("sid", 5.35, 7.6, .55, .3, "sq", -5, BLUE), ("danny", 7.6, 9.85, .42, .42, "sq", 4, CREAM),
      ("crowd", 9.85, 12.1, .5, .5, "sq", -3, "#E3A84B"), ("group", 12.1, 14.6, .5, .5, "wide", 2, BLUE)]
rng = np.random.default_rng(7)

def smooth(w, h, cell):
    a = rng.random((h // cell + 2, w // cell + 2)) * 255
    return np.asarray(Image.fromarray(a.astype("uint8")).resize((w, h), Image.BICUBIC), float) / 127.5 - 1

def paper(hex_, w=S + 16, h=S + 16):
    a = np.full((h, w, 3), np.array(Image.new("RGB", (1, 1), hex_).getpixel((0, 0))), float)
    a += smooth(w, h, 90)[..., None] * 2.5 + rng.normal(0, 3.5, (h, w, 1))
    return Image.fromarray(a.clip(0, 255).astype("uint8"))

def crop(im, fx, fy, asp):
    w, h = im.size
    cw, ch = (w, w / asp) if w / h < asp else (h * asp, h)
    x, y = (w - cw) * fx, (h - ch) * fy
    return im.crop((int(x), int(y), int(x + cw), int(y + ch)))

def boil(card, amp, warp=False):
    # edges boil through the alpha; with warp the whole picture moves too
    a = np.asarray(card); h, w = a.shape[:2]
    dx, dy = smooth(w, h, 26) * amp, smooth(w, h, 26) * amp
    yy, xx = np.mgrid[0:h, 0:w]
    sy, sx = (yy + dy).round().astype(int).clip(0, h - 1), (xx + dx).round().astype(int).clip(0, w - 1)
    b = a.copy()
    if warp: b = a[sy, sx]
    else: b[..., 3] = a[..., 3][sy, sx]
    return Image.fromarray(b)

def polaroid(im, sh):
    W, H = (720, 540) if sh == "wide" else (620, 620)
    m, foot = 26, 92
    c = Image.new("RGBA", (W + 2 * m + 40, H + m + foot + 40), (251, 248, 240, 0))
    ImageDraw.Draw(c).rectangle((20, 20, 20 + W + 2 * m, 20 + H + m + foot), fill="#FBF8F0")
    c.paste(im.resize((W, H), Image.LANCZOS), (20 + m, 20 + m))
    return c

def cutout(k):
    im = Image.open(SRC / f"{k}.jpg").convert("RGB")
    mk = Image.open(SRC / f"{k}-mask.png").convert("L").resize(im.size)
    x0, y0, x1, y1 = mk.getbbox()
    pad = 30; box = (max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, im.width), min(y1 + pad, im.height))
    im, mk = im.crop(box), mk.crop(box)
    k_ = min(1000 / im.width, 1000 / im.height)
    sz = (int(im.width * k_), int(im.height * k_))
    im, mk = im.resize(sz, Image.LANCZOS), mk.resize(sz, Image.LANCZOS)
    p = 34; c = Image.new("RGBA", (sz[0] + 2 * p, sz[1] + 2 * p), (251, 248, 240, 0))
    M = Image.new("L", c.size, 0); M.paste(mk, (p, p))
    edge = M.filter(ImageFilter.GaussianBlur(9)).point(lambda v: 255 if v > 28 else 0)
    c.paste(Image.new("RGBA", c.size, (251, 248, 240, 255)), (0, 0), edge)
    c.paste(im.convert("RGBA"), (p, p), mk)
    return c

def shadow(c, r=10, op=95):
    sh = Image.new("RGBA", c.size, (24, 42, 70, 0)); sh.putalpha(c.getchannel("A").point(lambda v: v * op // 255))
    return sh.filter(ImageFilter.GaussianBlur(r))

def ease(u): return 1 - (1 - u) ** 3

def place(fr, vars_, t, t0, cx, cy, deg, scale=1.0):
    # lands in 5 frames from 1.3x, a little overshoot, then holds on twos
    f = int((t - t0) * FPS)
    u = min(f / 5, 1); s = 1.3 + (1 - 1.3) * ease(u) if f < 5 else (.975 if f < 7 else 1)
    two = f // 2
    c = vars_[two % len(vars_)]
    d = deg * (1.8 - .8 * ease(u)) + (random.Random(two).uniform(-.25, .25))
    sc = s * scale
    cw = c.resize((int(c.width * sc), int(c.height * sc)), Image.BILINEAR).rotate(d, Image.BILINEAR, expand=True, fillcolor=(251, 248, 240, 0))
    sh = shadow(cw)
    jx, jy = random.Random(two * 3).randint(-1, 1), random.Random(two * 5).randint(-1, 1)
    x, y = cx - cw.width // 2 + jx, cy - cw.height // 2 + jy
    off = int(6 + 26 * (1 - u))
    fr.paste(sh, (x + off, y + off), sh); fr.paste(cw, (x, y), cw)

def footage():
    p = OUT / "foot.mp4"
    if not p.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(T0), "-t", str(DUR), "-i", FOOT, "-vf",
                        f"scale=1242:1242,crop=1080:1080:61:130,fps={FPS}", "-af", "loudnorm=I=-18:TP=-1.5", "-ar", "48000", "-c:v", "libx264", "-crf", "16", str(p)], check=True)
    r = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(p), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    return lambda: Image.frombytes("RGB", (S, S), r.stdout.read(S * S * 3))

PICS = {p[0]: Image.open(SRC / f"{p[0]}.jpg").convert("RGB") for p in PH}
BG = [paper(BLUE) for _ in range(3)]
GR = {h: [paper(h) for _ in range(2)] for h in (BLUE, CREAM, "#E3A84B")}

def cards(warp=False):
    return {p[0]: [boil(polaroid(crop(PICS[p[0]], p[3], p[4], 4 / 3 if p[5] == "wide" else 1), p[5]), 9 if warp else 5.5, warp) for _ in range(4)] for p in PH}

def active(t): return next((p for p in PH if p[1] <= t < p[2]), None)

POS = {"sid": (420, 440), "danny": (660, 470), "crowd": (450, 630), "group": (560, 560)}

def fr_cover(t, fr):
    p = active(t)
    if not p: return fr
    im = crop(PICS[p[0]], p[3], p[4], 1)
    u = (t - p[1]) / (p[2] - p[1]); z = 1.03 + .10 * u
    d = im.width / z; x = (im.width - d) * .5; y = (im.height - d) * .42
    return im.resize((S, S), Image.BICUBIC, (x, y, x + d, y + d))

def stack(t, fr, set_, scale=1.0):
    for p in PH:
        if p[1] <= t < 14.6:
            cx, cy = POS[p[0]]
            place(fr, set_[p[0]], t, p[1], cx, cy, p[6], scale)
    return fr

def fr_print(t, fr, set_):
    if not 5.35 <= t < 14.6: return fr
    b = BG[int(t * 12) % 3].crop((8, 8, S + 8, S + 8)).convert("RGBA")
    return stack(t, b, set_).convert("RGB")

CORNER = {"sid": (780, 760), "danny": (800, 770), "crowd": (770, 760), "group": (720, 790)}
def fr_over(t, fr, set_):
    p = active(t)
    if not p: return fr
    b = fr.convert("RGBA"); place(b, set_[p[0]], t, p[1], *CORNER[p[0]], p[6], .68)
    return b.convert("RGB")

def fr_cut(t, fr, set_):
    p = active(t)
    if not p: return fr
    gr = GR[p[7]][int(t * 12) % 2].crop((8, 8, S + 8, S + 8)).convert("RGBA")
    place(gr, set_[p[0]], t, p[1], S // 2, S // 2, 0)
    return gr.convert("RGB")

def env(n, tau): return np.exp(-np.arange(n) / (tau * 48000))
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / 48000); X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))
def snd(kind, seed):
    r = np.random.default_rng(seed); n = int(.26 * 48000); t = np.arange(n) / 48000
    if kind == "paper":     # card on a table: dry slap, soft thump
        x = band(r.normal(size=n), 900, 6500) * env(n, .012) + .7 * np.sin(2 * np.pi * (115 + seed * 6) * t) * env(n, .03)
    elif kind == "shutter": # two mechanical clicks
        x = band(r.normal(size=n), 1800, 9000) * (env(n, .004) + .8 * np.roll(env(n, .006), int(.07 * 48000)))
    elif kind == "flick":   # light finger flick on card, no thump
        x = band(r.normal(size=n), 2500, 8000) * env(n, .006) + .25 * np.sin(2 * np.pi * 620 * t) * env(n, .012)
    else:                   # tap: low wooden knock
        x = np.sin(2 * np.pi * 180 * t) * env(n, .035) + .3 * band(r.normal(size=n), 300, 1500) * env(n, .008)
    return x / np.abs(x).max()

def sfx_track(kind, level):
    a = np.zeros(int(DUR * 48000))
    for i, p in enumerate(PH):
        s = snd(kind, i) * level; j = int(p[1] * 48000); a[j:j + len(s)] += s
    p = OUT / f"sfx-{kind}.wav"
    w = wave.open(str(p), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((a.clip(-1, 1) * 32767).astype("<i2").tobytes()); w.close()
    return p

def build(name, fn, kind="paper", level=.3):
    nxt = footage(); o = OUT / f"{name}.mp4"; w = sfx_track(kind, level)
    e = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S}x{S}", "-r", str(FPS), "-i", "-",
                          "-i", str(OUT / "foot.mp4"), "-i", str(w), "-filter_complex", "[1:a][2:a]amix=2:normalize=0[a]", "-map", "0:v", "-map", "[a]",
                          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), str(o)], stdin=subprocess.PIPE)
    for i in range(N):
        e.stdin.write(fn(i / FPS, nxt()).tobytes())
    e.stdin.close(); e.wait(); print(o)

if __name__ == "__main__":
    pol, pol_w = cards(), cards(True)
    cut = {p[0]: [boil(cutout(p[0]), 5.5) for _ in range(4)] for p in PH}
    build("a-full-kenburns", fr_cover)
    build("b-polaroid-on-paper", lambda t, f: fr_print(t, f, pol))
    build("b2-polaroid-photo-warp", lambda t, f: fr_print(t, f, pol_w))
    build("c-polaroid-over-footage", lambda t, f: fr_over(t, f, pol))
    build("d-cutout", lambda t, f: fr_cut(t, f, cut))
    for k, lv in (("shutter", .22), ("flick", .3), ("tap", .3)):
        build(f"sound-{k}", lambda t, f: fr_print(t, f, pol), k, lv)
