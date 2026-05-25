# auto-002 — U-B path at Phase 4 entry (invariant-authoring commitment vs self-elimination)

**Author.** Lead agent, unattended overnight run 2026-05-25.
**Status.** **Round 2 (revised after adversarial review)** — switched to **option 4 (smoke-test variant)**: dispatch a single Phase-3.5 follow-up subagent to attempt 1 non-trivial machine-checkable cross-layer invariant per layer-pair (5 total). If smoke-test produces ≥1 non-trivial invariant per pair: U-B survives Phase 4 entry with full sub-track authorized. If ≤2 non-trivial invariants total: U-B self-eliminates at smoke-test close (Phase-3.5.5 follow-up). Round-1 option 1 (full Phase 4 sub-track) is **rejected** — both reviewers converged on the smoke-test as strictly dominant.
**Rewind point.** Two commits: (1) this brief's Round-1 commit `af54c72`; (2) the Round-2 revision commit on `claude/auto-002-ub-path`. Reverting both returns U-B to its Phase-3.5.5 `conditional survival` status; the morning user can re-adjudicate.

**Plus a morning-review item:** the scoping-principle skeptic flagged that BF-L (which is allowed to accept-as-RG on Codebase Model views) and U-B (which must deliver-or-die on cross-layer invariants) are getting asymmetric treatment without justification. This asymmetry should likely be lifted to a Phase-3.5.5 rule (any candidate with a load-bearing RG primitive may either commit to a bounded authoring sub-track *or* downgrade the dependent contract to accept-RG). This brief authorizes only the smoke-test for U-B; lifting the rule to apply to BF-L (and downstream consequences for both) needs user input.

---

## The question

[Phase 3.5.5 candidate re-check](../candidate-registry.md#u-b--pace-layered-escrow-factory) returned U-B as **conditional survival**. The load-bearing finding: [P-31 cross-layer drift detector](../primitives/P-31-cross-layer-drift-detector.md) is `research-grade-uncertainty` because Brier's pace-layer framework is descriptive, not algorithmic — no source in the corpus authors per-layer-pair invariants. U-B's substrate scaffolding for P-31 is buildable, but the contract (flag cross-layer drift) cannot be honored without an invariant catalog.

The sketch's specific recommendation: **U-B must commit at Phase 4 to an invariant-authoring sub-track delivering ≥3 machine-checkable invariants per layer-pair with corpus citations**, or self-eliminate.

The decision: which path does U-B take at Phase 4 entry?

## Alternatives considered

### Option 1 — Allow U-B to attempt the commitment (chosen)

Phase 4 dispatch includes a U-B invariant-authoring sub-track. If U-B authors ≥15 machine-checkable cross-layer invariants by Phase 4 close (5 layer-pairs × ≥3 invariants), U-B moves to `survives with deferred-defense flag` and proceeds normally through Phase 5/6/7/8. If U-B cannot author them by Phase 4 close, U-B self-eliminates at Phase 4 close on the honest evidence that the corpus does not support the invariant catalog.

**Pros.**
- Honors the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief) ("carry every defensible candidate forward"). U-B's other primitives are all buildable; the candidate as a whole hasn't been proven undefendable, only one of its primitives has been challenged.
- The work is bounded — 15 invariants drawn from corpus fragments. GtWR has intra-layer invariants pointing at L2↔L3 (spec → plan); EARS pattern requirements point at L2↔L3 conformance; AILCCP three-controls point at L1↔L2 (architecture-control → spec); pace-layer artifact-link graphs trivially admit L2↔L3 referential integrity. The fragments are there; whether they cohere into 15 invariants is U-B's Phase-4 work to determine.
- Self-elimination at Phase 4 close is *still reversible* — the registry update would say "Phase 4 close: U-B self-eliminated on inability to author per-layer-pair invariants," which is more defensible than self-elimination at Phase 3.5 close on the lead-agent's prior judgment.
- Cost is bounded — one extra subagent for the invariant-authoring sub-track + lead-agent review at Phase 4 close.

**Cons.**
- Phase 4 dispatch carries one extra workstream that may turn out unproductive.
- If U-B authors invariants that are too weak (e.g., trivially true or trivially false), Phase 4 close still has to render a verdict — which is harder to do crisply than a binary "did they author or not."

### Option 2 — Self-eliminate U-B now

U-B drops out of the catalog at Phase 3.5 close. Phase 4 dispatches over 9 candidates instead of 10. [`candidate-registry.md`](../candidate-registry.md) gets a withdrawn-with-reason note for U-B (struck-through, like the GF→BF continuity withdrawal).

**Pros.**
- Cleaner Phase 4 dispatch (9 candidates, no conditional).
- Honest acknowledgement that the corpus doesn't support U-B's load-bearing primitive.
- Saves the cost of an invariant-authoring sub-track that may produce nothing.

