# Skill Design Principles

Source: [What You're Actually Writing When You Write a SKILL.md](https://internals.laxmena.com/p/what-youre-actually-writing-when) by Lax Meiyappan

---

## The core insight: SKILL.md is a loader specification, not a prompt

A SKILL.md file is not a static block of text that gets fed to the model. It is a **loading specification** — it controls what gets loaded into context, when, and at what level of detail. Writing a skill well means understanding this architecture, not just writing clear instructions.

The kitchen metaphor:
- **Frontmatter** = the pinboard — always visible, routes decisions
- **SKILL.md body** = the recipe — pulled on demand when the skill fires
- **Reference files** = cookbook pages — consulted selectively during execution
- **Scripts** = appliances — not read, just run; only their output enters context

---

## Three loading levels

### Level 1 — Frontmatter (always loaded, ~100 tokens per skill)
The `name` and `description` fields are loaded **every turn** for every installed skill. This is the routing layer — the model reads all frontmatter to decide which skill applies. Implications:
- Keep `description` precise and unambiguous — it does double duty as routing logic
- Every word in `description` costs tokens on every turn, even when the skill isn't active
- Do not put content here that belongs in the body

### Level 2 — SKILL.md body (loaded on invocation, max ~500 lines)
The body is loaded only when the skill fires. This is the procedural instruction layer. Implications:
- **500 lines is the recommended ceiling.** Beyond that, consider splitting into reference files.
- Put the workflow here — phases, steps, decision trees, style rules
- Do not put content here that is only needed for specific sub-tasks; defer it to Level 3

### Level 3 — References and scripts (loaded on demand)
External files the skill reads selectively during execution, and scripts whose output (not source) enters context.
- Reference files: markdown files loaded when a specific branch of the workflow needs them
- Scripts: run via Bash; only stdout enters the context window
- This is how a 1,200-line monolithic skill becomes a 180-line spine with identical output at 1/3 the context cost

---

## The efficiency case for progressive disclosure

A real restructure documented in the source article:
- **Before:** 1,200-line monolithic SKILL.md — consumed 20% of the context window on every invocation
- **After:** 180-line spine + 3 reference files — consumed 7% of the context window
- **Result:** Identical output, 3× less context burned

The key move: identify what's always needed (the spine) versus what's conditionally needed (reference files loaded only when that branch fires). Most skills have a small always-needed core and a larger conditionally-needed body.

---

## Antipatterns to avoid

### 1. Frontmatter on reference files
Adding `name` and `description` YAML frontmatter to a file that is meant to be a reference (not a top-level skill) promotes it to Level 1 — it gets loaded every turn and participates in routing. Only `SKILL.md` files should have frontmatter.

### 2. Monolithic skills
Cramming everything into one file wastes context on content that isn't relevant to the current task. If a skill has conditional branches, the content for each branch should live in a reference file loaded only when that branch is active.

### 3. Hardcoded paths
Assumptions about workspace structure (`/src/components/`, `.claude/skills/td/samples/`) break portability. Use relative paths (`./samples/`) and runtime discovery (check common locations, ask if ambiguous).

### 4. Missing environment gotchas
Environment-specific constraints — build directories in monorepos, required dependencies, OS-specific commands — must be documented explicitly. The model cannot infer them from the skill's logic.

### 5. No evaluation strategy
Skills drift when the underlying model changes. A more capable model interprets instructions differently rather than following them literally — it may over-extrapolate or under-constrain. Skills tuned on one model are calibrated to that model's compliance characteristics, not just its capabilities. Without benchmarks or example outputs to test against, model upgrades silently degrade skill performance for specialized outputs (personal voice, org-specific style, strict format compliance).

---

## Practical guidelines for this repo

When building or reviewing a skill:

1. **Frontmatter `description`** — is it precise enough to route correctly? Does it name trigger phrases explicitly, including the `/skill-name` form? Does it list DO NOTs to prevent collisions with sibling skills?

2. **Body length** — is this approaching 500 lines? If so, identify the conditional branches and extract them to reference files in the skill directory.

3. **Level 3 opportunities** — is there content (detailed rubrics, sample formats, style guides) that is only needed for one branch? Move it to a reference file and have the skill load it with a Read call.

4. **Paths** — are all paths relative (`./samples/`, `../project_context.md`)? No hardcoded absolute or installation-assumed paths?

5. **Dependencies** — does the skill require external tools (python-pptx, python-docx, pandoc)? They must be in a Prerequisites section. Never reference "built-in capabilities" that don't exist.

6. **On activation** — does the skill announce itself? Users need to know the skill fired, especially when it leads with questions.

7. **Argument-hint** — is there a single clear piece of information the skill needs before it can start? If yes, add `argument-hint`.

8. **Credits** — is this adopted from another source? Credits go in `CREDITS.md` alongside `SKILL.md`, never inside the skill body itself.
