# Spec: `sandbox-docker-verification`

- **ID**: SKILL-SPEC-22d151dd2f
- **Source retrospective**: ../2026-06-08-258.md

## Intent

Verify Dockerized-prototype changes by building and running the exact shipped image and compose stack inside the Claude Code web sandbox, instead of reasoning from source or declaring the runtime unavailable. The sandbox has Docker (the daemon just needs starting) plus a documented CA-injection and token recipe, so packaging changes and full dogfood agent runs can be exercised end-to-end. This skill packages that workflow so it is repeatable and an agent never ships a Dockerized change as "unverified, no Docker here."

## Trigger

- Direct: "verify the image", "does the prototype run", "build and test the stack", "test this fix in the sandbox", "did you actually run it".
- Proactive: before declaring any change to a Dockerized component's packaging surface (`Dockerfile`, `entrypoint.sh`, `docker-compose*.yml`, baked assets) verified or merge-ready; and whenever a fix to such a component has been made and the `always test fixes` rule applies.
- Negative: pure unit-level changes with no packaging/runtime surface; a non-Dockerized repo.

## Inputs

- The repo working tree on the branch under test (built as-is, not a hand-rolled approximation).
- The repo's sandbox build recipe (for this project, `docs/HANDOFF.md` §3).
- Optionally a real subscription token (location documented in the recipe; for `software-factory-prototype` at `/home/claude/.claude/remote/.oauth_token`) — only needed for agent-execution paths, not for packaging or pre-agent paths.

## Outputs

- A pass/fail verdict tied to observed behavior (logs, exit codes, container state), written to a `/tmp` report.
- No committed verify-only artifacts (the CA-trusting Dockerfile, compose override, CA file, and `.env` are sandbox-only and must never be committed).
- A concise receipt back to the orchestrator (<25 lines): build result, checks, timeline, defects.

## Workflow

1. Start the daemon: `sudo dockerd >/tmp/dockerd.log 2>&1 &`; poll `docker info` until it responds. (A SessionStart hook may already have done this.)
2. Copy the repo to a `/tmp` working dir (never edit the real tree). Build a **CA-trusting** `Dockerfile.verify`: after each `FROM`, before first network use, install `ca-certificates`, `COPY` the sandbox CA (`cp /etc/ssl/certs/ca-certificates.crt`), and `update-ca-certificates`. Also add `ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` before any npm step (npm uses its own CA bundle). If `FROM` 429s on Docker Hub, pull from a mirror and retag.
3. The image build can exceed a 10-minute foreground call (~13 min for from-source builds). Run it with `run_in_background` and poll the log for success/error; never foreground `sleep`.
4. **Run tokenless checks first** — anything not needing agent auth (image contents, shims, config-load, pre-agent crash/recovery paths). Most packaging verification is tokenless.
5. Only if an agent-execution path must be exercised, write `.env` from the documented token file **without ever printing the token** (verify with `grep -c`), recreate the stack, run the path, then scrub.
6. Reproduce the original failure (for a fix) and confirm the change removes it on identical input; for a feature, exercise the real behavior.
7. Tear down: `docker compose ... down` (or `down -v` if the volume must be clean), remove the `/tmp` working dir (it holds `.env`), confirm the real repo tree is clean and no token-bearing files remain.
8. For anything long-running, do steps 1–7 inside a dispatched subagent that writes a full report to `/tmp` and returns only the concise receipt (keeps the orchestrator context lean).

## Concrete examples

### Example 1: packaging + dogfood (this session)

Built `software-factory-v4:latest` from the branch via `Dockerfile.verify`, verified tokenless that `python3 --version`, `which sftui`, `sftui --dump`, and `test -f /opt/tui/beadview.py` all passed in the running `city` container, then (with the token) ran a `gc bd create` chunk-1 bead that the fleet built end-to-end (~15 min, created → routed → polecat commit → refinery merge), proving the packaging *and* the dogfood loop. Stack torn down, token scrubbed.

### Example 2: a one-line fix, proven-necessary (this session)

To verify the `entrypoint.sh` crash-loop fix: built `:old` (guard restored) and reproduced the bug — `gc start` crash-looped, `RestartCount=5`, exact error `missing bundled pack cache marker; run "gc import install"`; then built `:latest` (fix) and ran the identical half-init-volume sequence — `RestartCount=0`, logs showed `installing/refreshing pack imports`, `gc agent list` healthy. Bug reproduced on old code, removed by the fix on identical input = PASS, tokenless.

## Anti-patterns

- **Declaring "no Docker / can't verify here."** The daemon just needs starting; check before claiming.
- **Verifying a hand-rolled approximation instead of the shipped config.** Build the real Dockerfile/compose from the branch, not a simplified stand-in.
- **Printing or committing the token / `.env` / CA files.** Read the token into `.env` without echoing; keep all verify-only files in `/tmp`; never `git add` them.
- **Foreground-sleeping through a 13-minute build.** Background it and poll.
- **Skipping the failure reproduction.** A fix "passes" only if the bug is shown to reproduce without it and disappear with it.

## Acceptance criteria

- [ ] The exact shipped image+compose from the branch is built and run (not a proxy).
- [ ] For a fix, the original failure is reproduced on the old code and shown gone on the fixed code.
- [ ] Tokenless paths are exercised without any token; token paths never leak the token.
- [ ] The stack is torn down and no verify-only or token-bearing files are committed or left behind.
- [ ] A concise receipt with observed evidence (logs/exit codes/state) is returned.

## Files this skill creates / modifies

- `/tmp/<verify-dir>/Dockerfile.verify`, `docker-compose.sandbox.yml`, `sandbox-ca.crt`, `.env` — sandbox-only; never committed.
- `/tmp/<verify>-report.md` — the full findings (ephemeral).
- No changes to the repo working tree.
