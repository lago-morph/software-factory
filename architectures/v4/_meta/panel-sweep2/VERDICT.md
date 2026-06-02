# Sweep-2 spine — expert-panel verdict (2026-06-01)

Five real adversarial opus personas reviewed the Sweep-2 implementation-depth of the 25-component safe-self-build spine, focused on the safety + self-build apex. Each opinion is a sibling file in this directory (`01`–`05`).

## Headline

**The spine SHAPE is sound; the build is gated on substrate verification and four (now-fixed) seam contradictions — not on architecture.** Verdicts: **4/5 `right-idea-change-X-before-building`**, **1/5 `sound-as-is`**. This mirrors the prior whole-corpus panel ("right idea, change X before building") — the changes are refinements and a verified-substrate precondition, not a redesign.

## Per-persona

| # | Persona | Verdict | Sharpest objection |
|---|---|---|---|
| 01 | Security/safety hawk | right-idea-change-X | The prevent-gate keystone (conformance Test A) is **unrun**; `HumanGated` must be a hard STOP, not a soft "pending-spike". Pre-spike + pre-twin, the trifecta bound is a *declaration*, not a control — blast radius rests on C04/C42 process boundaries whose strength is unmeasured. |
| 02 | Self-modification skeptic | right-idea-change-X | The C53 go/no-go bar reads `p10 + mean` but **discards `std_dev`** — structurally blind to bimodal/erratic behaviour (the seed of F54 drift). The same-family judge (D-1) is an uncalibrated closed loop (PF-2 "hall of mirrors") the gate treats as ground truth. |
| 03 | Substrate realist (G11) | right-idea-change-X | Substrate-honesty discipline is **genuinely good** (all 4 high-risk claims honestly flagged). But the conformance check has gaps: it never asserts `CLAUDE_CODE_OAUTH_TOKEN` reaches the pane (the likely first-deploy failure — silent 401), never wires the holdout `read_partition` grammar (can false-green C34), and Test B targets deferred twins yet the runbook makes it blocking. |
| 04 | Integration adversary | right-idea-change-X | **Four uncaught cross-product seam contradictions** the cluster reviews missed (C52↔C53 deadlock, `factory_build` enum collision, C09↔C05 ordering, C41 actor-kind). Now fixed (D-41). |
| 05 | Capability-bar purist | **sound-as-is** | **No over-build.** Depth was achieved by concretizing v4 OQs + wrapping the stack, not re-growing dropped hardening (C31 even ships an acceptance test *for the absence* of a custom runner). D-35/D-36 correctly foreclose C13/C24 pull-ins. |

## Change-before-building list (consolidated)

1. **C53 go/no-go rule shape (operator sign-off — see decision brief `auto-002`).** Panel recommends `p10 ≥ T_tail AND mean ≥ T_central AND std_dev ≤ T_spread` (add the spread ceiling — `std_dev` is already in `GoNoGoInput`), plus a `MinScenarios` floor and a PF-2 judge-FP-rate precondition. Thresholds remain operator policy.
2. **Prevent-gate posture.** Per-step **human-gated** first self-build is safe *now*; unattended/batched-review is **not** until conformance Test A returns overall-PREVENT (or the deferred D-30 watcher is built). Pin per-step review; run Test A the moment a Docker env exists.
3. **Conformance-check gaps (03).** Add an OAuth-token-reaches-pane assertion; wire the holdout `read_partition` grammar into Test A; make Test B (twins) non-blocking in the spine runbook (C44 is deferred).
4. **F-MODE-COVERAGE qualifiers (01).** Carry the phase/strength qualifier inline for the five trifecta-class modes (F12/F44/F56/F33/F51) so downstream doesn't over-trust bare "Addressed"; record the G37 × A2-SILENT plaintext-secrets compound residual. (C57-owned; non-spine.)
5. **Four integration fixes (04).** Done this run — D-41.

## Morning-review items surfaced

- **The C53 go/no-go rule shape** (decision brief `auto-002`) — the headline operator-judgment fork. Lead recommendation (post-panel): adopt the 3-term `p10 AND mean AND std_dev` default; operator confirms the shape + sets thresholds before the milestone is armed.
- Reaffirmed: the **owed empirical D-23 spike** (needs Docker) gates the unattended face + the D-30 watcher decision.

## What the panel did NOT find

No architectural rejection; no over-build; no missing spine component; the substrate-honesty discipline and the seam-decision ledger (D-31..D-41) were praised. The build can proceed to an attended Phase-0 substrate build now; the unattended/self-build face waits on the spike.
