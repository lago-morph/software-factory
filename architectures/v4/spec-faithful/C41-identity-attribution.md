# C41 — Identity / actor model & attribution  (Spec, Track A)

> Source: README Part 4 **P9 — Attribution** (lines 220–231: "Every commit, task, event carries actor identity. Foundation for debug, compliance, trust"; the 4-row component table — Identity model = "Gas City `actor` schema (cities, rigs, agents)"; Action attribution = "Gas City beads, events native `created_by`" / "strongest principle match"; Audit trail = "Gas City event bus + bead history"; Identity verification = "Custom: signature on bead provenance" / "**optional, deferred**"); README:90 ("attribution is automatic"); README:371 ("P9 (attribution): native; every bead and event carries `created_by`"); AI-CONTEXT §3.1 row 9 ("**Strongest match in entire corpus** — automatic everywhere"); AI-CONTEXT §3.2 ("nine concepts" #1 Session → P9, #2 Bead Store → P9, #3 Event Bus → P9, #6 Messaging → P9); AI-CONTEXT §3.3 vocabulary table (city = workspace, rig = agent worker role); AI-CONTEXT §13.3 rig-partition skeleton (`[[rig]]` blocks); F-MODE-COVERAGE §2 (F14 "Attribution collapse" → "every bead, event, action carries actor"; F32 "Mail-injection / unsigned coordination" → "P9 attribution + optional HMAC signing layer"), §6 (F43 "RSI Board-Visibility Gap" → "P9 attribution + audit trail + bead history"), §7 (F32 revisit → "HMAC signing on mail bus"); component-inventory C41 row (maps `A43, A44, A44b, A44c, A19d, B50, B51, A22i`; depends on C01, C19, C23; gap G36; foundational: yes; critical-path note: "cross-cutting load-bearer that touches nearly everything … every action"); ambiguities-and-gaps **G36** (minor — "Attribution integrity is optional/deferred … without signed provenance, attribution is *self-asserted* … an optional guard does not address a security failure").
> Inventory ID: C41   Kind: component   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C41 is the **identity / actor model and attribution layer** of the factory. It answers two questions
for every action in the system: **"who or what acted?"** (the actor model — cities, rigs, agents) and
**"is that recorded on the action?"** (attribution — `created_by` on every bead and event). It is P9 in
the principle taxonomy, which README and AI-CONTEXT both name **the single strongest native match in the
entire corpus** — attribution flows automatically through Gas City beads and events without
configuration (README:231; AI-CONTEXT §3.1 row 9).

C41 exists as a *named component* (not just "a field") because three things must be defined for
attribution to be load-bearing rather than incidental: (1) the **actor vocabulary** — the closed set of
actor kinds (city, rig, agent) that may legitimately appear in a `created_by`; (2) the **universality
invariant** — that *every* state-changing action carries a `created_by`, with no unattributed path; and
(3) the **audit trail** — that the union of bead history (C19) and the event bus (C23) is a queryable,
append-only record of who did what. The optional fourth piece — **identity *verification*** (signed
provenance proving the claimed actor is the actual actor) — v4 marks "optional, deferred" (README:229),
so C41 *defines the seam* for it but does not require it (gap G36; see §6).

**Responsibilities**
- Define the **actor model**: the actor kinds v4 names — **city** (workspace), **rig** (agent worker
  role), **agent** (the acting worker/judge/scenario role) — and how an actor is identified
  (README:226 "Gas City `actor` schema (cities, rigs, agents)"; AI-CONTEXT §3.3 city/rig vocabulary).
- Own the **`created_by` attribution semantics**: what a `created_by` value *is* (a reference to an actor
  in the actor model), so that C19 (beads) and C23 (events) — which merely *carry* the field — resolve to
  a defined actor (README:227 "native `created_by`"; component-inventory: beads/events carry `created_by`,
  verification deferred to C41).
- Assert the **universal-attribution invariant**: every action that writes a bead (C19/C20) or emits an
  event (C23) carries a `created_by`; there is no unattributed write path (README:222 "Every commit,
  task, event carries actor identity"; F14 "Addressed").
- Define the **audit trail** as the queryable union of **bead history** (C19) and the **append-only event
  bus** (C23) keyed by actor (README:228 "Audit trail — Gas City event bus + bead history").
- Define the **provenance-verification seam** (the *optional* signed-provenance pack): the place a
  signature over a bead/event's provenance would attach, what it would cover, and how a verifier would
  check it — **named and described, not required** (README:229 "Custom: signature on bead provenance …
  optional, deferred"; G36). The HMAC-mail-signing variant referenced for F32 attaches at this seam
  (F-MODE-COVERAGE §2/§7), though the mail bus itself is C06.

**Explicitly NOT**
- NOT the bead store (C19) or the bead schema (C20). C19 owns persistence and the `gc bd` graph; C20
  declares `created_by` as a required *envelope field*. C41 owns the **meaning** of that field — the
  actor it points at and the verification (or non-verification) of the claim. (C20 §1 states the same
  boundary in reverse: "C41 owns *who can act* and the `created_by` provenance semantics; C20 merely
  declares `created_by`".)
- NOT the event bus (C23). C23 is the append-only JSONL transport that *records* every action; C41
  defines that each such record carries a resolvable actor and that the bus + bead history *form* the
  audit trail. C41 ≠ C23 (inventory lists both as distinct foundational rows; C41 depends on C23).
- NOT **authorization / partitioning** (C42) or the **isolation boundary** (C43). C41 says *who acted*;
  it does **not** decide *what an actor is allowed to do*. Read/write partitions across worker/scenario/
  judge rigs are C42; the lethal-trifecta boundary is C43. C41 supplies the identity those policies are
  written against; it does not enforce them. (Inventory: C42 = "Worker/scenario/judge roles with read/
  write partitions"; C43 = "isolation & lethal-trifecta boundary".)
- NOT secrets / credential management (G37). OAuth tokens, mTLS certs, judge-provider credentials live in
  config (C03) / env; C41 does not store or rotate them. G37 is assigned to C03/C43, not C41.
- NOT a **mandatory cryptographic provenance** system. v4 marks identity verification "optional,
  deferred" (README:229). Track-A faithfulness forbids C41 from *requiring* signed provenance; it defines
  the seam and flags the residual risk (G36).
- NOT the messaging bus (C06). C06 owns Mail/Nudge and the *optional HMAC signing* of mail; C41 owns the
  identity that signing would bind to. (Inventory: C06 carries gap G36 too — the HMAC seam — but the
  signing layer attaches at C41's provenance seam.)

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | The `actor` schema, `created_by`, beads, and the event bus are all Gas City native (README:226–228; AI-CONTEXT §3.2). C41 elaborates Gas City's actor model; it does not build a new one. Inventory: C41 `depends on C01`. |
| Upstream (depends on) | **C19** Bead store / work-graph | Beads carry `created_by`; bead *history* is half the audit trail. C41 defines what that field resolves to. Inventory: C41 `depends on C19`. |
| Upstream (depends on) | **C23** Event bus | Append-only JSONL records every action with `created_by`; the bus is the other half of the audit trail (README:228). Inventory: C41 `depends on C23`. |
| Sibling (field declarer) | **C20** Bead schema registry | C20 declares `created_by` as a required envelope field on every bead; C41 supplies its meaning + verification seam. (C20 §1 / §6 cross-reference.) |
| Downstream (consumes identity) | **C42** Rig / agent-role partitioning | Writes read/write authorization policy *against* C41's actor identities (worker vs scenario vs judge rig). C41 supplies the subject; C42 supplies the policy. |
| Downstream (consumes identity) | **C43** Isolation & lethal-trifecta boundary | Boundary typing is written against actor identity; C41 supplies the "who". |
| Downstream (consumes the seam) | **C06** Messaging (Mail + Nudge) | Optional HMAC mail signing (F32) binds a message to a C41 actor via the provenance seam. Inventory: C06 gap G36. |
| Downstream (consumes audit trail) | **C35** Override→pattern→rule loop; **C46** meta-metrics; RSI visibility (F43) | Override beads, meta-metrics, and RSI-status declarations all read the actor-keyed audit trail (F43: "P9 attribution + audit trail + bead history"). |

C41 is **foundational** (inventory: yes) and in **Batch 1** (authored in parallel with C01/C19/C20/C23).
The inventory's critical-path note names C41 a **cross-cutting load-bearer that "touches nearly
everything but is not on a single linear path … every action."** It is load-bearing because the
universal-attribution invariant is a precondition for F14 (attribution collapse), F32 (unsigned
coordination), and F43 (RSI board-visibility) all being marked Addressed.

## 3. Interfaces / contracts

Sweep 1 — interfaces named and described (concrete actor-id grammar, signature format, and verification
API deferred to sweep 2).

1. **Actor model / actor-reference contract** — the closed vocabulary of actor *kinds* (`city`, `rig`,
   `agent`) and the shape of an *actor reference* that a `created_by` resolves to. Any component reading a
   `created_by` can resolve it to (kind, identifier) against this contract.
2. **`created_by` attribution contract** — the guarantee that every bead (via C20 envelope) and every
   event (via C23 record) carries a `created_by` whose value is a valid actor reference. This is the
   contract C19/C20/C23 rely on and that downstream auditors trust.
3. **Audit-trail query contract** — the named ability to ask "what did actor X do?" / "who created bead/
   event Y?" by reading the union of bead history (C19) + event bus (C23), keyed by actor. (The concrete
   query surface — `gc bd` filters + event-bus scan — is C19/C23's; C41 defines that it is *answerable by
   actor*.)
4. **Provenance-verification seam (optional)** — the *named, optional* interface where a signature over a
   bead/event's provenance attaches and is checked: what bytes the signature covers (the actor reference +
   the action's identifying content), where the signature is stored, and the verify operation
   (`actor-claimed == actor-signed`). Marked optional/deferred per README:229; see the G36 AMBIGUITY block
   in §6. The HMAC-mail-signing layer (F32) is one instantiation of this seam (a shared symmetric key);
   the bead-provenance-signature variant (README:229) is another (per-actor signing key).

**Invariants**
- **Universal attribution**: no state-changing action (bead write, event emit) exists without a
  `created_by` resolving to a valid actor. An unattributed write is invalid (this *is* F14 "Addressed";
  README:222).
- **Actor-kind closure**: every `created_by` resolves to one of the v4-named kinds (city / rig / agent);
  an actor of unknown kind is invalid. (> [FAITHFUL-FILL] — see §4.)
- **Append-only audit**: the audit trail (event bus + bead history) is append-only; attribution records
  are never rewritten (C23 is "append-only JSONL with monotonic seq" — AI-CONTEXT §3.2 #3). This is what
  makes the trail trustworthy for F43.
- **Self-asserted by default**: absent the optional verification pack, `created_by` is the actor's *own
  claim*, not a proven identity (README:229; G36). C41 records this as a stated invariant so downstream
  components do not over-trust attribution (see §6/§7).

## 4. Data model / state

C41 owns the **actor model and the attribution semantics**, not the stores. Bead instances live in C19;
event records live in C23. C41 defines what the `created_by` *on* those records means.

### 4.1 Actor reference (the value of `created_by`)

| Field | Meaning | v4 source |
|---|---|---|
| actor *kind* | one of `city` / `rig` / `agent` | README:226 ("cities, rigs, agents"); AI-CONTEXT §3.3 (city, rig) |
| actor *identifier* | the specific actor of that kind (e.g. the rig name from a `[[rig]]` block; the agent name) | AI-CONTEXT §13.3 `[[rig]]` blocks; §3.4 `[[agent]]` |
| (optional) *signature* | signed provenance binding the reference to the action — present only with the optional verification pack | README:229; F-MODE-COVERAGE §2/§7 |

> [FAITHFUL-FILL] **Actor-kind set = exactly {city, rig, agent}.** v4 names "cities, rigs, agents"
> verbatim as the Gas City `actor` schema (README:226); the `agent` kind is sourced from README:226 +
> §3.4 `[[agent]]` blocks (RC41A-01 — *not* from §3.3, which glosses only city/rig and ambiguously maps
> rig = "agent worker role"). The minimal faithful choice is to treat that
> triple as the *closed* kind set, because v4 never names a fourth actor kind and the universal-attribution
> invariant requires a *closed* set for "actor of unknown kind is invalid" to be well-defined. Whether
> the *human operator* is modeled as an `agent`, a distinct kind, or sits outside the actor model entirely
> is a real open question (overrides are operator actions — README P8) — flagged as OQ-C41-2; the smallest
> faithful reading is that the operator acts *through* an agent/rig and is attributed as such, since v4
> gives no fourth kind. Concrete identifier grammar deferred to sweep 2.

> [FAITHFUL-FILL] **Actor reference is (minimal faithful reading) a (kind, identifier) pair, not a flat
> string — pending C19/C23 ratification (OQ-C41-4).** v4 stores `created_by` as a field but never gives
> its internal shape. The smallest consistent elaboration that lets a reader "resolve to a valid actor"
> (§3 contract) is a structured (kind, identifier) reference rather than an opaque string, because the
> actor *kinds* are explicitly enumerated and partitioning (C42) is written against kind
> (worker/scenario/judge rigs). This does not add a store — it only structures an existing field.
> *Honesty caveat (RC41A-04):* C19/C23 faithful specs currently treat `created_by` as an **opaque carried
> value** and have not ratified this structure; if they ship a flat string, this fill is over-reach. The
> flat-string-vs-structured choice is the joint freeze OQ-C41-4 (plan M1). Wire encoding deferred to sweep 2.

### 4.2 Audit trail (derived, not owned)

The audit trail is **not new state** — it is the *actor-keyed view* over two stores C41 depends on:

```
audit-trail(actor X) ≡ { beads in C19 where created_by == X (+ bead history) }
                      ∪ { events in C23 where created_by == X }
```

C41 owns the *definition* (it is keyed by actor and append-only); C19 and C23 own the bytes. This is
README:228's "Audit trail — Gas City event bus + bead history". No separate audit store is introduced
(faithful: v4 names none).

### 4.3 Provenance signature (optional, deferred)

When the optional verification pack is installed, a signature attaches to a bead/event's provenance. v4
specifies only "signature on bead provenance" (README:229) and "HMAC signing on mail bus" (F-MODE §7).
C41 (sweep 1) defines *where it attaches and what it covers* (the actor reference + the action's
identifying content) but **not** the algorithm, key model, or rotation — those are sweep-2/sweep-3 of the
*optional pack*, and v4 marks the whole thing deferred (see §6 AMBIGUITY).

### 4.4 Persistence & consistency

C41 holds **no instance state of its own**. The actor model is a *definition* (like C20's registry); the
attribution values live on C19 beads and C23 events. C41's only consistency requirement is
**resolvability**: every `created_by` written by C19/C23 must resolve to a valid actor under the C41
actor model (otherwise F14 attribution-collapse re-opens). The actor *registry* (the enumeration of
which concrete rigs/agents exist) is sourced from Gas City config — `[[rig]]` / `[[agent]]` blocks in
`city.toml` (AI-CONTEXT §3.4, §13.3) — so C41 does not own a separate actor database (faithful: v4 names
none).

## 5. Behavior

C41 has no control loop; its behavior is **definitional**, **stamp-time**, and (optionally)
**verify-time**:

- **Definition-time**: declares the actor model (kinds + reference shape) and the universal-attribution
  invariant.
- **Stamp-time**: when any component writes a bead (C19/C20) or emits an event (C23), the substrate
  stamps `created_by` with the acting actor's reference. In faithful v4 this is **automatic** — README:231
  ("Attribution flows automatically … without configuration") and AI-CONTEXT §3.1 ("automatic
  everywhere"). C41's role is to guarantee the stamp is present and well-formed, not to perform the write.
- **Audit-time**: a reader (C35 override surfacing, F43 RSI visibility, meta-metrics C46, or an operator)
  queries the actor-keyed union of bead history + event bus.
- **Verify-time (optional)**: if the verification pack is installed, a verifier checks the provenance
  signature against the claimed actor (`actor-claimed == actor-signed`) and rejects/flags a mismatch.
  Absent the pack, this step is skipped and attribution is self-asserted (G36).

(Sequence diagrams for the stamp→audit flow and the optional verify path are deferred to sweep 2 per
BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C41 (faithful) |
|---|---|---|
| **F14** Attribution collapse (F-MODE §2, "Addressed") | The core mode C41 prevents: actions losing their actor. | **Addressed conditional on OQ-C41-3** at sweep-1 altitude by the universal-attribution invariant (§3): every bead/event carries a `created_by` resolving to a valid actor; an unattributed write is invalid. This is v4's "strongest principle match" (README:231). *Caveat (RC41A-03, aligns spec with plan §5 risk 1):* the "unattributed write is invalid" guarantee is firm only if Gas City *rejects* (not merely *defaults*) an unattributed write — an unverified G11-class assumption (OQ-C41-3). If the substrate only defaults the field, F14 is discipline-dependent, not enforced. Retire OQ-C41-3 (plan T7) before declaring F14 unconditionally Addressed. |
| **F32** Mail-injection / unsigned coordination (F-MODE §2 + §7) | Unsigned inter-agent mail can be spoofed; the guard is "optional HMAC signing." | **Addressed-on-paper-only** in the faithful reading: C41 defines the provenance-verification *seam* the HMAC layer attaches at (§3 #4, §4.3), but the signing is **optional** (G36). *Fidelity divergence (RC41A-02):* F-MODE-COVERAGE §2/§7 marks F32 **"Addressed"**, but that status is **not faithfully supportable** under C41's optional-signing reading — an optional guard "does not address a security failure" (G36). Per Track-A rule 3 this divergence is recorded (not silently resolved) and routed to C57 (F-mode owner) as a residual-risk flag; the architecture stays optional. The mail bus itself is C06; C41 supplies the actor identity the signature binds. Residual risk flagged below + §9. |
| **F43** RSI Board-Visibility Gap (F-MODE §6, "Partial") | Need an audit trail to see what self-modifying components did. | **Partially addressed**: C41's actor-keyed audit trail (event bus + bead history, §4.2) is exactly the "P9 attribution + audit trail + bead history" mechanism. The *declaration discipline* (pack-author declares RSI status in `pack.toml`) is operator-required and out of C41's scope (it's a pack-governance concern). |
| **G36** Attribution integrity is optional/deferred (minor) | Without signed provenance, `created_by` is self-asserted; F32's guard is "optional," which "does not address a security failure." | See the AMBIGUITY block below. Faithful resolution: C41 **defines** the verification seam and **requires** universal *self-asserted* attribution, but does **not require** verification (v4 marks it deferred). The gap is acknowledged + surfaced as residual risk, not closed. |

> [AMBIGUITY: G36] **Is signed provenance required for attribution to be load-bearing, or genuinely
> optional?**
> Reading A (faithful-literal — optional): README:229 explicitly lists Identity verification as
> "**optional, deferred**" with placement "Optional pack," and F32's guard is "**optional** HMAC signing"
> (F-MODE §2). On this reading C41 must NOT require signatures; attribution is self-asserted and that is
> the intended v4 posture. The whole P9 section's claim to "strongest match" rests on `created_by`
> *presence*, not *verification*.
> Reading B (security-consistent — should be required): the Skeptic's G36 finding (minor) argues an
> *optional* guard "does not address a security failure" — F32 is marked **Addressed** on the strength of
> a guard that may not be installed. On a self-modifying factory (F43/RSI), self-asserted attribution lets
> a compromised or drifting actor forge `created_by`. A truly load-bearing audit trail would require
> verification.
> **Pick: Reading A for the *requirement*, with Reading B surfaced as named residual risk.** Track-A
> faithfulness is binding: v4 says "optional, deferred" in plain words (README:229), so C41 **cannot make
> verification mandatory** without an architectural change (forbidden in Track A). The smallest faithful
> choice is to (1) require *self-asserted* universal attribution (which v4 does mandate — "every action
> carries identity"), (2) fully **specify the verification seam** so the optional pack can be added without
> rework, and (3) record the "self-asserted by default" invariant (§3) and the F32/F43 residual risk
> (§7, §9) so no downstream component over-trusts attribution. Making verification *mandatory* is exactly
> the kind of improvement Track B would propose as a `[DELTA]`; in Track A it is an open question routed to
> review-log (OQ-C41-1), not a decision C41 may take.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the central concern).** Attribution is **self-asserted by default** (README:229; G36).
  C41 guarantees *presence and well-formedness* of `created_by`, not its *truth*. This is sufficient for
  F14 (an action cannot be unattributed) but **not** for adversarial integrity (a malicious actor can
  claim another's identity absent the optional signature). The seam for closing this — signed bead
  provenance / HMAC mail signing — is defined (§4.3) but unbuilt by default. This residual risk is the
  load-bearing caveat on P9's "strongest match" claim and is surfaced to F-mode coverage (F32, F43) and
  the review-log (§9).
- **Cost.** Self-asserted attribution is *free* — it is a stamped field on writes that already happen
  (README:231 "without configuration"). The optional verification pack adds signing/verify cost (key
  management + per-action signature); v4 defers it, so the default-path cost is zero.
- **Scale.** No new store; the audit trail is a *view* over C19/C23, which carry their own scale story.
  C41 adds no scale concern beyond keeping the actor-kind set closed and small.
- **Observability.** Attribution *is* observability's foundation — the `created_by`-keyed audit trail is
  what makes "who did what, when" answerable (README:222 "Foundation for debug, compliance, trust"). C41's
  invariants are what let C35 (override surfacing), C46 (meta-metrics), and F43 (RSI visibility) attribute
  behavior to actors.
- **Ops.** The actor registry is sourced from `city.toml` `[[rig]]`/`[[agent]]` blocks (AI-CONTEXT §3.4,
  §13.3) under normal git review; C41 adds no separate operational surface. Enabling verification later is
  a pack install at the defined seam (§4.3) — additive, not a migration. *Caveat (RC41A-06):* the
  "additive later" property is **contingent on G37 (secrets/credential handling) being resolved first** —
  the optional pack needs somewhere for a signing key to live, and faithful v4 supplies no secrets store
  (G37 is an open gap assigned to C03/C43). The cheap-seam claim should not be oversold while G37 is open.

## 8. Acceptance criteria & test strategy

1. **Universal attribution (F14 closed)**: every bead write (C19/C20) and event emit (C23) produces a
   record with a non-empty `created_by`; a write path that omits it is rejected/invalid. No unattributed
   action exists.
2. **Actor resolvability**: every `created_by` resolves to a (kind, identifier) under the C41 actor model,
   with kind ∈ {city, rig, agent}; an unknown-kind actor is invalid.
3. **Audit trail answerable by actor**: given an actor X, the union of bead history (C19) + event-bus
   records (C23) keyed by `created_by == X` returns X's actions; given a bead/event Y, its creating actor
   is recoverable (README:228).
4. **Append-only integrity**: attribution records in the audit trail are never rewritten (C23
   append-only; bead history immutable-by-convention) — a test attempting to alter a past `created_by`
   must not silently succeed.
5. **Verification seam present (optional path)**: with the optional verification pack installed, a
   signature over (actor reference + action content) is attachable and a verifier rejects a forged
   `created_by` (`actor-claimed ≠ actor-signed`); **without** the pack, this test is N/A and attribution
   is self-asserted (faithful to README:229). The *default* acceptance run does NOT require verification.
6. **Self-asserted caveat is explicit**: downstream components that read attribution (C35, C42, C46,
   F43 consumers) can discover whether the current install verifies provenance, so they do not over-trust
   a self-asserted `created_by`.
(Concrete actor-id grammar, signature byte-layout, the verify API, and forged-attribution test vectors
are sweep-2 deliverables — and for the verification path, are deliverables of the *optional pack*, not
the default build.)

## 9. Open questions

- **OQ-C41-1** (→ review-log): **Should provenance verification be mandatory? (G36).** v4 says
  "optional, deferred" (README:229), so Track-A C41 leaves it optional and defines the seam (§6 AMBIGUITY).
  But the Skeptic's G36 finding argues an optional guard does not address F32/F43 on a self-modifying
  factory. This is the **top open question**: it is the load-bearing security decision and is precisely a
  Track-B `[DELTA]` candidate (make signing mandatory at the F32/F43 surface). Track A cannot decide it
  without an architectural change; route to review-log for the cross-track reconciler.
- **OQ-C41-2** (→ review-log): **Is the human operator a fourth actor kind?** v4 names only city/rig/agent
  (README:226), yet operator *overrides* are first-class actions (README P8 override-log row, README:214
  "beads with type `override`") and must be attributed. The
  faithful fill (§4.1) models the operator as acting *through* an agent/rig. Confirm against C42 (which
  partitions worker/scenario/judge roles — none of which is obviously "operator") whether a distinct
  `operator`/`human` actor kind is needed, or whether operator overrides are attributed to an agent acting
  on the operator's behalf.
- **OQ-C41-3** (→ review-log): **Does Gas City actually enforce universal `created_by`, or is it
  convention?** README/AI-CONTEXT assert attribution is "automatic everywhere," but Gas City's real
  behavior is asserted-not-run (G11-class). Confirm whether the substrate *rejects* an unattributed write
  or merely defaults the field — this determines whether the F14 invariant is enforced or
  discipline-dependent (and bears on OQ-C41-1).
- **OQ-C41-4** (→ review-log): **Actor reference encoding boundary with C20/C23.** C41 says `created_by`
  is a (kind, identifier) reference (§4.1 fill); C20 declares it as an envelope field and C23 records it
  on events. Confirm a single shared encoding so beads and events use the *same* actor-reference shape
  (else the audit-trail union in §4.2 cannot key cleanly across both stores).
