# Adversarial review — C04 Session & Provider Runtime (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Runtime Substrate
Target: spec/C04-session-provider.md (+ plan-faithful/C04-session-provider.md)
Charter: single canonical track. Track-A posture in force — attack **FIDELITY** and **COMPLETENESS**, not
the design — **plus** the capability-for-principle bar (HANDOFF §2): flag any addition that *hardens*
existing-stack capability (Gas City `runtime.Provider`, Claude Code session.id, tmux/k8s/subprocess,
prometheus/opentelemetry) instead of adding NEW capability tied to a 12-principle; when in doubt → DROP.

## Findings

### RC04-01 — major — Invented a non-canonical F-mode label ("F-(crash/restart)") and omitted the two canonical F-modes (F16, F22) that F-MODE-COVERAGE assigns to session/resume territory; in doing so overstated resume as "Addressed/lossless"
**Claim.** §6's failure table lists **F31** plus an ad-hoc **"F-(crash/restart)"** row that asserts
process/sandbox death is **"Addressed by I2 continuity: session resume + session-id restore."** I2 (§3) and
§5 likewise present resume as restoring "the same logical session" / "the restored context" with no
degradation caveat. **Evidence.** The canonical `F-MODE-COVERAGE.md` has **no** F-mode named
"crash/restart"; it has two modes squarely in C04's territory that the spec did not name:
(a) **F16 "Resume-fidelity decay"** → *"CXDB trajectory replay + Gas City session resume; **Partial — KV
cache loss inherent**"* (L33), and (b) **F22 "Zombie agents"** → *"Anomaly detection on session liveness
(PyOD on telemetry); … Addressed"* (L44). So the real F-mode for C04's headline resume claim is rated
**Partial**, not Addressed — KV-cache / in-flight-turn loss on a *crashed* (vs cleanly detached) session is
inherent — and the F22 liveness mode (which the C05 peer spec explicitly hands off to C04's session-
liveness surface, C05 §6 F22) was missing entirely. Inventing a label while dropping the two canonical
rows is a Track-A fidelity defect (mis-mapping + completeness gap), and the un-caveated "lossless" framing
contradicts the corpus's own Partial rating. **Fix (applied).** Replaced the invented row with the two
canonical rows: **F16** carrying its verbatim *"Partial — KV cache loss inherent"* rating (durable session
context + session-id restored so net work + parent-chaining survive, but KV-cache/in-flight-turn state may
be lost), and **F22** framed as *Addressed at the loop level, not C04-native* (C04 surfaces session
`status`; detection is C36's, re-dispatch is C18→C05's). Brought I2 (§3) and the §5 resume prose into line
("restoration is faithfully **Partial** for a crashed session"). **No machinery added** — C04 records the
canonical ratings and routes detection/re-dispatch to their owners; an explicit fidelity *token* and a
heartbeat *producer* are exactly the dropped Track-B DELTAs (see RC04-06) and are left as OQ2/forward-refs.

### RC04-02 — minor — `§5.4 L232` mis-cites the line for the "parent-chain via `session.id`" quote (it is L229); the C28 peer cites it correctly
**Claim.** §1, §2, and §3 each cite **"AI-CONTEXT §5.4 L232"** for the `session.id` parent-chain key (§3
even quotes *"parent-chain via `session.id`"*). **Evidence.** In AI-CONTEXT, the quoted phrase
*"parent-chain via `session.id`"* is on **L229** (the raw-API-bodies→CXDB table row); **L232** is the
unrelated *"Recommended: raw API bodies path"* prose. The C28 spec cites the same fact correctly as
"§5.4 L229". The section ref and quoted text are right; only the line number drifts — minor, but it is a
mis-cite and inconsistent with the peer. **Fix (applied).** Replaced all three `§5.4 L232` → `§5.4 L229`.

