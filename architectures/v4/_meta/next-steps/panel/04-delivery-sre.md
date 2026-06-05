# Panel review 04 — Delivery lead / SRE lens

> Reviewer 4 of 6. Angle: is the 2–3 week scope shippable by **one operator on one Max seat**, where
> is the critical path, and what blows the timeline first. Adversarial but constructive.

## 1. Verdict

**`accept-with-named-amendments`.**

The *sequence* is right and operationally honest — calibrate the instrument, drive one nail, then
widen — and it refuses to hand-wave the judge (`oversight_level = full` until calibrated, advisory
`tri_alignment`). That spine is shippable. What is **not** shippable as written is the **scope inside
the window**. The plan front-loads six deliverables (substrate probe + a *new* calibration mechanism +
holdout probe + first code build + a defect-provocation sweep + a four-component line) onto a single
operator who must also stand up *three rig classes* (worker, separate judge, parallel) and personally
review **every** build. Two gates are multi-week projects wearing a gate's clothing. I accept only with
the amendments below re-scoping Gates 1 and 5; without them the honest outcome is Gates 0–3 done and
4–5 slipped — fine, but the plan should *say* that rather than promise the line.

## 2. Top three named amendments

**A1 — CUT/RE-SEQUENCE: Gate 5's batch is mis-picked; the "clusterless slice" is not clusterless.**
Problem: Gate 5 pushes B3 → B16 → B6 → B9 as an unattended *batch*, but the agent-os plan headers say
B16 `estimate: L` upstream `[B3, A1, A6, A5, B13]`, B6 `estimate: XL` upstream `[A1, A2]`, B9
`estimate: L` upstream `[A1, A2, A5]` (`/tmp/agent-os/plans/components/B/plan-B16.md`,
`plan-B6.md`, `plan-B9.md`). A1 is **LiteLLM** — `estimate: XL`, the cluster-bound LLM gateway
(`plan-A1.md`). B3 itself sits on A7 (OPA install, `plan-A7.md`). So three of the four "infra-light"
batch members carry infra-heavy upstreams the factory *cannot build before twins* — the exact
twin-gap the plan names as Risk #3. Fix: replace the batch with genuinely standalone pure-code work
(the brief names the A18 audit-adapter library as a candidate) and explicitly **mark B6/B16/B9
twin-gated and out of the window**. One real second build (e.g. B3's `opa test` layer alone) is a
credible Gate 5; a four-component line is not.

**B2 — Gate 1 is a multi-week project, not a gate.** Problem: Gate 1 *designs and builds* the
PF-2/C46 calibration mechanism the backbone explicitly defers (`10-unified-plan.md` §1, §2 Gate 1;
`spec/C32-judge-harness.md` OQ6). "A small fixed set of human-authored ground-truth root-cause labels
spanning all five corners" with a measured false-green rate is a labelling + tooling effort, and the
bar value and sample size are admitted `[PROPOSED — not in source]` (§2 Gate 1 exit). Authoring
trustworthy five-corner ground truth is judgement-heavy work for the single non-coding operator
(`00-grounding-and-exemplar.md` A7). Fix: time-box Gate 1 to a **fixed tiny N (e.g. 10–15 labelled
trajectories)** declared up front, accept a *coarse* false-green bar, and defer "real" calibration to
the C46 horizon. Otherwise Gate 1 eats week 1 and starves Gate 3.

**B3 — The human-batched-review rhythm contradicts the plan's own oversight rule.** Problem: Gate 5
promises "a batched-review cadence that sustains one batch per review cycle" (§2 Gate 5 exit), but
C53 §3.3 defines `oversight_level = full` as **"every build reviewed"** and makes `full` *mandatory*
while the judge is `uncalibrated` (`spec/C53-bootstrap-validation.md` line 420–421). Since Gate 1
will at best produce a coarse calibration, the operator is still on `full` in Gate 5 — so "batch" is a
fiction: one human reviews every build serially on one seat. Fix: rename the Gate 5 exit to
**"serial human-gated builds, throughput = operator review bandwidth"**, drop "batch/parallel rigs,"
and make the honest claim — *2–3 builds total reviewed in the window*, not a sustained line.

## 3. The single thing most likely to blow the timeline

**Standing up and operating three rig classes (worker + separate cross-family judge + parallel rigs)
on one Max seat, while every judge run is multiplicatively expensive on that same seat.** The plan
itself flags multiplicative single-seat token cost (`00-grounding-and-exemplar.md` A6; §5 Risk #4) and
only measures it at Gate 3 — *after* Gates 0–2 have committed the rig topology. The separate-judge-rig
discipline (`spec/C32-judge-harness.md`) means the judge competes with the worker for the *one* seat's
throughput; "multiple rigs" (§2 Gate 5, `spec/C42-rig-partitioning.md`) is a config partition, not
added compute — parallel rigs on one seat **serialize at the seat**. This is the incoherence the brief
asked about: rig *partitioning* is real; rig *throughput parallelism* is not, on one seat. Move the
Gate-3 cost measurement to a **Gate-0 back-of-envelope** so the topology is sized before it is built.

## 4. What the plan gets right operationally and must be preserved

- **Calibrate-before-trust sequencing.** Refusing to read a green light before earning it
  (`10-unified-plan.md` §0, §3) is exactly right; `tri_alignment` advisory-until-calibrated and
  `oversight_level = full` as the default (C53 §3.3) is the honest on-call posture. Keep it verbatim.
- **Prevent-vs-detect as a near-zero-cost *first* action** (Gate 0; `00-grounding-and-exemplar.md` A2,
  decision #4). Turning the riskiest substrate assumption into a fact before stacking on it is textbook
  SRE discipline — and the detect-only branch already has a compensating audit gate (Gate 2).
- **The defect ledger routed by corner with a fix owner** (§3 table). This is a real triage runbook,
  not a metric vanity board; the corner-rate signal ("spec spike → tighten the crucible") is actionable.
- **B22 design-only as the very first pass** (Gate 0): zero upstreams (`plan-B22.md` upstream `[]`) —
  the right way to prove the pipe before asking it to write code.
- **The accepted fail branch** (Gate 3 `no_go` → "needs more substrate before Phase 3"). A plan that
  names its own honest failure outcome is one I can stand behind on-call.
