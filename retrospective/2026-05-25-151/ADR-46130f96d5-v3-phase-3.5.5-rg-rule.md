# ADR: Phase-3.5.5 RG-primitive rule (v3 synthesis, binding)

- **ID**: ADR-46130f96d5
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-151.md
- **PRs covered**: #144

## Context

At the close of Phase 3.5 (substrate-primitive buildability sketches) in the v3 architecture synthesis, three primitives landed research-grade-uncertainty: P-26 (Codebase Model — 2 of 6 views), P-31 (cross-layer drift detector), P-34 (independence auditor). Each was load-bearing for at least one candidate (BF-L, U-B, D7-U-1 respectively). The Phase-3.5.5 candidate re-check applied per-candidate handling: BF-L was told to "articulate Phase-4 plan or accept-as-RG"; U-B was told to "deliver ≥15 invariants or self-eliminate." The scoping-principle skeptic adversarial reviewer on `auto-002` Round 1 flagged this as asymmetric — BF-L was allowed accept-as-RG, while U-B was deliver-or-die, with no Phase-3.5.5-rule justification for the difference.

The user agreed with the skeptic's analysis 2026-05-25: lift the asymmetry to a Phase-3.5.5 rule applying uniformly across candidates. The rule was codified live in PR #144 (`d73a4df`).

## Decision

**Any v3-synthesis candidate with a load-bearing research-grade-uncertainty primitive at Phase-3.5 close may either commit to a bounded authoring sub-track at Phase 4 to convert the RG portion into designed-system content, or downgrade the dependent contract to accept-as-RG with the substrate documenting the gap; the choice is per-RG-portion (a candidate may pick option (a) on some and (b) on others), and the default if no choice is declared at Phase 4 entry is accept-as-RG.** Option (a) lands as a Phase-4 work item with explicit scope, deliverable, and Phase-4-close go/no-go gate. Option (b) flows into Phase-5 ADRs marked `accepted-with-RG-flag`, Phase-6 architecture specs with the accept-as-RG note in YAML header, and Phase-8 lean-evals that pressure-test the degradation pattern.

The rule lives in [`architectures/v3/candidate-registry.md`](../../architectures/v3/candidate-registry.md) as a section after the Phase-3.5.5 re-check, with a per-candidate application table assigning each known RG portion an option (or marking it as candidate's-choice-at-Phase-4-entry).

## Alternatives considered

- **Force option (a) (bounded sub-track) for all RG primitives.** Rejected because some RG portions are genuinely intractable from corpus material — forcing a sub-track would produce dishonest results or false-positive self-eliminations. BF-L's conventional view (LLM-with-structured-output + golden corpus) is exactly this case: the corpus has no industry standard for "good enough."
- **Force option (b) (accept-as-RG) for all RG primitives.** Rejected because some RG portions are tractable with bounded work (U-B's cross-layer invariants, per the smoke-test result). Forcing accept-as-RG would lose architectural rigor where rigor is available.
- **Decide per-candidate, no rule.** Rejected as the original (pre-rule) state. The scoping-principle skeptic showed it creates asymmetry without justification. A single rule applying uniformly is simpler and more defensible.
- **Per-RG-portion choice but no default.** Rejected because some candidates may not articulate a choice (e.g., a unified-attempt candidate that doesn't claim brownfield-fit doesn't have a Codebase Model author to speak for the RG views). A default of accept-as-RG protects the candidate from undeclared assumptions while leaving the option open.
- **Apply globally, not just to v3.** Rejected as overreach. The rule is grounded in the v3 synthesis pipeline's specific structure (Phase 3.5 = buildability close; Phase 4 = substrate-requirements per candidate; Phase 5 = ADRs). Generalizing prematurely risks anchoring future projects to a v3 framing that may not fit.

## Consequences

**Easier.** Future v3 candidate-rule decisions are governed by a single uniform rule rather than ad-hoc per-candidate adjudication. The per-RG-portion granularity allows mixed strategies (BF-L can accept-as-RG on conventional, attempt sub-track on invariant). Phase-4 entry has a clean default (accept-as-RG) so silence becomes a defensible position rather than ambiguous limbo. The rule generalizes the smoke-test pattern ([ADR-944bc4bd97](ADR-944bc4bd97-smoke-test-rg-primitive.md)) — sub-track commitments should run a smoke-test first.

**Harder.** Phase 4 dispatch must now consult the rule's per-candidate application table; candidates that didn't declare a choice get the default but may need that choice articulated when their substrate-requirements summary is authored. Phase-5 ADRs gain a new status (`accepted-with-RG-flag`) that downstream specs must propagate. Phase-8 lean-evals must include degradation-pattern pressure-tests for every accept-as-RG portion.

**Accepted trade-off.** The rule honors the scoping principle (carry every defensible candidate) without abandoning architectural honesty (don't pretend RG is designed-system). Per-RG-portion granularity adds modest bookkeeping in exchange for substantially better expressiveness across candidates. The default-to-accept-as-RG means a candidate that fails to engage doesn't get punished beyond losing the option to convert.

## References

- [`../2026-05-25-151.md`](../2026-05-25-151.md) — the source retrospective.
- [`../../architectures/v3/candidate-registry.md`](../../architectures/v3/candidate-registry.md) — the registry section carrying the rule.
- [`./ADR-944bc4bd97-smoke-test-rg-primitive.md`](./ADR-944bc4bd97-smoke-test-rg-primitive.md) — the smoke-test pattern that rule option (a) instances.
- [`../../architectures/v3/decisions/auto-002-ub-path.md`](../../architectures/v3/decisions/auto-002-ub-path.md) — the brief whose adversarial review surfaced the asymmetry.
- PRs the decision was made in: #144 (codified the rule in the registry live during the session).
