---
name: single-source-of-truth-data
description: When a list, enum, or config is referenced by multiple consumers (scripts, schemas, docs, rendered views), consolidate into one canonical JSON file plus a helper module that every consumer loads at runtime. Use this skill when adding any list/enum that two or more places will reference, when refactoring to eliminate detected drift, or when designing data that consumers will edit. Triggers on phrases like "single source of truth", "the same list is defined in three places", "scripts read from one canonical file", "consolidate this list", or proactively when authoring a list/enum/config that's about to be referenced by 2+ scripts. The pattern: canonical pretty-printed JSON + schema + helper module + CI gate linter + documentation that references (not duplicates).
tags: [data-modeling, refactoring, configuration]
allowed-tools: [Bash, Read, Write, Edit]
---

# single-source-of-truth-data

When the same list/enum/config gets referenced by multiple consumers, it tends to drift. This skill is the consolidation pattern: one canonical pretty-printed JSON file is authoritative; all consumers read from it at runtime via a helper; documentation references the file as the source of truth instead of duplicating it.

## When to use

Use when:
- Adding any list/enum/config that 2+ scripts or 2+ docs will reference.
- You discover (via `grep`) that a list IS already duplicated across files — consolidation refactor.
- Designing a skill that ships with a list the consumer will edit.

Do NOT use when:
- The list is genuinely defined only at one consumer (no duplication risk).
- The list is part of a schema's structural contract (a fixed enum that should never change without a schema version bump).
- The "list" is just two or three values that won't grow.

## Why this exists

A canonical example from this repo: the 15 catalog categories started life duplicated across (a) a markdown doc, (b) a hardcoded Python list, (c) a drain stage doc. Without consolidation, adding a 16th category requires editing three files; missing one silently allows invalid tags or drops the new category from the rendered view. The user caught the drift risk before any drift had actually happened and asked for consolidation.

Beyond categories, this pattern applies to:
- Enum values (status codes, severity levels)
- Filename allow/blocklists
- URL pattern lists (`casual_url_patterns`)
- Format → MIME type mappings
- Any "we have these N items" data that scripts iterate over

## The pattern (6 elements)

### 1. Canonical JSON file at a memorable path

Pick a path that is:
- Top-of-repo or near it (not buried in a skill subdir)
- Easy to grep for
- Co-located with related data (e.g., `reference-only/categories.json` lives next to `reference-only/sources.json`)

Format:
```json
[
  {"tag": "dark-factory", "description": "..."},
  {"tag": "intent-driven-architecture", "description": "..."}
]
```

For mappings, use objects:
```json
{
  "html": "text/html",
  "mhtml": "multipart/related"
}
```

### 2. JSON Schema alongside

`<canonical>.schema.json` constrains the shape. Use `additionalProperties: false` for objects to catch typos.

### 3. Pretty-print discipline

**Every write must produce a pretty-printed file.** Use:
```python
json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
```

Or via jq for shell-driven writes:
```bash
jq -S 'sort_by(.tag)' /tmp/new.json > <canonical>.json
```

This is non-negotiable. The user reads this file directly; it must be diff-friendly and human-scannable without tooling.

### 4. Helper module

Every consumer goes through a single helper file:

```python
# scripts/_<list>.py
import json
from pathlib import Path

def load_<list>() -> list[dict]:
    """Returns the canonical list. Validates against schema if jsonschema available."""
    path = Path(__file__).resolve().parents[<N>] / "<canonical-path>"
    return json.loads(path.read_text(encoding="utf-8"))

def <list>_keys() -> set[str]:
    """Convenience: the keys (e.g., tag names) as a set."""
    return {item["<key-field>"] for item in load_<list>()}
```

Helpers can cache via `@functools.lru_cache(1)` if loads are frequent.

### 5. CI gate linter

A linter that fails the build if anything references an invalid value:

```python
# scripts/check-<list>.py
from _<list> import <list>_keys

def main():
    valid = <list>_keys()
    invalid = []
    # Walk consumers (records, configs, etc.); for each value used, check membership
    for ...:
        if value not in valid:
            invalid.append((location, value))
    return 1 if invalid else 0
```

