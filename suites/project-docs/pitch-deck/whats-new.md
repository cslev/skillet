# Mode (b) — What's-new / release showcase

Level 3 reference for the pitch-deck skill. Read only when the user picked mode (b) in Step 1. Covers the source tiers (Step 2), the outlines (Step 3), and mode-(b)-specific pitfalls.

---

## Source strategy by comparison frame

### Frame (i) — Released version vs released version

The deck is about a specific release. If release docs for that version exist, they ARE the curated answer. Check tiers:

**Tier 1 — Release docs for the new version exist** in `docs/releases/` (User Guide and/or Technical Guide for `<NEW>`). **Prefer them as the source of truth.** They've already been generated through the documentation skill (or by the user manually) and the change inventory was validated. Read both guides if both exist; the User Guide framing tends to be more pitch-friendly (operational impact, user-facing capability), while the Technical Guide gives the implementation depth a technical attendee may ask about. The `[New in v<NEW>]` markers in those docs are authoritative — every item carrying that marker is a candidate for the pitch deck.

Do **not** re-run git log or re-read the changelog when Tier 1 applies. The markers in the guides already encode that work.

**Tier 2 — Release docs exist for the previous version but not the new one.** Read the previous-version docs to understand the "before" state, then determine the delta via the changelog and:
```bash
git log <previous-version-tag>..<new-version-tag-or-HEAD> --oneline --no-merges
```
Mention to the user once: "I don't have v<NEW> release docs, so I'm building from the v<PREVIOUS> docs plus changelog and git log. You may want to run the documentation skill first for a more reliable result."

**Tier 3 — No release docs in `docs/releases/` at all.** Fall back to gathering change signal from scratch via the changelog, git log, and code inspection.

### Frame (ii) — Current state vs a previous version

The deck is about *where things are now*, not about a specific release. Docs reflect a past snapshot (potentially months old) and are NOT the source of truth for current state. **Always use git/changelog/code as the primary source, regardless of whether docs exist.**

Gather change signal:
1. **Changelog** — read everything after the comparison-anchor version. If the changelog has a Keep-a-Changelog-style "Unreleased" section, read that too.
2. **Git log since the anchor version**, all the way to current HEAD: `git log <anchor-version-tag>..HEAD --oneline --no-merges`. Pay attention to dates — recency matters for status decks.
3. **Code inspection** for anything ambiguous.

Docs (if they exist for the anchor version) are useful as a **reference for the "before" state only** — to remind yourself what the project looked like at the anchor, then frame what's new relative to that. Do not use docs as the source of "what's new" itself.

---

## Pitch-relevant change inventory (both frames)

Narrower than the release-doc change inventory. Only include:

- **Headline additions** — major new capabilities a non-engineer would care about
- **Notable improvements** — performance, scale, accuracy gains with concrete numbers
- **Architectural shifts** — meaningful changes to how the system works
- **Work in progress** — *frame (ii) only* — significant ongoing efforts worth flagging, marked clearly as in-progress

Explicitly **exclude**: bug fixes, internal refactors, minor parameter changes, dependency bumps.

Share the inventory with the user and ask them to confirm or trim before generating the outline.

---

## Outlines

Role labels below are for structure only — every content slide still gets an **assertion title** (see `../deck-style.md`).

**Frame (i) — Version-vs-version** (standard length):
1. **Title** — comparison framing, e.g. `What's new from v1.5 to v2.0`
2. **Quick recap (optional)** — if some audience members may be new
3. **At a glance** — 3–6 items from the change inventory
4. **Each major addition** — one slide each, with the `[New in v<NEW>]` marker
5. **Improvements** — concrete numbers
6. **Architectural shifts** — before/after diagram placeholder if applicable
7. **What this enables** — capability framing, stated as concrete use cases

**Frame (ii) — Current state** (standard length):
1. **Title** — status framing, e.g. `Where we are, October 2026` or `Progress since v<ANCHOR>`. Avoid version-delta framing — this isn't one.
2. **Quick recap (optional)**
3. **Headline progress** — 3–6 items, ordered by impact, not chronology
4. **Each headline item** — frame as "we now do X", not "v<X> adds X". Use `[In progress]` for unshipped work.
5. **Improvements**
6. **Architectural shifts** — if any
7. **What's next (optional)** — only if the user asked for it

**Markers:** `[New in v<NEW>]` applies in frame (i) only. Frame (ii) uses `[In progress]` for unshipped work and no marker for shipped items. Markers are plain text after the title or first bullet — never a badge or pill.

---

## Mode (b) pitfalls

- In frame (i) Tier 1 (v<NEW> docs exist), re-running git log to second-guess the docs
- In frame (ii), trusting docs as the source of "what's new" — docs are a snapshot, not current state
- Highlighting bug fixes or internal refactors that don't matter to the audience
- Framing a frame (ii) deck as a version-vs-version delta
- Adding source-tier warnings *inside* the deck
