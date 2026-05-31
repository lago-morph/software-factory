# Spec: `verify-before-write-during-apply`

- **ID**: SKILL-SPEC-48bc990036
- **Source retrospective**: ../2026-05-31-218.md

## Intent

Apply phases — when a planned edit set is about to be folded into target artifacts — are deceptively risky because the planner often pattern-matched against artifact summaries, not the artifacts themselves. This skill enforces a verify-before-write discipline: for each intended edit, read the target file in full, check whether the minimal form is already present, and check whether the edit would overturn a deliberate prior decision the original author flagged as load-bearing. Apply only genuine gaps. Report no-ops explicitly — they are the proof the canonical was already correct.

## Trigger

**Direct triggers:**
- Operator says "apply", "go", "do it", "fold it in" after a planning phase
- Apply phase of a survivor-pass, decision survey, integration pass, or migration plan
- Any time a list of intended edits to existing artifacts has been compiled before opening any of those artifacts

**Proactive trigger:**
- You're about to write to N target files based on a plan/summary, but you haven't read those target files in full in this session.

**Negative trigger:**
- The "apply" is creating new artifacts that don't exist yet (no canonical to verify against).

## Inputs

- The plan: a list of intended edits, each tied to a target file path and a minimal form to add.
- Read access to each target file.
- The criterion/bar under which the edit was planned, expressed concretely enough to recognize "already there" vs "needs to be added."

## Outputs

- For each intended edit: a verdict (`already-in` / `apply` / `reclassify-drop` / `reclassify-defer`) with a one-sentence reason citing the artifact's specific text.
- The edit, applied, where the verdict is `apply`.
- A summary report: counts by verdict, the reclassifications surfaced for operator awareness.
- Updated planning artifact (the survivor-pass ledger, the migration plan, etc.) reflecting the apply outcomes.

## Workflow

1. **List intended edits as a table.** Columns: intended edit identifier, target file path, minimal form to add, and the bar under which the edit was planned. Don't open any target files yet.
2. **Read each target file in full.** Not just the section you think the edit goes in — the whole file. The original author's framing, NOT bullets, and AMBIGUITY blocks often live elsewhere and turn out to be decisive.
3. **For each intended edit, render a verdict against the artifact's specific text.** Four outcomes:
   - **`already-in`**: the minimal form is present (possibly under different vocabulary; recognize the *capability*, not just the wording). Mark no-op.
   - **`apply`**: the minimal form is genuinely absent. Add it surgically — strengthen an existing FILL, add a small bullet, add a sentence. Do not rewrite sections.
   - **`reclassify-drop`**: the edit would overturn a deliberate decision the canonical author flagged (e.g., a load-bearing choice between two readings of an ambiguity). The bar interpreted concretely says drop. Flag for the operator.
   - **`reclassify-defer`**: the edit adds real capability but the consumer doesn't exist yet (e.g., scoreable DoD interface, but no satisfaction-scorer yet built). Defer to a triggered enhancement.
4. **Apply only the `apply`-verdict edits.** Keep the surgical-edit discipline: one or two paragraphs of the canonical artifact at a time, never wholesale rewrites.
5. **Report no-ops, applies, and reclassifications separately** in the summary back to the operator. The reclassifications need to be surfaced for awareness; the no-ops need to be visible as proof of "the canonical was correct."
6. **Update the planning artifact** (ledger, plan doc, integration pass record) to reflect the apply outcomes with the same verdict vocabulary.

## Concrete examples

**Example 1: v4 SURVIVOR-PASS apply (this session, PR #218).** Planned: fold 25 KEEP-MINIMAL deltas into canonical specs. Apply phase read all 12 keep-bearing canonical specs in full. Verdicts: 21 `already-in` (faithful's minimal-fills charter had already produced the same minimal forms — e.g., C20 bead-type catalog, C24 bridge invariants, C42 3-role taxonomy), 3 `reclassify-drop` (C08-01/02 + C09-01 would have reversed faithful's deliberate spec/template collapse, flagged in C08 OQ-1 as load-bearing), 1 `reclassify-defer` (C08-03 enumerated-DoD is real P5 capability but its consumers C32/C33 are unbuilt → FE-5). Net edits: 0. Reported back: "the apply is essentially a no-op and that's the right outcome." Two of the reclassifications surfaced material the operator hadn't seen explicitly.

**Example 2: a hypothetical migration apply.** Planned: rename `getUserById(id)` to `getUserByPk(id)` across 47 call sites. Verify-before-write reads each call site. Finds: 30 are direct sites where rename is safe (`apply`), 12 are already using a wrapper `getUser(opts)` that internally calls the old name (effectively `already-in` for the migration's goal of "no direct getUserById calls"), 4 are in test files where the legacy name is intentionally preserved to test backward compat (`reclassify-drop`), 1 is in a comment block (`apply` as documentation update). Net: 31 surgical edits, 12 no-ops, 4 surfaced for operator awareness.

## Anti-patterns

- **"I already scored each item; the apply is mechanical."** No. The score was a summary; the artifact is the source of truth. Always re-read.
- **Reading just the section you think the edit targets.** The framing, the load-bearing AMBIGUITY blocks, the OQ list, and the cross-component notes often decide the verdict. Read the whole file.
- **Silently overturning a flagged decision.** If the original author wrote "this is the load-bearing call, the alternative is X (flagged as the integrator's decision)", do NOT pull in the alternative without surfacing the reversal to the operator.
- **Failing to report no-ops.** No-ops are not invisible work; they are the proof that the canonical was correct. Report them in the summary count.
- **Wholesale-rewriting a section when a surgical edit would do.** Surgical means: strengthen a one-paragraph FILL, add a bullet, add an invariant to a list. Not "I rewrote §4 to fold in the new contract."
- **Continuing to apply after multiple reclassifications.** If 2+ intended edits reclassified on close read, pause and have the operator re-examine the plan. The pattern-match assumptions that produced the plan are leaking.

## Acceptance criteria

1. Every intended edit gets a verdict tied to specific text in the target file (citation: file path + paragraph or invariant name).
2. The summary counts `already-in`, `apply`, `reclassify-drop`, and `reclassify-defer` separately.
3. Reclassifications are surfaced in the operator-facing summary, not just in the updated planning artifact.
4. No-ops are reported as work-done (verification work), not absent from the report.
5. No artifact is edited without first being read in full.

## Files this skill creates / modifies

- Modifies: the target files for `apply`-verdict edits (surgical).
- Modifies: the planning artifact (ledger / migration plan / integration pass record) to reflect apply outcomes.
- Creates: a short apply-summary report attached to the operator-facing message (or as a section in the planning artifact).
