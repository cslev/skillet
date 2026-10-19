#!/usr/bin/env python3
"""Suggest a deck colour template (brand + highlight) from a company logo.

Usage:
    python3 logo_palette.py LOGO.png [--swatch preview.png]

Prints the logo's dominant colours and a proposed template:
  - brand:     the logo's main colour, darkened if needed so white title text on it
               reaches WCAG contrast >= 4.5:1 (used for header band, dividers, big numbers)
  - highlight: a second logo colour that stands out on the brand colour (contrast >= 3:1),
               else a light tint of the brand colour (used for icons on brand slides)
The proposal is a suggestion for the user to approve, never a final choice.
--swatch writes a small preview image of the template (Read it to check before asking).
Needs Pillow. PNG/JPG/GIF/WebP input; SVG is not supported.
"""

import argparse
import colorsys
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("logo_palette.py needs Pillow: pip install pillow")


def luminance(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hls(rgb):
    return colorsys.rgb_to_hls(*(c / 255 for c in rgb))


def from_hls(h, l, s):
    return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))


def hexc(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def dominant(path, n=8):
    img = Image.open(path).convert("RGBA")
    img.thumbnail((240, 240))
    data = getattr(img, "get_flattened_data", img.getdata)()
    px = [p[:3] for p in data if p[3] >= 128]
    px = [p for p in px if min(p) < 235]  # drop near-white background
    if not px:
        sys.exit("no opaque, non-white pixels found in the logo")
    flat = Image.new("RGB", (len(px), 1))
    flat.putdata(px)
    q = flat.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    merged = []  # fold anti-aliasing shades into the nearest bigger colour
    for c, i in counts:
        rgb = tuple(pal[i * 3:i * 3 + 3])
        for m in merged:
            if sum((a - b) ** 2 for a, b in zip(rgb, m[0])) < 40 ** 2:
                m[1] += c / total
                break
        else:
            merged.append([rgb, c / total])
    return [(c, f) for c, f in merged]


def darken_for_white(rgb):
    h, l, s = hls(rgb)
    while contrast(rgb, (255, 255, 255)) < 4.5 and l > 0.05:
        l -= 0.02
        rgb = from_hls(h, l, s)
    return rgb


def hue_dist(a, b):
    d = abs(hls(a)[0] - hls(b)[0]) * 360
    return min(d, 360 - d)


def propose(colours):
    chromatic = [(c, f) for c, f in colours if hls(c)[2] > 0.25 and f >= 0.03]
    base = chromatic[0][0] if chromatic else colours[0][0]
    brand = darken_for_white(base)
    highlight, why = None, ""
    for c, f in colours:
        if c == base or f < 0.02 or hls(c)[2] < 0.25 or hue_dist(c, brand) <= 30:
            continue
        h, l, s = hls(c)
        cand = c
        while contrast(cand, brand) < 3 and l < 0.92:  # lighten, keeping the hue, until it reads on the brand
            l += 0.02
            cand = from_hls(h, l, s)
        if contrast(cand, brand) >= 3:
            highlight = cand
            why = "second logo colour" + ("" if cand == c else f", lightened from {hexc(c)} to stand out on the brand colour")
            break
    if highlight is None and hls(brand)[2] >= 0.15:
        h, _, s = hls(brand)
        highlight, why = from_hls(h, 0.78, min(1, s + 0.1)), "light tint of the brand colour (logo has no usable second colour)"
    if highlight is None:
        highlight, why = (0xF5, 0xA4, 0x00), "amber from the presets: the logo is monochrome, so ask the user to confirm or pick one"
    return base, brand, highlight, why


def swatch(path, brand, highlight):
    img = Image.new("RGB", (640, 220), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 640, 60], fill=brand)
    d.text((20, 22), "Header band: white title on brand", fill="white")
    d.rectangle([0, 80, 400, 220], fill=brand)
    d.text((20, 140), "Divider slide", fill="white")
    d.ellipse([300, 110, 380, 190], outline=highlight, width=8)
    d.text((420, 140), "0", fill=brand, font=ImageFont.load_default(size=72) if hasattr(ImageFont, "load_default") else None)
    img.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logo")
    ap.add_argument("--swatch")
    args = ap.parse_args()

    colours = dominant(args.logo)
    print("Dominant logo colours (share of non-background pixels):")
    for c, f in colours:
        print(f"  {hexc(c)}  {f:5.1%}  contrast vs white {contrast(c, (255, 255, 255)):.1f}")
    base, brand, highlight, why = propose(colours)
    print()
    print(f"Proposed brand:     {hexc(brand)}" + ("" if brand == base else f"  (darkened from {hexc(base)} for white text)"))
    print(f"Proposed highlight: {hexc(highlight)}  ({why})")
    print(f"White on brand: {contrast(brand, (255, 255, 255)):.1f}:1   highlight on brand: {contrast(highlight, brand):.1f}:1")
    h = hls(brand)[0] * 360
    if 250 <= h <= 290 and hls(brand)[2] > 0.3:
        print("Note: brand is in the purple/indigo range listed as an AI-default palette; fine if it IS the brand, but say so.")
    if args.swatch:
        swatch(args.swatch, brand, highlight)
        print(f"Swatch: {args.swatch}")


if __name__ == "__main__":
    main()
