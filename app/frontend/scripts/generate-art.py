"""Generate Cue artwork with Nano Banana (Gemini image models).

Reads the API key from ~/.config/gemini/key and never prints it.
Usage: python3 -I nano.py <out_dir>
"""

import base64
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.request

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
KEY = open(os.path.expanduser("~/.config/gemini/key")).read().strip()
MODELS = ["gemini-3-pro-image-preview", "gemini-3.1-flash-image", "gemini-2.5-flash-image"]

CHAR = (
    "the same original cartoon character every time: a young animator character with a round face, "
    "a messy fringe of short dark hair falling over the forehead, large expressive eyes, small "
    "nose, "
    "wearing a loose striped sweater; simple appealing shapes, clearly drawn by hand"
)

JOBS = {
    "hero-lighttable": (
        "16:9",
        "Cinematic photograph, top-down three-quarter view, of an animator's illuminated light "
        "table at night in a dark studio. "
        "Several sheets of thin animation paper with peg holes sit on a metal peg bar; on them "
        "are pencil drawings of "
        + CHAR
        + ", the head turning from facing forward to a three-quarter view to the left across the "
        "sheets, the drawings glowing "
        "and layering through the paper like onion skin. A warm desk lamp makes a pool of light; "
        "a mechanical pencil, a kneaded "
        "eraser and eraser crumbs. Deep rich blacks, warm paper glow, a single hot-pink sticky "
        "note. Shallow depth of field, "
        "35mm film grain. No text, no logos.",
    ),
    "key-start": (
        "16:9",
        "A single clean animation keyframe drawing on white animation paper: "
        + CHAR
        + ", head and shoulders, facing straight "
        "toward the viewer, neutral relaxed expression, eyes looking straight ahead. Confident "
        "graphite pencil line with a few "
        "light blue construction lines underneath, centred, lots of white paper around. Flat scan "
        "of the paper, no shadows, "
        "no text, no frame number.",
    ),
    "inbetween-sheet": (
        "16:9",
        "An animator's inbetween study sheet scanned flat: sixteen small pencil drawings arranged "
        "in a neat 4 by 4 grid on cream "
        "animation paper, showing "
        + CHAR
        + " performing one motion in order: first only the eyes move to the left, then the head "
        "turns slowly to a three-quarter view on the left, then a smile appears near the end. "
        "Light blue col-erase construction "
        "lines, a few red pencil arcs tracing the path of the nose, small handwritten numbers 1 "
        "to 16 in the corner of each cell. "
        "Authentic studio artefact, slightly uneven hand spacing.",
    ),
    "style-ink": (
        "4:5",
        "Expressive sumi ink brush drawing on rough washi paper of "
        + CHAR
        + ", caught mid head-turn to the left, eyes already "
        "looking left, a hint of a smile. Bold wet black strokes, dry-brush texture, one splash "
        "of hot pink ink. Gallery artwork, "
        "generous negative space, no text.",
    ),
    "style-charcoal": (
        "4:5",
        "Charcoal and white chalk drawing on mid-grey toned paper of "
        + CHAR
        + ", three-quarter view turned to the left, smiling, "
        "with faint ghosted earlier positions of the head drawn behind it like motion study "
        "lines. Smudged soft shading, "
        "visible paper tooth, life-drawing studio feel, no text.",
    ),
    "style-pencil": (
        "4:5",
        "Coloured pencil illustration on off-white paper of "
        + CHAR
        + ", head turned to the left with a warm smile, rendered with "
        "layered hatching in hot pink, deep plum and a touch of mint green, loose sketchy outline "
        "left visible. Contemporary "
        "children's book illustrator quality, no text.",
    ),
    "style-gouache": (
        "4:5",
        "Flat gouache painting with visible brush texture of "
        + CHAR
        + ", turning the head to the left and smiling, against a "
        "deep plum background, limited palette of plum, hot pink, cream and black, mid-century "
        "animation background style, "
        "graphic shapes, no text.",
    ),
    "hands-drawing": (
        "4:5",
        "Close-up photograph of an animator's hand drawing with a pencil on animation paper with "
        "peg holes on a glowing light "
        "table, the earlier drawing of "
        + CHAR
        + " showing through the sheet underneath like an onion skin. Dark room, warm light "
        "coming up through the paper, graphite smudges on the side of the hand, shallow depth of "
        "field, film grain, no text.",
    ),
}

EDITS = {
    # generated from key-start so the character stays the same
    "key-end": (
        "key-start",
        "16:9",
        "Redraw this exact same character, same drawing style, same paper and line quality, same "
        "framing and size, as the END "
        "keyframe of a short animation: the head is now turned to a three-quarter view to the "
        "character's left (the viewer's "
        "left), the eyes look to the left, and the character is smiling warmly. Keep everything "
        "else identical. No text.",
    ),
}


def call(model, parts, aspect):
    body = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY},
    )
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.load(r)
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            if "inlineData" in p:
                return base64.b64decode(p["inlineData"]["data"]), p["inlineData"].get(
                    "mimeType", "image/png"
                )
    raise RuntimeError("no image in response: " + json.dumps(d)[:300])


def gen(name, aspect, parts):
    last = None
    for m in MODELS:
        for _attempt in range(2):
            try:
                data, mime = call(m, parts, aspect)
                ext = "png" if "png" in mime else "jpg"
                path = os.path.join(OUT, f"{name}.{ext}")
                open(path, "wb").write(data)
                return f"{name}: ok ({m}, {len(data) // 1024} KB)"
            except Exception as e:  # noqa: BLE001
                last = f"{m}: {str(e)[:200]}"
                time.sleep(3)
    return f"{name}: FAILED {last}"


with cf.ThreadPoolExecutor(4) as ex:
    futs = {ex.submit(gen, n, a, [{"text": p}]): n for n, (a, p) in JOBS.items()}
    for f in cf.as_completed(futs):
        print(f.result(), flush=True)

for name, (src, aspect, prompt) in EDITS.items():
    srcs = [x for x in os.listdir(OUT) if x.startswith(src + ".")]
    if not srcs:
        print(f"{name}: skipped, {src} missing", flush=True)
        continue
    raw = open(os.path.join(OUT, srcs[0]), "rb").read()
    mime = "image/png" if srcs[0].endswith("png") else "image/jpeg"
    print(
        gen(
            name,
            aspect,
            [
                {"inlineData": {"mimeType": mime, "data": base64.b64encode(raw).decode()}},
                {"text": prompt},
            ],
        ),
        flush=True,
    )
