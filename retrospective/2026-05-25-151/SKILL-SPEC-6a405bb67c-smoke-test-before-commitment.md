# Spec: `smoke-test-before-commitment`

- **ID**: SKILL-SPEC-6a405bb67c
- **Source retrospective**: ../2026-05-25-151.md

## Intent

When a candidate, sub-system, or hypothesis has a load-bearing research-grade-uncertainty portion and a substantial Phase-N+ commitment is being considered to convert that RG portion into designed-system content, dispatch a single bounded smoke-test subagent first to attempt one representative instance of the work (one cross-layer invariant per layer-pair; one idiomatic-pattern per language; etc.) before committing to the full sub-track. The smoke-test either confirms the work is possible at scale (escalate to full commitment with high confidence) or surfaces honest negative evidence (downgrade to accept-as-RG, save 10-30× the cost of full commitment failure). The pattern emerged in the 2026-05-25 session when `auto-002` Round 1 proposed a full Phase-4 invariant-authoring sub-track for U-B (15 cross-layer invariants total) and both adversarial reviewers proposed a smoke-test (5 invariants, 1 per pair) as strictly dominant. The smoke-test passed (5/5) and U-B survived; had it failed, U-B would have self-eliminated at ~30× lower cost than the original proposal.

## Trigger

Direct: user says "smoke test this before we commit", "validate this is even possible first", "one-of-N first", "is this even buildable".

