---
guard: d7-blind-axis-u-1
target: unified-track convergence (cognitive-escrow / interval-as-substrate prohibited)
phase: 3.2
based-on-commit: 6da503a
based-on-date: 2026-05-25
---

# D7-U-1 blind-axis test: Unified-D — Adversarial-Falsification Topology

**Prohibitions applied:**
- Axes mentioning "interval", "escrow", or "cognitive escrow" — PROHIBITED.
- Substrate primitives derived from Kahana (research/30-cognitive-escrow.md, research/31-caremark-rsi-board-exposure.md) — specifically `EscrowSurface`, `EscrowInterval`, escrow-as-substrate-primitive promotion — PROHIBITED.
- The phenomenon (cognitive escrow) may be acknowledged at the methodology layer; the substrate-primitive promotion is what is prohibited.

## §0 Axis declaration and defense

**Chosen axis: adversarial-falsification topology.** Every load-bearing artifact in the factory — spec, plan, code change, evaluation, scaffold, ADR, knowledge-store entry, classifier decision — is parameterised by an **opposing-side declaration**: which model-family-different agent (or deterministic checker, or human-of-record) is responsible for *trying to falsify* it before it is allowed to compound forward. The architecture is the **topology** of those build/break pairs. Greenfield and brownfield are the same topology with different opposing-side instantiations.

The substrate's load-bearing primitive is not an interval, layer, or distance; it is a **falsification commitment**: a typed declaration that names (a) the artifact under test, (b) the opposing side (model family, deterministic checker, named human), (c) the falsification budget (cost ceiling, time budget, sample size), (d) the "did it survive?" verdict that gates compounding.

**Why this axis, and why for unified.**

1. **It is the corpus's *other* unifier.** The corpus repeatedly converges on opposing-side discipline without naming it as an axis: Tournament's "explicit model-family diversity to defeat the Hallucination Loop"; CJ Hess's `kevin`/`carl` cross-model QC pattern (report 34 §6.2, F46); Anthropic's Auto-Review subagent's five specialist critics (report 23 §3.5); Husain/Shankar's "judge doing a different task" finding (followup 07 §3.6); Willison's three-tier review; StrongDM's holdout-discipline (D-4); Attractor's *"do not unify"* (report 02, CTR-C4). Each is an *opposing-side commitment*; the corpus has not noticed it is the same axis.

2. **It treats F1/F27/F46/F48 as a single cascade and addresses them at substrate level.** All four canonical correlated-error failure modes share one mechanism: *no opposing side was committed to falsifying the output*. The substrate primitive (falsification commitment) is exactly the missing typed object the corpus needs.

3. **It is mandate-symmetric without using mandate as a parameter.** Greenfield's day-0 problem is that *no opposing side exists yet*. Brownfield's structural advantage is that *opposing sides are inherited*: the existing test suite, production telemetry, type system, dependency graph, and live users are *already* falsifiers. The mandate parameter is *which catalog of opposing sides exists at t=0*. This addresses CTR-G1 without inverting it.

4. **It survives F53 (voluntary-discipline fragility) without invoking the phenomenon at the substrate layer.** A falsification commitment is *not* a discipline — it is a typed declaration, written at artifact-creation time, mechanically refused by the substrate if absent. Structural-not-voluntary property comes from substrate refusing to compound un-declared artifacts.

5. **It pre-responds to the Brier "factory is the wrong metaphor" attack.** The frame is **Popperian conjecture-and-refutation** applied at the artifact level. Every artifact is a conjecture; every gate is a refutation attempt.

**Axes considered and rejected:**
- Interval-as-substrate / cognitive-escrow-interval — rejected by prohibition.
- Pace-layer-primary — rejected: corpus-thin and Brier-anchored.
- Substrate-vs-methodology layer — rejected: OQ-B2 is open.
- Anchor-distance / frozen-anchor — rejected as too close to interval/escrow convergence.
- Regime-classification by L3/L4/L5 — rejected as Jaymin-anchored.
- Work-unit-class taxonomy — rejected as derivative.
- Trajectory / event-store as substrate primitive — rejected as too thin.

## §1 Architecture sketch

**Name.** *Falsification-Topology Factory* (FTF).

