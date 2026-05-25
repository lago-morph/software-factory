# Context-slimming plan

**Status.** Plan, not implemented. Implementation deferred until the current long-running synthesis run completes (to avoid merge conflicts in the active branch chain).

**Author.** Lead agent, 2026-05-25.

**Motivation.** The Phase-4 startup prompt (handed off after the 2026-05-25 overnight run) immediately filled a fresh agent's context window to 147K tokens. Cause: the prompt's read-order section listed nine foundational documents totaling ~1690 lines of markdown, all loaded eagerly. The user wants new-agent startup load reduced without losing the accuracy that the prompt's full reading list was protecting.

This plan combines three proposals (1 progressive-disclosure entry doc + 3 task-aware reading lists + 4 TL;DR-first discipline) into a single implementation. Each proposal's text and tradeoffs were discussed in the 2026-05-25 session before this plan was authored; this file is the implementation specification.

---

## Goals

1. **Reduce session-start context load by ≥60%** from the current ~1690-line eager read.
2. **Preserve accuracy.** A fresh agent landing on the entry doc should reach the same decisions as one that read everything eagerly, given the same task.
3. **Defend against staleness.** The new top-level navigation document must not restate content from the docs it points at; it only names what's contained where. When sub-docs change, the entry doc does not silently drift.
4. **Be reversible.** Adopt the new shape via additive artifacts; do not delete or restructure load-bearing existing docs in the same change.

## Non-goals

