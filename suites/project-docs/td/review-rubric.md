# TD Self-Review Rubric

Reference file for Phase 3 of the TD skill. Read this at the start of Phase 3 — do not load it earlier.

---

## 3a. Reset context explicitly

Before reading the draft, state to yourself (in your reasoning, not necessarily out loud to the user):

> "I am now a critical-but-fair member of an internal Technology Disclosure review board. I have not seen this TD before. I have reviewed many TDs and would reject approximately 30% of submissions outright and accept the rest with revisions of varying severity. My job is to find problems, not to validate the author's choices. 'Looks good overall' is a failure of my role. If I feel a temptation to recognize the document or its arguments, I treat that recognition as suspicious — I am a reviewer, not an author.
>
> I have access to: the draft TD and the samples in `docs/td/samples/` (if any). I do not have access to `../project_context.md`, the drafting workflow, or any other context about how this TD was produced. I judge the document on its own merits."

Then read:
1. The draft (just written, but approach it as if seeing it for the first time)
2. All files in `docs/td/samples/` if present — used as **style reference**, not content reference. The reviewer compares tone, structure, and weight to the samples, not specific content.
3. `docs/td/samples/README.md` if present — any documented house-convention deviations apply to the reviewer's judgment too. The reviewer should NOT flag the draft for following a documented deviation; the reviewer SHOULD flag the draft for ignoring one.

If `docs/td/samples/` was empty (and the user chose to proceed anyway in the Phase 1 / samples-handling step), the reviewer works from abstract conventions only. Note this explicitly in the review verdict.

---

## 3b. Apply the rubric

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
16. Does the draft respect any documented house-convention deviations in `docs/td/samples/README.md`? If the README documents a rule the draft violates, flag it.

**Reviewer's gut check**
17. Reading this cold, would I recommend it for further consideration, or would I bounce it back?
18. If I had to summarize the contribution in one sentence to a colleague, could I, based only on this document?
19. Is there any section I would have skipped while reading because it didn't add value?

---

## 3c. Write the review file

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
