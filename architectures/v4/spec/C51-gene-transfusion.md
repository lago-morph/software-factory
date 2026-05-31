# C51 — Gene-transfusion discipline (`gene-transfusion`)  (Spec, canonical track)

> Source: AI-CONTEXT §9 ("Gene transfusion technique" — definition by analogy from v3 vocabulary: "applying a working pattern from one codebase to another by pointing the agent at a concrete exemplar and asking it to reproduce the behavior"; §9.1 transfusion-source map per layer; §9.2 "Discipline patterns" — `transfused_from: <url>`, "License hygiene: track transfusion source license per component", "Permissively-licensed transfusions can be donated back upstream; restrictively-licensed ones stay private"); AI-CONTEXT §16 cold-start step 2 ("Check `transfused_from` attribution"); README Part 7 "Discipline that keeps the bootstrap honest" (lines 496–500: "Gene transfusion always … No invention from scratch … evaluation grounded ('does this behave like the exemplar?')"; line 497 "Attribution of transfusion sources … records its `transfused_from: <url>` … P9 applied to the factory's own work"; line 499 "Scenarios drive evaluation … ensure its clusters match"; line 500 "External grounding for substrate"); README Part 8 bet #4 (line 511: "Gene transfusion is reliable for bounded components"); README Part 5 license census (lines 285–306 — per-source SPDX + "Verify before adopting" gating); component-inventory C51 row (maps `A86, A93, A107, A180-189, B52, B55`; depends on C08, C20; gaps G07, G14, G30; foundational: yes; critical-path note #4 — "without a correctness predicate the whole factory-builds-factory plan (C52–C54) has no acceptance contract"); ambiguities-and-gaps G07 (major — transfusion has "no acceptance criterion for *when a transfusion is correct/complete*, no contract for what 'behaves like the exemplar' means operationally, and no handling for exemplars under incompatible licenses"), G14 (major — reliability is "a bet"; Phases 3b/3c/3d all gated on it; "no fallback for 'factory cannot reliably transfuse'"), G30 (minor — Tracker license unverified; "the boundary between 'transfuse the code' and 'reimplement the pattern' is left to chance").
> Inventory ID: C51   Kind: cross-cutting   Status: sweep-1
> Track: canonical

## 1. Purpose & responsibility

C51 is the **gene-transfusion discipline**: the cross-cutting contract that every component the
**factory builds for itself** (Phase 3+) is grounded in at least one concrete external exemplar rather
than invented from scratch, records *which* exemplar(s) at the component grain (`transfused_from`),
proves it actually **behaves like** that exemplar before it can ship (the correctness/completeness
**predicate**), and stays inside the exemplar's **license** terms. v4 names this technique as the thing
"that makes the factory-builds-factory plan tractable" (AI-CONTEXT §9) and lists it first among the four
disciplines that "keep the bootstrap honest" (README:496) — but defines it only **by analogy**, with no
operational success contract (G07), no fallback if the bet fails (G14), and no rule for incompatibly
licensed exemplars (G30). C51 is the component that turns the analogy into an **acceptance contract**.

C51 is **foundational** and load-bearing for bootstrap: the inventory's critical-path note #4 states that
"without a correctness predicate the whole factory-builds-factory plan (C52–C54) has no acceptance
contract." C52 (self-bootstrap), C53 (validation milestone), and C54 (phase plan) all consume the
predicate C51 defines. The genuine custom engineering here is **the predicate** (the "bet" made
falsifiable), `transfused_from` at the component grain, and license hygiene — not new evaluation
machinery (that already exists in C30–C33).

**Responsibilities**
- Define the **transfusion record** — the component-grain metadata asserting `transfused_from: <url>`
  (≥1 exemplar) plus the per-source license fact, attached to the factory-built component's
  `factory_build` bead (AI-CONTEXT §9.2; §16 step 2; C20 owns the field schema). *(B52, A93.)*
- Define the **≥1-exemplar invariant**: a factory-built component with **zero** declared exemplars is
  out of discipline — "No invention from scratch" (README:496; B55). *(B55.)*
- Define the **transfusion-correctness / completeness predicate** (G07): the operational meaning of
  "does this behave like the exemplar?" — expressed as **exemplar-grounded scenarios** scored by the
  existing judge tier against the component's Definition-of-Done, with a **completeness** clause that the
  exemplar's *named* behaviors are each covered by ≥1 scenario. This is C51's load-bearing deliverable.
