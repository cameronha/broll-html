"""Lay the Leon b-roll and titles over the center-square footage.

usage: python3 tools/leon_composite.py OUT.mp4 REV_OF_EACH   e.g. t1=9 t2=8 t3=8 0=6 1a=7 1b=8 2=9 3=9 4=9
Files: 45-leon/title-{t}-rev{N}.mov (alpha) and 45-leon/beat{b}-rev{N}.mp4.
"""
import os, subprocess, sys

D = os.path.join(os.environ.get("BROLL_OUT", os.path.expanduser("~/broll-out")), "45-leon")
SRC = os.path.expanduser("~/Downloads/agentweekin leon2026-10-16 16-35-37.mp4")
TIMES = {"t1": (3.45, 6.31), "t3": (16.6, 19.3), "t2": (20.5, 24.0), "0": (6.31, 8.44), "t4": (8.9, 11.2), "1a": (11.2, 12.66),   # rev12+: short cuts
         "1b": (12.66, 14.2), "2": (28.28, 30.84), "t5": (32.2, 36.9), "3": (37.07, 39.72),
         "t6": (39.8, 44.0), "4": (44.0, 46.0)}

out, revs = sys.argv[1], dict(a.split("=") for a in sys.argv[2:])
GRADE = ("eq=gamma=1.09:contrast=1.025:brightness=0.0075:saturation=1.06,"        # footage only; rev20 = half of rev19 (Cam: "pale and washed out")
         "colorbalance=rs=0.015:bs=-0.015:rm=0.015:gm=-0.0025:bm=-0.015:rh=0.005:bh=-0.005,"
         "curves=all='0/0.01 0.25/0.255 0.5/0.525 0.75/0.775 1/1'")
ins, f, last = ["-i", SRC], [f"[0:v]crop=1080:1080:420:0,{GRADE}[s0]"], "s0"
for i, (k, (t0, t1)) in enumerate(TIMES.items(), 1):
    name = f"title-{k}-rev{revs[k]}.mov" if k.startswith("t") else f"beat{k}-rev{revs[k]}.mp4"
    ins += ["-i", os.path.join(D, name)]
    fmt = ":format=auto" if k.startswith("t") else ""
    f.append(f"[{i}:v]setpts=PTS-STARTPTS+{t0}/TB[c{i}]")
    f.append(f"[{last}][c{i}]overlay=eof_action=pass{fmt}:enable='between(t,{t0},{t1})'[s{i}]")
    last = f"s{i}"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(f), "-map", f"[{last}]", "-map", "0:a",
                "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", out], check=True)
print(out)
