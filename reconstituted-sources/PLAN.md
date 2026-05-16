# Reconstituted Sources — Execution Plan

**Branch:** `claude/reconstitute-sources-qdg0f`
**Status:** awaiting explicit user approval before execution
**Root:** `./reconstituted-sources/` (repo-relative)

## Resolved clarifications

1. **Path root** — repo-relative. All `/reconstituted-sources`, `/research/manual`, `/reference-only` references in the task brief = `./reconstituted-sources`, `./research/manual`, `./reference-only` inside this repo.
2. **INDEX.md scope** — catalogs ONLY `./reconstituted-sources`. `./reference-only` keeps its own existing per-cluster READMEs; we will NOT re-index those, and we will REMOVE from `./reconstituted-sources` anything that has a canonical copy in `./reference-only`.
3. **PR fan-out** — pre-filter to PRs that touched source-bearing paths (`research/manual/`, `research/fetched/`, `reference-only/`, top-level `*.txt|*.md|*.pdf|*.mhtml|*.html|*.ipynb` uploaded files). Skip PRs that only changed code/docs/retrospectives. Identical recovery result, much lower cost than 70 exhaustive subagents.
4. **Binary handling** — for `.mhtml`, `.pdf`, `.ipynb`, and other non-text sources, "strict subset" cannot be verified. Keep ALL distinct hashes, suffixed with `.v2`, `.v3`, etc. ordered by file size descending. No content-merge for binaries. Text sources still undergo subset-verify and content-merge per the original brief.
5. **Out-of-scope** — `research/figures/`, `research/followup/`, and the numbered report files (`research/00-…md` through `research/37-…md`) are **derived work, not sources**, so they will NOT be reconstituted. Same for retrospectives, ADRs, docs, harness, architectures.

## Source paths considered "source-bearing"

Paths that may have contained ingested sources (a file is a source candidate if the path matches OR the filename has an extension typical of an ingested source):

- `research/manual/**`
- `research/fetched/**` (the per-issue fetched directories, often deleted after drain)
- `reference-only/**`
- Top-level repo files: `*.txt`, `*.pdf`, `*.mhtml`, `*.html`, `*.ipynb` — early direct-to-main commits dropped raw uploads at the root before the `research/manual/` convention.

Excluded from "source-bearing":
- `research/[0-9][0-9]-*.md` (numbered reports)
- `research/{PLAN,INDEX,plan-sync,README}.md`
- `research/followup/**`, `research/figures/**`
- `retrospective/**`, `docs/**`, `harness/**`, `architectures/**`, `.github/**`, `.claude/**`, `.gitignore`, `AGENTS.md`, `spec-driven-ai-dev.md`, `initial-sources.md`, `research-plan.md`, top-level READMEs, top-level plan files

---

## Phase 0 — Setup (done before this plan was finalized)

- ✅ Created `./reconstituted-sources/`
- ✅ This PLAN.md written
- ⏳ Await user "go"

## Phase 1 — Per-PR fan-out (parallel subagents)

**Goal:** for each PR that touched a source-bearing path, recover the latest pre-deletion content of every source file the PR's branch deleted (or had deleted in its merge), into a unique per-PR subdirectory.

**Inputs:**
- All 70 merged PRs on `main` (`git log --merges`)
- Plus the 4 fetched-branch merges (`Merge fetched/issue-N`) which are not "PRs" but follow the same pattern

**Pre-filter:**
1. For each merge commit M with merge-base B:
   - Compute `git diff --name-status B..M` filtered to source-bearing paths.
   - If it shows any `D` (delete) or `R` (rename out) or `M` of a file that is now absent on main → enqueue.
