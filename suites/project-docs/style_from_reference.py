#!/usr/bin/env python3
"""Extract a deck style (fonts, colours, positions, logo) from a reference .pptx.

Deterministic replacement for doing this by eye: run it once per reference deck
and read its report, instead of a written "look at the file and figure it out"
procedure. Used by the `pitch-deck` skill (see `pitch-deck/style-from-reference.md`)
for STYLE adaptation only — it never touches slide count, order or content, which
stay the skill's own. (`td-deck` fills a template slide-for-slide instead and does
not use this script.)

Usage:
    python3 style_from_reference.py REFERENCE.pptx [--out-dir DIR] [--json FILE]

Prints a human-readable report: theme fonts/colours, one token set per detected
role (title / divider / closing / content), and logo candidates with a light/dark
classification (reusing the contrast math from logo_palette.py) so the skill knows
whether a logo belongs on a brand-coloured background or needs a light panel.
`--out-dir` saves each distinct logo candidate as a PNG/JPG; `--json` also writes
the full structured report for later reference.

This is a heuristic extractor, not a full OOXML style resolver — low-confidence
values are listed under "ambiguous"/"warnings" for a human (or the agent reading
this output) to confirm by eye, especially a deck's actual rendered colours.
Needs python-pptx and Pillow. SVG/WMF/EMF logo candidates are reported but not
decoded (Pillow can't open them); re-export those as PNG first if needed.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Emu
except ImportError:
    sys.exit("style_from_reference.py needs python-pptx: pip install python-pptx")

sys.path.insert(0, str(Path(__file__).parent))
from logo_palette import contrast, hexc, hls  # noqa: E402  (shared colour math)


def hex_to_rgb(h):
    return tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

ROLE_PATTERNS = {
    "title": r"\bcover\b|\btitle\s*slide\b",
    "divider": r"\bdivider\b|\bsection\s*header\b|\bsection\b",
    "closing": r"\bclosing\b|\bthank\s*you\b|\bend\s*slide\b",
}
MAX_LOGO_AREA = 0.12  # fraction of slide area; bigger is probably a photo, not a logo
RASTER_EXT = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


# ---------- theme colours ----------

def load_theme(master):
    scheme, fonts = {}, {"major": None, "minor": None}
    for rel in master.part.rels.values():
        if "theme" not in rel.reltype:
            continue
        xml = rel.target_part.blob.decode("utf-8", "ignore")
        m = re.search(r"<a:clrScheme.*?</a:clrScheme>", xml, re.S)
        if m:
            for slot, val in re.findall(r"<a:(\w+)>\s*<a:(?:srgbClr val|sysClr[^>]*lastClr)=\"([0-9A-Fa-f]{6})\"", m.group(0)):
                scheme[slot] = "#" + val.upper()
        for key, tag in (("major", "majorFont"), ("minor", "minorFont")):
            fm = re.search(rf"<a:{tag}>.*?<a:latin typeface=\"([^\"]*)\"", xml, re.S)
            if fm and fm.group(1):
                fonts[key] = fm.group(1)
    return scheme, fonts


def load_clrmap(master):
    el = master.element.find(f"{P}clrMap")
    return dict(el.attrib) if el is not None else {}


def resolve_scheme_slot(name, clrmap, theme):
    name = clrmap.get(name, name)
    return theme.get(name)


def apply_lum(hexcolor, lum_mod=None, lum_off=None):
    if hexcolor is None or (lum_mod is None and lum_off is None):
        return hexcolor
    rgb = tuple(int(hexcolor.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    h, l, s = hls(rgb)
    if lum_mod is not None:
        l *= lum_mod
    if lum_off is not None:
        l += lum_off
    l = max(0.0, min(1.0, l))
    from logo_palette import from_hls
    return hexc(from_hls(h, l, s))


def resolve_color_el(el, clrmap, theme):
    """A solidFill's child colour element -> hex, or None."""
    if el is None:
        return None
    sc = el.find(f"{A}schemeClr")
    if sc is not None:
        base = resolve_scheme_slot(sc.get("val"), clrmap, theme)
        lum_mod_el = sc.find(f"{A}lumMod")
        lum_off_el = sc.find(f"{A}lumOff")
        lum_mod = int(lum_mod_el.get("val")) / 100000 if lum_mod_el is not None else None
        lum_off = int(lum_off_el.get("val")) / 100000 if lum_off_el is not None else None
        return apply_lum(base, lum_mod, lum_off)
    srgb = el.find(f"{A}srgbClr")
    if srgb is not None:
        return "#" + srgb.get("val").upper()
    return None


