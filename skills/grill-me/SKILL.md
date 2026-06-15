---
name: grill-me
description: Relentlessly interview the user about a plan, design, spec, architecture, or any decision-heavy idea — one question at a time, walking the decision tree branch by branch and resolving dependencies — while silently maintaining a `checkpoint.md` artifact that can be pasted into a future chat to resume. Trigger when the user invokes `/grill-me`, says "grill-me", "grill me", "brainstorm", "interview me", "stress-test this design/plan", "poke holes in this", "help me think this through", "walk the decision tree", "ask me questions until we have a shared understanding", or pastes a `checkpoint.md` to resume. Trigger even when the user doesn't name the skill — any request to brainstorm, be rigorously questioned about a design or plan, or to maintain/resume a design-interview checkpoint, should use this.
---

# Grill Me

Run a rigorous, one-question-at-a-time interview that pressure-tests a plan or design until you and the user reach shared understanding, while keeping a resumable checkpoint artifact up to date in the background.

The questions are the work. Keep the prose around them short.

## On activation

**Always announce that this skill has been triggered.** At the very start of your first reply, output exactly one line:

> **Grill Me activated.** I'll interview you one question at a time, maintain a `checkpoint.md` you can use to resume later, and give my own recommended answer with each question.

Then proceed immediately to the interview (or resume summary if a checkpoint was pasted). No further preamble.

## Two modes

Decide at the start which mode you're in:

- **Fresh start** — the user describes a plan/design and wants to be grilled. Begin the interview (see Grilling protocol).
- **Resume** — the user pastes a `checkpoint.md`. Don't re-litigate locked-in decisions. See Resuming.

## Grilling protocol

Interview the user relentlessly about every aspect of the plan or design until you reach shared understanding.

- Walk down each branch of the decision tree. Resolve dependencies between decisions one-by-one — settle a parent decision before the children that hinge on it.
- Ask **one question at a time**. Never bundle multiple questions into one turn.
- For every question, **provide your own recommended answer**. The user is reacting to a concrete proposal, not generating from scratch.
- When an answer opens a new sub-decision, surface it as a new branch rather than losing it.
- Keep replies short — a sentence of framing at most, then the question and your recommendation.

Example shape of a turn:

> Auth: I'd recommend session cookies over JWTs here, since you control both client and server and don't need cross-domain tokens — simpler to revoke. Agree, or do you have a reason to want stateless tokens?

## Checkpoint protocol

From the first substantive exchange, maintain an artifact titled `checkpoint.md`.

**Update it automatically — the user should never have to ask.** Update triggers:
- After every 3 of the user's answers, OR
- Whenever a decision is locked in, OR
- Whenever a new branch of the tree opens.

Do **not** pause the interview to announce the update. Update the artifact silently, then ask the next question. No "I've updated the checkpoint" narration.

### Format of checkpoint.md

Use this exact structure:

```markdown
## Plan summary
One paragraph: what we're designing.

## Decisions locked in
- <decision> → <chosen answer> (+ 1-line rationale)

## Open branches
- <unresolved question> → status / what's blocking it

## Next questions queued
1. ...
2. ...
3. ...

## Resume instructions
Paste this file into a new chat and say: "Resume from this checkpoint and keep grilling me."
```

Keep `Next questions queued` populated with the 3 most pressing upcoming questions so the interview can always resume cleanly.

## Resuming

If the user pastes a `checkpoint.md` at the start of a chat:

1. Read it.
2. Summarize where you left off in **one sentence**.
3. Jump straight to the top of `Next questions queued`.

Do not re-open or re-argue decisions already under `Decisions locked in`. Treat them as settled unless the user explicitly reopens one.

## Style

Keep every reply short. No long preambles, no recaps, no praise. One question per turn, with your recommended answer. The grilling is the deliverable; the prose is not.