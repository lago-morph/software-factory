# Spec: `parallel-subagent-axis-coordination`

- **ID**: SKILL-SPEC-51fe4d298e
- **Source retrospective**: ../2026-05-24-128.md

## Intent

When N parallel subagents must select from an open set (organizing axis, design pattern, framing choice) and divergence is desired as the design signal, use a two-pass dispatch: pass 1 dispatches each subagent to propose-and-defend its axis in a single paragraph without doing the architecture work; the lead agent reviews; pass 2 dispatches full work with prior picks visible (or with convergent picks prohibited for the convergent subagents). Replaces single-pass independent dispatch, which has a documented prompt-anchored convergence failure mode. This skill exists because in the v3 work, three "pick-your-own-axis" subagents dispatched single-pass produced a convergence (two of three picked the same axis) that was later proven to be at least partly prompt-anchoring. The expensive full dispatch had to be discarded. The two-pass design would have caught the convergence at the cheap pass-1 stage.

## Trigger

**Direct user phrases:**
- "Dispatch N subagents to pick their own [axis / design / framing]"
- "Send three agents to explore alternatives in parallel"
- "Let the corpus tell us which approach is strongest" (paired with parallel dispatch)

**Proactive triggers:**
- The lead agent is about to write briefs for N≥2 parallel subagents whose instructions include "pick your own X" or "decide on an organizing principle for Y."
- The user has previously seen convergence on the same axis from prior parallel runs (signaling either honest corpus signal or anchored convergence — the two-pass design distinguishes them).

**Negative triggers:**
- Single-axis problems (only one subagent dispatched).
- Axis-prescribed problems (each subagent receives a different predetermined axis). The skill applies to *axis-free* dispatches specifically.
- One-shot exploratory dispatches where divergence-vs-convergence isn't the signal being measured.

## Inputs

- The pool of subagents to dispatch (N ≥ 2).
- The shared brief (the task description; everything except the axis choice).
- Any constraints on axis selection (e.g., a deny-list from prior runs).

## Outputs

- N axis-proposal documents (pass 1 outputs).
- N full architecture/design documents (pass 2 outputs).
- A coordination-decision log describing what the lead agent did between passes (whether any axes were prohibited; whether a supplementary off-list subagent was dispatched).
- Commits per the project's convention.

## Workflow

1. **Pass 1 — axis proposal.** Dispatch all N subagents in parallel with a brief like: "Propose your organizing axis in one paragraph and defend the choice. Do NOT do the architecture work yet. Cite the corpus material driving your choice. Return only the proposal."
2. **Lead-agent coordination.** Collect the N proposals. Categorize:
   - **All N distinct axes** → proceed to pass 2 with no prohibitions. Divergence is the honest design signal; explore each.
   - **Two or more on the same axis (partial convergence)** → decide whether to (a) accept the convergence and dispatch pass 2 unchanged (corpus-signal-likely case; this is appropriate when the convergent subagents independently cited different corpus material), (b) prohibit the convergent axis for the convergent subagents on pass 2 (forced divergence), or (c) dispatch a supplementary off-list track in parallel with pass 2. Document the choice + reasoning.
   - **All N convergent** → either the corpus genuinely points at one answer or the prompt has anchored everyone. Dispatch one supplementary subagent with the converged axis prohibited; if it finds a defensible alternative, the convergence was at least partly anchoring.
3. **Pass 2 — execution.** Dispatch all N (or N+1 with the supplement) in parallel with the full work brief, the prior axis proposals visible, and any prohibitions applied.
4. **Document the coordination.** Append a short note to the work log: how many proposals converged, what action was taken, whether the supplementary off-list test was used. This is the audit trail for whether the resulting outputs are convergence-by-signal or convergence-by-anchoring.

## Concrete examples

### Example 1: Three "pick-your-own-axis" subagents on a unified design problem

Context: three subagents are dispatched on the same brief — "find an architecture that addresses both mandate-X and mandate-Y; pick your own organizing axis; defend the choice." Expected design signal: divergence.

Pass 1 brief:

