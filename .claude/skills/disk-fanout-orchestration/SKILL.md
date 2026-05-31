---
name: disk-fanout-orchestration
description: Orchestrate massively-parallel subagent authoring where each subagent writes its deliverable to disk and returns only a short receipt, so the orchestrator's context stays lean enough to sustain many waves of fan-out. Use when producing a large corpus of files (specs, plans, docs, many modules) that will not fit in one context window, when the user says "use subagents to the max", "spare no expense", "preserve your context window", or asks for "incredibly detailed / exhaustive" output across many components, and proactively whenever a task decomposes into ~15+ independent authoring units. Distinct from `parallel-subagent-fanout` (which puts each subagent on its own sub-branch and merges in plan order, for code): this skill keeps subagents on the shared working tree writing DISJOINT files, returns receipts instead of content, and has the orchestrator own all git.
---

# Skill: disk-fanout-orchestration

Orchestrate a large body of parallel authoring whose total output far exceeds any
single context window — without the orchestrator's context being the bottleneck.

The pattern, in one line: **subagents read source material and write their
deliverables to disk, returning only a short receipt; the orchestrator holds just
a compact backbone (a component inventory) plus a stream of receipts, commits each
wave to git, and pipelines waves at the platform's real concurrency ceiling.**

This is the method that turned a 1500+ line architecture into a 100+ document
spec/plan corpus across ~15 waves with zero context exhaustion and zero lost work
(see [`retrospective/2026-05-30-214.md`](../../../retrospective/2026-05-30-214.md)).

---

## When to use this vs `parallel-subagent-fanout`

Both fan work out to concurrent subagents. They differ in the *unit of isolation*
and what comes back:

| | `parallel-subagent-fanout` | `disk-fanout-orchestration` (this skill) |
|---|---|---|
| Isolation | one **sub-branch per subagent** + `isolation: "worktree"` | one **disjoint file path per subagent** on the shared tree |
| Returns | a PR per subtask, merged in plan order | a **≤15-line receipt** (paths + headlines + open questions) |
| Orchestrator reads | subagent reports, merges branches | only receipts + a compact inventory; **never** large docs or full output |
| Best for | code/features that need branch isolation and a merge gate | large **authoring corpora** (specs, plans, docs) where context preservation is the constraint |
| Git | each subagent commits/pushes its own branch | **only the orchestrator** runs git, committing per wave |
| Scale driver | parallelism | parallelism **+ context economy** |

Use this skill when the corpus is large, the subtasks write to **distinct files**
(no overlap → no merge step needed), and the binding constraint is keeping the
orchestrator's context from filling up. Use `parallel-subagent-fanout` when the
work is code that benefits from per-subtask branch isolation and a merge review.

Negative trigger: fewer than ~8 units, or a single deliverable — the control-plane
overhead (inventory, standing briefs, ledger) is not worth it; just do it directly
or with a one-shot fan-out.

---

## Core invariants (do not violate)

1. **The orchestrator never reads the large source docs or full subagent output
   into its own context.** Subagents read; they return receipts. The only large
   thing the orchestrator holds is the compact inventory.
