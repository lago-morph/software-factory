# Adversarial review — C06 Messaging (Mail + Nudge) (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Runtime Substrate / coordination
Target: spec/C06-agent-messaging.md + plan-faithful/C06-agent-messaging.md
Charter: canonical (single) track → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (HANDOFF §2) — flag any hardening-on-existing-stack-capability that is not
new capability tied to a 12-principle. Gap in scope: **G36** only.

## Findings

### RC06-01 — major — I3/AC3 assert NATIVE-substrate attribution totality for **Nudge**, but v4's cited `created_by` evidence covers only **beads and events**
**Claim.** I3 ("attribution totality") and AC3 state that **every** message — Mail *and* Nudge — carries a
`created_by` actor, "because attribution is the substrate's native stamp (P9, README L226)," and that
"no anonymous coordination message exists" / "there is no path to emit an anonymous coordination message."
**Evidence.** README's P9 attribution evidence is explicitly scoped to **beads and events**: "Gas City
beads, events native `created_by`" (L227), "Attribution flows automatically through beads and events"
(L231), "every bead and event carries `created_by`" (L371). A **Nudge** is *ephemeral by construction*
(I2) — it is neither a bead nor necessarily an event (it may leave no durable record at all). v4's support
for "a Nudge carries `created_by`" is the **concept-6 → P9/P10 mapping** (AI-CONTEXT §3.2 L90: Messaging
→ P9, P10) — a row that maps the *concept* to the principle, **not** a demonstration that the ephemeral
signal flows through the same native stamp path the README documents for beads/events. So I3's *absolute*
totality for Nudge ("no anonymous message exists, **because** it is the substrate's native stamp") states
as a demonstrated substrate guarantee what is in fact a faithful inference from the concept→principle
mapping. This is the same class as the C23 review's RC23A-03 (asserting native completeness v4 backs for
beads/events but not for the specific adopted primitive). **Fix (applied).** Qualified I3 and AC3 so the
Mail-side stamp is asserted (Mail *is* a durable record, the bead/event-class path) but the **Nudge** side
is tagged as the concept-6→P9/P10 *faithful inference* — whether the ephemeral Nudge flows through the same
native `created_by` stamp is an adopted-substrate property to verify against real `gc` (sweep-2), not a
guarantee C06-the-spec demonstrates. The "attributed coordination" posture is kept; only the
asserted-as-fact totality over the ephemeral primitive is downgraded to the inference it is.

