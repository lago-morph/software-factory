# Adversarial review — C19 Bead store / typed work-graph (Track B, sweep 1)

Reviewer persona: Subsystem Adversary (Persistence & Memory)
Target: spec-optimized/C19-bead-work-graph.md (+ plan-optimized/C19-bead-work-graph.md)

Track B attacks the **design**: correctness, hidden coupling, failure handling, cost, simplicity,
scalability, security. Each delta is tested for justification.

## Findings

### RC19B-01 — major — C19↔C20 production write path is a hard cycle; the "soft/co-foundational" label hides a runtime ordering hazard
Evidence: §2 "C20 — soft/co-foundational: C19 calls C20's `validate` at the write seam (DELTA-06)… a
production write path is fail-closed against C20." C20-B §2 depends on C19. So the *production* write path is
a hard cycle: C19 cannot accept a typed bead without C20 `validate`, and C20 cannot validate without C19's
envelope/edge model. "Soft" is only true for the *pre-production generic envelope*, not the shipped path.
Reasoning: A scheduler could ship C19 first and find its production write path dead until C20 lands. The
plan's stub strategy (T5 against a C20 stub) is the right mitigation, but the *spec* sells the dependency as
softer than it is.
Suggested fix: State that the *production* write path has a hard mutual dependency on C20, broken only by the
interface freeze + a no-op validation stub. **DEFERRED** — this is XC-1; recommend the integrator ratify the
freeze-breaks-the-cycle resolution rather than edit one side unilaterally.

### RC19B-02 — major — DELTA-02 "`created_by` resolves to a C41 actor, fail-closed" is a runtime coupling downplayed as a "type dependency"
Evidence: §2 "C41… In a Phase-0 single-agent install the actor set is trivial (one `worker`), so this is a
*type* dependency, not a runtime blocker." But §3 invariant + §8 AC-2 require `create`/`update` to **reject**
a `created_by` that does not *resolve to a C41 actor* — resolution against an actor-set is a *runtime* check
needing C41's registry at every write.
Reasoning: If C41's actor set is unavailable/eventually-consistent, every bead write blocks or fails. Either
(a) C19 validates only presence + syntactic shape and defers actor-existence to C41's audit, or (b) C19
couples to a C41 lookup on the hot write path. The spec wants (b)'s wording at (a)'s cost.
Suggested fix: Split the invariant — presence/shape enforced by C19 (cheap, no C41 runtime); actor-existence
is C41's audit (or an explicit cached lookup with a stated staleness contract). **DEFERRED** — C19↔C41 seam;
recommend integrator pin which half C19 owns.

### RC19B-03 — major — Acyclicity invariant contradicted itself: `blocks` named the "single enforcement point" while `child_of` was marked acyclic ("yes (tree)") — a `child_of` cycle would pass `add_edge`
Evidence (pre-fix): §3 "the `blocks` edge sub-graph is a DAG…; `add_edge` is the **single** enforcement
point"; §4.2 table: `child_of` "Acyclic? yes (tree)". A molecule tree with a `child_of` cycle (bead is its
own ancestor) satisfied `add_edge` (only `blocks` checked) yet violated the table and broke C13's tree walk.
Reasoning: Correctness defect — the molecule tree (C13's core structure) had no actual acyclicity guard
despite being labelled acyclic.
Suggested fix: Enforce acyclicity on `child_of` too. **Applied** — §3 invariant, §4.2 table note, and the
`add_edge` signature now enforce acyclicity on both `blocks` and `child_of`; `caused_by`/`closes` remain
chain-only, bounded by C20.

### RC19B-04 — major — DELTA-04 durability oversells multi-process safety: the `file` provider's cross-writer lock is *advisory*
Evidence (pre-fix): §4.3 "single-writer… advisory lock for multi-process"; §3 durability invariant "once
`create`/`update` returns, the mutation survives process crash." Atomic-rename gives per-writer crash-safety,
but an *advisory* lock is cooperative — a non-cooperating writer or a stranded lock corrupts the shared
log/indexes. The spec presented file durability without bounding it to single-writer.
Reasoning: At L4/L5 fan-out (the system's point) many agents write beads; sharing one file store voids
DELTA-04. The honest contract: file provider is single-writer-safe; true multi-writer is Dolt.
Suggested fix: State the cross-writer-best-effort caveat; route multi-writer to Dolt. **Applied** — caveat
added to §4.4, advisory lock flagged in §4.3.

### RC19B-05 — minor — DELTA-05 conflates store-internal `seq` replay with C23 event emission
Evidence: DELTA-05 sells `seq` as both "ordered cross-session replay" and "cheap event-bus/C23 emission";
§6 makes C23 emission best-effort/droppable (OQ1). Replay determinism rests on the *internal* `seq`-ordered
log (correct) and must never depend on C23 delivery.
Reasoning: A reader could think cross-session replay depends on C23 completeness; it must not. The substance
is already correct in §6; only the delta wording couples them.
Suggested fix: Separate the claims — internal-log `seq` = deterministic replay (hard); emitted-event `seq` =
soft ordering for the lossy feed. **Not applied** (wording-only; substance correct) — sweep-2 clarification.

### RC19B-06 — minor — `ready_frontier()` silently depends on C20's per-type terminal-state set
Evidence: §3/§5 define ready-frontier via `blocks` predecessors "in a terminal state"; which states are
terminal is a C20 per-type lifecycle fact not listed in §2's dependency table.
Reasoning: Hidden coupling — ready-frontier correctness depends on C20's lifecycle catalog.
Suggested fix: Note that "satisfied" resolves against C20's per-type terminal states; freeze it in the
C19↔C20 contract. **Not applied** (sweep-2 contract detail) — flagged for the freeze.

### RC19B-07 — minor — Cost/scale: no log compaction or snapshot for the file provider; crash recovery is O(total history)
Evidence: §7 "zero marginal cost"; §4.4 recovery = "replay the log in `seq` order" = O(N) total mutations,
unbounded as the graph grows, with no compaction story (contrast C21-B DELTA-06 which specifies retention/GC).
Reasoning: A long-lived factory's bead log grows without bound; recovery time grows with it.
Suggested fix: Add a snapshot/compaction note (periodic index snapshot so recovery replays only the tail),
mirroring C21-B. **Not applied** (sweep-2 scope) — flagged as OQ; recommend a `bead log compaction` plan task.

## Cross-component resolutions recommended to the integrator
- **Bundle-id (XC-4):** see the C20-B review (RC20B-01) — the C20-B↔C22-B *ownership* fork is the
  load-bearing issue; C19-B is correctly silent on bead `bundle_id`.
- **C19↔C20 direction (XC-1):** **C20 depends on C19**; the production write path is a hard cycle broken by
  the interface freeze + a no-op `validate` stub. Drop the "soft" framing for the production path (RC19B-01).

## Verdict
**accept-with-fixes.** The design is strong — the provider seam (DELTA-01), durability contract (DELTA-04),
typed edges (DELTA-03), and mandatory attribution (DELTA-02) are well-justified deltas that genuinely close
G17/G36 at the graph layer. Applied fixes close a real correctness hole (RC19B-03 `child_of` acyclicity) and
an oversold durability claim (RC19B-04 advisory lock). The two majors I did *not* edit (RC19B-01 hard write
cycle, RC19B-02 C41 runtime coupling) are seam-ownership questions DEFERRED to the integrator. Residual scale
gap: file-log compaction (RC19B-07).
</content>
