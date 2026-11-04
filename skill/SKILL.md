---
name: talking-head-broll
description: Turn one of Cam's talking-head videos into a finished post with cut-paper SVG b-roll, cast heads (incl. Cam's likeness), paper-tag titles, color grade, voice EQ/compression, a music bed, tight trims and a split-frame thumbnail in the first frames. Use when Cam gives a talking-head video file and wants b-roll, titles, music, a thumbnail, or "the Leon treatment" / "do it like the last one".
---

# Talking-head b-roll (save points `save-leon-rev22`, `save-report-rev5`, `save-trash-rev3`; updated 2026-10-28)

Repo: `~/Coding/broll-html` (PUBLIC GitHub repo cameronha/broll-html since 2026-11-04, README for outsiders; `git push` after commits and tags). This skill is backed up in the repo as `skill/SKILL.md`: after each edit here, `cp` it there and commit. Eight videos done; each has `videos/NAME.json` + `tools/NAME_scenes.py` (leon, linkedin, investors, slop, stupid, report, trash, repetition). Outputs in `~/Claude-files/broll-html/NN-NAME/`.
Replies to Cam stay in STE (see CLAUDE.md). Titles are short labels, not prose. A clean take takes about 4 minutes to rev1; one with flub cuts about 13.

## If you are not Cam (read this first)

This skill was written for Cam Houser's videos. Most of it (beat length, framing, trims, captions, the 1.5 s face rule) applies to anyone. Change these parts:

- **The speaker's cartoon head.** `CAM_P = 10` in `tools/leon_scenes.py` is Cam's likeness. Never draw the user as p10. Ask the user: use one of the invented heads p1 to p9 for them, or make their own likeness with `tools/cast/cast.py` (needs a fal.ai key and about 40 US cents; ask before spending). Then set `CAM_P` to that number.
- **Music.** Cam's track (fred.mp3) is not in the repo. Ask the user for a music file, or leave `music` out of the video JSON (the build then skips the music bed).
- **Paths.** Write the user's folders into `paths.local` (see README). Ignore the Dropbox notes below.
- **Replies.** The "STE" reply style and "Cam's voice" rules are Cam's own preferences. Talk to the user normally.
- **Color.** Cam grades in Final Cut. For a new user, use `"grade": "fixed"` (or `"none"` if they already graded).
- **First run.** Start with a short clip (30 to 60 s) and two or three beats, so the user sees a result in about 15 minutes.

## Finding Cam's files

