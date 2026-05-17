# GitHub Actions

Three workflows ship with this skill. They live in `.github/workflows/` after `install-workflows.py` runs.

## `regen-sources-md-auto.yml`

**Trigger:** push to `main` that changes `reference-only/sources.json`.

**What it does:**
1. Checks out the repo
2. Validates the config block in SKILL.md
3. Validates `sources.json` against schema + structural rules
4. Normalizes `sources.json` (sort keys + sort by id + pretty-print)
5. Renders `sources.md` via `render-sources-md.sh`
6. Commits any diff with `[skip ci]` and pushes back to main

The `[skip ci]` prevents an infinite loop (the auto-commit doesn't re-fire the workflow). The path filter (`paths: ['reference-only/sources.json']`) means the workflow doesn't run for unrelated changes.

## `regen-sources-md-manual.yml`

**Triggers:**
- Push to any branch that changes `reference-only/.regen-trigger`
- `workflow_dispatch` from the Actions UI

**What it does:**
Same as auto, plus:
- Deletes the `.regen-trigger` file as part of its commit

**When to use:**
- The auto workflow failed (e.g., transient infra issue) and you want to manually force a regen after fixing
- You're debugging on a feature branch and want to preview the MD without merging to main
- You're testing changes to the rendering script

**How to trigger via tickle file:**
```bash
touch reference-only/.regen-trigger
git add reference-only/.regen-trigger
git commit -m "Trigger sources.md regen"
git push
# Wait ~30 seconds. The action runs, regenerates the MD, deletes the trigger,
# and pushes. You'll see two extra commits: yours and the bot's.
```

The trigger file should be gone within a minute. If it isn't, check the Actions tab — the workflow probably failed. Read the error and fix.

**How to trigger via GitHub UI:**
1. Go to the Actions tab
2. Select "Regenerate sources.md (manual)"
3. Click "Run workflow", pick a branch, "Run workflow"

## `test-research-pipeline.yml`

**Triggers:**
- Push or PR that changes anything under `.claude/skills/research-pipeline/scripts/`, `.claude/skills/research-pipeline/tests/`, or `reference-only/sources.schema.json`

**What it does:**
Runs `pytest tests/unit/ tests/integration/`. Fails the PR if any test fails.

Required to merge. If you broke a test, fix it. If you intentionally changed behavior, update the test.

## Installing the workflows

After cloning the repo (or pulling in a new branch):

```bash
ls .github/workflows/regen-sources-md-auto.yml \
   .github/workflows/regen-sources-md-manual.yml \
   .github/workflows/test-research-pipeline.yml 2>/dev/null | wc -l
```

If less than 3, run:
```bash
python .claude/skills/research-pipeline/scripts/install-workflows.py
```

This copies the templates from `resources/_workflows/`, substitutes `__SKILL_PATH__` for the actual path from config, writes to `.github/workflows/`, and commits.

Flags:
- `--force` overwrite existing workflow files
- `--dry-run` show what would happen without modifying
- `--no-commit` install but don't auto-commit

## Inspecting workflow runs

```bash
# Recent runs (assumes gh CLI; via MCP github tools in skill contexts)
mcp__github__list_workflow_runs ...
```

In this project's setup, use the GitHub MCP tools to check workflow status. See the skill's pre-flight check for how to verify workflows are installed.

## Editing a workflow

1. Edit the template in `resources/_workflows/<name>.yml`.
2. Reinstall:
   ```bash
   python scripts/install-workflows.py --force
   ```
3. Commit both the template and the regenerated workflow file in the same commit.

The template uses `__SKILL_PATH__` as a placeholder. The installer substitutes it. Don't hardcode the path in the template.

## What the workflows commit

`regen-sources-md-auto.yml` and `regen-sources-md-manual.yml` use the `github-actions[bot]` identity:

```
auto: regenerate sources.md from sources.json [skip ci]
```

Or:

```
regen: sources.md (manual trigger) [skip ci]
```

Both touch only `reference-only/sources.json` (normalized) and `reference-only/sources.md` (rendered). They don't touch the actual source files or anything else.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Workflow doesn't fire on push | Path filter didn't match | Verify your commit actually changed `reference-only/sources.json` |
| Workflow fires but fails at "Validate schema" | `sources.json` invalid | Read the error; fix locally; re-push |
| Workflow fires but fails at "Normalize JSON" | jq error or empty JSON | Verify `sources.json` parses as JSON |
| `sources.md` doesn't update | Workflow ran but no diff to commit | Check that your edit actually changed observable fields |
| Trigger file isn't deleted | Manual workflow failed before the delete step | Check workflow logs; fix the underlying issue |
