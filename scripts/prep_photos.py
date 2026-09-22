#!/usr/bin/env python3
"""Resize + compress photos into public/photos and write public/photos.json.

Usage:  python3 scripts/prep_photos.py <source_folder> [--append]

--append keeps the existing photos and numbering and adds the new ones on the end.

Drop new originals in any folder, run this, commit, push -> Railway redeploys.
Exact-duplicate files are skipped. EXIF rotation is respected.
"""
import hashlib, json, sys
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "originals")
OUT = Path(__file__).resolve().parent.parent / "public" / "photos"
OUT.mkdir(parents=True, exist_ok=True)

GRID_MAX = 700     # longest edge for grid tiles
FULL_MAX = 1800    # longest edge for lightbox

seen, entries = set(), []
APPEND = "--append" in sys.argv
MANIFEST = OUT.parent / "photos.json"
if APPEND and MANIFEST.exists():
    entries = json.loads(MANIFEST.read_text())
    for e in entries:
        if "md5" in e: seen.add(e["md5"])
files = sorted(p for p in SRC.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic", ".webp"})
for i, p in enumerate(files):
    digest = hashlib.md5(p.read_bytes()).hexdigest()
    if digest in seen:
        print("skip dup", p.name)
        continue
    seen.add(digest)
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    name = f"p{len(entries)+1:02d}"
    w, h = im.size
    for tag, mx in (("grid", GRID_MAX), ("full", FULL_MAX)):
        c = im.copy()
        c.thumbnail((mx, mx), Image.LANCZOS)
        c.save(OUT / f"{name}-{tag}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    entries.append({"id": name, "w": w, "h": h, "md5": digest})
    print("ok", p.name, "->", name, f"{w}x{h}")

MANIFEST.write_text(json.dumps(entries, indent=1))
print(f"\n{len(entries)} photos written to {OUT}")
