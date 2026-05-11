# Follow-up Research Threads

**Date:** 2026-05-10
**Purpose:** Catalog the worthwhile outbound threads surfaced by the v1/v2 research passes that were *not* chased then. Each thread below is a self-contained subagent brief that can be dispatched in parallel — no inter-thread dependencies.
**How to use:** Pick the threads that matter to you, spawn a subagent per thread with the brief verbatim, and let them run concurrently. Each brief lists its sources, extraction targets, and output path. Reports land in `research/followup/<NN-shortname>.md` so the main `research/` directory stays stable.

If a source returns 403 / Cloudflare in the sandbox, use the `fetch-blocked-urls` skill (`.claude/skills/fetch-blocked-urls/SKILL.md`) to file a GitHub issue (label: `fetch-urls`) that triggers the fetcher action. The action commits each URL's HTML + html2text markdown to a new `fetched/issue-<N>` branch you then merge into your working branch.

---

## Priority tiers

**Tier 1 — would change architecture decisions** (threads 1–4)
**Tier 2 — would refine or extend architectures** (threads 5–8)
**Tier 3 — grounding, governance, and remaining blocked sources** (threads 9–12)

Total: 12 threads. All independent and parallelizable.

---

## Thread 1: Dan Shapiro's "Five Levels" maturity model

**One-line:** The canonical 0→5 maturity model the rest of the corpus cross-references; would let the four architectures be positioned explicitly on the maturity scale.

**Why it matters:** El Kaim, Simon Willison, and StrongDM's own homepage all cite Shapiro's Five Levels as the framing for what level of AI adoption a team has reached. The comparison doc (`architectures/00-comparison.md`) currently describes architectures by trade-offs and contexts but does not place them on the Shapiro scale. Doing so would make hybrid recommendations more crisp (e.g., "Architecture 2 reliably operates at Level 3; pushing to Level 4 requires the additions in Architecture 4").

**Sources:**
- https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/

**Extraction targets:**
- Verbatim definitions of Levels 0–5 (or whatever the actual scale is — confirm count)
- Shapiro's named exemplars per level
- Capabilities and constraints implied at each level
- Where Shapiro positions his own work (Kilroy / DOT-graph orchestration)
- Any maturity-test heuristics ("you are at Level N if …")

**Output:** `research/followup/01-shapiro-five-levels.md` — 600–1200 words. Include a final section "Architecture mapping" placing each of our four architectures on the Shapiro scale with brief justification.

---

## Thread 2: Community Attractor implementations survey

**One-line:** 17+ implementations across 12 languages are claimed; surveying 4–5 distinctive ones tells us which design choices in Attractor reproduce vs. mutate.

**Why it matters:** The `architectures/04-evolutionary-tournament.md` "diversity policy" assumes pattern-level diversity is achievable across model families. Empirical confirmation that distinct independent teams converge on (or diverge from) the same Attractor pattern tells us how robust the pattern is. Amol Kabe's Python variant is particularly important because it introduces *named persona specialists* (Coding / Validator / Debugger / Planner), which is the design move Architecture 2 commits to but Architecture 1 doesn't.

**Sources (read READMEs and any AGENTS.md / docs, NOT source code):**
- https://github.com/danshapiro/kilroy (Go reimplementation by Shapiro)
- https://github.com/smartcomputer-ai/forge (Rust by Luke Buehler)
- https://github.com/joyrexus/software-factory (synthesis repo)
- The Amol Kabe Python "multi-agent Software Factory" repo (search GitHub for it; name is in `research/01-strongdm-factory.md`)
- One of: Fabro (Bryan Helmkamp, Rust), Arc (Point Labs, TypeScript)

**Extraction targets:**
- Which Attractor primitives each implementation kept (graph structure, node types, goal gates, supervisor loops, status.json)
- Which they dropped or replaced
- Which they ADDED that aren't in StrongDM's canonical spec
- Any named persona / role specialization
- Documented assumptions about model floor, provider alignment, sandbox

