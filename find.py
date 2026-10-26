"""Search Openverse (free, no key) and download candidate photos.

usage: python3 find.py "query[;query2;...]" OUTDIR [N] [category]
  several ;-separated queries are merged (round-robin, de-duplicated)
  category: photograph | illustration | digitized_artwork (Openverse filter)
            wikimedia  (search Wikimedia Commons files instead; try "PSF <thing>" for
                        Pearson Scott Foresman public-domain line drawings on white)
Writes OUTDIR/cand-01.jpg ... and OUTDIR/sheet.jpg (numbered contact sheet).
"""
import io, json, os, ssl, sys, urllib.parse, urllib.request

import certifi
from PIL import Image, ImageDraw

CTX = ssl.create_default_context(cafile=certifi.where())
UA = {"User-Agent": "broll-html/0.1 (personal B-roll experiment)"}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
        return r.read()


def search(query, n, category=None):
    p = {"q": query, "page_size": n * 2, "mature": "false"}
    if category:
        p["category"] = category
    q = urllib.parse.urlencode(p)
    data = json.loads(get(f"https://api.openverse.org/v1/images/?{q}"))
    return data.get("results", [])


def search_wikimedia(query, n):
    import time; time.sleep(1.5)            # Commons rate-limits bursts (HTTP 429)
    p = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
         "gsrsearch": query + " filetype:bitmap|drawing", "gsrlimit": n * 2,
         "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 1400}
    data = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0))
    return [{"url": pg["imageinfo"][0].get("thumburl") or pg["imageinfo"][0]["url"],
             "title": pg["title"]} for pg in pages if pg.get("imageinfo")]


def main():
    query, out = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    category = sys.argv[4] if len(sys.argv) > 4 else None
    os.makedirs(out, exist_ok=True)
    thumbs = []
    lists = [search_wikimedia(q.strip(), n) if category == "wikimedia" else search(q.strip(), n, category)
             for q in query.split(";")]
    results, seen = [], set()
    for row in zip(*[l + [None] * (n * 2 - len(l)) for l in lists]):
        for item in row:
            if item and item["url"] not in seen:
                seen.add(item["url"]); results.append(item)
    for item in results:
        if len(thumbs) >= n:
            break
        try:
            im = Image.open(io.BytesIO(get(item["url"])))
            if im.mode in ("RGBA", "LA", "P"):              # clip art: flatten onto white
                im = im.convert("RGBA")
                bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); im = bg
            im = im.convert("RGB")
        except Exception:
            continue
        if min(im.size) < 300:
            continue
        k = len(thumbs) + 1
        im.save(os.path.join(out, f"cand-{k:02d}.jpg"), quality=92)
        thumbs.append(im)
        print(f"cand-{k:02d}  {im.size[0]}x{im.size[1]}  {item.get('title', '')[:60]}")

    # contact sheet, 4 across, 300px cells
    cell, cols = 300, 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cell * cols, cell * max(rows, 1)), "white")
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(thumbs):
        t = im.copy()
        t.thumbnail((cell - 8, cell - 8))
        x, y = (i % cols) * cell + 4, (i // cols) * cell + 4
        sheet.paste(t, (x, y))
        d.rectangle([x, y, x + 34, y + 22], fill="black")
        d.text((x + 6, y + 5), f"{i + 1:02d}", fill="white")
    sheet.save(os.path.join(out, "sheet.jpg"), quality=80)


if __name__ == "__main__":
    main()
