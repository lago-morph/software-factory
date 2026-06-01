# auto-001 — detect-only binding gate on D-20

**Author.** Lead agent, autonomous-run session 2026-06-01.
**Status.** `Round 1 in flight`.
**Rewind point.** Commit `TBD` on branch `claude/architectures-v4-meta-guidance-OpJFZ-03-auto001`. Reverting it removes this brief and leaves the as-adopted D-23 posture (prevent-vs-detect = a noted caveat, not a gate) unchanged; the operator can re-adjudicate.

---

## Question

The expert panel ([VERDICT.md](../panel/VERDICT.md) R1/§6 item 1; security + methodology panelists) argues that the adopted [D-23](../review-log.md) decision is too weak: D-23 treats a *detect-only* Gas City outcome (i.e. `gc` permits an out-of-partition tool call and logs it after the fact, rather than refusing it at dispatch time) as a **noted caveat**, when it should be a **binding go/no-go gate** on [D-20](../review-log.md) (the C43 boundary-typing "fence" pulled forward to a Phase-2 entry precondition). This is recorded as the not-yet-operator-decided follow-up **PF-1**. **Decision: when the D-23 spike returns a detect-only result for `gc`, what binding consequence does that place on D-20 and on running the factory unattended (P2) / self-modifying (P3b)?** This decision affects C43 (fence), C34 (holdout integrity), C42 (partition), the Phase-2 entry checklist, and the autonomy-ladder gates (C56). It does **not** decide what `gc` actually does — that is the empirical D-23 spike ([protocol](../D-23-gas-city-spike-protocol.md)); it decides the *policy that binds to each spike outcome*.

Scope note: the prevent-vs-detect question itself is **OPEN** (the prototype proved bead-prefix is the scoping *mechanism* but deferred the smoke test that would test enforcement strength — see [substrate harvest F10](../D-23-substrate-harvest.md)). This brief pre-commits the *consequence* so the answer is not re-litigated under schedule pressure once the spike runs.

## Alternatives considered

### Option A — Binding go/no-go gate, dischargeable only by a real prevent layer

