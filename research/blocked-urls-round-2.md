# Blocked URLs — Round 2 (Jaymin / Overstory / OpenHands)

**Date:** 2026-05-10
**Purpose:** URLs the Round-2 subagents will probably need that are NOT reachable from the current sandbox. Feed these into the GitHub Action defined in `.github/workflows/fetch-blocked-urls.yml` by opening an issue titled `[fetch-urls] round-2 initial pull`. See `research/PLAN.md` §5–6 for the workflow.

The sandbox tested 2026-05-10 blocks essentially every host except `raw.githubusercontent.com` (and partial GitHub-API access via the MCP). The list below is the result of that probe.

---

## What is fetchable from the sandbox (no action needed)

| Host | Examples |
|---|---|
| `raw.githubusercontent.com` | `raw.githubusercontent.com/jayminwest/agentic-engineering-book/main/README.md`, `…/overstory/main/README.md`, `…/All-Hands-AI/OpenHands/main/README.md` |
| `api.github.com` | repo metadata via WebFetch |
| GitHub MCP tools (`mcp__github__get_file_contents`, etc.) | Any file in the `lago-morph/software-factory` repo (note: MCP is **restricted to this repo only** — it cannot read `jayminwest/*` or `All-Hands-AI/*`. Subagents must use raw.githubusercontent.com URLs.) |

**Practical implication:** Subagents 08, 09, 10, 11, 12 can do the *majority* of their work via raw.githubusercontent.com without needing the fetch action. The action is needed for the items below.

---

## Tier 1 (highest leverage — subagents should not be considered complete without these)

These are the canonical-source documents for the three sources, in forms the repo files don't contain.

1. **https://www.jayminwest.com/agentic-engineering-book** — the rendered book index (the website rebuilds daily from the repo, but the rendering may include navigation / cross-references that aren't in the raw markdown)
2. **https://www.jayminwest.com/agentic-engineering-book/6-harnesses** — Chapter 6 rendered (linked in search results; useful to confirm the rendered version matches the markdown)
3. **https://jayminwest.substack.com/p/a-manifesto-for-agentic-development** — Jaymin's published manifesto, **not in the repo**. This is the most likely source of doctrinal claims that don't appear in the book itself.
4. **https://docs.all-hands.dev/usage/how-to/headless-mode** — OpenHands headless mode docs. The repo README does not describe headless mode in any detail; the docs site is the primary source.
5. **https://docs.all-hands.dev/** (entire `usage/` and `architecture/` sub-trees) — OpenHands operating manual.
6. **https://arxiv.org/abs/2511.03690** — *The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents*. The published academic description of the SDK. Likely contains explicit comparisons against other agent runtimes and the rationale for the workspace abstraction.
7. **https://arxiv.org/pdf/2511.03690** — full PDF.
8. **https://github.com/marketplace/actions/openhands-ai-action** — the Marketplace listing for the OpenHands GitHub Action. The repo's `action.yml` will tell us the input/output contract, but the marketplace page describes intended usage.

## Tier 2 (would add useful color)

9. **https://www.youtube.com/watch?v=K7nY3MUzDuk** — "The Agentic Engineering Meta" (Jaymin). YouTube transcript URL form: `https://youtubetranscript.com/?server_vid2=K7nY3MUzDuk` is sometimes reachable.
10. **https://www.youtube.com/watch?v=njRAmppPvFk** — "Six Levels of Agentic Engineering" (Jaymin). The "six levels" framing appears to be Jaymin's analog of Dan Shapiro's "five levels" already cited in Round 1. Worth a comparison.
11. **https://www.youtube.com/watch?v=95TEFWdo6Mw** — "I'm Open Sourcing The Cutting Edge of Agentic Engineering" (Jaymin's announcement of the book).
12. **https://skillsllm.com/skill/overstory** — third-party description of Overstory (low priority).
13. **https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes** — third-party wiki page about CLI/deployment modes; could substitute partially for the docs site if it's blocked.
14. **https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering** — outside-perspective piece referencing several of our sources; would help cross-check our vocabulary.
15. **https://www.mindstudio.ai/blog/what-is-agentic-engineering** — basic explainer; useful for confirming terminology is industry-standard not idiosyncratic.
16. **https://www.ibm.com/think/topics/agentic-engineering** — IBM's framing of agentic engineering; useful for enterprise framing if we ever pursue Architecture 3 (Foundry).
17. **https://addyosmani.com/blog/agentic-engineering/** — Addy Osmani's take, often a strong distillation.
18. **https://agenticengineer.com/tactical-agentic-coding** — additional perspective.
19. **https://kiro.dev/** — Kiro IDE (claims to "bring engineering rigor to agentic development"); see whether it overlaps OpenHands.
20. **https://cloud.google.com/discover/what-is-agentic-coding** — Google's framing.

## Tier 3 (companion / referenced material we'd want for full provenance)

21. **https://link.springer.com/book/10.1007/979-8-8688-2361-9** — *Agentic AI for Engineers: Architecting Goal-Driven Systems* (Springer book). Tangentially related; likely paywalled.
22. **https://www.oreilly.com/library/view/building-agentic-ai/9781803238753/** — *Building Agentic AI Systems* (O'Reilly). Likely paywalled.
23. **https://agenticse-book.github.io/pdf/AgenticSE_Book.pdf** — *Agentic Software Engineering: Building Trustworthy Software* (open-access academic PDF). Possibly relevant to Architecture 3 (Foundry) since "trustworthy" implies V&V rigor.

---

