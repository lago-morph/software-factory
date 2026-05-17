# ADR 0004: Filesystem placement IS source identity (for reference-only/<id>/)

## Context

The drain pipeline (PR #79, refined PR #81) processes files from ingestion directories (`research/manual/`, `research/fetched/`) and integrates them into the catalog. The natural flow extracts a URL from the file content (HTML `<link rel="canonical">`, MHTML `Snapshot-Content-Location:`, etc.), computes the source ID, and moves the file into `reference-only/<id>/`.

But many real-world scenarios produce files where URL extraction fails:
- Images (PNG, JPEG) — no embedded URL.
- Text extracts of HTML — no `<link>` tags survive.
- PDF files where the source URL isn't in metadata.
- Manually-edited or annotated files.
- Files copied from another location during ad-hoc work.

If the drain treats all of these as errors, the workflow becomes brittle. Users would need to manually pre-process every file to add a URL header.

Conversely, when a user manually drops a file into `reference-only/<id>/<filename>`, the *user has already decided* which source it belongs to. The directory placement IS the assertion of identity.

## Decision

**Files located in `reference-only/<id>/` directories are considered to belong to record `<id>`, regardless of whether their content yields a matching URL via extraction.**

Operationalization:
- The drain reconcile step (`reconcile-source-dir.py`) processes orphan files in `reference-only/<id>/` directories. It does NOT require URL extraction to succeed. It computes sha256, detects format, adds a file entry with `ingestion_status=have`.
- If URL extraction *does* succeed and the extracted URL's canonical form host differs from the record's `canonical_url` host, that's a **warning** (potential misplacement) — not an error. The user makes the call.
- Files in *ingestion drop directories* (`research/manual/`, `research/fetched/issue-N/`) without an extractable URL ARE flagged as errors — those locations don't carry identity, so URL extraction is required.

## Alternatives considered

- **Require URL extraction always** — would force users to pre-process all manual drops. Rejected: too high friction for the common case (image, partial text, custom annotation).
- **Compute identity from sha256 of content** — would treat each file as its own source, contradicting the catalog's "one source, many representations" design.
- **Track identity in a sidecar metadata file** — `.<filename>.meta` with the URL. Rejected: requires users to maintain two files in sync; the directory IS the metadata.
- **Allow any path, ID derived from path** — too permissive; loses the canonical structure.

## Consequences

**Positive:**
- "Drop file into the right place" is a complete workflow — no URL header required.
- Image attachments (figures, diagrams, screenshots) can be added to a record by simply dropping them in `reference-only/<id>/` without any metadata authoring.
- Reconciliation is mechanical: walk the directory, register what's there.
- Manual user-supplied content (browser-saved MHTML, custom annotations) integrates without special handling.

**Negative:**
- A user dropping a file into the wrong directory creates a quiet misfiling (no error at drain time). Mitigation: `audit-records.py` (PR #86 follow-on) cross-checks file content against record identity using URL extraction + content-similarity heuristics and surfaces likely misfiles.
- The "directory IS identity" rule has to be respected by all tools — anything that moves files between `<id>/` directories without updating the catalog produces inconsistency. Mitigation: only `reconcile-source-dir.py` and the drain manipulate `reference-only/<id>/` directories programmatically; manual moves are user-initiated and the user accepts the responsibility.

## References

- `.claude/skills/research-pipeline/scripts/reconcile-source-dir.py` — implements the directory-as-identity behavior
- `.claude/skills/research-pipeline/scripts/drain.py` — flags missing URL in drop directories; tolerates missing URL in `<id>/` directories
- `.claude/skills/research-pipeline/resources/_drain/stage-3-catalog-update.md` — documents the rule for ingestion
- [Retrospective 2026-05-17-85, Phase 7](../2026-05-17-85.md) — confirmed during the issue-82 drain when many fetched HTMLs lacked canonical URLs in their content
