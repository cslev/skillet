# Credits

## `deck-style.md` and `lint_deck.py`

Several rules are adapted from **prznt-deck** by Prznt Perfect (MIT licence): https://github.com/przntperfect/prznt-deck (`SKILL.md`, `references/rules.md`, `scripts/inspect_pptx.py`), reviewed 2026-10-06.

The original is a brand-locked design system with its own python-pptx engine. This skill borrows its brand-neutral ideas: the hard bans (eyebrows, badges, text in filled shapes, shadows, rounded corners), sentence-case and en-dash rules, the line-end short-word rule, collapsing series slides, outline approval via AskUserQuestion, and a linter that gates delivery on its exit code. The vocabulary bans, assertion titles, default visual system, template-precedence rule, render check and the linter code are written for this skill. No text or code was copied verbatim.

Further rules were added on 2026-10-06 after reviewing these sources:

- **anti-ai-slop** by Vinayak Shukla (MIT licence): https://github.com/Vinayak-Shukla-03/anti-ai-slop (`SKILL.md`, `references/presentations.md`). Source of the bullet-rhythm and same-grid tells, stat-tile dashboards, page-counter chrome, fake variety, the "coloured last word" title, the second-order cream/terracotta/serif palette, unattributed quotes, honest comparison tables and the any-topic test.
- **"How to make AI slides that don't look AI-generated: a consultant's guide (2026)"**, Perceptis: https://perceptis.ai/blog/how-to-make-ai-slides-that-don-t-look-ai-generated-a-consultant-s-guide-2026. Source of the governing-thought-first outline, no invented explanations, on-slide source lines, native editable charts matched to the claim, and the editing pass.
- **"How to make AI slides that don't look like AI slop"**, Plus AI: https://plusai.com/blog/how-to-make-ai-slides-that-dont-look-like-ai-slop. Source of the accent-bar and dashboard tells, and asking for brand colours and fonts instead of improvising a palette.

All rules were rewritten for this skill; nothing was copied verbatim.

## `icon_to_png.py`

Fetches icons from **Lucide** (ISC licence): https://lucide.dev, https://github.com/lucide-icons/lucide. Icons are downloaded at run time into the generated deck; none are bundled.

## `logo_palette.py`

Written for this skill. Contrast thresholds follow WCAG 2.x (4.5 : 1 for text, 3 : 1 for graphics).

## `style_from_reference.py`

Written for this skill. Reuses the WCAG contrast math from `logo_palette.py`. Catalogues a real template's own named layouts (role, placeholder types and positions) as well as extracting its fonts, colours and logo, so the same template always yields the same analysis.

## `deck_lib.py` and `slide_guard.py`

Written for this skill, from the problems met building a conference deck on a corporate template: dropping demo slides, losing run formatting on placeholders, unfilled placeholders, charts with annotations positioned against a manual plot layout, and proving a single-slide edit left the rest untouched.