# ---------- backgrounds ----------

def get_own_background(obj):
    """Solid background hex defined directly on this slide/layout/master, or None."""
    bg = getattr(obj, "background", None)
    if bg is None:
        return None
    fill = bg._element.find(f"{P}bg/{P}bgPr/{A}solidFill")
    return fill  # caller resolves with resolve_color_el, needs clrmap/theme in scope


def effective_background(slide, clrmap, theme):
    for obj in (slide, slide.slide_layout, slide.slide_layout.slide_master):
        fill = get_own_background(obj)
        if fill is not None:
            hx = resolve_color_el(fill, clrmap, theme)
            if hx:
                return hx
    return theme.get("lt1", "#FFFFFF")


# ---------- text ----------

def run_props(run):
    rPr = run._r.find(f"{A}rPr")
    if rPr is None:
        return {}
    out = {}
    if rPr.get("sz"):
        out["size_pt"] = int(rPr.get("sz")) / 100
    if rPr.get("b"):
        out["bold"] = rPr.get("b") == "1"
    latin = rPr.find(f"{A}latin")
    if latin is not None and latin.get("typeface"):
        out["font"] = latin.get("typeface")
    fill = rPr.find(f"{A}solidFill")
    if fill is not None:
        out["_color_el"] = fill
    return out


def placeholder_by_idx(container, idx):
    try:
        for ph in container.placeholders:
            if ph.placeholder_format.idx == idx:
                return ph
    except Exception:
        pass
    return None


def largest_run(tf):
    best = None
    for para in tf.paragraphs:
        for r in para.runs:
            if not r.text.strip():
                continue
            props = run_props(r)
            size = props.get("size_pt", 0)
            if best is None or size >= best[1].get("size_pt", 0):
                best = (r.text.strip(), props)
    return best


def resolve_placeholder_text(slide, idx, fonts, clrmap, theme):
    """Representative run for this placeholder idx: slide's own text if present,
    else the layout's (common in templates that bake demo copy into the layout)."""
    for container in (slide, slide.slide_layout):
        ph = placeholder_by_idx(container, idx)
        if ph is not None and ph.has_text_frame:
            lr = largest_run(ph.text_frame)
            if lr:
                text, props = lr
                font = props.get("font")
                if font in ("+mj-lt", None):
                    font = fonts["major"] if font else font
                elif font == "+mn-lt":
                    font = fonts["minor"]
                color = resolve_color_el(props.get("_color_el"), clrmap, theme) if "_color_el" in props else None
                pos = None
                if ph.left is not None:
                    pos = [round(Emu(v).inches, 2) for v in (ph.left, ph.top, ph.width, ph.height)]
                return {"text": text[:60], "size_pt": props.get("size_pt"), "bold": props.get("bold"),
                        "font": font, "color": color, "pos": pos}
    return None


# ---------- role classification ----------

def classify_role_name(name):
    name = name.lower()
    for role, pat in ROLE_PATTERNS.items():
        if re.search(pat, name):
            return role
    return "content"


def classify_by_layout_name(slide):
    return classify_role_name(slide.slide_layout.name)


# ---------- layout catalogue (for strict template-reuse mode) ----------

PLACEHOLDER_TYPE_RE = re.compile(r"\((\d+)\)$")


def content_tag(layout):
    """Rough capability tag from placeholder types, so the skill can match an
    outline slide's intended layout (text / image / table / big number / ...)
    to the closest ACTUAL layout in the template, instead of guessing by name."""
    types = [str(ph.placeholder_format.type) for ph in layout.placeholders]
    has = lambda kw: any(kw in t for t in types)
    n_body = sum(1 for t in types if "BODY" in t)
    if has("TABLE"):
        return "table"
    if has("PICTURE") and n_body >= 5:
        return "multi_column_icons"
    if has("PICTURE") and n_body <= 2 and has("CENTER_TITLE"):
        return "big_statement_with_image"
    if has("PICTURE") and n_body <= 2:
        return "image"
    if has("PICTURE"):
        return "text_and_image"
    if has("CENTER_TITLE") and n_body <= 2:
        return "big_statement"
    return "paragraph"


