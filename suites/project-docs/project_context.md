# Project Context

This file is the single source of truth for *what this project is*. It is read by reference from all skills in `.claude/skills/`, and should be loaded into `CLAUDE.md` for every Claude Code interaction in this repo.

**Update this file whenever the project's identity changes** — components renamed or added, scope expansion, terminology shifts. Do NOT duplicate this content into the skill files; they read from here.

---

## How to fill this file in

Two approaches. Both are valid; pick whichever fits how you work.

- **Manually**: read your own code, README, and existing docs, then replace each `<fill in: ...>` marker with the real answer. Best when you want full control over wording, especially the canonical terminology table — those terms get enforced consistently across every document the skills generate.
- **Delegate to a coding agent**: in a Claude Code session, ask the agent to scan the repo and populate the placeholders. Tell it explicitly to leave anything uncertain unfilled (with a brief note) rather than guess, and to surface ambiguities at the end. The agent should pull canonical terms from the actual code (variable names, comments, docstrings), not pick plausible-sounding ones. See the top-level `.claude/skills/README.md` for a recommended prompt.

When unsure, partial is better than wrong. The skills will ask about unfilled placeholders before generating anything important. Confidently-wrong content silently propagates into every document.

---

## What the project is

**Name:** _<fill in: project name as it should appear in filenames and documents>_
**One-liner:** _<fill in: one sentence describing what the system does>_
**Longer description:** _<fill in: 2–4 sentences covering the problem it solves, the kind of data or workload it handles, and who uses it>_

## Components

<!-- List each major component of your project. Rename "Component 1" etc. to whatever fits (e.g. "API Server", "CLI", "Worker", "Frontend", "Database", "Pipeline X"). Add or remove entries as needed — there's nothing magical about three. -->

### Component 1: _<rename>_
- Purpose:
- Inputs:
- Outputs:
- Key tech / libraries:

### Component 2: _<rename>_
- Purpose:
- Inputs:
- Outputs:
- Key tech / libraries:

### Component 3: _<rename>_
- Purpose:
- Inputs:
- Outputs:
- Key tech / libraries:

## Terminology (canonical names — always use these)

| Canonical term | Don't use |
|---|---|
| _<e.g. scrape job>_ | _<e.g. scraping task, crawl run>_ |
| | |

## Repo layout (high-level)

```
<fill in the top-level directories Claude should know about, with a one-line description of what each contains>
```

## External integrations

_<APIs consumed, data sources, deployment targets, etc.>_

## What this project is NOT

_<optional but useful — explicitly rule out misinterpretations. Examples: "Not a real-time monitoring tool; runs in batches.", "Not a SaaS product; deployed on-prem.">_