- Define the **transfusion-mode boundary** (G30): per exemplar, whether the build may **transfuse the
  code** (verified-permissive license) or must **reimplement the pattern** (unverified/restrictive
  license) — and the **donate-back-vs-stay-private** disposition that follows (AI-CONTEXT:430).
- Define the **bet-failure fallback** at the discipline layer (G14): what a build does when the predicate
  **cannot be met** for a given component — the "factory cannot reliably transfuse *this*" exit — so the
  bet is falsifiable per-component instead of being an all-or-nothing wager.

**Explicitly NOT**
- **NOT a new evaluation engine.** The predicate is *expressed in terms of* the existing scenario store
  (C30), scenario runner (C31), judge harness (C32), and satisfaction aggregator (C33). C51 supplies the
  **acceptance contract** ("exemplar behavior → scenario → satisfaction ≥ bar"); it does not re-implement
  scoring. Building a second judge would be the over-build the bar forbids.
- **NOT the bead field schema.** `transfused_from`, the license fact, and the predicate-verdict slot are
  **fields on the `factory_build` bead, owned by C20** (D-3: C20 authors bead payload schemas). C51
  defines *what the values mean and when they are valid*; C20 defines the on-disk shape. C51 ≠ C20.
- **NOT the self-bootstrap loop.** C52 runs the recursion (author spec → build → human review → deploy)
  and *calls* C51's predicate as its acceptance gate; C53 is the go/no-go milestone that *consumes* a
  passing predicate. C51 is the **gate's contract**, not the loop or the milestone.
- **NOT the spec/DoD itself.** The component's Definition-of-Done lives in C08 (free-form, per D-15). C51
  adds the **exemplar-grounding** dimension on top of C08's DoD; it does not redefine the spec format.
- **NOT a license scanner / SPDX engine.** v4 already carries a hand-maintained license census
  (README:285–306) with explicit "Verify before adopting" gates. C51 makes that census a **build-blocking
  fact**, not an automated SBOM tool (that would exceed Phase-0 scope; flagged §9).
- **NOT a transfusion *executor*.** "Pointing the agent at the exemplar and asking it to reproduce the
  behavior" is the agent loop (C28) doing the work under a prompt (C09). C51 governs the **discipline
  around** that act (declare source, prove behavior, respect license), not the act of porting code.
- **NOT applicable to substrate.** The "External grounding" discipline (README:500, A107) keeps
  foundations (CXDB, Temporal, scikit-learn) as upstream OSS — those are **adopted, not transfused**, and
  carry no `transfused_from`. C51 governs only **factory-built** components (the orchestration glue).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C08** Spec artifact & format | The transfusion-correctness predicate is graded against the component's Definition-of-Done, which C08 owns (free-form DoD; D-15 holistic satisfaction). Inventory: C51 `depends on C08`. |
| Upstream (depends on) | **C20** Bead schema registry | `transfused_from`, per-source license fact, and the predicate-verdict slot are fields on the `factory_build` bead (C20 §4.2; D-3). Inventory: C51 `depends on C20`. C20 §2 lists C51 as a downstream consumer of `transfused_from`. |
| Upstream (concept) | **C30–C33** Scenario store / runner / judge / satisfaction | The predicate is *defined in terms of* exemplar-grounded scenarios (C30) run (C31), judged (C32), and aggregated into a satisfaction distribution (C33). C51 reuses this tier; it does not own it. |
| Sibling (concept) | **C29** Model floor & stylesheet | The transfusion *act* runs on the Claude Code floor (C28/C29). C51 governs discipline, not the model. |
| Downstream (consumes) | **C52** Self-bootstrap recursion | Calls C51's predicate as the acceptance gate before human design review / deploy (README:498). Inventory: C52 `depends on C51`. |
| Downstream (consumes) | **C53** Bootstrap-validation milestone | The go/no-go gate (G23) consumes a *passing* C51 predicate as the objective half of "if it works." Inventory: C53 `depends on C52` (→ C51 transitively). |
| Downstream (consumes) | **C54** Phase delivery plan | Phases 3a–3d each build factory components under C51 discipline (README:457–470). |
| Downstream (consumes) | **C57** Failure-mode coverage & residual-risk register | C57 "owns license hygiene + the honest residual/caution register" (inventory); C51 supplies the per-component license disposition C57 aggregates. Inventory: C57 `depends on C51`. |

