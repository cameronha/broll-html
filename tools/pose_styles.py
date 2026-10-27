"""Pose sheet: the pitching founder in six postures, from stiff to exaggerated
-> ~/Claude-files/broll-html/30-poses/poses-sheet.jpg

usage: python3 tools/pose_styles.py
Face, hands, clothes and pen stay fixed; only posture changes. The body is split at the hip: the legs
stay planted, the upper body rotates about the hip (bend), the head tilts about the neck, and the whole
figure shears about the feet (lean). The skeptic would be on the left, so negative x is "toward him".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rubens_scene as R
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/Claude-files/broll-html/30-poses")
HIP = (760, 606)


def clip(cid, y0, y1, body):
    return f'<clipPath id="{cid}"><rect x="0" y="{y0}" width="1080" height="{y1 - y0}"/></clipPath><g clip-path="url(#{cid})">{body}</g>'


def founder(lean=0, bend=0, head=0, arm2="open"):
    _, a2, arm, hd = R.careless_founder()
    if arm2 == "down":
        a2 = R.arm_down("far")
    body = R.body("jacket")
    upper = clip("up", 0, 612, body) + a2 + arm + f'<g transform="rotate({head} 746 340)">{hd}</g>'
    fig = clip("lo", 604, 1080, body) + f'<g transform="rotate({bend} {HIP[0]} {HIP[1]})">{upper}</g>'
    return f'<g transform="translate(0 962) skewX({lean}) translate(0 -962)">{fig}</g>'


POSES = [("1  Stiff (now)", dict()),
         ("2  Slight lean in", dict(lean=5, bend=-3, head=-4)),
         ("3  Strong lean in", dict(lean=9, bend=-8, head=-8)),
         ("4  Cartoon lunge", dict(lean=14, bend=-14, head=-14)),
         ("5  Lean back, proud", dict(lean=-6, bend=8, head=10)),
         ("6  Hip shift, casual", dict(lean=-2, bend=5, head=-9, arm2="down"))]


def cell(kw):
    head = R.root("poses")[0].replace('width="1080" height="1080" viewBox="0 0 1080 1080"', 'width="600" height="640" viewBox="100 50 920 981"')
    return head + R.group("f", founder(**kw)) + "</svg>"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 600, "height": 640}, device_scale_factor=1.0)
        for i, (_, kw) in enumerate(POSES):
            pg.set_content(f'<body style="margin:0;background:{R.BG}">{cell(kw)}</body>')
            pg.screenshot(path=f"{OUT}/pose-{i + 1}.png")
        b.close()
    W, H = 600, 640
    sheet = Image.new("RGB", (3 * W + 20, 2 * H + 10), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    for i, (label, _) in enumerate(POSES):
        x, y = (i % 3) * (W + 10), (i // 3) * (H + 10)
        sheet.paste(Image.open(f"{OUT}/pose-{i + 1}.png").convert("RGB"), (x, y))
        d.text((x + 14, y + 10), label, fill="black", font=f)
    sheet.save(f"{OUT}/poses-sheet.jpg", quality=88)
    print(f"{OUT}/poses-sheet.jpg")
