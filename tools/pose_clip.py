"""Pose-cut motion comic: 3 generated poses, registered on the feet, phone prop behind the grip hand."""
import subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Users/cameronhouser/Coding/broll-html/tools")
import puppet_test as P
from motion_comic_test import boil
SRC, OUT, MODE = sys.argv[1], sys.argv[2], sys.argv[3]       # MODE = cut | dissolve
K = 1.6
sheet = P.cutout(Image.open(SRC))
a = np.asarray(sheet.getchannel("A")) > 40
cols = np.where(a.sum(0) > 2)[0]
splits = np.split(cols, np.where(np.diff(cols) > 30)[0] + 1)
figs = []
for c in splits:
    x0, x1 = c[0], c[-1] + 1
    rows = np.where(a[:, x0:x1].sum(1) > 0)[0]; y0, y1 = rows[0], rows[-1] + 1
    sub = a[y0:y1, x0:x1]; h = y1 - y0
    legs = sub[int(h * .6):int(h * .9)]
    cx = np.nonzero(legs)[1].mean()                       # leg centre = register point
    figs.append((sheet.crop((x0, y0, x1, y1)), cx, y1))
print([(f[0].size, round(f[1])) for f in figs])

def phone(fig):
    """grey-ochre phone behind the curled fingers of pose 1"""
    im = Image.new("RGBA", fig.size)
    d = ImageDraw.Draw(im)
    x, y = PX, PY
    d.rounded_rectangle([x - 11, y - 22, x + 11, y + 22], 4, fill=(120, 88, 52, 255), outline=(52, 38, 30, 255), width=2)
    d.rounded_rectangle([x - 8, y - 18, x + 8, y + 18], 2, fill=(244, 226, 190, 255))
    im.alpha_composite(fig); return im

def frame_for(i_pose):
    fig, cx, bottom = figs[i_pose]
    if i_pose == 0: fig = phone(fig)
    fr = Image.new("RGBA", (1080, 1080), P.PAPER + (255,))
    f = P.up(fig, K)
    fr.alpha_composite(f, (int(540 - cx * K), int(1040 - f.height)))
    return np.asarray(fr.convert("RGB")).astype(float)

PX, PY = map(int, sys.argv[4:6]) if len(sys.argv) > 5 else (0, 0)
rng = np.random.default_rng(2)
var = [[boil(frame_for(p), rng) for _ in range(3)] for p in range(3)]
if MODE == "still":
    var[0][0].save(OUT); sys.exit()
T = [0, 2.2, 4.2]
tmp = tempfile.mkdtemp()
for i in range(195):
    t = i / 30
    p = 2 if t >= T[2] else 1 if t >= T[1] else 0
    im = var[p][(i // 3) % 3]
    if MODE == "dissolve" and p > 0 and t - T[p] < 0.2:
        im = Image.blend(var[p - 1][(i // 3) % 3], im, (t - T[p]) / 0.2)
    k = P.ease((t - T[p]) / 0.08) - P.ease((t - T[p] - 0.1) / 0.4) if p > 0 and MODE == "cut" else 0
    z = 1.0 + 0.10 * t / 6.5 + 0.03 * k
    w = 1080 / z; cy = min(max(470, w / 2), 1080 - w / 2)
    im.crop((540 - w / 2, cy - w / 2, 540 + w / 2, cy + w / 2)).resize((1080, 1080), Image.LANCZOS).save(f"{tmp}/{i:04d}.png")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", f"{tmp}/%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", OUT], check=True)
print("wrote", OUT)
