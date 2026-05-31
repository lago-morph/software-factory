# Adversarial review — C24 Telemetry → CXDB Ingestion Bridge (Track A, sweep 1)

Reviewer persona: Subsystem Adversary / critic-fixer — Persistence & Memory (CXDB-sink seam)
Target: spec/C24-telemetry-cxdb-bridge.md + plan-faithful/C24-telemetry-cxdb-bridge.md
Charter: single canonical track. Track-A posture — attack FIDELITY + COMPLETENESS (not the design),
PLUS the capability-for-principle bar (HANDOFF §2: hardening on existing stack capability → DROP;
when in doubt → DROP). Gaps in scope: G26, G27, G33. Two-sink (G04) check from the CXDB-sink side.

## Findings

### RC24-01 — major (OVER-BUILD) — the "durable buffer / pending queue" (I5, §4, INV-1/INV-3) reinvents the spool the inbox filesystem already is
**Claim.** I5 is named "**Durable buffer + retry / back-pressure**" and §4 lists a "**Pending/retry
buffer** — Complete-but-not-yet-acked bodies awaiting CXDB … **Durable local buffer (file or queue dir)**";
plan T7 says "**persist un-acked complete bodies**." This describes a *second* durable store into which the
bridge copies bodies that are already sitting durably in the `OTEL_LOG_RAW_API_BODIES` inbox.
**Evidence / reasoning.** The brief's explicit DROP bar: *"a custom durable-spool state machine (OS
filesystem IS the spool)"* was dropped from the kept P12 capability. A *complete* body file in the inbox is
**already** durably persisted by the OS filesystem; the minimal faithful design is "do not delete/advance
the inbox entry until CXDB acks; retry against the file in place." A separate "pending buffer (file or queue
dir)" that the bridge writes un-acked bodies into is net-new durable-spool machinery v4 never names — it is
hardening, not new capability tied to a principle. The kept capability here is **at-least-once + idempotent
posting + complete-file handling** (which the in-place-inbox design fully satisfies via INV-1's store-side
BLAKE3 no-op), *not* a custom queue. **Fix (applied).** Re-cast I5 / the §4 row / INV-1 / INV-3 / plan-T7
so the durable spool **is the inbox itself**: a complete body is retained *in the inbox* until CXDB acks,
then removed/advanced; "buffer" = "deferred-delete of inbox entries," and an explicit note that no separate
durable queue is introduced (OS filesystem is the spool). Behavior/back-pressure semantics unchanged; the
DROPPED machinery (separate spool store) removed.

### RC24-02 — major (OVER-BUILD / redundant state) — the "inbox cursor / processed set" persisted checkpoint (I5, §4, INV-5) is custom restart-state v4 doesn't name and store idempotency makes unnecessary
**Claim.** §4 lists an "**Inbox cursor / processed set** … **Durable local file**"; INV-5 makes a persisted
"which bodies have been posted" checkpoint a bridge invariant; plan T8 is a dedicated "Checkpoint/cursor +
restart-resume" task on the critical path.
**Evidence / reasoning.** §4 *itself* concedes the state "can be rebuilt by re-scanning the inbox (CXDB
idempotency makes re-posts no-ops), so the cursor/head-map are an *optimization* … not an independent source
of truth." If re-posting is a guaranteed no-op (INV-1, C21 AC-7) and the inbox is the spool (RC24-01), then a
restart can simply re-scan the inbox and re-post — duplicates are harmless. A *persisted processed-set
checkpoint* is therefore a performance optimization v4 never asks for, and the brief's bar drops optimization
that adds custom state without new principle-capability. (Contrast the **per-session head map**, RC24-03,
which is *not* reconstructible from idempotency alone and so is kept.) **Fix (applied).** Demoted the
inbox-cursor from an invariant/owned-durable-state + dedicated task to an **optional sweep-2 performance
optimization** (re-scan-on-restart is the faithful baseline; idempotency makes it correct); INV-5 reworded to
restart-*safety* (no loss, no dup) achieved by re-scan + idempotency, with a durable cursor noted as an
optional optimization. Plan T8 folded accordingly. Marked the residual "is a persisted cursor warranted?"
question into OQ-4-adjacent text rather than asserting the cursor as required.