C51 is **Batch-4** (inventory: "factory builds factory") but is **foundational** because every
Batch-4/Batch-5 factory-built component (C36–C39 Healer tier, C44–C45 twins, C46–C50 self-opt) is
acceptance-gated by C51's predicate. Per critical-path note #4 it gates C52–C54.

## 3. Interfaces / contracts

Sweep 1 — interfaces named and described (concrete signatures / scenario schemas deferred to sweep 2).

1. **Transfusion record (inbound declaration).** What a factory-build *declares*: one or more
   `transfused_from` exemplar URLs and, per exemplar, the license fact + chosen transfusion **mode**
   (code-port | pattern-reimplement). Recorded at the **component grain** on the `factory_build` bead
   (C20). The contract C52 writes and C57 reads.
2. **≥1-exemplar invariant (validation).** The predicate that the declared exemplar set is non-empty —
   "No invention from scratch" (README:496). A build asserting zero exemplars is rejected at the
   discipline gate.
3. **Transfusion-correctness predicate (the acceptance contract — G07).** Given (component, exemplar
   set), a **decision** {pass | fail | inconclusive} computed as: *the exemplar's named behaviors are each
   covered by ≥1 scenario (completeness), and the component's satisfaction distribution over those
   scenarios meets the bar (correctness)*. Expressed via C30 (scenarios), C31 (run), C32 (judge), C33
   (distribution). C51 owns the **predicate shape and the "exemplar-grounded" requirement**; the numeric
   satisfaction bar is operator/integrator policy routed to C50/C53 (consistent with C33 being
   threshold-free — C33:OQ-1).
4. **License-mode contract (G30).** Given an exemplar URL + its license fact (from the README:285–306
   census), a decision on the permitted **mode**: verified-permissive ⇒ code-port allowed and the result
   *may* be donated back upstream; unverified/restrictive ⇒ **pattern-reimplement only**, result stays
   private (AI-CONTEXT:430). Blocks a build that code-ports from an unverified-license exemplar.
5. **Bet-failure fallback (outbound signal — G14).** When the predicate returns fail/inconclusive for a
   component, C51 emits a **"transfusion-insufficient" outcome** that C52's loop and C53's milestone
   consume — the per-component falsification of bet #4, so the failure routes to human design review
   rather than silently shipping (README:498 keeps review mandatory until P12 is trusted).

**Invariants**
- **Every factory-built component carries ≥1 `transfused_from`** at the component grain (B52, B55,
  README:497). A factory-built component with an empty exemplar set is out of discipline.
- **`transfused_from` is component-level provenance, not per-record** (review-log RC11-01 NOTE): it is
  recorded once per factory-built component on its `factory_build` bead — not stamped on every bead or
  trajectory the build produces. This is "P9 applied to the factory's own work" at the **build** grain.
- **No code-port from an unverified or restrictive license** (G30; README:292,335; AI-CONTEXT:625): such
  an exemplar may only be *pattern-reimplemented*. License mode is fixed **before** the transfusion act,
  not discovered after.
- **The predicate is exemplar-grounded** (G07; README:496): a component's scenarios must trace to the
  declared exemplar's behavior — "does this behave like the exemplar?" — not merely to a generic spec.
  Completeness = every *named* exemplar behavior has ≥1 covering scenario.
- **External-grounding exclusion** (A107; README:500): substrate/foundational dependencies adopted as
  upstream OSS are **not** factory-built and carry no transfusion record; C51 governs only the glue the
  factory writes.

## 4. Data model / state

C51 owns **discipline semantics**, not storage. The three values it gives meaning to live as fields on
the `factory_build` bead (C20 §4.2; D-3) at the **component grain**:

