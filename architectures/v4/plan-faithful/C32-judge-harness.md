# C32 — LLM-as-judge Harness  (Build Plan, canonical track)

> Source / Spec ref: spec/C32-judge-harness.md
> Status: sweep-2

> **Sweep-2 contract changes (applied in-place):**
> - D-37 resolves OQ4: C31↔C32 contract = post-hoc scoring; C31 writes trajectory log; C32 scores it.
>   T3 below updated to reflect `score(trajectory_log, scenario, dod)` signature (spec §3.1).
> - D-38 resolves OQ5: judge runs in a **separate judge rig** (not a role-isolated read; a distinct rig
>   co-resident in the city per D-31). T7 updated.
> - D-39 resolves OQ2: `ScoreRecord` schema FROZEN (spec §3.2). T4 is no longer a milestone — it is
>   delivered (by this spec). C33/C34/C46 build against it immediately.
> - D-36: eval-tier trajectory source = Inspect AI trajectory log (NOT CXDB); C21 removed from T3 prereqs.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Inspect AI scorer wrap.** Expose the Inspect AI scorer as a Gas City pack/tool node (`inspect_eval`, AI-CONTEXT §13.3), adopted off-the-shelf — no scoring engine authored. This is "the harder part" v4 flags (README:442). The scorer must accept the trajectory log + judge prompt (§3.3) as inputs and return `{score, label, rationale}` JSON. | M | C02, C17, C30 (Inspect AI pack) |
| T2 | **Judge-model binding (C29).** Consume `resolveModel("judge")` + the `IndependenceConstraint` from C29; run the scorer's grader as the **Claude Code judge** (same provider, Phase-0 `L1`, D-1). Freeze the consumption shape so C29 and C32 evolve independently. | S | C29, C28 |
| T3 | **`score()` core (post-hoc, D-37).** Implement `score(trajectory_log, scenario, dod, judge_model, independence, n_judges) → ScoreRecord` (spec §3.1). The hand-off artifact is the C31-produced Inspect AI trajectory log — NOT a CXDB reference. C32 reads the log post-hoc (D-37). Bind it + scenario + DoD text into the judge prompt (§3.3); SHA-256 hash the prompt; invoke the Inspect AI scorer. The genuine custom glue C32 adds beyond the stack. | M | T1, T2, C31 (trajectory log), C30 (scenario) |
| T4 | **`ScoreRecord` emission (schema FROZEN, D-39).** Emit one structured, attributed (C41) `ScoreRecord` bead per `score()` call — all fields from the frozen §3.2 table — persisted to C19 as `softwarefactory.v4.beads:score_record`. Schema is already frozen; this task implements the writer. **C33, C34, C46 may build stubs against the schema immediately.** | M | T3, C41, C19 |
| T5 | **Judge-prompt construction + rubric binding (D-15, §3.3).** Construct the holistic judge prompt: scenario description + free-form DoD text (verbatim, per D-15 — no per-criterion enumeration) + trajectory excerpt. Hash it. C30 owns scenario content; C32 owns the prompt assembly. | S | T1, C30, C08 (DoD) |
| T6 | **Multi-judge ensemble (n_judges > 1).** Run N Inspect AI scorers over the same prompt (multi-scorer, README:187); collect `per_judge_scores` list; compute `disagreement = std-dev`. Inspect AI executes the multi-scorer; C32 owns only the request policy and the reduction. Set `error_code = "E-C32-03"` if a sub-judge fails. | M | T3, T4 |
| T7 | **Separate judge rig placement (D-38, D-31).** Run the judge in a **separate judge rig** co-resident in the city with the worker rig (D-31: multiple rigs per city). The judge rig MAY read the worker trajectory log + held-out scenarios; the worker rig MUST NOT read the judge rig or scenarios; no shared context window (D-38). Stamp `independence_level` on each record. C42 provides the partition; C34 enforces+audits; C32 runs inside it. | S | C42 (judge rig partition) |
| T8 | **Error paths (E-C32-01..06).** Implement all six E-code paths (spec §5a): judge-unavailable, log-unparseable, partial-ensemble, holdout-leak-detected, score-parse-fail, timeout. Each path emits a gate-event bead with the appropriate `error_code` and NO fabricated `ScoreRecord` (I4). `E-C32-04` (holdout-leak) additionally notifies C34. | S | T3, T4, T6 |
| T9 | **FE-1 seam (do NOT build).** `judge_model_id` + `independence_level` are the clean switch FE-1 flips for cross-family/cross-provider judging. Build no cross-family machinery, assume no second-provider credential (G08/G20, D-1). Document the fields as the seam in the frozen schema comment. | S | T2, T4 |

## 2. Dependency graph

Critical path: **C30 (scenario corpus) + C29 (judge model) + C31 (trajectory log) → T1 → T2 → T3 → T4 → end-to-end score consumable by C33**.

- T1 (Inspect AI scorer wrap) and T2 (judge-model binding) are the two gates; T3 joins them into the first real score.
- **Must precede C32:** C30 (held-out scenarios + Inspect AI pack), C29 (judge identity + independence constraint), C42 (judge rig partition, D-38), C31 (trajectory log producer, D-37), C19 (bead store for `score_record` emission), C41 (attribution).
- **`ScoreRecord` schema (§3.2) is FROZEN (D-39) — C33, C34, C46 build against it immediately without waiting for T4.**
- **Built concurrently with C32 now that schema is frozen:** C33 (aggregates `ScoreRecord` — builds against frozen §3.2), C34 (audits `judge_model_id` + `independence_level` + `judge_prompt_hash` — builds against frozen §3.2), C46 (FP-rate — reads `satisfaction_score` + `per_judge_scores` from frozen §3.2).
- **Note (D-36):** C21/CXDB is NOT a C32 dependency for the spine eval path. Trajectory source = C31 log.

