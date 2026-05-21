---
name: add-issue-behavior
description: Walk the user through adding or changing a behavior in the sibling `issue-management` skill. Triggers when the user says things like "add a behavior to the issue skill", "change the X behavior", "I want issues to also do Y", "update the issue conventions", "the STARTED comment should also …", "add an issue convention for …", or any request that proposes a new or altered automatic action tied to GitHub issues. Collects the trigger / required action / comment-or-not / template / side-effects / GitHub-MCP feasibility, then updates `issue-management/SKILL.md` and (if needed) creates a new template file in `issue-management/templates/`. Refuses behaviors that depend on GitHub-MCP capabilities this project doesn't have, and suggests downgraded variants instead.
---

# Skill: add-issue-behavior

Sub-skill of [`issue-management`](../issue-management/SKILL.md).

Use this skill any time the user wants to **add** a new behavior to the
issue-management conventions, **change** an existing one, or **remove**
one. The skill walks the user through a structured intake, checks GitHub
MCP feasibility, and writes the changes atomically to:

- `.claude/skills/issue-management/SKILL.md` (the behavior list + the
  per-type quick-reference table + the tag list in the shared skeleton
  rules).
- `.claude/skills/issue-management/templates/comment-<tag>.md` (a new
  template file, if the behavior emits a new comment type).
- `.claude/skills/issue-management/spec/FILLING-TEMPLATES.md` (the
  placeholder-by-placeholder guidance for any new placeholders).

The user should not be expected to know any of this structure. This
skill knows it on their behalf — the user just answers questions.

---

## When to use this skill

Trigger on any of:

- "Add a behavior to the issue skill"
- "Change the STARTED comment to also include X"
- "I want a new comment type for Y"
- "Drop the QUESTIONS behavior"
- "Update the issue conventions so that …"
- "When the agent closes an issue, post a comment"
- "Whenever the agent picks up an issue, also label it"
- Or in response to the `issue-management` skill's anti-pattern note
  about editing `SKILL.md` directly.

Do NOT use this skill for:

- One-off conventions the user wants to apply only to a single issue
  (those are just plain comments).
- Changes to *other* skills.
- PR-review conventions (those would belong in a separate, future skill).

---

## The intake walk

When invoked, run the user through these questions in order. Use the
`AskUserQuestion` tool one question at a time — don't ask all at once.

### 1. What's the behavior?

Free-form. Ask "In one sentence, what should happen?"

Examples of valid answers:

- "When the agent closes an issue without a PR, post a comment naming
  the reason."
- "When the agent realises an issue is a duplicate, link to the original
  and close as duplicate."
- "When an issue has been sitting in `[QUESTIONS]` state for more than
  24 hours, post a nudge."

### 2. What is the trigger?

Ask: "What event tells the agent to do this?" Push the user to be
specific. The trigger should be a *condition the agent can detect from
inside a session*, not a wall-clock event (the agent has no scheduler).

If the user proposes a time-based trigger (e.g., "after 24 hours"),
explain that the skill can only document the rule; *acting on* a
time-based trigger would need a GitHub Action or external scheduler.
Offer to add the rule as documentation only.

### 3. Does this behavior emit a comment? If so, what tag?

If yes, ask for the tag. Conventions:

- All caps.
- Hyphenated, no spaces.
- Wrapped in `[ ]` in the rendered comment.
- New tags must not collide with the existing list:
  `STARTED`, `QUESTIONS`, `ANSWERS`, `PR-OPENED`.

If no comment, the behavior is "silent" (e.g., applying a label without
announcing it). That's allowed but the user should be told that silent
behaviors don't leave a trail on the issue thread and are easier to
forget.

### 4. What side effects on the issue itself?

A checklist, ask via `AskUserQuestion` `multiSelect: true`:

- Assign someone (`jonathanmanton` or other).
- Apply a label (requires the label to already exist — see step 5).
- Change the issue's state (`open`, `closed`, with optional reason
  `completed` / `not_planned` / `duplicate`).
- Set a milestone (requires knowing the milestone number; cannot be
  looked up via MCP).
- Add as a sub-issue of another issue.
- None — comment only.

### 5. Feasibility check (mandatory)

For each side effect picked in step 4, verify it's achievable with the
GitHub MCP tools available to this project. The capability table:

| Side effect | Achievable? |
|---|---|
| Assign existing collaborator | Yes — `issue_write update assignees=[…]`. |
| Apply *existing* label | Yes — `issue_write update labels=[…]`. Verify with `get_label` first. |
| Apply a *new* label | **No** — there is no `create_label` MCP tool. Ask the user to create the label in the GitHub UI first, then proceed. |
| Close issue with reason | Yes — `issue_write update state=closed state_reason=…`. |
| Mark duplicate | Yes — `issue_write update state=closed state_reason=duplicate duplicate_of=N`. |
| Set milestone (when number is known) | Yes — `issue_write update milestone=N`. |
| Discover milestones by name | **No** — no list-milestones MCP tool. User must supply the number. |
| Set "issue type" (Bug, Feature, …) | **No** for this org — `list_issue_types` returned 403. Use labels instead. |
| Sub-issue link to parent | Yes — `sub_issue_write add`. |
| Lock / pin / convert issue | **No** — no MCP tool. |
| Tie PR closure to issue closure | Yes via convention — put `Closes #N` in PR body. |

If the proposed behavior depends on a **No** row, the skill must either:

