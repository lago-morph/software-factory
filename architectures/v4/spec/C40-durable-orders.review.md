# Adversarial review — C40 Durable Workflow Engine (Orders) (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Healing Loop
Target: spec/C40-durable-orders.md + plan-faithful/C40-durable-orders.md
Charter: canonical track → attack FIDELITY and COMPLETENESS only (not the design), PLUS the
capability-for-principle bar (flag any addition that hardens existing stack capability rather than
delivering new capability tied to a 12-principle). Binding decisions in force: D-6, D-8.

## Summary of attack surface checked
- **THE BAR (native Orders; no custom engine; no Temporal):** PASS. §1 boundaries, INV-5, AC-6, plan
  §6 bar-check, and risk #5 all enforce "no factory-authored durable-workflow engine / saga /
  compensation / state-machine runtime, and no Temporal integration at sweep 1". Temporal is held as
  the documented deferred upgrade only. G11 "no invented `gc` internals" is repeatedly honored
  (I3 caution, §4 [FAITHFUL-FILL], OQ-2). No bar violation found.
- **D-8 (Order owned by C40; convoy=C05; C12 references-not-defines; C07 glossary):** PASS and
  corroborated against the other docs. C07 line 125 carries the *Order* glossary row pointing to C40
  (verified); C12 lines 59–61 / 149–159 explicitly defer the Order definition to C40 per D-8 (verified);
  the convoy≠Order boundary (§1) matches C07's *Convoy*→C05 row and C12. No ownership drift.
- **G33 (document the durability ceiling honestly; do NOT harden):** PASS. §6 picks reading (b),
  states what survives (Gas-City-internal crash/retry) vs what does not (non-Gas-City OSS-component
  fault-tolerance; exactly-once / HA / cross-process saga → the Temporal-deferral trigger), and routes
  the cross-component partial-failure obligation to C21 §6 (fail-open) / C24 (buffer+retry) — both
  verified to exist and to own exactly that (C21 §6 G33 fail-open; C24 inbox-spool retry). The ceiling
  is stated, not raised. AC-7 makes it a documentation/review gate. This is the strongest part of the doc.
- **Citation fidelity:** every load-bearing README/AI-CONTEXT line was checked against the source and is
  accurate: README 246/258/261, 459–466; AI-CONTEXT §3.1/76, §3.2 concept 3/7/9, §3.3/109, §3.4/122,
  §5.3/220, §3.5/124–129, §10/333, §11.1/486, §9.1/408. C23 cross-refs (I2 ordered-read, I3
  checkpoint/resume-from-seq, C40 listed as a C23 downstream consumer) are consistent with spec/C23 —
  no contradiction.

## Findings

