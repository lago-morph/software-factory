# Spec: `failure-mode-coverage-matrix`

- **ID**: SKILL-SPEC-642714d0fa
- **Source retrospective**: ../2026-05-29-211.md

## Intent

When evaluating an architectural plan that has a defined set of failure modes catalogued, produce an explicit coverage matrix that maps every catalogued failure mode against the plan's mechanisms with a four-class status (Addressed, Partial, Gap, Caution). Forces honesty about gaps and surfaces cautions where the plan's design could worsen a failure if not actively guarded. Catalogued failure modes that go unmapped are silent risks; the matrix makes them visible.

## Trigger

**Direct triggers**:
- "How do our failure modes map to the plan?"
- "What does the plan miss?"
- "Where are the gaps?"
- Slash-command: `/coverage-matrix <plan-doc> <failure-catalog>`.

**Proactive triggers**:
- An architecture proposal is about to ship without an explicit failure-mode coverage evaluation.
- A failure-mode catalog exists in the repo but the latest architecture plan doesn't reference it.
- Decision-makers are reviewing the plan and need an evaluative lens.

**Negative triggers**:
- No failure-mode catalog exists for the domain (the matrix would be subjective).
- The plan is tactical (single file, single feature) — the coverage discipline is overkill.

## Inputs

- Path to the failure-mode catalog (e.g., `architectures/v3/failure-modes-v3.md`).
- Path to the architectural plan being evaluated (e.g., `architectures/v4/README.md`).
- Optional: subset of failure modes to focus on if the catalog is huge (>100 entries).

## Outputs

- A new file at `<plan-dir>/F-MODE-COVERAGE.md` containing:
  - One table per category, grouping failure modes by which plan mechanism addresses them.
  - Status per F-mode: Addressed, Partial, Gap, or Caution.
  - For Cautions: explicit guard discipline required.
  - For Gaps: explicit acknowledgment of residual risk.
- A summary table with overall counts per status.
- A "strongest matches" and "weakest matches" section.
- Recommendations folded back into the plan (concrete action items).

## Workflow

1. **Read the failure-mode catalog.** Extract every F-mode with ID, name, definition, severity per mandate.
2. **Read the architectural plan.** Identify each principle / component / mechanism the plan implements.
3. **For each F-mode**, assess against the plan:
   - **Addressed**: the plan has a clean mechanism that mitigates the failure. Cite the specific mechanism.
   - **Partial**: the plan reduces the failure but doesn't eliminate it. Cite what remains.
   - **Gap**: the plan has no mechanism. Note why (inherent limit, scope choice, systemic).
   - **Caution**: the plan's design could *worsen* the failure if not actively guarded. **This class is the most valuable output of the matrix.** Specify the guard discipline.
4. **Group F-modes by which mechanism addresses them.** Tables organized by Layer / Principle / Component, not by F-number.
5. **Write the matrix file.** Use the structure: per-mechanism tables → summary table → strongest/weakest matches → recommendations.
6. **Surface the Cautions prominently.** A separate section called "Cautions — F-modes the plan might worsen if not guarded" with explicit discipline per Caution.
7. **Fold recommendations into the plan.** Each Caution and each Gap-with-mitigation becomes a concrete action item the plan author can address.
8. **Commit + PR** if the plan is in a PR-shaped workflow.

## Concrete examples

### Example 1: v4 architecture against v3 failure-mode catalog

**Input**: 
- Catalog: `architectures/v3/failure-modes-v3.md` (61 F-modes)
- Plan: `architectures/v4/README.md` + `architectures/v4/AI-CONTEXT.md`

**Output** (excerpted from actual `architectures/v4/F-MODE-COVERAGE.md`):

Summary table:

| Status | Count | Percentage |
|---|---|---|
| Addressed | 24 | 39% |
| Partial | 20 | 33% |
| Gap | 11 | 18% |
| Caution | 4 | 7% |

Cautions section (the load-bearing output):

| F# | Name | Why v4 might worsen | Guard |
|---|---|---|---|
| F52 | Tempting-Wrong-Hybrid | v4's emphasis on self-healing + self-optimization is exactly the "more controller patches" trap | Every guard must point at a falsifying scenario |
| F35 | Federation drift | v4's pack architecture creates the exact failure shape if pack governance isn't first-class | Pack governance must ship in Phase 1 |
| F47 | Goodhart | v4's meta-metric layer creates visible targets | Multi-metric mandatory; no single visible target |
| F25 | Design starvation | v4's runtime is high-throughput | Document honest operator-throughput requirement |

This surfaced 4 design risks that the plan author had not consciously addressed; all 4 became recommendations folded back into the plan.

### Example 2: smaller scope — single layer

**Input**:
- Catalog: focused subset (10 F-modes related to attribution and trust)
- Plan: a new authentication design for a specific component

**Output**: A focused matrix at `<component>/F-MODE-COVERAGE.md` with only the relevant F-modes evaluated. Shorter, equally rigorous.

## Anti-patterns

- **Skipping F-modes you can't easily classify.** "I'll come back to it" → never does. Force the classification; "I don't know" gets classified as Gap with rationale "unevaluated".
- **Optimistic Addressed classifications.** When in doubt between Addressed and Partial, choose Partial. The matrix's value is honest evaluation.
- **Forgetting the Caution class.** Without Caution, you only have "good" and "neutral" — you lose the most valuable signal.
- **Producing the matrix without folding recommendations back.** The matrix is for action, not for filing.
- **Grouping by F-number instead of by mechanism.** F-number-order is hard to read; mechanism-order tells the story.
- **No "strongest matches / weakest matches" section.** This is where the reader learns what the plan is best and worst at, which informs investment.

## Acceptance criteria

1. Every F-mode in the catalog has a status.
2. Every Caution has explicit guard discipline.
3. Every Gap is named (inherent / scope / systemic) with one-line rationale.
4. The summary table shows overall counts.
5. Strongest and weakest matches are called out — at least 3 of each.
6. Recommendations are concrete and actionable, not generic.

## Files this skill creates / modifies

- `<plan-dir>/F-MODE-COVERAGE.md` — new file containing the matrix.
- (Optional) the plan document — additions of "Note: see F-MODE-COVERAGE.md" links and folded recommendations.
