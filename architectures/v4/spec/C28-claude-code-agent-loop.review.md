# Adversarial review — C28 Claude Code Agent Loop (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Agent Loop
Target: spec/C28-claude-code-agent-loop.md + plan-faithful/C28-claude-code-agent-loop.md
Charter: single canonical track. Track-A posture = attack FIDELITY and COMPLETENESS (not the design),
PLUS the capability-for-principle bar ([`HANDOFF.md`](../_meta/HANDOFF.md) §2 / [`SURVIVOR-PASS.md`](../_meta/SURVIVOR-PASS.md) C28 = all 7 deltas DROP, keep 0).

## Summary of posture checks (the bar)

- **Dropped-delta reintroduction:** NONE. Survivor-pass dropped all 7 C28 deltas (AgentLoopProvider
  contract, token/quota governor + admission control, multi-seat/seat-pool, capability/egress profile
  per invocation, deterministic context-budget management, provider-floor conformance suite,
  hooks/skills/subagents/MCP as typed config). I grepped the spec + plan for each: the only hit is
  "multi-seat / multi-session" inside **OQ3**, where it is correctly framed as a *deferred open question*
  ("is multi-seat ... in scope, and who owns it") and §7 Scale explicitly says "do not invent." The
  `[FAITHFUL-FILL]` on registration (§3) chooses declarative `.claude/` + C03 config and states "No new
  interface invented" — it does **not** redefine the four surfaces as custom typed config. PASS.
- **Capability-for-principle bar:** the only mitigations the spec names for the cost/scale gaps are
  **C29 cost/family-aware routing** and **C04 session suspension** — both existing-stack capability, and
  the spec explicitly says "No new mechanism may be invented in Track A." PASS.
