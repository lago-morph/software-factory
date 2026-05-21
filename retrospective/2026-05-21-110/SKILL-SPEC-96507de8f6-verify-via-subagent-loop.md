# Spec: `verify-via-subagent-loop`

- **ID**: SKILL-SPEC-96507de8f6
- **Source retrospective**: ../2026-05-21-110.md

## Intent

Dispatch a nitpicky verifier subagent to confirm a multi-item refactor matches its spec, then iterate on the agent's findings until the verdict is CLEAN. Use after completing any task with ten or more numbered items, a plan document with an explicit checklist, or any work whose correctness is hard to self-audit. The subagent's structured PASS / FACTUAL ERROR / MAJOR FINDING / VERDICT format makes the result actionable and the loop terminating, and it works because the verifier is given a fresh context that wasn't biased by the implementer's interpretation of ambiguity.

## Trigger

**Direct triggers** — activate immediately when the user says:

- "verify my work against the plan", "double-check the cleanup", "loop until clean"
- "spawn a verifier", "have an agent check this"
- `/verify` (when authored as a slash command)

**Proactive triggers** — offer the skill without being asked when **any** of these hold:

- A plan document or checklist with five or more numbered items has just been executed.
- A multi-file refactor touched more than five files and a single commit is imminent.
- The user explicitly framed the work as a "cleanup", "migration", "fanout", or "execute-the-plan" task.
- Any reflexive instruction like "after you commit, check that the end state matches what was instructed".

**Negative triggers** — skip when:

- The task was a single localized change (one file, one function, one config tweak).
- The user already verified by hand and asked you to commit.
- A separate review process (code-reviewer skill, CI check, security-review skill) is already running on the same change.

## Inputs

- **Plan document** — the canonical spec the work was supposed to follow. Path, content, or both.
- **Repo state** — the current working tree on the branch where the work was performed. Usually clean (post-commit) or staged.
- **Cap on iterations** — default 3 loops. If the verifier still reports NEEDS FIXES after the third pass, stop and surface the remaining findings to the user instead of looping forever.
- **(Optional) prior verifier output** — if a previous loop ran, the previous findings, so the new dispatch can confirm fixes landed.

## Outputs

- **Verifier finding report** — captured in the subagent's response. The verifier writes nothing to disk by default; the implementer reads the response and decides what to fix.
- **Inline-fix commits** (loop iteration N) — one commit per fix-batch, on the same branch.
- **A final CLEAN verdict** that gates PR creation.
- **(Optional) escalation note** — if the loop hits the iteration cap, a short summary of what's still outstanding and why convergence stalled.

## Workflow

1. **Confirm the inputs.** Identify the plan document, the branch the work was performed on, and the commit hash at the end of the work. If there's no plan document and the work was open-ended, this skill is the wrong tool — use `code-review` or `verify` instead.
2. **Author the verifier brief.** Use the template under "Verifier brief template" below. The brief must (a) name the plan document path, (b) list anything the verifier should consider already-done from prior PRs and explicitly count those as PASS, (c) require the three-bucket findings format, (d) require the closing VERDICT line.
3. **Dispatch via the Agent tool** with `subagent_type: general-purpose`. Run in foreground (you need the verdict before proceeding).
4. **Read the findings.**
   - **VERDICT: CLEAN** → skip to step 7.
   - **VERDICT: NEEDS FIXES** → continue.
5. **Fix the FACTUAL ERRORs and MAJOR FINDINGs.** Each finding should carry a specific location + change. Apply them. Commit each batch with a message that references the verifier's terminology (e.g. "Fix verifier finding: missing N6 record").
6. **Loop.** Increment the iteration counter. Re-dispatch a fresh verifier with the same brief plus a one-line note: "Previous verdict was NEEDS FIXES with N findings; all listed fixes have been applied as commit `<hash>`. Verify the end state again." Go to step 4.
7. **On CLEAN** — proceed with PR creation, push, or whatever the next planned step is. Save the verifier's CLEAN report path or quote it in the PR description.
8. **On iteration-cap exceeded** — stop. Write a short summary of the remaining findings to chat. Ask the user whether to keep iterating or accept the residual.

### Verifier brief template

