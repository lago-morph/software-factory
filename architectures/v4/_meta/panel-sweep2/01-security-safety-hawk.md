# Panel Sweep-2 — Security / Safety Hawk opinion (C43 / C34 / C42 / C01 prevent-gate)

**Reviewer angle:** attack the SAFETY of the "safe self-build" claim — the safety + self-build apex of the 25-component spine.
**Scope read:** C43 (isolation boundary), C34 (holdout integrity), C42 (rig partitioning), C01 §5.1/§8.1 (conformance/prevent-gate), `gascity-conformance-check.md`, review-log D-20 / D-23 / D-30.
**Date:** 2026-06-01.

---

## VERDICT: `right-idea-change-X-before-building`

The ownership split (D-13) is clean, the deterministic-typing keep (C43) is the right shape, and the HumanGated-until-prevention posture (D-30) is the *correct* interim stance. The shape is sound. But two things must change before the first self-build, and one claim must be relabeled. The fence is being built on a substrate fact that **has never once been observed** — and the specs, while admirably honest about this in prose, encode interim postures that quietly assume the unobserved fact will come out favorably.

---

## The single sharpest objection

**D-30 makes "prevent (block), not detect" a hard precondition for unattended (P2) and self-modification (P3b). The factual basis for whether that precondition can ever be met natively — Test A, the conformance KEYSTONE — has never been run. All 14 conformance tests are status OWED; the Results Record in `gascity-conformance-check.md` is entirely empty (every cell a dash). So at the moment of first self-build, the *realized* boundary around a self-modifying agent with broad Bash/network/fs access is exactly what XC-8 called detection-only: C42 *declares* the partition, C34 *detects after the fact* (and by its own `trail_completeness_caveat` "may miss raw filesystem reads" — `cat scenarios/…` via Bash — until C43 lands), and C43's blast-radius bound is *aspirational* because C44 twins (Phase 3c) do not yet exist, so a `twin`-typed surface has no twin to route to (C43 §3.2, INV "Aspirational-until-twins"). The "safe self-build" is safe in this window ONLY because the human gate is genuinely binding (D-30: unattended is blocked until prevention is established). That posture is sound as an interim — but it is being treated as a near-term formality pending a spike, when in fact the spike requires Docker, has not run, and its worst-case outcome (A2 SILENT) means an agent with shell access can read cross-rig files AND the plaintext `city.toml` secrets (G37 unsolved, D-25) with no trace whatsoever. The interim is not a brief gap before a likely-PREVENT result; it is an open, unbounded-duration, detection-or-worse window whose closure depends on an unrun test that may force an OS-level watcher that is, by D-30, undesigned. The HumanGated posture is the right call; the risk is that the org treats "HumanGated pending spike" as low-urgency rather than as a hard STOP on any lights-out self-build.**

---

## Findings (with severity)

### F-HAWK-1 (BLOCKER) — The prevent-gate's keystone is unrun; first self-build must not treat HumanGated as a soft state.
D-30 requires BLOCK for P2/P3b. The gate that decides whether BLOCK is achievable natively is conformance Test A (A1 bead/tool layer + A2 OS/Bash layer), routed by worst-case composite. **Status: OWED — never executed** (`gascity-conformance-check.md` §Live-run status; Results Record empty; C01 E-C01-09 "Prevent-vs-detect outcome unknown"). Until Test A runs and returns overall-PREVENT, the only safe posture is full human-in-the-loop on every self-modifying step. The specs say this (C43 §5.1 `HumanGated`; AC-C43-09; C34 OQ-C34-1; C42 §6 E-C42-04 D-30 note), so it is *consistent* — but the **change-before-building** is operational, not textual: **Test A must be run (Docker stood up) before any P2/P3b run is authorized, and the org must hold the line that "HumanGated pending spike" blocks lights-out self-build, full stop.** This is the de-risking action PF-1 already flagged; it is still owed.

### F-HAWK-2 (MAJOR) — In the pre-spike + pre-twin window, the trifecta blast-radius bound is a *declaration*, not a *control* — and the spec is right that it is, which is the problem.
C43's deterministic boundary-typing (Bash/net/fs, twin-by-default) is necessary but **not sufficient** to bound a self-modifying agent while C44 (twins) is deferred to Phase 3c. C43 itself concedes this: the `twin` type "is the intent, not the realized route" (§3.2), the bound is "aspirational until C44 ships" (INV; §3.1 `twin_id` omittable Phase 0→3b), and the dropped C43 enforcement-grant layer (C02-04) + dropped spawn-time OS jail (C04-05) mean **C43 polices nothing at tool-call time itself** — it relies entirely on (a) C04/C42 process boundaries and (b) C44 twins, of which (b) does not yet exist. So during the self-build window the typing is metadata. The blast-radius is held by C04/C42's process/worktree boundary alone — whose enforcement *strength* is the very thing Test A has not measured. **Net: deterministic typing alone does NOT bound a self-modifying agent in the P0→3b window; it is one of three layers and the only one that exists is the unverified one.**

