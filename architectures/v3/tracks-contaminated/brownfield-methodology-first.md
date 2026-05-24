---
based-on-commit: 9a205b6
based-on-date: 2026-05-24
track: brownfield-methodology-first
axis: methodology-first
mandate-scope: brownfield
---

# Brownfield, methodology-first

> A Phase-2 architecture-track output for the v3 software-factory synthesis. Strong on the **methodology-first** axis, scoped to the **brownfield mandate**. One of nine concurrent Phase-2 tracks (per [`decisions-captured`](../decisions-captured.md) D1). Does not resolve cross-mandate questions; does not merge with other tracks. Anticipates Phase-3 adversarial review.

---

## §0. Vocabulary, scope, and a pre-response to the "v2 inheritance" objection

### 0.1 Track-local vocabulary

The brief's [`glossary §0`](../00-brief-v3.md) is authoritative; only the OQ-B4 work-unit options need restating here because the axis turns on which one is load-bearing:

- **Atelier-style work unit** — an *issue* drawn from a queue. The cycle starts with a pre-existing issue artifact (bug report, feature request, PR comment, triaged ticket, or production-trace anomaly) and ends at a merged PR. Corpus anchor: Every Inc.'s Compound Engineering (report [`03`](../../../research/03-every-compound-engineering.md); per [`miscategorization-audit`](../bias-guards/phase-1/miscategorization-audit.md) CHALLENGE-6, now `brownfield-primary`).
- **Refinery-style work unit** — a *change request against a layered spec*. The cycle starts with a delta proposal against a versioned spec object and ends at a merged PR + updated spec. Corpus anchor: El Kaim's typed `ArchitectureSpecification` + `derivedFrom: DecisionRecord` chain (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)); Nystrom's `agent specs/` Markdown with spec-git-history-as-changelog (report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)).
- **Codebase-evolution proposal** — the work-unit shape not in the archived v2 set. The cycle starts with a *system-level invariant* (an architectural rule, a Brier pace-layer constraint, a performance budget, a security posture) and produces N derived issues plus the PRs that satisfy them. The unit is the *proposal*, not any single PR. Corpus anchor: Brier's pace-layered ARCHITECTURE.md (followup [`12`](../../../research/followup/12-brier-pace-layers.md)) + Gas Town's `hq-*` organisational beads vs `<rig>-*` implementation beads (followup [`14`](../../../research/followup/14-gas-town-deep-dive.md)).

Two additional terms used heavily below:

- **Cycle** — the methodology's atomic unit: one work-unit through one full traversal of the gate structure ending in either a merged PR, a rejected/closed unit, or a documented quarantine. This track's design centre.
- **Gate** — a substrate-enforced (per F53 voluntary-discipline-fragility avoidance) decision point in the cycle where a typed object must satisfy a deterministic predicate before the cycle proceeds.

### 0.2 Pre-response to the "you're inheriting Atelier vs Refinery" objection

The Phase-3 adversarial critic will say: *"You've inherited v2's Atelier/Refinery framing — both archived for good reasons per UC6 — and dressed it up. Show this isn't reframing."*

This track does not pick Atelier or Refinery. The chosen work-unit shape is the **codebase-evolution proposal** (the OQ-B4 option *not* in the v2 set), with **Atelier-style issue queues as one of its downstream artifacts** (cycles per issue) and **Refinery-style spec deltas as another** (when the proposal crosses a pace-layer boundary). The architecture this track proposes is a methodology in which Atelier and Refinery are not architectures but *work-unit specialisations dispatched by a higher-level proposal cycle.*

The defence that this is not v2-reframing rests on five brownfield-shaped failure modes that the methodology starts from rather than retrofits to. The Atelier and Refinery v2 architectures **did not start from these**; they each picked a single work-unit shape and inherited the failures of that choice:

