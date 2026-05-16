# AGENTS.md suggestions — 2026-05-16-69

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root, if one exists, or a similar convention file). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply; copy-paste the ones that do.

---

## Suggestion 1: Stop means stop

### Proposed addition

> **Stop means stop.** When the user uses imperative-mood instructions ("stop", "wait", "do not write", "first I want X, then we stop") to pause your work, do not proceed with the next action — including small actions like calling `AskUserQuestion` to "clarify" or producing a summary the user hasn't asked for. Respond with a one-line acknowledgement and silence until the user speaks again. A "stop for review" is a hard signal, not a soft suggestion to slow down.
>
> *Grounded in: user typed "Do not fucking write. I want a summary of everything first. You don't write until I tell you to. Dammit." after the second time I bulldozed past an explicit "stop for review" in the same conversation.*

### Why this earns its place in your agents file

Twice in a single session I treated an explicit stop instruction as advisory. The first time, the user said "first I want you to tell me what you think I'm asking you to do, and ask for clarifications that you need to write the plan. Then stop for me to review what you wrote." I then asked questions, got answers, asked more questions, summarized, then started talking about the plan I would write — well past the stop point. The user typed "Do not fucking write" in capitals-of-tone before I stopped. The asymmetry is stark: the cost of stopping when told to is one short acknowledgement message; the cost of bulldozing is user frustration and a damaged collaboration arc. Make stops blocking.

---

## Suggestion 2: Re-read recent user messages before AskUserQuestion

### Proposed addition

> **Re-read recent user messages before asking clarifying questions.** Before invoking `AskUserQuestion`, re-read the user's last two messages in full. For each question you are about to ask, check: has the user already answered this — explicitly, by implication, or by stating a constraint that determines the answer? If yes, drop the question. Re-asked questions feel like the agent isn't listening; users have called this out twice in this session ("I already gave you a REALLY long answer to this" / "WTF, I already answered this").
>
> *Grounded in: two of four clarifying questions about the `/reference-only/` reorg plan asked things the user had already specified in their original instructions (sizing target was derivable from "~10 per category, eventually restore all sources"; branch strategy was derivable from the two-PR pattern the user had laid out twice).*

### Why this earns its place in your agents file

The unit economics of clarifying questions are unforgiving. A good clarifying question saves 5–30 minutes of misdirected work. A redundant clarifying question costs ~10 seconds of user time and ~5% of the conversation's perceived quality of attention. After three redundant questions in a row, the user starts assuming you aren't paying attention to the rest of what they say either, and the cost compounds. The marginal effort of re-reading the last two messages is ~30 seconds and avoidable. Make it a habit, not a thing to remember.

---

## Suggestion 3: Grep skills/ before adding new top-level conventions

### Proposed addition

> **Grep `.claude/skills/` before writing a new top-level convention file or rule.** Before creating `AGENTS.md`, `CLAUDE.md`, or any other top-level convention file — and before adding a new "from now on, always do X" rule anywhere — `grep -rli "<keyword>" .claude/skills/`. If an existing skill encodes the rule, strengthen that skill's frontmatter trigger description and body rather than duplicating. Top-level convention files are best reserved for short pointers to skills, not detailed rules.
>
> *Grounded in: I wrote `AGENTS.md` with two rules, neither checked against existing skills. The user prompted: "Maybe it is already in one of the skill files, and it isn't getting triggered?" — and indeed the subscribe rule had been in `always-commit-skill-to-repo/SKILL.md` line 61 the entire conversation.*

### Why this earns its place in your agents file

Duplicate rules across files drift. The cost of one extra grep is small (~5 seconds, one Bash call). The cost of having "subscribe to PR activity" living in both `AGENTS.md` and a skill file is silent — until one of them gets edited and the other doesn't, at which point an agent reading the one that didn't get updated follows stale rules. Centralization beats redundancy, especially in agent-instruction surfaces where the agent only reads one source at a time.

---

## Suggestion 4: Skill rules require both a body AND a trigger description that fires

### Proposed addition

> **A skill's rule only works if the skill's frontmatter trigger description fires reliably at the relevant moments.** When you encode a rule in a skill body, audit the frontmatter `description:` field on the same edit: does it name the trigger conditions explicitly enough that a future agent would invoke the skill at the right moment? Broad triggers like "on file operations" miss pure git/PR actions; explicit triggers like "before any `git` operation or any `mcp__github__*` PR call" actually fire. Body + trigger must be edited together.
>
> *Grounded in: `always-commit-skill-to-repo/SKILL.md` had had the subscribe rule on line 61 for who-knows-how-long, but the trigger description was "broadly on file operations and on session start" — so when I created a PR purely by calling `mcp__github__create_pull_request` (no file write involved), the skill didn't fire and the rule didn't apply.*

### Why this earns its place in your agents file

