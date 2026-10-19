# Claude Skills Suite: Documentation, TD, TD Deck

A set of Claude Code skills for generating three kinds of project deliverables:

- **`documentation/`** — versioned release documentation: User Guide and Technical Guide (`.docx`)
- **`td/`** — Technology Disclosures: short research-paper-style documents for IP/disclosure purposes
- **`td-deck/`** — presentation decks (`.pptx`) derived from a completed TD, for IP review board and technical reviewer audiences

The skills share a common context file: **`project_context.md`** in this directory. That file is the single source of truth for what your project is — name, components, terminology, repo layout. Every skill reads it before doing anything else.

---

## Installing the suite into your project

Claude Code looks for skills at `.claude/skills/<skill-name>/SKILL.md` in your project's repo. To install this suite, copy the entire contents of this directory into your project's `.claude/skills/`:

```bash
# From the root of this skills repo:
mkdir -p /path/to/your-project/.claude/skills
cp -r suites/project-docs/. /path/to/your-project/.claude/skills/
```

…or with rsync (useful when re-syncing after updates, since it leaves your project-specific files alone):

```bash
rsync -av suites/project-docs/ /path/to/your-project/.claude/skills/
```

Then, open Claude Code, and let him know to do bootstrap. Then, it will create the `docs/` and its subdirectories within your project (after your approval). This concludes the basic "installation" step. 

After install, your project's layout will look like:

```
your-project/
├── docs/                               ← created automatically on first skill invocation
│   ├── assets/
│   │   └── logos/                     ← shared: drop your org logo(s) here (TD cover + header)
│   ├── td/
│   │   └── samples/                   ← drop your org's reference TDs here
│   ├── td-decks/
│   │   └── samples/                   ← drop template.pptx and reference decks here
│   ├── documentation/
│   │   └── samples/                   ← optional: reference docs for style calibration
│   └── decks/
│       └── samples/                   ← optional: reference .pptx files for visual cues
└── .claude/
    └── skills/
        ├── README.md                   ← from this suite
        ├── project_context.md          ← from this suite (fill in for your project)
        ├── deck-style.md               ← shared anti-slop rules for both deck skills
        ├── lint_deck.py                ← shared deck linter (quality gate)
        ├── icon_to_png.py              ← shared: renders Lucide icons for deck slides
        ├── logo_palette.py             ← shared: suggests a deck colour template from the company logo
        ├── style_from_reference.py     ← shared: extracts a style, or a reusable layout catalogue, from a reference .pptx
        ├── documentation/SKILL.md
        ├── td/
        │   └── SKILL.md
        └── td-deck/
            ├── SKILL.md
            └── specific_instructions.md  ← starter template; copy to docs/td-decks/samples/ and customize
```

> **Note:** The `docs/` directories are **not** part of the skill install — they live in your project root and are created automatically the first time each skill runs (see "Bootstrap" below). The `docs/*/samples/` subdirectories hold user-provided reference material and should be added to your project's `.gitignore`:
> ```
> docs/td/samples/
> docs/td-decks/samples/
> docs/documentation/samples/
> ```

**Cherry-picking individual skills:** if you only want some of the three, you can copy just those subfolders — but you still need `project_context.md`, since every skill reads from it. Note that `td-deck` depends on output from the `td` skill — installing one without the other is possible but you'll need to point it at a TD file manually.

---

## Getting started