**Unit of substrate.** A **Falsification Commitment** (`FC`): a typed declaration produced at artifact-creation time. Schema:

```yaml
FalsificationCommitment:
  id: stable-uuid
  artifact: content-addressed handle
  artifact-kind: spec | plan | code-change | eval | adr | skill | classifier-decision | scaffold-edit
  conjecture: declared-claim-about-the-artifact
  opposing-side:
    kind: model-family-different-agent | deterministic-checker | named-human | population-vote
    identity: provider/family/role
    independence-evidence: how was contamination-of-priors avoided
  refutation-attempt:
    budget: {tokens, time, sample-size}
    method: cross-model-judge | live-test | type-check | property-test | replay-trace | adversarial-paraphrase | red-team
    inputs: [content-addressed handles]
  verdict:
    outcome: survived | refuted | inconclusive | budget-exhausted
    counter-evidence: [pointers if refuted]
    survival-window: number-of-future-cycles-this-verdict-holds-for
  ledger:
    immutable-log-ref: AILCCP-style record
    trajectory-ref: D-7 event-stream handle
```

**Five substrate primitives:**

1. **FC store.** Content-addressed, append-only, ledger-style. An artifact with zero FCs cannot compound.
2. **Opposing-side router.** Substrate function producing the actual judging surface; honours Attractor's *do-not-unify* discipline.
3. **Compounding gate.** Refuses to make artifact A available to downstream artifact B unless A's declared FC has `outcome ∈ {survived, conditionally-survived-with-window}`. Structural replacement for voluntary review (F53) and D-4 holdout discipline at every artifact boundary.
4. **Independence auditor** (Patrol-tier per D-6). Monitors FC log for collusion / correlation patterns. F47, F48, F57 mitigation surface. Independence is *measured*, not declared.
5. **Survival-window registrar.** When a window expires, downstream artifacts that depended on the expired FC are flagged for re-falsification.

**Methodology layer (kept thin).** Methodology supplies the FC graph, defaults catalog, and attention-design layer (where the Kahana phenomenon is acknowledged — the substrate does *not* promote it to a primitive).

**How the same architecture serves both mandates.**
- **Greenfield day-0** has a sparse initial FC catalog. The operator is the only available opposing side for the day-0 intent FCs.
- **Brownfield ingestion** has a rich initial FC catalog: every existing test is an opposing side; production telemetry is an opposing side for runtime behaviour.
- **Steady-state for both** is the same topology.

## §2 How this addresses each load-bearing concern

### Lights-out / L5 tension

Option (b) + (c): lights-out is defined per-artifact-kind, conditioned on opposing-side independence and stability. CTR-A4 resolves: "lights-out" = no human in the per-cycle inner loop for artifact-kinds whose opposing-side stack is automated; "L5" = no human ever, which is *refused* because the independence auditor itself escalates to human-of-record when collusion is detected.

### UC4 (working hypothesis)

UC4 is *falsified for this architecture's domain*. Mandate-difference shows up as *initial FC-catalog density and opposing-side identity*, not as architecture-shape.

### OQ-B2

Boundary falls at *methodology*. Substrate primitives are shared.

### OQ-B3

Re-entry is structural: an FC with `opposing-side.kind: named-human` is the typed object.

### OQ-B4

All three (issue / change-request / codebase-evolution-proposal) are valid FC-graph shapes.

### OQ-B6

Per-artifact-kind, applied to the *opposing side's independence and stability*. Jaymin's K=5 thresholds are read as *opposing-side reliability bars*.

### F-mode coverage

- **F1 / F27 / F46 / F48 cascade**: foundational; FC primitive is the substrate's direct answer.
- **F12 / F33 / F44**: FCs on production-touching artifacts mandate `deterministic-checker` opposing-side; CaMeL-style typed-interpreter; substrate default-off production-scissors.
- **F36 / F37 / F38 / F39**: spec artifact's FCs include deterministic-checker (GtWR/EARS lint), cross-family-judge (Larbi contradiction detection), requirement-count-bound, complexity-diagnosis-checker.
- **F42 (cognitive-escrow negligence)**: acknowledged at methodology layer; the substrate does *not* promote attention-surface design to a primitive.
- **F43 (RSI board-visibility gap)**: FC ledger is the structured-reporting surface.
- **F53 (voluntary-discipline fragility)**: structural by construction — substrate refuses to compound artifacts without a survived FC.
- **F54 / F55 / F57**: cross-family judge mandatory on methodology-delta FCs; independence auditor monitors classifier decisions.