**Cons.**
- **Violates the scoping principle.** The user's verbatim direction: "carry forward every candidate that defended itself." U-B *did* defend itself at Phase 3.2/3.3 (own OQ-PLEF-1 / OQ-PLEF-8 are honest open questions, not defeats); the only new finding is at the substrate level, and there's a defensible path forward.
- Eliminates the only pace-layer-organized methodology candidate, foreclosing a structural axis that Phase 8 lean-evals might pressure-test usefully.
- Phase 4 plan revision required (mandate-fit matrix becomes 9 rows; subsequent Phase 5/6/7/8 work all loses a candidate slot).

### Option 3 — Defer to Phase 5

U-B carries forward through Phase 4 as a candidate with an unresolved load-bearing primitive. Phase 5 ADR authoring (for U-B's substrate-requirements) forces the question — the P-31 ADR cannot land without invariants.

**Pros.**
- Same as option 1 in terms of carrying U-B forward.
- Defers the work to Phase 5, where the ADR discipline forces tractable resolution.

**Cons.**
- Pushes the adjudication later without changing the underlying evidence. U-B's substrate-requirements summary at Phase 4 will already require resolution of the invariant question (Phase 4's per-candidate summary lists buildability-confirmed primitives; P-31 isn't confirmed). The deferral doesn't actually save work; it just renames the deadline.
- Risks Phase 4's per-candidate substrate-requirements summary for U-B coming out empty on P-31, which is a degenerate output.

## Decision (Round 1 — superseded by Round 2 below)

~~**Option 1.** Phase 4 dispatch includes a U-B invariant-authoring sub-track.~~ Round-1 option 1 was rejected by both adversarial reviewers (scoping-principle skeptic + cost/scope hawk). See Round 2 at the end of this brief. Round-1 reasoning preserved for traceability above.

## Downstream impact

- **Phase 4.1 (per-candidate substrate-requirements).** U-B's summary includes the invariant-authoring sub-track as a Phase-4-internal workstream.
- **Phase 4.3 (shared-discipline inventory).** May benefit from U-B's invariant-authoring work — cross-layer invariants are themselves a discipline-shaped artifact (declarative referential-integrity-style constraints between artifact layers). If U-B's work produces durable invariants, those may generalize to other candidates' use of pace-layer-style artifact stacks.
- **Phase 5 ADRs.** The P-31 ADR scopes are conditional on U-B's invariant-authoring result. If U-B delivers, the ADR lands as designed-system; if not, no ADR (U-B drops out before Phase 5).
- **Phase 6 (architecture specs).** U-B's spec exists iff U-B survives Phase 4 close.

## If-user-overrides rewind point

Rewind to: the commit on `claude/auto-002-ub-path` that lands this brief. Reverting it returns the registry to its Phase-3.5.5 status (U-B `conditional survival` adjudicated at Phase 4 entry). The morning user can then pick option 2 or option 3 and re-dispatch.

## Adversarial-review round 1 — both reviewers rejected option 1 with specific evidence

Two adversarial subagents were dispatched and both returned `accept with named amendments` against option 2 / option 4 (smoke-test) variants. Their convergent findings:

### Finding 1 — The brief misreads the P-31 sketch on cross-layer invariants (scoping skeptic + cost hawk)

The Round-1 brief argued: "GtWR has intra-layer invariants pointing at L2↔L3 (spec → plan); EARS pattern requirements point at L2↔L3 conformance; AILCCP three-controls point at L1↔L2." **This contradicts the P-31 sketch directly.** Per [`P-31` § Research-grade-uncertainty](../primitives/P-31-cross-layer-drift-detector.md): "INCOSE GtWR constrains L2 internally; AILCCP controls anchor L0; El Kaim 9-field intent block structures L2 — but **none of these are framed as cross-layer invariants the substrate can check**. … [U-B's] examples (GtWR / EARS / AILCCP presence) **are intra-layer**." The Round-1 brief reframed *intra-layer* fragments as *pointing at cross-layer* invariants — the plausibility claim depends on a misreading of the very sketch that returned the RG verdict.

The cost-hawk reviewer attempted to find one non-trivial cross-layer invariant by reading `unified-B.md` + `failure-modes-v3.md` directly and found exactly one trivial (referential-integrity) L2↔L3 invariant ("every L3 plan node declares a `derives-from` edge to ≥1 L2 spec requirement"), and **zero non-trivial invariants for L0↔L1, L1↔L2, L3↔L4** in the available documents. The P-31 sketch already disqualified the trivial referential-integrity tier as "not drift detection."

### Finding 2 — Cost was understated by ~30× (cost hawk)

Round-1 said cost = "one extra subagent + lead-agent review at Phase 4 close." The cost-hawk reviewer enumerated downstream commitments per the v1.2 plan: if U-B survives Phase 4 close, the plan commits to Phase 5 wave-3 ADRs (3–6 candidate-specific × 3 bias guards each), Phase 6 architecture spec (+ consolidator/splitter/cell-defender/cell-attacker/cross-mandate/DEC-1.a-falsifier audits), Phase 7 back-fill audit, Phase 8 lean-eval brief. Subagent dispatches: ~30 beyond what option 2 incurs. At ~30–80k tokens each, **0.9M–2.4M tokens of avoidable spend if U-B fails the invariant-authoring sub-track**.

### Finding 3 — Asymmetric treatment of U-B vs BF-L is unjustified (scoping skeptic)

BF-L (which has 2 RG views in its Codebase Model) is allowed to "articulate Phase-4 plan for the conventional + invariant views **or accept them as research-grade**" — per the [Phase-3.5.5 candidate registry entry for BF-L](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first). U-B is being told to "deliver ≥15 invariants or self-eliminate." The asymmetry has no Phase-3.5.5-rule justification. Either both candidates get the lifeline (accept-as-RG with bounded scope) or neither does; per-candidate ad-hoc decisions create future precedent confusion.

### Convergent counter-proposal — smoke-test variant

Both reviewers (independently arriving at the same shape): **one Phase-3.5 follow-up subagent, charter to attempt 1 non-trivial machine-checkable cross-layer invariant per layer-pair (5 total) with corpus citations.** If the smoke-test produces ≥1 non-trivial invariant per pair: escalate to full Phase 4 sub-track with high confidence. If ≤2 non-trivial invariants total: U-B self-eliminates at smoke-test close. Cost: ~1 dispatch (~50k tokens). Downside: ~30× lower than option 1 if U-B is undeliverable. Upside: same as option 1 (defensible self-elimination evidence on honest failure) if U-B fails; clean go-ahead if U-B succeeds.

## Round 2 decision — option 4 (smoke-test variant)

**Decision.** Adopt the smoke-test variant. Dispatch a single Phase-3.5 follow-up subagent with the following charter:

> Read `architectures/v3/tracks/unified-B.md`, `architectures/v3/primitives/P-31-cross-layer-drift-detector.md`, `architectures/v3/failure-modes-v3.md`. For each of the 5 layer-pairs (L0↔L1, L1↔L2, L2↔L3, L3↔L4, L0↔L4 long-distance), attempt to author 1 non-trivial machine-checkable cross-layer invariant with: (a) explicit cross-layer constraint statement, (b) corpus citation for the invariant's source, (c) construction sentence naming the substrate primitive that would check it (OPA / Postgres recursive CTE / LLM judge via P-14), (d) one example positive case + one example negative case. If for any layer-pair no non-trivial invariant is constructible from the corpus, report that explicitly and name the gap.

**Verdict logic at smoke-test close:**
- **≥4 of 5 layer-pairs produce non-trivial invariants** → U-B survives Phase 3.5 with full sub-track authorized for Phase 4 (the sub-track scales the smoke-test's recipe to ≥3 per pair).
- **2–3 of 5 layer-pairs produce non-trivial invariants** → U-B's contract restates to depend only on the layer-pairs with invariants; the other pairs accept-as-RG (analogous to BF-L's option). User-review item.
- **≤1 of 5 layer-pairs produces non-trivial invariants** → U-B self-eliminates at smoke-test close on honest evidence; the lead-agent updates the registry with the strikethrough and the smoke-test sketch is the evidence.

**Amendments incorporated from Round 1:**
1. ✅ Replace ≥15-invariants gate with ≥1-per-pair smoke-test (then full sub-track if smoke-test passes).
2. ⏸ Lift the BF-L / U-B asymmetry to a Phase-3.5.5 rule — **morning-review item, not auto-decided.** This brief does not authorize the rule change; it documents the asymmetry and recommends the rule shape (any candidate with a load-bearing RG primitive may either commit to a bounded sub-track or downgrade dependent contract to accept-RG with substrate-documented gap). User input needed because the rule change is meta-governance.
3. ✅ Correct the GtWR/EARS/AILCCP misreading by deleting the "fragments point at cross-layer" claim from the Round-1 Pros bullet (the Round-1 section above is preserved with this brief's Round-2 supersession marker; the misreading is explicitly noted here).

## Downstream impact of Round 2 revision

- **Phase 3.5.5 close.** U-B's status moves from `conditional survival adjudicated at Phase 4 entry` to `conditional survival adjudicated at smoke-test close (Phase-3.5 follow-up)`. The smoke-test result lands as `architectures/v3/primitives/P-31-smoke-test-invariants.md`.
- **Candidate registry.** U-B's Phase-3.5.5 subsection will be updated with the smoke-test result and the Round-2 verdict logic.
- **Phase 4 dispatch.** If U-B survives smoke-test, Phase 4 dispatches over 10 candidates. If U-B self-eliminates, Phase 4 dispatches over 9 candidates.
- **BF-L parallel.** BF-L's parallel option (accept-as-RG vs author work) is deferred to morning-review item — does the lifted Phase-3.5.5 rule apply retroactively or only prospectively? User decides.

### Verdict status from reviewers (recorded)

- Scoping-principle skeptic: `accept with named amendments` ✓ (amendments 1, 3 incorporated; amendment 2 surfaced as morning-review item)
- Cost/scope hawk: `reject and amend — switch to smoke-test variant` ✓ (incorporated as the Round-2 decision)

