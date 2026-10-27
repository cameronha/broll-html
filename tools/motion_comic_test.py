"""Motion-comic test: the realistic puppet held still; life comes from camera, expression cuts and line boil -> mp4

usage: python3 tools/motion_comic_test.py BODY_SHEET.png HEAD_SHEET.png OUT.mp4
No limb turns. Beat: slow push-in on a neutral woman; at 2.3 s a hard cut to the surprised head with a small
jolt and a short punch-in. The lines boil on threes (3 displacement variants per head, like svgpieces).
"""
import subprocess, sys, tempfile
import numpy as np
from PIL import Image
import puppet_test as P

FOCUS = (540, 430)      # push-in centre (her upper body)
BOIL = 1.4              # boil amplitude in pixels


def still(parts, expr):
    body, forearm, hand, heads = parts
    fr = Image.new("RGBA", (1080, 1080), P.PAPER + (255,))
    fr.paste(body, (int(P.OFF[0]), int(P.OFF[1])), body)
    fr.alpha_composite(forearm, (int(P.OFF[0]), int(P.OFF[1])))      # forearm and hand back in their drawn place
    nx, ny = P.F(P.NECK); ex, ey = P.F(P.EYES_BODY)
    anchor = (P.EYES_SHEET[0] * P.HEAD_K + (nx - ex), P.EYES_SHEET[1] * P.HEAD_K + (ny - ey))
    P.paste_rot(fr, heads[expr], anchor, (nx, ny), 0)
    return np.asarray(fr.convert("RGB")).astype(float)


def noise(rng, n=18):
    g = rng.normal(0, 1, (n, n)).astype(np.float32)
    return np.asarray(Image.fromarray(g, "F").resize((1080, 1080), Image.BICUBIC))


def boil(img, rng):
    dx, dy = noise(rng) * BOIL, noise(rng) * BOIL
    yy, xx = np.mgrid[0:1080, 0:1080].astype(np.float32)
    x, y = np.clip(xx + dx, 0, 1078), np.clip(yy + dy, 0, 1078)
    x0, y0 = x.astype(int), y.astype(int); fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    a, b, c, d = img[y0, x0], img[y0, x0 + 1], img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return Image.fromarray((a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy).astype(np.uint8))


def camera(im, z, dy):
    w = 1080 / z
    cx, cy = FOCUS[0], min(max(FOCUS[1] + dy, w / 2), 1080 - w / 2)    # keep the crop inside the frame
    return im.crop((cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2)).resize((1080, 1080), Image.LANCZOS)


def main(body_path, head_path, out):
    parts = P.build(body_path, head_path)
    # build() erased the hand for the puppet; reload an un-erased forearm+hand region for the still
    sheet = P.cutout(Image.open(body_path)).crop((0, 0, 260, 430))
    keep = P.poly_mask(sheet.size, P.HAND_ERASE)
    arm = Image.new("RGBA", sheet.size); arm.paste(sheet, mask=keep)
    parts = (parts[0], P.up(arm, P.S), parts[2], parts[3])
    rng = np.random.default_rng(3)
    var = {e: [boil(still(parts, e), rng) for _ in range(3)] for e in ("neutral", "surprised")}
    tmp = tempfile.mkdtemp()
    for i in range(135):
        t = i / 30
        hit = t >= 2.3
        k = P.ease((t - 2.3) / 0.12) - P.ease((t - 2.45) / 0.6) if hit else 0
        z = 1.0 + 0.10 * (t / 4.5) + 0.05 * k
        frame = var["surprised" if hit else "neutral"][(i // 3) % 3]
        camera(frame, z, -10 * k).save(f"{tmp}/{i:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", f"{tmp}/%04d.png",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
