---
guard: red-team
target: draft-brownfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 red-team critique — brownfield draft

## §1 Persona stance

I'm attacking the load-bearing claims of the brownfield synthesis from a corpus-grounded adversarial position. The draft is ambitious about what its substrate can do — "queryable, incrementally maintained codebase model"; "role-partitioned reads"; "AttributedEventLog at Stripe scale"; "cross-model judge as brownfield default" — yet the corpus the draft cites either does not establish these primitives at the scale claimed, *contradicts itself on whether they're necessary*, or quietly inherits a single-author shape without independent corroboration. The strongest attack vector is not that any single claim is false — it is that the load-bearing claims chain together in a way the corpus does not actually warrant *together*.

## §2 Top attack findings

### Attack 1 (PRIMARY). ROBUST-B7 + ROBUST-B6 collapse together: in-codebase scenarios cannot be cleanly role-partitioned from builder context

**Target.** ROBUST-B7 ("D-2 explicitly challenged for brownfield — scenarios live inside the codebase") plus ROBUST-B6 ("D-4 holdout discipline substrate-enforced via role-partitioning of in-codebase reads").

**Attack.** Three problems:

1. **A builder agent's *job* is to read the codebase.** Per ROBUST-B3 and the three tracks unanimously, the codebase model is the agent's *primary input*. CTR-B5 / WEAK-3 sharpening does not, in StrongDM's own primary text, separate "the agent that builds" from "the agent that judges" by partitioning code views. StrongDM partitions *scenarios* (out-of-tree) from *code* (in-tree, fully readable). The Phase-3 draft inverts this — scenarios are now *in* the codebase — but then asks the substrate to invent a *new* partition that the corpus has not established precedent for. Brownfield-substrate-first §1.S-3 says builders "cannot read holdout telemetry; only the V&V agent role can" — but offers *zero corpus citation* for that as an enforceable substrate operation.

2. **The codebase is a connected graph; the partition leaks via dependency edges.** ROBUST-B4's S-2 (dependency-and-impact graph) and the call-graph view in S-1 *transitively* connect every held-out telemetry / test to the modules a builder must touch. A builder fixing `payments/charge.py` queries S-2's blast radius, which surfaces `test_charge.py::test_replay_2024_11_incident` as an impacted test. The "role-partition" must either (a) tell the builder "there's an impacted test you can't see" — which leaks existence and approximate purpose, or (b) hide the dependency edge — which breaks ROBUST-B9's F34 cross-layer-drift detector.

3. **Brownfield-methodology-first §7 OQ-T4 already concedes the attack:** *"D-2 challenge inverts holdout-location but does not specify how the unseen subset is selected from a codebase-derived pool without leaking."* The draft promotes this to a ROBUST claim by combining it with brownfield-substrate-first §1's *assertion* that the substrate enforces partition, but assertion is not evidence.

**Severity: HIGH, load-bearing.**

**Recommended action.** Demote ROBUST-B7 to DPB-11. Reframe ROBUST-B6 to acknowledge soft-partition with declared leakage paths.

### Attack 2. ROBUST-B3 "queryable, incrementally maintained codebase model" presumes substrate machinery the corpus has not built

**Target.** ROBUST-B3 + ROBUST-B4 (five sub-stores) is "load-bearing" and unanimous.

**Attack.** CTR-C5 is *high-impact and unresolved*: the two corpus-derived substrate-stack recommendations point at incompatible systems (OpenHands+Overstory in Python vs. Gas City in Go). Neither has a documented `CodebaseModel` primitive at the five-view shape:

- OpenHands V1 measurement context is **single-cycle replay** across SWE-Bench Verified — there is no documented *cross-cycle incrementally maintained codebase model* primitive.
- Gas City's `discovered-from` edge in Beads is one *attribution* edge, not a five-view-store.
- DPB-4 already concedes the corpus is split on whether the model is *maintained* (BF-S, BF-L) or *per-cycle reconstructed* (BF-M). The draft elevates the *existence* of a unified model to ROBUST while admitting the *maintenance cadence* to DPB.

**Severity: MEDIUM-HIGH, load-bearing.**

**Recommended action.** Re-cite ROBUST-B3 to name the *capabilities* it requires and explicitly mark each as either (a) corpus-attested at a named substrate, or (b) capability-gap that becomes a Phase-5 ADR.

### Attack 3. ROBUST-B8 cross-model judge as brownfield default is genuinely unresolved

**Target.** ROBUST-B8 says cross-family judge is the brownfield default; the draft adds a soft caveat about Anthropic same-model-different-role.

**Attack.** CTR-D7 is direct: *"a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements"* and *"For LLM-as-Judge selection, using the same model is usually fine because the judge is doing a different task than your main LLM pipeline."* This is **Anthropic's deepest evals primary**. CTR-D8 adds Husain/Shankar same.

