# auto-003 — BF-L per-RG-view choice at Phase 4 entry

**Author.** Lead agent, unattended Phase-4 dispatch session 2026-05-25.
**Status.** **Round 1 (lead-agent's best call, prior to adversarial review).** Round 2 will be appended after real adversarial subagents return per the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents).
**Rewind point.** This brief's commit on `claude/auto-003-bfl-rg-view-choice`. Reverting returns BF-L to its [Phase-3.5.5 status](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first) where the registry's "candidate's choice at Phase 4 entry; default (b) accept-as-RG if no choice declared" remains the operative wording and no Phase-4 sub-tracks are authorized for BF-L's two RG views.

**User direction (received 2026-05-25 with this dispatch).** The user has directed: "dedicate resources to research what has already been done in terms of implementing the two RG aspects of the primitive. Do all of the research and primitive design/implementation work in subagents and continue in parallel with the rest of phase 4. […] I want to carry even the RG-severity concerns much further in the pipeline. These are active areas of work, and a solution sketch may become available very soon." This brief records the **lead-agent framing** of how that direction implements as Phase-4 work (sub-track scope, deliverables, gate criteria, parallel-research dispatch). Adversarial review focuses on the framing, not the user's underlying choice.

---

## The question

Per the [Phase-3.5.5 rule on load-bearing RG primitives](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), any candidate with a load-bearing RG primitive may either:

- **(a)** Commit to a bounded authoring / specification sub-track at Phase 4 to convert the RG portion into designed-system content, with explicit scope, deliverable, and Phase-4-close go/no-go gate.
- **(b)** Downgrade the dependent contract to accept-as-RG; the methodology specifies how it degrades gracefully when the RG portion is unreliable.

The rule applies per RG-portion (not per candidate). [BF-L](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first) has **two** RG views in its load-bearing primitive [P-26 Codebase Model](../primitives/P-26-codebase-model.md): conventional and invariant. Each gets the (a)/(b) choice independently. The registry's default for both, in the absence of an explicit declaration at Phase 4 entry, is **(b) accept-as-RG**.

BF-L is not a live candidate-author. The lead agent must either (i) write a recommendation per each view and dispatch adversarial review, (ii) surface to the user for direct decision, or (iii) accept the default (b).

## Alternatives considered

### A. Both views → (a) bounded sub-tracks + parallel deep-research dispatch — **chosen** (per user direction)

- **Conventional view sub-track at Phase 4.** Deliverable: an LLM-with-structured-output Convention extractor calibrated against a golden corpus of human-labelled conventions. Bounded scope: ≥20 idiomatic patterns per supported language for the top-3 languages by representative-codebase coverage (typically Python / TypeScript / Java in modern polyglot enterprise codebases). Construction path drawn from [P-26 §Construction-conventional](../primitives/P-26-codebase-model.md): Pydantic-typed `Convention { name, pattern, scope, evidence-symbols, confidence }` over a stratified sample (recency × churn), with a cross-family judge ensemble via [P-14 judge router](../primitives/P-14-judge-router.md). Phase-4-close go/no-go gate: a working prototype on ≥1 representative codebase per language with manual-spot-check precision ≥0.7 on extracted conventions against the golden corpus. If gate fails, conventional view falls back to (b) accept-as-RG.

- **Invariant view sub-track at Phase 4.** Deliverable: a Daikon-style runtime invariant inference pipeline integrated with the structural view's symbol-space. Bounded scope: ≥5 declared machine-checkable invariants per language for the top-3 languages (15 total minimum). Construction path drawn from [P-26 §Construction-invariant](../primitives/P-26-codebase-model.md): Daikon ingesting [P-07](../primitives/cluster-C2.md) trace dumps joined with structural symbol ranges, plus CodeQL for declared-invariant queries, plus LLM-extracted narrative invariants from docs/comments, writing to a Glean `Invariant` predicate with `source` provenance. Phase-4-close go/no-go gate: ≥15 corpus-citable invariants demonstrable on a representative codebase, with per-invariant precision sampling. If gate fails, invariant view falls back to (b) accept-as-RG.

- **Parallel deep-research dispatch (independent of the sub-tracks above).** Two research subagents fire concurrent with the Phase-4 substrate-requirements fanout, *regardless of the Phase-4-close verdict* on the sub-tracks. Their charter: catalogue prior art and active work on (i) machine-extracted code convention catalogues (industry tools, academic prototypes, language-specific lint ecosystems, structured-output LLM applications, semantic-naming-convention extractors) and (ii) production-grade runtime invariant inference (Daikon-style and successors, polyglot integration attempts, observability-stack integrations, symbolic-execution alternatives, type-inference-system invariant extraction). Output: research notes + primitive design refinements that feed both the Phase-4 sub-tracks AND any downstream resurrection of the views after their initial Phase-4 verdict.

- **Pros.**
  - Honors the user's direction: research happens in parallel regardless of sub-track outcome; RG-severity carries deeper into the pipeline.
  - Maximizes information value: the Phase-4 sub-tracks (constructive prototype work) and the research dispatch (prior-art survey + design refinement) are complementary, not redundant — the sub-tracks attempt to build, the research catalogues what others have tried.
  - Resilient to the "solution sketch may become available very soon" possibility the user named — if external prior art or active work surfaces a better path, the research subagents are the watching mechanism.
  - Preserves the Phase-3.5.5 RG-primitive rule's degradation pathway: if a sub-track fails its Phase-4 gate, the view falls back to (b) accept-as-RG, and BF-L's methodology gates that depend on it degrade gracefully (or are deferred per the rule's option (b) text).
  - Symmetric with U-B's authorized invariant-authoring sub-track per [auto-002 Round 2](auto-002-ub-path.md) — both candidates get bounded-attempt treatment on their load-bearing RG primitives, with research dispatch as additional structural defense.

- **Cons.**
  - Highest cost option: 2 sub-tracks (each at least 1 subagent + 1 evaluator) + 2 research subagents = 4-6 additional dispatches over the Phase-4 baseline. Mitigated by parallel dispatch and the fact that all are bounded-scope.
  - Phase-4-close requires four go/no-go calls (one per view's sub-track + one per view's research output), increasing aggregation complexity.
  - If both sub-tracks fail their gates, the Phase-4 budget on them is spent without a designed-system promotion. Counter-counter: the research output still feeds downstream phases, and the failure is evidence material for Phase-8 lean-eval design.

### B. Conventional → (b) accept-as-RG; Invariant → (a) bounded sub-track only

The original lead-agent default in the [SESSION-HANDOFF brief](../SESSION-HANDOFF-2026-05-25-phase-3.5-close.md#phase-4-entry-blockers-user-input-territory): accept conventional as RG (LLM-with-structured-output is non-trivial calibration work, deferring to use-time is honest); commit to invariant sub-track only (Daikon-style runtime inference is well-understood prior art).

- **Pros.** Lowest cost; addresses only the more tractable RG view; matches "lean toward (a) for the well-trodden case and (b) for the less-trodden" heuristic.
- **Cons.** Violates the user's direction (which calls for research subagents on **both** views, regardless of sub-track choice). Treats the two views asymmetrically without strong evidence that the conventional view is less tractable than the invariant view — both have honest unwitnessed-at-scale gaps per [P-26 §RG-flag](../primitives/P-26-codebase-model.md). Forecloses the conventional-view research dispatch the user explicitly authorized. **Rejected** on user-direction grounds; preserved as the contrast option.

### C. Both views → (b) accept-as-RG only

The registry's default if no choice is declared.

- **Pros.** Lowest cost; honest about the unwitnessed-at-scale gap; BF-L's methodology degrades gracefully per the (b) rule.
- **Cons.** Forecloses both research dispatches; loses the parallel-research watching mechanism the user wants; sends weaker signal to downstream phases that BF-L is actively defending its load-bearing primitive vs accepting structural limitation. **Rejected** on user-direction grounds.

### D. Both views → (a) bounded sub-tracks, no separate research dispatch

Option A minus the deep-research subagents.

- **Pros.** Slightly lower cost than A.
- **Cons.** Misses the user's explicit "research what has already been done" direction. Sub-tracks attempt construction without first surveying prior art at the depth the research subagents would produce — risks rediscovering known failure modes or missing recently-published advances. **Rejected** on user-direction grounds; the sub-track work itself does some prior-art reading but not at the dedicated depth a research subagent would.

## Decision (Round 1)

**Option A. Both views → (a) bounded sub-tracks + parallel deep-research dispatch.**

Lead-agent reasoning (preserved for traceability against Round 2):

1. **User direction is explicit and binding.** The user has directed deep-research subagents on both RG views and the choice to "keep" regardless. Option A is the implementation that satisfies both halves.

2. **Symmetric treatment across RG candidates.** U-B got a bounded smoke-test + full sub-track on P-31 ([auto-002 Round 2](auto-002-ub-path.md)). D7-U-1 got an A+C hybrid on P-34 ([P-34 sketch](../primitives/P-34-independence-auditor.md)). BF-L on (a)+(a)+research-dispatch is the same treatment scaled to two RG portions. The [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) is designed for exactly this symmetry; option A applies it consistently.

3. **Bounded scope is real.** "≥20 patterns per language across top-3 languages" and "≥5 invariants per language" are tractable Phase-4 deliverables drawing on named existing tools (LLM-with-structured-output via P-14; Daikon + CodeQL + LLM ensemble via P-26 construction sketch). The work is engineering and prior-art reading, not novel research.

4. **Cost is bounded and proportionate.** 4-6 additional subagents in a Phase that's already running 10 per-candidate substrate-requirements subagents + 1 lead-agent overlap + a discipline-extraction fanout. The marginal cost of carrying BF-L's RG defense forward is small against the catalog cost of the broader Phase-4 dispatch.

5. **Failure modes are absorbed by the (b) fallback.** If either sub-track fails its Phase-4-close gate, the view degrades to (b) accept-as-RG per the binding rule. BF-L's methodology spec at Phase-6 must already articulate the graceful-degradation pattern; option A does not increase that methodology obligation.

## Downstream impact

- **Phase 4.1 (per-candidate substrate-requirements).** BF-L's substrate-requirements summary explicitly names both sub-tracks as Phase-4-internal workstreams + the parallel research dispatch as a long-running Phase-4 input. The summary lists P-26 conventional and invariant views as "authoring-attempt in progress" with the Phase-4-close go/no-go criteria as named gates.

- **Phase 4 parallel-research dispatch (NEW per option A).** Two research subagents fire concurrent with the Phase-4 substrate-requirements fanout (and with this brief's adversarial review). Their outputs land as `architectures/v3/research-notes/bfl-conventional-view-prior-art.md` and `bfl-invariant-view-prior-art.md`. The notes feed (i) the Phase-4 sub-track design, (ii) Phase-5 ADR alternatives-considered, (iii) Phase-8 lean-eval pressure-test design.

- **Phase 5 (ADRs).** Two BF-L-specific ADRs for the conventional + invariant views. Each ADR cites the sub-track verdict (designed-system promoted vs accept-as-RG fallback) and the research notes for alternatives-considered. If the sub-track succeeded, the ADR is `accepted`. If it fell back, the ADR is `accepted-with-RG-flag` per the Phase-3.5.5 rule.

- **Phase 6 (architecture spec for BF-L).** Per-view treatment: any view that promoted to designed-system carries a normal substrate-slot declaration; any view that fell back carries an explicit accept-as-RG note in the YAML header + a methodology-degradation pattern describing how regime classification and scenario derivation operate when that view is unreliable.

- **Phase 8 (lean-eval brief for BF-L).** Pressure-tests both views' outcomes: if promoted, lean-eval probes the sub-track's precision/recall claims under adversarial input; if fallen back, lean-eval probes the degradation pattern.

- **X_UNM_B finding interaction.** Per the [X_UNM_B finding](../candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes), unified-attempt candidates (U-A, U-B, U-C, D7-U-1) that claim brownfield-fit must articulate Codebase Model acquisition. BF-L's per-view outcomes set the bar for what "Codebase Model" can plausibly mean at Phase-6: if BF-L's own bounded sub-tracks fail their gates, the X_UNM_B obligation tightens (the unified candidates cannot rely on a primitive BF-L itself could not promote) — informational, not a blocker.

## If-user-overrides rewind point

Rewind to: the commit on `claude/auto-003-bfl-rg-view-choice` that lands this brief. Reverting it returns BF-L to the registry's Phase-3.5.5 default (both views accept-as-RG; no sub-tracks authorized). The user can then pick option B (asymmetric: invariant only), option C (full default), or option D (sub-tracks without research dispatch).

To roll back the research-dispatch portion only (keeping the sub-tracks): the research-dispatch subagents are queued as separate commits with their own rewind points; option A's full landing is the union of the brief + the sub-track authorization + the research dispatches, so each component is independently rewindable.

## Adversarial review

**Status: pending.** Per the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents), real adversarial subagents will be dispatched against this brief before its final commit. Reviewer angles:

1. **Methodology-purist reviewer.** Challenges whether the sub-track scope ("≥20 patterns per language across top-3 languages" / "≥5 invariants per language") is rigorously defined or hand-wavy. Probes the Phase-4-close go/no-go criteria for sufficiency. Tests whether the "manual-spot-check precision ≥0.7" gate is a real measurement or a substitute for one.
2. **Cost/scope hawk.** Challenges the 4-6 additional subagent dispatches against the Phase-4 baseline. Probes whether the sub-tracks and the research dispatches are redundant. Argues for option B or D as a less-expensive variant the user might accept.
3. **Scoping-principle skeptic.** Challenges whether option A's bounded-sub-track + research-dispatch shape preserves the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief). Tests whether the Phase-4-close gates set the bar high enough to be defensible without being so high they functionally pre-eliminate BF-L's views.

Round 2 will follow with the reviewers' findings + the lead-agent's revised decision (or confirmation of Round 1) + amendments to the sub-track and research-dispatch briefs.
