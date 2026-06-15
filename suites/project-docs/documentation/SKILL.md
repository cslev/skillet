---
name: documentation
argument-hint: "Version to document (e.g. v2.0)"
description: Generate or update versioned release documentation — User Guide (.docx) and Technical Guide (.docx) — for a specific release of the project. Trigger whenever the user mentions creating, updating, generating, refreshing, or producing documentation, a user guide, technical guide, release notes, version docs, or "what's new" docs for a specific release — even when phrased casually ("docs for the new release", "write up the changes", "update the guide"). Also trigger when the user asks to compare documentation versions or summarize changes between versions for the documentation set. Do NOT trigger for pitch decks or change-summary slide decks (the pitch-deck skill handles all slide decks, including release showcases), Technology Disclosures (the td skill handles those), inline code comments, README edits, or docstring generation.
---

# Documentation Skill

This skill generates and updates the project's release documentation deliverables.

**Distinct from the `pitch-deck` skill**: that skill produces all standalone slide decks (pitch decks for external audiences, release showcase decks, status decks). This skill produces written `.docx` guides only — no decks.

**Distinct from the `td` skill**: that skill produces Technology Disclosures (research-paper-style documents for IP/disclosure purposes). This skill produces user-facing and engineer-facing release documentation.

## Deliverables

Each release produces two files:

1. **User Guide** — `.docx`, technical overview level
2. **Technical Guide** — `.docx`, internals-deep level

If a release-showcase slide deck is also wanted, that's the pitch-deck skill's job (mode (b) frame (i) — version-vs-version pitch deck). The two skills are designed to be used together when needed: this one for the prose docs, the pitch-deck skill for the deck.

Both guides target a technical audience. The User Guide explains *what the system does and how to operate it*; the Technical Guide explains *how it works internally*. Tone and structure should loosely match the previous versions in the project's documentation directory but improvements are welcome — do not slavishly copy formatting quirks.

---

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **Documentation skill activated.** I'll generate versioned User Guide and Technical Guide `.docx` files for your release.

Then proceed immediately to the workflow. No further preamble.

---

## Prerequisites

`python-docx` must be installed in the environment (`pip install python-docx`). All `.docx` reading and generation depends on it.

---

## Required reading before doing anything

Before writing any code or generating any file:

1. Read `../project_context.md` — authoritative facts about the project (name, components, terminology). Everything in the docs must be consistent with this file.
2. Determine where existing release documentation lives in this repo (commonly a directory called `documentations/`, `docs/releases/`, `release-docs/`, or similar) — see "Locating the docs directory" below.
3. Read the **most recent** existing doc of each type in that directory — for tone, structure, terminology, and filename patterns.

For producing the `.docx` files themselves, use `python-docx` via a Python script. If updating existing docs in place (rather than creating new versioned files), use `python-docx`'s revision-tracking support to apply tracked changes to the existing file.

If `../project_context.md` has placeholder `<fill in: ...>` markers still unfilled and they're relevant to the section being documented, stop and tell the user — the docs cannot be reliable until those are real.

---

## Locating the docs directory and filename pattern

This skill is project-generic. It does not assume a specific directory name or filename convention. Determine both at runtime:

1. **First, look for an obvious docs directory.** Check (in order): `documentations/`, `docs/releases/`, `release-docs/`, `docs/`. Use the first one that exists and contains files matching the pattern of release docs (versioned `.docx` files).

2. **If multiple plausible directories exist or none does**, ask the user where release docs should live.

3. **Read existing filenames in that directory** to infer the project's filename pattern. For example:
   - `MyProject_UserGuide_v1.2.docx` → pattern is `<ProjectName>_UserGuide_v<MAJOR>.<MINOR>.docx`
   - `userguide-v1.2.docx` → pattern is `userguide-v<MAJOR>.<MINOR>.docx`
   - `release-1.2/user-guide.docx` → pattern is `release-<MAJOR>.<MINOR>/user-guide.docx`

4. **If the directory is empty** (first release), ask the user what filename pattern they'd like, or propose a default based on the project name from `../project_context.md`:
   ```
   <ProjectName>_UserGuide_v<MAJOR>.<MINOR>.docx
   <ProjectName>_TechnicalGuide_v<MAJOR>.<MINOR>.docx
   ```

5. **Other documents in the same directory** (pitch decks from the pitch-deck skill, TDs, ad-hoc notes, slide decks of any kind) should be ignored for release-documentation work — filter to files matching the User Guide and Technical Guide patterns specifically.

---

## Workflow

### Step 1 — Determine the target version

Ask the user for the new version number (e.g. "v2.0") if it isn't already clear from the prompt or recent context. Do not guess. The version string drives output filenames and the "what's new" markers throughout the docs.

### Step 2 — Find the latest existing version of each doc

For each release-doc type (User Guide, Technical Guide), list the docs directory, filter to files matching the patterns identified above, and pick the file with the highest version number by parsing the version suffix. **Do not assume alphabetical sort gives the right answer** — `v1.10` sorts before `v1.2` alphabetically but is newer. Parse numerically.

