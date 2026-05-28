# Handoff — v3 build guide continuation

This document captures where the v3 build-guide work stands, what's been done, what's next, and the context you (the reader, or the next agent) need to continue without rebuilding it from scratch. Written following the [`human-scoped-deliverables`](../../.claude/skills/human-scoped-deliverables/SKILL.md) conventions: plain language, tables for comparison, no hash-IDs in body, honest acknowledgements.

## TL;DR

You're producing a human-readable build guide for the v3 synthesis output. **Items 1-4 are landed in PR #202** ([build guide foundation](README.md): vocabulary, paradigm, substrate, candidates side-by-side). **The `human-scoped-deliverables` skill is in PR #203** (reader profile and format conventions for any future agent producing human-facing material). **Items 5-6 — per-candidate methodology Mermaid diagrams — are next** but have not been started. The user wants to sign off on the framework in PR #202 before items 5-6 are produced, so producing 30 diagrams that share a wrong framework doesn't waste effort.

## Current state

| Artifact | PR | Status | What's in it |
|---|---|---|---|
| Phase 8 autonomous run | #194-#201 | **MERGED** | 10 lean-eval briefs, 3 bias-guard audits, cross-candidate evaluator-brief, Phase-8-close handoff, run summary, retrospective. Closed the v3 synthesis pipeline. |
| Build-guide items 1-4 | **#202** | **OPEN — awaiting user review** | Plain-English foundation: vocabulary translation, Five Levels paradigm, OSS substrate landscape, 10-candidate side-by-side. |
| `human-scoped-deliverables` skill | **#203** | **OPEN — awaiting user review** | Reader profile + format conventions for human-facing material. Triggers on "summary", "overview", "primer", "in plain language", "comparison", "help me understand", etc. |
| Build-guide items 5-6 | not started | pending | Per-candidate methodology + discipline + substrate Mermaid diagrams (30 total). |
| Recommendation memo ("what to actually ship") | not started | pending | Separate artifact, not part of the build guide. Speculative; needs the lean-evals to actually run before any concrete recommendation is grounded. |

## Background — what this whole thing is about

The repo at `lago-morph/software-factory` ran a multi-phase synthesis pipeline that produced 10 candidate methodologies for building software with AI agents. The output is structurally normalized for an AI agent re-entering cold — dense, cross-referenced, jargon-heavy. The user (jonathan@manton.com) is a 35+ year software/hardware engineer who explicitly called the pipeline output "like reading directly from individual tables in a SQL database — not possible for a human to work that way," and that working through it "made me feel like an inadequate moron."

The build guide is the BI-tool / report layer that the SQL underlay needs to be usable. The user wants to **pick one or more of the 10 candidates and actually build it** — not as an academic exercise, but to use. Specifically, they want to understand what can be assembled from existing open-source (Kilroy, Fabro, Gas City, OpenHands, Overstory, CXDB, Beads, LiteLLM) vs. what would have to be custom-built.

The user is a Kubernetes / distributed systems expert. They've read most of the corpus material in `reference-only/` directly. They are explicitly **resource-aware** (cognitive load, attention, time, money, engineer hours, patience with AI agents are all real resources) and want **descriptive effort scoping** rather than quantitative time estimates (their phrasing: "What a 5-person team did in a month in 2023 a skilled engineer with AI tools now does in a day — days/weeks/dollars are very hard to use as comparison points in May 2026").

## How we figured out what to build

This was several rounds of negotiation. Worth surfacing the decisions because future agents (and the user revisiting this) shouldn't have to rebuild the framework from the conversation.

### Round 1: the user's initial critique

After Phase 8 closed, the user asked how to review the 10 candidate designs. I initially recommended reading the spec files directly. The user responded that the specs hadn't changed in two phases, the artifacts were impenetrable, jargon-laden, cross-referenced beyond usability, and that adversarial-reviewer findings "aren't incorporated into the spec" — they shape the design through silent edits but the *learning* is hidden in audit appendices.

### Round 2: what would actually help