| Failure mode | What it forces on the methodology | Why v2 Atelier or v2 Refinery alone cannot start from this |
|---|---|---|
| **F30** (liability vacuum, brownfield = **critical** per [`failure-modes-v3`](../failure-modes-v3.md) §2 + bias-guard S2.1) | The cycle must produce a *declared classification* per work-unit before the cycle is dispatched: stakes, RSI status, regulatory exposure, blast-radius. Without this, no downstream gate can be sized. | Atelier's "issue from a queue" assumes the queue itself encodes classification — but production issue queues (Jira / GitHub) do not carry RSI / Caremark fields. Refinery assumes the spec carries them, but Nystrom's `agent specs/` (report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) demonstrably do not. |
| **F33** (adversarial-prompt defeat of LLM judges, brownfield = **critical**) | The cycle's gates cannot be LLM-judge-only. Each gate must compose at least one deterministic predicate with at most one probabilistic judge — and the probabilistic judge's verdict is never load-bearing alone. | Atelier's review-panel pattern (report [`03`](../../../research/03-every-compound-engineering.md)) is multiple LLM judges; Refinery's spec-vs-implementation conformance check is naturally LLM-judged. Both push F33 to the operator. |
| **F34** (cross-layer drift, brownfield = **critical**) | The cycle must check, before merge, whether the proposed change crosses a Brier pace-layer boundary (code → plan → spec → architecture → standards). If it does, the cycle escalates from issue-shape to proposal-shape. | Atelier dispatches issues as if all are at the same layer; Refinery treats spec-as-uniform without pace-layer differentiation. Brier's framework (followup [`12`](../../../research/followup/12-brier-pace-layers.md)) is *the* corpus voice that names this and is the corpus' explicit factory-counter-metaphor. |
| **F44** (lethal-trifecta production-scissors default, brownfield = **critical**) + **F56** (guardrail-bypass under stress, brownfield = **critical**) | The cycle's perimeter is substrate-default-off, not operator-discipline. Production-mutating tools are only enabled per declared classification, and only after the deterministic-gate predicates pass. Instruction-shaped guardrails ("do not deploy") are *not* trusted (F56's Replit anchor). | Both v2 architectures bolt security on as an out-of-loop concern. F44/F56 require the cycle structure itself to encode permission as a typed gate-emitted artifact. |
| **F60** (parallel-cycle compounding error, brownfield = **high**) + **F35** (federation-as-family drift, brownfield = **high**) | The methodology must own the *parallelism budget* per layer of the proposal. The aggregate-error formula `1−(1−p)ⁿ` (Overstory STEELMAN risk 1, [`10`](../../../research/10-overstory-substrate-audit.md) §9) is a methodology constraint, not a substrate setting. Family-drift requires periodic derivation-rule checks against the spec graph. | Atelier scales by adding queue consumers without parallelism awareness; Refinery's phase-gating treats parallelism as orthogonal. Neither has a methodology-layer aggregate-error model. |

These five are the brownfield-mandate-critical or brownfield-mandate-high failure modes the v2 architectures handled at the substrate or operator layer. The proposal of this track is that **the brownfield methodology owns them inside the cycle**, because the substrate cannot know which work units cross which pace-layer, which RSI threshold, or which blast-radius classification.

This is the load-bearing test of whether the track has earned its methodology-first axis: §1 must show the cycle starts from these failure modes, not from "issue → PR" or "spec → PR."

---

## §1. Methodology axis: the cycle is the architecture

### 1.1 Why methodology is load-bearing for brownfield (and what that *means*)

A brownfield factory's substrate is largely **inherited**: the codebase, tests, CI, deployment pipeline, secret store, observability, issue tracker, and review tooling already exist. The substrate-investment thesis Round-2 endorsed ([archived `13-round-2-synthesis`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §8: *"configure a methodology on top of an existing substrate"*) is most cleanly true for **greenfield**, where the operator picks the substrate. For brownfield, the substrate is mostly given; the **decision variable is the methodology that walks work units through that substrate without compounding defects**.

The methodology-first claim, then, is precise:

> **For brownfield, the architecture is the cycle that consumes a codebase-evolution proposal, dispatches it as one or more typed work units, walks each through a gate structure of deterministic-plus-bounded-probabilistic checks, and emits artifacts that compound knowledge without becoming F8-stale or F55-self-referential.**

The substrate's job is to *make the cycle expressible and enforceable*. The substrate is not the architecture; it is the *enabling layer for the architecture*. This inverts the Round-2 framing for brownfield specifically.

### 1.2 The cycle (canonical shape, single-iteration view)

```
PROPOSAL (typed object) → CLASSIFICATION GATE → DECOMPOSITION → DISPATCH → 
[per work unit:] INTENT GATE → BUILD → REVIEW GATE → MERGE GATE → COMPOUND → 
PROPOSAL CLOSE / RE-DISPATCH
```

The cycle is described as eight stages. The four gates (CLASSIFICATION, INTENT, REVIEW, MERGE) are substrate-enforced (per F53); the four non-gate stages (DECOMPOSITION, DISPATCH, BUILD, COMPOUND) are agent-executed under operator-defined policy.

**Stage 1 — PROPOSAL (typed object).** Every cycle starts from a typed proposal object with five required fields:

| Field | Type | Rationale (corpus anchor) |
|---|---|---|
| `intent` | El Kaim 9-field intent block (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3) | Defeats F41 (under-defined intent debt); CTR-B6's MISSED-3 warns the El Kaim intent block is the spec-malleability counter-anchor — for brownfield this is the *prerequisite*, not a contradiction. |
| `invariants` | Brier pace-layer references (followup [`12`](../../../research/followup/12-brier-pace-layers.md)) | What pace-layers the proposal touches; defeats F34 silent layer crossing. |
| `classification` | `{stakes, RSI-status, regulatory-exposure, blast-radius}` per Kahana ([`31`](../../../research/31-caremark-rsi-board-exposure.md)) + AILCCP (followup [`10`](../../../research/followup/10-governance.md)) | Defeats F30, F43, F57 (design-authority erosion). |
| `parallelism-budget` | Integer N per work-unit class | Defeats F60: `N` is set per `(1 − (1−p)ⁿ) ≤ threshold` for the work-unit's measured error rate. |
| `out-of-distribution-anchor` | Pointer to existing tests / production traces / runtime telemetry that constrains the proposal | Defeats F1/F27 by giving the cycle an OOD signal *the LLM judges cannot manufacture*. |