If no previous version of a given doc type exists, treat this as a first release for that doc and generate from scratch — but still gather change context (Step 3) so the doc is grounded in actual current state.

### Step 3 — Gather change signal from all four sources

To determine what's new in this version, cross-reference **all of the following**, in this order:

1. **`CHANGELOG.md`** at repo root (or wherever the project's changelog lives — check `CHANGELOG`, `HISTORY.md`, `RELEASES.md` if `CHANGELOG.md` isn't there) — the user's curated source of truth. Read the section for the new version. If a section for the new version doesn't exist yet, ask the user whether to proceed using the other three sources only, or wait for the changelog to be updated.

2. **Git log since the previous release tag**:
   ```bash
   git log <previous-version-tag>..HEAD --oneline --no-merges
   ```
   If tags don't match an obvious pattern, fall back to `git log -n 100` and use commit dates to bracket the relevant window. Read full commit messages for any commit whose one-liner is ambiguous.

3. **Direct content diff of the previous-version docs** — extract text from the previous `.docx` (using python-docx) and compare conceptually against the current state of the code. The point is to find features documented in the old guide that have changed behavior, plus features that exist now but weren't documented before.

4. **Code inspection** — for anything still unclear after the first three sources, read the actual code in the repo. This is the tiebreaker when changelog / commits / old docs disagree.

If sources conflict, surface the conflict to the user before writing. Do not silently pick one.

### Step 4 — Build a change inventory

Before generating any document, produce an internal list of changes categorized as:

- **Added** — new in this version
- **Changed** — existed before but behaves differently now
- **Removed** — present in previous version, gone now
- **Fixed** — bug fixes worth mentioning to users
- **Internal** — refactors / changes invisible to users (Technical Guide only)

Share this inventory with the user as a short summary and ask them to confirm or correct before generating the final docs. This catches misattributions early.

### Step 5 — Generate the deliverables

For each deliverable, use `python-docx` to create and style the document. Use canonical terminology from `../project_context.md` throughout. Specifics:

**Marking what's new.** Anywhere a feature, parameter, output, or behavior is new or changed in this version, append a bracketed marker to the heading or first sentence:

- New feature: `[New in v<VERSION>]`
- Changed behavior: `[Changed in v<VERSION>]`
- Removed: `[Removed in v<VERSION>]` — used sparingly in the User Guide where the prior behavior was prominent enough that users need to know it's gone. Most removals belong in the Technical Guide's "Known limitations" or migration notes, not in the User Guide.

Place the marker immediately after the feature name in headings, like:

```
Feature 2 [New in v2.0]: <feature name>
```

For inline mentions in prose, the marker goes at the end of the sentence introducing the feature.

**User Guide structure** (loosely match the previous version; adapt to the project):
- Overview / purpose
- Installation & prerequisites
- Configuration
- Operation (sections for each major component or workflow)
- Outputs and where to find them
- Troubleshooting

**Technical Guide structure** (loosely match):
- Architecture overview (diagram if the previous version had one)
- Module-by-module breakdown
- Data flow
- Extension points / APIs
- Internal data structures
- Deployment notes
- Known limitations
- Migration notes (when behavior changed in a breaking way)

### Step 6 — Output handling (ASK BEFORE OVERWRITING)

Default output filenames follow the same pattern as the inputs (identified in "Locating the docs directory" above), with the new version number substituted.

**Before writing**, ask the user:

> "I'll generate two new files for v<NEW>. Should I:
> (a) create new versioned files alongside the existing ones (default), or
> (b) edit the existing v<PREVIOUS> files in place with tracked changes?"

If they pick (b), use the tracked-changes workflow when editing the existing `.docx` files.

### Step 7 — Hand off

Provide direct access to the generated files and a brief written summary:

- Which files were created/modified and where
- The change inventory used (so they can spot anything you got wrong)
- Anything flagged as uncertain during the process
- Anything in `../project_context.md` that was incomplete or that you had to fill in via user input — so the context file can be updated

---

## Things to get right

- **Version markers must be accurate.** A misplaced `[New in v2.0]` on a feature that existed in v1.x is worse than no marker. When in doubt, leave the marker off and flag it for the user to check.
- **Don't invent features.** If the change signal sources don't actually evidence a feature, don't document it. Ask the user.
- **Preserve terminology.** Use the canonical terms from `../project_context.md`. Consistency across versions matters for users searching the docs.
- **Keep the audience in mind.** Both guides are technical, but the User Guide stops at *how to use it*; the Technical Guide is where internals belong. Resist putting implementation detail in the User Guide.

## Things to avoid

- Generating docs without confirming the version number and change inventory first
- Overwriting files in the docs directory without asking
- Using alphabetical sort to find the "latest" version
- Marking everything as `[New in v<VERSION>]` without diffing — markers must reflect real diffs
- Generating slide decks of any kind — that's the pitch-deck skill's job; if the user asks for a "change summary deck" or "release deck," redirect to the pitch-deck skill (mode (b) frame (i))
- Pulling content or style cues from pitch decks or TDs in the same directory — those are for different audiences