Wire into `lint-sources.sh` or equivalent.

### 6. Documentation references, doesn't duplicate

Docs that previously contained the list now link to the canonical file:

> The 15 categories live in `reference-only/categories.json` (canonical). See
> that file for the authoritative list.

Don't paste the data into markdown — markdown tables drift.

## Bootstrap pattern (for skills that ship the list)

If the canonical file lives in the consumer repo (not the skill itself) and a fresh repo wouldn't have it, ship a bootstrap copy inside the skill and auto-install via the `self-bootstrapping-skill` pattern:

- Bootstrap: `.claude/skills/<skill>/resources/_catalog/<list>.bootstrap.json`
- Install script copies it to the canonical location on first run if missing.
- `--force` does NOT clobber existing user-edited copies; reserve that for `--clobber`.

## Concrete example: the 15-category taxonomy

Before consolidation:
- `.claude/skills/research-pipeline/resources/_catalog/category-taxonomy.md` — markdown table
- `.claude/skills/research-pipeline/scripts/render-sources-md.py` — `CATEGORY_ORDER` Python list
- `.claude/skills/research-pipeline/resources/_drain/stage-3-catalog-update.md` — referenced inline

After consolidation:
- `reference-only/categories.json` — canonical array of `{tag, description}` objects (pretty-printed)
- `reference-only/categories.schema.json` — schema
- `.claude/skills/research-pipeline/scripts/_categories.py` — `load_categories()`, `category_tags()`
- `render-sources-md.py` reads via helper: `CATEGORY_ORDER = [(c["tag"], c["description"]) for c in load_categories()]`
- `category-taxonomy.md` — links to JSON, no duplicated table
- `check-categories.py` — CI gate; fails if any record uses a tag not in `categories.json`

Adding a 16th category now: edit `categories.json`, push. Everything else updates on next render.

## Anti-patterns

- **Schema-as-canonical-list** — putting the enum in JSON Schema's `enum` field. Tempting because the schema validates membership, but ties list maintenance to schema versioning. Schema bumps should be rare; list edits frequent. Use a runtime linter instead.
- **Markdown table as source** — easy for humans, hostile to scripts. Even if your humans like the table, render it FROM the JSON; don't read it.
- **Hardcoded fallback in consumer** — `LIST = load_list() or [<fallback>]` defeats the purpose. If the canonical file is missing, fail loudly.
- **Forgetting docs** — updating scripts but leaving an old markdown table inline. The table WILL drift, often within the same PR.
- **Multiple "canonical" files** — "the schema has the enum AND there's a JSON file AND a Python list." Pick exactly one canonical and treat the others as derived (or delete).
- **Unsorted output** — without `sort_keys=True` or `jq -S`, the file's diff churns on every write. Always sort.

## Acceptance criteria

1. `grep -r "<list-name>"` returns ≤ 2 matches: the canonical file and the helper.
2. CI fails if a consumer uses a value not in the canonical file.
3. Editing the canonical file + re-running consumers picks up the change with no other modifications.
4. The canonical file is human-readable: pretty-printed, sorted, no tooling needed to view.
5. If the skill ships the list, it self-bootstraps when the canonical file is missing.

## Files this skill creates

- `<canonical-path>/<list>.json` — the data
- `<canonical-path>/<list>.schema.json` — JSON Schema
- `<skill>/scripts/_<list>.py` — helper module
- `<skill>/scripts/check-<list>.py` — CI gate linter
- `<skill>/resources/_catalog/<list>.bootstrap.json` — bootstrap copy (if shipping in skill)

Modifications:
- Docs that previously contained the list → replaced with reference link
- Consumer scripts → replaced hardcoded lists with helper calls

## See also

- [ADR 0003 — single source of truth for category taxonomy](../../../retrospective/2026-05-17-85/ADR-0003-single-source-of-truth-category-taxonomy.md) — design rationale + concrete instantiation
- [`self-bootstrapping-skill`](../self-bootstrapping-skill/SKILL.md) — the bootstrap-from-skill pattern this uses for missing canonical files