Video JSON paths use `$BROLL_RAW`, `$BROLL_MEDIA` and `$BROLL_OUT` (Cam's values are in the git-ignored `paths.local`; `tools/render1.sh` renders one scene). Raw takes are in `~/Downloads`. His Final Cut exports ("NAME - 1080WebShareName.mov") land in the DROPBOX Downloads folder: `~/3 day startup Dropbox/Cam Houser/My Mac (Cameron’s MacBook Air)/Downloads`. He often misspells or shortens names: run `ls -t` on both folders, or `mdfind -onlyin ~ "kMDItemFSName == '*word*'c"`. In zsh, a glob with no match aborts the whole command; never put two globs in one `ls`.

## What is fixed (do not re-ask Cam)

- **Color: Cam grades it himself now.** Start work on the raw take at once (the order does not matter). When his export arrives: set `src` to it, `crop_x` 0 (it comes back square, same framing), `"grade": "none"`, and NO `base` zoom: **the main shot is his file with zero zoom** (Cam, 2026-11-02: "that was my intent all along"). Nov 2026 home set: punch-in `zoom_k` 1.15, `zoom_x` 56, `zoom_y` 43 (Cam, 2026-11-03: 1.15x, the head at the same height as in the main shot; the wall may show). Check it: full length, audio offset 0 against the original (loudness-envelope correlation), and the speech level change. If the change is a flat gain (spread under 1 dB), keep the full VOICE chain; if he did audio work, `"voice": "light"` (loudnorm only). Before his file arrives, the default is the fixed half-strength `GRADE` (`"grade": "fixed"`). The measured `"auto"` look was rejected twice; do not use it unless he asks.
- **Frame (raw takes):** if Cam sits low (big gap above his head), set `"base": [k, y]` (1.15x zoom, crop top at source y; [1.15, 130] on the Oct 2026 home footage) so his head top sits about 100 px from the frame top. Check one frame before the build. Then a center square crop, `crop_x` so the face is centered (390 to 450 on the August couch footage).
- **Voice:** `VOICE` chain (EQ, 3:1 compression, limiter, loudnorm -16 LUFS).
- **Music:** "Fred" (`fred.mp3`, path in any json). Start at 93.9 s (the loud part; the first 33 s are silence). Bass band 62 to 151 Hz. `under_db` 9 is the default; Cam asked for "a little" louder on repetition (6). If he says it is hard to hear, offer a wider band (up to about 300 Hz) before more level.
- **Trim:** start at the first word, end 0.1 to 0.15 s after the last SOUND of the last word (Cam: "end it more tightly after good luck", 2026-10-29; 0.35 s and more was too loose). Find it in the 20 ms loudness list, not the pause list: room noise in the April 2025 studio footage sits at 26 to 33 dB and hides the end. Cut a throat-clear word ("All right") if he asks.
- **Thumbnail:** split frame, spliced in as the first 3 frames. Left: `thumb.face_t` (scan a contact sheet for a smile with open eyes) or `thumb.face_file` (a still Cam gives, even from another video). Right: a b-roll panel that fits a TALL half (map, globe, Rule of 7). One red tag.
- **No framing under 0.6 s** (Cam: a 0.2 s flash before a punch-in looks like an error). `talkinghead.py` snaps zoom edges to b-roll edges and cut joints, and prints `short framing` for any that remain. Overlays also hold their last frame, since a clip can be 1 or 2 frames shorter than its window. After each build, scan every frame of the output (16x16 gray, bright = b-roll, dark = footage; read the real fps, often 23.976) and fix any run under 15 frames. **The face between two b-rolls must show for at least 1.5 s** (Cam, teacher2 rev1: 0.8 s and 1.3 s flashes "should never happen"); `talkinghead.py` prints `SHORT A-ROLL`. Fix: lengthen the earlier beat (re-render with stretched times, not a frozen hold) so the two butt together, or widen the gap.
- **Punch-ins:** 1.15x (Cam, 2026-11-03; 1.2 was "a little too tight", 1.31 to fill the backdrop was rejected). Pick `zoom_y` so the strip above the backdrop keeps its height: zoom_y = top * (1 - 1/k). jump-cut zooms (`zooms`), about one every 10 s, on a new sentence or at a cut joint, never under b-roll. `zoom_y` 60 for the August couch footage, 140 when Cam sits low. Check a frame inside one.
- **B-roll look:** v9 cut paper, boil 100%, brand colors navy #182A46, cream #F6EEDC, red #DE4A30, light blue #8CBDDC. No peach or orange sticky notes.
- **Beats:** about 3 s each (2 s was "too brief"). No beat may sit still for more than about 1.5 s: if the last new element appears early, add a second-half action (a swap, a tilt, a reveal). Boil alone reads as a freeze (Cam, 2026-10-29, the "What AI is" beat). Time each element to the real word. Never overlap cast heads.
- **Cast:** `assets/heads/p1..p10`, 8 expressions each. p10 = Cam (v5, 2026-11-02, Cam picked it): brown hair that sits LOW, SHORT on top and swept back, sides a short SCISSOR cut (not shaved, no fade), a longer narrower face, light hazel eyes, raised open eyebrows, a light-brown beard with a reddish tint, NO grey. Keep his hairline as it is (he said do not change it). Old sets: `43-cast/p10-v1..v4`. Cam dislikes p7 (the old woman); avoid her. Latino-looking for Mexico: p2, p5, p8, p9.

## Steps for a new video

1. **Transcribe:** `ffmpeg -i SRC -ar 16000 -ac 1 audio.wav`, then `whisper-cli -m ~/.cache/whisper-models/ggml-small.en.bin -f audio.wav` with `-otxt` and with `-osrt -ml 1`. Also the PAUSE list (loudness under 30 dB for 0.25 s+, 20 ms frames).
2. **Fix the word times:** Whisper is often 1 to 2 s early when the file starts with silence. Find the first word with the loudness envelope, trim the audio from there, run Whisper again, and add the offset. Confirm start and end by transcribing those short pieces.
3. **Beat list:** about 6 b-roll beats and 3 to 5 titles. Render and iterate; Cam reacts to video, not lists.
4. **Scenes:** `tools/NAME_scenes.py` imports the parts it needs. Useful ones: `leon_scenes` (`root`, `title_root`, `tag`, `check`, `robot`, `map_scene`, `across`, `talk`, `workshop`), `linkedin_scenes` (`rig`, `g`, `sheet`, `building`, `export`, `dump`), `investors_scenes` (`head`, `label`, `bill`, `xmark`), `stupid_scenes` (`bubble`), `slop_scenes` (`button`, `inbox`), `report_scenes` (`regions()` globe that lights countries up as he names them and spins, `report` booklet, `centered`), `trash_scenes` (`heart`, bin, bag, name badge), `repetition_scenes` (`pill` speech bubble, scrolling `feed`). Earlier renders can be reused as files (the Austin to León map is `45-leon/beat0-rev25.mp4`).
5. **Render:** `python3 svgpieces.py scenes/X.svg RIG rig && python3 render.py RIG OUT.mp4` (titles come out as alpha `.mov`). 2 or 3 at a time, in the background, retry once. Make a contact strip and look at it.
6. **Settings + finish:** write `videos/NAME.json` (overlays in ORIGINAL footage time), run `python3 tools/talkinghead.py videos/NAME.json REV`. Transcribe the output, check a frame strip, `open -a "QuickTime Player"` the video and `open` the thumbnail.
7. **Save:** commit after each rev; after Cam approves, tag `save-NAME-revN`. Add one line to memory `project-broll-html.md`.

## Captions and title placement

- **Captions:** burn them in after the build: `python3 tools/captions.py WORDS.srt OUT.mp4 OUT-captions.mp4` (Whisper `-osrt -ml 1` of the OUTPUT). Half size, centered in the strip above the backdrop: `--mid Y` (the strip middle; 28 on the Nov 2026 home footage, painting top at y 57). They must not overhang the backdrop (Cam, 2026-11-03). Deliver the `-captions` file.
- **Titles stay off the subject:** before the first build, look at a frame for anything that the titles would cover (a pet, a prop, hands). Move the tags to the clear side (see `rtag` in `tools/tools_scenes.py`, flush right).

## Gotchas

- **Slow or failed renders:** check `ps -Ao pcpu,comm -r | head`. A runaway Chrome tab in Cam's browser once took a full core for hours (do not close it; tell him). If `svgpieces` stops early, the rig dir has pieces but no index, and `render.py` fails with "Failed to fetch": delete the dir and cut again. macOS has no `timeout` command.
- **Whisper invents words** ("All right") at the start of a short clip. To check a cut, match the loudness shape of the output against the source.
- **Small places on a map:** add a pin on the active one (Guatemala next to gold Belize read as one shape).
- **Two background jobs that both `git commit`:** the second one fails with "nothing to commit". The build itself is fine.
- A transform on a rigged or cut group (even translate) clips or drops the piece; no inner `<g transform>` wrappers. Transforms on single elements are fine. Mirror heads by flipping pixels.
- zsh: write `${G}[b]`, never `$G[b]`. Parse volumedetect with `mean_volume: (..) dB`.
- Upload: files over 10 MB cannot go through the browser tool. Cam drags the file in himself.
- LinkedIn post copy: use the `cam-voice-print-march-2026-writer` skill; repeat the video's ask in the text; tags as real @mentions.

## New cast heads (costs money: about 5 US cents per image, 40 cents per expression set)

`python3 tools/cast/cast.py new N "description"` or `likeness N REF.png "look"`, then `edit` for one change at a time, then `expr N`, then `python3 tools/head_library.py N ~/Claude-files/broll-html/43-cast assets/heads`. Show a comparison sheet before the expression set. `head_library.py` now cleans the outline (drops orange hoodie blends at the rim, smooths the beard edge, removes stray dots). Scene SVGs EMBED the head PNGs: after a re-cut, run the `*_scenes.py` script again before you render. Keep the old set (`pN-v1`) before you overwrite.
