# ADR 0030: P-29 policy mediator substrate framework

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1b)

## Context

Three candidates claim P-29 policy mediator as a load-bearing substrate primitive: [U-A interval-closure mediator](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch), [U-B per-layer-boundary mediator](../../architectures/v3/tracks/unified-B.md), and [D7-U-1 compounding gate](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-29-policy-mediator.md#buildability-verdict) verdicts the primitive `designed-system`: the policy engine is commodity, the per-variant policy DSL is the load-bearing design content.

Per the [Phase-4.2 overlap verdict](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants):

> **Verdict: SAME primitive (P-29 policy mediator framework), DISTINCT policy DSLs.** All three share the underlying engine (OPA Rego primary; Cedar alternate path per [P-29 sketch](../../architectures/v3/primitives/P-29-policy-mediator.md)). The policy vocabulary differs: U-A reasons about interval-slot satisfaction; U-B reasons about layer-pair closure; D7-U-1 reasons about FC-survival windows. The differences are at the *predicate vocabulary* level, not the *engine* level.

This ADR covers the shared substrate framework — engine choice, policy-loading discipline, bundle-API contract. Per-variant policy DSL vocabularies are deferred to Wave 5.3.

The forcing failure mode is [F53 (voluntary-discipline fragility)](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class): any gate whose enforcement depends on an operator (or LLM) *choosing* to apply it will be skipped exactly under the conditions where it matters. A declarative mediator at the substrate boundary turns the gate into a structural property — the calling primitive *cannot* complete the write without an `allow` verdict. Adjacent F-modes: [F56 (guardrail-bypass under stress)](../../architectures/v3/failure-modes-v3.md#f56--guardrail-bypass-under-stress-replit-class-incident), [F28 (holdout leakage)](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders), [F44 (lethal-trifecta default)](../../architectures/v3/failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default).

## Decision

**Build P-29 as a declarative policy-mediator framework with [Open Policy Agent (OPA) + Rego](https://www.openpolicyagent.org/) as the primary engine and [Cedar](https://www.cedarpolicy.com/) as the supported alternate engine.** The boundary primitive serialises the candidate write/transition to a structured JSON `input` document, invokes the engine against a loaded policy bundle, and keys its commit-or-refuse decision on the structured verdict (`allow: bool`, typed `reasons[]`, `obligations[]`, `audit_envelope`). The verdict is *binding* — the boundary refuses to complete the write unless `allow == true`.

**Policy-loading discipline.** Policy bundles are content-addressed (sha256 over the canonical Rego/Cedar source set) and loaded from a versioned store. The bundle hash is recorded in every verdict's `audit_envelope`, so every gate decision is replayable against the exact policy text that produced it. Bundle changes go through the same review discipline as code (signed commits, ADR if invariants change). Drift between deployed bundle and source-of-truth is a Patrol-monitorable property.

**Bundle-API for L0-standards-versioned policies.** Policies that encode L0 standards (named-discipline ADRs 0018–0027) are loaded as a separate `l0-standards` namespace within the bundle. The mediator exposes a `bundle.l0_standards.version` field so downstream substrate primitives can verify they are running against a compatible standards version before evaluating. Standards-version mismatch is itself a deny condition, not a silent fallthrough.

**Engine selection.** OPA + Rego is the default (CNCF-graduated, broad ecosystem, Kubernetes admission control / Envoy ext_authz / Terraform plan-gating as prior art). Cedar is supported for deployments needing finer-grained per-action/per-resource/per-principal authorisation and formally-verified evaluation semantics; the bundle-API contract is engine-agnostic so a deployment can swap engines without rewriting the calling primitives.

## Alternatives considered

**B. P-29 as three distinct primitives (one per variant).** Treat U-A's interval-closure mediator, U-B's layer-boundary mediator, and D7-U-1's compounding gate as independent primitives with no shared substrate. *Why rejected:* the [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) found the differences are at the *predicate vocabulary* level, not the *engine* level. Three separate engine deployments would triple the substrate ops cost, force three sets of bundle-loading discipline to evolve in parallel, and lose the shared audit/replay machinery. The per-variant differences belong in policy DSL, not engine.

**C. Embed policy logic directly in the calling primitive (no mediator).** Each boundary primitive carries its gate logic inline as code. *Why rejected:* this is exactly the [F53 fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) the mediator is designed to defeat. Inline gate code is editable by anyone who can write to the calling primitive, without policy-bundle review; under time pressure, the gate becomes a comment. The two-part discipline (declarative DSL + boundary enforcement) is load-bearing — separability of policy from code is the property we are paying for.

**D. Use a general-purpose rules engine (Drools, JSON-Logic).** *Why rejected:* general rules engines lack the production substrate-boundary prior art OPA and Cedar have (admission control, ext_authz, Verified Permissions). Rego/Cedar policy text is also human-readable in a way that survives review by non-engine-experts, which Drools DRL does not. Drools remains a viable choice for the [P-19 decision-table classifier](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) per its own sketch, but P-29's substrate-boundary role rules it out here.

## Consequences

**Easier:** F53 mitigation becomes a structural substrate property rather than an operator-discipline ask. All three claiming candidates share one engine deployment, one bundle-loading pipeline, one audit/replay surface. L0-standards-versioned policies get a uniform load-and-version contract. Engine swap (OPA ↔ Cedar) is mechanical, not a methodology-layer rewrite.

**Harder:** OPA/Cedar deployment + bundle-signing infrastructure becomes a per-environment ops requirement. Policy authors need DSL fluency (Rego is non-trivial; Cedar is simpler but newer). Bundle-hash audit-envelope storage adds modest write amplification.

**Explicitly NOT promising — scope boundary.** This ADR covers the **shared engine substrate only** (engine choice, policy-loading discipline, bundle-API). The **per-variant policy DSL vocabularies** are out of scope and deferred to Wave 5.3 as three candidate-specific ADRs: U-A interval-policy schema, U-B layer-boundary schema, D7-U-1 FC-survival schema. Per the overlap verdict, the engine is shared; the predicate vocabulary differs per candidate. A deployment running multiple candidates loads multiple policy bundles on one engine — not multiple engines.

## References

- [P-29 buildability sketch](../../architectures/v3/primitives/P-29-policy-mediator.md)
- [Phase-4.2 overlap verdict on P-29 three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants)
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class), [F56 guardrail-bypass under stress](../../architectures/v3/failure-modes-v3.md#f56--guardrail-bypass-under-stress-replit-class-incident), [F28 holdout leakage](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders), [F44 lethal-trifecta default](../../architectures/v3/failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default)
- Substrate-requirements summaries citing P-29: [U-A](../../architectures/v3/substrate-requirements/u-a.md), [U-B](../../architectures/v3/substrate-requirements/u-b.md), [D7-U-1](../../architectures/v3/substrate-requirements/d7-u-1.md)
- [ADR 0015: P-08 scenario storage with runner contract](./0015-p-08-scenario-storage-with-runner-contract.md) — Wave 5.1a exemplar this ADR mirrors
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md)
