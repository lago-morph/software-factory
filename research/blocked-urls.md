# Blocked URLs — Sandbox Reachability Report
**Date:** 2026-05-10
**Purpose:** Six of seven research subagents reported HTTP 403 ("host not allowed" / "host not in allowlist") from a substantial portion of their assigned source domains. This document lists every URL that was blocked so the user can fetch them externally and re-feed the content for a higher-fidelity second pass.

---

## What was blocked, by domain

| Domain | Status | Notes |
|---|---|---|
| `factory.strongdm.ai` | Blocked (403) | All paths — homepage, principles, techniques + sub-pages, products + sub-pages |
| `every.to` | Blocked (403, Cloudflare) | The guide and the chain-of-thought / source-code articles |
| `simonwillison.net` | Blocked (403) | All paths — software-factory post, agentic-engineering-patterns guide hierarchy, adjacent posts |
| `news.ycombinator.com` | Blocked (403) | The HN thread itemid 46924426 |
| `lennysnewsletter.com` | Blocked (403) | The AI state-of-the-union piece |
| `el-kaim.com` | Blocked (403, Medium custom domain) | The Dark Factory article |
| Substack mirrors of Simon Willison | Blocked (403) | Used as fallback |

| Domain | Status | Notes |
|---|---|---|
| `github.com` (web) | Accessible | Used for repo browsing |
| `raw.githubusercontent.com` | Accessible | Primary source for repo file contents |

---

## Initial-sources.md URLs — fetch status

From `initial-sources.md`, every URL the user originally listed:

| URL | Status |
|---|---|
| https://factory.strongdm.ai/products/attractor | ❌ blocked |
| https://github.com/strongdm/attractor | ✅ fetched (raw URLs) |
| https://factory.strongdm.ai/ | ❌ blocked |
| https://factory.strongdm.ai/principles | ❌ blocked |
| https://factory.strongdm.ai/techniques | ❌ blocked |
| https://every.to/guides/compound-engineering | ❌ blocked |
| https://github.com/everyinc/compound-engineering-plugin | ✅ fetched |
| https://github.com/EveryInc/compound-knowledge-plugin | ✅ fetched |
| https://github.com/EveryInc/claude_commands | ✅ fetched |
| https://github.com/EveryInc/symphony-thumbtack | ✅ fetched |
| https://github.com/EveryInc/everyskill/tree/main/skills | ✅ fetched |
| https://simonwillison.net/2026/Feb/7/software-factory/ | ❌ blocked |
| https://news.ycombinator.com/item?id=46924426 | ❌ blocked |
| https://www.lennysnewsletter.com/p/an-ai-state-of-the-union | ❌ blocked |
| https://simonwillison.net/guides/agentic-engineering-patterns/ | ❌ blocked |
| https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e | ❌ blocked |

---

## Specific URLs the research agents wanted to read (and were blocked)

These are the URLs that subagents *tried* to fetch, beyond the original initial-sources.md list. Re-feeding the content of these to the lead designer would tighten quotations and possibly surface chapters/sections that were reconstructed from secondary sources.

### StrongDM Factory (subagent 01) — all blocked

- https://factory.strongdm.ai/
- https://factory.strongdm.ai/principles
- https://factory.strongdm.ai/techniques
- https://factory.strongdm.ai/techniques/gene-transfusion
- https://factory.strongdm.ai/techniques/pyramid-summaries
- https://factory.strongdm.ai/techniques/dtu (Digital Twin Users)
- https://factory.strongdm.ai/techniques/semport (Semantic Ports / Semports)
- https://factory.strongdm.ai/techniques/scenarios (if it exists as a distinct page)
- https://factory.strongdm.ai/techniques/satisfaction (if it exists as a distinct page)
- https://factory.strongdm.ai/techniques/shift-work (referenced but not directly readable)
- https://factory.strongdm.ai/products
- https://factory.strongdm.ai/products/attractor
- https://factory.strongdm.ai/products/cxdb
- https://factory.strongdm.ai/products/strongdm-id (if it exists)

### Every.to compound engineering (subagent 03) — all blocked

- https://every.to/guides/compound-engineering
- https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents
- https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it
- https://every.to/p/the-agent-that-saved-my-brain
- Any sub-pages within /guides/compound-engineering/ if such hierarchy exists

### Simon Willison (subagent 05) — all blocked

- https://simonwillison.net/2026/Feb/7/software-factory/
- https://simonwillison.net/guides/agentic-engineering-patterns/ (index)
- https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/
- https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/
- https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/
- https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
- https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/
- https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/
- https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/
- https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/
- https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/
- https://simonwillison.net/guides/agentic-engineering-patterns/subagents/
- https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/
- https://simonwillison.net/guides/agentic-engineering-patterns/prompts/
- https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/ (meta-post about the guide)
- https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
- https://simonwillison.net/2025/Oct/5/parallel-coding-agents/
- https://simonwillison.net/2025/May/22/tools-in-a-loop/
- https://simonwillison.net/2025/Sep/18/agents/
- https://simonwillison.net/2025/Apr/19/claude-code-best-practices/
- https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/
- https://simonwillison.net/2026/Apr/2/lennys-podcast/
- https://simonwillison.net/2025/Dec/10/normalization-of-deviance/
- https://simonwillison.net/2025/Apr/11/camel/
- https://simonwillison.net/tags/evals/
- https://simonwillison.net/tags/agentic-engineering/

### HN + Lenny (subagent 06) — all blocked