```
You are a thorough, nitpicky reviewer. Your one job is to verify
that the work executed on branch <BRANCH> actually matches every
instruction in <PLAN_PATH>.

The repo is at <REPO_PATH>. The most recent commit on the branch is
<COMMIT_SHA>.

Your task: read <PLAN_PATH> IN FULL, then verify the current state of
the repo against EVERY numbered instruction in that file (<RANGE
DESCRIPTION>).

Some items may have already been executed in PRIOR commits — list
them inline and count them as PASS, do NOT treat them as missing.
Specifically: <PRIOR-WORK CALLOUTS>

For each instruction, check the actual file state. Report findings in
three buckets:
  1. PASS — instruction was followed correctly (one brief line per item)
  2. FACTUAL ERROR — something is objectively wrong; MUST be fixed
  3. MAJOR FINDING — important deviation that the user would want fixed;
     MUST be fixed

For each FACTUAL ERROR or MAJOR FINDING:
- Quote the plan instruction by item number.
- State what the actual repo state is.
- State what the expected state is.
- If you can identify the exact fix (path + line + change), include it.

Be specific. Don't say "looks good"; check each item. Cosmetic
preferences are NOT findings.

End your report with one of:
  - VERDICT: CLEAN  (no factual errors, no major findings)
  - VERDICT: NEEDS FIXES  (list of fixes summarized)
```

## Concrete examples

### Example 1: cleanup-plan-revised.md (PR #110)

**Input.** Plan at `cleanup-plan-revised.md` with 52 numbered items plus L.1–L.6 and N1–N6. Cleanup commit at `58216ff`. Prior work in PRs #106 and #109 had executed items N1, N3, and 51.

**Dispatch.** Brief authored from the template, dispatched via Agent tool with `subagent_type: general-purpose`, ran in foreground.

**First-pass verdict.** `VERDICT: CLEAN`. The verifier returned PASS lines for every numbered item — items 1–52, L.1/L.2/L.3/L.6, N1–N6 — with file paths and line citations, plus a small "Notes (non-findings)" section calling out trade-offs (the `version-line` advisory error, the `round-consistency` warning for legacy bullets) and explicitly classifying them as non-findings consistent with the plan's intent.

**Outcome.** Zero loop iterations needed. PR #110 opened immediately, merged later that day with no CI failures or review comments. The verifier's structured report gave the PR description its talking points.

### Example 2: hypothetical — needs-fixes loop

**Input.** Plan with 30 items, cleanup commit applied. Verifier returns NEEDS FIXES citing two factual errors:

1. Item 14: plan said delete `legacy.txt`; file still exists.
2. Item 22: plan said tag new record with `evals`; tag is `eval` (missing 's').

**First fix-batch.** `git rm legacy.txt`; jq edit on the record. Commit "Fix verifier findings 1+2: delete legacy.txt; correct record tag".

**Second dispatch.** Fresh verifier, brief unchanged, plus the note: "Previous verdict was NEEDS FIXES with 2 findings; fixes applied in commit `<hash>`. Re-verify."

**Second-pass verdict.** `VERDICT: CLEAN`. PR opens.

## Anti-patterns

- **Self-verifying instead of dispatching.** Reading the plan and the repo state with your own context is bias-prone — you already have a story. The whole point is fresh context. Don't skip the dispatch.
- **Vague brief.** A brief like "check that I did the cleanup right" produces vague findings. The brief must name the plan document, the commit, and the prior-work callouts; require the three-bucket format and the VERDICT line.
- **Looping past the iteration cap silently.** If the third pass still says NEEDS FIXES, stop and ask the user. Continuing to fix the same findings without diagnosis is wasted effort.
- **Treating "Notes (non-findings)" as fixes.** The verifier may surface trade-offs or stale tooling that aren't part of the spec. Read them, decide whether to act, but don't conflate them with FACTUAL ERRORs.
- **Dispatching without naming prior work that satisfied the plan.** If PR #109 already did item N1, tell the verifier that explicitly — otherwise it will flag N1 as missing because nothing in the current branch's diff touches the relevant files.

## Acceptance criteria

- [ ] The skill activates proactively after any plan-driven multi-item execution (≥5 numbered items).
- [ ] The verifier brief always names the plan document, the branch, the commit SHA, and the prior-work callouts.
- [ ] The verifier output always ends with `VERDICT: CLEAN` or `VERDICT: NEEDS FIXES`.
- [ ] The loop terminates on the first CLEAN verdict OR at the iteration cap (default 3).
- [ ] On iteration-cap exit, the user is surfaced the residual findings with a single sentence about what stalled.

## Files this skill creates / modifies

The skill itself writes nothing to disk by default. It dispatches subagents and reads their responses. Any disk writes are downstream of the implementer's choice to fix findings.

If implemented as a packaged skill in `.claude/skills/verify-via-subagent-loop/`:

- `SKILL.md` — this spec collapsed to the canonical SKILL.md format (frontmatter + sections).
- `resources/brief-template.md` — the verifier brief template (referenced in Workflow step 2).
