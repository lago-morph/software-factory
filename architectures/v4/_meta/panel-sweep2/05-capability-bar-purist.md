# Panel Sweep-2 — 05 · Capability-Bar Purist

**Reviewer angle.** The operator's bar, and nothing else (HANDOFF §2 / SURVIVOR-PASS): *new
capability tied to a named 12-principle → KEEP; polish/hardening that does the same thing "better"
in a non-principle way → DROP; partial satisfaction by the existing stack (Gas City, Inspect AI,
prometheus, scikit-learn, sigstore, …) counts; when in doubt → DROP.* My single question for
Sweep-2: **did implementation-readiness smuggle in scope** — did the depth pass re-grow any
hardening the SURVIVOR-PASS already dropped, or stand up custom machinery the stack already
provides?

**Specs read (purpose / boundary / "the-bar" / dropped sections):** C30, C31, C32(via C31/C33
seams), C33, C34, C43, C51, C53, C29, C08, C09, C52; SURVIVOR-PASS (the per-component DROP/KEEP
ledger), HANDOFF §2, review-log D-35/D-36/D-39, implementation-dependencies §backbone.

**Date:** 2026-06-01.

---

## VERDICT: `sound-as-is`

This is the one axis on which the Sweep-2 corpus is not just defensible but *exemplary*. The depth
pass did **not** reintroduce dropped hardening. Every custom-code spec the brief flagged (C29
stylesheet, C51 predicate, C53 rule, the C33 aggregator) carries an explicit, citation-grounded
**"what got DROPPED / the bar"** section that refuses the exact machinery the SURVIVOR-PASS dropped,
and the two riskiest reinvention temptations — rebuilding Inspect AI (C30/C31/C32/C33) and rebuilding
OS isolation (C43/C34) — are both met by *wrapping* and *typing*, not by re-implementing. I could not
find an over-build flag that survives contact with the bar. The three prior panelists all landed
`right-idea-change-X-before-building`, but every one of their changes is an **honesty / sequencing /
safety** fix (run Test A, pin per-step review, add a std_dev gate, wire a calibration precondition) —
**none of them adds scope; several would add a term to an existing predicate at ~zero cost.** On the
over-build axis specifically, the corpus is sound as-is, and the discipline is structural, not
accidental (see "why the depth stayed disciplined").

---

## The single sharpest objection

It is a purist's duty to find the *one* place depth bought something the principle didn't ask for, so
here it is, stated at full strength — and then why it does not move the verdict.

**C29's full CSS-cascade stylesheet (the `[[model_rule]]` grammar + specificity ranking + 6 E-codes +
10 AC-codes) is the closest the corpus comes to re-growing a SURVIVOR-PASS drop.** The SURVIVOR-PASS
kept exactly two C29 deltas — DELTA-01 (`model_family` registry slot, for P2) and DELTA-02-L1 (the
"policy is gradable, L1 default" slot, for P5/D-1) — and explicitly DROPPED **DELTA-04 "compiled
deterministic routing function"** as "over-engineered for model selection; we use config-based
routing." A reader could argue that a *cascade engine with selector-specificity tie-breaking* is
precisely DELTA-04 wearing a CSS hat: at Phase-0 the entire registry is **one** adapter
(`claude-code@max`) and the worked example (§5.3) routes coder→floor, judge→economy, catch-all→floor —
a result a three-line `if role == "coder"` would produce identically. The cascade machinery earns its
keep only at FE-1 (a second family), which is deferred. So *is the cascade itself the dropped
routing-function, smuggled back as "implementation-readiness"?*

