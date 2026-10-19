# pitch-deck: a deck builder that works from your outline

## Deck

- **Core message:** pitch-deck turns an outline into a slide deck built on your own template, holds it to anti-slop rules, and edits one slide without touching the rest.
- **Supporting points:**
  1. It acts only on the outline: no invented facts, no silent rewording, no generated images.
  2. It reads your template and builds every slide from its real layouts.
  3. Without a template, it applies a design system and rules that remove the tells of a generated deck.
  4. A linter and a render check gate delivery.
  5. It updates a single slide in place and proves the others are unchanged.
- **Audience:** engineers and teams who use Claude Code skills and build decks regularly; technical, not designers.
- **Length:** 12 content slides plus 2 dividers, about 12 minutes.
- **Filename:** PitchDeckSkill_2026-10-19.pptx
- **Template:**
- **Logo:** examples/cslev_logo.png
- **Off-limits:** none.

---

## Slide 1 — pitch-deck: a deck builder that works from your outline

**Role:** title

**On slide:**
- Subtitle: A Claude Code skill for template-faithful decks without the AI tells
- Presenter: Levente Csikor
- Date: 19 October 2026
- Footer: github.com/cslev/skillet

**Speaker notes:** This is a Claude Code skill that turns a markdown outline into a PowerPoint deck. Two things set it apart: it builds on your organisation's own template, and it holds the result to rules that stop it from looking machine-made.

---

## Slide 2 — Generated decks ignore your template and look generated

**Role:** content
**Layout hint:** text

**On slide:**
- Slides arrive in a default style, not your company template
- Titles name a topic instead of making a point
- Bullet lists come in threes, with the same rhythm on every slide
- Gaps in the source get filled with plausible facts
- Fixing one slide means regenerating the whole deck

**Speaker notes:** These are the five habits the skill is built against. The first is about fit: the deck should look like it belongs to you. The next three are the tells that make a deck read as generated. The last one is practical: if you change one slide, you do not want the other nineteen to move.

---

## Slide 3 — The skill takes an outline and returns a deck, nothing more

**Role:** content
**Layout hint:** diagram

**On slide:**
- Input: outline.md, required
- Input: your template .pptx, optional
- Input: your logo, optional
- Output: a .pptx in decks, ending in a Thank-you slide

**Visual:** a flow from the three inputs, through the pitch-deck skill, to the finished deck. The outline box is drawn heavier than the other two inputs.

**Speaker notes:** Writing the outline is a separate step. You can do it by hand, or have any agent draft it from your papers, docs or code. The skill never reads those sources and never adds facts of its own. The only slide it adds on its own is the Thank-you slide at the end.

---

## Slide 4 — Built on your template

**Role:** divider

**On slide:**
- Subtitle: Interpreting a company template, layout by layout

**Speaker notes:** First part: what happens when you give the skill a template.

---

## Slide 5 — The skill labels every layout in your template

**Role:** content
**Layout hint:** table

**On slide:**
- One script reports fonts, colours, logo and every named layout
- The same template always gives the same analysis

**Chart or table data:** example from a 29-layout company template

| Layout name | Role the skill assigns | Content tag |
|---|---|---|
| Cover 1 | title | none |
| Divider 1A | divider | none |
| Content 1: Paragraph | content | paragraph |
| Content 4: Table | content | table |
| Closing 1 | closing | none |

**Source:** style_from_reference.py run on a corporate template

**Speaker notes:** The analysis is a script, not a guess by the model, so it is repeatable. It guesses a role for each layout from its name and its placeholders, and says when it is unsure. The roles it looks for are title, divider, content and closing. Each content layout also gets a tag such as paragraph, table or text with image.

---

## Slide 6 — Every slide comes from a real layout, never an imitation

**Role:** content
**Layout hint:** text

**On slide:**
- Strict layout reuse: each slide instantiates one of your template's own layouts
- Masters, placeholders, logo and artwork stay exactly as designed
- Charts and tables are native PowerPoint objects, built from the outline's numbers
- Style only: a loose example deck gives fonts, colours and logo
- You approve the slide-to-layout table before anything is built

**Speaker notes:** Strict reuse is the default for a real template. If the file is only one or two example slides, the skill takes just its style and builds with its own design. Either way you see the mapping first, with any slide that has no good layout flagged.

---

## Slide 7 — Layout names can lie, so the skill renders them first

**Role:** content
**Layout hint:** text

