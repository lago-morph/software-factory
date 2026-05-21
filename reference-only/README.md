# `/reference-only/` — source catalog

This directory holds the source catalog for the research corpus. Canonical data is `sources.json`; the human-browsable view is `sources.md` (auto-regenerated, do not hand-edit). Per-source files live in `<id>/` subdirectories, where `id = sha256(canonical_url)[:10]`.

See `.claude/skills/research-pipeline/SKILL.md` for editing procedures (catalog mutations, drain pipeline, audit checks). All edits to `sources.json` go through `jq` + `bash scripts/normalize-sources-json.sh` per the skill's hard rules.

`MIGRATION-EXCEPTIONS.md` records URLs cited in reports that have been deliberately excluded from the catalog (casual mentions, homepage references, etc.) so the URL-vs-reports lint check knows to skip them.

## What does NOT belong here

- `research/manual/` — transient drop zone for unfinished work. See its README.
- Anything not yet incorporated into a numbered report. Run the `research-pipeline` skill's Phase 0 first.
