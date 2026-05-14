# Spec: `subagent-cleanup-sweep`

## Intent

Parallel drain subagents routinely produce *intermediate artifacts* that aren't covered by their explicit "delete these files when done" instructions: `.extracted.txt` plaintext renders of HTML, `.tmp.*` partial outputs, `*.bak` defensive backups, generated `.txt` versions of `.ipynb` notebooks. The orchestrator instructs each subagent to delete the *source files* it consumed (per the research-pipeline `git rm` discipline), but intermediate files fall through the cracks. They end up committed by an `git add -A` and pollute `research/manual/` (which is supposed to be a transient drop-zone — non-empty = unfinished drain work).

Grounded in this session's Phase D Anthropic Skills drain: the subagent extracted three Jupyter notebooks through several HTML→JSON→plaintext intermediates and left both the `.extracted.txt` and the simplified `.txt` versions of all three notebooks behind in `research/manual/`. The orchestrator only caught them via a follow-up `ls research/manual/` and had to `rm` them by hand.

`subagent-cleanup-sweep` formalizes the post-subagent cleanup so this doesn't recur.

## Trigger

**Direct phrases:**
- "Clean up the subagent intermediates"
- `/subagent-cleanup-sweep`

**Proactive trigger:** invoke automatically as the *last step* of any orchestration that dispatched ≥2 parallel subagents to a shared directory. The skill is cheap (a glob + classification + git commands) and forgetting it costs cleanup later.

**Negative trigger:** if the orchestrator is mid-dispatch (subagents still running), do NOT run — wait for all subagents to return.

## Inputs

