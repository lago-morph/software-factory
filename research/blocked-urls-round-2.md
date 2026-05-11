# Blocked URLs — Round 2 (Jaymin / Overstory / OpenHands)

**Date:** 2026-05-10 (initial); fetch-action results merged 2026-05-11; issue #8 results processed 2026-05-11.
**Purpose:** URLs the Round-2 subagents will probably need that are NOT reachable from the current sandbox.

**Status as of 2026-05-11:** Issue [#4](https://github.com/lago-morph/software-factory/issues/4) ran the first fetch — 13 of 14 URLs returned HTTP 200; content was incorporated into reports and the cache files have since been deleted. Issue [#8](https://github.com/lago-morph/software-factory/issues/8) (Wayback supplements) has now landed: the Substack manifesto and the arXiv HTML render are now ACCESSED and incorporated into reports 09 and 11; the Boris Cherny Lenny interview is PARTIAL (paywall persists in Wayback) and is reflected in report 06; the el-kaim article was never archived in Wayback (still BLOCKED). Cache files have been deleted after incorporation. A third retrieval pass (manual browser-cookie fetches dropped into `research/manual/` on 2026-05-11) confirmed the Cherny and Willison-Lenny paywalls hold even with cookies (need a *paid* subscription) and that the el-kaim Cloudflare challenge cannot be bypassed by cookies (need Path B from `research/unfetched-sources.md`). See `research/blocked-urls.md` for the cross-round canonical inventory. The §3 inventory below has been updated with per-URL final status.

The sandbox blocks essentially every host except `raw.githubusercontent.com` (and partial GitHub-API access via the MCP). The list below is the result of that probe.

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

| # | URL | Fetch status |
|---|---|---|
| 1 | https://www.jayminwest.com/agentic-engineering-book | ✅ via #4 (188 KB; rendered TOC matches raw markdown) |
| 2 | https://www.jayminwest.com/agentic-engineering-book/6-harnesses | ✅ via #4 (113 KB; consumed by `research/09-jaymin-harnesses-partial.md`) |
| 3 | https://jayminwest.substack.com/p/a-manifesto-for-agentic-development | ✅ via #8 Wayback (capture 2026-05-11 00:25:03; full manifesto body recovered; consumed by `research/09-jaymin-harnesses-partial.md` §12) |
| 4 | https://docs.all-hands.dev/usage/how-to/headless-mode | ✅ via #4 (400 KB; consumed by `research/11-openhands-substrate-audit.md`) |
| 5 | https://docs.all-hands.dev/ | ✅ via #4 (353 KB; doc-tree fingerprint) |
| 6 | https://arxiv.org/abs/2511.03690 | ✅ via #4 (abstract + metadata) |
| 7 | https://arxiv.org/pdf/2511.03690 | ✅ HTML render `arxiv.org/html/2511.03690v2` fetched via #8 Wayback (capture 2026-05-11 00:25:03; full paper body, 761 lines markdown; consumed by `research/11-openhands-substrate-audit.md` v0.2) |
| 8 | https://github.com/marketplace/actions/openhands-ai-action | ✅ via #4 (222 KB; third-party `xinbenlv/openhands-action`, 10 stars) |

## Tier 2 (would add useful color)

| # | URL | Fetch status |
|---|---|---|
| 9 | https://www.youtube.com/watch?v=K7nY3MUzDuk — *The Agentic Engineering Meta* | Not attempted (YouTube transcripts require a transcript-extraction service). Defer. |
| 10 | https://www.youtube.com/watch?v=njRAmppPvFk — *Six Levels of Agentic Engineering* | Same as above. Worth fetching the transcript via a transcript service in a future round — the "six levels" framing complements Dan Shapiro's "five levels." |
| 11 | https://www.youtube.com/watch?v=95TEFWdo6Mw — *I'm Open Sourcing The Cutting Edge* | Same as above. |
| 12 | https://skillsllm.com/skill/overstory | Not yet attempted; low priority. |
| 13 | https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes | ✅ via #4 (2.1 MB; consumed by report 11) |
| 14 | https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering | ✅ via #4 (167 KB; Cisco pilot study, consumed by report 12 §2.2) |
| 15 | https://www.mindstudio.ai/blog/what-is-agentic-engineering | Not yet attempted; report 12 already has enough definitional cross-checks. Skip. |
| 16 | https://www.ibm.com/think/topics/agentic-engineering | ✅ via #4 (253 KB; consumed by report 12 §2.4) |
| 17 | https://addyosmani.com/blog/agentic-engineering/ | ✅ via #4 (182 KB; consumed by report 12 §2.1 — strongest Tier-2 piece) |
| 18 | https://agenticengineer.com/tactical-agentic-coding | Not yet attempted. Add to next fetch issue if appetite remains. |
| 19 | https://kiro.dev/ | ✅ via #4 (232 KB; consumed by report 12 §2.5 — surfaces a new substrate candidate) |
| 20 | https://cloud.google.com/discover/what-is-agentic-coding | ✅ via #4 (2.2 MB; consumed by report 12 §2.3 — governance checklist) |

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