I proposed five candidate artifacts (Phase-7 exec summary, Phase-8 exec summary, 10-candidate comparison sheet, recommendation memo, plus Phase-specific story narratives). The user picked the three most foundational: exec summaries + comparison sheet + recommendation memo. Then asked me to do the same diagnostic for Phase 8 before starting. I diagnosed Phase 8's specific readability problems (falsifiers are practitioner-impenetrable, DEC-1.a pattern reads like math, comparison axes don't actually compare).

### Round 3: stopped me mid-flight; clarified what was actually wanted

I started writing the Phase-7 summary file. User stopped me and clarified the real question: "How do I compare these proposals to the various things people have written about in blog posts over the past 12 months. I need to be able to form a mental model in my head for all of these alternatives." Visual thinker. Wants tables and diagrams. Mermaid is the preferred medium. ≤7-8 elements per diagram (Mermaid auto-layout fails at scale).

I asked back: which external sources, which diagram types, what depth. The user clarified:

- **External sources**: don't ask by author name; "that forces me to memorize every author, name, and distinct (and often contradictory) term." Lead with the idea; attach the source name as a footnote.
- **Diagram types**: methodology diagrams. Separated explicitly into discipline / methodology / substrate (three distinct things that should be understood independently, then their relationships derived).
- **Human involvement**: needs to be an explicit axis. StrongDM's attractor pattern (set it running, it converges like a control system) is the reference for what the user finds most compelling about the work.
- **Shipping perspective**: what can be built from existing OSS (Kilroy, Fabro, Gas City, OpenHands, Overstory, the 2389 ecosystem). User is K8s expert; can build substrate with AI agent help but doesn't want to build what doesn't need building.
- **Pressure-testing**: zero chance any candidate works first time. Wants to swap methodologies on top of shared substrate. Solution-specific construction is bad.
- **Terminology**: plain, descriptive, boring. No "polecats" (a Gas City term). All 10 candidates use the same term for the same thing.

### Round 4: research before producing

User pointed me at the 5 OSS project URLs (Kilroy, Fabro, Gas City, OpenHands, Overstory) and told me to look in `reference-only/` for the StrongDM material I was about to bullshit about. I read the El Kaim "Dark Factory" synthesis, the Shapiro Five Levels piece, the StrongDM Factory pages, and the OSS project READMEs. This dramatically reframed what to produce:

- The corpus already has the vocabulary (Dark Factory, Five Levels, Three-Layer Architecture, Attractor, scenarios-as-holdout-sets, satisfaction, DTU, Healer / self-healing loop, Gene Transfusion, Pyramid Summaries, Dorodango, etc.) — the v3 pipeline invented parallel jargon for things that already have names.
- The three-layer architecture (LLM client + agent loop + pipeline engine) is the convergent shape every Attractor implementation lands on.
- El Kaim's 12 principles are the established discipline checklist.
- The substrate is mostly already solved — 5+ OSS projects in the pipeline-engine slot, 2-3 in the agent-runtime slot, CXDB for observability, Beads for work ledger, LiteLLM for model routing.

### Round 5: framework first, diagrams later

User accepted my refined recommendation: produce items 1-4 (the framework, anchored to corpus vocabulary) first; sign off; then produce items 5-6 (the per-candidate diagrams). Specifically:
- **NO** DOT-graph-style diagrams per candidate ("too detailed; I want to get a sense for things").
- Output at `architectures/v3/build-guide/`.
- Items 1-4 first, then 5-6.

Items 1-4 are now landed in PR #202.

### Round 6: reader profile → skill

User asked for a profile of themselves as a reader, to use as a shortcut with future agents. I produced one as a chat message. User accepted with two corrections:
1. **"Cost-aware" → "resource-aware"** — broader framing. Cognitive load, time, money, attention, engineer hours, patience with AI agents are all resources.
2. **Drop quantitative time estimates** — in May 2026, "engineer-weeks" and "dollar costs" date instantly. Use descriptive effort scoping ("configure existing OSS" / "small custom harness" / "major engineering build").

