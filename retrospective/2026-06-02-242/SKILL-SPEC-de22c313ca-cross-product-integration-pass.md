# Spec: `cross-product-integration-pass`

- **ID**: SKILL-SPEC-de22c313ca
- **Source retrospective**: ../2026-06-02-242.md

## Intent

A massively-parallel authoring run that decomposes a corpus into clusters/products, reviews each cluster with its own seam adversary, then declares the corpus done has a structural blind spot: **seams that cross two clusters are each half-verified** — every per-cluster reviewer checks its own side and trusts the other. This skill adds a final **cross-product integration adversary** that traces the end-to-end critical path and diffs every cross-cluster contract at the field level, catching the deadlocks, enum collisions, and ordering contradictions that per-cluster reviews structurally cannot. It earned its place when one such pass over the Sweep-2 spine caught four build-breakers (a C52↔C53 deadlock, a `factory_build` status-enum collision, a C09↔C05 sequence-ordering contradiction, and a C41 actor-kind enum gap) that all six per-cluster seam reviews had passed.

## Trigger

- **Proactive (primary):** a parallel-authored corpus has finished its per-cluster/per-product reviews and is about to be declared done, merged, or PR'd — especially when ≥3 clusters share contracts (record schemas, wire types, call ordering, status enums) across cluster boundaries.
- **Direct:** "do a cross-product / whole-corpus integration review", "check the seams between products", "does the whole thing actually compose?"
- **Negative:** skip for a single-cluster corpus, or where no contract crosses a cluster boundary (each cluster is an island).

## Inputs

- The set of cluster/product specs (the whole corpus), and the per-cluster seam-review files already produced.
- The cross-component decision ledger (the numbered decisions that define shared contracts).
- The dependency/critical-path description (what hands off to what).

## Outputs

- One review file (`<corpus>-integration-review.md`) listing findings by severity, each naming the two components and the exact field/ordering/enum that contradicts.
- A short receipt: verdict + the count of *uncaught* contradictions (the ones no per-cluster review found).
- Applied fixes for the confident ones (or a dispatched integration-fix subagent), recorded as a ledger decision.

## Workflow

1. **Enumerate the cross-cluster seams.** From the dependency graph, list every contract that crosses a cluster boundary: shared record schemas, wire types, call/ordering hand-offs, status enums, shared envelope fields.
2. **Trace the end-to-end critical path** as a single chain (e.g. spec → bind → dispatch → worker → run → judge → reduce → gate) and walk each hand-off.
3. **For each seam, diff both sides at the field level.** Producer's emitted fields (names + types) vs consumer's read fields. Call ordering: does A call B, or B call A — and do both specs' diagrams agree? Enum membership: does every value one side emits appear in the other side's accepted enum? Status/lifecycle: does a terminal value one component writes match the envelope/query the other reads?
4. **Check the ledger decisions actually propagated** to *both* sides of each seam (a decision applied on one side and missed on the other is the classic failure).
5. **Classify findings**; apply confident fixes (or dispatch one integration-fix subagent with precise per-fix guidance); record the batch as a numbered ledger decision.
6. **Return the receipt** emphasizing the *uncaught* contradiction count — that number is the skill's whole justification.

## Concrete examples

**Example 1 — the deadlock.** C52 (self-bootstrap) and C53 (validation gate) were reviewed in the same cluster, but the reviewer verified `RubricResult == GoNoGoDecision` (type identity) without checking the call graph: C52's deploy gate consumed C53's output *and* C53's `decide()` required C52's `ReviewVerdict` — neither could run first. The integration pass traced `C52.review → ReviewVerdict → C53.decide() → GoNoGoDecision → C52.deploy` and found the cycle; the fix linearized it.

**Example 2 — the enum collision.** A ledger decision introduced `factory_build` `status = completed`. The bead-schema component's envelope enum was `{open, in_progress, closed}` (terminal `closed`). `completed` was illegal — a "find finished builds" query would silently return nothing. No per-cluster review caught it because the decision was authored in the bootstrap cluster and the envelope lived in the schema cluster. Fix: align to `closed`, put the outcome in a separate `milestone_verdict` field.

## Anti-patterns

- **Trusting type identity as contract identity.** `RubricResult = GoNoGoDecision` says the *types* match; it says nothing about whether the *call ordering* is acyclic. Check the call graph, not just the type.
- **Re-running per-cluster reviews and calling it integration.** The integration pass's value is *only* the cross-cluster seams; re-litigating intra-cluster findings wastes it.
- **Accepting "applied corpus-wide" without checking both sides.** A propagated decision is only propagated if *every* consumer was updated; verify the laggards.

## Acceptance criteria

1. Every cross-cluster seam is diffed at the field/ordering/enum level (not just named).
2. The review distinguishes *uncaught* contradictions (missed by per-cluster reviews) from already-known items.
3. Each finding names both components and the exact contradicting token.
4. Confident fixes are applied (or precisely briefed to one fix subagent) and recorded as a ledger decision.
5. The receipt states the uncaught-contradiction count.

## Files this skill creates / modifies

- `<corpus>-integration-review.md` — the cross-product review (new).
- The affected component specs — minimal seam fixes applied in place.
- The decision ledger — one numbered entry recording the batch of integration fixes.
