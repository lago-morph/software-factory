# C56 — Autonomy ladder (L0–L5)  (Spec, canonical track)

> Source: README §Part 2 "the autonomy ladder" (L77–90: the L0→L5 flowchart — "**L0 Manual**, **L1
> Intern**, **L2 Pair**, **L3 HITL**, **L4 PM mode**, **L5 Dark**"; L77 "every working factory aims at one
> of the upper rungs of the autonomy ladder"; L90 "v4's substrate is built for **L4-L5 operation** — most
> steps run **without per-step human review**, scenarios drive evaluation, attribution is automatic, the
> self-healing loop catches and fixes what breaks"); README §Part 6/7 (L498 "**Design review before
> deployment.** Human reviews the factory's design output before any factory-built component goes into
> production use. **Required until P12 is mature and trusted**"; L527 "**No commitment to L5 autonomy on
> day one.** The runtime can run at **L4 (PM mode, specs in, software out, batched review)** for as long as
> needed. **L5 is the natural endpoint, not a precondition**"); README §P11 (L248 "Observability → anomaly
> → diagnosis → fix → **ship, without human intervention**"); AI-CONTEXT §2 (L56 "**Five-Levels autonomy
> ladder: L0 manual → L1 intern → L2 pair → L3 HITL (the trap) → L4 PM mode → L5 dark. v4 targets
> L4-L5**"); F-MODE-COVERAGE §9 (F5 L112 "v4 mitigates via **L4-L5 batching (no per-cycle review)** … v4
> explicitly targets **out-of-loop**"; F6 L113 "Operator mental-model erosion is an **accepted cost of
> L4-L5 operation**"); F-MODE-COVERAGE §11/§12 (F54 goal-subversion "the **weakest** v4 mechanism", L178
> "**Plan an F54 audit pack** … regular goal-statement comparisons across cycles, **escalation on detected
> drift**"); component-inventory C56 row (subsystem Security & Governance; kind cross-cutting; "Maturity
> scale manual→intern→pair→HITL→PM-mode→dark; v4 targets L4–L5 (out-of-loop batched review)"; maps **A13,
> B10**; depends on **C52**; gaps **G15, G35**; foundational: no; Batch 4); ambiguities-and-gaps **G15**
> (minor — autonomy levels assume one operator can author specs fast enough; guard "honest staffing /
> document it") and **G35** (major — RSI/goal-subversion is the weakest acknowledged mechanism on a
> self-modifying factory whose P11 fix-tasks auto-ship at L5); review-log **D-6** (canonical track — no
> "Track A/B" framing).
> Inventory ID: C56   Kind: cross-cutting (governance/policy artifact)   Status: sweep-1
> Track: canonical (faithful posture)

## 1. Purpose & responsibility

C56 is the **autonomy ladder**: the canonical, named scale of six **autonomy levels** — **L0 Manual, L1
Intern, L2 Pair, L3 HITL, L4 PM mode, L5 Dark** (README:81–86; AI-CONTEXT:56) — together with **the
per-level authorization boundary**: *which level authorizes which class of autonomous action without a
human in the loop*. It is a **governance/policy artifact**, not a runtime service. Its single load-bearing
output is a **declared, read-only "current authorized autonomy level"** plus the **rule that maps a level
to what may proceed without per-step human review** — the boundary between human-in-loop and out-of-loop
operation that the rest of the factory *consumes* to decide whether a given action may auto-proceed.

