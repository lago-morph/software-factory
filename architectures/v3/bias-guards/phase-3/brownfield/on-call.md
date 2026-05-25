---
guard: on-call-10yr
target: draft-brownfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 10-year on-call critique — brownfield draft

## §1 Persona stance

I am the engineer who inherited the factory at year 3, runs the year-3-to-year-6 pager rotation alone every fourth week, and is now staring at the year-7 board where the factory has eaten three acquisitions (a Python-shop AdTech, a Go-shop payments runtime, a SQL-and-TypeScript dashboard product) on top of a 200 kLOC original codebase now at 800 kLOC. The original operator who wrote the trifecta-perimeter policy left in year 4. My core claim: **the codebase model rots non-uniformly, the substrate's freshness metrics do not exist for the views that rot fastest, and Patrol's F34 cross-layer-drift detector is the first sensor that goes blind because the "slow layer" it watches has itself drifted.**

## §2 The 3am paging story

3:47am. Patrol fires an F34 cross-layer-drift alarm: regression-fix cycles to the `pricing-engine/` directory (vendored Go code from acquisition #2) have systematically violated an invariant the S-5 view says is load-bearing — "no pricing path may bypass the audit-log middleware." Daemon shows the cycles all completed green; trajectory capture shows clean attribution; cross-model judge approved every one. The PRs are merged, deployed, and have been running for nine days. SOC 2 audit is in eleven days.

I do what the draft tells me I can do: query the substrate for "when did each view of `pricing-engine/` last refresh?" The codebase index (S-1) was updated 14 minutes ago — healthy. The dependency-and-impact graph (S-2) shows... a number, but for Go code in `pricing-engine/`, the graph was built on day 1 using a Go-static-analysis pipeline deprecated since year 5 because the org swapped to a polyglot indexer that downgraded Go to "best-effort" fidelity (per BF-S OQ-T2). Nobody noticed because S-2 still *returned answers* — they were just stale, missing the new middleware wrapper added six months ago. Telemetry view (S-3) shows production traces for `pricing-engine/`, but the OpenTelemetry endpoint was re-pointed during the year-5 infrastructure migration; the traces are from the *staging* mirror, not production. Nobody told the substrate (DPB-9 surfaces this exact case but only at bootstrap, not as a continuous risk).

By 6am I have my diagnosis: **S-2 has been silently rotting since the indexer swap; S-3 has been pointing at staging since the migration; Patrol's F34 detector was correctly comparing fast-layer code changes against a slow-layer invariant view that was itself stale, so the audit-log-bypass change *looked* compliant against the snapshot of invariants S-5 had when the polyglot indexer was installed.** The Caremark prong-1 board report for this quarter is going to have to disclose that the factory's compliance attestation rested on three views the org cannot prove were fresh.

## §3 Specific protection-set claims that break

**ROBUST-B3 / ROBUST-B4 (codebase model + five sub-stores)** — breaks in three distinct ways:
- **S-2 (dependency-and-impact graph) is the silent-rot frontrunner.** Acquired-codebase merges *guarantee* polyglot. The graph keeps returning answers; nothing in the substrate distinguishes "high-fidelity graph for the original TypeScript core" from "best-effort graph for the acquired Go module." **This is the view most likely to silently rot.**
- **S-3 (runtime/telemetry) rots on infrastructure events, not commits.** ROBUST-B13 treats telemetry connection as a day-0 task; DPB-9 acknowledges it as a bootstrap problem. Neither names the continuous failure mode: telemetry pipelines get re-pointed, sampled-rate-changed, schema-migrated, vendor-swapped.
- **S-5 (invariant/debt) is per-acquisition.** The original codebase had hand-curated invariants; acquisition #1's code was ingested with auto-extracted invariants from its tests; acquisition #2 had no tests so S-5 there is empty; acquisition #3 had a different invariant DSL. Patrol treats S-5 as uniform. **It is not.**

**ROBUST-B9 (Patrol watches F34/F54/F55/F57)** — the claim assumes the slow-layer reference (S-2/S-5) is fresher than the fast layer. Brier's pace-layer framing *inverts* in the acquired-codebase case: the slow-layer invariant view of the acquisition is *staler than* the code, because ingestion happened once and the invariants were never refreshed against subsequent acquisition-code changes. **F34 detection is structurally backwards in the regions Patrol most needs to watch.**

**ROBUST-B10 (`AttributedEventLog`)** — content-addressed, signed, immutable for cycles run by the factory. Says nothing about *pre-ingestion* code. Three acquisitions' worth of commits are tagged "unattributed" per the day-0 rule, but the *factory's cycles against that code* attribute to the factory while operating against an unattributed-history baseline. F14's "forensic reconstruction widened" mitigation cannot reach back across the pre-ingestion boundary.

**DPB-4 (codebase-model continuity)** — BF-S/BF-L's "continuously maintained" framing assumes the maintainer keeps working. The original operator who configured the per-language fidelity tiers, the telemetry endpoints, and the invariant-extraction rules left. **There is no operator-handoff artifact in the draft.**

**DPB-6 (per-region regime classification)** — BF-L's own OQ-T4 flags this for F43. When the regulator asks "what regime is the factory at?" the truthful answer in year 3 is "L4 in `core/`, L3 in `pricing-engine/` because S-3 fidelity is degraded there, mixed in `acquisitions/` per-subregion." **The substrate has no `freshness-score` primitive per (view × region).**

**ROBUST-B14 (graduation discipline)** — bar inputs are S-2 impact-graph stability, S-3 telemetry density, S-1 coverage, cross-model judge agreement rate. **None has a freshness term.** A stable S-2 reading against a stale S-2 view passes the bar. F57 fires here exactly: the eligibility-classification mechanism drifts because its inputs are silently stale, not because anyone moved the threshold.

## §4 Concrete recommendations for Phase-3.4

1. **Per-view freshness primitive as a substrate ADR (Phase-5 wave-1).** Every query against S-1/S-2/S-3/S-4/S-5 returns `(answer, freshness-tuple)` where the tuple includes: last-rebuild-timestamp, last-incremental-update-timestamp, ingestion-pipeline-version-hash, source-fidelity-tier, confidence scalar. Methodology cycles refuse to consume any S-view answer without consuming the freshness tuple.

2. **Acquired-codebase merge as a named substrate event class.** Distinct from "incremental commit." Triggers a re-run of ROBUST-B13's day-0 legacy-ingestion sequence *scoped to the merged region* and writes a `merge-event` record to AttributedEventLog. Until re-ingestion completes, the merged region is force-classified L3.

3. **Infrastructure-event substrate webhook.** Telemetry endpoint swaps, indexer swaps, schema migrations, sandbox-config changes — substrate exposes a `substrate-config-event` endpoint operators *must* call. Resets affected view's freshness to "stale, pending re-validation."

4. **Per-region freshness dashboard as the Caremark prong-1 surface.** The board report is: `(region, view, freshness-tier, eligibility-regime, last-event)` rather than a single L-level. Per-region regime (DPB-6) becomes regulator-defensible only if the on-call has this surface.

5. **Operator-rotation handoff artifact, substrate-resident.** A `substrate-config.md` co-located with the codebase model, version-controlled, listing per-(view × region) configuration semantics. The new operator's first action is `substrate-config diff <last-handoff-tag> HEAD`.

6. **F34 detector self-test as Patrol's daily smoke test.** Patrol periodically introduces a known-bad change against a known-fresh region and verifies the detector fires. Treats Patrol itself as an instrument that needs calibration.

7. **Phase-8 lean-eval candidate: year-3 brownfield maintenance simulation.** Spin up the factory against a synthetic 200→800 kLOC growth with two synthetic-acquisition merges injected at month 12 and month 18. Measure which views drift fastest, whether Patrol catches the F34 drift, whether the freshness-tuple primitive suffices.

The protection set is not wrong. It is *under-instrumented for time.*
