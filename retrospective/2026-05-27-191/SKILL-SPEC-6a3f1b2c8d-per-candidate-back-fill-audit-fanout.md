# Spec: `per-candidate-back-fill-audit-fanout`

- **ID**: SKILL-SPEC-6a3f1b2c8d
- **Source retrospective**: ../2026-05-27-191.md

## Intent

Encapsulate the per-candidate parallel-fanout + bias-guards-concurrent + omnibus-PR + lead-agent-matrix-aggregation pattern used in Phase 7 of the v3 architecture synthesis (auto-007) for **any** "audit a body of prior art against the current set of candidates" pass. Phase 7 ran 9 per-candidate back-fill subagents + 2 bias-guard subagents (silent-absorption auditor + historian) in **one parallel wave** producing 12 disjoint files, then lead-agent aggregated into a single matrix view (`backfill-notes.md`) and decided spec-patch firing per a candidate-count threshold. The pattern works because (a) each candidate's notes file is uniquely-named so concurrent writes can't collide; (b) bias-guards' input streams (specs + archive) are independent of per-candidate output, so they can fire concurrent rather than waiting; (c) a lead-agent-authored exemplar with a passing self-check gates the fanout, holding shape consistency across 9 sibling subagents; (d) the matrix view is a derived read-only artifact rather than a concurrent-write target.

## Trigger

User says "audit the archive against the current candidates", "back-fill audit", "per-candidate audit pass against prior-phase material", "do a phase-N back-fill", or any structurally-equivalent ask where N candidates need parallel independent audits against the same shared body of prior art. Proactive trigger: any multi-candidate synthesis phase whose plan says "the audit runs per candidate". Negative trigger: skip when only 1-2 candidates (no fanout benefit) OR when candidates' notes files MUST share state (Option D in auto-007 — aggregation-only file with concurrent writers; rejected because of merge-conflict surface).

## Inputs

