# AGENTS.md suggestions — 2026-05-16-71

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Plan-file branch names win over session-bootstrap branch names

### Proposed addition

> **Plan-file branch names win.** When a fresh-agent plan file (e.g. `reorg-plan.md`, `migration-plan.md`, any numbered-step plan checked into the repo) specifies a branch name for the current step, that branch name takes precedence over the branch the session was bootstrapped on. Create or switch to the plan-specified branch before doing the step's work — even if the session-bootstrap branch is clean and off `main`. Rationale: the plan-file name is the durable identifier across resumed sessions; the bootstrap branch is session-ephemeral.
>
> *Grounded in: PR #71 — session was bootstrapped on `claude/execute-reference-step-one-FZ07O` but `reorg-plan.md` specified `claude/reference-only-step-1-categorize`. Followed the plan-file name and opened the PR from the plan-named branch.*

### Why this earns its place in your agents file

Multi-step plans (like `reference-only/reorg-plan.md` here, or any numbered-step migration plan) are resumable: a fresh agent two weeks from now reads the plan, looks at the "Branch: ..." line for the current step, and tries to find that branch on the remote. If a prior session opened the PR under the session-bootstrap branch name instead, that fresh agent now has to grep through PR history to figure out which branch actually carries the step's work. The cost of the rule is two seconds (`git checkout -b <plan-name>`); the cost of skipping it is up to half an hour of follow-up archaeology when a later session picks up the plan. Asymmetry is large enough that codifying the default is worth the line of agents-file real estate.

---

## Suggestion 2: Subject-matter is the default categorisation axis for curated citation corpora

### Proposed addition

> **Subject-matter, not medium, is the default categorisation axis for any curated citation corpus** (`/reference-only/`, `/sources/`, any folder whose purpose is "preserved primary material that reports cite"). Medium-based categories (books / essays / papers / transcripts / vendor-docs) make the *physical shape* of the corpus legible but obscure *why a reader would ever look here*. Subject-matter categories (e.g. `dark-factory-methodology`, `practitioner-harnesses`, `security-primitives`) map directly onto the topic-anchored questions a reader actually arrives with. Fall back to medium only when the corpus is a heterogeneous dump with no subject through-line.
>
> *Grounded in: PR #71 — first pass landed `books / essays / vendor-docs / academic-papers / podcast-transcripts / external-syntheses`; orchestrator rejected in favour of subject-matter; rework cost a full re-`git mv` cycle.*

### Why this earns its place in your agents file

The first pass on `/reference-only/` produced six perfectly-sized medium-based categories that the orchestrator immediately threw out. Reading the rejection one level deeper: a reader of `/reference-only/` is hunting for primary-source backing for a *claim about a topic*. They don't care whether the answer is a blog post or a podcast transcript — they want the topic content. Medium-based categorisation buries the navigation cue inside the medium and hides cross-cutter tension (e.g. the lenny-podcast-transcripts subdir spans `practitioner-harnesses` and `substrate-and-skills` — invisible under "all transcripts go in `podcast-transcripts/`"). Codifying subject-matter as the default saves the next agent the iteration cost we just paid; the rule has almost zero downside since the fall-back clause covers the legitimate medium case.

---

## Suggestion 3: On a directional redirect, propose options with preview content — don't re-execute on a guess

### Proposed addition

> **When the user's response is a short directional redirect** ("I wanted X instead", "go simpler", "this should be Y-based"), prefer `AskUserQuestion` with **two concrete options whose `preview` fields show the exact resulting structure** over (a) executing on your best guess at the redirect or (b) asking open-endedly "what did you mean?". The preview-content form lets the user confirm the *shape* of the answer in one click without writing prose. Skip this rule only when the redirect is unambiguous and the next step is mechanical (e.g. "rename foo to bar").
>
> *Grounded in: PR #71 — orchestrator said "I wanted the categories to be subject matter based"; recovery used `AskUserQuestion` with fine-grained (6-subject) vs coarser (4-subject) preview options showing the actual mapping of the 8 sources. User picked in one click, no further clarification needed.*

### Why this earns its place in your agents file

Short directional redirects are a recurrent failure mode: the user knows what they want, has minimal patience for re-explanation, and the agent has to make a guess or escalate. Open-ended "what did you mean?" pings cost a context-switch on the user's end and rarely close in one round. Best-guess execution risks a third iteration. The preview-content form of `AskUserQuestion` lets the user see the actual end state of each option and choose without typing — a single click closes the redirect. Marginal cost: writing two preview strings (5–10 minutes of agent time). Marginal benefit: avoids a third loop. This is the kind of pattern that a fresh agent won't reach for unless the agents file names it.

---

## Suggestion 4: When backfilling an inventory, `ls` the actual directory — don't trust a parent README's chapter / file count

### Proposed addition