### RC24-03 — minor — INV-2 / §4 per-session head map: correctly KEPT, but its durability claim should be stated as forced-by-need, not asserted
**Claim.** §4 makes the "Per-`session.id` head map" a "**Durable local state (must survive restart to keep
chaining)**" and INV-2/I3 build the parent-chain on it.
**Evidence / reasoning.** This one *passes* the bar: the parent-pointer for "the next body of an
already-seen session after a restart" is **not** reconstructible from store-side idempotency (idempotency
dedups identical turns; it does not tell the bridge which prior turn is the head of a session). So a head map
is genuine capability needed for INV-2 (the `session.id`→parent-turn mapping v4 names at AI-CONTEXT §5.4
line 229) — keep it. The faithful subtlety the spec glosses: whether the head is *re-derivable from CXDB*
(query the store for the session's current head on restart) vs *must be a bridge-local durable map* is
exactly OQ-3's "across bridge restarts" question — v4 does not force a bridge-local persistent map if CXDB
can be queried for the head. **Fix (applied).** Reworded §4/INV-2 to state the head map is *required state*
(kept) but flagged that its **persistence mechanism** (bridge-local durable map vs re-query CXDB for the
session head on restart) is OQ-3, not settled — so the spec doesn't over-commit to custom durable state where
a store query may suffice.

### RC24-04 — minor (fidelity) — "AI-CONTEXT §5.5 (BLAKE3 idempotency)" is cited as if v4 states idempotency; it is a faithful inference from BLAKE3 CAS/dedup
**Claim.** The §1 Source line cites "§5.5 (BLAKE3 idempotency)"; INV-1/AC-5 lean on "re-posting the same
turn is a no-op (AI-CONTEXT §5.5; spec/C21 §6 AC-7)" as the load-bearing safety property.
**Evidence / reasoning.** AI-CONTEXT §5.5 / §5.3 state **BLAKE3 Blob CAS + dedup + tamper-evidence** (C21
INV-1/INV-4 cite §5.5 line 236 for dedup/tamper-evidence). "Idempotent **ingest** of a re-posted *turn*" is
an inference *built on* CAS-dedup (and one C21 itself makes, but flags as a [FAITHFUL-FILL] reading at C21
§6/AC-7), not a verbatim v4 statement that the bridge can cite as bare fact. The inference is sound and is
the correct faithful basis for at-least-once; it just shouldn't read as "v4 says idempotency." **Fix
(applied).** Adjusted the §1 citation and INV-1's [FAITHFUL-FILL] note to attribute idempotent re-post to
"BLAKE3 CAS/dedup (§5.5) ⇒ re-post no-op, *as ratified by C21 AC-7*" — i.e. a derived property resting on
C21's own faithful reading, not an independent v4 fact. (Already partly hedged in the INV-1 fill; tightened.)

### RC24-05 — minor (fidelity / cross-component) — C25-vs-C28 producer ownership is muddled across §1 and §2
**Claim.** §2's upstream row says "**C28** … dumps untruncated request/response JSON to the inbox," while §1's
NOT-list says "Claude Code's emission of raw bodies to disk (the producer side) is **C25**," and the env
binding is attributed to "C04/C28" in one place and to the "C25 escape-hatch config" in another.
**Evidence / reasoning.** Per the C25 spec (its INV-1…INV-4, §1, §3.1) and inventory, the faithful split is:
**C28** is the *process* that produces the bodies; **C25** is the *interface/contract that activates the
escape hatch* (owns the `OTEL_LOG_RAW_API_BODIES` env binding + emission contract); the env var physically
lives in `[[agent]] env` carried by C03/C04. C24's inventory `depends on` is **C21 + C28** (NOT C25) — so
naming C28 as the dependency is correct, but the prose oscillates between "C28 dumps," "C25 producer," and
"C04/C28 binding" without pinning the C25=contract / C28=emitter / C03-C04=config-carrier split that C25's
own spec fixes. Not a contradiction (each statement is locally true) but a clarity defect that could mislead
on who owns the file-completeness contract (OQ-2). **Fix (applied).** Normalized the producer-side language
in §1 NOT-list and §2 to: *C28 emits the raw bodies; C25 owns the escape-hatch activation contract; the env
binding lives in C03/C04 `[[agent]] env`; C24 depends on C28 (emitter) + C21 (sink)* — matching C25 §1/§3.1
and the inventory. No dependency edge changed.

### RC24-06 — minor — G33 buffer-bound "known limitation" is faithful, but the spec should not imply v4 endorses *any* bounded buffer over plain in-inbox retention
**Claim.** §6 G33 and OQ-4 frame the durability ceiling as "a sufficiently long CXDB outage exceeding the
**buffer** can still lose the oldest window," treating a bounded buffer as the design and its size as the
limit.
**Evidence / reasoning.** Once RC24-01 makes the inbox itself the spool, the honest limit is **inbox disk
capacity** (and the raw-body writer outpacing drain), not a bridge-invented "buffer bound." v4 names no
bridge buffer at all (G26 lists "back-pressure when CXDB is down" as *undefined*); the faithful limit is "the
inbox fills" — which §6's "Inbox disk fills / body writer outpaces bridge" bullet already states correctly.
The two framings (bounded-buffer-overflow vs inbox-fills) are redundant and the first imports machinery
RC24-01 removed. **Fix (applied).** Re-pointed the G33 limit and OQ-4 at **inbox-retention/disk capacity**
(the OS spool's natural bound) rather than a custom buffer bound; kept the genuine open question (is in-inbox
retention sufficient for P11/P12, or does the *optimized* track later want spill/WAL) as the deferred item.

### RC24-07 — minor (consistency, no fix needed) — G27 resolution correctly matches C23's pre-concurred reading (b); verified consistent
**Claim.** §6 G27 binds the **raw-API-bodies** path and treats the event-bus "Lowest impedance" ranking as a
property statement, with C23 remaining a latent source.
**Evidence / reasoning.** This is the binding side of the contradiction C23 §6 deferred to C24, and it
matches C23's adopted reading (b) verbatim in spirit (C23 RC23A-01 even pre-flagged the "events lack the full
bodies" *inference* as an inference, not a v4 fact — and C24 §6 correctly labels its own version "a faithful
inference, not a v4 fact"). The two specs are consistent; the residual contradiction is routed to OQ-1 on
both sides. No over-reach. **No fix** — recorded as a positive consistency check.

## Verdict
**accept-with-fixes.** The spec is faithful on the load-bearing things: the two-sink split is stated from
the CXDB side (OTLP→C26→C27 separate, OTLP→CXDB rejected — G04/C21 INV-6/C25 INV-1 all consistent), G27 is
bound consistently with C23, G26/G33 are addressed at the right seam, the type-bundle and store ownership are
correctly deferred to C22/C21, and no D-1..D-5 decision is violated. The one real problem is **scope creep at
the durability layer**: I5's separate "durable buffer/queue" (RC24-01) and the persisted inbox-cursor
(RC24-02) reinvent the spool the inbox filesystem already provides and the restart-safety that store
idempotency already buys — exactly the custom-durable-spool the bar DROPS. Those are fixed in place by making
the inbox the spool and re-scan-on-restart the baseline; the genuinely-needed per-session head map (RC24-03)
is kept but its persistence mechanism left open. Remaining fixes are fidelity tightenings (idempotency as
derived not stated; C25/C28 producer split). Nothing architecturally significant is deferred unapplied — the
buffer-bound→inbox-capacity reframing (RC24-06) and head-map persistence (RC24-03) are pushed to existing
OQs rather than left as open spec contradictions.
