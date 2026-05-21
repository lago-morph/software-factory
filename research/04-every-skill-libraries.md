# Every.to Skill Libraries (claude_commands, symphony-thumbtack, everyskill) — Research Report

**Sources covered:**
- https://github.com/EveryInc/claude_commands (README, 5 top-level command files, 5 agent definitions in `agents/`)
- https://github.com/EveryInc/symphony-thumbtack (README, WORKFLOW.md, SETUP.md, INSTRUCTOR_NOTES.md, `.claude/skills/{commit,land,pull,push,tasks}/SKILL.md`)
- https://github.com/EveryInc/everyskill/tree/main/skills (README + initial SKILL.md for 14 skills: ai-check, app-growth-investigator, coding-tutor, daily-social-agent, every-editorial-triage, every-social-style, every-style-check, hemingway, intercom-api, kate-top-edit, model-hierarchy, skill-generalizer, social-clips, submit-to-everyskill)

**Date:** 2026-05-10

## Executive summary

These three Every.to repositories represent three distinct layers of a skill-and-agent methodology that has clearly co-evolved across the company's editorial and engineering practice.

1. **`claude_commands`** is the *primitive* layer: a handful of well-shaped slash-command prompts (`/experiment-driven-development`, `/analyze_github_issue`, `/create_github_issue`, `/resolve_pr_comments`, `/generate_codebase_context`) plus five "agents" (sub-agent definitions) that target very narrow concerns: `codebase-researcher`, `design-implementation-reviewer`, `design-iterator`, `prompt-engineer`, `react-figma-ui-engineer`. The commands all follow a research → plan → ask-for-approval → implement → verify cycle, and each one expects a single GitHub issue or PR as its input "spec." Notably, the experiment-driven-development command introduces an explicit *log file in `/experiments`* with reward/penalty framing to force agents to articulate goals, learnings, plans, and outcomes per iteration — a lightweight scientific journal.

2. **`symphony-thumbtack`** is the *orchestration* layer: a teaching/demo repo where a Python orchestrator (Symphony) dispatches concurrent Claude Code agents against a local repo, each isolated in its own git worktree, picking issues off a queue (`tasks.json` or Linear), running a 9-phase workflow per issue, and surfacing results back through a state machine: `Backlog → Todo → In Progress → Human Review → Merging → Done` (with `Rework` as an explicit reset). Each agent maintains a single persistent "workpad" comment on its issue containing plan, acceptance criteria, validation strategy, and progress checkboxes. The skill folder contains exactly 5 git-flow primitives — `commit`, `pull`, `push`, `land`, `tasks` — that the per-issue agent invokes by name.

3. **`everyskill`** is the *registry/marketplace* layer: a curated, AI-and-human-reviewed library of SKILL.md files that any Claude Code instance can fetch. Skills here are domain-heterogeneous (editorial, growth-analytics, video rendering, model routing, intercom API) and weighted toward Every's content-production business. Their frontmatter is standardized (`name`, `description`, optional `tags`, `version`, `allowed-tools`) and `description` doubles as the *trigger contract* — it tells the host agent under which natural-language conditions to auto-invoke the skill.

For a software factory, the practical takeaways are: (a) per-issue git worktrees + a persistent workpad artifact are a clean isolation primitive; (b) the 5-state queue with `Human Review` and `Rework` as first-class states is a minimally sufficient handoff vocabulary between agents and the human; (c) skills should be very small, named after the verb the agent will say ("commit", "push", "land"), and gated by explicit preconditions; (d) sub-agent definitions live separately from command/skill definitions and are model-typed (most are Opus); (e) editorial-style review skills (kate-top-edit, hemingway, ai-check) suggest a *checklist-emitting* pattern rather than auto-fixing — that pattern transplants directly into code review.

## Skill / command taxonomy

