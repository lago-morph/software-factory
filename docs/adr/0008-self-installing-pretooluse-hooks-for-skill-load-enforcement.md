# ADR 0008: Self-installing PreToolUse hooks as the canonical mechanism for skill-load enforcement

- **ID**: ADR-dec26d09fd
- **Status**: Accepted
- **Date**: 2026-05-21

## Context

The session that produced [PR #116](https://github.com/lago-morph/software-factory/pull/116) ("Fix issue 105") opened with a prompt that triggered two skills — the [`research-pipeline`](../../.claude/skills/research-pipeline/SKILL.md) skill (content) and the [`issue-management`](../../.claude/skills/issue-management/SKILL.md) skill (process). The content trigger drowned out the process trigger; the agent loaded `research-pipeline` and went straight to catalog work. Every `mcp__github__issue_read` and `mcp__github__add_issue_comment` call after that happened without `issue-management` loaded, which meant the STARTED claim, the `good first issue` label, the per-event comments — every convention the skill exists to enforce — were silently skipped until the user pointed it out one turn before the PR opened. Backfilling was tractable; the same failure in a less-attentive session would have shipped without the audit trail and surfaced only at retrospective time, if at all.

The root cause is structural: skill loading is an attentional act the agent performs based on prompt-pattern matching. When two skills share a session, the higher-salience one wins; the other one's conventions vanish. Documentation rules ([`AGENTS.md`](../../AGENTS.md), skill descriptions) are necessary but not sufficient — they still depend on the agent reading the right doc at the right moment. The same failure mode applies to [`always-commit-skill-to-repo`](../../.claude/skills/always-commit-skill-to-repo/SKILL.md) (gates git ops) and [`in-flight-workflow-tracking`](../../.claude/skills/in-flight-workflow-tracking/SKILL.md) (gates long-running dispatch); both are described as mandatory but enforced only attentionally today. Filed as [issue #118](https://github.com/lago-morph/software-factory/issues/118) for follow-up generalization.

## Decision

Process skills whose conventions must fire on every interaction with a class of tool surface install a self-syncing PreToolUse hook (via the skill's own `scripts/install.py`) that hard-blocks the gated tool calls unless a per-session marker file shows the skill has been loaded.

The marker is touched by a successful pre-flight (`install.py --check` exit 0); a failed pre-flight runs `--force` with no user prompt, installs the hook script + merges the `PreToolUse` entry into [`.claude/settings.json`](../../.claude/settings.json), and auto-commits. The skill's `SKILL.md` opens with a "STOP — run the pre-flight" stanza that makes the install the unconditional first action. Reference implementation: `issue-management` after [PR #117](https://github.com/lago-morph/software-factory/pull/117) — the `.claude/hooks/require-issue-management-skill.sh` hook script and the `mcp__github__(issue_*|add_issue_comment|list_issues|search_issues|sub_issue_write)` matcher entry.

## Alternatives considered

- **SessionStart hook that auto-loads the skill on issue keywords in the first prompt.** Still pattern-matches prompt text, so it fails when an issue is mentioned mid-session or when the user uses phrasing the matcher misses. Useful as a complement, not a replacement.
- **Tighten the skill's `description` / "When to use" section so the trigger surface is unambiguous.** Done in [PR #117](https://github.com/lago-morph/software-factory/pull/117) as a precursor, but on its own this is still attentional — the agent has to read the description and recognise the match. Necessary, not sufficient. Documentation rules ([`AGENTS.md`](../../AGENTS.md)) are in the same category.
- **AGENTS.md "non-negotiable triggers" section listing process skills.** Strictly documentation, equally attentional. Adopted as a complement in [`AGENTS.md`](../../AGENTS.md) under "Process skills — non-negotiable triggers" (rule `AGENTS-MD-9573ff5b60`), but not a substitute for the gate.
- **Centralised "skill-loaded?" registry that every MCP tool consults.** Architecturally cleaner than per-skill hooks, but requires Claude Code core changes; the per-skill PreToolUse hook is the most powerful primitive available to a userspace skill today.

## Consequences

**Easier**: forgetting to load a process skill becomes a deterministic block with an instructive stderr — agent reads the message, loads the skill, retries. The failure mode that bit PR #116 is mechanically impossible after the gate is in place. The pattern is generalizable; once the `issue-management` `install.py` + hook script exists, adding the same enforcement to `always-commit-skill-to-repo` and `in-flight-workflow-tracking` is a near-mechanical refactor ([issue #118](https://github.com/lago-morph/software-factory/issues/118) tracks this).

**Harder**: the skill author now ships more than markdown — `scripts/install.py`, a hook script template, settings.json merge logic. The per-skill installer has ~300 lines of Python (mostly idempotent JSON-merge + filesystem checks). The follow-up refactor in [issue #118](https://github.com/lago-morph/software-factory/issues/118) should lift the shared bits into `.claude/lib/` so the per-skill cost drops back to ~20 lines.

**Trade-off accepted**: a fresh-repo bootstrap blind spot. Until the skill has run once in a given repo, the hook isn't installed and the first session can still miss the skill load. Acceptable because (a) once `settings.json` and the hook script are committed to the repo, every subsequent session inherits the gate from the clone, and (b) the alternative (some kind of out-of-band installation) violates the harness's "ephemeral sandbox, repo is the source of truth" model.

## References

- [retrospective/2026-05-21-117.md](../../retrospective/2026-05-21-117.md) [§Part 1 — what happened](../../retrospective/2026-05-21-117.md#part-1--what-happened), [§Part 4 — proposed ADRs](../../retrospective/2026-05-21-117.md#part-4--proposed-adrs) — the source retrospective and the original draft.
- [retrospective/2026-05-21-117/ADR-dec26d09fd-self-installing-pretooluse-hooks-for-skill-load-enforcement.md](../../retrospective/2026-05-21-117/ADR-dec26d09fd-self-installing-pretooluse-hooks-for-skill-load-enforcement.md) — the draft this ADR was promoted from; ID `ADR-dec26d09fd` preserved.
- [ADR 0009: Repurpose the GitHub default `help wanted` label as the permanent marker of agent-authored issues](./0009-help-wanted-label-as-permanent-marker-of-agent-authored-issues.md) — sibling decision recorded in the same session (added by PR #117 to the `issue-management` skill alongside the gate).
- [`.claude/skills/issue-management/SKILL.md`](../../.claude/skills/issue-management/SKILL.md) — the reference implementation's documentation, including the "STOP — run the pre-flight" stanza.
- [`.claude/skills/issue-management/scripts/install.py`](../../.claude/skills/issue-management/scripts/install.py) — the installer; idempotent JSON-merge + hook-script copy.
- [`.claude/skills/issue-management/resources/hooks/require-issue-management-skill.sh`](../../.claude/skills/issue-management/resources/hooks/require-issue-management-skill.sh) — the hook script template.
- [`.claude/hooks/require-issue-management-skill.sh`](../../.claude/hooks/require-issue-management-skill.sh) — the installed hook (committed because settings.json's `command` field points at it).
- [`.claude/settings.json`](../../.claude/settings.json) — the merged PreToolUse hook entry.
- PRs the decision was made in: [#116](https://github.com/lago-morph/software-factory/pull/116) (the slip), [#117](https://github.com/lago-morph/software-factory/pull/117) (the gate). Follow-up: [issue #118](https://github.com/lago-morph/software-factory/issues/118) (generalize to other process skills).
- Reference precedent: [`.claude/skills/architecture-failure-mode-gate/scripts/install.py`](../../.claude/skills/architecture-failure-mode-gate/scripts/install.py) — the self-installing pattern this ADR generalizes from.
