---
name: pitch-deck
argument-hint: "Purpose and audience, e.g. 'investor pitch', 'v2.0 release showcase for internal team', 'conference intro deck'"
description: Generate a pitch deck (.pptx) about the project for external audiences (investors, conferences, technical evaluators) OR a release-showcase deck highlighting what's new in a specific version. Trigger when the user mentions a pitch deck, investor deck, conference deck, project overview deck, status deck, release deck, change summary deck, "what's new" deck, or asks for slides about the architecture, components, database, or what's new across the project. Also trigger for phrases like "pitch the project", "slides for the conference", "deck about how it works", "status update deck", "weekly progress deck", "where we are now", "slides for v2.0", "release showcase". Do NOT trigger for written release documentation like User Guides or Technical Guides (the documentation skill handles those), Technology Disclosures (the td skill handles those), inline code comments, or general code explanation.
---

# Pitch Deck Skill

This skill generates pitch decks about the project.

**Distinct from the `documentation` skill**: that skill produces versioned release documentation with strict version-diffing logic. This skill produces standalone pitch decks. Pitch decks come in two modes: **(a) fresh introduction** for a new audience, or **(b) what's-new / release showcase** highlighting changes since a previous version. The user chooses the mode at the start of every run.

**Distinct from the `td` skill**: that skill produces Technology Disclosures (research-paper-style writeups). This skill produces persuasive/narrative slide decks. Different audience and different format.

## What this produces

A single `.pptx` pitch deck per request. Decks are generated fresh each time — there is no canonical version. The user may ask for the same deck repeatedly with different framing; treat each request as independent.

## Audience model

Default audience for project pitch decks: **mixed external audiences** (investors, conference attendees, prospects, technical evaluators). Often mostly non-technical with a technical minority who will push on the architecture and component sections.

Calibration this implies:
- **Opening framing is accessible.** Assume the reader doesn't know what the project does. No jargon in the first two slides.
- **The technical core is substantive, not hand-wavy.** Vague boxes labeled "AI MAGIC" or "PROCESSING" lose credibility. Technical attendees will spot them instantly.
- **No marketing fluff.** Sophisticated audiences spot it. State what the system does and how, plainly.
- **No problem-statement-sales-pitch-call-to-action arc by default.** Technical pitch decks are about what + how + architecture + components. Add other slides only if the user explicitly asks.

If the user describes a different audience (e.g. internal stakeholders, technical-only review, sales prospects), adjust calibration accordingly in Step 1.

---

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **Pitch Deck skill activated.** I'll guide you through a few quick questions, then generate a `.pptx` deck tailored to your audience and purpose.

Then proceed immediately to Step 1. No further preamble.

---

## Prerequisites

`python-pptx` must be installed in the environment (`pip install python-pptx`). All `.pptx` generation depends on it.

---

## Required reading before doing anything

Before writing any code or generating any slides:

1. Read `../project_context.md` — authoritative facts about the project. Everything in the deck must be consistent with this file.
2. Run the Bootstrap check (see below) — creates output and samples directories if missing.
3. Read the most recent `.pptx` file in `docs/decks/`, if one exists — for visual style/template reference only, not for content. Older projects may have pre-existing change-summary decks from before this skill suite took over slide-deck generation; ignore their content structure entirely and just borrow color/font/layout cues.

For producing the `.pptx` file itself, use `python-pptx` via a Python script.

If no existing `.pptx` is present in the project, generate a clean, modern style from scratch — neutral palette, generous whitespace, one idea per slide.

---

## Bootstrap — first-time setup check

Run this before anything else, every invocation:

1. Check whether `docs/decks/` exists at the project root.
2. **If it does not exist**, create both directories:
   ```bash
   mkdir -p docs/decks/samples/
   ```
   Then tell the user:
   > "`docs/decks/` did not exist — created it along with `docs/decks/samples/`. You can optionally drop reference `.pptx` files (previous decks, style templates) into `docs/decks/samples/` — the skill borrows visual cues (colors, fonts, layouts) from them. This is optional; if you have no reference decks, I'll generate a clean modern style from scratch. Tell me to proceed when ready."

   Wait for the user's response before continuing to Step 1.