**Why it does not move the verdict (and the bar's own logic answers it):** the stylesheet *concept* —
a "CSS-like, cost-aware model stylesheet" — is **v4-named** (Fabro, AI-CONTEXT §6.2 line 262;
README:191 "configuration on the Gas City model stylesheet"), and the concrete grammar was an *open
question v4 explicitly posed* (AI-CONTEXT §12 line 514 "specific Gas City model stylesheet syntax for
judge != coder"). Resolving a named OQ to a concrete TOML schema is the *assigned* Sweep-2 deliverable,
not scope creep. Crucially, C29 stops exactly where the bar says stop: it kept the dropped items
**dropped** — `crossFamilyRule` is the *advisory FE-1 seam, not a Phase-0 fail-closed gate* (I2 relaxed
per D-1; E-C29-04 "at Phase-0 this code path is unreachable"); cost-tier is a *preference label, not a
live budget-aware optimizer* (DELTA-05 still dropped, §7 defers the cost model to C46); there is no
fail-closed `degraded_eval` (DELTA-06 still dropped). DELTA-04's actual content — a *compiled*
routing function as an optimization — is absent; what is present is a *declarative config grammar*,
which is the form the SURVIVOR-PASS kept ("we use config-based routing"). The cascade is the
*minimum* way to give a config file deterministic resolution semantics (I3, lintable/auditable), and
determinism here is P4-tied. So the sharpest objection lands as **"down-scopeable in principle but
correctly bounded in practice"**: I would not block on it, but it is the one spec where a future sweep
should resist any urge to add selector dimensions beyond `role`/`stage`/`cost_tier` until FE-1
actually arrives. Flagging, not dropping.

---

## Top-3 over-build flags

**None found that survive the bar.** Per the brief's instruction, here is *why the depth stayed
disciplined* — the structural reasons over-build did not creep in, with the receipts:

1. **Every custom spec self-polices with an explicit DROP ledger that cites the SURVIVOR-PASS verbatim.**
   This is the single biggest reason. C53 §6 "The bar — what got DROPPED" refuses a second scorer, the
   general transfusion predicate (C51's), the recursion loop (C52's), a recurring promotion gate
   (C50/C39's), and inventing the cutline value. C51 §1/§6/§7 refuses a new judge ("Building a second
   judge would be the over-build the bar forbids"), a license/SBOM scanner, and a transfusion executor.
   C33 §6 refuses a custom stats engine (scipy is C48's), a built-in verdict, trend modelling (C46's).
   C31 §6 enumerates seven drops (custom runner/scheduler/eval-loop, parallel-fan-out engine, retry
   policy, holdout-audit, scoring, scenario store, CXDB delivery). C52 §7 refuses a second build engine
   and second judge. These are not decorative — they are the bar applied at the component grain, and
   they hold.

2. **The two reinvention temptations are met by wrap/type, not re-implement — and the specs prove it
   with a code-review AC.** *Inspect AI:* C30 adopts the Task DSL verbatim ("Authoring no DSL of our
   own"); C31's only custom code is the `[[service]]`/`[[tool]]` wrap + the **session-id adapter (G25)**
   — and G25 is a genuine KEEP (the OSS stack does not reconcile Inspect-AI vs Gas-City session identity;
   "impedance unknown" is v4's own words; P5/P6/P10/P11 trajectory-threading cannot be met without it).
   C31 even ships **AC-C31-13**: "*code review confirms C31 contains no custom runner/scheduler/eval-loop,
   no parallel-run engine, no retry policy, no scoring …*" — a test *for the absence of over-build*.
   C33's reduction is "Inspect AI score reduction + a thin distribution-summary helper," with AC-C33-08
   asserting no bespoke estimator. *OS isolation:* C43 §1 `[FAITHFUL-FILL]` lists the **four** dropped
   mechanisms (C02-04 capability-grant layer, C04-05 isolation-at-spawn, C41-07 boundary_class tag,
   C42-06 OPA) and keeps only the *deterministic typing + scissors routing declaration* — "C43 types
   and routes; it does not re-build OS sandboxing." C34 §1 `[FAITHFUL-FILL]` drops OPA, the MAC kernel,
   and the tool-call-time interceptor, keeping only the v4-sanctioned "policy + perms + audit ('custom,
   your work, small')." The genuinely custom pieces are minimal *because the stack provides the rest*.

3. **The depth pass actively *prevented* two scope pull-ins via ledger decisions, rather than passively
   avoiding them.** D-35 routes C09's render-context variables to the C05 `DispatchRequest` *expressly
   so C13 is not pulled into the spine* ("C13 is NOT pulled into the spine … avoids scope creep").
   D-36 keeps the eval-tier trajectory flow on the Inspect AI log and C33's write on C19 beads *expressly
   so C24/CXDB stay non-spine*. And C08/C09 — the SURVIVOR-PASS's most-scrutinized DROP (C08-01/02
   standalone-bundle, C09-01 `spec_id` binding) — **held the line at depth**: C08 keeps Reading A (the
   collapse), states "no `spec_id` indirection on the canonical track (that indirection is DELTA-01,
   deferred)," and C09 §3.1a confirms "C09 does NOT receive a separate `spec_id`." The dropped bundle
   machinery did not regrow under depth pressure. (Honourable mention as a *near*-flag: C33's
   `excluded_count` field + E-C33-04 boundary-saturation informational event — but both are bead fields
   / logged events, not machinery, and `excluded_count` is the minimal honest way to not let one
   malformed bead poison the distribution. Not a drop.)

---

## Is keeping C13 / C24 (and C44 / C54) OUT of the spine correct?

**C13 — correct to stay OUT.** C13 (molecule runtime state) is a *native Gas City* lifecycle FSM; the
SURVIVOR-PASS dropped all seven C13 deltas as hardening over what Gas City already provides. The only
Sweep-2 risk was a backdoor pull-in via C09's render context — and D-35 closed it deliberately by
sourcing `BeadId`/`CreatedBy` from the C05 `DispatchRequest`. Note C52 *dispatches into* "the existing
convergence flow (C12/C13/C28)" — but that is *using the adopted substrate*, not pulling C13 in as
custom spine work. No spine component grew a dependency that requires C13 to be *built*. Correct.

**C24 — correct to stay OUT.** C24 (telemetry→CXDB bridge) was the live decision-fork. D-36 settles it:
the spine eval tier reads the **Inspect AI log**, not CXDB; C31 explicitly performs *no* CXDB
interaction (AC-C31-13), C33 writes satisfaction to **C19 beads** (D-36), and C53/C51 read C33's beads.
The whole CXDB-reading back-half (self-heal C36–C39 / replay C49 / self-opt) is correctly deferred, so
nothing in the 25-component spine needs the bridge. The SURVIVOR-PASS *did* keep four C24 deltas
KEEP-MINIMAL — but as the **shape of C24 when it is eventually built**, not as a spine obligation; the
backbone doc lists C24 as its own non-backbone internal product. Pulling it in now would be exactly the
over-build the bar rejects. Correct.

**C44 — correct to stay OUT (with the standing honest caveat).** C43 enters via its boundary-typing
half (needs only C42); the twin-isolation half (C44) is Phase-3c per D-20. This is the operator-adopted
split, not a purist call, and the corpus is scrupulously honest that until C44 lands the blast-radius
bound is "aspirational" / detect-only (C34 §4.3, XC-8) — which is the *Hawk's* and *Substrate Realist's*
territory (a safety/honesty caveat), **not** an over-build. From the bar's angle, building C44's bespoke
per-service twins now — before the factory can build itself — would be premature scope. Correct to defer.

**C54 — IN the spine, and correctly so (minor brief imprecision).** The brief pairs "C44/C54" as
out-candidates, but C54 (phase plan) is a **backbone governance product** (implementation-dependencies
§backbone, gated on C52 + C43). C51:OQ-C51-2 and C52:OQ5 route the G14 *class-level* transfusion-failure
fallback to C54 — that is a dependency *within* the spine being correctly homed, not a pull-in of an
excluded component. No action; noting so the panel record is precise.

---

## Change-before-building

**None required on the over-build axis** — the verdict is `sound-as-is`. Two *watch-items* (neither a
gate, neither blocking; recorded so a later sweep does not let depth drift into scope):

1. **C29 cascade — hold the selector surface flat until FE-1.** The `[[model_rule]]` grammar is correctly
   bounded today (`role`/`stage`/`cost_tier` only; advisory cross-family; no cost optimizer). Resist any
   future urge to add selector dimensions, a compiled/optimized resolver (the dropped DELTA-04), or a
   live cost-budget input (the dropped DELTA-05) before a *second model family actually exists*. At
   Phase-0 with one adapter, the cascade must not acquire weight the single-floor reality cannot justify.

2. **Treat the prior panel's "add a term" fixes as zero-scope, and do not let them metastasize into
   engines.** The Self-Mod Skeptic's std_dev spread-ceiling (F1) and judge-calibration precondition
   (F2/PF-2) are *additions to an existing predicate / an existing C46 measurement* — `std_dev` is
   already in `GoNoGoInput`; C46 already owns judge-FP-rate. Implemented as a third conjunction term and
   a precondition edge, they cost ~nothing and stay on-bar. The only way they *become* over-build is if a
   builder reifies "judge calibration" into a new C53-owned scorer instead of wiring the existing C46
   signal. Keep them as terms/edges, not engines.

---

## Bottom line

On the capability-bar axis the Sweep-2 depth is the strongest part of the corpus: implementation-
readiness was achieved by **concretizing v4-named OQs into schemas/signatures/ACs** and by **wrapping
and typing the existing stack**, with every custom spec carrying a verbatim-cited DROP ledger and, in
C31's case, an acceptance test *for the absence of over-build*. The dropped hardening did not return;
the two reinvention temptations (Inspect AI, OS isolation) were resisted structurally; and the two
scope pull-ins that could have crept in (C13 via C09, C24 via the eval tier) were *actively foreclosed*
by ledger decisions D-35/D-36. C13 and C24 are correctly out; C44 is correctly deferred; C54 is
correctly in. The single sharpest objection (C29's cascade) is down-scopeable in principle but
correctly bounded in practice. **Verdict: `sound-as-is`.** When in doubt, the bar says DROP — and on
this axis, this corpus already did.

---

*Authored 2026-06-01 by the Capability-Bar Purist, Sweep-2 depth panel. Grounded against SURVIVOR-PASS
(per-component DROP/KEEP ledger), HANDOFF §2, review-log D-35/D-36/D-39, implementation-dependencies
§backbone, and the purpose/boundary/the-bar sections of C08/C09/C29/C30/C31/C33/C34/C43/C51/C52/C53.*
