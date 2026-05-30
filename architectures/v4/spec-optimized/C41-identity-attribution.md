# C41 — Identity / actor model & attribution  (Spec, Track B)

> Source: component-inventory.md C41 row (maps A43/A44/A44b/A44c "who/what can act"; A19d attribution-via-events; B50/B51 actor model; A22i rig identity); README Part 4 **P9 — Attribution** (l.220–231: "Every commit, task, event carries actor identity"; Identity model = "Gas City `actor` schema (cities, rigs, agents)" l.226; Action attribution = "beads, events native `created_by` … strongest principle match" l.227; Audit trail = "event bus + bead history" l.228; **Identity verification = "Custom: signature on bead provenance … (optional, deferred)"** l.229), README l.371 ("every bead and event carries `created_by`"), l.497 (`transfused_from` attribution on factory-built components), l.90 ("attribution is automatic"); AI-CONTEXT §1 P9 (l.39 "Every event carries actor identity"), §3.3 vocab (city/rig/agent, l.99–101), §13.3 rig partitions (l.586–597); F-MODE-COVERAGE **F14** (Attribution collapse — "Addressed", P9 native, l.32/146), **F32** (Mail-injection / unsigned coordination — "Addressed" via "P9 attribution + **optional** HMAC signing", l.34 & l.87), **F43** (RSI board-visibility — "Partial", P9 + audit trail, l.75); _meta gaps **G36** (attribution integrity optional/deferred — *assigned*), **G31** (lethal-trifecta isolation unbuilt/last — *cross-cutting, considered here*).
> Inventory ID: C41   Kind: component   Status: sweep-1
> Deltas: DELTA-01 (signed provenance is **graduated-mandatory, not optional/deferred** — closes G36; signature requirement is config-tiered, default-on for cross-boundary/security-relevant actions from Phase 0); DELTA-02 (one canonical `Actor` identity model with a typed `ActorClass` taxonomy — `human`/`agent`/`rig`/`city`/`pack`/`tool-node`/`external` — replacing the loose "cities, rigs, agents" list); DELTA-03 (`created_by` is a structured `Attribution` record, not a bare string — carries `actor_ref` + `on_behalf_of` delegation chain + `capability_context`, so the lethal-trifecta blast-radius question (G31) is *answerable from the attribution record itself*); DELTA-04 (attribution is **append-only and tamper-evident** — every event/bead mutation chains a per-actor provenance hash, so "attribution collapse" F14 is detectable, not merely asserted-addressed); DELTA-05 (identity **verification** is a first-class service `verify(attribution) → Verdict`, with three assurance levels `asserted`/`signed`/`attested`, so consumers choose the bar they need instead of trusting self-assertion); DELTA-06 (the **signing-key / actor-credential model** is specified — keys are per-actor, minted at actor registration, rotated, and the trust root is the human operator — closing the "where do signatures come from" hole G36 leaves open); DELTA-07 (attribution carries a `boundary_class` tag — `production`/`twin`/`isolated` — co-owned with C43, so that even before twin isolation exists (G31's exposure window) every action is *labelled* with the boundary it touched, making the unbuilt-isolation period auditable rather than invisible).

## 1. Purpose & responsibility

C41 is the **identity and attribution substrate**: the single component that defines *who or what can act* in the factory and guarantees that *every action carries a verifiable, tamper-evident record of its actor*. It is README Principle 9 ("Attribution") rendered as a v4 component, and it is **foundational** — it owns the `Actor` model and the `Attribution` record that C19 beads, C23 events, C06 messages, and every control loop embed.

C41's load-bearing transform: **"every commit, task, event, and message is bound to a typed actor, and that binding can be verified — not merely trusted — at a chosen assurance level."** The corpus calls P9 Gas City's "strongest native match" (README l.227, l.231); the *gap* (G36) is that the verification half is "optional, deferred," which makes attribution self-asserted and therefore worthless for the failure modes (F32 mail-injection, F14 attribution collapse, F43 RSI visibility) it is credited with addressing. C41-Track-B's job is to keep the native ergonomics ("attribution flows automatically") while making integrity **real and graduated** rather than optional.

C41 owns:
- **The `Actor` model** — a canonical, typed identity for every actor class that can act: `human`, `agent` (Claude Code worker), `rig` (worker-role partition), `city` (workspace), `pack` (extension code), `tool-node` (subprocess), `external` (a real third-party service behind a twin). One registry, one identity envelope (DELTA-02).
- **The `Attribution` record** — the structured value embedded as `created_by` everywhere (DELTA-03): `actor_ref`, optional `on_behalf_of` delegation chain, `capability_context`, `boundary_class` (DELTA-07), assurance level, and (when signed) the provenance signature.
- **The signing / credential model** — per-actor keys, minted at registration, rooted in the human operator, rotatable (DELTA-06); the mechanism that turns "asserted" into "signed."
- **The verification service** — `verify(attribution) → Verdict` with assurance levels `asserted`/`signed`/`attested` (DELTA-05), so consumers (C06 mail bus, C34 holdout audit, C41's own audit trail) demand the bar they need.
- **The audit-trail query surface** — the queryable, `seq`-ordered, tamper-evident history of who did what (README l.228), built over C19 bead history + C23 event log, with a per-actor provenance chain (DELTA-04).
- **The attribution *policy*** — config-tiered rules (via C03) for *which* actions require which assurance level (e.g., cross-`boundary_class` and mail-bus actions require `signed` from Phase 0; intra-rig task notes may stay `asserted`). This is what makes signing graduated-mandatory rather than blanket-optional (DELTA-01).

What it is **NOT**:
- **Not authorization / access control.** C41 answers *"who acted, provably"* — not *"who is allowed to act."* Capability grants, rig read/write partitions, and the isolation boundary are **C42** (rig partitioning) and **C43** (isolation / lethal-trifecta). C41 *labels* the boundary an action touched (`boundary_class`, DELTA-07) and *attributes* the actor, but it does not enforce the partition. (Clean split: C42 says "the judge rig cannot read the `code` partition"; C41 says "this read was performed by actor `judge-rig-7`, signed, against `boundary_class=isolated`.")
- **Not the bead store or event bus.** C19 owns the work-graph and the `created_by` *field*; C23 owns the append-only action log. C41 owns the *meaning, shape, and verification* of the actor and the attribution record those stores embed. C41 requires `created_by` be non-null (it co-owns that invariant with C19/DELTA-02 there) but does not store the graph.
- **Not the messaging layer.** C06 (Mail + Nudge) carries the messages; C41 supplies the signing/verification C06's "optional HMAC" (G36/F32) is upgraded to use. C41 is the *crypto + identity* C06 calls.
- **Not secrets management.** Credential *storage* (where private keys / OAuth tokens physically live) is the secrets concern G37 raises (C03/C43 territory). C41 defines the *key model and trust root* (DELTA-06) and consumes a secrets store; it does not implement one.
- **Not twin isolation.** C44 builds the twins and C43 the boundary that *contains* blast radius (G31). C41 makes the exposure window *auditable* by tagging every action's `boundary_class`, but it does not isolate anything.

## 2. Context & dependencies

- **Depends on:**
  - **C01** (Gas City substrate) — the `actor` schema is a native Gas City primitive (README l.226); C41 is the v4 spec of that primitive + the registry + the verification/signing layer Gas City does not natively provide.
  - **C19** (bead work-graph) — beads embed the `Attribution` record as `created_by`; C41 reads bead history for the audit trail. Co-foundational: C19's non-null-`created_by` invariant (its DELTA-02) references C41's actor model.
  - **C23** (event bus) — every event carries an `Attribution`; the append-only `seq`-ordered log is one half of the audit trail and the substrate for the tamper-evident provenance chain (DELTA-04).
  - **C03** (config / feature-flags) — the attribution *policy tier* (which actions require `signed`/`attested`) and the signing on/off state are config (DELTA-01). Section presence/value gates assurance requirements.
  - **C43** (isolation boundary) — `boundary_class` taxonomy (DELTA-07): **C43 owns/defines the boundary taxonomy `{production, twin, isolated}`; C41 *consumes* it and owns only the *stamping* of it on every attribution** (RC41B-05 — corrected from "co-owned" to avoid the XC-4 shared-vocabulary-drift pattern). This is a *vocabulary* dependency, not a runtime blocker (C41 can label `production` from Phase 0 even before twins exist — which is the point: it makes G31's exposure window auditable). Until C43 exists, C41 uses a **provisional** enum and reconciles via a named C41↔C43 freeze (plan §2); if C43 defines a different taxonomy, C41's stamped values migrate to match — C41 does not get a vote on the taxonomy, only on stamping it.
- **Consumed by (fan-out — C41 is a Batch-1 cross-cutting load-bearer touching *every* action):**
  - **C19 / C20 / C23** — embed `Attribution`; enforce non-null actor at the write/emit seam.
  - **C06** (messaging) — calls C41 to sign/verify Mail (F32 mail-injection; upgrades the "optional HMAC" to graduated-mandatory signing).
  - **C42** (rig partitioning) — each rig *is* an `Actor` of class `rig`; partition decisions are attributed.
  - **C34** (holdout integrity) — the after-the-fact audit that the judge/implementer did not cross the isolation line *is an attribution query* over `boundary_class` + actor (DELTA-07 makes this answerable).
  - **C35** (override loop) — override beads attributed to the human operator; the "who overrode and why" record (P8) rides C41.
  - **C51** (gene-transfusion) — `transfused_from` provenance (README l.497) is an attribution sub-record on factory-build beads.
  - **C57** (failure-mode coverage / residual-risk register) — F14/F32/F43 status is *derived from* C41's assurance guarantees, not asserted.
  - **bootstrap / audit / compliance** — the queryable history (README l.228) every debug and compliance flow reads.
- **Sits at:** the base of the **Security & Governance** subsystem, cross-cutting into Persistence & Memory. Foundational and *horizontal*: it is not on a single linear path (component-inventory l.129 names it a "cross-cutting load-bearer that touches nearly everything"). Freeze the `Actor` + `Attribution` shapes and the `verify`/`sign` contracts **first** so every other component embeds them from day one.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures, key/signature byte-shapes, and Mermaid sequence/state diagrams in sweep 2).

**Inbound — the Identity Registry API:**
- `register_actor(class, name, parent_ref?) → ActorRef` — mints an actor identity and (DELTA-06) its keypair; `parent_ref` records hierarchy (a `rig` belongs to a `city`; an `agent` runs under a `rig`). Trust-rooted in the operator for top-level actors.
- `resolve(actor_ref) → Actor` / `list_actors(predicate) → [Actor]`.
- `rotate_key(actor_ref) → ()` / `revoke_actor(actor_ref) → ()` — rotation + revocation, with old signatures still verifiable against the historical key (DELTA-06).

**Inbound — the Attribution API (what every writer/emitter calls):**
- `attribute(actor_ref, op_context) → Attribution` — constructs the structured `Attribution` (DELTA-03): binds `actor_ref`, current `on_behalf_of` delegation chain, `capability_context`, `boundary_class` (DELTA-07), and stamps the required assurance level per the active policy tier (DELTA-01). If policy demands `signed`/`attested`, it signs here (DELTA-06).
- `sign(attribution) → SignedAttribution` — produces the provenance signature over the canonical attribution + payload digest.
- `delegate(from_attr, to_actor) → Attribution` — extends the `on_behalf_of` chain (an `agent` acting for a `human`; a `tool-node` acting for an `agent`), so authority provenance is explicit, not flattened.

**Inbound — the Verification API:**
- `verify(attribution, expected_level?) → Verdict` — checks signature validity, key non-revocation, and chain integrity; returns `{level_met: asserted|signed|attested, ok: bool, reason}` (DELTA-05). C06/C34 call this to gate cross-boundary actions.

**Inbound — the Audit API:**
- `audit(predicate) → [AttributedAction]` — queries the `seq`-ordered, tamper-evident history by actor / boundary_class / time / op-type, over C19 history + C23 log (README l.228). This is the F14/F43 and holdout-audit (C34) surface.
- `verify_chain(actor_ref, range) → ChainVerdict` — verifies the per-actor provenance hash chain is unbroken (DELTA-04) — the structural test that "attribution collapse" (F14) has not occurred.

**Outbound:**
- → **C23** every `attribute`/`sign` participates in the append-only event that anchors the provenance chain.
- → **secrets store** (C03/C43 territory) — fetch/store private key material; C41 holds the *model*, not the bytes (G37 boundary).

**Invariants:**
- **Mandatory actor (co-owned with C19):** no bead/event/message is creatable without a resolvable `Attribution.actor_ref` (closes the *presence* half of G36; the structural truth behind README l.227's "strongest match").
- **Graduated-mandatory signing (DELTA-01, closes G36's integrity half):** any action whose policy tier requires `signed`/`attested` is *rejected* if it carries only an `asserted` attribution. Cross-`boundary_class` actions and all C06 Mail are `signed` by default from Phase 0. "Optional" is replaced by "tiered, default-on where it matters."
- **Tamper-evidence (DELTA-04, D-5):** each actor's attributions form an append-only hash chain **owned by C41** and computed over **C23-provided ordered gap-free `event_id`s** (C23 supplies the ordered ids, not the chain); any retroactive edit/deletion breaks the chain and is detected by `verify_chain` (makes F14 *detectable*, not merely "Addressed").
- **Delegation transparency (DELTA-03):** authority is never flattened — an `agent` acting for a `human` carries the full `on_behalf_of` chain, so "who really authorized this" is recoverable (load-bearing for F43 RSI visibility and F32 mail-injection).
- **Boundary labelling (DELTA-07):** every attribution is stamped with the `boundary_class` it touched, *unconditionally and from Phase 0* — even while C43/C44 isolation is unbuilt (G31), so the exposure window is fully audited rather than invisible.
- **Verifiable-not-trusted (DELTA-05):** assurance level is explicit on every attribution; a consumer that needs `signed` never silently accepts `asserted`.

## 4. Data model / state

### 4.1 `Actor` (C41-owned, registry record)

| Field | Req | Notes |
|---|---|---|
| `actor_ref` | yes | Stable, immutable identifier (URN-style: `actor:rig:judge-7`). |
| `class` | yes | ∈ `{human, agent, rig, city, pack, tool_node, external}` (DELTA-02). |
| `name` | yes | Human-readable label. |
| `parent_ref` | — | Hierarchy edge (rig→city, agent→rig); roots at the operator/city. |
| `public_key` | yes* | Verification key; `*` absent only for `asserted`-only actors in a no-signing config (DELTA-01/06). |
| `key_history` | — | Prior public keys, for verifying historical signatures after rotation (DELTA-06). |
| `status` | yes | `active` / `revoked`. |
| `registered_by` | yes | The `Attribution` of whoever registered this actor (trust chain to operator root). |

### 4.2 `Attribution` (C41-owned; embedded as `created_by` everywhere — DELTA-03)

| Field | Req | Notes |
|---|---|---|
| `actor_ref` | yes | Non-null ref into the registry (the mandatory-actor invariant). |
| `on_behalf_of` | — | Ordered delegation chain `[human → agent → tool_node]` (DELTA-03). Empty for direct action. |
| `capability_context` | — | The capability/role under which the actor acted (links to C42; *labels*, does not grant). |
| `boundary_class` | yes | ∈ `{production, twin, isolated}` (DELTA-07, co-owned C43). |
| `assurance` | yes | `asserted` / `signed` / `attested` (DELTA-05). |
| `signature` | cond | Present iff `assurance ≥ signed`; over canonical attribution + payload digest (DELTA-06). |
| `prev_provenance_hash` | yes | Link to the actor's previous attribution → the tamper-evident chain (DELTA-04). |
| `at` | yes | RFC3339 timestamp; `seq` comes from the C23 event it anchors. |

### 4.3 Assurance levels (DELTA-05)

| Level | Meaning | Cost | Default policy tier (DELTA-01) |
|---|---|---|---|
| `asserted` | Actor self-claims; no signature. | ~free | Intra-rig, same-`boundary_class`, non-security ops. |
| `signed` | Provenance signature over payload digest, verifiable against the actor's `public_key`. | one signature/verify | **Default for** cross-`boundary_class` ops, **all C06 Mail** (closes F32), override beads (P8), factory-build provenance. |
| `attested` | `signed` **plus** a second-key/second-role co-signature **within one trust root** (e.g., rig + city) — defense-in-depth against single-key compromise. *Caveat (RC41B-04):* this is **not** independent-family attestation — a truly independent attestor needs a second model family / provider, which v4 cannot source (G08/G20: Max issues one adapter; G34 single seat). So `attested` hardens against single-key compromise but does **not** by itself close RSI goal-drift (G35), which a same-trust-root co-signature cannot detect. | two signatures | Self-modifying / RSI-relevant actions (F43/G35), L5 auto-ship fix-tasks — *with the G35 caveat above*. |

> [DELTA-01] **v4 said:** "Identity verification — verify claimed actor matches actual" is "**optional, deferred**," an "Optional pack" (README l.229); F32 is "Addressed" via "**optional** HMAC signing" (F-MODE l.34). **Change:** signing is **graduated-mandatory** — a config-tiered policy that is **default-on** for cross-boundary and coordination (Mail) actions from Phase 0, escalating to `attested` for self-modifying actions. **Rationale (security):** an *optional* guard does not address a security failure (the exact G36 finding); F32 (mail-injection) and F14 (attribution collapse) are credited as "Addressed" but an opt-out reduces them to "Addressed only if someone remembers to turn it on." Tiering keeps the cheap path cheap (intra-rig notes stay `asserted`) while making the security-relevant path non-bypassable. **Tradeoff:** every cross-boundary action now pays a signature; the policy tier table (C03) is a new config surface operators must understand (OQ1). Phase-0 key bootstrap (DELTA-06) becomes load-bearing earlier than v4's "deferred" implied.

### 4.4 Provenance chain (DELTA-04)

Per actor, attributions form an append-only hash chain: `prev_provenance_hash` links each attribution to that actor's previous one. `verify_chain` walks the chain; a missing/edited/reordered link is a break. This is the structural backing for "Audit trail — queryable history" (README l.228) and the detection mechanism F14 ("attribution collapse") needs to move from *asserted-addressed* to *verified*.

> **Ownership note (RC41B-01 — RESOLVED by D-5):** the integrator's ruling **D-5** ratifies the split:
> **C41 owns the provenance hash-chain**, computed over **C23-provided ordered gap-free `event_id`s**.
> Concretely C41 computes and stores `prev_provenance_hash` in the `Attribution` it writes, keyed on C23's
> `event_id=(stream,seq)` — the chain is a **C41-owned application-level structure over C23 records**. C23
> provides ordered gap-free `event_id`s **only**; it does **not** provide the chain (C23-optimized §7
> correctly defers record-level hash-chaining). With D-5 ratified, F14 is **detectable** via `verify_chain`,
> not merely append-only-on-disk.

> [DELTA-04] **v4 said:** audit trail = "Gas City event bus + bead history" (README l.228) — queryable, but no integrity guarantee; a sufficiently privileged actor (or a compromised one) could rewrite history and attribution would "collapse" silently. **Change:** per-actor tamper-evident hash chain over the existing log. **Rationale (security/failure):** F14 is the failure mode "attribution collapse"; without tamper-evidence the control credited with addressing it cannot *detect* the collapse it is named for. **Tradeoff:** one hash per attribution + a chain-verify pass; history becomes append-only (legitimate redaction needs an explicit tombstone, not deletion — OQ3).

## 5. Behavior

Key flows (Mermaid sequence/state diagrams in sweep 2):

- **Action attribution (the hot path, every write):** actor performs op → caller invokes `attribute(actor_ref, op_context)` → C41 builds the `Attribution`, stamps `boundary_class` (DELTA-07), consults the policy tier (DELTA-01) for required assurance → if `≥ signed`, signs over the payload digest (DELTA-06) → links `prev_provenance_hash` (DELTA-04) → the `Attribution` is embedded as `created_by` in the C19 bead / C23 event. Native-feeling ("flows automatically", README l.231) but now integrity-bearing.
- **Cross-boundary / Mail send (F32):** C06 builds a Mail message → `attribute` with `boundary_class` of the recipient → policy demands `signed` → C41 signs → recipient's C06 calls `verify(attribution, expected_level=signed)` → reject on bad/`asserted`. Mail-injection is structurally blocked, not opt-in (closes F32 properly).
- **Verification at a trust boundary:** consumer calls `verify` / `verify_chain`; gets `{level_met, ok, reason}`; gates the action. C34 holdout audit runs `audit(boundary_class=isolated, actor=judge-rig)` to prove the judge never read `production`/`code`.
- **Actor registration + key bootstrap (DELTA-06):** operator registers the root `city` actor (trust root) → registers child `rig`/`agent` actors, each minted a keypair, `registered_by` chaining back to the operator. Rotation re-keys while `key_history` keeps old signatures verifiable.
- **Delegation (DELTA-03):** a `human` dispatches an `agent`, which spawns a `tool_node` → each step extends `on_behalf_of`, so the final action's attribution names the full authority chain (load-bearing for F43 RSI visibility).
- **Audit / compliance read (P9):** `audit(predicate)` over the `seq`-ordered, chain-verified history → "who did what, under whose authority, against which boundary."

## 6. Failure modes & handling

- **G36 (attribution integrity optional/deferred — RESOLVED AS A MECHANISM; security-effective only once G37 + RC41B-01 resolve):** signing is graduated-mandatory and default-on for security-relevant actions (DELTA-01); verification is a first-class service (DELTA-05); the key model is specified (DELTA-06); history is tamper-evident (DELTA-04). The *presence* of an actor is mandatory (co-owned with C19). Attribution is no longer self-asserted where it matters. **Two load-bearing caveats the integrator must not miss:** (1) *Key storage (G37/OQ2):* `signed`/`attested` assurance is only as strong as where private keys live; at Phase 0, with no v4 secrets store, keys risk sitting in plaintext `city.toml`, which collapses the assurance ladder (an attacker who can read the key can forge a `signed` attribution as easily as an `asserted` one). Signing is **resolved as a mechanism but not security-effective until G37 is solved** (C03/C43). (2) *Tamper-evidence ownership (RC41B-01 — RESOLVED by D-5):* DELTA-04's chain is owned by C41 *over* C23 records — D-5 ratifies that **C41 owns the provenance hash-chain computed over C23-provided ordered gap-free `event_id`s**; C23 provides the ordered `event_id`s only, not the chain. F14 is now detectable via `verify_chain`. Residual: the policy tier defaults are an operator decision (OQ1).
- **G31 (lethal-trifecta isolation unbuilt and last — PARTIALLY ADDRESSED, by design, from C41's side):** C41 cannot build twin isolation (that is C43/C44, and G31's core risk is the *timeline* — isolation arrives in Phase 3c). What C41 *can* and *does* do is make the exposure window **auditable**: every action from Phase 0 carries a `boundary_class` tag (DELTA-07), so the period in which the factory runs Claude Code with Bash/network/fs access against `production` is fully recorded and queryable, not invisible. C57's residual-risk register can then quantify exposure from real attribution data rather than narrative. **Deferred (correctly to C43/C44):** the actual isolation/containment of blast radius. C41's contribution is *visibility and attributability of the gap*, explicitly flagged as not a substitute for the missing isolation.
- **F14 (attribution collapse — now detectable):** tamper-evident per-actor chain (DELTA-04) + `verify_chain`; a rewrite breaks the chain and surfaces.
- **F32 (mail-injection — now structurally addressed):** Mail is `signed` by default (DELTA-01); `verify` gates receipt; the "optional HMAC" becomes non-bypassable signing.
- **F43 (RSI board-visibility — strengthened from Partial):** delegation chain (DELTA-03) + `attested` tier for self-modifying actions (DELTA-01) make "who authorized this self-modification" recoverable; still requires the operator to set the policy tier, so not fully closed here (interacts with G35, owned by C57/C39).
- **Key compromise / lost key:** `rotate_key` + `revoke_actor` with `key_history` so historical signatures remain verifiable while new ones use the fresh key; a revoked actor's future attributions fail `verify`.
- **Unattributable legacy/external action:** an `external` actor class (DELTA-02) gives third-party-service actions (behind a twin) a place in the model rather than an unattributed hole.

## 7. Cross-cutting

- **Security / governance:** C41 *is* the governance substrate — verifiable attribution + tamper-evident audit + graduated signing. It deliberately stays out of *authorization* (C42/C43) to keep the "who acted, provably" concern clean and reusable. The `attested` tier gives the highest-risk actions (RSI/L5 auto-ship) a stronger bar without taxing routine work.
- **Cost / scale:** `asserted` is **cheap but not free** (RC41B-07): it carries no signature, but *every* attribution — including `asserted` — still writes a `prev_provenance_hash` chain link (DELTA-04, `prev_provenance_hash` is required in §4.2) and a `boundary_class` stamp (DELTA-07), and the per-actor chain head is a **serialization point** that must be sized in sweep 2. `signed` is one signature/verify (cross-boundary only); `attested` (two signatures) is reserved for rare high-stakes actions. The signature/verify cost (not the chain hash) scales with cross-boundary action volume, not total volume — a deliberate tiering choice; the chain-link + boundary-stamp cost is per-action and on the hot path.
- **Observability:** attribution *is* observability's actor dimension — every C23 event and CXDB trajectory inherits a verifiable actor + boundary tag, enriching the self-heal feed (C24/C37) with "who/where," not just "what."
- **Operability:** the registry + key bootstrap (DELTA-06) is the one new operational surface; rotation/revocation are standard. The policy tier (C03) is declarative. Freeze `Actor`/`Attribution`/`verify`/`sign` first (DELTA index) so the whole system embeds them uniformly.

## 8. Acceptance criteria & test strategy

1. **Mandatory actor (G36 presence):** any bead/event/message with null/unresolvable `actor_ref` is rejected at the write/emit seam. (Golden negative test, shared with C19/C23.)
2. **Graduated-mandatory signing (DELTA-01 / G36 integrity):** a cross-`boundary_class` action or a C06 Mail carrying only `asserted` is rejected under the default policy tier; the same action with a valid `signed` attribution passes. (Policy-tier conformance test.) *Note (RC41B-02):* this proves the *mechanism* (rejection of under-signed actions); it does **not** prove the *security value*, which is contingent on key storage (G37/OQ2) — a separate test once a secrets store exists confirms keys are not forgeable by an actor that can already forge an `asserted` attribution.
3. **Signature validity + verification levels (DELTA-05):** `verify` returns `ok` only for a signature that checks against the actor's (current or historical) public key; `verify(expected_level=signed)` fails an `asserted` attribution. (Crypto + level test.)
4. **Tamper-evidence (DELTA-04 / F14):** edit/delete/reorder an actor's historical attribution → `verify_chain` reports a break at the right link. (Tamper-injection test.)
5. **Delegation chain (DELTA-03 / F43):** an `agent` acting for a `human` through a `tool_node` yields an attribution whose `on_behalf_of` names all three in order. (Integration test.)
6. **Boundary labelling from Phase 0 (DELTA-07 / G31):** every action — *before any twin/isolation exists* — carries a `boundary_class`; `audit(boundary_class=production)` enumerates exactly the exposure-window actions. (Audit-coverage test against a Phase-0 install.)
7. **Key lifecycle (DELTA-06):** after `rotate_key`, new actions sign with the new key and old signatures still verify via `key_history`; after `revoke_actor`, new attributions fail `verify`. (Lifecycle test.)
8. **Holdout audit answerability (C34 consumer):** `audit(actor=judge-rig, boundary_class=isolated)` proves the judge never touched `production`/`code` — the after-the-fact isolation check is a pure attribution query. (Cross-component contract test with C34.)
9. **Native ergonomics preserved:** the common `attribute` call requires no per-call ceremony (policy + signing are automatic), preserving README l.231 "flows automatically without configuration" for the `asserted` path. (Ergonomics/contract test.)

## 9. Open questions

- **OQ1 (→ review-log):** **Default policy-tier table.** Exactly which `(class, boundary_class, op_type)` combinations require `signed` vs `attested` at Phase 0? Proposed default: all cross-`boundary_class` + all C06 Mail + override beads = `signed`; self-modifying / L5-auto-ship = `attested`; everything else = `asserted`. The defaults are a security-posture decision the operator owns (DELTA-01) and they set how much of G36 is actually closed in practice. *Top open question.*
- **OQ2 (→ review-log):** **Key-storage / trust-root boundary with G37.** C41 specifies the key *model* and trust root (operator), but private-key bytes live in a secrets store that v4 does not yet define (G37: "secrets/credential handling is absent"). The C41↔secrets-store seam (HSM? OS keychain? sealed file?) must be pinned with C03/C43; until then, `signed`/`attested` assurance is only as strong as plaintext-in-`city.toml` allows.
- **OQ3 (→ review-log):** **Append-only history vs legitimate redaction.** Tamper-evidence (DELTA-04) makes history append-only, but compliance sometimes requires redaction (PII, secrets accidentally logged). A tombstone/redaction-with-proof mechanism is needed so redaction is *attributable and chain-preserving* rather than a silent edit that looks like tampering. Interacts with C57's residual-risk register and any future data-retention policy.