def build_layout_catalogue(master):
    cat = []
    for layout in master.slide_layouts:
        phs = []
        for ph in layout.placeholders:
            pos = None
            if ph.left is not None:
                pos = [round(Emu(v).inches, 2) for v in (ph.left, ph.top, ph.width, ph.height)]
            phs.append({"idx": ph.placeholder_format.idx, "type": str(ph.placeholder_format.type), "pos": pos})
        cat.append({"name": layout.name, "role_guess": classify_role_name(layout.name),
                   "content_tag": content_tag(layout), "placeholders": phs})
    return cat


def layout_is_customized(layout):
    """True if this layout itself carries a deliberate design choice (a background
    fill of its own, or an embedded picture such as a logo) rather than being an
    untouched stock Office layout. Every python-pptx Presentation() ships the 11
    default Office layouts regardless of use — layout COUNT alone can't tell a
    real template from an unused default theme, so we require actual evidence."""
    if layout.background._element.find(f"{P}bg") is not None:
        return True
    return any(sh.shape_type == 13 for sh in layout.shapes)


def is_reusable_template(catalogue, master):
    """A real design-system template (worth offering strict reuse for) vs a loose
    reference deck, or just the unused stock Office layouts every pptx ships with."""
    roles = {c["role_guess"] for c in catalogue}
    content_tags = {c["content_tag"] for c in catalogue if c["role_guess"] == "content"}
    customized = sum(1 for l in master.slide_layouts if layout_is_customized(l))
    return len(catalogue) >= 4 and "divider" in roles and len(content_tags) >= 2 and customized >= 2


def word_count(slide):
    n = 0
    for sh in slide.shapes:
        if sh.has_text_frame:
            n += len(sh.text_frame.text.split())
    return n


def classify_by_heuristic(slides, bgs):
    """Fallback when layout names give no signal at all (e.g. every slide uses
    a generic 'Blank' layout, as decks this skill itself generates do)."""
    n = len(slides)
    bg_counts = {}
    for b in bgs:
        bg_counts[b] = bg_counts.get(b, 0) + 1
    content_bg = max(bg_counts, key=bg_counts.get)
    roles = []
    for i, (slide, bg) in enumerate(zip(slides, bgs)):
        if i == 0:
            roles.append("title")
        elif i == n - 1 and n > 1:
            roles.append("closing")
        elif bg != content_bg and word_count(slide) < 15:
            roles.append("divider")
        else:
            roles.append("content")
    return roles


# ---------- logos ----------

def picture_blobs(prs):
    """One entry per distinct image per slide (counting the same picture shown via both the
    slide and its inherited layout once), so a logo reused across N slides recurs N times."""
    out = []
    for si, slide in enumerate(prs.slides):
        contributed = set()
        for container, src in ((slide, "slide"), (slide.slide_layout, "layout")):
            for sh in container.shapes:
                if sh.shape_type != 13:  # PICTURE
                    continue
                try:
                    img = sh.image
                except Exception:
                    continue
                h = hashlib.sha1(img.blob).hexdigest()
                if h in contributed:
                    continue
                contributed.add(h)
                area_pct = None
                if None not in (sh.width, sh.height):
                    area_pct = Emu(sh.width).inches * Emu(sh.height).inches / (prs.slide_width / 914400 * prs.slide_height / 914400)
                out.append({"hash": h, "ext": img.ext, "blob": img.blob, "slide_idx": si,
                           "source": src, "area_pct": area_pct})
    return out


def dedupe_candidates(pics):
    by_hash = {}
    for p in pics:
        if p["hash"] not in by_hash:
            by_hash[p["hash"]] = {**p, "count": 0}
        by_hash[p["hash"]]["count"] += 1
    return sorted(by_hash.values(), key=lambda p: (-p["count"], p.get("area_pct") or 1))


