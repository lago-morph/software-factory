# auto-001 — detect-only binding gate on D-20

**Author.** Lead agent, autonomous-run session 2026-06-01.
**Status.** `ADOPTED by operator 2026-06-01` (ledger **D-30**), after 2 rounds / 6 real adversaries. See "Operator adoption" immediately below, then the Final decision.

---

## Operator adoption (2026-06-01) — D-30

The operator adopted the rubric and **re-adopted D-20 as conditional on prevention**, with one decisive amendment to the discharge:

- **It must block.** Unattended operation (P2) / self-modification (P3b) requires the substrate to **PREVENT (block at the tool-call/process boundary)**, not merely detect. Detection-only does not authorize an unattended run.
- **The watcher is the sanctioned discharge — design deferred.** If Gas City does not prevent natively (per the [D-23 spike](../D-23-gas-city-spike-protocol.md)), **we will add an enforcement watcher that blocks.** The watcher is sanctioned in principle; its **design is deferred until the spike confirms the substrate does not already prevent** ("don't design what we may not need"). When built, the watcher's design must still pass the bar. This **supersedes** the Round-2 "prevent layer NOT pre-blessed / descope-to-L4 as the *sole* default" wording — the operator sanctions the prevent path explicitly, just not its premature design.
- **Until prevention is established** (native or watcher), unattended operation is **blocked** (human-in-the-loop).
- **Per-rig-class autonomy** (the "missing middle") **remains available but secondary** to the block requirement.

This resolves both morning-review items: #1 (block — yes) and #2 (per-rig-class — kept, secondary). The Final decision below stands as the rubric; this section records the operator's binding adoption + the watcher-as-discharge amendment.
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

## Decision (Round 1 — written before any adversarial review) — ~~SUPERSEDED by Round 2 below~~

> **Superseded by Round 2** (after the Round-1 adversarial wave). Round 1 selected Option A *with the OS-level prevent layer pre-blessed as a named discharge*; all three Round-1 reviewers flagged that pre-blessed discharge as a bar violation (it is the literal union of SURVIVOR-PASS-dropped deltas), gameable, and outcome-incomplete. Round 2 keeps the binding-gate **policy** but de-blesses the prevent-layer build. Round-1 text preserved verbatim below for traceability.

~~**Selected: Option A** (binding go/no-go gate, dischargeable by a real prevent layer **or** an explicit descope), with **Option C's prevent layer as the named discharge mechanism** and **Option D available as the operator's explicit descope choice**.~~ A and C+D are not really rivals: A is the *policy* (detect-only ⇒ P2 is gated); C is *one* discharge (build the prevent layer); D is the *other* discharge (descope). Option A names both exits; Option B is rejected as the posture the operator already disliked.

Reasoning (preserved for traceability):

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

**Reviewer 1 (red-team/security) — strong amendments.** The brief's discharge layer closes the *cross-partition read* face but does **not** stop the lethal trifecta it claims to fence: an agent with *legitimate in-partition* access, fed untrusted content, can exfiltrate over an *allowed* egress channel (commit message, in-partition service call, DNS) — none of the brief's named controls touch that. So "closes the P2→P3b window" over-claims; the in-partition-read + allowed-egress path stays open regardless and must be a standing C57 residual. Also: detect/prevent is not binary (realistic outcome = "prevents FS, detects network"), so discharge must be **per-face** (read-face AND egress-face), with the egress allowlist a named deliverable. The L4-descope "safe floor" is asserted, not shown — a self-modifying agent between review batches still has a window (ties to VERDICT R3/§6-item-4). The C34 clause allowing "a documented weaker guarantee with operator sign-off" silently re-admits rejected Option B.

**Reviewer 2 (cost/scope + buildability-bar) — strong amendments, near-reject of the discharge.** Decisive finding: the named discharge layer (FS-namespace + seccomp/landlock + egress policy) is the **literal union of deltas SURVIVOR-PASS already DROPPED under the bar** — C42-02 "read-isolation enforced at OS/process boundary" (DROP), C04-05 "isolation-at-spawn OS enforcement" (DROP), C28-04 "capability/egress profile per invocation" (DROP), C42-06 OPA (DROP). The brief's defense ("a 12-principle capability, not polish") cites no P-number and re-bills *enforcement of an already-kept principle* as fresh capability — relabeling, not a real distinction. Pre-committing the consequence with a pre-argued buildable discharge loads the dice toward building (cost not bounded, just deferred + pre-justified). Option D delivers identical safety content (no unattended P2 under detect-only) with zero build and zero gate machinery across C43/C34/C42/C56. Amendments: (1) Option D is the *sole default discharge*; (2) **delete** the OS-prevent layer as a pre-blessed discharge — any future prevent build re-enters the bar fresh, owned + costed + P-numbered; (3) the gate pre-commits **policy only, never a build**.