### RC04-03 — minor — I3 asserts env injection is a *total no-bypass guarantee C04 enforces*, stronger than v4 backs for an adopted Gas City mechanism
**Claim.** **I3 "env injection is total"** stated that the OAuth+OTEL block "is present in every
started/resumed session, so no turn runs un-telemetered or unauthenticated." **Evidence.** v4 establishes
that the `env = { … }` map is *injected* via Gas City session config (AI-CONTEXT §13.2 L569–580). It does
**not** establish that the adopted Gas City session mechanism guarantees *no bypass* — that env-totality is
an inherited upstream property (the same adopted-primitive caveat the C23 review applied to "records every
action", RC23A-03), to be proven by the conformance gate, not enforced by C04-the-spec. As written it
slightly overstates a guarantee for an adopted concept. **Fix (applied).** Re-worded I3 to separate the
*injection* (C04's, at every start/resume) from the *no-bypass totality* (an adopted-substrate property
verified by `runtimetest/conformance.go` / AC5), not a guarantee C04 independently enforces.

### RC04-04 — minor — `gc converge resume <bead_id>` is a *workflow*-level resume (§16 step 5) presented as the session re-bind itself; defensible but conflates two seams
**Claim.** §3 ("operator-facing resume entry") and §5 step 2 present `gc converge resume <bead_id>`
(AI-CONTEXT §16 L699) as the command by which "C04 re-binds the session by id." **Evidence.** AI-CONTEXT
§16 is the *cold-pickup of an in-progress factory build*: L699 is **step 5 of resuming the build
workflow**, not a session-runtime primitive. The session re-bind is the C04-owned action the workflow
resume *drives*; the optimized twin itself notes the §16 command is "the workflow-level expression of this."
Reading the workflow command as the session API conflates the C40/C52 build-resume seam with C04's
session-resume seam. Faithful and harmless because the former drives the latter, but worth disentangling.
**Fix (applied).** §5 step 2 now states `gc converge resume` is the **workflow-level** resume entry that
*drives* C04's by-id session re-bind, naming the two as distinct seams.

### RC04-05 — minor — F31 handling cites AI-CONTEXT §3.6 L135 (the adoption-vs-extraction recommendation), not the safety-floor basis
**Claim.** §6's F31 row attributed "Addressed" to "AI-CONTEXT §3.6 recommendation **L135**." **Evidence.**
AI-CONTEXT L135 is *"Recommendation tested: full Gas City adoption beats tmux-only extraction … Gas City
provides P1,P2,P3,P4,P9,P10 native"* — an adoption-choice statement, not the single-adapter *safety-floor*
basis. The F31 "Addressed by single-adapter choice" rationale is grounded in `F-MODE-COVERAGE` L73
("v4 uses only Claude Code via Gas City tmux runtime; floor is well-defined and stable") and L148. Minor
mis-citation of the supporting line. **Fix (applied).** Re-pointed the F31 row to F-MODE-COVERAGE L73/L148.

### RC04-06 — positive (no action) — THE BAR check passes: the faithful C04 correctly DROPPED all of the optimized twin's hardening machinery
**Claim/Evidence.** The frozen Track-B twin (`spec-optimized/C04`) adds, as DELTAs, exactly the kind of
existing-stack hardening HANDOFF §2 + the brief say to flag: **DELTA-04** substrate-owned
heartbeat/last-progress/zombie machinery; **DELTA-02** a typed `ResumeToken` fidelity contract;
**DELTA-03** a `CredentialSource` Max→AgentSDK→metered-API fallback ladder (the API-key path G12 names);
**DELTA-06** a multi-session pool/ceiling/drain/supervised-restart. A keyword sweep of the faithful spec +
plan for `heartbeat|watchdog|keepalive|retry|backoff|reconcil|ResumeToken|credential ladder|pool|ceiling`
returns **clean** — the only "custom" hit is plan T1's *"No custom code — config."* The faithful doc keeps
session lifecycle / resume / liveness as **adopted** Gas City `runtime.Provider` behaviour (parked items
live in FE-1..FE-4 / the Track-B reference). This is the correct posture and the headline positive: C04
did not custom-build session/resume/heartbeat machinery the substrate already provides. *No change.*

### RC04-07 — G12 verification (assigned gap) — addressed correctly; no blocker
**Claim/Evidence.** Brief requires verifying G12. The canonical gap (`ambiguities-and-gaps.md` L37, rated
**major**) is "does unattended `claude`-under-Max subprocess automation stay permitted for L4/L5; the
API-key fallback is named but not designed (contradicts §4.1 'No separate API key issued')." C04 §6 +
OQ1 record **both readings** (A: §4.1 L146 "officially supported"; B: §14 fallback vs §4.1 L144 no-key
contradiction) and pick **Reading A as the operating assumption** — *identical* to the C28 twin's G12
resolution (C28 §6 / OQ1), with which it is shared, so the two are consistent. Crucially, C04 frames its
G12 role as **structural, not authorial**: because everything binds to `runtime.Provider` (I1), a future
auth/provider swap is *mechanically a Provider swap behind C04's seam*, but the fallback auth path itself
is **C28/C29 territory and left undesigned** — C04 correctly does **not** invent the API-key path (which
would both violate Track A and be the dropped DELTA-03). All citations verified verbatim against source
(§4.1 L144/L146/L147, §4.2 L151, §16 L695/L699, §3.6 L133/L135, §13.2 L572–580, README L119/L240/L361,
§6.3 L268). Deferral routed to review-log via OQ1. **No fidelity defect; no blocker.**

## Verdict
**accept-with-fixes.** Strong, faithful, well-traced, and — the headline — correctly *restrained*: C04
adopts Gas City's `runtime.Provider` / session-resume / session-id wholesale and drops every piece of the
optimized twin's lifecycle/resume/heartbeat/credential machinery (RC04-06), so it clears the
capability-for-principle bar cleanly. G12 is handled correctly and consistently with C28 (RC04-07). The one
non-trivial fidelity defect (RC04-01) was an F-mode mis-mapping that also overstated resume as lossless;
fixed in place by substituting the canonical F16 ("Partial — KV cache loss inherent") and F22 rows and
aligning I2/§5 — **without** adding any machinery, so the fix stays inside Track A. Remaining fixes
(citation drift §5.4, I3 over-assertion, workflow-vs-session resume conflation, F31 cite) are all
"qualify/correct a citation or an adopted-property claim," applied in place. **Nothing architectural
deferred** — every applied fix is a fidelity correction, not a design choice; the genuinely deferred items
(resume *modes* + resume-failure escalation = OQ2; the undesigned API-key fallback = OQ1/G12; multi-session
scale = OQ3/G34) were already correctly routed to the review-log by the builder and remain there.
