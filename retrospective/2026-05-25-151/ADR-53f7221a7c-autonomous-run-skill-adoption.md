# ADR: autonomous-run skill adopted as canonical pattern for unattended sessions

- **ID**: ADR-53f7221a7c
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-151.md
- **PRs covered**: #136–#145, #148

## Context

The 2026-05-25 overnight run (PRs #136–#145) executed the unattended pattern documented in [ADR-f702da3352 (unattended decision-brief pattern)](../2026-05-25-134/ADR-f702da3352-unattended-decision-brief-pattern.md). The pattern worked — 10 PRs landed, two substantive decisions (`auto-001` dispatch shape; `auto-002` U-B path) went through adversarial review and revised in Round 2 based on real-subagent findings. But several gaps surfaced in operation. The run stopped at 10 PRs because the next phase had user-input blockers; the user said this was "way too quickly" and they expected significantly more work per unattended session. The inline-simulated reviewer pattern (used in `auto-001` Round 1) was structurally too weak to catch the lead agent's own blind spots — caught by adding real subagents in Round 2, which produced a different verdict. There was no scope-envelope at the start, leading to under- or over-running ambiguity. The morning summary was useful but lacked a suggested merge order, and the user clarified they review PR descriptions, not code, which has implications for what PR descriptions must contain.

ADR-f702da3352 described the brief + adversarial-review + rewind-point shape. The 2026-05-25 session generated enough operational learnings to formalize the full pattern as a project-shipped skill with strict parameters, rather than relying on each unattended-run prompt to re-derive them from session memory.

## Decision

**Adopt the `autonomous-run` skill at [`.claude/skills/autonomous-run/`](../../.claude/skills/autonomous-run/) as the canonical pattern for unattended / overnight / long-running sessions.** The skill is shipped as part of PR #148. It codifies:

- A scope-envelope alignment step before any work, posted to the user for confirmation or implicit-confirm-after-wait;
- A decision-brief protocol with **2 rounds minimum**, each round dispatching **≥3 real subagent reviewers** (per [`AGENTS-MD-d72e1a4f3c`](../../AGENTS.md#adversarial-review-must-be-real-subagents) — inline-simulated reviewers forbidden);
- Stacked-PR discipline with a **30-PR cap** and a target floor of 20–30 PRs (the prior 10-PR run was too short);
- A required morning summary including a **suggested merge order**;
- A required end-of-run auto-invocation of [`self-retrospective`](../../.claude/skills/self-retrospective/SKILL.md);
- Stop-conditions explicitly enumerated (context-budget exhaustion, hard-failed dependency, scope-envelope completion, 30-PR cap, user-interrupt) with "sub-phase closure" explicitly forbidden as a stop reason;
- PR-description discipline naming the user's stated review style ("I do not review code in general. I review the PR descriptions") with required sections;
- Five resource templates: scope envelope, decision brief, overnight summary, handoff doc, adversarial-reviewer angles.

## Alternatives considered

- **Continue with ADR-f702da3352 alone, no shipped skill.** Rejected because the operational parameters (2 rounds × ≥3 reviewers, 30-PR cap, scope-envelope-first) are non-obvious from the brief-pattern description alone. Without a shipped skill, every unattended-run prompt would have to re-derive them, with predictable drift.
- **Ship the pattern as a slash command instead of a skill.** Rejected because the pattern is activated by intent (user mentioning "overnight", "while I'm away") rather than by an explicit command. Skill-based discovery via trigger phrases matches the user's natural language.
- **Lift the operational parameters into [`AGENTS.md`](../../AGENTS.md) instead of a skill.** Rejected because the parameters are situational (apply only to unattended sessions, not interactive ones), so they belong in skill content where they're loaded on trigger, not as global conventions every session must absorb.
- **Ship more reviewers (≥5 per round) instead of 3.** Rejected as over-provisioning. The 2026-05-25 evidence is that 3 real reviewers per round was sufficient to catch the lead agent's blind spots in both `auto-001` and `auto-002`. Higher counts cost proportionally more without proportional signal.
- **Single round of review only.** Rejected because Round-1 reviewers identify the wrong objections too often; their counter-proposals may not survive Round-2 challenge. The 2026-05-25 evidence is that Round 2 produced different conclusions from Round 1 in both `auto-001` and `auto-002`.

## Consequences

**Easier.** Future unattended-run prompts can read as "kick off an autonomous-run session" rather than re-deriving the full protocol. The morning hand-off has a predictable shape (summary + suggested merge order + per-PR rewind points). The 30-PR cap with 20-30 floor sets a calibrated volume expectation. Auto-invoking the retrospective at end-of-run captures durable lessons that would otherwise be lost to context truncation.

**Harder.** Each unattended-run substantive decision now costs ≥6 reviewer subagent dispatches (3 per round × 2 rounds), plus the brief + revision. Throughput per decision is lower than the inline-pattern. The scope-envelope adds a brief synchronous step at run start. End-of-run retrospective adds ~1 PR (small) to every run.

**Accepted trade-off.** The skill favors reversibility, audit-trail completeness, and operational predictability over raw throughput per decision. The user's stated preference is volume-of-reversible-work over speed-of-irreversible-work — and reviews must catch misreads even when the lead agent doesn't know they're misreading. The 2026-05-25 evidence is that real reviewers materially changed two of two substantive decisions in this session, justifying the cost.

## References

- [`../2026-05-25-151.md`](../2026-05-25-151.md) — the source retrospective.
- [`../2026-05-25-134/ADR-f702da3352-unattended-decision-brief-pattern.md`](../2026-05-25-134/ADR-f702da3352-unattended-decision-brief-pattern.md) — the prior ADR this builds on.
- [`../../.claude/skills/autonomous-run/SKILL.md`](../../.claude/skills/autonomous-run/SKILL.md) — the skill itself, shipped in PR #148.
- [`../../AGENTS.md`](../../AGENTS.md) — the convention file that carries `AGENTS-MD-d72e1a4f3c` (real-subagent review rule, codified live during PR #144).
- PRs the decision was made in: #136–#145 (the overnight chain that motivated formalization), #148 (the skill itself), #151 (the context-slimming plan that interlocks with the skill at start-of-session).
