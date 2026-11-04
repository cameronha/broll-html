"""Make cast heads with the image model (fal nano-banana, about $0.05 per image; keys in ~/.config/keys/.env).

usage:
  python3 tools/cast/cast.py new N "a Mexican man in his 30s with short black hair..."   -> OUT/cast-N.png
  python3 tools/cast/cast.py likeness N REF.png "long face, high forehead, ..."          -> OUT/cast-N.png  (a real person)
  python3 tools/cast/cast.py edit IN.png OUT.png "make the eyes slightly narrower ..."    (change one thing, keep the rest)
  python3 tools/cast/cast.py expr N                                                      -> OUT/pN-{7 expressions}.png
then: python3 tools/head_library.py N OUT assets/heads   (cuts the 8 heads + anchors.json)

The neutral head (cast-N.png) is also copied to pN-neutral.png. Every prompt is built and checked BEFORE the paid call:
an edit that fails its check must not spend money (2026-10-27: a failed patch once ran the old prompt anyway).
Lessons: heads must stay where the template head is (else head_library cannot cut them); "Must not resemble any real
person" is for invented people only; say the beard color in words (Cam: brown with a reddish tint, never grey).
"""
import base64, os, shutil, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.expanduser("~/Coding/paper-collage-animation"))
os.environ["BROLL_BACKEND"] = "fal"
import stylize as G

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get("BROLL_OUT", os.path.expanduser("~/broll-out")), "43-cast")
EXPR = {
    "happy": "a warm, closed-mouth smile, relaxed eyes, cheeks lifted",
    "excited": "an open-mouth smile showing teeth, eyebrows raised, eyes wide and bright",
    "skeptical": "strong disbelief: one eyebrow raised HIGH, the other pulled down LOW, eyes narrowed, mouth pulled tight to one side in a doubtful smirk",
    "confused": "eyebrows pulled together and up in the middle, head slightly tilted, mouth slightly open and crooked",
    "tired": "heavy drooping eyelids half closed, eyebrows low, mouth slack and flat",
    "worried": "eyebrows raised and pulled together, eyes wide, lips pressed tight, a tense jaw",
    "surprised": "eyebrows high, eyes wide open, mouth open in a small round O",
}
STYLE = ("Edit the FIRST image. Keep the body, clothes, pose, background and floor exactly as they are. Replace ONLY the "
         "cartoon head (face, hair, ears) with the head of {who}. Draw the new head exactly in the style of the two faces in the "
         "SECOND image: flat color shapes with no outlines, two or three flat skin tones for light and shadow, hair as solid shapes, "
         "realistic Rubens-like proportions and features. Make the head the same size relative to the body as the heads in the second "
         "image. Three-quarter view facing toward the LEFT edge of the image. Calm neutral expression, mouth closed, eyes open. "
         "Small drawn eyes with flat shapes, NOT the large white cartoon eyes of the first image. The new head must be the SAME SIZE as "
         "the cartoon head it replaces, no larger, in the SAME PLACE. {extra}Do not change anything below the neck. No text.")


def img(p):
    return {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(open(p, "rb").read()).decode()}}


def call(parts, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    G._call_fal(parts, out); print("wrote", out)


def new(n, desc):
    p = STYLE.format(who=desc, extra="Weathered and specific, not idealized: real wrinkles and skin texture shapes. "
                                     "Must not resemble any real or famous person. ")
    assert desc in p
    call([{"text": p}, img(f"{HERE}/template.png"), img(f"{HERE}/style.png")], f"{OUT}/cast-{n}.png")
    shutil.copy(f"{OUT}/cast-{n}.png", f"{OUT}/p{n}-neutral.png")


def likeness(n, ref, look):
    p = STYLE.format(who="the man in the THIRD image (photos of the same man)",
                     extra=f"Make him clearly recognizable as that man. {look} A stylized likeness in the flat style, not a photo copy. ")
    assert look in p and "Must not resemble" not in p
    call([{"text": p}, img(f"{HERE}/template.png"), img(f"{HERE}/style.png"), img(ref)], f"{OUT}/cast-{n}.png")
    shutil.copy(f"{OUT}/cast-{n}.png", f"{OUT}/p{n}-neutral.png")


def edit(src, out, change):
    p = (f"Edit this image. Change ONLY this: {change} Keep everything else exactly the same: the face, hair, beard, colors, "
         "flat style, head size and head position, the body and the background. No text.")
    call([{"text": p}, img(src)], out)


def expr(n):
    src = f"{OUT}/p{n}-neutral.png"
    def one(e):
        p = ("Edit this image. Keep EVERYTHING identical: the head shape, size, angle and position, the hair, the ears, the skin "
             "tones, the flat color technique, the body and the background. Change ONLY the facial expression to: " + EXPR[e] +
             ". Make the expression clear and readable at a small size. No text.")
        call([{"text": p}, img(src)], f"{OUT}/p{n}-{e}.png")
    with ThreadPoolExecutor(7) as ex:
        list(ex.map(one, EXPR))


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"new": new, "likeness": likeness, "edit": edit, "expr": expr}[cmd](*a)