**Reviewer 3 (pre-mortem) — strong amendments.** Dominant failure: *gate gamed / discharged on paper* — the spike returns A1 detect-only / A2 silent, schedule pressure mounts, someone wraps `bd` in OPA, checks "prevent-layer verified" against the **bead layer only**, and P2 launches with the OS/Bash (`cat ../rig2/...`) door still open — *worse* than an honest caveat because it adds false confidence. Early-warning sign: a discharge artifact citing A1 evidence but never re-running A2. Also: the brief pre-binds only "a detect-only result" but the protocol has **three** verdicts (PREVENT / DETECT-ONLY / SILENT) plus mixed per-face — the mixed/SILENT outcomes have no pre-bound consequence and will be re-litigated under the very schedule pressure the brief meant to forestall. And the discharge has no named owner / no deadline → indefinite P2 block (shipped-too-late). Cheapest fix: bind "verified" to re-passing spike Test A on **both A1 and A2**; pre-bind all outcomes; name an owner + descope-by-default date.

**Convergence.** All three independently land on the same shape: the **binding-gate policy is right and honest** (it states D-20's premise plainly), but the **pre-blessed OS-prevent-layer discharge is wrong** — bar violation (R2), gameable/incomplete (R1 trifecta gap, R3 A2-untested), and outcome-incomplete (R1/R3). This changes the decision → Round 1 superseded.

### Verdict status (per reviewer)

- Reviewer 1 (red-team/security): **`accept-with-named-amendments`** (4 named).
- Reviewer 2 (cost/bar hawk): **`accept-with-named-amendments`** (3 named; amounts to reject-of-the-discharge while keeping the gate policy).
- Reviewer 3 (pre-mortem): **`accept-with-named-amendments`** (3 named).

No reviewer rejected the gate *policy*; all three rejected the *pre-blessed prevent-layer discharge*. → Revise (Round 2).

---

## Decision (Round 2 — revised after Round 1)

**Final-candidate: Option A as POLICY ONLY, with Option D (descope-to-L4) as the sole default discharge; the OS-level prevent layer is NOT pre-blessed.**

The binding gate now reads: **any D-23 Test-A outcome other than full PREVENT on both faces (A1 bead-visibility AND A2 OS/Bash) blocks unattended operation (P2) and self-modification (P3b).** This is a *policy* pre-commitment, not a build mandate. It binds every spike outcome, not just "detect-only":

| Spike Test-A outcome | Consequence (pre-bound) |
|---|---|
| **PREVENT on both A1 + A2** | D-20's fence is a real control; P2 precondition satisfied (no extra work). |
| **DETECT-ONLY (either face)** | P2/P3b **blocked**. Default discharge: **descope to L4** (human-in-loop) and record it. |
| **SILENT (either face — access succeeds, no trail)** | P2/P3b **blocked**, *and* C34 holdout audit is also unsound on that face → treat as strictly worse than detect-only. |
| **MIXED (e.g., A1 prevent / A2 detect)** | P2/P3b **blocked** until the *failing face* reaches PREVENT; per-face, not a single boolean. |

Reasoning for the change (Round-1 findings folded in):

1. **Gate = policy, not build (R2).** The gate pre-commits only that a non-PREVENT substrate blocks unattended P2. It mandates **no** code. The OS-level prevent layer is **removed as a pre-blessed discharge**; if anyone later wants to build prevention to *unblock* P2, that build must re-enter the bar fresh — owned, costed, and citing a specific P-number — exactly like any other candidate capability. This removes the bar violation (the brief no longer relabels SURVIVOR-PASS-dropped deltas as pre-authorized) and de-loads the dice toward building.
2. **Default discharge = descope to L4 (R2), but L4 is not asserted "safe" (R1).** Under a non-PREVENT substrate the standing posture is L4 human-in-loop; the brief does **not** claim L4 is a clean safety floor. L4's residual exposure (a self-modifying agent between review batches) is bound to D-21's checkpoint-cadence + named-artifact requirement (VERDICT §6 item 4), not hand-waved.
3. **Drop the "closes the window" claim; record the trifecta residual (R1).** Even full PREVENT on both faces bounds only the *cross-partition* face. The **in-partition-read + allowed-egress** trifecta path remains open and is recorded as a **standing C57 residual** (egress-allowlist granularity is its own future work, not solved here).
4. **Bind all outcomes incl. SILENT + MIXED (R1, R3).** The consequence table above pre-binds PREVENT / DETECT-ONLY / SILENT / MIXED so no result is re-litigated under schedule pressure. SILENT is treated as worse than detect-only (it also breaks C34's audit soundness).
5. **If a prevent layer is ever built, "verified" = re-pass spike Test A on BOTH faces (R3).** A discharge that cites A1 evidence but skips A2 does not count. This closes the "discharged on paper" failure.
6. **Strike the C34 weaker-guarantee-with-sign-off clause (R1).** It re-admitted rejected Option B; removed. Under a non-PREVENT substrate C34 holdout integrity is *also* gated (or the factory runs at L4 where a human reviews holdout exposure), not waved through with sign-off.
7. **Name an owner + a descope-by-default trigger (R3).** The gate names the Phase-2 entry checklist owner as accountable for the spike + the verdict; absent a verified prevent build by P2-entry, the default is descope-to-L4 (no indefinite limbo).

### Revised downstream impact

- **D-23 protocol §6:** the results table's "decision triggered" column adopts the 4-row consequence table above (PREVENT / DETECT-ONLY / SILENT / MIXED), per-face.
- **C43 (fence):** "the boundary-typing fence is a *control* iff the substrate prevents on the relevant face; under any non-PREVENT face the C43 P2 precondition is satisfied only by descope-to-L4 (default) — a substitute prevent layer is NOT pre-authorized and must re-enter the bar." Plus a C57 residual cross-ref for the in-partition-read + allowed-egress trifecta path.
- **C34 (holdout) / C42 (partition):** cross-reference the same gate; SILENT outcome flags C34 audit-unsoundness explicitly. No weaker-guarantee-with-sign-off clause.
- **C56 (autonomy ladder):** P2 entry gate = "Test A PREVENT on both faces verified, OR operator descope-to-L4 recorded"; L4 residual bound to D-21 cadence.
- **C57 (residual register):** add the in-partition-read + allowed-egress trifecta path as a standing residual (no bare "Addressed").

### Revised if-user-overrides rewind point

Revert this brief's commit(s) on `…-03-auto001`. Survives: the D-23 milestone (PR #230). Restores: the as-adopted D-23 noted-caveat posture. The Round-1→Round-2 history is preserved in-file as the audit trail.

---

## Adversarial-review round 2

Dispatched ≥3 MORE real adversarial reviewers on the **revised brief**, cold (no Round-1 transcript). 3-tier verdicts.

### Reviewer angles dispatched

- Reviewer 4: **Domain practitioner / on-call operator** — does the descope-to-L4 default actually ship value and operate cleanly, or does it quietly kill the factory's reason to exist?
- Reviewer 5: **Methodology-purist / scoping-principle skeptic** — does "policy-only, prevent-build re-enters the bar" hold consistently, or does it still covertly weaken the bar / the autonomy thesis?
- Reviewer 6: **Falsification designer** — name the spike result (or operational outcome) that would falsify the revised decision's central claim; if it can't be named, the decision is too soft.

### Findings

**Reviewer 4 (domain practitioner / on-call) — amendments.** The Round-2 default (descope-to-L4 under any non-PREVENT face) + "any prevent layer re-enters the bar fresh" together form a **one-way ratchet into L4 with no funded exit**: for a young OSS binary, detect-only is the modal outcome, so the modal path is "L4 forever" — quietly trading away v4's reason to exist (the dark factory) while looking prudent. Missing artifacts: an L4 throughput/on-call feasibility analysis (L4 is now the standing default; is batched human review runnable at target volume?), and the **"missing middle"** — per-rig-class autonomy (L5 on classes that structurally can't assemble the trifecta — no private-data reach OR no untrusted input OR no egress; L4 on production-touching classes), which ships real autonomy under a detect-only substrate without re-blessing hardening. Also: an owner is named for *entering* L4 but none for *graduating off* it — no descope-review tripwire.

**Reviewer 5 (methodology-purist) — amendments (deepest).** "Policy only" doesn't fully hold: the 4-cell **consequence table itself pre-decides findings the spike exists to produce** (SILENT⇒worse, MIXED⇒block) — answer-before-evidence, the exact buildability-first anti-pattern D-23 invokes. Fix: demote the table to a **decision *rubric*** — bind the *criterion* the operator applies to spike findings, not the per-branch outcomes. The PREVENT/DETECT/SILENT/MIXED enum is **invented altitude**: real enforcement is a spectrum (syscall/path-glob/symlink-race/partial-namespace), and a result like "prevents reads but only for glob-matched paths, racy on symlinks" maps to no cell. And: the C43 "fence is a *control iff* prevents" rewrite **covertly reframes operator-adopted D-20** (which adopted the fence as the *unconditional* mandatory precondition) — the honest move is to surface this as a *proposed amendment to D-20 requiring operator re-adoption*, not silently restate D-20's text.

**Reviewer 6 (falsification designer) — amendments.** The decision is falsifiable (good). Two concrete escape hatches: (1) **No row for "Test A cannot be run."** The protocol's own §1 prerequisites (Docker daemon, host-staged binaries, `gc` building at Go 1.26.3 vs README's 1.25) may not hold; an inconclusive/not-run spike falls between rows, and under schedule pressure "couldn't run it" gets read as "not-yet-detect-only" and waved through. Add an **INCONCLUSIVE/NOT-RUN row that fails closed** (P2 blocked, L4 default). (2) **Row-1 internal contradiction:** "PREVENT-on-both ⇒ precondition satisfied, no extra work" is falsified by the brief's own C57 trifecta residual — PREVENT-on-both bounds only the cross-partition face while the in-partition-read + allowed-egress path stays open; Row 1 must read "cross-partition face satisfied; trifecta residual independently gates P3b," deleting "no extra work." (3) Name the L4→PREVENT exit evidence/cadence (one-way ratchet otherwise).