The proposal object's source is *not constrained* — it may be human-authored (the typical case for high-classification proposals), agent-drafted (Compound Engineering–style Cora workflow, report [`03`](../../../research/03-every-compound-engineering.md)), or auto-promoted from an issue queue (when an issue's classification is high enough to require a wrapping proposal). The corpus' three native work-unit sources (issue queue / spec delta / proposal) thus all *enter* the cycle as Stage-1 proposals.

**Stage 2 — CLASSIFICATION GATE (substrate-enforced).** A deterministic predicate checks that all five Stage-1 fields are present and well-typed. The probabilistic component (an LLM judge cross-checking `classification` against `intent`) is advisory and cannot block alone. This gate's purpose is to **prevent F30/F43 unclassified work** from entering the cycle. Failure rejects to the proposer with a structured diff naming the missing field — *not* a free-form chat response (F10 mitigation).

**Stage 3 — DECOMPOSITION.** Per the proposal's `invariants`, the proposal is decomposed into one or more typed work units:

- If the proposal touches only the *code* pace-layer with `stakes=low`, decomposition emits a single **Atelier-style issue unit** (one issue → one PR).
- If the proposal modifies a spec (Brier layer 3), decomposition emits a **Refinery-style spec-delta unit** plus zero-or-more Atelier issue units derived from the delta.
- If the proposal modifies architecture or standards (Brier layers 4–5), decomposition emits a **codebase-evolution sub-proposal** that itself re-enters Stage 1 at a higher classification tier (recursive escalation), plus the Atelier/Refinery units necessary to land the constituent code changes.

The Atelier vs Refinery v2 architectures are thus **work-unit specialisations**, not architectures. Decomposition is the methodology's typed dispatch.

**Per-work-unit Stages 4–7 (DISPATCH → BUILD → REVIEW GATE → MERGE GATE)** are the inner loop. Each unit carries the proposal's `parallelism-budget` slice (Overstory aggregate-error formula per F60) and the proposal's `classification` (which gates have which strictness).

**Stage 4 — DISPATCH.** Units fan out to agents per `parallelism-budget`. The substrate guarantees worktree isolation (F17) and that no agent has tools above the unit's `classification` permits (F44 default-off; F56 stress-bypass mitigation by *capability removal* rather than *instruction-shaped restriction*).

**Stage 5 — BUILD.** Per-unit agent activity. The methodology does not constrain the agent's internal loop; this is a substrate concern. The methodology *does* require that BUILD emits typed trajectory events (the OpenHands sub-ms persist model, [`11`](../../../research/11-openhands-substrate-audit.md)) and that BUILD respects the per-unit cost ceiling (D-5).

**Stage 6 — REVIEW GATE.** Composed of three predicates per F33-mitigation discipline:

- **Deterministic-perimeter predicate** — type-check, compile, test, lint, security-scan, contract-check against the proposal's `out-of-distribution-anchor`. Load-bearing.
- **Bounded-probabilistic predicate (single, mandate-task-different)** — one LLM-as-judge call with a binary pass/fail per Anthropic's evals discipline (followup [`07`](../../../research/followup/07-evals-deepdive.md) §3.6, *"a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements"*; CTR-D7 / MISSED-1). Advisory unless the operator-policy has explicitly weighted this gate.
- **Holdout predicate** — the proposal's `out-of-distribution-anchor` must pass; the *acceptance criteria* derived from `intent` must be applied by an agent that has not seen them (D-4 holdout discipline, substrate-enforced; F28 mitigation).

This composition addresses CTR-D4/D7/D8: the methodology does not pick a side in the same-model-vs-cross-model debate. It picks the **deterministic predicate as load-bearing and the LLM judge as advisory-only-by-default**. The cycle does not depend on judge-diversity being the right answer to F1/F27. (Anticipates Phase-3 adversarial: "you skipped the question." Response: the methodology declines to make the question load-bearing.)

**Stage 7 — MERGE GATE.** Deterministic predicate only: deterministic-perimeter passed, holdout passed, parallelism-budget not exceeded (F60), pace-layer-crossing matches `invariants` declaration (F34). On pass, the unit's PR merges via a Bors-style queue (followup [`14`](../../../research/followup/14-gas-town-deep-dive.md) Refinery pattern). On fail, the unit either re-enters DISPATCH with the failure as input, or escalates to the proposal level.

