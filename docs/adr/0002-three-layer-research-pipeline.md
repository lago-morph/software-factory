# ADR 0002: Three-layer research-to-architecture knowledge pipeline

- **Status**: Accepted
- **Date**: 2026-05-21

## Context

The repo accumulates source material in three different shapes — primary-source
reports, condensed cross-source synthesis, and committed architecture specs —
and they have very different durability and authority properties. Without an
explicit contract for what each layer is *for*, the next agent has no way to
know whether to extend a report, fold it into a synthesis, or promote it into
an architecture; and reviewers have no way to know which file is the load-bearing
one when they conflict.

[`research-plan.md`](../../research-plan.md) describes the existing structure
explicitly as a three-stage funnel: provenance → condensation → action. This
ADR codifies that contract so future contributions land in the right layer and
the layers stay honest about their roles. It does *not* attempt to settle the
open question of when and how to collapse the synthesis layer to a single
unified document — that is a sequencing decision, addressed elsewhere.

## Decision

The repo organizes research-to-build knowledge in **three layers with fixed,
non-overlapping purposes**:

1. **Reports (provenance layer)** — [`research/01-38-*.md`](../../research/) +
   [`research/followup/01-14-*.md`](../../research/followup/). Each report
   covers one source (or one tightly-scoped follow-up thread) and exists to
   anchor every downstream claim to a primary source. Reports are **immutable
   in shape**: they are not folded together, not deleted, and not edited to
   reflect later consensus. Errata are appended; superseding analysis happens
   in a later report or in synthesis. Followup reports are the same kind of
   artifact as the main reports — they live in `followup/` only because they
   were dispatched after the initial rounds, not because they have lesser
   status.

2. **Synthesis (condensation layer)** — currently
   [`research/00-synthesis.md`](../../research/00-synthesis.md) (Round 1) and
   [`research/13-round-2-synthesis.md`](../../research/13-round-2-synthesis.md)
   (Round 2). The synthesis layer's job is to produce, from the reports, the
   canonical cross-source artifacts: the failure-mode catalog (F1, F2, ...),
   the consensus list, the tensions list, and the open-questions list. The
   synthesis layer is the **first place actionable claims appear** — reports
   describe what one source says; synthesis says what the corpus, taken
   together, supports. Synthesis files may be superseded by a later
   synthesis but never deleted.

3. **Architectures (action layer)** —
   [`architectures/00-comparison.md`](../../architectures/00-comparison.md)
   plus the four specs ([`01-specification-refinery.md`](../../architectures/01-specification-refinery.md),
   [`02-compound-atelier.md`](../../architectures/02-compound-atelier.md),
   [`03-phase-gated-foundry.md`](../../architectures/03-phase-gated-foundry.md),
   [`04-evolutionary-tournament.md`](../../architectures/04-evolutionary-tournament.md)).
   This is where the project commits to **what to build**. Architecture specs
   cite synthesis (not raw reports) for justification, and they make binding
   choices about substrate, roles, loops, gates, and artifacts. When a
   choice within an architecture is itself architectural — substrate,
   sandbox model, scenario storage, knowledge format, manager-loop primitive —
   it is promoted out of the spec and into an ADR under [`docs/adr/`](.).

Flow direction is strictly one-way: **reports → synthesis → architectures →
ADRs**. Architectures do not cite reports directly except for footnoted
provenance; ADRs do not cite reports directly at all. A claim that has not
made it through the synthesis layer is not yet eligible to drive an
architectural choice.

## Alternatives considered

- **Single unified knowledge document.** Fold reports, synthesis, and
  architectures into one long living doc. Rejected: provenance and
  decisions have different durability — reports are evidence (immutable in
  shape, never deleted), architectures are decisions (revised by superseding
  versions). Conflating them loses the audit trail that the present
  structure exists to provide.

- **Two layers (reports + architectures), no synthesis.** Skip the
  condensation layer and have architectures cite reports directly.
  Rejected: every architecture would re-derive the failure-mode catalog and
  consensus list from scratch, and cross-architecture comparison would lose
  its shared vocabulary. The 38 reports + 14 followups are too many primary
  sources to fan into four architectures without an intermediate layer.

