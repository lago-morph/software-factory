# Spec: `silent-absorption-precedence-with-confidence`

- **ID**: SKILL-SPEC-3c5b9e8f47
- **Source retrospective**: ../2026-05-27-191.md

## Intent

When a parallel fanout has both per-candidate / per-spec subagents AND a fresh-context audit subagent (e.g., a silent-absorption auditor) that may produce findings overriding the per-candidate subagents' verdicts at lead-agent aggregation, the silent-absorption-precedence-with-confidence pattern requires the audit subagent to label each finding with a 3-tier confidence (`high` / `medium` / `low`) and applies a strict precedence rule: only `high`-confidence findings override per-candidate verdicts; `medium` triggers a `tbd` reconciliation row; `low` is informational only. Per-candidate `not-applicable-to-candidate-mandate` is NEVER overridden — structural mandate-mismatch is not re-litigable by an auditor. The pattern preserves per-candidate scoping-principle while still allowing the audit subagent's fresh-context-advantage to catch silent absorptions the per-candidate subagents missed.

## Trigger

Direct user phrases:
- "how do I reconcile auditor findings against per-candidate verdicts?"
- "the auditor disagrees with per-candidate subagents on these cells — who wins?"
- "should the auditor's findings override per-candidate verdicts?"

Proactive triggers:
- Any aggregation step in a parallel fanout where both fresh-context audit subagents AND per-candidate workers have produced verdicts on overlapping cells.
- When authoring a dispatch brief that includes both per-candidate fanout AND a fresh-context bias-guard / verifier — name the precedence rule + confidence threshold inline.

Negative triggers:
- Single-subagent verification (no per-candidate fanout to reconcile against).
- Audit subagent's findings are advisory-only, not overrides (no precedence question).

## Inputs

- Per-candidate / per-spec subagents' verdicts on cells (one verdict per cell per candidate; canonical taxonomy: `absorbed | rejected (reason) | not-applicable-to-candidate-mandate | tbd` or project-equivalent).
- Audit subagent's findings, each labeled with a 3-tier confidence (`high` / `medium` / `low`) and pointing at a specific (spec, spec-section, archive-source) tuple.
- Aggregation rubric naming the precedence rule.

## Outputs

- Aggregation file's reconciliation section, with one row per disagreement cell showing: per-candidate verdict, auditor finding (with confidence label), precedence resolution (override / `tbd` / informational), and reconciliation-action description.
- `tbd` rows surfaced as design inputs to the downstream-phase brief (Phase-7 → Phase-8 lean-eval design).

## Workflow

1. **At dispatch time**: the audit subagent's dispatch brief carries a verbatim confidence-labeling requirement: *"For each silently-absorbed finding, label with confidence `high` (verbatim or near-verbatim phrase from archive appears in spec without citation) / `medium` (semantic equivalence in spec without citation; arguable) / `low` (lineage suggestive but not concrete)."*
2. **The aggregation file's reconciliation rubric carries the precedence rule verbatim**: *"Only `high`-confidence findings override per-candidate `rejected` verdicts; `medium` triggers a `tbd` reconciliation row for lead-agent / user adjudication; `low` is informational only. Per-candidate `not-applicable-to-candidate-mandate` is NEVER overridden at any confidence level."*
3. **At aggregation time**, for each cell where audit subagent's finding overlaps per-candidate's verdict:
   - If per-candidate said `absorbed` (any variant) AND auditor said `silently absorbed at confidence X`: per-candidate verdict stands; auditor finding is a citation-gap flag, not an override (the cell becomes `absorbed (silently, X-confidence — flagged for downstream-phase cite)`).
   - If per-candidate said `rejected` AND auditor said `silently absorbed at confidence high`: override to `absorbed (silently, high-confidence)`.
   - If per-candidate said `rejected` AND auditor said `silently absorbed at confidence medium`: cell becomes `tbd`; surface for lead-agent / user adjudication.
   - If per-candidate said `rejected` AND auditor said `silently absorbed at confidence low`: per-candidate verdict stands; auditor finding informational.
   - If per-candidate said `not-applicable-to-candidate-mandate`: per-candidate verdict stands at ALL confidence levels.
4. **`tbd` cells are surfaced to the downstream-phase brief** (Phase-8 lean-eval brief design inputs) — they're per-candidate design questions, not aggregation-time blockers.

## Concrete examples

### Example 1: Phase-7 silent-absorption auditor (actual session)