**Stage 8 — COMPOUND.** Per-unit and per-proposal emit typed knowledge artifacts (the Compound Knowledge plugin's four-way classification: `insight` / `playbook` / `correction` / `pattern` per followup [`11`](../../../research/followup/11-compound-knowledge.md)) with `kw:confidence` first-class. Critically, compound is *gated*: a knowledge artifact only enters the durable knowledge store if (a) the proposal merged, (b) its OOD anchor still validates, and (c) it survives a staleness check against artifacts written more than N cycles ago (F8 mitigation). See §3 for the knowledge accumulation design.

### 1.3 The cycle answers the brief's required questions

- **Which work-unit shape is load-bearing?** The codebase-evolution proposal (the non-v2 OQ-B4 option). Atelier and Refinery shapes are *typed downstream specialisations* the proposal dispatches.
- **What is the gate structure that prevents F60 parallel-cycle compounding?** The proposal's `parallelism-budget` field, sized per `(1 − (1−p)ⁿ) ≤ threshold` per work-unit class, substrate-enforced at DISPATCH. F60 is owned at proposal level, not per cycle.
- **What is the gate structure that prevents F7 normalisation of deviance?** The acceptance threshold for any cycle is *the proposal's `out-of-distribution-anchor`* — an artifact the cycle did not write. The cycle cannot relax its own acceptance bar (CTR-D6 sycophancy paradox avoided by structural separation, not by prompt discipline).
- **How does knowledge accumulate without F8 stale-knowledge inversion?** Compound is gated; staleness check is mandatory; the durable store carries `kw:confidence` per typed artifact. See §3.
- **How does this not depend on operator voluntary discipline (F53)?** Every gate is substrate-enforced; the operator authors the *policy* (thresholds, classifications) at upstream time, not the gate-pass action at cycle time. See §4.4.

---

## §2. The five brownfield-critical failure modes, in cycle terms

This section maps the brownfield-critical and brownfield-high failure modes the bias guard flagged onto specific cycle stages. The mapping is the test of whether the methodology genuinely starts from these failures.

### 2.1 F30 (liability vacuum) — owned at Stage 2

CLASSIFICATION GATE's deterministic predicate forces `classification = {stakes, RSI-status, regulatory-exposure, blast-radius}` to be present and well-typed. The cycle cannot begin without it. The proposal's classification is itself a board-visibility artifact (F43 mitigation): an immutable record naming who declared which class. Anchors: Kahana ([`31`](../../../research/31-caremark-rsi-board-exposure.md)); AILCCP missing-fourth-question (report [`30`](../../../research/30-cognitive-escrow.md) §5 + followup [`10`](../../../research/followup/10-governance.md)).

### 2.2 F33 (adversarial-prompt defeat) — owned at Stage 6

REVIEW GATE's composition rule — *deterministic load-bearing + at most one bounded probabilistic, advisory-by-default* — directly answers the F33 cascade (F12 → F33 → F44). The LLM-judge defeat scenario is structurally non-decisive because the LLM judge cannot block alone. Anchor: [`failure-modes-v3`](../failure-modes-v3.md) §2 F33; followup [`08`](../../../research/followup/08-security-primitives.md) CaMeL discussion.

### 2.3 F34 (cross-layer drift) — owned at Stages 1 and 7

Stage 1's `invariants` field forces the proposer to declare which pace-layers the proposal touches; Stage 7's MERGE GATE re-checks the declaration. A diff that silently modifies a layer above the declared scope fails MERGE. Anchor: Brier (followup [`12`](../../../research/followup/12-brier-pace-layers.md)).

### 2.4 F44 + F56 (lethal trifecta + guardrail bypass) — owned at Stage 4

DISPATCH is the substrate's permission-emission point. Production-mutating capability is a typed artifact the cycle *emits*, gated by `classification`. The agent at BUILD never has more capability than its dispatch token grants; F56 (Replit-class stress bypass) cannot occur because the *capability is not present at the boundary*, not because the agent was instructed not to use it. Anchors: Shapiro Claw R3 *"do not give it production scissors"* (report [`32`](../../../research/32-shapiro-completion-chat-agent-claw.md) §8.2); F44 in [`failure-modes-v3`](../failure-modes-v3.md) §5; F56 in §5a.

### 2.5 F60 + F35 (parallel compounding + federation drift) — owned at Stages 1, 4, and 8

Stage 1's `parallelism-budget` is the per-proposal aggregate-error envelope. Stage 4's DISPATCH enforces it. Stage 8's COMPOUND staleness check periodically re-derives the family's derivation rules against current proposals (F35 mitigation: the family stays *executable*, not just claimed). Anchor: Overstory STEELMAN risk 1 ([`10`](../../../research/10-overstory-substrate-audit.md) §9); El Kaim Ch 9 family-drift (report [`24`](../../../research/24-el-kaim-book-product-line-variability.md)).

### 2.6 F52 (tempting-wrong-hybrid) — the meta-failure-mode the methodology has to dodge

Schillace's Letter 11 ([`28`](../../../research/28-schillace-sunday-letters.md) §6): *"a desire to 'go back to' the syntactic and deterministic world ... wrap a lot of code around an LLM in a subconscious attempt to get away from that uncomfortable randomness."* This track is at maximum risk of F52: the cycle is built on substrate-enforced gates and deterministic predicates. The defence is structural, not stylistic:

The methodology distinguishes **gates** (deterministic predicates on typed objects produced by stochastic agents — these are the "foreman's clipboard" Schillace endorses, *meta-cognitive code*) from **the agent's internal loop** (which is left unconstrained, semantic, stochastic — Schillace's *cauldron*). The cycle does not wrap the model; it wraps the *artifacts the model emits*. This is the "Decide clearly what belongs inside the model and what belongs in code" instruction Schillace gives at the bottom of his diagram. F52 indicts wrapping the model; this track wraps the model's typed outputs. The line is the F52 falsification test, and Phase-3 adversarial review must hold the track to it.

