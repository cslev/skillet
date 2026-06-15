# TD Deck — Template-Specific Instructions

> **This file is a starting template. Replace the placeholder content below with the actual slide structure of your `template.pptx`.** The skill reads this file to know how to map TD sections to your template's slides. The more precise and accurate this file is, the better the generated deck will be.
>
> This file lives in `./samples/` and is gitignored — safe to include company-specific details here.

---

## Template overview

Describe your template briefly here. Example:
- Number of slides: _N_
- Available layouts: _list them_ (e.g. Cover, Content, Divider, Closing)
- Slide dimensions: _e.g. 13.33" × 7.50" (widescreen 16:9)_

---

## Slide mapping

For each slide in your template, specify:
- The slide's **title/purpose**
- Which **TD section** provides the content
- The **slide count limit** (if the template enforces one)
- Whether the slide **requires user input** (i.e. cannot be filled from the TD alone)

Replace the example rows below with your actual template's slides.

| Slide # | Template title | TD source | Limit | Notes |
|---|---|---|---|---|
| 1 | Cover / Title | TD title, authors, date | 1 | Fill inventor names and department from TD metadata |
| 2 | Problem statement | Introduction — problem section | 1 | One sentence, plain language, application context |
| 3 | Solution overview | Technical Description — architecture | 2 max | Use diagram placeholder |
| 4 | Innovative elements | Introduction — innovation claim | 2 max | State new algorithm vs adaptation |
| 5 | Technical description | Technical Description — algorithm steps | 3 max | Enough detail to implement |
| 6 | Results | Results/Evaluation | 3 max | Concrete numbers, verbatim from TD |
| 7 | Benchmarking | Results — baseline comparisons | 2 max | Quantitative only |
| 8 | Limitations | Limitations section | 2 max | State what doesn't work and why |
| 9 | Other applications | Conclusion / Future Work | 1 | Where else this applies |
| 10 | Claims | Synthesize from novelty angle | 1 | Top 3 patent claims — present drafts to user for confirmation before generating |
| 11 | IP / Commercial | _User fills_ | 1 | Cannot be derived from TD — flag in hand-off |
| 12 | Closing | Leave as-is from template | 1 | No content needed |

---

## Slides requiring user input

List slides that cannot be filled from the TD. The skill will leave these flagged in the hand-off summary rather than attempting to fill them.

- Slide 11 — IP/Commercial: requires deployment readiness status, licensing plans, and related patent information not present in the TD.
- _(add others as needed)_

---

## Content placeholder conventions

Describe how content placeholders work in your template so the skill knows which shape to fill:

- **Title placeholder** — shape name or index used for the slide heading (e.g. `Text Placeholder 2`, idx=1)
- **Content placeholder** — shape name or index used for the main body (e.g. `Rectangle 3`, idx=2). Contains instructional text in the template — always replace entirely, never append.
- **Footer placeholder** — if present, leave as-is.

---

## Special handling notes

Add any other conventions here. Examples:
- "Diagram slides use a diagram placeholder rectangle — do not attempt to auto-generate diagrams"
- "Claims must reference specific slide numbers in the final deck"
- "The Benchmarking slide expects a results table, not bullet points"
