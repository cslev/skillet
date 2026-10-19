# pitch-deck

Builds a `.pptx` deck from an **`outline.md`**, on your own PowerPoint template (its layouts, logo, icons) or a clean default style. Checks it with a linter and a render, always ends it with a Thank-you slide, and edits single slides in place.

It only acts on the outline. Writing the outline (by hand, or by an agent reading your docs, papers or code) is a separate step, and the skill does not do it. It never generates images: described images become outlined placeholders, and image files are placed.

## Install

Copy this folder into a project's `.claude/skills/`:

```bash
cp -r skills/pitch-deck /path/to/your-project/.claude/skills/
```

Needs `python-pptx`. Optional: LibreOffice and poppler (render check), Pillow (template and logo analysis). Missing tools are skipped, never installed for you.

## What you give it

1. **`outline.md`** (required): see [`outline-template.md`](outline-template.md). Each slide has a role, an assertion title, the text for the slide, a visual (file, or a description for a placeholder), chart or table data as markdown tables, a source, and speaker notes. Names, spellings and terms in the outline are used exactly; the outline is the only source of content.
2. **A template `.pptx`** (optional): put it in `docs/decks/samples/` or name it. The skill analyses it, finds its title, divider, content, table, closing and other layouts, and builds every slide from them. Without one it uses a default style and asks for your logo and brand colours.
3. **A logo** (optional, no template): `docs/assets/logos/`.

Output goes to `docs/decks/`.

## Using it

**Build:** "build the deck from outline.md", or "make slides from the outline using template.pptx". The skill first reports problems in the outline (structure, copy rules, claims the numbers don't support) with proposed fixes, which you accept or decline. It never rewords your text without asking. It then shows a slide-to-layout table for your approval, builds, and runs the quality gate.

**Thank-you slide:** always added last. The template's own closing layout is used if it has one; otherwise a styled one is built. It is not in the outline.

**Update a single slide.** Tell it what you want, in plain words:

- "redo slide 13" (after you changed that slide in `outline.md`)
- "update slide 7: add the new latency numbers"
- "change the chart on slide 15 to show X"
- "add a slide after 12 about Y", "delete slide 9", "move slide 5 after 8"

It works on the deck file as it is now, including your manual edits, never regenerates the whole deck, and proves the other slides are byte-for-byte unchanged (`slide_guard.py`). It reports which slide changed and that the slide count is as expected.

Slide numbers are positions in the deck as it is now; hidden slides count. If your outline numbers differ, say which you mean.

## What's in the folder

| File | Role |
|---|---|
| `SKILL.md` | the workflow Claude follows |
| `outline-template.md` | the outline format to copy |
| `deck-style.md` | copy rules, visual bans, default visual system, quality gate |
| `reference/layout-reuse.md` | analysing a template, mapping slides to its layouts, building from them |
| `deck_lib.py` | build and edit helpers (template opener, placeholders, native charts, tables, Thank-you slide, slide edit helpers) |
| `slide_guard.py` | snapshot and compare, to prove an edit touched only the intended slides |
| `lint_deck.py` | anti-slop linter, the gate before hand-off |
| `style_from_reference.py` | template analysis: fonts, colours, logo, layout catalogue |
| `logo_palette.py`, `icon_to_png.py` | brand colours from a logo; Lucide icons for big-type slides |

## Quality gate

`python3 lint_deck.py <deck.pptx> --max-words 60 [--template] [--allow TERM ...]` must exit 0. Add `--template` when built on a template; `--allow` terms from your outline that collide with the vocabulary bans. The render check converts the deck with LibreOffice and the skill looks at every page.