2. Bucket: ~10–15 PRs likely qualify (drain PRs #38/#39/#43/#44/#67, fetched/issue-29/30/31/36/41/42 merges, plus any that moved files into `reference-only/`).

**Subagent dispatch (parallel, in batches of 8 via parallel-subagent-fanout pattern):**
- Each subagent gets one PR (or fetched-merge) to process.
- Each works in its own worktree: `../sf-recon-pr-<N>/` based on `main`.
- Each subagent has a self-contained brief: PR number, merge SHA, list of deleted-source paths, output directory `./reconstituted-sources/by-pr/pr-<N>/`.
- For each deleted file, subagent runs `git show <last-good-sha>:<path> > ./reconstituted-sources/by-pr/pr-<N>/<flattened-name>` (the LAST sha at which the file existed — `git log --diff-filter=D --pretty=format:"%H" -- <path> | head -1` then `^`).
- For binary files, uses `git show --binary` or `git cat-file -p`.
- Writes a per-PR `MANIFEST.txt` listing original path → flattened output filename.
- Subagent is **read-only on shared repo state**: it writes only to `./reconstituted-sources/by-pr/pr-<N>/` in the main worktree (the worktree is for git history isolation, not for output isolation). Returns to main agent, gets cleaned up.
- Brief explicitly forbids modifying anything outside its target output dir, opening PRs, or running tests.

## Phase 2 — Direct-to-main fan-out (parallel subagents)

**Goal:** for each non-merge commit directly on main that touched source-bearing paths, recover any added/deleted source files into per-commit subdirectories.

**Inputs:** `git log --no-merges --first-parent main` filtered to commits whose diff touched source-bearing paths. Visible early ones: `bf84ab5 lots of inputs`, `f15f744 lenny transcript`, `6fbc881 Add files via upload`, `8daf89d el-kaim chapters`, `889197d added sources`, `2b0e02f more sources`, `dd8968d a few more sources`, `e374bed more sources`, `b00c79a research sources`, plus drain-related non-merge commits.

**Dispatch:** parallel subagents, ~3 commits per subagent. Each works in its own worktree. Output to `./reconstituted-sources/by-direct-commit/<short-sha>/`.

For each touched source path, the subagent reconstructs the file content at the version introduced by that commit (the post-commit blob). If the same file was later modified in a subsequent direct-to-main commit, the LAST version that existed at any point on main wins. If the file currently exists on main, it skips (no recovery needed — but writes a stub manifest entry pointing to the live path).

## Phase 3 — Merge & flatten

After all Phase 1 + Phase 2 subagents return:

1. Collect everything from `./reconstituted-sources/by-pr/**` and `./reconstituted-sources/by-direct-commit/**` into `./reconstituted-sources/_staging/`.
2. Also copy `./research/manual/*` into `./reconstituted-sources/_staging/` (the user noted "Start with those" — these are the canonical "ingested but not yet deleted" set; treat them as the seed).
3. Compute SHA256 of every file in `_staging/`.
4. Group by basename (case-insensitive, after stripping the per-PR / per-commit dir prefix).
5. For each group:
   - **Identical hashes** → keep one, discard rest.
   - **Different hashes, text files** → run subset check (see Phase 4).
   - **Different hashes, binary files** → keep all distinct hashes, rename `name.v2.ext`, `name.v3.ext`, ordered largest first (largest is unsuffixed).
6. Output: flat layout in `./reconstituted-sources/` (one file per source, version-suffixed where needed).

## Phase 4 — Text dedup with subset verification (parallel subagents)

For each text-cluster with multiple distinct-hash candidates:

- Spawn a subagent per cluster (≤8 clusters at a time).
- Subagent gets: list of candidate file paths.
- Subagent identifies the largest file as the "candidate canonical".
- For each other file, checks whether its content is a strict substring/subset (normalized whitespace, ignoring trivial header differences) of the candidate.
- If yes → delete the smaller.
- If no → extract the diff content not present in the canonical; append it to the canonical under a clearly-marked `\n\n---\n\n## APPENDED FROM <other-filename> (NOT IN PRIMARY)\n\n<extracted-unique-content>\n` block; then delete the smaller.
- Result: one file per cluster.

## Phase 5 — Reference-only deduplication

Build a hash index of `./reference-only/**`. For every file in `./reconstituted-sources/`:

- If its hash matches a `./reference-only/**` file → delete from `reconstituted-sources`.
- If its basename matches a `./reference-only/**` file (different hash) → run a subset check (text) or size check (binary):
  - Reference-only ≥ reconstituted → delete from reconstituted.
  - Reconstituted has more text content → APPEND-and-mark the extra into the reference-only copy? **NO — user said reference-only is canonical and we leave it alone.** Instead, keep the reconstituted version (it has additional info beyond the canonical) and rename it `<name>.has-extras.<ext>` so the contrast with reference-only is explicit.

## Phase 6 — Move new-index.md and build INDEX.md (parallel subagents)

1. `git mv research/manual/new-index.md reconstituted-sources/new-index.md` (preserve as historical reference data — it has summaries for ~71 sources already).
2. Compute the final list of files in `./reconstituted-sources/` (excluding `PLAN.md`, `new-index.md`, `INDEX.md`).
3. Partition into chunks of 2–3 files each → ~25–30 chunks for ~70 files.
4. Spawn one subagent per chunk (in batches of 8 parallel).
5. Each subagent receives its 2–3 filenames and:
   - Reads the file (text or extracts text from MHTML).
   - Pulls the canonical URL from MHTML `Content-Location:` header, or filename pattern, or `new-index.md` lookup.
   - Writes a 2–3 sentence summary in the style of `new-index.md`.
   - Returns a markdown table fragment: `| filename | canonical URL | summary |`.
6. Main agent assembles fragments into `./reconstituted-sources/INDEX.md` (alphabetically by filename, one table).

## Phase 7 — Commit, push, draft PR

1. `git add reconstituted-sources/` (and the `git mv` of `new-index.md`).
2. Commit with a descriptive message documenting counts (files reconstituted, files deduped, files appended-with-extras).
3. Push `claude/reconstitute-sources-qdg0f` to origin.
4. Open a draft PR if one doesn't already exist; otherwise update the existing PR.
5. Subscribe to PR activity per AGENTS.md guidance.

---

## Risk register

- **Worktree volume.** Phase 1 may spin up ~10–15 worktrees concurrently; Phase 2 may add ~10 more. The fanout skill knows how to clean these up. We'll cap concurrent worktrees at 8.
- **MHTML/binary size.** Some MHTML files are 100s of KB. Total `reconstituted-sources/` may end up 50–150 MB. Will check `.gitignore` to make sure binaries aren't auto-ignored before committing.
- **Summary quality on MHTML.** Subagents will need to parse MHTML to extract a summary; falls back to header metadata if body parsing is brittle. Will note unparseable cases in the INDEX entry rather than hallucinate.
- **Subset check on text.** "Strict subset" is approximated as: candidate's normalized text contains the other's normalized text (whitespace-collapse, ignore leading title lines that differ between captures of the same article). Will be conservative — prefer to keep both with version suffix when in doubt.
- **`new-index.md` move.** Once moved into `reconstituted-sources/`, anything in `research/` or elsewhere that linked to it will break. Per user direction we do NOT need cross-references back to reports, so this is acceptable.

---

## Subagent brief template (Phase 1)

```
GOAL: Recover deleted source files from PR <N> (merge <SHA>) and write them to ./reconstituted-sources/by-pr/pr-<N>/ in the MAIN repo at /home/user/software-factory.

You are working in worktree <PATH> based on main.

DELETED FILES (each entry: path, last-good-sha):
  <path1>  <sha1>
  <path2>  <sha2>
  ...

INSTRUCTIONS:
1. For each entry, run: git show <sha>:<path> in your worktree.
2. Write the result to /home/user/software-factory/reconstituted-sources/by-pr/pr-<N>/<flattened-name>
   where <flattened-name> = basename(path) (do NOT preserve directory structure).
3. If two files in your list share a basename, suffix the second one with .v2 etc.
4. Write a MANIFEST.txt in your output directory: "<flattened-name>  <-  <original-path>  @  <sha>"
5. Return a one-paragraph summary: count of files recovered, any errors.

DO NOT: open PRs, modify the main worktree's source tree, run tests, commit anything in your worktree.
```

---

## Estimated counts

- Phase 1: ~12 source-touching PRs × 1 subagent each, in 2 parallel batches
- Phase 2: ~10 direct-to-main commits, grouped 3-per-subagent → ~4 subagents
- Phase 4: ~5–10 text dedup clusters
- Phase 6: ~25–30 summary subagents in parallel batches of 8
- Total subagent calls: ~55–60. Total wall time estimate: 30–60 minutes.
