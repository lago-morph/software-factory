# Spec: `wave-split-with-checkpoint`

- **ID**: SKILL-SPEC-2412f18523
- **Source retrospective**: ../2026-05-25-170.md

## Intent

When a parallel ADR-authoring fanout exceeds the wave-size limit (≤10-15 subagents) or mixes commodity-tier and designed-system-tier items, split the wave into ordered sub-waves with a lead-agent checkpoint between them so re-dispatch budget is preserved and exemplar-calibration drift is caught early. In the 2026-05-25 Phase-5-entry run, the original auto-005 Round-1 Wave 5.1 sized at 13 subagents — the upper edge of the ≤15 cap with zero headroom for re-dispatch. The ADR-pipeline-architect Round-1 reviewer's amendment split it into Wave 5.1a (8 commodity-tier ADRs) + Wave 5.1b (9 designed-system + 2-candidate ADRs) with a checkpoint between. Result: zero re-dispatches needed, one quality finding caught at checkpoint (wrong-number forward-ref in ADR 0034), all 17 ADRs landed cleanly.

## Trigger

Activate when:
- A planned parallel ADR-authoring fanout has >10 subagents.
- The fanout mixes commodity-tier items (simple contracts, single-candidate) with designed-system items (multi-variant, complex contracts).
- Round-1 adversarial review on the parent decision brief raises "wave size too large" or "exemplar miscalibration" concerns.

Direct triggers: "split this wave", "checkpoint between sub-waves", "stagger the dispatch". Negative trigger: a wave with ≤8 uniformly-commodity items needs no split.

## Inputs

- The parent decision brief naming the wave's scope and exemplar choice.
- The list of ADR-target items (primitive IDs / discipline names / candidate IDs).
- The wave-size cap from the autonomous-run skill (currently ≤10 conservative, ≤15 hard).

## Outputs

- Two (or more) sub-waves with disjoint scopes.
- A checkpoint protocol document (or section in the parent brief) describing what the lead agent verifies between sub-waves and what triggers re-dispatch.
- Optionally a second exemplar if sub-wave 2's items are materially harder than sub-wave 1's.

## Workflow

1. Classify each item by tier. Use overlap.md (or equivalent same-vs-distinct analysis) + the per-item buildability sketch's "designed-system vs commodity" tag.
2. Group commodity-tier items first (sub-wave A), designed-system items second (sub-wave B). 2-candidate primitive folds (if the parent brief includes them) go in sub-wave B because they typically need cross-reference discipline.
3. Cap each sub-wave at ≤10 subagents. If sub-wave A would exceed ≤10, split it further into A1/A2 with a lighter checkpoint.
4. Author one exemplar for sub-wave A (the exemplar is normally a mid-difficulty commodity item). If sub-wave B's items differ materially, author a second sub-wave-B exemplar; otherwise reference sub-wave A's exemplar with variant-scope guidance in each sub-wave-B subagent's brief.
5. Dispatch sub-wave A. After it returns, run the checkpoint: (a) verify all ADRs meet rubric (word count, sections, references, self-check); (b) spot-check that cross-cutting references are consistent (e.g., a commodity sandbox-using ADR cites P-01 the same way other commodity sandbox-using ADRs do); (c) confirm exemplar discipline held — no rubric drift.
6. If >1 ADR fails the checkpoint: budget ≤2 PRs for re-dispatch on a stacked fix branch. Re-dispatch only the failing subset to fresh subagents with a rubric-gap summary. Wait for fix before sub-wave B fires.
7. If 0–1 ADR failures: proceed to sub-wave B. Each sub-wave-B subagent's brief includes variant-scope guidance (per `AGENTS-MD-a9fb7b42f8` framework-ADR scope-boundary discipline if applicable).
8. After sub-wave B returns, run a second checkpoint covering both sub-waves' integration.

## Concrete examples

### Example 1: 2026-05-25 Wave 5.1a/5.1b

Original Wave 5.1 sized at 13 subagents for ADRs 0010–0022 (substrate primitives shared by ≥3 candidates). ADR-pipeline-architect Round-1 reviewer flagged: no headroom for re-dispatch + P-01 exemplar miscalibrated for designed-system items.

Split:
- **Wave 5.1a** (8 commodity-tier): P-01 sandbox, P-02 cost ceilings, P-05 trajectory, P-06 watchdog, P-07 telemetry, P-08 scenario storage (EXEMPLAR), P-14 judge router, P-22 polyglot index. Exemplar P-08 (designed-system shape; teaches runner-API contract + partition semantics).
- **Wave 5.1b** (9 designed-system + 2-candidate): P-19 regime classifier framework, P-28 typed-object store framework, P-29 policy mediator framework, P-23 dep-impact graph, P-12 linter framework, P-25 CaMeL (2-cand), P-27 archaeological-brief (2-cand), P-24 attribution (2-cand), P-30 substrate (variant deferred).

Checkpoint between 5.1a and 5.1b verified 8/8 ADRs met rubric. Sub-wave B reused P-08 exemplar with variant-scope guidance in each brief. One ADR (0034, P-27) had a wrong-number forward-reference caught at sub-wave-B aggregation; fixed inline in 1 commit. Total: 17 ADRs delivered cleanly across 2 PRs.

### Example 2: Hypothetical Wave-5.3 split

Wave 5.3 (deferred to next run) has 29 ADRs — too large for a single fanout. Split into sub-waves by candidate cluster: 5.3a (greenfield candidates: GF-S, GF-M, GF-C orphans + P-19 variants × 2), 5.3b (brownfield: BF-S, BF-M, BF-L orphans + P-19/P-28 variants where applicable), 5.3c (unified-attempt: U-A, U-B, U-C, D7-U-1 + all remaining per-variant ADRs). Each sub-wave 6–11 subagents, checkpoint between.

## Anti-patterns

- **Splitting without a checkpoint protocol**. A split that has no defined verification step between sub-waves loses the entire benefit — calibration drift just gets caught later at higher cost.
- **Mixing commodity and designed-system in the same sub-wave**. Defeats the calibration benefit of the exemplar. Commodity ADRs anchor low; designed-system items anchor high.
- **Sub-wave size > 10**. The skill exists to keep aggregation tractable. A sub-wave at 12 is just a smaller version of the original problem.
- **Reusing sub-wave-A's exemplar verbatim for sub-wave B without variant guidance**. The exemplar must remain referenced, but each sub-wave-B subagent needs explicit "here is what differs about your sub-wave" guidance in the brief.

## Acceptance criteria

- [ ] No sub-wave exceeds 10 subagents.
- [ ] Each sub-wave has at least one exemplar (lead-agent inline-authored before dispatch).
- [ ] The checkpoint protocol explicitly names: (a) what to verify, (b) what triggers re-dispatch, (c) the re-dispatch budget cap.
- [ ] Sub-wave B does not fire until sub-wave A's checkpoint passes.

## Files this skill creates / modifies

- The parent decision brief — adds the wave-split section.
- Per-sub-wave PRs in the stacked chain.
- The lead-agent checkpoint can be encoded as a brief inline document or a sub-wave-close commit message.
