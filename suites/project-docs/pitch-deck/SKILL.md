---
name: pitch-deck
argument-hint: "Purpose and audience, e.g. 'investor pitch', 'v2.0 release showcase for internal team', 'conference intro deck'"
description: Generate a pitch deck (.pptx) about the project for external audiences (investors, conferences, technical evaluators) OR a release-showcase deck highlighting what's new in a specific version. Trigger when the user mentions a pitch deck, investor deck, conference deck, project overview deck, status deck, release deck, change summary deck, "what's new" deck, or asks for slides about the architecture, components, database, or what's new across the project. Also trigger for phrases like "pitch the project", "slides for the conference", "deck about how it works", "status update deck", "weekly progress deck", "where we are now", "slides for v2.0", "release showcase". Do NOT trigger for written release documentation like User Guides or Technical Guides (the documentation skill handles those), Technology Disclosures (the td skill handles those), TD presentation decks (the td-deck skill handles those), inline code comments, or general code explanation.
---

# Pitch Deck Skill

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **Pitch Deck skill activated.** I'll guide you through a few quick questions, then generate a `.pptx` deck tailored to your audience and purpose.

Then proceed immediately to the Bootstrap check and Step 1. No further preamble.

---

## What this produces

A single `.pptx` deck per request, generated fresh each time — there is no canonical version. Two modes, chosen by the user at the start of every run:

- **(a) Fresh introduction** for a new audience
- **(b) What's-new / release showcase** highlighting changes since a previous version

**Distinct from siblings:** the `documentation` skill produces versioned written release docs; the `td` skill produces Technology Disclosures; the `td-deck` skill turns a TD into an IP-review deck. This skill produces persuasive/narrative slide decks.

## Audience model

Default: **mixed external audiences** (investors, conference attendees, prospects, technical evaluators) — mostly non-technical, with a technical minority who will push on the architecture and component slides.

- **Accessible opening.** Assume the reader doesn't know what the project does. No jargon in the first two slides.
- **Substantive technical core.** Vague boxes labeled "AI MAGIC" or "PROCESSING" lose credibility instantly.
- **No marketing fluff.** State what the system does and how, plainly. The anti-slop rules in `../deck-style.md` are mandatory.
- **No problem → sales pitch → call-to-action arc by default.** These decks are about what + how + architecture + components. Add other slides only if the user explicitly asks.

If the user describes a different audience (internal stakeholders, technical-only review, sales prospects), adjust calibration in Step 1.

---

## Prerequisites

- **Required:** `python-pptx` (`pip install python-pptx`).
- **Optional:** LibreOffice (`soffice`) and poppler (`pdftoppm`) — enable the render check in the quality gate. LibreOffice + Pillow + network access also enable icons on the big-type slides via `../icon_to_png.py`. If anything is missing, that step is skipped, never installed unprompted.

---

## Required reading before doing anything

1. **`../project_context.md`** — authoritative project facts. Everything in the deck must be consistent with it.
2. **`../deck-style.md`** — copy rules, visual bans, default visual system and quality gate. Shared with `td-deck`. Every rule there applies to this skill.
3. **Run the Bootstrap check** below.
4. **Visual reference:** if a `.pptx` exists in `docs/decks/samples/` or `docs/decks/`, read `./style-from-reference.md` now and follow it to extract a style (fonts, colours, positions, logo) from it — never its content or slide count. Older projects may have pre-existing change-summary decks; ignore their content structure entirely. The extracted style takes precedence over the default visual system (see `../deck-style.md` §1), but the copy rules and visual bans still apply to every shape you add.

---

## Bootstrap — first-time setup check

Run every invocation. Output always goes to `docs/decks/`; reference samples live in `docs/decks/samples/`. These paths are fixed.

1. **If `docs/decks/` does not exist**, run `mkdir -p docs/decks/samples/` and tell the user:
   > "This skill requires `docs/decks/` in your project root — created it now along with `docs/decks/samples/`. You can optionally drop reference `.pptx` files (previous decks, style templates) into `docs/decks/samples/` — the skill borrows visual cues (colors, fonts, layouts) from them. If you have none, I'll use a clean default style. Tell me to proceed when ready."

   Wait for the user's response before continuing.