def classify_light_dark(blob, ext):
    if ext.lower() not in RASTER_EXT:
        return None, "cannot decode (not a raster format)"
    try:
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(blob)).convert("RGBA")
        data = getattr(img, "get_flattened_data", img.getdata)()
        px = [p[:3] for p in data if p[3] >= 128]
        if not px:
            return None, "fully transparent"
        mean = sum(sum(p) / 3 for p in px) / len(px)
        return (mean > 140), None
    except Exception as e:
        return None, f"decode error: {e}"


# ---------- report ----------

def build_report(path, out_dir):
    prs = Presentation(path)
    master = prs.slide_masters[0]
    theme, fonts = load_theme(master)
    clrmap = load_clrmap(master)
    warnings = []

    slides = list(prs.slides)
    if not slides:
        sys.exit("reference deck has no slides")

    roles = [classify_by_layout_name(s) for s in slides]
    if set(roles) == {"content"}:
        warnings.append("layout names gave no role signal (all generic/Blank) — used position+background heuristic instead")
        bgs = [effective_background(s, clrmap, theme) for s in slides]
        roles = classify_by_heuristic(slides, bgs)
    else:
        bgs = [effective_background(s, clrmap, theme) for s in slides]

    role_tokens = {}
    for role in ("title", "divider", "closing", "content"):
        idxs = [i for i, r in enumerate(roles) if r == role]
        if not idxs:
            warnings.append(f"no '{role}' slide found — build it from the closest role's style")
            continue
        i = idxs[0]
        slide = slides[i]
        tokens = {"source_slide": i + 1, "source_layout": slide.slide_layout.name, "background": bgs[i], "fields": {}}
        for ph in slide.placeholders:
            info = resolve_placeholder_text(slide, ph.placeholder_format.idx, fonts, clrmap, theme)
            if info:
                tokens["fields"][str(ph.placeholder_format.idx)] = info
        role_tokens[role] = tokens
        if len(idxs) > 1:
            tokens["other_instances"] = [j + 1 for j in idxs[1:]]
        # sanity check: a near-invisible title suggests the real background is a SHAPE
        # (e.g. a coloured panel behind the placeholder) that this script doesn't resolve
        title_field = next((f for f in tokens["fields"].values() if f.get("color")), None)
        if title_field and bgs[i]:
            c = contrast(hex_to_rgb(title_field["color"]), hex_to_rgb(bgs[i]))
            if c < 1.8:
                warnings.append(
                    f"'{role}' (slide {i + 1}): title text {title_field['color']} has almost no "
                    f"contrast against the resolved background {bgs[i]} (ratio {c:.1f}:1) — the real "
                    f"background is probably a coloured SHAPE behind the placeholder, not the slide "
                    f"background; open the slide and check its colour by eye")

    pics = dedupe_candidates(picture_blobs(prs))
    logo_candidates = [p for p in pics if (p["area_pct"] or 0) <= MAX_LOGO_AREA]
    if not logo_candidates and pics:
        warnings.append("every picture covers more than 12% of the slide — no confident logo candidate; largest-excluded list still saved")

    saved = []
    if out_dir:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    for n, p in enumerate(logo_candidates[:6], 1):
        is_light, note = classify_light_dark(p["blob"], p["ext"])
        entry = {"rank": n, "recurrences": p["count"], "area_pct": round((p["area_pct"] or 0) * 100, 1),
                 "format": p["ext"], "is_light": is_light, "note": note}
        if out_dir and p["ext"].lower() in RASTER_EXT:
            fn = out_dir / f"logo_candidate_{n}.png"  # always PNG: lets us crop to the opaque bbox
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(p["blob"])).convert("RGBA")
                box = img.getbbox()
                (img.crop(box) if box else img).save(fn)
            except Exception:
                fn = out_dir / f"logo_candidate_{n}.{p['ext']}"
                fn.write_bytes(p["blob"])
            entry["saved_to"] = str(fn)
        saved.append(entry)

    # brand/highlight proposal from the deck's own backgrounds, not re-derived from the logo:
    # the deck already made this decision, so trust its title/divider background over guessing.
    brand = None
    for role in ("divider", "title", "closing"):
        if role in role_tokens and role_tokens[role]["background"] not in (None, theme.get("lt1"), "#FFFFFF"):
            brand = role_tokens[role]["background"]
            break
    highlight, highlight_why = None, None
    if brand:
        accents = [theme[k] for k in ("accent2", "accent3", "accent4", "accent5", "accent6") if k in theme and theme[k] != brand]
        accents = list(dict.fromkeys(accents))  # de-dupe, keep order
        best = max(accents, key=lambda c: contrast(hex_to_rgb(c), hex_to_rgb(brand)), default=None)
        if best:
            highlight, highlight_why = best, "theme accent with the most contrast against the brand colour"

    catalogue = build_layout_catalogue(master)
    reusable = is_reusable_template(catalogue, master)
    if not reusable:
        warnings.append("not enough evidence of a deliberately designed template (custom layout backgrounds/logos, "
                        "a divider, 2+ content variants) — this looks like a loose reference deck, or just the "
                        "unused stock Office layouts every .pptx ships with; strict layout reuse is not offered")

    return {
        "source": str(path),
        "theme_colors": theme,
        "fonts": fonts,
        "roles": role_tokens,
        "logo_candidates": saved,
        "proposed_brand": brand,
        "proposed_highlight": highlight,
        "proposed_highlight_why": highlight_why,
        "reusable_as_template": reusable,
        "layout_catalogue": catalogue,
        "warnings": warnings,
    }


