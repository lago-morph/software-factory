# ADR 0045: BF-M P-03 worktree isolation

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3b subagent (BF-M orphan)

## Context

P-03 is the per-cycle filesystem-isolation primitive on which [BF-M's stage-5 Build phase](../../architectures/v3/tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage) depends to prevent concurrent cycles operating on the same source repository from silently overwriting each other's working state. Per the [P-03 buildability sketch](../../architectures/v3/primitives/cluster-C1.md#p-03-worktree-isolation), the contract is: each cycle receives its own working copy of the repository rooted at a path the cycle's P-01 closure binds in as `/work`; merges back to the canonical branch happen only through P-04 (PR creator), never through direct filesystem coordination; and cycles cannot read or write each other's worktrees. API surface is `create(repo-url, base-ref) → worktree-path` and `destroy(worktree-path)`.

The forcing failure mode is [F17 — parallel agents on shared dirs lose data](../../architectures/v3/failure-modes-v3.md#f17--parallel-agents-on-shared-dirs-lose-data) (greenfield `high`, brownfield `high`): "filesystem is the coordination medium; no built-in concurrency control." BF-M's [§2.5 row for F17](../../architectures/v3/tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage) assigns the mitigation to stage 5 as "per-cycle isolated worktree." The closure must be substrate-enforced rather than agent-discipline-dependent (otherwise [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) applies). High-parallelism architectures relying on cross-cycle concurrency (Compound, Symphony per the [cluster-C1 sketch's corpus-why citation](../../architectures/v3/primitives/cluster-C1.md#p-03-worktree-isolation)) presume this primitive exists for their composition story to hold.

P-03 composes against two adjacent primitives whose ADRs frame the boundaries: [ADR 0010 P-01 sandbox runtime](0010-p-01-sandbox-runtime.md) provides the bind-mount surface that exposes the worktree to the cycle as `/work`; [ADR 0012 P-05 trajectory capture](0012-p-05-trajectory-capture.md) records the cycle-id → worktree-path mapping so the trajectory is replayable.

## Decision

**Build P-03 as ephemeral `git worktree add` checkouts rooted on a tmpfs-mounted directory, one worktree per cycle-id, torn down by a cleanup hook fired on cycle end.** Per cycle, the substrate runs `git worktree add --detach /mnt/factory-tmpfs/cycle-<id> <base-ref>` against the shared bare-repo cache; this creates an isolated working tree and `HEAD` while sharing the repository's object database (no full clone per cycle). The tmpfs mount (`tmpfs /mnt/factory-tmpfs tmpfs size=<budget>,mode=0700`) gives the worktree fast-create / fast-destroy semantics and ensures no cross-cycle filesystem state survives a host reboot. Each cycle's worktree path is bound into the P-01 closure as `/work` (`bwrap --bind /mnt/factory-tmpfs/cycle-<id> /work` — per the [ADR 0010 decision](0010-p-01-sandbox-runtime.md#decision)), so the agent inside the cycle sees only its own copy.

Cleanup is hook-driven, not GC-driven: on cycle terminal-state (commit-pushed-via-P-04, abort, or cost-ceiling kill), the substrate runs `git worktree remove --force /mnt/factory-tmpfs/cycle-<id>` and unlinks any residual files. The cycle-id → worktree-path mapping is written to the trajectory store at `create()` time and the destroy event is appended at `destroy()` time, so trajectory replay (per [ADR 0012](0012-p-05-trajectory-capture.md)) can reconstruct which path held which cycle's state.

The worktree is operated on a per-cycle ref namespace (`refs/cycle/<id>/...`) so parallel sibling cycles cannot collide on branch names; the P-04 PR creator promotes from this namespace to a `refs/heads/cycle-<id>` head at push time.

## Alternatives considered

**B. Shared monorepo checkout with per-cycle branches.** A single working tree on disk; each cycle does `git checkout cycle-<id>` and operates in-place. *Why rejected:* branch state leaks across cycles. Uncommitted edits, untracked files, partial merges, stash entries, and any non-version-controlled scratch state (build artifacts, `.pyc`, IDE caches, language-server indices) persist between checkouts and reappear in the next cycle's worktree. The F17 contract requires that "cycles cannot read or write each other's worktrees" (per the [sketch's partition statement](../../architectures/v3/primitives/cluster-C1.md#p-03-worktree-isolation)) — shared-checkout-plus-branches violates that at the untracked-files surface, which is exactly where brownfield's stage-5 build step produces the most state. It also serializes cycles on the single working tree lock, defeating BF-M's parallelism story.

**C. Ephemeral container with full clone per cycle.** Spin up a fresh container with `git clone <repo-url> /work` at cycle boot. *Why rejected:* per-cycle full clone is slow (minutes for large brownfield repos vs. milliseconds for `git worktree add` against a warm bare cache), which defeats BF-M's per-cycle quick-turnaround posture. It also duplicates the object database per cycle — for the brownfield case with multi-GB histories, this multiplies storage by the parallelism factor. The container layer would be redundant with the P-01 closure already in place (per [ADR 0010](0010-p-01-sandbox-runtime.md)), giving two isolation mechanisms with no additional containment over the worktree-on-tmpfs approach.

## Consequences

**Easier:** F17 mitigation becomes substrate-enforced at stage 5 with negligible per-cycle setup cost (`git worktree add` against a warm bare cache is sub-second even on multi-GB repos). The tmpfs root makes destroy semantics bulletproof — host reboot guarantees no state survives. Composition against P-01 is one bind-mount; composition against trajectory capture is two log lines per cycle. The cluster-C1 deny-default-at-the-boundary invariant (per [the cluster coda](../../architectures/v3/primitives/cluster-C1.md#cluster-coda)) is preserved: cycles cannot reach outside `/work` because P-01 doesn't bind anything else writable.

**Harder:** tmpfs sizing becomes a deployment-time capacity calculation — the substrate must size the tmpfs mount for `max-parallel-cycles × max-worktree-size`. Worktrees that exceed the budget mid-cycle hit `ENOSPC` rather than disk-spilling; the substrate must surface this as a typed cycle-failure (not silent corruption). Bare-repo cache invalidation when the upstream history is rewritten (force-push to base-ref) is a secondary concern: the cleanup hook must invalidate the cache, not just the worktree.

**Explicitly NOT promising:** cross-cycle communication via filesystem. The partition is hard. Cycles that need to share state must route through trajectory capture (P-05) or the PR/forge surface (P-04), not via a shared `/work` path.

## References

- [P-03 buildability sketch (cluster-C1)](../../architectures/v3/primitives/cluster-C1.md#p-03-worktree-isolation) and [cluster coda on deny-default invariant](../../architectures/v3/primitives/cluster-C1.md#cluster-coda)
- [BF-M substrate-requirements §1 P-03 entry](../../architectures/v3/substrate-requirements/bf-m.md) and [stage-5 F17 mitigation row in §2.5 of the BF-M track](../../architectures/v3/tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage)
- [F17 parallel-agents failure mode](../../architectures/v3/failure-modes-v3.md#f17--parallel-agents-on-shared-dirs-lose-data) and [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class)
- [ADR 0010 P-01 sandbox runtime](0010-p-01-sandbox-runtime.md) — P-03 worktree is bound into the P-01 closure as `/work`
- [ADR 0012 P-05 trajectory capture](0012-p-05-trajectory-capture.md) — cycle-id → worktree-path mapping recorded for replay
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave 5.3b authoring brief