**Output:** `research/followup/02-attractor-implementations.md` — 1200–2000 words. Include a comparison table: row per implementation, columns for the major design primitives (graph, personas, gates, supervisor, fidelity modes, etc.).

---

## Thread 3: Boris Cherny "What happens after coding is solved"

**One-line:** Currently the strongest single scaling data point in the corpus ("10–30 PRs/day, 10–15 parallel sessions, no hand-edited code since November 2025") — known only via summary. Worth fetching the full interview.

**Why it matters:** Cherny is the head of Claude Code at Anthropic and operates further into the "Dark Factory" levels than anyone in our corpus except StrongDM. His specific claims (parallel-session count, no-hand-edit since a specific date, PR throughput) would calibrate the cost/throughput numbers in our four architectures. The comparison doc currently has a "human role" axis that's coarsely "supervises vs. schedules"; Cherny's lived experience would refine this.

**Sources:**
- https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens — Lenny Rachitsky interview with Boris Cherny, Feb 19 2026 (paywalled; may need Every-style fetch + manual extract)

**Extraction targets:**
- Cherny's exact workflow (how he distributes work across parallel sessions, what each session does, how he reviews)
- The "10–15 parallel sessions" claim verbatim with context (supervisor mode? scheduler mode?)
- The "10–30 PRs/day" claim verbatim — what counts as a PR, what's the merge gate
- The Cowork product build timeline ("10 days, small team, Claude Code")
- Cherny's stated quality/review discipline
- Any cost numbers
- His prediction or normative claims about where it goes next

**Output:** `research/followup/03-cherny-interview.md` — 1000–1500 words. Note paywall status; if only the editorial summary is accessible, say so and synthesize from what's there.

---

## Thread 4: Steve Yegge's Gas Town + Beads (orchestration deep-dive)

**One-line:** El Kaim's article names Gas Town as a sibling to Attractor; the SQLite-to-Dolt migration story in Beads is itself a multi-agent-infra case study.

**Why it matters:** Attractor and Gas Town are independent realizations of the same underlying pattern (graph-orchestrated agent pipelines). The diff between them tells us which design choices are pattern-level vs. team-level. The Beads migration story (the team hit SQLite write-concurrency limits and moved to Dolt — "Git for databases" — to handle multi-agent writes) is concrete evidence that "embarrassingly parallel" multi-agent workflows expose infrastructure assumptions in standard tooling.

**Sources:**
- https://2389.ai/posts/the-dark-factory-is-a-dot-file/ — the 2389 Research deep-dive on DOT-graph orchestration
- https://github.com/gastownhall/gastown — Steve Yegge's Gas Town orchestrator
- https://github.com/gastownhall/beads — Beads task-graph + the SQLite→Dolt migration story
- (Optional) https://www.dolthub.com/ — Dolt, if needed for context

**Extraction targets:**
- Gas Town's DOT-graph node types vs. Attractor's
- Gas Town's "knows when to pause for human input" criterion (Attractor uses `wait.human` hexagons; what does Gas Town use?)
- Beads's task-graph schema and how it differs from a flat `tasks.json` (Symphony) or markdown todo list
- The SQLite-to-Dolt migration: what specifically broke, what the new architecture buys, what the migration cost
- Any explicit comparison to Attractor

**Output:** `research/followup/04-gastown-beads.md` — 1500–2500 words. Include a comparison table for Gas Town vs. Attractor (rows = primitives, columns = each tool).

---

## Thread 5: Klaassen's three sibling Every articles

**One-line:** Compound engineering has more depth than the single "Chain of Thought" article we have access to. Three sibling pieces add the "spec authorship as a meta-skill" angle and the Opus 4.5 model-floor argument.

**Why it matters:** The Atelier (Architecture 2) implementation roadmap (§11) is structured by mechanism adoption. The "Stop Coding and Start Planning" piece reportedly captures the *practice* of teaching the AI how you think — which is the implicit prerequisite for the whole compound-engineering loop. The "Teach Your AI to Think Like a Senior Engineer" piece likely details how the persona library is taught/curated. The Opus 4.5 piece would tell us whether the architecture relies on a specific model capability.

