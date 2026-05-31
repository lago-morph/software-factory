# C32 — LLM-as-judge Harness  (Build Plan, canonical track)

> Source / Spec ref: spec/C32-judge-harness.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Inspect AI scorer wrap.** Expose the Inspect AI scorer as a Gas City pack/tool node (`inspect_eval`, AI-CONTEXT §13.3), adopted off-the-shelf — no scoring engine authored. This is "the harder part" v4 flags (README:442). | M | C02, C17, C30 (Inspect AI pack) |
| T2 | **Judge-model binding (C29).** Consume `resolveModel(judge node)` + the `IndependenceConstraint` from C29; run the scorer's grader as the **Claude Code judge** (same provider, Phase-0 `L1`, D-1). | S | C29, C28 |
| T3 | **`scoreTrajectory` core.** Bind (trajectory ref + held-out scenario `Task`/rubric) into one scoring run → one satisfaction score. The genuine custom glue C32 adds beyond the stack. | M | T1, T2, C21/C19 |
| T4 | **`ScoreRecord` emission.** Emit one structured, attributed (C41) score per (trajectory, scenario, judge) to a bead/CXDB turn ("judge outputs from beads", README:426) for C33/C34/C46. | M | T3, C41, C19/C21 |
| T5 | **Rubric binding.** Load the scenario's versioned grading criteria (Inspect AI Python objects, README:186) at score time; do not author/mutate them (C30 owns content). | S | T1, C30 |
| T6 | **Multi-judge ensemble.** Run N scorers over one trajectory; reduce to a disagreement signal in the `ScoreRecord` (README:187; F46) — **Inspect AI provides the multi-scorer *execution* (off-the-shelf); C32 authors no ensemble engine**, only the request + the disagreement field (capability-for-principle bar). | M | T3, T4 |
| T7 | **Judge rig placement (independence-by-isolation).** Run the judge in the **`judge` rig** (a distinct *role* — grounded in inventory C42 + spec/C42, not AI-CONTEXT §13.3) with a disjoint role/prompt/rubric from the coder; stamp the active independence level on each record (D-1/D-13). **The judge's exact partition read-surface is OQ-C42-3/OQ-C34-3 (deferred); build against the C42/C34 ruling, do not pre-decide it.** | S | C42 |
| T8 | **Degraded paths.** Judge-unavailable / partition-miss → unscored + bead/gate event; never a fabricated score (I4). Partial ensemble flagged with reduced N. | S | T3, T4, T6 |
| T9 | **FE-1 seam (do NOT build).** Leave the judge-model identity + independence-level fields as the clean switch FE-1 flips for cross-family/cross-provider judging; build no cross-family machinery, assume no second-provider credential (G08/G20, D-1). | S | T2, T4 |

## 2. Dependency graph

