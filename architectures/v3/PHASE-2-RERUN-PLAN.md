# Phase-2 clean re-run plan (for next session)

**Purpose.** Takeover plan for the next session to execute Phase 2 of the v3 architecture synthesis. Pairs with [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md).

---

## 0. Operating rule

Follow this plan step by step. Don't do side work outside it. Stop and ask before each step in §3 that has an explicit "stop-and-ask" line. See [`AGENTS.md`](../../AGENTS.md) "Interactive operation."

---

## 1. Standing intent

Re-execute Phase 2 of the v3 architecture-synthesis plan: 9 parallel mandate-and-axis-specific tracks producing architecture sketches, against cleaned source files. A prior Phase-2 dispatch was contaminated; the contaminated artifacts and the contamination diagnosis are preserved as permalinks in [`history/HISTORICAL-RECORD.md`](history/HISTORICAL-RECORD.md) — do not read them into context.

Source-file cleanup and contaminated-artifact relocation were already completed earlier on this branch (the source files in `architectures/v3/` are clean as listed in §2). The next session starts directly at the dispatch step.

---

## 2. Pre-flight: where everything is

**Live tree state (post-cleanup):**

| Path | Status | Notes |
|---|---|---|
| [`00-brief-v3.md`](00-brief-v3.md) | clean | unchanged since Phase 0 |
| [`constraints-extracted.md`](constraints-extracted.md) | clean | UC1–UC8 |
| [`decisions-captured.md`](decisions-captured.md) | clean | D1–D7 (D5/D6/D7 sanitized) |
| [`contradictions.md`](contradictions.md) | clean | carries bias-guard-sharpening citation discipline note |
| [`failure-modes-v3.md`](failure-modes-v3.md) | clean | one prior contamination resolved in commit `3ba0085` |
| [`corpus-inventory.md`](corpus-inventory.md) | clean | post-Phase-1 bias-guard re-tags landed |
| `tracks/` | empty | populated by step 3.1 |
| [`bias-guards/phase-1/`](bias-guards/phase-1/) | clean | Phase-1 inputs |
| `bias-guards/phase-2/` | empty | populated by step 3.2 |
| [`history/HISTORICAL-RECORD.md`](history/HISTORICAL-RECORD.md) | preserved | permalinks to past contaminated artifacts; **do not read** |

**Open PR for Phase 2:** none currently. PR opens at step 3.3.

---

## 3. The 4 substantive steps

Each step has: **What** (concrete action), **Why (intent)** (the goal), **Expected outcome**. Steps with a **Stop-and-ask** line require explicit user go-ahead before executing.

### Step 3.1 — Re-dispatch all 9 Phase-2 tracks against the clean sources

**What.** Dispatch 9 Opus subagents in parallel (one Agent tool call per subagent, all in one assistant message). Each writes its output to `architectures/v3/tracks/<track-name>.md`. The dispatch prompts are embedded below.

**Why (intent).** Fresh subagents on clean source files produce uncontaminated Phase-2 outputs. The 6 mandate-specific tracks explore predetermined axes; the 3 unified-mandate tracks pick their own axis (per D1) and test whether a single architecture covering both mandates exists.

**Expected outcome.** 9 new track files in `tracks/`. Commits as each subagent reports back.

**Stop-and-ask:** before dispatching, surface the 9 prompts (below) and the dispatch plan; wait for user go-ahead before invoking the Agent tool.

#### Shared brief (applies to all 9 tracks)

Every dispatch prompt should include the following shared elements. The track-specific axis instructions follow.

