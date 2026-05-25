# Phase 3.4 — Decisions resolved (running)

This file records user decisions made at the Phase-3.4 checkpoint as they are made. Each entry replaces the corresponding `DEC-N` in [`phase-3.4-integration-brief.md`](phase-3.4-integration-brief.md).

---

## Scoping principle (immutable, overrides any conflicting framing in the integration brief)

**Carry forward every candidate methodology / architecture that has defensible supporting arguments and that successfully addressed Phase-3.2 / Phase-3.3 criticism. Do not eliminate at end-of-Phase-3.**

Rationale (user, verbatim paraphrase): no public source has given details of a software-factory architecture/methodology that actually works. Company blogs, white papers, and books are written by authors with incentives to convince; what they describe is not the same as a working factory. Trying to eliminate promising candidates at the end of Phase 3 forecloses *crossover* opportunities where pieces of one candidate turn out to be exactly the missing piece for another. Pressure-testing against each other in simulation or mock-up of the final solution is the appropriate evaluation surface — Phase 8's lean evaluations, plus downstream simulation work, do this. The objective is "however many candidates can pass review and pressure-testing make a strong case for being evaluated," not "narrow to 1–3."

**Effect on the rest of the synthesis pipeline:** see "How this changes prior and future work" below.

---

## DEC-2 — Cognitive escrow placement: **METHODOLOGY**

The cognitive-escrow surface (substrate-triggered reflection prompts, success-criterion articulation, similar-past surfacing, STIR-cascade reflection) is a **methodology-layer pattern**, not a substrate primitive.

Rationale: substrate support for cognitive escrow is nice-to-have but composable from basic cloud-native primitives (trajectory capture, watchdog, alerting, event sinks). Substrate-typing is overkill for something that any methodology can compose from primitives the substrate already provides for other purposes.

**Effect:**
- `ROBUST-G14` in [`draft-greenfield-synthesis.md`](draft-greenfield-synthesis.md) and `ROBUST-U10` in [`draft-unified-synthesis.md`](draft-unified-synthesis.md) demote from substrate primitives to methodology-layer recommendations.
- Phase-5 wave-1 ADR scope drops the "`EscrowSurface` substrate-primitive schema" candidate. A methodology-pattern ADR may still exist, but it's per-architecture (not in shared substrate).
- Architecture specs in Phase 6 do not declare an `EscrowSurface` substrate slot. Each architecture that wants the discipline composes it from trajectory + watchdog + alerting primitives.
- F42 / F53 mitigation depth is now methodology-dependent. Each surviving candidate (per scoping principle) must articulate its own answer.

---

## DEC-3 — Greenfield methodology shape: **CARRY ALL DEFENSIBLE CANDIDATES**

Carry GF-C (Bootstrap-Bench), GF-M (two-regime spec-discovery → spec-anchored execution), and GF-S (substrate-thin) all forward into Phase 4 and beyond. Each has powerful aspects; each defended itself against Phase-3.2 / Phase-3.3 critique. Eliminating any of them at Phase 3 is exactly the move the scoping principle prohibits.

Combinations (e.g., GF-C bootstrap + GF-M steady-state on a GF-S substrate stack) are also valid as additional candidates if they have substantive distinguishing arguments.

**Effect:**
- Phase 4 substrate / divergence extraction produces a substrate-requirements summary *per surviving candidate*. The "shared substrate" extraction is reframed as "primitive overlap analysis" — useful for downstream tooling decisions, not as a winner-picking exercise.
- Phase 5 ADRs are scoped *per candidate*. Common ADRs (where the methodologies agree on a substrate primitive) get drafted once and cross-referenced.
- Phase 6 produces *one architecture spec per candidate*. The mandate-fit matrix has a row per candidate.
- Phase 8 lean-eval briefs are *per candidate*. This is where pressure-testing per the scoping principle happens.

---

## DEC-4 — Brownfield methodology shape: **CARRY ALL DEFENSIBLE CANDIDATES**

Carry BF-L (3-loop over CodebaseModel), BF-M (8-stage cycle-as-architecture), and BF-S (substrate-continuous-thin-methodology) all forward. Same rationale as DEC-3.

Combinations (e.g., BF-L's CodebaseModel as substrate, with BF-M's 8-stage cycle as the methodology that queries it) are valid additional candidates.

**Effect:** symmetric to DEC-3 on the brownfield side.

---

## DEC-1 — UNRESOLVED (user to address next)

See [`dec-1-unification-verdict.md`](decisions/dec-1-unification-verdict.md). Note that under the scoping principle, the unification verdict question reframes: instead of "pick one of A/B/C/D," it becomes "which of the unified candidates (from the three unified-mandate Phase-2 tracks plus D7-U-1's Adversarial-Falsification Topology alternative) defended themselves successfully and should carry forward alongside the mandate-specific candidates from DEC-3 / DEC-4?"