- **Description.** A detect-only `gc` result **hard-blocks unattended operation (P2) and self-modification (P3b)** until a *prevent* control exists at the boundary. The block is discharged by either (i) a named OS/container-level prevent layer (filesystem partition + seccomp/landlock + network-egress policy enforced at tool-call/process boundary, so an out-of-partition read is *refused*, not merely logged), or (ii) an explicit operator decision to descope autonomy (stay at L4 human-in-loop until prevent exists). D-20's "fence pulled to P2" is reframed: the fence is a *real control* only when the boundary prevents; under detect-only the fence is a *declaration* and P2 is gated.
- **Pros.**
  - Matches the operator's own framing: on a self-modifying factory, "we noticed after it happened" is the wrong failure mode ([decisions-to-make item 1](../../../../decisions-to-make.md)).
  - Converts a silent assumption into an explicit, testable precondition; the autonomy claim becomes honest (no "fence" that doesn't fence).
  - The discharge path (OS-level prevent) is buildable with mature OSS (seccomp/landlock/gVisor, egress policy, FS namespaces) — defense-in-depth that does not depend on `gc`'s internals.
- **Cons.**
  - Risks reintroducing exactly the hardening the [bar](../HANDOFF.md) deliberately dropped (custom seccomp/OPA/network policy were dropped in Sweep-1) — needs a careful "is this a 12-principle capability or polish?" test.
  - Hard-block has schedule cost if `gc` turns out to prevent and the gate fires spuriously; mitigated because the gate is *conditional on the detect-only outcome*.

### Option B — Caveat + after-the-fact compensating controls (≈ as-adopted)

- **Description.** Keep D-20's sequencing unchanged. If detect-only, layer *after-the-fact* compensating controls — enhanced audit completeness (incl. OS-level Bash reads, panel §6 item 8), rapid rollback, blast-radius accounting — but do **not** hard-block P2. This is roughly the posture D-23 adopted (noted caveat).
- **Pros.** Lowest schedule cost; no new prevent layer to build; keeps Sweep-1's drop-the-hardening discipline intact.
- **Cons.** Leaves the P2→P3b exposure window the panel (4/5) flagged as a real (not documented-only) risk under detect-only; "compensating after-the-fact controls" on a self-modifying system is the failure mode the operator explicitly disliked. The fence remains a declaration.

### Option C — Prevent-by-construction outside `gc` (make the question moot)

- **Description.** Do not rely on `gc` enforcement for the safety boundary at all. Mandate an OS/container-level prevent layer as the P2 fence *regardless* of what `gc` does, so the prevent-vs-detect question about `gc` becomes irrelevant to the safety boundary (it still matters for holdout-integrity ergonomics, but not for blast radius).
- **Pros.** Removes dependence on a third-party binary's internals for a safety-critical control; defense-in-depth by default; the spike outcome no longer gates anything.
- **Cons.** Pays the full prevent-layer cost *unconditionally*, even if `gc` already prevents (over-building, bar violation); pre-commits to a build before the cheap spike that might show it's unnecessary — the opposite of the buildability-first thesis D-23 embodies.

### Option D — Descope autonomy under detect-only (L4-forever until prevent)

- **Description.** If detect-only, simply cap the factory at L4 (human-in-loop batched review) indefinitely; never claim P2 unattended until a prevent layer is independently motivated. No new build mandated; the autonomy claim is just narrowed.
- **Pros.** Honest, zero new build, reversible. Aligns with "L5 is the endpoint, not a precondition" ([C39](../../spec/C39-fix-task-loop-closure.md) cites README:527).
- **Cons.** Forfeits the central v4 value proposition (unattended/dark factory) on a single substrate property; a strict reading makes the whole architecture contingent on `gc` preventing, with no engineering response other than "give up autonomy."

## Decision (Round 1 — written before any adversarial review)

**Selected: Option A** (binding go/no-go gate, dischargeable by a real prevent layer **or** an explicit descope), with **Option C's prevent layer as the named discharge mechanism** and **Option D available as the operator's explicit descope choice**. A and C+D are not really rivals: A is the *policy* (detect-only ⇒ P2 is gated); C is *one* discharge (build the prevent layer); D is the *other* discharge (descope). Option A names both exits; Option B is rejected as the posture the operator already disliked.

Reasoning:

1. **The fence's entire job is in-the-moment resistance.** D-20 pulled the fence forward precisely so a prompt-injection/self-mod during P2→P3b is *stopped*, not *noticed*. Under detect-only, the pulled-forward fence does not do that job — so D-20's safety claim is conditional on prevent. Making that conditionality a binding gate (A) is just stating D-20's own premise honestly; B leaves D-20 over-claiming.
2. **The operator already ruled against detection-only at this boundary.** [decisions-to-make item 1](../../../../decisions-to-make.md) rejected "accept detection-only Phase 0" (XC-8) in favor of pulling the fence forward. A detect-only `gc` re-opens XC-8 by the back door; Option A closes that door consistently with the operator's adopted stance, where B silently re-admits it.
3. **The discharge path is buildable under the bar without over-building.** seccomp/landlock/network-egress/FS-namespace prevention is mature OSS and is a *12-principle capability* (P-level blast-radius bound), not non-principle polish — so it passes the bar's "MORE capability tied to a principle" test where Sweep-1's dropped custom hardening did not. But — and this is why A beats C — it is built **only if the spike shows detect-only**, preserving buildability-first: we do not pay the cost until the cheap spike proves it necessary.
4. **A is reversible and honest; it pre-commits a *policy*, not a *build*.** No code is written now; the brief simply binds the consequence so the question is not re-litigated under schedule pressure when the spike runs. If `gc` prevents, the gate never fires and nothing was over-built (the failure mode of C).

## Downstream impact

- **D-23 protocol:** the §6 results table's "decision triggered" column for a detect-only Test-A outcome becomes "fire the auto-001 P2 gate" (binding), not "note the caveat."
- **C43 (fence):** spec gains a conditional: "the boundary-typing fence is a *control* iff the substrate prevents; under a detect-only substrate the C43 P2 precondition is satisfied only by a named external prevent layer (FS-namespace + seccomp/landlock + egress policy) — otherwise P2 is blocked."
- **C34 (holdout) / C42 (partition):** cross-reference the same gate; holdout integrity under detect-only also depends on the external prevent layer (or accepts a documented weaker guarantee with operator sign-off).
- **C56 (autonomy ladder):** P2 entry gate gains "prevent-layer verified OR operator descope-to-L4 recorded" as a hard precondition.
- **Phase-2 entry checklist:** leads with the D-23 spike; a detect-only result routes to this gate before any unattended run.

## If-user-overrides rewind point (Round 1)

Revert this brief's commit on `claude/architectures-v4-meta-guidance-OpJFZ-03-auto001`. What survives: the D-23 milestone (PR #230) — protocol, harvest, spec annotations — all independent of this brief. What restores: the as-adopted D-23 posture (detect-only = noted caveat, no P2 gate). The operator can then pick B/C/D directly.

---

## Adversarial-review round 1

Per [`AGENTS.md` real-subagent rule](../../../../AGENTS.md#adversarial-review-must-be-real-subagents), ≥3 real adversarial reviewer subagents. Each reviewer returns one of three verdict tiers (per [`AGENTS.md` verdict-tiers rule](../../../../AGENTS.md#adversarial-review-verdict-tiers)): `accept-as-is`, `accept-with-named-amendments`, or `reject-with-counter-proposal`.

### Reviewer angles dispatched

- Reviewer 1: **Red-teamer / security** — attack the strongest claim (that Option A closes the exposure window) using worst-case reasoning; find where A still leaves the factory exposed.
- Reviewer 2: **Cost/scope hawk + buildability-bar enforcer** — does the prevent-layer discharge covertly reintroduce the custom hardening the bar dropped? Is A over-engineering vs B/D?
- Reviewer 3: **Pre-mortemer** — 6 months on, the auto-001 gate caused a bad outcome (shipped-too-late, or shipped-unsafe-anyway, or gate gamed). Tell the failure story.

### Findings (after reviewers return)

_(to be filled in after Round-1 reviewers return)_

### Verdict status (per reviewer)

_(to be filled)_
