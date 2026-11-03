"""B-roll for "when to sell with video" (raw 2026-11-02 15-31-15) -> scenes/sv-*.svg
Times inside each beat are local; windows in videos/sell.json (raw time + 255.72).
b1 asked     Cam at a startup program; founders pop; one asks "When do I send a video?"; a video card; a sales funnel
b2 effort    one customer; a video card flies to them; a clock spins, a weight, a light bulb
b3 story     the robot snips a film strip ("Easier"); Story, Message, Content cards stack; "Really important"
b4 profile   a customer profile card fills: Who, Into, Type, Fit
b5 research  a magnifier scans pages; a video goes out; a clock spins long
b6 message   a chat: typing dots, then "Quick question?"; an interest meter rises; the profile fills
b7 stage     a pipeline: Message, Talk, Video; the marker moves along; a camera records
b8 receptive the video reaches the customer; neutral, happy, excited; "Sold"
t1 Not at the / beginning (used twice)
"""
import os
from leon_scenes import root, calm, robot, check, CREAM, NAVY, ORANGE, HERE, CAM_P
from linkedin_scenes import rig, g, GREY
from investors_scenes import head, label, xmark, GOLD
from repetition_scenes import pill
from report_scenes import centered
from stupid_scenes import bubble
from teacher2_scenes import steps, lines
from nov2_parts import two, video_card, spin_clock, meter, doc, envelope, BLUE, WHITE


def asked():
    dur = 6.2
    s = root(dur, "1,0,0")
    s += head(CAM_P, [(0.05, "happy")], (220, 1010), 0.7, False, "cam")
    for i, (p, x, t) in enumerate(((2, 560, 0.3), (8, 760, 0.5), (5, 960, 0.7))):
        s += head(p, [(t, "neutral"), (2.4, "confused" if i == 1 else "neutral")], (x, 1010), 0.36, True, f"f{i}")
    s += pill("prog", 300, 170, "Startup program", 54, NAVY, CREAM, (0.9, dur + 1))
    s += bubble("q", 470, 330, 560, 120, "When do I send", 50, (2.6, dur + 1), (1, 1))
    s += g("q2", label(510, 520, "a video?", 50, ORANGE), (3.0, dur + 1), rig(700, 450, 3, 0.8))
    s += g("vid", video_card(80, 330, 260), (4.1, dur + 1), rig(210, 490, 4, 1.0))
    s += g("fun", f'<path d="M640 600 L1000 600 L880 720 L760 720Z" fill="{ORANGE}"/><rect x="790" y="720" width="60" height="70" fill="{ORANGE}"/>'
                  + centered(820, 660, "Sales", 40, CREAM), (5.3, dur + 1), rig(820, 790, 3, 0.9))
    return s + "</svg>\n"


def effort():
    dur = 4.9
    s = root(dur, "1,0,0")
    s += g("spot", f'<path d="M760 60 L560 900 L1000 900Z" fill="{WHITE}" opacity="0.35"/>', (0.05, dur + 1))
    s += head(5, [(0.05, "neutral"), (2.0, "happy")], (780, 1010), 0.6, True, "cust")
    s += steps("vid", lambda x, y: video_card(x, y, 200), [(80, 300), (220, 260), (360, 240), (500, 260)], 0.4, 1.4, dur, r=lambda x, y: rig(x + 100, y + 120, 3, 0.9))
    s += pill("one", 300, 150, "One customer", 52, NAVY, CREAM, (1.4, dur + 1))
    s += spin_clock("clk", 180, 640, 110, 2.8, dur, dur, 8)
    s += g("wt", f'<path d="M330 820 L400 640 L520 640 L590 820Z" fill="{NAVY}"/><circle cx="460" cy="620" r="34" fill="none" stroke="{NAVY}" stroke-width="16"/>'
                 + centered(460, 780, "Effort", 40, CREAM), (3.4, dur + 1), rig(460, 820, 4, 1.1))
    s += g("bulb", f'<circle cx="460" cy="430" r="70" fill="{GOLD}"/><rect x="430" y="490" width="60" height="50" rx="8" fill="{NAVY}"/>', (4.0, dur + 1), rig(460, 540, 5, 1.3))
    return s + "</svg>\n"


