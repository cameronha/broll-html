"""B-roll for "trust" (gym story; raw 2026-11-02 15-37-43) -> scenes/tr-*.svg
Times inside each beat are local; windows in videos/trust.json (raw time + 137.80).
b1 gym       a gym; Cam walks to the door; the general manager pops up with a "GM" badge
b2 direct    the manager says "Honestly..."; young members pop in; "Young crowd"
b3 tripods   a phone on a tripod records (REC blinks); "Influencer"; sweat drops on a bench; the wipe spray gets an X
b4 older     Cam among the young members; the manager: "Fair warning"
b5 lists     "Doesn't work" items get X marks, "Good" items get checks; "Probably true"
b6 joined    a member card; "Joined" stamp; Cam happy
b7 connect   Cam and the manager; a line joins them; a heart
b8 ads       the robot pumps out ad cards; a trust meter drops
b9 yours     "Your website" window; "What you do"; a note "One flaw" sticks on
b10 buy      the trust meter rises; a cart; a check
t1 He named / the flaws     t2 Be direct / and honest
"""
import os
from leon_scenes import root, calm, robot, check, CREAM, NAVY, ORANGE, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bubble
from teacher2_scenes import steps, window, lines
from nov2_parts import two, gym, tripod_phone, dumbbell, meter, heart, doc, BLUE, WHITE

MGR = 3            # the general manager


def gym_scene():
    dur = 6.0
    s = root(dur, "1,0,0")
    s += g("gym", gym(400, 860, 600, 420), (0.2, dur + 1), rig(700, 860, 1, 0.4))
    s += g("door", f'<rect x="640" y="700" width="120" height="160" rx="8" fill="{ORANGE}"/>', (3.2, dur + 1))     # the door opens
    s += head(CAM_P, [(1.0, "neutral"), (3.2, "happy")], (250, 1010), 0.55, True, "cam")
    s += steps("arr", lambda x, y: f'<path d="M{x} {y} L{x + 60} {y}" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/><path d="M{x + 60} {y - 22} L{x + 92} {y} L{x + 60} {y + 22}Z" fill="{NAVY}"/>',
               [(380, 640), (450, 640), (520, 640)], 1.6, 3.0, dur, r=lambda x, y: rig(x, y, 2, 0.8))
    s += head(MGR, [(4.7, "happy")], (860, 1040), 0.5, False, "mgr")
    s += pill("gm", 860, 560, "General manager", 46, ORANGE, CREAM, (5.0, dur + 1))
    return s + "</svg>\n"


def direct():
    dur = 4.5
    s = root(dur, "1,0,0")
    s += head(MGR, [(0.05, "neutral"), (1.4, "skeptical")], (250, 1010), 0.75, False, "mgr")
    s += bubble("say", 90, 160, 520, 130, "Honestly...", 66, (0.1, dur + 1), (-1, 1))
    for i, (p, x, y, t) in enumerate(((2, 640, 640, 2.6), (8, 840, 600, 2.9), (5, 950, 900, 3.2), (2, 700, 960, 3.4))):
        s += head(p, [(t, "happy")], (x, y), 0.32, True, f"y{i}")
    s += pill("yc", 800, 220, "Young crowd", 56, NAVY, CREAM, (3.6, dur + 1))
    return s + "</svg>\n"


def tripods():
    dur = 9.1
    s = root(dur, "1,0,0")
    s += g("tri", tripod_phone(260, 360), (0.4, 5.6), rig(260, 780, 2, 0.6))
    for k in range(5):
        s += g(f"rec{k}", f'<circle cx="290" cy="290" r="14" fill="{ORANGE}"/>' + label(200, 210, "REC", 44, ORANGE), (1.2 + 0.8 * k, 1.6 + 0.8 * k))
    s += head(2, [(0.8, "happy"), (3.0, "excited")], (720, 1010), 0.6, True, "inf")
    s += steps("db", lambda x, y: dumbbell(x, y, 1.0), [(720, 520), (720, 470), (720, 520), (720, 470), (720, 520)], 1.0, 3.4, 5.6, r=lambda x, y: rig(x, y, 2, 0.8))
    s += pill("infl", 760, 170, "Influencer", 60, ORANGE, CREAM, (4.4, 5.6))
    bench = f'<rect x="200" y="640" width="680" height="70" rx="20" fill="{NAVY}"/><rect x="260" y="710" width="40" height="160" fill="{NAVY}"/><rect x="780" y="710" width="40" height="160" fill="{NAVY}"/>'
    s += g("bench", bench, (5.6, dur + 1), rig(540, 870, 1, 0.5))
    for i, (x, t) in enumerate(((330, 5.9), (520, 6.2), (700, 6.5), (430, 6.8))):
        s += g(f"drop{i}", f'<path d="M{x} 520 Q{x - 30} 580 {x} 600 Q{x + 30} 580 {x} 520Z" fill="{BLUE}"/>', (t, dur + 1), rig(x, 600, 6, 1.3))
    spray = f'<rect x="820" y="300" width="110" height="200" rx="18" fill="{WHITE}"/><rect x="845" y="250" width="60" height="60" fill="{GREY}"/><rect x="890" y="250" width="70" height="24" fill="{GREY}"/>'
    s += g("spray", spray + label(832, 420, "Wipe", 36, NAVY), (6.9, dur + 1), rig(875, 500, 3, 0.9))
    s += xmark("x", 875, 380, (7.4, dur + 1), 90)
    return s + "</svg>\n"


