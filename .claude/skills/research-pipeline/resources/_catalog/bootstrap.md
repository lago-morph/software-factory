# Bootstrap: creating the catalog from scratch

If `reference-only/sources.json` doesn't exist (or is `{}`), this doc walks the steps to seed it.

## Prerequisites

- Workflows installed: run `python scripts/install-workflows.py` if not.
- Empty starting catalog: `echo '{}' > reference-only/sources.json`
- Schema in place: `reference-only/sources.schema.json` should exist (it's tracked in the repo).
- Lint passes on empty catalog: `bash scripts/lint-sources.sh` — should report 0 errors (warnings about no URLs in reports yet are expected).

## Seed from existing reports (recommended)

If `research/` already has reports citing URLs, treat those citations as the seed:

```bash
# 1. Collect every URL cited in reports
find research -name '*.md' -exec grep -hoE 'https?://[^[:space:]<>")]+' {} \; \
  | sed 's/[.,;:!?)\]}"]\+$//' \
  | sort -u > /tmp/cited-urls.txt

# 2. Process them as a URL list
python scripts/process-url-list.py /tmp/cited-urls.txt
```

This produces a catalog of "wanted, URL known" records — one per cited URL — with no files attached. The drain pipeline takes it from there.

## Seed from existing `reference-only/<topic>/` content (legacy migration)

If `reference-only/` already has topical subdirectories from before the per-id convention (e.g., `anthropic-agent-skills/`, `lenny-podcast-transcripts/`, `el-kaim-book/`), you have two paths:

### Option 1: Keep legacy paths via `location` overrides (low-risk, recommended)

For each file in a legacy directory, create a record whose file entry uses `location` to point at the legacy path. No file moves; reports keep working.

Use a one-shot script (write inline; not packaged because this is one-time work):

```bash
F=reference-only/sources.json

for dir in reference-only/*/; do
  base=$(basename "$dir")
  # Skip per-id dirs and control files
  case "$base" in
    [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]) continue ;;
    sources.*) continue ;;
  esac
  echo "=== legacy dir: $base ==="
  # User does the URL identification per file manually here
done
```

### Option 2: Migrate to per-id (cleaner, more work)

For each legacy file, identify its canonical URL, compute the id, create the record properly, and `git mv` the file. Reports that link to the legacy path need updating.

In this project, Option 1 is the default — see `file-layout.md` for the rules.

## Seed from `source-dedup.md` (this project's PR #80)

PR #80 specifically handles the one-time migration of the existing `source-dedup.md` worksheet into the new structure. See `resources/migration-from-md.md` for the procedure (created in PR #80).

## After seeding

```bash
# Normalize key ordering
mv reference-only/sources.json /tmp/n.json
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh /tmp/n.json
mv /tmp/n.json reference-only/sources.json

# Lint
bash scripts/lint-sources.sh

# Render markdown (or wait for the workflow to do it)
bash scripts/render-sources-md.sh > reference-only/sources.md

# Commit + push
git add reference-only/
git commit -m "bootstrap source catalog"
git push
```

The auto-workflow fires on push to main and regenerates `sources.md` automatically. If you're on a branch, the manual-workflow can be triggered via:
- The Actions tab in GitHub (workflow_dispatch)
- Pushing a `reference-only/.regen-trigger` file (which gets deleted by the workflow)