| Repo | Name | Granularity | What it does | When invoked |
|---|---|---|---|---|
| claude_commands | `00_meet_claude` | Meta / capabilities dump | Self-description of Claude Code's toolset | One-shot orientation |
| claude_commands | `01_experiment_driven_development` | Methodology macro | Creates `/experiments/*.md` log with goal, learnings, plan; iterates with explicit failure tracking and pseudo-reward signal | Complex features / hard bugs |
| claude_commands | `02_generate_codebase_context` | Macro / artifact generator | Produces an `llms.txt`-style codebase map (file goals, function signatures, ASCII dependency diagram, style guide, data formats) | Onboarding new agents/humans |
| claude_commands | `03_analyze_github_issue` | Per-issue planner | `gh issue view` → analyze codebase → make branch → produce a `<plan>` and ask for approval before coding | Start of feature/fix work |
| claude_commands | `04_create_github_issue` | Spec generator | Drafts a GH issue at MINIMAL/MORE/A LOT detail levels with conventions, labels, file refs, cross-links | Turning intent into a spec |
| claude_commands | `05_resolve_pr_comments` | Per-PR resolver | Discovers all PR comments via `gh api`, classifies them, plans, optionally spawns parallel sub-agents per file, validates, commits | Post-review |
| claude_commands | `agents/codebase-researcher` | Sub-agent (Opus) | Reverse-engineers patterns/algorithms from an existing codebase | Spawned by a parent agent |
| claude_commands | `agents/design-implementation-reviewer` | Sub-agent | Diffs live UI against Figma; emits structured review | Spawned for UI review |
| claude_commands | `agents/design-iterator` | Sub-agent | Iterates UI N times: screenshot → 3–5 improvements → implement → repeat | "Iterate on this 10 times" |
| claude_commands | `agents/prompt-engineer` | Sub-agent (Opus) | Writes/reviews/optimizes system prompts | Meta work on prompts |
| claude_commands | `agents/react-figma-ui-engineer` | Sub-agent (Opus) | Translates Figma → React/Tailwind using existing component library | Spec'd UI implementation |
| symphony-thumbtack | `.claude/skills/commit` | Git primitive | Conventional commit with summary/rationale/tests body, heredoc safety | Per-implementation step |
| symphony-thumbtack | `.claude/skills/pull` | Git primitive | Merge local `main` into feature branch w/ rerere + zdiff3 conflict style | Before push, after sync |
| symphony-thumbtack | `.claude/skills/push` | Git primitive | Composes `/tmp/pr_body.md` (What/Why/How/Validation), creates/updates a local PR record via `tasks pr-create` | End of implementation |
| symphony-thumbtack | `.claude/skills/land` | Merge primitive | Squash-merge branch → main, mark PR `MERGED`, move issue → `Done` | After human approval only |
| symphony-thumbtack | `.claude/skills/tasks` | CLI wrapper / contract | List/get/transition issues, manage comments, manage local PR records; workpad protocol | Throughout the issue lifecycle |
| everyskill | `ai-check` | Checklist emitter | Detects AI tells, outputs sequential checklist (no auto-fix) | Any writing review |
| everyskill | `app-growth-investigator` | Investigative analyst | Funnel/segment analysis with explicit source authority rules; ends with "levers" | Growth/retention/conversion questions |
| everyskill | `coding-tutor` | Stateful tutor | Persistent `~/coding-tutor-tutorials/` with learner profile, spaced-repetition quiz, codebase-anchored examples | "Teach me X" |
| everyskill | `daily-social-agent` | Pipeline / cron | Slack-scan → draft posts → AI-tell-detect → human-review queue | Scheduled |
| everyskill | `every-editorial-triage` | Rubric | Fast first-pass: essentials, strategy fit, 2–3 suggestions, conditional next-steps | New draft arrives |
| everyskill | `every-social-style` | Style guide | Voice/tone/archetype guide for X + LinkedIn | Writing social copy |
| everyskill | `every-style-check` | Checklist emitter | Validates against editorial style guide; no auto-fix | Pre-publish |
| everyskill | `hemingway` | Editor | Ruthless trim; tracks original vs trimmed word counts; cut-table | "Tighten this" |
| everyskill | `intercom-api` | API wrapper | Curl recipes for reply/note/assign/close/snooze and Help Center CRUD | Support automation |
| everyskill | `kate-top-edit` | Checklist emitter | Top-edit screen for vague openers, AI tells, missing links, hedging, marketing-speak | Pre-publish |
| everyskill | `model-hierarchy` | Routing policy | 3-tier model tiers, classify task → route; ~10x cost reduction claim | Whenever spawning sub-agents |
| everyskill | `skill-generalizer` | Meta-skill | Turns team-specific skill into onboardable distributable skill | "Generalize this skill" |
| everyskill | `social-clips` | Tool/pipeline | Slack threads → Remotion video (vertical + landscape MP4 + GIF) | Content production |
| everyskill | `submit-to-everyskill` | Meta-skill / submission | Package skill into base64'd files, POST to `/api/agent-submit`, get back a PR URL | After authoring a skill |

