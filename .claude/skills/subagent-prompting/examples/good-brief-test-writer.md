# Good brief example: iter-2 test-writer

This is a real subagent brief from the session. It produced 110
passing tests in one shot, hit all the explicit pinning targets, and
came in at 92% coverage. Notable strengths:

- Self-contained: subagent didn't need clarification.
- Concrete success criteria (test count + coverage targets).
- Explicit pinning targets per section (A through H).
- Known-issues section warning about jsonschema env config.
- Word-budget on the report.
- Explicit don'ts.

---

## Original brief (lightly edited for readability)

You are expanding the test suite for the agent-job-protocol POC at
`/home/user/poc-github-ai-sandbox`. This is iteration 2 step 3.

### Current state
- Branch: `claude/start-sandbox-yolo-check-kjFPc` (in sync with main)
- 67 tests pass at 87% coverage (iter 1 baseline)
- Spec: `SPEC.md`
- Iter 2 just landed impl tightening (PR #3 merged). New behaviors
  to cover:
  - `unsupported_version` parse_error path in handler
  - `unknown_command` is now terminal `error` (was `parse_error`)
  - 40-char-only SHA pattern in envelope schema
  - `GitHubClient.delete_branch` (Protocol + InMemory impl)
  - `merge.py` deletes subagent branches by default; returns `deleted` list
  - `poll.py` accepts optional `heartbeat` callable
  - `main()` stubs print env-var requirements and exit 0

### Goals for iter 2 tests
[8 sections of pinning targets, each with 2-5 specific test names
and assertions]

### Approach
1. Read the existing tests/conftest.py and tests/unit/* to understand
   fixtures and patterns.
2. Update permissive assertions per Section A (modify existing tests).
3. Add new test files / cases per B-H.
4. Run `python -m pytest tests/ -v --tb=short 2>&1 | tail -60` to
   confirm pass status.
5. If any test fails because of an actual impl bug (not your test
   bug), DO NOT fix the impl — that is iter 3's job. Mark such tests
   with `@pytest.mark.xfail(reason="impl bug, see iter 3", strict=False)`
   so they don't stop the suite.
6. Run coverage: `python -m pytest tests/ --cov=.agent --cov=skills --cov-report=term-missing`.
   Aim for >=90% line coverage overall.

### When done
1. Commit: `git add -A && git commit -m "test(iter2): expand pinning, new-behavior, build, e2e, edge cases" && git push`
2. Open PR via `mcp__github__create_pull_request`:
   - title: "test(iter2): expanded test coverage"
   - base: main
   - head: claude/start-sandbox-yolo-check-kjFPc
   - body: summary of what was added (counts), pass/fail, coverage delta
3. Report back: PR number, total test count, pass/fail count, coverage
   %, any xfail tests added with their reason.

### Env note
If pytest can't find jsonschema: `uv tool install pytest --with jsonschema --with pytest-cov --force`.

---

## Why this worked

- **Zero ambiguity on success criteria.** "67 → >=90% coverage" is
  measurable.
- **Per-section enumeration.** A through H with named tests prevents
  scope drift.
- **Failure-mode handling** (xfail on real impl bugs) means the
  subagent can make progress without fixing things outside its scope.
- **Known traps.** The jsonschema env note saved a 3-minute confusion.
- **Explicit deliverable shape.** Subagent knew exactly what
  commit + PR to produce.