- https://news.ycombinator.com/item?id=46924426 (the thread)
- Specific HN comment IDs from this thread: 46955602, 46931733, 46926133 (would not be reachable individually anyway since they're inside the thread)
- https://www.lennysnewsletter.com/p/an-ai-state-of-the-union
- https://www.lennysnewsletter.com/p/the-coming-ai-security-crisis (Schulhoff piece referenced)
- https://www.lennysnewsletter.com/p/ai-prompt-engineering-in-2025-sander-schulhoff
- https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens (Boris Cherny piece — the highest-leverage referenced post)
- https://www.lennysnewsletter.com/p/naming-expert-david-placek

### El Kaim Dark Factory (subagent 07) — all blocked

- https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e

---

## Other URLs the research surfaced as worth pursuing (status mixed)

Subagents recommended these as additional sources for a future research round. Not yet fetched.

| URL | Why useful | Status |
|---|---|---|
| https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ | Stanford CodeX legal/governance critique of dark factories | unknown |
| https://www.thepragmaticcto.com/p/the-software-factory-when-no-human | Detailed pitfalls write-up | unknown |
| https://rywalker.com/research/strongdm-factory | Independent technique annotation | unknown |
| https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ | The 0–5 maturity framing El Kaim cites | unknown |
| https://2389.ai/posts/the-dark-factory-is-a-dot-file/ | Deep dive on Gas Town's DOT orchestration | unknown |
| https://github.com/gastownhall/gastown | The Gas Town orchestration repo | likely accessible (GitHub) |
| https://github.com/gastownhall/beads | The Beads task-graph repo | likely accessible (GitHub) |
| https://github.com/openai/codex | codex-rs reference for Attractor's OpenAI profile | likely accessible (GitHub) |
| https://github.com/anthropics/claude-code | Claude Code reference | likely accessible (GitHub) |
| https://github.com/google-gemini/gemini-cli | gemini-cli reference | likely accessible (GitHub) |
| https://github.com/simonw/showboat | Simon's manual-testing artifact tool | likely accessible (GitHub) |
| https://github.com/simonw/tools | The "knowledge hoarding" example repo | likely accessible (GitHub) |
| https://psychsafety.com/normalisation-of-deviance/ | Source for the Vaughan / Challenger frame Simon applies | unknown |
| https://arxiv.org/abs/2406.06608 | "The Prompt Report" academic survey | likely accessible |
| https://arxiv.org/abs/2503.18813 | DeepMind CaMeL paper | likely accessible |

---

## Suggested fetch order (highest to lowest leverage)

If the user can fetch and re-feed URLs in order, this prioritization maximizes the gains:

### Tier 1 (highest leverage — would change architecture decisions)

1. **https://factory.strongdm.ai/principles** — the canonical wording of the cardinal rules; current report reconstructs from secondary quotes
2. **https://factory.strongdm.ai/techniques** + the seven sub-pages — the technique definitions are quoted in many places; direct text would tighten Architecture 1 and Architecture 4
3. **https://every.to/guides/compound-engineering** — the canonical compound-engineering thesis; current report reconstructed from plugin docs
4. **https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents** — the narrative origin story
5. **https://simonwillison.net/2026/Feb/7/software-factory/** — Simon's reportage of StrongDM; the most-cited outsider analysis
6. **https://simonwillison.net/guides/agentic-engineering-patterns/** (and all chapter sub-pages) — Simon's pattern catalog; currently reconstructed
7. **https://el-kaim.com/the-dark-factory-...** — the dark-factory article itself

### Tier 2 (would add useful color but not change architectures)

8. https://news.ycombinator.com/item?id=46924426 — the HN thread (specific comment quotes are reconstructed; verbatim wording would tighten attribution)
9. https://www.lennysnewsletter.com/p/an-ai-state-of-the-union — Lenny's interview with Simon
10. https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens — Boris Cherny's "10–30 PRs/day" interview; the strongest scaling data point

### Tier 3 (recommended additional sources; would extend research, not patch reconstructions)

11. https://www.danshapiro.com/blog/2026/01/the-five-levels... — the maturity model that anchors the dark-factory framing
12. https://2389.ai/posts/the-dark-factory-is-a-dot-file/ — the orchestration-graph deep dive
13. https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ — governance/liability angle, currently uncovered
14. https://simonwillison.net/2025/Dec/10/normalization-of-deviance/ — referenced by HN/Lenny report
15. https://www.thepragmaticcto.com/p/the-software-factory-when-no-human — surfaces the `return true` reward-hacking story

---

## How to feed content back

When fetching externally, the most useful format for re-feeding is:

```
URL: <full URL>
Title: <page title>

<full body text, markdown if available; otherwise HTML stripped to plain text>
```

If feeding multiple URLs in one batch, separate them with `---` on its own line. The lead designer can then re-run targeted research subagents over the fetched content with instructions like "update `research/01-strongdm-factory.md` with verbatim quotes from these pages, marking which previously-paraphrased claims now have direct attribution."

---

## What the architectures depend on (so you can prioritize)

If certain architectures matter more, the URL fetch priorities shift:

- **Architecture 1 (Specification Refinery)** — Tier 1 items 1, 2, 6 are most relevant.
- **Architecture 2 (Compound Atelier)** — Tier 1 items 3, 4 are most relevant; the plugin docs already give 90% of what's needed.
- **Architecture 3 (Phase-Gated Foundry)** — None of the blocked URLs are critical; this architecture draws primarily from pre-agile methodology literature (waterfall, V-model, RUP, Cleanroom) which was not blocked.
- **Architecture 4 (Evolutionary Tournament)** — Tier 1 items 1, 2, 7 most relevant; especially the dark-factory discussion of selection-pressure-style validation.
