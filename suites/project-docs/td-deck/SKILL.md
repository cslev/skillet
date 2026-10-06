---
name: td-deck
argument-hint: "Path to the completed TD markdown file (e.g. td/MyProject_TD_framework_2026-06-15.md)"
description: Generate a presentation deck (.pptx) from a completed Technology Disclosure (TD) document, for presentation to an IP review board and technical reviewers. Trigger when the user mentions "td deck", "td presentation", "present the TD", "slides for the TD", "deck from the TD", "TD slides", or invokes /td-deck. Do NOT trigger for product pitch decks or release showcase decks (the pitch-deck skill handles those), or for generating the TD document itself (the td skill handles that).
---

# TD Deck Skill

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **TD Deck skill activated.** I'll build a presentation deck from your TD document for the IP review board and technical reviewers.

Then proceed immediately to Phase 1. No further preamble.

---

## Prerequisites

- **Required:** `python-pptx` (`pip install python-pptx`). All `.pptx` generation depends on it.
- **Optional:** LibreOffice (`soffice`) and poppler (`pdftoppm`) — enable the render check in Phase 4. LibreOffice + Pillow + network access also enable icons on the big-type slides via `../icon_to_png.py`. If anything is missing, that step is skipped, never installed unprompted.

---

## Required reading

**`../deck-style.md`** — copy rules, visual bans, default visual system and quality gate. Shared with `pitch-deck`. Read it before Phase 2; every rule applies to this skill, with one precedence rule: when `template.pptx` is used, the template's own styling wins and the visual bans apply only to shapes you add. The copy rules always apply.

---

## What this produces

A single `.pptx` presentation deck per request, derived entirely from the content of a completed TD document. The deck is saved in the td-deck output directory — not alongside the TD file.

**This skill does not write or edit TD documents.** If the TD is not yet complete, stop and tell the user to finish it first (using the `td` skill), then come back.

---

## Bootstrap — first-time setup check

Run this before anything else, every invocation:

1. Check whether `docs/td-decks/` exists at the project root.
2. **If it does not exist**, create it:
   ```bash
   mkdir -p docs/td-decks/samples/
   ```
   Then tell the user:
   > "This skill requires `docs/td-decks/` in your project root — created it now along with `docs/td-decks/samples/`. Before I proceed, consider adding:
   > - `docs/td-decks/samples/template.pptx` — your organization's PowerPoint template (the deck will be built from it)
   > - Any reference TD presentation decks (`.pptx`) alongside it — for additional visual calibration
   >
   > These are optional. Tell me to proceed now and I'll fall back to a default structure."

   Wait for the user's response before continuing to Phase 1.

3. **If it exists** but `docs/td-decks/samples/` does not, create it silently and proceed.

---

## Samples handling

The `docs/td-decks/samples/` directory serves two purposes:

1. **`template.pptx`** (optional) — if present, used as the base for all deck generation. All slides, layouts, and styles are inherited from it.
2. **Reference decks** (optional) — any other `.pptx` files, used for visual and structural calibration. Do not borrow content from them.

**On startup, always check `docs/td-decks/samples/` for both.** Specifically:

- Look for `docs/td-decks/samples/template.pptx` — the template file. If found, load it via `Presentation('docs/td-decks/samples/template.pptx')` and **inspect its structure before generating anything**: read every slide's title placeholder and content placeholders, note instructional/guidance text already in placeholders (this is template scaffolding — it must be replaced with real content, not appended to), note slide count limits per section, and identify slides that cannot be filled from the TD alone (see Phase 2).
- Look for any other `.pptx` files in `docs/td-decks/samples/` — read them for style cues.
- If `docs/td-decks/samples/README.md` exists, read it — it may document house-convention notes or deviations. These override what you'd infer from the files alone.

**If `docs/td-decks/samples/` is empty**: note the absence of both template and style references, but do not stop — continue to Phase 1. Both absences will be flagged in the hand-off summary.

---

## Output directory

Always use `docs/td-decks/` for output and `docs/td-decks/samples/` for reference samples. These paths are fixed — do not look for or create alternative locations.

Output filename pattern: `<PROJECT>_TD_<same-slug-as-source-TD>_deck_<YYYY-MM-DD>.pptx`

Where `<PROJECT>` and `<same-slug-as-source-TD>` are derived from the source TD filename. Keep the slug consistent so the deck and its source TD are obviously paired.

---

## Workflow

### Phase 1 — Pre-flight

#### 1a. Validate the TD file

The argument-hint should have provided the path. Resolve it:

- If the file exists and is readable: proceed.
- If the file does not exist: stop immediately.
  > "I can't find a TD file at `<path>`. Please check the path and re-invoke. The TD must be a completed `.md` file generated by the `td` skill."
- If no path was provided via the argument-hint: ask the user for it before doing anything else.

