# Agent entry document

This is the top-level navigation document for new agent sessions on this repo. It **names what is contained where** so a fresh agent can locate the right sub-doc without eagerly loading everything. Per the [context-slimming plan](CONTEXT-SLIMMING-PLAN.md), this entry doc deliberately does NOT restate the content of the docs it points at — it only names the topics each doc covers, so it stays accurate when those docs change.

**Reading rule.** Always read [`AGENTS.md`](AGENTS.md) first (binding conventions; required by the harness hook before any non-Read tool). Then read this file. Then follow the navigation for your stated task. If your task matches one of the [task-aware reading lists](#reading-lists-by-task) below, follow that list. Otherwise, navigate from sections 1–7 on demand.

**Discipline for editors of this file.** Each navigation line **names a topic**, it does not **summarize the conclusion**. One-line heuristic: would this line need updating if the sub-doc changed its conclusion? If yes, it restates content — rewrite to name the topic instead.

---

## 1. Binding conventions

- [`AGENTS.md`](AGENTS.md) — project conventions for AI agents; PR-default-to-ready-for-review rule; real-subagent adversarial-review rule; internal-document-references rule; process-skills non-negotiable triggers.

## 2. Current state

- [Phase-4 close handoff](architectures/v3/SESSION-HANDOFF-2026-05-25-phase-4-close.md) — pickup brief for the next agent; Phase-4 close state per concern; per-candidate Phase-5 entry posture; Phase-5 entry checklist; open questions for the next agent; current git PR-chain state. **This is the active handoff.** Update this entry's link target when a new SESSION-HANDOFF is written.

## 3. Plan

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

### Phase 5 dispatch shape decision (`auto-005`)

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
