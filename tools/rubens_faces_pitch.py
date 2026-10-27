"""PRIVATE TEST: pitch scene with heads cut from a Rubens-faces sketch sheet + bodies drawn in its style -> PNG

usage: python3 tools/rubens_faces_pitch.py SHEET.png OUT.png
The sheet is another artist's drawing, so this is a style test only, never published b-roll.
Heads: a polygon cut of the sheet, ochre kept, white made transparent, scaled into place.
Bodies: sketch_head.sk()/hatch() loose pen lines over one flat ochre shape per figure.
"""
import base64, io, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright
import sketch_head as S

S.OCHRE = "#E4AB55"
OCH = (228, 171, 85)
FRANCIS = [(118, 300), (130, 250), (170, 225), (230, 222), (280, 240), (330, 280), (345, 330), (340, 380), (320, 420),
           (300, 470), (290, 512), (230, 522), (170, 512), (130, 470), (108, 430), (112, 360)]
CAPTAIN = [(310, 520), (340, 460), (400, 445), (480, 460), (540, 500), (580, 560), (590, 640), (560, 680), (500, 690),
           (460, 700), (430, 712), (395, 712), (350, 690), (320, 650), (305, 600)]


def cut_head(sheet, poly):
    im = np.asarray(sheet).astype(float)
    lum = im @ [0.3, 0.59, 0.11] / 255
    sat = (im.max(2) - im.min(2)) / 255
    line_a = np.clip((0.62 - lum) / 0.35, 0, 1)
    rgba = np.zeros(im.shape[:2] + (4,))
    rgba[..., :3] = OCH
    rgba[..., 3] = np.where(sat > 0.2, 1, 0)
    ink = np.array([43, 36, 32])
    rgba[..., :3] = rgba[..., :3] * (1 - line_a[..., None]) + ink * line_a[..., None]
    rgba[..., 3] = np.maximum(rgba[..., 3], line_a)
    m = Image.new("L", sheet.size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(2))) / 255
    rgba[..., 3] *= m
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    box = (min(xs) - 4, min(ys) - 4, max(xs) + 4, max(ys) + 4)
    out = Image.fromarray((rgba * [1, 1, 1, 255]).astype(np.uint8), "RGBA").crop(box)
    buf = io.BytesIO(); out.save(buf, "PNG")
    return box, base64.b64encode(buf.getvalue()).decode()


def head_img(box, b64, cx, cy, k, src_c):
    x = cx - (src_c[0] - box[0]) * k
    y = cy - (src_c[1] - box[1]) * k
    return f'<image href="data:image/png;base64,{b64}" x="{x:.1f}" y="{y:.1f}" width="{(box[2] - box[0]) * k:.1f}" height="{(box[3] - box[1]) * k:.1f}"/>'


def blob(pts, dx=-10, dy=8):
    s = S.smooth(pts + pts[:1], 6)
    S.OUT.append(f'<path d="M{" L".join(f"{x:.0f} {y:.0f}" for x, y in s)} Z" fill="{S.OCHRE}" transform="translate({dx} {dy})"/>')


def skeptic():
    blob([(180, 420), (300, 410), (440, 430), (480, 560), (540, 690), (600, 740), (630, 1000), (450, 1030), (190, 1020), (150, 800), (150, 560)])
    sk = S.sk
    # stool
    sk([(215, 770), (205, 1010)], 2.4); sk([(360, 770), (372, 1010)], 2.4); sk([(210, 900), (366, 902)], 1.8)
    # robe: back, chest, lap, the drop from the knee, hem
    sk([(190, 450), (162, 560), (166, 680), (188, 750), (230, 790)], 2.4)
    sk([(420, 455), (446, 540), (452, 640)], 2.4)
    sk([(200, 690), (360, 678), (520, 690), (578, 724)], 2.4)
    sk([(578, 724), (592, 850), (604, 992)], 2.4)
    sk([(604, 992), (520, 1002), (440, 990), (430, 900), (452, 780)], 2.2)
    for k in range(5):
        sk([(470 + k * 26, 760 + k * 4), (476 + k * 26, 870), (466 + k * 28, 990)], 1.4, 1, 3)
    for k in range(3):
        sk([(250 + k * 70, 700), (300 + k * 70, 690 + k * 6), (360 + k * 60, 708)], 1.3, 1, 2)
    # hood bunched around the neck
    sk([(196, 440), (300, 486), (424, 446)], 2.4); sk([(206, 462), (300, 504), (414, 466)], 1.6); sk([(186, 430), (176, 470), (196, 520)], 1.8)
    # arms folded into the sleeves, rope belt
    sk([(192, 470), (186, 540), (204, 596)], 2.2); sk([(424, 470), (446, 530), (444, 584)], 2.2)
    sk([(204, 596), (300, 612), (420, 590)], 2.4); sk([(206, 560), (320, 560), (430, 560)], 2)
    sk([(444, 584), (340, 574), (236, 564), (226, 600), (250, 618)], 2.4)
    sk([(420, 560), (436, 576), (432, 600)], 1.8)
    sk([(190, 650), (320, 652), (452, 640)], 2.2); sk([(194, 660), (320, 662), (452, 650)], 1.4, 1)
    sk([(404, 652), (412, 720), (402, 770)], 1.8); sk([(414, 652), (426, 740)], 1.4, 1)
    # bare feet in sandals
    sk([(452, 996), (520, 1004), (590, 1010), (624, 1016), (612, 1024), (456, 1022)], 2.2)
    sk([(500, 1000), (494, 1022) , (546, 1004), (540, 1022)], 1.4, 1)
    # shadows
    S.hatch([(200, 600), (430, 590), (440, 630), (210, 640)], 35, 7, 1.2)
    S.hatch([(166, 480), (190, 470), (200, 740), (176, 720)], 70, 7, 1.2)
    S.hatch([(470, 770), (560, 760), (590, 990), (520, 1000)], 80, 8, 1.1)
    S.hatch([(216, 800), (360, 800), (366, 1000), (210, 1000)], 20, 10, 1)