### F-HAWK-3 (MAJOR) — F12 / F44 / F56 / F33 / F51 are carried in F-MODE-COVERAGE as bare "Addressed"; only the per-component spec text qualifies them.
This is the "claims Addressed that are actually only detected (or only declared)" finding. C43 §6 and §1 are scrupulously honest — every "Addressed" is led with "Addressed-on-paper until twins land" + the G31/XC-8 caveat, and the C43 AMBIGUITY block explicitly rejects Reading B ("status implies a present control"). C34 §6 does the same for F28 ("Addressed-on-paper / detect-after-the-fact"). **The defect is not in the specs — it is that the source register (F-MODE-COVERAGE) still shows the bare token "Addressed" with no phase qualifier.** Any downstream reader (C57, an operator, a future self-build planner) who reads the coverage map and not the full C43/C34 prose will over-trust five lethal-trifecta-class modes. **Change before building: C57's residual register must carry the "Addressed-on-paper / realized-at-P3c / detect-only-until-prevention" qualifier inline on F12/F28/F44/F56, not only by reference.** (C43 AC-C43-11 asks for this for G31; it must also cover F33/F51, which currently read as clean deterministic-guard wins but inherit the same twins-unbuilt caveat.)

### F-HAWK-4 (MAJOR) — RSI / objective-drift (G35) blast-radius is split correctly, but the drift half has no tripwire active at first self-build.
C43 correctly owns only the *blast-radius* half of G35 and routes the *objective-drift / fix-ship-authorization* half to C39/C56/C35 (C43 §6 G35 row). But D-21 puts the real drift detector before *L5 lights-out*, and PF-3 (a cheap mechanical tripwire active from the first P3b self-modification) is an **unadopted** panel recommendation. So at first self-build (P3b, pre-L5), drift mitigation is a periodic *human checkpoint* only (D-21 Option A). Combined with F-HAWK-2 (blast radius is declaration-only) and F-HAWK-1 (prevention unverified), the self-build window has: no realized blast-radius bound, no prevention, and no mechanical drift tripwire — only human review at batched points. That is defensible *if and only if* the human gate is per-step at P3b, not batched. **The specs do not pin P3b human-review granularity to per-step; this should be made explicit before first self-build.**

### F-HAWK-5 (MINOR, compounding) — Plaintext secrets (G37) make the A2-SILENT branch materially worse, and this coupling is under-stated.
G37 (secrets in plaintext `city.toml`/env, deferred per D-14/D-25) is treated as a minor, separable gap in C43 §6. But conformance Test A2's SILENT outcome explicitly includes "read cross-rig files and **city secrets** without any detection" (`gascity-conformance-check.md` A2 SILENT). A self-modifying agent that can read `city.toml` reads production credentials in clear. The secrets gap is not separable from the trifecta blast-radius in the pre-prevent window — it is a force-multiplier on it. **Recommend C57 record G37 × A2-SILENT as a single compound residual, not two minor independent ones.**

---

## Is the HumanGated-until-prevention posture a sound interim, or does it understate exposure?

**The posture is the right design choice; the framing understates exposure in three specific ways.** It is sound that D-30 blocks unattended operation until prevention is established (native or watcher) — that is the correct conservative stance and it directly closes the XC-8 detection-only hazard *for attended operation*. What understates the exposure:
1. The interim is presented as "pending the D-23 spike" as though the spike is imminent; it requires Docker, has never run, and **its worst-case result mandates an OS-level watcher that is undesigned** (D-30 defers the watcher design). The interim could be long.
2. During the interim the realized control is detection-or-worse (F-HAWK-2), and the audit that provides the "detection" floor itself may miss raw Bash reads (C34 `trail_completeness_caveat`). So "HumanGated + detection backstop" overstates the backstop: it is "HumanGated + best-effort detection that has a known blind spot the unrun spike is supposed to size."
3. The human gate's *granularity* at P3b is not pinned (F-HAWK-4). "Human-in-the-loop" with batched review is meaningfully weaker than per-step review for a self-modifying agent.

---

## Recommended change-before-building (ordered)

1. **Run conformance Test A before authorizing any P2/P3b self-build** (stand up Docker; PF-1). Record the composite verdict. Treat overall-PREVENT as the *only* result that lifts HumanGated. This is the gate, not a caveat.
2. **Pin P3b human-review granularity to per-step (not batched)** until both (a) Test A returns overall-PREVENT or the D-30 watcher is built+gating, and (b) a mechanical drift tripwire (PF-3) is active. Make this an explicit precondition in C56/C39.
3. **Propagate the phase/strength qualifier inline into C57's register** for F12/F28/F33/F44/F51/F56 — never the bare "Addressed" — and record G37 × A2-SILENT as one compound residual (F-HAWK-3, F-HAWK-5).
4. **Do not let the deferred watcher design become a silent gap:** if Test A is not run before the self-build milestone, the watcher cannot be designed, so the milestone is blocked by construction. Make that dependency explicit on the critical path.

**Bottom line on proceeding to first self-build:** NOT safe to proceed to an *unattended or batched-review* self-build until Test A is run and returns overall-PREVENT (or the watcher is built and gating). It IS safe to proceed to a *per-step human-gated* first self-build now, because the human gate is the real control while typing is aspirational and prevention is unverified — provided the org treats HumanGated as a hard STOP on lights-out, not a formality. The architecture's shape supports this; the risk is purely in treating the unrun spike as low-urgency.
