# ADR 0010: P-01 sandbox runtime (deny-by-default)

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.1a subagent

## Context

P-01 is the per-cycle execution closure that every other substrate primitive composes against: P-02 (cost ceilings), P-03 (worktree isolation), and P-04 (PR creator) all rely on P-01 to mediate filesystem, network, and tool/syscall surface. Per the [Phase-4.2 coverage-tier summary](../../architectures/v3/primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal), P-01 is shared by all 10 candidates — the commodity-floor primitive of the substrate set.

The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/cluster-C1.md#p-01-sandbox-runtime) names the contract: a deny-by-default closure over filesystem, network, and tool/syscall surface; capability grants declared in the cycle manifest at boot and unwidenable mid-cycle; production-credentialled scissors substrate-disabled unless an explicit declaration triggers escalation to a separate, more-restricted profile. API surface is `launch(cycle-manifest) → handle` plus `revoke(handle)`.

The forcing failure modes are the [F12 → F33 → F44 lethal-trifecta cascade](../../architectures/v3/failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) (greenfield `high`, brownfield `critical` at F44; mitigations stack: perimeter typing → judge architecture → substrate default-off). [F53 (voluntary-discipline fragility)](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) marks operator-voluntary closure as fragile under load — the deny-default invariant must be substrate-enforced, not agent-discipline-dependent. [GF-S §1.S1](../../architectures/v3/tracks/greenfield-substrate-first.md#1s1--sandbox-closure-first-substrate-default-off-for-production-scissors) names P-01 as the closure-first foundation for the Shapiro R1–R5 production-scissors rules.

## Decision

**Build P-01 as a two-profile layered runtime.** The default profile is Bubblewrap (`bwrap --unshare-all --ro-bind / / --bind ./work /work`) providing kernel-namespace closure with deny-all default and per-mount allow-listing in a single CLI invocation; manifest-declared filesystem and env-var grants map one-to-one onto `--bind` / `--setenv` flags. The escalated profile is Firecracker microVM (`firecracker --config-file cycle.json` with per-cycle tap-device) providing hypervisor-grade closure for cycles whose manifest declares unrestricted shell exec, broad network egress, or any production-scissors capability. Profile selection is **substrate-decided at `launch()` time from the manifest's capability declaration** — operator-voluntary downgrade is forbidden (F53 mitigation).

Network closure inside either profile is enforced by an nftables deny-all default with per-host allow rules generated from the manifest's egress allow-list. Capability grants are immutable for the cycle's lifetime; widening requires `revoke(handle)` + a new `launch()` with a new manifest.

Production-credentialled scissors are substrate-default-off per [GF-S §1.S1](../../architectures/v3/tracks/greenfield-substrate-first.md#1s1--sandbox-closure-first-substrate-default-off-for-production-scissors); enabling them forces the Firecracker profile and writes an audit record before `launch()` returns.

## Alternatives considered

**B. Single-profile container runtime (Docker / Podman with default seccomp).** *Why rejected:* Docker's default seccomp + AppArmor profile is permissive relative to the deny-default contract — outbound network is open by default; the closure is operator-configured, not substrate-enforced, which the sketch identifies as exactly the [F53 voluntary-discipline](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) failure mode. The container surface is also too coarse for the production-scissors escalation case — there is no harder profile available without changing runtime. See the [P-01 sketch's Construction path](../../architectures/v3/primitives/cluster-C1.md#p-01-sandbox-runtime).

**C. gVisor user-space kernel as the single profile.** *Why rejected:* gVisor provides syscall-level isolation strictly stronger than Bubblewrap but at a steady-state performance cost (Google's own benchmarks report 2–5× slowdown on syscall-heavy workloads) that is wasted on the common case where the cycle is running deterministic linters, model calls, and git operations. The two-profile layered approach reserves the heavy isolation for the cases that need it. gVisor remains a viable substitute for the escalated profile in deployments where Firecracker's KVM dependency is unavailable; the ADR does not foreclose that swap. See the [cluster coda](../../architectures/v3/primitives/cluster-C1.md#cluster-coda) on the deny-default-at-the-boundary invariant.

## Consequences

**Easier:** the F12 / F33 / F44 cascade is substrate-closed for the default profile (deny-all-default + per-cycle allow-list + production-scissors-default-off); the cascade's [F44 closure-the-substrate-must-enforce](../../architectures/v3/failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default) lands on the Firecracker profile by manifest declaration rather than per-Claw operator discipline. P-02, P-03, and P-04 compose against a single `handle` API regardless of which profile is active — they do not need to know whether they're inside Bubblewrap or Firecracker. The cluster-C1 deny-default-at-the-boundary invariant (F53 cross-primitive mitigation) is realized.

**Harder:** two-runtime ops surface — operators must install both Bubblewrap (userspace, kernel ≥ 4.x) and Firecracker (KVM-capable host) and keep both profiles' policy bundles in sync. The nftables rule-generation step is a new substrate component (small but it is now load-bearing for network closure). Manifest schema must encode capability-profile selection explicitly; ambiguous manifests are rejected at `launch()` rather than defaulted.

**Explicitly NOT promising:** multi-tenant adversarial isolation (mutually untrusted agents on shared substrate). All 10 candidates assume a single-tenant, semi-trusted-agent threat model per the [P-01 sketch's research-grade-uncertainty flag](../../architectures/v3/primitives/cluster-C1.md#p-01-sandbox-runtime); adversarial multi-tenancy would require primitive-level escape isolation that remains research-grade and is out of scope.

## References

- [P-01 buildability sketch (cluster-C1)](../../architectures/v3/primitives/cluster-C1.md#p-01-sandbox-runtime) and [cluster coda on deny-default invariant](../../architectures/v3/primitives/cluster-C1.md#cluster-coda)
- [Phase-4.2 coverage-tier summary — P-01 in all-10 commodity-floor tier](../../architectures/v3/primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal)
- Substrate-requirements summaries citing P-01: [GF-S §1.S1](../../architectures/v3/tracks/greenfield-substrate-first.md#1s1--sandbox-closure-first-substrate-default-off-for-production-scissors) and [BF-M substrate set](../../architectures/v3/substrate-requirements/bf-m.md)
- Lethal-trifecta cascade: [F12 lethal trifecta](../../architectures/v3/failure-modes-v3.md#f12--lethal-trifecta--prompt-injection), [F44 production-scissors default](../../architectures/v3/failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default), [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave 5.1a authoring brief
