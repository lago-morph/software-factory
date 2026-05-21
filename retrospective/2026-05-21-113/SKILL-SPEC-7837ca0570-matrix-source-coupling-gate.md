# Spec: `matrix-source-coupling-gate`

- **ID**: SKILL-SPEC-7837ca0570
- **Source retrospective**: ../2026-05-21-113.md

## Intent

A reusable factory skill: given a markdown table file and a glob of source files corresponding to rows or columns, generate the lint script and CI gate that enforce 1:1 correspondence (source changes require matching row/column changes with no spillover). Generalizes the architecture-failure-mode-gate pattern PR #113 built specifically for the failure-mode coverage matrix into a one-shot skill that scaffolds the same gate for any coupled-edit matrix in the repo.

The motivating session moment: PR #113 built `architecture-failure-mode-gate` — a self-installing skill that owns one specific table (`architectures/failure-modes.md` §2.4) and enforces that edits to `architectures/0N-*.md` and column N of the table travel together. The pattern is general — any table whose columns or rows are 1:1 with a glob of source files (e.g., a feature-status table vs. feature implementations, an evaluation-criteria matrix vs. evaluator implementations, a tier-pricing table vs. tier config files) deserves the same enforcement. This skill is the factory that materializes the gate skill for a new (table, source-glob) pair in one invocation.

## Trigger

**Direct triggers**:
- "Add a coupled-edit gate for `<file>`."
- "Scaffold a matrix-source-coupling-gate skill for `<table>` vs `<glob>`."
- "Make sure when X changes, the row/column for it in Y also changes."

**Proactive triggers**:
- A new markdown table is being authored whose rows or columns are 1:1 with files matching a glob, AND the table is referenced by ≥2 downstream consumers (docs, scripts, other docs).
- A reviewer comment of the form "when you change X also update Y" appears in a PR.
- The user uses phrases "coupled edits", "1-to-1 correspondence", "column matches file", "row per X".

**Negative triggers**:
- The table's rows/columns do NOT have a stable file-mapping (rows are arbitrary IDs, not files).
- The list of items is genuinely small (≤3) and stable; the lint overhead exceeds the benefit.
- The "table" is actually rendered from a single-source-of-truth JSON (use the `single-source-of-truth-data` skill instead).

## Inputs

- `table_path` — repo-relative path to the markdown file containing the matrix (e.g., `architectures/failure-modes.md`).
- `table_section` — the H3 (or other) heading that opens the validated table region (e.g., `### 2.4 Failure mode coverage`).
- `table_section_end` — the marker that closes the region (e.g., `**Coverage column scores ...**`), OR `null` if the table extends to end-of-file.
- `source_glob` — glob describing the source files coupled to rows or columns (e.g., `architectures/0[1-9]-*.md`).
- `axis` — `"column"` or `"row"`: are sources mapped to columns or rows?
- `key_extractor` — regex (or callable) that maps a source filename to its key (e.g., `^0([1-9])-` → integer N).
- `header_pattern` — regex that the column header (or row label) must match (e.g., `^(\d+):\s*\S+`).
- `skill_name` — kebab-case name for the new skill (e.g., `architecture-failure-mode-gate`).
- `override_label` — PR label that permits one-axis-only edits (default: `<skill-name>-only`).

## Outputs

- A new skill directory at `.claude/skills/<skill-name>/` with:
  - `SKILL.md` — schema description, pre-flight, update discipline, override flow, "Handling the gate review" section.
  - `scripts/install.py` — `--check` / `--force` / `--dry-run` / `--no-commit` with three exit codes.
  - `scripts/lint-<table-basename>.py` — markdown table parser + structure check + `--check-diff <BASE_REF>` mode.
  - `resources/_workflows/<skill-name>-gate.yml` — workflow template with `__SKILL_PATH__` placeholder.
- The installed workflow at `.github/workflows/<skill-name>-gate.yml` (via auto-run of install.py).
- A first-commit bootstrap that registers the new skill + commits the workflow.
- Updates to any related skill's SKILL.md decision tree to cross-reference the new skill.

## Workflow

