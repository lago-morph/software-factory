# Session handoff — `<YYYY-MM-DD>` (`<Phase N close>` or `<milestone>`)

This is the pickup brief for the next agent. `<Phase / milestone>` is **closed** as of the autonomous run completed `<YYYY-MM-DD>`. The next work is `<Phase N+1 / next milestone>`.

Supersedes the [prior handoff](`<path-to-prior-handoff>`).

## Where we are

Summary of the close state. Table format:

| Concern | State | Detail |
|---|---|---|
| `<Concern 1>` | `Closed` / `Open` / `Resolved` | `<link to artifact>` |
| `<Concern 2>` | ... | ... |

## `<Project-specific state section, e.g., candidate-set state>`

Whatever load-bearing state the next agent needs to know. For a research-synthesis project, this might be the candidate set; for a code-base project, this might be the architecture / module / API surface state.

Use a table or per-item bulleted list. Link out to detailed artifacts; don't re-state their content.

## The next work — `<Phase N+1 / next milestone>`

Cross-reference the project's plan document (e.g., `ARCHITECTURE-V3-SYNTHESIS-PLAN.md`) for the canonical phase description. Then list the next phase's deliverables.

### Entry blockers (user-input territory, if any)

Decisions that genuinely need user input before the next phase can dispatch. Each blocker:

- Question
- Lead-agent recommendation
- Rewind path if user disagrees

Per the autonomous-run skill, entry blockers should be rare — most user-input territory is handled by decision briefs + adversarial review during the run. If there's a true blocker that *can't* be handled that way, name it explicitly.

### Work that doesn't need user input

What can start immediately when the next agent picks up.

## Carried-forward material (binding artifacts list)

Every artifact the next agent must read before starting. Numbered list with one-line description per artifact. The reading order matters — earlier items establish vocabulary for later ones.

1. [`<path>`](<path>) — `<one-line description; what's binding about it>`.
2. [`<path>`](<path>) — ...
3. ...

## Open questions / suggestions for the next agent to surface

Numbered list of items the next agent should consider surfacing or deciding. Each item:

- The question / suggestion.
- Lead-agent's view (if any) — but flag if it's a value judgment vs an evidence-based position.
- Where in the corpus / artifact set the evidence lives.

## Task-aware reading lists

The next likely tasks the next agent will pick up, with a per-task curated reading list. These feed directly into the [`AGENT-ENTRY.md`](../../../../AGENT-ENTRY.md) "Reading lists by task" section at handoff time — the autonomous-run skill's handoff discipline updates the entry doc from this section.

Format: one subsection per anticipated task; per-subsection a "Read:" line + a "Skip:" line. Each entry is a markdown link with a descriptive label (no bare-text references, no backtick-wrapped paths-in-link). Per [`AGENTS.md` § Internal document references](../../../../AGENTS.md#internal-document-references).

### `<Likely-next-task 1>`

- Read: `[<descriptive label>](<path>)`, `[<descriptive label>](<path>)`, ... (the docs the next agent needs to make this decision or perform this work).
- Skip: `<category of docs the agent should NOT eagerly load>` (e.g., "per-candidate substrate-requirements until the ADR is authored", "per-primitive sketches; drill on demand").

### `<Likely-next-task 2>`

- Read: ...
- Skip: ...

If you cannot enumerate the next likely tasks at handoff time, leave a single subsection: `### (Next tasks not yet enumerated)` — and explain why. The next agent then falls back to the entry doc's section-by-section navigation.

## Concrete pickup steps for the next agent

Numbered list, in order:

1. Read `<key artifact 1>`.
2. Read `<key artifact 2>`.
3. ...
N. Once read, surface to the user: `<entry blockers>`. Per [`AGENTS.md` `AGENTS-MD-d72e1a4f3c`](../../AGENTS.md#adversarial-review-must-be-real-subagents) (or wherever the project lives), real-subagent adversarial review applies to any decision brief.
N+1. Once blockers resolved, dispatch `<phase>`.

## Current git state

Branch chain at handoff (top to bottom):

- `claude/<tip-branch>` (this commit; PR pending or merged)
- `claude/<prior-branch>` ([PR `#NNN`](`<URL>`))
- ...
- `main`

`<Any additional metadata: subagent count from the run, current open PRs, etc.>`

When the chain merges, the SESSION-HANDOFF state above becomes the canonical pickup point for the next agent.
