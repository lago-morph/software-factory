# Drain stage 4 — validation gate

Before any content extraction (stage 5), the catalog must be valid.

## Run the linter

```bash
bash .claude/skills/research-pipeline/scripts/lint-sources.sh
```

If exit code is 0, proceed to stage 5.

If non-zero, halt the drain. Do not proceed to content processing on a broken catalog.

## Common failures after stage 3

| Failure | Cause | Fix |
|---|---|---|
| `id doesn't match sha256(canonical_url)[:10]` | Wrong canonicalization during stage 2 | Re-canonicalize the URL; correct either the id or the canonical_url |
| `file not on disk at <path>` | Stage 3 set `ingestion_status=have` but the `git mv` didn't actually happen | Verify the file is at the expected location; check for typos in `filename` |
| `sha256 mismatch` | File content was modified after stage 3 wrote the sha | Recompute `sha256sum <file>` and update the record |
| `file on disk not in record's files[]` | A file was moved into `reference-only/<id>/` but the catalog wasn't updated | Run `reconcile-source-dir.py <id>` |
| `pointer_to doesn't exist as a record` | Drain set a pointer to a record that wasn't created yet | Reorder the drain: create target record first, then set pointers |
| `URL cited in <report> but no record in catalog` | A report citation has no matching record yet | Either add a wanted record now, or accept the error if the URL will be fetched later |

## Sanity warnings (not errors, but worth reading)

```
⚠ <id>: file 'X' title 'A' has only 12% token overlap with record title 'B'
```

This is `sanity-check-record.py` saying the file content doesn't match the record's title. Investigation:

```bash
# Check the actual file content
cat reference-only/<id>/X | head -50

# Check the record's title
jq --arg id "<id>" '.[$id].title' reference-only/sources.json
```

If the file genuinely doesn't belong to this record, move it elsewhere. If the title is just out of date, update the record's title field.

## Halt-and-fix loop

```bash
# Drain stage 3 finishes
bash scripts/lint-sources.sh
# → ✗ N error(s)

# Fix each error
# ...

# Re-validate
bash scripts/lint-sources.sh
# → if errors, loop again

# Only when clean
echo "✓ catalog valid, proceeding to stage 5"
```

## Snapshot before stage 5

Before stage 5 (content processing into reports) modifies anything beyond the catalog, commit:

```bash
git add reference-only/
git commit -m "drain: stage 1-4 complete; N records added, M files attached"
```

This way if stage 5 produces bad report content and gets rolled back, the catalog state is still safe.