The draft's justification — *"the absence of pre-graduated work-unit-class evidence at the start of any new factory's brownfield engagement"* — is a temporal hedge, not a corpus citation. It is a *lead-agent inference*. The cross-family case rests primarily on CJ Hess kevin/carl (one personal-harness anchor) and F46 (which IS the failure mode, not the mitigation).

**Severity: MEDIUM-HIGH.** Unit economics matter at Stripe scale.

**Recommended action.** Demote ROBUST-B8 to a per-cell decision: cross-family REQUIRED *only* for work-unit-classes touching production-adjacent code or where prior cycle's same-model judge agreed with builder >X% (collusion signal). Otherwise same-model-different-task per Anthropic/Husain-Shankar.

### Attack 4. ROBUST-B10 AttributedEventLog at Stripe-scale is asserted, not corpus-supported

**Target.** ROBUST-B10 says trajectory capture + immutable attribution is "substrate-resident, content-addressed, signed."

**Attack.** Substrate-cost evidence is OpenHands' sub-ms persist over **433 SWE-Bench Verified replays**. 433 ≠ 1,300/week × 52 weeks × N codebases. The draft cites Stripe's 1,300 PRs/week (ROBUST-B11) as the brownfield-scale anchor in the SAME section that promotes AttributedEventLog to substrate, but there is no corpus measurement of trajectory-capture cost or attribution-store query-throughput at that scale.

F43 (RSI Board-Visibility Gap) requires *structured board reporting* on Caremark prong-1 — *not* an event log. Kahana names "structured reporting" as the failure surface; an AttributedEventLog is a corpus-grounded *input* to such reporting, not the reporting itself.

**Severity: MEDIUM.**

**Recommended action.** Split ROBUST-B10 into (a) "trajectory + attribution capture as substrate primitive" (corpus-supported at single-cycle scale; UNCERTAIN at industrial scale) and (b) "Caremark prong-1 board-reporting surface" (a *derived methodology layer* on top of (a), NOT a substrate primitive).

### Attack 5. DPB-6 per-region regime classification *does* fragment audit surface

**Target.** DPB-6 lists per-region classification as user-decision-pending and notes F43 board-visibility interaction.

**Attack.** Brownfield-legacy-ingestion-first §7 OQ-T4 raises this *as its own track's open question*. The answer per Kahana primary (report 31, F43 source) is **yes**: the Caremark prong-1 board report has to answer "is this deployment subject to SB 53 reporting?" — a yes/no per *deployment*, not a 47-region scatterplot.

**Severity: MEDIUM.**

**Recommended action.** In DPB-6's "concrete next action" line, add: "Per-region classification adopters MUST also commit to a per-deployment aggregation rule for the board-reporting surface."

## §3 What survives the attack

A meaningful core survives. **ROBUST-B1, B2, B5, B9, B11, B12, B13, B14** are not seriously challenged by corpus material: code-archaeological mandate, cold-start asymmetry, production-scissors-off as substrate-default, tiered watchdog with Patrol on F34, cost ceilings as non-optional, the 8-stage cycle aggregate shape, legacy-ingestion as substrate setup, and Day-0 default-to-L3-Augmentation are all corpus-anchored at multiple independent voices. The DPB-* set is the right shape — open user-facing questions with concrete next actions per ADR-0005.

The §1.6 F-mode coverage table is mostly defensible *at the mitigation-locus level*; my attacks are about whether the underlying primitives are corpus-warranted at the strength claimed, not about whether the mappings are wrong.

The draft's adversarial-dispatch design anticipates several of my attack vectors — which is good harness discipline.

## §4 Concrete recommendations for Phase-3.4

1. **Demote ROBUST-B7 to DPB-11 ("scenario-from-codebase governance — leakage mechanics unresolved").** Cite BF-M's §7 OQ-T4 as track-internal evidence. Reframe ROBUST-B6 to acknowledge soft-partition with declared leakage paths.

2. **Restructure ROBUST-B3 as a capability bundle.** Each of the five sub-stores in ROBUST-B4 must cite an independent corpus voice for the *substrate-primitive* promotion (not the phenomenon). Sub-stores that lack such a citation become Phase-5 ADR candidates.

3. **Demote ROBUST-B8 to a per-cell rule.** Cross-family judge mandatory ONLY for production-adjacent + same-model-judge-collusion-signal cells.

4. **Split ROBUST-B10 into capture-vs-reporting.** Attribution capture survives as substrate primitive (D-7); board-reporting surface becomes a Phase-6 architecture-spec concern.

5. **Strengthen DPB-6's regulatory-surface warning.** Per-region adopters explicitly commit to per-deployment aggregation for F43 prong-1.

6. **Add a "primitive-promotion bar" discipline section.** Every claim that promotes a phenomenon to a substrate primitive must cite *multiple independent corpus voices for the substrate-promotion specifically*. ROBUST-B3, B6, B8, B10 each fail this bar in their current form.

7. **Add an explicit "industrial-scale evidence gap" disclaimer.** The 433-SWE-Bench-replay measurement does not transfer to Stripe-scale claims without further evidence.
