# Extracting a style from a reference deck

Read this when Required reading step 4 finds a `.pptx` in `docs/decks/samples/` or `docs/decks/`.

**This is style adaptation, not template filling.** That distinction matters because `td-deck` works the opposite way: it fills a fixed `template.pptx` slide-for-slide and never adds, removes or reorders slides. Here, the reference deck supplies *how the deck looks* — fonts, colours, positions, logo treatment. The outline, slide count, structure and layout choices from `pitch-deck/SKILL.md` Step 3 are entirely this skill's own. Never copy the reference deck's text, slide order, or slide count.

## Which file

The most recently modified `.pptx` in `docs/decks/samples/`; if that's empty, the most recent in `docs/decks/`. If more than one plausible style file sits in `samples/`, ask the user which one to use.

## Step 1 — Classify each slide by role

Open the deck and sort every slide into one role, by its background fill and its largest text block:

- **Title** — slide 1, or any slide with a distinct background whose largest text reads as a deck or company name, not a sentence.
- **Section divider** — shares a distinct background (often the title slide's) and appears more than once, with short text and no body content.
- **Closing** — the last slide, especially if its background echoes the title slide.
- **Content** — everything else. If the deck contains more than one recognisable content pattern (e.g. some slides have an image area and some don't), record each pattern separately — you need one token set per pattern you intend to use.

If the deck is too short or too uniform to tell roles apart, say so and fall back to the default visual system (`../deck-style.md` §4), keeping only whatever is unambiguous (e.g. a clear font or accent colour).

## Step 2 — Extract concrete tokens per role

For each role found, record:

| Token | Where to look |
|---|---|
| Background | the slide background fill, or a full-bleed rectangle behind everything |
| Title font, size, colour, weight | the slide's largest text run |
| Title position | that text box's left / top / width |
| Body font, size, colour | a representative paragraph on a content slide |
| Body position, margins | the body placeholder or textbox's left / top |
| Accent colour(s) | any text or shape colour that isn't the title, body or background colour, used sparingly |
| Logo | a picture shape repeated across slides at a consistent position and size |
| Footer | any small recurring text (page number, company name) and its position |

Write this down as a token table before building anything — it replaces the table in `../deck-style.md` §4 for this run.

## Step 3 — Reconcile with the brand questions

- If `docs/assets/logos/` already has a logo, prefer it over one extracted from the reference deck — the user-provided file is authoritative. Mention it if the reference deck's embedded logo differs.
- Offer the reference deck's colours as the "From `<file>`" option in the colour-template question (`../deck-style.md` §4), pre-filled with the extracted hex values, not just the filename. The user still approves it like any other option.
- Font comes from the extracted title/body fonts; don't ask separately unless extraction failed.

## Step 4 — Build with the skill's own rules

Everything else is unchanged: the core message, outline, slide count, assertion titles, layout choices (Text / Text + visual / Full-width visual / Big number / Statement), the banned vocabulary and visual bans, and the quality gate (`../deck-style.md`). The reference deck supplies the look; it never supplies the content or the slide count.

If the outline needs a role the reference deck doesn't have (e.g. it wants a divider but the reference deck has none), build it from the closest extracted role — apply the title slide's background and font to the divider spec in `../deck-style.md` §4 — rather than inventing an unrelated style for it.