---

## §3. Knowledge accumulation without F8 / F55 inversion

The Compound Engineering and Compound Knowledge primitives (reports [`03`](../../../research/03-every-compound-engineering.md), followup [`11`](../../../research/followup/11-compound-knowledge.md)) are brownfield-native (per [`miscategorization-audit`](../bias-guards/phase-1/miscategorization-audit.md) CHALLENGE-6/7). They are also at maximum risk of F8 (stale-knowledge inversion) and F55 (behavioural drift via self-reference) — the two corpus-promoted failure modes that target knowledge accumulation directly.

The track's design for knowledge accumulation:

1. **Typed at write.** Every artifact carries the CK four-way classification (`insight` / `playbook` / `correction` / `pattern`) plus `kw:confidence` plus a pointer to the proposal that produced it. No untyped writes.
2. **Gated at write.** Stage 8 COMPOUND only writes if the proposal merged AND the OOD anchor still validates AND the staleness check passes. F10 (findings-disappear-into-chat) is mitigated; F8 inversion is mitigated.
3. **Staleness-checked at read.** Any read of the knowledge store by a cycle agent triggers a confidence-check against the artifact's age and the cited code's current state (CK's inline `kw:confidence` model, followup [`11`](../../../research/followup/11-compound-knowledge.md), vs CE's separate `ce-compound-refresh` cadence — the inline model is F8-stricter).
4. **OOD-anchored at compound.** F55 (behavioural drift / self-reference loop) is the corpus' sharpest critique of compounding. The mitigation: every COMPOUND must cite an *out-of-distribution anchor* (existing test, production trace, human review, prior PR review of a different proposal). An artifact whose only justification is *another agent-emitted artifact* does not enter the durable store. This is the F55 firewall.
5. **Family-rule check at periodic intervals.** F35 (federation-as-family drift) is addressed by a substrate-scheduled re-derivation: every N cycles or M days, the knowledge store's family of typed objects is checked against an executable derivation rule (El Kaim's `derivedFrom: DecisionRecord` chain, report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)). Drift is named explicitly; resolution is itself a proposal.

The substrate primitive that makes this expressible: a **typed knowledge-store with first-class typed nodes and edges** — most cleanly satisfied by Gas City's Beads `discovered-from` edge (report [`38`](../../../research/38-gas-systems-substrate.md) §3, *"strictly more expressive than Compound Atelier's flat-file `docs/solutions/`"*) — but the methodology does not require Gas City. Any substrate that can store typed nodes with typed edges and run executable derivation rules will do. (See §6 for the substrate sketch.)

---

## §4. §4 defaults (per D3): accepted vs challenged

Per D3, each of the seven Round-1/Round-2 defaults must be marked. This track's markings:

