# Adversarial review — C41 Identity / actor model & attribution (Track B, sweep 1)

Reviewer persona: Subsystem Adversary (Security & Governance)
Target: spec-optimized/C41-identity-attribution.md (+ plan-optimized/C41-identity-attribution.md)

Track-B mandate: attack the **design** — correctness, hidden coupling, failure handling, cost, simplicity,
scalability, security (esp. lethal-trifecta / isolation gaps), and whether each `[DELTA]` is justified
against concrete forces or is unsupported taste. The seven deltas turn v4's "optional, deferred" signing
into a graduated-mandatory, tamper-evident, keyed identity substrate. The ambition is defensible and the
G36 critique is correct — but the spec **over-claims what is feasible at Phase 0** and **buries a hard
cross-component dependency on C23 that C23 itself has deferred**. Findings ordered by severity.

## Findings

### RC41B-01 — blocker — DELTA-04 (tamper-evident provenance chain "anchored in C23") depends on a C23 capability C23-optimized has explicitly *deferred* (its OQ3)
**Claim.** DELTA-04 and the §3 `verify_chain` / §4.4 provenance-chain make per-actor hash-chaining a
**hard invariant** ("each actor's attributions form an append-only hash chain anchored in C23 … any
retroactive edit/deletion breaks the chain and is detected"). It is presented as closed (G36/F14
"RESOLVED"/"detectable"). But C23-optimized §7 states: *"Tamper-evidence beyond append-only-on-disk (e.g.
hash-chaining records) is a candidate hardening **flagged OQ3**; signed actor provenance is C41's (G36)."*
C23 ships only **append-only-on-disk + non-null `created_by`** — *not* a hash chain. So C41's tamper-
evidence either (a) re-implements a hash chain *on top of* C23 records (C41-owned, not "anchored in C23"),
or (b) assumes a C23 feature C23 has punted. As written, two foundational specs disagree about who owns
tamper-evidence and whether it exists at Phase 0.
**Why it matters.** F14 ("attribution collapse") is marked **detectable/RESOLVED** on the strength of a
chain that may not exist. The whole "verified-not-trusted" claim degrades to "append-only-on-disk," which
a privileged/compromised actor (the F14/F43 threat) can still rewrite if it can edit the JSONL. This is
the same class of over-claim Track B is meant to *fix* in v4, reintroduced one layer down.
**Suggested fix.** Pick one and state it as a delta: **(A)** C41 owns the per-actor hash chain as an
application-level structure over C23's `event_id=(stream,seq)` (C41 computes/stores `prev_provenance_hash`
in the `Attribution` it writes — *this is in fact what §4.2/§4.4 describe*), and explicitly **drop the
"anchored in C23 [tamper-evidence]" framing** so it does not depend on C23-OQ3; OR **(B)** promote C23-OQ3
(record hash-chaining) to a C23 delta and make it a named C41↔C23 contract. Option A is cheaper and keeps
the coupling honest. Either way, file the C41↔C23 tamper-evidence ownership as a cross-component issue
(like XC-1/XC-4 in review-log). **DEFERRED — needs C23 author + integrator** (cross-component, cannot be
fixed in C41 alone).

### RC41B-02 — major — Graduated-mandatory signing at Phase 0 (DELTA-01) is undermined by the unresolved secrets store (G37): `signed`/`attested` assurance is only as strong as plaintext keys in `city.toml`
**Claim.** DELTA-01 makes signing **default-on from Phase 0** for cross-boundary + all Mail; DELTA-06
roots keys in the operator and mints per-actor keypairs at registration. OQ2 honestly concedes private-key
bytes "live in a secrets store that v4 does not yet define (G37)" and that "until then, `signed`/`attested`
assurance is only as strong as plaintext-in-`city.toml` allows." That concession **contradicts** the §6
claim that G36 is **RESOLVED** and the §8 AC2/AC3 that signing is enforced. If keys sit in plaintext
version-controlled config at Phase 0, an attacker who can forge an `asserted` attribution (the F32/F14
threat) can equally read the key and forge a *`signed`* one — the assurance ladder collapses to one rung.
**Why it matters.** The feasibility question in my brief — "is graduated-mandatory signing actually
feasible at Phase 0 under Max?" — turns on this. The *signing mechanism* is feasible (local keys, one
signature/verify, no external service — §7 is right about cost). The *security value* of signing is **not**
realized until G37 is solved, which v4 punts to C03/C43 with no design. So DELTA-01's Phase-0 default-on is
real as a *mechanism* but **premature as a security guarantee**.
**Suggested fix (applied — wording only).** Downgrade §6 "G36 … RESOLVED" to "**RESOLVED as a mechanism;
security-effective only once G37 (key storage) is resolved**" and cross-reference OQ2 from the §6 G36 row
and the §8 AC2/AC3, so the resolved-claim is not read as unconditional. The architectural decision (solve
G37 before claiming signing as a security control) is **DEFERRED to C03/C43/integrator**.

