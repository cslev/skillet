---
name: td
argument-hint: "Topic or title of the disclosure (e.g. 'multi-agent orchestration framework', 'real-time anomaly detection pipeline')"
description: Generate a Technology Disclosure (TD) document for a project. A TD is a short (typically under 20 pages) research-paper-style document describing a software contribution, tool, framework, or technique developed within a project. It includes abstract, introduction, literature review, technical description, evaluation, and conclusion. Trigger when the user mentions "TD", "technology disclosure", "tech disclosure", "write up the disclosure", "patent disclosure", "invention disclosure", or asks for a research-paper-style writeup of a project, a component of it, or a specific technique. Also trigger when the user asks to review or critique an existing TD draft. Do NOT trigger for release documentation (the documentation skill handles that), pitch decks (the pitch-deck skill handles that), or general code documentation.
---

# Technology Disclosure (TD) Skill

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **TD skill activated.** I'll run a pre-flight, draft the disclosure in markdown, then step you through review, humanizing, and `.docx` generation — pausing for your go-ahead at each step.

Then proceed immediately to Phase 1. No further preamble.

---

This skill generates Technology Disclosures: short research-paper-style documents describing a software contribution from a project. The working format is markdown (for fast iteration). Generation of the final `.docx` is the **last** step and happens only after the user has approved the draft — never automatically right after drafting.

The flow is gated: draft → (ask) self-review → revise until satisfied → (ask) humanize → (ask) generate `.docx`. Each arrow is a checkpoint where you stop and wait for the user. Do not run ahead to the next step on your own.

A TD is **not**: release documentation, a pitch deck, a marketing piece, a code walkthrough. It is closer to an academic research paper but produced for internal IP/disclosure purposes — typically under 20 pages, with the structure and rigor of a short conference paper.

## Deliverables

Files written to the TD output directory, in the order they appear:

1. **Draft TD** — `<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>.md` (always)
2. **Self-review** — `<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>_review.md` (only if the user opts into review)
3. **Final TD** — `<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>.docx` (only when the user approves generation, as the last step)

Where `<PROJECT>` is the project name from `../project_context.md`.

The markdown draft is the working artifact; it is revised in place across review and humanizing. The `.docx` is generated once, at the end, from the approved draft.

---

## Prerequisites

Both are needed for the `.docx` generation step (Phase 5). They do not need to be installed up front — that phase checks for them and offers to install what's missing (see `./docx-generation.md`):

- **`pandoc`** (`brew install pandoc` / `apt install pandoc`) — converts the markdown body and builds the Word table-of-contents field.
- **`python-docx`** (`pip install python-docx`) — adds the cover page, sections, header/footer, page numbering, and justification.

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
2. **If it does not exist**, create it along with the shared assets directory:
   ```bash
   mkdir -p docs/td/samples/ docs/assets/logos/
   ```
   `docs/assets/logos/` is a **shared** project asset directory (not specific to this skill — other skills, e.g. documentation, can use the same logos). Then tell the user:
   > "This skill requires `docs/td/` in your project root — created it now along with `docs/td/samples/` and a shared `docs/assets/logos/`. Two things to drop in:
   > - **Sample TDs** (`.pdf` / `.docx`) into `docs/td/samples/` — the skill calibrates its tone, structure, and citation style against them.
   > - **Your organization's logo** (`.png` / `.jpg`) into `docs/assets/logos/` — it goes on the `.docx` cover page and in the page header.
   >
   > Re-invoke me once you've added them, or tell me to proceed now (I'll work without samples — output may not match your house style — and ask about the logo when it's time to generate the `.docx`)."

   Wait for the user's response before continuing to Phase 1.

3. **If `docs/td/` exists** but `docs/td/samples/` or `docs/assets/logos/` do not, create the missing ones silently and proceed.

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

## Output directory

Always use `docs/td/` for output and `docs/td/samples/` for reference samples. These paths are fixed — do not look for or create alternative locations.

---

## Workflow

The skill has six phases, each gated on the user's go-ahead:

1. **Pre-flight** — gather scoping context.
2. **Draft** — write the markdown draft. Then *ask* whether to run the self-review.
3. **Self-review** — if the user agrees, review and then revise the draft until they're satisfied.
4. **Humanize** — *ask* whether to apply the `/humanizer` skill to the approved draft.
5. **Generate `.docx`** — *ask* whether the user is ready; then handle the logo and build the document.
6. **Hand off** — summarize and point to the files.

Do them in order. Do not skip a checkpoint or run the next phase before the user says to.

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

10. **Authors / inventors.** The full list, in order, as they should appear on the cover page (one per row). These also feed the author metadata in the document. Capture them now so the `.docx` step in Phase 6 doesn't have to stop and ask.

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

**Anti-AI-writing checklist** — apply to all prose as you draft, section by section:

- No em dashes (—). Use a comma, semicolon, or rewrite the sentence.
- No significance inflation: avoid *crucial*, *vital*, *critical*, *transformative*, *groundbreaking*, *revolutionary*, *pivotal*. State the fact; let it speak for itself.
- No AI vocabulary: avoid *leverage*, *robust*, *seamlessly*, *streamline*, *delve*, *comprehensive*, *facilitates*, *cutting-edge*, *state-of-the-art* (unless citing a prior art paper title).
- No rule-of-three sentence endings: "X, Y, and Z" as a rhetorical closer signals generated text. If three items are genuinely enumerable, a list or table is clearer.
- No hedged numbers: "significant improvement," "substantial reduction," "fast inference" — replace with the actual number or omit the claim.
- Active voice preferred. Passive is acceptable when the subject is genuinely unknown or irrelevant, not as a default register.