## Symphony orchestration model

The "symphony" metaphor in `symphony-thumbtack` is concrete and worth dissecting because it is the only one of the three repos that builds an actual multi-agent runtime rather than just a prompt library.

- **The conductor** is the Symphony Python process (`scripts/run.sh` → `symphony.orchestrator`). It ticks on a 10-second poll, reads the queue, decides what to dispatch, applies a concurrency cap (`agent.max_concurrent_agents = 4`), enforces per-turn (3600s) and per-issue (20-turn) limits, and watches for state transitions. From the log line in SETUP.md: `ts=… msg=tick candidates=8 running=0 ... msg=dispatched issue_identifier=ENG-1`.
- **The score** is the queue plus the WORKFLOW.md document. The queue (`tasks.json` or Linear) is the *ordered material to play*; WORKFLOW.md is the *score's rules* — it defines the 9-phase per-issue prompt every agent receives, the state machine, the operating principles, and the cross-references to skills. The agent does not invent the workflow; it executes the score.
- **The sections of the orchestra** are concurrent Claude Code agent instances. Each one is given: a freshly hydrated issue (identifier, title, status, description), an isolated git worktree (`_workspaces/<issue>`), a Claude session, and the same 9-phase prompt. The agents are *interchangeable players* — there is no per-issue specialization.
- **The rehearsal space** is the per-issue git worktree under `_workspaces/`, plus a feature branch `symphony/<identifier>` in the target repo. Worktrees are created by `after_create` hooks and destroyed on reset.
- **The score for each piece** (per-issue prompt) is templated with front matter and walks the agent through: *Kickoff & Routing → Plan & Validate → Implementation → Validation → Push & PR → PR Feedback Sweep → Human Review (waiting) → Merging → Rework (on rejection)*. Each phase has explicit entry conditions and called-out skills.
- **The persistent musical chart per piece** is the *workpad*: "exactly **one** persistent workpad comment per issue," marked with a `## Workpad` header. It contains plan, acceptance criteria, validation strategy, and a checkbox list. Agents update it on each progress checkpoint; humans read it to know what was done. This is the single most important coordination artifact — it survives turn boundaries and Claude session restarts, and it's the human's review surface.
- **The audience cue** is the `Human Review` state. The agent moves itself into it after passing its own validation; the human then either drags the ticket to `Merging` (approve) or `Rework` (reject). Symphony reconciles within ~10s of the human action and re-dispatches if needed.
- **The encore / cleanup** is the `land` skill: squash-merge, mark PR `MERGED`, transition `Done`. Critically, `git merge` is *forbidden outside the land skill flow* — the only legitimate merge path is through this skill.