## Specific paths inside accessible repos (no fetch needed; listed here so the subagents know what to ask for)

These should be fetched by the subagents themselves via raw.githubusercontent.com — but listing them so the next agent doesn't have to re-derive the URLs.

### jayminwest/agentic-engineering-book (branch `main`)

Base URL: `https://raw.githubusercontent.com/jayminwest/agentic-engineering-book/main/`

- `README.md`
- `TABLE_OF_CONTENTS.md`
- `chapters/1-foundations/_index.md`, `chapters/1-foundations/1-twelve-leverage-points.md`
- `chapters/2-prompt/_index.md`, `1-prompt-types.md`, `2-structuring.md`, `3-language.md`
- `chapters/3-model/_index.md`, `1-model-selection.md`, `2-model-behavior.md`, `3-model-limitations.md`, `4-multi-model-architectures.md`, `5-model-evaluation.md`
- `chapters/4-context/_index.md`, `1-context-fundamentals.md`, `2-context-strategies.md`, `3-context-patterns.md`, `4-multi-agent-context.md`, `5-context-management-architectures.md`, `6-context-at-codebase-scale.md`
- `chapters/5-tool-use/_index.md`, `1-tool-design.md`, `2-tool-selection.md`, `3-tool-restrictions.md`, `4-scaling-tools.md`, `5-skills-and-meta-tools.md`
- `chapters/6-harnesses/_index.md`, `1-what-is-a-harness.md`, `2-harness-stack.md`, `3-harness-categories.md`, `4-harness-as-control-system.md`, `5-harness-engineering.md`, `6-security-permissions-trust.md`, `7-designing-for-your-context.md`
- `chapters/7-patterns/_index.md`, `1-plan-build-review.md`, `2-self-improving-experts.md`, `3-orchestrator-pattern.md`, `4-autonomous-loops.md`, `5-react-pattern.md`, `6-human-in-the-loop.md`, `7-progressive-disclosure.md`, `8-expert-swarm-pattern.md`, `9-multi-agent-collaboration.md`, `10-multi-agent-landscape.md`, `11-production-multi-agent-systems.md`
- `chapters/8-practices/_index.md`, `1-debugging-agents.md`, `2-evaluation.md`, `3-cost-and-latency.md`, `4-production-concerns.md`, `5-workflow-coordination.md`, `6-knowledge-evolution.md`, `7-operating-agent-swarms.md`
- `chapters/9-mental-models/_index.md`, `1-pit-of-success.md`, `2-prompt-maturity-model.md`, `3-specs-as-source-code.md`, `4-context-as-code.md`, `5-execution-topologies.md`, `6-design-as-bottleneck.md`, `7-software-factories.md`
- `chapters/10-practitioner-toolkit/_index.md`, `1-claude-code.md`, `2-google-adk.md`, `3-ide-integrations.md`, `4-agent-frameworks.md`, `5-multi-agent-workspace-managers.md`, `6-enterprise-context-tools.md`
- `appendices/examples/gastown/` (directory — list via API to enumerate)
- `appendices/examples/kotadb/`
- `appendices/examples/overstory/`
- `appendices/examples/pi-mono/`

### jayminwest/overstory (branch `main`)

Base URL: `https://raw.githubusercontent.com/jayminwest/overstory/main/`

- `README.md`, `STEELMAN.md`, `CLAUDE.md`, `SECURITY.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODEOWNERS`, `LICENSE`
- `package.json`, `bunfig.toml`, `tsconfig.json`, `biome.json`
- `docs/` — directory; enumerate via API
- `agents/` — directory
- `src/` — directory (the meat — coordinator, mail, worktree, merge queue, runtime adapters)
- `templates/`, `scripts/`
- `.github/workflows/` — enumerate
- `.overstory/`, `.canopy/`, `.claude/`, `.pi/`, `.sapling/`, `.mulch/`, `.seeds/` — config dirs

### All-Hands-AI/OpenHands (branch `main`)

Base URL: `https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/`

- `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `LICENSE`, `config.template.toml`
- `openhands/` — core package; enumerate the entry points and the workspace abstractions
- `skills/` — read a representative sample
- `containers/`, `docker-compose.yml`, `Makefile`
- `.github/workflows/` — enumerate
- `.openhands/`, `.agents/`
- `pyproject.toml`, `uv.lock`, `poetry.lock`

### Companion OpenHands repos

- `https://raw.githubusercontent.com/OpenHands/software-agent-sdk/main/README.md` and tree
- `https://raw.githubusercontent.com/OpenHands/OpenHands-CLI/main/README.md` and tree
- `https://raw.githubusercontent.com/OpenHands/openhands-github-action/main/action.yml` and `README.md`

---

## Fetch action issue template

When opening the `[fetch-urls]` issue, use this body (Tier 1 first):

```
[fetch-urls] round-2 initial pull

Tier 1:
https://www.jayminwest.com/agentic-engineering-book
https://jayminwest.substack.com/p/a-manifesto-for-agentic-development
https://docs.all-hands.dev/usage/how-to/headless-mode
https://arxiv.org/abs/2511.03690
https://arxiv.org/pdf/2511.03690
https://github.com/marketplace/actions/openhands-ai-action

Tier 2:
https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering
https://addyosmani.com/blog/agentic-engineering/
https://www.ibm.com/think/topics/agentic-engineering
https://kiro.dev/
https://cloud.google.com/discover/what-is-agentic-coding
https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes
```

Open Tier 2 in a second issue if Tier 1 runs into the 50-URL cap.

---

*End — `research/blocked-urls-round-2.md` v0.1*