Proactive: a decision brief is being authored that commits a candidate / proposal to a sub-track converting RG content into designed-system content; the bounded version of that sub-track is itself substantive (≥5 worker-units like primitives, invariants, patterns, golden examples); the rejection cost (if the sub-track fails) is ≥10× the smoke-test cost; the failure-mode is plausible from existing evidence (the RG flag exists because there's genuine uncertainty about feasibility).

Negative: skip the smoke-test pattern when the sub-track work is trivially small (≤3 worker-units; just do it); when the failure-mode is implausible (the RG flag is calibration-grade, not feasibility-grade); when the smoke-test subagent can't be given a tight bounded charter (open-ended "see if it works" smoke-tests waste cost without producing decision-grade evidence).

## Inputs

- A decision brief proposing a Phase-N+ sub-track to convert an RG portion into designed-system content.
- The source RG sketch (the artifact that landed the RG verdict in the first place).
- An adversarial-reviewer pass that surfaced the smoke-test as a counter-proposal (typical; the pattern is reviewer-discovered more often than lead-agent-discovered).
- The corpus / project material the smoke-test will draw on.

## Outputs

- One smoke-test subagent dispatch with a tight charter (≤2 paragraphs of brief; explicit verdict-logic).
- One smoke-test result file: `<project>/<phase>/<rg-primitive-id>-smoke-test-<scope>.md` (or analog). Contains: per-unit attempt result, verdict (pass / partial / fail) per unit, overall verdict per the charter's decision rule.
- An updated decision brief in Round-N+1 reflecting the smoke-test outcome.
- A registry / candidate-status update flowing from the verdict.

## Workflow

1. **Identify the smoke-test scope.** From the proposed sub-track, pick the smallest meaningful unit of work that represents the whole. For per-layer-pair invariants, that's 1 invariant per pair. For per-language patterns, that's 1 pattern per language. For per-module-class scenarios, that's 1 scenario per class. The number of attempts should be small (3-7 typical) but cover the structural variety of the full sub-track.
2. **Draft the verdict logic explicitly in the smoke-test brief.** Before dispatching, write down what "pass" / "partial" / "fail" looks like. Example from `auto-002`: ≥4 of 5 pairs → full sub-track authorized; 2-3 → contract restate with accept-as-RG for barren pairs; ≤1 → self-eliminate. The verdict logic is a public contract — the subagent's output is adjudicated against it, not against the lead agent's later judgment.
3. **Constrain the subagent's evidence sources.** The smoke-test should attempt the work using only the corpus / project material that would be available in the full sub-track. If the subagent invents material outside that pool, the smoke-test result over-estimates feasibility.
4. **Dispatch one subagent (not a fanout).** Single subagent keeps the cost bounded and the result attributable. The subagent writes the result file directly to disk; returns a short summary.
5. **Adjudicate against the pre-declared verdict logic.** Do not soften or harden the verdict logic after seeing the result; if it doesn't fit cleanly, that itself is a finding (the verdict logic was malformed).
6. **Update the decision brief in Round-N+1.** The smoke-test result is now the strongest evidence on the decision. Mark Round-N superseded; write Round-N+1 with the smoke-test outcome and the corresponding decision.
7. **Cascade the verdict into the project's registry / candidate-status doc.** A pass converts conditional survival to survival; a fail converts conditional survival to self-elimination. A partial triggers a contract-restate per the verdict logic.

## Concrete examples

### Example 1: U-B cross-layer invariants (from the 2026-05-25 session)

`auto-002` Round 1 proposed: U-B commits at Phase 4 to authoring ≥15 cross-layer invariants (5 layer-pairs × ≥3 per pair) from corpus material. Round-1 cost estimate: "one extra subagent + lead-agent review at Phase 4 close." Reality (per cost-hawk reviewer): ~30 subagent dispatches across Phases 5/6/7/8 if U-B survives; 0.9M–2.4M tokens of avoidable spend if U-B fails. Both reviewers proposed smoke-test: one subagent, charter to author 1 non-trivial machine-checkable cross-layer invariant per layer-pair (5 attempts), with explicit verdict logic. Cost: one dispatch (~50K tokens). 30× cheaper than full sub-track failure.

Smoke-test result: 5/5 layer-pairs produced non-trivial invariants with verbatim corpus citations. Verdict per pre-declared logic: U-B survives, full sub-track authorized. The smoke-test result file (`primitives/P-31-smoke-test-invariants.md`) carried the per-pair invariants, construction sentences, positive + negative examples. Cascaded into `candidate-registry.md` Phase-3.5.5 section.

Counterfactual: if Round-1 option 1 (full sub-track) had been pursued without smoke-test, U-B would have entered Phase 4 with ~30 dispatches in flight before any verdict became available. If the work had turned out infeasible, all that work was wasted; if feasible, the smoke-test would have produced the same authorize-the-sub-track verdict more cheaply.

### Example 2: Hypothetical — codebase-model conventional-view authoring (BF-L)

The Phase-3.5.5 RG-primitive rule offers BF-L two options for its conventional-view RG portion: (a) bounded sub-track (LLM-with-structured-output + golden corpus of ≥20 idiomatic patterns per supported language), or (b) accept-as-RG. Before committing to (a) across ≥5 languages × ≥20 patterns = ≥100 patterns total, dispatch a smoke-test: one subagent, charter to author 1 idiomatic-pattern per language for 3 representative languages. Verdict logic: ≥2 of 3 produce well-formed patterns with corpus citations → escalate to full sub-track; 1 of 3 → bounded sub-track only on the language that worked; 0 of 3 → accept-as-RG.

If the smoke-test fails on 2 of 3 languages, the failure-mode is feasibility-grade (the convention-extraction methodology isn't broadly applicable). Accept-as-RG is the honest verdict. Cost of smoke-test: ~30K tokens. Cost of full sub-track failure: estimated 200K+ tokens.

## Anti-patterns

- **Smoke-testing with the verdict logic undefined.** If you can't articulate what "pass" looks like before dispatching, the smoke-test produces ambiguous evidence and Round-N+1 ends up re-litigating the original decision.
- **Open-ended "see if this works" charters.** The subagent then under-invests in the hardest case (because it's not required) and over-invests in the easiest (because it's all there is). The smoke-test should specify the units to attempt; the verdict logic should specify what success looks like per unit.
- **Skipping the smoke-test when reviewers suggest it.** Real adversarial reviewers proposing a smoke-test is high-signal — they've identified that the full sub-track cost is mis-estimated. Defaulting to "no, let's just do the full thing" is the failure-mode the smoke-test exists to prevent.
- **Smoke-testing when the work is trivially small.** If the full sub-track is 3 invariants total, just do the 3 — the smoke-test cost approaches the full cost, no information gain.
- **Smoke-testing the easy half.** If the proposed sub-track has 5 layer-pairs and the lead agent picks the 3 easiest ones for the smoke-test, the verdict is biased. Smoke-test should sample structurally — one of each variety the full sub-track would face.

## Acceptance criteria

- [ ] Smoke-test brief states verdict logic explicitly before dispatch (pass / partial / fail thresholds; one of those three for each unit attempted).
- [ ] Subagent writes the smoke-test result to a named file on disk; returns ≤100-word summary.
- [ ] Round-N+1 decision brief adjudicates against the pre-declared verdict logic, not post-hoc judgment.
- [ ] Result cascades into project-level state (candidate registry, status doc, ADR draft) — the smoke-test result is not orphaned.
- [ ] Cost ratio between smoke-test and full sub-track is documented in the decision brief so future smoke-tests can be sized appropriately.

## Files this skill creates / modifies

- `<project>/<phase>/<rg-primitive-id>-smoke-test-<scope>.md` — the smoke-test result file written by the dispatched subagent.
- `<project>/decisions/auto-NNN-*.md` (Round N+1) — the decision brief updated with the smoke-test outcome and the final decision.
- `<project>/<candidate-or-status-doc>.md` — cascaded status update reflecting the smoke-test verdict.