**Convergence.** All three endorse the binding-gate **policy** and `accept-with-named-amendments`; none rejects or switches the option. The amendments cluster as: (i) express the gate as a **rubric/criterion**, not a pre-bound outcome enum (R5); (ii) **fail closed** on inconclusive/not-run (R6); (iii) fix Row-1 to keep the **trifecta residual** independently gating (R1+R6); (iv) add the **per-rig-class middle** + L4 feasibility + a named **L4-exit tripwire** (R4); (v) surface the **D-20 reinterpretation** as a proposed re-adoption, not a silent restatement (R5). These strengthen the same option → fold into Final.

### Verdict status

- Reviewer 4 (on-call/value): **`accept-with-named-amendments`** (3 named).
- Reviewer 5 (methodology-purist): **`accept-with-named-amendments`** (3 named).
- Reviewer 6 (falsification): **`accept-with-named-amendments`** (3 named).

All three accept the option with amendments; none switches it. → Fold amendments, finalize (no Round 3).

---

## Final decision (after Round 2)

**Final: the detect-only binding gate is adopted as a policy-level *decision rubric* (not a pre-bound outcome enum), decided 2026-06-01 after 2 rounds of adversarial review.**

### The rubric (binds the criterion, not the branch — R5a)

> **Unattended operation (P2) and self-modification (P3b) require that the Gas City substrate *refuses* (prevents at the tool-call/process boundary), not merely logs, the out-of-boundary accesses within an agent's blast radius — on every face that blast radius can touch. Where the substrate does not prevent on a relevant face, the standing posture is descope-to-L4 (human-in-loop) for the affected rig class, until prevention is independently established. Building a prevent layer to lift that posture is NOT pre-authorized: it must re-enter the bar fresh (owned, costed, P-numbered). The gate pre-commits this *policy*; it mandates no code.**