def print_report(r):
    print(f"Source: {r['source']}")
    print(f"Fonts: major={r['fonts']['major']}  minor={r['fonts']['minor']}")
    print(f"Theme colours: {r['theme_colors']}")
    print()
    for role, t in r["roles"].items():
        print(f"=== {role} (slide {t['source_slide']}, layout {t['source_layout']!r}) ===")
        print(f"  background: {t['background']}")
        for idx, f in t["fields"].items():
            print(f"  [{idx}] {f['size_pt']}pt bold={f['bold']} font={f['font']} color={f['color']} pos={f['pos']} text={f['text']!r}")
        if "other_instances" in t:
            print(f"  (also appears as slides {t['other_instances']})")
        print()
    print("Logo candidates (ranked by how often they recur):")
    for c in r["logo_candidates"]:
        light = "light (use ON a brand-colour background)" if c["is_light"] else (
            "dark (needs a light panel, or footer-only placement)" if c["is_light"] is False else f"unknown — {c['note']}")
        print(f"  #{c['rank']}: {c['format']}, {c['area_pct']}% of slide, seen {c['recurrences']}x, {light}"
              + (f" -> {c['saved_to']}" if "saved_to" in c else ""))
    print()
    if r["proposed_brand"]:
        print(f"Proposed brand: {r['proposed_brand']}")
        print(f"Proposed highlight: {r['proposed_highlight']}  ({r['proposed_highlight_why']})")
    else:
        print("Could not propose a brand colour from backgrounds — check the title/divider roles above by eye.")
    print()
    if r["reusable_as_template"]:
        print(f"This looks like a real template library ({len(r['layout_catalogue'])} layouts) — "
              f"strict layout reuse is an option. Layout catalogue:")
        for c in r["layout_catalogue"]:
            tag = f", {c['content_tag']}" if c["role_guess"] == "content" else ""
            idxs = ", ".join(f"{p['idx']}:{p['type'].split()[0]}" for p in c["placeholders"])
            print(f"  [{c['role_guess']}{tag}] {c['name']!r}  placeholders: {idxs}")
    else:
        print("Not a reusable template library (too few distinct layouts) — style-only extraction applies.")
    if r["warnings"]:
        print()
        print("Warnings:")
        for w in r["warnings"]:
            print(f"  - {w}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("reference")
    ap.add_argument("--out-dir", help="save extracted logo candidates here")
    ap.add_argument("--json", help="also write the full structured report here")
    args = ap.parse_args()

    report = build_report(args.reference, args.out_dir)
    print_report(report)
    if args.json:
        with open(args.json, "w") as f:
            json.dump({k: v for k, v in report.items()}, f, indent=2, default=str)
        print(f"\nFull report: {args.json}")


if __name__ == "__main__":
    main()
