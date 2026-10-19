# Analysing a template and building from it

Read this when a template `.pptx` is available (found by the lookup order in `SKILL.md`). Slide count, order and content always come from the outline, never from the template. What varies is how much of the template's own construction gets reused:

- **(A) Strict layout reuse**: every slide is built by instantiating one of the template's own named layouts (real masters, placeholders, fonts, logo, background art, embedded photos) and filling it. As many slides as the outline needs, as long as each is a real layout from that file, never a hand-drawn approximation.
- **(B) Style only**: fonts, colours and positions are extracted and reapplied to the skill's own brand-frame system (`deck-style.md` §4). Use it when the template is just one or two loose example slides, or the user prefers it.

(A) is far more faithful for a real design-system template. Default to it when the catalogue looks reusable.

## Step 1: run the extractor

```bash
python3 <skill-dir>/scripts/style_from_reference.py <template.pptx> --out-dir <scratch>/logos --json <scratch>/style.json
```

It is deterministic; do not improvise the analysis by eye. It reports:

- theme fonts and colours, and the resolved tokens for each role (title, divider, closing, content);
- `reusable_as_template: true/false`: at least one divider-like layout and two or more distinct content layouts;
- the **layout catalogue**: every named layout, a guessed role, a content tag (`paragraph`, `table`, `image`, `text_and_image`, `multi_column_icons`, `big_statement`, ...), and each placeholder's index, type and position;
- logo candidates, classified light or dark (a light logo goes on brand-colour slides, a dark one needs a light panel), and a proposed brand and highlight colour.

If `reusable_as_template` is false, only (B) applies.

## Step 2: resolve ambiguity by eye

The extractor is a heuristic, not an OOXML renderer.

- **Contrast warnings** (title text on a background of the same colour) usually mean the real background is a *shape* in the layout, not the slide background. Render the layout and look. It does not block (A).
- **Logo candidates**: read the top one or two (saved as PNGs) to confirm which is the logo. WMF/EMF logos cannot be decoded; the layout still shows them.
- **Content tags** are rough. Read a layout's actual placeholder list before relying on it for anything structural.
- **Render the layouts you plan to use.** Add one slide per candidate layout, fill every placeholder with its own name and index, convert with LibreOffice and look. Names lie (a "Cover" can carry a baked-in photo; a "Closing" a baked-in "THANK YOU"; a "Big Idea" a coloured panel placeholder). Do this once; it saves rework.

## Step 3: map the outline to the catalogue

For each outline slide pick the layout whose `role_guess` matches the slide's role and whose content tag fits what it needs: plain text → `paragraph`; text beside a picture → `text_and_image`; tabular data → `table`; one number or claim → `big_statement`; a chart or anything custom → the template's **empty** content layout, with native charts and shapes added on top. If several share a tag, prefer the one the template's own demo slides use.

Show the user the mapping (slide, role, chosen layout, why) for approval. Flag every slide with no good match and say what you'll do instead: approximate it in style (B) for that slide only, or use the empty layout.

## Step 4 (mode A): build

1. Open the template as the base `Presentation`, drop its demo slides from `prs.slides._sldIdLst` (and `drop_rel`), which keeps masters and layouts, then `add_slide(layout)` per outline slide. `deck_lib.open_template` does this.
2. Fill each placeholder by `idx` from the catalogue. Replace the template's instructional text entirely; never leave or append to it.
3. Leave every non-placeholder design element as the layout defines it: background art, logo, decorative chrome, baked-in closing text. The visual bans in `deck-style.md` §3 apply only to shapes this skill adds.
4. **A table, picture or chart placeholder may be narrower than the slide** (room reserved for a caption). If nothing else shares the space, stretch it to the content width: set the frame's `left`/`width`, and set each column's width explicitly (resizing the frame does not rescale a table's columns).
5. **A text-type placeholder can secretly be the layout's decorative panel** (it carries its own fill). Check its `spPr` for a `solidFill` before deleting it. If it has one and spans a large area, leave it and fill it with something short, or choose another layout.
6. **Delete every placeholder you don't fill** (`deck_lib.scrub_placeholders`), except those in rule 5. LibreOffice renders unfilled placeholders as "Click to add text".
7. **Picture placeholders**: images the outline provides go in with `add_picture`. Images it only describes (prompts, "paste Fig. 3") become an outlined placeholder box with the brief in the speaker notes. The skill never generates images.
8. **Setting text on a placeholder that already has runs drops their formatting** (the title can turn black and non-bold). Use `deck_lib.set_text`, which keeps the first run's properties.
9. **Footers**: the layout's classification and source placeholders are filled (a `Source: ...` line on data slides) or deleted. Never leave template guidance text.
10. **The Thank-you slide**: use the template's closing layout if the catalogue has one (see `deck-style.md` §4). Otherwise `deck_lib.add_closing` builds a styled one on the empty layout.

In (A), run the linter with `--template`.

## Step 4 (mode B): reconcile and build fresh

- A logo found by the lookup order in `SKILL.md` wins over one extracted from the template; mention it if they differ and let the user choose. A logo the user approves from the template is saved there so later runs don't re-extract it.
- Offer the extractor's `proposed_brand` / `proposed_highlight` as the "From the template" option in the colour question (`deck-style.md` §4), with the hex values. The user approves it like any option.
- The font comes from the extractor's `fonts.major` / `fonts.minor`.
- Build with the default visual system: brand frame, big-type title and divider slides, the five layouts (Text, Text + visual, Full-width visual, Big number, Statement).
