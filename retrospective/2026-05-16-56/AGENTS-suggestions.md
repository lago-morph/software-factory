# AGENTS.md suggestions — 2026-05-16-56

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

The project still has no `AGENTS.md` file. Cumulative backlog across this and prior retrospectives is 45+ suggestions (per PLAN.md §3.4); the four below are net-new from session 2026-05-16-56.

---

## Suggestion 1: Honor lifecycle READMEs in transient drop-zone directories

### Proposed addition

> **Transient drop-zone READMEs are authoritative.** Before deleting, moving, or "cleaning up" any file in a drop-zone directory (e.g., `research/manual/`, `inbox/`, `staging/`), read the directory's `README.md` if one exists. The README specifies the file's lifecycle — including whether consumed files should be `git rm`'d outright or `git mv`'d to a permanent reference location. Do not infer the disposition from the file's apparent role; follow the README.
>
> *Grounded in: 2026-05-16 Lenny-transcript drain — `research/manual/README.md` mandated `git mv` to `/reference-only/lenny-podcast-transcripts/`, not `git rm`. A subagent that defaulted to `git rm` (the Phase-9 default in the research-pipeline skill) would have destroyed the canonical primary-source preservation.*

### Why this earns its place in your agents file

The research-pipeline skill's Phase 9 says to `git rm` consumed fetched files. The `research/manual/README.md` *contradicts* that default for primary-source manual drops, saying the orchestrator may move to `/reference-only/` instead. A subagent dispatched with only the Phase-9 default would have deleted a 102 KB primary-source transcript whose retention was the difference between a re-quotable canonical reference and a citation-only reference that decays as the corpus drifts. The marginal cost of the rule is one `ls + Read` per drain pass (the README is in the same directory you're already inventorying). The cost of getting it wrong is a permanently lost primary source, recoverable only by re-transcribing the YouTube video.

---

## Suggestion 2: Parallel subagents on the same source need file-boundary scoping

### Proposed addition

> **When dispatching parallel subagents that share an input source, partition by output file.** Each subagent's brief must explicitly name the file(s) it owns and the file(s) it must NOT touch. State the partition in the brief; do not rely on tacit non-overlap. Same-file edits from concurrent subagents produce merge conflicts that are expensive to diagnose because the conflict surface is the same source the agents were trying to summarize.
>
> *Grounded in: 2026-05-16 Cherny drain — two `general-purpose` subagents read the same 102 KB transcript. Subagent A owned `research/followup/03-cherny-interview.md` + the source-file move; subagent B owned `research/06-hn-and-lenny.md` with an explicit "do NOT touch followup/03" instruction. Zero merge conflicts; both edits applied cleanly in the same commit.*

### Why this earns its place in your agents file

The subagent-prompting skill already covers brief composition, but it doesn't make file-boundary scoping mandatory for shared-input fanouts. This session's two-agent dispatch worked specifically because both briefs named the owned file(s) and the forbidden file(s). The marginal cost is one sentence per brief. The cost of omitting it is a merge conflict in the very document the agent was trying to extend — the most expensive kind because resolving it requires re-reading both agents' work to decide which version of each section to keep.

---

## Suggestion 3: Pre-delete grep for retention notes before removing "redundant" fetched stubs

### Proposed addition

> **Before deleting any file in `research/fetched/`, `research/manual/`, or any similarly named drop-zone, grep `research/blocked-urls*.md` and `research/PLAN.md` for the file's basename or its source URL.** Prior drain passes routinely leave explicit retention notes (e.g., *"retained as 404 evidence; could now be deleted after the e-print recovery"*) that turn a deletion decision into a one-grep lookup. Without the grep you are guessing.
>
> *Grounded in: 2026-05-16 arxiv-stub deletion — the round-7 author had left an explicit eligibility note in `research/blocked-urls-round-8.md` ("Could now be deleted (the e-print route subsumes this), but keeping is harmless"). One `grep "2503.18813" research/*.md` surfaced it in <1s and turned a judgment call into a documented disposition.*

### Why this earns its place in your agents file

The retention/deletion eligibility convention is implicit and decentralized — it lives in whichever round's `blocked-urls-round-N.md` happened to encode it. Without the grep habit, a fresh-context agent has to re-derive the retention reason from first principles ("why was this 10 KB arxiv stub kept? is it load-bearing?") or err toward the safe-but-bloating "keep everything." Both alternatives are worse than `grep <basename> research/*.md`. The marginal cost is one grep per fetched-file deletion. The cost of skipping it is either unwarranted retention (repo bloat) or unwarranted deletion (provenance loss).

---

## Suggestion 4: When primary source contradicts a corpus claim, downgrade — don't delete

### Proposed addition

> **When a primary-source drain reveals that a claim previously held in the corpus is not actually supported by the primary source — either because the primary contradicts it or because the primary simply does not mention it — downgrade the claim's confidence (e.g., to "single-secondary-source") rather than deleting it.** Annotate the downgrade with the primary-source check that produced it ("not in `<file>`, minutes ~XX–YY") and keep the claim's original citation chain intact. Deletion erases the audit trail; downgrade preserves it.
>
> *Grounded in: 2026-05-16 Cherny drain — three corpus claims (`/loops` slash command, `/batch` slash command, "thousands of overnight agents") were not mentioned anywhere in the 90-min Cherny transcript that the corpus had been waiting on as their primary unlock. All three were downgraded in-place rather than deleted. A future agent now sees "we checked the highest-leverage primary source and it didn't confirm" instead of having to re-discover the gap.*

### Why this earns its place in your agents file

The default failure mode for an agent encountering an "unsupported" claim is one of two extremes: silently delete it (loses the audit trail; future agents may re-introduce the same claim from the same secondary) or silently leave it (loses the falsification work). The downgrade convention captures both: the claim stays visible *and* the falsification is recorded. The marginal cost is one annotation per downgraded claim. The cost of either extreme is recurring re-discovery of the same gap by future sessions — the cross-corpus-propagation problem already documented in PLAN.md §6.

---

*End of suggestions for session 2026-05-16-56.*