| Value | Meaning | Grain | v4 source / owner |
|---|---|---|---|
| `transfused_from` | ≥1 external exemplar URL the component was grounded in | per factory-built component | README:497; AI-CONTEXT §9.2; field owned by C20 |
| `transfusion_license` | per-exemplar license fact + verified? flag (from README:285–306 census) | per (component, exemplar) | AI-CONTEXT:429 "track transfusion source license per component"; G30 |
| `transfusion_mode` | per-exemplar {code-port \| pattern-reimplement}, derived from license | per (component, exemplar) | AI-CONTEXT:625; G30; **> [FAITHFUL-FILL]** below |
| `transfusion_verdict` | predicate outcome {pass \| fail \| inconclusive} + the scenario set it was computed over | per factory-built component | README:496,499; G07; **> [FAITHFUL-FILL]** below |

> [FAITHFUL-FILL] **`transfusion_mode` and `transfusion_verdict` are inferred field names.** v4 names
> `transfused_from` verbatim (README:497) and names license tracking and the code-vs-pattern boundary in
> prose (AI-CONTEXT:429–430,625; G30) but gives **no field** for the mode decision or the predicate
> outcome. The minimal consistent choice is to record both as component-grain facts alongside
> `transfused_from`, because (a) G30 requires the code/pattern decision to be **made and auditable**
> before the build, and (b) G07 requires the "behaves like the exemplar?" check to have a **recorded
> verdict** that C52's gate and C53's milestone can read. These are C20 schema-slot requests (like
> C20's own G18 slots); concrete field shape is C20's sweep-2 deliverable. No richer provenance model is
> invented — the grain stays **component-level** per RC11-01.

> [FAITHFUL-FILL] **`transfused_from` cardinality = "≥1", set-valued.** README:497 writes the field
> singular (`transfused_from: <url>`) but README:496 / AI-CONTEXT §9.1 routinely name **multiple**
> exemplars per component (e.g. the Diagnosis agent transfuses Tracker's APIs *and* Anthropic
> investigation patterns *and* Sentry/Honeycomb — AI-CONTEXT:407). The minimal faithful reading is a
> **set** with a ≥1 floor, so the multi-exemplar components the corpus actually describes are
> expressible. (A86/B55 say "at least one external exemplar".)

C51 holds **no persistent state of its own**: it is a predicate + invariants over C20-stored values and
C30–C33-produced scenario verdicts. Its only consistency requirement is **grain agreement**: the
transfusion record is written **once per factory-built component** (RC11-01), and the verdict is computed
**over the scenarios attributed to that component's exemplars** — not over the whole trajectory population.

## 5. Behavior

C51 has no control loop of its own; its behavior is **gate-time** and **definitional**, invoked by C52's
bootstrap recursion at two points:

- **Declaration-time (pre-build).** A factory-build declares its exemplar set. C51 checks the
  **≥1-exemplar invariant** (else out of discipline) and resolves each exemplar's **license mode** against
  the census (README:285–306): unverified/restrictive ⇒ pin `transfusion_mode = pattern-reimplement`
  (G30). This fixes the legal envelope *before* the agent (C28) does the porting work.
- **Acceptance-time (post-build, pre-deploy).** C51 evaluates the **correctness/completeness predicate**:
  the component's exemplar-grounded scenarios (C30) are run (C31) and judged (C32) into a satisfaction
  distribution (C33); C51 returns `pass` iff every *named* exemplar behavior is covered (completeness)
  **and** the distribution meets the bar (correctness). The verdict is recorded on the `factory_build`
  bead and handed to C52's design-review gate (README:498) and C53's milestone (G23).
- **On fail/inconclusive (G14 fallback).** C51 emits **transfusion-insufficient**; C52 routes the
  component to human design review rather than auto-deploy. This is the per-component falsification of
  bet #4 — the bet is tested one bounded component at a time, with a defined non-shipping exit, instead of
  being an unguarded global wager.

The transfusion *act* itself (point the agent at the exemplar; reproduce the behavior — AI-CONTEXT §9)
happens **between** declaration-time and acceptance-time and is C28/C09's job, not C51's.

(Sequence diagram for the declare→build→accept→review flow, and the exact scenario-coverage check, are
sweep-2 deliverables per BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C51 (canonical) |
|---|---|---|
| **G07** (major) — transfusion has no correctness/completeness acceptance criterion; "behaves like the exemplar" undefined | C51 is the component that *closes* G07 by defining the predicate. | **Addressed at sweep-1 altitude**: §3.3 defines the predicate as exemplar-grounded scenarios (C30) → judged satisfaction (C32/C33) ≥ bar, **plus** a completeness clause (every named exemplar behavior ⇒ ≥1 scenario). The *numeric* bar is operator/integrator policy (C50/C53; C33 is threshold-free). C51 owns the **predicate shape + exemplar-grounding requirement**, not a new scorer. |
| **G14** (major) — transfusion reliability is an unhedged "bet"; ~half the principles (P7/P8/P11/P12) gated on it; no fallback | The predicate makes the bet **falsifiable per component**. | **Addressed (discipline-layer fallback)**: §3.5 defines the *transfusion-insufficient* outcome — fail/inconclusive routes to human design review (README:498) instead of shipping. C51 cannot make transfusion *succeed*; it makes failure **detectable, bounded, and non-shipping**. The strategic fallback for a *whole class* failing (re-sequence phases / hand-build) is a C54 phase-plan decision, flagged §9. |
| **G30** (minor) — code-vs-pattern transfusion boundary "left to chance"; Tracker license unverified | The license-mode contract removes the chance. | **Addressed**: §3.4 — unverified/restrictive license ⇒ `transfusion_mode = pattern-reimplement` (no code-port); verified-permissive ⇒ code-port allowed + donate-back permitted (AI-CONTEXT:430). Built on the existing README:285–306 census (a build-blocking fact), **not** an automated SBOM scanner (over-build; §9). Tracker is the canonical instance: unverified ⇒ pattern-only until verified (README:335; AI-CONTEXT:625). |
| **F54** (RSI / goal-subversion — F-MODE §11; G35) | A self-modifying factory could drift its own acceptance bar over cycles. | C51 reduces blast radius by keeping the predicate **exemplar-anchored** (an external, human-chosen ground truth) and the verdict **recorded + design-reviewed** (README:498). C51 does not *enforce* against RSI (that is C43/audit-pack; G35) — flagged as residual §9. |
| **F9** Spec overfitting (F-MODE §1) | Exemplar-grounded scenarios could be gamed/overfit. | The predicate inherits C30's holdout discipline (C34) — the implementer does not author/read its own grading scenarios; transfusion scenarios are held out like any other. C51 adds no new isolation; it relies on C34. |
| Empty / missing `transfused_from` | Silent "invention from scratch" violating B55 | Invariant §3: rejected at declaration-time. A factory-built component **must** declare ≥1 exemplar. |
| License declared but unverified, yet code-ported | Legal exposure (README:292 "Verify before adopting") | License mode is fixed **pre-build** (§5 declaration-time); a code-port from an unverified license is blocked before the agent runs, not caught after. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security / license.** The license-mode contract (§3.4) is the factory's **legal-hygiene control**:
  no code enters a factory-built component from an exemplar whose license is unverified or restrictive
  (README:292,335; AI-CONTEXT:625). This is the load-bearing half of G30. Signed provenance of the
  transfusion record is **not** required (attribution is self-asserted per G36/D-14; signing is FE-3,
  blocked on G37) — surfaced as residual risk §9.
- **Cost.** Negligible incremental cost — C51 reuses the C30–C33 evaluation tier (the transfusion
  scenarios are *part of* the component's own scenario suite, README:499). It adds no second judge, so it
  does not multiply the per-component judge token cost (the C32/C28 cost concern, G13/G32) — this is
  exactly the over-build the bar rejects.
- **Scale.** One predicate evaluation per factory-built component at acceptance-time — build-cadence, not
  request-cadence. No scale concern.
- **Observability.** The transfusion record (`transfused_from` + license + verdict) **is** the audit
  trail for "where did this component's behavior come from and did we prove it?" — it is what the §16
  cold-start step 2 ("Check `transfused_from`") reads, and what C57's residual-risk register aggregates.
- **Ops.** The license census (README:285–306) is hand-maintained and rides normal git review; C51 makes
  its facts **build-blocking** but does not replace it with tooling. Census staleness is an ops risk (a
  new exemplar must be added before its first use) — flagged §9.

## 8. Acceptance criteria & test strategy

1. **≥1-exemplar enforced (B55 closed)**: a factory-built component declaring zero exemplars is rejected
   at the discipline gate; one declaring ≥1 `transfused_from` URL passes the declaration check
   (README:496).
2. **Component-grain provenance (RC11-01)**: `transfused_from` is recorded **once per factory-built
   component** on its `factory_build` bead — verified by §16 cold-start step 2 resolving it from the
   component's build bead, **not** from arbitrary downstream beads/turns.
3. **Predicate is exemplar-grounded + complete (G07)**: for a factory-built component, every *named*
   behavior of the declared exemplar is covered by ≥1 scenario (completeness), and a `pass` verdict
   requires the satisfaction distribution over those scenarios to meet the bar (correctness). A component
   that satisfies a generic spec but covers **no** exemplar behavior does **not** pass. **Note: the numeric
   bar is C50/C53 policy, not set here** — C51 guarantees the *predicate shape*, not the cutline (parity
   with C20 providing G18 slots but not the threshold).
4. **License mode blocks code-port on unverified/restrictive (G30)**: a build attempting to **code-port**
   from an exemplar whose license is unverified or restrictive is rejected; the same exemplar is permitted
   under `pattern-reimplement`. Tracker (unverified) is the test instance (README:335).
5. **Bet-failure routes to review, never silent-ships (G14)**: a component whose predicate returns
   fail/inconclusive emits *transfusion-insufficient* and is routed to human design review (README:498),
   not deployed. **Note: this is G14 *made falsifiable*, not G14 *eliminated*** — the residual "what if a
   whole class can't be transfused" is a C54 phase-plan decision (OQ-C51-2), not closed here.
6. **External-grounding exclusion holds (A107)**: an *adopted* upstream substrate dependency (CXDB,
   Temporal) is **not** flagged for a missing `transfused_from` — only factory-built glue is in scope
   (README:500).

(Concrete scenario-coverage schema, the verdict field shape on the `factory_build` bead, and
conformance vectors for the license-mode decision table are sweep-2 deliverables, co-frozen with C20
(fields) and C30/C32/C33 (predicate wiring).)

## 9. Open questions

- **OQ-C51-1** (→ review-log): **"Named exemplar behaviors" extraction (the completeness anchor).** The
  completeness clause requires enumerating the exemplar's behaviors so each can be covered by a scenario —
  but v4 defines transfusion *by analogy* and names no behavior-extraction method (AI-CONTEXT §9). Is the
  behavior list authored by the operator at intent-intake (C11), derived from the exemplar's own
  tests/docs, or a [FAITHFUL-FILL] left to sweep-2? Without a defined anchor, "complete" is subjective —
  the residual edge of G07. **Top open question.**
- **OQ-C51-2** (→ review-log): **G14 class-level fallback ownership.** C51 makes the bet falsifiable
  *per component* and routes a single failure to review, but the strategic fallback for "a whole
  high-value class (Healer/twins/self-opt) cannot be reliably transfused" (re-sequence phases? hand-build?
  abandon a principle?) is a **C54 phase-plan** decision, not C51's. Confirm C54 owns the class-level
  hedge so G14 is fully homed.
- **OQ-C51-3** (→ review-log): **Numeric satisfaction bar + threshold owner (shared G09).** C51's
  predicate is bar-relative but threshold-free (parity with C33:OQ-1). Confirm the transfusion-acceptance
  cutline lives at **C53** (bootstrap milestone) / **C50** (promotion gate) as operator/integrator policy,
  and that the same satisfaction statistic C33 emits is the one C51's predicate reads.
- **OQ-C51-4** (→ review-log): **License census authority + staleness (G30 / shared with C57).** C51
  treats README:285–306 as the build-blocking license source of truth, but it is hand-maintained and lists
  several sources "verify (convention)". Confirm C57 (which "owns license hygiene") is the authoritative
  home of the census and the verification workflow, and that adding a new exemplar's license is a
  prerequisite step before its first transfusion (no automated SBOM scanner at Phase 0 — confirm that
  scope boundary).
- **OQ-C51-5** (→ review-log): **Transfusion-record signing (G36/G37/FE-3).** `transfused_from` and the
  verdict are **self-asserted** (no signature; D-14). Confirm this is acceptable for Phase 0 (consistent
  with C20's self-asserted `created_by`) and that signed transfusion provenance is FE-3 (blocked on G37
  secrets), not a Phase-0 requirement.