1. **Validate inputs.** Confirm `table_path` exists, `source_glob` matches at least one file, and the table at `table_path` contains a header row matching `header_pattern`.
2. **Scan for existing skill.** If `.claude/skills/<skill-name>/` already exists, abort with a clear message ("the skill exists; modify it directly or pick a new name").
3. **Generate the linter.** Author `scripts/lint-<table-basename>.py` from a template, parameterized by `table_section`, `table_section_end`, `header_pattern`, the `ARCH_PATH_PATTERN` derived from `source_glob`, and the axis-mode (`column` vs `row`). The linter implements `parse_table`, `structure_errors`, `changed_columns` (or `changed_rows`), and `diff_errors` — identical in shape to `architecture-failure-mode-gate`'s linter.
4. **Generate the workflow template.** Author `resources/_workflows/<skill-name>-gate.yml` with `__SKILL_PATH__` placeholders, the `pull_request` trigger restricted to `paths: ['<table-dir>/**', '<skill-path>/**']`, and the lint+post-or-dismiss-review step.
5. **Generate the install script.** Author `scripts/install.py` from a template with the `REQUIRED_SKILL_FILES` list reflecting this skill's structure and `SKILL_PATH = ".claude/skills/<skill-name>"`. Three exit codes (0/1/2).
6. **Generate the SKILL.md.** From the canonical template: STOP-pre-flight section first; description in frontmatter LEADS with the install command (per AGENTS rule `AGENTS-MD-bfb7c7722c`); schema description specific to this (table, glob); update discipline explaining single-axis-edit; "Handling the gate review" section.
7. **Run the install once** to land the workflow at `.github/workflows/<skill-name>-gate.yml`. Verify `install.py --check` returns 0.
8. **Run the linter** in structure-only mode to confirm the current table state is valid.
9. **Cross-reference**: for every existing skill whose SKILL.md mentions the table by path, add a row to its decision tree pointing at the new skill. Commit.

## Concrete examples

### Example 1: Scaffold a feature-status × feature-implementation gate

Inputs:
- `table_path = "docs/feature-status.md"`
- `table_section = "## Feature status matrix"`
- `table_section_end = null` (table is last in file)
- `source_glob = "features/*/README.md"`
- `axis = "row"`
- `key_extractor = r"^features/([^/]+)/"` (the feature slug)
- `header_pattern = None` (rows, not columns; row labels match feature slugs from glob)
- `skill_name = "feature-status-gate"`

Outputs:
- `.claude/skills/feature-status-gate/{SKILL.md, scripts/install.py, scripts/lint-feature-status.py, resources/_workflows/feature-status-gate.yml}`
- `.github/workflows/feature-status-gate.yml` installed via `--force`.
- One commit landing all of the above plus a first-pass `--check` verifying the current table is consistent.

After landing: any PR that edits `features/auth/README.md` but not the `auth` row in `docs/feature-status.md` is blocked by a `REQUEST_CHANGES` review.

### Example 2: Scaffold a model-eval × evaluator gate

Inputs:
- `table_path = "evaluations/COVERAGE.md"`
- `table_section = "### Coverage matrix"`
- `table_section_end = "## Notes"`
- `source_glob = "evaluations/criteria/*.toml"`
- `axis = "column"`
- `key_extractor = r"^evaluations/criteria/([^.]+)\.toml$"`
- `header_pattern = r"^[a-z][a-z0-9-]*$"` (criterion slug as column header)
- `skill_name = "eval-coverage-gate"`

Outputs equivalent to Example 1 but for the eval-coverage table. The same shape — different parameters.

## Anti-patterns

- **Hardcoding the table parser logic.** The linter must accept `table_section` / `table_section_end` / `header_pattern` as parameters, not bake them in. PR #113's mistake: `lint-failure-modes.py` literally encodes `### 2.4 Failure mode coverage` as a constant. That's fine for one table; for a factory, parameterize.
- **Skipping the cross-reference step.** Once the gate skill exists, every other skill that touches the table needs a one-line cross-reference. Skipping this means future agents edit the table without loading the gate skill, and discover the gate via failing CI instead of via documentation.
- **Re-running `--force` install on every invocation when `--check` would suffice.** The install pattern is already proven idempotent; only `--force` on actual drift, not as a "make sure it's there" reflex.
- **Generating a mutator CLI in addition to the lint+gate.** PR #113 explicitly chose "lightest" (no JSON canonical, no mutator CLI). Most coupling gates do not need a mutator — the lint and the column-spillover ban are usually sufficient. If a project genuinely needs single-cell mutator tooling, that's a separate skill (e.g., `single-source-of-truth-data`).

## Acceptance criteria

- [ ] Scaffolding a new gate for a (table, source-glob) pair takes ≤ 5 minutes of agent time end-to-end, including the first-commit bootstrap.
- [ ] The generated linter passes its own structure check on a known-good table state.
- [ ] The generated workflow posts a REQUEST_CHANGES review on a synthetic spillover case (verified via a test-PR-against-self in the scaffolding session).
- [ ] The generated SKILL.md leads with the install command in both the frontmatter description and the body's STOP-pre-flight section.
- [ ] Cross-references to the new skill land in every other skill whose SKILL.md previously named the gated table or source-glob.

## Files this skill creates / modifies

- `.claude/skills/<skill-name>/SKILL.md` — the gate skill's documentation.
- `.claude/skills/<skill-name>/scripts/install.py` — three-exit-code installer.
- `.claude/skills/<skill-name>/scripts/lint-<table-basename>.py` — markdown table parser + diff-correspondence linter.
- `.claude/skills/<skill-name>/resources/_workflows/<skill-name>-gate.yml` — CI workflow template.
- `.github/workflows/<skill-name>-gate.yml` — installed copy (auto-committed by install.py).
- (For every existing skill that names the table or source-glob): one row added to its SKILL.md decision tree.
