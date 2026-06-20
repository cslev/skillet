---
name: td
argument-hint: "Topic or title of the disclosure (e.g. 'multi-agent orchestration framework', 'real-time anomaly detection pipeline')"
description: Generate a Technology Disclosure (TD) document for a project. A TD is a short (typically under 20 pages) research-paper-style document describing a software contribution, tool, framework, or technique developed within a project. It includes abstract, introduction, literature review, technical description, evaluation, and conclusion. Trigger when the user mentions "TD", "technology disclosure", "tech disclosure", "write up the disclosure", "patent disclosure", "invention disclosure", or asks for a research-paper-style writeup of a project, a component of it, or a specific technique. Also trigger when the user asks to review or critique an existing TD draft. Do NOT trigger for release documentation (the documentation skill handles that), pitch decks (the pitch-deck skill handles that), or general code documentation.
---

# Technology Disclosure (TD) Skill

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **TD skill activated.** I'll guide you through a pre-flight, draft the disclosure, run a self-review, and hand off both files.

Then proceed immediately to Phase 1. No further preamble.

---

This skill generates Technology Disclosures: short research-paper-style documents describing a software contribution from a project. The output is markdown (for fast iteration), with conversion to `.docx` as a separate explicit step for final submission.

A TD is **not**: release documentation, a pitch deck, a marketing piece, a code walkthrough. It is closer to an academic research paper but produced for internal IP/disclosure purposes — typically under 20 pages, with the structure and rigor of a short conference paper.

## Deliverables

Each invocation produces **two files** in the TD output directory:

1. **Draft TD** — `<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>.md`
2. **Self-review** — `<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>_review.md`

Where `<PROJECT>` is the project name from `../project_context.md`.

The user reviews both and decides next steps. The skill does **not** auto-revise based on the review.

---

## Prerequisites

`pandoc` must be installed in the environment (`brew install pandoc` / `apt install pandoc`). The markdown→docx conversion step in Phase 4 depends on it.

---

## Required reading before doing anything

Before writing any code, generating any draft, or running the review pass:

1. Read `../project_context.md` — authoritative facts about the project.
2. Run the Bootstrap check (see below) — creates output and samples directories if missing.
3. Check `docs/td/samples/` — see "Samples handling" below for what to do based on what you find.

If `../project_context.md` has placeholder `<fill in: ...>` markers still unfilled and they're relevant to what the TD is about, stop and tell the user — the TD cannot be reliable until those are real.

---

## Bootstrap — first-time setup check

Run this before anything else, every invocation:

1. Check whether `docs/td/` exists at the project root.
2. **If it does not exist**, create both directories:
   ```bash
   mkdir -p docs/td/samples/
   ```
   Then tell the user:
   > "`docs/td/` did not exist — created it along with `docs/td/samples/`. Before I continue, drop your organization's sample TDs (`.pdf` or `.docx`) into `docs/td/samples/`. The skill calibrates its tone, structure, and citation style against them. Add samples and re-invoke me, or tell me to proceed now and I'll work without calibration (output may not match your house style)."

   Wait for the user's response before continuing to Phase 1.

3. **If `docs/td/` exists** but `docs/td/samples/` does not, create it silently:
   ```bash
   mkdir -p docs/td/samples/
   ```
   Then proceed without stopping — the Samples handling section covers the empty-samples case.

---

## Samples handling

The `docs/td/samples/` directory holds reference TDs from the user's organization. They are used by both the drafter (for tone, structure, conventions) and the reviewer (for style reference during the self-review pass).

**If `docs/td/samples/` contains usable files** (`.pdf`, `.docx`, or `.md` files; ignore `README.md`): read all of them carefully. They are the calibration target for tone, section weight, citation style, table use, and figure conventions.

**If `docs/td/samples/` is empty**: ask the user before proceeding:

> "I don't see any sample TDs in `docs/td/samples/`. The skill works best with at least one reference TD from your organization so the output matches your house style. You can:
> (a) drop one or more `.pdf` / `.docx` TDs into `docs/td/samples/` and re-invoke me, or
> (b) tell me to proceed anyway and I'll produce a best-effort TD using abstract conventions only (output may not match your org's specific style).
>
> What would you like to do?"

If the user picks (b), proceed but include a brief note in the hand-off summary mentioning that the TD was generated without samples and may not match house style. Do not silently lower quality without flagging.

**If `docs/td/samples/` contains a `README.md`**: read it — it may contain user-supplied notes about which samples illustrate which patterns, or about house-convention deviations from the samples (e.g. "samples name commercial competitors but house convention is generic descriptions"). These notes override what you'd infer from the samples alone.

---

## Locating the TD output directory

The canonical output directory is `docs/td/` at the project root — created during Bootstrap if it didn't exist. Use it.

