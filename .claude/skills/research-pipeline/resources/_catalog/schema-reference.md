# Schema reference

The full JSON Schema is at `reference-only/sources.schema.json`. This doc explains the field semantics, value sets, and the gotchas that aren't expressible in the schema itself.

## Top-level structure

`sources.json` is a single object whose keys are 10-char hex record IDs:

```json
{
  "0a7f3b8e00": { "id": "0a7f3b8e00", ... },
  "1b2c3d4e00": { "id": "1b2c3d4e00", ... }
}
```

Keys must be sorted alphabetically. `validate-sources.py` warns if not.

## Record fields

### `id` (required, immutable)
The 10-character hex prefix of `sha256(canonical_url)`. **Always derived, never invented.** Compute with:

```bash
python .claude/skills/research-pipeline/scripts/url_canonicalize.py <url>
```

The `id` field inside the record MUST equal the parent map key. If they diverge, validation fails.

### `pointer_to` (optional)
A different record's `id`. Used to indicate **this record is superseded** — the canonical content has moved to the pointed-to record. Two scenarios:

1. **Wrong URL discovered.** We thought a file lived at URL A, computed id-A, created record A. Later we discovered the file actually lives at URL B. Create record B (with the correct files), set A's `pointer_to=B`. Don't delete A — there may be back-references to it in older work.
2. **URL renamed upstream.** A site's URL pattern changes. Create record B (new URL), set A's `pointer_to=B`.

A record with `pointer_to` set is rendered in § 4 (Superseded) of the markdown view.

`pointer_to` chains can be more than one hop deep. Validators reject circular chains and self-pointers.

### `canonical_url` (required unless title-only)
The URL whose hash produced this record's `id`. Must be in canonical form (see `url_canonicalize.py` for the rules). If you set this field, the linter verifies that `sha256(canonical_url)[:10] == id`.

A record without `canonical_url` is only valid if it's a "title-only / find-me" record — you know the source exists by name but don't have a URL yet. In that case, populate `search_hints`.

### `original_url` (optional)
The pre-canonicalization URL, kept for back-reference lookups. The `check-source-refs.py` linter matches both `canonical_url` and `original_url` against report citations, so old links in reports still resolve.

### `title` (required)
The source's own title — what *it* calls itself. Not the URL, not the filename. Use `(unknown)` if not yet determined (for example, in records auto-created from a URL list).

### `short_summary` (optional)
8–10 word summary suitable for the markdown browse view. Max 120 chars.

### `long_summary` (optional)
Paragraph-length summary of the source's substantive content and why it matters. Not surfaced in the markdown view — jq the JSON to read it.

### `comments` (optional)
Unstructured notes about the record itself. File-specific notes belong in `files[].comment`.

### `search_hints` (optional, array of objects)
Each hint:
```json
{ "hint": "search Google for 'X Y Z'", "tried": false, "found": false }
```

When you exhaust a hint (tried and didn't find anything useful), set `tried: true`. When a hint led you to the file, set `found: true`. Records with all hints marked tried+!found are signals that the source is probably unrecoverable.

### `has_useful_diagrams`
`"yes"` / `"no"` / `"unknown"`. Set after a human or vision-capable AI has looked at the source's images. Default `"unknown"` for fresh records.

### `references_from`
Array of repo-relative paths to research reports that cite this source's `canonical_url`. Auto-derived by `check-source-refs.py`. Don't hand-edit — let the linter populate it after each new report is committed.

### `tags`
Lowercase kebab-case strings. No leading/trailing dashes. Use to group records by theme.

### `bibliographic` (optional)
Structured citation data:
```json
{
  "authors": ["Smith, J.", "Jones, K."],
  "year": 2024,
  "title": "Paper Title",
  "venue": "ICLR 2024",
  "doi": "10.48550/arXiv.2310.06770",
  "raw_bibtex": null
}
```

If structured fields don't fit (e.g., a blog post, a podcast transcript, a tweet), use `raw_bibtex` for free-form citation text and leave the structured fields null.

### `files` (array)
Each file entry represents one physical file OR one *desired* file. See "File entries" below.

## File entries

### `format` (required)
MIME-style identifier. Common values: `html`, `mhtml`, `md`, `txt`, `pdf`, `ipynb`, `image/png`, `image/jpeg`, `image/svg+xml`, `youtube-transcript`. See the schema for the full enum. Use `"other"` for anything not listed.

`youtube-transcript` is a special plain-text format whose file's **first line is the canonical YouTube URL** and whose body is the transcript. It pairs with the `youtube_url` field below. Full lifecycle and audit rules: `resources/_drain/youtube-transcripts.md`.

### `filename` (optional)
**Basename only** — no path components. The physical location is computed as `reference-only/<id>/<filename>`. Use `null` when `ingestion_status=want` and you don't have a specific desired filename yet.

### `location` (optional, override)
Repo-relative path that overrides the default location. Use ONLY for:
- Legacy files in `reference-only/<topic>/` (e.g., `anthropic-agent-skills/`, `lenny-podcast-transcripts/`) that predate the per-id convention
- Shared assets in `research/figures/`
- Anything else that genuinely can't live at `reference-only/<id>/<filename>`

If you set `location`, the linter trusts it as the file's location and silences the orphan-file warning for it.

### `sha256` (optional)
SHA-256 of the file content as hex. The linter computes the actual file's sha256 and fails on mismatch. Always set when `ingestion_status=have`.

### `ingestion_status` (required)
| value | meaning |
|---|---|
| `have` | File exists on disk; we have it |
| `want` | We want this format/file but don't have it |
| `skip-not-necessary` | We've decided we don't need this format (got equivalent content elsewhere) |
| `skip-unknown` | We don't know if we want it |

### `completeness`
| value | meaning |
|---|---|
| `complete` | Full content captured |
| `partial` | Truncated or missing sections (e.g., a 30-min cut of a 90-min transcript) |
| `error` | Fetch produced an error page (404, paywall, JS shell, cloudflare challenge) |
| `unknown` | Not yet verified |

### `comment`
File-specific notes. **For images, this is where the auto-generated visual summary lives.**

### `youtube_url` (conditional)
**Required when** `format=youtube-transcript`. **Forbidden on any other format** (schema-enforced). The canonical `https://www.youtube.com/watch?v=<ID>` URL of the video the transcript is for. Use `python scripts/youtube_urls.py <file>` to inspect or `youtube_urls.canonicalize_youtube_url()` to normalize.

When `ingestion_status=have`, the audit also requires that the same URL appears as the first line of the transcript file (check 15: `youtube-transcript-content-matches`).

### `fetch_provenance` (optional)
For files acquired via the `fetch-blocked-urls` GitHub Actions workflow:
```json
{
  "issue_number": 42,
  "pr_number": 99,
  "branch": "fetched/issue-42",
  "status": "open"
}
```

`status` is `"open"`, `"merged"`, `"closed"`, or `"abandoned"`. When `completeness=complete`, the linter expects `status` to be `merged` or `closed` and surfaces an error with suggested actions otherwise.

## Hard rules summary

1. `id` always derived from `canonical_url` (sha256 prefix), never invented.
2. `id` field must equal parent map key.
3. `pointer_to` chains can't cycle or self-loop.
4. `filename` is basename only; use `location` for paths.
5. `ingestion_status=have` requires the file to exist on disk and (if `sha256` set) match.
6. `completeness=complete` + `fetch_provenance.status=open` is an error.
7. Top-level keys must be sorted alphabetically.
8. Never delete a record — use `pointer_to` to retire it.