3. **If `docs/decks/` exists** but `docs/decks/samples/` does not, create it silently and proceed.

---

## Locating the output directory

The canonical output directory is `docs/decks/` at the project root — created during Bootstrap if it didn't exist.

**Exception:** if the project already stores decks elsewhere (e.g. `documentations/`, `decks/`, `pitch/`) and `docs/decks/` was not created by Bootstrap, ask the user to confirm which directory to use rather than creating a duplicate alongside an existing one.

**Visual style reference:** read the most recent `.pptx` in `docs/decks/` (or `docs/decks/samples/` if present) for color/font/layout cues. If no existing decks are found in either place, generate a clean modern default — neutral palette, generous whitespace.

Filenames derive from the project name in `../project_context.md` plus mode/frame and date — see Step 1.

---

## Workflow

### Step 1 — Clarify scope with the user

Ask the user before generating. **The first question is the most important** because it determines the deck's entire structure:

1. **Deck mode** — ask:

   > "Is this deck:
   > (a) a **fresh introduction** to the project for a new audience, or
   > (b) a **what's-new / release showcase** highlighting what's changed since a previous version, for an audience that already knows the project?"

   Do not proceed to the outline until the user picks one.

   If the user picks **(b)**, ask immediately:
   - **Comparison frame** — "Is this:
     - (i) **Released version vs released version** — e.g. 'what's new in v2.0 vs v1.5'. For release announcements, post-mortems, retrospective decks tied to a specific release.
     - (ii) **Current state vs a previous version** — e.g. 'where we are now vs v2.0'. For weekly/monthly status updates, ongoing-progress decks, meetup recaps."

     **Default to (ii)** if the user doesn't specify and isn't clearly talking about a specific release event. Status-update decks are the more common case and fail more gracefully if guessed wrong.
   - Which previous version is the comparison anchor?
   - Should the deck include a brief recap of *what the project is* for audience members who may be new?

2. **Audience** — confirm or override the default audience model (mixed external, mostly non-technical with technical minority). If the user says "this is for a technical-only audience" or "internal sales pitch," adjust framing depth accordingly. Audience determines what a sensible length default is, so ask this before length.

3. **Length target** — short (8–10 slides), standard (12–16), or extended (18–22). Propose a default based on the audience and context from Q2 rather than defaulting blindly to standard.

4. **Filename / suffix** — using the project name from `../project_context.md` (call it `<PROJECT>`), default patterns:
   - Mode (a) fresh intro: `<PROJECT>_PitchDeck_<YYYY-MM-DD>.pptx`
   - Mode (b) frame (i) version-vs-version: `<PROJECT>_PitchDeck_WhatsNew_v<NEW>_<YYYY-MM-DD>.pptx`
   - Mode (b) frame (ii) current-state-vs-version: `<PROJECT>_PitchDeck_Status_<YYYY-MM-DD>.pptx`

   Confirm the date or offer to let the user supply a custom suffix.

5. **Anything to emphasize or de-emphasize** this round.

6. **Anything off-limits** — features still under NDA, customers not to be named, unreleased capabilities.

### Step 2 — Pull the project facts and (in mode b) determine the source tier

