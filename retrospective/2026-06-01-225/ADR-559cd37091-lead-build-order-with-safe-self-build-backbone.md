# ADR: Lead the v4 build order with the safe-self-build backbone and a product-cluster staffing model

- **ID**: ADR-559cd37091
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-01
- **Source retrospective**: ../2026-06-01-225.md
- **PRs covered**: #224

## Context

The implementer build order ([`architectures/v4/implementation-dependencies.md`](../../architectures/v4/implementation-dependencies.md)) originally opened with a single-line "long pole" critical path (`C01 → C02 → C17 → C30 → C32 → C33 → C46 → … → C50`). The operator flagged it as too thin: it ran straight to the self-optimization gate while omitting components the factory genuinely cannot run without (C04 session, C05 sling, C19 beads, C28 agent loop). The deeper problem was that the planning conversation had no canonical *spine* — no agreed answer to "what is the minimum to get the factory to where it can safely build itself, and what is the highest-value thing to build after that?" Without that spine, every breadth-first phase list reads as 57 equally-weighted components, which is the wrong altitude for deciding what to build first.

A second confusion compounded it: the operator did not see why capabilities that ship inside one adopted binary (beads, event bus, config, sessions, reconciler) are listed as separate "components" with dependency arrows, making "install and configure Gas City" look like a dozen separate builds.

## Decision

The implementation-dependencies doc leads with the **25-component safe-self-build backbone** — a vertical dependency slice computed as the closure of `{C53 bootstrap-validation, C43 boundary-typing fence}` plus the run-flow and safety-collar rings (19 → 22 → 25) — organized into six **product-keyed implementation clusters**, followed by a top-ten-next-by-cost/benefit list, ahead of (and reconciled with) the unchanged full-breadth phase view. A `Product → components` table makes explicit that one adoption (e.g. Gas City) discharges many components at once, separating adopt-and-configure work from build-from-scratch work.

## Alternatives considered

- **Keep the one-line long pole, just add the missing nodes.** Rejected: it would still be eyeballed and would still conflate "the deepest chain" with "the minimum to a milestone." The milestone-closure framing is what makes the backbone defensible and computable.
- **Lead with the full breadth (phase-by-phase) and let readers infer the slice.** Rejected: that is the existing failure mode — 57 flat components give no spine for first-build decisions. The breadth view is retained as the reference, not the lead.
- **Express the clusters by abstract workstream only (no product names).** Rejected after operator feedback: keying clusters to named products ("C19 and C23 *mean* Gas City") is what dissolves the "why are these separate" confusion and grounds the adopt-vs-build distinction.

## Consequences

- **Easier:** Sweep-2 and any staffing conversation now have a canonical spine — a defensible "build these 25 first, in these product-clustered workstreams," then a ranked next-ten. The adopt-vs-build distinction makes effort estimation honest (one Gas City install ≠ eleven tickets).
- **Harder / accepted trade-offs:** The backbone is a second view layered over the breadth phases, so the two must be kept reconciled (the doc states the deferred set explicitly to manage this). The backbone also bakes in two corrections — C31 is required, C43 splits per D-20 so C44 defers — which the breadth-view phase tables must stay consistent with. And the whole backbone rests on the unverified G11 Gas City assumption: every "native" cluster member is a claim to verify against a pinned `gc` (D-23), not yet a fact.

## References

- [`../2026-06-01-225.md`](../2026-06-01-225.md) — the source retrospective.
- [`./SKILL-SPEC-45a01d510b-inventory-backbone-closure.md`](./SKILL-SPEC-45a01d510b-inventory-backbone-closure.md) — the procedure that produces a backbone like this.
- [`../../architectures/v4/implementation-dependencies.md`](../../architectures/v4/implementation-dependencies.md) — the doc this decision shapes.
- PRs the decision was made in: #224.