def founder():
    blob([(640, 400), (900, 390), (960, 460), (990, 700), (990, 1080), (600, 1080), (630, 760), (600, 600), (440, 560), (430, 360), (590, 370)])
    sk = S.sk
    # cloak over the far shoulder
    sk([(840, 410), (930, 456), (968, 640), (972, 900), (980, 1080)], 2.4)
    sk([(884, 690), (900, 880), (906, 1080)], 2); sk([(920, 520), (940, 760), (946, 1080)], 1.4, 1)
    S.hatch([(906, 470), (956, 520), (972, 1060), (912, 1060), (890, 700)], 75, 8, 1.2)
    # far arm, hand on the hip
    sk([(892, 440), (948, 520), (946, 600), (900, 650)], 2.2); sk([(876, 470), (918, 540), (904, 600)], 1.8)
    sk([(900, 650), (880, 664), (866, 650), (876, 628), (900, 626)], 2)
    # doublet: front, back, waist, buttons, collar
    sk([(690, 420), (664, 520), (656, 620), (664, 712)], 2.4)
    sk([(880, 440), (890, 560), (876, 712)], 2.4)
    sk([(664, 712), (770, 724), (876, 712)], 2.2); sk([(662, 730), (770, 742), (878, 728)], 1.6)
    sk([(744, 420), (738, 560), (732, 710)], 1.8)
    for y in range(450, 700, 40):
        S.OUT.append(f'<circle cx="{742 - (y - 450) * 0.04:.0f}" cy="{y}" r="4" fill="none" stroke="{S.INK}" stroke-width="1.6"/>')
    sk([(706, 398), (752, 430), (830, 404)], 2.2); sk([(700, 404), (690, 426), (728, 446), (760, 436)], 1.8); sk([(830, 404), (850, 424), (800, 444), (760, 436)], 1.8)
    sk([(748, 376), (752, 400)], 1.8, 1); sk([(784, 372), (790, 400)], 1.8, 1)
    # legs to the frame
    sk([(680, 730), (664, 860), (676, 940), (660, 1080)], 2.2); sk([(764, 740), (770, 860), (752, 940), (746, 1080)], 2.2)
    sk([(790, 740), (800, 880), (814, 1080)], 2); sk([(872, 730), (884, 880), (870, 1080)], 2)
    sk([(670, 930), (756, 940)], 1.6); sk([(806, 900), (878, 896)], 1.6)
    S.hatch([(660, 730), (700, 740), (690, 1076), (664, 1076)], 75, 8, 1.1)
    S.hatch([(800, 740), (870, 735), (880, 1076), (816, 1076)], 70, 9, 1)
    # near arm reaches out with the tablet
    sk([(690, 440), (640, 500), (604, 560)], 2.4); sk([(664, 480), (630, 530), (622, 584)], 2)
    sk([(604, 560), (610, 590), (636, 580)], 1.8)
    sk([(606, 560), (580, 530), (560, 508)], 2.2); sk([(624, 580), (592, 540), (574, 518)], 2)
    S.hatch([(664, 490), (690, 444), (700, 470), (640, 560), (622, 584)], 30, 6, 1.1)
    # tablet: a board with a bar chart
    S.OUT.append(f'<path d="M448 372 L566 360 L580 530 L462 542 Z" fill="#FBF8F2"/>')
    sk([(448, 372), (566, 360), (580, 530), (462, 542), (448, 372)], 2.6)
    sk([(458, 384), (556, 374), (568, 518), (470, 528), (458, 384)], 1.4, 1)
    for x, h in [(486, 50), (514, 80), (542, 118)]:
        S.OUT.append(f'<path d="M{x - 9} {520 - (x - 486) * 0.1:.0f} l0 {-h} l18 -2 l0 {h} Z" fill="{S.INK}" opacity="0.85"/>')
    # hand gripping the right edge: fingers over the front, thumb behind
    sk([(560, 504), (552, 486), (560, 474), (580, 476), (594, 494), (590, 516), (574, 524)], 2.2)
    sk([(566, 488), (556, 494)], 1.6, 1); sk([(568, 502), (558, 508)], 1.6, 1); sk([(574, 514), (566, 520)], 1.6, 1)


def main(sheet_path, out):
    sheet = Image.open(sheet_path).convert("RGB")
    S.OUT.append('<path d="M0 1010 Q300 1000 640 1012 T1080 1004" fill="none" stroke="#2B2420" stroke-width="1.6" opacity="0.7"/>')
    skeptic()
    fb, fimg = cut_head(sheet, FRANCIS)
    S.OUT.append(head_img(fb, fimg, 300, 330, 0.62, (225, 370)))
    founder()
    cb, cimg = cut_head(sheet, CAPTAIN)
    S.OUT.append(head_img(cb, cimg, 770, 300, 0.62, (450, 580)))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">'
           f'<rect width="1080" height="1080" fill="{S.PAPER}"/>' + "".join(S.OUT) + "</svg>")
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        pg.set_content(f'<body style="margin:0">{svg}</body>'); pg.screenshot(path="/tmp/rfp.png"); b.close()
    Image.open("/tmp/rfp.png").resize((1080, 1080), Image.LANCZOS).save(out)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:3])