```
You are Phase-2 subagent <TRACK-ID> in the v3 software-factory architecture
synthesis. Your job: produce ONE architecture-track output strong on a
specific framing axis. Eight other Phase-2 subagents are running concurrently
on different axes; the divergence is the design.

## Your axis

<TRACK-SPECIFIC AXIS INSTRUCTION — see per-track blocks below>

## Required reading (in this order)

v3 framing:
1. architectures/v3/00-brief-v3.md
2. architectures/v3/constraints-extracted.md
3. architectures/v3/decisions-captured.md (note D5/D6/D7 are bias-guard
   safeguards — read for context, do not cite their fictitious examples)

Phase-1 artifacts (your primary corpus inputs):
4. architectures/v3/contradictions.md (note the bias-guard-sharpening
   citation discipline at the top — cite underlying corpus, not WEAK-N IDs)
5. architectures/v3/failure-modes-v3.md
6. architectures/v3/corpus-inventory.md

Phase-1 bias-guard reports (context, NOT corpus references):
7. architectures/v3/bias-guards/phase-1/uncomfortable-contradictions-audit.md
8. architectures/v3/bias-guards/phase-1/missing-failure-modes-audit.md
9. architectures/v3/bias-guards/phase-1/miscategorization-audit.md

For greenfield tracks + any unified track touching greenfield, the cold-start
required reading per brief §5.1 is also required:
- research/25-requirements-engineering-foundations.md
- research/26-prompt-underspecification-academic.md
- research/30-cognitive-escrow.md
- research/31-caremark-rsi-board-exposure.md
- research/followup/10-governance.md

DO NOT read anything under architectures/v3/history/. Those files are
historical records of past contaminated artifacts; reading them risks
re-introducing bias.

## Output

Write to: architectures/v3/tracks/<TRACK-FILE>.md

Use standard 8-section structure with YAML frontmatter (track, axis,
mandate-scope, based-on-commit, based-on-date).

Sections:
  §0 Axis declaration and defense (pre-respond to Phase-3 adversarial)
  §1 Architecture sketch
  §2 How this addresses each load-bearing concern
     (lights-out / L5 tension per brief §2.1; UC4; cold-start if greenfield-
     adjacent; OQ-B1 through OQ-B10 to taste)
  §3 Citations and grounding (cite CTR-IDs, F-numbers, inventory anchors)
  §4 §4 defaults: accepted vs challenged (all 7 marked)
  §5 Cold-start (MANDATORY for greenfield + unified-touching-greenfield)
  §6 What this track is NOT trying to be
  §7 Open questions surfaced by this track

## Discipline

1. Strong on your axis, not comprehensive.
2. Cite the corpus — every load-bearing claim has at least one citation.
3. §4 defaults marked for all 7. Both accepted and challenged are valid.
4. Don't resolve cross-mandate questions (that's Phase 3).
5. Don't try to merge with other tracks.
6. Use brief glossary §0 vocabulary.
7. Anticipate Phase-3 adversarial passes; pre-respond in §0.

## Report back

5 sentences: chosen sub-axis, 2-3 load-bearing architectural choices,
§4 markings summary, single most-cited contradiction/F-mode, single biggest
open question surfaced.
```

#### Per-track axis instructions

**Track 1 — `greenfield-substrate-first`** (output: `tracks/greenfield-substrate-first.md`):

> Substrate is the primary organizing principle. Start from substrate primitives (sandbox, scenario storage, trajectory capture, cost ceilings, watchdog tiers, judge routing, coordination medium, guard mediator) and derive methodology as the minimum process needed to use them. The "how" is upstream of the "what". For greenfield specifically: what substrate makes the spec-malleable phase (UC4) work — what substrate primitives keep an evolving spec coherent across cycles, what catches the regressions that UC4 implies, what bootstraps from zero?

**Track 2 — `greenfield-methodology-first`** (output: `tracks/greenfield-methodology-first.md`):

> Methodology is the primary organizing principle. Start from the per-cycle process (work-unit shape, gate structure, knowledge accumulation, failure recovery) and derive substrate as what's required to support it. The "what" is upstream of the "how". For greenfield specifically: what cycle shape makes the spec-malleable phase productive instead of paralytic?

**Track 3 — `greenfield-cold-start-first`** (output: `tracks/greenfield-cold-start-first.md`):

> Cold-start is the primary organizing principle. Day 0 of a greenfield lights-out factory — no scenarios, no docs/solutions, no prior runs, no holdout suite — is the hardest moment. Build the architecture around getting through it; everything else is steady-state and downstream. Per brief §5, cold-start is the load-bearing greenfield risk.

**Track 4 — `brownfield-substrate-first`** (output: `tracks/brownfield-substrate-first.md`):