def older():
    dur = 5.1
    s = root(dur, "1,0,0")
    for i, (p, x, t) in enumerate(((2, 560, 0.1), (8, 760, 0.25), (5, 960, 0.4))):
        s += head(p, [(t, "happy")], (x, 1010), 0.34, True, f"y{i}")
    s += head(CAM_P, [(0.05, "neutral"), (1.4, "skeptical"), (3.0, "happy")], (260, 1010), 0.65, False, "cam")
    s += pill("old", 270, 380, "A bit older", 54, NAVY, CREAM, (1.2, dur + 1))
    s += g("warn", f'<path d="M780 170 L940 450 L620 450Z" fill="{GOLD}" stroke="{NAVY}" stroke-width="12" stroke-linejoin="round"/>'
                   + centered(780, 420, "!", 150, NAVY), (3.9, dur + 1), rig(780, 450, 5, 1.2))
    s += pill("fair", 780, 540, "Fair warning", 50, ORANGE, CREAM, (4.3, dur + 1))
    return s + "</svg>\n"


def lists():
    dur = 5.5
    s = root(dur, "1,0,0")
    s += g("bad", f'<rect x="290" y="110" width="500" height="360" rx="20" fill="{WHITE}"/>' + label(330, 180, "Doesn't work", 50, ORANGE), (0.05, dur + 1), rig(540, 470, 1, 0.5))
    s += g("good", f'<rect x="290" y="520" width="500" height="400" rx="20" fill="{WHITE}"/>' + label(330, 590, "Good", 54, NAVY), (1.8, dur + 1), rig(540, 920, 1, 0.5))
    for i, t in enumerate((0.4, 0.8, 1.2)):
        s += g(f"bl{i}", f'<rect x="330" y="{230 + 70 * i}" width="{300 - 50 * (i % 2)}" height="18" rx="9" fill="{GREY}"/>', (t, dur + 1))
        s += xmark(f"bx{i}", 710, 238 + 70 * i, (t + 0.2, dur + 1), 22)
    for i, t in enumerate((2.2, 2.9, 3.6, 4.2)):
        s += g(f"gl{i}", f'<rect x="330" y="{650 + 66 * i}" width="{300 - 50 * (i % 2)}" height="18" rx="9" fill="{GREY}"/>', (t, dur + 1))
        s += check(f"gk{i}", 680, 630 + 66 * i, t + 0.2, dur, 54)
    s += pill("true", 820, 960, "Probably true", 46, NAVY, CREAM, (4.8, dur + 1))
    return s + "</svg>\n"


def joined():
    dur = 2.9
    s = root(dur, "1,0,0")
    s += g("card", f'<rect x="440" y="300" width="560" height="340" rx="26" fill="{NAVY}"/><rect x="440" y="370" width="560" height="50" fill="{ORANGE}"/>'
                   + label(480, 520, "GYM member", 54, CREAM) + f'<rect x="480" y="560" width="300" height="18" rx="9" fill="{GREY}"/>', (0.05, dur + 1), rig(720, 640, 3, 0.9))
    s += head(CAM_P, [(0.05, "neutral"), (1.3, "excited")], (240, 1010), 0.7, False, "cam")
    s += g("stamp", f'<rect x="560" y="660" width="380" height="130" rx="18" fill="none" stroke="{ORANGE}" stroke-width="14" transform="rotate(-8 750 725)"/>'
                    + f'<text x="610" y="755" font-family="Libre Franklin" font-weight="800" font-size="76" fill="{ORANGE}" transform="rotate(-8 750 725)">JOINED</text>',
           (1.2, dur + 1), rig(750, 790, 4, 1.2))
    return s + "</svg>\n"


