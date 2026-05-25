# ADR 0060: D7-U-1 P-33 opposing-side router

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c2 subagent

## Context

[P-33 opposing-side router](../../architectures/v3/primitives/P-33-opposing-side-router.md) is claimed by exactly one candidate — [D7-U-1 prohibit-interval-escrow](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) — and is classified `orphan` in the [Phase-4.2 coverage table](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage). The primitive consumes a **Falsification Commitment (FC)** plus a content-addressed handle to the artifact-to-be-falsified, and returns the resolved opposing-side handler — an LLM-judge of distinct `(model-family, role)`, a named deterministic checker, a named human-of-record, or a population-vote pool — contractually responsible for trying to falsify the artifact before the [P-29 FC-survival compounding gate](../../architectures/v3/substrate-requirements/d7-u-1.md#3-load-bearing-design-content-the-architecture-locks-in-with-honest-rationale) propagates it.

P-33 forces a same-vs-distinct call against [P-14 judge router (ADR 0016)](0016-p-14-judge-router.md): both ride LiteLLM `Router` + a model-family taxonomy + tag-based cross-family routing. The [Phase-4.2 overlap analysis renders an explicit DISTINCT verdict](../../architectures/v3/primitives/overlap.md#p-33-vs-p-14--opposing-side-router-vs-judge-router):

> "**Verdict: DISTINCT primitives** despite shared underlying tool. … **P-14 (judge router)** is a *router over LLM judge endpoints* with provider-family-diverse routing and typed input/output shapes per judge role. The handler universe is LLM judges (with optional deterministic-judge inclusion as a degenerate case). **P-33 (opposing-side router)** is a *router over the full opposing-side handler universe* — LLM judges (with unconditional builder-family exclusion), deterministic checkers (Python predicates), named-human approvers, population votes. The router's load-bearing value-add is the *exclusion logic* (three-layer denylist: call-time computed + LiteLLM tag-exclusion + registry family-allowlists) and the *kind-dispatch logic* (FC-shaped: routes by `refutation-attempt.method`). … P-14 → P-33 is NOT a generalization-specialization relationship at the substrate level; the routers have different *contract surfaces*. A deployment could share LiteLLM Router infrastructure but the routing-policy layer is per-primitive."

The forcing failure modes are the [F1 / F27 / F46 / F48 correlated-error cascade](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot) — D7-U-1 §0 names this cascade as the single mechanism the FC primitive addresses. Any router that can return the builder's own family as opposing side defeats the cascade-mitigation contract.

## Decision

**Build P-33 as a FC-typed dispatch layer over the same LiteLLM `Router` infrastructure used by [P-14 (ADR 0016)](0016-p-14-judge-router.md), but with a distinct routing-policy contract**: `resolve_opposing_side(fc, artifact) → Handler` that (1) reads `FC.artifact-kind` + `FC.refutation-attempt.method`; (2) queries a **capability registry** (YAML/SQLite) mapping `(artifact-kind × method) → eligible handler classes` covering LLM-judge families, deterministic checkers (Python predicates), named human-of-record identities, and population-vote pools; (3) for LLM-judge classes computes `denylist := {artifact.builder.family}` at call-time and invokes `Router.get_available_deployment(model, request_kwargs={"tags": ["exclude:" + builder.family]})`; (4) for deterministic / human / vote classes returns the registered binary / identity / pool ID directly.

The **three-layer denylist** that distinguishes P-33 from P-14 is mandatory and structural:

1. **Call-time computed denylist** from `artifact.builder.family` — sourced from the artifact's provenance metadata, NOT from methodology config, so methodology layers cannot weaken it.
2. **LiteLLM tag-exclusion** at dispatch (`tags=["exclude:" + builder.family]`); the router raises if no eligible deployment survives, and the substrate escalates to a named-human handler rather than weakening the denylist.
3. **Registry family-allowlists** per builder family, so registry entries cannot list a re-introducing handler. The [P-29 FC-survival compounding gate](../../architectures/v3/substrate-requirements/d7-u-1.md#3-load-bearing-design-content-the-architecture-locks-in-with-honest-rationale) refuses any verdict where `Handler.family == artifact.builder.family` as a fourth post-hoc check.

Unlike P-14, the builder-family exclusion is **unconditional** (not gated on a `cross-family` methodology flag), and the handler universe is **broader** (deterministic checkers, named humans, and population votes are first-class registry-typed classes, not degenerate cases of LLM-judge routing).

## Alternatives considered

**B. Collapse P-33 into P-14 as a thin FC-typed wrapper.** *Why rejected:* the [Phase-4.2 overlap verdict explicitly rejects this collapse](../../architectures/v3/primitives/overlap.md#p-33-vs-p-14--opposing-side-router-vs-judge-router): "P-33 has substantial shared substrate with P-14 but is NOT collapsible without losing D7-U-1's *do-not-unify* discipline (the unconditional builder-family exclusion)." Collapsing would force P-14's optional `cross-family` flag onto every dispatch and conflate two distinct contract surfaces (judge-shape input vs FC-shape input). The do-not-unify discipline must be a substrate invariant, not a methodology-configurable policy.

**C. Build P-33 as a pure LLM-judge router that delegates deterministic / human / vote handlers to separate substrates.** *Why rejected:* this defeats the broader-handler-universe contract that P-33 explicitly exists to provide. The FC-shaped dispatch surface promises that `FC.method ∈ {property-test, type-check, replay-trace, …}` routes to deterministic checkers under the same exclusion-logic regime as LLM-judge methods. Splitting the handler universe across substrates re-fragments the cascade-mitigation contract and re-exposes the F46/F48 surface that the unified router exists to close.

## Consequences

**Easier:** the F1/F27/F46/F48 cascade is mechanically blocked at substrate level; methodology layers cannot weaken builder-family exclusion. FC-typed dispatch lets `FC.refutation-attempt.method` deterministically select the handler class without per-cycle agent-discipline. Operations reuses P-14's LiteLLM deployment, model-family taxonomy, and tag scheme — no second router runtime.

**Harder:** capability-registry authoring becomes a per-deployment ops requirement (registry schema is per-`(artifact-kind × method)`); registry edits need audit. Named-human handlers introduce a queue-attention design problem (escalation when no eligible LLM-judge survives the denylist). [F47 Goodhart-on-Tokens](../../architectures/v3/failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens) on "survived" remains open at the registry-eligibility layer.

**Explicitly NOT promising:** an answer to D7-U-1 §7 OQ-1 — *what counts as "opposing-enough"* between two open-weights families fine-tuned from the same base, or whether a deterministic checker generated by the builder model counts as opposing. Eligibility-predicate calibration is a Phase-4+/Phase-8 question deferred from this ADR.

## References

- [P-33 primitive sketch](../../architectures/v3/primitives/P-33-opposing-side-router.md) — construction path, three-layer denylist, do-not-unify discipline.
- [Phase-4.2 overlap analysis § P-33 vs P-14](../../architectures/v3/primitives/overlap.md#p-33-vs-p-14--opposing-side-router-vs-judge-router) — DISTINCT verdict (verbatim text-pulled in Context).
- [D7-U-1 substrate-requirements summary § P-33](../../architectures/v3/substrate-requirements/d7-u-1.md) — `(artifact-kind × method × builder.family)` input contract.
- [ADR 0016 P-14 judge router](0016-p-14-judge-router.md) — shared LiteLLM Router substrate, distinct routing-policy contract.
- [F46 single-model review blindspot](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot) + [F48 tacit collusion via shared context](../../architectures/v3/failure-modes-v3.md#f48--tacit-collusion-via-shared-context) — forcing failure modes.
