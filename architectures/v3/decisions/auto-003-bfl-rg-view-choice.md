# auto-003 — BF-L per-RG-view choice at Phase 4 entry

**Author.** Lead agent, unattended Phase-4 dispatch session 2026-05-25.
**Status.** **Round 2 (revised after real adversarial review).** Round 1's option A (both views → (a) bounded sub-tracks per pre-defined count + parallel deep-research dispatch) is **superseded** by **option A′: smoke-test-first per view, then full sub-track if smoke-test passes, plus parallel deep-research dispatch with negative-result coverage required**. Round 1 reasoning preserved for traceability below; the revised decision and amendments are in [§Decision (Round 2)](#decision-round-2) at the end.
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

## Decision (Round 1 — superseded by Round 2 below)

~~**Option A. Both views → (a) bounded sub-tracks + parallel deep-research dispatch.**~~ Round-1 option A was rejected (1× reject-with-counter-proposal; 1× accept-with-amendments) by the real adversarial reviewers. See [§Decision (Round 2)](#decision-round-2). Round-1 reasoning preserved below for traceability.

### Round 1 reasoning (preserved)

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

## Adversarial review — Round 1 (real subagents)

Per the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents), two real adversarial subagents were dispatched against the Round-1 brief. Both returned substantive findings; one rejected option A with a counter-proposal, one accepted with named amendments. Convergent findings drove the Round-2 revision below.

### Reviewer 1 — Methodology-purist (verdict: `reject-with-counter-proposal`)

Core finding: option A's gates are count-targets without substance discipline, replaying the exact failure mode auto-002 Round 2 walked back from on U-B.

- **"≥20 patterns per language" is not binary-checkable.** A subagent under deadline pressure can emit 20 trivially-true patterns (file-naming regexes, PEP-8 ordering checks) that are *extractable* but don't *constrain the substantive convention surface* BF-L's regime classifier needs. P-31's smoke-test carries an explicit non-trivial-definition clause and disqualifies referential-integrity; auto-003 inherits none of that discipline.
- **"≥5 invariants per language" replays auto-002 Round 1's count-gate shape.** Auto-002 Round 1 was rejected partly because "≥15 invariants" was a count without a substance gate; the smoke-test redefinition (1 non-trivial per pair, positive/negative examples, corpus citation) is what fixed it. auto-003 Round 1 regresses to the rejected shape with the precedent in-hand.
- **"Manual-spot-check precision ≥0.7" is a substitute for measurement, not a measurement.** Golden corpus is undefined (who labels; what schema; inter-rater κ; N); "manual spot check" is undefined (sample size; blinding); 0.7 threshold has no corpus-anchored justification.
- **"Representative codebase per language" has no sampling frame.** Enterprise-Python-with-Django and embedded-Python share little convention surface; an extractor calibrated on one codebase is calibrated against itself.
- **No honesty-discipline clause.** P-31's "if no corpus-citable non-trivial invariant exists, say so explicitly and name the gap — fabricated invariants without corpus support do not count" has no analogue in auto-003.
- **Sub-track and research dispatch are redundant for the conventional view** (lint ecosystems, structured-output LLM applications, semantic-naming extractors are exactly what the sub-track has to read *before* construction; parallel firing means the sub-track starts blind).

Counter-proposal: **option A′: smoke-test-first per view, mirroring auto-002 Round 2.** Phase-3.5 follow-up smoke-test (≤2 subagents): 3 non-trivial substantive conventions/invariants per language for one named representative codebase, with corpus citation + positive/negative example + explicit honesty-discipline clause. Verdict: ≥2/3 per cell across ≥2 languages → full Phase-4 sub-track authorized; otherwise restate contract or accept-as-RG. Define "non-trivial" up front (constrains substance; disqualifies regex-grade pattern matches). Define "representative codebase" before launch (named sampling frame). Sequence research dispatch *before* (or at) smoke-test, not in parallel — prior-art survey feeds sub-track design.

### Reviewer 2 — Scoping-principle skeptic (verdict: `accept-with-named-amendments`)

Core finding: option A is structurally right (honors scoping principle + user direction), but imports two structural defects from the U-B precedent and adds one new defect.

