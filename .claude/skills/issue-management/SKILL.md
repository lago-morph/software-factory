---
name: issue-management
description: Conventions for working with GitHub issues in this repository, plus a modify-behavior mode for adding, changing, or removing the behaviors it defines. Primary mode triggers whenever the agent is asked to work on, pick up, claim, investigate, answer questions on, close, mark duplicate / invalid / wontfix, link as a sub-issue, or open a pull request for a GitHub issue — phrases like "work on issue #N", "pick up #N", "address #N", "close #N as duplicate", "this is invalid", "wontfix this", "make this a sub-issue of #M". Modify-behavior mode triggers on phrases of the form "I want to (action) issue behavior (name or synonym)" or semantically equivalent — e.g. "I want to add issue behavior X", "I want to change the STARTED issue behavior", "I want to modify the issue behavior for duplicates", "I want to remove the wontfix issue behavior", "I want to update issue behavior QUESTIONS", "tweak / edit / revise / adjust the issue skill's ANSWERS behavior", "add a new issue behavior for Y". In modify mode the skill walks the user through a 6-step intake (trigger, comment-or-not, side effects, MCP feasibility, edit-vs-add) and updates this SKILL.md plus the templates atomically.
---

# Skill: issue-management

This skill is a **conventions registry** for working with GitHub issues in
this repository. It runs in one of two modes:

- **Primary mode** — execute one of the defined behaviors when the agent is
  working with an actual issue (claim it, ask questions, summarize answers,
  close as duplicate/invalid/wontfix, link sub-issues, open a PR).
