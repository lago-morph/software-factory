# Next-agent dispatch prompt — Phase 7 entry (back-fill audit per candidate against archived v1/v2)

**Generated:** 2026-05-27 (Phase 6 closed; 10 specs + matrix + verifier PASS WITH AMENDMENTS landed via PRs #181-#185).
**Designed for:** the first unattended / autonomous session of Phase 7.

Copy from `START HERE` down into the new session prompt.

---

## START HERE

You are operating in autonomous (unattended) mode. The user has delegated execution for this run; do not wait for confirmations on reversible decisions. Per the [`autonomous-run` skill](.claude/skills/autonomous-run/SKILL.md), your first action is to write a one-page scope envelope and post it to the user before any non-Read tool call.

## Read order (minimal)

In order, before any non-Read tool call after the scope envelope:

1. [`AGENTS.md`](AGENTS.md) — binding conventions (17 rules; ~134 lines).
2. [`AGENT-ENTRY.md`](AGENT-ENTRY.md) — root navigation. Follow it to the current SESSION-HANDOFF (`architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md`) and pull the per-task reading list for "Phase 7 back-fill audit".

**Run the new pre-flight check first.** Per the newly-adopted [`AGENTS-MD-4f8c2a1b03`](AGENTS.md#pre-flight-prior-phase-merge-state-verification), before any new-phase work fires, verify the Phase-6 deliverables are actually in `main`:

```bash
git fetch origin main
git ls-tree -r origin/main --name-only | grep -cE "architectures/v3/specs/" # expect 10
git ls-tree -r origin/main -- architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md
git ls-tree -r origin/main -- architectures/v3/mandate-fit-matrix.md
git ls-tree -r origin/main -- architectures/v3/phase-6-verification-findings.md
```

If any check fails, surface to user via AskUserQuestion before proceeding.

Do NOT eagerly load the 10 Phase-6 specs or the 55 Phase-5 ADRs. Each per-candidate subagent will load only the spec it audits + the archive items it considers.

## What to build

Phase 7 produces a **per-candidate back-fill audit** against archived v1/v2 material. For each candidate, the audit asks: "what's in the archived synthesis material that didn't make it into the candidate's Phase-6 spec? Was it absorbed silently, rejected with reason, or genuinely missed?"

### Sub-product breakdown

- **One `backfill-notes.md` aggregation file** at `architectures/v3/backfill-notes.md` with one section per archive item × 10 candidate columns; each cell classified as `absorbed`, `rejected (reason)`, or `TBD`. Alternative shape per `auto-007`: per-candidate `backfill-notes/<candidate-id>.md` × 10 files. Default: aggregation file (simpler).
- **Per-candidate spec patches** for any absorbed material — stacked PRs targeting `architectures/v3/specs/<id>.md`.
- **Phase-7-close session handoff** unblocking Phase 8 (lean-eval design per candidate).
- **Morning summary + retrospective** per the autonomous-run end-of-run protocol.

### Bias guards (per the v1.2 plan § Phase 7)

- **Silent-absorption auditor.** Compares each final candidate spec to archive *independently* of the lead-agent classification. Surfaces disagreements — particularly cases where the lead agent classified something `rejected` for a candidate that the auditor thinks slipped in anyway.
- **Historian.** "What's in the archive that doesn't appear in *any* candidate spec in any form?" Independent gap detection.

## First decision — write `auto-007`: Phase-7 dispatch shape

User confirmed at Phase-6-close that Phase 7 should use **per-candidate parallel fanout** (10 subagents, one per candidate, each auditing one spec against the archive). `auto-007` formalizes this. Open questions for the brief:

1. **Wave shape.** Default = 10 per-candidate parallel subagents in one wave. Each subagent reads one spec + the full archive (or a topic-indexed slice) and produces its candidate's row of the back-fill matrix.
2. **Archive scope.** Which archive directories are in scope? At minimum: [`archive/synthesis-v1-v2/`](archive/). Possibly: [`archive/architectures-v2/`](archive/). Verify directories exist at brief-write time.
3. **Per-candidate rubric.** What classification taxonomy beyond `absorbed | rejected | TBD`? Suggested: include a `not-applicable-to-candidate` token for items that are mandate-specific to a candidate the audited candidate doesn't claim.
4. **Aggregation vs per-file output.** Default: aggregation file. Alternative: per-candidate file + lead-agent-authored aggregation at run close.
5. **Bias-guard dispatch.** Silent-absorption auditor + historian — fire concurrent with the per-candidate fanout, or after? Default: concurrent (independent input streams).
6. **Phase-7-followup deferral mechanism.** Same shape as Phase-6's binding-artifact triple per [`AGENTS-MD-2adf78e54a`](AGENTS.md#deferred-work-binding-artifact-triple) — pre-author the deferral artifact-set if any candidate's back-fill is expected to defer.

Per [`AGENTS-MD-d72e1a4f3c`](AGENTS.md#adversarial-review-must-be-real-subagents): dispatch ≥3 real adversarial subagents in Round 1, then ≥3 more in Round 2 with fresh angles. Per [`AGENTS-MD-8a7029647f`](AGENTS.md#adversarial-review-verdict-tiers): 3-tier verdict scheme (accept-as-is / accept-with-named-amendments / reject-with-counter-proposal). Land `auto-007` as its own stacked PR before any back-fill subagent fires.

## Working-mode reminders

- **Scope envelope first** (per autonomous-run skill). Wait briefly for user reply; proceed with envelope as written if no response.
- **PR-cap budget.** Phase 6 used 5 PRs (substantially under the 15 cap thanks to omnibus consolidation per [ADR 0066](docs/adr/0066-omnibus-pr-over-sub-wave-prs-when-files-are-disjoint.md)). Phase 7 should fit in ≤10: 1 for `auto-007` brief + 1-2 for back-fill fanout (omnibus per ADR 0066 if files are disjoint) + 1 for any spec-patch sub-PRs + 1 for handoff + 1 for morning summary + 1 for retrospective.
- **Webhook verification.** Per the newly-adopted [`AGENTS-MD-c5a92e6017`](AGENTS.md#pr-webhook-merged-is-advisory-not-authoritative), `merged` webhook notifications MUST be verified via `mcp__github__pull_request_read` before acting.
- **Omnibus consolidation.** Per [`AGENTS-MD-d71e845b29`](AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint), if `auto-007` plans sub-wave PRs but actual delivery has shared parent branch + disjoint files, consolidate to omnibus and acknowledge in 3 places (PR body, handoff, morning summary).
- **§0 ADR-citation index format.** Per [ADR 0065](docs/adr/0065-section-0-adr-citation-index-table.md), back-fill spec patches that touch ADR citations should preserve §0 table consistency in the patched spec.
- **Variant-bearing primitives.** Per [`AGENTS-MD-a9fb7b42f8`](AGENTS.md#framework-adr-scope-boundary-discipline): if a back-fill spec patch adds a framework-ADR reference, it MUST also add the candidate's per-variant ADR reference.
- **Full-package retrospective at run close.** Per [`AGENTS-MD-1d7c94415e`](AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern): no lean-mode unless context is mechanically exhausted.
- **All 17 rules in AGENTS.md apply.** Re-read the file before dispatch; don't rely on memory.

## Non-load-bearing carry-forwards from Phase 6 (optional, not Phase-7 blockers)

Per the [Phase-6-close handoff](architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md) Phase-6-followup section:

1. **BF-L 0036 framing alignment with U-A/D7-U-1.** Verifier Finding-2; non-blocking; defer to Phase 7 / Phase 8 if operator confusion surfaces during the back-fill audit. Address only if a Phase-7 subagent surfaces it as a real ambiguity.
2. **Cross-spec characterization audit of shared framework ADRs.** Optional Phase-7 sub-step; could surface naturally during back-fill.
3. **Phase-5-close handoff documentation hygiene pass.** Only the BF-M / 0049 row was identified as defective; a full sweep could find others. The erratum in the Phase-6-close handoff is the canonical correction; full sweep is optional QoL.

None of these block Phase 7's main work.

## What "Phase 7 closed" looks like

- [`backfill-notes.md`](architectures/v3/backfill-notes.md) at the aggregation file (or `backfill-notes/` per-candidate directory per `auto-007`) with all 10 candidate columns filled.
- Any absorbed-material spec patches merged to `architectures/v3/specs/<id>.md`.
- [`architectures/v3/SESSION-HANDOFF-<UTC-DATE>-phase-7-close.md`](architectures/v3/) with Phase 8 entry posture.
- Phase 8 unblocked (per the v1.2 plan, Phase 8 = lean-eval design per candidate; per-candidate sub-fanout shape, analogous to Phase 6 and Phase 7).
- All work committed, pushed, PR'd, and merged. No drafts; no unmerged work at session close.