### RC41B-03 — major — DELTA-02 expands the actor taxonomy from v4's 3 kinds to 7 with no scenario forcing five of them; some duplicate C42/C43 concepts
**Claim.** DELTA-02 replaces v4's `{city, rig, agent}` with seven `ActorClass` values:
`human, agent, rig, city, pack, tool_node, external`. Track-B rule 3 requires each deviation be justified
against a concrete force, not taste. Justification is given for `human` (operator overrides, P8) and
`external` (third-party-behind-twin attribution) — both sound. But `pack`, `tool_node` are weakly
motivated: a `pack` is *code*, not an actor that "acts" independently of the agent/tool that runs it, and
`tool_node` overlaps the C02 tool-node ABI and the C42 partition model. Minting keypairs and registry
entries for every `pack`/`tool_node` is registry bloat and a key-management surface (DELTA-06) with no
stated failure mode it retires.
**Why it matters.** Each class is a key to mint/rotate/revoke (DELTA-06) and a row in the policy tier
(DELTA-01/OQ1). Seven classes × the policy-tier matrix is a real operator-comprehension cost (§OQ1 already
flags the tier table as the top open question). Simpler is safer here.
**Suggested fix.** Justify each of the 7 classes against a *named* failure mode/force or collapse the
unmotivated ones. Concretely: keep `{human, agent, rig, city, external}` (5, each with a clear distinct
actor); treat `pack` and `tool_node` as **capability_context / delegation-chain entries** (they already
have `on_behalf_of` and `capability_context` in DELTA-03) rather than first-class keyed actors, unless a
scenario requires a `tool_node` to sign independently of its parent `agent`. **DEFERRED — taxonomy scope
is architecturally significant** (touches DELTA-06 key model + OQ1 policy tier); flagged not applied.

### RC41B-04 — major — the `attested` tier (DELTA-05) assumes an independent co-signer that v4 cannot source (G08/G20 second model family; G34 single-Max-seat)
**Claim.** §4.3 defines `attested` = "`signed` **plus** an independent co-signature (e.g. the rig + the
city, or a **second-family attestor**)" for RSI/L5 auto-ship actions. The "rig + city" co-signature is a
*self*-co-signature (both keys minted by the same operator trust root, DELTA-06) — it proves two keys the
same authority holds both signed, which adds little against a compromised/ drifting authority (the F43/G35
RSI threat the tier is *for*). The genuinely independent variant ("second-family attestor") collides with
G08/G20: v4 has **no second model family and no second provider/key** (Max issues one adapter). So the
strongest tier's independence is either illusory (same trust root) or unsourceable (no second family).
**Why it matters.** `attested` is sold as the control for the *highest-stakes* actions (self-modifying,
L5 auto-ship) — exactly the RSI/goal-subversion class (G35) the corpus calls its weakest. A tier whose
"independence" reduces to two keys held by one authority does not address goal-drift, so F43 is
"strengthened" less than §6 claims.
**Suggested fix (applied — wording only).** Qualify §4.3/§6 so `attested` is described as "two-key /
two-role co-signature **within one trust root** (defense-in-depth against single-key compromise), **not**
independent-family attestation — which is blocked by G08/G20 until a second model family is sourced (C29/
C32)." Cross-reference G35 (RSI) as **not** closed by `attested`. The architectural question (where a
truly-independent attestor comes from) is **DEFERRED to C29/C32/C57**.

### RC41B-05 — minor — G31 "visibility not isolation" framing is honest, but one sentence over-reaches into C43/C44 ownership
**Claim.** The §6 G31 handling is the strongest part of the spec: it explicitly says C41 *cannot* build
twin isolation, that `boundary_class` labelling is "visibility and attributability of the gap, **not a
substitute for the missing isolation**," and defers containment to C43/C44. This is exactly the honest
framing my brief asks for — accept it. **However**, DELTA-07 stamps `boundary_class` "**co-owned with
C43**" and §2 calls it "a *vocabulary* dependency, not a runtime blocker." Co-ownership of a taxonomy
across two specs is the XC-4 failure pattern (two specs disagree on a shared vocabulary). C43-isolation
owns the boundary *taxonomy*; C41 should *consume* it, not *co-own* it, or the enum drifts.
**Why it matters.** If C41 freezes `{production, twin, isolated}` (DELTA-07 / §4.2) before C43 exists
(plan §2 admits C41 proceeds "with a provisional enum and reconcile"), C43 may define a different boundary
taxonomy and the attribution records become inconsistent — the audit (C34 holdout) then queries a stale
enum.
**Suggested fix (applied — wording only).** Changed "co-owned with C43" to "**C41 consumes the
`boundary_class` taxonomy C43 defines; C41 owns only the *stamping* of it on every attribution**," and
noted the provisional-enum reconciliation as a named C41↔C43 freeze (mirrors plan §2). Keeps the (good)
G31 visibility story while removing the co-ownership ambiguity.

