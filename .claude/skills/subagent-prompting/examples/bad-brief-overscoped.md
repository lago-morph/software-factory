# Bad brief example: overscoped lock-vs-bot fix

This brief requested too much work in a single dispatch. The subagent had to
hold ~11 deliverables in working memory simultaneously, span 15-20 files
across multiple architectural layers, and ran out of budget mid-task. Recovery
succeeded only because the agent had committed local changes early — but the
dispatcher had to manually push and complete the PR, and some deliverables
were left undone.

---

## The problematic brief (outline)

```
You are implementing the lock-vs-bot workflow fix for the agent-job-protocol
POC. This is a comprehensive update addressing the GitHub lock feature
interacting with bot-initiated writes.

### What to build
1. Update config.py — add LOCK_EXEMPT_BOTS list and LOCK_CHECK_INTERVAL setting
2. Update config schema (JSON Schema) — add new fields with validation
3. Update batch_handler.py — detect locked repos before processing
4. Update batch_handler.py — skip non-exempt bots when repo is locked
5. Update lock_detector.py — new module for lock-state polling
6. Update merge.py — pass lock state to downstream handlers
7. Update poll.py — surface lock events in the heartbeat stream
8. Write unit tests for lock_detector (happy path, locked, rate-limited)
9. Write integration tests for batch_handler lock-skip behavior
10. Write scenario doc: "what happens when a repo goes locked mid-session"
11. Amend SPEC.md §4 and §7 to describe lock behavior
11. Amend SPEC.md §9 to add lock-state to the state machine diagram

### Don't
- Don't break existing tests (currently 110 passing)

### When done
Commit everything, push, open a PR.
```

---

## What went wrong

**Too many deliverables.** 11 numbered items across code, tests, docs, and
spec amendments. The subagent had to context-switch between implementation
mode, test-writing mode, documentation mode, and spec-editing mode — each
requires a different mental model of the codebase.

**Too many files.** 15-20 files across config, handler, detector, merge,
poll, tests, scenario docs, and spec. Reading all of them up front consumed a
large portion of the subagent's context window before any writing started.

**Too many architectural layers.** Config schema validation, runtime handler
logic, test infrastructure, narrative documentation, and formal spec
amendments are four different layers. Changing all four in one dispatch means
a bug in layer 1 invalidates work in layers 2-4.

**No early commit instruction.** The brief didn't say "commit after the code
changes, before starting the docs." When the subagent ran out of budget after
completing ~7 of 11 items, the partial work was local but unpushed. The
dispatcher recovered it manually, but this took 20 minutes.

**Vague deliverable.** "Commit everything, push, open a PR" doesn't say what
to put in the PR body or what test count to confirm.

---

## The fix: split into 3 sequential focused briefs

### Brief A — code changes (~4 files, 10-20 min)

```
You are implementing lock detection for the agent-job-protocol POC.

## What to build
1. New file: src/lock_detector.py — LockDetector class with poll() and
   is_locked() methods. Success: class instantiates, poll() calls GitHub API.
2. Update src/config.py — add LOCK_EXEMPT_BOTS (list[str], default []) and
   LOCK_CHECK_INTERVAL (int, default 60). Success: config loads without error.
3. Update src/config_schema.json — add lock_exempt_bots and
   lock_check_interval with type validation.
4. Update src/batch_handler.py — check LockDetector before processing;
   skip non-exempt bots. Success: handler skips processing when locked.

## Don't
- Don't write tests (Brief B handles tests)
- Don't update SPEC.md (Brief C handles spec)
- Don't refactor unrelated code
- Don't break existing 110 tests

## Validation
`python -m pytest tests/ -v --tb=short 2>&1 | tail -20`
Confirm 110 still pass. If any break, fix before committing.

## Deliverables
1. git add -A && git commit -m "feat: lock detection + batch handler skip"
2. git push -u origin <branch>
3. mcp__github__create_pull_request — title: "feat: lock detection", base: main
4. Report: PR number, files changed, line counts, 110 tests still passing.

## Time budget
~20 minutes. If stuck on the GitHub API call shape, check gh api /repos/{owner}/{repo}.
```

### Brief B — tests (~pattern-based, 10 min)

Dispatch after Brief A's PR is merged.

```
You are writing tests for the lock detection code added in PR #<N>.

## What to write
1. tests/unit/test_lock_detector.py — 8 tests covering:
   - happy path (unlocked repo): poll() returns False
   - locked repo: poll() returns True
   - rate-limited API: poll() raises LockDetectorError
   - is_locked() before first poll: raises RuntimeError
   - LockDetector with exempt bot: skips check
2. tests/unit/test_batch_handler_lock.py — 4 tests covering:
   - handler skips non-exempt bot when locked
   - handler processes exempt bot when locked
   - handler processes all bots when unlocked
   - handler surfaces LockDetectorError as batch error

## Don't
- Don't modify implementation files
- Don't break existing 110 tests

## Validation
`python -m pytest tests/ -v --tb=short 2>&1 | tail -30`
Confirm >=122 pass (110 existing + 12 new).

## Deliverables
PR with test files only. Report: PR number, test count delta.
```

### Brief C — spec amendments (~2-3 sections, 10 min)

Dispatch after Brief B's PR is merged.

```
You are amending SPEC.md to document the lock-detection behavior added in
PRs #<N> and #<M>.

## What to update
1. SPEC.md §4 (GitHub integration) — add subsection "Lock detection":
   explain LOCK_EXEMPT_BOTS, LOCK_CHECK_INTERVAL, behavior when locked.
2. SPEC.md §7 (batch processing) — add one paragraph on skip-when-locked.
3. SPEC.md §9 (state machine) — add "locked" as a transient state with
   transitions to "skipped" and "resumed".
4. New file: docs/scenarios/lock-mid-session.md — 200-400 word narrative
   of what happens when a repo goes locked mid-session (timeline + recovery).

## Don't
- Don't touch implementation files
- Don't rewrite sections unrelated to lock detection

## Deliverables
PR with SPEC.md and docs/ changes. Report: PR number, sections amended.
```

---

## The general heuristic

Split a brief into multiple sequential dispatches when it has:
- **More than 8 deliverables** — subagent working memory degrades beyond ~8
  items.
- **More than 10 files to modify** — reading them all consumes context before
  writing starts.
- **More than 3 architectural layers** — each layer switch requires a
  different mental model.

A good split keeps each brief under 20 minutes, touches ≤5 files, and has a
single clear output (code, tests, or docs — not all three).