C56 exists because v4 is built for **L4–L5 operation** (README:90; AI-CONTEXT:56) — and "L4 vs L5" is a
*specific authorization difference* (L4 = batched human review of out-of-loop work; L5 = dark / no human in
the loop) that multiple components must agree on. Rather than each consumer re-deriving "what does L5
permit," v4 needs **one place** that (a) names the levels, (b) fixes the **L3→L4 out-of-loop transition**
(the "HITL trap", AI-CONTEXT:56) and the **L4→L5 auto-ship transition**, and (c) declares which level is
currently authorized. C56 is that place. The two components whose safety hinges on this boundary are
**C39** (fix-task loop-closure — gates *L5 ship-authorization* of an autonomous fix on the level; G35) and
**C53** (bootstrap-validation milestone — gates the *bootstrap deploy* on the level / the "design review
before deployment … required until P12 is mature", README:498). C56 **defines the ladder; those components
consume the level.**

**Responsibilities**
- **Define the closed L0–L5 ladder** — the six named levels in order (manual → intern → pair → HITL → PM
  mode → dark), each with a one-line semantics anchored to v4 (README:81–86; AI-CONTEXT:56), and the
  ordering invariant `L0 < L1 < L2 < L3 < L4 < L5` (monotone increasing autonomy).
- **Define the per-level authorization boundary** (the G35-relevant KEEP) — for each level, *what class of
  action may proceed without per-step human review*. The load-bearing rows are the **L3/L4 boundary**
  (at/below L3 a human is in the per-step or per-cycle loop; at L4 work runs out-of-loop with **batched**
  review; README:90/527, F5/F6) and the **L4/L5 boundary** (at L4 autonomous output is **batched for human
  review before it ships**; at L5 it may **auto-ship / deploy without a human**; README:248/527).
- **Declare the current authorized level** — expose a single read-only value, *the level the operator has
  authorized the factory to operate at right now*, that consumers (C39, C53, …) read to gate their own
  out-of-loop actions. v4 makes this **operator-set and downgradable** ("no commitment to L5 … for as long
  as needed", README:527).
- **Own the architecture-level seam for the G35 objective-drift bound** — name (and route to C57's
  residual-risk register) that **higher rungs (L4/L5) carry the weakest-controlled failure mode, F54
  goal-subversion over cycles** (F-MODE-COVERAGE §11/§12), and that the *response* is the **F54 audit pack**
  (periodic goal-statement comparison across cycles, escalation on drift; F-MODE-COVERAGE:178). C56 owns
  *the ladder + which level may auto-ship* (the policy); it **names** the audit-pack obligation and defers
  the audit *mechanism* to C57 (register) + the deferred audit pack (Phase-3+). (See §6/G35.)
- **State the L4-default posture** — v4's binding default is **L4 (PM mode, batched review), not L5**; L5 is
  an opt-in endpoint requiring P12 maturity + trust (README:498/527). C56 makes "what is the safe default
  level" explicit so consumers fail safe (treat L5 as not-authorized unless explicitly declared).

**Explicitly NOT**
- **NOT an enforcement engine.** C56 is **policy/definition only**. It declares the levels and the
  level→authorization map and the current level; it does **not** intercept, gate, or block any action at
  runtime. *Enforcement* of "this action may not proceed because the level is too low" lives in the
  components that take the action: **C39** enforces the L5 ship-gate on fixes (its I4 invariant), **C53**
  enforces the bootstrap deploy gate, **C43** bounds the *blast radius* that makes a given level survivable,
  and **C34** enforces holdout read-isolation. C56 is the *single source of the level*, the way a feature
  flag is the source of a capability bit but not the code that branches on it. (Flagging the over-build the
  bar warns against: an autonomy *enforcement* engine would duplicate C39/C43/C34 and is dropped — see §7.)
- **NOT the fix-task termination / ship policy (C39).** C39 owns the **numeric** heal-loop policy
  (N-attempts→escalate, F52 oscillation detection) **and** the act of gating a fix's ship on the level
  (C39 §3 contract 7, I4; XC-3/D-3). C56 supplies *the level and what each level authorizes*; C39 *reads it
  and enforces the gate on fixes*. (C39 §1 states the reverse: "NOT the autonomy ladder itself … C39 reads
  the current authorized level; it does not define or set the ladder.")
- **NOT the bootstrap deploy gate (C53) or its rubric.** C53 owns the **go/no-go bootstrap-validation
  rubric** ("does the first factory-built component pass review and deploy"; G23). C56 supplies the
  *autonomy level* that decides whether that deploy needs human review (L4 batched vs L5 dark; README:498).
  C53 reads the level; C56 does not own the rubric.
- **NOT the lethal-trifecta / blast-radius bound (C43).** C43 bounds **what an autonomous agent can touch**
  (twin-by-default; G31) — the *blast-radius* half of G35. C56 sets **how autonomous the factory is
  authorized to be** — the *authorization* half. Higher C56 rungs are only *survivable* because C43 caps the
  blast radius (C43 §2 "the blast-radius bound is what makes higher autonomy rungs (L4/L5) survivable").
  Distinct axes: C56 = how much autonomy; C43 = how much damage that autonomy can do. (C43 §1 states the
  reverse boundary.)
- **NOT the override→rule discipline loop (C35).** C35 detects operator overrides and (operator-gated)
  converts recurring ones to rules. C56 sets the level *at which* such operator interventions are expected
  (per-step at low levels; batched/none at L4/L5). C35 is a *loop*; C56 is the *level definition* that loop
  operates under. The multi-cycle goal-drift audit (F54) is shared **C56/C57** scope (the ladder owner +
  the residual-risk register), not C35's.
- **NOT the residual-risk register / F54 audit-pack mechanism (C57).** C56 **names** that L4/L5 carry the
  F54 objective-drift risk and that the response is an audit pack; **C57** owns the canonical residual-risk
  register and the honest "weakest mechanism" accounting (inventory C57: gaps include G35), and the audit
  *pack* itself is a deferred Phase-3+ build. C56 owns the ladder + the per-level auto-ship boundary; it
  routes the drift-audit *mechanism* to C57 (§6).
- **NOT a staffing/throughput solution (G15).** That one operator can author specs fast enough to feed an
  L4/L5 factory is an **operator-side capacity assumption**, not a runtime mechanism (F-MODE-COVERAGE F25,
  guard "honest staffing / document it"). C56 *documents* it as a precondition for sustained L4/L5; it does
  not solve it (§6/G15).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C52** Self-bootstrap recursion & design review | The sole inventory dependency (C56 `depends on C52`). The autonomy level is the dial on the **self-bootstrap** loop: C52 "authors a spec for its own next component, runs, **human-reviews before deploy**, extends itself" — *whether* that review is per-step (L≤3), batched (L4), or absent (L5) is exactly what C56's level governs. C56 supplies the level; C52's design-review discipline (README:498) is the L4-default behavior the ladder formalizes. > [FAITHFUL-FILL] — see §4. |
| Downstream (fix-ship gate) | **C39** Fix-task generation & loop-closure | **The primary G35 consumer.** C39 gates **L5 ship-authorization** of an autonomous fix on C56's current level (C39 I4: ship-without-review only at L5; L4 batched; below L4 per-fix-gated). C39 *reads* the level; C56 *defines* it. The C39↔C56 tie is the **G35 disposition seam** (C39 §6/OQ3), not a hard inventory dependency of C39. |
| Downstream (bootstrap deploy gate) | **C53** Bootstrap-validation milestone | C53's go/no-go deploy of the first factory-built component is gated by the **design-review-before-deployment** rule (README:498) — i.e. by the autonomy level (L4 batched-review vs L5 auto-deploy). C53 reads the level; C56 supplies it + the L4-default. |
| Downstream (blast-radius pairing) | **C43** Isolation & lethal-trifecta boundary | C43 caps the **blast radius** that makes a C56 rung **survivable** (C43 §2/§6/G35: "more autonomy ⇒ more potential blast radius, capped by C43's twin-by-default posture"). Paired axes: C56 = authorized autonomy, C43 = bounded damage. |
| Downstream (objective-drift audit) | **C57** Failure-mode coverage & residual-risk register | C56 names the **F54 goal-subversion** risk that L4/L5 carry (the weakest v4 mechanism) and routes the **audit-pack** obligation to C57's register (inventory C57 gaps include G35). C56 = ladder + auto-ship boundary; C57 = residual-risk accounting + the deferred audit mechanism. |
| Downstream (override expectation) | **C35** Override→pattern→rule loop | The level sets the *expected cadence* of operator intervention C35 observes (per-step at low levels; batched/none at L4/L5). Soft seam, not a contract. |
| Config seam (where the level lives) | **C03** Layered config / feature-flag model | > [FAITHFUL-FILL] — the **current authorized level** is most consistently a single operator-set value carried in layered config (C03), the same way capabilities are section-gated there. The exact representation (a `[autonomy] level = "L4"` key vs a dedicated C56 surface) is **sweep-2 / OQ-2**; v4 names no on-disk form. |

C56 is **not foundational** (inventory: no) and is in **Batch 4** ("factory builds factory" — built
alongside C39/C43/C51–C55). It sits in the **Security & Governance** subsystem. Its weight is not on a
build critical path; it is a **small, load-bearing policy artifact** that the self-healing and bootstrap
tiers read to know how far they may act without a human.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; the concrete level-read API/representation, the per-level
authorization table's machine form, and the audit-pack interface are sweep-2 deliverables.

1. **Ladder definition (the level vocabulary).** The closed, ordered set of six levels
   `{L0 Manual, L1 Intern, L2 Pair, L3 HITL, L4 PM mode, L5 Dark}` with the ordering
   `L0 < L1 < L2 < L3 < L4 < L5`, each carrying a one-line v4-anchored semantics (§4.1). Any component can
   name a level and compare two levels. This is the canonical vocabulary C07's glossary cross-references.
2. **Per-level authorization boundary (the load-bearing KEEP).** A mapping `level → {what may proceed
   without per-step human review}`, with the two load-bearing thresholds named: the **out-of-loop
   threshold** (the L3→L4 boundary: at/below L3 a human is in the per-step/per-cycle loop; at L4 work runs
   out-of-loop with *batched* review) and the **auto-ship threshold** (the L4→L5 boundary: at L4 autonomous
   output is *batched for review before it ships*; at L5 it may *auto-ship/deploy without a human*).
   Consumers (C39, C53) read this to decide whether their own action may auto-proceed. *Sweep-1: named +
   described as a table (§4.2); the precise per-action predicate form is sweep-2.*
3. **Current-authorized-level read (the runtime output).** A single read-only value — *the level the
   operator has authorized right now* — that any consumer reads to gate out-of-loop behavior (C39's ship
   gate reads exactly this; C39 §3 contract 4 "Current-autonomy-level read (C56 → C39)"). **Operator-set,
   monotone-not-assumed: a consumer that cannot read it, or reads an undefined value, MUST treat the level
   as the safe default (≤ L4, i.e. *not L5*)** — fail-safe (README:527 "no commitment to L5").
4. **L4-default declaration.** The binding statement that the **default operating level is L4** (batched
   review), and that L5 is opt-in requiring P12 maturity + trust (README:498/527). Consumers use this to
   pick the safe behavior when the level is unset.
5. **F54 audit-pack obligation (named seam, not a mechanism).** The declaration that operating at L4/L5
   incurs the **F54 objective-drift** residual and obliges the **F54 audit pack** (periodic goal-statement
   comparison across cycles + escalation on drift; F-MODE-COVERAGE:178), whose register + mechanism are
   **C57's** (and a deferred Phase-3+ build). C56 publishes the *obligation*; it does not implement the
   audit. (Per the bar this is a one-line routing note, not an audit engine — §6/§7.)

**Invariants**
- **Ladder closure & order.** Exactly six levels, in the fixed order L0<L1<L2<L3<L4<L5. A "level" outside
  this set is invalid; comparison of two levels is total. (README:81–87; AI-CONTEXT:56.)
- **Authorization monotonicity.** If an action class is authorized to proceed without per-step review at
  level Lₙ, it is authorized at every Lₘ > Lₙ. (Autonomy only *adds* out-of-loop authority going up the
  ladder — the ladder is a maturity scale, README:77.) The two named thresholds (out-of-loop at L4,
  auto-ship at L5) are the points where authority is *added*.
- **Fail-safe default (load-bearing).** Absent an explicit operator declaration, the authorized level is
  the **L4 default**, never L5; a consumer that cannot resolve the level treats it as *not L5* (no
  auto-ship). This is the invariant that prevents an unset/garbled level from silently authorizing dark
  operation (README:527).
- **Definition-not-enforcement.** C56's output is *read*; C56 takes no enforcing action. Every "the action
  was blocked" guarantee is the *consumer's* invariant (C39 I4, C53 gate, C43 blast bound), not C56's. C56
  guarantees only that *the level and its authorization meaning are defined, ordered, and readable*.

## 4. Data model / state

C56 owns a **definition** (the ladder + the level→authorization map) and a **single declared scalar** (the
current authorized level). It owns **no per-run instance state** and **no store**.

### 4.1 The ladder (the level vocabulary)

| Level | Name | One-line semantics (v4-anchored) | Human-in-loop? |
|---|---|---|---|
| **L0** | Manual | Operator does the work; the system assists at most. | Fully in-loop (does it). |
| **L1** | Intern | System proposes; operator does/checks each step as for a junior. | Per-step in-loop. |
| **L2** | Pair | System and operator work together, turn by turn (pairing). | Per-turn in-loop. |
| **L3** | HITL | Human-in-the-loop on each cycle — *"the trap"* (AI-CONTEXT:56): looks autonomous but the operator is still the per-cycle bottleneck (F5/F6, F-MODE §9). | Per-cycle in-loop. |
| **L4** | PM mode | **Specs in, software out, batched review** (README:527): work runs **out-of-loop**; the operator reviews **batches** of output, not each step. v4's **default** target. | Out-of-loop, **batched** review. |
| **L5** | Dark | No human in the loop: autonomous output **ships without human intervention** (README:248). The natural endpoint, opt-in (README:527). | Out-of-loop, **no** review. |

> [FAITHFUL-FILL] **One-line per-level semantics.** v4 gives the six level *names* (README:81–86;
> AI-CONTEXT:56) and rich definition only for the **L3/L4/L5** band it actually targets (HITL = "the trap";
> L4 = "PM mode, specs in, software out, batched review"; L5 = "dark / ship without human intervention").
> L0–L2 are named but not elaborated. The minimal faithful fill is the standard "Five-Levels" reading the
> docs invoke ("Five-Levels autonomy ladder", AI-CONTEXT:56) — manual / intern (junior, per-step) / pair
> (per-turn) — chosen because (a) it matches the level *names* verbatim and (b) only the L3→L5 band is
> load-bearing for v4's consumers (C39/C53 gate on L4 vs L5), so the low rungs need only enough semantics to
> make the *ordering* and the *out-of-loop threshold* well-defined. No consumer branches on L0/L1/L2
> distinctly in v4.

### 4.2 The per-level authorization boundary (the load-bearing KEEP — G35)

The boundary answers, per level, *what may proceed without per-step human review*. The two thresholds that
v4 names are the only load-bearing rows; the rest follow from monotonicity (§3 invariant).

| Level | Out-of-loop execution? | Autonomous **ship/deploy** without a human? | What a consumer (C39/C53) does at this level |
|---|---|---|---|
| L0–L2 | No (operator in per-step/per-turn loop) | No | Each step/ship is human-driven or human-gated. |
| **L3 (HITL)** | Per-cycle human gate (the "trap") | No — human gates each cycle | A fix/deploy is **gated per cycle** by the operator. |
| **L4 (PM mode, default)** | **Yes** — runs out-of-loop | **No** — output is **batched for human review before it ships** | C39 **batches** the proven fix for operator review before "shipped"; C53 routes the bootstrap deploy through **design review** (README:498). |
| **L5 (Dark)** | Yes | **Yes** — **auto-ship / deploy without a human** | C39 may **auto-ship** the proven fix (its escalation/oscillation bounds still hold); C53 may auto-deploy. |

> [FAITHFUL-FILL] **The boundary table is the operational reading of v4's prose; the two thresholds are
> v4-stated.** v4 states the **L4↔L5 ship difference** explicitly ("batched review" at L4 vs "ship without
> human intervention" at L5; README:248/527) and the **out-of-loop transition** at L4 ("most steps run
> without per-step human review", README:90; F5 "L4-L5 batching (no per-cycle review) … out-of-loop",
> F-MODE §9). The minimal faithful elaboration fills the L0–L3 rows by monotonicity (autonomy only adds
> going up) — these rows are *implied*, not invented, and no v4 consumer needs a finer L0–L3 distinction.
> The table is the *authorization* artifact; the **enforcement** of any row is the consumer's (C39/C53), and
> the **per-action predicate** form (e.g. an OPA policy the `Healer governance | OPA` row, AI-CONTEXT:335,
> would carry for C39) is sweep-2.

### 4.3 The current authorized level (the declared scalar)

A single operator-set value naming the level the factory is authorized to operate at now. v4 properties
(README:527): **operator-set**, **defaults to L4**, **downgradable at any time** ("for as long as needed"),
**L5 is opt-in**. > [FAITHFUL-FILL] the on-disk representation (a C03 config key vs a dedicated surface) is
**OQ-2 / sweep-2**; v4 names no form. The **fail-safe rule** (§3 invariant) makes an unset/garbled value
resolve to *not-L5*.

### 4.4 Persistence & consistency

C56 holds **no store and no per-run state**. The ladder + authorization map are **definitional** (this
spec + C07 glossary); the current level is a single value in config (C03, faithful — §2). Consistency
requirement: the current level is **read at the point of the gated action** (C39 re-reads at ship time so a
mid-flight downgrade is honored — C39 edge "autonomy-level downgrade mid-flight"), so the authoritative
value is whatever config holds at decision time, not a cached snapshot.

## 5. Behavior

C56 has **no control loop**; its behavior is **definitional** and **read-time**:

- **Definition-time:** declares the six-level ladder (§4.1), the per-level authorization boundary (§4.2)
  with the two named thresholds, the L4-default, and the F54 audit-pack obligation seam (§3.5).
- **Operator-set-time:** the operator declares/changes the current authorized level (config, C03 — faithful)
  — e.g. raising from L4 to L5 once P12 is "mature and trusted" (README:498), or lowering it at any time
  (README:527). C56 defines what the value *means*; the act of setting it is an operator/config action.
- **Read-time (the consumers act, not C56):** C39's ship gate reads the current level and **enforces** the
  L4-batched / L5-auto-ship branch (C39 §5 "Gate the ship"); C53's deploy gate reads it to decide whether
  the bootstrap deploy needs design review. C56 **supplies the level + its meaning**; it performs no gating
  itself.
- **Audit-obligation-time (C57/deferred):** at L4/L5, the named F54 audit-pack obligation is in force; the
  audit *mechanism* (periodic goal-statement comparison + drift escalation, F-MODE-COVERAGE:178) is C57's
  register + a deferred Phase-3+ build. C56 declares the obligation; it does not run the audit.

(Sequence/state diagrams for the operator-set transition and the consumer read-gate are deferred to sweep 2
per BUILDER-BRIEF altitude. There is no state machine internal to C56 beyond "the current level is whatever
the operator last declared, defaulting to L4".)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C56 (faithful) |
|---|---|---|
| **G35** RSI / goal-subversion blast-radius on a self-modifying L5 factory (major) | The major gap C56 co-owns: a factory that **auto-ships its own fixes at L5** (P11/C39) with the **weakest** control on objective drift (F54). | **Authorization-half owned + named; objective-drift audit deferred to C57 (faithful).** C56 owns the **authorization** dimension of G35: it **defines which level may auto-ship** (the L4↔L5 threshold, §4.2) and makes **L4-batched-review the default** so dark/auto-ship is *opt-in*, not the resting state (README:527). This bounds *when* the factory may self-modify-and-ship without a human. C56 then **names** that L4/L5 carry the **F54** objective-drift residual (the weakest v4 mechanism, F-MODE-COVERAGE §11/§12) and that the response is the **F54 audit pack** (goal-statement comparison across cycles + drift escalation, F-MODE-COVERAGE:178) — routing the audit **register + mechanism to C57** (residual-risk register; inventory C57 gaps include G35) and the audit pack itself to a **deferred Phase-3+** build. The **blast-radius** half of G35 (what an L5 agent can touch) is **C43's** (twin-by-default; G31). The **per-fix** termination/ship enforcement is **C39's** (I4). So G35 is split: **C56 = which level may auto-ship + L4 default + audit obligation; C43 = blast radius; C39 = per-fix gate enforcement; C57 = drift-audit register**. Recorded, routed, not absorbed. See the §6 AMBIGUITY. |
| **G15** One operator may not author specs fast enough for L4/L5 (minor) | An L4/L5 factory consumes operator-authored specs faster than at low rungs; F-MODE F25 "design starvation … by construction", guard "honest staffing / document it". | **Documented as a precondition, not solved (faithful — it is operator-side).** C56 records that **sustained L4/L5 operation assumes the operator can author specs fast enough to feed the factory** (F-MODE-COVERAGE F25). This is an **operator-capacity assumption**, not a runtime mechanism; v4's own guard is "honest staffing / document it." C56's faithful response is exactly to *document it* as a stated precondition for raising the level (and route to C57's residual register), not to design a throughput mechanism (which would exceed the artifact's scope and the bar). See OQ-1. |
| **F5** Cognitive ceiling / **F6** Cognitive debt (F-MODE §9) | Operator mental-model erosion under out-of-loop operation. | **Accepted cost, named (faithful).** F-MODE §9 marks these as **operator-side accepted costs of L4-L5 operation** ("v4 explicitly targets out-of-loop"; "accepted cost"). C56 names that **raising to L4/L5 trades per-step operator insight for throughput** — the cost the ladder's upper rungs deliberately accept. Not a C56 mechanism; surfaced so consumers/operators choose the level knowingly. |
| **F54** Goal subversion over cycles (the weakest v4 mechanism) | Multi-cycle objective drift on a self-modifying factory at L5. | **Named + audit-pack obligation routed to C57 (faithful).** This is the failure mode that *makes G35 major*. C56 does not detect drift (that is the audit pack's job); it **names the obligation** that L4/L5 carry it and **points at C57** (register) + the deferred audit pack (F-MODE-COVERAGE:178). C56's *own* contribution to bounding F54 is structural: **L4-default + the L5-opt-in threshold** keep dark auto-ship from being the resting state. |
| **Unset / garbled current level** (operational) | A consumer reads an undefined or unparseable level. | **Fail-safe to not-L5 (faithful, §3 invariant).** The consumer treats an unresolvable level as the **L4 default (not L5)** — no auto-ship. An unset level can never *raise* autonomy; only an explicit operator declaration can reach L5 (README:527). |

> [AMBIGUITY: G35] **Does C56 *enforce* the autonomy bound, or only *define* the levels + which level
> authorizes auto-ship?**
> Reading A (definition/policy artifact — faithful): the inventory kinds C56 **cross-cutting**, the source
> material is the *ladder* (README:81–90; AI-CONTEXT:56) and the *L4-vs-L5 ship difference* (README:248/527),
> and every consumer spec already treats C56 as the thing it **reads** (C39 §3 "Current-autonomy-level read
> (C56 → C39)"; C39 §1 "C39 reads the current authorized level; it does not define or set the ladder"; C53
> deploy gate; C43 "more autonomy ⇒ more blast radius"). On this reading C56 **defines** the ladder + the
> per-level authorization boundary + the current level, and **enforcement is the consumer's** (C39 I4, C53
> gate, C43 blast bound).
> Reading B (C56 as an autonomy *enforcement* engine): one could make C56 a runtime gate that intercepts and
> blocks any out-of-bound action — a central "autonomy controller" that all auto-ship/auto-deploy calls must
> pass through.
> **Pick: Reading A.** Most consistent with the rest of v4 and binding under the capability-for-principle
> bar. (1) v4 *describes* the ladder as a **maturity scale / governance frame** (README Part 2; AI-CONTEXT
> §2), never as a runtime interceptor. (2) The downstream specs are **already written to read C56, not be
> gated by it** — C39 explicitly owns its own ship-gate enforcement (I4) and names C56 as the *level source*,
> not the gate; making C56 an enforcement engine would **duplicate C39/C43/C34** and contradict their frozen
> specs. (3) The bar: an enforcement engine is **more machinery without a new principle** — the levels are
> *policy*; enforcement already lives at C43 (blast radius), C34 (holdout), C39 (fix ship). So the KEEP is
> **the ladder definition + the per-level authorization boundary + the declared current level + the L4
> default + the named F54 audit-pack obligation**; the DROP is any autonomy enforcement engine. C56 is the
> *single source of the level and what it authorizes*; the components that act enforce their own bound
> against it. (The objective-drift *audit* mechanism is C57's; the per-fix gate is C39's; the blast bound is
> C43's — G35 is split across these owners with C56 owning the ladder + auto-ship threshold + L4 default.)

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the central concern).** C56 is the **governance dial** of the whole factory: it declares **how
  autonomous the factory is authorized to be**, and therefore *when production change may happen without a
  human* (the L5 auto-ship threshold) and *when the factory may modify itself without review* (the L4-default
  design-review rule, README:498). Its security value is entirely in **(a) the L4-default** (dark/auto-ship
  is opt-in, never the resting state) and **(b) the named L4↔L5 threshold** every consumer gates on. The
  matching guarantees that an over-bound action is *actually stopped* are the consumers' invariants (C39 I4,
  C53 gate) plus C43's blast-radius bound; C56 makes the *level and its meaning* unambiguous so those gates
  have a single authority to read. The **F54 objective-drift** residual (the weakest v4 mechanism) is C56's
  named obligation routed to C57. **Over-build flag (the bar):** a tempting addition is an *autonomy
  enforcement engine* (a central interceptor for all auto-ship/auto-deploy). **Dropped** — the levels are
  policy; enforcement lives at C43/C34/C39, and an interceptor would duplicate them and exceed a
  governance-artifact's scope. The KEEP is the ladder + per-level authorization boundary + the declared
  level + the L4 default + the F54 audit obligation.
- **Cost.** Effectively zero: a definition + a single config value (C03). No store, no engine, no per-run
  state. (The *audit pack* the ladder obliges at L4/L5 has cost — but that is C57's / a deferred build.)
- **Scale.** None — a scalar read at decision time. The level read is O(1) config access; it adds no
  throughput concern. (The *operator-spec-throughput* limit G15 names is an operator-capacity issue C56
  documents, not a C56 scaling property — §6.)
- **Observability.** The current level and any change to it should be visible/attributable (it is a
  governance act): a level change is an operator action that ought to land on the event bus (C23) with
  `created_by` (C41) like any other — so "who raised the factory to L5, and when" is auditable. > [FAITHFUL-FILL]
  v4 does not state this explicitly; it is the minimal consistent choice given P9 universal attribution
  (every action attributed). Concrete wiring is sweep-2.
- **Ops.** C56 is **pure policy/config**: changing the authorized level is a **config change** (C03), not a
  redeploy; the ladder definition + authorization map are documentation + glossary (C07). Raising to L5 is
  an explicit, reviewable operator decision gated on "P12 mature and trusted" (README:498) — an ops/governance
  checklist item, not an automated promotion.

## 8. Acceptance criteria & test strategy

1. **Ladder is defined, closed, and ordered (AC).** The six levels `{L0 Manual … L5 Dark}` are named with
   one-line semantics and a total order `L0<L1<L2<L3<L4<L5`; a value outside the set is invalid; any two
   levels compare. (README:81–87; AI-CONTEXT:56.)
2. **Per-level authorization boundary is explicit, with the two named thresholds (AC — the G35 KEEP).** For
   each level the table (§4.2) states whether work runs out-of-loop and whether autonomous output may
   **ship/deploy without a human**; the **out-of-loop threshold (L4)** and the **auto-ship threshold (L5)**
   are stated as v4 states them (L4 batched review; L5 ship without human intervention; README:90/248/527).
3. **Current authorized level is readable and fail-safe (AC).** A consumer can read the current authorized
   level; an unset/garbled value resolves to the **L4 default (not L5)**; only an explicit operator
   declaration reaches L5. (README:527.)
4. **L4 is the default; L5 is opt-in (AC).** The spec states L4 (PM mode, batched review) as the binding
   default and L5 as opt-in requiring P12 maturity + trust (README:498/527) — so a factory with no explicit
   level set never auto-ships.
5. **Consumer-seam correctness (AC — C39/C53).** C39 can gate its ship-without-review on the level (L5 →
   auto-ship; L4 → batch; below L4 → per-fix gate) by **reading** C56's level (matching C39 I4); C53 can
   gate the bootstrap deploy on the level. C56 supplies the level + boundary; the gate enforcement is the
   consumer's. (C39 §3 contract 4, §5; C53 / README:498.)
6. **G35 split is explicit and routed (AC).** The spec records that C56 owns *which level may auto-ship + the
   L4 default + the F54 audit obligation*; **C43** owns blast radius; **C39** owns the per-fix gate; **C57**
   owns the objective-drift audit register/mechanism — so no consumer over-trusts C56 as an enforcement
   engine, and the F54 audit-pack obligation is discoverable. (G35; F-MODE-COVERAGE §11/§12.)
7. **G15 precondition is documented (AC).** The spec records that sustained L4/L5 assumes the operator can
   author specs fast enough (F-MODE F25) — a documented precondition for raising the level, not a runtime
   mechanism.
8. **No-enforcement-engine check (AC — the bar).** The spec contains **no** central autonomy interceptor;
   every "action blocked" guarantee is attributed to a consumer (C39/C53/C43), confirming C56 is a
   definition/policy artifact. (Reading A, §6.)
(Concrete level-read API/representation, the machine form of the §4.2 table / the `Healer governance | OPA`
predicate, the level-change event schema, and the F54 audit-pack interface are sweep-2 deliverables — and
the audit *mechanism* is C57's / a deferred build.)

## 9. Open questions

- **OQ-1 (→ review-log; G15, top open question):** **Is the one-operator spec-authoring bottleneck a
  precondition C56 merely documents, or does sustained L4/L5 need a design response?** v4's guard is "honest
  staffing / document it" (F-MODE F25) — i.e. C56 documents it as a precondition for raising the level. The
  open question is whether the factory-builds-factory plan (C52) eventually *relieves* the operator
  spec-authoring load (the factory authoring more of its own specs) such that the L4/L5 staffing assumption
  changes — a C52/C56 boundary the docs do not resolve. Routed to C57 (residual register) + review-log.
- **OQ-2 (→ review-log; G11/sweep-2):** **Where does the current authorized level live, and how is it
  read?** v4 names no on-disk form. Faithful fill: a single operator-set value in C03 layered config, read
  at the gated action (so a mid-flight downgrade is honored — C39's downgrade-safe re-read). Confirm the
  representation (a `[autonomy] level` config key vs a dedicated C56 surface) and the read API against the
  real `gc`/C03 shape at sweep-2. *(Shared seam with C39 §3 contract 4 — "config in C03 vs a C56 query".)*
- **OQ-3 (→ review-log; G35):** **Confirm the G35 ownership split and the F54 audit-pack home.** C56's
  disposition: C56 owns *the ladder + which level may auto-ship + the L4 default + the named F54 audit
  obligation*; **C43** owns blast radius; **C39** owns the per-fix ship-gate enforcement (I4); **C57** owns
  the objective-drift **audit register + mechanism** (the F54 audit pack, F-MODE-COVERAGE:178), itself a
  deferred Phase-3+ build. Confirm with C57 (unbuilt — Batch 5) that the audit pack lands there, and that
  C56 is *named* (not depended-on) by C39/C53 as the level source. *(C39 OQ3 is the reciprocal seam.)*
- **OQ-4 (→ review-log; sweep-2):** **Is the L5 promotion gated by anything machine-checkable, or purely an
  operator decision?** README:498 gates L5 on "P12 mature and trusted" — a judgment, not a predicate. Open:
  whether raising to L5 should require a machine-checked precondition (e.g. F54 audit-pack present + green,
  C53 bootstrap validated) or remain a documented operator decision. Faithful sweep-1: operator decision +
  documented checklist; a machine gate is a sweep-2/C57 question.
