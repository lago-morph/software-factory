# Validation playbook

When `bash scripts/lint-sources.sh` fails, the relevant linter prints a message identifying the record id and field. This doc maps each common error to its fix.

## How to run validation

```bash
# All linters in one go (run before every commit)
bash .claude/skills/research-pipeline/scripts/lint-sources.sh

# Individual linters (when you know what to focus on)
python .claude/skills/research-pipeline/scripts/validate-config.py
python .claude/skills/research-pipeline/scripts/validate-sources.py
python .claude/skills/research-pipeline/scripts/check-source-dirs.py
python .claude/skills/research-pipeline/scripts/check-source-refs.py
python .claude/skills/research-pipeline/scripts/check-fetch-provenance.py
python .claude/skills/research-pipeline/scripts/sanity-check-record.py [id ...]
```

`validate-config.py` and `sanity-check-record.py` produce warnings only — they never block. The other three can return exit code 1.

## Error messages and fixes

### `schema: <path>: <message>`
From: `validate-sources.py`. The catalog violates the JSON schema. The path identifies which field. Common cases:

- `additionalProperties`: you added a field not in the schema. Remove it, or extend the schema if it's genuinely needed.
- `enum`: a value isn't in the allowed set. Check `schema-reference.md` for valid values.
- `pattern`: an id or sha256 doesn't match the expected hex pattern. Regenerate via `url_canonicalize.py`.
- `required`: a required field is missing. Common: `id` or `title`.

### `<id>: id doesn't match sha256(canonical_url)[:10]=<expected>`
The record's id doesn't match what canonicalizing+hashing its canonical_url produces. Two fixes:
1. The canonical_url is wrong — correct it.
2. The id is wrong — change the map key (and `id` field) to the expected value.

Compute the right id:
```bash
python .claude/skills/research-pipeline/scripts/url_canonicalize.py "<the url>"
```

### `<id>: record.id=X doesn't match map key Y`
The `id` field inside the record doesn't equal the parent object's key. Set them equal — the map key is authoritative.

### `<id>: pointer_to=<X> doesn't exist as a record`
The id you set in `pointer_to` isn't a record in the catalog. Either:
1. Typo in the target id — fix it
2. The target record was deleted — restore it or pick a different target
3. You meant a different field — `pointer_to` is specifically for record-to-record redirection

### `<id>: pointer_to points to itself`
A record can't supersede itself. Either remove `pointer_to` or point to a different record.

### `<id>: pointer_to chain is circular (involves X)`
Two or more records point at each other forming a cycle. Break the cycle by clearing one of the `pointer_to` fields.

### `<id> files[N]: filename "X" contains path separator`
`filename` must be a basename. Either:
1. Rename to a basename (drop the path components)
2. If the path is meaningful, use the `location` override field instead

### `<id> files[N]: ingestion_status=have but file not on disk at <path>`
Either:
1. The file should exist — restore it (`git restore`, redownload, etc.)
2. The file is gone — change `ingestion_status` to `want` or `skip-not-necessary`

### `<id> files[N]: sha256 mismatch (recorded=X, actual=Y)`
The file's content doesn't match the recorded hash. Either:
1. The file was edited — update the recorded sha256 to the actual:
   ```bash
   sha256sum reference-only/<id>/<filename>
   ```
2. The file was corrupted — restore the original

### `<id>: file on disk not in record's files[]: <path>`
A file exists in `reference-only/<id>/` but no entry in the record's `files[]` lists it. Run:
```bash
python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py <id>
```
This will add the missing entry automatically.

### `URL cited in <report> but no record in catalog: <url>`
A research report cites a URL that has no catalog record. Either:
1. Add a record for the URL (see `edit.md` "Case 1: URL only")
2. The citation in the report is wrong — fix the report

### `<id>: completeness=complete but fetch_provenance.status=open`
A file is marked complete, but the GitHub issue/PR/branch that fetched it is still open. Either:
1. Close the issue / merge the PR / delete the branch as suggested
2. Update `fetch_provenance.status` to `merged` / `closed` to reflect reality

### `directory reference-only/<id>/ exists but no record with that id`
A per-id directory exists but the catalog has no matching record. Either:
1. Create the record (see `edit.md`)
2. The directory is orphaned — delete it via `git rm -r reference-only/<id>/`

### `legacy dir <path>: N referenced, M unreferenced files`
Files exist in a non-id directory (e.g., `reference-only/anthropic-agent-skills/`). The `M unreferenced` ones aren't pointed at by any record's `location` field. Either:
1. Create records for them with `location` overrides pointing to the legacy paths
2. Migrate to per-id directories (move files to `reference-only/<id>/`, update records)

This is a warning, not an error — legacy dirs are tolerated.

## Sanity warnings (no exit code 1)

`sanity-check-record.py` flags semantic inconsistencies as warnings. These don't fail the build but are worth investigating:

- `file 'X' title 'A' has only Y% token overlap with record title 'B'` — the file's `<title>` doesn't match the record. Possibly mis-filed; verify by opening the file.
- `files 'X' and 'Y' have only N% word overlap — possible misplacement` — two files in the same record have wildly different content. One of them is probably in the wrong directory.
- `file 'X' has URL host A, record canonical_url host is B` — file extracts to a different URL than the record's canonical URL. May be a redirected URL (fine) or a misplaced file (not fine).

To investigate a sanity warning, read the file content directly:
```bash
ls -la reference-only/<id>/
cat reference-only/<id>/<filename> | head -50
```

## The lint-or-fix-and-relint loop

```bash
# Edit
jq '<transform>' "$F" > /tmp/new.json
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"

# Lint
bash .claude/skills/research-pipeline/scripts/lint-sources.sh

# If lint fails: fix, re-lint. Repeat.

# When lint passes:
git add "$F"
git add reference-only/<id>/    # if you also added/changed files
git commit -m "..."
```

Don't ever push a sources.json that doesn't pass the linter. The GitHub Action runs the same lint on every push and will refuse to regenerate the markdown view if the catalog is invalid.