Read the TD file end-to-end. Build an internal map of its sections before proceeding — you'll use this in Phase 2.

#### 1b. Template and style check

Already handled by "Samples handling" above. At this point you know:

- Whether `docs/td-decks/samples/template.pptx` exists → will use it as the generation base, or fall back
- Whether reference style decks exist → will use them for visual calibration, or proceed without

**If no `template.pptx` was found**: tell the user and offer two options (via **AskUserQuestion** when available):

> "No `template.pptx` found in `docs/td-decks/samples/`. How would you like to proceed?
> (a) Use a default TD presentation structure I'll propose — a standard layout for IP review board presentations, which you can adjust.
> (b) Describe the outline yourself, slide by slide, and I'll build exactly what you specify."
>
> To use your own template in future runs, drop it into `docs/td-decks/samples/template.pptx`.

If the user picks **(a)**: proceed with the default structure defined in "Default outline" below. Confirm the proposed outline with the user before generating.

If the user picks **(b)**: collect the slide-by-slide description from the user. Confirm it back before generating.

#### 1c. Ask any remaining questions

Bundle these and ask once:

1. **Length target** — how many slides? Default: 10–14 for a standard IP review board presentation.
2. **Anything to emphasize** — a specific result, a particular innovation, a component the reviewers will push on.
3. **Anything off-limits** — unreleased capabilities, NDA-bound details, internal implementation specifics not yet disclosed.
4. **Company logo** — always ask (logo from `docs/assets/logos/`, per "Brand questions" in `../deck-style.md` §4), even with a template: confirm whether the template already carries the logo or one should be added.
5. **Colour template** — if `template.pptx` is used, its colours apply and this is skipped. Otherwise always ask after the logo: analyse the logo with `../logo_palette.py`, offer the logo-derived template first for approval, plus presets or the user's own colours (same section). Never pick colours on the user's behalf.

---

### Phase 2 — Content extraction

Read the TD file and map its sections to slide content. Every claim in the deck must trace back to the TD — do not invent, editorialize, or add information not present in the source document.

#### When template.pptx is present

Check for the slide-mapping file in this order:

1. **`docs/td-decks/samples/specific_instructions.md`** — the user's filled-in version for their specific template. If present, read it and follow it exactly. It contains the slide-by-slide mapping, which TD sections feed which slides, slide count limits per section, and which slides require user input rather than TD content.

2. **`.claude/skills/td-deck/specific_instructions.md`** — the starter template shipped with the skill. If the user-filled version doesn't exist yet, read this one. Then tell the user:
   > "I used the starter `specific_instructions.md` from the skill's defaults — it's a generic template, not calibrated to your actual slide layout. For better results, copy `.claude/skills/td-deck/specific_instructions.md` to `docs/td-decks/samples/specific_instructions.md` and customize the slide mapping to match your `template.pptx`."

If neither file exists, fall back to inspecting the template directly: read each slide's title placeholder to infer its purpose, then apply general judgment to map TD sections to slides. Note any slides whose purpose cannot be satisfied from the TD and flag them for the user.

Regardless of source: **replace** any instructional or guidance text already in template content placeholders with real content — do not preserve or display it.

#### When no template is present

Use the default outline defined at the end of this skill.

**Numbers must be verbatim from the TD** regardless of template presence. "92% accuracy" not "~90%" or "over 90%."

**Assertion titles.** Each content slide gets a title that states its point as a short sentence (per `../deck-style.md` §2) — e.g. `Adaptive batching cuts inference latency by 38%`, not `Results`. Exception: when `template.pptx` / `specific_instructions.md` fixes a slide's title text, keep the template's title and put the assertion as the first line of the body.

**Copy rules vs. TD wording.** The anti-slop vocabulary bans apply to wording you write. If the TD itself uses a banned word as a technical term (e.g. "robust estimator"), keep it verbatim and pass it to the linter with `--allow`. Don't import the TD's promotional adjectives ("novel", "innovative") onto slides — show the novelty through the mechanism instead.

**Core message.** Open the content map with one sentence stating the TD's contribution (usually its key-novelty claim) and the 3–5 points that support it (`../deck-style.md` §2). Every slide serves one of them.

**Source lines.** Results, benchmark and prior-art slides carry a small `Source: …` line citing the TD section, table or reference the numbers come from.

**Layouts.** Without a template, give each slide a layout from `../deck-style.md` §4 (e.g. a headline result as Big number, the contribution as Statement) and avoid long runs of bullet slides.

Share the extracted content map (core message, then slide-by-slide: role, title, layout, content summary) with the user and get approval via **AskUserQuestion** — one question with 2–3 options tailored to this map (e.g. **Build it** / **Adjust the mapping** / **Revise the claims**), never a prose "shall I build it?". This is the cheapest point to catch mistakes. If the mapping includes synthesized content (e.g. patent claims), present those drafts here too for confirmation before slide generation.