| Default | Marking | Justification |
|---|---|---|
| **D-1** Specs are durable, version-controlled, human-curated | **accepted with justification** | The proposal object's `intent` field is durable and version-controlled. For brownfield the spec is *layered* (Brier) — code, plans, specs, architecture, standards — not a single artifact. The "spec" D-1 refers to is the union of Brier layers 3–5. Anchor: Nystrom's `agent specs/` checked into the repo ([`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)). |
| **D-2** Scenarios live outside the codebase as a holdout set | **challenged** | Brownfield's `out-of-distribution-anchor` lives *inside* the codebase: existing tests, production traces, runtime telemetry, prior PR reviews. The fragility-flag in brief §4.1 is correct: brownfield inverts D-2. Per [`uncomfortable-contradictions-audit`](../bias-guards/phase-1/uncomfortable-contradictions-audit.md) WEAK-3, even StrongDM's own primary pages (*"incident replays, agentic simulation"*) permit scenarios inside the running system. D-2 should be re-stated as *"scenarios live where they can be held out from the builder"* — substrate enforcement of holdout (D-4) is load-bearing; their *location* is mandate-conditional. |
| **D-3** Agent = Model + Harness | **challenged** | Per CTR-C10 (MISSED-8): report [`37`](../../../research/37-academic-llm-agent-collusion.md)'s Portuguese-vs-English finding empirically shows *natural-language-of-prompt* shifts agent policy. The vocabulary needs to be at least *Agent = Model + Harness + Natural-Language-Register*; for the brownfield cycle, the prompt's language is a methodology parameter (the cycle's natural-language-register is fixed per proposal classification, English by default unless the codebase's documentation language differs). |
| **D-4** Holdout discipline is substrate-enforced | **accepted with justification** | Stage 6's holdout predicate is substrate-enforced exactly as D-4 prescribes. Per F53, this is one of the few defaults that is correctly placed at substrate. |
| **D-5** Hard cost ceilings non-optional in CI | **accepted with justification** | The proposal's `parallelism-budget` is the cycle-level cost envelope; the substrate enforces a per-cycle cap. The CTR-E1 ($100K/mo vs $500/day) range is itself a *classification* concern — high-classification proposals run at higher budgets, declared. |
| **D-6** Tiered watchdog (Daemon / Triage / Patrol) is substrate primitive | **accepted with justification** | The cycle assumes the Daemon/Triage/Patrol substrate (F22/F23 mitigation). Stage 5 BUILD's zombie-agent detection depends on it. |
| **D-7** Trajectory capture is cheap and production-tested | **accepted with justification** | The cycle's typed-event emission at every stage assumes OpenHands-class sub-ms persist ([`11`](../../../research/11-openhands-substrate-audit.md)). Without it, COMPOUND staleness checks are not affordable. |

**Two challenged defaults: D-2 (scenarios location) and D-3 (Agent = Model + Harness vocabulary).** Per D3, each surfaces as DECISIONS-PENDING for Phase 3.

### 4.4 The F53 (voluntary-discipline-fragility) discipline test

Per the brief, this track must show its mitigations do not depend on operator voluntary discipline at cycle time. The eight cycle stages:

| Stage | Operator action at *cycle* time? | Operator action at *upstream* (policy) time? |
|---|---|---|
| 1 PROPOSAL | Sometimes (high-classification) | Always (defines classification taxonomy, intent-block schema) |
| 2 CLASSIFICATION GATE | Never (substrate-enforced) | Yes (defines required fields, declares regime per [Jaymin §5.5 thresholds OR alternate]) |
| 3 DECOMPOSITION | Never | Yes (defines dispatch rules per `invariants`) |
| 4 DISPATCH | Never | Yes (defines capability tokens per `classification`) |
| 5 BUILD | Never (lights-out) | Yes (defines agent loop substrate, cost ceilings) |
| 6 REVIEW GATE | Never (substrate-enforced) | Yes (defines deterministic predicates, judge prompts) |
| 7 MERGE GATE | Never (substrate-enforced) | Yes (defines merge-queue policy) |
| 8 COMPOUND | Never (substrate-enforced staleness check) | Yes (defines knowledge schema, staleness thresholds) |

No cycle-time stage depends on voluntary operator action. F53 is mitigated by **moving operator action upstream of cycle time** — the operator defines policy at proposal-batch time; the substrate enforces it at cycle time. The substrate enforcement is the F53 defence, *not* the operator's vigilance.

---

## §5. Cold-start

**Treated as warm-start / first-codebase-encounter.** Per the brief §5 instruction, this section is optional for brownfield tracks; the brownfield "cold-start" analogue is the *first encounter with a previously-untouched codebase*. Brief treatment:

The methodology requires no `docs/solutions/`-style accumulated knowledge to begin. The first proposal against a new codebase declares its `out-of-distribution-anchor` as *the existing tests + production telemetry* (which the codebase always has by brownfield definition). The first cycle's Stage 8 COMPOUND writes the first artifact to a previously-empty knowledge store. The cycle structure is identical from cycle 1; the difference is the size of the knowledge store the COMPOUND staleness-check reads from. This is the brownfield analogue of greenfield cold-start, but it is *not* the same problem — brownfield's codebase + tests + telemetry are the cold-start substitute the greenfield mandate does not have.

The track does *not* attempt the greenfield cold-start. (Per scope: this is a brownfield track.)

---

## §6. Substrate the methodology requires (under-specified by design, see §7)

This section enumerates what the substrate *must provide* for the methodology to run. It does not specify implementations. (Phase-3 adversarial: "this is hand-waving." Response in §7.)

| Methodology dependency | Substrate primitive required | Corpus exemplar (not normative) |
|---|---|---|
| Typed proposal object with five required fields | Typed-object store with deterministic schema validation | El Kaim typed objects ([`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)); Gas City Beads + Dolt cell-merge (followup [`13`](../../../research/followup/13-gas-city-deep-dive.md)) |
| Deterministic gate predicates at Stages 2/6/7 | Programmable rules engine (Starlark / similar) | Codex `.rules` DSL ([`18`](../../../research/18-openai-codex-substrate.md)) |
| Capability-token emission at Stage 4 | Per-cycle scoped credential issuance | OS-keyring + scoped tokens ([`18`](../../../research/18-openai-codex-substrate.md)); Shapiro Claw R3 default-off ([`32`](../../../research/32-shapiro-completion-chat-agent-claw.md)) |
| Typed trajectory events per stage | Event-sourced sub-ms persistence | OpenHands V1 ([`11`](../../../research/11-openhands-substrate-audit.md)) |
| Typed knowledge store with `discovered-from`-class edges | Typed graph store with executable derivation rules | Gas City Beads (report [`38`](../../../research/38-gas-systems-substrate.md), followup [`13`](../../../research/followup/13-gas-city-deep-dive.md)) |
| Tiered watchdog | Daemon + Triage + Patrol per D-6 | Overstory ([`10`](../../../research/10-overstory-substrate-audit.md)) |
| Parallelism budget enforcement | Worktree isolation + work-stealing queue with per-classification limits | Symphony hard-cap; Bors-style merge queue (followup [`14`](../../../research/followup/14-gas-town-deep-dive.md)) |
| Holdout-enforced acceptance criteria | Substrate role-separation: builder cannot read holdout artifacts | D-4; report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2a |

