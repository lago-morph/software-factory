# SKILL-SPEC-3a8b1d472e — pre-flight-prior-phase-merge-state-verification

## Name
`pre-flight-prior-phase-merge-state-verification`

## Priority
**High.** Mechanically catches the dominant failure mode of multi-session phased workflows: prior-phase PRs merged into stacked bases instead of `main`, causing the new phase to author against a stale or missing dependency tree.

## Description (for skill discovery)
When picking up a new phase whose dispatch prompt or session-handoff doc claims "Phase N closed; the following PRs landed", verify the PRs' content is actually in `origin/main` before authoring any new-phase artifact. Triggers on dispatch prompts saying "phase closed", "ADRs landed", "X work merged"; on session handoffs referencing prior phases by PR number; on the first non-Read action of any session that picks up from a prior phase.

## What this skill does

1. Parses the dispatch prompt / session-handoff for claims of form "Phase N closed; PRs #A-#B landed (delivering files X/Y/Z or ADRs NNNN-MMMM)".
2. For each claim:
   - `git fetch origin main`
   - `git ls-tree -r origin/main --name-only | grep -E "<expected file pattern>"` — verify expected files exist.
   - `git log --oneline origin/main --before=<dispatch-prompt-authordate> | grep -E "#(A|B|...)"` — verify expected PR-merge commits are in main's first-parent history.
3. If any check fails: surface to user via AskUserQuestion (unattended mode: default action = open a bring-forward PR; ask user to confirm or override).
4. If all checks pass: proceed normally.

## When NOT to use
- For phase work that explicitly starts from a stacked-PR base (e.g., stacked-PR-on-feature-branch pattern). The skill applies to the "next phase reads main as baseline" case.
- For first session of a project (no prior phase exists).

## Justification for skill-shape rather than AGENTS.md-rule
The check is a multi-step procedure (fetch + ls-tree + log + branch comparison + AskUserQuestion if fail), not a one-line constraint. SKILL-SPEC encapsulates the procedure as discoverable; the AGENTS.md rule (`AGENTS-MD-4f8c2a1b03`) provides the universal trigger.

## Origin event
2026-05-26 Phase-6 autonomous run: Phase-5 work (55 ADRs + handoff + AGENT-ENTRY) was missing from main because PRs #160-#177 stacked-merged into branch `claude/auto-2026-05-25-A5-verification-fixes` which never tipped into main. Discovery cost ~30 minutes investigation + one AskUserQuestion round-trip + PR #181 bring-forward. Pre-flight verification would have surfaced the issue in ~10 seconds.