- (a) **Downgrade**: change the behavior to use a feasible mechanism
  (e.g., "use a comment instead of a label"); or
- (b) **Defer**: ask the user to pre-create the missing artifact (label,
  milestone) in the GitHub UI, then the behavior becomes feasible; or
- (c) **Decline**: tell the user the behavior can't be added with
  current tooling and explain why.

Always offer (a) before (c).

### 6. Edit-vs-add decision

Confirm with the user: is this a **new** behavior or a **change** to an
existing one?

- **New**: append a new `### Behavior: <NAME>` section to
  `issue-management/SKILL.md`, add a row to the per-type quick-reference
  table, add the new tag to the shared skeleton's "Tags in use" list,
  and create the template (if any).
- **Change**: edit the relevant `### Behavior:` section in place; bump
  the marker version in the template (`v1` → `v2`) so old comments
  remain identifiable as the prior schema. Edit `FILLING-TEMPLATES.md`
  for any new or removed placeholders.
- **Remove**: delete the section and the table row, but **keep** the
  template file with a `<!-- deprecated as of YYYY-MM-DD: <reason> -->`
  comment at the top, so historic comments remain interpretable.

---

## Producing the changes

After the intake walk:

1. Read [`../issue-management/SKILL.md`](../issue-management/SKILL.md)
   end-to-end so the edits stay consistent with the surrounding prose.
2. Apply edits to `SKILL.md` in this order:
   - Add / change the `### Behavior:` section.
   - Update the **Per-type quick reference** table.
   - Update the **Tags in use** list inside the "shared comment
     skeleton" section.
   - Update the **Bundled files** list if a template file was added.
3. If the behavior emits a new comment type:
   - Copy
     [`../issue-management/templates/comment-skeleton.md`](../issue-management/templates/comment-skeleton.md)
     to `comment-<tag-lowercased>.md`.
   - Fill in the body with the placeholders the behavior needs.
   - Add an `## <TAG> — comment-<tag>.md` section to
     [`../issue-management/spec/FILLING-TEMPLATES.md`](../issue-management/spec/FILLING-TEMPLATES.md)
     describing each placeholder.
4. Run a quick consistency check: every tag mentioned in the table
   appears in the skeleton tag list, in the body of `SKILL.md`, and as a
   template file (or is explicitly silent). Every template ends with a
   matching machine marker comment.
5. Commit on the current feature branch with a message of the form
   `issue-management: add behavior <NAME>` (or `change` / `remove`).
   Per [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md),
   commit AND push.
6. Open or update the PR for the issue-management skill on the current
   branch.

---

## Worked example

User says: "When the agent closes an issue without an associated PR
(e.g., user clarified it's not actually a bug), post a comment naming
the reason."

Intake walk:

1. **Behavior**: post a comment when the agent closes an issue without
   a PR.
2. **Trigger**: agent about to call `issue_write update state=closed`
   for an issue that has no linked PR.
3. **Comment tag**: `CLOSED-NO-PR`. Body summarizes the reason.
4. **Side effects**: set state=closed with state_reason of `completed`
   or `not_planned`. (Duplicates are handled by a separate behavior.)
5. **Feasibility**: all green — closing an issue and setting state
   reason are supported. No label needed.
6. **New** behavior.

The sub-skill then:

- Adds `### Behavior: CLOSED-NO-PR` to `SKILL.md`.
- Adds a row to the quick-reference table: `Closed (no PR) | [CLOSED-NO-PR] | Agent closes issue with no linked PR | state=closed; state_reason=completed or not_planned | comment-closed-no-pr.md`.
- Adds `CLOSED-NO-PR` to the tags list.
- Creates `templates/comment-closed-no-pr.md` from the skeleton, with a
  `**Reason for closing**` body field and a `**State reason**` field
  (one of `completed` / `not_planned`).
- Adds the placeholder docs to `FILLING-TEMPLATES.md`.
- Commits and pushes.

---

## Anti-patterns

- **Don't accept a behavior without going through all six intake
  steps.** Skipping the feasibility check is the most common way the
  skill ends up promising something the MCP can't deliver.
- **Don't introduce a tag that overlaps an existing one.** Even
  near-duplicates (`STARTED-AGAIN`) are bad — they break the
  scan-the-thread-at-a-glance property the templates are designed for.
- **Don't silently change a template's `v1` marker.** If the body
  shape changes, bump to `v2` so historic comments are clearly the old
  schema.
- **Don't add a behavior whose trigger is something the agent cannot
  observe.** Wall-clock-only triggers belong in a GitHub Action, not in
  this skill.
- **Don't update only `SKILL.md` and forget the template / spec.** The
  three files are the unit of change; partial updates leave the skill
  internally inconsistent. The post-edit-reread-pass skill applies.

---

## See also

- [`../issue-management/SKILL.md`](../issue-management/SKILL.md) — the
  skill being modified.
- [`../issue-management/templates/comment-skeleton.md`](../issue-management/templates/comment-skeleton.md)
  — starting point for any new per-event template.
- [`../issue-management/spec/FILLING-TEMPLATES.md`](../issue-management/spec/FILLING-TEMPLATES.md)
  — where new placeholders get documented.
- [`../post-edit-reread-pass/SKILL.md`](../post-edit-reread-pass/SKILL.md)
  — mandatory after multi-section edits like these.
- [`../always-commit-skill-to-repo/SKILL.md`](../always-commit-skill-to-repo/SKILL.md)
  — commit + push + PR discipline for the changes.
