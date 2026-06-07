# Spec: `probe-injected-exec-environment`

- **ID**: SKILL-SPEC-16761ebad2
- **Source retrospective**: ../2026-06-07-11.md

## Intent

When you must write a script that runs inside an environment some host injects (unknown working directory, unknown environment variables, unknown PATH, an unknown set of helper vars), reasoning about that environment from source is a hypothesis, not a fact. This skill says: first ship a throwaway probe that dumps the real cwd and environment (and, if cheap, exercises the one risky operation), read the actual values, then write the real script against them. It earns its place because in this session a one-line probe order revealed that a city-level gc exec order runs with cwd=/workspace/city, PACK_DIR pointing at the city dir rather than the source pack, and RIG1_NAME/RIG2_NAME plus the managed-Dolt GC_DOLT_* vars already exported - facts that determined the script's whole shape and would have been guessed wrong from the source.

## Trigger

- Direct: "write the order/hook/script that runs in X", where X is a controller, CI runner, git hook, cron/order dispatcher, container entrypoint, or any host that invokes your code with an environment it controls.
- Proactive: the moment you're about to write a script whose correctness depends on injected `cwd`, env vars, helper binaries, or PATH that you have not directly observed in *that* invocation context — especially if you've only read the host's source.
- Negative: skip when you fully control the invocation (you write both the caller and the callee), or the environment is trivially known and stable.

## Inputs

- A cheap way to register and run a throwaway unit in the target host (e.g. a `trigger = "manual"` order you invoke with `gc order run`, a no-op CI job, a temporary hook).
- The single risky operation the real script will perform (a cross-scope command, a write, a network call), so the probe can exercise it once.

## Outputs

- A printed dump of the real invocation environment: `pwd`, the relevant `env` subset, available helper vars/binaries.
- A confirmed answer to "does my one risky operation work from here?" before the real script depends on it.
- A throwaway artifact that is deleted before shipping (never committed).

## Workflow

1. Identify the unknowns the real script depends on: working directory, which env vars are present, whether helper binaries/credentials are wired, whether a flag/feature is on.
2. Write a **throwaway** probe in the target host's own mechanism (manual trigger, no-op job) whose body is just `echo "CWD=$(pwd)"; env | grep -E '<relevant prefixes>' | sort`.
3. Run it in the *real* context (not a hand-rolled approximation) and read the actual values.
4. If the real script has one risky operation (e.g. a cross-scope mutation), add a second throwaway probe that performs exactly that operation and verify its effect, plus the negative case (it must not touch the wrong thing).
5. Write the real script against the observed values — not the source-derived guesses. Note any surprise (e.g. an env var meaning something other than its name implies).
6. Delete the throwaway probe(s) before building the shippable artifact.

## Concrete examples

### Example 1: a gc controller `exec` order (this session)

Before writing `route-rig-tasks`, a `trigger = "manual"` probe order with body `echo CWD=$(pwd); env | grep -E '^(GC_|PACK_DIR|RIG)' | sort` was run via `gc order run _probe-env`. It revealed `cwd=/workspace/city`, `PACK_DIR=/workspace/city` (the city dir, **not** the source pack — so referencing `$PACK_DIR/assets/scripts/...` would have broken), `GC_RIG=""`, and that `RIG1_NAME`/`RIG2_NAME` plus all `GC_DOLT_*` were already exported. A second probe (`_probe-route`) ran the candidate list-filter + `gc sling` and proved the sling worked from the city-scope env and that `sh` (dash) — not bash — runs the body (`set -o pipefail` errored, exit 2). Both surprises would have been guessed wrong from source; the real order was written correctly the first time and both probes were deleted.

### Example 2: a CI job's shell environment (generalization)

Before relying on a tool being on PATH in a CI runner, add a one-off job step `echo "PATH=$PATH"; which mytool; env | sort`. It frequently reveals the tool is absent in that image, or PATH differs from the login shell, or a secret env var is named differently than the docs claim — caught in a no-op step instead of a red pipeline three commits later.

## Anti-patterns

- **Referencing an injected var by its assumed meaning.** `PACK_DIR` sounded like "the source pack dir" but pointed at the city dir; using it for a script path would have failed silently. Read the value, don't assume it.
- **Assuming the interpreter.** The exec ran under `sh`/dash, not bash; `set -o pipefail` is a bashism that errored. The probe surfaced this before it was buried in the real script.
- **Probing a hand-rolled approximation instead of the real host.** Run the probe through the *actual* dispatcher (`gc order run`), not a local `bash -c` that doesn't inject the same env.
- **Committing the probe.** It is scaffolding; delete it before shipping the real artifact.

## Acceptance criteria

- [ ] The real invocation environment (cwd + relevant env vars + interpreter) is observed via a probe run in the actual host, not inferred from source.
- [ ] Any one risky operation the real script performs is exercised once in the probe, including its negative case.
- [ ] Every source-derived assumption that the probe contradicted is recorded.
- [ ] All throwaway probes are deleted before the shippable artifact is built; none are committed.

## Files this skill creates / modifies

- A throwaway probe artifact in the host's own format (e.g. `pack/orders/_probe-*.toml`), created then deleted — never committed.
