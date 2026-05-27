# Spec: `silent-absorption-precedence-with-confidence`

- **ID**: SKILL-SPEC-3c5b9e8f47
- **Source retrospective**: ../2026-05-27-191.md

## Intent

Encapsulate the reconciliation precedence rule between a *fresh-context audit subagent* (silent-absorption auditor, cross-spec verifier, historian, or any analogous read-only auditor that sees a body of work end-to-end) and a *fanout of per-candidate / per-spec subagents* (each of which sees only its own slice), guarded by a 3-tier confidence label so the fresh-context auditor's low-confidence guesses do NOT silently override per-candidate high-confidence verdicts at lead-agent aggregation. The skill earns its place because Phase 7 (auto-007) discovered empirically that without the confidence threshold, a single fresh-context auditor pass produces ~15 cross-spec findings — and naive precedence ("auditor sees more, auditor wins") would override every per-candidate `rejected` verdict on the cells the auditor touches. With the threshold, only the 3 `high`-confidence findings override; 7 `medium` become `tbd` reconciliation rows; 5 `low` are informational only. This preserves per-candidate scoping-principle authority over the cells where the per-candidate read actually has higher epistemic standing, while still letting the fresh-context auditor catch the genuine cross-spec patterns no per-candidate subagent can see alone.

## Trigger

Direct: user says "the auditor's findings should override the fanout", "fresh-context auditor needs precedence", "silent-absorption reconciliation rule", "how do we handle disagreement between the auditor and the per-candidate subagents?". Proactive: any time a brief plans BOTH (a) per-candidate / per-spec fanout subagents AND (b) a fresh-context audit subagent whose mandate includes cross-cutting findings about the same artifacts the fanout audits. Negative: skip when only one of (a) or (b) exists; skip when the auditor's scope is fully disjoint from the fanout's (no cell-level overlap possible).

## Inputs

- The decision brief (`auto-NNN`) authoring the wave, which MUST already specify the per-candidate and bias-guard subagent set.
- The list of cell-axes the audit and the fanout share (e.g., per-candidate × per-archive-item matrix in Phase 7).
- The set of verdict tokens the per-candidate fanout uses (`absorbed` / `rejected` / `not-applicable` / `tbd` or analogous).
- The fresh-context auditor's dispatch brief draft.
- The aggregation file template (the destination where reconciliation rows land).

## Outputs

- Two paragraphs added to the auditor's dispatch brief: (a) the confidence-labeling instruction (`high` / `medium` / `low`), (b) the per-tier override-behavior statement.
- A `## Reconciliation precedence` section in the aggregation file template that names the three tiers and the cell-update rules.
- Zero new files; this is a brief-and-aggregation amendment skill, not a fanout-creation skill.

## Workflow

1. **Identify overlap.** Enumerate the cell-axes the auditor's mandate covers vs the per-candidate fanout's outputs. If overlap is empty, skip — no precedence question.
2. **Amend the auditor's dispatch brief.** Add the confidence-labeling instruction verbatim: "Label every finding `high` / `medium` / `low`. `high` = the auditor would stake a per-candidate-verdict-override on this; `medium` = the auditor sees a pattern but the per-candidate spec may have sufficient rationale; `low` = informational only, no aggregation-time effect."
3. **Amend the auditor's output schema.** Each finding row in the auditor's output table MUST have a `confidence` column AND a `recommended action` column that reflects the tier (override / tbd-row / informational).
4. **Amend the aggregation file template.** Add a `## Reconciliation precedence` section with the explicit rule: `high` overrides any per-candidate `rejected` on the same cell (cell becomes `absorbed (silently, high-confidence — flagged for cite)`); `medium` triggers a `tbd` reconciliation row for lead-agent adjudication; `low` is recorded for completeness but does NOT trigger any cell update.
5. **At aggregation time, enforce the precedence mechanically.** Walk the auditor's findings; for each `high` apply the override; for each `medium` create the `tbd` row; for each `low` add to an informational appendix only.
6. **Document the count distribution in the aggregation file.** e.g., "Silent-absorption auditor returned 15 findings: 3 high (overrides applied) / 7 medium (tbd rows created) / 5 low (informational)."
7. **Never override `not-applicable-to-candidate-mandate` cells.** The auditor's mandate excludes N/A cells entirely; the override surface is only `rejected` and (for `medium`) `absorbed-without-cite` rows.