- **Synthesis as the action layer (no separate architectures).** Let the
  synthesis directly state what to build. Rejected: synthesis is descriptive
  ("the corpus supports X"); architecture is prescriptive ("we will build
  X"). The distinction matters because synthesis must remain honest about
  tensions and open questions, whereas architecture must commit. Mixing the
  two produces synthesis that quietly editorializes.

- **Treat followup reports as a different artifact class.** Give
  `research/followup/` a distinct contract from `research/`. Rejected: they
  serve the same provenance function. The directory split records *when*
  they were dispatched, not *what* they are.

## Consequences

What this buys:

- **Clear contribution surface.** A new primary source → a new file in
  `research/` (or `research/followup/`). A cross-source observation → a
  delta into the synthesis layer. A build decision → an architecture spec
  edit or a new ADR. Contributors do not have to guess.

- **Auditable decisions.** Every architectural choice has a citation chain:
  ADR cites synthesis section, synthesis section cites reports, reports
  cite primary URLs. Future-us can audit any decision back to its source.

- **Stable evidence under shifting consensus.** Reports do not need to be
  rewritten when consensus changes; the synthesis layer absorbs the
  revision. This is the property that lets the corpus grow without
  invalidating older work.

What this costs:

- **Maintenance overhead at the synthesis layer.** New reports do not
  automatically appear in synthesis — someone has to do the condensation
  pass. The current state (two synthesis files covering Rounds 1–2 only,
  with F21–F34+ scattered across Rounds 3+ reports and the followups) is
  the visible form of that cost. The fix is a dedicated synthesis pass,
  not a structural change.

- **Duplication risk between synthesis and architectures.** Architecture
  specs are tempted to restate the synthesis findings rather than cite
  them. Convention: architectures cite synthesis by section anchor; they
  do not re-derive.

- **A claim cannot be load-bearing until it reaches synthesis.** A finding
  that lives only in one report — including a fresh followup — is not yet
  eligible to drive an architectural choice. This is the intended
  guardrail, not a bug.

What this is explicitly **not** promising:

- It does not settle whether the two existing synthesis files (Round 1 and
  Round 2) should collapse into a single v3 synthesis, or how many
  architecture specs survive the next revision. Those are sequencing
  decisions that follow from this contract but are not the contract itself.
  See [`research-plan.md`](../../research-plan.md) [§what-enough-research-should-trigger](../../research-plan.md#what-enough-research-should-trigger).

- It does not commit `spec-driven-ai-dev.md` to any specific layer. That
  document predates the three-layer split and its placement is an open
  question (see [`research-plan.md` §what-stays-as-individual-documents-vs-gets-folded](../../research-plan.md#what-stays-as-individual-documents-vs-gets-folded)).

## References

- [`research-plan.md`](../../research-plan.md) [§the-three-layer-pipeline](../../research-plan.md#the-three-layer-pipeline), [§what-enough-research-should-trigger](../../research-plan.md#what-enough-research-should-trigger), [§what-stays-as-individual-documents-vs-gets-folded](../../research-plan.md#what-stays-as-individual-documents-vs-gets-folded), [§one-specific-risk-for-the-greenfield-mandate](../../research-plan.md#one-specific-risk-for-the-greenfield-mandate) — the source document this ADR extracts.
- [`research/00-synthesis.md`](../../research/00-synthesis.md) [§4](../../research/00-synthesis.md#4-failure-modes-any-architecture-must-defend-against), [§3](../../research/00-synthesis.md#3-where-the-sources-disagree), [§2](../../research/00-synthesis.md#2-where-the-sources-agree) — the Round-1 synthesis exemplifying the condensation layer's output (failure modes, tensions, consensus).
- [`research/13-round-2-synthesis.md`](../../research/13-round-2-synthesis.md) [§1](../../research/13-round-2-synthesis.md#1-what-changed-in-the-consensus), [§3](../../research/13-round-2-synthesis.md#3-what-changed-in-the-failure-mode-list) — the Round-2 synthesis demonstrating supersession-by-extension within the condensation layer.
- [`research/INDEX.md`](../../research/INDEX.md) — the catalog of reports in the provenance layer.
- [`research/PLAN.md`](../../research/PLAN.md) [§2](../../research/PLAN.md#2-repository-layout-what-lives-where), [§10](../../research/PLAN.md#10-round-by-round-canonical-reports-lookup-table) — repository layout and the round-by-round report lookup table.
- [`architectures/00-comparison.md`](../../architectures/00-comparison.md) [§7.1](../../architectures/00-comparison.md#71-the-single-recommended-starting-path), [§7.4](../../architectures/00-comparison.md#74-build-the-shared-infrastructure-first) — the action layer's current recommendation and the shared-infrastructure sequencing it depends on.
- [ADR-0001: Use the fetch-blocked-urls action for sandbox-blocked sources](./0001-fetch-blocked-urls-mechanism.md) — example of an ADR extracted from a layer-3 architecture concern (primary-source access for the provenance layer).