- **Auditor input**: 10 Phase-6 specs + 9 archive files (no per-candidate audit outputs — those don't exist at dispatch time because bias-guards ran concurrent with per-candidate fanout).
- **Auditor returned**: 15 findings labeled by confidence — 3 high / 7 medium / 5 low.
- **At aggregation** (verbatim from `architectures/v3/backfill-notes.md` §3):
  - 3 high-confidence findings applied precedence — but didn't actually override anything because per-candidate verdicts on those 3 cells were already `absorbed (with adaptation)`. The cells became `absorbed (silently, high-confidence — flagged for Phase-8 cite obligation)`.
  - 7 medium-confidence findings became `tbd` reconciliation rows. Lead-agent decision: defer to Phase-8 lean-eval design — each `tbd` cell becomes a per-candidate brief design input asking "is the candidate's framing distinguishable from the archive item, or silent inheritance worth citing?"
  - 5 low-confidence findings were informational only.
- **Result**: ~12 spurious cell-overrides prevented (7 medium + 5 low that would have overridden per-candidate `rejected` verdicts in a no-threshold regime).

### Example 2: ADR-0036 framing drift (Phase-6-followup #1, folded into Phase-7 silent-absorption auditor mandate)

The auditor's expanded mandate folded the Phase-6-followup #1 carry-forward (BF-L "commodity dispatch surface" vs U-A/D7-U-1 "registrar-framework" framing of ADR 0036). The auditor's audit output ([`audit-silent-absorption.md` §B.2](architectures/v3/backfill-notes/audit-silent-absorption.md)) confirmed 3-way drift across BF-L (commodity-dispatch), U-A (event-driven registrar-framework), D7-U-1 (timer-driven registrar-framework). Each framing is internally consistent within its candidate's spec — the drift is at the cross-spec characterization level.

The precedence rule resolution: per-candidate `§N.3 ADR-0036 framing` entries in BF-L / U-A / D7-U-1's notes files (added per [auto-007 Reviewer 5 Defect 2 amendment](architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md#round-2-reviewer-findings)) carry verbatim cites from each candidate's §0 ADR-citation index row. The cells are `absorbed (verified)` per-candidate; the auditor's cross-spec finding is `informational` (high-confidence about the drift's existence but not an override of any per-candidate cell). Resolution: glossary-amendment opportunity, NOT a Phase-7 spec patch. Phase-6-followup #1 closed at aggregation.

## Anti-patterns

- **No confidence labeling.** Without a 3-tier label, fresh-context auditor findings act as binary overrides at aggregation. The Phase-7 auditor would have produced 15 forced overrides, including 12 that were low- or medium-confidence guesses moving authority from per-candidate subagents (heavy context) to a single auditor read (less context). This is exactly the failure mode Reviewer 5 (scoping-skeptic) caught in Round 2 Defect 3.
- **Overriding per-candidate `not-applicable-to-candidate-mandate`.** The not-applicable verdict reflects structural mandate-mismatch — Architecture-4-Tournament primitives audited against GF-S, for instance. An auditor cannot re-litigate structural mandate-mismatch; the precedence rule must NEVER override `not-applicable` at any confidence level.
- **Treating `medium` and `high` as the same.** Medium-confidence findings are arguable semantic equivalence; high-confidence are near-verbatim phrase matches. Lumping them together either over-overrides (treating medium as high) or under-overrides (treating high as medium); both lose calibration.
- **Lazy auditor labeling.** If an auditor labels every finding `medium`, the confidence threshold loses signal. The dispatch brief must require the auditor to actually distinguish high (specific evidence: verbatim phrase + section ref) vs medium (semantic equivalence; arguable) vs low (lineage suggestive). Phase-7 auditor produced 3/7/5 distribution — a healthy spread.

## Acceptance criteria

- [ ] Audit subagent's dispatch brief requires 3-tier confidence labeling for every override-eligible finding.
- [ ] Aggregation file's reconciliation rubric carries the precedence rule verbatim.
- [ ] `not-applicable-to-candidate-mandate` verdicts are NEVER overridden, at any confidence level.
- [ ] Medium-confidence findings produce `tbd` rows surfaced as downstream-phase design inputs.
- [ ] No silent overrides: every reconciliation cell carries an explicit (verdict, confidence, resolution) tuple in the aggregation matrix.

## Files this skill creates / modifies

- `<audit-subagent-dispatch-brief>` — adds confidence-labeling requirement.
- `<aggregation-file>` — adds reconciliation section with precedence rule verbatim and per-cell resolution rows.
- `<downstream-phase-brief>` (next phase) — inherits `tbd` reconciliation cells as design inputs.
