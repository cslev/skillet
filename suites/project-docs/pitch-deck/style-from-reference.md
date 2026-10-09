# Using a reference deck: strict layout reuse, or style only

Read this when Required reading step 4 finds a `.pptx` in `docs/decks/samples/` or `docs/decks/`.

**This skill never does template filling** the way `td-deck` does: `td-deck` fills a fixed set of slides one-to-one and never adds, removes or reorders any. Here, the slide count, order and content are always this skill's own — chosen from the outline in Step 3, not from the reference deck. What varies is *how much of the reference deck's own construction gets reused*:

- **(A) Strict layout reuse** — every slide in the deck is built by instantiating one of the reference file's own named slide layouts (its real masters, placeholders, fonts, logo, background art, even an embedded photo) and filling it with this skill's generated content. The skill can still create as many content or divider slides as the outline needs — more or fewer than the reference file happens to contain — as long as each one reuses an actual layout from that file, never a hand-drawn approximation of it.
- **(B) Style only** — fonts, colours and positions are extracted and reapplied to the skill's own brand-frame system (`../deck-style.md` §4). Nothing from the reference file's own slide construction is reused directly.

(A) produces a far more authentic result when the reference file is a real design-system template (an org's PowerPoint template, for instance) — it keeps real photography, icon chrome and closing-slide design that (B) can't approximate. (B) is the only sensible option when the reference file is just one or two loose example slides, not a layout library.

## Step 1 — Run the extractor

Which file: the most recently modified `.pptx` in `docs/decks/samples/`; if that's empty, the most recent in `docs/decks/`. If more than one plausible style file sits in `samples/`, ask the user which one to use.

```bash
python3 <suite-dir>/style_from_reference.py <reference.pptx> --out-dir <scratch>/logos --json <scratch>/style.json
```

This is a deterministic script, not a written procedure to improvise. It reports `reusable_as_template: true/false` — true when it found at least one divider-like layout and two or more distinct content-capable layouts (a real template library), false for a loose reference deck. It also prints the full **layout catalogue**: every named layout, a guessed role (title / divider / closing / content), a content-tag for content layouts (`paragraph`, `table`, `image`, `text_and_image`, `multi_column_icons`, `big_statement`, …), and every placeholder's index, type and position. It separately resolves each role's background/font/colour tokens, finds logo candidates, classifies each as light or dark, and proposes a brand + highlight colour.

## Step 2 — Ask which mode, when both are plausible

If `reusable_as_template` is false, skip the question — only (B) applies, and the script's role/colour/logo extraction feeds Steps 4–5 below as before.

If `reusable_as_template` is true, ask the user (via **AskUserQuestion** when available), after showing a short summary of the layout catalogue:

> "`<file>` looks like a real template, with N layouts including a divider and M content variants (table, image, etc.). Should the deck be built strictly from the template's own layouts (A), or should I just take its colours and fonts and build with my own slide designs (B)?"

Default to (A) when the catalogue looks genuinely reusable — it's the more faithful result. Fall back to (B) if the user prefers the skill's own consistent design regardless, or if a specific layout the outline needs has no good match in the catalogue (say so, and ask whether to approximate it in (B)'s style instead for just that slide).

## Step 3 — Resolve the script's warnings and ambiguity by eye

The script is a heuristic extractor, not a full OOXML renderer, and says so when unsure:

- **Contrast warnings** — e.g. a role's title text has almost no contrast against the resolved background, meaning the real background is a *shape* behind the placeholder (a coloured panel) rather than the slide background — the script doesn't resolve arbitrary shape fills. Open that slide in the catalogue/report and read its actual colour by eye; this doesn't block using the layout in mode (A), since the layout's own shape renders correctly regardless — it only affects a colour value you'd otherwise want for mode (B) or for choosing a matching highlight.
- **Logo candidates** — ranked by recurrence and size. Read the top 1–2 (saved as cropped PNGs) to confirm which one is the actual logo. `is_light`/`is_dark` tells you whether it belongs directly on a brand-coloured background or needs a light panel (`../deck-style.md` §4).
- **Content-tag mismatches** — the tag is a rough heuristic (placeholder types and counts); read a layout's actual placeholder list before relying on it for something structurally important (e.g. confirm "table" really is a table placeholder, not a wide text box).

## Step 4 (mode A) — Map the outline to the catalogue, then fill

For each slide in the Step 3 outline (`pitch-deck/SKILL.md`):

1. Pick the catalogue entry whose `role_guess` matches the slide's role (title/divider/closing/content) and whose `content_tag` best matches what the slide needs (a plain text slide → `paragraph`; a slide with a diagram or photo → `image`/`text_and_image`; tabular data → `table`; one number or claim → `big_statement`; several items → `multi_column_icons`). If several layouts share a tag (e.g. multiple cover variants), prefer the one the reference deck's own demo slides actually used, else the first.
2. Build the deck on top of the reference file itself: open it as the base `Presentation`, remove its existing (demo) slides from `prs.slides._sldIdLst` — this keeps the masters and layouts intact while dropping only the example content — then call `prs.slides.add_slide(layout)` for each outline slide, using the chosen layout object directly from `prs.slide_masters[0].slide_layouts` (or `prs.slide_layouts`).
3. Fill each placeholder by its `idx` from the catalogue (title idx → the slide's assertion title, body idx → its content, picture idx → `add_picture`/a diagram placeholder image, table idx → the generated table). Never append to or leave untouched any placeholder that still carries the template's own instructional/guidance text — replace it entirely, the same rule `td-deck` already follows for `template.pptx`.
4. Leave every non-placeholder design element exactly as the layout defines it (background art, logo, decorative chrome, a baked-in closing line like "Thank you" that is part of the layout's own fixed design, not something this skill wrote) — this is the template's own authored content, not the skill's filler, so the anti-slop ban on "Thank you" slides (`../deck-style.md` §2) does not apply to it. The visual bans in `../deck-style.md` §3 apply only to shapes this skill adds on top, same precedent as `td-deck`.
5. If the outline wants more content or divider slides than the reference deck's demo set happened to show, that's fine — just call `add_slide` again with the same layout object; it isn't consumed.
6. **A table, image or chart placeholder may be narrower than the slide** — some templates reserve room beside it for a caption or another element, so its placeholder is deliberately not full-width. When that slide has nothing else sharing the space (confirmed by the render check), stretch it to the content width instead of leaving a dead gap: set the `GraphicFrame`'s `left`/`width` to match a nearby full-width placeholder (e.g. the slide's own title), and set each column's width explicitly — resizing the frame alone does **not** rescale a table's columns, since each column's width is its own XML attribute, independent of the frame's.
7. **A placeholder that is nominally a text type (e.g. `BODY`) can secretly be the layout's own decorative background shape**, carrying its own fill rather than inherited placeholder styling. If an unused placeholder turns out to be load-bearing like this, deleting it (per the usual "scrub unfilled placeholders" rule below) will delete the background with it — confirmed by testing. Check a placeholder's own `spPr` for a `solidFill` before deleting it; if it has one and spans most of the slide, leave it alone and choose a different layout entirely for that slide's content rather than trying to rescue it.
8. **Delete every placeholder you deliberately choose not to fill** — rather than leave it untouched. An unfilled placeholder can render a literal "Click to add text" prompt into the exported slide in LibreOffice (confirmed by the render check); real PowerPoint is expected not to show this, but it isn't practical to verify that here, so don't rely on it. The one exception is rule 7's background-fill shapes, which must never be deleted.

## Step 4 (mode B) — Reconcile with the brand questions, then build fresh

- If `docs/assets/logos/` already has a logo, prefer it over one extracted from the reference deck — the user-provided file is authoritative. Mention it if the reference deck's embedded logo differs, and let the user choose.
- Offer the script's `proposed_brand` / `proposed_highlight` as the "From `<file>`" option in the colour-template question (`../deck-style.md` §4), with the actual hex values. The user still approves it like any other option.
- Font comes from the script's `fonts.major`/`fonts.minor`; don't ask separately unless extraction failed.
- If the user approves a logo extracted from the reference deck, save it into `docs/assets/logos/` so future runs don't need to re-extract it.
- Build with the skill's own default visual system (`../deck-style.md` §4): brand frame, big-type title/divider/closing slides, the five layout choices (Text / Text + visual / Full-width visual / Big number / Statement).

## Step 5 — The rest of the skill's own rules, either mode

The core message, outline, slide count, assertion titles, banned vocabulary and quality gate (`../deck-style.md`) are unchanged in both modes. The reference deck supplies the look (mode A: its actual construction; mode B: its colours and fonts); it never supplies the content or the slide count.

**Quality gate note:** in mode (A), pass `--template` to `lint_deck.py` (per `../deck-style.md` §5) — the deck is built almost entirely from inherited template formatting, so the visual checks would otherwise flag the template's own shapes; the copy rules (titles, banned vocabulary, speaker notes) still run in full. In mode (B), run the linter without `--template` as usual.
