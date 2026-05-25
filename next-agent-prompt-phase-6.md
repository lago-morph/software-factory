# Next-agent dispatch prompt — Phase 6 entry (architecture-spec authorship per candidate)

**Generated:** 2026-05-25 (Phase 5 closed; all 55 ADRs landed across PRs #165-#177).
**Designed for:** the first unattended / autonomous session of Phase 6.

Copy from `START HERE` down into the new session prompt.

---

## START HERE

You are operating in autonomous (unattended) mode. The user has delegated execution for this run; do not wait for confirmations on reversible decisions. Per the autonomous-run skill, your first action is to write a one-page scope envelope and post it to the user before any non-Read tool call.

## Read order (minimal)

In order, before any non-Read tool call after the scope envelope:

1. [`AGENTS.md`](AGENTS.md) — binding conventions (14 rules; ~116 lines).
2. [`AGENT-ENTRY.md`](AGENT-ENTRY.md) — root navigation. Follow it to the current SESSION-HANDOFF (now `architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5-close.md`) and pull the per-task reading list for "Phase 6 architecture-spec authorship".

Do NOT eagerly load the 55 Phase-5 ADRs. Each per-candidate subagent will load only the ADRs that candidate references (per the ADR-ID-to-file mapping in the Phase-5-close handoff).

## What to build

Phase 6 produces **one architecture spec per surviving candidate** — 10 specs total — composing each candidate's substrate + discipline + per-variant ADR set into a coherent architecture description. Per the [v1.2 plan § Phase 6](ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-6--architecture-spec-authorship-one-per-surviving-candidate-revised-in-v12), each spec also contributes a row to a cross-candidate **mandate-fit matrix** (10 rows × work-unit-classes per [DEC-2](architectures/v3/decisions-captured.md#dec-2)).

### Sub-product breakdown

- **10 architecture specs**, one per candidate (GF-S, GF-M, GF-C, BF-S, BF-M, BF-L, U-A, U-B, U-C, D7-U-1). Each spec is a self-contained markdown document describing how the candidate composes its substrate ADRs + discipline ADRs + per-variant ADRs + methodology shape + cycle structure. Spec word budget: TBD via `auto-006` (suggested default: 2000-3500 words per spec).
- **1 mandate-fit matrix** comparing all 10 candidates across work-unit-classes. Authored at Phase-6 close as the aggregation artifact.
- **Phase-6-close session handoff** unblocking Phase 7 (back-fill audit per candidate against archived v1/v2).
- **Morning summary + retrospective** per the autonomous-run end-of-run protocol.

## First decision — write `auto-006`: Phase-6 dispatch shape

Phase 6 is amenable to per-candidate parallel fanout (same shape as Phase 4 Wave 4.1 worked cleanly). Open questions for the brief:

1. **Wave shape.** 10 per-candidate parallel subagents in one wave? Or sub-cluster by mandate (greenfield batch / brownfield batch / unified-attempt batch) to keep aggregation tractable?
2. **Per-spec rubric.** Section structure (Overview / Substrate composition / Methodology / Discipline binding / Mandate fit / Open carries / References); word budget; mandatory cross-reference floor to ADR set (probably ≥(common ADRs + per-variant ADRs + relevant discipline ADRs) for that candidate).
3. **Exemplar choice.** Per [AGENTS-MD-eec503a3c2](AGENTS.md#exemplar-before-parallel-uniform-schema-fanout) — least-contested candidate (GF-M is the historical exemplar from Wave 4.1; could reuse).
4. **Mandate-fit matrix shape.** One row per candidate; columns = work-unit-classes per [DEC-2](architectures/v3/decisions-captured.md). Authored by lead agent inline after per-candidate specs land, or dispatched as its own subagent?
5. **Cross-spec consistency check.** After 10 specs land, dispatch fresh-context verification subagents (per [SKILL-SPEC-ad9a173772 phase-A-fresh-context-verification](retrospective/2026-05-25-170/SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md)) to verify: every ADR is referenced by at least one spec; no spec references a non-existent ADR; mandate-fit claims are consistent with the candidate's claimed substrate.

Per [AGENTS-MD-d72e1a4f3c](AGENTS.md#adversarial-review-must-be-real-subagents): dispatch ≥3 real adversarial subagents in Round 1, then ≥3 more in Round 2 with fresh angles. Per [AGENTS-MD-8a7029647f](AGENTS.md#adversarial-review-verdict-tiers): 3-tier verdict scheme.

Land `auto-006` as its own stacked PR before any spec-authoring subagent fires.

## Working mode reminders

- **Scope envelope first** (per autonomous-run skill). Wait briefly for user reply; proceed with envelope as written if no response.
- **PR-cap budget.** Phase 5 used 13 PRs in this run. Phase 6 should fit in ≤15: 1 for `auto-006` brief + 3-4 for spec sub-waves + 1 for mandate-fit matrix + 1 for handoff + 1 for morning summary + 1 for retrospective.
- **Per-ADR rubric inheritance.** Architecture specs inherit the ADR rubric discipline (alternatives ≥2, references mandatory). Per [AGENTS-MD-8740bd7b0a](AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs): publish the full ADR-ID-to-file mapping (already in the Phase-5-close handoff) in every per-candidate spec brief.
- **Variant-bearing primitives.** Per [AGENTS-MD-a9fb7b42f8](AGENTS.md#framework-adr-scope-boundary-discipline): when a spec references a framework ADR (P-19/P-28/P-29/P-30 frameworks), it MUST also reference the candidate's per-variant ADR. The Phase-6 cross-reference check verifies this.
- **Full-package retrospective at run close.** Per [AGENTS-MD-1d7c94415e](AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern): no lean-mode unless context is mechanically exhausted.
- **All 14 rules in AGENTS.md apply.** Re-read the file before dispatch; don't rely on memory.

## What "Phase 6 closed" looks like

- 10 architecture spec files under `architectures/v3/specs/<candidate-id>.md` (or per-candidate-dir per `auto-006`).
- 1 mandate-fit matrix under `architectures/v3/mandate-fit-matrix.md`.
- `architectures/v3/SESSION-HANDOFF-<UTC-DATE>-phase-6-close.md` with Phase 7 entry posture.
- Phase 7 unblocked (per the v1.2 plan, Phase 7 = back-fill audit per candidate against archived v1/v2; per-candidate sub-fanout shape, analogous to Phase 6).
- All work committed, pushed, PR'd, and merged. No drafts; no unmerged work at session close.