1. **Fill in `project_context.md`.** Until you do, the skills will keep stopping to ask you about basic facts. Spending the time on this file once saves hours later. Look for the `<fill in: ...>` markers and replace them. Rename the numbered `Component N` placeholders to whatever fits your project (e.g. "API Server", "Worker", "Database", "Pipeline X"), and add or remove entries as needed.

   You have two ways to fill it in:

   **Option A — Fill it in manually.** Read your own code, README, and existing docs, then write the answers in yourself. Best when you know the project well and want maximum control over wording, especially for the canonical terminology table (which encodes naming conventions the skills will enforce consistently across all generated documents).

   **Option B — Delegate to Claude Code.** Open a fresh Claude Code session in the repo and ask it to fill the file in for you. A prompt that works well:

   > "Read this repo's code, README, and any existing documentation. Then open `.claude/skills/project_context.md` and fill in every `<fill in: ...>` placeholder based on what you find. Important: if you cannot determine something from the repo with reasonable confidence, leave the placeholder unfilled and add a comment noting what you couldn't determine — do NOT guess. For the canonical terminology table, scan the codebase for the actual terms used in variable names, comments, and docstrings rather than picking plausible-sounding ones. When done, list anything you left unfilled or were unsure about so I can answer."

   Option B is faster and usually produces a decent first draft, but review the output — Claude can misread architecture, miss terminology nuances, or fill placeholders too confidently if not prompted to be honest about gaps. The "don't guess, flag gaps" instruction in the prompt above is the most important part.

   Whichever option you pick, treat `project_context.md` as a living file — update it when components, terminology, or scope change.

2. **Wire `project_context.md` into your `CLAUDE.md`** so every Claude Code session in this repo has the project facts loaded by default:
   ```markdown
   @.claude/skills/project_context.md
   ```
   (Plus any other context files you load — code conventions, contributing guidelines, etc.)

3. **Skills auto-trigger.** You don't need to invoke them explicitly. Phrases like "create the user guide for v2.0" or "write up a TD on this" will activate the right skill automatically. The YAML frontmatter `description` field in each `SKILL.md` controls what phrases trigger it.

4. **Bootstrap happens automatically on first invocation.** Each skill checks for its output directory (`docs/td/`, `docs/td-decks/`, `docs/documentation/`) at the start of every run. If the directory doesn't exist, the skill creates it along with a `samples/` subdirectory and pauses to tell you what to put there. This happens once per skill, the first time you use it in a project.

5. **Drop samples before first use — or tell the skill to proceed without them.**
   - **TD skill:** drop at least one sample TD (`.pdf` or `.docx`) into `docs/td/samples/`. The skill calibrates tone, structure, and citation style against them. Without samples, it will ask whether to proceed with abstract conventions only. Optionally drop your organization's logo into `docs/assets/logos/` (a shared asset directory created at bootstrap) — it goes on the cover page and in the page header of the final `.docx`. The deck skills use the same logo, and suggest a deck colour template from it. The `.docx` step needs both `pandoc` and `python-docx` installed, and offers to install them if missing.
   - **TD Deck skill:** drop your organization's PowerPoint template into `docs/td-decks/samples/template.pptx`. Also copy `.claude/skills/td-deck/specific_instructions.md` to `docs/td-decks/samples/specific_instructions.md` and customize the slide-by-slide mapping to match your template.
   - **Documentation skill:** optionally drop reference `.docx` files into `docs/documentation/samples/` for style calibration. Not required — the skill will use the most recent release doc as its style reference once one exists.

6. **Optional: install LibreOffice and poppler** (`soffice`, `pdftoppm`) and Pillow for the two deck skills. With them, each deck is rendered to images and visually checked before hand-off, and the title and divider slides get icons; without them, those steps are skipped and the hand-off says so.

---

## How the skills relate

```
                  project_context.md
                  (shared facts)
                         │
              ┌──────────┴──────────┐
              │                     │
       documentation          td ──────► td-deck
       (User Guide,         (Tech        (TD presentation
        Tech Guide           Disclosures, deck for IP review
        — .docx              research-    board — reads the
        only)                paper style) TD file as input)
```

`td-deck` is the only skill with a hard dependency on another: it requires a completed TD file as input. All other skills are independent — you can adopt any one without the others. Skills cross-reference each other in their `description` fields only to make sure each triggers on the right phrases and not on phrases that belong to a sibling.

---

## Deck quality (td-deck)

