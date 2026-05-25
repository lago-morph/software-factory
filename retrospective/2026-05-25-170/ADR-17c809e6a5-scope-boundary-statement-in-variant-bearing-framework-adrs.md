# ADR: Scope-boundary statement in variant-bearing framework ADRs

- **ID**: ADR-17c809e6a5
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-170.md
- **PRs covered**: #165, #167

## Context

Phase-5 ADR dispatch separates **framework** (common) ADRs from **per-variant** (candidate-specific) ADRs. Per the [overlap.md Phase-4.2 analysis](../../architectures/v3/primitives/overlap.md), four substrate primitives have variant complexity: P-19 eligibility/regime classifier (4 distinct feature sources across candidates), P-28 typed-object store (4 distinct envelope schemas), P-29 policy mediator (3 distinct policy DSLs), P-30 event registrar (2 DISTINCT state machines on shared Temporal substrate). Wave 5.1b of the 2026-05-25 run authored framework ADRs for these primitives (0028, 0029, 0030, 0036), with per-variant ADRs deferred to Wave 5.3 next run.

The auto-005 Round-2 pre-mortemer reviewer surfaced a specific failure mode: a Phase-6 architecture-spec author could cite "the P-30 ADR" for state-machine semantics without realizing the common ADR covers Temporal substrate only — the U-A re-entry-interval and D7-U-1 survival-window state machines are separate per-variant ADRs in Wave 5.3. Without an explicit scope-boundary in the framework ADR's Consequences section, the silent under-reference erodes Phase-6 spec correctness.

The auto-005 Round-2 amendment required each Wave-5.1b subagent's brief to mandate a scope-boundary statement in the Consequences section of the produced ADR. All four (P-19, P-28, P-29, P-30) complied; ADR 0036 (P-30) carried the verbatim DISTINCT-primitives scope warning per AGENTS-MD-bf4431be57.

## Decision

**Common ADRs for substrate primitives that have deferred per-variant ADRs MUST carry an explicit scope-boundary statement in their `## Consequences` section naming (a) the variant landscape, (b) the deferral target (next run / wave / phase), (c) the cross-reference requirement for downstream consumers.** The required form: "Per [parent decision brief], this ADR's scope is [framework-element] only. [Downstream phase] specs MUST reference BOTH (a) this common ADR AND (b) the candidate's per-variant ADR from [deferral target]. Referencing only this ADR for [variant-element] is a known scope error."

## Alternatives considered

- **No rule; rely on Phase-6 spec reviewers to catch under-references.** Rejected because Phase-6 reviewers cannot mechanically distinguish "intentional partial-reference" from "missed-variant under-reference" without reading the framework ADR + every per-variant ADR + the candidate's substrate-requirements summary — high cognitive load that the scope-boundary statement eliminates.
- **Inline the variant content in the framework ADR.** Rejected because variant content is non-overlapping across candidates (per overlap.md verdicts); inlining N variants into the framework ADR produces a long, multi-conclusion ADR violating the [adr skill](../../.claude/skills/adr/SKILL.md)'s one-decision-per-file convention.
- **Defer the framework ADR until variants exist.** Rejected because the framework decision (e.g., Temporal vs EventBridge for P-30) is independent of variant semantics and benefits from being settled early — Wave 5.1b lands now; Wave 5.3 builds on top.

## Consequences

**Easier:** Phase-6 architecture specs have an explicit, in-ADR pointer to "look here for variant semantics." Cross-reference completeness becomes auditable: a Phase-6 spec that cites a framework ADR but no per-variant ADR is mechanically flaggable. The scope-boundary text serves as documentation for downstream agents who may not know about the variant landscape.

**Harder:** Each variant-bearing framework ADR has 3-5 extra sentences in Consequences (a small authorial cost). Authors of new framework ADRs must check whether their primitive has variant complexity at the overlap.md level before deciding whether the rule applies.

**Trade-off accepted:** A small ADR-length tax in exchange for cross-reference correctness.

**Explicitly NOT promising:** the rule does not apply to framework ADRs for primitives with no variant complexity (e.g., P-01 sandbox; P-08 scenario storage). For those, no per-variant ADRs exist and no scope-boundary is needed.

## References

- [`../2026-05-25-170.md`](../2026-05-25-170.md) — source retrospective.
- [`./AGENTS-MD-a9fb7b42f8-framework-adr-scope-boundary-discipline.md`](./AGENTS-MD-a9fb7b42f8-framework-adr-scope-boundary-discipline.md) — per-rule agents-file addition.
- [`../../docs/adr/0036-p-30-event-registrar-substrate.md`](../../docs/adr/0036-p-30-event-registrar-substrate.md) — exemplar of the discipline in practice (verbatim DISTINCT-primitives scope warning).
- [`../../docs/adr/0028-p-19-eligibility-regime-classifier.md`](../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [`../../docs/adr/0029-p-28-typed-object-store.md`](../../docs/adr/0029-p-28-typed-object-store.md), [`../../docs/adr/0030-p-29-policy-mediator.md`](../../docs/adr/0030-p-29-policy-mediator.md) — three more applications of the rule.
- [`../../architectures/v3/primitives/overlap.md`](../../architectures/v3/primitives/overlap.md) — the variant landscape source.
- PRs: #165 (auto-005 Round 2 added the requirement), #167 (Wave 5.1b ADRs applied it).
