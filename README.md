# broll-html

Turn a talking-head video into a finished short: animated cut-paper illustrations over the boring parts, title tags, zoom-in jump cuts, tightened pauses, background music, captions and a thumbnail.

![A 7-second clip from a finished video](docs/demo.gif)

**Left: the video as recorded. Right: the same moment, finished.**

![Before and after](docs/before-after.jpg)

**The illustrations are drawn for each video, from what you say.** These four come from a video about a cat who jumped into a sales pitch:

![Four illustration frames](docs/broll-frames.jpg)

**Each video also gets a thumbnail:**

![Thumbnail](docs/thumbnail.jpg)

Built by Cam Houser ([camhouser.com](https://camhouser.com)) with Claude Code. Free to use (MIT license).

## The easy way: let Claude do it

**Requires a paid Claude plan (Pro or higher).** Claude Code is not on the free plan.

You do not need to know how to code, and you do not need to open the Terminal. The tools run on your Mac, but Claude runs them for you: the **Code** tab in the Claude desktop app is Claude Code in a normal window. You chat; Claude installs the tools, runs them, and shows you the result. (If you already use Claude Code in the Terminal, that works the same way.)

1. Install the Claude desktop app from [claude.ai/download](https://claude.ai/download), sign in with your paid plan, and open the **Code** tab.
2. Paste this:
   > Set up https://github.com/cameronha/broll-html on my Mac. Follow the README, install everything it needs, and copy skill/SKILL.md into my Claude skills. Ask me before anything that costs money.
3. Record a video of yourself talking. Landscape or square both work (the result is cropped to square), 30 seconds to 2 minutes, with you in the middle of the frame. Phone videos shot upright (portrait) do not work yet.
4. Tell Claude where the file is and say: *"Give this video the talking-head b-roll treatment."*
5. Watch the first version, then say what to change in plain words ("the music is too loud", "cut the part where I stumble", "make that drawing show a calendar"). Each change takes a few minutes.

The first setup takes about 30 minutes, mostly downloads. The skill file was written for Cam's videos (his cartoon face, his music); Claude will ask you about yours.

**Can I just paste this link into ChatGPT or claude.ai chat instead?** A chat can read this page and walk you through it, but it cannot run anything on your computer. You would type each command into the Terminal app yourself and paste the errors back. It works, slowly. Claude Code does those steps for you.

## For developers

Everything is code. B-roll scenes are SVG files written by small Python scripts, rendered frame by frame in a headless browser, then composited onto the footage with ffmpeg. One JSON file per video holds every edit decision, so a new rev is one command. Expect to read code.

### What you need

macOS was the only tested platform.

| Tool | Why | Install |
|---|---|---|
| Python 3.11+ | everything | python.org or Homebrew |
| Pillow, NumPy, Playwright | drawing, image math, rendering | `pip3 install pillow numpy playwright && python3 -m playwright install chromium` |
| ffmpeg | cutting, compositing, audio | `brew install ffmpeg` |
| whisper.cpp + `ggml-small.en.bin` | word timings for cuts and captions | `brew install whisper-cpp`, model from huggingface.co/ggerganov/whisper.cpp |
| Libre Franklin font (Medium, ExtraBold) | titles and captions | Google Fonts; install so the files are in `/Library/Fonts/` |
| A music track | the bed under your voice | any file; set it in the video JSON |

Optional, only to make new cartoon heads: a fal.ai API key and the [paper-collage-animation](https://github.com/cameronha/paper-collage-animation) repo next to this one (`tools/cast/cast.py`, about 5 US cents per image).

### Paths

Video JSON files use three variables, so nothing is tied to one machine:

- `$BROLL_OUT`: where renders and finished videos go (default `~/broll-out`)
- `$BROLL_MEDIA`: where your edited exports and music live (default `~/Downloads`)
- `$BROLL_RAW`: where raw camera takes live (default `~/Downloads`)

Set them in your shell, or put `KEY=path` lines in a `paths.local` file at the repo root (git-ignored):

```
BROLL_OUT=~/videos/out
BROLL_MEDIA=~/videos/exports
BROLL_RAW=~/videos/raw
```

### How a video gets made

0. **Get the code:** `git clone https://github.com/cameronha/broll-html && cd broll-html`. The input is a 1080p landscape or square video; the output is square 1080x1080.
1. **Transcribe** the take for word timings:
   ```
   ffmpeg -i TAKE.mov -ar 16000 -ac 1 audio.wav
   whisper-cli -m ~/.cache/whisper-models/ggml-small.en.bin -f audio.wav -osrt -ml 1 -of words
   ```
2. **Write the scenes.** Copy a `tools/*_scenes.py` file (for example `tools/pinky_scenes.py`) and change the beats. Each function returns one SVG; running the script writes `scenes/PREFIX-*.svg`. Shared parts (heads, speech pills, globes, documents, a cartoon cat) live in the other `*_scenes.py` files and `tools/nov2_parts.py`.
3. **Render** each scene (titles, names starting with `t`, come out as `.mov` with transparency):
   ```
   python3 tools/myvideo_scenes.py
   tools/render1.sh PREFIX $BROLL_OUT/01-myvideo b1 rev1
   ```
4. **Write `videos/myvideo.json`.** Copy `videos/pinky.json`. It sets the source file, the start and end cut, pauses to remove, punch-in zooms, each overlay's window (in source-file seconds), music level and the thumbnail.
5. **Build:**
   ```
   python3 tools/talkinghead.py videos/myvideo.json 1
   ```
   It prints warnings for any face shot shorter than 1.5 s between two b-rolls. Fix those by moving an overlay edge.
6. **Captions:** transcribe the OUTPUT, then
   ```
   python3 tools/captions.py words.srt $BROLL_OUT/01-myvideo/myvideo-rev1.mp4 out-captions.mp4 --mid 28
   ```
   `--mid` is the row (in pixels) the caption text centers on.

### The Claude Code skill

`skill/SKILL.md` is the Claude Code skill that runs this pipeline end to end: it knows the house rules (beat length, framing, music level, trim tightness, caption placement) learned over a dozen videos. Copy it to `~/.claude/skills/talking-head-broll/SKILL.md`, hand Claude a video file, and ask for the treatment. The skill is written for Cam's setup (his face, his cast, his file names); edit those parts for yours.

### Layout

```
svgpieces.py, render.py, render.html   SVG -> rigged pieces -> video frames (Playwright)
tools/talkinghead.py                   the build: cuts, zooms, overlays, voice chain, music, thumbnail
tools/captions.py                      burned-in captions
tools/*_scenes.py                      one b-roll script per video, plus shared parts
tools/head_library.py, tools/cast/     cartoon head library tools
assets/heads/p1..p10                   cartoon heads, 8 expressions each (p10 is Cam)
videos/*.json                          one edit file per video
scenes/                                generated SVGs
STYLE.md                               the cut-paper look
skill/SKILL.md                         the Claude Code skill
```

## Rights

Code: MIT (see LICENSE). The cartoon head `assets/heads/p10` is Cam Houser's likeness and is not covered by the license: do not use it to depict him. The other heads are generated, invented people.
