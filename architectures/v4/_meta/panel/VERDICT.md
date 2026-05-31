# Panel verdict — Software Factory v4 (reconciled)

> **What this is:** the lead reconciler's synthesis of five independent expert
> [panel opinions](.) on the v4 architecture. It distinguishes two layers: the **PANEL-OPINION layer**
> (§2, what the panelists said — each cited to its file/persona) and the **SYNTHESIS layer**
> (§3–§7, the reconciler's reconciliation, grounded in citations but not itself a sixth opinion).
> **Inputs:** [01-operability](01-operability.md), [02-security](02-security.md),
> [03-pragmatist](03-pragmatist.md), [04-buildability](04-buildability.md),
> [05-methodology](05-methodology.md), the six adopted operator decisions in
> [`decisions-to-make.md`](../../../../decisions-to-make.md) (D-20..D-25), and the decision
> ledger ([`review-log.md`](../review-log.md)).
>
> **Decision-id mapping** (from [`decisions-to-make.md`](../../../../decisions-to-make.md), items 1–6 → adopted D-20..D-25):
> D-20 = fence (C43 boundary-typing) pulled to a P2 precondition · D-21 = objective-drift (F54) logged-unbuilt + human checkpoint ·
> D-22 = counterfactual replay (C49) ship-deterministic-half / keep LLM-half experimental · D-23 = Gas City prevent-vs-detect reality check (G11) ·
> D-24 = C46 meta-metrics dependency-edge wiring correction · D-25 = secrets deferred to first-credential + Unleash license version-pin.

---

## TL;DR

*(structure-not-conclusions: each line names a structural element, not a verdict that would need rewriting if the conclusion changed)*

- **Reconciled verdict tier:** all five panelists independently returned `right-idea-but-change-X-before-building`; this verdict adopts that tier.
- **Load-bearing convergence:** the unverified-substrate question (G11 / D-23 — does `gc` *prevent* or merely *detect* out-of-partition tool calls) is named by 5/5 panelists as the single highest-leverage unknown.
- **Sound-thesis line:** the substrate-first inversion (build runtime once, run methodology as config) and the C57 honest residual register are named as strengths by ≥4 panelists.
- **Top cross-cutting risk cluster:** G11 substrate verification (5/5), the same-family judge C32/C33 eval signal + F54/C55 Goodhart drift (3/5), and the P2→P3b unattended-self-modification exposure window (4/5).
- **Decision-coverage line:** D-20, D-21, D-23, D-25 each *partially* address a named risk; the security and methodology panels argue D-23 must be re-framed from "noted caveat" to a **go/no-go gate** on D-20.
- **New-recommendation count line:** §6 lists the changes that go *beyond* the adopted D-20..D-25 (judge-independence tier, shadow evaluator, work-type taxonomy, integration-seam owner, transfusion completeness anchor, Unleash version-pin timing).

---

## 2. Panel positions at a glance

> **PANEL-OPINION layer.** Each row is what that panelist said in their own file — not the reconciler's view.

| Panelist (persona) | File | Verdict tier | Single top risk | Top recommended change |
|---|---|---|---|---|
| Distributed-systems / operability skeptic | [01-operability.md](01-operability.md) | `right-idea-but-change-X-before-building` | G11 — entire corpus rests on an unverified Gas City substrate; every "Native" claim across 57 components is an unexercised assertion | Run the Gas City conformance pack (C01 AC-2) as the **first** sweep-2 action, before any other work |
| Security reviewer | [02-security.md](02-security.md) | `right-idea-but-change-X-before-building` | The C43 fence is a *declaration, not a control,* until G11/D-23 is resolved; same gap undermines C34 holdout integrity | Make D-23's prevent-vs-detect spike a **go/no-go gate** on D-20's "fence pulled to P2" precondition, not a noted caveat |
| AI-agent pragmatist (Willison-style) | [03-pragmatist.md](03-pragmatist.md) | `right-idea-but-change-X-before-building` | The C32/C33 satisfaction signal is a same-family "hall of mirrors" (judge shares the coder's training distribution); F48 only `Partial`, cross-family deferred to FE-1 | Add a `judge_independence_tier` field to C33 now; block C48/C50/C55 auto-promotion on same-family scores |
| Buildability engineer | [04-buildability.md](04-buildability.md) | `right-idea-but-change-X-before-building` | The integration tax between individually-sound OSS choices (C25→C26→C27, C44 three-layer twins, C49→C44→C43) is uncosted and unowned | Run the Gas City reality-check spike before binding any "native" claim; pin the Unleash version *now*, not in sweep-2 |
| Methodology critic | [05-methodology.md](05-methodology.md) | `right-idea-but-change-X-before-building` | Structural Goodhart: C33 is both the optimization target (C47/C50) *and* the selection signal (C55/C56); F54 drift audit is UNBUILT | Build a structurally-independent **shadow evaluator** C47 cannot see, *before* C47/C50 are built |

---

## 3. Where the panel agrees v4 is sound

> **SYNTHESIS layer.** Cross-cutting strengths named by ≥2 panelists, with citations.

1. **The substrate-first / principle-first inversion is the correct architectural thesis (5/5).** Building the runtime once and treating methodology as a swappable config is named as sound by [operability §1/§6](01-operability.md), [pragmatist §2](03-pragmatist.md), [buildability §1](04-buildability.md), and is the "strongest intellectual move in the corpus" per [methodology §2](05-methodology.md). [Security §1](02-security.md) endorses the security-goal framing built on it.

2. **The C57 honest residual register is a genuine, rare contribution (5/5).** Every panelist singles out the "no bare Addressed" invariant — that each unbuilt mechanism carries its exposure-window caveat — as architecturally valuable: [operability §2](01-operability.md), [security §2](02-security.md), [pragmatist §2](03-pragmatist.md), [buildability](04-buildability.md) (G19 partition), [methodology §2](05-methodology.md).

3. **Attribution is substrate-native and the strongest single property (3/5).** Gas City's automatic `created_by` on every bead/event (C41/C01 INV-3) is called out by [operability §2](01-operability.md), [security §2](02-security.md) ("strongest single security property"), and [buildability §2](04-buildability.md) ("strongest native fit … zero integration risk").

4. **OSS-first discipline ("the bar") genuinely holds at the component level (2/5+).** [Buildability §2](04-buildability.md) verifies custom code is scoped to wiring/contracts in C27/C44/C48; [pragmatist §2](03-pragmatist.md) confirms the low-hype discipline of configuring PyOD/HDBSCAN/Inspect AI rather than inventing.

5. **C49's honest deterministic/LLM partition and C51's per-component falsifiability are the right engineering posture (3/5).** The split of a tractable deterministic-replay slice from a deferred LLM slice is endorsed by [pragmatist §2](03-pragmatist.md), [buildability §2](04-buildability.md); C51's transfusion predicate as per-component falsifiability is praised by [pragmatist §2](03-pragmatist.md) and [buildability §2](04-buildability.md).

6. **Phase sequencing (Phases 0–2 before factory-builds-factory) is sound risk management (2/5).** [Buildability §2](04-buildability.md) and [pragmatist §2](03-pragmatist.md) both credit gating Phase 3+ on bootstrap validation; [security §2](02-security.md) credits D-20's fence-before-unattended sequencing specifically.

---

## 4. Where the panel agrees v4 is risky

> **SYNTHESIS layer.** Cross-cutting risks named by ≥2 panelists, ranked by panelist-count × severity. Each notes whether an adopted D-20..D-25 fully / partially / does-not address it.

**R1 — G11 / D-23: the entire substrate is unverified; prevent-vs-detect is unknown (5/5, CRITICAL).**
Every "Native" claim — C43 fence enforcement, C34 holdout, C42 partitioning, C40 Orders durability, session resume — is an untested assertion against a third-party binary nobody has run ([operability §3 R1](01-operability.md), [security §3](02-security.md), [pragmatist §3](03-pragmatist.md), [buildability §3](04-buildability.md), [methodology §4](05-methodology.md)). The pivotal sub-question: does `gc` *refuse* an out-of-partition tool call at dispatch time, or permit-and-log?
**Decision coverage: PARTIAL.** D-23 names this as the first reality-check spike — but [security §4](02-security.md) and [methodology §4](05-methodology.md) argue D-23 must become a **binding go/no-go gate** on D-20, not a research item to note. As adopted, the *trigger consequence* of a detect-only outcome is undecided. (See §6, new.)

**R2 — P2→P3b unattended-self-modification exposure window (4/5, CRITICAL/HIGH).**
The factory runs unattended at scale (P2) and self-modifies (P3b) *before* C43/C44 twin isolation lands (P3c). A declaration-only fence offers no in-the-moment resistance to a prompt injection during that window ([operability §3 R4](01-operability.md), [security §3](02-security.md), [pragmatist §3](03-pragmatist.md), [methodology §4](05-methodology.md) on the drift face).
**Decision coverage: PARTIAL.** D-20 pulls the C43 boundary-typing half forward to a P2 precondition — the right call (all four endorse) — but it only closes the window *if the fence actually prevents* (depends on R1/D-23). Until D-23 resolves prevent, D-20 closes a documented window, not necessarily a real one.

**R3 — Same-family eval signal + structural Goodhart drift (C32/C33 → C47/C50/C55; F54) (3/5, CRITICAL).**
The satisfaction metric C33 is scored by a judge in the coder's own provider/family ([pragmatist §3](03-pragmatist.md): "hall of mirrors"; [security §3](02-security.md): single-layer detect-only holdout) **and** is simultaneously the target the self-optimization loop optimizes and the signal methodology selection (C55) and ladder-climbing (C56) read ([methodology §3](05-methodology.md): canonical Goodhart). F48 is `Partial`; cross-family strengthening is deferred to FE-1 with no trigger date.
**Decision coverage: PARTIAL / mostly OPEN.** D-21 logs F54 unbuilt + a human checkpoint, but [security §3](02-security.md) and [methodology §3/§6](05-methodology.md) both argue a human at a batched review *cannot* detect C33-drift-from-intent by reading output alone — D-21 is a process intention, not a control on this risk. The judge-independence and shadow-evaluator fixes (§6, new) are not covered by any adopted decision.

**R4 — Integration tax between sound OSS components is uncosted and unowned (2/5, HIGH).**
The seams — C25→C26→C27 OTLP signal-split (C27 OQ-1 open), C44's three-OSS-layer twin assembly, C49→C44→C43 replay chain, the two-sink C24/CXDB vs LangFuse join with no designed correlation path — are where build cost actually lives ([buildability §3](04-buildability.md), [operability §3 R3](01-operability.md)).
**Decision coverage: OPEN.** No D-20..D-25 assigns an integration owner or budget. (See §6, new.)

**R5 — Orders durability ceiling opaque; Temporal trigger unmeasured (C40) (2/5, HIGH).**
Crash-resume granularity and the concrete threshold that makes Orders "insufficient" (C40 OQ-1/OQ-3) are unknown; the P11 self-healing loop is specced against an unknown durability floor ([operability §3 R5](01-operability.md), [buildability §3](04-buildability.md) on substrate-behavior assumptions).
**Decision coverage: PARTIAL.** Folds into the D-23 / G11 reality check if Orders conformance is run alongside the substrate gate; not separately decided.

**R6 — Factory-builds-factory bet front-loads the hardest unsolved problem; C51 completeness anchor (OQ-C51-1) unsolved (2/5, MEDIUM/HIGH).**
Phase 2 validates on a "small new component"; generalizing to the Healer / counterfactual-replay / twin-scaffolding tier is a large inductive leap ([pragmatist §3](03-pragmatist.md)), and the transfusion predicate's *completeness* clause (how to enumerate an exemplar's named behaviors) is load-bearing and open ([buildability §3](04-buildability.md)).
**Decision coverage: OPEN.** Not addressed by D-20..D-25. (See §6, new.)

**R7 — G37 plaintext secrets + Unleash license/version ambiguity (1–2/5, MEDIUM).**
[Security §3](02-security.md) flags plaintext-secrets debt compounding precisely when production scissors first reach real systems; [buildability §3](04-buildability.md) flags an irreconcilable Unleash license contradiction (README MIT vs Apache-2.0 vs commercial) with no pinned version.
**Decision coverage: PARTIAL.** D-25 defers secrets to first-credential and pins a clearly-open license — but [buildability §4](04-buildability.md) argues the version-pin must happen *before* C48 implementation, not in sweep-2 as currently scheduled.

---

## 5. Dissents and minority views

> **SYNTHESIS layer.** Genuine divergences, named — not flattened toward consensus.

- **Methodology critic dissents on the depth of the Goodhart problem ([05-methodology.md §3](05-methodology.md)).** Where the pragmatist frames the same-family judge as an *eval-credibility* problem fixable with a tier flag, the methodology critic argues it is a *structural* flaw: because C33 is simultaneously target and selector, even a fixed independence tier doesn't help once C47 optimizes against it — only a structurally-independent shadow evaluator does. This is a stronger claim than any other panelist makes; do not collapse it into R3's "add a field."

- **Methodology critic alone challenges the load-bearing "methodology = config file" thesis ([05-methodology.md §3, HIGH](05-methodology.md)).** The other four accept the substrate/methodology decoupling as sound (it appears in §3 as a strength). The methodology critic argues it is *false for the full evaluation surface* (prompt templates, rig configs, tool-node availability, work-type taxonomy G05 all encode methodology). This is a genuine minority counter to a consensus strength.

- **Buildability engineer is the sole voice on license hygiene as a *blocking* item ([04-buildability.md §3/§4](04-buildability.md)).** Others either omit it or (D-25) route it to sweep-2; buildability insists the Unleash version-pin is a pre-implementation gate, framing it as "a concrete contradiction, not housekeeping." A real disagreement about urgency, not substance.

- **Operability is the only panelist to foreground the two-sink observability seam and the throughput/cost ceiling ([01-operability.md §3 R2/R3](01-operability.md)).** No other panelist models the single-$200/mo-Max-seat throughput ceiling (G32/G34) or the CXDB↔LangFuse no-join problem. Not contradicted by anyone — but a minority emphasis worth preserving because it is the only operational-capacity lens on the panel.

- **No panelist dissents from the verdict tier.** All five returned `right-idea-but-change-X-before-building`; there is no "reject" or "accept-as-is" minority. The consensus is on the tier; the disagreement is on *which* X is most load-bearing.

---

## 6. Changes worth making before implementation

> **SYNTHESIS layer.** Ranked. Each is tagged **[covered by D-NN]** (the adopted decision already addresses it) or **[NEW]** (raised by the panel, not yet decided).

1. **Run the Gas City reality-check spike (prevent-vs-detect, Orders durability, `[[service]]` semantics) as the literal first sweep-2 action — and make a detect-only outcome a binding trigger, not a caveat.** **[covered by D-23 for the spike; NEW for the gating consequence]** All 5 name the spike; [security §4](02-security.md) and [methodology §6](05-methodology.md) add the binding part: if `gc` is detect-not-prevent, D-20's "fence pulled forward" must be re-evaluated and a compensating prevent layer (OPA/seccomp/namespace) added or the autonomy claim descoped. The adopted D-23 does not yet bind this consequence.

2. **Add a structurally-independent shadow evaluator that the self-optimization loop (C47/C50) cannot see, before C47/C50 are built.** **[NEW]** [Methodology §4/§6](05-methodology.md). This is the only proposed control on the structural Goodhart risk (R3); D-21's human checkpoint does not cover it.

3. **Add a `judge_independence_tier` field to C33 and gate C48/C50/C55 auto-promotion on it now.** **[NEW]** [Pragmatist §4](03-pragmatist.md). Cheap (one struct field + one policy); converts the same-family hall-of-mirrors from a silent failure into an explicit limit until FE-1.

4. **Specify the D-21 human-checkpoint cadence as a hard ceiling tied to P3b entry, with a named artifact the reviewer inspects.** **[partially covered by D-21; NEW for the cadence + artifact]** [Security §4](02-security.md), [methodology §6](05-methodology.md). "Periodic"/"batched" are not controls; define the max interval and the specific diff (self-modified prompt vs signed original) before the first P3b self-modification.

5. **Pin the Unleash version (or swap to GrowthBook) before C48 implementation, not in sweep-2.** **[partially covered by D-25; NEW for the timing]** [Buildability §4](04-buildability.md). Trivial cost; prevents a late commercial-tier surprise rewriting C48's routing layer.

6. **Assign an integration owner + budget for the C25→C26→C27 OTLP pipeline and the C44 twin assembly.** **[NEW]** [Buildability §4](04-buildability.md), [operability §3 R3](01-operability.md). These seams are where most Phase 1–2 time goes and no spec owns them end-to-end.

7. **Resolve the C51 completeness anchor (OQ-C51-1) and pin the work-type taxonomy (G05 / C55 OQ-2) before Phase 3 / the first methodology experiment.** **[NEW]** [Buildability §4](04-buildability.md), [methodology §6](05-methodology.md). Determines whether the transfusion predicate and methodology selection are real acceptance contracts or rubber stamps.

8. **Confirm C34's holdout audit captures OS-level (Bash) reads, not just tool-invocation events, before P2.** **[NEW]** [Security §4](02-security.md). A `cat scenarios/foo.md` may not appear in the bead/OTLP trail; verify the read-trail source before treating C34 as an audit boundary.

**Already covered with no further action needed:** D-22 (ship C49's deterministic half, keep the LLM half experimental) is endorsed by [pragmatist §2](03-pragmatist.md) and [buildability §2](04-buildability.md) with no panel objection. D-24 (C46 wiring correction) is uncontested housekeeping.

**Count of new, not-yet-decided recommendations: 8** (items 1–8 each carry a [NEW] component; items 1, 4, 5 are partially covered by an adopted decision but add an undecided element).

---

## 7. Bottom line

The panel is unanimous on the shape of the answer: v4 is the right idea — the substrate-first inversion, the spec-as-source-of-truth spine, the honest C57 residual register, and the OSS-first "bar" are all sound and, in places, unusually disciplined — but it must change one class of thing before building. The single load-bearing fact the entire architecture pivots on is whether Gas City *prevents* an out-of-partition tool call at dispatch time or merely *detects* it after the fact (G11 / D-23); five of five panelists name this as the highest-leverage unknown, and both the security and methodology reviewers argue the adopted decision is too weak — it treats a detect-only outcome as a noted caveat when it should be a binding go/no-go gate on running the factory unattended (D-20). Two further structural risks are under-covered by the adopted decisions: the same-family judge that makes the C32/C33 satisfaction signal a "hall of mirrors," and the fact that that same signal is simultaneously the optimization target and the methodology-selection signal — a textbook Goodhart trap that arms the moment C47 starts optimizing, before L5 is ever authorized. The adopted D-20..D-25 are the right *direction* on every risk they touch, but several only close their window conditionally (D-20 depends on D-23 resolving "prevent") or as process intentions rather than controls (D-21). The recommended path: run the Gas City reality-check spike first, bind its consequence, and add the cheap independence/shadow-evaluator instrumentation before the self-optimization loop is built — eight concrete changes beyond what is already decided, none of them expensive relative to the risk they close.
