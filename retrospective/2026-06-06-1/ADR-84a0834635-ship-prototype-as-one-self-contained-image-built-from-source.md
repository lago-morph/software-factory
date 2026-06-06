# ADR: Ship the Gas City prototype as one self-contained image built from source

- **ID**: ADR-84a0834635
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-06
- **Source retrospective**: ../2026-06-06-1.md
- **PRs covered**: #1

## Context

The deliverable target is a non-developer who should bring the prototype up with `docker compose up --build` and nothing more than Docker and a Claude subscription. The earlier gascity-prototype `COPY`ed host-pre-staged binaries into the image, which means the image only works on a machine where those exact binaries were already built — not laptop-portable. The user also confirmed the target laptop is Windows/amd64 (arm was dropped). The sandbox imposes a TLS-inspection proxy that blocks in-build HTTPS, but that is an environment-specific constraint, not a property of the shipped image. These factors made "what does the image contain and how is it built" a binding portability decision.

## Decision

Build everything (gc from source, plus dolt/bd/node/claude-code) inside the Dockerfile so a laptop needs only Docker, instead of COPYing host-pre-staged binaries as the earlier gascity-prototype did. The compiled `gc` is built on a base matching the runtime's ICU/glibc, and the committed Dockerfile carries no sandbox-specific hacks.

## Alternatives considered

- **COPY host-pre-staged binaries (gascity-prototype approach)** — rejected: the image then depends on binaries built outside it, so it is not laptop-portable and cannot be reproduced from a clean checkout with only Docker.
- **Patch the committed Dockerfile to satisfy the sandbox (trust the TLS-inspection CA)** — rejected: that contaminates a laptop-facing artifact with an environment-specific hack; the sandbox constraint is handled with a throwaway patched copy used only for verification.

## Consequences

The first build is slow because it compiles `gc` from source and installs the full toolchain, but Docker layer caching makes subsequent builds fast. Building a CGO binary in the image imposes a base-match requirement: the builder stage must use the same distro release as the runtime stage, or the binary fails to load by SONAME (ICU 72 vs 74 was the concrete failure this session). In exchange, the image is reproducible from a clean checkout on any Docker-capable laptop with no pre-staging step.

## References

- [`../2026-06-06-1.md`](../2026-06-06-1.md) — the source retrospective.
- [`./SKILL-SPEC-f62885124d-dockerize-gas-city.md`](./SKILL-SPEC-f62885124d-dockerize-gas-city.md) — the dockerize-gas-city skill spec.
- [`./SKILL-SPEC-e16f11e633-verify-container-image-in-restricted-sandbox.md`](./SKILL-SPEC-e16f11e633-verify-container-image-in-restricted-sandbox.md) — the sandbox-verification skill spec.
- PRs the decision was made in: #1 (lago-morph/software-factory-prototype).
