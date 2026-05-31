# Spec: `disk-fanout-orchestration`

- **ID**: SKILL-SPEC-3fb4e487e9
- **Source retrospective**: ../2026-05-30-214.md

## Intent

Orchestrate a large body of parallel subagent work whose total output far exceeds any single context window, without the orchestrator's context being the bottleneck. The pattern: subagents read source material and write their deliverables **to disk**, returning only a short receipt; the orchestrator holds just a compact backbone (a component inventory) plus a stream of receipts, commits each wave to git, and pipelines waves at the platform's real concurrency ceiling. This session used it to turn a 1500+ line architecture into a 100+ document spec/plan corpus across ~15 waves with zero context exhaustion and zero lost work.

## Trigger

- User asks to produce "incredibly detailed" / "exhaustive" output across **many** units (components, endpoints, files) that won't fit in one context.
- User says "use subagents to the max", "spare no expense", "preserve your context window".
- Proactively: any task that decomposes into ≥15 independent authoring units where the orchestrator would otherwise have to read everything.
- Negative trigger: small tasks (<~8 units) where a single agent or a one-shot fan-out suffices — the ledger/receipt machinery is overhead there.

## Inputs

- A decomposable goal and its source material (architecture docs, a spec, a list of modules).
- A writable git working tree on a feature branch.
- The `Agent` tool with background dispatch.

## Outputs

- A `_meta/` (or equivalent) directory with: a canonical inventory (the dispatch backbone), standing persona briefs, a decision/review ledger, and a status/handoff file.
- One deliverable file per unit, written by the responsible subagent.
- A git history with one commit+push per wave.

## Workflow

1. **Ground (small wave).** Dispatch 2–3 reader subagents to decompose the source into a canonical inventory (stable IDs, deps, gaps), writing to disk and returning only counts + headlines. Reconcile to one inventory; this is the only large artifact the orchestrator keeps in context.
2. **Write standing briefs.** Author `BUILDER-BRIEF.md` / `ADVERSARY-BRIEF.md` files that encode all standing instructions (what to read, what to write, the receipt format). Per-agent prompts then shrink to ~6 lines: id, name, one-liner, track, target paths.
3. **Fan out in waves of ~6–8** (the platform ceiling — see the cap rule). Each subagent writes distinct paths and returns a ≤15-line receipt. Never read large docs or full output into the orchestrator.
4. **Pipeline.** Let in-flight agents drain to ~2, then dispatch the next chunk. Run cooperative (builder) and adversarial (reviewer) personas; reviewers apply confident fixes in place and defer architectural ones to the ledger.
5. **Commit+push every wave boundary** (orchestrator owns git; subagents never run it).
6. **Reconcile drift** with a single integrator subagent that applies adopted ledger decisions across already-written files.
7. **Maintain a status/handoff file** every wave so a fresh session (or post-truncation self) can resume with zero re-grounding.

## Concrete examples

**Example A — v4 spec/plan (this session).** 57 components × 2 tracks. Phase 0: Cartographer-A, Cartographer-B, Skeptic → `component-inventory.md` + `ambiguities-and-gaps.md`. Then builder waves of ~8 (one agent per component×track) writing `spec-faithful/C21-….md` etc., each returning a receipt like "Files: …; 3 FAITHFUL-FILL, 1 AMBIGUITY; G17 resolved; OQ: …". Adversary waves wrote `.review.md` siblings and applied fixes. An integrator applied D-1…D-5. Result: 23/57 components fully built+reviewed+integrated before the token budget ran out, all in `main`.

**Example B — N independent API endpoints.** Inventory = the endpoint list. Builder brief = "implement endpoint X against the frozen OpenAPI contract; write handler+test files; return a receipt of paths + one risk." Dispatch 8 at a time; adversary reviews each for contract conformance; commit per wave. The orchestrator never holds more than the endpoint list + receipts.

## Anti-patterns

- Reading the source docs or full subagent transcripts into the orchestrator — defeats the entire purpose (the JSONL transcript file is explicitly not to be tailed).
- Dispatching >8 at once — the surplus is rate-limited to zero (see the cap rule).
- Letting subagents run git — causes working-tree races; centralize commits.
- Fat per-agent prompts — push standing instructions into brief files and keep dispatch prompts tiny.
- Skipping the ledger — parallel agents drift on cross-cutting decisions and the corpus becomes internally inconsistent.

## Acceptance criteria

1. Orchestrator context stays bounded (no large doc reads) across the whole run.
2. Every deliverable is on disk and committed within one wave of being produced.
3. Sustained concurrency tracks the platform ceiling (~6–8) without rate-limit losses.
4. Cross-component decisions are captured once and reproduced by later agents.
5. A handoff file lets a cold session resume without re-reading the source.

## Files this skill creates / modifies

- `<root>/_meta/component-inventory.md` — the dispatch backbone.
- `<root>/_meta/BUILDER-BRIEF.md`, `ADVERSARY-BRIEF.md` — standing persona briefs.
- `<root>/_meta/review-log.md` — the adopted-decision ledger.
- `<root>/_meta/STATUS.md`, `HANDOFF.md` — live state + resume runbook.
- `<root>/<deliverable>/<unit>.md` — one file per unit, authored by subagents.
