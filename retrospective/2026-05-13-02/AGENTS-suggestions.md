# AGENTS.md suggestions — 2026-05-13-02

These are proposed additions to the project's agents file (typically
`AGENTS.md` at the repo root, currently does not exist for this repo —
the retrospective from 2026-05-11-01 also flagged this gap). Each
section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for
   doing it, grounded in something that happened in this session.

Decide each on its own merits. Skip ones that don't apply to your
operating posture; copy-paste the ones that do.

---

## Suggestion 1: Always open a PR when stopping with significant pending work

### Proposed addition

> **Always open a PR when stopping with significant pending work.** If a feature branch has been pushed with commits beyond what's currently in any open PR, open (or update) a PR before ending your turn. Don't ask "want me to open it?" — just open it. Significant pending work = anything beyond a one-line typo fix.
>
> *Grounded in: 2026-05-13 session; user feedback "you should never stop without doing a PR! make a PR for fuck's sake."*

### Why this earns its place in your agents file

Mid-session, after drain phase A and B, I had pushed 8 commits to `claude/implement-drain-qlhhT` after PR #37 was merged — a clean, mergeable state, with real value (Chapter 8 + 9 drains, round-7 drain) — but stopped at "want me to open it?" The user had to interrupt to say to just do it. The cost of not having this rule: a session-ending pause that requires the user to come back, pick up the loose end, and prompt again. The marginal cost of adopting the rule: zero, since the PR-opening tool call is fast and the alternative (an unowned pile of pushed commits) is strictly worse for the user's mental model.

---

## Suggestion 2: Never trust the model's notion of today's date — verify via `date -u`

### Proposed addition

> **Never trust the model's notion of today's date.** When a workflow embeds the date in a filename, commit message, or report (retrospectives, ADRs, blocked-urls-round-N.md files), verify via `date -u +%Y-%m-%d` before writing. Cross-check with `python3 -c "import datetime; print(datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d'))"` if both shells are available.
>
> *Grounded in: `self-retrospective` skill's Step 0 mandatory tool call; also matches the prior 2026-05-11-01 retrospective's identified discipline.*

### Why this earns its place in your agents file