**Sources (all every.to; likely Cloudflare-gated — use the fetch-blocked-urls skill):**
- https://every.to/chain-of-thought/stop-coding-and-start-planning — Klaassen, Nov 6 2025
- https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer — likely same chain-of-thought subdomain
- https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5 — likely same subdomain

**Extraction targets:**
- "Spend an hour teaching AI how you think" — what does this concretely involve? What artifacts does it produce?
- Senior-engineer thinking — what's the persona / instruction shape that produces it?
- Opus 4.5 specific capabilities Klaassen relies on
- Any new compound-engineering primitives not in the main guide

**Output:** `research/followup/05-klaassen-siblings.md` — 1200–1800 words. If sources are paywalled, capture the visible portion and flag.

---

## Thread 6: Competitor factory landscape survey

**One-line:** Five named competitors (Devin, 8090, Factory/Droid, Superconductor, Jesse Vincent's Superpowers) — knowing what each is shipping helps situate our four architectures in the live market.

**Why it matters:** Our four architectures are designed against the StrongDM/Every.to/Simon/El Kaim sources. A landscape survey would tell us which architecture is *already a product*, which is unique, and which gaps in the field our architectures fill. Particularly: Factory's Droid and Devin claim to be full software factories; their actual marketing and docs would clarify what the field considers "in scope."

**Sources (homepage + docs only; no code):**
- https://devin.ai/ — Cognition's Devin
- https://8090.inc/ (or whatever the canonical 8090 URL is — search)
- https://www.factory.ai/ — Factory's Droid
- https://superconductor.io/ (or canonical URL — search)
- Jesse Vincent's "Superpowers" — find the canonical URL via Vincent's recent posts

**Extraction targets per competitor:**
- One-line product description
- Workflow primitives (do they use specs? scenarios? what's their judge?)
- Human role per their pitch
- Cost / pricing model
- Differentiator they claim
- Any methodology document or public spec

**Output:** `research/followup/06-competitor-landscape.md` — 1500–2500 words. Include a comparison table: row per competitor, columns for spec, scenarios, judge, human role, cost.

---

## Thread 7: Anthropic multi-agent research + Husain/Shankar evals FAQ

**One-line:** Simon endorses both as gold-standard primers; our four architectures' eval discipline (judges, satisfaction scoring, scenario testing) would be sharpened by reading them.

**Why it matters:** Architecture 4 (Tournament) uses fitness components and predator scenarios as the core mechanism. Architecture 1 (Refinery) uses an LLM judge separated from the implementer. Architecture 3 (Foundry) uses independent V&V. All four depend on eval quality. Anthropic's multi-agent research writeup is the canonical example of small-scale-first eval design; the Husain/Shankar FAQ is the practical primer.

**Sources:**
- Anthropic's "How we built our multi-agent research system" (mid-2025; find via anthropic.com/research or Anthropic's engineering blog)
- Hamel Husain and Shreya Shankar, "Frequently Asked Questions (And Answers) About AI Evals" (find via hamel.dev or Shankar's writing)

**Extraction targets:**
- The "start small, evolve" methodology for eval sets
- LLM-as-judge: when it works, when it doesn't
- Error analysis as a percentage of development time (Husain's 60–80% claim)
- "If you're passing 100% of your evals" heuristic — what does it mean and what do you do
- Anthropic's subagent-research-system specific architecture (subagents for context preservation; eval discipline; lessons learned)

**Output:** `research/followup/07-evals-deepdive.md` — 1500–2000 words. Include a final section "Implications for the four architectures" mapping evals practices to each architecture's judge / fitness / V&V structure.

---

## Thread 8: Security primitives (CaMeL + Safe YOLO + Lethal Trifecta)

**One-line:** Our four architectures all mention sandboxing and lethal-trifecta defense in passing; consolidating Willison + Anthropic + DeepMind material gives a coherent security primer.

**Why it matters:** F12 (lethal trifecta / prompt injection) is in every architecture's failure-mode coverage but is treated as "sandbox the implementer." That's necessary but not sufficient. CaMeL's capability-typed-program approach, Willison's Dual LLM pattern, and Anthropic's Safe YOLO container spec together give a layered defense model that any factory operating with real data should adopt. The comparison doc could add a row for "security posture" if this is fleshed out.

**Sources:**
- https://arxiv.org/abs/2503.18813 — Google DeepMind CaMeL paper
- https://simonwillison.net/2025/Apr/11/camel/ — Simon's explainer
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — Simon's framework
- Anthropic Claude Code "Safe YOLO" docs (find via docs.anthropic.com)
- (Optional) https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ — the Dual LLM pattern (April 2023 origin)

**Extraction targets:**
- Verbatim definitions of the lethal trifecta
- CaMeL's typed-capability program model — concrete enough to implement
- Dual LLM pattern's privileged-vs-quarantined LLM separation
- Anthropic's Safe YOLO container constraints (network, file access, secrets)
- Threat models the factory should defend against

**Output:** `research/followup/08-security-primitives.md` — 1500–2500 words. Include a "Security posture per architecture" section adding nuance to F12 coverage.

---

## Thread 9: Methodology ancestors (Kaner / Rumelt / Deming)

**One-line:** Three pre-LLM methodology ancestors that the architectures structurally inherit from; reading them adds historical grounding and surfaces design moves the original authors made that we may want.

**Why it matters:** Cem Kaner's *Scenario Testing* (2003) is the source StrongDM repurposes. Richard Rumelt's *Good Strategy Bad Strategy* is named in compound engineering's `ce-strategy` skill. Deming's PDCA cycle is structurally identical to compound engineering's Plan → Work → Review → Compound loop. These aren't optional reading; they're the design documents the modern methodologies inherit from. Sometimes the ancestor has design moves the descendant dropped.

**Sources:**
- Cem Kaner, "An Introduction to Scenario Testing" (2003 paper, kaner.com or testingeducation.org)
- Richard Rumelt, *Good Strategy Bad Strategy* — the diagnosis / guiding policy / coherent action framework (book; use a summary/review of the framework section if full text is unavailable)
- W. Edwards Deming, PDCA cycle (Plan-Do-Check-Act) — the Wikipedia entry plus one primary Deming source if available

**Extraction targets per source:**
- The original methodology in the author's own words
- Design moves the author made that modern descendants kept
- Design moves the author made that modern descendants dropped (and why)
- Any practical guidance not yet incorporated in our four architectures

**Output:** `research/followup/09-methodology-ancestors.md` — 1500–2000 words. Three sub-sections, one per ancestor.

---

## Thread 10: Governance / liability angle

**One-line:** Our four architectures address methodology and quality but say almost nothing about regulatory exposure, liability allocation, or audit-trail-for-counsel requirements.

**Why it matters:** Architecture 3 (Phase-Gated Foundry) is the most regulation-aware, but even it doesn't engage with current regulatory thinking. The Stanford CodeX piece, the BCG Platinion analysis, and the Pragmatic CTO piece together form a small but coherent governance literature that the comparison doc could synthesize into a "compliance posture" row.

**Sources:**
- https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ — Stanford CodeX
- BCG Platinion, "The Dark Software Factory" insight piece — find via bcg.com
- https://www.thepragmaticcto.com/p/the-software-factory-when-no-human — Pragmatic CTO

**Extraction targets:**
- Who is liable when an agent-written feature causes a regulatory incident? (Each source likely takes a position.)
- What evidence does counsel/insurance/regulator demand from a factory's audit trail?
- Specific failure modes named in the legal/governance literature (different from our 20 failure modes)
- How current frameworks (SOC 2, ISO 27001, GDPR Art. 22, EU AI Act) apply to agent-produced software
- Recommended controls

**Output:** `research/followup/10-governance.md` — 1500–2500 words. Include a "Compliance posture per architecture" comparison.

---

## Thread 11: Compound Knowledge plugin deep-dive

**One-line:** Tedesco's knowledge-work twin of compound engineering is documented less in our research than the engineering plugin; understanding it sharpens Architecture 2's knowledge layer.

**Why it matters:** The Compound Atelier architecture treats `docs/solutions/` as the canonical knowledge store. Tedesco's plugin operates the same pattern in *knowledge work* (not code), with two-track classification (insight / playbook / correction / pattern) and a separate `stale-knowledge-checker`. The knowledge-work variant exposes design moves that didn't have to make engineering compromises — and may be cleaner.

**Sources:**
- https://github.com/EveryInc/compound-knowledge-plugin — full docs (README, AGENTS.md, plugins/*/README.md, docs/skills/kw-*.md, agents/*.md)
- https://every.to/p/the-agent-that-saved-my-brain — already read in v2 but worth re-extracting with the plugin docs as context

**Extraction targets:**
- The kw-compound + kw-refresh pair (analog to ce-compound + ce-compound-refresh)
- Two-track classification (insight / playbook / correction / pattern) vs. the engineering plugin's bug / knowledge tracks
- `stale-knowledge-checker` — how it identifies staleness
- `strategic-alignment-reviewer` and `data-accuracy-reviewer` — what they catch
- The "no silent overwrites" stance — CK agents return text only; only orchestrating skills write files
- Confidence check primitive (kw:confidence)

**Output:** `research/followup/11-compound-knowledge.md` — 1500–2200 words.

---

## Thread 12: Dark Factory via archive.org (still blocked)

**One-line:** The El Kaim article remains Cloudflare-gated. Wayback Machine may have an archived copy.

**Why it matters:** Report 07 is the only report in the corpus that remains a reconstruction from secondary sources. The Wayback Machine's snapshot (if it exists) would let us verify quotes and possibly surface material the secondary sources don't quote.

**Sources:**
- https://web.archive.org/web/2026*/el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e — Wayback Machine search
- https://web.archive.org/web/2026*/welkaim.medium.com/* — Wayback Machine search of the author's profile
- If Wayback fails: try Google Cache (`cache:`), archive.is, or scribe.rip (Medium frontend mirror)

**Extraction targets:**
- The full article text, ideally verbatim
- All direct quotes the v2 report has flagged as "reconstructed"
- Any sections the secondary sources didn't cover
- Footnotes / linked references

**Output:** `research/followup/12-dark-factory-archive.md` — variable length. If recovery succeeds, also update `research/07-dark-factory.md` with verbatim quotes and a revision note. If recovery fails, document what was tried.

---

## Suggested dispatch order

For maximum value per token, run threads in roughly this order. Each can be a separate parallel subagent:

**First wave (highest leverage, parallel):**
- Thread 1 (Shapiro Five Levels) — small, fast, anchors the rest
- Thread 2 (Attractor implementations) — empirical, parallelizes per-repo
- Thread 3 (Cherny interview) — scaling data
- Thread 4 (Gas Town + Beads) — orchestration alternatives

**Second wave (refinements, parallel):**
- Thread 5 (Klaassen siblings)
- Thread 6 (Competitor landscape)
- Thread 7 (Evals deep-dive)
- Thread 8 (Security primitives)

**Third wave (grounding, parallel):**
- Thread 9 (Methodology ancestors)
- Thread 10 (Governance)
- Thread 11 (Compound Knowledge plugin)
- Thread 12 (Dark Factory archive recovery)

After each wave, consider re-synthesizing the deltas back into `research/00-synthesis.md` and the affected architecture specs.

---

## Notes for subagents

- Save reports to `research/followup/NN-<shortname>.md` per the brief.
- If a source returns 403 / Cloudflare / paywall: use the fetch-blocked-urls skill (file an issue with the URLs, title `[fetch-urls] …`, label `fetch-urls`). Do NOT fabricate quotes.
- If a brief asks for a comparison table, produce one — the synthesis pass relies on tables for cross-thread integration.
- Flag any new external references the source surfaces (potential Tier 4 threads for a future round).
- Mark unresolved questions; the comparison/synthesis pass will pick them up.
- Aim for the word-count target; don't pad.
