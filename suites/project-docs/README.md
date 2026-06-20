# Claude Skills Suite: Documentation, Pitch Deck, TD, TD Deck

A set of Claude Code skills for generating four kinds of project deliverables:

- **`documentation/`** — versioned release documentation: User Guide and Technical Guide (`.docx`)
- **`pitch-deck/`** — slide decks (`.pptx`): pitch decks for external audiences, status decks, and release-showcase decks tied to a specific version
- **`td/`** — Technology Disclosures: short research-paper-style documents for IP/disclosure purposes
- **`td-deck/`** — presentation decks (`.pptx`) derived from a completed TD, for IP review board and technical reviewer audiences

All three skills share a common context file: **`project_context.md`** in this directory. That file is the single source of truth for what your project is — name, components, terminology, repo layout. Every skill reads it before doing anything else.

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
rsync -av --exclude='project_context.md' \
  suites/project-docs/ /path/to/your-project/.claude/skills/
```

The `--exclude` flag preserves your filled-in `project_context.md` — that's the only file you customize that lives in the suite root. Everything else (SKILL.md files, samples READMEs) re-syncs freely. Your private files in `samples/` directories are safe because they're gitignored in skillet and will never appear in the rsync source.

After install, your project's layout will look like:

```
your-project/
├── docs/                               ← created automatically on first skill invocation
│   ├── td/
│   │   └── samples/                   ← drop your org's reference TDs here
│   ├── td-decks/
│   │   └── samples/                   ← drop template.pptx and reference decks here
│   ├── releases/
│   │   └── samples/                   ← optional: reference docs for style calibration
│   └── decks/
│       └── samples/                   ← optional: reference .pptx files for visual cues
└── .claude/
    └── skills/
        ├── README.md                   ← from this suite
        ├── project_context.md          ← from this suite (fill in for your project)
        ├── documentation/SKILL.md
        ├── pitch-deck/SKILL.md
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
> docs/releases/samples/
> docs/decks/samples/
> ```

**Cherry-picking individual skills:** if you only want some of the four, you can copy just those subfolders — but you still need `project_context.md`, since every skill reads from it. Note that `td-deck` depends on output from the `td` skill — installing one without the other is possible but you'll need to point it at a TD file manually.

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

3. **Skills auto-trigger.** You don't need to invoke them explicitly. Phrases like "create the user guide for v2.0" or "make me a pitch deck" or "write up a TD on this" will activate the right skill automatically. The YAML frontmatter `description` field in each `SKILL.md` controls what phrases trigger it.

4. **Bootstrap happens automatically on first invocation.** Each skill checks for its output directory (`docs/td/`, `docs/td-decks/`, `docs/releases/`, `docs/decks/`) at the start of every run. If the directory doesn't exist, the skill creates it along with a `samples/` subdirectory and pauses to tell you what to put there. This happens once per skill, the first time you use it in a project.

5. **Drop samples before first use — or tell the skill to proceed without them.**
   - **TD skill:** drop at least one sample TD (`.pdf` or `.docx`) into `docs/td/samples/`. The skill calibrates tone, structure, and citation style against them. Without samples, it will ask whether to proceed with abstract conventions only.
   - **TD Deck skill:** drop your organization's PowerPoint template into `docs/td-decks/samples/template.pptx`. Also copy `.claude/skills/td-deck/specific_instructions.md` to `docs/td-decks/samples/specific_instructions.md` and customize the slide-by-slide mapping to match your template.
   - **Documentation skill:** optionally drop reference `.docx` files into `docs/releases/samples/` for style calibration. Not required — the skill will use the most recent release doc as its style reference once one exists.
   - **Pitch Deck skill:** optionally drop reference `.pptx` files into `docs/decks/samples/` for visual cues. Not required — the skill generates a clean modern default without them.

---

## How the skills relate

```
                  project_context.md
                  (shared facts)
                         │
              ┌──────────┼──────────┐
              │          │          │
       documentation  pitch-deck   td ──────► td-deck
       (User Guide,  (all slide   (Tech        (TD presentation
        Tech Guide   decks:        Disclosures, deck for IP review
        — .docx      pitch/        research-    board — reads the
        only)        status/       paper style) TD file as input)
                     release
                     showcase)
```

`td-deck` is the only skill with a hard dependency on another: it requires a completed TD file as input. All other skills are independent — you can adopt any one without the others. Skills cross-reference each other in their `description` fields only to make sure each triggers on the right phrases and not on phrases that belong to a sibling.

---

## Customizing

These skills are written to be generic. Common customizations:

- **Project name and components:** all of this lives in `project_context.md` — never hardcoded in the skill files.
- **Filename patterns:** skills auto-detect from existing files in `documentations/` (or equivalent) on first run. You can also tell them explicitly the first time.
- **Trigger phrases:** edit the `description:` field in any `SKILL.md` if you find a skill under-triggering or over-triggering. The description is what Claude reads to decide whether to load the skill body.
- **TD samples:** drop your organization's TDs into `docs/td/samples/` (created on first run).
- **TD Deck template and samples:** drop your PowerPoint template as `docs/td-decks/samples/template.pptx` and any reference decks alongside it. Copy and customize `specific_instructions.md` to `docs/td-decks/samples/specific_instructions.md` for your specific template's slide mapping.
- **Style deviations from samples** (the TD skill has this for competitor naming): add explicit notes in the skill if your org has rules that intentionally diverge from what the samples show.

---

## File overview

**Skill files (in `.claude/skills/` inside your project):**

```
.claude/skills/
├── README.md                      ← this file
├── project_context.md             ← shared project facts (REQUIRED, fill in first)
├── documentation/
│   └── SKILL.md
├── pitch-deck/
│   └── SKILL.md
├── td/
│   ├── SKILL.md
│   └── review-rubric.md           ← Level 3 reference; loaded only during Phase 3 self-review
└── td-deck/
    ├── SKILL.md
    └── specific_instructions.md   ← starter template for slide mapping; copy to docs/td-decks/samples/ and customize
```

**Project output and samples (in `docs/` inside your project — created automatically):**

```
docs/
├── td/
│   ├── samples/                   ← drop reference TDs here (gitignore this dir)
│   └── <generated TD files>
├── td-decks/
│   ├── samples/                   ← drop template.pptx, reference decks, specific_instructions.md (gitignore)
│   └── <generated deck files>
├── releases/
│   ├── samples/                   ← optional: reference docs for style calibration (gitignore)
│   └── <generated User/Technical Guide .docx files>
└── decks/
    ├── samples/                   ← optional: reference decks for visual calibration (gitignore)
    └── <generated pitch deck .pptx files>
```