2. **If it exists** but `docs/decks/samples/` does not, create it silently and proceed.

---

## Workflow

### Step 1 — Clarify scope

Use the **AskUserQuestion** tool for these choices when it is available (plain text otherwise). The first question determines the deck's entire structure — ask it alone:

1. **Deck mode** — (a) fresh introduction, or (b) what's-new / release showcase for an audience that already knows the project. Do not proceed until the user picks one.

   If **(b)**, read `./whats-new.md` now, then ask:
   - **Comparison frame** — (i) released version vs released version (release announcements, retrospectives), or (ii) current state vs a previous version (status updates, progress decks, meetup recaps). **Default to (ii)** if unclear — it's the more common case and fails more gracefully.
   - Which previous version is the comparison anchor?
   - Include a brief recap of *what the project is* for newcomers?

Then ask the rest together (AskUserQuestion takes at most 4 questions per call — ask 2–6 in plain text or one call, and the brand questions 7–8 in their own calls, logo first, since the colour options depend on it):

2. **Audience** — confirm or override the default audience model. Ask before length, since audience sets the sensible length.
3. **Length** — short (8–10 slides), standard (12–16), or extended (18–22). Propose a default from the audience instead of defaulting blindly to standard.
4. **Filename** — using `<PROJECT>` from `../project_context.md`:
   - Mode (a): `<PROJECT>_PitchDeck_<YYYY-MM-DD>.pptx`
   - Mode (b)(i): `<PROJECT>_PitchDeck_WhatsNew_v<NEW>_<YYYY-MM-DD>.pptx`
   - Mode (b)(ii): `<PROJECT>_PitchDeck_Status_<YYYY-MM-DD>.pptx`
5. **Emphasis** — anything to emphasize or de-emphasize this round.
6. **Off-limits** — features under NDA, customers not to be named, unreleased capabilities.
7. **Company logo**, then 8. **colour template** — always ask both, in that order, exactly as described under "Brand questions" in `../deck-style.md` §4: the logo from `docs/assets/logos/`, analysed with `../logo_palette.py` to propose a matching template, which the user approves (or picks a preset / reference-deck colours / their own). Never pick colours or skip the logo on the user's behalf.

### Step 2 — Pull the project facts

**Always:** read `../project_context.md` end-to-end. Every factual claim in the deck must trace back to it or to the user's answers in Step 1. If it still has unfilled `<fill in: ...>` markers, stop and tell the user. If a fact you need isn't there, ask — never invent it.

- **Mode (a):** `../project_context.md` is the only source. Do not read release docs in `docs/releases/` — they're aimed at a different audience.
- **Mode (b):** follow the source tiers and build the change inventory as described in `./whats-new.md`. Get the user to confirm the inventory before the outline.

### Step 3 — Outline with assertion titles

Produce a plain-text outline. At the top: the deck's **core message** (one sentence) and its 3–5 supporting points (`../deck-style.md` §2). Then, for each slide: its **role**, its **assertion title**, its **layout** (`../deck-style.md` §4, or the reference deck's equivalent) and a 1-line content summary. Read the titles in sequence — they should tell the story on their own. Check the layout column for long runs of the same layout or of bullet slides before showing the outline.

**Mode (a) — fresh introduction** (standard length):
1. **Title** — project name, one-line tagline (plain description, no slogans), presenter, date
2. **What it is** — plain language: what this thing does and for whom, opening on a concrete fact
3. **How it works** — end-to-end story in 3–5 numbered steps, no jargon
4. **Architecture** — one diagram-placeholder slide; components labeled with canonical names from `../project_context.md`
5+. **Component slides** — one per major component, ordered by the user's emphasis. Derive the list from `../project_context.md` and the repo layout; confirm it with the user if what counts as "major" is ambiguous.
- **Data / database** — if relevant, one schema-level slide after the components

