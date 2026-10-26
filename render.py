"""Record render.html to a square mp4 with your installed Chrome (headless).

usage: python3 render.py SCENEDIR OUT.mp4   (SCENEDIR holds manifest.json)
"""
import base64, os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    work, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    frames = tempfile.mkdtemp(prefix="broll-html-")
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
        page = b.new_page(viewport={"width": 1080, "height": 1080})
        page.goto("file://" + os.path.join(HERE, "render.html"))
        n = page.evaluate("b => setup(b)", "file://" + work)
        for f in range(n):
            data = page.evaluate("f => renderAt(f)", f)
            with open(os.path.join(frames, f"{f:04d}.png"), "wb") as fh:
                fh.write(base64.b64decode(data.split(",", 1)[1]))
        b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24",
                    "-i", os.path.join(frames, "%04d.png"), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
    print(out)


if __name__ == "__main__":
    main()
