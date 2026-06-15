# TD Samples

This directory contains reference TDs from your organization, used by the `td` skill for two purposes:

1. **Drafting reference** — the skill reads all samples here to calibrate section structure, weight, tone, citation style, and table/figure conventions for new TDs.
2. **Review reference** — during the self-review phase, the reviewer also reads all samples (with explicit instructions to use them as style reference, not content reference).

## What to put here

- Completed TDs that represent the kind of work your organization produces. Anonymized is fine as long as structure and tone survive.
- Blank or partially-filled templates if your org uses a specific template document.

Accepted formats: `.pdf`, `.docx`, `.md`.

## What NOT to put here

- Drafts in progress (those go in the TD output directory, not in samples)
- TDs from other organizations with different conventions
- Marketing material or pitch decks (different document type)

## House-convention deviations from samples

If your organization's TDs have evolved away from some convention that older samples still reflect, document the deviation in this file. The `td` skill reads this README and will apply the deviation rules during both drafting and review.

Format suggestion:

```markdown
## Deviations from samples

- **Competitor naming:** older TDs name specific commercial competitors directly (Company X's Product Y). Current convention is generic descriptions ("leading commercial platforms in this category"). Apply to Lit Review and Introduction sections.
- **Section header style:** older TDs use sentence case; current convention is title case.
- (etc.)
```

Without documented deviations, the skill matches the samples as-is. With them, the skill prefers the documented rule over what the samples show.

## How the skill behaves when this directory is empty

If you haven't added any samples yet (only this README is here), the `td` skill will ask you the first time you invoke it:
- (a) drop sample TDs in here and try again
- (b) proceed without samples and get a best-effort generic TD

Option (b) works but the output won't match your house style. Adding at least one sample dramatically improves quality.