**On slide:**
- A cover layout may carry a photo baked into the layout
- A closing layout may carry fixed Thank-you text
- A text placeholder can secretly be a coloured panel
- Unfilled placeholders print Click to add text
- Setting a title's text can drop its formatting

**Speaker notes:** Each of these showed up while building a conference deck on a company template. The skill renders the layouts it plans to use before building, deletes placeholders it does not fill, keeps decorative panels, and uses a helper that preserves a run's formatting.

---

## Slide 8 — Held to anti-slop rules

**Role:** divider

**On slide:**
- Subtitle: What stops a deck from looking generated

**Speaker notes:** Second part: the rules. They matter most when there is no template, because then the skill designs the deck itself.

---

## Slide 9 — Titles state the point, not the topic

**Role:** content
**Layout hint:** table

**On slide:**
- Titles are short sentences in sentence case, with no ending punctuation
- Read in order, the titles tell the story

**Chart or table data:**

| Topic label | Assertion title |
|---|---|
| Architecture | Three services share one event queue |
| Performance | Ingest latency fell from 4 s to 300 ms |

**Source:** reference/deck-style.md, section 2

**Speaker notes:** This is the single most visible rule. A topic label tells you where you are; an assertion tells you what to conclude. The skill also bans question titles, the X colon The Y of Z formula, and series counters.

---

## Slide 10 — Visual bans remove the tells of a generated deck

**Role:** content
**Layout hint:** text

**On slide:**
- No eyebrow labels, badges or pills; the title is the topmost text
- No shadows, glows, gradients, rounded boxes or decorative accent bars
- No icon-card grids, stat-tile dashboards or page-counter chrome
- No purple or indigo palettes, no cream with terracotta and a serif
- One accent colour, one font family, charts that are native and labelled

**Speaker notes:** Each of these is a common mark of a generated deck. The design comes from a consistent frame and big-type section slides, not from ornaments added per element. When a template is used, none of these rules restyle the template; they apply only to shapes the skill adds.

---

## Slide 11 — A linter and a render check gate delivery

**Role:** content
**Layout hint:** text + visual

**On slide:**
- The linter checks banned words, em dashes, title case and length limits
- A deck with errors is not delivered
- Then the deck is rendered and every page is inspected

**Visual:** a code box:

```
python3 scripts/lint_deck.py deck.pptx --max-words 60
0 error(s), 0 warning(s)
```

**Speaker notes:** The linter exits with a failure code on errors, so the rules are acceptance criteria, not suggestions. The render check catches what a linter cannot: clipped text, overlapping shapes, empty placeholders. Warnings need a judgment call and are listed in the hand-off.

---

## Slide 12 — Your outline stays yours: the skill flags, you decide

**Role:** content
**Layout hint:** diagram

**On slide:**
- The skill lists every outline problem with a proposed fix
- You apply all, apply none, or choose per item
- Terms and spellings in the outline win over the vocabulary bans
- It never states a cause the outline's own numbers do not support

**Visual:** a three-step flow: check the outline, propose fixes, you decide.

**Speaker notes:** This is the contract. The outline is the only source of content. The skill reports conflicts and claims the numbers cannot support, but it does not quietly reword. If your product's name is a banned word, it is allowed and listed in the hand-off.

---

## Slide 13 — Change one slide without touching the rest

**Role:** content
**Layout hint:** text + visual

**On slide:**
- Say it plainly: redo slide 13, or add a slide after 12
- It edits the deck as it is now, manual changes included
- A before and after comparison proves the other slides are unchanged

**Visual:** a code box:

```
slide_guard.py snapshot deck.pptx snap.json
slide_guard.py compare deck.pptx snap.json --changed 13
guard passed: 20 slides, only [13] changed
```

**Speaker notes:** Update mode never regenerates the deck, because you may have edited it by hand. It takes a backup and a snapshot, changes the one slide in place, and checks that every other slide is byte for byte identical.

---

## Slide 14 — Copy the folder, write an outline, ask for the deck

**Role:** content
**Layout hint:** text + visual

**On slide:**
- Copy skills/pitch-deck into .claude/skills in a project, or into your home .claude/skills
- Put your template and logo in the project's decks folder
- Write outline.md from the skill's template, then ask for the deck

**Visual:** a QR code for github.com/cslev/skillet, supplied later.

**Speaker notes:** Everything is in the skillet repository. The skill looks for the template and logo in a fixed order: the path you name, the outline's front matter, the project's decks folder.
