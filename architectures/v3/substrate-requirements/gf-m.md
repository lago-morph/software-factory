# Substrate requirements — GF-M (Greenfield, methodology-first)

**Candidate.** [GF-M — Greenfield, methodology-first](../tracks/greenfield-methodology-first.md). Mandate: greenfield. Axis: methodology drives; substrate is downstream derivation.

**Phase-3.5.5 status.** `survives` (per [registry §GF-M](../candidate-registry.md#gf-m--greenfield-methodology-first-1)). Forward action: P-21 paraphrase divergence calibration carried to Phase-8 lean-eval (OQ-T6); slice-coherence operational definition owed at Phase-4/5 methodology spec, not at this substrate-requirements layer.

**Authoring note.** This file serves as the **exemplar** for the Wave-4.1 per-candidate substrate-requirements fanout per [auto-004 Round 2](../decisions/auto-004-phase-4-dispatch-shape.md#wave-41-brief-shape-revised-per-reviewer-1-amendments). Other Wave-4.1 subagents consume it as a model for §1-§6 shape.

## §1 Primitive list (buildability-confirmed)

GF-M requires 5 substrate primitives (cognitive-escrow primitive demoted to methodology-layer per [DEC-2](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology); not listed here).

- **[P-02 — Cost ceilings (hard, multi-axis)](../primitives/cluster-C1.md).** Per-cycle / per-cycle-class hard caps on tokens, calls, $. Load-bearing for GF-M because Regime-A's paraphrase fan-out (N× multiplier on every reversible-commitment cycle) is the dominant cycle-cost driver. Verdict: `commodity`.
- **[P-06 — Watchdog tiers (Daemon / Triage / Patrol)](../primitives/cluster-C2.md).** 3-tier escalation. Used at promote-or-reverse boundaries to flag anomalous reversibility patterns (Daemon) and cross-cycle paraphrase-divergence drift (Patrol). Verdict: `commodity`.
- **[P-08 — Scenario storage (out-of-tree, holdout-partitioned)](../primitives/cluster-C3.md).** Append-only scenario store with substrate-enforced training/holdout partition. Load-bearing for GF-M's Regime-B (spec-anchored execution) — holdout enforcement is substrate-typed, NOT agent-discipline, per the track's CTR-G2 mitigation. Verdict: `designed-system` (escalated from commodity at sketch time per [P-08 sketch](../primitives/cluster-C3.md)).
- **[P-20 — Reversibility primitive (event-sourced)](../primitives/P-20-reversibility-primitive.md).** Cheap commit-and-reverse on intent / scenario / artifact objects via event-sourced storage. THE load-bearing primitive for Regime-A's unit-of-work (reversible commitments). Sub-ms cost per the sketch; cycle cost dominated by paraphrase fan-out, not by reversibility itself. Verdict: `designed-system`.
- **[P-21 — Paraphrase divergence primitive](../primitives/P-21-paraphrase-divergence.md).** N model-family-diverse paraphrasers callable in parallel with deterministic prompt-paraphrase generators. Used by Regime-A to probe spec-stability via divergence measurement before promoting a reversible commitment. Verdict: `designed-system` (calibration is RG — but calibration is not buildability).

## §2 RG primitives

Per the [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), GF-M carries one **partial RG flag** (not a full load-bearing RG primitive):

- **P-21 paraphrase divergence — calibration partial-RG.** The construction is `designed-system` (LiteLLM + asyncio.gather + Jinja2 seeded macros + sentence-transformers per [P-21 sketch](../primitives/P-21-paraphrase-divergence.md)). The *calibration* — choosing N, divergence-metric, and threshold against Larbi MCC ≤ 0.55 — is the open question (Phase-8 lean-eval candidate, GF-M's own OQ-T6).
- **Choice:** (b) accept-as-RG on the *calibration sub-component*. GF-M's methodology accepts that calibration is per-deployment work; the substrate exposes N, divergence-metric, and threshold as first-class first-class parameters so Phase-8 sweeps are tractable. No bounded sub-track is owed at Phase 4 — the calibration is methodology-layer (lean-eval) work, not substrate-layer.
- **Application-table row (per Phase-3.5.5 RG-primitive rule):** GF-M does NOT appear in the [Application to current candidates table](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) because P-21's RG portion is calibration-only, not the load-bearing RG class the rule was authored for. GF-M's calibration carries as Phase-8 lean-eval input per the [registry GF-M forward action](../candidate-registry.md#gf-m--greenfield-methodology-first-1).

## §3 Candidate-specific contracts on each primitive

GF-M's contracts on each primitive align with the per-primitive sketches' defaults; one exception with named delta:

- **P-08 scenario storage (holdout partition).** GF-M's contract: holdout enforcement is *substrate-typed*, not agent-policy. The sketch's default contract is OPA-mediated ABAC over `partition=train|holdout` with builder/judge role tokens (per [cluster-C3 § P-08](../primitives/cluster-C3.md)). GF-M takes this default as-is — the sketch's design content already meets GF-M's CTR-G2 mitigation requirement.
- **P-20 reversibility primitive.** GF-M's contract: event-sourced storage of intent + scenario artifacts with sub-ms per-event persist (per [P-20 sketch](../primitives/P-20-reversibility-primitive.md) and OpenHands V1 prior art). GF-M takes the default.
- **P-21 paraphrase divergence.** GF-M's contract: N ≥ 3 model-family-diverse paraphrasers callable in parallel via LiteLLM Router with cross-family tags. Deterministic prompt-paraphrase generators via Jinja2 seeded macros. GF-M parameterizes N, divergence-metric, threshold as first-class so Phase-8 lean-eval can sweep them.
- **No contested-primitive references.** GF-M does not name any of P-28, P-29, P-30, or P-19 (the Phase-4.2 same-vs-distinct candidates). No fixed sub-section headers needed.

## §4 X_UNM_B articulation

`N/A (mandate-specific candidate; X_UNM_B does not apply)`. GF-M is greenfield-only (per [working definitions](../phase-3.4-decisions-resolved.md#working-definitions-greenfield-brownfield-entry-mode-framing)); it does not need to acquire a Codebase Model from legacy artifacts because its system originates inside the methodology.

## §5 Open carries

- **Phase-4-internal workstreams.** None. GF-M has no Wave-4.5 authoring sub-track owed (no load-bearing RG primitive). The slice-coherence operational definition (own OQ-T1) and stage-A→B transition cost-modeling are *methodology-layer* questions for Phase 5 / Phase 6 methodology spec, not substrate Phase-4.1 work.
- **Phase-5 ADR seeds.** (i) P-20 reversibility primitive's integration contract with intent-artifact schema (event-sourcing storage choice — EventStoreDB vs Postgres event_log per [P-20 sketch](../primitives/P-20-reversibility-primitive.md) is an ADR question); (ii) P-21 paraphrase-generator deterministic-seed strategy (Jinja2 macro family choice); (iii) P-08 holdout-partition ABAC policy choice (OPA vs Cedar per [cluster-C3](../primitives/cluster-C3.md)).
- **Phase-8 lean-eval candidates.** (i) P-21 calibration sweep on N × divergence-metric × threshold against Larbi MCC ≤ 0.55 (GF-M's OQ-T6 confirmed; carries from Phase-3.5.5 registry forward-action); (ii) Regime-A→B slice-coherence transition cost (own OQ-T1) — measure cycle-cost overhead of slice-coherence enforcement.
- **F-mode carries.** F40 (last-mile drift) remains accepted-open at the methodology layer; addressed within GF-M's Regime-B (spec-anchored execution) per [DEC-1.b](../phase-3.4-decisions-resolved.md#dec-1b--greenfield--brownfield-artifact-continuity-na-lead-agent-misread-users-framing), not via a cross-mandate continuity deliverable.

## §6 Scoping-principle compliance

This summary preserves GF-M as a defensible architecture proposal:

- No primitive has been pre-eliminated; all 5 buildability-confirmed primitives carry forward.
- The single partial-RG flag (P-21 calibration) is honestly surfaced and routed to Phase-8 lean-eval rather than papered over.
- Open methodology questions (slice-coherence, stage-compression, paraphrase-fan-out cost) are named in §5 and routed to Phase-4-methodology-spec / Phase-5 / Phase-8 — not used to demote the candidate.
- The candidate's load-bearing claim (methodology drives; substrate is downstream commodity + 2 designed-system primitives) is preserved.

GF-M survives Phase-4.1 with no shrinkage, no RG-fallback, and no pre-elimination. The Phase-3.5.5 status (`survives`) is confirmed.
