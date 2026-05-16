# Spec: `plan-as-skill-precursor`

## Intent

When a user asks for a multi-step plan AND mentions (or it becomes obvious during planning) that the work will eventually be encoded as a reusable skill, do not write the plan and the skill spec as separate artifacts. Write a single plan file in which the *terminal step* authors the skill, using two structured knowledge-accumulators that are part of the plan itself: (a) pre-execution guidance baked into the terminal step as Principles / Anti-patterns / Verification rules, and (b) per-step `### Lessons learned` subsections that get populated during execution. The skill is then synthesized from the plan + the prior steps' PR descriptions.

This earns its place in the skill library because in this session I initially produced two files (a plan and a skill spec stub), the spec stub turned out to be a hollow set of `TBD` placeholders despite the user having given substantial pre-execution wisdom, and the user had to point out that the cleanest shape was to collapse them: "the skill is really 'do this plan, but in a general way'." The right shape was *one* file with the spec material embedded.

## Trigger

Activate when **all** of these conditions hold:

- The user is asking for a plan with multiple steps that will be executed across multiple sessions or by multiple fresh agents.
- The user mentions a future skill (explicitly: "I want a skill out of this", or implicitly: "we'll generalize this later", "this should become a reusable thing").
- The plan's specific work is itself an instance of the general pattern the skill would encode (i.e. you can literally "do the plan generally" to apply the skill elsewhere).

Direct user phrases:
- "Create a plan and we'll turn it into a skill at the end"
- "I want a skill that does this kind of thing in general"
- "We'll do this once concretely, then generalize"

Negative triggers (skip):
- One-shot tasks with no generalization intent.
- Plans whose specific subject matter is the whole point (e.g. a migration plan for a specific service) — these don't generalize.
- The user has explicitly asked for a separate skill spec file.

## Inputs

- The user's description of the multi-step work.
- The user's stated pre-execution wisdom (sizing rules, anti-patterns, principles) — usually surfaces during the planning conversation and must be captured verbatim or near-verbatim.
- The conventions of sibling skills in `.claude/skills/` (frontmatter style, section ordering, anti-pattern list shape).

## Outputs