### RC06-02 — minor — "at-least-once on resume" is stated with invariant/AC force where v4 says only "Mail = durable"
**Claim.** Family 2 ("Delivery is *at-least-once on resume*"), AC1, and the §4 lifecycle assert a specific
delivery guarantee — *at-least-once*, delivered-on-C04-resume. **Evidence.** v4 states only **"Mail =
durable"** (AI-CONTEXT §3.2 L90); README L364 says Phase-0 has "no mail." The *specific* semantics
"at-least-once, drained on run / on C04 resume" is C06's inference about the adopted `[mail]` substrate's
behavior, not a v4 statement. I1 itself already hedges this correctly ("to the extent the adopted Gas City
`[mail]` mechanism provides durable queueing … a substrate property C06 adopts and relies on, not one
C06-the-spec independently implements"), but family 2 / AC1 state "at-least-once" more baldly than I1 does.
**Fix (applied).** Tagged "at-least-once on resume" in family 2 and AC1 as the *adopted-substrate
semantics* C06 relies on (consistent with the I1 hedge), so it is not read as a v4-stated delivery
contract. The C04-resume-delivery claim (the one cross-seam functional behavior, AC1/T5) is kept — it is
the faithful entailment of "durable Mail to a session that was offline."

### RC06-03 — minor — C06 does not acknowledge it is the HMAC-mail-signing **seam** C41 names it as (cross-component consistency)
**Claim.** §1 NOT-list and §6/§7 say C06 "must **not** build a signing subsystem or a secrets store" and
treats the optional HMAC signing as wholly C03(G37)/FE-3 territory; C41 is named only as the identity
authority C06 *consumes*. **Evidence.** C41's spec frames the relationship reciprocally and more specifically:
"C06 owns Mail/Nudge and the *optional HMAC signing* of mail; C41 owns the identity that signing would bind
to" (C41 §1 NOT-list) and lists C06 as "Downstream (consumes the seam) — Optional HMAC mail signing (F32)
binds a message to a C41 actor via the provenance seam" (C41 §2). The inventory assigns **G36 to both C41
and C06**. C06 is correct that it must not *build* signing on the canonical track, but it is silent on the
fact that the HMAC-mail-signing *seam* (where a future signature would attach) is the **C06 Mail envelope**,
binding to **C41's** provenance-verification seam. Without this, the two specs' G36 ownership reads as
under-coordinated. **Fix (applied).** Added a one-line reciprocal note (§1 NOT-list / §6 F32 row) that the
deferred HMAC signature would attach at C06's Mail envelope and bind to C41's provenance seam (C41 §2/§4.3),
so the shared G36 ownership is explicit — without changing the "not built here" disposition.

### RC06-04 — minor — F-MODE-COVERAGE line citations drift by 1–2 lines (content matches)
**Claim.** §6 cites F14 at "F-MODE-COVERAGE L33," F17 at "L84," F32 revisit at "L87"; the header/§6 cite F32
at "L34." **Evidence.** Actual F-MODE-COVERAGE rows: F14 = **L32** (cited L33), F32 = L34 (correct), F17 =
**L86** (cited L84), F32 revisit = L87 (correct). The *content* of every cited row matches what C06 attributes
to it ("P9 attribution + optional HMAC signing layer", "worktree isolation … OPA", "HMAC signing on mail
bus"), so this is citation-precision only, not a substantive mis-cite. **Fix (applied).** Corrected the F14
(L32) and F17 (L86) line references; left the F32 references (already correct).

### RC06-05 — minor — F17 isolation attributed to "C42/C43"; the native mechanism v4 names is C42 worktree isolation (+ OPA straddling C42/C34/C43)
**Claim.** §6 F17 row says "the isolation that prevents shared-dir clobber is C42/C43's." **Evidence.**
F-MODE-COVERAGE L86 names the F17 mechanism as "Gas City worktree isolation per session (native); OPA policy
on shared partitions." Per inventory, *worktree isolation per run* is **C42** (rig partitioning); the OPA /
read-isolation enforcement is **C34** (holdout-integrity enforcement, per D-13) with the lethal-trifecta
blast-radius bound being **C43** (D-13). So "C42/C43" is loose — it omits C42's primary ownership of the
named worktree mechanism and folds in C43 (which owns a *different*, lethal-trifecta concern). The
load-bearing claim (C06 does **not** build locking/coordination-of-writes) is correct regardless.
**Fix (applied).** Re-attributed the F17 isolation to **C42 worktree isolation per run** (the native
mechanism v4 names) with the shared-partition policy noted as C34/C43's per D-13 — matching the inventory and
the binding decision, and keeping the anti-build conclusion.

### RC06-06 — minor — minor source-anchor imprecision: "README L226" used as the `created_by`-native anchor
**Claim.** Several places (§1, I3, behavior, AC3) anchor "native `created_by`" to "README L226." **Evidence.**
The README rows that actually carry the bead/event `created_by` evidence are **L227** ("Gas City beads,
events native `created_by`") and **L231** ("flows automatically through beads and events"); L226 is the
table header row ("Identity model … Gas City `actor` schema"). C41 (the G36 co-owner) anchors the same claim
to README L227/L231/L371. This is a one-line anchor slip, not a fabrication. **Fix (applied).** Repointed the
`created_by`-native anchor to README L227 (and L371 for "every bead and event") where the claim is actually
stated, aligning with C41's citation.

## Verdict

**accept-with-fixes.** The spec is faithful, well-traced, and disciplined on the two things the brief makes
load-bearing: (1) **the bar** — Mail (durable) + Nudge (ephemeral) are treated as NATIVE Gas City primitives,
there is an explicit anti-build NOT-list (§1) and an anti-build audit AC (AC5), no custom queue/broker/
retry/pub-sub/durable-inbox machinery is invented, and **the optional HMAC signing is correctly DROPPED**;
and (2) **G36** — the forged-sender integrity gap is handled exactly as the brief and D-14 require: Reading A
(attribution *presence*, the active P9 control) is the canonical-track operating posture, Reading B
(integrity shortfall, forged-sender undetected) is recorded as the honest residual deferred to **FE-3**
(graduated-mandatory signing, blocked on **G37 = secrets, owned by C03**), it is **not built**, and the F32
"Addressed" label is **qualified, not falsely re-claimed as fully addressed** (AC6, OQ1, escalated to
review-log). FE-3/FE-1, D-14, the F-MODE rows, and the C04/C05/C23/C41 boundaries all verify. No invented
architecture; no [FAITHFUL-FILL] mislabeled as fact beyond the items below. The one **major** finding
(RC06-01) is a fidelity *qualification*, not an architectural defect: I3/AC3 asserted native-substrate
attribution *totality* for the ephemeral **Nudge** where v4's cited `created_by` evidence covers only
beads/events — fixed by tagging the Nudge side as the concept-6→P9/P10 faithful inference (verify vs real
`gc`, sweep-2), matching the C23-review RC23A-03 pattern. All six findings are applied in place (qualify an
adopted/inferred property as such; fix citation drift; add the reciprocal C41 seam note). **Nothing
architecturally significant is deferred** — the only deferrals are the spec's own already-correct OQ1–OQ4
(G36 FE-3 trigger, Mail retention/dead-letter, Nudge gating, addressing granularity), which are sweep-2 /
orchestrator items by design, not review-introduced.