### RC40-01 — major — "Batch 3 / Phase 3b" conflates two non-aligned numbering schemes; C40 is **not** a README Phase-3b bullet
**Claim.** §1 (line 46), §1 Position (lines 107–108), §5 "Enable (**Phase 3b**)" (line 174), §7 Ops
"a **Phase-3b** step" (line 275), §2 C03 row ("on in **Phase 3b**", line 102), and plan §2 ("off until
**Phase 3b**") all place C40's enable in **Phase 3b** and several treat "**Batch 3 / Phase 3b**" as the
same milestone. **Evidence.** These are two *different* decompositions that do **not** map 1:1:
- The **inventory** puts C40 in **Batch 3** (line 111, the "Evaluation, workflow tooling, override
  discipline" batch — "…durable Orders").
- **README Phase 3b** (lines 459–466) is "**P11 components (Healer in pieces)**" and lists exactly:
  anomaly detection, trajectory clustering, diagnosis agent, fix-task bead schema, loop-closure tracking
  — i.e. **C36/C37/C38/C39**, which the inventory places in **Batch 4** (line 113), *not* Batch 3.
  **"Durable workflow / Orders" is NOT one of the Phase-3b build bullets**; it appears only as a row in
  the P11 *capability* table (README line 258).
So C40 (inventory Batch 3) is the durable-Order substrate seam that must be **ready before** the
Phase-3b Healer pieces (inventory Batch 4) turn on and consume it; equating "Batch 3" with "Phase 3b",
and asserting C40 is enabled "in Phase 3b … when the self-healing loop is built", overstates a phase
placement README does not give Orders. The underlying true facts — off at minimum (AI-CONTEXT §3.4),
enabled when the self-healing loop is stood up — are unaffected. **Fix (applied).** Decoupled the two
schemes throughout: C40 is **built in inventory Batch 3** so the Order seam is *standing/ready before*
the **Phase-3b** P11 Healer pieces (Batch 4) consume it; removed the "Batch 3 = Phase 3b" equation and
the "enabled in Phase 3b" overstatement (it is enabled when the self-healing loop is built, which the
Healer pieces are part of), keeping the off-at-minimum fact.

### RC40-02 — major — "C39 fix-task loop-closure is the workflow an Order drives" is an unlabeled inference stated as established; v4 says only "Orders subscribing to crashes/gates", and C39's own deps do not list C40
**Claim.** §1 (line 40, "C39 fix-task loop-closure, **which is the workflow an Order most naturally
drives**"), §2 ("**The canonical workflow an Order drives in P11**", line 103), AC-8 ("drives the P11
workflow"), and plan T8/§2 treat the *Order→C39 fix-task* launch coupling as an established v4
relationship, citing "README §3b". **Evidence.** v4 never states that an Order *drives/launches* the
fix-task or loop-closure chain. What it actually says is narrower: "**Orders subscribing to
crashes/gates**" (AI-CONTEXT §3.1 line 76) — i.e. Orders *trigger off* crash/gate events. The
fix-task→resolution chain is described as a "**Custom bead chain**" + "Bead schema" (README lines
257–259), with no Order named as its carrier. README "Phase 3b" lists the Healer pieces but does **not**
say an Order drives them, so the "README §3b" citation does not support the claim (and README has a
"Phase 3b" section, not a "§3b"). Mild counter-evidence: **C39's own inventory dependency list is
C38/C20/C08 — it does not list C40** (inventory line 51). The coupling is a reasonable *architectural
inference* (an event-triggered durable carrier is the natural thing to drive a crash-triggered fix-task
loop), and the spec does hedge it elsewhere ("typically", and OQ-4 flags the C40↔C39 seam as
unconfirmed) — but §1/§2/AC-8 state it more firmly than v4 supports. **Fix (applied).** Relabeled the
C39-drives-coupling as a faithful *inference* (not a v4 fact) in §1, §2, and AC-8; fixed the "README
§3b" cite to point at what README actually says ("Orders subscribing to crashes/gates", AI-CONTEXT §3.1
line 76; Healer pieces, README Phase 3b); kept OQ-4 as the open seam that must be confirmed with C39.

### RC40-03 — minor — "an Order launches a C12 formula / C13 molecule" is an inference presented as concrete in I3 / §5
**Claim.** I3 ("the Order **launches its workflow** — typically a C12 formula instantiated as a C13
molecule…"), §5 run-path step 3, and §4 [FAITHFUL-FILL] (`launches: <formula|fix_task workflow ref>`)
present formula/molecule as a concrete launch target. **Evidence.** v4 defines an Order as an
"event-triggered **workflow**" (AI-CONTEXT §3.3 line 109) and defines formula/molecule as the workflow
primitive (AI-CONTEXT §3.2 concept 7), so "an Order launches a formula/molecule" is a *natural*
composition — but v4 nowhere states it directly; it is a faithful inference of the same kind as RC40-02.
I3 already hedges with "typically", and §4 is correctly tagged [FAITHFUL-FILL]. The only gap is that
the §5/I3 prose reads slightly more asserted than inferred. **Fix (applied).** Added a half-clause to
I3 marking the formula/molecule (and fix-task) launch target as the *inferred* composition of "Order =
event-triggered workflow" (§3.3) with "formula/molecule = the workflow primitive" (§3.2 concept 7),
pinned to pinned-`gc` at sweep 2 — so it is not read as a v4-stated wiring. No change to §4 (already
labeled).

### RC40-04 — minor — §1 calls C39 the "P11 consumer" while §2 also names C39 a "tightly-coupled consumer"; consistent, but the §3.5 cite span is off-by-one
**Claim.** Minor hygiene: the spec cites AI-CONTEXT "§3.5 (lines 124–129)" for the migration-tail
risk. **Evidence.** §3.5 spans lines 124–130 (header at 124, last bullet at 129–130); harmless. Also
the dual "P11 consumer" (§1) / "tightly-coupled consumer" (§2) labels for C39 are consistent once
RC40-02's inference framing is applied. **Fix (not applied — cosmetic).** Left as-is; the line span is
within rounding and not load-bearing. Noted for sweep-2 cleanup.

## Verdict
**accept-with-fixes.** A strong, faithful, exhaustively-cited spec+plan. The capability-for-principle
bar (native Orders, no custom engine, no Temporal at sweep 1) and the D-8 ownership boundaries are
handled correctly and corroborated against C07/C12/C23. The G33 durability-ceiling disclosure — reading
(b), "state the ceiling, do not harden", with partial-failure routed to C21/C24 — is exactly right and
is the doc's best feature; OQ-1 correctly converts the deferred-Temporal bet into a falsifiable
trigger. The two `major` findings are *fidelity overstatements*, not design problems: (1) "Batch 3 =
Phase 3b" conflates two non-aligned numbering schemes and over-places C40 in a README Phase-3b bullet
list it is not part of (fixed by decoupling the schemes); (2) the Order→C39 launch coupling is an
inference stated as established (fixed by relabeling it an inference and correcting the cite). Both
fixes applied in place; nothing architecturally significant deferred. No blockers.