The operator applies this rubric to the spike's *findings*. Enforcement is a **spectrum**, not a 4-cell enum (R5b); the rows below are *illustrative shapes* of how findings map to the rubric, not an exhaustive taxonomy:

| Illustrative spike finding | Rubric outcome |
|---|---|
| Substrate **refuses** on all blast-radius-relevant faces (verified A1 **and** A2) | Cross-partition precondition satisfied. **The in-partition-read + allowed-egress trifecta path is an INDEPENDENT C57 residual that still gates P3b** (R6-2; not "no extra work"). |
| Substrate **logs-only** on a relevant face (detect-only) | P2/P3b **blocked** for affected rig classes; default posture **descope-to-L4**. |
| Substrate **silent** on a relevant face (access succeeds, no trail) | **Blocked**, *worse* than detect-only — C34 holdout audit is also unsound on that face. |
| Substrate **prevents partially / spectrum result** that fits no clean cell | Operator applies the rubric per-face to the actual finding; default = treat the un-refused face as non-PREVENT (blocked) until shown otherwise. |
| **Spike INCONCLUSIVE or NOT-RUN** (no Docker / `gc` won't build at Go 1.26.3 / ambiguous) | **Fails closed** (R6-1): treat as non-PREVENT ⇒ P2 blocked, L4 default. "Couldn't run it" ≠ "safe." |

### Folded amendments (all Round-1 + Round-2)

1. **Gate = policy/rubric, no build; prevent layer de-blessed** (R2/R5a). Any prevent build re-enters the bar fresh.
2. **Fail closed on inconclusive/not-run** (R6-1).
3. **Trifecta residual is independent and standing** (R1, R6-2): full-PREVENT bounds the cross-partition face only; the in-partition-read + allowed-egress path → **C57 residual** (no bare "Addressed").
4. **Per-rig-class "missing middle"** (R4a): unattended/L5 is permittable on rig classes that *structurally cannot* assemble the trifecta (no private-data reach **or** no untrusted input **or** no egress), independent of the global substrate verdict. This ships autonomy value under a detect-only substrate without re-blessing hardening.
5. **L4 feasibility artifact** (R4b): a throughput/on-call note for the L4 review queue is a P2-entry artifact, since L4 is the standing default.
6. **Named L4→PREVENT exit tripwire** (R4c, R6-3): an owner + periodic review date for graduating off L4, and the evidence under which the operator may authorize broader unattended operation. Not a one-way ratchet.
7. **D-20 governance** (R5c): reframing C43's fence as "a control *iff* the substrate prevents" is a **proposed amendment to operator-adopted D-20**, surfaced for operator re-adoption as a **morning-review item** — NOT a silent in-brief reinterpretation. Until the operator re-adopts, D-20 stands as written and this brief's C43 wording is a *proposal*.
8. **Strike C34 weaker-guarantee-with-sign-off** (R1); **L4 not asserted safe** — its residual is bound to D-21's checkpoint cadence + named artifact (R1).

### Final downstream impact

- **D-23 protocol §6:** results→decision column adopts the rubric (incl. the INCONCLUSIVE/NOT-RUN fail-closed row and the spectrum/per-face reading).
- **C43 / C34 / C42 / C56:** carry the rubric as a *proposed* P2-entry gate, explicitly flagged pending operator re-adoption of D-20's conditionality (item 7). Per-rig-class autonomy added to C56.
- **C57:** add the in-partition-read + allowed-egress trifecta path as a standing residual; add "substrate-silent face ⇒ C34 audit unsound" as a residual.
- These spec edits are **deferred to a follow-up** (this brief is the decision; the spec wiring is a separate Sweep-2 wave) and are gated on the operator re-adoption flagged in item 7 — so this run does NOT silently rewrite the operator-adopted D-20 in the specs.

### Final if-user-overrides rewind point

Revert this brief's commits on `…-03-auto001`. Survives: the D-23 milestone (PR #230). Restores: the as-adopted D-23 noted-caveat posture. **Morning-review item:** does the operator re-adopt D-20 as *conditional on substrate prevention* (the rubric above), or keep D-20 unconditional + treat detect-only as a noted caveat (the original adoption)? Lead recommendation: re-adopt as conditional (the rubric), because an unconditional "fence" that the substrate doesn't enforce is a declaration, not a control — but this is a genuine operator risk-tolerance call, surfaced not auto-applied.

**Final: adopted as a policy-level rubric (binding criterion, fail-closed, per-rig-class, trifecta-residual-preserved), pending operator re-adoption of D-20's conditionality — 2 rounds, 6 real adversaries.**
