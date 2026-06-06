# Spec: `dockerize-gas-city`

- **ID**: SKILL-SPEC-f62885124d
- **Source retrospective**: ../2026-06-06-1.md

## Intent

Package a Gas City deployment as one self-contained, laptop-portable Docker image plus compose that a user brings up with `docker compose up --build` and only a Claude subscription. The skill captures the hard-won wiring: compile `gc` from source on a base matching the runtime's ICU/glibc, install dolt/bd/node/claude-code/tmux/socat, pre-ack the three interactive-claude onboarding dialogs and set IS_SANDBOX for root, run a gc-managed Dolt bead store bridged to a host/port with socat, and authenticate agents with a subscription OAuth token rather than an API key.

## Trigger

Activate when: the task is to produce a runnable Gas City prototype a non-developer can bring up locally; the user wants "one image", "docker compose up and it works", or laptop portability without pre-staged binaries; the deployment must run the gastown pack (which depends on `gc bd`). Direct phrases: "dockerize gas city", "package the city as a container", "make it run on my laptop with just Docker". Negative triggers: a deployment targeting an already-provisioned host with pre-installed `gc`/dolt (no need to compile from source), or a non-gastown workload that does not require the bd-contract bead store.

## Inputs

- The target `gc` version (this session: 1.1.1) and the gastown pack to import.
- The runtime base image (this session: `ubuntu:24.04`), which fixes the ICU/glibc the compiled `gc` must match.
- A `city.toml` template, rig definitions, and `.env` for the deployment.
- A Claude **subscription** OAuth token (`CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`) — not an API key.
- Target platform (this session: Windows/amd64 — arm was dropped).

## Outputs

- A multi-stage `Dockerfile` that compiles `gc` from source and installs dolt/bd/node/claude-code/tmux/socat.
- A `docker-compose.yml` and an entrypoint that renders city.toml, provisions local rigs, bridges the bead store, and starts `gc`.
- A gastown-importing pack, `city.toml`, `.gc/site.toml`, and `.env`.
- A self-contained image (no pre-staged host binaries) that boots with `docker compose up --build`.

## Workflow

1. Choose the runtime base image first; compile `gc` from source in a builder stage on the **same** base (same distro release) so ICU/glibc SONAMEs match the runtime stage.
2. In the runtime stage install dolt, bd, node, claude-code, tmux, and socat.
3. Configure the bead store as a **gc-managed Dolt** SQL server; bridge it with socat to a compose-reachable host/port (e.g. `0.0.0.0:3307`). Do **not** pin `[dolt].port` (it breaks gc 1.1.1's managed lifecycle); use the bridge to republish the loopback-bound managed port. Use `DOLT_ROOT_HOST=%` for cross-container root (dolt 2.1.4 removed `--user`/`--password`).
4. Add a `[providers.claude] base="builtin:claude"` catalog entry (gc 1.1.1 requires it).
5. Pre-ack the three interactive claude-code onboarding dialogs and set `IS_SANDBOX` for root so the entrypoint does not block on prompts.
6. Author the entrypoint to render `city.toml`, move deprecated `workspace.name` to `.gc/site.toml`, provision local rigs, start the managed Dolt + socat bridge, then `gc start`.
7. Author the gastown-importing pack and `.env`; supply agent auth via `CLAUDE_CODE_OAUTH_TOKEN` (subscription), never `ANTHROPIC_API_KEY`.
8. Verify build + tokenless boot in-sandbox (see the `verify-container-image-in-restricted-sandbox` skill) before shipping.

## Concrete examples

### Example 1: multi-stage Dockerfile shape (base-matched CGO compile)

Builder stage and runtime stage both start `FROM ubuntu:24.04`. The builder compiles `gc` from source (CGO, links ICU by SONAME); the runtime stage `COPY --from=builder` the `gc` binary and installs dolt/bd/node/claude-code/tmux/socat. Because both stages share the noble base (ICU 74), the copied `gc` loads cleanly — the earlier bookworm-builder/noble-runtime split produced an ICU-72-vs-74 SONAME failure (exit 127). This compiles everything inside the image: the laptop needs only Docker, unlike the earlier gascity-prototype which `COPY`ed host-built binaries and was therefore not laptop-portable.

### Example 2: managed-Dolt + socat bead store

The bead store is a gc-managed Dolt SQL server. gc binds it on loopback at a hashed port and rejects host `0.0.0.0`; pinning `[dolt].port` to force a stable port breaks gc 1.1.1's managed lifecycle. The resolution: leave gc to manage Dolt, and run a socat bridge that republishes the loopback port to `0.0.0.0:3307` so the whole compose group can reach the bead store by host/port over a non-synced data file. Cross-container root works via `DOLT_ROOT_HOST=%` because dolt 2.1.4 removed `--user`/`--password` from `sql-server`. The user selected this option over a dedicated external Dolt service via AskUserQuestion, after the external route hit a gc external-endpoint bootstrap circularity.

### Example 3: claude onboarding acks + tokenless boot

The entrypoint pre-acks the three interactive claude-code onboarding dialogs and sets `IS_SANDBOX` so root can run claude non-interactively. For verification the agents are left tokenless so they fail auth harmlessly while the rest of the city boots — proving the full wiring without spending the user's Claude Max subscription.

## Anti-patterns

- **File provider for the bead store.** The gc-native `file` provider disables `gc bd`, and the gastown pack makes ~368 `gc bd` calls — so file cannot run the proven gastown fleet.
- **Pinning `[dolt].port`.** Forcing the managed Dolt port breaks gc 1.1.1's managed lifecycle; bridge the hashed loopback port with socat instead.
- **Pre-staged / host-built binaries.** `COPY`ing host-compiled binaries (as the earlier gascity-prototype did) is not laptop-portable — build everything in the image.
- **Mismatched CGO base.** Compiling `gc` on a different distro release than the runtime yields a SONAME load failure (ICU 72 vs 74).
- **Assuming an API key.** A subscription user has no `ANTHROPIC_API_KEY`; use `CLAUDE_CODE_OAUTH_TOKEN`.

## Acceptance criteria

- [ ] `docker compose up --build` brings the city up from a clean checkout with only Docker installed.
- [ ] `gc bd` works against the bead store (gastown's ~368 calls succeed), i.e. the store is a bd-contract provider.
- [ ] The compiled `gc` loads on the runtime base without SONAME errors.
- [ ] Agent auth uses a subscription OAuth token, not an API key.
- [ ] No host-pre-staged binaries are `COPY`ed in — everything is built/installed in the image.

## Files this skill creates / modifies

- `Dockerfile` — multi-stage: base-matched `gc`-from-source compile + dolt/bd/node/claude-code/tmux/socat install.
- `docker-compose.yml` — the compose group bringing up the city and bead store.
- `entrypoint` (e.g. `entrypoint.sh`) — renders city.toml, provisions rigs, starts managed Dolt + socat bridge, runs `gc start`.
- `city.toml`, `.gc/site.toml` — city config (deprecated `workspace.name` moved to site.toml).
- the gastown-importing pack — imports the proven gastown fleet.
- `.env` — supplies `CLAUDE_CODE_OAUTH_TOKEN` and deployment settings.