**Mode (b):** use the frame (i) or (ii) outline in `./whats-new.md`.

**Big-type slides:** in either mode, the outline includes section dividers where the core message splits into real sections (at most two in a deck of ≤ 10 slides, counted in the length), and a closing slide that restates the core message. Name the icon planned for each (`../deck-style.md` §4).

**Mode (a) uses no markers** (`[New in v…]`, `[In progress]`) and no version-diffing logic.

Get sign-off through **AskUserQuestion** — never a prose "shall I build it?". One question ("Build this deck, or adjust first?") with 2–3 options tailored to this outline, e.g. **Build it** / **Adjust the structure** (name the most likely tweak, such as "split the architecture slide") / **Change the angle**. Generate only after **Build it**, or after the user's change is folded in and re-approved. Outlines are cheap to iterate; finished decks are not.

### Step 4 — Diagram placeholders

For every slide that needs a diagram (architecture, component flow, DB schema), insert a placeholder per `../deck-style.md` §4 instead of drawing one:

- An outline-only rectangle filling the diagram area
- Centered label `[ DIAGRAM PLACEHOLDER ]`, with a one-line description of what the diagram should show underneath
- In speaker notes: a detailed brief — which components appear and how they connect

Auto-generated diagrams in pitch decks consistently look amateur. A clean placeholder with a good brief is more useful.

### Step 5 — Generate the deck

- Write a Python script using `python-pptx`; follow `../deck-style.md` §3–4 (or the reference deck's style, per §1): the brand frame on every content slide, and brand-background title, divider and closing slides with big type and one icon or the logo
- One idea per slide. More than 5 bullets or ~60 words of body text → split
- Use the layout chosen in the outline; vary form instead of defaulting to bullets
- Data slides: one claim, one native editable chart or table, values labelled, a source line when the origin is known
- Speaker notes on every slide: full spoken sentences, presenter script plus diagram briefs, same copy rules as slides
- Canonical terminology from `../project_context.md` on every slide
- Apply the marker conventions from Step 3

### Step 6 — Quality gate

Run the full quality gate in `../deck-style.md` §5:

1. `python3 <suite-dir>/lint_deck.py docs/decks/<file>.pptx --max-words 60` (add `--allow` for canonical terms that hit the vocabulary ban). Fix and regenerate until exit code 0.
2. Render check, if `soffice` and `pdftoppm` are installed; otherwise skip and note it.
3. Editing pass (titles, claims, 8-second test, cuts, any-topic test, rhythm).

### Step 7 — Hand off

Give the full path of the file, then a short summary:
- Slide count and section breakdown
- Diagram placeholders still to fill in
- Numbers on slides whose origin is unknown (shown without a source line)
- Quality gate result: lint errors/warnings remaining (with reasons), and whether the render check ran or was skipped (and why)
- Anything in `../project_context.md` that was incomplete or that you had to ask about

---

## Things to get right

- **No invented facts.** Numbers, capabilities, integrations — all from `../project_context.md` or explicit user input.
- **Technical slides hold up to scrutiny.** Would a senior engineer in the audience find this credible?
- **Canonical terminology, every slide.** Inconsistent terms are the fastest signal a deck was machine-generated.
- **No slop.** `../deck-style.md` is not optional styling advice — it's the acceptance criteria, enforced by the linter.

## Things to avoid

- Generating without the mode (and, in mode (b), the frame) chosen, and without an approved outline
- Topic-label titles ("Architecture", "Performance") instead of assertions
- Titles or bullets that explain *why* something happened when the source doesn't say
- Slides that exist because a pitch template has them, not because they serve the core message
- Adding sales/problem/call-to-action, "Key takeaways" or "Thank you" slides not in the agreed scope
- In mode (a), version-diffing logic, markers, or reading release docs
- Filling unknown facts with plausible-sounding guesses
- One slide carrying five ideas
- Delivering a deck that fails the linter
