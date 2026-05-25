# auto-002 — U-B path at Phase 4 entry (invariant-authoring commitment vs self-elimination)

**Author.** Lead agent, unattended overnight run 2026-05-25.
**Status.** Decided — proceeding with **option 1 (allow U-B to attempt the invariant-authoring commitment at Phase 4)**.
**Rewind point.** The brief commit on `claude/auto-002-ub-path`. Reverting it reverses the decision; U-B's path is then re-adjudicated by the morning user from the [`overnight-summary`](../../../overnight-summary.md#morning-decision-item) item.

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

## Decision

**Option 1.** Phase 4 dispatch includes a U-B invariant-authoring sub-track. The U-B substrate-requirements summary at Phase 4.1 lists P-31 as "construction confirmed; invariant catalog in authoring (sub-track)." Phase 4 close adjudicates whether U-B has delivered ≥15 cross-layer invariants; if yes, U-B proceeds; if no, U-B self-eliminates with the registry entry "Phase 4 close: U-B self-eliminated on failure to author per-layer-pair invariants in the bounded sub-track."

This is the path most consistent with the scoping principle and most reversible. If the morning user disagrees and prefers option 2 (eliminate now), revert this brief's commit; the registry's Phase-3.5.5 entry already documents the conditional-survival shape and the morning user can override by adding a strikethrough.

## Downstream impact

- **Phase 4.1 (per-candidate substrate-requirements).** U-B's summary includes the invariant-authoring sub-track as a Phase-4-internal workstream.
- **Phase 4.3 (shared-discipline inventory).** May benefit from U-B's invariant-authoring work — cross-layer invariants are themselves a discipline-shaped artifact (declarative referential-integrity-style constraints between artifact layers). If U-B's work produces durable invariants, those may generalize to other candidates' use of pace-layer-style artifact stacks.
- **Phase 5 ADRs.** The P-31 ADR scopes are conditional on U-B's invariant-authoring result. If U-B delivers, the ADR lands as designed-system; if not, no ADR (U-B drops out before Phase 5).
- **Phase 6 (architecture specs).** U-B's spec exists iff U-B survives Phase 4 close.

## If-user-overrides rewind point

Rewind to: the commit on `claude/auto-002-ub-path` that lands this brief. Reverting it returns the registry to its Phase-3.5.5 status (U-B `conditional survival` adjudicated at Phase 4 entry). The morning user can then pick option 2 or option 3 and re-dispatch.

## Adversarial-review round

Two adversarial subagents will be dispatched to attack this brief from independent angles:
- **Scoping-principle skeptic** — does option 1 preserve scoping, or does it covertly weaken the principle by carrying forward a candidate whose load-bearing primitive is unbuildable?
- **Cost/scope hawk** — is the invariant-authoring sub-track worth the cost, or is option 2 strictly cheaper-and-equivalent?

This brief will be updated with their findings in a follow-up commit on the same branch (Round 2), or in this commit if the reviewers' findings strengthen rather than overturn option 1.