- Working directory (defaults to the repo root).
- The set of directories subagents may have written to (typically `research/manual/`, `research/fetched/issue-*/`, sometimes `reference-only/<topic>/`).
- Optionally, a manifest of which files were "expected outputs" (provided by the orchestrator's dispatch state); files NOT in that manifest are candidates for cleanup.

## Outputs

- A short cleanup report (printed inline, ≤ 10 lines) listing which files were classified as intermediates and deleted.
- A `git rm` (for tracked files) or plain `rm` (for untracked) execution path that removes them.
- A staged commit is NOT created — the orchestrator's next commit will pick up the deletions.

## Workflow

1. **Inventory.** Run `find <subagent-write-dirs> -type f -newer <session-start-time>` to find files created/modified during the session.

2. **Classify by suffix and content.**
   - **Intermediate (delete):** `*.extracted.txt`, `*.extracted.md`, `*.tmp.*`, `*.bak`, `*.orig`, `*~`, files whose names match `<base>.<ext>` and `<base>.<other-ext>` simultaneously where the second is a plaintext render of the first (e.g., `.ipynb` + `.txt` siblings; `.html` + `.md` siblings produced by html2text). For the `.ipynb` case: keep the `.ipynb` (or move to reference-only/), delete the `.txt` if its content is clearly a flattened render of the same notebook.
   - **Primary source (keep, move to reference-only/):** Files explicitly listed by a drain subagent as "this is the primary source for report X." These should already have been moved by the orchestrator's post-drain step, but if any are still in `research/manual/`, move them now.
   - **Drain target output (keep):** Files matching `research/NN-*.md` or `research/followup/NN-*.md` that the subagent edited or created.
   - **Failure evidence (keep):** 404-status HTML files under `research/fetched/issue-*/` — per the research-pipeline skill rules, these stay as evidence.
   - **Unknown (flag for orchestrator):** Anything else — surface in the inline report; orchestrator decides per file.

3. **For each Intermediate file:** check `git ls-files --error-unmatch <path>` to determine tracked status.
   - Tracked → `git rm <path>`.
   - Untracked → `rm <path>` (then `git add -A` later when committing will pick up the deletion implicitly, though there's nothing to record).

4. **For each Primary source file** still in `research/manual/`: prompt the orchestrator to specify a `reference-only/<topic>/` destination and a README addition. (This is the only step that requires orchestrator input — everything else is mechanical.)

5. **For each Unknown file**: print to chat with classification options ("delete? move? leave?"). Default to leave-and-flag for orchestrator review.

6. **Print summary:** N files deleted, M files moved, K files flagged.

## Concrete examples

### Example 1 — Anthropic Skills drain leftover (this session, Phase D)

After the Anthropic Skills subagent returned, `research/manual/` contained:

```
01_skills_introduction.extracted.txt
01_skills_introduction.ipynb
01_skills_introduction.txt
02_skills_financial_applications.extracted.txt
02_skills_financial_applications.ipynb
02_skills_financial_applications.txt
03_skills_custom_development.extracted.txt
03_skills_custom_development.ipynb
03_skills_custom_development.txt
README.md
lenny-An AI state of the union.txt
lenny-Head of Claude Code.txt
platform.claude.com-agent-skills-overview.txt
support.claude.com-what-are-skills.txt
```

`subagent-cleanup-sweep` would classify:

- **Intermediate (delete):** `01_skills_introduction.extracted.txt`, `01_skills_introduction.txt`, `02_skills_financial_applications.extracted.txt`, `02_skills_financial_applications.txt`, `03_skills_custom_development.extracted.txt`, `03_skills_custom_development.txt` — both the `.extracted.txt` and `.txt` are flattened renders of the same `.ipynb`. Six files deleted.
- **Primary (move to reference-only/anthropic-agent-skills/):** the three `.ipynb` notebooks, plus `platform.claude.com-agent-skills-overview.txt` and `support.claude.com-what-are-skills.txt`. Five files moved.
- **Primary (move to reference-only/lenny-podcast-transcripts/):** `lenny-An AI state of the union.txt`, `lenny-Head of Claude Code.txt`. Two files moved.
- **Keep:** `README.md`.

Final state of `research/manual/`: just `README.md`. Inline summary: "6 intermediates deleted; 7 primaries moved to reference-only; 0 unknown."

### Example 2 — `research/fetched/issue-N/` after an action

After a fetch action commits, `research/fetched/issue-N/` contains all attempted URLs as `<hash>_<host>__<path>.html` plus `.md` siblings. The drain subagent processes them and deletes the consumed `.html`/`.md` pairs. `subagent-cleanup-sweep` does NOT touch this directory unless asked — the surviving files are usually 404 evidence (keep) or files the subagent forgot to delete. If the orchestrator passes `--include-fetched-dirs`, the sweep classifies:

- Files whose HTTP status was 404 (per the action's per-URL summary comment) → **Failure evidence (keep).**
- Files whose HTTP status was 200 AND the corresponding source URL appears as a ✅ row in some `research/*.md` source table → **Successfully drained (delete).**
- Files whose HTTP status was 200 but no ✅ row references them → **Unknown (flag).** Could be a missed drain target.

## Anti-patterns

- **Sweeping mid-orchestration.** If parallel subagents are still running, deleting their intermediate files mid-flight will break their work. Always wait for all subagents to return.
- **Auto-deleting Unknown files.** When in doubt, flag for orchestrator; never delete blindly. Lost provenance is expensive; disk is cheap.
- **Sweeping `reference-only/`.** Files there are primary sources kept for re-quoting; never delete from `reference-only/` as part of a sweep.
- **Skipping the `git ls-files` tracked-status check.** `git rm` an untracked file errors out (per this session's mishap: my first cleanup attempt used `git rm` and bombed on untracked `.txt` files). Always check tracked status first.
- **Sweeping without recording.** If a file is deleted, the inline summary must list it. The orchestrator's commit message should reference the sweep so future reviewers can audit what was removed.

## Acceptance criteria

1. `research/manual/` after the sweep contains only `README.md` (or whatever README the dropzone documents).
2. Every file deleted is recorded in the inline summary.
3. Every "Unknown" file is flagged, not silently kept or deleted.
4. `git status` after the sweep shows a clean working tree OR a working tree with only the orchestrator's pending changes (no surprise leftover staged-but-not-committed files from sub-subagent intermediate cleanup).
5. The sweep takes < 30 seconds (it's a glob + classification, not a deep scan).

## Files this skill creates / modifies

- Deletes (via `git rm` or `rm`) any file classified as Intermediate.
- Moves (via `git mv`) any file classified as Primary source still in `research/manual/`, to a `reference-only/<topic>/` destination chosen by the orchestrator.
- Creates or updates `reference-only/<topic>/README.md` for newly-introduced subdirs.
- Does NOT commit. The orchestrator's next commit will pick up the changes.