**House-convention deviations from samples:**

The samples in `docs/td/samples/` may reflect older conventions that the user's organization has moved away from. Check `docs/td/samples/README.md` for any documented deviations — these override what you'd infer from the samples directly.

A common example (which the user may or may not have): samples may name specific commercial competitors directly (by company and product name), while the current convention is to use generic descriptions. If the samples' README mentions this kind of rule, follow it. Otherwise, match the samples.

#### 2d. Save the draft

Write to: `<TD-output-dir>/<PROJECT>_TD_<short-title-slug>_<YYYY-MM-DD>.md`

Use the title-derived slug from pre-flight Q9. Slug is lowercase, hyphenated, no special chars.

**Do not generate a `.docx` here.** The draft is markdown only at this stage.

Confirm to the user that the markdown draft is written (give the full path), then **stop and ask** whether to run the self-review now:

> "Draft is ready at `<path>`. Would you like me to run the self-review pass on it now? (It simulates a critical internal review-board member and writes a separate review file.)"

Wait for the answer.
- **Yes** → go to Phase 3.
- **No / not now** → skip to the relevant later checkpoint the user names (e.g. straight to humanizing, or straight to `.docx`), or stop if they just want the draft. Don't force the review.

---

### Phase 3 — Self-review (clean slate) and revision

Run this only if the user opted in at the end of Phase 2.

This is the most important quality phase. Done casually, self-review produces validation theater. Done with the right framing, it catches real issues.

**Read `./review-rubric.md` now.** It contains the role-reframing prompt, the full 19-checkpoint rubric, the review file format, and verdict calibration. Follow it exactly to produce the review file.

After writing the review, present its verdict and the blocking issues to the user, then **ask how to proceed**:

> "Self-review is done (verdict: `<verdict>`). Want me to apply the suggested revisions to the draft, apply only some of them, or leave it as-is?"

- If the user asks for revisions, apply them to the **markdown draft in place** and tell them what changed. The user may iterate (re-review, more edits) as many rounds as they want.
- Do not apply revisions silently or without being asked — the user decides what goes in.
- Stay in this phase until the user says they're satisfied with the draft. Only then move on.

---

### Phase 4 — Humanize (ask first)

Once the user is satisfied with the (revised) draft, **ask** whether to humanize it:

> "Would you like me to run the `/humanizer` skill over the draft to make it read less like AI and more like a person wrote it? It rewrites in place; you'll see what changed."

- **Yes** → invoke the `humanizer` skill on the markdown draft, apply its final rewrite to the draft file in place, and summarize the changes. The TD draft is technical/academic, so keep the neutral register — do not inject opinion or first-person color.
- **No** → leave the draft as-is and continue.

After humanizing, the user may want one more look or further tweaks. When they're done, move on.

---

### Phase 5 — Generate the `.docx` (ask first)

This is the final step and the only one that produces a `.docx`. **Ask before doing anything:**

> "Ready for me to generate the final `.docx` from the approved draft?"

Only on a clear yes, **read `./docx-generation.md` now** and follow it. It covers: checking for `pandoc` / `python-docx` and offering to install what's missing, confirming the title / authors / institute / date for the cover, resolving the logo from `docs/assets/logos/` (including what to do when there are zero or multiple logos), running `build_td_docx.py`, and telling the user to update the Word fields.

Do not generate the `.docx` earlier in the flow, and do not reintroduce the old title block — the cover page replaces it.

---

### Phase 6 — Hand off

Mention the full paths of the files that exist (draft, review if produced, `.docx` if generated) so the user can open them immediately.

Then provide a short written summary:
- The verdict from the self-review, if one was run, and whether revisions were applied
- Whether the draft was humanized
- Anything in `../project_context.md` that was missing or incomplete, so the context file can be updated
- If `docs/td/samples/` was empty: a reminder that the TD was generated without house-style calibration
- If a `.docx` was generated: remind the user to update fields in Word (`Ctrl/Cmd+A` then `F9`) so the TOC and page numbers populate, and note whether a logo was used or omitted

---

## Things to get right

- **Pre-flight is non-negotiable.** Do not start drafting without the user's answers. A "generic" TD is worse than no TD.
- **Honor the checkpoints.** Each step (review, humanize, `.docx`) is gated on the user's go-ahead. Stop and ask; never run ahead to the next phase on your own.
- **`.docx` is last and explicit.** Never generate it right after drafting. It comes only after the user approves the draft and confirms they're ready.
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
- Running the self-review, humanizer, or `.docx` step without first asking the user
- Generating the `.docx` right after drafting instead of as the final, approved step
- Reintroducing an AI-style title block at the top of the `.docx` — the cover page replaces it
- Letting the reviewer praise the draft without applying the full 19-checkpoint rubric
- Applying the review's suggested rewrites without the user asking — user decides which land
- Asking the user to provide content that should come from `../project_context.md`, the code, or web search for prior art
- Hedging numbers with vague adjectives ("significant," "substantial," "fast") when concrete values are available