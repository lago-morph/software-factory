# Spec: `verify-container-image-in-restricted-sandbox`

- **ID**: SKILL-SPEC-e16f11e633
- **Source retrospective**: ../2026-06-06-1.md

## Intent

Build and boot a container image inside a network/TLS-restricted sandbox to catch real, laptop-affecting bugs before shipping, without polluting the committed Dockerfile or spending paid API/subscription tokens. The skill builds a throwaway copy of the Dockerfile patched only to trust the sandbox's TLS-inspection CA, boots the image with no auth token so agent processes fail auth harmlessly, and exercises the real entrypoint far enough to validate wiring (servers start, schemas init) — surfacing bugs like shared-library version mismatches and removed CLI flags that a build-only check would miss.

## Trigger

Activate when: you have authored or modified a Dockerfile / docker-compose meant to run on a user's machine and want to verify it before shipping; the working environment is a sandbox with a TLS-inspection proxy that breaks in-build HTTPS (`curl` exit 60, `git` certificate failures); the image runs agents or services that would otherwise spend paid API/subscription tokens on each verification pass. Direct phrases: "verify the image builds and boots", "does the container actually come up", "test the Dockerfile here before we ship it". Negative triggers: a plain build-only smoke test where boot behavior does not matter, or an environment with unrestricted egress where no CA patch is needed (still apply the tokenless-boot half).

## Inputs

- The committed `Dockerfile` and `docker-compose.yml` (or equivalent) under verification.
- The sandbox's TLS-inspection CA certificate (path or PEM contents).
- The entrypoint's expected wiring contract: which servers must start, which schemas/ports must come up.
- Knowledge that no auth token will be supplied (the verification runs tokenless by design).

## Outputs

- A pass/fail verdict on the image's build and boot wiring.
- A list of concrete bugs found (with the exact error text and the fix).
- A throwaway patched Dockerfile used only for verification — **never committed**.
- No modification to the committed Dockerfile; no tokens spent.

## Workflow

1. Copy the committed Dockerfile to a throwaway path (e.g. `Dockerfile.sandbox-verify`).
2. Patch the throwaway copy **only** to trust the sandbox TLS-inspection CA (add the CA, run `update-ca-certificates`); change nothing else.
3. Build from the throwaway copy. If the build backgrounds (`docker build ... &`), do not trust a wrapper "completed" signal — confirm true completion by checking the build process and the resulting image artifact.
4. Boot the image / compose group with **no auth token** (omit `CLAUDE_CODE_OAUTH_TOKEN` / `ANTHROPIC_API_KEY`). Agent processes will fail auth harmlessly.
5. Assert on the **wiring**, not on agent output: servers are up, ports are bound, schemas/tables are initialized, the entrypoint progressed past each provisioning step.
6. Capture any runtime failures (exit codes, missing-library errors, removed-flag errors) and fix the **committed** Dockerfile (not the throwaway).
7. Re-run steps 1–6 until the boot wiring is green. Discard the throwaway copy; confirm the committed Dockerfile carries no sandbox-specific hacks.

## Concrete examples

### Example 1: ICU SONAME mismatch caught at boot

The committed Dockerfile compiled `gc` in a Debian bookworm builder (ICU 72) and ran it on an ubuntu noble runtime (ICU 74). A build-only check passed — the image built fine. Booting the image tokenless in the sandbox surfaced the real failure: `gc` exited 127 on first invocation because the loader could not find `libicui18n.so.72` (noble ships `.so.74`). The fix landed in the committed Dockerfile: build `gc` on the same `ubuntu:24.04` base as the runtime stage. This bug would have hit the user's laptop identically, so catching it in-sandbox saved a shipped-broken package.

### Example 2: tokenless boot catches removed flags and a missing catalog entry

Booting the compose group with no `CLAUDE_CODE_OAUTH_TOKEN` let the agents fail auth instantly while the rest of the stack initialized fully. That full boot path surfaced two more bugs: (a) dolt 2.1.4 had **removed** `--user`/`--password` from `sql-server`, so the bead-store service failed to start until the entrypoint switched to `DOLT_ROOT_HOST=%` for cross-container root; (b) gc 1.1.1 refused to resolve providers until a `[providers.claude] base="builtin:claude"` catalog entry was added to the config. Both are boot-time failures invisible to a build-only check, and both were found and fixed without spending a single subscription token.

## Anti-patterns

- **Putting the CA hack in the committed Dockerfile.** Trusting the sandbox's TLS-inspection CA in the shipped file contaminates every laptop user with an environment-specific trust anchor and a security smell — patch a throwaway copy instead.
- **Build-only verification.** "The image builds" hides SONAME mismatches, removed CLI flags, and missing config entries that only appear on first invocation. Always boot.
- **Booting with a real token to verify.** Spends the user's subscription on every pass (this session needed ~6 passes). Boot tokenless and assert on wiring.
- **Trusting a wrapper's "completed exit 0" for a backgrounded build.** The `&` detaches the build; the wrapper reports the shell returning, not the build finishing. Check the process and the image artifact.

## Acceptance criteria

- [ ] The committed Dockerfile contains zero sandbox-specific hacks after verification.
- [ ] Verification boots the image and asserts on at least one runtime wiring property (server up / port bound / schema present), not just on a successful build.
- [ ] The verification spends no API/subscription tokens (no auth token supplied).
- [ ] At least one class of runtime-only bug (shared-library version, removed flag, missing config entry) is detectable by this procedure.

## Files this skill creates / modifies

- `Dockerfile.sandbox-verify` (or similar) — throwaway, CA-patched copy used only for in-sandbox verification; never committed.
- The committed `Dockerfile` — modified only to fix real bugs found at boot (e.g. base-image alignment), never with sandbox hacks.
