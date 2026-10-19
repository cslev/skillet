# Credits

## Rules inspiration

The copy rules and visual bans in `reference/deck-style.md`, and the checks in `scripts/lint_deck.py`, were written independently for this skill after reviewing the projects and articles below (2026-10-06). Ideas were borrowed; no text or code was copied.

- **prznt-deck** by Prznt Perfect (MIT licence): https://github.com/przntperfect/prznt-deck. Hard visual bans, sentence-case and en-dash rules, the line-end short-word rule, outline approval before building, and a linter that gates delivery on its exit code.
- **anti-ai-slop** by Vinayak Shukla (MIT licence): https://github.com/Vinayak-Shukla-03/anti-ai-slop. Bullet-rhythm and same-grid tells, stat-tile dashboards, page-counter chrome, fake variety, unattributed quotes, honest comparison tables, the any-topic test.
- **"How to make AI slides that don't look AI-generated: a consultant's guide (2026)"**, Perceptis: https://perceptis.ai/blog/how-to-make-ai-slides-that-don-t-look-ai-generated-a-consultant-s-guide-2026. Governing thought first, no invented explanations, on-slide source lines, native editable charts, the editing pass.
- **"How to make AI slides that don't look like AI slop"**, Plus AI: https://plusai.com/blog/how-to-make-ai-slides-that-dont-look-like-ai-slop. Accent-bar and dashboard tells, and asking for brand colours and fonts instead of improvising a palette.

## Icons

`scripts/icon_to_png.py` fetches icons from **Lucide** (ISC licence): https://lucide.dev. They are downloaded at run time into the generated deck; none are bundled in this skill.