The substrate the methodology needs is **a typed-object store + a rules engine + a capability-token system + event-sourced trajectories + worktree isolation + Daemon/Triage/Patrol**. Whether this maps onto OpenHands+Overstory, Gas City, Codex-substrate, or a custom build is a substrate-track concern, not a methodology-track concern. The methodology survives substrate substitution if all the dependencies in the table are honoured.

---

## §7. Open questions, anticipated adversarials, decisions-pending

### 7.1 Open questions surfaced by this track

- **OQ-T1.** Where does the proposal-classification taxonomy come from? The track requires the operator define it upstream; Jaymin §5.5 thresholds + AILCCP risk classes are corpus candidates. **Action:** Phase 3 must select or commission a classification schema; the methodology cannot proceed without one. *(Anchor: OQ-B6.)*
- **OQ-T2.** What is the right error-rate `p` for the F60 aggregate-error formula at each work-unit class? Round-1's 5% Overstory anchor is a single data point; the corpus has no per-class measurements. **Action:** Phase 8 lean-eval design must measure per-class `p` against a corpus of historical PRs.
- **OQ-T3.** How does the codebase-evolution proposal cycle interact with *human-authored* proposals that bypass agent decomposition? The cycle's Stage 3 DECOMPOSITION must handle pre-decomposed proposals from humans without losing classification fidelity. **Action:** ADR in Phase 5 specifying the human-decomposed proposal path.
- **OQ-T4.** Does the methodology require a separate "proposal-review" persona before Stage 2? Currently the CLASSIFICATION GATE is purely schema validation; a proposal could be schema-valid but semantically nonsensical. **Action:** Lead-agent call whether to add a substrate-enforced proposal-review stage between 1 and 2; cost is one extra agent invocation per cycle.
- **OQ-T5.** The CTR-A4 lights-out/L5 mapping is *not* resolved by this track. The cycle is lights-out per UC1 at Stages 2-8 for any unit whose `classification` says automation-eligible; high-classification units get Stage-1 human authorship and Stage-2 human classification co-signature. **Action:** Phase 3 unified-mandate-attacker pass must test whether the classification-gates-determine-regime answer is operationally honest, or smuggles human-in-loop back into the inner loop.

### 7.2 Anticipated Phase-3 adversarial critiques (and pre-responses)

