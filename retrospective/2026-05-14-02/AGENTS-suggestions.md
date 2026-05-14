# AGENTS.md suggestions — 2026-05-14-02

These are proposed additions to the project's agents file (typically
`AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for
   doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your
operating posture; copy-paste the ones that do.

---

## Suggestion 1: Promote durable Q&A to repo docs

### Proposed addition

> **Promote durable Q&A.** When the user asks an explanatory or strategic question whose answer (a) took non-trivial investigation, (b) is forward-looking (about how the project will work, not just what it currently is), and (c) the user engages with substantively, proactively offer to capture the answer to a versioned repo doc. The answer has outlived the chat the moment the user is acting on it.
>
> *Grounded in: research-plan.md (this session, 2026-05-14).*

### Why this earns its place in your agents file

The user asked "how do we condense research into action?" — answering took reading INDEX.md + PLAN.md + the architectures comparison + the synthesis files. The answer ran ~600 words and laid out a concrete three-phase pipeline. Without the capture-to-repo step, that answer would have evaporated when the session ended. Instead, it now lives at `research-plan.md` and is referenced from PR #46; future sessions (and future-you after a context truncation) can read the proposed plan and either ratify it or push back against a concrete artifact. The cost of the rule is one offered sentence at the end of a substantive answer ("want me to capture this?"); the benefit is that strategic framing stops dying with the chat. Especially relevant for this repo, which is itself an exercise in turning ephemeral knowledge into durable artifacts.

---

## Suggestion 2: Frame recommendations as proposals, not decisions

### Proposed addition

> **Recommendations are not decisions.** When the user asks for strategic direction, open the response with an explicit framing — "this is a recommendation, not a settled plan; push back on any of it" — and keep the recommendation form throughout (no "we will" / "the plan is"; use "I'd recommend" / "one option is"). Do not write recommendations into repo docs in a tone that pre-commits the user. If the user later decides to commit, that commitment goes into an ADR, not back-edited into the proposal doc.
>
> *Grounded in: research-plan.md framing decisions (this session, 2026-05-14).*

### Why this earns its place in your agents file

The harness system prompt already says "present it as something the user can redirect, not a decided plan" for exploratory questions — but the temptation to over-confidently propose architectural directions is strong, and once a proposal lands in a repo doc with confident phrasing it accretes weight it didn't earn. In this session the recommendation to "collapse the four architectures to one" is genuinely speculative; if `research-plan.md` had phrased it as "Architecture v3 will collapse to one path" instead of "v3 likely collapses to one chosen path," that speculative call would now read as settled. The cost of the rule is choosing modal verbs deliberately; the benefit is that proposal docs and decision docs stay distinct — the latter are ADRs, the former are clearly marked as still-up-for-debate.

---

## Suggestion 3: Load deferred MCP tool schemas before promising the user you'll use them

### Proposed addition

> **Load before promising.** Before telling the user "yes, I'll do X" where X requires a deferred MCP tool (anything appearing only in a `<system-reminder>` deferred-tools list, not in the current functions block), call `ToolSearch` with `select:<tool_name>` to load its schema first. Otherwise the next turn is a tool-loading interruption between promise and delivery.
>
> *Grounded in: mcp__github__create_pull_request schema load between PR-request and PR-creation (this session, 2026-05-14).*

### Why this earns its place in your agents file

When the user said "yes, open pr" I had to call `ToolSearch` for `mcp__github__create_pull_request` before I could actually open the PR, because deferred MCP tools don't have schemas until ToolSearch fetches them. The user saw an extra "Tool loaded" turn between asking and getting the URL. It's a small friction but it'll happen on every PR/issue/comment operation unless the schema is pre-loaded earlier in the session. Cheap rule: when the user signals likely GitHub-MCP work ("create a PR", "comment on", "subscribe to"), pre-load schemas in the same turn as the verbal "on it." Cost is one extra tool call; benefit is the user doesn't see a mid-promise schema-load.

---

## Suggestion 4: Read INDEX.md + PLAN.md before answering structural questions about `research/`

### Proposed addition

> **Ground structural answers.** When the user asks how something in `research/` is organized — what lives where, which files supersede which, when a doc is updated — read `research/INDEX.md` and `research/PLAN.md` before answering. Both files exist precisely so the convention is documented; re-deriving from filenames is slower and more error-prone.
>
> *Grounded in: research-structure Q&A (this session, 2026-05-14).*

### Why this earns its place in your agents file

In this session the user asked about `/research` vs `/research/followup`, when `00-synthesis.md` is updated, and whether followups influence `/architectures`. The clean answers came directly from INDEX.md's "How to use this index" section and PLAN.md's "Repository layout" + "Round 3" sections. Without those, I'd have had to grep filenames and infer the convention — slower, and likely to miss things like "Round-3 Thread 12 was folded into `research/07-dark-factory.md` instead of getting its own followup file," which is documented in PLAN.md §12 but is invisible from filenames alone. Cost: two file reads at the start of a structural question. Benefit: answers cite the canonical doc instead of reconstructing it.
