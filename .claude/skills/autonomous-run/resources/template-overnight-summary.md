# `<run-name>` summary — `<YYYY-MM-DD>`

Author: lead agent, autonomous-run session.

This file is the user's primary review artifact for this unattended run. Read this first, then drill into the PRs and decision briefs below. **The user reviews PR descriptions, not code diffs** — the PRs themselves carry the substantive findings; this summary is the index.

## TL;DR

4-6 bullets. What changed, what's resolved, what's queued, what's morning-review territory. Be specific, not vague ("Phase 4 closed with X" not "made progress on Phase 4").

- `<bullet 1>`
- `<bullet 2>`
- ...

## Suggested merge order

Explicit, numbered list of which PRs to merge in what sequence. Stack-bottom first by default. Call out any PRs that are safe to merge independently or out of order.

1. **PR `#NNN`** — `<branch>` — `<title>`. Stack base. Merge first.
2. **PR `#NNM`** — `<branch>` — `<title>`. Auto-rebases when #NNN merges.
3. ...

If any PR is independent (rare): "**PR #XYZ is independent** — can be merged separately at any time."

If the user wants to merge in batch: "All PRs can be merged in sequence via the GitHub UI's 'Merge' button; bases auto-update."

## PRs opened (in stack order)

Table of every PR opened during the run.

| # | Branch | Title | Base | Status | Per-PR rewind point |
|---|---|---|---|---|---|
| `#NNN` | `claude/<slug>` | `<title>` | `main` or `claude/<parent>` | Open, ready-for-review, doc-only / has CI | Revert commit `<SHA>` → `<what reversal undoes>` |
| ... | ... | ... | ... | ... | ... |

**Recommended merge order:** see the [Suggested merge order](#suggested-merge-order) section above.

## Decision briefs written

Table of every `auto-NNN-*.md` brief landed during the run.

| Brief | Status | One-line summary |
|---|---|---|
| `auto-NNN-<slug>` | Decided after Round `<N>` | `<question>` — chosen `<option>` after `<N>` rounds of real-subagent adversarial review |
| ... | ... | ... |

If you disagree with any decision, each brief carries an "If-user-overrides rewind point" section naming the specific commit SHA to revert.

## Chain status

Current state of any cross-PR work, phase boundaries, or carried-forward state.

Example: "Phase 4 closed; Phase 5 queued. 10 candidates carry forward (BF-L chose accept-as-RG for conventional view, bounded sub-track for invariant view per auto-003 Round 2). One outstanding question on the discipline-extraction subagent's output (P-foo-bar) flagged in the morning-review items below."

## Morning-review items

Explicit list of decisions or adjudications needing user input. **Zero is a valid state** if the run genuinely closed everything. For each item:

1. **`<Item title>`** — the question, the lead-agent recommendation, the rewind path if the user disagrees.
2. ...

If no morning-review items: "**0 morning-review items.** All decisions auto-resolved via brief + adversarial review per the autonomous-run skill."

## What I deliberately did NOT do

Adjacent work I bounded out per the scope envelope, plus any in-scope work I chose to defer with reason. **Honesty here is critical; hiding deferrals creates morning confusion.**

- `<bounded item 1>` — reason: per scope envelope §`<bullet>`.
- `<deferred item 1>` — reason: `<why>`; queued for next run.

If you genuinely did everything: "Nothing deferred. The scope envelope's deliverables list is fully addressed."

## Rewind points (summary)

Table mapping commit SHAs to what each reversal undoes. The user can rewind any layer of the work independently as long as they start from the top of the stack.

| Rewind | What it undoes | What survives |
|---|---|---|
| Revert PR `#NNN` (`<SHA>`) | `<scope>` | `<everything underneath>` |
| ... | ... | ... |

## Session metadata

- **Run started:** `<timestamp or start signal>`.
- **Run ended:** `<timestamp or end signal>`.
- **Branch chain at run end (top to bottom):** `claude/<tip-branch>` → `claude/<next>` → ... → `main`.
- **Subagents dispatched:** `<N>` total (`<M>` adversarial-reviewer + `<K>` worker).
- **Scope envelope:** [link to the scope-envelope file committed at start of run].
- **Self-retrospective:** [link to the retrospective dir written at end of run per the autonomous-run skill's end-of-run protocol].

---

If you have questions about any decision or want me to dispatch follow-up work, the chain is stable and the rewind points are documented. Each PR's description carries the substantive findings.