def connect():
    dur = 3.0
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "neutral"), (1.4, "happy")], (260, 1010), 0.62, False, "cam")
    s += head(MGR, [(0.05, "neutral"), (1.4, "happy")], (820, 1010), 0.62, True, "mgr")
    for i in range(5):
        s += g(f"d{i}", f'<rect x="{390 + 60 * i}" y="560" width="36" height="14" rx="7" fill="{NAVY}"/>', (0.5 + 0.15 * i, dur + 1))
    s += g("heart", heart(540, 400, 1.6), (2.0, dur + 1), rig(540, 440, 6, 1.4))
    s += pill("tr", 540, 170, "Connection", 56, NAVY, CREAM, (1.4, dur + 1))
    return s + "</svg>\n"


def ads():
    dur = 9.8
    s = root(dur, "1,0,0")
    s += g("bot", robot(220, 620, 4.0), (0.05, dur + 1), rig(220, 710, 6, 1.4))
    s += pill("ai", 260, 170, "AI marketing", 56, NAVY, CREAM, (0.2, dur + 1))
    words = ("Best ever!", "#1 choice", "Amazing!", "Guaranteed", "Life-changing", "Act now!")
    for i, w in enumerate(words):                               # ad cards pile up
        t = 0.6 + 0.7 * i
        x, y = 420 + 60 * (i % 2), 280 + 95 * i
        s += g(f"ad{i}", f'<rect x="{x}" y="{y}" width="360" height="86" rx="14" fill="{[ORANGE, WHITE][i % 2]}" transform="rotate({[-3, 2, -2, 3, -1, 2][i]} {x + 180} {y + 43})"/>'
                         + label(x + 24, y + 58, w, 44, [CREAM, NAVY][i % 2]), (t, dur + 1), rig(x + 180, y + 86, 3, 1.0))
    s += meter("tm", 920, 300, 520, [0.6, 0.4, 0.25, 0.1], [0.3, 5.8, 7.0, 8.9], dur, ORANGE, "Trust")
    return s + "</svg>\n"


def yours():
    dur = 7.3
    s = root(dur, "1,0,0")
    s += g("win", window(320, 130, 680, 560, "Your website") + lines(370, 240, 9, 520, 44), (0.3, dur + 1), rig(660, 690, 1, 0.5))
    s += head(CAM_P, [(0.05, "neutral"), (3.0, "happy")], (170, 1010), 0.55, False, "cam")
    s += pill("wy", 660, 820, "What you do", 56, NAVY, CREAM, (2.4, dur + 1))
    s += g("note", f'<rect x="640" y="300" width="320" height="260" fill="{GOLD}" transform="rotate(5 800 430)"/>'
                   + centered(800, 420, "One flaw", 64, NAVY), (5.4, dur + 1), rig(800, 300, 4, 1.0))
    s += g("note2", f'<rect x="380" y="380" width="260" height="200" fill="{GOLD}" transform="rotate(-4 510 480)"/>'
                    + centered(510, 495, "or two", 54, NAVY), (6.4, dur + 1), rig(510, 380, 4, 1.0))
    return s + "</svg>\n"


def buy():
    dur = 5.4
    s = root(dur, "1,0,0")
    s += meter("tm", 160, 220, 560, [0.1, 0.35, 0.6, 0.9], [0.1, 1.2, 1.9, 2.6], dur, NAVY, "Trust")
    cart = (f'<path d="M500 420 L560 420 L620 700 L900 700 L950 480 L590 480" stroke="{NAVY}" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="650" cy="770" r="34" fill="{NAVY}"/><circle cx="870" cy="770" r="34" fill="{NAVY}"/>')
    s += g("cart", cart, (3.5, dur + 1), rig(760, 800, 3, 1.0))
    s += g("box", f'<rect x="650" y="540" width="120" height="120" rx="10" fill="{ORANGE}"/><rect x="790" y="560" width="110" height="100" rx="10" fill="{GOLD}"/>', (4.0, dur + 1),
           rig(760, 660, 4, 1.2))
    s += check("ok", 880, 300, 4.6, dur, 100)
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("He named", "the flaws", 3.0, 0.8)), ("t2", lambda: two("Be direct", "and honest", 2.3, 0.7)),
                 ("b1", gym_scene), ("b2", direct), ("b3", tripods), ("b4", older), ("b5", lists), ("b6", joined), ("b7", connect),
                 ("b8", ads), ("b9", yours), ("b10", buy)):
        open(os.path.join(HERE, f"scenes/tr-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/tr-{n}.svg")