### RC41B-06 — minor — DELTA-04 makes history append-only, but the redaction story (OQ3) is unsolved and interacts with compliance — the "tamper = chain break" test will false-positive on legitimate redaction
**Claim.** AC4 (§8) tests that any "edit/delete/reorder" breaks the chain. OQ3 concedes legitimate
redaction (PII/secrets accidentally logged) is *needed* and currently looks identical to tampering. So the
tamper-evidence control, as specified, makes the system **unable to comply with a deletion request without
tripping its own integrity alarm** — a real operability/compliance bug, not just an open question.
**Why it matters.** A governance substrate (C41's self-description) that cannot redact without looking
compromised is a liability the moment a secret is logged. README:222 names "compliance" as a P9 goal.
**Suggested fix.** Specify a tombstone/redaction-with-proof primitive (an attributed, chain-preserving
redaction record) as part of DELTA-04 rather than deferring it wholesale to OQ3, OR explicitly scope C41
to "no redaction in sweep 1; redaction is a known gap that makes tamper-evidence and compliance mutually
exclusive until resolved." **DEFERRED — interacts with C57 residual-risk register + data-retention policy**
(flagged, not applied).

### RC41B-07 — minor — cost/scale claim "cost scales with cross-boundary volume, not total volume" ignores the chain-hash + registry-write on *every* action
**Claim.** §7 says `asserted` is free and cost "scales with cross-boundary action volume, not total
action volume." But DELTA-04 puts a `prev_provenance_hash` (a hash + a per-actor chain-head read/write)
on **every** attribution including `asserted` ones (§4.2 marks `prev_provenance_hash` **required**), and
DELTA-07 stamps `boundary_class` on every action. So there *is* a per-action cost on the hot path that the
"asserted is ~free" line understates — modest, but not zero, and it serializes per-actor (chain-head
contention).
**Suggested fix (applied — wording only).** Corrected §7 to "`asserted` is *cheap* (no signature) but
**not free**: every attribution still writes a `prev_provenance_hash` chain link (DELTA-04) and a
`boundary_class` stamp (DELTA-07); the per-actor chain head is a serialization point sized in sweep 2."

## What I did NOT find wrong (credit where due)
- The G36 critique driving DELTA-01/05 is **correct**: an optional guard does not address F32/F14, and
  graduated-mandatory tiering (cheap `asserted` for intra-rig, `signed` for cross-boundary) is a genuinely
  better design than blanket-optional or blanket-mandatory.
- The G31 "make the exposure window auditable, explicitly not a substitute for isolation" framing is
  honest and is the right thing for C41 to contribute (modulo RC41B-05's co-ownership nit).
- The carrier-vs-resolver split with C19/C23 is clean: C19/C23 carry `created_by`, C41 owns the meaning +
  verification. `attribute`/`verify` signature stability (plan §4) correctly lets Batch-1 ship the
  `asserted` path and upgrade assurance with zero caller churn — a strong plan move.

## Verdict

**needs-rework.** The design direction is right and well-argued, but two load-bearing claims are not
currently sound: **(RC41B-01, blocker)** tamper-evidence is "anchored in C23," yet C23-optimized has
*deferred* record hash-chaining — the two foundational specs must agree who owns the chain before F14 can
be called "detectable"; and **(RC41B-02/04, major)** Phase-0 `signed`/`attested` assurance is over-stated
while G37 (key storage) is unsolved and no independent attestor exists (G08/G20/G34). Applied confident
wording fixes (RC41B-02/04/05/07 qualifications; the §6 over-claims). **Deferred** the architecturally
significant items: RC41B-01 (C23 chain ownership — cross-component), RC41B-03 (7-class taxonomy scope),
RC41B-06 (redaction primitive). **The load-bearing decision the integrator must settle:** whether signing
is mandatory (Track B's DELTA-01) or optional (Track A / v4 README:229) — and, if mandatory, it is *not a
real control until G37 (secrets) and the C23 tamper-evidence ownership (RC41B-01) are also resolved*.
Graduated-mandatory signing is the right call **only if** those two dependencies are pulled forward with it.