## §4 §4 defaults: accepted vs challenged

| # | Default | Stance |
|---|---|---|
| D-1 | accepted | Spec is artifact-kind `spec`; FCs attach. |
| D-2 | challenged | Scenarios are opposing-side instances on FCs; opposing sides may live in-tree or out-of-tree. |
| D-3 | challenged | Agent = opposing-side declaration; population and graph-node agents are FC opposing-side kinds. |
| D-4 | accepted with justification | This architecture *generalises* D-4 to every artifact boundary. |
| D-5 | accepted with justification | Cost ceiling is the FC's `refutation-attempt.budget` field. |
| D-6 | accepted with justification | Daemon/Triage/Patrol map onto FC-monitoring tiers. |
| D-7 | accepted with justification | Each FC's `ledger.trajectory-ref` is an OpenHands-style pointer. |

## §5 Cold-start

The FC store is initialised with a *seed catalog* of FCs whose opposing side is the operator-of-record plus deterministic checkers seeded from priors. Day-0 FC defaults are strictest (every artifact-kind has minimum two opposing sides; operator-as-opposing-side mandatory on intent / architecture-sketch FCs; survival-window defaults to single-cycle).

Transition criteria: opposing-side independence has been measured; survival-window calibration done; operator-as-opposing-side instances are *replaceable* by automated instances on at least one artifact-kind; board-visibility apparatus has produced its first quarterly report.

## §7 Open questions

1. **Independence is measured, not declared — what if the measurement itself colludes?** Candidate mitigation: the auditor must be deterministic where possible; LLM-shaped audits require cross-family auditor-of-the-auditor. The corpus does not name a "recursion-stopping" rule.

2. **FC-graph cost at high parallelism.** Per-artifact-kind opposing-side stacks combined with CaMeL utility tax and cross-family judging is corpus-unmeasured at Stripe scale.

3. **Survival-window calibration.** Corpus thin.

4. **Opposing-side gaming (F47 Goodhart).**

5. **Operator-as-opposing-side scalability.** F42 acknowledged at methodology layer; the operator's review FCs are themselves subject to F53 if voluntary.

6. **F58 (runtime/design-time compliance split) at the FC layer.**

7. **Methodology-layer treatment of the Kahana phenomenon.** The track explicitly declines to promote interval-as-substrate. A methodology built on this substrate may *still* find that attention-surface design is load-bearing; whether that absent substrate-promotion is sufficient is the blind-axis-test answer.

## Honest assessment

**Adversarial-falsification topology IS a defensible alternative.** It is corpus-grounded (F1/F27/F46/F48 cascade; CJ Hess `kevin/carl`; Anthropic Auto-Review; Tournament; Husain/Shankar; Attractor do-not-unify; CaMeL; D-4 holdout). It is mandate-symmetric. It addresses F53 structurally via a different mechanism than escrow.

**Honest concession.** The track does *not* close F42 at the substrate layer. The operator-as-opposing-side cold-start regime and the methodology-layer attention-surface design needed to keep operator review FCs from collapsing under F53 are areas where the escrow-interval substrate primitive (in unified-A/B/C) is *stronger*.

**Two things both could be true.** The corpus contains *two* organising signals that span both mandates: (a) the cross-family / opposing-side cluster (anchored on F1/F27/F46/F48, multiple corpus voices, no single primary source); (b) the interval / attention-surface cluster (anchored on Kahana, secondarily on Schillace's Attention Firewall, Anthropic's Sensitive-Action gates, AILCCP fourth-question). The required-reading list for cold-start over-weights cluster (b).

**Recommendation:** treat the unified-track set as needing *both* an escrow-flavoured architecture and an opposing-side-flavoured architecture in the v3 final set, not one chosen over the other — the corpus supplies signal for both, and the D2 mandate-fit matrix is the right surface for picking per-work-unit-class.
