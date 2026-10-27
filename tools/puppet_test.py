"""Cut-out puppet test from two image-AI character sheets (body sheet + head-expression sheet) -> mp4

usage: python3 tools/puppet_test.py BODY_SHEET.png HEAD_SHEET.png OUT.mp4
Coordinates below are in body-sheet pixels, measured by hand for the first test woman (Gemini, 2026-10-27).
The standing body faces right, the head sheet faces left, so the heads are mirrored. White -> transparent.
Beat: she raises her phone (forearm turns at the elbow), looks down at it, then reacts (neutral -> surprised).
"""
import math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PAPER = (251, 248, 242)
S = 2.1                         # body sheet -> frame scale
OFF = (540 - 132 * S, 1010 - 425 * S)
HEAD_K = 0.37 * S               # head sheet -> frame scale
HAND_K = 0.40 * S
ELBOW = (196, 168)              # forearm pivot (body sheet), her front arm
FOREARM = [(186, 162), (214, 156), (236, 226), (208, 232)]
HAND_ERASE = [(186, 156), (252, 150), (252, 268), (204, 268), (204, 236), (188, 200)]
HEAD_ERASE = [(78, 0), (182, 0), (182, 86), (165, 88), (120, 90), (78, 88)]
WRIST0 = (220, 228)              # wrist with the arm hanging
NECK = (142, 88)
EYES_BODY, EYES_SHEET = (142, 43), (162, 120)   # eye midpoint: body / mirrored head cell
HAND_WRIST = (928, 408)         # phone hand: wrist point on the body sheet
HAND_BOX = (892, 252, 1010, 425)
CELLS = {"neutral": (0, 0), "happy": (1, 0), "excited": (2, 0), "skeptical": (3, 0),
         "confused": (0, 1), "tired": (1, 1), "worried": (2, 1), "surprised": (3, 1)}


def cutout(im):
    a = np.asarray(im.convert("RGB")).astype(float)
    alpha = np.clip((765 - a.sum(2)) / 90, 0, 1)
    return Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")


def poly_mask(size, poly, scale=1.0, off=(0, 0)):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon([((x - off[0]) * scale, (y - off[1]) * scale) for x, y in poly], fill=255)
    return m


def up(im, k):
    return im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)


def build(body_path, head_path):
    sheet = cutout(Image.open(body_path))
    body = sheet.crop((0, 0, 260, 430))
    forearm = Image.new("RGBA", body.size); forearm.paste(body, mask=poly_mask(body.size, FOREARM))
    hole = poly_mask(body.size, HAND_ERASE); hole.paste(255, mask=poly_mask(body.size, HEAD_ERASE))
    body.putalpha(Image.fromarray((np.asarray(body.getchannel("A")) * (1 - np.asarray(hole) / 255)).astype(np.uint8)))
    hand = sheet.crop(HAND_BOX)
    hs = cutout(Image.open(head_path))
    cw, ch = hs.width // 4, hs.height // 2
    heads = {k: up(hs.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)).transpose(Image.FLIP_LEFT_RIGHT), HEAD_K) for k, (c, r) in CELLS.items()}
    return up(body, S), up(forearm, S), up(hand, HAND_K), heads


def F(p):
    return (OFF[0] + p[0] * S, OFF[1] + p[1] * S)


def paste_rot(frame, im, anchor_src, anchor_dst, deg):
    """Rotate im by deg (counterclockwise) about its point anchor_src, then place that point at anchor_dst."""
    pad = int(math.hypot(*im.size)) + 4
    big = Image.new("RGBA", (pad * 2, pad * 2))
    big.paste(im, (int(pad - anchor_src[0]), int(pad - anchor_src[1])))
    big = big.rotate(deg, resample=Image.BICUBIC, center=(pad, pad))
    frame.alpha_composite(big, (int(round(anchor_dst[0] - pad)), int(round(anchor_dst[1] - pad))))


def ease(t):
    t = min(max(t, 0), 1)
    return t * t * (3 - 2 * t)


def frame_at(t, parts):
    body, forearm, hand, heads = parts
    fr = Image.new("RGBA", (1080, 1080), PAPER + (255,))
    raise_ = ease((t - 0.3) / 0.9)
    react = ease((t - 2.4) / 0.12)
    settle = ease((t - 2.55) / 0.5)
    arm = 99 * raise_
    tilt = -5 * raise_ + 7 * react - 3 * settle          # look down at the phone, snap back on the surprise
    # elbow disc hides the cut while the forearm turns
    ex, ey = F(ELBOW)
    fr.paste(body, (int(OFF[0]), int(OFF[1])), body)
    d = ImageDraw.Draw(fr)
    d.ellipse([ex - 20, ey - 20, ex + 20, ey + 20], fill=(226, 172, 92, 255))
    pe = (ELBOW[0] * S, ELBOW[1] * S)
    paste_rot(fr, forearm, pe, (ex, ey), arm)
    a = math.radians(-arm)                               # screen rotation of the wrist about the elbow
    vx, vy = (WRIST0[0] - ELBOW[0]) * S, (WRIST0[1] - ELBOW[1]) * S
    wx, wy = ex + vx * math.cos(a) - vy * math.sin(a), ey + vx * math.sin(a) + vy * math.cos(a)
    hw = ((HAND_WRIST[0] - HAND_BOX[0]) * HAND_K, (HAND_WRIST[1] - HAND_BOX[1]) * HAND_K)
    paste_rot(fr, hand, hw, (wx, wy), arm - 99)
    # head: mirrored cell, eye midpoint on the body's eye midpoint, rotated about the neck
    eye = EYES_SHEET
    nx, ny = F(NECK)
    ex_, ey_ = F(EYES_BODY)
    anchor = (eye[0] * HEAD_K + (nx - ex_), eye[1] * HEAD_K + (ny - ey_))
    if react <= 0:
        paste_rot(fr, heads["neutral"], anchor, (nx, ny), tilt)
    else:
        h = Image.blend(heads["neutral"], heads["surprised"], react)
        paste_rot(fr, h, anchor, (nx, ny), tilt)
    return fr.convert("RGB")


def main(body_path, head_path, out):
    parts = build(body_path, head_path)
    tmp = tempfile.mkdtemp()
    for i in range(135):
        frame_at(i / 30, parts).save(f"{tmp}/{i:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", f"{tmp}/%04d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    frame_at(1.8, parts).save(out.replace(".mp4", "-a.png"))
    frame_at(3.6, parts).save(out.replace(".mp4", "-b.png"))
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
