# Drain stage 1 — inventory

Identify every file not yet in the catalog.

## Three input kinds

1. **Content files in ingestion drop dirs** — html, mhtml, md, txt, pdf, ipynb files in `research/manual/` or `research/fetched/issue-N/`.
2. **URL-list files** — `.txt` (or `.md`) files that contain only URLs (see `classify_text.py` rules). These represent intent, not content.
3. **Orphan files in `reference-only/<id>/`** — files dropped manually into existing source directories that aren't yet in the record's `files[]`.

## Discovery commands

### Content files in drop dirs not yet registered

```bash
F=reference-only/sources.json

# All candidate files
find research/manual research/fetched -type f \
  \( -name '*.html' -o -name '*.mhtml' -o -name '*.md' -o -name '*.txt' \
  -o -name '*.pdf' -o -name '*.ipynb' -o -name '*.png' -o -name '*.jpg' \) \
  > /tmp/all-candidates.txt

# Registered files (by basename match — heuristic)
jq -r '[.[] | (.files // [])[] | .filename] | map(select(. != null)) | .[]' "$F" \
  | sort -u > /tmp/registered-names.txt

# Candidates whose basename isn't already registered
while read f; do
  b=$(basename "$f")
  if ! grep -qFx "$b" /tmp/registered-names.txt; then
    echo "$f"
  fi
done < /tmp/all-candidates.txt > /tmp/uningested-candidates.txt

wc -l /tmp/uningested-candidates.txt
```

The basename-match is a heuristic — two files with the same basename in different drops would collide. The catalog can have multiple records with the same filename (different ids, different `<id>/` dirs), so this is just a first-pass filter; stage 2 will do per-file URL extraction to confirm identity.

### Orphan files in existing `<id>/` dirs

```bash
python .claude/skills/research-pipeline/scripts/check-source-dirs.py 2>&1 \
  | grep "not in record" \
  > /tmp/orphan-files.txt
```

## Per-file classification

For each uningested candidate:

```bash
EXT="${file##*.}"
case "$EXT" in
  txt|md)
    # Could be a URL list. Classify it.
    CLASS=$(python scripts/classify_text.py "$file" | jq -r '.kind')
    case "$CLASS" in
      url_list)              echo "→ stage 1b: process as URL list" ;;
      source_with_first_url) echo "→ stage 2: extract URL from first line" ;;
      source_with_header_url) echo "→ stage 2: use URL from header" ;;
      mixed_error)           echo "→ FLAG: mixed URL/non-URL content" ;;
      unrecognized)          echo "→ FLAG: no recognizable structure" ;;
      empty)                 echo "→ skip: empty file" ;;
    esac
    ;;
  html|mhtml|pdf|ipynb)
    echo "→ stage 2: per-format URL extraction"
    ;;
  png|jpg|jpeg|svg|gif|webp)
    # Images in drop dirs can't be auto-identified.
    echo "→ FLAG: image in drop dir (move to reference-only/<id>/ to associate)"
    ;;
  *)
    echo "→ FLAG: unknown format"
    ;;
esac
```

## Stage 1b: process URL lists immediately

URL list files are easy — they don't need stage 2. Process them at the end of stage 1:

```bash
for f in /tmp/url-list-files.txt; do
  python scripts/process-url-list.py "$f" --delete-after
done
```

This adds wanted records to the catalog. The trigger file gets deleted as part of the run.

## Stage 1c: defer orphans to stage 3

Orphan files in existing `<id>/` directories don't need URL extraction (their directory IS the identity). They get processed in stage 3 via `reconcile-source-dir.py`. List them now for the operator:

```bash
ORPHAN_DIRS=$(cat /tmp/orphan-files.txt | grep -oE 'reference-only/[0-9a-f]{10}' | sort -u)
echo "Orphan files found in: $ORPHAN_DIRS"
```

## Output of stage 1

A categorized list:

```
PROCESS NOW (URL lists, no human input needed):
  - research/manual/urls-batch-1.txt  (5 URLs)
  - research/manual/urls-batch-2.txt  (3 URLs)

TO STAGE 2 (URL extraction):
  - research/manual/page1.mhtml
  - research/manual/article.html
  - research/fetched/issue-42/0a1b...html
  - (...)

TO STAGE 3 RECONCILIATION (already in <id>/ dirs):
  - reference-only/0a7f3b8e00/ (1 orphan file)
  - reference-only/1b2c3d4e00/ (3 orphan files)

FLAGGED (operator attention):
  - research/manual/random.txt — mixed_error: contains URLs and non-URL content
  - research/manual/diagram.png — image in drop dir; move to reference-only/<id>/ manually
```

Surface this to the user. Let them confirm before proceeding to stage 2.
