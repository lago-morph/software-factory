# ADR 7e5c2af193: §0 ADR-citation index table is the testable framework + per-variant pairing surface

## Status
Proposed (retrospective draft from 2026-05-26 Phase-6 run).

## Context

[AGENTS-MD-a9fb7b42f8](../../AGENTS.md#framework-adr-scope-boundary-discipline) requires that any spec citing a framework ADR (currently P-19 / P-28 / P-29 / P-30) MUST also cite the candidate's per-variant ADR. At Phase-6 dispatch time, the question arose: how is this rule mechanically tested?

Initial draft of the Phase-6 spec rubric (auto-006 Round 1) said specs MUST pair framework with per-variant in the §References section. But `grep` for the pairing across a spec's prose can't verify co-location — a spec could cite ADR 0050 in §6 References and ADR 0028 in §3 Methodology and they would never be co-located in any local context, making the pairing untestable by single-pass tooling.

Reviewer 2 (Round 1 spec-quality auditor) raised this: "Framework-ADR + per-variant cross-reference floor is not mechanically testable."

## Decision

**Every Phase-6 architecture spec MUST include a mandatory §0 "ADR-citation index" markdown table as the first section after the YAML frontmatter.** Columns: `ADR ID | Title | Layer | Variant of | Citing §`. Sort ascending by ADR ID. The `Variant of` column is `—` (em-dash) for non-per-variant ADRs and the parent framework ADR ID (4-digit zero-padded) for per-variant ADRs.

This makes the framework + per-variant pairing rule **mechanically testable** as a single-row grep:
- `grep -E "^\| 0028 " <spec>` returns the framework row.
- `grep -E "^\| .* \| 0028 " <spec>` returns rows where Variant-of = 0028 (i.e., per-variant ADRs of the framework).
- Pairing rule: if the first grep returns a row, the second must return ≥1 row.

Verifier 1 (in the Phase-6 verification subagent's scope) executes this check as item B.3.

## Alternatives considered

**A. Pair in prose (one paragraph in §2 that names both ADRs).** Rejected: prose-level pairing is unverifiable by tool; requires manual cross-checking.

**B. Single References section listing all ADRs with annotation.** Rejected: the alphabetical / numerical ordering separates framework + per-variant ADRs (e.g., 0028 and 0058 are 30 rows apart), losing the single-row grep target.

**C. Two-table format (framework + per-variant tables).** Rejected: adds authoring overhead; doesn't survive in the verifier's grep without cross-table joining.

## Consequences

**Easier.** Verification reduced from "read all prose for cross-references" to "grep §0 table". Verifier B.3 runs in seconds. The §0 table also serves as a navigation aid for spec readers.

**Harder.** Spec authors must maintain the §0 table consistency with prose citations — every ADR cited in §1-§7 should appear in §0. Self-check (e) `grep -cE "^\| 0[0-9]+ " <spec>` verifies row count against expected ADR set; self-check (g) `grep` per framework-ADR row verifies non-empty Variant-of.

## References

- [AGENTS-MD-a9fb7b42f8](../../AGENTS.md#framework-adr-scope-boundary-discipline) — framework-ADR scope boundary discipline (the rule this ADR makes testable).
- [auto-006 Round 1 Reviewer 2 Amendment 4](../../architectures/v3/decisions/auto-006-phase-6-dispatch-shape.md#reviewer-2--spec-quality-auditor-accept-with-named-amendments) — the objection that drove this decision.
- [auto-006 Round 2 revised per-spec rubric](../../architectures/v3/decisions/auto-006-phase-6-dispatch-shape.md#revised-per-spec-rubric-round-2-amendments-folded-in) — the rubric making §0 mandatory.
- [Phase-6 verification findings § A.2 + B.3](../../architectures/v3/phase-6-verification-findings.md) — verifier confirming the pairing check works in practice.
- All 10 Phase-6 specs at [`architectures/v3/specs/`](../../architectures/v3/specs/) — exemplars of the §0 table format.
