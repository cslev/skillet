# skillet

A curated collection of Claude Code skills and skill suites.

## Repo structure

```
skills/          standalone skills (one per subdirectory)
  <name>/
    SKILL.md     the skill itself
    CREDITS.md   attribution — only present for adopted/adapted skills
suites/          coherent skill groupings with shared context
  <suite>/
    README.md    install instructions and inter-skill relationships
    <skill>/
      SKILL.md
```

## Skill anatomy

Each `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: kebab-case-name
description: >
  One or more sentences describing what the skill does AND when to trigger it.
  Be explicit: list /slash-command, "hyphenated-name", and key natural-language
  phrases the user might say (e.g. "brainstorm", "less tokens").
argument-hint: "Optional prompt shown when the skill accepts arguments."
---
```

The body is the instruction Claude follows when the skill fires. Keep it tight — the instructions are the deliverable, not the prose around them.

If the skill should announce itself on activation, add an **On activation** section at the top of the body with an exact announcement line.

## Adding a skill

### From scratch
1. Create `skills/<name>/SKILL.md` with frontmatter + body.
2. Add a one-liner entry to the **Standalone skills** table in `README.md`.

### Adopted from an external repo
1. Fetch the original (use the GitHub API for raw content when `gh` isn't available).
2. Copy to `skills/<name>/SKILL.md`. Adapt frontmatter/body as needed.
3. Create `skills/<name>/CREDITS.md`:
   - Source URL + date copied (absolute, e.g. `2026-06-15`)
   - One sentence: what the original provides vs. what this version adds or changes.
   - If copied verbatim: say so explicitly.
4. Add a one-liner entry to `README.md`.

Credits go in `CREDITS.md` only — never inside `SKILL.md`.

## README conventions

Each skill entry in `README.md` is one line:

```
- **`name`** — what it does + key triggers. → [skills/name/SKILL.md](skills/name/SKILL.md)
```