> **When updating an inventory README based on a source's own local README, also `ls` the actual directory.** Parent-README claims about chapter count, file count, "what's outstanding" status, and similar disk-state assertions drift silently — chapters are added, transcripts are dropped, files are restored from git history. The local README is a *story* about the directory; only the directory itself is authoritative. Spot-fix any stale disk-state claims you find inline if it's a one-liner; otherwise flag them for a follow-up commit.
>
> *Grounded in: PR #71 — `el-kaim-book/README.md` claimed 7 chapters; disk had 9 (chapters 8 and 9 had been added in a later drop). Also: `lenny-podcast-transcripts/README.md` flagged the full Cherny transcript as "still outstanding" but `cherny-head-of-claude-code-full.txt` was already present.*

### Why this earns its place in your agents file

The `el-kaim-book` chapter-count drift only got caught because the backfill row needed an accurate chapter count — if the README update had just copied the existing row's text, the stale claim would have been re-emitted on every future commit, and downstream reports counting "El Kaim's 7 chapters" would have stayed wrong. The cost of the rule is one extra `ls` per source row (literally seconds). The cost of skipping it is the propagation of stale facts into the citation graph. The "spot-fix or flag" clause keeps the rule from ballooning the scope of a backfill commit.

---

## Suggestion 5: Before/after `find` diff is the canonical verification for any multi-source `git mv` reorg

### Proposed addition

> **For any multi-source `git mv` reorg, capture `find <root> -type f -not -path '*/.*' | sort` before and after the moves, then `comm` the two lists.** Every "before" path must appear renamed in "after"; "after" must have no new paths other than intentional additions; no duplicates may appear across destination directories. This is more reliable than `git status` for catching accidental skips or duplications, because it works on the raw filesystem and survives multiple rounds of moves (e.g. an initial reorg + a rework on the same branch).
>
> *Grounded in: PR #71 — verified both the medium-based first pass (29 source files moved + 32-entry tree match) and the subject-matter rework (same files re-moved a second time, 32-entry tree match against the *original* pre-anything state, not just against the intermediate post-first-pass state). Confirmed no source ended up under two category directories.*

### Why this earns its place in your agents file

`git status` shows you what's staged; it doesn't tell you whether the on-disk tree is the one you intended. For a multi-source reorg with intermediate iterations, the right invariant is "every original file is accounted for exactly once at a new path" — and that invariant is testable in two lines of `find | sort | comm`. The verification ran twice on PR #71 (once after each reorg) and caught both: the first run confirmed the original moves were complete, the second confirmed the rework didn't lose anything to the intermediate medium-named directories before they were `rmdir`'d. Without the rule, an agent might `rmdir` an "empty" directory that actually still had a stray file and silently delete data. The rule's cost is two `find` captures + a `comm`. The cost of skipping is silent data loss.

---

## Suggestion 6: PR description gets *rewritten* on a same-branch rework, not appended to

### Proposed addition

> **When you rework a PR's underlying approach on the same branch** (rather than opening a fresh PR), **fully rewrite the PR description to describe the final state**, not the original state plus an "update" addendum. Prefix the body with one short note ("Update YYYY-MM-DD: first pass was X; orchestrator asked for Y; description below reflects final state.") so a reviewer with a stale tab can recognise the pivot, but make the body itself describe only the post-rework state. Do not preserve the original description's structure underneath.
>
> *Grounded in: PR #71 — initial body described medium-based categorisation; after the orchestrator redirect, the body was wholly replaced with the subject-matter version. Resulting body reads as if a single coherent plan landed in one go (with the pivot note at the top giving the historical context).*

### Why this earns its place in your agents file

Stratified PR descriptions ("Original plan: X; Update: actually Y; Update 2: …") force reviewers to mentally reconstruct the current state from a stack of revisions. They also drift faster than mono-state descriptions because each update layer has its own staleness lifecycle. A reviewer arriving cold on PR #71 reads "the PR does the subject-matter categorisation, here's the table, here's the test plan" — exactly the model they need to do the review. The pivot note at the top costs one sentence and serves the legitimate audit need without polluting the main description. Rule cost: one rewrite per pivot. Skip cost: every reviewer mentally diff-applies the update layers.

---

## Suggestion 7: Auto-subscribe webhook discharges the manual subscribe action — don't re-call as a no-op

### Proposed addition

> **If the PR-creation flow auto-subscribes the session** (recognisable by the immediate `<github-webhook-activity>` "You are now subscribed to PR activity" message after `mcp__github__create_pull_request`), **do not call `mcp__github__subscribe_pr_activity` again as a "closing action"**. The closing action is satisfied. Note the auto-subscription in the user-facing summary so they can audit that subscription is in place, but a second call is a no-op that obscures whether the original subscription took.
>
> *Grounded in: PR #71 — the create-PR flow triggered an immediate auto-subscribe webhook; manual subscribe-call from the plan's closing actions would have been an idempotent no-op.*

### Why this earns its place in your agents file

The plan's closing actions list "subscribe to PR activity" as a discrete step, which created ambiguity about whether to call `subscribe_pr_activity` even when a webhook had already announced subscription. The cleaner pattern is to treat auto-subscription as the *fulfilment* of the closing action, not as a redundant signal to ignore. Cost of the rule: zero (it just removes a step in some cases). Benefit: clarifies the contract between the closing-action checklist and the webhook stream, and saves one tool call per PR creation. Mark this rule as conditional ("if the webhook arrived") so plans that don't auto-subscribe still get the explicit subscribe call.
