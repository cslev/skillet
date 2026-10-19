#!/usr/bin/env python3
"""Render a Lucide icon (https://lucide.dev, ISC licence) to a transparent, recoloured PNG.

Usage:
    python3 icon_to_png.py NAME_OR_SVG --color F5A400 --out icon.png [--stroke 1.5]

NAME_OR_SVG is a Lucide icon name (e.g. "workflow", "eye", "shield-check"; browse
https://lucide.dev/icons) fetched from GitHub, or a path to a local SVG.

Needs: network access (for names), LibreOffice (`soffice`) and Pillow. ImageMagick's
built-in SVG renderer silently produces blank images for these icons, so LibreOffice
is used instead: it renders black-on-white, and the brightness becomes the alpha channel.
Exits non-zero with a message if a dependency is missing, so the caller can skip icons.
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

URL = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{}.svg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("icon")
    ap.add_argument("--color", required=True, help="hex colour, e.g. F5A400")
    ap.add_argument("--out", required=True)
    ap.add_argument("--stroke", default="1.5", help="stroke width on the 24-unit grid (Lucide default 2)")
    args = ap.parse_args()

    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit("icon_to_png.py needs Pillow: pip install pillow")
    if not shutil.which("soffice"):
        sys.exit("icon_to_png.py needs LibreOffice (soffice) on PATH")

    path = pathlib.Path(args.icon)
    if path.suffix == ".svg" and path.exists():
        svg = path.read_text()
    else:
        try:
            svg = urllib.request.urlopen(URL.format(args.icon), timeout=20).read().decode()
        except Exception as e:
            sys.exit(f"could not fetch Lucide icon '{args.icon}': {e}")

    svg = svg.replace("currentColor", "#000000")
    svg = re.sub(r'width="24"', 'width="960"', svg, count=1)
    svg = re.sub(r'height="24"', 'height="960"', svg, count=1)
    svg = re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{args.stroke}"', svg)

    with tempfile.TemporaryDirectory() as d:
        src = pathlib.Path(d, "icon.svg")
        src.write_text(svg)
        subprocess.run(["soffice", "--headless", "--convert-to", "png", "--outdir", d, str(src)],
                       check=True, capture_output=True, timeout=120)
        gray = Image.open(pathlib.Path(d, "icon.png")).convert("L")

    rgb = tuple(int(args.color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    img = Image.new("RGBA", gray.size, rgb + (0,))
    img.putalpha(ImageOps.invert(gray))
    box = img.getbbox()
    if box is None:
        sys.exit("rendered icon is empty")
    img.crop(box).save(args.out)
    print(args.out)


if __name__ == "__main__":
    main()
