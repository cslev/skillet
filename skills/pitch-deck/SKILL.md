---
name: pitch-deck
description: >
  Build a slide deck (.pptx) from an outline.md, on the user's PowerPoint template
  (its layouts, logo and icons) or a clean default style, then check it with a linter and a
  render. Also edits a deck it built: redo or change a single slide, add, remove or reorder
  slides, leaving every other slide untouched. Trigger on "make slides from the outline",
  "build the deck", "pitch deck", "conference slides", "slides for the talk", "redo slide 13",
  "update slide 7", "I changed the outline for slide 5", or when the user hands over an
  outline.md and a template. It only acts on an outline: it does not read project code,
  papers or docs to invent content, and it does not generate images. Do NOT use it to write
  the outline, write release docs or technology disclosures, or fill a fixed corporate
  template slide-for-slide.
argument-hint: "Path to outline.md, and optionally the template .pptx and logo."
---

# Pitch Deck skill

## On activation

Output exactly one line first:

> **Pitch Deck skill activated.** I'll build the deck from your outline, on your template if you have one.

Then go straight to the inputs.

## What this skill does and doesn't do

It turns an **outline** into a **`.pptx`**. Everything shown on a slide comes from the outline: wording, numbers, spellings, terms. The skill adds no facts and silently rewrites nothing. It reads no project code, papers or documentation; the outline can be written by hand or drafted by any agent, separately.

It never generates images. Images the outline describes become outlined placeholders; images it points to (files) are placed.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| **Outline** (`outline.md`) | yes | the user names it, or look for `outline.md` in the project root and `decks/`. See `outline-template.md` for the shape. |
| **Template** (`.pptx`) | no | see lookup order below. None found: use the default visual system. |
| **Logo** (PNG/JPG) | no | see lookup order below. Not asked about when a template is used. |

**Lookup order for the template and the logo**, first hit wins: (1) a path the user gives in the request; (2) the `Template:` / `Logo:` fields in the outline's front matter; (3) the project: `decks/templates/` (the newest `.pptx`) and `decks/logos/`. Nothing inside the skill's own folder is ever used as a default; `examples/` is for reference only. `decks/` always means a folder in the project, i.e. the directory Claude Code was started in, never the home directory or the skill folder. Say which file you picked and from where.

Output goes to `decks/` in the project (create it, with `decks/templates/` and `decks/logos/`, if missing, and tell the user). The filename comes from the outline, else `<title>_<YYYY-MM-DD>.pptx`.

Needs `python-pptx`. Optional: LibreOffice (`soffice`) and poppler (`pdftoppm`) for the render check; Pillow for the template analysis and the logo analysis. If something is missing, skip that step and say so; never install anything unprompted.

Read `reference/deck-style.md` now (copy rules, visual bans, default visual system, quality gate). Every rule there applies.

## Build mode

### Step 1: read the outline and check it

Read the whole outline. Do not start building until you have reported, in one message:

- **Structure problems:** a slide with no role or no title, chart data without numbers, a visual with no description, a missing core message.
- **Copy-rule conflicts**, each quoted with the proposed fix: topic-label titles, em dashes, banned vocabulary, terminal periods, question titles, arrows and other decorative glyphs, more than 5 bullets, titles that wrap badly.
- **Claims the source can't support:** a title or bullet that states a cause or consequence the outline's own numbers don't. Flag; don't fix.
- **Visuals needing the user:** images to be supplied later (placeholders), unreadable file paths.

Never apply a fix to the user's wording without their say-so. Ask once, with the full list, via **AskUserQuestion**: apply all proposed fixes / apply none, build as written / let me choose. Terms and spellings in the outline win over the vocabulary bans: pass them to the linter with `--allow`. If a name appears spelled two ways in the outline, ask which; don't pick.

### Step 2: analyse the template

If a template exists, read `reference/layout-reuse.md` and follow it: run `style_from_reference.py`, resolve its warnings, and render the layouts you intend to use. Ask the user: strict layout reuse (A) or style only (B), when both are plausible. Default to (A) for a real layout library.

No template: run the brand questions in `reference/deck-style.md` §4 (logo first, then colour template), one call each. Never pick a palette or skip the logo on the user's behalf.

### Step 3: map slides to layouts, get approval

Show a table: outline slide, role, assertion title, the layout you'll use (template layout name in (A); the five default layouts in (B)/none), and one line of content. Flag every slide with no good match and what you'll do instead. Add the always-last Thank-you slide as a row (template closing layout, or "styled, built by the skill").

Vary the layouts; no more than three consecutive slides with the same one. Dividers only where the outline has them.

Get approval through **AskUserQuestion** (never a prose "shall I build it?"): one question, "Build this deck, or adjust first?", with options tailored to this outline. Generate only after "Build it".

### Step 4: build

Write a Python script for this deck (keep it in the project, e.g. next to the outline, so single-slide edits can re-run it) and run it. Import the helpers:

```python
import sys; sys.path.insert(0, "<skill-dir>/scripts")
from deck_lib import *
```

`scripts/deck_lib.py` has the template opener, placeholder helpers, native charts with a manual plot layout (annotations can be positioned exactly), tables, placeholder boxes, the Thank-you slide, and the edit helpers. Read its docstrings before writing the script; use it instead of re-deriving python-pptx workarounds.

Rules while building:

- Content comes from the outline only. Bullets stay as written (after any approved fixes).
- Layout (A): fill placeholders by `idx`; never leave template guidance text; delete unfilled placeholders (`scrub_placeholders`); keep filled decorative panels. Layout (B): the brand frame from `reference/deck-style.md` §4.
- Data: native charts and tables built from the outline's numbers, values labelled, one claim per slide, a `Source: ...` line when the outline gives one (the origin, never the outline's filename). Numbers with no source are listed in the hand-off.
- Speaker notes on every slide: the outline's notes if given, else a short presenter script from the slide's own content. Put an image or diagram brief in the notes of every placeholder.
- Hidden slides (`**Hidden:** yes`): `deck_lib.set_hidden`.
- **Last, always: the Thank-you slide.** Template closing layout if it has one (`find_closing_layout`), else `add_closing` (styled, brand background, logo if any). It isn't in the outline and is the only slide you add on your own.

### Step 5: quality gate

1. `python3 <skill-dir>/scripts/lint_deck.py <deck.pptx> --max-words 60` (add `--template` in layout mode (A); `--allow` the outline's own terms). Fix and rebuild until exit 0; a fix that changes the user's wording goes back to the user first.
2. Render check, if `soffice` and `pdftoppm` exist: convert to PDF, render pages, **read every image**. Look for clipped or overlapping text, titles that jump, unfilled placeholders ("Click to add text"), half-empty slides, anything from the bans. Hidden slides are skipped in the PDF, so page numbers after one are off by one. A font that isn't installed makes text wider than it will be; judge fit with that in mind.
3. Editing pass (`reference/deck-style.md` §5): do the titles tell the story, does every number trace to the outline, the 8-second test, rhythm.

### Step 6: hand off

Full path of the file, then briefly: slide count and sections; the template mode used; every diagram, image and QR **placeholder** still to fill; numbers shown without a source; lint result (errors, and each warning you left and why); whether the render check ran; every outline fix you applied or declined; anything in the outline that was missing or ambiguous.

## Update mode

Triggered when a deck made by this skill already exists and the user asks for a change: "redo slide 13", "I changed the outline for slide 13, update it", "move slide 5 after 8", "add a slide after 12 about X", "delete slide 9", "fix the legend on slide 15".

The user may also have edited the deck by hand, so **work on the file as it is, never regenerate the whole deck.**

1. Identify the slide. Numbers are positions in the deck as it is now (hidden slides count); if the user means the outline's numbering and it differs, say which slide you'll edit. Confirm by title if there's any doubt (`find_slide`).
2. Take a backup copy of the deck (scratch directory) and a snapshot: `python3 <skill-dir>/scripts/slide_guard.py snapshot <deck> <snapshot.json>`.
3. If the change comes from the outline, re-read that slide's section only and run Step 1's checks on it alone.
4. Apply the change in place with `deck_lib`: `clear_slide` keeps the title, footer and source placeholders and removes what the earlier build added; rebuild the slide's content; keep the template layout and the title's formatting (`set_text`). Add, delete and move with `add_slide`, `delete_slide`, `move_slide`. Don't touch other slides, the master, or the theme.
5. Prove nothing else changed: `slide_guard.py compare <deck> <snapshot.json> --changed N` (and `--expect-count` when slides were added or removed). A failure means undo and redo.
6. Re-run the linter and render just the edited slide; read it.
7. Report: what changed on which slide, that the guard passed, the slide count, and any decision you made.

The Thank-you slide stays last. Adding a slide at the end goes before it.

## Things to get right

- **No invented facts, no silent rewording.** The outline is the contract. Flag problems; don't paper over them.
- **Exact spelling and terms from the outline**, on every slide and in the notes.
- **Placeholders honestly marked.** An outlined box with a label and a one-line brief, and the full brief in the notes. Never an AI-generated stand-in.
- **Native charts.** Editable PowerPoint chart objects, never images, never bars drawn from shapes.
- **Test with the template's real layouts**, not their names (`reference/layout-reuse.md`).

## Things to avoid

- Building before the outline is checked and the layout mapping approved.
- Reading project files for content, or filling a gap in the outline with a plausible guess. Ask or leave a visible placeholder.
- Adding sales arcs, "key takeaways" or "questions?" slides that the outline lacks. The Thank-you slide is the only addition.
- Regenerating the deck when asked to change one slide.
- Delivering a deck that fails the linter.
