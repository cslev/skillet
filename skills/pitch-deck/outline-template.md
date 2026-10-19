# <Deck title> — <event or audience> outline

<!--
Template for the outline the pitch-deck skill builds from. Copy it, fill it in, delete
the comments. Write it by hand or have an AI agent draft it from your documents; the
skill itself never reads your project, papers or code, only this file. Everything on a
slide comes from here: names, spellings, numbers, wording. If a term has a canonical
spelling, write it that way here and the deck will follow.
Keep slide numbers stable: "redo slide 13" refers to them.
-->

## Deck

- **Core message:** one sentence the audience should remember.
- **Supporting points:** 3–5, non-overlapping. Every slide should serve one.
- **Audience:** who, and how technical.
- **Length:** number of content slides, or a time slot.
- **Filename:** `<Name>_<YYYY-MM-DD>.pptx` (optional; default `<Deck title>_<date>.pptx`).
- **Template:** path to a `.pptx` (optional; else the lookup order in the skill: project `docs/decks/samples/`, then the skill's `assets/`).
- **Logo:** path (optional; else `docs/assets/logos/`, then the skill's `assets/`).
- **Off-limits:** anything not to show (NDA, unreleased, names).

The skill always adds a Thank-you slide at the end; don't list one.

---

## Slide 1 — Title as it appears on the slide

**Role:** title | divider | content | statement   <!-- statement = one claim, one sentence -->
**Layout hint:** text | text + visual | full-width visual | table | chart | big number | diagram   <!-- optional; the skill chooses if blank -->

**On slide:**
- Fragment bullets, no terminal periods, at most 5, about 12 words each
- Names, numbers and spellings exactly as they should appear

**Visual:** what goes next to or under the text. One of:
- a file path to a real image (`figs/fig5.png`), which the skill places;
- a description of an image you will supply later, which becomes an outlined placeholder (the skill never generates images);
- a diagram brief, which becomes a placeholder with the brief in the notes.

**Chart or table data:** give the numbers in a markdown table; the skill builds a native, editable chart or table from it. Say the chart type if it matters (bar, paired bar, scatter, log axis) and anything to annotate.

| Label | Value |
|---|---|
| A | 12.3% |

**Source:** where the numbers come from (`Table 4 of the paper`). Shown as a small line under the data.

**Speaker notes:** full spoken sentences. Also put here anything the audience shouldn't see on the slide.

---

## Slide 2 — Assertion titles state the point

<!--
Titles are assertions in sentence case, at most ~12 words, no ending punctuation,
no question titles, no "X: The Y of Z". Read in sequence they should tell the story.
Dividers: use at most two in a deck of 10 slides or fewer, only where the message splits.
Add `**Hidden:** yes` to a slide that should be in the file but skipped in the show.
-->