**Always:** read `../project_context.md` end-to-end. Every factual claim in the deck must trace back to it (or to the user's answers in Step 1). If `../project_context.md` has placeholder `<fill in: ...>` markers still unfilled, stop and tell the user.

If a fact you need for the deck isn't in `../project_context.md`, ask the user rather than inventing it.

**In mode (a)** (fresh introduction), `../project_context.md` is the only source. Do not read release docs in `docs/releases/` — they're aimed at a different audience. Proceed to Step 3.

**In mode (b)** (what's-new), the source strategy depends on the comparison frame.

---

#### Frame (i) — Released version vs released version

The deck is about a specific release. If release docs for that version exist, they ARE the curated answer. Check tiers:

**Tier 1 — Release docs for the new version exist** in `docs/releases/` (User Guide and/or Technical Guide for `<NEW>`). **Prefer them as the source of truth.** They've already been generated through the documentation skill (or by the user manually) and the change inventory was validated. Read both guides if both exist; the User Guide framing tends to be more pitch-friendly (operational impact, user-facing capability), while the Technical Guide gives the implementation depth a technical attendee may ask about. The `[New in v<NEW>]` markers in those docs are authoritative — every item carrying that marker is a candidate for the pitch deck.

Do **not** re-run git log or re-read the changelog when Tier 1 applies. The markers in the guides already encode that work.

**Tier 2 — Release docs exist for the previous version but not the new one.** Read the previous-version docs to understand the "before" state, then determine the delta via the changelog and:
```bash
git log <previous-version-tag>..<new-version-tag-or-HEAD> --oneline --no-merges
```
Mention to the user once: "I don't have v<NEW> release docs, so I'm building from the v<PREVIOUS> docs plus changelog and git log. You may want to run the documentation skill first for a more reliable result."

**Tier 3 — No release docs in `docs/releases/` at all.** Fall back to gathering change signal from scratch via the changelog, git log, and code inspection.

---

#### Frame (ii) — Current state vs a previous version

The deck is about *where things are now*, not about a specific release. Docs reflect a past snapshot (potentially months old) and are NOT the source of truth for current state. **Always use git/changelog/code as the primary source, regardless of whether docs exist.**

Gather change signal:
1. **Changelog** — read everything after the comparison-anchor version. If the changelog has a Keep-a-Changelog-style "Unreleased" section, read that too.
2. **Git log since the anchor version**, all the way to current HEAD: `git log <anchor-version-tag>..HEAD --oneline --no-merges`. Pay attention to dates — recency matters for status decks.
3. **Code inspection** for anything ambiguous.

Docs (if they exist for the anchor version) are useful as a **reference for the "before" state only** — to remind yourself what the project looked like at the anchor, then frame what's new relative to that. Do not use docs as the source of "what's new" itself.

---

**Regardless of frame:** build a **pitch-relevant change inventory**. This is narrower than the release-doc change inventory. Only include:

- **Headline additions** — major new capabilities a non-engineer would care about
- **Notable improvements** — performance, scale, accuracy gains with concrete numbers
- **Architectural shifts** — meaningful changes to how the system works
- **Work in progress** — *frame (ii) only* — significant ongoing efforts worth flagging, marked clearly as in-progress

Explicitly **exclude**: bug fixes, internal refactors, minor parameter changes, dependency bumps.

Share the inventory with the user and ask them to confirm or trim before generating the outline.

### Step 3 — Outline before slides

Produce a plain-text slide-by-slide outline and share it with the user for sign-off. Outlines are cheap to iterate; finished decks are not.

**Mode (a) — Fresh introduction outline** (standard-length deck):
1. **Title** — project name, one-line tagline, presenter, date
2. **What it is** — plain language, what does this thing do
3. **How it works (high level)** — end-to-end story in 3–5 numbered steps. No jargon.
4. **Architecture** — single diagram slide with placeholder. Major components labeled with canonical names from `../project_context.md`.
5+. **Component deep dives** — one slide per major component (variable count). Derive the component list from `../project_context.md`'s description and repo layout, and from inspecting the codebase if those aren't detailed enough. Confirm the list with the user before generating slides if there's any ambiguity about what counts as a "major" component. Order matches the user's emphasis from Step 1.
- **Data/database** — if relevant, add one slide after the component dives. Schema-level view.

**Mode (b) frame (i) — Version-vs-version outline** (standard-length deck):
1. **Title** — comparison framing ("v1.5 → v2.0: What's New")
2. **Quick recap (optional)** — if some audience members may be new
3. **What's new at a glance** — 3–6 bullets from the change inventory
4. **Deep dive on each major addition** — one slide each, use `[New in v<NEW>]` marker
5. **Improvements** — concrete numbers
6. **Architectural shifts** — before/after diagram if applicable
7. **What this enables** — capability framing

**Mode (b) frame (ii) — Current-state outline** (standard-length deck):
1. **Title** — status framing ("Where we are: <Month Year>" or "Progress since v<ANCHOR>"). Avoid version-delta framing — this isn't one.
2. **Quick recap (optional)**
3. **Headline progress** — 3–6 bullets, ordered by impact, not chronology
4. **Deep dive on each headline item** — frame as "we now do X" not "v<X> adds X." Use `[In progress]` for unshipped work.
5. **Improvements**
6. **Architectural shifts** — if any
7. **What's next (optional)** — only if user asked for it

The marker convention `[New in v<NEW>]` applies in frame (i) only. Frame (ii) uses `[In progress]` for unshipped work and no marker for shipped items. In mode (a), no markers at all.

### Step 4 — Diagram placeholders

For every slide that should contain a diagram (architecture, component flow, DB schema), insert a **clearly marked placeholder** rather than attempting to auto-generate diagrams:

- A large outlined rectangle filling the slide's diagram area
- Inside, centered text: `[ DIAGRAM PLACEHOLDER ]`
- Below: a one-line description of what the diagram should show
- In speaker notes for that slide: a more detailed prompt covering which components should appear and how they connect

Auto-generated diagrams in pitch decks consistently look amateur. A clean placeholder with a detailed brief in speaker notes is more useful.

### Step 5 — Generate the deck

Once the outline is approved:

- Use `python-pptx` via a Python script to produce the file
- Borrow visual cues (colors, fonts, title styles) from existing `.pptx` files in `docs/decks/` or `docs/decks/samples/` if present; otherwise use a clean modern default
- One idea per slide. If a slide needs more than ~5 bullets or ~60 words of body text, split it.
- Speaker notes on every slide (full sentences, presenter script + diagram briefs)
- Use canonical terminology from `../project_context.md`
- Apply marker conventions per the rules in Step 3

### Step 6 — Hand off

Provide the generated file and a short summary:
- Filename and location
- Slide count and section breakdown
- A list of diagram placeholders the user still needs to fill in
- Anything in `../project_context.md` that was incomplete or that you had to ask the user about

---

## Things to get right

- **No invented facts.** Numbers, capabilities, integrations — all from `../project_context.md` or explicit user input.
- **Technical sections must hold up to scrutiny.** Aim for "would a senior engineer in the audience find this credible."
- **Canonical terminology, every slide.** Inconsistency on terms is the fastest signal that a deck was machine-generated.
- **Diagram placeholders are real placeholders.** Don't try ASCII art or auto-shapes.

## Things to avoid

- Generating a deck without first asking which mode (a or b), and in mode (b) which frame (i or ii), and without the user-confirmed outline
- Adding sales/problem/call-to-action slides not in the agreed scope
- In mode (a), pulling in version-diffing logic or `[New in vX.X]` markers
- In mode (a), reading release docs at all — `../project_context.md` is the only source
- In mode (b) frame (i) Tier 1 (v<NEW> docs exist), re-running git log to second-guess the docs
- In mode (b) frame (ii), trusting docs as the source of "what's new" — docs are a snapshot, not current state
- In mode (b), highlighting bug fixes or internal refactors that don't matter to the audience
- Framing a frame (ii) deck as a version-vs-version delta
- Adding source-tier warnings *inside* the deck
- Filling unknown facts with plausible-sounding guesses
- One-slide-fits-all dumps where five separate ideas pile onto one slide