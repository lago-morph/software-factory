# ADR 0003: Single source of truth for category taxonomy

## Context

PR #84 introduced 15 canonical categories for tagging catalog records (`dark-factory`, `intent-driven-architecture`, etc.). Initially the list lived in three places:

1. `.claude/skills/research-pipeline/resources/_catalog/category-taxonomy.md` — markdown documentation table.
2. `.claude/skills/research-pipeline/scripts/render-sources-md.py` — hardcoded `CATEGORY_ORDER` Python list with descriptions.
3. `.claude/skills/research-pipeline/resources/_drain/stage-3-catalog-update.md` — referenced inline as the tagging guide.

This is classic drift bait. Adding a 16th category requires editing three files; missing one silently allows untagged records or invalid tags. The user flagged the drift risk before any drift actually happened ("the canonical list should be in a separate JSON file under resources, and referred to in the skill").

## Decision

**The 15-category taxonomy lives in exactly one canonical file: `reference-only/categories.json` at the top of the repo.** It is pretty-printed JSON (`json.dumps(data, indent=2, sort_keys=True) + "\n"`), schema-validated by `reference-only/categories.schema.json`, and read at runtime by every consumer through a single helper `scripts/_categories.py`.

The schema for `tags` in `sources.schema.json` deliberately does **not** include an enum constraint pointing at the categories list. Reasoning: schema versioning is too coarse-grained for list maintenance — adding a category shouldn't require a schema version bump. Instead, a runtime linter (`check-categories.py`) enforces that all tags are members of the canonical list.

Documentation (`category-taxonomy.md`) becomes a pointer that says "see `reference-only/categories.json` for the authoritative list" — it can still contain prose about how to choose tags, but doesn't duplicate the data.

A bootstrap copy lives at `.claude/skills/research-pipeline/resources/_catalog/categories.bootstrap.json` so the skill is self-contained: if the canonical file is missing on first run, the skill restores it from the bootstrap.

## Alternatives considered

- **Schema enum constraint** — put `enum: [<15 tags>]` on the `tags` field in `sources.schema.json`. Rejected: ties category maintenance to schema versioning; every category change is a schema-version event.
- **YAML config block in SKILL.md** — same place as `casual_url_patterns`. Rejected: SKILL.md gets edited frequently for unrelated reasons; embedding structured data there increases the risk of malformed edits breaking the config parser.
- **Per-skill resource markdown table as canonical** — easy for humans to read but hostile to scripts. Rejected: every consumer would need a markdown table parser.
- **Inside the skill scripts directory** (e.g., `scripts/categories.json`) — keeps it self-contained but breaks the "skill = code, repo = data" separation we use elsewhere.

## Consequences

**Positive:**
- `grep -r '<category-name>'` reliably shows the canonical file plus only the helper that loads it.
- New consumers (the upcoming `recategorize.py`, `audit-records.py`) read from the same source as existing ones.
- The user can edit `categories.json` directly — it's pretty-printed and at a memorable path — without needing to understand the schema or any scripts.
- Pretty-print discipline (`sort_keys=True`, `indent=2`) makes diffs reviewable.

**Negative:**
- The schema doesn't enforce category membership at the schema level — invalid tags only get caught at lint time. (Mitigation: `lint-sources.sh` runs `check-categories.py`.)
- A two-step bootstrap (canonical file + skill-internal bootstrap copy) is one more thing to keep in sync. (Mitigation: the skill's self-syncing pattern from ADR 0006 covers this — pre-flight installs the bootstrap if canonical is missing.)
- Renders need to load JSON at runtime instead of importing a Python list. Tiny startup cost (~1ms).

## References

- `reference-only/categories.json` — the canonical list (to be created in PR #86 follow-on or PR #87)
- `reference-only/categories.schema.json` — schema (to be created)
- `.claude/skills/research-pipeline/scripts/_categories.py` — helper module (to be created)
- `.claude/skills/research-pipeline/scripts/check-categories.py` — linter (to be created)
- [ADR 0006](./ADR-0006-skill-self-bootstrapping.md) — bootstrap copy pattern
- [Retrospective 2026-05-17-85, Phase 8](../2026-05-17-85.md) — moment the user requested consolidation