**Exception:** if the project already stores TDs elsewhere (e.g. `td/`, `tds/`, `disclosures/`) and `docs/td/` was not created by Bootstrap (i.e. the project predates this convention), ask the user to confirm which directory to use rather than creating a duplicate alongside an existing one.

---

## Workflow

The skill has four phases: **Pre-flight**, **Draft**, **Self-review**, **Hand off**. Do them in order.

---

### Phase 1 — Pre-flight (ask the user)

TDs are scoped, audience-aware documents. Ask the user the following before drafting. This is "ask more" mode — gather enough context that the draft is grounded, not generic. Bundle the questions; don't ask one at a time.

1. **What is this TD about?** One sentence naming the contribution (a feature, technique, framework, tool, or the whole project).

2. **What is the novelty angle?** What makes this worth disclosing? One or two sentences. This becomes the spine of the abstract and the "innovation" framing in the introduction.

3. **Target audience for the TD itself.** Internal IP review board? External patent attorney? Cross-team technical reviewers? This affects depth of explanation for project-specific terms.

4. **Target deployment context** for the disclosed technology. Cloud / on-prem / edge / hybrid / research-only? This shapes the deployment-model section if present.

5. **Baseline data.** Do you have measured performance data comparing this against existing methods or against an obvious baseline? If yes — where (paths to logs, benchmarks, results files, or paste the numbers)? If no — say so and the TD will report absolute numbers only, no baseline comparison.

6. **Where do the metrics come from this time?** Existing benchmark scripts in the repo? Test outputs? Manually run experiments? User-provided numbers?

7. **Specific prior art** the user already has in mind that must be cited. Optional — Claude will research more on top of this.

8. **Anything off-limits** — unreleased capabilities, NDA-bound details, internal-only methods.

9. **Title for the TD.** Used in the filename slug and as the document title. If the user doesn't have one, suggest one based on the contribution.

Do not skip these. The pre-flight is the difference between a generic TD and one that lands.

---

### Phase 2 — Draft

#### 2a. Derive contextual material from the repo

Before writing, gather material the user didn't have to spell out:

- **Project facts** — already in `../project_context.md`.
- **Performance numbers** — from wherever the user pointed in pre-flight Q6, or by running existing benchmark scripts if the user said "from the repo."
- **Challenges** — derive from a combination of `../project_context.md`, the changelog, code comments mentioning known difficulties, and the structure of the codebase. The "Challenges" section (if used) should reflect *real* engineering challenges visible in the code/history, not generic field-level difficulties. If no meaningful challenges surface from this derivation, omit the section.
- **Prior art** — web search. This is the section most prone to error. Be aggressive about searching: search for the specific techniques used, the names of comparable tools, the protocols/standards involved. Read at least the abstracts of cited works; do not cite from titles alone.

#### 2b. Build the section structure for *this* TD

A TD's structure adapts to its content. Use the following section list as the menu — include what fits, omit what doesn't:

**Required sections (always include):**
- **Title** + **author/inventor metadata** (per the samples' conventions; check what's there)
- **Abstract** — one or two paragraphs. First sentence frames the problem; the contribution is named explicitly; the last sentence previews the impact.
- **Introduction** — sets up the broader context. End the introduction by explicitly naming the problem and the innovation. Bold lead-ins like `**Problem:**` and `**Innovation:**` are acceptable when the introduction is long enough that the reader needs signposting; optional otherwise.
- **Literature Review** / **Background and Prior Art** — depth scales with how much actually-comparable prior work exists. If there are several close competitors, cover them with subsections. If there's little close work, a few paragraphs honestly stating that is better than padding with tangentially-related references. Do not invent references; cite real work or say nothing.
- **Technical Description** (variable name: "System Architecture", "Framework Design and Implementation", "Methodology", whichever fits) — the technical core. Use figures for architecture and flow. Use tables when describing components with multiple attributes. Name specific tools/frameworks used in the implementation (libraries, frameworks, languages) — these are *implementation choices* and naming them is fine.
- **Results / Evaluation** — what was measured, how, and what came out. Concrete numbers with units. If baseline comparisons are available (from pre-flight Q5), present them in a results table.
- **Conclusion** — restates the contribution, broadens to implications. Brief — one paragraph is often enough.
- **References** — numbered, IEEE-style (or whatever convention the samples use), with full URLs for web sources. Every citation must be a real reference you have actually checked.

**Optional sections (include when warranted):**
- **Challenges** — numbered list of engineering challenges the contribution addresses. Include when the contribution is methodologically complex. Derive from real evidence in the repo, not generic field-level difficulties.
- **Deployment Model** — when deployment context is part of the contribution.
- **Scalability & Performance** — when the contribution has nontrivial scaling characteristics worth discussing separately from headline results.
- **Evaluation Metrics** — when nontrivial metric choices are part of the contribution (e.g., justifying why a specific combination of metrics together). Skip when metrics are obvious.
- **Operational Workflow** — when the technology is an interactive system whose runtime behavior matters.
- **Future Work** — when there's a meaningful planned extension. Skip if it would be a generic "we will continue to improve X."

