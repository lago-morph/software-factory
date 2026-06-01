# Overnight summary — v4 Sweep-2 run (D-23 substrate verification + first depth cluster)

**Run date:** 2026-06-01 · **Mode:** autonomous unattended · **Branch model:** stacked PRs (operator-directed) · **Stack:** PRs #229 → #230 → #231 → #232 → (this wrap PR).

> This is the primary review artifact for the run. Read this, the [scope envelope](architectures/v4/_meta/RUN-SCOPE-2026-06-01.md), and the per-PR descriptions; you do not need to read the diffs. The two genuine **operator decisions** are in §6.

## 1. TL;DR

- **The D-23 Gas City reality-check was executed the way you chose — protocol + harvest, no live agents.** I verified empirically (not from a subagent's say-so) that **Gas City is real** (`github.com/gastownhall/gascity`), cloned the `gascity-prototype` you pointed me at, and harvested the substrate facts it already proved into the corpus. **Prevent-vs-detect stays OPEN** (the prototype deferred the smoke test); a runnable spike protocol is now on disk for whoever has Docker.
- **3 "contradictions" the harvest flagged turned out to be 0 true contradictions** after I verified them against the actual specs — v4's discipline of deferring unverified substrate names to G11 held up. Closed OQs: **XC-9, C42:OQ-4, C04:OQ-4**.
- **The run's pivotal decision (auto-001) is settled after 2 rounds of real adversarial review (6 opus reviewers):** if `gc` is detect-only, that's a **binding go/no-go gate** on unattended operation — but expressed as a *policy rubric*, not a pre-blessed build (the reviewers killed my first draft's OS-prevent-layer as a bar violation).
- **First Sweep-2 implementation-depth cluster landed:** the evidence/data substrate (C19/C20/C21/C23/C41) deepened to signatures/schemas/Mermaid/error-taxonomies/acceptance-tests. A seam adversary caught a **HIGH build-breaking contract drift** (C23 `EventId` struct vs C41 bare `uint64`) — fixed as ledger decisions **D-26…D-29**.
- **2 things genuinely need you (§6):** (a) re-adopt D-20 as *conditional on substrate prevention* (the auto-001 rubric) or keep it unconditional; (b) accept the per-rig-class autonomy "missing middle." Both are reversible.
- **Deliberately deferred (§7):** the live spike (your call), Sweep-2 depth for the other ~52 components (long tail), and wiring the auto-001 rubric into C43/C34/C42/C56/C57 (gated on your D-20 re-adoption).

## 2. Suggested merge order

Stack-bottom first; each PR's base is the previous branch, so GitHub auto-retargets to `main` as you merge down the stack:

1. **#229** — scope envelope (the run's contract).
2. **#230** — D-23 spike protocol + substrate harvest + 13 spec annotations + OQ closures.
3. **#231** — auto-001 decision brief (detect-only binding gate). *Merging this records the decision; it does NOT wire the rubric into specs — that's deferred pending your §6(a) re-adoption.*
4. **#232** — Sweep-2 evidence/data-substrate cluster (C19/C20/C21/C23/C41) + seam fixes D-26…D-29.
5. **(this wrap PR)** — this summary + HANDOFF refresh + retrospective.

All five are a linear chain; merge in order. None is safe to merge out of sequence (each depends on its parent's diff).

## 3. PRs opened (in stack order)

| PR | Branch (suffix) | Title | Base | Rewind point |
|---|---|---|---|---|
| #229 | `…-OpJFZ` | scope envelope | `main` | revert `94d3fc4`+`c6c7f70` → before the run |
| #230 | `…-02-d23-spike` | D-23 protocol + harvest | #229 branch | revert `432335a`→`3a3cb32` → drops D-23 milestone |
| #231 | `…-03-auto001` | auto-001 decision brief | #230 branch | revert `f39b420`→`ad7fec3` → as-adopted D-23 caveat posture |
| #232 | `…-04-sweep2-data` | Sweep-2 data cluster | #231 branch | per-component commits + `D-26..29` ledger + seam-fix commit, individually revertible |
| (wrap) | `…-05-wrap` | wrap kit (summary/HANDOFF/retro) | #232 branch | revert the wrap commit(s) |

PR descriptions are the primary per-chunk review artifact.

## 4. Decision briefs written

| Brief | Question | Rounds | Outcome |
|---|---|---|---|
| [auto-001](architectures/v4/_meta/decisions/auto-001-detect-only-binding-gate.md) | If `gc` is detect-only, what binds on D-20 / unattended P2? | 2 (3+3 real opus adversaries) | **Decided:** policy-level rubric — non-PREVENT substrate ⇒ P2 gated; default discharge = descope-to-L4; prevent layer NOT pre-blessed (re-enters the bar); fail-closed on inconclusive; per-rig-class middle; trifecta residual→C57. Round 1 (pre-blessed OS-prevent discharge) superseded — preserved with strikethrough. |

## 5. Chain status

- **D-23 (Sweep-2 first action): DONE** as protocol + harvest. Empirical prevent-vs-detect run is **owed** (needs a Docker-capable environment; protocol is ready).
- **auto-001: DECIDED**, but its spec wiring (C43/C34/C42/C56/C57) is **deferred** pending operator re-adoption of D-20's conditionality (§6a).
- **Sweep-2 depth: 5 of 57 components done** (the data substrate). ~52 components remain at Sweep-1 depth — the long tail (§7), with a suggested next-cluster order in the [HANDOFF](architectures/v4/_meta/HANDOFF.md).
- **8 expert-panel NEW recommendations:** PF-1 (D-23 spike) addressed; the auto-001 rubric absorbs the panel's binding-gate ask + the shadow-evaluator-adjacent independence concern partially; the rest (judge_independence_tier C33, Unleash pin, shadow evaluator, drift tripwire) remain queued for later clusters (§7).

## 6. Morning-review items (need your input)

**(a) Re-adopt D-20 as *conditional on substrate prevention*?** *(from auto-001)*
- **Question:** D-20 was adopted as an *unconditional* "fence pulled to P2." auto-001 argues an unenforced fence is a *declaration, not a control*, so D-20 should be conditional: unattended P2 requires the substrate to *prevent* (not just log) on the relevant blast-radius face; otherwise descope-to-L4. This reframes an operator-adopted decision, so I did **not** silently apply it.
- **Lead recommendation:** re-adopt as conditional (the rubric). An unenforced fence gives false confidence on a self-modifying factory.
- **Rewind / alternative:** keep D-20 unconditional and treat detect-only as a noted caveat (the original posture) — revert PR #231.

**(b) Accept the per-rig-class autonomy "missing middle"?** *(from auto-001 Round 2)*
- **Question:** Under a detect-only substrate, instead of "L4-forever globally," permit unattended/L5 on rig classes that *structurally cannot* assemble the lethal trifecta (no private-data reach **or** no untrusted input **or** no egress), L4 only on trifecta-capable/production-touching classes. Plus: an L4 throughput/on-call feasibility note as a P2-entry artifact, and a named L4→PREVENT exit tripwire (so "stay L4" isn't a silent permanent trap).
- **Lead recommendation:** accept — it preserves the product's reason to exist (real autonomy) under a detect-only substrate without re-blessing dropped hardening.
- **Rewind / alternative:** global gate only (the simpler, more conservative posture).

*Both are recorded in [auto-001](architectures/v4/_meta/decisions/auto-001-detect-only-binding-gate.md); neither is wired into specs yet.*

## 7. What I deliberately did NOT do

- **Run a live Gas City / spend tokens on live agents** — your explicit decision. The spike is a ready-to-run protocol, not an executed spike. *Binding deferral:* the empirical prevent-vs-detect answer is owed and gates the auto-001 rubric's outcome.
- **Wire the auto-001 rubric into C43/C34/C42/C56/C57** — gated on your §6(a) re-adoption of D-20's conditionality; applying it now would silently relitigate an operator-adopted decision. Flagged in HANDOFF as the first follow-up if you re-adopt.
- **Sweep-2 depth for the other ~52 components** — exceeds one run. Done: C19/C20/C21/C23/C41 (data substrate). Suggested next clusters (workflow engine; eval/holdout — note the holdout cluster is partly gated on §6a): see [HANDOFF](architectures/v4/_meta/HANDOFF.md).
- **The other panel NEW recommendations** (judge_independence_tier on C33, Unleash version-pin, shadow evaluator, pre-L5 drift tripwire) — queued, not done; each belongs with its component's Sweep-2 cluster.
- **Touch `spec-optimized/` / `plan-optimized/`** (frozen) or read the four v4 source docs into primary context (subagents read targeted sections).

## 8. Rewind points (full chain)

| Revert | Undoes |
|---|---|
| whole stack (PRs #229–wrap) | the entire run → back to `origin/main` @ #228 |
| `94d3fc4`,`c6c7f70` (#229) | the scope envelope only |
| `432335a`,`97ac3dd`,`3a3cb32` (#230) | D-23 protocol / ledger OQ-closures / 13 spec annotations |
| `f39b420`,`91c4dad`,`ad7fec3` (#231) | the auto-001 brief (Round 1/Round 2/Final) → restores noted-caveat posture |
| the `D-26..29` ledger commit + seam-fix commit (#232) | the cross-component seam resolutions (keeps the per-component depth) |
| each C19/C20/C21/C23/C41 commit (#232) | that one component's Sweep-2 depth |

## 9. Session metadata

- **Stack:** 5 branches (`…-OpJFZ`, `-02-d23-spike`, `-03-auto001`, `-04-sweep2-data`, `-05-wrap`); one PR each (#229–#232 + wrap).
- **Subagents:** ~14 dispatches — 1 recon, 2 D-23 (protocol+harvest), 1 harvest-integrator, **6 opus adversaries** (auto-001, 2 rounds), 1 C20 opus exemplar builder, 4 sonnet sibling builders, 1 seam reviewer, 1 seam-fix integrator. Each wrote to disk + returned a receipt; the orchestrator owned all git; commit+push every wave.
- **Model choices:** opus for the lead, the auto-001 adversaries, and the C20 exemplar; sonnet for authoring/harvest/integration/sibling-builders/seam-review (per "dynamic model choices; opus for decisions, sonnet in general").
- **Discipline:** empirical verification over subagent narrative (caught a confabulated "gc v1.2.0/brew install"); real-subagent adversarial review (no inline simulation); cross-component decisions through the ledger (D-26…D-29); prevent-vs-detect kept OPEN throughout.
