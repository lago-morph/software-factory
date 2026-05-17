# Spec: `single-source-of-truth-data`

## Intent

When a list/config/enum is referenced by multiple consumers (scripts, schemas, docs, rendered views), it tends to drift. This session had the "15 categories" list defined in three places: `category-taxonomy.md` (free-form table), `render-sources-md.py` (hardcoded Python list `CATEGORY_ORDER`), and `_drain/stage-3-catalog-update.md` (referenced as part of the drain procedure). The user caught the drift risk before any actual drift happened and asked for consolidation. This skill establishes the pattern: **one structured data file is the canonical list; all consumers read from it at runtime; documentation references the file as authoritative**. Schemas are deliberately *not* the canonical location because schema versioning is too coarse for list maintenance.

## Trigger

Use when:
- Adding any list/enum/config that 2+ scripts or 2+ docs will reference
- Discovering that a list IS already duplicated across files (consolidation refactor)
- Designing a skill that ships with a list the consumer will edit

Do NOT use when:
- The list is genuinely defined only at one consumer (no duplication risk)
- The list is part of the schema's structural contract (e.g., a fixed enum that should never change without a schema version bump)

## Inputs

- The list/data being canonicalized (current location(s) + content)
- Names of consuming scripts and docs that need to read it

## Outputs

- A canonical structured data file (typically JSON, pretty-printed)
- A schema constraining the data file
- A helper module (`_<list>.py` or similar) that loads + validates and returns the list
- Updates to consumers: replace hardcoded lists with calls to the helper
- Documentation updated to reference the canonical file (not duplicate the data)

## Workflow

1. **Pick the canonical location**: a JSON file at a memorable, top-of-repo path (e.g., `reference-only/categories.json`, NOT buried in a skill subdir). Reasoning: top-of-repo paths are easier to spot in `ls`, easier to grep for, and don't bind the data's lifetime to the skill's lifetime.
2. **Write the schema** alongside: e.g., `reference-only/categories.schema.json`. Constrains shape; explicit `additionalProperties: false`.
3. **Pretty-print discipline**: every write goes through `json.dumps(data, indent=2, sort_keys=True) + "\n"`. The user reads this file directly; it must be diff-friendly and human-scannable. Make the install/edit workflow re-pretty-print after every change (a normalize step like `jq -S 'sort_by(.tag)'` enforced post-write).
4. **Write the helper**:
   ```python
   # scripts/_categories.py
   def load_categories() -> list[dict]:
       path = repo_root() / "reference-only" / "categories.json"
       data = json.loads(path.read_text())
       # Optional: validate against schema here
       return data

   def category_tags() -> set[str]:
       return {c["tag"] for c in load_categories()}
   ```
5. **Update all consumers** to call the helper. Search the codebase first (`grep -r "CATEGORY_ORDER"` etc.) — miss one and the drift comes back immediately.
6. **Bootstrap copy in skill** (if shipping in a skill): keep a copy at `resources/_catalog/categories.bootstrap.json` and have the skill's pre-flight install it if the canonical location is missing. This makes the skill self-bootstrapping (see `self-bootstrapping-skill` skill).
7. **Documentation updates**: docs that previously contained the list now say "see `reference-only/categories.json` (canonical)". Don't duplicate the data in markdown — the markdown will drift.
8. **CI gate**: a linter (e.g., `check-categories.py`) verifies that everything tagged with a category tag uses a tag in `categories.json`. Test that adding an invalid tag fails CI.

## Concrete examples

### Example 1: 15-category taxonomy in software-factory

Before:
- `category-taxonomy.md` — 15-category table in markdown
- `render-sources-md.py` — `CATEGORY_ORDER` list with 15 tuples
- `_drain/stage-3-catalog-update.md` — "use these 15 categories"

After:
- `reference-only/categories.json` — canonical JSON array of `{tag, description}` objects
- `reference-only/categories.schema.json` — schema
- `.claude/skills/research-pipeline/scripts/_categories.py` — `load_categories()` + `category_tags()`
- `render-sources-md.py` — `from _categories import load_categories; CATEGORY_ORDER = [(c["tag"], c["description"]) for c in load_categories()]`
- `category-taxonomy.md` — links to canonical JSON instead of duplicating the table
- `check-categories.py` (CI gate) — fails build if records have tags outside the canonical list

### Example 2: where this would NOT apply

The `casual_url_patterns` config in SKILL.md's YAML block is used only by `check-source-refs.py`. One file reads it, one file defines it (in the SKILL.md config block). Adding a separate `casual_url_patterns.json` would be over-engineering. Keep it in the config block until a second consumer emerges.

## Anti-patterns

- **Schema-as-canonical-list** — putting the enum in the JSON Schema's `enum` field for `tags`. Tempting but binds list maintenance to schema versioning. List updates should be lightweight; schema updates aren't.
- **Markdown table as source of truth** — the table renders nicely for humans but is a nightmare to parse from scripts. Use JSON; render markdown from JSON if needed.
- **Hardcoded fallback in consumer** — `CATEGORY_ORDER = load_categories() or [("fallback", "...")]` defeats the purpose. If the canonical file is missing, fail loudly.
- **Forgetting docs** — updating scripts but leaving the markdown table inline. The markdown WILL drift. Replace duplicated data with a reference link.
- **Multiple "canonical" locations** — "the schema has the enum AND there's a JSON file" → two canonicals = no canonical. Pick one.

## Acceptance criteria

1. `grep -r "<list-name>"` returns ≤ 2 matches: the canonical file and the helper that loads it.
2. CI fails if a consumer uses a value not in the canonical file.
3. Editing the canonical file + re-running consumers picks up the change with no other modifications.
4. The skill is self-bootstrapping if the canonical file is missing.
5. The canonical file is pretty-printed and human-readable without tooling.

## Files this skill creates / modifies

- `<canonical-path>/<list>.json` — the data, pretty-printed
- `<canonical-path>/<list>.schema.json` — JSON Schema
- `<skill>/scripts/_<list>.py` — helper module
- `<skill>/scripts/check-<list>.py` — CI gate linter
- `<skill>/resources/_catalog/<list>.bootstrap.json` — bootstrap copy (if shipping in a skill)
- Docs: replace duplicated data with reference link
- Consumers: replace hardcoded lists with helper calls
