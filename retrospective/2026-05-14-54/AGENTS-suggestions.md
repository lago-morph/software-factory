# AGENTS.md suggestions — 2026-05-14-54

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened) in the session that produced PR #54.

Decide each on its own merits. Skip ones that don't apply; copy-paste the ones that do.

---

## Suggestion 1: Grep-verify after multi-section refactors

### Proposed addition

> **Grep-verify after multi-section refactors.** When renaming an identifier or changing a convention that appears in many places across multiple files, run a final `grep` for the OLD identifier across all touched files before committing. First-pass `Edit` calls reliably catch the obvious occurrences but routinely miss references buried in embedded templates, comment blocks, or downstream sections you didn't plan for. The cost of a final grep is one Bash call; the cost of skipping it is shipping a doc that contradicts itself.
>
> *Grounded in: PR #54's first-pass edit caught the bash variable definitions and the metadata block but missed two `${SEQ}` references — one in a Step 4 path declaration, one in an embedded AGENTS-suggestions template — that the post-edit grep flagged for fixing.*

### Why this earns its place in your agents file

The dominant failure mode for "rename X to Y everywhere" work is *partial completion*: the first 80% of references are in the planned-for sections, and the last 20% are in places the planner didn't notice (template strings, anti-pattern lists referencing the old name, See-Also blocks pointing to old paths). Those last 20% break the rename's invariant — the doc claims one thing in the header and another in a downstream section.

The marginal cost of the rule is one extra Bash invocation per refactor (~3 seconds). The marginal cost of *not* having it is shipping a self-contradicting document, which then either confuses the next reader silently or requires a follow-up "cleanup" PR. In PR #54 the grep caught two such stragglers; without the rule they would have shipped.

This is a narrower, more mechanical version of the `post-edit-reread-pass` skill — the skill mandates a full re-read for multi-section edits, the rule mandates a grep for renames specifically. They compose.

---

## Suggestion 2: Plan-first when the user explicitly asks

### Proposed addition

> **When the user says "tell me what you plan to do before you change anything," produce a structured plan with file paths, exact strings to change, and a list of open questions BEFORE any tool calls that modify state.** Read the affected files first (read-only investigation is fine, even encouraged). Present the plan as something the user can redirect. Surface decisions you'd otherwise guess at via `AskUserQuestion`, batched into a single call. Do not start typing edits until the user confirms.
>
> *Grounded in: PR #54's opening exchange — user asked for a plan, agent read the four affected files, identified every line that needed changing, batched three design decisions (last-PR semantics, no-PR fallback, collision rule) into one AskUserQuestion call, and waited for the answers before editing.*

### Why this earns its place in your agents file

"Plan first" is a common ask precisely because it lets the user redirect cheaply *before* destructive work happens. An agent that nods and starts editing anyway converts the user's redirect window from "review the plan" to "review the diff" — a much more expensive intervention point.

The rule has three operational parts: (1) read the affected files end-to-end so the plan is concrete, not generic; (2) batch decisions via `AskUserQuestion` so the user makes them all at once rather than answering serial questions; (3) wait for confirmation. Each part has been demonstrated to work in this session (the user picked answers that *did* change the plan — e.g., the no-PR fallback decision wasn't obvious from the request).

The cost is up-front investigation time. The benefit is decisions made when they're cheap to change. The asymmetry is large enough that this should be the default response to any "plan first" request.

---

## Suggestion 3: Don't physically reorder workflow steps when forward-references work

### Proposed addition

> **Don't physically reorder workflow steps across two related documents (e.g., SKILL.md and SPEC.md) just because operational order differs from narrative order.** Pick ONE: either reorder both consistently, or keep narrative order in both and add an explicit forward-reference where needed ("Step 1 depends on Step 2's output; run Step 2 first operationally"). Inconsistent ordering between paired docs creates silent drift — a reader comparing them will assume the difference is meaningful.
>
> *Grounded in: PR #54's edits to `self-retrospective` — SKILL.md kept Step 1 (determine last-PR) before Step 2 (collect commits by PR) with a forward-reference; SPEC.md §7 physically reordered them. Both are individually correct, but the docs now describe the workflow in slightly different orders.*

### Why this earns its place in your agents file

This is a subtle inconsistency — neither document is wrong, but the pair doesn't agree on a canonical ordering. A reader cross-checking SKILL.md against SPEC.md will hit the mismatch and have to figure out whether it's intentional or accidental. That cost compounds over the project's life.

The fix is mechanical: pick one ordering, apply to both. The marginal cost is one extra `Edit` call to align the lagging doc. The marginal cost of *not* doing it is a low-grade documentation drift that's invisible until someone reads both docs in the same session.

In PR #54 the inconsistency wasn't caught before merge. It's not worth a follow-up PR to fix on its own, but it should be aligned the next time either doc is touched.

---

## Suggestion 4: Interpret `total_count: 0` from `get_status` as "no CI configured", not "pending"

### Proposed addition

> **When `mcp__github__pull_request_read method=get_status` returns `state: "pending"` AND `total_count: 0` AND `get_check_runs` returns `total_count: 0` with `check_runs: []`, the PR has NO CI configured — not "CI in progress." Do not poll waiting for checks to complete; there are none. Do not report "CI is running" to the user; report "no checks configured." The `pending` state is the default for empty-status, not a wall-clock-related signal.**
>
> *Grounded in: PR #54's auto-subscribe webhook triggered a CI check; `get_status` returned `pending`/`0` and `get_check_runs` returned `[]`. The PR merged seconds later — there was no CI to wait for.*

### Why this earns its place in your agents file

The GitHub combined-status endpoint's `state: "pending"` is overloaded: it means "at least one check is pending" when checks exist, and "no checks reported yet" when none do. The disambiguator is `total_count` — `> 0` means real CI to wait on, `0` means no CI at all.

Without the rule, an agent watching a PR with no CI will either (a) poll for status updates that will never come, or (b) misreport to the user that CI is in progress. Both are minor failures, but they erode the agent's trustworthiness when monitoring PRs.

Cost: one extra check (`get_check_runs` empty + `total_count: 0` from status). Benefit: correct interpretation of the no-CI case.

---