What's deliberately *not* in the orchestra metaphor: there's no inter-agent communication. Agents don't talk to each other; they only talk to the queue, the workpad, and the conductor's state machine. This is a key design choice — it keeps the system to a star topology and makes failure isolated.

## Composition and chaining patterns

Three distinct composition models show up across the three repos:

1. **Inline phase composition (claude_commands).** A single command is a linear script of phases: Research → Plan → (Get approval) → Implement → Verify. Composition is by reference: `05_resolve_pr_comments` describes spawning parallel sub-agents (one per file with unresolved comments) using the Task tool, with a coordination/integration step at the end. This is *fan-out from within a command*.

2. **Skill invocation by name (symphony).** The per-issue agent prompt references skills by file path: "open `.claude/skills/land/SKILL.md` and run the land flow." Skills are *callable subroutines* with explicit preconditions (e.g., land requires: on `symphony/<id>` branch, clean worktree, issue in Merging state, PR `OPEN`). This is *named-skill composition*, and it's strict — `land` will refuse if preconditions aren't met.

3. **Trigger-phrase composition (everyskill).** Skills in the registry self-declare their triggers in the `description` field (e.g., `every-social-style` triggers on "write tweets, X posts, LinkedIn posts, social copy"). The host agent picks skills based on user-language matching. This is *emergent composition* — no explicit chaining is defined.

Symphony's model is the most explicit and most rigid. The cleanest pattern for a software factory is probably the symphony approach for the core git/CI/review flow, with trigger-phrase composition for ancillary skills (style, docs, security review).

## Spec/brief input-output conventions

The shapes are very consistent across repos:

**Input shapes:**
- *A GitHub issue* (`03_analyze_github_issue`, symphony per-issue prompt) — identifier, title, status, labels, description, comments. Often hydrated with the issue's full comment thread plus a freshly-pulled state read.
- *A PR* (`05_resolve_pr_comments`, symphony PR feedback sweep) — comments classified by priority (`MUST/should/nit`) and grouped by file.
- *A draft* (every-editorial-triage, kate-top-edit, hemingway, ai-check, every-style-check) — a Google Doc / markdown text.
- *A natural-language goal* (claude_commands `01`, coding-tutor) — augmented by reading existing context (codebase, learner profile).

**Output shapes:**
- *A `<plan>` block + an approval request* — `03_analyze_github_issue` ends with "ASK FOR APPROVAL BEFORE YOU START WORKING."
- *A persistent workpad comment* on an issue, with sections: plan, acceptance criteria, validation strategy, progress checkboxes (symphony).
- *A PR body* with What/Why/How/Validation sections written to `/tmp/pr_body.md` (symphony push skill).
- *An ordered checklist of issues with fixes*, in document order (ai-check, kate-top-edit, every-style-check). Format: `- [ ] "quoted text" → suggested fix`. **Crucially, no auto-fix.**
- *An experiment log entry* with goal, learnings, plan, outcome, lessons, revised strategy (`01_experiment_driven_development`).
- *A short structured report* with release context, funnel & bottleneck, key findings, interpretation, recommended next checks, product levers (app-growth-investigator).
- *A revised SKILL.md + onboarding state* (skill-generalizer).

The pattern is: **inputs are atoms of work (issue, PR, draft, goal); outputs are either a structured artifact (workpad/PR body/plan) or a checklist of human-actionable items.**

## Review and quality patterns

Several review/quality archetypes recur:

1. **Checklist-emitting review skills** (kate-top-edit, ai-check, every-style-check, hemingway, every-editorial-triage). These deliberately do *not* auto-fix. Output is `- [ ] "quoted text" → fix`. The human (or another agent) decides which to apply. This is a high-leverage pattern: it produces a small artifact a reviewer can scan in seconds.
2. **Multi-stage human gate** (symphony). `Human Review` is a first-class state with a *waiting* phase — agents must not modify code while in this state, only re-read comments each turn. Approval is an out-of-band action by the human (drag ticket to Merging).
3. **AI-then-human approval** for skill submissions (everyskill README): two AI reviewers (Claude Opus 4.6 + GPT-5.2) check for prompt injection, dangerous tool use, exfiltration; human merges the PR.
4. **Self-validation before handoff** (symphony). The agent must run all acceptance criteria and validation commands before transitioning to Human Review and must document outcomes with exact commands and output in the workpad.
5. **Conventional-commit body discipline** (commit skill): every commit body has `Summary`, `Rationale`, `Tests`.
6. **Rework as a clean reset, not an edit-in-place.** Symphony's Rework phase requires: re-read issue + comments, close existing PR, *delete the workpad comment*, create a fresh branch from main. This forces re-planning rather than band-aid patching.
7. **Design implementation reviewer** (claude_commands agent): structured review categories (correctly implemented / minor / major / measurements / recommendations) with exact pixel values and hex codes.
8. **Experiment log with reward signal** (`01_experiment_driven_development`): each iteration must update the log with outcome and lessons; explicit "$1000 reward / $100 penalty" framing is theatrical but functions as a "did I actually verify this?" forcing function.

## Human leverage techniques

Patterns that make a single human run many agents efficiently:

- **One persistent workpad per issue.** A single, well-shaped artifact per unit of work, in a known location, with predictable sections. Humans can scan 10 workpads faster than 10 different agent outputs.
- **Five-state queue with one waiting-on-human state.** All human attention concentrates on issues in `Human Review`. Everything else is either agent-active (`In Progress`, `Merging`) or agent-blocked-by-state (`Backlog`, `Done`). This makes the human's inbox a sortable list.
- **Tile layout for monitoring.** INSTRUCTOR_NOTES.md prescribes a 4-pane terminal layout: orchestrator log, queue, agent activity (`scripts/watch-agents.sh`), browser. The human's attention is distributed across panes by role, not interleaved.
- **Idempotent reset.** `scripts/reset-demo.sh` and `scripts/clean.sh` are idempotent. The human can confidently retry without state divergence.
- **Forbidden commands list.** Each skill enumerates what's banned (e.g., land forbids `git push`, `gh`, `--force`; push forbids `git push`, `gh pr`). The human can trust that an agent won't escape its sandbox.
- **`[claude]` prefix on agent comments.** Every agent-authored comment is prefixed `[claude]` — so the agent can scan the workpad and distinguish its own past notes from human feedback, and the human can scan for non-`[claude]` comments to find what needs an answer.
- **Trigger-phrase descriptions on skills.** The agent can auto-pick the right skill from a library based on the user's natural-language request, so the human doesn't have to remember skill names.
- **Approval-before-implementation prompt.** `03_analyze_github_issue` forces the agent to plan and ask for approval before touching code; the human approves a plan once and reaps an implementation.
- **Detail-level escape hatch.** `04_create_github_issue` offers MINIMAL / MORE / A LOT — the human controls the spec depth they want.
- **Model-hierarchy skill.** Provides a cost rubric so the agent itself routes sub-tasks to cheap models, freeing the human from micro-managing spend.
- **Default to acting unattended.** Symphony's #1 operating principle: "Never ask a human to perform follow-up actions inline — the human is not at the console." Combined with: "Stop early ONLY for a true blocker." This explicitly biases agents toward proceeding rather than halting.

## Naming and design principles