> Substrate is the primary organizing principle. Start from substrate primitives that ingest existing code, tests, telemetry, dependency graphs, issue history, deployment infrastructure as primary inputs. Brownfield's substrate must do work greenfield's doesn't: codebase indexing, dependency-graph maintenance, change-impact analysis, runtime instrumentation parsing. The "how" is upstream of the "what".

**Track 5 — `brownfield-methodology-first`** (output: `tracks/brownfield-methodology-first.md`):

> Methodology is the primary organizing principle. The per-cycle process for brownfield typically starts from an issue, a change request, or a codebase-evolution proposal and ends at a PR. Build the architecture around that cycle shape; substrate is whatever supports it.

**Track 6 — `brownfield-legacy-ingestion-first`** (output: `tracks/brownfield-legacy-ingestion-first.md`):

> Code-archaeology is the primary organizing principle. The architecture's first move on any new codebase is understanding what's there: structure, conventions, test patterns, hot paths, debt clusters, idioms, latent invariants. Everything else (cycle, substrate, gates) is downstream of ingestion quality.

**Track 7 — `unified-no-axis-A`** (output: `tracks/unified-A.md`):

> Find ONE architecture that addresses both greenfield and brownfield mandates. Pick your own organizing axis — mandate is NOT required to be primary. Defend the axis choice. Two other unified subagents (B, C) are running concurrently on the same instruction; they're expected to pick different axes; the divergence (or convergence) is the signal. You don't need to be comprehensive — you need to be strong on the unified case. If you conclude the unified case is impossible, say so explicitly with corpus grounding (this falsifies D1's premise; that's a load-bearing finding).

**Track 8 — `unified-no-axis-B`** (output: `tracks/unified-B.md`): same instruction as Track 7.

**Track 9 — `unified-no-axis-C`** (output: `tracks/unified-C.md`): same instruction as Track 7.

### Step 3.2 — Re-run the Phase-2 bias guards on the new tracks

**What.** After all 9 tracks return and are committed, dispatch 4 Phase-2 bias-guard subagents in parallel: anchor-detector, splitter, lumper, axis-divergence auditor. Outputs go to `architectures/v3/bias-guards/phase-2/`. The bias-guard briefs are recoverable from earlier dispatches in this branch's git history if needed.

**Why (intent).** The bias guards evaluate convergence patterns. Running them on the clean tracks reveals which convergences survive cleaning (corpus signal) vs which were prompt-anchoring (contamination).

**Expected outcome.** 4 new bias-guard reports.

**Stop-and-ask:** before dispatching, surface the bias-guard plan and confirm the briefs; wait for user go-ahead.

### Step 3.3 — Open the Phase-2 PR

**What.** Open a PR for the Phase-2 work — 9 re-dispatched tracks (step 3.1), bias-guard re-runs (step 3.2), and any prior commits on this branch not yet on `main`. Ready-for-review (not draft) per AGENTS.md.

**Why (intent).** The PR is the user's review surface and the audit trail for the contamination-fix discipline.

**Expected outcome.** One PR, ready for review.

**Stop-and-ask:** before opening, surface the proposed PR title and body; wait for user go-ahead.

### Step 3.4 — Clean up transient artifacts and update the master plan's pointer

**What.** After the Phase-2 PR merges to `main`:

1. Remove `architectures/v3/PHASE-2-RERUN-PLAN.md` from the live tree (preferred: `git rm`; alternative: move to `archive/` with a status header).
2. Update the current-state pointer at the top of [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) from "in Phase 2" to "in Phase 3" — and remove the line referencing the takeover plan (which no longer exists).

The banner at the top of [`research/PLAN.md`](../../research/PLAN.md) stays as-is. It points at the master synthesis plan, which is durable.

**Why (intent).** The takeover plan is transient — exists only for this one session-to-session handoff. The master plan is durable and continues through Phases 3-8. Updating its current-state pointer keeps the chain to subsequent phases intact.

**Expected outcome.** No takeover plan in the live tree. Master plan's pointer reflects current phase.

---

## 4. Appendix

Historical artifacts (do not read into context): [`history/HISTORICAL-RECORD.md`](history/HISTORICAL-RECORD.md).
