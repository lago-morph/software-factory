# Spec: `coverage-ledger-batch-cadence`

- **ID**: SKILL-SPEC-d7d47fca26
- **Source retrospective**: ../2026-05-31-220.md

## Intent

Orchestrate authoring of a large uniform-schema corpus (dozens of component spec+plan docs) as per-batch build -> adversary-review -> integrator waves, gated by a four-axis coverage ledger {Built, Reviewed, Incorporated, iNtegrated} that is the mechanical guarantee no component ships unreviewed or with findings left in limbo. It earns its place because a long run that can be cut off at any token-window boundary must keep completed batches fully closed and minimize unreviewed surface at every instant -- which this pattern achieved across 57 components with zero missed reviews.

## Trigger

- **Direct:** the user asks to author/extend a large corpus of uniform-schema artifacts (specs, plans, modules, docs) "in batches", "with review", "don't miss any", "all checks incorporated", or names a dependency-ordered batch plan.
- **Proactive:** a task decomposes into ~15+ independent authoring units that each owe more than one pass (e.g. build + adversary-review + integration), especially under an unattended/long-run framing where truncation is expected.
- **Negative:** a one-shot doc, a handful of units with a single pass each, or work that is not uniform-schema (use `parallel-subagent-fanout` or `disk-fanout-orchestration` directly instead).

## Inputs

- A canonical component inventory (IDs, slugs, deps, per-component gap/issue IDs) and a dependency-ordered batch plan.
- A standing builder brief and adversary brief, plus a decision ledger file and a per-component template/exemplar.
- The governing "bar" (what to keep vs drop) and any binding prior decisions (D-1.., etc.).
- Concurrency cap (here ~8) and the branch/PR the run commits to.

## Outputs

- Per component: `spec/<ID>-*.md` + `plan/<ID>-*.md` + `spec/<ID>-*.review.md`.
- A coverage ledger (one row/component × {B,R,I,N}) kept current every wave.
- Numbered cross-component decisions appended to the ledger; OQs harvested per batch.
- Checkpoint commits each wave; a run-summary + refreshed handoff at close.

## Workflow

1. **Stand up the ledger.** Create the four-axis table (rows = all components incl. any already built; columns B/R/I/N). Mark existing evidence honestly — this is where pre-existing review debt becomes visible.
2. **Per batch, build wave:** dispatch one builder/component (≤cap; pipeline, draining to ~2 before topping up). Each writes its files + returns a ≤12-line receipt; subagents never run git. Commit+push every wave; mark B✓.
3. **Per batch, review wave:** dispatch one adversary (critic-fixer)/component. Each writes `<ID>.review.md`, applies confident fixes in place, and flags architecturally-significant items DEFERRED. For parallel-built siblings sharing a seam, brief each adversary to read the sibling's spec. Mark R✓.
4. **Integrator pass:** the orchestrator authors any cross-component rulings (numbered, in the ledger); one integrator subagent transcribes + applies them corpus-wide and harvests OQs. Mark I✓ and N✓.
5. **Close the batch** in the ledger; only then open the next batch. Carry the owed-review debt (any built-but-unreviewed components) into the first review wave.
6. **At run end:** the ledger must be ✓ on all four axes for every row; write the run-summary + refresh the handoff; surface provisional/risk-tolerance rulings as morning-review items.

## Concrete examples

**Example A — clearing silent review debt.** The v4 run inherited 23 built components, of which 11 ("Batch-2-partial": C04,05,09,10,12,13,24,25,28,29,42) had been built in an earlier two-track phase but never adversary-reviewed. Standing up the ledger immediately showed those 11 as `B✓ R· I· N·`. The first review wave folded them in alongside the 2 new tail components (C26,C27) — 13 adversaries pipelined 8+5 — so the debt was cleared before any new batch opened. Without the ledger the 11 would have shipped unreviewed.

**Example B — a batch closing cleanly under the cadence.** Batch 4 (13 components) ran build wave (chunk 8 + chunk 5) → commit; review wave (8+5 adversaries, all `accept-with-fixes`) → commit; then the orchestrator authored D-18/D-19 + resolved XC-3 in the ledger and dispatched one integrator subagent that applied them across the corpus and harvested 59 OQs → commit. The ledger flipped Batch-4's row to `B✓ R✓ I✓ N✓` and only then did Batch 5 open. A cutoff at any instant during Batch 4 would have left Batches 1–3 fully closed.

## Anti-patterns

- **Build-all-then-review.** Under truncation this yields a pile of unreviewed specs — the exact debt the ledger exists to prevent.
- **Marking an axis ✓ without disk evidence.** "Reviewed" means a `.review.md` exists; "Incorporated" means every finding is applied or deferred-with-reason. Self-attestation drifts.
- **Letting the orchestrator read full builder/adversary outputs.** Receipts only (≤12 lines); the filesystem is the working set. Reading transcripts blows the context that sustains many waves.
- **Inventing cross-component rulings inside one component.** Conflicts go to the shared ledger as numbered decisions, then one integrator applies them corpus-wide.
- **Committing mid-wave or letting >1 wave sit uncommitted.** Checkpoint every wave; the sandbox is ephemeral.

## Acceptance criteria

1. At run end, every component row is ✓ on all four axes, verifiable from disk (spec+plan+review present; ledger decisions applied).
2. At any wave boundary, completed batches are fully closed and at most one batch is partial.
3. Every cross-component conflict is a numbered ledger decision or a harvested OQ — none silently resolved inside a single component.
4. Pre-existing review debt is surfaced by the ledger at stand-up, not discovered at the end.
5. The run is recoverable from disk alone: coverage ledger + decision ledger + run-summary reconstruct state with no transcript.

## Files this skill creates / modifies

- `<corpus>/STATUS.md` (or equivalent) — the four-axis coverage ledger, updated every wave.
- `<corpus>/review-log.md` (or equivalent) — numbered cross-component decisions + harvested OQs.
- `spec/<ID>-*.md`, `plan/<ID>-*.md`, `spec/<ID>-*.review.md` — per-component deliverables (written by subagents).
- `run-summary.md` + the handoff doc — written at close.