- **Gate-calibration asymmetry with U-B is in the wrong direction.** U-B's smoke-test gate is a *constructive existence* test (≥4/5 pairs produce non-trivial invariants — observable from the artifact). BF-L's Round-1 gate is a *measurement* test against a measurement instrument the brief admits does not exist. The bars are not the same calibration; BF-L's is structurally harder *and* depends on a deliverable (golden corpus) not part of the sub-track.
- **Pre-elimination via the back door.** Round-1 sub-track scope silently absorbs golden-corpus authoring without budgeting it. BF-L could fail its Phase-4-close gate not because the prototype is bad but because the measurement instrument does not exist — functional pre-elimination under the scoping principle.
- **The (b) fallback is currently a fig leaf at the methodology level.** BF-L §2.1 (eligibility function) depends on invariant and convention densities as load-bearing inputs to the regime classifier. If both views fall back to accept-as-RG, BF-L's regime classifier degrades to "structural+historical+runtime+debt only" — empirically BF-S with extra storage. BF-L's track does not articulate the degradation pattern; the (b) fallback needs operational specification at Phase 6 methodology spec.
- **Research dispatch anchoring risk.** "Catalogue prior art on Daikon-style runtime invariant inference" anchors the sub-track on Daikon's known failure modes (instrumentation overhead, false-positive noise) rather than surfacing alternatives (type-inference-based invariants, contract-discovery from tests, LLM-extracted from test names). Charter must explicitly require negative-result coverage and an "alternatives-to-Daikon / alternatives-to-LLM-structured-output" axis.
- **BF-S/BF-M asymmetry unjustified.** BF-S accepts B7 partition-leakage as structurally unmitigable; BF-M accepts brief-quality calibration as Phase-5/8 work. Neither got a Phase-4 sub-track. BF-L gets two. Asymmetry is defensible on load-bearing grounds (P-26 is BF-L's entire thesis; B7-leakage is a measured residual side channel; P-27 brief-quality is one input among many) but the brief does not say so — creates a future precedent-confusion landmine.
- **X_UNM_B interaction is inverted.** Round-1 says "if BF-L's sub-tracks fail, X_UNM_B obligation *tightens*" — backwards. BF-L's failure is *evidence the primitive is RG*, which should make the unified candidates' obligation more *honest*, not tighter. The obligation should remain constant (articulate Codebase Model acquisition) regardless of BF-L's verdict; the *evidence available* shifts.

Named amendments: (A1) reframe both views' gates as constructive-existence tests symmetric with U-B; (A2) add methodology-degradation clause specifying how BF-L's regime classifier downgrades when either view falls back; (A3) research-dispatch charter requires negative-result coverage + alternatives axis; (A4) one sentence justifying BF-S/BF-M asymmetry on load-bearing grounds; (A5) fix X_UNM_B interaction (obligation constant; evidence shifts).

## Decision (Round 2)

**Option A′: smoke-test-first per view, then full sub-track if smoke-test passes, plus parallel deep-research dispatch with negative-result coverage required.**

This is option A re-shaped along the auto-002 Round-2 pattern. Round-1's bounded count-gates are replaced with U-B-symmetric constructive-existence tests; the research charter is widened to include negative results; the methodology-degradation clause is made explicit.

### Phase-3.5 follow-up smoke-test (NEW; Wave 4.5-pre, lead-agent-coordinated)

Two smoke-test subagents (one per RG view) fire **before** the full sub-track is authorized. Each subagent attempts a small, well-defined existence test:

- **Conventional-view smoke-test.** For one named representative codebase per top-3 language, produce **≥3 non-trivial substantive conventions per language** (9 total minimum across the 3 languages). Each convention carries: (i) typed envelope per the [P-26 sketch](../primitives/P-26-codebase-model.md) (`Convention { name, pattern, scope, evidence-symbols, confidence }`); (ii) corpus citation (the research source motivating the convention as a worth-extracting class); (iii) positive example from the representative codebase; (iv) negative example (a near-miss the convention does NOT satisfy); (v) honesty-discipline clause if no non-trivial convention exists for a (language × scope) cell ("name the gap explicitly; fabricated conventions without corpus support do not count").
- **Invariant-view smoke-test.** For one named representative codebase per top-3 language, produce **≥3 non-trivial machine-checkable invariants per language** (9 total minimum). Each invariant carries: (i) typed envelope per the P-26 sketch (`{symbol, predicate-AST, support, refuted, source}`); (ii) corpus citation; (iii) positive example; (iv) negative example; (v) same honesty-discipline clause.

**Non-trivial definition (binding for both views).** Mirrors P-31's clause: the convention/invariant must constrain *substance* (the content of one symbol's behavior or the codebase's idiom register), not just *presence* of a structural artifact. Disqualifies: file-naming regex matches; PEP-8-style ordering; test-file-name suffix checks; "every class has a docstring" presence checks; trivial type-system tautologies. Qualifies: structural-style rules with non-obvious enforcement edges (e.g., "data classes in `core/` modules are frozen=True; mutating writes go through a designated factory function — verifiable by AST inspection at construction sites"); behavioral invariants extractable by Daikon-style trace ingestion with corpus-citable support count.

**Representative codebase sampling frame (binding).** Each language gets one named representative codebase from a pre-declared sampling frame. Frame: open-source repository on GitHub with ≥3 years history, ≥100k LOC, ≥10 contributors, in active maintenance (commit in last 6 months), with permissive license. Specific named codebases to be selected by the smoke-test subagent from this frame and recorded in the smoke-test report. (Suggested defaults: Python = Django itself or pytest; TypeScript = VS Code or TanStack Query; Java = Spring Boot or Apache Kafka — subagent's call within the frame.)

**Smoke-test verdict logic (binding, mirrors auto-002 Round 2):**

- **≥2 of 3 languages produce non-trivial artifacts for both views** → full Phase-4 sub-track authorized (Wave 4.5 fires); scale smoke-test recipe from 3-per-language to ≥10-per-language; aggregate ≥30 conventions and ≥30 invariants by Phase-4-close.
- **1 of 3 languages produces non-trivial artifacts for both views** → contract restates per-view; the language that produced artifacts gets the full sub-track scaled; other two languages fall back to (b) accept-as-RG for that view at this Phase. Methodology-degradation clause activates.
- **0 of 3 languages produces non-trivial artifacts for either view** → both views fall back to (b) accept-as-RG for the full BF-L Phase-4 scope. Methodology-degradation clause activates fully.

The two views are evaluated independently — conventional may pass smoke-test while invariant fails, or vice versa.

### Parallel deep-research dispatch (revised charter)

Two research subagents fire **in parallel with the smoke-test**, *and their outputs feed the full-sub-track design if the smoke-test passes*. (Reviewer 1 wanted research *before* smoke-test; Reviewer 2 wanted research alongside but with widened charter. Compromise: parallel firing remains — total Phase-4 wall-clock matters — but research output is required input to the full Wave-4.5 sub-track if smoke-test passes. Smoke-test itself does not wait on research; the smoke-test exercise is small enough to overlap with research without redundancy at smoke-test scale.) Each subagent's charter is widened from Round 1:

- **Conventional-view research charter.** Catalogue prior art on machine-extracted code convention catalogues: industry tools (SonarQube, ESLint, ArchUnit, language-specific lint ecosystems); academic prototypes (naturalness-of-software; Allamanis et al. on naming and idioms); LLM-with-structured-output applications; semantic-naming-convention extractors; layering / architecture-rule extractors; test-pattern extractors; golden-corpus precedents. **NEW: required negative-result coverage** — explicit "what has been tried and abandoned" axis; explicit "alternatives to LLM-with-structured-output" axis (rule-mining; embedding clustering; pattern frequency on AST shapes).
- **Invariant-view research charter.** Catalogue prior art on production-grade runtime invariant inference: Daikon and successors; symbolic execution and abstract interpretation (KLEE, Z3, CBMC, Infer, CodeQL); type-inference-system invariant extraction; property-based testing inference; observability-driven invariant detection; LLM-extracted invariants from docs/comments; polyglot integration attempts. **NEW: required negative-result coverage** — "what has been tried and abandoned" axis; "alternatives to Daikon" axis (contract-discovery from tests; type-inference-lifted invariants; specification mining).

Outputs land as `architectures/v3/research-notes/bfl-conventional-view-prior-art.md` and `bfl-invariant-view-prior-art.md`. These notes feed (i) the full Wave-4.5 sub-track design if smoke-test passes, (ii) Phase-5 ADR alternatives-considered, (iii) Phase-8 lean-eval pressure-test design — regardless of smoke-test outcome.

### Full Wave-4.5 sub-track scope (if smoke-test passes; superseded if it fails)

If smoke-test verdict authorizes the full sub-track for a view (per the verdict logic above), the sub-track scales the smoke-test recipe to ≥10 non-trivial artifacts per language across the qualifying language set. Inputs: smoke-test artifacts as scaffold; research-notes as prior-art frame; P-26 sketch construction sentence as the engineering recipe; P-14 judge router for LLM dispatch; Daikon/CodeQL prior art per the invariant-view research notes. Phase-4-close gate: ≥30 conventions / ≥30 invariants (depending on view and qualifying-language count) demonstrable on the named representative codebases, with the honesty-discipline clause carried through and per-artifact corpus citations preserved.

### Methodology-degradation clause (NEW per Reviewer 2 A2)

When either RG view falls back to (b) accept-as-RG (either at smoke-test close or at full-sub-track close), BF-L's eligibility function and regime classifier explicitly downgrade as follows:

- **Conventional view fallback.** Regime classifier loses convention-density as an input feature. Cycles that touch regions with no convention coverage default to L3 eligibility (rather than L4 lights-out), pending operator approval. The methodology spec at Phase 6 carries this as an explicit clause; lean-eval at Phase 8 pressure-tests the L3-default's drift behavior.
- **Invariant view fallback.** Regime classifier loses invariant-density as an input feature. Scenario-derivation primitive (P-27) cannot pre-condition derived scenarios on invariant-satisfaction; derived scenarios are flagged "invariant-unconditioned" and routed to cross-family review rather than to L4 acceptance. Phase 6 spec carries this; Phase 8 lean-eval pressure-tests the cross-family-review overhead.

This makes the (b) fallback operationally viable rather than a fig leaf. BF-L's Phase-6 architecture spec (when it lands) MUST include both clauses regardless of smoke-test verdict — they're the structural defense the (b) option requires.

### BF-S/BF-M asymmetry justification (NEW per Reviewer 2 A4)

P-26 is **BF-L's entire thesis** — the candidate is defined as "three loops over one Codebase Model." Two of P-26's six views landing as RG-uncertainty puts the candidate's load-bearing claim on the line in a way that BF-S's B7 partition-leakage (a measured residual side channel; not a defeat of the substrate-first framing) and BF-M's P-27 brief-quality calibration (one input among many to the per-cycle Comprehension stage) do not. Bounded sub-tracks + research dispatch + smoke-test follow-up are proportionate to the load-bearing magnitude. The asymmetry is intentional and defensible on load-bearing grounds, not arbitrary.

### X_UNM_B interaction (corrected per Reviewer 2 A5)

The unified-attempt candidates' (U-A / U-B / U-C / D7-U-1) X_UNM_B obligation — articulate Codebase Model acquisition from legacy artifacts when claiming brownfield-fit — **remains constant regardless of BF-L's smoke-test or sub-track outcomes**. What shifts is the *evidence available* to each unified candidate's articulation:

- If BF-L's smoke-tests pass and the sub-tracks promote both views to designed-system, the unified candidates may cite BF-L's promoted views as feasibility evidence for the components they reference.
- If BF-L's smoke-tests fail and both views fall back to accept-as-RG, the unified candidates may legitimately cite that as evidence that the Codebase Model is genuinely RG (lowering the bar for what their X_UNM_B articulation can plausibly claim).
- If smoke-tests pass for one view and fail for the other, the unified candidates can cite per-view feasibility evidence.

The X_UNM_B obligation is informational, not contingent. Round-1's "obligation tightens on BF-L failure" framing was inverted; this correction makes the obligation evidence-aware rather than outcome-punishing.

### Round-2 cost summary

- 2 smoke-test subagents (1 per view) — small, bounded.
- 2 research subagents (1 per view) — already fired pre-Round-2; charter widened retroactively (research output integrates negative-result coverage by appending a follow-up subagent or by lead-agent supplementation at merge time).
- Conditional 1-2 full Wave-4.5 sub-track subagents (only if smoke-test passes).
- Total worst case: 5-6 additional subagents (same as Round 1) but with smoke-test gating before scaling.

### Round-2 rewind point

Rewind to: the commit landing this Round-2 revision on `claude/auto-003-bfl-rg-view-choice`. Reverting Round 2 returns to Round-1 option A wording (count-gates without smoke-test discipline). Reverting both Round 2 and Round 1 returns BF-L to its Phase-3.5.5 default (both views accept-as-RG; no sub-tracks).

### Round-2 honest acknowledgements

- **Research subagents already fired pre-Round-2.** The Round-1 dispatch fired research subagents in parallel with the adversarial review. Reviewer 1's "research before smoke-test" sequencing was not honored at firing time. Mitigation: the research output integrates retroactively at Wave-4.5 dispatch time if smoke-test passes; the in-flight charter is widened by lead-agent-authored follow-up notes (added to the research-notes documents after they land if negative-result coverage is thin).
- **Smoke-test recipe count (3 per language) is calibrated against auto-002's 1-per-pair**, scaled up because conventions and invariants are individually thinner than cross-layer invariants (which already encode pair-level structure). 3 is the minimum that produces a binary verdict signal across the (3 language × 2 view = 6 cell) matrix — anything lower risks zero-signal degenerate outcomes.
- **The deep-research dispatch survives smoke-test failure** because its output is valuable at Phase-5 ADR alternatives and Phase-8 lean-eval design regardless of whether BF-L's bounded construction succeeds. Discarding the research on smoke-test failure would punish the candidate twice.
