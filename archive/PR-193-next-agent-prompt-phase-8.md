# Next-agent prompt — Phase 8 (lean-eval design per candidate)

**Status.** Dispatch prompt for the next autonomous run. Authored 2026-05-28 in PR opened after Phase 7 closed (PRs #187-#192 merged to `main`).

**How to use this file.** Open a fresh Claude Code session against this repo. Paste the contents of [§Prompt body](#prompt-body) below as the initial user message. The agent will read it, run pre-flight, write a scope envelope, and proceed.

Per [`AGENTS-MD-a43c9584c9`](AGENTS.md#dispatch-prompt-edit-before-run-pattern): this prompt is committed at a stable commit before the run fires, so the run's scope envelope can cite the prompt verbatim by SHA.

---

## Prompt body

```
You are operating in autonomous (unattended) mode. The user has delegated execution for this run; do not wait for confirmations on reversible decisions. Per the autonomous-run skill, your first action is to write a one-page scope envelope and post it to the user before any non-Read tool call.

## Read order (minimal)

In order, before any non-Read tool call after the scope envelope:

1. AGENTS.md — binding conventions (17 rules at Phase-7 close; 5 more proposed in retrospective/2026-05-27-191/AGENTS-MD-*.md — adopt or skip per §"Pre-flight" below).
2. AGENT-ENTRY.md — root navigation. Section 2 should point at architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md. Follow the "Phase 8 dispatch shape decision (auto-008)" task-aware reading list.

**Run the pre-flight check first.** Per AGENTS-MD-4f8c2a1b03 (pre-flight prior-phase merge-state verification), verify Phase-7 deliverables are actually in main:

  git fetch origin main
  git ls-tree -r origin/main --name-only | grep -cE "architectures/v3/backfill-notes/"  # expect 12 (10 candidates + 2 bias-guards)
  git ls-tree -r origin/main -- architectures/v3/backfill-notes.md
  git ls-tree -r origin/main -- architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md
  git ls-tree -r origin/main -- retrospective/2026-05-27-191.md
  git ls-tree -r origin/main -- run-summary-2026-05-27-phase-7.md

If any check fails, surface via AskUserQuestion before proceeding.

**Pre-flight: pending adoptions from the Phase-7 retrospective.** Five proposed AGENTS.md rules and two ADR drafts landed in retrospective/2026-05-27-191/ but have NOT been adopted into the canonical AGENTS.md / docs/adr/. Per AGENTS-MD-a43c9584c9 (dispatch-prompt edit-before-run pattern), surface to user via AskUserQuestion whether to adopt before auto-008 fires, or defer. The rules are directly relevant to auto-008's shape:

- AGENTS-MD-4a7c2e9f6b (adversarial-review amendment-inheritance) — would mandate pre-folding auto-007's audit-trail amendments at auto-008 Round 1 authoring time.
- AGENTS-MD-8e5d3a7c4b (phase-followup carry-forward absorption into bias-guard mandates) — would mandate folding any Phase-7 carry-forwards into Phase-8 bias-guards.
- AGENTS-MD-5b3e8a1c2f (silent-absorption confidence-threshold) — relevant if Phase-8 bias-guards produce override-eligible findings.
- AGENTS-MD-7d9c4e1b3a (matrix-flag over spec-patches) — relevant if Phase-8 surfaces analogous citation gaps.
- AGENTS-MD-2f8a6c9d51 (per-candidate engagement over blanket-skip) — relevant if auto-008 proposes any "skip" instruction for prior-phase material.

Do NOT load the 10 per-candidate Phase-6 specs or the 10 per-candidate Phase-7 back-fill notes eagerly. Each per-candidate subagent in Wave 8.1 will load only the spec + back-fill notes for its assigned candidate.

## What to build

Phase 8 produces lean-eval brief designs per candidate — the first pressure-testing surface where candidates begin to differentiate empirically AND the falsification surface for the DEC-1.a working hypothesis.

### Sub-product breakdown

- 10 per-candidate lean-eval briefs at architectures/v3/lean-evals/<candidate-id>.md. Each carries: target candidate, test scenario set (drawn from corpus or from the candidate's own scenario-derivation primitives), success criteria, failure modes the lean-eval is designed to surface, expected evaluator time (~1 day), references to the candidate's open critique findings, AND the Phase-7 cite obligations that apply to this candidate (see "Phase-7 load-bearing inputs" below).
- 1 cross-candidate evaluator-brief at architectures/v3/lean-evals/00-cross-candidate.md. Names the comparison axes across all 10 lean-evals so a downstream simulator can pressure-test candidates against each other.
- 3 bias-guards (per v1.2 plan § Phase 8): domain practitioner (validates each brief; "would this actually validate the discipline?"); falsification-designer (per-candidate; names the falsifying outcome — if the brief can't articulate one, it's too soft); hypothesis-falsifier (cross-candidate; names *in advance* the result pattern that would falsify DEC-1.a so post-hoc reinterpretation is impossible).
- Phase-8-close session handoff unblocking the downstream simulator-harness work (post-v3).
- Morning summary + full-package retrospective per the autonomous-run skill.

### Phase-7 load-bearing inputs (each per-candidate Phase-8 brief MUST honor these)

Per the Phase-7-close handoff:

1. 3 high-confidence silently-absorbed cells — Phase-8 brief mandatory cite obligations:
   - U-A: Knowledge-promotion 4-token enum lifted from Compound Atelier without cite.
   - 7 specs (GF-M / U-A / U-B / U-C / D7-U-1 / BF-S / BF-M): Compound-Engineering "plan → work → review → compound" 4-step loop appears verbatim without archive cite.
   - 5 specs (BF-S / BF-L / BF-M / D7-U-1 / U-A): 4-architecture taxonomy from archive/architectures-v2/00-comparison.md §1 without archive cite.

2. 7 medium-confidence TBD reconciliation cells — Phase-8 brief design inputs (per-candidate questions asking "is the candidate's framing distinguishable from the archive item, or silent inheritance worth citing?"). Specific cells in architectures/v3/backfill-notes/audit-silent-absorption.md §B.1.

3. 5 historian load-bearing gaps — Phase-8 design inputs:
   - H-1 stable-ID lettering (R/A/F/AE/U/S/K) — recommend ONE candidate (U-C or D7-U-1) adopts; track as Phase-8 design input.
   - H-2 + H-8 paired (self-improving-prompts pattern + role) — methodology decision for GF-S / GF-M / U-A.
   - H-3 Pulse report (production-trace-to-spec-amendment) — BF-L Phase-8 brief specifically (BF-L's P-13 is closest analog).
   - H-5 scaffold/harness C11 vocabulary — glossary addition opportunity (non-blocking).

## First decision — write auto-008: Phase-8 dispatch shape

User confirmed at Phase-7-close that Phase 8 should use per-candidate parallel fanout (10 subagents, one per candidate, each authoring one lean-eval brief). auto-008 formalizes this. Open questions for the brief:

1. Wave shape. Default = 10 per-candidate parallel subagents in one wave (Wave 8.1) + cross-candidate evaluator-brief either concurrent or after (Wave 8.2). Per the bias-guards-concurrent precedent in retrospective/2026-05-27-191/ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md: bias-guards fire concurrent IF their input streams are independent of per-candidate outputs. **Hypothesis-falsifier auditor explicitly depends on reading all 10 lean-eval briefs** → must fire serially AFTER Wave 8.1, not concurrent. Domain-practitioner and falsification-designer could fire concurrent per-candidate (one practitioner + one falsification-designer attached to each per-candidate brief) OR after-the-fanout (single cross-spec read each).

2. Tier-table calibration. Phase-7 evidence: 9-of-10 candidates over their tier budget; Light median +28%; Heavy median +11%. Lead-agent recommendation (per Phase-7-close advisory carry-forward): adopt Light 5000-6500 / Heavy 5500-7500 at auto-008 Round-1 authoring rather than waiting for Round-2 reviewers to surface it.

3. Lean-eval brief rubric. Each brief: §1 candidate + scenario set; §2 success criteria; §3 falsifying outcome (load-bearing per falsification-designer auditor); §4 failure modes the test surfaces; §5 evaluator time + protocol; §6 open critique references; §7 Phase-7 cite obligations honored; §8 references. Mandatory falsifying-outcome: YAML frontmatter field — the falsification-designer auditor's first check is `grep "falsifying-outcome:" architectures/v3/lean-evals/*.md`.

4. Cross-candidate evaluator-brief shape. Comparison axes across the 10 briefs. Names DEC-1.a falsifying result pattern verbatim per hypothesis-falsifier auditor (e.g., "If ≥2 unified-attempt candidates pass BOTH the greenfield AND brownfield lean-eval cleanly with no escape-hatches invoked, DEC-1.a is falsified.").

5. Phase-7 cite obligation propagation mechanism. Each per-candidate brief receives its candidate's specific cite obligations as part of the dispatch input (NOT just a reference to the aggregation matrix). Lead-agent pre-authors the cite-obligation mapping in auto-008 so subagents don't have to derive it.

6. Adopting Phase-7 retro AGENTS-MD rules into auto-008 discipline. If the 5 proposed rules are adopted before auto-008 Round 1, fold them at authoring time (especially AGENTS-MD-4a7c2e9f6b audit-trail amendment inheritance from auto-007). If not adopted, follow the patterns informally — but flag the gap in the brief's honest-acknowledgements.

Per AGENTS-MD-d72e1a4f3c: dispatch ≥3 real adversarial subagents in Round 1, then ≥3 more in Round 2 with fresh angles. Per AGENTS-MD-8a7029647f: 3-tier verdict scheme. Land auto-008 as its own stacked PR before any lean-eval-brief subagent fires.

## Working-mode reminders

- Scope envelope first (per autonomous-run skill). Wait briefly for user reply; proceed with envelope as written if no response.
- PR-cap budget. Phase 7 used 6 PRs against 15-PR cap. Phase 8 should fit in ≤8 PRs: 1 for auto-008 brief + 1 for exemplar (lead-agent-authored; least-contested candidate; same pattern as Phase 7 BF-S exemplar) + 1 for lean-eval fanout omnibus (Wave 8.1; 9 sibling briefs disjoint files) + 1 for cross-candidate evaluator brief (Wave 8.2) + 1 for bias-guards (3 auditors, omnibus if disjoint) + 1 for handoff + 1 for summary + 1 for retro.
- Webhook verification. Per AGENTS-MD-c5a92e6017, verify "merged" webhook events via mcp__github__pull_request_read before acting.
- Audit-trail discipline inheritance from auto-007. Pre-fold at auto-008 Round 1 authoring time: commit-SHA pinning at both rounds; time-anchored honest-acknowledgement git ls-tree commands; Appendix A scaffolding for verbatim Round-1 reviewer-return text; 3-tier verdict menu commitment; TL;DR structure-not-conclusions; PR-webhook handling commitment.
- Bias-guards-concurrent decision (per Phase-7 ADR draft). Audit subagents fire concurrent ONLY if their input streams are independent of per-candidate outputs. Hypothesis-falsifier reads all 10 lean-evals → serial AFTER Wave 8.1. Domain-practitioner + falsification-designer could be concurrent per-candidate.
- Matrix-flag over spec-patches discipline (per Phase-7 ADR draft). Phase 8 produces brief designs, not content patches — there's no obvious analog of Wave 7.3 spec-patches. But if any bias-guard surfaces a "rewrite the brief vs flag in cross-candidate evaluator-brief" question, prefer the flag.
- Falsifier discipline is load-bearing. Every per-candidate brief must name its falsifying outcome verbatim. Every cross-candidate brief must name the DEC-1.a falsifying result pattern verbatim. Briefs that hand-wave the falsifier get rewritten. This is the load-bearing discipline that makes Phase 8 the actual pressure-testing surface rather than another internal-consistency exercise.
- Full-package retrospective at run close. Per AGENTS-MD-1d7c94415e: no lean-mode unless context is mechanically exhausted. Author retro artifacts INLINE — the Phase-7 run learned the hard way that delegating sibling-artifact authoring to subagents produces thinner content than inline authoring (full retrospective material in retrospective/2026-05-27-191/).
- All AGENTS.md rules apply. Re-read the file (and the 5 proposed-but-not-yet-adopted retrospective rules) before dispatch; don't rely on memory.

## Non-load-bearing carry-forwards from Phase 7 (optional, not Phase-8 blockers)

Per the Phase-7-close handoff "advisory carry-forwards":

1. Word-budget tier-table recalibration — adopt at auto-008 Round 1 authoring (recommended; see §"First decision" item 2 above).
2. Common silent-absorption flags as future skill-rule (auto-detect cite-gap during spec/brief authoring). Not Phase-8 territory; could be a separate run if user wants it.
3. ADR-0036 framing glossary clarification — non-blocking; could land in decisions-captured.md as a one-line clarification or be deferred.

None of these block Phase 8's main work.

## What "Phase 8 closed" looks like

- 10 per-candidate lean-evals/<id>.md briefs with mandatory falsifying-outcome: YAML field populated.
- 1 cross-candidate lean-evals/00-cross-candidate.md with DEC-1.a falsifying result pattern named in advance.
- 3 bias-guard audit outputs (domain-practitioner; falsification-designer; hypothesis-falsifier).
- architectures/v3/SESSION-HANDOFF-<UTC-DATE>-phase-8-close.md with downstream-simulator-harness entry posture.
- Phase 8 unblocked (downstream simulator harness execution; outside v3 synthesis pipeline).
- All work committed, pushed, PR'd, and merged. No drafts; no unmerged work at session close.
```

---

## Provenance

Authored at end of the Phase-7 autonomous run (2026-05-27). See:

- [`run-summary-2026-05-27-phase-7.md`](run-summary-2026-05-27-phase-7.md) — Phase-7 run summary.
- [`retrospective/2026-05-27-191.md`](retrospective/2026-05-27-191.md) — Phase-7 retrospective.
- [`architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md`](architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md) — active handoff at Phase-8 start.
- Phase-7 PR stack: #187 (envelope) → #188 (auto-007) → #189 (BF-S exemplar) → #190 (fanout omnibus) → #191 (handoff) → #192 (summary + retro).
