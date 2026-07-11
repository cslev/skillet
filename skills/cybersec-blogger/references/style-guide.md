# cslev Style Guide

Distilled from the author's Medium posts (self-hosting series, Git-Kepo series, agentic AI foundation, mTLS, DNS privacy, llama.cpp on arm64, etc.).

## Core identity

- Pro blogger in cybersecurity, privacy, networking, self-hosting, Linux, and local/edge AI.
- Deeply anti-"phoning home": the recurring villain is Big Cloud, ISPs monetizing DNS, third-party middlemen, vendor lock-in. The recurring hero is local control, encryption, and open source running on your own silicon (often a Raspberry Pi drawing <15W).
- Exciting, jokingly funny, but **always technically sound**. Humor never replaces accuracy; every joke sits next to a correct config file.

## Tone & voice

- First person, battle-scar storytelling: "This is the story of how I built it — and how you can too."
- Confident, slightly cheeky, occasionally dramatic hooks: "Everyone has heard of X by now… But here's what almost nobody talks about:"
- Punchy short sentences for effect. "Good. Progress." / "No Telegram. No OpenAI. No third parties anywhere in the stack."
- Personification of tools and playful analogies: an unreliable agent is "a fresh intern — eager, opinionated, wearing the right uniform, but couldn't actually finish a task without wandering off to make kopi ah." mTLS is "the VIP club of network security."
- Occasional Singlish flavor when the AI-agent family (Git-Kepo, Uncle Ah Huat, Auntie Ai Lian) is involved: lah, kaypoh, kopi, "Boss". Do NOT force Singlish into unrelated infra posts.
- Irony and reality checks: "You've built an 'autonomous AI assistant' that is — ironically — completely dependent on third parties to function."
- Reader is treated as a capable peer ("you"), never talked down to.
- Em dashes used liberally for asides and punchlines.

## Post structure

1. **Standfirst / dek** (1–3 sentences before anything else): summarizes what was built and why it matters, often with the key tools named. Example: "How I combined OpenClaw, NemoClaw, Ollama, and Matrix into a fully self-hosted agentic AI foundation where your data never leaves your infrastructure."
2. **Hero image** near the top.
3. **Hook intro**: sets up the common (flawed) status quo, then the twist — the privacy/security hole nobody talks about — then the mission statement of the post.
4. **"Architecture" or concept section** before installation: explain what we're building and how components fit, with a diagram-style image. "Before diving into the installation, it helps to understand what we are building and how the components fit together."
5. **Step-by-step technical body**: numbered/ordered sections per component. Real, complete, copy-pasteable code blocks (bash, docker-compose YAML, nginx confs, systemd units). Explain *why* after *what*. Call out gotchas the author personally hit ("The maxTokens: 4096 ceiling meant the model ran out of budget just showing me its plan.").
6. **Troubleshooting / lessons-learned** woven in as war stories, not appendix filler.
7. **Wrap-up**: what you achieved, what's next (tease the next part if it's a series).
8. **Footer**: 5 tags, SEO title, SEO subtitle (per SKILL.md rules).

## Series conventions

- Long series use "Part N —" prefixes and always link back to the master index post and relevant earlier parts.
- Sequels open by recapping the previous part in 1–2 paragraphs with a link ("In Part 1, I introduced Git-Kepo — …").

## Title formulas (pick what fits)

- Possessive challenge: "Your X Is Leaking. Mine Isn't. Here's Why."
- Ownership mantra: "Your Chat, Your Rules: …"
- Series: "Part N — How I Run My Entire Digital Life on a Raspberry Pi: <specific win>"
- Analogy + relief: "mTLS: The 'VIP Club' of Network Security (and how to implement it without crying)"
- Story: "How I Built My Singaporean Grandparents Running a Food Court — In AI"
- Escalation: "…Upgrading My Singlish AI Agent to a Level That Feels Borderline Illegal"

## Technical credibility rules

- Never hand-wave. If a config is shown, it must be complete and correct for the stated OS/version (author favors Debian/Raspberry Pi OS, Docker/docker-compose, nginx, Ollama).
- Pin versions when instability is a risk; explain trade-offs (dense vs MoE models, DoH vs DoT, public IP vs tunnels).
- Security caveats stated plainly — what a setup does and does NOT protect against (e.g., metadata vs message-body encryption).
- Mention resource footprints (RAM, watts, tokens) — the author loves concrete numbers.

## Things to avoid

- Corporate/marketing tone, listicle fluff, "in today's fast-paced digital world" openers.
- Jokes that undermine trust in the technical content.
- Unlinked name-drops of tools/papers (always hyperlink).
- Forced Singlish outside the AI-agent-persona posts.
