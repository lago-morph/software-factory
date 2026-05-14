# AGENTS.md suggestions — 2026-05-14-01

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened in the 2026-05-14 drain session.

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Body-inspect every fetched file before declaring success

### Proposed addition

> **Body-inspect fetched files.** "HTTP 200 from the fetch-blocked-urls action does NOT mean the fetch succeeded. Before feeding any file from `research/fetched/issue-<N>/` to a drain subagent, inspect its `<title>`, run `wc -c`, run `file <path>`, and grep its body for stub markers: `Just a moment`, `Enable JavaScript and cookies to continue`, `404`, `Not Found`, `Page not found`, `Loading...`. If any of those appear — or if `file` reports `gzip compressed data` or `PDF document` instead of HTML — the file is a stub or a binary mis-extraction, not real content. Record the outcome in `research/blocked-urls-round-<N>.md` and `git rm` the stub. Never pass an unverified file to a subagent."
>
> *Grounded in: the 2026-05-14 round-8 drain identified 4 Cloudflare JS-challenge stubs in `fetched/issue-41/` and 1 gzip mis-extraction (the CaMeL paper) in `fetched/issue-42/` — all returning HTTP 200.*

### Why this earns its place in your agents file

The fetch-blocked-urls workflow has zero awareness of body-class failures. It writes whatever curl returned. Three previous rounds of drains in this repo have each separately discovered Cloudflare JS-challenge stubs by feeding them to a subagent that then spent tokens telling the orchestrator "this file has no content." Each instance cost roughly 5–10K subagent tokens; across rounds the cumulative waste exceeds the marginal cost of a 30-second pre-drain inspection pass.

More importantly, the 2026-05-14 round-8 drain found the arXiv CaMeL paper body via a gzip mis-extraction that *no status-code check would catch*. The fetch action saved the gzipped LaTeX tarball under a `.html` extension. The body-inspection rule (`file <path>` rather than trust-the-extension) surfaced this as a recoverable failure rather than an unrecoverable one — and a paper body that round-7 had documented as "accept the gap" was suddenly recoverable in minutes.

The marginal cost of the rule is one `file` invocation and one `grep` per fetched file. The marginal benefit, demonstrated three times in three rounds, is multiple subagent dispatches saved per drain.

---

## Suggestion 2: Never merge a workflow drop-branch directly

### Proposed addition

> **Workflow drop-branches are cherry-picked, not merged.** "The `fetched/issue-N` branches created by `.github/workflows/fetch-blocked-urls.yml` are forked from whatever `main` was when the workflow ran, which may be days or weeks behind current `main`. A direct merge of a workflow drop-branch into a feature branch will re-introduce already-removed content and re-delete recently-added files. Always cherry-pick only the workflow's namespace: `git checkout origin/fetched/issue-N -- research/fetched/issue-N/`. Never `git merge` a `fetched/issue-N` branch."
>
> *Grounded in: in the 2026-05-14 round-8 drain, the `fetched/issue-41` and `fetched/issue-42` branches were forked from a `main` commit that predated PR #43; a direct merge would have re-deleted `user-next-steps.md` and `research/next-fetch-batch.md`.*

### Why this earns its place in your agents file

The fetch-action's branch-creation contract is "snapshot main + add fetched files." It is NOT "rebase onto current main." For a feature branch that has moved on, this is a destructive merge waiting to happen, and the destruction is silent — git will happily complete the merge with no conflicts because nothing on the feature branch conflicts with the workflow's old-main view.

The cherry-pick recipe (`git checkout origin/fetched/issue-N -- research/fetched/issue-N/`) is one command. Every drain round in this repo will face this issue; making it a standing rule avoids re-discovering it. The asymmetry: zero cost to follow the rule, multi-hour recovery cost if the destructive merge lands and isn't caught for a few commits.

---

## Suggestion 3: Diff modified files at the byte level before declaring a branch safe to delete

### Proposed addition

> **Before deleting a branch, hash-compare its modified files against main.** "When auditing whether a branch is safe to delete, do not trust commit messages or diff-stat output. For each file the branch modifies, compute `sha256sum` of the file on the branch and on main; only if they match (or if the branch's version is strictly older with no unique content) is the branch safe. Specifically: `bh=$(git show origin/<branch>:<path> | sha256sum); mh=$(git show origin/main:<path> | sha256sum); diff <(echo $bh) <(echo $mh)`. Do this for every NEW or MODIFIED file in the branch's diff."
>
> *Grounded in: the 2026-05-14 audit of `claude/drain-issue36-extras` — the branch's commit was titled "Fix report 07 source table: welkaim profile rows resolved 2026-05-13" but the fix was already on main via a different commit; merging the branch would have reverted other work.*

### Why this earns its place in your agents file

Commit messages are aspirational; diffs are factual. A branch with one commit whose message sounds valuable can still be net-destructive — especially if the "valuable" change has already arrived on main via a different route (squash-merge, cherry-pick, or hand-applied edit). Without byte-level verification, the audit reduces to "trust the commit message," which is the same as not auditing.

The hash compare costs two git invocations per modified file. A typical post-merge branch audit covers 5–10 branches with 5–10 modified files each; total cost is seconds. The cost of getting it wrong — merging a destructive branch and not catching it until later commits build on the regression — is hours to days.

---

## Suggestion 4: Drain subagents commit no code; the orchestrator batches

### Proposed addition

