# Agent entry document

This is the top-level navigation document for new agent sessions on this repo. It **names what is contained where** so a fresh agent can locate the right sub-doc without eagerly loading everything. Per the [context-slimming plan](CONTEXT-SLIMMING-PLAN.md), this entry doc deliberately does NOT restate the content of the docs it points at — it only names the topics each doc covers, so it stays accurate when those docs change.

**Reading rule.** Always read [`AGENTS.md`](AGENTS.md) first (binding conventions; required by the harness hook before any non-Read tool). Then read this file. Then follow the navigation for your stated task. If your task matches one of the [task-aware reading lists](#reading-lists-by-task) below, follow that list. Otherwise, navigate from sections 1–7 on demand.

**Discipline for editors of this file.** Each navigation line **names a topic**, it does not **summarize the conclusion**. One-line heuristic: would this line need updating if the sub-doc changed its conclusion? If yes, it restates content — rewrite to name the topic instead.

---

## 1. Binding conventions

- [`AGENTS.md`](AGENTS.md) — project conventions for AI agents; PR-default-to-ready-for-review rule; real-subagent adversarial-review rule; internal-document-references rule; process-skills non-negotiable triggers.

## 2. Current state

- [Factory discovery charter](factory-discovery-charter.md) — the why/how/vocabulary for the **current
  phase**: exercising and evolving the v4 factory by building a portfolio of real projects (agent-os
  first) through it. Names the co-implementation framing, the prototype-for-discovery stance, the
  trust map (🌑→🌕), the play-menu-of-cards selection model, the toy/reduced-model/driver/self-build
  vocabulary, the two ledgers, the hard-won rules-of-the-game, and the fun-first constraint. **Read
  this for the feel before the v4 design docs.** Practical companions: [next-steps report](next-steps-plain-english.md),
  [methodology & formulas](methodology-and-formulas-plain-english.md).
- [Session handoff (2026-06-06) — board + backbone-plan close](architectures/v4/SESSION-HANDOFF-2026-06-06-board-and-backbone-plan-close.md)
  — **the active handoff.** Records that the planning arc is closed (Step 1 board + Step 2 backbone build
  plan both merged) and that the next work is Step 3 (execute), which is **gated on a real environment** —
  the ephemeral web sandbox can author and commit but cannot host the running factory. Names the Gate-B0
  entry blocker (which host), the in-sandbox prep that needs no answer, and task-aware reading lists.
  Update this entry's link target when a newer handoff is written.
- [Discovery-phase session handoff (2026-06-05)](architectures/v4/SESSION-HANDOFF-2026-06-05-discovery-charter-and-next-steps.md)
  — **superseded by the 2026-06-06 handoff above.** Records that the discovery charter + plan were merged
  with no factory code yet, and named the three steps (board / backbone plan / execute); Steps 1–2 are now done.
- [Board 1 — the opening play menu](BOARD.md) — the first **board of cards** (handoff Step 1): the
  shakedown-cruise card set for the backbone-25, the live trust map, the per-card pressure targets, the
  two ledgers, and the operator decisions settled for this board (real-drivers-are-self-builds-only,
  portfolio-frozen, bead-viewer-added).
- [Phase-8 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-28-phase-8-close.md) — pickup brief for the next agent; **Phase 8 fully closed with 10 per-candidate lean-eval briefs + 3 cross-candidate bias-guard audits + lead-agent cross-check artifact + cross-candidate evaluator-brief**; DEC-1.a falsifying result pattern named verbatim pre-execution (K=1 universal-negation falsifier); v3 synthesis pipeline COMPLETE; downstream simulator-harness execution is post-v3 scope; task-aware reading lists for downstream-simulator-harness picker + retrospective reviewer. **The active handoff for the v3 synthesis phase** (superseded for the current v4 discovery phase by the 2026-06-06 handoff above).
- [Phase-7 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md) — superseded by Phase-8-close above. Phase 7 closed with 10 per-candidate back-fill notes + 2 bias-guard audits + lead-agent aggregation matrix; Wave 7.3 spec patches NOT FIRED. Phase-8 Phase-7-cite-obligations propagated through auto-008's per-candidate mapping table.
- [Phase-6 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md) — superseded by Phase-7-close above. Phase-6-followup carry-forwards #1/#2/#3 closed by Phase 7 (silent-absorption auditor + historian expanded mandates).
- [Phase-5 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5-close.md) — superseded by Phase-6-close + Phase-7-close above. **Note**: per-candidate ADR set table has documentation defects on BF-M + BF-L rows; see the Phase-7-close handoff erratum-extension for the full correction set.

## 3. Plan

- [Backbone implementation plan](architectures/v4/backbone-implementation-plan.md) — the plan to **build
  the first 25 components** (handoff Step 2): the adopt-vs-build classification of the 25, the five build
  gates (B0 substrate-truth → B4 shakedown), how the rules-of-the-game and the 8 panel amendments map
  onto the build, per-product "done" definitions, single-seat sizing, and the seam handing off to the
  exercising phase. **The build plan; ends where the unified plan starts.**
- [Unified plan — exercising the factory](architectures/v4/_meta/next-steps/10-unified-plan.md) — the
  panel-reviewed plan for **exercising** the built factory on real `agent-os` work (Gates 0–5: calibrate
  → drive one nail → widen behind the fence). Its horizon begins once the backbone-25 exist.
- [v3 synthesis plan](ARCHITECTURE-V3-SYNTHESIS-PLAN.md) — phased synthesis plan for the v3 architecture (Phases 0 through 8 with v1.2 revision of Phase 5 ADR-dispatch structure). **Read only the section for your current phase**; earlier phases are historical context, later phases are scaffolding. If your task is in Phase N, the Phase-N section is the binding spec for that phase.

## 4. Decisions (binding)

- [Tier-1 decisions resolved](architectures/v3/phase-3.4-decisions-resolved.md) — Tier-1 decisions resolved at Phase 3.4 close; scoping principle; refined two-part substrate-buildability rule; working definitions of architecture / substrate / methodology / discipline; entry-mode greenfield/brownfield/unified definitions.
- [Candidate registry](architectures/v3/candidate-registry.md) — 10 methodology candidates (3 greenfield, 3 brownfield, 4 unified-attempt); per-candidate mandate scope, axis declaration, required substrate primitives, methodology shape, defense status; Phase-3.5.5 RG-primitive application table updated with Wave-4.5 verdicts; Phase-4 close summary.

## 5. Substrate primitives

- [Primitive index](architectures/v3/primitives/index.md) — canonical primitive enumeration (P-01 through P-34); dispatch-tier per primitive; per-primitive claiming candidates; cluster boundaries (C1 execution & resource control, C2 ops, C3 evidence). **Read this index in full; drill into individual P-NN sketches only when a specific decision requires them.**
- [Primitive overlap verdicts](architectures/v3/primitives/overlap.md) — Phase-4.2 same-vs-distinct verdicts on primitives that looked similar across candidates; absorption decisions (P-08↔P-09, P-12↔P-16); shared-primitive count for Phase-5 Wave-5.1 ADR scope.
- [Primitive sketches directory](architectures/v3/primitives/) — directory of individual P-NN buildability sketches (24 sketches at Phase-3.5 close).

## 6. Decision briefs (historical)

- [Decisions directory](architectures/v3/decisions/) — directory of resolved decision briefs. Includes Tier-1 `dec-N` briefs from Phase 3.4 and `auto-NNN` briefs from later phases ([auto-001 Phase-3.5 dispatch shape](architectures/v3/decisions/auto-001-phase-3.5-dispatch-shape.md); [auto-002 U-B path](architectures/v3/decisions/auto-002-ub-path.md); [auto-003 BF-L per-RG-view choice](architectures/v3/decisions/auto-003-bfl-rg-view-choice.md); [auto-004 Phase-4 dispatch shape](architectures/v3/decisions/auto-004-phase-4-dispatch-shape.md)). **Read only if relevant to your current decision** — each brief is self-contained, no need to read the directory wholesale.

## 7. Disciplines

- [Disciplines index](architectures/v3/disciplines/index.md) — canonical 21-discipline list extracted from track sketches at Wave 4.3 + 4.6 merge; per-discipline owners, applicable candidates, and target architecture layer. Drives Wave-5.2 discipline ADRs.
- [Disciplines directory](architectures/v3/disciplines/) — directory of individual discipline write-ups (one per discipline + the sketch-registry extraction trace).

---

## Reading lists by task

Pre-curated per-task reading lists. If your first task is on this list, read exactly the named files and skip everything else until needed. Lists are accelerators — if your task isn't here, fall back to navigation sections 1–7.

### Step 3 entry — stand up Gas City + run the Gate B0 conformance check (on a real host)

- Read: [`AGENTS.md`](AGENTS.md), this file, [the 2026-06-06 handoff](architectures/v4/SESSION-HANDOFF-2026-06-06-board-and-backbone-plan-close.md), [backbone plan § Gate B0](architectures/v4/backbone-implementation-plan.md#gate-b0--substrate-truth-the-literal-first-move), [C01 substrate/conformance](architectures/v4/spec/C01-gas-city-substrate.md), [decision #4 prevent-vs-detect](decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact), [C43 fence](architectures/v4/spec/C43-isolation-boundary.md), [C34 holdout](architectures/v4/spec/C34-holdout-integrity.md).
- Skip: the [unified/exercising plan](architectures/v4/_meta/next-steps/10-unified-plan.md) (that phase begins after the 25 exist); all v3 synthesis docs.

### Author Gate B0/B1 prep artifacts in-sandbox (no running `gc` needed)

- Read: [`AGENTS.md`](AGENTS.md), this file, [backbone plan § Gate B0–B1](architectures/v4/backbone-implementation-plan.md#gate-b0--substrate-truth-the-literal-first-move), [C01 substrate](architectures/v4/spec/C01-gas-city-substrate.md), [C03 config](architectures/v4/spec/C03-config-feature-flags.md), [C20 bead schema](architectures/v4/spec/C20-bead-schema.md), [C08 spec artifact](architectures/v4/spec/C08-spec-artifact.md), [methodology companion](methodology-and-formulas-plain-english.md).
- Skip: eval-tier (C30–C33), fence-holdout (C34), and bootstrap (C51–C53) specs until their gates.

### Downstream simulator-harness picker (post-v3 entry point)

- Read: [`AGENTS.md`](AGENTS.md), this file, [Phase-8 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-28-phase-8-close.md), [cross-candidate evaluator-brief](architectures/v3/lean-evals/00-cross-candidate.md), all 10 per-candidate lean-eval briefs at [`architectures/v3/lean-evals/<id>.md`](architectures/v3/lean-evals/), the 3 bias-guard audits at [`architectures/v3/lean-evals/audit-*.md`](architectures/v3/lean-evals/), [DEC-1.a working hypothesis](architectures/v3/decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8).
- Skip: per-candidate `specs/` + `backfill-notes/` (referenced from lean-eval briefs; drill on demand); ADRs (drill on demand).

### Phase 8 dispatch shape decision (`auto-008`, historical)

- Read: [`AGENTS.md`](AGENTS.md), this file, [Phase-7 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md), [v3 synthesis plan § Phase 8](ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12), [auto-007 Phase-7 dispatch shape brief](architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md) (precedent for `auto-NNN` brief shape), [Phase-7 aggregation matrix](architectures/v3/backfill-notes.md) for Phase-8 brief inputs (cite obligations + reconciliation TBDs + historian load-bearing gaps), [autonomous-run skill](.claude/skills/autonomous-run/SKILL.md).
- Skip: per-candidate back-fill notes (only needed when Wave 8.1 per-candidate briefs are authored); per-candidate specs (only needed for content authoring, not dispatch shape).

### Phase 8 per-candidate lean-eval brief authoring (Wave 8.1; after auto-008 fires)

- Read per candidate: [`AGENTS.md`](AGENTS.md), this file, [Phase-7 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md), the candidate's `architectures/v3/specs/<id>.md`, the candidate's `architectures/v3/backfill-notes/<id>.md`, the candidate's open-carries from `specs/<id>.md` §6, the auto-008 brief (when authored), the cite obligations from [aggregation §3.1](architectures/v3/backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule) that touch this candidate.
- Skip: other candidates' specs + back-fill notes.

### Phase 8 cross-candidate evaluator-brief (Wave 8.2; after Wave 8.1 closes)

- Read: [`AGENTS.md`](AGENTS.md), this file, [Phase-7 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md), all 10 candidate `architectures/v3/lean-evals/<id>.md` files (after Wave 8.1 lands), [DEC-1.a falsifier discipline](architectures/v3/decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), [aggregation §6.4 DEC-1.a observation](architectures/v3/backfill-notes.md#64-dec-1-a-working-hypothesis-observation-neutral-pre-phase-8).
- Skip: per-candidate specs (already absorbed via lean-eval brief authoring); per-candidate back-fill notes (Phase-7 done).

### Phase 5 dispatch shape decision (`auto-005`, historical)

- Read: [`AGENTS.md`](AGENTS.md), this file, [Phase-4 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-25-phase-4-close.md), [v3 synthesis plan § Phase 5](ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12), [Primitive overlap verdicts](architectures/v3/primitives/overlap.md), [Disciplines index](architectures/v3/disciplines/index.md), [auto-004 Phase-4 dispatch shape](architectures/v3/decisions/auto-004-phase-4-dispatch-shape.md) (precedent for `auto-NNN` brief shape), [autonomous-run skill](.claude/skills/autonomous-run/SKILL.md), [decision-brief adversarial-review lifecycle SKILL-SPEC](retrospective/2026-05-25-155/SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md).
- Skip: per-candidate substrate-requirements (only needed when ADRs are authored), per-primitive sketches (drill on demand).

### Phase 5 ADR Wave 5.1 dispatch (common-primitive ADRs)

- Read: [`AGENTS.md`](AGENTS.md), this file, [Primitive overlap verdicts](architectures/v3/primitives/overlap.md), [Primitive index](architectures/v3/primitives/index.md), [adr skill](.claude/skills/adr/SKILL.md), [parallel-fanout-with-exemplar-and-rubric SKILL-SPEC](retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md), the per-primitive sketches under [primitives directory](architectures/v3/primitives/) for the primitives appearing in the wave (drill as needed), the per-candidate substrate-requirements summaries under [substrate-requirements directory](architectures/v3/substrate-requirements/) for §3 candidate-specific contracts on each common primitive.
- Skip: candidate-specific-only primitives, discipline write-ups (those are Wave 5.2).

### Phase 5 ADR Wave 5.2 dispatch (discipline ADRs)

- Read: [`AGENTS.md`](AGENTS.md), this file, [Disciplines index](architectures/v3/disciplines/index.md), individual discipline write-ups under [disciplines directory](architectures/v3/disciplines/), [adr skill](.claude/skills/adr/SKILL.md), [parallel-fanout-with-exemplar-and-rubric SKILL-SPEC](retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md).
- Skip: primitive sketches (those are Wave 5.1 territory).

### Phase 5 ADR Wave 5.3 dispatch (candidate-specific ADRs)

- Read: [`AGENTS.md`](AGENTS.md), this file, the candidate's entry in [Candidate registry](architectures/v3/candidate-registry.md), the candidate's file under [substrate-requirements directory](architectures/v3/substrate-requirements/), the candidate-specific primitive sketches under [primitives directory](architectures/v3/primitives/) (orphans + per-variant), the merged ADRs from Waves 5.1 + 5.2 under [docs/adr directory](docs/adr/) for cross-reference, [adr skill](.claude/skills/adr/SKILL.md).
- Skip: other candidates' substrate-requirements and orphan primitives.

### Drain incoming `research/manual/` sources

- Read: [`AGENTS.md`](AGENTS.md), this file, [research-pipeline skill](.claude/skills/research-pipeline/SKILL.md), [preliminary-index-pass skill](.claude/skills/preliminary-index-pass/SKILL.md), [research PLAN](research/PLAN.md), [research INDEX](research/INDEX.md).
- Skip: architecture synthesis docs.

### Adopt Phase-4 retrospective rules into `AGENTS.md`

- Read: [`AGENTS.md`](AGENTS.md), this file, [retrospective 2026-05-25-155](retrospective/2026-05-25-155.md) §Part 3, each of the seven `AGENTS-MD-*.md` rule drafts under [retrospective 2026-05-25-155 directory](retrospective/2026-05-25-155/).
- Skip: synthesis docs, primitive sketches (this task is meta-governance, not synthesis).

---

## Maintenance

This file is updated at end-of-run when the SESSION-HANDOFF is rotated:

1. Update section 2's link target if a new SESSION-HANDOFF was written.
2. Refresh the [Reading lists by task](#reading-lists-by-task) section from the handoff's "next likely tasks" if the SESSION-HANDOFF template carries one (per the PR A3 update to [autonomous-run handoff-doc template](.claude/skills/autonomous-run/resources/template-handoff-doc.md)).
3. If any sub-doc was renamed or moved, fix the link here and run [`check-internal-refs.py`](scripts/check-internal-refs.py) to catch the rest.

Do **not** rewrite navigation lines to incorporate sub-doc conclusions. This file stays accurate when sub-docs change because it only names topics, never restates content.
