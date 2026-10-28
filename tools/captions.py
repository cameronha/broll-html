"""Burned-in captions for a finished talking-head rev: one phrase at a time, top center (Cam's FCP caption style).

usage: python3 tools/captions.py WORDS.srt IN.mp4 OUT.mp4 [--print]
WORDS.srt = whisper-cli -osrt -ml 1 on IN's audio. Phrases break at . ? , and pauses, max MAXC characters.
Caption PNGs + a concat list become a transparent qtrle track that is overlaid; audio is copied.
"""
import os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/Library/Fonts/LibreFranklin-Medium.ttf"
SIZE, TOP, MAXC, W = 29, 26, 26, 1080                  # half size, in the dark strip above the background panel (Cam, rev3)
NAVY = (24, 42, 70, 255)                               # outline keeps white text legible on the light-blue b-roll
FIXES = {"gonna": "going to"}


def words(path):
    t = open(path).read()
    out = []
    for m in re.finditer(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)\n(.*)", t):
        a = [int(x) for x in m.groups()[:8]]
        s, e, w = a[0] * 3600 + a[1] * 60 + a[2] + a[3] / 1000, a[4] * 3600 + a[5] * 60 + a[6] + a[7] / 1000, m.group(9).strip()
        if not w:
            continue
        glue = out and (w[0] in ".,?!'-" or out[-1][2] in ("$", "-") or out[-1][2].endswith("-") or (out[-1][2][-1] == "," and w[0].isdigit()))
        if glue:
            out[-1][1], out[-1][2] = e, out[-1][2] + w
        else:
            out.append([s, e, FIXES.get(w, w)])
    return out


def phrases(ws):
    chunks, cur = [], []                               # chunks end at . ? ! , or a pause
    for s, e, w in ws:
        if cur and (cur[-1][2][-1] in ".?!" or (cur[-1][2][-1] == "," and len(" ".join(x[2] for x in cur)) > 10) or s - cur[-1][1] > 0.35):
            chunks.append(cur); cur = []
        cur.append((s, e, w))
    chunks.append(cur)
    ph = []
    for c in chunks:                                   # a long chunk splits into n parts of near-equal length
        n = -(-len(" ".join(x[2] for x in c)) // MAXC)
        target = len(" ".join(x[2] for x in c)) / n
        part, parts = [], 1
        for x in c:
            if part and parts < n and len(" ".join(y[2] for y in part + [x])) > target + 4:
                ph.append(part); part = []; parts += 1
            part.append(x)
        ph.append(part)
    out = []
    for i, p in enumerate(ph):
        text = " ".join(x[2] for x in p).rstrip(".,")
        end = p[-1][1] + 0.3
        if i + 1 < len(ph):
            end = min(max(end, p[-1][1]), ph[i + 1][0][0]) if ph[i + 1][0][0] - p[-1][1] < 0.6 else end
        out.append((p[0][0], end, text))
    return out


def card(text, path):
    f = ImageFont.truetype(FONT, SIZE)
    im = Image.new("RGBA", (W, TOP + SIZE * 2), (0, 0, 0, 0))
    x = (W - f.getlength(text)) / 2
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + 1, TOP + 2), text, font=f, fill=(0, 0, 0, 190), stroke_width=2, stroke_fill=(0, 0, 0, 190))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(im).text((x, TOP), text, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=NAVY)
    im.save(path)


def main():
    src, vin, vout = sys.argv[1:4]
    ph = phrases(words(src))
    if "--print" in sys.argv:
        for s, e, t in ph:
            print(f"{s:7.2f} {e:7.2f}  {t}")
        return
    d = tempfile.mkdtemp()
    Image.new("RGBA", (W, TOP + SIZE * 2), (0, 0, 0, 0)).save(f"{d}/blank.png")
    lst, t = [], 0.13                                  # the first 3 frames are the thumbnail: no caption there
    lst.append(("blank.png", 0.13))
    for i, (s, e, text) in enumerate(ph):
        s = max(s, t)
        if s > t:
            lst.append(("blank.png", s - t))
        card(text, f"{d}/c{i}.png"); lst.append((f"c{i}.png", e - s)); t = e
    with open(f"{d}/list.txt", "w") as fh:
        for f, dur in lst:
            fh.write(f"file '{f}'\nduration {dur:.3f}\n")
        fh.write("file 'blank.png'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{d}/list.txt", "-r", "24000/1001",
                    "-c:v", "qtrle", "-pix_fmt", "argb", f"{d}/cap.mov"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vin, "-i", f"{d}/cap.mov", "-filter_complex", "[0:v][1:v]overlay=0:0:eof_action=pass[v]",
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", vout], check=True)
    print(vout)


main()
