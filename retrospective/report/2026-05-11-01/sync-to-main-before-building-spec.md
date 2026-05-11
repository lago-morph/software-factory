# Spec: `sync-to-main-before-building`

## Intent

Prevent duplicate-mechanism builds where two agents work in parallel and each builds the same capability with incompatible conventions. The fix is a mandatory pre-build sync check against `main` whenever an agent is about to author new infrastructure (workflows, scripts, skills, shared config).

In this session, I built `fetch-blocked-sources.yml` end-to-end before discovering that main already shipped `fetch-blocked-urls.yml` (built by a parallel agent). My version had: different label name (`fetch-sources` vs `fetch-urls`), different output location (repo root vs `research/fetched/issue-N/`), different branch strategy (push to triggering branch vs new `fetched/issue-N` side branch), different authorization model (label + author allowlist vs label-only via Triage role). Reconciliation took ~20 minutes. Shipping both would have produced two parallel mechanisms — the cleanup would have taken hours, plus data fragmentation across two output trees.

The check is cheap (a few seconds of `git fetch` + `git log` + `grep`). The cost of skipping it scales with how many parallel agents the user runs.

## Trigger

**Direct user requests:**
- "Sync first"
- "Check main before you build"
- `/sync-check`

**Proactive triggers (automatic; the skill activates without prompting):**
- The agent is about to create a new file under `.github/workflows/`.
- The agent is about to create a new file under `.github/scripts/`.
- The agent is about to create a new directory under `.claude/skills/`.
- The agent is about to commit a config file (`.github/dependabot.yml`, `pyproject.toml`, `package.json`, etc.) that didn't exist before.
- The user mentions adding infrastructure, mechanisms, or shared config.

**Negative triggers (do NOT activate):**
- The work is bug-fix-only within a single file.
- The work is research / documentation / ADRs (not infrastructure).
- The agent is on `main` directly (extremely unusual — separate issue).

## Inputs

- The path(s) of file(s) the agent is about to create.
- Optional: keywords describing the feature ("URL fetching", "Cloudflare bypass", "PR labeler").

## Outputs

- Either:
  - **Clear-to-proceed signal.** main has nothing similar; build as planned.
  - **Reconciliation requirement.** main has a similar mechanism. Stop and design the reconciliation (extend, discard, or replace via ADR).
- A short pre-build report listing what was checked and what was found, written to the agent's working notes.

## Workflow

1. **Sync.** `git fetch origin main`.
2. **Survey recent main activity.**
   ```bash
   git log origin/main --oneline -20
   git log origin/main --since="2 weeks ago" --oneline
   ```
3. **Search by filename prefix.** For each new file the agent plans to create, look for prefix matches on main:
   ```bash
   git ls-tree -r origin/main --name-only | grep -iE "<prefix>"
   ```
4. **Search by feature intent.** Synonyms matter — `fetch-blocked-sources` and `fetch-blocked-urls` are the same feature.
   ```bash
   git ls-tree -r origin/main --name-only \
     | grep -iE "<synonym1>|<synonym2>|<synonym3>"
   ```
5. **Read design docs.** `find` for `*.md` files in `research/`, `docs/`, `.github/scripts/` on main that reference the feature area. If any exist, read them before building.
6. **Decision.**
   - **No overlap found:** proceed with the build; log "sync check clear" in working notes.
   - **Overlap found:** stop. Three options: (a) extend main's mechanism, (b) discard the planned build and use main's, (c) propose replacing main's via an ADR. Choose one with the user; do not silently ship both.
7. **Verify post-build.** Before push, run the file-modification intersection check:
   ```bash
   merge_base=$(git merge-base HEAD origin/main)
   my_changes=$(git diff --name-only "$merge_base" HEAD)
   main_changes=$(git diff --name-only "$merge_base" origin/main)
   comm -12 <(echo "$my_changes" | sort) <(echo "$main_changes" | sort)
   ```
   Empty output = no conflict. Non-empty = re-reconcile.

## Concrete examples

### Example 1 — catching this session's duplicate

Pre-build, what should have happened:

```bash
$ git fetch origin main
$ git log origin/main --since="2 weeks ago" --oneline | head -10
2861320 Merge pull request #7 from lago-morph/claude/fix-fetch-workflow-author-allowlist
4b76edf Switch to label-based gate; drop title and username gates
49daa63 Switch from author_association to explicit username allowlist
7f7553a Merge pull request #6 from lago-morph/claude/fix-fetch-workflow-length-fn
d019bc9 Replace length() with bash ${#var} — length is not a GH Actions function
9864320 Merge pull request #5 from lago-morph/claude/fix-fetch-workflow-observability
...
$ git ls-tree -r origin/main --name-only | grep -iE "fetch"
.github/scripts/extract_urls.py
.github/scripts/fetch_urls.sh
.github/workflows/fetch-blocked-urls.yml
```

Conclusion: STOP. main has a fetcher mechanism. Read `.github/workflows/fetch-blocked-urls.yml` and `research/PLAN.md` §5–6 (visible in `find` results) before designing your own. Almost certainly the right move is to extend or adopt rather than duplicate.

### Example 2 — clean case (proceed)

```bash
$ git fetch origin main
$ git log origin/main --oneline -5
abc1234 Merge PR #42: Fix lint config
def5678 Merge PR #41: Add docs
...
$ git ls-tree -r origin/main --name-only | grep -iE "github-action-runner|cache-warmer"
(no output)
```

Conclusion: proceed. Log `sync check clear: no main-side files match {github-action-runner, cache-warmer}`.

### Example 3 — synonym handling

User asks: "build a thing that grabs blocked URLs". You're about to create `.github/scripts/url-grabber.py`.

Pre-build synonym search:

```bash
$ git ls-tree -r origin/main --name-only \
    | grep -iE "fetch|grab|retrieve|download|pull|crawl|scrape" \
    | grep -iE "url|page|source|web|blocked|cloudflare"
.github/scripts/fetch_urls.sh
.github/workflows/fetch-blocked-urls.yml
```

Match found. Even though my planned filename is "url-grabber" and main's is "fetch-urls", they're the same feature. Stop and reconcile.

## Anti-patterns

- **Building first, then "checking compatibility" at the end.** I did this in this session. The sunk cost of the built work makes reconciliation harder.
- **Assuming the absence of a file means absence of work.** Main might have a similar feature under a different name. Search by intent, not just by filename.
- **Single-word search.** "url" alone is too narrow. Search the synonym cluster.
- **Skipping design-doc reads.** When `research/PLAN.md` exists on main and mentions the feature area, read it before authoring infra. It contains the design rationale.
- **Silent duplicate ship.** If you discover overlap and ship both anyway, you've made the reconciliation problem worse, not solved it.

## Acceptance criteria

1. Before any new file is created in `.github/`, `.claude/skills/`, or other shared-infra locations, `git fetch origin main` was run.
2. Filename-prefix and synonym-cluster searches were performed against main.
3. Any matching files on main were read (or design docs that reference them were read) before the agent decided to proceed.
4. Working notes (commit message, scratch file, or chat output) explicitly state "sync check clear" or "reconciliation required".
5. Post-build, the file-modification intersection check against main returns empty.

## Files this skill creates / modifies

- An entry in the agent's working notes / commit message (not a new file).
- Optionally: `.claude/skills/sync-to-main-before-building/checklist.md` as a reusable pre-build checklist the agent can `cat` before starting.