Date drift in filenames silently breaks day-sequencing — a retrospective written on 2026-05-13 but filenamed 2026-05-12-XX would land BEFORE the 2026-05-13-01 file already on disk and cause confusion later when someone reads the timeline. The marginal cost of verifying is one shell call. The cost of not verifying is non-zero (model's "today's date" may be stale by hours or wrong by days). This is the cheapest discipline in the entire AGENTS.md.

---

## Suggestion 3: When a drain refutes a prior corpus claim, grep for every propagation site before committing

### Proposed addition

> **Cross-corpus refutation propagation.** When a primary-source drain refutes or amends a claim already in the corpus, run `grep -niE` for the refuted framing across `research/*.md research/followup/*.md research/blocked-urls*.md architectures/*.md` BEFORE committing the drain. Apply trivial swaps inline; surface narrative inversions to the user for editorial judgement; mark audit-trail entries with strikethrough + reversal annotation (do NOT delete them).
>
> *Grounded in: 2026-05-13 "4 agents → 11 AM" reversal-of-reversal; 12 propagation sites across 3 files; would have stayed wrong if not swept in one pass.*

### Why this earns its place in your agents file

The Lenny × Willison transcript drain established that "Simon runs 4 agents in parallel and is exhausted by 11 AM" is verbatim-correct. A prior round had "corrected" the claim, calling the count a fabrication; that correction propagated to 12 places across 3 files. Without the cross-corpus sweep, the corpus would contain two contradictory framings of the same fact — and the wrong (fabricated-was-fabricated) one would silently outnumber the right one. The marginal cost of the sweep is one `grep`. The cost of not doing it is: every future agent reading the corpus inherits the older, wrong framing in 7 places and the newer, right one in 1.

---

## Suggestion 4: 200-OK with `Loading...` placeholders is not content (JS-SPA detection)

### Proposed addition

> **JS-SPA detection.** After a fetch action returns, spot-check each body before draining. If the markdown extract contains repeated `Loading...` placeholders, or if multiple URLs from the same domain produce extracts of *exactly* the same byte size, the page is a JS-rendered SPA — the curl-based fetch action cannot execute the JavaScript that renders the body. Classify as ❌ in the blocked-urls table and escalate to Path B (user Save-Page-As after JS renders).
>
> *Grounded in: 2026-05-13 issue #36, `platform.claude.com/docs/en/agent-skills/{overview,best-practices,security}` — all three returned HTTP 200 with bodies of exactly 505 KB raw / 143 lines of markdown extract, and the markdown was nav chrome plus ~17 `Loading...` placeholders.*

### Why this earns its place in your agents file

`platform.claude.com/docs/*` is a JS-rendered SPA. So is `developers.openai.com/docs/*` (probably). Without this check, an action-fetch will return 200 OK, the drain subagent will read 143 lines of placeholder text, hallucinate content from the surrounding context, and confidently produce a refutation-laden report. The marginal cost of the check: one `head -50` and one `wc -l` per fetched file. The cost of not checking: confabulated drain output that needs to be reversed.

---

## Suggestion 5: Action-reachability re-testing before classifying a host as Path B-only

### Proposed addition

> **Re-test action-reachability before classifying as Path B.** Before flagging a URL as "Path B only" or "Cloudflare-blocked," file an action-fetch first. The GitHub Actions runner IP space is different from the sandbox IP space; many hosts that 403 the sandbox return 200 from the runner. Re-test any host whose "blocked" classification is more than two rounds old.
>
> *Grounded in: round-6 lesson; round-7 confirmed when 9 hosts previously tagged "Cloudflare-only" all returned HTTP 200 from the action runner (`simonwillison.net`, `hamel.dev`, `anthropic.com/engineering`, `arxiv.org/abs`, `danshapiro.com`, `devin.ai`, `factory.ai`, `8090.inc`, `blog.fsck.com`).*

### Why this earns its place in your agents file

Stale classifications are how the corpus accumulates technical debt. Round 5's `blocked-urls.md` v5 tagged most of those 9 hosts as "Path B only" — based on a single sandbox `WebFetch` test from one prior agent. Round 6 found that almost every one was action-reachable; round 7 confirmed. The marginal cost of one action-fetch issue (action runs in 1–2 min) is much less than the cost of asking the user to manually Save-Page-As a dozen URLs. This rule alone has un-blocked >30 URLs in the corpus.

---

## Suggestion 6: 404 from same domain that also returned 200 = URL-specific (moved/typo), not domain-blocked

### Proposed addition

> **404 ≠ block.** When an action-fetch returns 404 for some URLs but 200 for others on the same domain in the same fetch issue, the 404 is URL-specific — page moved, slug typo, or docs reorganization — not a domain-level block. (a) Read sibling pages from the successful 200s for cross-links to the missing target. (b) Run a WebSearch for the new canonical path. (c) Re-file a follow-up fetch with the corrected URL.
>
> *Grounded in: 2026-05-13 issue #29 Shapiro slug-guess miss (correct slug discovered in companion-post sidebar); issue #30 6 GH Copilot 404s (GH docs reorganized — all 6 had new canonical paths surfaced via one WebSearch); issue #31 3 competitor 404s (URLs simply moved within still-live sites).*

### Why this earns its place in your agents file

In two of three round-7 fetch issues, every 404 was a moved/renamed URL on a still-reachable host. The pattern is fixable, but only if recognized. Default behavior of treating 404 as "this URL is dead, drop it" is wrong about 80% of the time. Marginal cost of the recovery: read one sibling page or run one WebSearch. Cost of not doing it: 5 corpus claims permanently flagged `[pending re-anchor]` for no reason.

---

## Suggestion 7: One subagent per target file; orchestrator handles cross-cutting updates

### Proposed addition

> **Subagent dispatch convention.** When dispatching parallel subagents to drain or update reports, give each subagent exactly one target report. If a drain produces cross-cutting updates (e.g., a finding that affects multiple reports, or a status flip that needs to propagate to `INDEX.md` and `PLAN.md`), the *orchestrator* applies them inline post-merge — not the subagents. Tell each subagent explicitly: "Don't touch <files outside your target>; surface cross-references as a list in your report-back."
>
> *Grounded in: 2026-05-13 phases A, B, C, D — 11 parallel subagents across 4 drain rounds, 0 merge conflicts; cross-cutting updates (report 06-hn-and-lenny, INDEX, PLAN) all applied orchestrator-side without coordination friction.*

### Why this earns its place in your agents file

The convention prevented 11 potential edit conflicts across 4 drain rounds. If two parallel drains had both tried to update `research/06-hn-and-lenny.md` (Cherny drain wanting to add a section + Willison drain wanting the same), the second commit would have rejected the first. Marginal cost: one extra sentence in each subagent brief. Cost of not having it: a midnight merge conflict and a lost drain.

---

## Suggestion 8: Orchestrator sweeps subagent intermediate files before committing

### Proposed addition

> **Subagent intermediate file sweep.** After parallel subagents return, run `find research/manual/ -type f -newer <session-start>` (and similar globs for other write directories). Classify each file: intermediate (delete), primary source (move to `reference-only/<topic>/`), drain output (keep), failure evidence (keep), unknown (flag). Subagent briefs cannot reliably specify "delete these intermediates" because the intermediates are produced ad-hoc by the subagent's extraction tooling.
>
> *Grounded in: 2026-05-13 Phase D Anthropic Skills drain — subagent left 6 intermediate files (`.extracted.txt`, `.txt` flattened renders of `.ipynb` notebooks) in `research/manual/`; orchestrator had to clean them up by hand.*

### Why this earns its place in your agents file

`research/manual/` is documented as a transient drop-zone — non-empty after a drain signals unfinished work. Without the orchestrator sweep, drains routinely leave 4-8 intermediate files behind. A future agent reading the directory after the drain commits sees a non-empty drop-zone and thinks there's more drain work to do. The marginal cost of the sweep: one `find` + a few `git rm`. The cost of not doing it: 5 minutes of confusion per future-agent visit + a stale `manual/` directory polluting the workspace.

---

## Suggestion 9: Read small files in full — they often contain large information

### Proposed addition

> **Small files can be high-leverage.** A 5-KB profile page, a 2-KB README, an index page that looks like nav chrome — read them fully before classifying as transient. Author profile pages often surface lists of unread sibling content; READMEs often state lifecycle conventions the orchestrator hasn't internalized; index pages often surface URLs the corpus needs but hasn't seen.
>
> *Grounded in: 2026-05-13 Phase B — `welkaim.medium.com` post-index page (5.9 KB, looked like nav chrome) was almost classified as "trivial bio metadata"; on full read it revealed 10+ unread El Kaim posts (including LeanIX governance series + Cyrano prompting method + Vibes-to-Codex-to-Claw), now logged as a future-research cluster in PLAN.md.*

### Why this earns its place in your agents file

The default classification of small files as "transient" because they're small is wrong about as often as it's right. Marginal cost of reading a 5 KB file: ~5 seconds. Cost of misclassifying: losing pointers to ~10 unread primary sources that surface only on a full read.

---

## Suggestion 10: When MCP is intermittent, stage external actions as paste-ready markdown files

### Proposed addition

> **MCP resilience: stage paste-ready files.** When a tool depending on an MCP server may be intermittent (GitHub MCP, Notion MCP), and you need to invoke that tool, write a paste-ready markdown file with the exact request body in addition to (or instead of) calling the tool directly. The user can paste the staged body manually if the MCP is unavailable, and a future MCP-connected session can pick up from the staged file.
>
> *Grounded in: 2026-05-13 GitHub MCP disconnected twice mid-session; resolution was to stage `research/next-fetch-batch.md` with the full issue body — user could have pasted manually, and when MCP reconnected I filed the issue myself from the staged content. Zero-cost fallback.*

### Why this earns its place in your agents file

External MCPs disconnect and reconnect unpredictably. Without the staged-file fallback, the session has to wait for reconnection (or for the user) before progressing. With it, the user has full information in a paste-ready form regardless of MCP state. Marginal cost: writing the file (which is mostly the content you'd send to the MCP anyway). Cost of not doing it: a session that stalls on MCP outage, or that the user has to clean up after.
