# Deck style and anti-slop rules

Shared by the `pitch-deck` and `td-deck` skills. Read this before writing an outline and again before generating slides. The goal: a deck a human designer and a sceptical engineer would both accept, with none of the tells that mark a deck as machine-made.

---

## 1. Precedence

- **A template or reference deck exists** (`template.pptx`, or a `.pptx` in the skill's samples directory): its fonts, colours and layout positions win. Section 3 bans apply only to shapes **you add** — never restyle or delete template elements to satisfy them. Section 2 copy rules always apply, except that a template's own fixed, non-placeholder design elements (e.g. a baked-in "Thank you" on its own closing layout) are the template's authored content, not this skill's filler, so the copy bans don't apply to them.
  - **`td-deck`** fills the template slide-for-slide: its master and slides are reused directly, per `specific_instructions.md`, and the deck never gains, loses or reorders slides beyond what the template defines.
  - **`pitch-deck`**, when the reference deck is a real layout library, offers **strict layout reuse**: slide count, order and content stay this skill's own (it can create more or fewer slides than the reference deck has), but each slide is built from one of the reference file's own named layouts — its real masters, placeholders, fonts, logo and art — never a hand-drawn approximation (see `pitch-deck/style-from-reference.md`).
  - **`pitch-deck`**, otherwise (a loose reference deck, or the user prefers it), falls back to **style only**: fonts, colours, positions and logo are extracted and reapplied to this skill's own brand-frame system (section 4) — nothing of the reference file's own slide construction is reused directly.
- **No template**: use the default visual system in section 4.
- Canonical terms from `project_context.md` (or verbatim TD wording, for td-deck) override the vocabulary bans. If a banned word *is* the product's name for something, keep it.

---

## 2. Copy rules (always apply — slides AND speaker notes)

### Deck message and claims

- **Core message first.** Before outlining, write the one sentence the audience should remember, plus 3–5 non-overlapping supporting points. Put them at the top of the outline. Every slide serves one of those points; a slide that serves none is cut. The template's arc (or a memorised pitch arc) is not a reason for a slide to exist.
- **Claims stay inside the source.** An assertion title or bullet may only state what the source supports. Don't invent causes ("…because of X"), consequences or "so-whats" the material doesn't contain. If the source gives only the number, the title states only the number. (In tests, AI deck tools routinely added plausible explanations that the data didn't support.)
- **Interpret, don't restate.** A bullet that just re-reads the table or chart next to it adds nothing. Give the takeaway the source supports, or drop the bullet.
- **Source line on data slides.** A chart, table or headline number gets a small muted `Source: …` line underneath when its origin is known (benchmark, dataset, paper, TD section or reference). Cite the real origin, never "project_context.md". If the origin isn't known, omit the line and list the number in the hand-off as unsourced.
- **No unattributed quotes.** A pull quote needs a real, named source — otherwise cut it.
- **Honest comparisons.** A comparison table where we win every row is not an analysis. Include the rows where alternatives are better, or drop the table.
- **Concrete opening.** The first content slide opens on a specific fact (what the thing does, a real number), never a scene-setting cliché.

### Titles

- **Assertion titles.** Each content slide's title states the slide's one point as a short sentence (≤ ~12 words, max 2 lines). Read in sequence, the titles alone should tell the story.
  - ✗ `Performance` → ✓ `Ingest latency fell from 4 s to 300 ms`
  - ✗ `Architecture` → ✓ `Three services share one event queue`
  - Exempt: the title slide, agenda, references, and title text fixed by a template / `specific_instructions.md`.
- **Sentence case.** Capitalise the first word and proper nouns only. Never Title Case, never ALL CAPS.
- **No terminal punctuation.** No period, exclamation mark or question mark at the end of a title. No question titles ("Why does this matter?").
- **No formula titles.** No `X: The Y of Z`, no `Introducing X`, no `Meet X`.
- **No dangling short words.** If a title wraps, don't leave a, an, the, of, to, in, on at the end of a line — break before it.
- **No series counters.** No `(1/3)`, `Part 2`, or the same title repeated across slides. Either collapse short parts onto one slide, or give each part its own assertion title.

### Body text

- **No em dashes (—)** anywhere. Use an en dash (–) only for ranges (`2–4 s`); otherwise use a comma, colon, or a new sentence.
- **Fragments, no periods.** Bullets are fragments without terminal periods — consistently across the deck. ≤ 5 bullets per slide, ≤ ~12 words each, one level of nesting at most.
- **Concrete over intensifiers.** No "significantly", "dramatically", "massive", "blazing fast" without the number. If there is no number, state the fact plainly.
- **Don't pad to three.** Lists have as many items as the content has — two is fine, four is fine.
- **Vary the form.** "3–4 equal-length parallel bullets" on slide after slide is the most reliable deck tell. Let the content choose: one sentence, one number with context, a table, a diagram, or bullets. Never more than two consecutive slides of 3–4 parallel bullets, and vary bullet count and length.
- **No negative parallelism.** No "not just X, but Y", "it's not X — it's Y", "more than just".
- **No emoji, no decorative glyphs** (→ ✓ ★ ✨ 🚀 as bullets or ornaments), and no `·` middots as separators.
- **No filler slides.** No "Key takeaways" slide that repeats earlier titles, no "Thank you!" / "Questions?" closing slide — unless the user asks or the template has one.

### Banned vocabulary

Do not use (in any inflection) unless it is a canonical term:

> seamless, robust, cutting-edge, state-of-the-art (as an adjective), revolutionary, game-changing, game-changer, leverage (verb), unlock, empower, harness, delve, elevate, streamline, supercharge, next-generation, next-gen, world-class, best-in-class, holistic, synergy, paradigm shift, transformative, innovative, powerful, effortless, unparalleled, unprecedented, comprehensive, cutting edge, journey, landscape, realm, tapestry, testament, beacon, all-in-one, fast-paced, ever-evolving, ever-changing, "at the heart of", "in today's", "it's worth noting", "dive into", "look no further", "navigate the complexities", "build the future"

Show novelty with the mechanism or the number, not the adjective.

### Speaker notes

Same copy rules. Plain spoken sentences a presenter could read aloud — no markdown, no bullet syntax, no "In this slide we will…".

---

## 3. Visual bans (every shape you add)

- **No eyebrows or kickers.** Nothing above the slide title — no small label like "Overview" or "Case study". The title is the topmost text on the slide.
- **No badges, pills, chips or tags.** No text inside a filled shape. Page numbers, if any, are plain small text.
- **No shadows, glows, bevels, 3D, reflections.**
- **No rounded rectangles, no gradients, no scattered decoration** (blobs, circles, thin accent bars, coloured stripes along card edges, divider lines that carry no meaning). Design comes from the **brand frame** and **section dividers** in §4 — deliberate, identical on every slide — not from ornaments added per element.
- **No icon-card grids.** The "three cards, each with icon + bold title + two-line blurb" layout is the single most recognisable slop layout. Use a plain list, a table, or a diagram placeholder.
- **No stat-tile dashboards.** A grid of equal-weight number tiles is built for monitoring, not for making a point. One data claim per slide, with one table or chart as evidence.
- **No page-counter chrome.** No `01 / 10` counters, progress dots, zero-padded section numbers (`02`) or numbered corner marks. If pages are numbered, a plain small number in the footer, never on the title slide.
- **No fake variety.** No alternating background tints or decorative changes to simulate design; variety comes from layouts that fit the content (§4).
- **No AI default palettes.** No purple/indigo/violet; no warm cream canvas with terracotta/clay/muted-red accents and an editorial serif (Fraunces, Playfair); no dark slate with sky/indigo accent. These read as "generated" on sight.
- **No emoji, clip art or glossy 3D/stock imagery.** Icons come from one open-source line-icon set, in one colour, used sparingly (§4).
- **One font family** (a heading/body pair only if the template defines one). No italics. Bold at most once per slide, for the one number or term that matters.
- **One accent colour in the content**, on at most one element per slide. The brand frame and divider backgrounds use the brand colour and don't count. Everything else is near-black, grey, white. Titles are a single colour — never the accent on the last word (or any part) of a title.
- **Left-aligned body text.** Centre only the title slide and the diagram-placeholder label.
- **Full-colour backgrounds via the slide background**, never a full-bleed rectangle — and only on the title, section-divider and closing slides.
- **Numbers shown visually come with their values.** Prefer a native table. Charts are native, editable PowerPoint chart objects (python-pptx `add_chart`) — never images and never bars drawn from shapes, so the numbers can be updated later. Pick the type the claim needs (bar to compare, line for a trend, stacked bar for a breakdown), label values directly on it, one chart per slide; no 3D charts, no pie charts with more than 4 slices.
- **Nothing outside the slide bounds**, and no text box overflowing its area.

---

## 4. Default visual system (no template)

Use these exact values so every slide is consistent. The brand colour, highlight, font and logo come from the **brand questions** below — never chosen silently; everything else stays as listed.

| Element | Value |
|---|---|
| Canvas | 16:9, 13.333 × 7.5 in |
| Margins | 0.6 in left/right |
| Font | Calibri (LibreOffice substitutes the metric-compatible Carlito), or the brand / reference deck's font |
| Colours | brand + highlight from the chosen colour template (below); text `#1F2328`, muted `#57606A`, hairline `#D0D7DE`, footer band `#F1F3F5`, on-brand light text `#C9D6EA`, background `#FFFFFF` |
| Title (content slides) | white, 28 pt, on the header band at (0.6 in, 0.2 in), width 12.1 in, height 0.95 in, anchored middle — identical on every content slide |
| Body | 18 pt (never below 14 pt); 24 pt for short lists of ≤ 4 items, so the slide isn't top-heavy; line spacing 1.15, left-aligned, starts at 1.75 in from top, ends above the footer band |
| Text beside a visual | text column ≤ 5.6 in wide, ≥ 0.4 in gap to the visual |
| Content accent | the brand colour on white slides (e.g. a big number); the highlight only on brand-coloured slides |
| Diagram placeholder | outline-only rectangle (1 pt `#57606A`, no fill), centred label `[ DIAGRAM PLACEHOLDER ]`, one-line description underneath |

**Brand frame (every content slide, identical).** Pick one frame per deck and never vary it:

- **Header band + footer band (default):** a full-width brand-colour band 0 – 1.35 in carrying the white title, and a 0.45 in footer band at the bottom (`#F1F3F5`) with the project name (or logo, 0.3 in tall) left and the plain page number right, both 11 pt muted.
- **Side rail + footer band:** a brand-colour rail 0.35 in wide down the left edge, near-black title on white, same footer band.

The frame is two plain rectangles behind the text — no gradients, no shadows, no extra lines or stripes. The title slide, dividers and closing slide have no frame.

**Title, section-divider and closing slides (the "big type" slides).**

| Element | Value |
|---|---|
| Background | slide background in the brand colour |
| Big text | white, left-aligned, 60 – 66 pt (title slide) or 54 – 60 pt (divider and closing statement), starting ~2.2 in from top, max 2 lines |
| Subtitle | 24 pt, on-brand light text, one line under the big text |
| Presenter / date (title slide only) | 14 pt, on-brand light text |
| Visual | one large icon (3 – 3.6 in) or the logo on the right side, in the highlight colour — or a full-bleed image at ≤ 25 % opacity behind the text. Never more than one |
| Dark logo, no light version | **split title slide**: brand background on the left with the text (width ≤ 7.6 in), a full-height white panel from x = 8.9 in to the right edge, the logo ~3.2 in centred in it. Dividers and closing keep icons |

Use dividers to mark real sections: at most one per section, at most two in a deck of ≤ 10 slides, and only before sections that the deck's core message actually splits into. The closing slide states the deck's core message (or the user's ask) — never "Thank you".

**Icons, logos and images.**

- Icons: one open-source line-icon set for the whole deck. Default: [Lucide](https://lucide.dev) (ISC licence), fetched by name and rendered to a recoloured, transparent PNG with `<suite-dir>/icon_to_png.py` (see the script's header for usage). Only on big-type slides, or one small icon per item in a list where each item is a distinct thing. Never in card grids, never as bullet decoration.
- Logo: as settled in the brand questions — in the footer band (0.3 in tall, in place of the project name) and, if a light version exists, as the visual on the title slide.
- Images: only user-provided or project-owned (screenshots, photos); no stock imagery.
- If the icon tooling isn't available (no network, no LibreOffice, no Pillow), skip icons and use the logo or no visual — the big type carries the slide on its own.

**Brand questions (always ask, before any styling).** Ask them in this order, via AskUserQuestion when available. Never fall back to a default palette or skip the logo without the user's answer.

1. **Company logo.** Look in `docs/assets/logos/` first (shared with the `td` skill; create it if missing):
   - one file → offer "Use `<file>`" / "Use a different logo" / "No logo";
   - several → ask which one;
   - none → offer "I'll add one to `docs/assets/logos/`" (then wait until it's there) / "No logo — use the project name".

   Logos must be PNG or JPG (python-pptx can't place SVG). A dark logo can't sit on the brand-colour slides: ask whether a light/white version exists; if not, offer the split title slide (below) or footer-only, and keep icons on the dividers and closing slide.

2. **Logo analysis (when there is a logo).** Run:

   ```bash
   python3 <suite-dir>/logo_palette.py docs/assets/logos/<file> --swatch <scratch>/swatch.png
   ```

   It lists the logo's dominant colours and proposes a **brand** colour (the logo's main colour, darkened if needed so white titles on it reach 4.5 : 1 contrast) and a **highlight** (a second logo colour that reads on the brand colour, or a fallback it explains). Then Read both the logo and the swatch and check the proposal makes sense to the eye: a gradient, photo or tiny accent can mislead the script. Adjust if needed and say why. If the script can't run (no Pillow), Read the logo and propose the colours by eye, saying the hex values are estimates.

3. **Colour template.** Ask the user to approve. Options, in this order:
   - **From your logo (Recommended)** — when a logo was analysed. The description gives both hex codes, the "darkened from …" note if any, and where each colour shows up.
   - **From `<file>`** — when a template or reference deck exists.
   - The presets below, filling the remaining options (the question takes at most 4).
   - The user can also type their own hex codes and a font via "Other".

   | Template | Brand (frame, dividers, big numbers) | Highlight (icons on brand slides) |
   |---|---|---|
   | Cobalt & amber | `#0B3D91` | `#F5A400` |
   | Deep teal & sun yellow | `#0F4C5C` | `#F2C14E` |
   | Graphite & signal red | `#2B2D42` | `#E63946` |
   | Forest & mint | `#1B4332` | `#95D5B2` |

   A custom brand colour must be dark enough for white title text on it (contrast ≥ 4.5 : 1); if not, say so and propose a darker shade. Accept any custom choice, but warn if it matches one of the AI default palettes in §3. Font defaults to Calibri unless the user names one. Don't build anything until a colour template is approved.

**Layouts.** The frame and title position are fixed on every content slide; what varies is the composition below the title. Pick the layout the content needs:

| Layout | Use when the slide is… | Composition below the title |
|---|---|---|
| Text | a short list or explanation | body text, column ≤ 9 in wide |
| Text + visual | a point supported by a diagram, table or chart | text column left (≤ 5.6 in), visual right |
| Full-width visual | the diagram, table or chart *is* the point | visual spans the margins from 1.75 in down |
| Big number | one number carries the point | the number at 96 – 120 pt in the brand colour, one context line 20 pt muted, source line |
| Statement | one claim that needs no support on the slide | the assertion title, plus one 28 pt sentence; detail goes in speaker notes |

No more than three consecutive content slides share a layout. Use Big number and Statement where the content really is one number or one claim — not as decoration.

python-pptx gotchas:
- Create text with `add_textbox`, not `add_shape` — shapes inherit the theme's fill, shadow, blue outline and **white text**.
- For the diagram-placeholder rectangle (the one `add_shape` you need): delete the theme style element (`el = shape._element; el.remove(el.find(qn("p:style")))`, with `from pptx.oxml.ns import qn`), then `fill.background()`, set `line.color.rgb` and `line.width`, and set the label's font colour and size explicitly. `shadow.inherit = False` alone is not enough — LibreOffice still renders the theme shadow — and without explicit colours the label renders white-on-white.
- Set `word_wrap = True` and every font size, name and colour explicitly.
- Use the Blank layout (or delete unused placeholders) so no empty "Click to add" boxes ship.
- Frame bands: also `add_shape` rectangles, so delete `p:style` from them too, then set `fill.solid()` + colour and `line.fill.background()`. Add them before the text so they sit behind it.
- Slide background: `slide.background.fill.solid()` then `.fore_color.rgb`.
- Image opacity: python-pptx has no API; add `<a:alphaModFix amt="25000"/>` inside the picture's `a:blip`.

---

## 5. Quality gate (before hand-off)

Run all three. Fix and regenerate until clean — never deliver a deck that fails step 1.

**Step 1 — Lint (mandatory).** From the project root, where `<suite-dir>` is the directory containing this file (normally `.claude/skills`):

```bash
python3 <suite-dir>/lint_deck.py <deck.pptx> [--template] [--max-words N] [--allow TERM ...]
```

- `--template` — the deck was built on a template; skips the visual checks (they would flag the template's own shapes) and keeps the copy checks.
- `--max-words` — body-word limit per slide (default 60).
- `--allow` — canonical terms that collide with the banned-vocabulary list.

Exit code 0 = no errors. Errors must be fixed. Warnings need a judgment call: fix them, or mention in the hand-off why they stand.

**Step 2 — Render check (optional, only if the tools are installed).** Check with `command -v soffice pdftoppm`. If both exist:

```bash
OUT=$(mktemp -d)
soffice --headless --convert-to pdf --outdir "$OUT" <deck.pptx> >/dev/null
pdftoppm -png -r 50 "$OUT"/*.pdf "$OUT/slide"
```

Then Read every `slide-*.png` and look for: clipped or overflowing text, overlapping shapes, titles that jump position between slides, half-empty slides, leftover template guidance text, runs of slides that look identical, anything from section 3. If either tool is missing, skip this step — don't install anything — and say in the hand-off that the visual check was skipped and why. (LibreOffice rendering differs slightly from PowerPoint; treat small font-metric shifts as noise.)

**Step 3 — Editing pass.** Go through the deck as a sceptical editor would:

- **Titles:** list them in order. Do they tell the story on their own and support the core message, with no repeats and no topic labels? Rewrite any that don't.
- **Claims:** every number and every "because" traces to the source. Delete what can't be verified.
- **8-second test:** could the audience take in each slide in about 8 seconds? If not, split it or move detail to the speaker notes.
- **Cut:** slides that serve no supporting point, content repeated from an earlier slide, decoration that carries no information.
- **Any-topic test:** could this deck be about a different project with only the nouns swapped? If yes, it isn't specific enough yet. Add the concrete mechanism, number or name.
- **Rhythm:** is there a run of same-layout or same-bullet-shape slides? Break it.
