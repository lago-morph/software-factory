# Spec: `parallel-fanout-with-exemplar-and-rubric`

- **ID**: SKILL-SPEC-069f0f31bf
- **Source retrospective**: ../2026-05-25-155.md

## Intent

Dispatch N parallel subagents producing a uniform-schema deliverable by first authoring one exemplar of the format and shipping it with the dispatch brief, plus a per-subagent self-check rubric that verifies section-presence, word count, link relativity, and required text-pulls before the subagent returns. Drawn from the Wave-4.1 dispatch pattern in the Phase-4 dispatch session 2026-05-25, where the GF-M exemplar served as the model for 9 parallel Wave-4.1 subagents and required text-pulls + fixed contested-primitive headers made Wave-4.2 lead-agent aggregation tractable. Without an exemplar, subagents drift across section boundaries, word counts, and citation discipline; downstream lead-agent aggregation then re-shapes the outputs at significantly higher cost than authoring one exemplar up front.

## Trigger

- User asks to "dispatch N parallel subagents", "fan out", "do this for each X", or proposes a parallel fanout of ≥3 subagents producing the same kind of deliverable.
- Lead agent has identified an inventory operation (per-candidate, per-primitive, per-module) where each unit gets the same deliverable shape.
- Proactive: any plan that includes "produce one file per [class] in parallel" should trigger this skill before dispatch.

Negative triggers: single-subagent dispatches; subagents whose deliverables are intentionally heterogeneous (e.g., adversarial reviewers with different angles); fanouts ≤2 where exemplar overhead exceeds savings.

## Inputs

- Inventory list: the N items (candidates, primitives, modules) the fanout covers.
- Deliverable schema: required section headers, length budget, required citations, required fixed sub-section headers for contested fields.
- Source material per item (paths, registry entries, prior-art notes).
- Exemplar-selection criterion: typically "least contested" — the inventory item with fewest RG flags, contested references, or special-case obligations.

## Outputs

- One exemplar file authored by the lead agent at the deliverable path for the chosen exemplar item, committed before fanout dispatch.
- N-1 parallel subagent dispatches, each producing one deliverable file at its assigned path.
- Each subagent's deliverable conforms to the exemplar's section structure and passes the self-check rubric.

## Workflow

1. Enumerate the N items and confirm they share the same deliverable shape.
2. Pick the exemplar item: smallest cross-cutting obligations (no RG flags, no contested-primitive references, no shared-skeleton sections), so the exemplar can be authored without first making decisions that other items will defer to.
3. Author the exemplar inline (lead agent). Write all required sections; cite by relative link; demonstrate every fixed sub-section header that contested-class items will use.
4. Commit the exemplar to a branch with a message naming it as the exemplar for the fanout.
5. Write the per-subagent brief. It MUST include:
   - The exemplar path as required input.
   - The required section list with one-line description per section.
   - The fixed sub-section header set for contested-class items.
   - Required text-pulls (verbatim from binding rule tables, not paraphrase).
   - Shared skeletons for any cross-cutting articulation (e.g., X_UNM_B in this session).
   - A self-check rubric the subagent runs as the final step. Each measurable item in the rubric (word count, link relativity) requires a tool call.
6. Dispatch N-1 subagents in parallel with `run_in_background: true`.
7. As completion notifications arrive, verify each deliverable's existence + word count + section count via `wc -w` and `grep -c '^## §'`. Do NOT re-read the full files; the rubric was the contract.
8. Commit the fanout outputs in a single batch with a manifest listing all N items.

## Concrete examples

### Example 1: Wave 4.1 substrate-requirements summaries (Phase 4, 2026-05-25)

- Inventory: 10 candidate architectures (GF-S, GF-M, GF-C, BF-S, BF-M, BF-L, U-A, U-B, U-C, D7-U-1).
- Shape: 6-section schema (§1 Primitive list / §2 RG primitives / §3 Candidate-specific contracts / §4 X_UNM_B / §5 Open carries / §6 Scoping-principle compliance), 800-1500 words.
- Exemplar pick: GF-M — least-contested (no RG flags, no contested-primitive references in §3, §4 = N/A as greenfield-only).
- Lead agent authored `architectures/v3/substrate-requirements/gf-m.md` (896 words) inline.
- 9 subagents dispatched in parallel; each consumed the GF-M exemplar as required input.
- Wave 4.2 aggregation read 10 files of known shape and rendered 8 same-vs-distinct verdicts in one lead-agent pass.

### Example 2: Per-primitive sketches (Phase 3.5, 2026-05-25 overnight)

- Inventory: 21 designed-system / research-grade primitives (P-14 through P-34).
- Shape: contract restatement + construction path + corpus-why + RG flag + verdict.
- Exemplar pick: P-14 judge router (commodity-adjacent designed-system; well-trodden prior art).
- 21 subagents dispatched in parallel; cluster sketches (3 subagents) handled commodity primitives separately.
- All 24 sketches landed within rubric on first dispatch.

## Anti-patterns

- **Authoring all N inline without parallelism.** Saturates lead-agent context; loses subagent independent fresh-read benefit.
- **Dispatching N without an exemplar.** Section drift across N outputs; downstream aggregation pays the cost.
- **Picking a contested exemplar.** The exemplar then has to make decisions that the fanout would otherwise defer to lead-agent merge; anchoring risk.
- **Self-check rubric without tool calls.** Subagents self-attest without running `wc -w`; word-count drift goes undetected (Wave 4.1 BF-L came in at 1676 vs 800-1500 budget while claiming self-check passed).
- **Skipping required text-pulls.** Parallel subagents handling the same binding rule (e.g., Phase-3.5.5 application table) paraphrase it three different ways; lead-agent re-reads the rule to normalize.

## Acceptance criteria

- [ ] Exemplar exists at the deliverable path before fanout dispatch.
- [ ] Every subagent brief names the exemplar as required input.
- [ ] Self-check rubric has at least one tool-call-verified item per measurable property.
- [ ] All N deliverables exist at their assigned paths after fanout.
- [ ] Lead-agent aggregation reads N files of known shape (no re-reading of source material).

## Files this skill creates / modifies

- `<deliverable-dir>/<exemplar-item>.md` — the lead-agent-authored exemplar.
- `<deliverable-dir>/<item>.md` × (N-1) — the subagent-authored deliverables.
- Optionally: `<deliverable-dir>/MANIFEST.md` listing all N items + paths.
