---
name: verify-the-shipped-config-not-a-proxy
description: Before declaring a packaged artifact verified, exercise the exact artifact and configuration that ships — the real compose file with its real volume/network settings, the real entrypoint, on the target-equivalent platform — not a hand-rolled approximation that happens to be easier to run. A verification that diverges from the shipped config can pass while the shipped config fails, because the divergence is exactly where the bug hides. Triggers on phrases like "verify the image", "does the prototype run", "ship it", "is the compose file good", "test on Windows", "the operator says it's slow"; and proactively any time you are about to declare a packaged deliverable (Docker image, compose stack, installer, release tarball) verified, or whenever the verification path and the shipped path could differ in volumes, networking, entrypoint, base image, version pins, or platform. Skip for pure unit-level changes with no packaging surface; when the shipped artifact genuinely cannot be exercised in any available environment, state that limitation explicitly rather than substituting a proxy and calling it verified.
---

# Verify the shipped config, not a proxy

Before declaring a packaged artifact verified, **exercise the exact artifact and
configuration that ships** — the real compose file with its real volume/network
settings, the real entrypoint, on the target-equivalent platform — not a
hand-rolled approximation that happens to be easier to run.

A verification that diverges from the shipped config **can pass while the
shipped config fails, because the divergence is exactly where the bug hides**.
This skill is grounded in a session where verification used `docker run` with a
named volume while the shipped `docker-compose.yml` used a host bind mount,
hiding a Docker-Desktop-on-Windows performance failure that only the shipped
config exhibited.

---

## When to use this skill

**Activate when:**

- You are about to declare a packaged deliverable (Docker image, compose stack,
  installer, release tarball) verified.
- The verification path and the shipped path could differ in volumes,
  networking, entrypoint, base image, env vars, version pins, or platform.
- The user says "verify the image", "does the prototype run", "ship it", "is
  the compose file good", "test on Windows", or "the operator says it's slow".

**Do not activate for:**

- Pure unit-level changes with no packaging surface.
- When the shipped artifact genuinely cannot be exercised in any available
  environment — state that limitation explicitly rather than substituting a
  proxy and calling it verified.

---

## Inputs

- The shipped artifact and its real configuration file(s): `docker-compose.yml`,
  `Dockerfile`, entrypoint scripts, `.env` template.
- A target-equivalent platform (or the closest available — and a note when it
  is not exact).
- The version pins the artifact is supposed to build with.
- Any credentials the run legitimately needs (loaded without printing).

## Outputs

- Evidence that the exact shipped config was booted and behaved correctly
  (logs, timings, healthchecks).
- A list of divergences between any convenience-verification and the shipped
  config, each reconciled or justified.
- Bug reports / fixes for failures that only the shipped config exhibits.

---

## Workflow

1. **Identify the exact artifact and config that ships.** Read the real
   `docker-compose.yml` / `Dockerfile` / entrypoint — do not reconstruct them
   from memory.
2. **List every property that affects runtime behavior**: volume type (named vs
   bind mount), network mode, ports, entrypoint, base image, env vars, version
   pins.
3. **Boot using the shipped invocation** (`docker compose up`, not a hand-rolled
   `docker run`) on the target-equivalent platform.
4. **Exercise the real workload** the operator will run, and measure what they
   will feel (latency, startup time, command success).
5. **Diff any convenience approximation against the shipped config
   property-by-property.** Any difference is a candidate hiding place for a
   bug — re-run that exact property on the shipped path.
6. **Fix failures that the shipped config exhibits**, then re-verify on the
   shipped config.

---

## Concrete examples

### Example 1: bind-mount vs named-volume

The Windows operator reported the bead store was "extremely slow." Verification
had been done with `docker run` plus a named volume — fast. The shipped
`docker-compose.yml` used a host bind mount (`./workspace`). On Docker Desktop's
translated host filesystem (drvfs/9p), Dolt's many small reads/writes and file
locking crawled. The bug lived precisely in the property the proxy verification
had swapped out. Fix: switch `/workspace` to a named volume in the shipped
compose file and re-verify on the shipped path.

### Example 2: version float vs intended pin

The `Dockerfile` built `gc` from `main` rather than a pinned release, so the
shipped image stamped `gc 1.1.1` while the intended, gascity-matched version was
`v1.2.1`. A verification that didn't check the actual stamped version inside the
shipped image would miss the skew — and `dolt latest` had previously removed
`sql-server --user`, exactly the class of breakage floating pins invite. Fix:
pin to the matched `deps.env` set and verify the stamped versions inside the
built image.

---

## Anti-patterns

- **Verifying with a hand-rolled invocation because it's easier to run.** The
  bind-mount perf failure was invisible to `docker run` + named volume and only
  the shipped compose exhibited it.
- **Trusting the version you intended over the version the image stamped.** The
  Dockerfile floated to 1.1.1 despite the intent of v1.2.1 — read the artifact,
  don't assume.
- **Verifying on a convenient platform when the target is different.** Docker
  Desktop on Windows behaves nothing like native Linux for bind-mount I/O.

---

## Acceptance criteria

- [ ] The exact shipped artifact and config were booted via the shipped
      invocation.
- [ ] Every runtime-affecting property of the shipped config was exercised
      (volumes, network, entrypoint, version pins).
- [ ] Any convenience-verification divergence was diffed against the shipped
      config and reconciled.
- [ ] Platform used for verification is the target or the closest available,
      with non-exactness stated.

---

## Files this skill creates / modifies

- `docker-compose.yml`, `Dockerfile`, entrypoint scripts — corrected so the
  shipped path is the verified path.
- An optional verification log (timings, stamped versions, healthchecks)
  captured in the PR or retro.

---

## See also

- `execute-docs-against-running-system` — once the shipped config is booted,
  run every documented command against it so the docs match the artifact users
  actually get.