2. **All real output goes to disk; receipts are for orchestration only** (see
   [AGENTS-MD-b320fa8233](../../../AGENTS.md#subagents-persist-to-disk-and-return-short-receipts)).
3. **One subagent = one (or a few) distinct file path(s).** Distinct paths mean no
   write races and no merge step.
4. **Only the orchestrator runs git.** Subagents never commit/push. The
   orchestrator commits **between waves, never mid-wave** (see
   [AGENTS-MD-91d82dcea3](../../../AGENTS.md#commit-and-push-at-every-wave-boundary)).
5. **Concurrency is capped at ~8.** Beyond that the platform rate-limits and
   silently drops the surplus (see
   [AGENTS-MD-a2077561e2](../../../retrospective/2026-05-30-214/AGENTS-MD-a2077561e2-cap-subagent-fanout-at-eight.md)).
   Pipeline instead.

---

## Step 0 — ground (a small reader wave)

Do **not** read the source corpus yourself. Dispatch 2–3 reader subagents to
decompose it, writing to disk and returning only counts + headlines:

- 1–2 **cartographers** (use different lenses — e.g. structural vs. dataflow — for
  diversity-by-redundancy) → each writes a `component-inventory-X.md`.
- 1 **skeptic** (adversarial) → writes an `ambiguities-and-gaps.md` of
  contradictions, undefined terms, missing pieces, with severities.

Then one **reconciler** fuses them into the canonical
`_meta/component-inventory.md`: stable IDs (`C01..Cnn`), one-line description,
dependencies, the gap IDs each component must address, and a dependency-ordered
batch grouping. **This inventory is the only large artifact the orchestrator keeps
in context** — it is the dispatch backbone.

---

## Step 1 — build the `_meta/` control plane

Create a `_meta/` directory holding:

- `META-PLAN.md` — the orchestration contract (this skill, instantiated for the task).
- `component-inventory.md` — the backbone from Step 0.
- `ambiguities-and-gaps.md` — the adversarial read.
- `review-log.md` — the adopted-decision ledger (see the
  `cross-component-decision-ledger` skill).
- `STATUS.md` / `HANDOFF.md` — live state + a resume runbook.

---

## Step 2 — write standing briefs (so dispatch prompts stay tiny)

Author `_meta/BUILDER-BRIEF.md` and `_meta/ADVERSARY-BRIEF.md` that encode ALL
standing instructions: what to read (the charters, templates, inventory row, gap
IDs, and only the relevant slice of the source — never the whole corpus), what to
write (exact target paths), the depth for this pass, and the **receipt format**
(≤15 lines: paths written, 1-line purpose, marks/deltas, gaps addressed/deferred,
top open question).

With the standing briefs on disk, each per-agent dispatch prompt shrinks to ~6
lines: "Follow `_meta/BUILDER-BRIEF.md`. Component: `<ID> [slug]`, one-liner: …,
track/variant: …, depth: …, write `<paths>`. Return receipt only." This is what
keeps the orchestrator's per-dispatch context cost near-constant.

---

## Step 3 — fan out in waves of ~6–8 (pipelined)

Dispatch builders **in the background** (`run_in_background: true`), one per unit,
in waves of **no more than ~8**. Each subagent writes its distinct file(s) and
returns a receipt.

- **Do not** dispatch 20+ at once — the surplus is rate-limited to zero output
  (observed: 24 attempted → 16 failed). Cap at ~8.
- **Pipeline**: when in-flight agents drain to ~2, dispatch the next chunk. This
  keeps sustained concurrency near the ceiling without losses.
- Process units in **dependency-batch order** from the inventory, so a component's
  dependencies are specced before it.
- Run cooperative (builder) and adversarial (reviewer) personas — see Step 5.

When a receipt comes back, record it briefly and move on. **Never** tail a
subagent's transcript file — it will overflow your context.

---

## Step 4 — commit every wave boundary

After a wave's receipts are in, the orchestrator stages and commits the new files
and pushes (with backoff retry). Subagents never touch git. Commit messages name
the wave/components. This is the only thing that survives the ephemeral sandbox, so
**never** let more than one wave of work sit uncommitted.

---

## Step 5 — adversarial review (cooperative + adversarial at every step)

For each unit (or subsystem group), dispatch an **adversary** persona that reads
the just-written deliverable, writes a `<unit>.review.md` sibling with findings
(severity-tagged), applies the fixes it is confident about **in place**, and defers
anything architecturally significant to the ledger. Run reviewers in their own
waves (still ~8 cap). Track-appropriate attack surface: fidelity/completeness for a
faithful track; the design itself for an optimized track.

---

## Step 6 — reconcile drift with an integrator pass

Parallel authors drift on cross-cutting choices. Use the
`cross-component-decision-ledger` skill: record each conflict resolution as a
numbered adopted decision in `review-log.md`, feed the decision id into later
briefs (so subsequent units self-align), and run a single **integrator** subagent
that applies the adopted decisions across already-written files and emits an
`INTEGRATION-PASS-N.md` consistency report.

---

## Step 7 — keep a live status + handoff

Update `_meta/STATUS.md` every wave and maintain `_meta/HANDOFF.md` as a
self-contained resume runbook (what is done, what is not, the exact resume
procedure, adopted decisions, open human questions). Because the sandbox is
ephemeral and the token budget can be cut at any time, a current handoff is what
lets a fresh session resume the fan-out with zero re-grounding.

---

## Concrete examples

**Example A — dual-track v4 spec/plan (the origin).** 57 components × 2 tracks.
Step 0: Cartographer-A (structural), Cartographer-B (dataflow), Skeptic →
`component-inventory.md` + 45-finding `ambiguities-and-gaps.md`; a reconciler
produced the canonical 57-ID inventory in 5 batches. Steps 2–6: builder waves of
~8 (one agent per component×track) wrote `spec-faithful/C21-….md` etc. and returned
receipts like *"Files: …; resolved G17; 3 FAITHFUL-FILL; OQ: …"*; adversary waves
wrote `.review.md` siblings and applied fixes; decisions D-1…D-5 in `review-log.md`
were applied corpus-wide by an integrator. 23/57 components were fully
built+reviewed+integrated before the budget ran out — all committed, nothing lost.

**Example B — N independent service modules.** Inventory = the module list with
deps. Builder brief = "implement module `<id>` against the frozen interface in
`_meta/contracts.md`; write `src/<id>/…` + `tests/<id>/…`; return a receipt of paths
+ one risk." Dispatch 8 at a time in dependency order; adversaries review each for
contract conformance; the orchestrator commits each wave. The orchestrator never
holds more than the module list + receipts, so a 60-module build never fills its
context.

---

## Anti-patterns (never do these)

- **Reading source docs or full subagent transcripts into the orchestrator.**
  Defeats the entire purpose. The transcript file is explicitly not to be tailed.
- **Dispatching >8 subagents at once.** The surplus is rate-limited to zero; you
  pay tool-uses for nothing and have to re-dispatch.
- **Letting subagents run git.** Causes working-tree races. Centralize commits in
  the orchestrator, between waves.
- **Fat per-agent prompts.** Push standing instructions into brief files; keep
  dispatch prompts to ~6 lines.
- **Skipping the ledger / integrator.** Parallel authors drift on cross-cutting
  decisions and the corpus silently becomes inconsistent.
- **Letting work sit uncommitted across multiple waves.** The sandbox is
  ephemeral; an unreclaimed wave of expensive output vanishes on container reset.
- **Using this for code that needs branch isolation or a merge gate.** That is
  `parallel-subagent-fanout`'s job.

---

## Acceptance criteria

1. Orchestrator context stays bounded (no large doc reads) across the whole run.
2. Every deliverable is on disk and committed within one wave of being produced.
3. Sustained concurrency tracks the ~8 ceiling without rate-limit losses.
4. Cross-component decisions are captured once and reproduced by later agents.
5. A current `HANDOFF.md` lets a cold session resume without re-reading the source.

---

## See also

- [`parallel-subagent-fanout`](../parallel-subagent-fanout/SKILL.md) — sub-branch + merge model for code.
- [`cross-component-decision-ledger`](../cross-component-decision-ledger/SKILL.md) — the consistency mechanism Step 6 uses.
- [`subagent-prompting`](../subagent-prompting/SKILL.md) — brief construction.
- [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md) — tracking background dispatch that won't return synchronously.
- [ADR 0067](../../../docs/adr/0067-dual-track-per-component-v4-layout.md) — the corpus layout this orchestration produces.
- [`retrospective/2026-05-30-214.md`](../../../retrospective/2026-05-30-214.md) — the session this skill was extracted from.