#### 2c. Write the draft

Style rules (calibrated against `docs/td/samples/` when available; defaults below otherwise):

- **Voice:** first person plural ("we developed," "we evaluate"). Academic but not stuffy. Use contractions sparingly.
- **Numbers:** concrete, unhedged, with units. "92% accuracy" not "high accuracy." "700 Mbps" not "significant throughput."
- **Limitations:** state honestly. A TD that hides limitations reads as marketing and loses credibility.
- **Tables:** use when content has multiple attributes per row (component descriptions, results across methods, case-study walkthroughs). Prose for narrative content. Don't default to tables — use them when they earn their place.
- **Figures:** describe what the figure shows in the surrounding prose (figures aren't self-explanatory in a TD). Insert markdown placeholders for figures the user will add later — use the convention `![Figure N: <description>](placeholder)` followed by a one-paragraph speaker-notes-style brief on what the figure should actually depict.
- **Citations:** numbered `[1]`, `[2]` style inline (or match the samples' convention). References section at the end with full URLs. Every reference must be a real, verified source. If a search didn't return a usable source for a claim, soften the claim rather than fabricating a citation.

**House-convention deviations from samples:**

The samples in `docs/td/samples/` may reflect older conventions that the user's organization has moved away from. Check `docs/td/samples/README.md` for any documented deviations — these override what you'd infer from the samples directly.

A common example (which the user may or may not have): samples may name specific commercial competitors directly (by company and product name), while the current convention is to use generic descriptions. If the samples' README mentions this kind of rule, follow it. Otherwise, match the samples.

#### 2d. Save the draft

Write to: `<TD-output-dir>/<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>.md`

Use the title-derived slug from pre-flight Q9. Slug is lowercase, hyphenated, no special chars.

Confirm to the user that the draft is written, and that the self-review pass is starting next. Do **not** present the draft for user review yet — the self-review goes first.

---

### Phase 3 — Self-review (clean slate)

This is the most important phase. Done casually, self-review produces validation theater. Done with the right framing, it catches real issues.

**Read `./review-rubric.md` now.** It contains the role-reframing prompt, the full 19-checkpoint rubric, the review file format, and verdict calibration. Follow it exactly for steps 3a, 3b, and 3c.

---

### Phase 4 — Hand off

Mention the full paths of both output files directly so the user can open them immediately.

Then provide a short written summary:
- The verdict from the self-review (so the user knows whether to expect heavy revisions)
- A one-line preview of the most important blocking issue, if any
- Anything in `../project_context.md` that was missing or incomplete, so the context file can be updated
- If `docs/td/samples/` was empty: a reminder that the TD was generated without house-style calibration
- The path for converting markdown → docx when the user is ready for submission (e.g., `pandoc <draft>.md -o <draft>.docx`)

Do **not** apply the review's suggested rewrites automatically. The user decides what to do with the review. If they want rewrites applied, they ask in the next turn.

---

## Things to get right

- **Pre-flight is non-negotiable.** Do not start drafting without the user's answers. A "generic" TD is worse than no TD.
- **Citations must be real.** Every reference verified, not just title-cited. If a search didn't find a usable source, soften the claim rather than fabricate.
- **Self-review with clean slate.** The reviewer pass is the part most likely to be done sloppily. Take it seriously — the role-reframing prompt at the start of Phase 3 is there for a reason.
- **Limitations are honest, not buried.** TDs that hide limitations read as marketing.
- **Numbers are unhedged.** "92% accuracy" not "high accuracy." If a number isn't available, say so explicitly rather than hedging.
- **Respect samples/README.md deviations.** When the README documents a rule that diverges from what the samples show, the README wins. Both drafter and reviewer follow this.

## Things to avoid

- Drafting without pre-flight
- Drafting without samples *and* without explicit user permission to proceed anyway
- Pattern-matching samples on dimensions that `samples/README.md` documents as outdated conventions
- Padding the lit review with tangentially-related citations to "look thorough"
- Inventing reference URLs or citing papers Claude hasn't verified
- Putting prose-shaped content in tables, or multi-attribute content in prose
- Skipping the self-review because the draft "feels good"
- Letting the reviewer praise the draft without applying the full 19-checkpoint rubric
- Applying the review's suggested rewrites automatically — user decides
- Asking the user to provide content that should come from `../project_context.md`, the code, or web search for prior art
- Hedging numbers with vague adjectives ("significant," "substantial," "fast") when concrete values are available