# HANDOFF — v4 Spec & Plan run (resume from here)

**Last updated:** 2026-05-30, at session token-limit cutoff.
**Branch:** `claude/architecture-v4-spec-plan-9Dxkg` · **Origin PR #213: MERGED** (all work below is in `main`).
**Working tree at cutoff:** clean, HEAD pushed. Nothing stranded. Components not listed as "done" were
**never built** (session token limit), not lost.

This file + the other `_meta/` artifacts are sufficient to resume with zero re-grounding.

---

## 1. Where we are: 23 of 57 components built (both tracks, Sweep-1 / architecture altitude)

**DONE (23)** — each has 4 docs: `spec/`, `plan-faithful/`, `spec-optimized/`, `plan-optimized/`:
C01 C02 C03 C04 C05 C07 C08 C09 C10 C12 C13 C17 C19 C20 C21 C22 C23 C24 C25 C28 C29 C41 C42

- **Batch 1 (C01,02,03,07,08,17,19,20,21,22,23,41)** is the gold standard: built → adversarially
  reviewed by 5 subsystem red-teamers (fixes applied, `.review.md` per doc) → **Integration Pass 1**
  reconciled to internal consistency (`_meta/INTEGRATION-PASS-1.md`).
- **Batch 2 partial (C04,05,09,10,12,13,24,25,29,42 + C28)** built on both tracks; plans reconciled to
  rulings D-1..D-5. **NOT yet adversary-reviewed.**

**NOT BUILT (34)** — id [slug] (subsystem) — build next, in this batch order:

| Batch | Components (id [slug]) |
|---|---|
| 2 tail | C26 [otel-collector], C27 [langfuse-traces] |
| 3 | C06 [agent-messaging], C11 [intent-intake], C14 [formula-dot-translator], C15 [workflow-linter], C16 [discipline-linter], C18 [reconciler-convergence], C30 [scenario-store], C31 [scenario-runner], C32 [judge-harness], C33 [satisfaction-metric], C34 [holdout-integrity], C35 [override-why-loop], C40 [durable-orders] |
| 4 | C36 [anomaly-detection], C37 [trajectory-clustering], C38 [diagnosis-agent], C39 [fix-task-loop-closure], C43 [isolation-boundary], C44 [digital-twin], C45 [twin-fidelity], C51 [gene-transfusion], C52 [self-bootstrap], C53 [bootstrap-validation], C54 [phase-plan], C55 [methodology-experiment], C56 [autonomy-ladder] |
| 5 | C46 [meta-metrics], C47 [variant-identification], C48 [ab-routing-stats], C49 [counterfactual-replay], C50 [promotion-gate], C57 [failure-mode-coverage] |

(Full descriptions, dependencies, and per-component gap IDs are in `_meta/component-inventory.md`.)

## 2. Then: passes still owed
1. **Batch-2 adversary review wave** for C04,05,09,10,12,13,24,25,28,29,42 (Batch 1 already reviewed).
2. **Adversary review** for Batches 2-tail/3/4/5 as each is built.
3. **Integration Pass 2+**: re-run the integrator after each batch to catch new cross-component drift.
4. **Sweep 2 (implementation-ready):** concrete signatures, schemas, sequence/state diagrams, error
   taxonomies, acceptance tests — re-enter every component once Sweep-1 breadth is complete.
5. **Sweep 3 (exhaustive):** pseudocode, skeletons, edge-case catalogs, perf/sec/ops.
6. **Final cross-cutting pass:** whole-system consistency, critical-path/parallelism analysis of the
   build plan, Track A vs Track B comparison memo, top-level README/index.

## 3. How to resume (exact procedure)
1. Read this file + `_meta/META-PLAN.md` (process), `_meta/review-log.md` (decisions D-1..D-5 + open
   issues), `_meta/component-inventory.md` (backbone). Do NOT read the four v4 source docs into the
   primary context — subagents do that.
2. Use the standing briefs verbatim: `_meta/BUILDER-BRIEF.md`, `_meta/ADVERSARY-BRIEF.md`. Dispatch one
   builder per (component × track) with a tiny prompt: component id+slug+one-liner, track, sweep level.
3. **Concurrency cap is ~8** (platform rate-limits beyond that; 16/24 failed when I tried 24). Pipeline
   at width 6–8; let it drain to ~2 then dispatch the next chunk.
4. **Subagents never run git.** Primary commits + pushes between waves (the only thing that survives the
   ephemeral sandbox). Retry push with backoff.
5. After each batch builds, run the adversary wave, then the integrator to apply any new rulings.

## 4. Binding decisions already made (do not relitigate) — detail in `review-log.md`
- **D-1** same-provider judge baseline; cross-provider judge → `FUTURE-ENHANCEMENTS.md` FE-1.
- **D-2** one namespace: `softwarefactory.v4.{beads,trajectory,packs}` (no vendor `strongdm.*`).
- **D-3** C20 authors bead-type schemas; C22 = registration mechanism + CXDB-turn types only.
- **D-4** C20 depends on C19 (co-foundational; M1 interface freeze + no-op `validate` stub).
- **D-5** C41 owns the provenance hash-chain over C23-provided ordered `event_id`s.

## 5. Open items needing a HUMAN decision (carry into next session)
- Signing **mandatory vs optional** (Track A optional per README:229; Track B graduated-mandatory).
- **G37** secrets store — no secrets manager chosen; blocks several Track-B security assurances.
- **XC-6** Phase-0 signing assurance is a mechanism, not a control, until G37 lands.
- Bundle granularity within `softwarefactory.v4.beads` (one shared bundle vs per-type) — sweep-2 detail.

## 6. Key risks the Skeptic flagged (still true, must be designed for in the unbuilt components)
- **G11** — entire plan assumes Gas City exists/behaves as described; every "Native" claim unverified.
  Sweep 2 must freeze real `gc` schemas (formula/molecule/bead) before dependents bind. (Hits C12/C13/C14/C15.)
- **G18** — self-healing loop (C36–C39) needs a termination bound + fix-authorization contract; schema
  slots exist (C20) but the numeric policy is owed by **C39** (unbuilt).
- **G31** — lethal-trifecta isolation window; C04/C42 shrink it at spawn but the real fix is **C43** (unbuilt).

## 7. Artifact map (`architectures/v4/_meta/`)
META-PLAN · TRACK-CHARTERS · DOC-TEMPLATES · BUILDER-BRIEF · ADVERSARY-BRIEF · component-inventory
(+ -A/-B raw) · ambiguities-and-gaps · review-log · INTEGRATION-PASS-1 · FUTURE-ENHANCEMENTS · STATUS · HANDOFF (this).