Then asked me to build it as a skill instead of a one-time chat artifact. Skill is in PR #203. Triggers on "summary", "overview", "primer", "in plain language", "comparison", etc.

### Now

User is concerned about context window and wants this handoff so the work can continue cleanly in a new session.

## What items 5-6 actually are (the concrete next step)

The recommended path forward, pending user sign-off on the framework in PR #202:

**Item 5: per-candidate methodology diagrams** — 10 small Mermaid diagrams (one per candidate). Each ≤7 elements. Each shows the candidate's methodology loop / cycle at a conceptual level — actors (human, agent, judge), arrows (flow), gates (decisions). Not the DOT graph; the *shape*. Examples of what each might look like:

- **GF-M (two-regime greenfield)**: a Regime-A box (intent → paraphrase → probe → promote-or-reverse) with an arrow to a Regime-B box (Compound-Engineering loop with cross-model review panel). 5-6 elements.
- **BF-L (legacy-ingestion brownfield)**: three loops over a central Codebase Model box — Ingestion / Work / Maintenance. 4-5 elements.
- **D7-U-1 (Falsification-Topology unified)**: artifact creation → FC declaration → opposing-side refutation → survival verdict → compounding gate. 5 elements.

**Item 6: per-candidate discipline binding tables + substrate composition** — each candidate gets, alongside its methodology diagram:
- A small table of which of the 12 principles it binds (the matrix is in [`02-paradigm.md`](02-paradigm.md), already done at the cross-candidate level; per-candidate breakouts add the *why* and *how* for that candidate specifically).
- A small Mermaid diagram showing the substrate composition (which OSS in each slot — pipeline engine, agent runtime, event store, work ledger, LLM client, plus the candidate-specific custom piece). ≤6-7 elements.

**Total**: ~20 diagrams + 10 short discipline tables. Plus a per-candidate prose paragraph (~150 words each) explaining what the candidate is *like* to use — when you'd reach for it, what it costs in the relevant resources, what it's betting on.

**Where**: append to [`04-candidates.md`](04-candidates.md), or create new files `05-methodology-diagrams.md` and `06-substrate-and-discipline-diagrams.md`. The skill says one document per concern is fine; if items 5-6 are tightly paired (one diagram of each per candidate), one combined file might read better. **This is a layout decision the user can override** when items 5-6 are produced.

## Open decisions

| Decision | Status | Lead-agent recommendation |
|---|---|---|
| Sign off on framework in PR #202 (vocabulary, paradigm, substrate, candidates) before items 5-6 fire? | **Pending user review** | Yes — produce items 5-6 only after the framework is signed off. Re-doing 30 diagrams that share a wrong framework is expensive. |
| Layout for items 5-6: one combined file or two separate ones? | **Pending** | One combined file (`05-per-candidate-diagrams.md`) with each candidate's three diagrams (methodology / discipline / substrate) grouped together. Easier to read per-candidate than to flip between files. |
| Vocabulary picks in `01-vocabulary.md` (e.g., "Attractor" over "compound engineering pipeline" as the umbrella term) | **Pending user review** | Accept as-is. Alternatives are in the glossary. |
| The recommendation memo ("what would I actually ship?") | **Not started; not part of items 5-6** | Recommend deferring until the lean-evals actually run. Pre-execution recommendation is speculation; post-execution recommendation has evidence. Honest separation. |
| Adopt the deferred Phase-7 retro AGENTS-MD rules into canonical AGENTS.md? | **Deferred during Phase 8 run, never revisited** | Lower-priority; can sit until the build-guide work closes. |

## User's preferences (also in the skill, but worth restating)

The `human-scoped-deliverables` skill captures these in full. Headline summary for the next agent picking up cold:

- **Visual thinker.** Tables for comparison; Mermaid diagrams ≤7 elements each.
- **Plain corpus vocabulary.** No invented terms in parallel to the corpus the reader has already read.
- **No hash IDs in body.** AGENTS-MD-xxx and similar are AI-navigation artifacts, not for humans.
- **No "per §X.Y of file Z" cross-references.** Quote the relevant sentence inline.
- **Resource-aware.** Cognitive load, attention, time, money, engineer hours are all resources.
- **Descriptive effort scoping.** No quantitative day/week/month estimates — use "configure existing OSS" / "small custom harness" / "major engineering build."
- **Sample-first when scaling.** Produce one representative piece, get sign-off, then scale.
- **Honest disclosure.** What's known, what's speculative, what's audit-trail. Lead-agent opinion clearly marked when present.

## How to resume

After context reset, paste this into a new session:

```
I am resuming work on the v3 build guide. Context:

- I'm jonathan@manton.com, the human reader. The human-scoped-deliverables
  skill captures my reader profile; it should auto-load if you've made
  the right tool calls.

- The v3 synthesis pipeline closed in Phase 8 (PRs #194-#201, merged).

- I've reviewed PR #202 (build-guide items 1-4: vocabulary, paradigm,
  substrate, candidates) and PR #203 (the human-scoped-deliverables
  skill).

- The next step is items 5-6: per-candidate methodology Mermaid diagrams
  + discipline binding tables + substrate composition diagrams. ~30 small
  diagrams (≤7 elements each), 10 candidates × 3 layers.

- Full handoff context is at architectures/v3/build-guide/HANDOFF.md.

Please read:
1. architectures/v3/build-guide/HANDOFF.md (full context)
2. architectures/v3/build-guide/README.md
3. architectures/v3/build-guide/04-candidates.md
4. .claude/skills/human-scoped-deliverables/SKILL.md

Then ask me [whether PRs #202 and #203 are merged, what my decision is
on items 5-6 layout, anything else from the "Open decisions" table in
the handoff doc that needs answering].

Do NOT produce items 5-6 until I tell you to start. Sample-first
discipline — show me one candidate's three diagrams as a representative
before producing the other 9.
```

## Files referenced in this handoff

For the next agent: these are the load-bearing inputs.

| File | What it contains |
|---|---|
| [`README.md`](README.md) | Build-guide entry point; reading order. |
| [`01-vocabulary.md`](01-vocabulary.md) | Corpus terms used in the guide + translation table from v3-pipeline jargon to corpus names. |
| [`02-paradigm.md`](02-paradigm.md) | Five Levels axis (Mermaid diagram) + 12 principles + per-candidate principle-binding matrix. |
| [`03-substrate.md`](03-substrate.md) | Three-layer architecture (Mermaid) + slot-by-slot OSS map + per-candidate "what's actually new" table. |
| [`04-candidates.md`](04-candidates.md) | At-a-glance table + per-candidate cards with distinctive bet, methodology shape, substrate composition, what could kill it, practitioner verdict. |
| `.claude/skills/human-scoped-deliverables/SKILL.md` | Reader profile and format conventions as a skill. Triggers on "summary", "overview", "primer", "comparison", etc. |

## Honest acknowledgements

- **Items 5-6 are scoped but not started.** The 30-diagram estimate is rough; some candidates may need 2 diagrams (methodology + substrate), others may need 4 (if a discipline diagram is genuinely separate). Adjust at production time.
- **The framework in PR #202 has not been user-reviewed yet.** If the vocabulary picks or the paradigm framing are wrong, items 5-6 inherit the wrong framework. Sign-off before producing is the safe path.
- **The recommendation memo is intentionally deferred.** Pre-execution recommendation is speculation. Post-execution recommendation has evidence. Don't conflate them.
- **PR #202 and #203 stack relationship.** PR #203 (skill) is on its own branch off main; doesn't depend on #202. PR #202 (build guide) is on its own branch off main; doesn't depend on #203. This handoff doc is in a third branch stacked off #202's branch. Three independent landing decisions.
- **Context-window concern is the user's stated reason for the handoff.** The next agent should treat this as a fresh start: read the handoff + the 4 build-guide files + the skill, ask clarifying questions, then proceed. Don't try to reconstruct the conversation history from scratch.