def story():
    dur = 7.3
    s = root(dur, "1,0,0")
    strip = f'<rect x="90" y="150" width="900" height="170" rx="10" fill="{NAVY}"/>' + "".join(
        f'<rect x="{110 + 70 * i}" y="160" width="40" height="22" rx="4" fill="{CREAM}"/><rect x="{110 + 70 * i}" y="288" width="40" height="22" rx="4" fill="{CREAM}"/>'
        for i in range(13)) + "".join(f'<rect x="{120 + 220 * i}" y="198" width="190" height="74" rx="6" fill="{[BLUE, GOLD, ORANGE, BLUE][i]}"/>' for i in range(4))
    s += g("strip", strip, (0.05, 2.6), rig(540, 320, 1, 0.5))
    s += steps("bot", lambda x, y: robot(x, y, 2.6), [(200, 440), (420, 420), (640, 440), (860, 420)], 0.3, 2.0, 2.6)
    for i, t0 in enumerate((0.6, 1.2, 1.8)):
        s += g(f"snip{i}", f'<rect x="{318 + 220 * i}" y="140" width="14" height="190" rx="7" fill="{ORANGE}"/>', (t0, 2.6))
    s += pill("easy", 540, 640, "Editing: easier", 60, ORANGE, CREAM, (0.9, 2.6))
    for i, (w, t, c) in enumerate((("Story", 2.8, NAVY), ("Message", 3.5, ORANGE), ("Content", 4.8, NAVY))):
        y = 700 - 190 * i
        s += g(f"card{i}", f'<rect x="250" y="{y}" width="580" height="160" rx="18" fill="{c}" transform="rotate({[-3, 2, -1][i]} 540 {y + 80})"/>'
                           + centered(540, y + 105, w, 76, CREAM), (t, dur + 1), rig(540, y + 160, 2, 0.8))
    s += g("star", f'<path d="M900 240 L930 320 L1015 320 L947 370 L972 450 L900 400 L828 450 L853 370 L785 320 L870 320Z" fill="{GOLD}"/>', (6.1, dur + 1), rig(900, 450, 6, 1.2))
    s += pill("imp", 540, 940, "Really important", 56, GOLD, NAVY, (6.3, dur + 1))
    return s + "</svg>\n"


def profile():
    dur = 6.7
    s = root(dur, "1,0,0")
    s += g("card", f'<rect x="120" y="120" width="840" height="820" rx="24" fill="{WHITE}"/><rect x="120" y="120" width="840" height="90" rx="24" fill="{NAVY}"/>'
                   f'<rect x="120" y="180" width="840" height="30" fill="{NAVY}"/>' + label(160, 185, "Customer profile", 52, CREAM), (0.05, dur + 1), rig(540, 940, 1, 0.5))
    s += head(5, [(0.2, "neutral"), (5.6, "happy")], (290, 560), 0.42, False, "c")
    rows = (("Who they are", 1.5), ("What they're into", 2.9), ("What type", 4.0), ("How they fit", 5.7))
    for i, (w, t) in enumerate(rows):
        y = 300 + 150 * i
        s += g(f"r{i}", label(460, y + 50, w, 46, NAVY) + f'<rect x="460" y="{y + 75}" width="{380 - 60 * (i % 2)}" height="14" rx="7" fill="{GREY}"/>', (t, dur + 1),
               rig(640, y + 90, 2, 0.8))
        s += check(f"k{i}", 860, y + 10, t + 0.3, dur, 64)
    s += pill("res", 540, 1010 - 130, "Research", 50, ORANGE, CREAM, (6.0, dur + 1))
    return s + "</svg>\n"


def research():
    dur = 4.8
    s = root(dur, "1,0,0")
    for i in range(3):
        s += g(f"pg{i}", doc(110 + 40 * i, 140 + 30 * i, 440, 560, None, 11, WHITE, i), (0.05, dur + 1), rig(330 + 40 * i, 700 + 30 * i, 1, 0.5))
    s += steps("mag", lambda x, y: f'<circle cx="{x}" cy="{y}" r="80" fill="{BLUE}" fill-opacity="0.5" stroke="{NAVY}" stroke-width="20"/>'
                                   f'<rect x="{x + 50}" y="{y + 50}" width="30" height="130" rx="15" fill="{NAVY}" transform="rotate(-45 {x + 65} {y + 115})"/>',
               [(300, 320), (460, 360), (320, 480), (480, 540), (360, 640)], 0.1, 1.9, dur, r=lambda x, y: rig(x, y, 3, 1.0))
    s += steps("env", lambda x, y: envelope(x, y, 220), [(640, 600), (740, 480), (820, 380)], 1.9, 2.6, dur, r=lambda x, y: rig(x + 110, y + 70, 4, 1.0))
    s += spin_clock("clk", 860, 760, 120, 3.0, dur, dur, 8, 0, 60)
    s += pill("long", 860, 560, "A long time", 48, ORANGE, CREAM, (4.1, dur + 1))
    return s + "</svg>\n"