- **"You under-specified substrate."** Yes — by design. The methodology-first axis means the substrate primitives are dependencies, not designs. The substrate-first sibling tracks (greenfield-substrate-first, brownfield-substrate-first, both-mandates-substrate-first) are explicitly tasked with the substrate question. If the substrate-first track for brownfield converges on primitives that cannot honour the §6 table, *that* is a load-bearing finding for Phase 4.
- **"The cycle assumes primitives that may not exist."** The §6 table is candid: every dependency has a corpus exemplar, but no single substrate has *all* of them. Gas City has typed knowledge + Beads but no LLM-as-judge primitive (report [`38`](../../../research/38-gas-systems-substrate.md) §3 gap). Codex has `.rules` but no `discovered-from`-edge store. OpenHands has trajectory but no rules DSL. The methodology survives substrate fragmentation if a *composite* substrate is built; whether that composite is feasible is a Phase-4 question.
- **"This is Atelier+Refinery with a wrapper."** Pre-responded in §0.2. The wrapper is the load-bearing artifact, not a wrapper — Atelier and Refinery are downstream specialisations of decomposition, not architectures. The five brownfield-critical failure modes in §0.2's table are the test.
- **"F52 (Tempting-Wrong-Hybrid) is exactly what you've built."** Pre-responded in §2.6. The structural distinction (gate-the-typed-output, not the-model) is the falsification test. If Phase-3 adversarial can show a cycle stage that *wraps the model itself* rather than wrapping a typed artifact, the track fails F52.
- **"The classification taxonomy you require doesn't exist."** Conceded; named as OQ-T1. The methodology cannot run without it, and Phase 3 must source one.
- **"The bias-guard sharpening on D-3 (Agent = Model + Harness + Natural-Language-Register) is a side-show."** Possibly; included because CTR-C10 (MISSED-8) explicitly flags it and the brief instructs subagents to honour bias-guard findings. The methodology's commitment is minimal — the natural-language-register is fixed per proposal, not per cycle — but the declaration matters.

### 7.3 Decisions-pending for user / lead-agent review

| ID | Decision | Next action | Owner |
|---|---|---|---|
| DP-T1 | Adopt or reject the codebase-evolution proposal as the load-bearing work-unit shape | Phase 3 merge step compares this track's choice against brownfield-substrate-first + brownfield-legacy-ingestion-first | Lead agent |
| DP-T2 | Adopt or reject classification taxonomy source (Jaymin / AILCCP / other / commission) | Phase 3 specifies; ADR in Phase 5 | Lead agent + user |
| DP-T3 | Validate the §6 substrate-dependency table against the substrate-first track outputs | Phase 4 shared/divergent extraction | Lead agent |
| DP-T4 | Test the §0.2 five-failure-mode-derivation against the Phase-3 brownfield-synthesis adversarial pass | Phase 3 unified-mandate-attacker + brownfield-attacker | Phase-3 personas |
| DP-T5 | Resolve the D-2 challenge (scenarios location is mandate-conditional) | Phase 3 surfaces as DECISIONS-PENDING per D3 | Lead agent |
| DP-T6 | Resolve the D-3 challenge (Agent vocabulary needs Natural-Language-Register) | Phase 3 surfaces as DECISIONS-PENDING per D3 | Lead agent |

---

## §8. Citations (rolled up)

**Primary methodology-shaping corpus inputs:**
- Report [`03`](../../../research/03-every-compound-engineering.md) — Compound Engineering loop (Plan/Work/Review/Compound); `docs/solutions/`. **Brownfield-primary** per bias-guard CHALLENGE-6.
- Report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) — 9-field intent block; typed `ArchitectureSpecification`; `derivedFrom: DecisionRecord`.
- Report [`22`](../../../research/22-academic-foundations.md) — SWE-Bench Verified Issue + Codebase → PR (brownfield-canonical work-cycle shape per bias-guard CHALLENGE-8).
- Report [`27`](../../../research/27-dotfile-pipelines-as-product.md) — `.dot` as durable methodology artifact.
- Report [`28`](../../../research/28-schillace-sunday-letters.md) §6 — F52 Tempting-Wrong-Hybrid (Letter 11); meta-cognitive-code-not-model-wrapping.
- Report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) — Notion/Boxy spec-driven; spec-git-history-as-changelog; AFIS strategy-3 industrial anchor.
- Followup [`11`](../../../research/followup/11-compound-knowledge.md) — Compound Knowledge typed four-way classification; `kw:confidence`.
- Followup [`12`](../../../research/followup/12-brier-pace-layers.md) — pace-layers (Code/Plans/Specs/Architecture/Standards); F34.

**Failure-mode anchors (per [`failure-modes-v3`](../failure-modes-v3.md)):**
F1, F7, F8, F10, F12, F17, F22, F23, F27, F28, F30 (raised to brownfield-critical per bias-guard S2.1), F33, F34, F35, F41, F43, F44, F46, F52, F53, F55, F56, F57, F60.

**Contradictions engaged (per [`contradictions`](../contradictions.md)):**
CTR-A4 (lights-out/L5 vocabulary), CTR-B5 (scenarios location, D-2 challenge), CTR-B6 (MISSED-3 El Kaim intent vs UC4), CTR-C10 (MISSED-8 D-3 vocabulary), CTR-D4/D7/D8 (judge-independence cluster), CTR-D6 (sycophancy paradox).

**Most-cited CTR / F-mode:** **F34 (cross-layer drift, brownfield = critical)** and the Brier pace-layer framing it rests on — load-bearing for the codebase-evolution-proposal work-unit choice. Runner-up: **F53 (voluntary-discipline-fragility)** — the bias-guard CANDIDATE-2 finding that drove the upstream-operator-action-only design.

*End of brownfield-methodology-first.md.*