- **Binding decisions D-1..D-5:** none violated (C28 touches none of them directly; the same-provider
  judge / namespace / bead-schema-ownership / hash-chain rulings are out of C28's surface).
- **Invented architecture:** none. Every behavioral claim is the adopted Claude-Code loop made explicit,
  flagged `[FAITHFUL-FILL]`.

## Findings

### RC28-01 — major — Systematic mis-citation: README (and AI-CONTEXT) content attributed to `one-shot-specs-and-research.md` at line numbers the file does not have
**Claim.** The spec repeatedly cites `one-shot-specs-and-research.md` for content that lives in
[`README.md`](../README.md). The source header cites "one-shot-specs L21, L119–124, L212–218, L240,
L289, L336"; §1-NOT cites "one-shot-specs L121" and "(one-shot-specs L240 cross-session continuity)";
§3 interface 6 cites "one-shot-specs L240"; **AC1** cites "one-shot-specs L537" and **AC2** cites
"one-shot-specs L539". **Evidence.** [`one-shot-specs-and-research.md`](../one-shot-specs-and-research.md)
is **122 lines long** (`wc -l` = 122; last non-empty line 122). Lines 119–124 are blank/EOF-adjacent and
212/240/289/336/537/539 **do not exist**. Only L21 is real (the `coding-agent-loop-spec.md` table row).
The text AC1 quotes — "Verify Claude Code runs in the Gas City tmux runtime with attribution flowing into
beads" — is verbatim **README L537** (Phase-0 "Concrete first steps" checklist). AC2's text ("Set up an
OpenTelemetry Collector ...") is verbatim **README L539**. "Cross-session continuity" is **README L240**
("Resume after agent restarts | Gas City session resume + Claude Code session-id"). For a Track-A faithful
spec the citation IS the audit trail; pointing at a 122-line file with L537 refs is a fidelity defect even
though the underlying facts are real and correctly stated. **Fix (applied).** Retargeted every
`one-shot-specs-and-research.md` reference whose content is in README to the correct README line: source
header, §1-NOT, §3 interface 6, AC1, AC2. The one genuine one-shot-specs reference (L21, the agent-loop
spec row) is kept. No factual claim changed — only the source pointer corrected.

### RC28-02 — minor — "convergent four-layer shape" relabels v4's "Three-layer + persistence"
**Claim.** §1 calls the architecture the "convergent four-layer shape (AI-CONTEXT §2, L48–52)" and says
C28 "occupies layers 1+2." **Evidence.** [`AI-CONTEXT.md`](../AI-CONTEXT.md) §2 (L48) heads the list
"**Three-layer + persistence:**" with items 1 LLM client, 2 agent loop, 3 pipeline engine, 4 persistence;
[`README.md`](../README.md) L113 is "**Principle 2 — Three-layer architecture**" and L61 "three layers,
plus persistence." So the canonical name is *three-layer (+persistence)*, not "four-layer." The "1+2"
claim is correct (LLM client + agent loop are list items 1 and 2). The relabel is defensible but is a
fill presented as v4's wording. **Fix (applied).** Reworded to "convergent three-layer-plus-persistence
shape" and kept the "layers 1+2 (LLM client + agent loop)" mapping, matching the source heading.

### RC28-03 — minor — §13.3 partition line citations are off by a few lines
**Claim.** §1 cites the `implementer`-rig / no-`scenarios` partition as "AI-CONTEXT §13.3 L592–597" (§1
body) and "L586–597" (§1-NOT). **Evidence.** The two `[[rig]]` blocks are AI-CONTEXT **L587–596**
(`scenario_authoring` L587–590, `implementer` L592–596 with the "explicitly does NOT include scenarios"
comment at L596). The cited ranges bracket the right region but are loose. **Fix (applied).** Tightened
both citations to §13.3 L592–596 (the `implementer` block) / L587–596 (both rigs). Trivial precision fix.

### RC28-04 — minor — G12/G13/G34 are correctly deferred; one header label conflates G34 and G13
**Claim.** §6's second gap block is headed "[AMBIGUITY: G34 / G13]" and titled "Single-Max-seat throughput
& cost ceiling." **Evidence.** [`ambiguities-and-gaps.md`](../_meta/ambiguities-and-gaps.md) treats G13
(cost/throughput vs the $200 subscription, "no token-budget math") and G34 (the agent-side scale ceiling)
as **distinct** gaps. The spec body actually handles both correctly and splits them back out into OQ2
(G13/G32) and OQ3 (G34); only the merged header is imprecise. This is the inverse of a fidelity problem —
the gaps ARE addressed-or-deferred-with-reason ("Reading B is correct on the facts; v4 simply has not
modeled it ... the quantification is deferred"), consistent with C04's identical G12/G34 handling. No
resolution is fabricated; no new mechanism is invented. **Fix (applied).** Kept the combined block (the
two gaps share one root cause and one deferral) but reworded the header to name both gaps with their
distinct scopes ("G13 cost/throughput + G34 scale ceiling") so the label matches the gap doc. Substance
unchanged.

### RC28-05 — minor — G12 deferral is sound and matches C04; flag only that the OQ→review-log entries are not yet written (orchestrator task, not C28's)
**Claim.** §6 G12 block and OQ1 defer the Max→API-key fallback to review-log ("This is a deferral, not a
resolution — escalated to review-log"); the plan T9/DoD say findings will be "written in
`_meta/review-log.md`." **Evidence.** [`review-log.md`](../_meta/review-log.md) currently has **no C28
entry** (grep returns nothing). This is consistent with C04, whose identical G12 OQ also points at
review-log without a written entry yet — i.e. the review-log population is a cross-component orchestrator
pass (HANDOFF §3 item "Adversary review wave"), not a single-component authoring obligation. The spec's
deferral language is correct and the contradiction it names (Max "No separate API key issued" vs §14
"have API-key fallback ready") is real and faithfully recorded. **No fix needed in C28's files**; noted so
the orchestrator's review-log pass picks up C28 OQ1–OQ4 alongside C04 OQ1/OQ3 (they are shared). DEFERRED —
review-log population is an orchestrator step, out of C28's edit scope.

### RC28-06 — minor — AC1 "dispatches at least one tool" + I3 "no silent turns" are slightly stronger than the cited source, but defensible as faithful restatement
**Claim.** I3 asserts "Every C28 action is attributed (session-id) and telemetered (raw API bodies) — no
silent turns," and AC6/I1 assert "no token leaves Claude Code." **Evidence.** The telemetry totality
("no turn runs un-telemetered") is actually an **adopted-substrate property injected by C04** (C04 I3 says
the env injection is C04's but the "no-bypass totality" is "an adopted-substrate property verified by the
`runtimetest/conformance.go` gate, not a guarantee C04-the-spec independently enforces"). C28's I3 states
the property as if C28 upholds it, when C28 only *emits* given C04's injection. The OAuth-egress constraint
(I1) is solidly AI-CONTEXT §4.1 L147. **Fix (applied).** Qualified I3 to note the no-silent-turns totality
rests on C04's env injection (C04 I3) + the conformance gate, mirroring C04's own hedge — so C28 does not
overclaim a guarantee it inherits. Consistent with the §1 "C28 runs inside a C04 session" framing.

## Verdict

**accept-with-fixes.** The spec is faithful, correctly scoped, and — importantly under this run's bar —
reintroduces **none** of the 7 dropped C28 deltas: no token/quota governor, no admission control, no
deterministic context-budget management, no multi-seat pool, no per-invocation egress/capability profile,
no provider-floor conformance suite, no hooks/skills/MCP-as-typed-config. G12/G13/G34 are each
addressed-or-deferred-with-a-stated-reason and routed to OQs, matching C04's twin handling; no gap is
falsely "resolved." The one material defect is RC28-01 — a systematic mis-citation pointing real README
(and one AI-CONTEXT) facts at a 122-line file at impossible line numbers — which is mechanically fixable
and now fixed in place (citations retargeted, no fact changed). Remaining fixes are precision/label
tightening (RC28-02/03/04) and an inherited-property hedge (RC28-06). The only DEFERRED item (RC28-05) is
the review-log population, which is an orchestrator-level cross-component pass, not within C28's edit scope.
No blockers; nothing architecturally significant left unapplied.