---

## Cross-cutting orientation: methodology drives; substrate requirements fall out

The user named a broader concern (paraphrase): the synthesis should be trying to find **methodologies**, not substrates. Methodologies should *issue requirements* for a substrate. Substrate requirements, if sufficiently detailed, will likely be implementable on any cloud platform.

**Recorded as orientation, with one substantive caveat:**

This reorientation is correct for the bulk of substrate primitives — sandbox, trajectory capture, cost ceilings, watchdog tiers, coordination medium, perimeter closure, event sinks, alerting — these are cloud-engineering-once-specified.

**Caveat:** some primitives the corpus called "substrate" are not commodity infrastructure and should not be dismissed as such. The clearest example is `CodebaseModel` (the brownfield-side queryable artifact with five sub-stores — symbol index, dependency-and-impact graph with blast-radius compute, runtime/telemetry view with role-based partitioning, change-history-with-symbol-level-attribution, invariant/debt view). For a polyglot codebase that has been through acquisitions, this is a knowledge-graph / code-analysis system in its own right. If a methodology "issues a requirement" for `CodebaseModel`, that requirement is "we need a tool that does X" rather than "we need a 3-line Terraform module" — and *the choice of what X is* is methodology-load-bearing.

Similar caveats apply, in milder form, to: cross-family judge routing with TPR/TNR-aligned evaluations; per-cycle holdout enforcement with role-partitioned views; AILCCP-grade immutable attribution at industrial scale.

**Refined orientation:** methodologies drive; substrate requirements fall out per methodology; *but* when a methodology requires a primitive that is itself a designed system (not a configuration), name the primitive explicitly and don't pretend it's commodity. Most Phase-4/5 work survives the reframe by changing framing (from "pick shared substrate" to "what does each methodology require of infrastructure?"); some substrate primitives that are themselves designed systems get their own ADRs.

---

## How this changes prior and future work

### Prior work (Phase 1–3.3 outputs)

- **Phase 1 outputs survive** unchanged: contradictions register, failure-mode catalog, corpus inventory are inputs to all candidates.
- **Phase 2 tracks survive** unchanged: 9 tracks remain in the corpus as candidate seeds.
- **Phase 3.1 drafts** (three pre-adversarial syntheses) survive as the merged-by-axis summaries. Their ROBUST/DECISIONS-PENDING markings remain useful for understanding cross-track convergence/divergence within each axis.
- **Phase 3.2 critiques** (18 persona-adversarial + 2 D7 blind-axis) reframe purpose: previously each critique was material for "should this draft demote?" Under the scoping principle, each critique is material for *"what must this candidate address before it carries forward?"* — critiques become improvement requirements, not elimination grounds. Any draft whose critique findings have been addressed (or whose authors have given a substantive defense) carries forward.
- **Phase 3.3 cross-mandate tests** reframe similarly: the "unify advocate" and "cannot-unify attacker" pair is no longer a winner-picker. Both verdicts can be true at once — unified candidates *and* mandate-specific candidates can coexist. The "unified-fails-mandate-X" attackers identify concerns each unified candidate must address.
- **D7 blind-axis tests** produced an alternative unified axis (Adversarial-Falsification Topology). Under the scoping principle, this becomes a fourth unified-candidate alongside U-A/U-B/U-C, not a challenger to them.

### Future work

- **Phase 4** reframes from "shared/divergent extraction over surviving syntheses" to "substrate-requirements extraction per surviving candidate, with primitive-overlap analysis as a side artifact." Still useful, but no longer a winner-picking step.
- **Phase 5** ADR count grows substantially. ADRs are per-candidate where the methodology specifies; common ADRs (for primitives the candidates agree on) get drafted once and cross-referenced.
- **Phase 6** produces an architecture spec per candidate. The mandate-fit matrix has one row per candidate (could be many rows).
- **Phase 7** back-fill audit runs per candidate against archived v1/v2 material.
- **Phase 8** lean-eval briefs are per candidate; this is the first pressure-testing surface where candidates begin to differentiate empirically.

### Downstream of the methodology

Outside the 8-phase synthesis pipeline, the user's plan includes simulation / mock-up evaluation of candidates against each other. This is *post-v3* and not in the current methodology, but the scoping principle is designed to keep candidates alive for that evaluation. The Phase-8 lean-eval briefs become inputs to whatever simulation harness the project builds.

---

## Audit trail

- Scoping principle: declared 2026-05-25 in user message to lead agent. Immutable per user direction.
- DEC-2 / DEC-3 / DEC-4: declared 2026-05-25 in same message.
- DEC-1: pending in next user message.

This file should be updated when DEC-1 resolves and at any subsequent Phase-3.4 decision the user finalises.
