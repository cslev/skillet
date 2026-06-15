# skillet

A collection of [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) skills and skill suites for various tasks.

## What's in this repo

The repo is organized into two top-level directories:

- **`suites/`** — coherent groupings of skills designed to be installed and used together. Each suite has its own README explaining what it does, how to install it into a project, and how the skills inside it relate to each other. Although, if you need one of them only, you might be able to reuse it individually - just that they come with a(n additional) common file they all refer to. Bring that file along.
- **`skills/`** — standalone skills that don't depend on suite-level context. Grab any one independently.

---

## Suites

### `suites/project-docs/` — Project documentation suite

Three skills for generating project deliverables, sharing a common `project_context.md` for project facts:

- **`documentation/`** — versioned release documentation (User Guide and Technical Guide, `.docx`)
- **`pitch-deck/`** — slide decks (`.pptx`): pitch decks, status decks, release-showcase decks
- **`td/`** — Technology Disclosures: short research-paper-style writeups for IP/disclosure purposes

See `suites/project-docs/README.md` for install instructions and usage.

<!-- Add more suites here as they're created. -->

---

## Standalone skills

<!-- List skills under skills/ here once any exist. Each entry: one line description + pointer to skills/<name>/SKILL.md. -->

- **`grill-me`** — one-question-at-a-time design/plan interview with a resumable `checkpoint.md`. Triggers on `/grill-me`, "grill-me", or "brainstorm". → [skills/grill-me/SKILL.md](skills/grill-me/SKILL.md)
- **`caveman`** — ultra-compressed ~75% token reduction mode that drops filler while keeping full technical accuracy. Triggers on `/caveman`, "caveman mode", or "less tokens". → [skills/caveman/SKILL.md](skills/caveman/SKILL.md)
- **`handoff`** — compacts the current conversation into a resumable handoff document saved to the OS temp dir, so a fresh agent can continue without re-reading the full chat. → [skills/handoff/SKILL.md](skills/handoff/SKILL.md)

---

## How Claude Code finds skills

Claude Code looks for skills at `.claude/skills/<skill-name>/SKILL.md` inside a project's repo. Skills auto-trigger based on the YAML frontmatter `description` field at the top of each `SKILL.md` — you don't need to invoke them by name.

To use anything from this repo in your own project, copy the relevant files into your project's `.claude/skills/` directory. Each suite's README explains the install for that suite specifically.

---

## Contributing

<!-- Fill in if you want contributions, or remove this section. -->

## License

<!-- Add a LICENSE file at the repo root. Common choices for skill collections: MIT, Apache 2.0, CC-BY. -->