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
2. Check `./samples/` — see "Samples handling" below for what to do based on what you find.
3. Locate the TD output directory (see "Locating the TD output directory" below).

If `../project_context.md` has placeholder `<fill in: ...>` markers still unfilled and they're relevant to what the TD is about, stop and tell the user — the TD cannot be reliable until those are real.

---

## Samples handling

The `./samples/` directory holds reference TDs from the user's organization. They are used by both the drafter (for tone, structure, conventions) and the reviewer (for style reference during the self-review pass).

**If `./samples/` contains usable files** (`.pdf`, `.docx`, or `.md` files; ignore `README.md`): read all of them carefully. They are the calibration target for tone, section weight, citation style, table use, and figure conventions.

**If `./samples/` is empty or contains only `README.md`**: ask the user before proceeding:

> "I don't see any sample TDs in `./samples/`. The skill works best with at least one reference TD from your organization so the output matches your house style. You can:
> (a) drop one or more `.pdf` / `.docx` TDs into `samples/` and re-invoke me, or
> (b) tell me to proceed anyway and I'll produce a best-effort TD using abstract conventions only (output may not match your org's specific style).
>
> What would you like to do?"

If the user picks (b), proceed but include a brief note in the hand-off summary mentioning that the TD was generated without samples and may not match house style. Do not silently lower quality without flagging.

**If `./samples/` contains a `README.md`**: read it — it may contain user-supplied notes about which samples illustrate which patterns, or about house-convention deviations from the samples (e.g. "samples name commercial competitors but house convention is generic descriptions"). These notes override what you'd infer from the samples alone.

---

## Locating the TD output directory

This skill is project-generic. Determine where TD drafts should go:

1. Check (in order): `td/`, `tds/`, `disclosures/`, `docs/td/`. Use the first one that exists.
2. If none exists, default to creating `td/` at the repo root, but ask the user first to confirm.

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

Style rules (calibrated against `./samples/` when available; defaults below otherwise):