The deck skill follows `deck-style.md`: a one-sentence core message per deck, assertion-style slide titles that never claim more than the source supports, sentence case, no em dashes, a banned list of AI-slop vocabulary, varied slide layouts instead of bullet after bullet, a consistent brand frame (header and footer bands) with big-type title and divider slides, and visual bans, and a deterministic script to extract that style from a reference deck when one exists (no eyebrow labels, badges, shadows, rounded corners, gradients, icon-card grids, stat-tile dashboards, page counters or AI-default palettes). When a `template.pptx` or reference deck is used, its styling wins; the bans then apply only to shapes the skill adds. Before hand-off, the deck must pass `lint_deck.py`:

```bash
python3 .claude/skills/lint_deck.py docs/td-decks/<file>.pptx [--template] [--max-words N] [--allow TERM ...]
```

To tune the rules for your org (e.g. allow a word that is part of your product's vocabulary), edit the banned list in both `deck-style.md` and `lint_deck.py`, or pass `--allow`.

The general-purpose slide-deck skill, `pitch-deck`, is no longer part of this suite: it builds a deck from an `outline.md` and lives on its own at [`skills/pitch-deck/`](../../skills/pitch-deck/SKILL.md).

---

## Customizing

These skills are written to be generic. Common customizations:

- **Project name and components:** all of this lives in `project_context.md` — never hardcoded in the skill files.
- **Filename patterns:** skills auto-detect from existing files in `documentations/` (or equivalent) on first run. You can also tell them explicitly the first time.
- **Trigger phrases:** edit the `description:` field in any `SKILL.md` if you find a skill under-triggering or over-triggering. The description is what Claude reads to decide whether to load the skill body.
- **TD samples:** drop your organization's TDs into `docs/td/samples/` (created on first run).
- **TD logo:** drop a `.png`/`.jpg` logo into `docs/assets/logos/` (shared across skills, created at bootstrap) for the `.docx` cover page and page header. One file is used automatically; multiple prompts you to pick; none prompts you to continue without one or add a file.
- **TD Deck template and samples:** drop your PowerPoint template as `docs/td-decks/samples/template.pptx` and any reference decks alongside it. Copy and customize `specific_instructions.md` to `docs/td-decks/samples/specific_instructions.md` for your specific template's slide mapping.
- **Style deviations from samples** (the TD skill has this for competitor naming): add explicit notes in the skill if your org has rules that intentionally diverge from what the samples show.

---

## File overview

**Skill files (in `.claude/skills/` inside your project):**

```
.claude/skills/
├── README.md                      ← this file
├── project_context.md             ← shared project facts (REQUIRED, fill in first)
├── deck-style.md                  ← td-deck's copy rules, visual bans, default style, quality gate
├── lint_deck.py                   ← deck linter run by td-deck before hand-off (exit 1 on anti-slop violations)
├── icon_to_png.py                 ← renders a Lucide icon to a recoloured PNG for divider/title slides (optional)
├── logo_palette.py                ← analyses the logo in docs/assets/logos/ and proposes brand + highlight colours for approval
├── style_from_reference.py        ← extracts a style from a reference .pptx (also shipped with `skills/pitch-deck/`)
├── CREDITS.md                     ← attribution for the adapted deck-style rules
├── documentation/
│   └── SKILL.md
├── td/
│   ├── SKILL.md
│   ├── review-rubric.md           ← Level 3 reference; loaded only during the self-review phase
│   ├── docx-generation.md         ← Level 3 reference; loaded only during the .docx phase
│   └── build_td_docx.py           ← generator: cover page, TOC, header/footer, page numbers, justified body
└── td-deck/
    ├── SKILL.md
    └── specific_instructions.md   ← starter template for slide mapping; copy to docs/td-decks/samples/ and customize
```

**Project output and samples (in `docs/` inside your project — created automatically):**

```
docs/
├── assets/
│   └── logos/                     ← shared: drop your org logo(s) here (TD cover + header)
├── td/
│   ├── samples/                   ← drop reference TDs here (gitignore this dir)
│   └── <generated TD files>
├── td-decks/
│   ├── samples/                   ← drop template.pptx, reference decks, specific_instructions.md (gitignore)
│   └── <generated deck files>
├── documentation/
│   ├── samples/                   ← optional: reference docs for style calibration (gitignore)
│   └── <generated User/Technical Guide .docx files>
```