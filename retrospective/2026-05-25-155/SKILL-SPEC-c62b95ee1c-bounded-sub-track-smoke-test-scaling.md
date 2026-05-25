# Spec: `bounded-sub-track-smoke-test-scaling`

- **ID**: SKILL-SPEC-c62b95ee1c
- **Source retrospective**: ../2026-05-25-155.md

## Intent

When a candidate carries a research-grade-uncertainty load-bearing primitive and elects the Phase-3.5.5 option (a) bounded sub-track, attempt a small smoke-test first (3 non-trivial artifacts per cell across top-N cells with positive/negative examples and corpus citation), gate the full sub-track on a multi-cell binary verdict, scale to ≥10 per cell only on pass, fall back to accept-as-RG plus methodology-degradation clause on fail. Drawn from the convergence between auto-002 R2 (U-B P-31) and auto-003 R2 (BF-L conventional + invariant) on the same shape. Without this pattern, bounded sub-tracks adopt count-gates without substance discipline; count-inflation is then the failure mode (a subagent under deadline can emit ≥N trivially-true artifacts that pass the count but don't honor the load-bearing claim).

## Trigger

- A candidate's substrate-requirements summary names a load-bearing primitive flagged `research-grade-uncertainty` at Phase 3.5 close.
- The candidate elects Phase-3.5.5 option (a) bounded sub-track over option (b) accept-as-RG.
- Lead agent is designing the sub-track's Phase-4-close go/no-go gate.

Negative triggers: partial-RG flags on calibration-style sub-components (those are Phase-8 lean-eval candidates, not Phase-4 sub-tracks); RG portions where (b) accept-as-RG is the declared choice.

## Inputs

- The RG primitive's sketch (construction path, RG flag rationale, named gap).
- The candidate's track file (what the methodology needs from the primitive's content).
- Prior art / research notes if any have been authored (Wave 4.4 in this session was the precedent).
- The cell space: typically `(top-N languages × top-N components)`, named explicitly in the smoke-test brief.

## Outputs

- Smoke-test deliverable at `architectures/v3/sub-tracks/<candidate-id>-<view>-smoke-test.md` containing N non-trivial artifacts per cell with positive/negative examples + corpus citation + honesty-discipline clause.
- Conditional scale-up deliverable if smoke-test passes.
- Updated registry annotations with the smoke-test verdict + (if pass) the scaled sub-track artifact list.

## Workflow

1. Define the **non-trivial** clause for the artifact class. Must mirror P-31's: constrains *substance*, not presence-of-link; disqualifies regex-grade pattern matches, trivial type-system tautologies, file-naming-suffix checks.
2. Define the **representative cell** sampling frame. Examples: top-3 languages by representative-codebase coverage; top-3 layer-pairs by load-bearing-ness; top-3 corpus regions by citation density. The frame is binding before launch.
3. Define the **verdict logic** as a binary multi-cell gate: e.g., "≥2 of 3 cells produce ≥3 non-trivial artifacts each → full sub-track authorized."
4. Define the **fallback** if smoke-test fails: which cells fall to accept-as-RG; what methodology-degradation clause activates in the candidate's regime-classifier / dispatcher.
5. Define the **honesty-discipline clause**: "If a cell has no corpus-citable non-trivial artifact, the report says so explicitly and names the gap — fabricated artifacts without corpus support do not count."
6. Dispatch the smoke-test subagent. Brief must include items 1-5 verbatim, plus exemplar (one fully-worked artifact for one cell) if this is the candidate's first smoke-test.
7. On return, render the verdict. Update the registry + the candidate's substrate-requirements summary.
8. If pass: dispatch the scale-up subagent. Same shape, scaled to ≥10 per cell. Inherit corpus citations from smoke-test; scaling must add new corpus diversity (smoke-test caveat #c).
9. If fail: write the methodology-degradation clause into the Phase-6 spec slot. Phase-8 lean-eval pressure-tests the degradation pattern.

## Concrete examples

### Example 1: U-B cross-layer drift detector (auto-002 R2 + Wave 4.5)

- Primitive: P-31 cross-layer drift detector.
- Cell space: 5 pace-layer pairs (L0↔L1, L1↔L2, L2↔L3, L3↔L4, L0↔L4).
- Smoke-test scope: 1 non-trivial invariant per pair (5 total). Verdict: ≥4/5 → full sub-track.
- Result: 5/5 pairs produced non-trivial invariants with verbatim corpus citations (AILCCP / EARS / El-Kaim-Ch8 / F36 empirical / F34 expected-touch).
- Scale-up (Wave 4.5): scaled to 20 invariants total (4 per pair × 5 pairs); 10+ new corpus citations beyond smoke-test base.

### Example 2: BF-L conventional view (auto-003 R2 + Wave 4.5)

- Primitive: P-26 Codebase Model conventional view.
- Cell space: 3 languages × 1 representative codebase each (Python = Django, TypeScript = VS Code, Java = Spring Boot — within the pre-declared frame of "open-source, ≥3 years history, ≥100k LOC, ≥10 contributors, permissive license").
- Smoke-test scope: 3 non-trivial substantive conventions per language (9 total). Verdict: ≥2/3 languages → full sub-track.
- Result: 3/3 languages PASSED. Methodology-degradation clause stayed dormant.
- Scale-up owed at Phase 5/6: 10+ per language.

## Anti-patterns

- **Count-gate without substance discipline.** "≥20 patterns" without a non-trivial clause invites count-inflation. (auto-003 R1 failure mode caught by methodology-purist.)
- **Calibrated-precision gate against a non-existent measurement instrument.** "Manual-spot-check precision ≥0.7 against the golden corpus" when no golden corpus exists is functional pre-elimination. (auto-003 R1 failure mode caught by scoping-skeptic.)
- **Missing honesty-discipline clause.** Subagent under deadline incentivized to inflate; honesty clause makes "gap" an admissible outcome.
- **Single-cell smoke-test.** Doesn't produce a binary verdict signal; degrades to "is this any good?" rather than "did N of M cells succeed?"
- **Skipping the fallback methodology-degradation clause.** If the smoke-test fails, the candidate's methodology must already specify graceful degradation; if it doesn't, (b) accept-as-RG is a fig leaf.

## Acceptance criteria

- [ ] Smoke-test deliverable exists with N non-trivial artifacts per cell.
- [ ] Each artifact carries positive example + negative example + corpus citation.
- [ ] Honesty-discipline clause appears verbatim in the smoke-test brief.
- [ ] Verdict logic is binary multi-cell (not "is this good?" qualitative).
- [ ] If pass, scale-up adds new corpus diversity beyond smoke-test base.

## Files this skill creates / modifies

- `architectures/v3/sub-tracks/<candidate-id>-<view>-smoke-test.md` — smoke-test deliverable.
- `architectures/v3/sub-tracks/<candidate-id>-<view>-full-sub-track.md` — conditional scale-up deliverable.
- `architectures/v3/candidate-registry.md` — Phase-4-close annotations + verdict.