- **[Modify-behavior mode](#modify-behavior-mode-add-change-or-remove-a-behavior)**
  — edit the skill itself: add a new behavior, change an existing one,
  or remove one, with templates and the quick-reference table kept in
  sync. Triggered by phrases like *"I want to add issue behavior X"*,
  *"change the STARTED issue behavior"*, *"modify the duplicate issue
  behavior"*. The two modes never run together; identify which one the
  user's request matches and stay in it for the turn.

---

## When to use primary mode

Read this skill at the start of any turn that involves an issue, including:

- "Work on issue #N" / "pick up #N" / "look at #N" / "address #N".
- "What's the status of issue #N?" — the skill tells you which comments to expect.
- "Close #N as duplicate of #M" / "this is invalid" / "wontfix this".
- "Make #N a sub-issue of #M" / "link these as parent / child".
- The user answers a question you previously posted — the **ANSWERS** behavior triggers.
- You're about to open a PR that fixes an issue — the **PR-OPENED** behavior triggers.

Do NOT use this skill for:

- Pull-request review conventions (separate concern; not in scope here).
- Issue-comment text that is purely conversational and not one of the
  defined events. Conversational replies don't use the template.

For modify-behavior triggers, see the
[modify-behavior section](#modify-behavior-mode-add-change-or-remove-a-behavior)
below.

---

## Identity resolution (do this first)

**The agent's GitHub identity is not hardcoded anywhere in this skill.**
Whenever a behavior needs the login name (to self-assign, or to format
the metadata line of a comment), the agent must look it up:

```text
call mcp__github__get_me  →  read the `login` field of the result  →  use that string
```

Cache the value for the rest of the session. The result is the same
identity that authored any comments and commits the MCP makes on the
user's behalf.

In this skill, the placeholder `<mcp-login>` always means "the login
returned by `get_me`." Never substitute a literal username into the
skill or its templates.

---

## Repository context

- **Repo**: `lago-morph/software-factory`
- **Authenticated MCP identity**: resolved at runtime via
  `mcp__github__get_me` — see [Identity resolution](#identity-resolution-do-this-first).
  In this project the MCP identity happens to be the same human as the
  user typing the prompts, so "the agent" and "the user" share a single
  login. This is **not** load-bearing for the skill — the distinguishing
  signal that an *agent* (rather than the human) is acting is the
  presence of the structured `[TAG]` comments below, not the author
  name.
- **Default GitHub labels are present in this repo.** Confirmed by
  `get_label` probe: `bug`, `documentation`, `duplicate`, `enhancement`,
  `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`.
  Several behaviors below rely on this — they will gracefully no-op the
  label step if a label has been deleted.
- **Label-create not available via MCP** — `get_label` works,
  `create_label` does not exist. Any new behavior that wants a *new*
  label must require the user to pre-create it in the GitHub UI.

---

## The behaviors

Each behavior names the **trigger** (when the agent must act), the
**comment type** to post (if any), and the **side effects** on the
issue itself (assignee, label, state). The comment templates live in
`templates/` next to this file.

### Behavior: STARTED (claiming an unclaimed issue)

**Trigger**: The agent is told to work on an issue (e.g. "pick up #N",
"start on #N", "address #N", "work on issue N") **and** the issue has
no current assignee.

**Required action**:

1. `get_me` → resolve `<mcp-login>`.
2. `issue_read` method=`get` to confirm the issue is unassigned (the
   `assignees` field is empty) and read its title/body.
3. `issue_read` method=`get_comments` to ensure no prior STARTED comment
   already exists. If one does, do not post a duplicate.
4. `issue_write` method=`update` with `assignees: [<mcp-login>]` to
   claim it. (If the issue is already assigned to someone else, do NOT
   reassign — instead ask the user whether to proceed.)
5. `get_label` for `good first issue`. If it exists (it's a GitHub
   default and should), `issue_write` method=`update` with
   `labels: [...existing, "good first issue"]` to mark the issue as
   claimed-by-an-agent. The `good first issue` label is the *visible*
   marker in the issue list — the assignee avatar alone is too small to
   notice.
6. Post a **STARTED** comment using [`templates/comment-started.md`](./templates/comment-started.md).

> **Note on the choice of label**: this repo repurposes GitHub's default
> `good first issue` label (originally "good for newcomers") as the
> "claimed by an agent" marker, because (a) it already exists with no
> setup needed and (b) it renders as a colored pill in the issue list.
> If you want a dedicated label later, create one in the GitHub UI and
> update this behavior via [modify-behavior mode](#modify-behavior-mode-add-change-or-remove-a-behavior).

**Comment template**: `templates/comment-started.md`.

### Behavior: QUESTIONS (asking the user for clarification)

**Trigger**: The agent has clarifying questions for the user about an
in-flight issue. Each batch of questions gets one comment — do not post
one comment per question.

**Required action**:

1. Group questions logically. Number them so the user's answers can
   reference numbers.
2. `get_label` for `question` (GitHub default). If it exists,
   `issue_write` method=`update` with
   `labels: [...existing, "question"]`. The `question` label flags in
   the issue list that the issue is waiting on user input.
3. Post a **QUESTIONS** comment using [`templates/comment-questions.md`](./templates/comment-questions.md).
4. If the agent's session is about to end before the user can answer,
   record the QUESTIONS comment in the in-flight tracking file per the
   [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md)
   skill.

**One outstanding QUESTIONS comment at a time.** If a previous QUESTIONS
comment hasn't been answered yet, add to that batch rather than opening
a new one (post a new comment that references the prior question
numbers; do not edit the original).

### Behavior: ANSWERS (summarizing the user's answers)

**Trigger**: The user has answered a prior QUESTIONS comment, either by
posting on the issue or by replying in the agent's chat session.

**Required action**:

1. Re-read the most recent unanswered QUESTIONS comment (`issue_read`
   method=`get_comments`) so the summary uses the same question numbers.
2. `issue_write` method=`update` with the issue's current labels
   **minus** `question`. Use `issue_read` method=`get_labels` first to
   get the current label set; pass the filtered list back. (The MCP
   `issue_write` update replaces the label set; there is no
   "remove-one" verb.)
3. Post an **ANSWERS** comment using [`templates/comment-answers.md`](./templates/comment-answers.md).
   The body summarizes the user's answers in the agent's words — this
   produces a durable record on the issue thread even when the user
   answered in chat (which is otherwise invisible to the issue thread).
4. If the answers materially change the planned work, also note the
   change in the next commit message or PR description so the diff
   record reflects the new direction.

**Always summarize, even if the user's answer was on the issue thread
itself.** The ANSWERS comment is what the agent is committed to — it
removes ambiguity about which interpretation the agent took.

### Behavior: PR-OPENED (a PR was opened for this issue)

**Trigger**: The agent has just created a pull request that addresses an
issue.

**Required action**:

1. Ensure the PR body contains `Closes #N` (or `Fixes #N`, `Resolves
   #N`) so GitHub auto-closes the issue on merge. This is the **only
   supported way** to tie a PR to its issue via the MCP — there is no
   dedicated tool. When GitHub auto-closes the issue this way, **leave
   the `good first issue` label in place** — the claim was real and the
   work landed.
2. Post a **PR-OPENED** comment on the issue using
   [`templates/comment-pr-opened.md`](./templates/comment-pr-opened.md).
3. After pushing and opening the PR, also follow the
   [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md)
   and [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md)
   conventions.

**One PR-OPENED comment per PR.** If a second PR is opened against the
same issue (e.g. the first was closed without merging), post a new
PR-OPENED comment naming the new PR; do not edit the old comment.

### Behavior: CLOSED-NO-PR (agent closes an issue without a PR)

**Trigger**: The agent is closing an issue without an associated PR —
e.g. the user clarified the issue is not actually a bug, or the work
was completed by some other means.

**Required action**:

1. Decide the `state_reason`: `completed` if the situation it describes
   is now resolved (e.g. "it was already fixed in an unrelated PR"),
   `not_planned` if the work is being abandoned.
2. `issue_write` method=`update` with `state: "closed"` and the chosen
   `state_reason`.
3. The `good first issue` label is **left in place**. This behavior
   does not remove it — only the discard-style closures
   (DUPLICATE / INVALID / WONTFIX) do.
4. Post a **CLOSED-NO-PR** comment using
   [`templates/comment-closed-no-pr.md`](./templates/comment-closed-no-pr.md).

### Behavior: DUPLICATE (close as duplicate of another issue)

**Trigger**: The agent (or the user via the agent) determines the
issue is a duplicate of another issue.

**Required action**:

1. Identify the original issue's number (`<orig>`).
2. `issue_read` method=`get_labels` to get the current label set;
   compute the new set as `(current ∪ {"duplicate"}) - {"good first issue"}`.
3. `issue_write` method=`update` with:
   - `state: "closed"`
   - `state_reason: "duplicate"`
   - `duplicate_of: <orig>`
   - `labels: <computed set>`
4. Post a **DUPLICATE** comment using
   [`templates/comment-duplicate.md`](./templates/comment-duplicate.md),
   naming the original issue.

### Behavior: INVALID (close as invalid)

**Trigger**: The agent (or the user via the agent) determines the
issue does not represent a real problem — e.g. it's based on a
misunderstanding, or the described behavior is intentional.

**Required action**:

1. `issue_read` method=`get_labels`; compute new set as
   `(current ∪ {"invalid"}) - {"good first issue"}`.
2. `issue_write` method=`update` with:
   - `state: "closed"`
   - `state_reason: "not_planned"`
   - `labels: <computed set>`

   (GitHub's `state_reason` enum has no `invalid` value; the label
   carries the semantic distinction.)
3. Post an **INVALID** comment using
   [`templates/comment-invalid.md`](./templates/comment-invalid.md)
   explaining the reasoning.

### Behavior: WONTFIX (close as wontfix)

**Trigger**: The agent (or the user via the agent) determines the
issue is valid but the project will not address it — out of scope, too
expensive, conflicts with a design choice, etc.

**Required action**:

1. `issue_read` method=`get_labels`; compute new set as
   `(current ∪ {"wontfix"}) - {"good first issue"}`.
2. `issue_write` method=`update` with:
   - `state: "closed"`
   - `state_reason: "not_planned"`
   - `labels: <computed set>`
3. Post a **WONTFIX** comment using
   [`templates/comment-wontfix.md`](./templates/comment-wontfix.md)
   explaining the reasoning.

### Behavior: SUB-ISSUE-LINKED (link an issue as a sub-issue of a parent)

**Trigger**: The agent links one issue as a sub-issue of another — e.g.
breaking a large issue into trackable parts, or recognising that an
existing issue is a sub-task of another.

**Required action**:

1. Identify the parent issue number and the child issue's GitHub node
   ID. The child node ID is **not** the issue number — get it from
   `issue_read` method=`get` on the child (the `id` field in the
   result, or equivalent GraphQL node ID).
2. `sub_issue_write` method=`add` with `issue_number: <parent>` and
   `sub_issue_id: <child_node_id>`.
3. Post a **SUB-ISSUE-LINKED** comment **on the parent issue** using
   [`templates/comment-sub-issue-linked.md`](./templates/comment-sub-issue-linked.md),
   naming the child by number and title. (Do not also post on the
   child — that's noise; the child's linkage is visible in its own
   sidebar.)

---

## The shared comment skeleton

Every issue-management comment uses **the same structural skeleton** so
the issue thread reads as a uniform timeline, but each type has a
**distinctive bold tag and one-line summary line** so a reader scanning
the thread sees the event types at a glance.

```markdown
> **[TAG]** — <one-line human-readable summary>
> <ISO-8601 UTC timestamp> · <event-specific metadata>

<body — content varies by type; see per-type template>

<sub>posted by the <code>issue-management</code> skill</sub>
<!-- issue-management:<event-tag>:v1 -->
```

Rules every comment template MUST follow:

1. **Opens with a blockquote** containing two lines: the tag line and
   the metadata line. Blockquotes render as a left-margin bar in the
   GitHub UI, giving every skill-emitted comment a recognizable
   silhouette and distinguishing it from free-form prose.
2. **The tag is in bold square brackets**, uppercase, no emojis. Tags
   in use: `[STARTED]`, `[QUESTIONS]`, `[ANSWERS]`, `[PR-OPENED]`,
   `[CLOSED-NO-PR]`, `[DUPLICATE]`, `[INVALID]`, `[WONTFIX]`,
   `[SUB-ISSUE-LINKED]`. When modify-behavior mode adds a new behavior,
   the new tag goes here in this list.
3. **A short one-line summary** follows the tag on the same line,
   separated by `— `. The summary tells a thread-scanner *what*
   without forcing them to expand the comment.
4. **The body uses standard markdown** — no nested blockquote (which
   would visually conflate it with the header bar).
5. **Footer is a single HTML `<sub>` line plus a machine-readable HTML
   comment marker**. The marker lets future automation grep for, count,
   and validate skill-emitted comments. The marker form is exactly
   `<!-- issue-management:<event-tag>:v1 -->` so it survives copy-paste
   into anywhere markdown is rendered (the comment is invisible).
6. **No emojis.** This repo's style avoids them in committed artifacts.

The per-type templates all share this skeleton; only the tag, summary,
and body fields differ. This gives the desired effect: visually
*similar* (same shape, same left bar, same footer), but *distinct at a
glance* (the bold tag and summary tell you immediately which kind of
event it is).

---

## Per-type quick reference

| Event | Tag | Trigger | Side effects on issue | Template |
|---|---|---|---|---|
| Picked up | `[STARTED]` | Agent picks up an unassigned issue | Assignee = `<mcp-login>`; `good first issue` label | [`templates/comment-started.md`](./templates/comment-started.md) |
| Asked | `[QUESTIONS]` | Agent needs user input | Add `question` label | [`templates/comment-questions.md`](./templates/comment-questions.md) |
| Got answers | `[ANSWERS]` | User answered (here or in chat) | Remove `question` label | [`templates/comment-answers.md`](./templates/comment-answers.md) |
| PR exists | `[PR-OPENED]` | A PR addressing the issue was opened | PR body must say `Closes #N`. `good first issue` left in place — merge will auto-close the issue. | [`templates/comment-pr-opened.md`](./templates/comment-pr-opened.md) |
| Closed (no PR) | `[CLOSED-NO-PR]` | Agent closes issue without a PR | `state=closed`; `state_reason=completed` or `not_planned`. Label set unchanged. | [`templates/comment-closed-no-pr.md`](./templates/comment-closed-no-pr.md) |
| Duplicate | `[DUPLICATE]` | Issue is a duplicate of another | `state=closed`; `state_reason=duplicate`; `duplicate_of=<orig>`; add `duplicate` label; **remove `good first issue`** | [`templates/comment-duplicate.md`](./templates/comment-duplicate.md) |
| Invalid | `[INVALID]` | Issue is invalid (not a real problem) | `state=closed`; `state_reason=not_planned`; add `invalid` label; **remove `good first issue`** | [`templates/comment-invalid.md`](./templates/comment-invalid.md) |
| Wontfix | `[WONTFIX]` | Issue is valid but won't be worked on | `state=closed`; `state_reason=not_planned`; add `wontfix` label; **remove `good first issue`** | [`templates/comment-wontfix.md`](./templates/comment-wontfix.md) |
| Sub-issue linked | `[SUB-ISSUE-LINKED]` | A child is linked under a parent | `sub_issue_write add` (no label / state change) | [`templates/comment-sub-issue-linked.md`](./templates/comment-sub-issue-linked.md) |

---

## Label lifecycle summary

| Closure path | `good first issue` |
|---|---|
| PR merged (auto-close via `Closes #N`) | **kept** — work landed |
| CLOSED-NO-PR | **kept** — agent decides per-case |
| DUPLICATE | **removed** |
| INVALID | **removed** |
| WONTFIX | **removed** |

| Behavior | `question` label |
|---|---|
| QUESTIONS | **added** |
| ANSWERS | **removed** |

| Behavior | Closure-reason label |
|---|---|
| DUPLICATE | `duplicate` added |
| INVALID | `invalid` added |
| WONTFIX | `wontfix` added |

---

## Workflow (per event)

### STARTED

```text
1. get_me → cache <mcp-login>
2. issue_read get (confirm unassigned)
3. issue_read get_comments (abort if STARTED already present)
4. issue_write update assignees=[<mcp-login>]
5. get_label("good first issue"); if found, issue_write update labels=[...existing, "good first issue"]
6. add_issue_comment using templates/comment-started.md
```

### QUESTIONS

```text
1. compose grouped, numbered questions
2. get_label("question"); if found, issue_write update labels=[...existing, "question"]
3. add_issue_comment using templates/comment-questions.md
4. if session may end before user answers: record in research/PLAN.md or IN-FLIGHT.md per in-flight-workflow-tracking
```

### ANSWERS

```text
1. issue_read get_comments → find the prior QUESTIONS comment
2. issue_read get_labels → current set
3. issue_write update labels=(current - {"question"})
4. add_issue_comment using templates/comment-answers.md
```

### PR-OPENED

```text
1. confirm PR body contains "Closes #N" (or "Fixes #N" / "Resolves #N") — update PR if it doesn't
2. add_issue_comment using templates/comment-pr-opened.md, naming the PR by number and URL
```

### CLOSED-NO-PR

```text
1. decide state_reason ("completed" or "not_planned")
2. issue_write update state="closed", state_reason=<chosen>
3. add_issue_comment using templates/comment-closed-no-pr.md
```

### DUPLICATE

```text
1. identify original issue number <orig>
2. issue_read get_labels → current set
3. issue_write update
     state="closed", state_reason="duplicate", duplicate_of=<orig>,
     labels=(current ∪ {"duplicate"}) - {"good first issue"}
4. add_issue_comment using templates/comment-duplicate.md
```

### INVALID

```text
1. issue_read get_labels → current set
2. issue_write update
     state="closed", state_reason="not_planned",
     labels=(current ∪ {"invalid"}) - {"good first issue"}
3. add_issue_comment using templates/comment-invalid.md
```

### WONTFIX

```text
1. issue_read get_labels → current set
2. issue_write update
     state="closed", state_reason="not_planned",
     labels=(current ∪ {"wontfix"}) - {"good first issue"}
3. add_issue_comment using templates/comment-wontfix.md
```

### SUB-ISSUE-LINKED

```text
1. issue_read get on the child → cache its `id` (the node ID, not the issue number)
2. sub_issue_write method="add" issue_number=<parent> sub_issue_id=<child node id>
3. add_issue_comment ON THE PARENT using templates/comment-sub-issue-linked.md, naming the child
```

---

## Anti-patterns

- **Hardcoding the MCP login.** Always `get_me`. The skill must work
  even if the MCP identity changes (re-auth, different repo, fork).
- **Posting a STARTED comment for an issue you didn't actually claim.**
  The assignee update, the label, and the STARTED comment are a *unit*
  — do all three or none.
- **Posting QUESTIONS spread across multiple comments.** One batched
  numbered list per round-trip. The user can then answer with
  "1: foo, 2: bar" without ambiguity.
- **Forgetting to remove the `question` label when posting ANSWERS.**
  The label is how a thread-scanner knows the issue is still waiting on
  the user. Leaving it on after an answer is misleading.
- **Skipping the ANSWERS comment when the user answered in chat.** The
  issue thread has no idea what the user said in chat. Without the
  ANSWERS summary, the next agent (or the next human reader) sees only
  the question and no resolution.
- **Editing prior issue-management comments to "fix" what's now wrong.**
  Post a new comment instead. The append-only timeline is the point.
- **Forgetting `Closes #N` in the PR body.** Without it, merging the
  PR does NOT close the issue automatically — and the PR-OPENED
  comment's "will close" claim becomes a lie.
- **Removing the `good first issue` label after a successful PR.**
  Don't. The label means "an agent claimed this and the claim was
  real"; PR-merge preserves that signal.
- **Failing to read `get_labels` before label-updating writes.** The
  MCP `issue_write` *replaces* the label set; if you pass only the new
  label, you wipe the old ones. Always compute the new full set from
  the current set.
- **Editing this `SKILL.md` directly to add a behavior.** Use
  [modify-behavior mode](#modify-behavior-mode-add-change-or-remove-a-behavior)
  so the change is structured, the template is generated alongside, and
  the per-type quick-reference table stays in sync.

---

## Capability reference

A summary of what the GitHub MCP integration can and can't do — used
both by primary-mode behaviors and by the modify-behavior feasibility
check:

- **Can**: create / update / close issues; comment on issues and PRs;
  read issues, comments, labels, sub-issues; assign existing
  collaborators; apply *pre-existing* labels; create branches; create /
  update PRs (including body text, draft state, reviewers); merge PRs;
  enable / disable auto-merge; link parent/child via `sub_issue_write`.
- **Cannot via MCP**: create / edit / delete *labels*; list / create
  *milestones* (you can `issue_write milestone=N` if you already know
  the number); manage *issue types* (org-level admin); lock / pin /
  convert issues; mention people who aren't repo collaborators.
- **Via convention, not tool**: `Closes #N` / `Fixes #N` / `Resolves
  #N` in PR body to auto-close on merge.
- **Identity**: resolved at runtime via `mcp__github__get_me` — never
  hardcoded.
- **`labels` writes REPLACE the set.** No "add one" / "remove one"
  verb. Read with `issue_read get_labels` first, then write the merged
  new set.
- **Default labels confirmed present** in `lago-morph/software-factory`:
  `bug`, `documentation`, `duplicate`, `enhancement`, `good first
  issue`, `help wanted`, `invalid`, `question`, `wontfix`. Behaviors
  may rely on these without setup.

---

## Modify-behavior mode (add, change, or remove a behavior)

This mode edits the skill itself. Use it any time the user wants to
**add** a new behavior to the conventions, **change** an existing one,
or **remove** one.

### Triggers for this mode

Phrases of the form **"I want to (action) issue behavior (name or
synonym for the behavior)"**, and semantic equivalents. Examples:

- "I want to add issue behavior X"
- "I want to change issue behavior STARTED"
- "I want to modify the issue behavior for duplicates"
- "I want to remove the wontfix issue behavior"
- "I want to update issue behavior QUESTIONS"
- "Tweak / edit / revise / adjust the issue skill's ANSWERS behavior"
- "Add a new issue behavior for marking a stale issue"
- "Drop the SUB-ISSUE-LINKED behavior"

Action synonyms that should trip this mode: add, create, introduce,
change, modify, update, alter, adjust, tweak, edit, revise, rewrite,
remove, delete, drop, retire.

Behavior names can be referenced by their tag (`STARTED`,
`PR-OPENED`, ...) or by a synonym ("the claim behavior", "the duplicate
behavior", "the answers comment").

Do NOT enter this mode for:

- One-off conventions the user wants to apply to a single issue (those
  are plain comments).
- Changes to *other* skills.
- PR-review conventions (those would belong in a separate, future skill).

### The intake walk

Run the user through these questions in order. Use `AskUserQuestion`
one question at a time — don't ask all at once.

#### 1. What's the behavior?

Free-form. Ask "In one sentence, what should happen?"

Examples of valid answers:

- "When the agent closes an issue without a PR, post a comment naming
  the reason."
- "When the agent realises an issue is a duplicate, link to the original
  and close as duplicate."
- "When an issue has been sitting in `[QUESTIONS]` state for more than
  24 hours, post a nudge."

#### 2. What is the trigger?

Ask: "What event tells the agent to do this?" Push the user to be
specific. The trigger should be a *condition the agent can detect from
inside a session*, not a wall-clock event (the agent has no scheduler).

If the user proposes a time-based trigger (e.g., "after 24 hours"),
explain that the skill can only document the rule; *acting on* a
time-based trigger would need a GitHub Action or external scheduler.
Offer to add the rule as documentation only.

#### 3. Does this behavior emit a comment? If so, what tag?

If yes, ask for the tag. Conventions:

- All caps.
- Hyphenated, no spaces.
- Wrapped in `[ ]` in the rendered comment.
- New tags must not collide with the existing list:
  `STARTED`, `QUESTIONS`, `ANSWERS`, `PR-OPENED`, `CLOSED-NO-PR`,
  `DUPLICATE`, `INVALID`, `WONTFIX`, `SUB-ISSUE-LINKED`.

If no comment, the behavior is "silent" (e.g., applying a label without
announcing it). That's allowed but the user should be told that silent
behaviors don't leave a trail on the issue thread and are easier to
forget.

#### 4. What side effects on the issue itself?

A checklist, ask via `AskUserQuestion` with `multiSelect: true`:

- Assign someone (`<mcp-login>` for self, or another login).
- Apply a label (requires the label to already exist — see step 5).
- Remove a label.
- Change the issue's state (`open`, `closed`, with optional reason
  `completed` / `not_planned` / `duplicate`).
- Set a milestone (requires knowing the milestone number; cannot be
  looked up via MCP).
- Add as a sub-issue of another issue.
- None — comment only.

#### 5. Feasibility check (mandatory)

For each side effect picked in step 4, verify it's achievable with the
GitHub MCP tools available to this project. The capability table:

| Side effect | Achievable? |
|---|---|
| Self-assign as the MCP identity | Yes — `get_me` → `login` → `issue_write update assignees=[<login>]`. Never hardcode the login. |
| Assign existing collaborator (other than self) | Yes — `issue_write update assignees=[…]`. |
| Apply *existing* label | Yes — `issue_write update labels=[…]`. `get_label` first to confirm presence. **Note**: `issue_write update labels=…` REPLACES the set; always read current via `issue_read get_labels` and pass the merged list. |
| Apply a *new* label (not yet in the repo) | **No** — there is no `create_label` MCP tool. Ask the user to create the label in the GitHub UI first, then proceed. |
| Default GitHub labels | Yes — confirmed present (see [Capability reference](#capability-reference)). Behaviors may rely on them without setup. |
| Remove a label | Yes — same `issue_write update labels=…` replace-with-the-filtered-set pattern. |
| Close issue with reason | Yes — `issue_write update state=closed state_reason=…`. Reason enum: `completed` / `not_planned` / `duplicate`. No `invalid` or `wontfix` reason — use `not_planned` + the corresponding label. |
| Mark duplicate | Yes — `issue_write update state=closed state_reason=duplicate duplicate_of=N`. |
| Set milestone (when number is known) | Yes — `issue_write update milestone=N`. |
| Discover milestones by name | **No** — no list-milestones MCP tool. User must supply the number. |
| Set "issue type" (Bug, Feature, …) | **No** for this org — `list_issue_types` returned 403. Use labels instead. |
| Sub-issue link to parent | Yes — `sub_issue_write add issue_number=<parent> sub_issue_id=<child node id>`. Note the child arg is the **node ID**, not the issue number. |
| Lock / pin / convert issue | **No** — no MCP tool. |
| Tie PR closure to issue closure | Yes via convention — put `Closes #N` in PR body. |

If the proposed behavior depends on a **No** row, the skill must either:

- **(a) Downgrade**: change the behavior to use a feasible mechanism
  (e.g., "use a comment instead of a label"); or
- **(b) Defer**: ask the user to pre-create the missing artifact
  (label, milestone) in the GitHub UI, then the behavior becomes
  feasible; or
- **(c) Decline**: tell the user the behavior can't be added with
  current tooling and explain why.

Always offer (a) before (c).

#### 6. Edit-vs-add decision

Confirm with the user: is this a **new** behavior or a **change** to an
existing one?

- **New**: append a new `### Behavior: <NAME>` section to the
  [behaviors list](#the-behaviors), add a row to the
  [per-type quick reference](#per-type-quick-reference) table, add the
  new tag to the [shared skeleton's "Tags in use" list](#the-shared-comment-skeleton),
  add a workflow block to the [Workflow section](#workflow-per-event),
  and create the template (if any).
- **Change**: edit the relevant `### Behavior:` section in place; bump
  the marker version in the template (`v1` → `v2`) so old comments
  remain identifiable as the prior schema. Edit
  [`spec/FILLING-TEMPLATES.md`](./spec/FILLING-TEMPLATES.md) for any
  new or removed placeholders.
- **Remove**: delete the section, the table row, the tag from the tags
  list, and the workflow block. **Keep** the template file with a
  `<!-- deprecated as of YYYY-MM-DD: <reason> -->` comment at the top,
  so historic comments remain interpretable.

### Producing the changes

After the intake walk:

1. Read this `SKILL.md` end-to-end so the edits stay consistent with
   the surrounding prose.
2. Apply edits to `SKILL.md` in this order:
   - Add / change / remove the `### Behavior:` section.
   - Update the **Per-type quick reference** table.
   - Update the **Tags in use** list inside the shared skeleton section.
   - Update the **Workflow (per event)** section.
   - Update the **Bundled files** list if a template file was added /
     removed.
   - Update the **Label lifecycle summary** if the new behavior touches
     `good first issue`, `question`, or a closure-reason label.
3. If the behavior emits a new comment type:
   - Copy
     [`templates/comment-skeleton.md`](./templates/comment-skeleton.md)
     to `templates/comment-<tag-lowercased>.md`.
   - Fill in the body with the placeholders the behavior needs.
   - Add an `## <TAG> — comment-<tag>.md` section to
     [`spec/FILLING-TEMPLATES.md`](./spec/FILLING-TEMPLATES.md)
     describing each placeholder.
4. Run a consistency check (per
   [`post-edit-reread-pass`](../post-edit-reread-pass/SKILL.md)): every
   tag mentioned in the table appears in the skeleton tag list, in the
   body of `SKILL.md`, and as a template file (or is explicitly
   silent). Every template ends with a matching machine marker comment.
5. Commit on the current feature branch with a message of the form
   `issue-management: add behavior <NAME>` (or `change` / `remove`).
   Per [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md),
   commit AND push.
6. Open or update the PR for this skill on the current branch.

### Worked example

User says: "I want to add an issue behavior for when an issue is
re-opened after being closed — post a comment naming why."

Intake walk:

1. **Behavior**: post a comment when the agent re-opens a closed issue.
2. **Trigger**: agent about to call `issue_write update state=open`
   for an issue currently in the `closed` state.
3. **Comment tag**: `REOPENED`. Body summarizes the reason.
4. **Side effects**: `state=open`. Also: if the prior closure was
   DUPLICATE / INVALID / WONTFIX, removing the corresponding label
   should be considered (ask the user).
5. **Feasibility**: all green — re-opening and removing labels are
   supported.
6. **New** behavior.

The skill then:

- Adds `### Behavior: REOPENED` to the behaviors list.
- Adds a row to the quick-reference table:
  `Re-opened | [REOPENED] | Agent re-opens a previously closed issue | state=open; optionally remove the prior closure-reason label | comment-reopened.md`.
- Adds `REOPENED` to the tags list.
- Adds a workflow block.
- Creates `templates/comment-reopened.md` from the skeleton, with a
  `**Why re-opened**` body field.
- Adds the placeholder docs to `FILLING-TEMPLATES.md`.
- Commits and pushes.

### Anti-patterns specific to modify-behavior mode

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
  internally inconsistent.
- **Don't conflate the two modes.** If a turn begins in primary mode
  (the agent is working an issue) and the user mid-turn says "actually,
  change the STARTED behavior to do X", finish the in-flight primary
  action first, then switch to modify-behavior mode. Don't interleave.

---

## Bundled files

- `templates/comment-started.md` — STARTED comment template.
- `templates/comment-questions.md` — QUESTIONS comment template.
- `templates/comment-answers.md` — ANSWERS comment template.
- `templates/comment-pr-opened.md` — PR-OPENED comment template.
- `templates/comment-closed-no-pr.md` — CLOSED-NO-PR comment template.
- `templates/comment-duplicate.md` — DUPLICATE comment template.
- `templates/comment-invalid.md` — INVALID comment template.
- `templates/comment-wontfix.md` — WONTFIX comment template.
- `templates/comment-sub-issue-linked.md` — SUB-ISSUE-LINKED comment template.
- `templates/comment-skeleton.md` — the shared skeleton, copied from
  when modify-behavior mode creates a new per-event template.
- `spec/FILLING-TEMPLATES.md` — concrete guidance on how to fill each
  placeholder in each template.

---

## See also

- [`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md)
  — for cases where the agent posts a QUESTIONS comment and the session
  may end before the user answers.
- [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md)
  — discipline that applies whenever this skill changes.
- [`github-connection-resilience`](../github-connection-resilience/SKILL.md)
  — what to do if a GitHub MCP call inside one of these behaviors fails.
- [`post-edit-reread-pass`](../post-edit-reread-pass/SKILL.md) —
  mandatory after modify-behavior mode produces a multi-section edit
  to this file.
