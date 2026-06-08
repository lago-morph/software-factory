# Skill: sandbox-docker-verification

Verify Dockerized-prototype changes by building and running the **exact shipped
image and compose stack inside the Claude Code web sandbox**, instead of
reasoning from source or declaring the runtime unavailable. The sandbox has
Docker (the daemon just needs starting) plus a documented CA-injection and token
recipe, so packaging changes and full dogfood agent runs can be exercised
end-to-end. This skill packages that workflow so it is repeatable and an agent
never ships a Dockerized change as "unverified, no Docker here."

This skill operationalizes two `AGENTS.md` rules — `always test fixes — no
exceptions, ever` and `read the full handoff/environment doc before claiming an
environment limitation` — for the specific case of Dockerized components.

---

## When to use

Activate when **any** apply:

- **Direct**: "verify the image", "does the prototype run", "build and test the
  stack", "test this fix in the sandbox", "did you actually run it".
- **Proactive**: before declaring any change to a Dockerized component's
  packaging surface (`Dockerfile`, `entrypoint.sh`, `docker-compose*.yml`, baked
  assets) verified or merge-ready; and whenever a fix to such a component has
  been made (the always-test-fixes rule then requires this).

Do **not** use for: pure unit-level changes with no packaging/runtime surface, or
a non-Dockerized repo.

The reference repo for this skill is
[`software-factory-prototype`](https://github.com/lago-morph/software-factory-prototype),
whose `HANDOFF.md` (under `docs/`) §3 is the authoritative sandbox build/test recipe. Read
it first; this skill is the procedure around it.

---

## Inputs

- The repo working tree on the branch under test — built **as-is**, not a
  hand-rolled approximation.
- The repo's sandbox build recipe (`HANDOFF.md` (under `docs/`) §3 for the prototype).
- Optionally a real subscription token (location in the recipe; for the
  prototype, `/home/claude/.claude/remote/.oauth_token`) — needed **only** for
  agent-execution paths, not for packaging or pre-agent paths.

## Outputs

- A pass/fail verdict tied to observed behavior (logs, exit codes, container
  state).
- **No committed verify-only artifacts** — the CA-trusting Dockerfile, compose
  override, CA file, and `.env` are sandbox-only and must never be committed.
- When run via a subagent (recommended for long runs): a full report on disk and
  a concise (<25-line) receipt to the orchestrator.

---

## Workflow

1. **Start the daemon**: `sudo dockerd >/tmp/dockerd.log 2>&1 &`; poll
   `docker info` until it responds. (A SessionStart hook may already have done
   this.) Never conclude "no Docker" without this step.
2. **Build a CA-trusting verify image.** Copy the repo to a `/tmp` working dir
   (never edit the real tree). In `Dockerfile.verify`, after **each** `FROM`,
   before first network use, insert: install `ca-certificates`, `COPY` the
   sandbox CA (`cp /etc/ssl/certs/ca-certificates.crt <ctx>/sandbox-ca.crt`),
   `update-ca-certificates`. **Also** add
   `ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` before any npm
   step (npm uses its own CA bundle, else `SELF_SIGNED_CERT_IN_CHAIN`). If a
   `FROM` 429s on Docker Hub, pull from a mirror (e.g. AWS ECR public ubuntu)
   and retag locally.
3. **Background the build.** A from-source build can exceed a 10-minute
   foreground Bash call (~13 min). Run it with `run_in_background` and poll the
   log for success/error markers; never foreground `sleep`.
4. **Run tokenless checks first.** Anything not needing agent auth — image
   contents, shims, config-load, and pre-agent crash/recovery paths — runs with
   no token. Most packaging verification is tokenless. Use a sandbox compose
   override and `--no-build` to run the prebuilt image.
5. **Token paths only if required.** If an agent-execution path must run, write
   `.env` from the documented token file **without ever printing the token**
   (verify with `grep -c '^CLAUDE_CODE_OAUTH_TOKEN=' .env`), recreate the stack,
   run the path, then scrub `.env`.
6. **Reproduce, then confirm.** For a fix: reproduce the original failure (e.g.
   build the pre-fix variant) and confirm the change removes it on identical
   input. For a feature: exercise the real behavior and observe it.
7. **Tear down.** `docker compose ... down` (or `down -v` if the volume must be
   clean), remove the `/tmp` working dir (it holds `.env`), confirm the real
   repo tree is clean (`git status`) and no token-bearing files remain.
8. **For long runs, dispatch a subagent** to do steps 1–7, write a full report
   to `/tmp`, and return only the concise receipt — this keeps the
   orchestrator's context lean (see
   [`subagent-prompting`](../subagent-prompting/SKILL.md)).

---

## Concrete examples

### Example 1 — packaging + dogfood

Built the prototype image from the branch via `Dockerfile.verify`; verified
tokenless that `python3 --version`, `which sftui`, `sftui --dump`, and
the baked `beadview.py` was present in the running `city` container; then (with
the token) ran a `gc bd create` chunk-1 bead that the fleet built end-to-end
(~15 min: created → routed → polecat commit → refinery merge), proving the
packaging *and* the dogfood loop. Stack torn down, token scrubbed.

### Example 2 — a one-line fix, proven-necessary

To verify an `entrypoint.sh` crash-loop fix: built an `:old` image with the bug
restored and reproduced it (`gc start` crash-loop, `RestartCount=5`, exact error
`missing bundled pack cache marker; run "gc import install"`); then built the
fixed image and ran the identical half-init-volume sequence —
`RestartCount=0`, logs showed recovery, `gc agent list` healthy. Bug reproduced
without the fix and gone with it = PASS, entirely tokenless.

---

## Anti-patterns

- **Declaring "no Docker / can't verify here."** The daemon just needs starting;
  probe before claiming. (Violates the read-the-full-doc and always-test rules.)
- **Verifying a hand-rolled approximation instead of the shipped config.** Build
  the real Dockerfile/compose from the branch.
- **Printing or committing the token / `.env` / CA files.** Read the token into
  `.env` without echoing; keep verify-only files in `/tmp`; never `git add` them.
- **Foreground-sleeping through a 13-minute build.** Background it and poll.
- **Skipping the failure reproduction.** A fix "passes" only if the bug is shown
  to reproduce without it and disappear with it.

---

## Acceptance criteria

- [ ] The exact shipped image+compose from the branch is built and run (not a proxy).
- [ ] For a fix, the original failure is reproduced on the old code and shown gone on the fixed code.
- [ ] Tokenless paths run without any token; token paths never leak the token.
- [ ] The stack is torn down and no verify-only or token-bearing files are committed or left behind.
- [ ] A verdict backed by observed evidence (logs/exit codes/state) is reported.

---

## See also

- The prototype's `HANDOFF.md` (under `docs/`) §3 — the authoritative sandbox build/test recipe.
- [`verify-the-shipped-config-not-a-proxy`](../verify-the-shipped-config-not-a-proxy/SKILL.md) — the principle this skill enforces for Docker.
- [`subagent-prompting`](../subagent-prompting/SKILL.md) — for dispatching the long-running verification.
- Source: [`SKILL-SPEC-22d151dd2f`](../../../retrospective/2026-06-08-258/SKILL-SPEC-22d151dd2f-sandbox-docker-verification.md).