- **Skills are named after the verb the agent will say.** `commit`, `push`, `pull`, `land`, `tasks` (in symphony); `quiz-me`, `teach-me` (in coding-tutor). The skill name is the action vocabulary the host agent uses.
- **Commands are numbered + verb-phrased.** `01_experiment_driven_development`, `02_generate_codebase_context`, `03_analyze_github_issue`. Numbering implies a recommended progression / order of operations.
- **Sub-agents are named by role + domain.** `codebase-researcher`, `design-implementation-reviewer`, `design-iterator`, `prompt-engineer`, `react-figma-ui-engineer`. Each is paired with a model tier (most are Opus).
- **Granularity choice: a skill is one thing.** From skill-generalizer: skills should be "specific" and "do one thing well." `commit` doesn't `push`; `push` doesn't `land`; `land` doesn't `pull`. Each is a single verifiable transition.
- **YAML frontmatter is the trigger contract.** `name`, `description` (with explicit trigger phrases), `tags`, `version`, `allowed-tools`. The description *is* the discovery mechanism.
- **Skills can have side-files.** `scripts/`, `references/`, `assets/` under a SKILL.md, capped at 50 files / 1MB. The body of SKILL.md remains the index.

> **Cross-reference from [`23-anthropic-engineering-trilogy`](23-anthropic-engineering-trilogy.md) §3 drain (2026-05-13):** Anthropic's primary platform docs and cookbook notebooks tighten / contradict four of the conventions above:
>
> 1. **`name` is bounded:** max 64 chars, lowercase-alphanumeric+hyphens only, reserved words `anthropic` and `claude` are forbidden, no XML tags. Every's docs don't surface these constraints — they're inherited from the canonical Anthropic spec.
> 2. **`description` is bounded:** non-empty, max 1024 chars, no XML tags. (Every's docs say only that the field "doubles as the trigger contract" without quoting a length.)
> 3. **`allowed-tools` is a Claude Code extension, not canonical SKILL.md.** Anthropic's platform docs and cookbook notebooks do not include `allowed-tools` in the canonical frontmatter schema; it's a Claude-Code-host-specific extra. Symphony-style skills that use it are Claude-Code-portable but may not load on the API / claude.ai surfaces.
> 4. **The Level-1 (progressive disclosure) budget is ~100 tokens per Skill** (per Anthropic platform docs), not the "30–50 tokens" figure that circulated in earlier reconstructions. Symphony and `everyskill` descriptions written to a 30–50-token budget are leaving headroom unused; loosening to ~100 tokens per description gives the host loader more discriminative power for trigger-matching.
> 5. **The 50-file / 1MB cap is less permissive than Anthropic's framing.** The Anthropic platform docs treat Level-3 (script-execution) content as "effectively unlimited" because *script code never enters the context window* — only output does. The 50-file / 1MB cap quoted above is real but applies to bundle size, not to context cost; large scripts are fine as long as they only emit short outputs.
>
> Cross-surface non-portability is also relevant: Anthropic Custom Skills do NOT sync across claude.ai / API / Claude Code — three separate uploads are required. Every's `everyskill` registry sits *above* this fragmentation; users still pay the per-surface upload cost.
- **Preconditions enumerated, exits enumerated, banned commands enumerated.** Symphony's skills all open with preconditions and a "never do X" section. This makes them robust to being called from wrong states.
- **Numbered phases over conversational instructions.** The commands and skills all use numbered phases (Phase 1: Research; Phase 2: Plan; ...). This makes them resumable and skim-able.

## Notable quotes

- "Symphony orchestrates Claude Code agents to build software." (symphony-thumbtack/README)
- "Never ask a human to perform follow-up actions inline — the human is not at the console." (WORKFLOW.md operating principles)
- "Stop early ONLY for a true blocker." (WORKFLOW.md)
- "one persistent workpad comment per issue" (tasks SKILL.md, workpad protocol)
- "Do not call `git merge` outside the `land` skill flow." (WORKFLOW.md)
- "If a turn boundary forces an exit while the issue is still active, Symphony will continuation-retry." (WORKFLOW.md)
- "All agent-authored comments begin with `[claude]` to distinguish them from human reviewer feedback." (tasks SKILL.md)
- "ASK FOR APPROVAL BEFORE YOU START WORKING on the TODO LIST." (`03_analyze_github_issue.md`)
- "80% of agent tasks are janitorial." (model-hierarchy SKILL.md)
- "Identify style issues but does not automatically fix them." (every-style-check SKILL.md)
- "Curated skill files that extend AI agent capabilities" / "Must pass both AI reviews, then receive human approval." (everyskill README)
- "Always start by reading `~/coding-tutor-tutorials/learner_profile.md`." (coding-tutor SKILL.md)

## Recommended additional sources

1. **`symphony/workflow.py` and `symphony/orchestrator.py`** — these are explicitly skipped per the user's "don't deep-dive" rule, but if any single file in this set is worth a follow-up read for the synthesis, it's the orchestrator (state machine, dispatch loop, hook system).
2. **`symphony/prompt.py`** — would reveal how WORKFLOW.md's per-issue template is hydrated from issue state. Useful for the spec-pipeline architecture option.
3. **The `linear-demo` branch of symphony-thumbtack** — same workflow but with Linear + GitHub. Comparing the two branches shows which abstractions are core vs. integration-specific.
4. **EveryInc/plus-one-bot (referenced by skill-generalizer)** — the "Plus One bot" appears multiple times as a target deployment for skills; understanding that runtime would clarify how skills are consumed in production.
5. **`registry.json` on skills.every.to** — would surface the full curated skill list and how it's indexed (referenced in everyskill README).
6. **Anthropic Claude Code Skills documentation** — the SKILL.md format, `allowed-tools` syntax, and trigger-phrase discovery semantics are inherited from Claude Code's native skills feature.

## Open questions for synthesis

1. **Workpad vs. spec.** The workpad is *the* coordination artifact in symphony, and it's a hybrid: part spec (acceptance criteria), part plan, part log, part progress checklist. Should the software factory split these apart (a separate immutable spec vs. mutable workpad) or follow symphony's single-artifact model?
2. **One-agent-per-issue vs. role-specialized sub-agents.** Symphony uses interchangeable agents (any agent can pick up any issue); claude_commands has role-typed sub-agents (`react-figma-ui-engineer`, `codebase-researcher`). Where's the right cut?
3. **How does scaling to a small team change the queue model?** Symphony has one human as the sole reviewer; if 3 humans share a queue, do you partition by label, route by skill, or just hand-pick?
4. **Skill registries vs. project-local skills.** Symphony's skills live in `.claude/skills/`; everyskill's live in a central registry. A factory likely needs both: a small repo-local set for project-specific git flow + a broader curated set for cross-project skills. What's the loading order, and how do project-local skills override registry skills?
5. **Trigger-phrase discovery at scale.** When the registry has 100 skills, do trigger phrases still discriminate well? Symphony's named-skill invocation is more reliable but loses auto-discovery — is there a hybrid?
6. **`Rework` semantics — destructive reset or revision?** Symphony's Rework deletes the workpad. That's clean but loses history. Is there a "soft Rework" worth defining?
7. **Sub-agent fan-out for parallel review/implementation.** `05_resolve_pr_comments` spawns sub-agents per file. Symphony does not fan out within an issue. A factory probably wants both: one issue = one symphony agent, but that agent can fan out to file-level sub-agents internally. How is that coordinated against the workpad?
8. **Cost routing as a system-level concern.** model-hierarchy is a skill (agent-invoked), but cost routing arguably belongs in the conductor (Symphony decides which model to dispatch). Where should that policy live in the factory?
9. **Experiment-driven-development as a methodology vs. a one-off command.** The "/experiments/*.md with reward signal" pattern is a strong forcing function for accountability. Could it be the *default* per-issue prompt (i.e., promote it from command to workflow) for hard issues?
10. **The "checklist-only" review pattern for code.** All of Every's editorial review skills emit checklists, not auto-edits. Should code review skills (security, lint, design-against-spec) do the same — i.e., be advisory-only, with implementation left to the implementing agent? This is in tension with compound-engineering's "two-loop review" pattern (covered by another agent).