## 3. Parallelization

After T1 + T2 land, three independent workstreams fan out:

- **WS-A (scoring core):** T3 + T4 + T5 — prompt-construct→score→emit→rubric-bind. The spine; produces the first real `ScoreRecord`. T5 feeds T3 (prompt) and T4 (DoD version field).
- **WS-B (variety lever):** T6 — multi-judge ensemble + disagreement reduction. Independent of WS-A once T4's emission shape is implemented; the P5-Ashby/F46 lever.
- **WS-C (isolation + robustness):** T7 (judge rig, D-38) + T8 (error paths, E-C32-01..06) + T9 (FE-1 seam). Governance/robustness; independent of A/B once the record carries `independence_level`.

Because the `ScoreRecord` schema is already frozen (D-39), the downstream C33/C34/C46 parallelism is unblocked from day one of the C32 build.

## 4. Interfaces-first / contract milestones

> **Schema already frozen (D-39) — no milestone needed for `ScoreRecord`.**
> The schema in spec §3.2 is the contract. C33, C34, C46 build against it now.

Remaining contract milestones (gates in the critical path):

1. **`score(trajectory_log, scenario, dod, ...) → ScoreRecord`** (T3) — the harness entry point; freeze so any batch/replay caller can invoke C32 without waiting for full T3 implementation. The signature is already concrete (spec §3.1); the milestone is a stub that validates inputs and emits a placeholder `ScoreRecord` so downstream callers can integrate.
2. **Judge-model + independence contract** (T2) — what C32 consumes from C29 (`resolveModel("judge")` + `IndependenceConstraint`, Phase-0 `L1`). Already specified (spec §3.1 `ModelIdentity`/`IndependenceConstraint` params); freeze the consumption interface so C29 evolves independently.
3. **Judge-rig partition contract** (T7) — the separate judge rig (D-38) C42 provides. Freeze C32's dependency on the rig config (`[[rig]]` name in `.gc/site.toml`; `city.toml` partition per D-32 G11 caution) so C42 and C34 build the partition + audit against C32's declared rig name.
4. **E-C32-04 (holdout-leak) notification seam to C34** (T8) — freeze the gate-event schema so C34 can subscribe to it. This is the highest-severity error path.

## 5. Risks & de-risking order

1. **Inspect-AI-scorer-as-pack (T1), highest.** Prove the scorer wraps cleanly as a Gas City pack/tool node and accepts the judge prompt (§3.3) format + trajectory excerpt — v4 explicitly flags "the Inspect AI wrap" as a harder part (README:442). Underpins the whole "adopt the stack" premise; spike first.
2. **Post-hoc scoring with C31's log format (T3, D-37).** Prove C32 can parse and excerpt C31's Inspect AI trajectory log format as input to the judge prompt. The hand-off artifact format (Inspect AI `EvalLog` JSON) must be agreed with C31 before T3 locks.
3. **Judge-as-Claude-Code in a separate rig (T7, D-38).** Prove a same-provider Claude Code judge runs in a **separate rig** (not just a disjoint prompt/role) with no shared context window with the worker rig. De-risks D-38 the canonical way; confirms the judge rig partition C42 provides is the correct isolation boundary.
4. **Same-family bias residual (OQ1 — partially resolved).** Not a build task. The FE-1 trigger is: C46 measures a persistent judge-FP-rate above threshold (e.g. >15%) on a calibration set → activate FE-1. Write the finding to review-log; do **not** build cross-family judging.
5. **Shared-seat cost/throughput (OQ3, with C28 G13/G34 — still open).** Judge calls (`n_judges × trajectory count`) compete with build calls for the single Phase-0 Max seat. Quantify a judge token-budget probe → review-log; do not design horizontal scale on the canonical track. Ensemble scoring is the multiplier; default `n_judges = 1` defers the cost until calibration warrants it.

## 6. Definition of done

- **Per spec ACs (concrete):** AC-C32-01 through AC-C32-14 (spec §8) — each has a given/when/then and an E↔AC cross-reference.
- **Per-task DoD:** each task's artifact (scorer pack, binding, record emission, rig placement, error paths) is version-controlled in a Gas City pack (C02) and exercised by at least one real scoring run with the `ScoreRecord` persisted as a C19 bead.
- **Component DoD:**
  - A C31-produced Inspect AI trajectory log + a held-out C30 scenario + a C08 DoD text flow through `score()` end-to-end, with the **same-provider Claude Code judge** in the isolated judge rig, emitting an attributed `ScoreRecord` that C33 can aggregate and C34 can audit.
  - All 14 ACs pass.
  - E-C32-01 and E-C32-04 paths are exercised (AC-C32-07, AC-C32-09).
  - Deferred edges documented in review-log: G08/G20 same-family bias residual (FE-1 trigger = C46 FP-rate gate); OQ3 cost/throughput quantification.
  - **No cross-family/independent-judge machinery and no second-provider credential are built (D-1/FE-1).**