1. Compressing the foundational docs themselves (those have their content for good reasons).
2. Moving files into hot/cold subdirectories (rejected: premature structural change).
3. Compacted-state self-summarization (rejected: fidelity-loss risk; the lead agent's compaction is hard to trust across many runs).

---

## Implementation specification

### Part 1 — Entry document (Proposal 1)

Add a single top-level file [`AGENT-ENTRY.md`](AGENT-ENTRY.md) at the repo root. This document is the **only file a new agent's prompt should require them to read first** (other than [`AGENTS.md`](AGENTS.md), which remains the binding conventions doc).

**Discipline.** The entry doc **names what is contained in each sub-doc**, with one line per doc. It does NOT summarize the sub-doc's content. Example permitted line:

> [`architectures/v3/phase-3.4-decisions-resolved.md`](architectures/v3/phase-3.4-decisions-resolved.md) — Tier-1 decisions resolved at Phase 3.4 close; scoping principle; refined two-part substrate-buildability rule; working definitions of architecture / substrate / methodology / discipline; entry-mode greenfield/brownfield definitions.

Example **not** permitted (restates content):

> phase-3.4-decisions-resolved.md — the scoping principle is "carry forward every candidate that defended itself; do not eliminate at end-of-Phase-3."

The distinction is critical: the entry doc names *what topics live in the file*, not *what the file says about those topics*. This is the staleness mitigation — when phase-3.4-decisions-resolved.md is edited, the entry doc still accurately names its contents at the topic level.

**Sections of `AGENT-ENTRY.md`:**

1. **Binding conventions** — names [`AGENTS.md`](AGENTS.md) only. (Hard requirement: every agent reads it.)
2. **Current state** — names the active SESSION-HANDOFF document. Convention: this entry's link target is updated whenever a new SESSION-HANDOFF is written. The line itself only names what the handoff carries; it does not need an update when the handoff body changes.
3. **Plan** — names the current architecture-vN synthesis plan with a note that the agent should read only their current phase's section.
4. **Decisions (binding)** — names the resolved-decisions doc + the candidate registry.
5. **Substrate primitives** — names [`primitives/index.md`](architectures/v3/primitives/index.md) with the note that individual P-NN sketches drill on demand.
6. **Decision briefs (historical)** — names the `decisions/` directory and says "read only if relevant to your current decision."
7. **Task-aware reading lists** — see Part 2.

**Note on `AGENTS.md` reading.** `AGENTS.md` continues to be required reading because the hook enforces it (`Read tool on AGENTS.md before any non-Read tool call`). The entry doc does not absolve the agent of this; it complements it.

### Part 2 — Task-aware reading lists (Proposal 3)

Embedded within [`AGENT-ENTRY.md`](AGENT-ENTRY.md) — a "by task" section that names per-task reading lists. Format:

```markdown
## Reading lists by task

If your first task is "decide BF-L's per-RG-view choice at Phase 4 entry":
- Read: AGENTS.md, candidate-registry.md §BF-L (Phase-3.5.5 subsection), primitives/P-26-codebase-model.md sketch, plan §Phase 4 entry-blockers, autonomous-run skill SKILL.md.
- Skip: everything else until needed.

If your first task is "Phase 4 dispatch shape decision":
- Read: AGENTS.md, current handoff, plan §Phase 4, autonomous-run skill SKILL.md.
- Skip: per-candidate detail until 4.1 fires.

If your first task is "drain incoming research/manual/ sources":
- Read: AGENTS.md, research-pipeline skill, preliminary-index-pass skill, research/PLAN.md.
- Skip: architecture synthesis docs.
```

These lists are maintained at end-of-run (when the SESSION-HANDOFF is updated) and seeded by the lead agent based on what the next likely tasks are. They're not exhaustive; if the agent's task isn't on the list, they fall back to the navigation in Part 1.

### Part 3 — TL;DR-first discipline for heaviest docs (Proposal 4)

For the two largest foundational docs only:

- [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](ARCHITECTURE-V3-SYNTHESIS-PLAN.md) (~558 lines)
- [`architectures/v3/candidate-registry.md`](architectures/v3/candidate-registry.md) (~345 lines and growing)

Add a `## TL;DR (≤200 words)` section at the top of each. The TL;DR is **regenerated by a subagent at end-of-run from the body**, not maintained alongside it. The body is the source of truth.

**Implementation detail for regeneration:** the `autonomous-run` skill's end-of-run protocol gains one new sub-step: dispatch a "TL;DR regeneration" subagent over each tagged doc. The subagent reads the body, writes a new TL;DR, and the lead agent commits the regenerated TL;DR section. Staleness window: ≤1 run.

Smaller foundational docs (`AGENTS.md`, `phase-3.4-decisions-resolved.md` at 242 lines, the active SESSION-HANDOFF at ~106 lines, `primitives/index.md` at 193 lines) do **not** need TL;DRs — they're already small enough that reading them fully is cheap. Premature TL;DR-ing every doc creates maintenance burden without context savings.

### Part 4 — Per-primitive sketches stay drill-on-demand

No change required — they are already structured this way. But the entry doc reinforces it: "read [`primitives/index.md`](architectures/v3/primitives/index.md); drill into individual P-NN sketches only when you need them for a specific decision."

The mistake in the Phase-4 startup prompt was telling the agent to "skim primitives/index.md to understand the buildability landscape" without naming a stopping criterion. The new entry doc reads: "read primitives/index.md in full; drill into individual sketches only when a specific decision requires them."

---

## What this plan changes

| Artifact | Change |
|---|---|
| `AGENT-ENTRY.md` | NEW — top-level navigation doc. Names sub-docs at topic level; does not restate content. |
| `ARCHITECTURE-V3-SYNTHESIS-PLAN.md` | Add `## TL;DR (≤200 words)` section at top; otherwise unchanged. TL;DR regenerated at end-of-run. |
| `architectures/v3/candidate-registry.md` | Same as above. |
| `.claude/skills/autonomous-run/SKILL.md` | Add an "End-of-run TL;DR regeneration" sub-step to the end-of-run protocol; add an "Update AGENT-ENTRY.md filename pointers if any sub-doc was renamed" sub-step to the handoff discipline. |
| `.claude/skills/autonomous-run/resources/template-overnight-summary.md` | No change (the entry doc is for next-agent startup; the overnight summary is for user review). |
| `.claude/skills/autonomous-run/resources/template-handoff-doc.md` | Add a "Task-aware reading lists" section that the handoff doc populates with the next likely tasks + per-task reading lists. The handoff feeds the AGENT-ENTRY.md's per-task section. |
| Startup prompts (the kind given by the user to spin up a new session) | Change from "read these 9 files in order" to "read AGENTS.md, then read AGENT-ENTRY.md and follow its navigation for your stated task." |

## Expected savings

- **Eager read at session start.** From ~1690 lines (current) to: AGENTS.md (102) + AGENT-ENTRY.md (~80 estimated) + the active SESSION-HANDOFF (~106) + the per-task reading list's items (varies, typically 2-3 docs at ~200-300 lines total) = **~500-600 lines = ~30-35% of current**.
- **Context window hit at session start.** Roughly proportional. Expect 50K-70K tokens for the eager read instead of ~80K-100K. Total session-start budget (with system prompt + skills definitions) goes from 147K to roughly 90-110K.
- **Accuracy.** Should be preserved because: the agent still loads all binding conventions; the entry doc gives them a complete map of *what exists where*; task-aware reading lists pre-curate the right detail per the most common next moves; TL;DR sections preserve high-level structure for the heaviest docs; drill-on-demand is explicit.

## Failure modes + mitigations

| Failure mode | Mitigation |
|---|---|
| Entry doc drifts because someone moves a file and forgets to update the entry | Run [`scripts/check-internal-refs.py`](scripts/check-internal-refs.py) on the entry doc; the existing infrastructure flags broken paths. |
| Entry doc gets longer over time as people add summaries despite the discipline | Code review (PR description) catches this; the discipline is explicit at top of the entry doc itself. |
| Agent reads the entry doc but ignores the "drill on demand" guidance and eager-loads everything anyway | The entry doc's per-task reading lists give the agent permission to read less; the autonomous-run skill's context-budget section reinforces this. Persistent over-reading suggests a skill update. |
| TL;DR regeneration produces a misleading summary | The body is source-of-truth; the TL;DR is a cached convenience. Agents should still link into the body for binding decisions. Annual / periodic review of TL;DR accuracy can be added if drift is observed. |
| Per-task reading lists go stale because they don't anticipate the next agent's actual task | The agent falls back to the entry doc's navigation in Part 1. The per-task lists are accelerators, not the only path. |
| The "named what is contained" discipline degrades into "summarized content" | Reviewer note in PR descriptions; one-line review heuristic — "would this line need updating if the sub-doc changed its conclusion?" If yes, it's restating content; rewrite to name topic instead. |

## Implementation order

When the current long-running synthesis run completes (and its PR chain merges):

1. **PR A.** Add `AGENT-ENTRY.md` at repo root with Parts 1 + 2 (navigation + task-aware reading lists; tasks seeded by the lead agent based on Phase 4's then-current state).
2. **PR B.** Update the two heaviest docs (`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`, `candidate-registry.md`) with `## TL;DR (≤200 words)` sections. Seed the TL;DRs by lead-agent inline review; the autonomous-run skill's end-of-run protocol then regenerates them in future runs.
3. **PR C.** Update `autonomous-run` skill (SKILL.md + template-handoff-doc.md) with the TL;DR regeneration sub-step and the task-aware-reading-list section.
4. **PR D.** Update the existing startup-prompt template (and any documented "how to start a new session" guidance) to reference AGENT-ENTRY.md.

PRs A and B can land in either order. PRs C and D should follow A and B so they reference real artifacts.

Estimated effort: 1 short unattended run could land all 4 PRs.

## Alternatives explicitly rejected

- **Hot/cold file separation.** Premature structural change; entry doc + reading lists achieve the same outcome without moving files.
- **Compacted-state self-summarization.** Fidelity loss risk; the lead agent's compaction is hard to trust across many runs.
- **Smaller foundational docs.** Each doc has its size for a reason; cutting their content would lose accuracy. Indirection (entry doc + drill-on-demand) achieves the same context savings without cutting content.

## Open questions deferred

1. Should the TL;DR regeneration be done by a subagent per doc, or by one subagent over all tagged docs? (Cost vs cleanliness tradeoff; decide at implementation time.)
2. Should `AGENT-ENTRY.md` be at the absolute repo root, or under `docs/`? (Root is more discoverable; `docs/` is more conventional for navigation docs. Lean root.)
3. Should the entry doc be picked up automatically by the harness (like AGENTS.md is) or stay opt-in via prompt instruction? (Opt-in for now; auto-load would be a stronger guarantee but requires harness change.)