- A single plan file (typically at the working area of the plan's subject — e.g. `<subject-dir>/<plan>.md`).
- No separate skill spec file. The skill is authored only in the plan's terminal step.
- The plan's *terminal step* outputs a real skill at `.claude/skills/<skill-name>/SKILL.md` when executed.

## Workflow

1. **Recognize the dual nature.** When the user describes a plan whose generalization is itself an interesting reusable thing, identify the skill it will become. Name it (e.g. `reconstitute-and-index-sources`).
2. **Structure the plan with these top-level sections:**
   - `## Status` — Current step / Completed steps / Next step. Updated as last action of every step.
   - `## How a fresh agent should use this file` — handoff protocol. Anchor it to existing canonical skills (e.g. `always-commit-skill-to-repo`) where they apply.
   - `## Why "Lessons learned" subsections exist` — explicit framing that per-step lessons-learned subsections exist to feed the terminal-step skill synthesis.
   - `## Scope` — what the plan does and (especially) does NOT do.
   - `## Step N — …` — one heading per executable step. Each step ends with a `### Lessons learned (Step N)` subsection that the executing agent fills before opening that step's PR.
   - `## Additional steps (to be added by user)` — explicit placeholder section between Step N and the terminal step. Includes a fresh-agent note: "If empty, skip to the terminal step."
   - `## Terminal step — Instantiate the skill` — always at the bottom. Contains:
     - Inputs: read the whole plan, fetch prior PR descriptions, inspect sibling skills.
     - **Principles to bake in** — captured from the user's pre-execution conversation, verbatim where possible.
     - **Anti-patterns to bake in** — same.
     - **Verification rules to bake in** — same.
     - Synthesis discipline + closing actions.
3. **Capture pre-execution wisdom in the terminal step.** Do not let it disappear into casual prose. Make a list under "Principles to bake in" with each user-stated rule as a bullet, using the user's exact framing where it's vivid.
4. **Mark the terminal step as terminal.** Add a note in `How a fresh agent should use this file` that the terminal step is always last; new steps added later slot in *before* it.
5. **Resist adding a separate skill spec file.** If you catch yourself thinking "I'll also write a spec for the skill," stop. The plan IS the spec. The spec is harvested in the terminal step.

## Concrete examples

### Example 1 — `/reference-only/` reorg → `reconstitute-and-index-sources` skill (this session)

User asked for a plan to reorganize `/reference-only/` into categories. During planning, user said: "I'm also definitely going to want a full reconstitute-and-index-sources skill out of this." Initial mistake: I wrote two files, a plan and a skill spec stub. The spec stub had sections like:

```markdown
## Triggers (draft, refine in final step)

TBD. Candidate triggers:
- User asks to "reorganize the reference-only directory"
```

…that is, hollow placeholders. The user pointed out: "Did we include all the things you just summarized into the individual plan steps? Basically, if i started a new session now, I don't want to lose any information." The fix was to delete the spec file and add to the plan's terminal step:

```markdown
#### Principles to bake in (from this session's pre-execution discussion)

- **Sizing target ~5–15 sources per category** with explicit permission for tiny natural categories…
- **Counting rule:** vendor doc sets and multi-chapter books count as one source.
- **Cross-cutting sources:** pick one home, note alternatives briefly — *not* a long discussion. Just record that they're conceptually in multiple places.
- **Survey before categorizing:** scan the existing corpus to get a feel for total count and natural clustering *before* deciding category names.
- …
```

Each principle is the user's actual wording captured verbatim. The terminal step then includes synthesis instructions: read all `### Lessons learned` subsections + fetch prior PR descriptions + inspect sibling skills, then author `.claude/skills/reconstitute-and-index-sources/SKILL.md`.

### Example 2 — counterfactual: refactoring a single function

User asks for a plan to refactor `parseUserPrefs()` into three smaller functions. No generalization intent. Skip this skill — write a normal plan or just do the refactor.

## Anti-patterns

- **Writing the skill spec as a separate file alongside the plan.** Hollow stubs result. The plan and the spec drift apart. In this session, this is the exact mistake the user had to correct.
- **Capturing pre-execution wisdom only in casual narrative prose.** It gets lost. Make it a bulleted list under explicit "Principles to bake in" / "Anti-patterns to bake in" headings.
- **Allowing the terminal step to drift away from the bottom.** New steps must slot *before* the terminal step. Otherwise the synthesizer doesn't have access to the later steps' lessons-learned.
- **Inventing the principles yourself instead of using the user's exact framing.** Sentences like "I don't want a long discussion about this, just to know that they are in multiple places" are the highest-fidelity record of user intent. Quote them.
- **Empty `### Lessons learned` subsections at PR time.** Mandatory: every step's executing agent fills its lessons-learned subsection before opening the step's PR. Skipped subsections = knowledge permanently lost.

## Acceptance criteria

1. The plan file contains a terminal step that includes Principles / Anti-patterns / Verification rules baked in from the user's pre-execution conversation.
2. Every executable step has a `### Lessons learned (Step N)` subsection at its bottom, with placeholder text that says when to fill it (before the PR is opened).
3. There is no separate skill spec file. The plan stands alone.
4. The "How a fresh agent should use this file" section explicitly identifies the terminal step and the rule that new steps slot before it.
5. A fresh agent reading only the plan can execute any step without additional context, and the terminal step can produce a working skill from the plan + prior PR descriptions alone.

## Files this skill creates / modifies

- `<plan-location>/<plan-name>.md` — the plan file. Typically lives in the working area of the plan's subject (e.g. `/reference-only/reorg-plan.md`).
- `.claude/skills/<skill-id>/SKILL.md` — created only by the plan's terminal step when it executes. Not created at plan-authoring time.