- The set of N candidates (each with a Phase-(N-1) spec at a known path).
- The archive scope (enumerated body of prior-phase material, typically 5-15 files).
- A decision brief (`auto-NNN`) that names the wave shape, rubric, classification taxonomy, word-budget tier table, self-check rubric, and bias-guard mandates. The brief MUST have passed two rounds of real adversarial review per `AGENTS-MD-d72e1a4f3c`.
- The lead-agent-authored exemplar (one candidate's notes file, authored before fanout per `AGENTS-MD-eec503a3c2`).
- The full enumeration of fixed paths each subagent will write to (each per-candidate file uniquely named, bias-guard files at fixed audit-filenames, aggregation at top-level).

## Outputs

- N-1 per-candidate notes files at `<scope>/<candidate-id>.md` (one per sibling subagent; exemplar's file authored by lead before fanout).
- M bias-guard audit files at `<scope>/audit-<kind>.md` (one per bias-guard).
- 1 lead-agent-authored aggregation file with cross-candidate matrix + per-finding reconciliation rows.
- Optionally: 0+ spec patches (Wave N.3) OR a matrix-flag aggregation row IF auditor recommends + patch-count would exceed deferral threshold (see ADR-b4e7c2a9d6).
- 1 omnibus PR consolidating all fanout files per `AGENTS-MD-d71e845b29`.

## Workflow

1. **Read** the decision brief, confirm Round-2 closed with all reviewers `accept-with-named-amendments` or better.
2. **Choose exemplar candidate** = the least-contested candidate (single dominant prior-phase lineage; no flagged-RG items; smallest absorption surface).
3. **Author exemplar inline**: produce the full rubric-conformant notes file, run self-check items (a)-(g), commit. If any item fails (especially enumeration-floor item (d)), re-author before fanout.
4. **Dispatch fanout wave** (N-1 per-candidate subagents + M bias-guards) **in one parallel call**. Each subagent receives: the brief, the exemplar, its candidate's spec, the archive files, the candidate-registry entry, and verbatim cites of every AGENTS-MD rule the rubric references.
5. **Commit subagent outputs in batches** as the stop-hook fires during the wait — preserves sandbox work.
6. **Author aggregation file**. One section per archive file × N candidate columns; populate from per-candidate files; add reconciliation rows for any bias-guard `high`-confidence findings per the silent-absorption-precedence rule (SKILL-SPEC-3c5b9e8f47).
7. **Decide Wave N.3** (spec patches): count candidates that need patches. If `≤ deferral_threshold`, fire patches as omnibus. If `> deferral_threshold` AND auditor recommended a matrix-flag alternative, prefer matrix-flag + downstream-phase cite-obligation per ADR-b4e7c2a9d6. Document the decision in the aggregation file.
8. **Commit aggregation** + open omnibus PR with per-cluster sectioning preserved in the description.
9. **Author Phase-N-close handoff** noting Wave-N.3 outcome + any carry-forwards.

## Concrete examples

### Example 1: Phase-7 back-fill audit (the originating session)

10 candidates (GF-S, GF-M, GF-C, BF-S, BF-M, BF-L, U-A, U-B, U-C, D7-U-1) × 9 archive files. BF-S chosen as exemplar (single dominant Atelier-primary lineage). Exemplar landed at 5698 words (over Light tier 5000) → flagged in `exemplar-budget-flag:` YAML but accepted; sibling subagents told they may land at 5000-5700. Wave 7.1+7.2 fired 11 subagents in one call; all returned `accept-as-is` or `accept-with-named-amendments` in ~13 minutes. Lead-agent aggregated at `architectures/v3/backfill-notes.md`. Silent-absorption auditor returned 15 findings (3 high / 7 medium / 5 low); per the confidence-threshold rule only the 3 high overrode any per-candidate verdicts. Wave 7.3 decision: 7+ candidates would have needed patches → matrix-flag adopted (ADR-b4e7c2a9d6); zero patches fired. Omnibus PR (PR #190) carried all 12 files.

### Example 2: Reusable shape for a "back-fill against deprecated framework FR-X" audit

Hypothetical: 6 services × 4 deprecated-FR-X docs. Choose service-with-shallowest-FR-X-usage as exemplar; author exemplar `services/<id>/fr-x-audit.md`; fanout 5 subagents + 1 bias-guard (cross-service auditor checking for silent inheritance of FR-X idioms); aggregate into `services/fr-x-audit-matrix.md`. Wave-3 spec patches conditional on per-service migration debt; matrix-flag alternative if patch count > 3.

## Anti-patterns

- **Fanout-without-exemplar**. Violates `AGENTS-MD-eec503a3c2`; sibling subagents drift in §-structure, classification token usage, and citation discipline. Caught at aggregation when matrix rows don't align.
- **Bias-guards-after-fanout**. Wastes a full fanout wall-clock; bias-guard input streams are independent of per-candidate output (they read specs + archive only). See ADR-3f8c1e5b7a.
- **Aggregation-as-subagent**. Aggregation requires the cross-candidate read; a subagent dispatched to "write the aggregation" lacks the lead's full context. Lead-agent authoring at fanout-close is strictly cleaner.
- **Per-mandate sub-wave PRs when files are disjoint**. Repeats the Phase-6 learned-the-hard-way pattern; collapse to omnibus per `AGENTS-MD-d71e845b29`.

## Acceptance criteria

- [ ] Exemplar self-check items (a)-(g) all pass (or item (a) flagged in `exemplar-budget-flag:` and accepted with sibling-subagent guidance) before Wave N.1 dispatch.
- [ ] All fanout subagents (per-candidate + bias-guard) fire in ONE parallel call, not sequentially.
- [ ] Each per-candidate file is uniquely-named; no two subagents write to the same path.
- [ ] Aggregation file carries a reconciliation row for every `high`-confidence bias-guard finding.
- [ ] Wave-N.3 decision (patches vs matrix-flag vs deferral) is documented in the aggregation file with explicit reasoning and user-override path.

## Files this skill creates / modifies

- `<scope>/<candidate-id>.md` — N per-candidate notes files (one per fanout subagent).
- `<scope>/audit-<kind>.md` — M bias-guard audit files (one per bias-guard).
- `<scope>.md` — top-level aggregation matrix file (lead-agent authored).
- `architectures/v3/decisions/auto-NNN-*.md` — decision brief (input to this skill, authored before fanout).
- `SESSION-HANDOFF-<DATE>-phase-N-close.md` — phase-close handoff naming carry-forwards.