- **Voice:** first person plural ("we developed," "we evaluate"). Academic but not stuffy. Use contractions sparingly.
- **Numbers:** concrete, unhedged, with units. "92% accuracy" not "high accuracy." "700 Mbps" not "significant throughput."
- **Limitations:** state honestly. A TD that hides limitations reads as marketing and loses credibility.
- **Tables:** use when content has multiple attributes per row (component descriptions, results across methods, case-study walkthroughs). Prose for narrative content. Don't default to tables — use them when they earn their place.
- **Figures:** describe what the figure shows in the surrounding prose (figures aren't self-explanatory in a TD). Insert markdown placeholders for figures the user will add later — use the convention `![Figure N: <description>](placeholder)` followed by a one-paragraph speaker-notes-style brief on what the figure should actually depict.
- **Citations:** numbered `[1]`, `[2]` style inline (or match the samples' convention). References section at the end with full URLs. Every reference must be a real, verified source. If a search didn't return a usable source for a claim, soften the claim rather than fabricating a citation.

**House-convention deviations from samples:**

The samples in `./samples/` may reflect older conventions that the user's organization has moved away from. Check `./samples/README.md` for any documented deviations — these override what you'd infer from the samples directly.

A common example (which the user may or may not have): samples may name specific commercial competitors directly (by company and product name), while the current convention is to use generic descriptions. If the samples' README mentions this kind of rule, follow it. Otherwise, match the samples.

#### 2d. Save the draft

Write to: `<TD-output-dir>/<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>.md`

Use the title-derived slug from pre-flight Q9. Slug is lowercase, hyphenated, no special chars.

Confirm to the user that the draft is written, and that the self-review pass is starting next. Do **not** present the draft for user review yet — the self-review goes first.

---

### Phase 3 — Self-review (clean slate)

This is the most important phase. Done casually, self-review produces validation theater. Done with the right framing, it catches real issues.

#### 3a. Reset context explicitly

Before reading the draft, state to yourself (in your reasoning, not necessarily out loud to the user):

> "I am now a critical-but-fair member of an internal Technology Disclosure review board. I have not seen this TD before. I have reviewed many TDs and would reject approximately 30% of submissions outright and accept the rest with revisions of varying severity. My job is to find problems, not to validate the author's choices. 'Looks good overall' is a failure of my role. If I feel a temptation to recognize the document or its arguments, I treat that recognition as suspicious — I am a reviewer, not an author.
>
> I have access to: the draft TD and the samples in `./samples/` (if any). I do not have access to `../project_context.md`, the drafting workflow, or any other context about how this TD was produced. I judge the document on its own merits."

Then read:
1. The draft (just written, but approach it as if seeing it for the first time)
2. All files in `./samples/` if present — used as **style reference**, not content reference. The reviewer compares tone, structure, and weight to the samples, not specific content.
3. `./samples/README.md` if present — any documented house-convention deviations apply to the reviewer's judgment too. The reviewer should NOT flag the draft for following a documented deviation; the reviewer SHOULD flag the draft for ignoring one.

If `./samples/` was empty (and the user chose to proceed anyway in the Phase 1 / samples-handling step), the reviewer works from abstract conventions only. Note this explicitly in the review verdict.

#### 3b. Apply the rubric

For each checkpoint below, the reviewer gives a yes/no/concern answer with a one-sentence rationale. Do not skip checkpoints — answer all explicitly.

**Substance**
1. Is the novelty claim made explicitly somewhere in the abstract or introduction?
2. Is the novelty claim *supported* by evidence in the technical description and results?
3. Are performance metrics specific (numbers, units, conditions)? Or vague ("significant improvement", "fast")?
4. If baselines are claimed or implied, are they real, comparable, and named honestly?
5. Are limitations stated, or has the TD been written as marketing?

**Structure**
6. Are all required sections present (Abstract, Introduction, Lit Review/Prior Art, Technical Description, Results, Conclusion, References)?
7. Is each section the right weight? (Common failures: introduction is 40% of the doc, lit review is one sentence, results is a single paragraph with no numbers.)
8. Does the introduction end by explicitly naming the problem and the proposed contribution?
9. Does the conclusion restate the contribution without merely repeating the abstract?

**Prior Art**
10. Does the prior-art section cite specific, real work? Or does it gesture vaguely at "existing approaches"?
11. Is each citation actually relevant to the contribution, or is the lit review padded?
12. Are there obvious omissions — well-known competing approaches the TD ignores?

**Style and conventions**
13. Does the tone match the samples (academic, first-person plural, concrete, limitation-honest)? If no samples: does it follow general TD/research-paper conventions?
14. Are tables used appropriately (multi-attribute content) rather than for prose-shaped content?
15. Are figures described in the surrounding prose (not left to speak for themselves)?
16. Does the draft respect any documented house-convention deviations in `./samples/README.md`? If the README documents a rule the draft violates, flag it.

**Reviewer's gut check**
17. Reading this cold, would I recommend it for further consideration, or would I bounce it back?
18. If I had to summarize the contribution in one sentence to a colleague, could I, based only on this document?
19. Is there any section I would have skipped while reading because it didn't add value?

#### 3c. Write the review file

Write to: `<TD-output-dir>/<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>_review.md`

Structure:

```markdown
# Review: <TD title>
**Reviewer role:** Critical-but-fair internal TD review board member (simulated)
**Date:** <YYYY-MM-DD>

## Verdict
**[ACCEPT | ACCEPT WITH REVISIONS | REJECT]**

<One-paragraph rationale, 3–6 sentences. Concrete, not "this is a good/bad TD." Name the specific reason for the verdict.>

## Issues

### Blocking
<Issues that prevent acceptance. Each entry: one-line summary, then 2–3 sentences of detail, then a "Suggested rewrite" subsection with concrete drafted text the user can paste in. If there are zero blocking issues, write "None.">

### Significant
<Issues that don't block but should be addressed before submission. One-line summary + 1–2 sentences of detail. No suggested rewrites.>

### Nit
<Polish-level issues. One line each.>

## Strengths
<2–4 specific things the TD does well. Concrete, not generic praise.>

## Rubric responses
<A brief table or list showing the reviewer's answers to the 19 checkpoints. This is the receipts — it shows the verdict isn't pulled from thin air.>
```

**Verdict calibration** (critical-but-fair, ~30% rejection rate):
- **REJECT** — fundamental problems: no clear novelty claim, no real evaluation, fabricated citations, contribution is unclear even after reading. Use for ~30% of TDs.
- **ACCEPT WITH REVISIONS** — has the bones of a real TD but needs work. One or more blocking issues exist but they're fixable. Most TDs that aren't outright rejects fall here.
- **ACCEPT** — solid as-is. Significant and nit issues only, no blocking. Rare — reserve for TDs that genuinely don't need changes. ACCEPT verdicts still need substantive justification, not just "no blocking issues."

---

### Phase 4 — Hand off

Mention the full paths of both output files directly so the user can open them immediately.

Then provide a short written summary:
- The verdict from the self-review (so the user knows whether to expect heavy revisions)
- A one-line preview of the most important blocking issue, if any
- Anything in `../project_context.md` that was missing or incomplete, so the context file can be updated
- If `./samples/` was empty: a reminder that the TD was generated without house-style calibration
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