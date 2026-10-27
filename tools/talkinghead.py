"""Finish a talking-head video with b-roll: one command from rendered beats to the upload file.

usage: python3 tools/talkinghead.py videos/NAME.json REV
       -> OUT_DIR/NAME-revREV.mp4  (+ OUT_DIR/NAME-thumbnail.png)

Steps (each one is what Cam approved on the Leon video, rev22, 2026-10-27):
  1. composite  center-square crop of the footage, the GRADE, then every overlay at its time (titles = alpha .mov)
  2. trim       one segment, cut[0]..cut[1]; short audio fades so the cut does not click
  3. voice      VOICE chain: EQ + 3:1 compression + limiter + loudnorm -16 LUFS
  4. music      filtered music bed, `under_db` below the voice mean, light ducking, 0.3 s in / 2 s out
  5. thumbnail  split frame: graded face (left half), a b-roll panel (right half), one red paper tag
  6. splice     the thumbnail as the first 3 frames (0.125 s, silent): X uses frame 1 as the preview

The JSON (see videos/leon.json):
  src, out_dir, crop_x, cut [in, out], overlays {key: [file, t0, t1]} in ORIGINAL footage time,
  music {file, start, band [hp, lp], under_db}, thumb {face_t, panel_file, panel_t, panel_x, tag}
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

GRADE = ("eq=gamma=1.09:contrast=1.025:brightness=0.0075:saturation=1.06,"        # half of rev19 (Cam: full was "pale and washed out")
         "colorbalance=rs=0.015:bs=-0.015:rm=0.015:gm=-0.0025:bm=-0.015:rh=0.005:bh=-0.005,"
         "curves=all='0/0.01 0.25/0.255 0.5/0.525 0.75/0.775 1/1'")
VOICE = ("highpass=f=80,equalizer=f=300:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=3,highshelf=f=10000:g=2,"
         "acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=3,alimiter=limit=0.89:level=false,"
         "loudnorm=I=-16:TP=-1.5:LRA=11")
FONT = "/Library/Fonts/LibreFranklin-ExtraBold.ttf"
CREAM, RED = "#F6EEDC", "#DE4A30"
ENC = ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k"]


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def mean_db(path, *pre):
    r = subprocess.run(["ffmpeg", *pre, "-i", path, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    return float(r.stderr.split("mean_volume: ")[1].split(" dB")[0])


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))


def composite(v, out):
    d = os.path.expanduser(v["out_dir"])
    ins, f, last = ["-i", os.path.expanduser(v["src"])], [f"[0:v]crop=1080:1080:{v['crop_x']}:0,{GRADE}[s0]"], "s0"
    for i, (k, (name, t0, t1)) in enumerate(v["overlays"].items(), 1):
        ins += ["-i", os.path.join(d, name)]
        fmt = ":format=auto" if name.endswith(".mov") else ""
        f.append(f"[{i}:v]setpts=PTS-STARTPTS+{t0}/TB[c{i}]")
        f.append(f"[{last}][c{i}]overlay=eof_action=pass{fmt}:enable='between(t,{t0},{t1})'[s{i}]")
        last = f"s{i}"
    ff(*ins, "-filter_complex", ";".join(f), "-map", f"[{last}]", "-map", "0:a", *ENC, out)


def trim_voice(src, v, out):
    a, b = v["cut"]
    ff("-i", src, "-filter_complex",
       f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,"
       f"afade=t=in:d=0.03,afade=t=out:st={b - a - 0.15:.2f}:d=0.15,{VOICE},aresample=48000[a]",
       "-map", "[v]", "-map", "[a]", *ENC, out)


def music(src, v, out):
    m = v["music"]; mf = os.path.expanduser(m["file"]); D = duration(src)
    band = f"highpass=f={m['band'][0]},lowpass=f={m['band'][1]}"
    gain = mean_db(src) - m["under_db"] - mean_db(mf, "-ss", str(m["start"]), "-t", str(D))
    ff("-i", src, "-ss", str(m["start"]), "-i", mf, "-filter_complex",
       f"[1:a]aresample=48000,atrim=0:{D},asetpts=PTS-STARTPTS,{band},volume={gain:.1f}dB,"
       f"afade=t=in:d=0.3,afade=t=out:st={D - 2:.2f}:d=2.0[m];[0:a]aresample=48000,asplit=2[v][sc];"
       "[m][sc]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=500[md];"
       "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89:level=false[a]",
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out)


def thumbnail(v, tmp, out):
    t = v["thumb"]; d = os.path.expanduser(v["out_dir"])
    face, panel = os.path.join(tmp, "face.png"), os.path.join(tmp, "panel.png")
    ff("-ss", str(t["face_t"]), "-i", os.path.expanduser(v["src"]), "-frames:v", "1",
       "-vf", f"crop=1080:1080:{v['crop_x']}:0,{GRADE}", face)
    seek = ["-sseof", str(t["panel_t"])] if t["panel_t"] < 0 else ["-ss", str(t["panel_t"])]
    ff(*seek, "-i", os.path.join(d, t["panel_file"]), "-frames:v", "1", panel)
    im = Image.new("RGBA", (1080, 1080), CREAM)
    im.paste(Image.open(face).convert("RGBA").crop((270, 0, 810, 1080)), (0, 0))
    px = t["panel_x"]; im.paste(Image.open(panel).convert("RGBA").crop((px, 0, px + 540, 1080)), (540, 0))
    ImageDraw.Draw(im).rectangle([532, 0, 548, 1080], fill=CREAM)
    F = ImageFont.truetype(FONT, 92); w = F.getbbox(t["tag"])[2]
    tg = Image.new("RGBA", (w + 46, 129), RED); ImageDraw.Draw(tg).text((23, 9), t["tag"], font=F, fill=CREAM)
    im.alpha_composite(tg.rotate(2, expand=True, resample=Image.BICUBIC), (90, 880))
    im.convert("RGB").save(out)


def splice(thumb, src, out):
    ff("-loop", "1", "-framerate", "24", "-t", "0.125", "-i", thumb, "-f", "lavfi", "-t", "0.125",
       "-i", "anullsrc=r=48000:cl=stereo", "-i", src, "-filter_complex",
       "[0:v]format=yuv420p,setsar=1[t];[2:v]setsar=1[m];[t][1:a][m][2:a]concat=n=2:v=1:a=1[v][a]",
       "-map", "[v]", "-map", "[a]", *ENC, "-movflags", "+faststart", out)


if __name__ == "__main__":
    cfg, rev = sys.argv[1], sys.argv[2]
    v = json.load(open(cfg)); name = os.path.splitext(os.path.basename(cfg))[0]
    d = os.path.expanduser(v["out_dir"])
    with tempfile.TemporaryDirectory() as tmp:
        steps = [os.path.join(tmp, n) for n in ("1-comp.mp4", "2-voice.mp4", "3-music.mp4")]
        composite(v, steps[0]); print("composite")
        trim_voice(steps[0], v, steps[1]); print("trim + voice")
        music(steps[1], v, steps[2]); print("music")
        thumb = os.path.join(d, f"{name}-thumbnail.png"); thumbnail(v, tmp, thumb); print("thumbnail", thumb)
        out = os.path.join(d, f"{name}-rev{rev}.mp4"); splice(thumb, steps[2], out)
    print(out, f"{duration(out):.2f}s")