> **Drain subagents do not commit.** "A subagent dispatched to drain a fetched source into a research report MUST NOT call `git commit` or `git push`. The orchestrator (lead agent) is solely responsible for committing the consolidated drain outputs. Subagents may `git rm` consumed fetched files (those deletions are part of the disposition the orchestrator will commit). Subagents return a structured report — files modified, sections updated, findings — and the orchestrator integrates that into one commit per drain round (or one commit per disjoint logical unit). This avoids partial-state commits, conflict cascades from parallel subagents, and missed bookkeeping (INDEX.md, PLAN.md, blocked-urls-round-N.md)."
>
> *Grounded in: the 2026-05-14 round-8 drain dispatched 4 subagents in parallel (Replit, OpenAI Codex, GH Copilot, CaMeL); all 4 modified disjoint reports + `git rm`'d their consumed files; the orchestrator committed once with INDEX/PLAN/blocked-urls updates folded in.*

### Why this earns its place in your agents file

The structure makes the drain idempotent and reviewable. If a subagent's work is rejected on review, the orchestrator can discard it; if subagents committed independently, rolling back one would mean rewriting history. Centralizing the commit also means INDEX.md, PLAN.md, and the round-N blocked-urls log can be updated to reflect the FINAL state, not intermediate states. Reviewers see one commit per drain round with a clear blast radius.

The marginal cost of the rule is that the orchestrator must wait for all subagents before committing — but the orchestrator was waiting anyway. The marginal benefit is one of the cleanest commit histories possible for this kind of work.

---

## Suggestion 5: End the turn after dispatching parallel subagents

### Proposed addition

> **End the turn after dispatching parallel subagents.** "When dispatching multiple subagents in a single message (e.g. via parallel `Agent` tool calls), end the message after the dispatch. Do not begin working on overlapping content while subagents are running. The orchestrator's job during subagent execution is to wait for completion notifications, not to make speculative progress on the same files. After all subagents return, consolidate their outputs into one commit."
>
> *Grounded in: the 2026-05-14 round-8 drain dispatched 4 subagents in parallel; the orchestrator deliberately ended the turn and consolidated only after all 4 completion notifications arrived. Conversely, in earlier rounds, attempting to update INDEX.md while subagents modified reports led to merge conflicts.*

### Why this earns its place in your agents file

Parallel-subagent fanout is one of the highest-leverage patterns for drain-style work — independent reports updated concurrently with no merge conflicts. The pattern only works if the orchestrator respects the boundaries: each subagent owns a disjoint set of files, and the orchestrator owns the consolidation. Mixing the two roles loses the parallelism benefit and creates conflict cleanup work.

The rule also signals the right rhythm to the user: "I dispatched N subagents; I'll consolidate when they all return." This is calmer than mid-flight narration and harder to get wrong.

---

## Suggestion 6: Always extract via `gunzip | tar -xf` when an arXiv `/e-print/` file is in scope

### Proposed addition

> **arXiv `/e-print/<id>` is the gold-standard recovery route for paper bodies.** "When an arXiv paper's `/html/<id>v<v>` URL returns 404 and `/pdf/<id>` returns a binary that html2text can't read, fetch `arxiv.org/e-print/<id>` and process it as a gzipped tarball. The fetch action will misclassify the response as `.html` and html2text will produce binary noise as the `.md` — both must be ignored. Instead, `cp` the `.html` (it's actually gzip), `gunzip` it, `tar -xf` the resulting archive, and copy the relevant `.tex` + `.bbl` files into `reference-only/<paper-slug>/` with a `README.md`. The LaTeX source IS the paper body — the most authoritative content arXiv exposes."
>
> *Grounded in: the 2026-05-14 round-8 drain recovered the CaMeL paper body via this route after round-7 had documented it as "accept the gap."*

### Why this earns its place in your agents file

Without this rule, the project's default behavior on an arXiv paper-body gap is "accept the gap; the abstract and any sympathetic writeup are enough" — which round 7 explicitly logged for the CaMeL paper. Round 8 demonstrated that the gap was never necessary: 4 shell commands recover the LaTeX source, which is then primary-source-anchorable. Anchoring `research/followup/08-security-primitives.md` §3 to the paper body grew that section from 7 to ~15 subsections with verbatim quotes — a substantial uplift in evidence quality for a single security claim.

The rule also forecloses the asymmetric mistake: accepting a gap that is, in fact, recoverable. The cost of trying the route is ~30 seconds; the cost of skipping it can be a load-bearing claim left under-evidenced for the life of the report.

---

## Suggestion 7: When a `<title>` is set by JavaScript, trust the body not the title

### Proposed addition

> **Title-checks are insufficient for SPA pages.** "Modern Single Page Application pages (Next.js, React, etc.) set `<title>` via JavaScript before the body finishes loading. A fetched page can have `<title>Factory.ai</title>` while its body says 'These are not the droids you are looking for...' — a 404 in cosplay. When inspecting fetched files, always check the body for stub markers in addition to the title. Specifically: render via html2text (or visible-text-only via a regex strip) and read at least the first 500 chars before classifying a fetch as successful."
>
> *Grounded in: the 2026-05-14 round-8 drain found `factory.ai/product` with `<title>Factory.ai</title>` but body "These are not the droids you are looking for..." — a 404 stub whose title would have passed a title-only check.*

### Why this earns its place in your agents file

This is a specialization of Suggestion 1 ("body-inspect every fetched file") but the SPA case deserves its own callout because the failure mode is non-obvious: an engineer who has spent the morning telling Cloudflare stubs apart from real pages by their title (`Just a moment...` vs `Real Title — Real Site`) will pattern-match `Factory.ai` as a real title and move on. The rule says: don't.

The marginal cost is reading a few extra lines per file. The marginal benefit is catching the SPA-mock-success class of failure, which Suggestion 1 alone won't.