```
You are subagent <ID> of 3 in a unified-design exploration. Each
subagent picks its own organizing axis. The other two are running in
parallel. Your task this pass:
1. Propose your organizing axis in one paragraph.
2. Cite 2-3 corpus sources that drove the choice.
3. Defend why your axis is the strongest available organizing
   principle for this problem.

Do NOT do the architecture work yet. Return only the proposal.
```

Pass 1 results:
- Subagent A: "tier-based axis (T0-T4 by blast-radius × reversibility × regulatory-exposure)"
- Subagent B: "Brier pace-layers (Code / Plans / Specs / Architecture / Standards)"
- Subagent C: "stakes-tier axis (T0-T3 by reversibility × scope × regulatory-exposure)"

Coordination: A and C picked near-identical tier-based axes with different naming. B picked a layer-based axis. The lead agent has three options. Option (a) accept the convergence — but A and C cite overlapping corpus material, which is a contamination flag. Option (b) prohibit the tier axis for C on pass 2 — but that doesn't test whether A and C's convergence is genuine. Option (c) dispatch a supplementary off-list track with both tier and pace-layers prohibited.

Lead agent chooses (c). Pass 2 dispatches A, B, C as proposed plus a 4th supplementary subagent (D) with "tier and pace-layers prohibited." Pass 2 outputs:
- A: full tier-axis architecture
- B: full pace-layers architecture
- C: full tier-axis architecture (variant of A)
- D: full verification-topology architecture

Conclusion: A and C's convergence was partly prompt-anchoring (D found a defensible alternative under the prohibition). Phase 3 merge treats A and C as variants of one tier family; B as a peer; D as a third candidate. Without the two-pass design, the lead agent would not have known D's axis was available, and Phase 3 would have merged only A+C+B with the implicit assumption that the corpus only supported those two axes.

### Example 2: Three "design pattern" subagents on a sub-component choice

Context: three subagents dispatched to pick a sync-or-async pattern for a sub-component, with the brief "pick your own pattern; defend the choice."

Pass 1 results:
- Subagent A: "event-driven pub/sub"
- Subagent B: "request/response with backpressure"
- Subagent C: "actor model"

Coordination: three distinct picks. No prohibitions needed. Proceed to pass 2 as-is.

Pass 2 dispatches A, B, C with full design work. The divergence is the design signal; Phase-3 merge treats all three as alternatives the architecture catalog can include.

## Anti-patterns

- **Single-pass independent dispatch on axis-free problems.** This is the failure mode the skill prevents. The lead agent cannot distinguish corpus-signal convergence from anchored convergence after the full expensive dispatch has already happened.
- **Sequential dispatch with cumulative prohibition.** Track 1 dispatches first; once it picks axis X, track 2 dispatches with "X prohibited"; track 3 dispatches with "X and Y prohibited." This produces guaranteed divergence but introduces order-effect bias (track 1 has more axis freedom than track 3) and triples the wall-clock time.
- **Pre-specifying axes.** The lead agent picks N axes upfront and assigns one per subagent. Loses the design intent ("let the corpus tell us") entirely; the lead agent's axis choices may themselves be biased.
- **Skipping coordination after pass 1.** Even if all N proposals look distinct, the lead agent must verify each cites different corpus material. Two subagents on different-looking axes that cite the same underlying source are still anchored.
- **Treating the supplementary off-list test as a substitute for the two-pass design.** The off-list test is the *fallback* when single-pass was used (or when full convergence requires falsification). The two-pass design prevents the expensive failure entirely.

## Acceptance criteria

- [ ] Pass 1 dispatch returns N axis proposals before any pass-2 work begins.
- [ ] The lead agent's coordination decision is documented (what action was taken between passes, why).
- [ ] If two or more subagents converged on pass 1, one of three actions was taken: accept (with citation-diversity verified), prohibit-for-convergent-subagents, or dispatch off-list supplement.
- [ ] Pass 2 dispatch happens in parallel (not sequentially).
- [ ] The work log documents the pass-1-to-pass-2 transition so a future reader can understand why the dispatch shape ended up where it did.

## Files this skill creates / modifies

- The work-area's track files or design proposal files (paths depend on the project) — creates.
- A coordination log entry — typically a paragraph in the work-area's plan doc or PR description — modifies/creates.
- No new infrastructure files. The two-pass design is a workflow pattern, not a tooling change.