## Concrete examples

### Example 1: Phase-7 silent-absorption auditor (the originating session)

The auditor dispatched in Wave 7.2 returned 15 findings against the 10-candidate × 9-archive-file matrix. Findings #1, #2, #3 carried `high` confidence (U-A × `02-compound-atelier.md` §3.2 knowledge-doc category set; 7 candidates × `02-compound-atelier.md` §1 Compound-Engineering four-step loop; 5 candidates × `00-comparison.md` §1 four-architecture taxonomy). Findings #4-#10 carried `medium` (Atelier-derived envelope shapes; reviewer-panel structural analogies; Klaassen plan-prompt naming). Findings #11-#15 carried `low` (informational — including a negative finding for D7-U-1's Popperian framing being NOT in archive). At aggregation: the 3 high findings would have overridden any per-candidate `rejected` verdict, but per-candidate verdicts were already `absorbed (silently)` so no actual override fired; the 7 medium findings became `tbd` reconciliation rows for Phase-8 design input; the 5 low findings landed in the aggregation file's informational appendix. Net effect: zero spurious cell-overrides; complete cross-spec finding capture.

### Example 2: Reusable shape for a cross-package security-vuln auditor

Hypothetical: 12 packages × 30 CVE rows from a fresh-context vuln scanner that sees all packages at once; per-package subagents already produced "patch / mitigate / accept-risk" verdicts based on per-package context. Without confidence labels, the scanner's 90 findings might override 90 per-package `accept-risk` verdicts (the per-package read may have justified the risk acceptance with context the scanner can't see). With confidence labels: scanner labels each finding `high` (exploitable in this package's actual call graph) / `medium` (theoretically reachable; per-package review may have ruled out) / `low` (CVE matches a dependency but no code path uses the affected function). Only `high` overrides per-package `accept-risk`; `medium` triggers a re-review row; `low` is informational. Same shape, different domain.

## Anti-patterns

- **Defaulting to "auditor sees more, auditor wins".** Phase-7 Reviewer 5 (scoping-skeptic) explicitly flagged this in Round 2: the fresh-context auditor's epistemic standing is broader-but-shallower; the per-candidate subagent's is narrower-but-deeper. Override only where the auditor stakes a `high`.
- **Omitting the confidence column from the auditor's output schema.** Without the schema slot, the auditor will not label findings, and lead-agent at aggregation has no mechanical basis to apply the precedence rule.
- **Overriding `not-applicable` cells.** N/A cells are scope-exclusions by per-candidate construction. The auditor's mandate explicitly excludes them; an auditor that proposes overrides on N/A cells is in scope violation.
- **Letting `medium` findings auto-override.** `medium` exists precisely as the "needs lead-agent adjudication" tier; auto-override on `medium` collapses the 3-tier rule back to the binary "auditor wins / auditor doesn't matter" failure mode.

## Acceptance criteria

- [ ] Auditor dispatch brief contains a verbatim 3-tier confidence-labeling instruction.
- [ ] Auditor's output schema has a `confidence` column on every finding row.
- [ ] Aggregation file template has a `## Reconciliation precedence` section naming the per-tier behavior.
- [ ] At aggregation time, the finding-count distribution is documented (e.g., "3 high / 7 medium / 5 low").
- [ ] Zero overrides applied to `not-applicable-to-candidate-mandate` cells.

## Files this skill creates / modifies

- `<scope>/decisions/<auto-NNN>.md` — amend with confidence-labeling instruction + per-tier override-behavior statement in the auditor's dispatch section.
- `<scope>/audit-<kind>.md` — auditor's output file carries the `confidence` column on each finding row.
- `<scope>/<aggregation-file>.md` — carries the `## Reconciliation precedence` section + the per-tier cell updates.