def message():
    dur = 5.3
    s = root(dur, "1,0,0")
    for k in range(3):                                            # typing dots
        s += g(f"dots{k}", f'<rect x="100" y="180" width="240" height="110" rx="40" fill="{WHITE}"/>'
                           + "".join(f'<circle cx="{160 + 60 * j}" cy="{235 - (12 if j == k else 0)}" r="16" fill="{NAVY if j == k else GREY}"/>' for j in range(3)),
               (0.3 + 0.35 * k, 0.3 + 0.35 * (k + 1)))
    s += bubble("msg", 100, 160, 560, 120, "Quick question?", 52, (1.4, dur + 1), (-1, 1))
    s += head(5, [(0.05, "neutral"), (2.8, "happy")], (300, 1010), 0.5, False, "c")
    s += meter("int", 640, 300, 520, [0.15, 0.35, 0.6, 0.8], [2.5, 2.8, 3.1, 3.4], dur, ORANGE, "Interest")
    s += g("prof", doc(800, 360, 220, 300, None, 0), (3.7, dur + 1), rig(910, 660, 2, 0.8))
    for i in range(5):
        s += g(f"pl{i}", f'<rect x="820" y="{400 + 48 * i}" width="{170 - 40 * (i % 2)}" height="16" rx="8" fill="{NAVY}"/>', (3.9 + 0.22 * i, dur + 1))
    return s + "</svg>\n"


def stage():
    dur = 3.4
    s = root(dur, "1,0,0")
    s += g("line", f'<rect x="140" y="520" width="800" height="18" rx="9" fill="{NAVY}"/>', (0.05, dur + 1))
    for i, (w, x) in enumerate((("Message", 200), ("Talk", 540), ("Video", 880))):
        s += g(f"s{i}", f'<circle cx="{x}" cy="529" r="44" fill="{[GREY, BLUE, ORANGE][i]}"/>' + centered(x, 660, w, 54, NAVY), (0.05 + 0.15 * i, dur + 1),
               rig(x, 573, 2, 0.8))
    s += steps("mk", lambda x, y: f'<path d="M{x} {y} L{x - 36} {y - 70} L{x + 36} {y - 70}Z" fill="{GOLD}"/>',
               [(200, 470), (370, 470), (540, 470), (710, 470), (880, 470)], 0.4, 2.0, dur, r=lambda x, y: rig(x, y, 3, 1.0))
    cam = (f'<rect x="760" y="140" width="240" height="160" rx="20" fill="{NAVY}"/><circle cx="880" cy="225" r="54" fill="{BLUE}"/>'
           f'<circle cx="880" cy="225" r="26" fill="{NAVY}"/>')
    s += g("cam", cam, (2.3, dur + 1), rig(880, 300, 3, 0.9))
    for k in range(3):
        s += g(f"rec{k}", f'<circle cx="970" cy="170" r="14" fill="{ORANGE}"/>' + label(800, 360, "REC", 44, ORANGE), (2.6 + 0.3 * k, 2.75 + 0.3 * k))
    s += g("recl", f'<circle cx="970" cy="170" r="14" fill="{ORANGE}"/>' + label(800, 360, "REC", 44, ORANGE), (3.2, dur + 1))
    return s + "</svg>\n"


def receptive():
    dur = 6.2
    s = root(dur, "1,0,0")
    s += steps("vid", lambda x, y: video_card(x, y, 240), [(80, 260), (220, 240), (360, 260), (440, 300)], 0.1, 1.0, dur, r=lambda x, y: rig(x + 120, y + 150, 3, 0.9))
    s += head(5, [(0.05, "neutral"), (1.8, "happy"), (4.4, "excited")], (780, 1010), 0.62, True, "cust")
    s += g("ear", "".join(f'<path d="M{560 + 30 * i} {560 - 20 * i} Q{600 + 30 * i} {600} {560 + 30 * i} {640 + 20 * i}" stroke="{GOLD}" stroke-width="12" fill="none" stroke-linecap="round"/>'
                          for i in range(3)), (1.9, dur + 1), rig(600, 640, 6, 1.4))
    s += pill("rec", 760, 160, "Receptive", 56, NAVY, CREAM, (2.2, dur + 1))
    for i, (x, y, t) in enumerate(((180, 720, 4.5), (300, 660, 4.7), (240, 820, 4.9))):
        s += g(f"coin{i}", f'<circle cx="{x}" cy="{y}" r="44" fill="{GOLD}"/>' + label(x - 16, y + 18, "$", 52), (t, dur + 1), rig(x, y + 44, 8, 1.4))
    s += check("sold", 360, 520, 5.2, dur, 90)
    return s + "</svg>\n"


if __name__ == "__main__":
    for n, f in (("t1", lambda: two("Not at the", "beginning", 2.4, 0.9)),
                 ("b1", asked), ("b2", effort), ("b3", story), ("b4", profile), ("b5", research), ("b6", message), ("b7", stage), ("b8", receptive)):
        open(os.path.join(HERE, f"scenes/sv-{n}.svg"), "w").write(calm(f()))
        print(f"wrote scenes/sv-{n}.svg")
