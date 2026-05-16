# AGENTS.md suggestions — 2026-05-16-67

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for adopting it, grounded in something that happened (or nearly happened) in PR #67.

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Forward-allocate report numbers in an orchestrator-decisions table

### Proposed addition

> **Forward-allocate report numbers before dispatching subagents.** When a drain creates more than one new numbered report, pre-allocate the numbers (e.g. "27, 28, 29, ...") in an orchestrator-decisions table at the top of the index file, and commit that decision before dispatching any subagent. Each subagent brief must cite the pre-allocated number for its target report. Subagents must NOT pick their own report number.
>
> *Grounded in: PR #67 — the 13-cluster Round-10 drain reserved reports 27–37 in an orchestrator-decisions table, and zero subagents collided on numbering.*

### Why this earns its place in your agents file

The drain created 11 new numbered reports. Without forward-allocation, two parallel subagents would pick the same next-available number; with serial subagents (this drain's pattern), the second one would silently overwrite the first's INDEX row. Forward-allocation costs ~5 minutes of orchestrator decision work and eliminates the entire failure class. The marginal alternative — a shared lock file or post-hoc renumbering — adds far more friction.

---

## Suggestion 2: Commit + PLAN.md update after every subagent return

### Proposed addition

> **One commit, one PLAN update, per subagent return.** Never batch multiple cluster outputs into a single commit. After a subagent returns, (a) run `git status --short` and `git diff --stat` to verify the change scope, (b) update the in-progress checklist in `PLAN.md` (flip the cluster checkbox + inline 3–8 surprises from the subagent's change report), (c) commit with a multi-line message capturing the surprises in the body, (d) push. Only then dispatch the next subagent.
>
> *Grounded in: PR #67 — 13 cluster commits became the PR's reviewable audit trail.*

### Why this earns its place in your agents file

If a session terminates mid-drain (network blip, context exhaustion, manual interrupt), batched-commit state is unrecoverable; per-cluster commits resume cleanly. The PR reviewer also benefits: each commit's diff matches the cluster's brief. Marginal cost: ~30 seconds of orchestrator time per cluster. Cost of the alternative (one giant commit at end): unbounded recovery work after any failure.

---

## Suggestion 3: Verify subagent claims against `git diff` before committing

### Proposed addition

> **Trust but verify subagent change reports.** Before committing a subagent's work, run `git status --short` and `git diff --stat HEAD` to verify the actual change scope matches the deliverable claim. Subagents sometimes claim "already present" when their diff says +176 lines, and sometimes claim "comprehensive update" when only one file changed. The diff is authoritative; the prose is not.
>
> *Grounded in: PR #67 Cluster E — subagent claimed §4.3 / §4.4 were "already present pre-edit" but the diff showed +176 lines of new content. Cluster F's subagent then caught the *real* drift — an earlier indexing pass had forward-edited the sources table to claim Cluster F was already complete while leaving §1 prose / §5 author / §7 follow-up list / §8 verdict in mirror-era form.*

### Why this earns its place in your agents file

The Cluster F subagent caught an actual sources-table-vs-prose drift that would have shipped to the PR as silent misinformation. The verification check is 2 tool calls per cluster. The cost of missing one drift is a refutation in the next cluster's PR (or worse, in the final synthesis).

---

## Suggestion 4: Cross-section drift check on multi-section subagent edits

### Proposed addition

> **Run a top-to-bottom re-read on any subagent edit that touched ≥5 sections of a long-lived document** (PLAN.md, INDEX.md, a multi-thousand-word report). Use the `post-edit-reread-pass` skill. The dominant failure mode is a sources table updated to claim primary-anchored status while the prose body still reads in `🟡 mirror-era` voice.
>
> *Grounded in: PR #67 Cluster F — the prior pass updated only the sources table; §1 / §5 / §7 / §8 of report 18 stayed mirror-era for an entire cluster cycle until Cluster F's primary-text drain caught it.*

### Why this earns its place in your agents file

The check costs one Read call per affected file. The alternative is misinformation propagating until the *next* cluster catches it (which it might not, if no later cluster touches the same file). The Cluster F catch was lucky, not structural.

---

## Suggestion 5: `mhtml_extract.py` is at `.claude/skills/research-pipeline/scripts/`, not `scripts/`

### Proposed addition

> **The MHTML extractor's canonical path is `.claude/skills/research-pipeline/scripts/mhtml_extract.py`.** When briefing a subagent to extract MHTML images, include the full path. The `scripts/` top-level directory does NOT contain this script; cite the right path in every brief.
>
> *Grounded in: PR #67 Cluster H — a subagent reported it could not find `scripts/mhtml_extract.py`; the correct path is under `.claude/skills/research-pipeline/scripts/`.*

### Why this earns its place in your agents file

One wrong path costs a subagent a turn (Bash failure, recovery, re-dispatch). Document the canonical path once; every subagent brief inherits the fix.

---

## Suggestion 6: `mhtml_extract.py info` and `save-image` index bases are inconsistent — call out the off-by-one in every brief

### Proposed addition

> **`mhtml_extract.py info` reports 1-based image indices; `save-image` consumes 0-based.** This is a real defect in the script (see retrospective `2026-05-16-67/mhtml-image-extract-fix-spec.md`). Until fixed, every subagent brief that does MHTML image extraction must explicitly call out the off-by-one and suggest verifying the saved file against the `info` output (e.g. check `file <out>.png` reports the expected dimensions).
>
> *Grounded in: PR #67 Cluster C — saved files had mismatched sizes vs `info` claims until the off-by-one was identified.*

### Why this earns its place in your agents file

Same trap, hit in Clusters C, H, L. Cost of the rule: one extra sentence in the subagent brief. Cost of missing it: an entire subagent turn wasted on wrong images, often caught only when the figure caption doesn't match the embedded image.

---

## Suggestion 7: MHTML embedded images may be AVIF-bytes-inside-`.png` — convert via Pillow

### Proposed addition

> **MHTML embedded images sometimes carry AVIF bytes in a file with a `.png` extension.** After `save-image`, verify the saved file is the format you expect (`file <path>` is the canonical check). If the bytes are AVIF, decode with Pillow (`pip install pillow-avif-plugin`) and re-save as true PNG before embedding in any report.
>
> *Grounded in: PR #67 Cluster H — the Replit App Monitoring image came back as AVIF inside `.png`; Pillow conversion was required before the figure could be embedded.*

### Why this earns its place in your agents file

Markdown renderers that don't speak AVIF will render a broken-image icon in the report. The Pillow conversion is two lines of Python. The alternative is a silent rendering failure that the reviewer notices later.

---

## Suggestion 8: Failure-mode numbering is strictly sequential — never reuse

### Proposed addition

> **F-numbers (failure-mode identifiers) are strictly globally sequential.** Before promoting a new F-mode, grep all `research/**/*.md` for the highest existing F-number and pick the next one. If two reports have already collided on the same F-number (e.g. F36 in both report 25 and report 26 — flagged in `research/PLAN.md` §3.6), pick an F-number above both to avoid further collision. The pending triage on the existing collision is a separate task; do NOT add to the problem.
>
> *Grounded in: PR #67 — F40 through F49 were promoted, deliberately starting at F40 to avoid the F36/F37 collision flagged in PLAN.md §3.6 since Round-9.*

### Why this earns its place in your agents file

Failure-mode references will become load-bearing cross-corpus links if the corpus is to do any synthesis work; collisions break that. The grep cost is one Bash call per F-mode promotion. The lead-agent triage on the existing F36/F37 collision is a separate task — this rule just prevents recurrence.
