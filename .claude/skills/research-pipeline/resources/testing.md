# Testing the pipeline scripts

Run the test suite before modifying any script in `scripts/`. CI runs it on every PR via `.github/workflows/test-research-pipeline.yml`.

## Running the tests

```bash
cd .claude/skills/research-pipeline

# Everything
python3 -m pytest tests/ -v

# Just unit tests (fast)
python3 -m pytest tests/unit/ -v

# Just integration tests (slower, run the actual shell scripts)
python3 -m pytest tests/integration/ -v

# Specific file
python3 -m pytest tests/unit/test_url_canonicalize.py -v

# One test by name
python3 -m pytest tests/unit/test_url_canonicalize.py::TestCanonicalize::test_idempotent -v
```

## Dependencies

```bash
pip install pyyaml jsonschema pytest
```

The CI workflow installs them automatically.

## Test layout

```
tests/
├── conftest.py                  # shared fixtures: tmp_repo, helpers
├── unit/
│   ├── test_url_canonicalize.py
│   ├── test_classify_text.py
│   ├── test_extract_url.py
│   ├── test_validate_sources.py
│   ├── test_check_source_dirs.py
│   ├── test_check_source_refs.py
│   ├── test_check_fetch_provenance.py
│   ├── test_process_url_list.py
│   └── test_reconcile_source_dir.py
└── integration/
    ├── test_full_lint_pipeline.py    # runs lint-sources.sh end-to-end
    └── test_render_md.py             # runs render-sources-md.sh end-to-end
```

## Writing a new test

Patterns to follow:

### Unit test for a pure function
Import the module directly (conftest adds `scripts/` to sys.path):

```python
from url_canonicalize import canonicalize_url

def test_my_case():
    assert canonicalize_url("https://Example.com/") == "https://example.com/"
```

### Unit test for a script with side effects
Use the `tmp_repo` fixture from conftest. Copy the script into the temp repo, write fixtures, run as subprocess:

```python
def _run(repo, *args):
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("my-script.py", "_config.py", "url_canonicalize.py"):
        (repo / ".claude/skills/research-pipeline/scripts" / name).write_text(
            (src_dir / name).read_text()
        )
    script = repo / ".claude/skills/research-pipeline/scripts/my-script.py"
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True)

def test_my_case(tmp_repo):
    write_skill_md(tmp_repo, default_config_yaml())
    write_sources_json(tmp_repo, {...})
    result = _run(tmp_repo)
    assert result.returncode == 0
```

### Integration test
Mark with `@pytest.mark.integration`. Use `REPO_ROOT = Path(__file__).resolve().parents[5]` to find the real repo (where the actual scripts live), copy them into a temp repo, and exercise the script:

```python
@pytest.mark.integration
def test_pipeline(tmp_path):
    repo = _setup_repo(tmp_path)
    result = subprocess.run(
        ["bash", str(repo / ".claude/skills/research-pipeline/scripts/lint-sources.sh")],
        capture_output=True, text=True, cwd=str(repo),
    )
    assert result.returncode == 0
```

## Conventions

- One test class per concern (`TestCanonicalize`, `TestPointerTo`, etc.).
- One test function per check — descriptive names (`test_id_mismatch_fails`).
- Assert both happy paths and error paths.
- Don't share state between tests; each gets a fresh `tmp_repo`.
- Don't depend on real network access.
- Don't read or write outside the `tmp_path` or `tmp_repo` fixture.

## When a test fails

Look at the actual output:
```bash
python3 -m pytest tests/unit/test_X.py::TestY::test_z -v -s
```

`-s` disables output capture so you see stderr/stdout from the failing test.

The conftest's helpers always produce a self-contained `tmp_repo` you can inspect:
```python
# Inside a failing test, save the repo state for manual inspection:
import shutil
shutil.copytree(tmp_repo, "/tmp/debug-repo", dirs_exist_ok=True)
```

Then `ls -la /tmp/debug-repo/` to see exactly what the script saw.

## Don't skip tests

Before committing a script change:
```bash
bash .claude/skills/research-pipeline/scripts/lint-sources.sh   # ad-hoc smoke
python3 -m pytest tests/ -v                                     # full suite
```

CI will run the full suite on the PR — failing tests block merge.