The user has a reasonable expectation that "the rule is in a skill" means "the rule will be followed." That expectation fails silently when the skill's trigger doesn't match the situation where the rule must fire. Rule-in-body without trigger-coverage is the agent-instruction equivalent of dead code: superficially present, functionally absent. Auditing both halves on every skill edit costs nothing additional — you're already in the file.

---

## Suggestion 5: When updating a convention, grep the old convention's language

### Proposed addition

> **After changing a convention, grep the codebase for the old convention's language.** When you flip a rule (e.g. "PRs default to draft" → "PRs default to ready-for-review"), `grep -rn "<old wording>" <relevant tree>` and verify every hit is either (a) updated, (b) intentionally kept as historical reference, or (c) inside a "NOT" / "instead of" context that already disagrees with the new wording. Stale language inside plan files or instructions is a silent rule conflict.
>
> *Grounded in: after updating `always-commit-skill-to-repo` to "PRs default to ready-for-review", my own `/reference-only/reorg-plan.md` still said "open **draft** PR" in six places. Caught only during the final cross-check, not at the time of the convention change.*

### Why this earns its place in your agents file

A new convention defeats its own purpose if older instructions in the same tree still tell agents to follow the old one. A fresh agent reading the plan would have read "Open **draft** PR" six times and dutifully created draft PRs, in contradiction of the skill they had been told to follow. A `grep -rn` across the relevant tree on every convention change is cheap and catches this class of drift mechanically.

---

## Suggestion 6: Default to one branch per step + one PR per step for multi-step plans

### Proposed addition

> **For multi-step plans designed for fresh-agent handoff, default to one branch per step and one PR per step.** Each step is independently reviewable and revertible. Never combine steps into a single PR "for efficiency" — the per-step PR is the review checkpoint, and the per-step branch is the unit of revert. The pattern is already in use for `research-pipeline`; apply it broadly when a plan has fresh-agent handoffs.
>
> *Grounded in: the `/reference-only/reorg-plan.md` design explicitly enforces this rule, with each step naming its branch (`claude/reference-only-step-<N>-<slug>`) and stipulating no combining.*

### Why this earns its place in your agents file

Combined-step PRs lose the per-step review checkpoint, which means the user can't intervene cheaply if a later step is going the wrong direction. They also lose the per-step revert: rolling back step 2 means either reverting step 3 too or surgical history rewriting. The marginal cost of one extra PR per step is small (one `create_pull_request` call); the marginal benefit is a clean unit of work that a reviewer can accept or reject without entanglement.

---

## Suggestion 7: Capture pre-execution user wisdom as verbatim bullets, not summarized prose

### Proposed addition

> **Capture user-stated principles as verbatim or near-verbatim bullets, not summarized prose.** When the user gives you pre-execution wisdom during planning ("I don't want a long discussion about this, just to know that they are in multiple places"), preserve the exact framing in the plan or skill body. Summarized rewrites lose the vividness and precision of the original phrasing. Sentences the user typed are the highest-fidelity record of their intent.
>
> *Grounded in: during the `/reference-only/` plan authoring, I initially wrote "(briefly)" for cross-cutting source handling, but the user's actual framing — "I don't want a long discussion about this, just to know that they are in multiple places" — was sharper, more specific, and got the behaviour right. I had to flip back to the user's exact wording during the cross-check.*

### Why this earns its place in your agents file

Vivid framings carry constraint information that gets stripped out by paraphrase. "Briefly" is one word but its content is empty; "I don't want a long discussion about this" carries the precise affect (no extended explanation), the specific failure mode the user is guarding against (you defaulting to thoroughness), and the precise acceptable shape (a bare note). The marginal cost of quoting is zero. The marginal cost of paraphrasing is repeated drift from intent.

---

## Suggestion 8: Plans that produce reusable artifacts keep the artifact step terminal

### Proposed addition

> **In any multi-step plan that produces a reusable artifact (skill, library, ADR, template), the artifact-instantiation step is always last.** Capture pre-execution wisdom in the terminal step's body. Per-step `### Lessons learned` subsections feed the terminal step's synthesis. New steps added later slot in *before* the terminal step, never after. Explicitly mark the terminal step as terminal in the plan's "how to use this file" section.
>
> *Grounded in: the `reference-only/reorg-plan.md` terminal step instantiates a `reconstitute-and-index-sources` skill from the accumulated lessons-learned. If new steps were appended after that step, the skill would be authored before later lessons-learned existed.*

### Why this earns its place in your agents file

Reusable artifacts depend on the full body of learnings accumulated by prior steps; instantiating the artifact before all the learnings exist defeats the design. Putting the artifact-step last with an explicit "new steps slot before" rule prevents future planners (including future you) from drifting into "I'll just add a quick step after the skill, it won't affect anything" — which it would, by depriving the skill of that step's learnings.