---

### Phase 3 — Generate the deck

Once the content map is confirmed:

- Load `docs/td-decks/samples/template.pptx` if found; otherwise use the default visual system in `../deck-style.md` §4, including the brand frame and the big-type title, divider and closing slides (with a template, use the template's own cover and divider layouts instead)
- Borrow layout and density cues from other `.pptx` files in `docs/td-decks/samples/` if present
- Every shape you add follows the visual bans in `../deck-style.md` §3 — no eyebrows, badges, shadows, rounded corners, icon-card grids
- One idea per slide. If a slide needs more than ~5 bullets or ~50 words of body text, split it
- Speaker notes on every slide — full spoken sentences, presenter script, same copy rules as the slides
- Use canonical terminology from the TD throughout — no paraphrasing of technical terms
- Apply diagram placeholders (per `../deck-style.md` §4) for any architecture, flow, or schema slide:
  - An outline-only rectangle filling the diagram area
  - Centered text: `[ DIAGRAM PLACEHOLDER ]`
  - Below: one-line description of what the diagram should show
  - In speaker notes: a detailed brief covering which components appear and how they connect

---

### Phase 4 — Quality gate

Run the full quality gate in `../deck-style.md` §5:

1. `python3 <suite-dir>/lint_deck.py docs/td-decks/<file>.pptx --max-words 50` — add `--template` if the deck was built on `template.pptx`, and `--allow` for TD terms that hit the vocabulary ban. Fix and regenerate until exit code 0.
2. Render check, if `soffice` and `pdftoppm` are installed; otherwise skip and note it. With a template, look especially for leftover template guidance text and content overflowing the template's placeholders.
3. Editing pass (titles, claims, 8-second test, cuts, any-topic test, rhythm).

---

### Phase 5 — Hand off

Mention the full path of the generated file directly so the user can open it immediately.

Then provide a short written summary:
- Filename and location
- Slide count and section breakdown
- List of diagram placeholders still to be filled in
- Whether `docs/td-decks/samples/template.pptx` was used
- Whether style reference decks were available in `docs/td-decks/samples/` — if not, flag that visual calibration was done without house-style samples
- Anything in the TD that was ambiguous and required a judgment call during content extraction
- Quality gate result: lint errors/warnings remaining (with reasons), and whether the render check ran or was skipped (and why)

---

## Default outline

Used when no template is found and the user picks option (a). Standard structure for an IP review board + technical reviewer audience (10–12 slides). The bold names are slide **roles**, not titles — each content slide still gets an assertion title:

1. **Title** — TD title, authors/inventors, project name, date
2. **Overview** — one-slide abstract: what the contribution is, in plain language
3. **Problem & motivation** — what gap or limitation does this address
4. **Prior art** — what exists today and why it's insufficient (condensed; 4–6 bullets max)
5. **Key contribution** — the novelty claim, stated directly. Lead with the innovation
6. **Technical approach** — how it works at a high level (diagram placeholder)
7. **Architecture / components** — deeper technical breakdown (diagram placeholder)
8. **Results** — evaluation metrics, concrete numbers, baseline comparisons if available
9. **Conclusion** — implications and where else the contribution applies; don't just repeat earlier slide titles
10. **References** — condensed, IEEE-style

Optional additions (discuss with user in 1c):
- Challenges slide (between Prior art and Key contribution)
- Deployment model slide (after Architecture)
- Future work slide (before Conclusion)

---

## Things to get right

- **Content must come from the TD.** No invented claims, no paraphrased metrics, no added context.
- **Numbers are verbatim.** Copy them exactly as they appear in the TD.
- **Confirm the content map before generating.** Slide generation is harder to undo than an outline adjustment.
- **Diagram placeholders are real placeholders.** No ASCII art or auto-shapes.
- **Terminology matches the TD exactly.** Inconsistency signals the deck and document were generated separately.

## Things to avoid

- Generating slides without a confirmed TD file that actually exists on disk
- Adding information not present in the TD
- Rounding or softening numbers from the TD
- Generating the deck without confirming the content map first
- Filling diagram slots with ASCII art or auto-generated shapes
- Saving output into the `td/` directory — decks go in `td-decks/` (or equivalent)
- Using the pitch-deck skill's product-pitch framing — this is a research/IP presentation, not a pitch
- Topic-label titles ("Results", "Approach") on slides whose title you control
- Promotional adjectives ("novel", "innovative", "powerful") in place of the actual mechanism or number
- Explanations, causes or implications the TD doesn't state — an assertion title must be supported by the TD
- Prior-art or benchmark tables where the contribution wins every row by construction — show where baselines are stronger if the TD reports it
- Restyling or deleting template elements to satisfy the visual bans — the bans cover only shapes you add
- Delivering a deck that fails the linter