Critical path: **C30 (scenario corpus) + C29 (judge model) → T1 → T2 → T3 → T4 → end-to-end score consumable by C33**.
- T1 (Inspect AI wrap) and T2 (judge-model binding) are the two gates; T3 joins them into the first real score.
- **Must precede C32:** C30 (held-out scenarios + the Inspect AI pack), C29 (judge identity + independence constraint), C42 (the `judge` rig/partition), C21/C19 (trajectory source), C41 (attribution).
- **Built concurrently with C32:** C33 (aggregates C32's `ScoreRecord` — depends on the *record schema*, not C32 internals), C34 (audits judge-independence/isolation — consumes the stamped level, enforces separately per D-13), C46 (judge-FP-rate meta-metric — consumes scores), C31 (runner — may *invoke* C32 as scorer; the C31↔C32 seam is the join, OQ4).

## 3. Parallelization

After T1 + T2 land, three independent workstreams fan out:
- **WS-A (scoring core):** T3 + T4 + T5 — bind→score→emit→rubric. The spine; produces the `ScoreRecord`.
- **WS-B (variety lever):** T6 — multi-judge ensemble + disagreement. Independent of emission once the record shape (T4) is frozen; the P5-Ashby/F46 lever.
- **WS-C (isolation + robustness):** T7 (judge rig) + T8 (degraded paths) + T9 (FE-1 seam). Governance/robustness; independent of A/B once the record carries the independence level.

T4 (the `ScoreRecord` schema) is the **freeze-early join point** — C33, C34, and C46 all build against it, so it gates the most downstream parallelism (see §4).

## 4. Interfaces-first / contract milestones (freeze early)

1. **`ScoreRecord` schema** (T4) — the single most load-bearing contract: C33 (aggregate), C34 (independence audit), and C46 (judge-FP-rate) all bind to it. Freeze first so all three build against stubs in parallel. Must carry: scenario id+version, trajectory ref, score (Inspect AI shape), judge model id + **active independence level**, ensemble disagreement. (`[FAITHFUL-FILL]` — needs a canonical schema ruling, OQ2.)
2. **`scoreTrajectory(trajectoryRef, scenarioRef) → ScoreRecord`** (T3) — the harness entry point; freeze so C31 (runner) and any batch/replay caller can invoke C32 as the scorer.
3. **Judge-model + independence contract** (T2) — what C32 consumes from C29 (`resolveModel` + `IndependenceConstraint`, Phase-0 `L1`). Freeze the *consumption* shape so C29 and C32 evolve independently.
4. **Judge-rig partition contract** (T7) — the `judge` rig (role) C42 provides and C34 audits (D-13); the exact partition read-surface (dedicated `judge` partition vs role-isolated read of `code`+scenario-outputs) is the **open** joint question OQ-C42-3/OQ-C34-3, owned by C42/C34, not frozen by C32. Freeze C32's *consumption* shape so C42/C34 build the partition + audit against it.

## 5. Risks & de-risking order

1. **Inspect-AI-scorer-as-pack (T1), highest.** Prove the scorer wraps cleanly as a Gas City pack/tool node and accepts a trajectory + rubric — v4 explicitly flags "the Inspect AI wrap" as a harder part (README:442). Underpins the whole "adopt the stack" premise; spike first.
2. **Judge-as-Claude-Code under D-1 (T2/T7).** Prove a **same-provider** Claude Code judge runs in a **separate rig** with a disjoint role/prompt and produces a usable score *without* a second-provider credential. De-risks G08/G20 the canonical way (isolation, not family); confirms FE-1 is genuinely deferrable.
3. **`ScoreRecord` schema adequacy (T4).** Spike the record against *all three* consumers (C33 aggregate, C34 audit, C46 FP-rate) before freezing — a missing field strands three downstream components (OQ2).
4. **Same-family bias residual (OQ1).** Not a build task — capture *how* same-family judge bias (F48 Partial) will be measured (judge-FP-rate via C46 / a calibration set) so the FE-1 trigger has evidence. Write the finding to review-log; do **not** build cross-family judging.
5. **Shared-seat cost/throughput (OQ3, with C28 G13/G34).** Judge calls (×N for ensembles) compete with build calls for the single Phase-0 Max seat. Quantify a judge token-budget probe → review-log; do not design horizontal scale on the canonical track.

## 6. Definition of done

- **Per spec ACs:** AC1 (one attributed `ScoreRecord` per (trajectory, scenario), consumable by C33), AC2 (same-provider judge in a separate rig, disjoint rubric, no second-provider credential, level `L1` stamped), AC3 (probabilistic score → distribution, not gate-pass), AC4 (multi-judge disagreement surfaced), AC5 (secondary-guard — never a deterministic safety gate), AC6 (honor-don't-enforce independence; audit is C34's), AC7 (no silent/fabricated score on failure).
- **Per-task DoD:** each task's artifact (the scorer pack, the binding, the record, the rig placement) is version-controlled in a pack (C02) and exercised by at least one real scoring run with the `ScoreRecord` captured on a bead/CXDB turn.
- **Component DoD:** a held-out scenario scores a real trajectory end-to-end via the **same-provider Claude Code judge** in the isolated `judge` rig, emitting an attributed `ScoreRecord` that **C33 reduces to a distribution** and **C34 can audit**; and the deferred edges (G08/G20 same-family bias residual → FE-1; OQ3 cost/throughput) have written findings in `_meta/review-log.md` — closed by escalation, not silent assumption. **No cross-family/independent-judge machinery and no second-provider credential are built (D-1/FE-1).**
