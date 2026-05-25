# ADR 0037: GF-S P-10 coordination medium

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3a subagent

## Context

[GF-S](../../architectures/v3/tracks/greenfield-substrate-first.md) is the only candidate that names [P-10 — Coordination medium](../../architectures/v3/primitives/cluster-C3.md#p-10--coordination-medium-ci-friendly-content-addressed) as a load-bearing substrate primitive (its S7 slot, per [GF-S §1.S7](../../architectures/v3/tracks/greenfield-substrate-first.md#1s7--coordination-medium-ci-friendly-substrate-resident-no-in-memory-mail-bus)); BF-L, BF-M, GF-M, and the U-cluster candidates either fold coordination into their typed-object-store primitives (P-28) or rely on their methodology layer's cycle protocol. This is therefore a GF-S **orphan ADR** — a candidate-specific decision with no cross-candidate same-vs-distinct verdict owed.

The contract restated from the [P-10 sketch](../../architectures/v3/primitives/cluster-C3.md#p-10--coordination-medium-ci-friendly-content-addressed): a shared blob/object medium accessible by both CI workers and agents, addressed by content hash, supporting append-only typed event-log writes for cross-cycle coordination. GF-S explicitly refuses an in-memory mail bus (per [Round-2 §5.1](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) on Overstory translatability) because the medium must survive the move into CI-runner environments that share only `git` + GitHub issues/comments. The forcing failure mode is [F32 (mail-injection / unsigned coordination)](../../architectures/v3/failure-modes-v3.md#f32--mailinjection--unsigned-coordination-messages), motivating a signing discipline on every event written to the log.

The decision must pick a concrete substrate that (a) is content-addressed by construction, (b) is reachable from any standard CI runner without a separate broker daemon, (c) supports an append-only typed event stream with fast-forward-only semantics, and (d) scales down to single-agent greenfield cycles and up to multi-agent merges without re-architecture.

## Decision

**GF-S P-10 is built as a Git-LFS content-addressed object store for cycle-output artifacts plus a GitHub-Actions-friendly artifact-pointer convention for the typed event log: `refs/factory/artifacts/<sha256>` for blobs and signed fast-forward-only Git refs `refs/factory/events/<stream>` for events.** Cycle outputs are written as Git LFS blobs (large artifacts off-tree, small artifacts inline as Git blob objects); each event in the typed log is a signed commit (GPG or Sigstore `git-gitsign`) whose tree contains a canonicalised JSON event envelope (`{event-type, stream, artifact-pointer, prev-event-sha, timestamp, signer-id}`) and whose parent chain encodes append-only ordering. Cross-agent coordination consumes the medium by ref-walking `refs/factory/events/<stream>` and resolving artifact pointers through `git-lfs fetch`. The medium is reachable from any GitHub Actions runner (`actions/checkout` with `lfs: true`) without provisioning a broker; it is reachable from agent sandboxes by the same Git plumbing the sandbox already trusts for code I/O.

The signing discipline (per F32) is satisfied by signed commits on every event-log append; verification at read time is `git verify-commit`. Multi-agent merges go through a Refinery-class merge resolver as a separate primitive, not as part of P-10's substrate.

## Alternatives considered

**B. Shared POSIX filesystem (NFS / SMB / local `/var/factory`).** *Why rejected:* not CI-portable. A GitHub Actions runner gets a fresh ephemeral filesystem per job; persisting state across cycles would require either an out-of-band volume (defeats the "no separate broker" requirement) or rebuilding the filesystem semantics on top of `actions/cache` (which is not content-addressed and has eviction semantics outside the substrate's control). The cross-platform permission story (Linux/macOS/Windows local dev + container/host boundary in CI) is the same problem the [ADR 0015 alternative C analysis](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md#alternatives-considered) rejected for P-08.

**C. Message queue / coordination broker (Redis Streams, NATS JetStream, Kafka).** *Why rejected:* heavyweight for the one-candidate scope. GF-S is a single substrate-first candidate; deploying and operating a broker (provisioning, auth, retention policy, broker-version drift across deployments) is operational tax that the Git-LFS + GitHub-Actions path avoids entirely. Brokers are also not content-addressed by construction — the substrate would have to layer hashing on top, then reconcile broker-side retention with substrate-side immutability. The corpus's preferred shape is content-addressed-by-construction (per [P-10 sketch §Construction path](../../architectures/v3/primitives/cluster-C3.md#p-10--coordination-medium-ci-friendly-content-addressed)).

**D. IPFS + Automerge CRDT log.** Considered as the [sketch's alternate construction path](../../architectures/v3/primitives/cluster-C3.md#p-10--coordination-medium-ci-friendly-content-addressed). *Why rejected for GF-S:* IPFS adds a peer-discovery and pinning operational surface that the GitHub-Actions path does not require; Automerge's CRDT semantics are stronger than GF-S needs (greenfield cycles do not require concurrent-write convergence — fast-forward-only on a Git ref is sufficient). IPFS remains a valid drop-in for cross-organisation deployments per the sketch.

## Consequences

**Easier:** the substrate composes with [P-01 sandbox](./0010-p-01-sandbox-runtime.md) (the sandbox already has Git available; no new tool to allow-list) and with [P-08 scenario storage](./0015-p-08-scenario-storage-with-runner-contract.md) (P-08's Git-LFS backend is the same substrate, so P-10 events can pointer-reference P-08 artifacts without a translation layer). CI portability is closed by construction — any standard runner with `actions/checkout` and `git-lfs` works. F32 signing is satisfied by commit-signing the substrate already supports.

**Harder:** Git-LFS quota management is now a substrate-ops concern (GitHub LFS storage caps, bandwidth caps); large-blob cycles need a self-hosted LFS server (e.g., `lfs-test-server`, `Gitea LFS`, or S3-backed `git-lfs-s3`) at scale. Ref-walking the event log has linear cost in stream length; consumers needing low-latency-tail-reads will want a snapshot cache (out of substrate scope).

**Explicitly NOT promising:** multi-writer concurrent-merge semantics beyond fast-forward-only. Multi-agent merge resolution is a separate methodology-layer primitive; the substrate refuses to embed CRDT semantics it does not need.

## References

- [P-10 sketch in cluster-C3](../../architectures/v3/primitives/cluster-C3.md#p-10--coordination-medium-ci-friendly-content-addressed) — buildability-confirmed `commodity` verdict.
- [GF-S §1.S7](../../architectures/v3/tracks/greenfield-substrate-first.md#1s7--coordination-medium-ci-friendly-substrate-resident-no-in-memory-mail-bus) — S7 contract and Overstory-translatability framing.
- [GF-S substrate-requirements §1 (S7 entry)](../../architectures/v3/substrate-requirements/gf-s.md#1-primitive-list-buildability-confirmed) — `commodity` verdict carrying forward to Phase 5.
- [F32 — Mail-injection / unsigned coordination messages](../../architectures/v3/failure-modes-v3.md#f32--mailinjection--unsigned-coordination-messages) — forcing signing discipline.
- [ADR 0010: P-01 sandbox runtime](./0010-p-01-sandbox-runtime.md) — composes with this ADR via shared Git tooling.
- [ADR 0015: P-08 scenario storage](./0015-p-08-scenario-storage-with-runner-contract.md) — shares the Git-LFS substrate; P-10 event-log pointers reference P-08 artifacts.
