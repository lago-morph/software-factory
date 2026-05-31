# Adversarial review — C27 LangFuse trace store & browser (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Observability (C27)
Target: spec/C27-langfuse-traces.md  +  plan-faithful/C27-langfuse-traces.md
Charter: Track A → attack FIDELITY and COMPLETENESS only, not the design. PLUS the
capability-for-principle bar (HANDOFF §2): flag any addition that hardens existing stack
capability rather than delivering new principle-tied capability. THE BAR for C27: it IS
off-the-shelf self-hosted LangFuse (deploy + config, not custom code).

> **Re-review note (supersedes the prior pass on disk).** A previous review of this component tagged
> its fixes "(applied)" but **none of those edits were present in the spec/plan on disk** — the docs
> were still the original builder text. This pass re-derives the findings, **grounds the LangFuse OTLP
> facts against the LangFuse docs (verified 2026‑05‑31)**, **corrects one fidelity miss the prior pass
> blessed** (the G37→FE-3 cross-reference — RC27-06), and **actually applies** the confident fixes.

## Findings

### RC27-01 — major — RESOLVED by D-11 — C26↔C27 ingestion seam is INCONSISTENT on the *signal set*: C26 pipelines metrics + logs/events + traces into LangFuse's OTLP endpoint, but LangFuse ingests TRACES ONLY.

> **RESOLVED by D-11 (integrator pass 2026-05-31).** LangFuse ingests **traces only** (verified vs LangFuse OTel docs). C27 already stated traces-only; C26 §3.3/AC-5/§5/OQ-1 were updated to match — metrics/events forwarded best-effort or not routed, **not asserted in LangFuse**, **never** to CXDB. Seam transport = OTLP/HTTP + HTTP Basic auth (base64 `public:secret`); path/headers remain sweep-2.
**Claim.** C27 §3.1 says its inbound payload is "OTLP **traces**" and OQ-1 only *hedges* that
"non-trace OTLP signals (metrics/events) may not be browsable there." The upstream C26 spec (§3.3
pipeline table + §8 AC-5) unconditionally routes **three** pipelines — metrics, logs/events, AND beta
traces — all into the single LangFuse OTLP exporter, and C26 §3.2 asserts "**every** signal accepted
at the receiver … is delivered to LangFuse" with AC-5 claiming "metrics+events … **appear in
LangFuse**." So C26 ships a signal set that the C27 sink does not actually store, and C26 AC-5
directly conflicts with C27 AC-3/AC-4 (which only browse traces/sessions).
**Evidence/reasoning.** LangFuse's native OTLP ingestion endpoint (`/api/public/otel`, signal path
`/api/public/otel/v1/traces`) implements OTLP **trace** ingestion only — metrics and logs are not
ingested there (LangFuse OpenTelemetry docs, verified 2026‑05‑31). v4 itself says only "point the OTel
Collector at it" (README:540) and never enumerates the signal set, so neither "all three" (C26) nor
"traces only" (C27) is a stated v4 fact — both are fills, and the two builders filled the same seam
differently. This is exactly the OQ-1 sub-question ("what happens to metrics/events vs traces"). The
faithful seam is **traces-only at C27**; the disposition of metrics/logs (drop at C26, or route to a
non-LangFuse sink) edits **C26's** pipeline and must be ruled jointly so C26's export description and
C27's ingestion contract are one contract.
**Fix.** **DEFERRED — needs orchestrator decision (joint C26↔C27 seam).** C27-side only: upgraded
§3.1's payload row and OQ-1 from the soft "may not be browsable" hedge to the **grounded fact**
(LangFuse OTLP ingests **traces only**; C27's inbound contract is **traces-only**) and named the
concrete C26-side consequence (C26's metrics+logs pipelines / AC-5 cannot land in LangFuse as specced)
as the joint item to resolve. The *direction* of the corrective edit lands in C26 §3.3/AC-5 (out of
bounds for this reviewer) → left deferred; C27's files now state the fact, not the resolution.

### RC27-02 — major — Ingestion-auth/transport shape is described vaguely and (across specs) inconsistently; the grounded LangFuse shape (HTTP Basic auth, OTLP/HTTP only) should be C27's published contract. (FIXED)
**Claim.** C27 §3.1 Auth row says only "LangFuse **project/public+secret API keys** … C26's exporter
presents them"; C26 §3.2/§7 describe the same hop as "an ingestion key in an exporter header." Close,
but neither pins the actual construction C26's `otlphttp` `headers:` block needs frozen.
**Evidence/reasoning.** LangFuse's OTLP ingestion authenticates with **HTTP Basic auth** built from a
base64-encoded `public_key:secret_key` pair (plus an `x-langfuse-ingestion-version` header), over
**OTLP/HTTP only — HTTP/JSON or HTTP/protobuf; gRPC is not supported** (LangFuse OTel docs, verified
2026‑05‑31). v4 specifies none of this (README:540 silent) — it is a fill, but a *knowable* one that
sharpens (not contradicts) the seam: it matches C26 calling the exporter `otlphttp` and C26 §7's
"ingestion key in an exporter header." C27 owns the far side of the seam, so C27 should publish the
precise shape for C26 to bind against; the exact path/version header stays sweep-2 (OQ-1).
**Fix (applied).** Tightened C27 §3.1's Auth row to name **HTTP Basic auth from the base64
`public:secret` key pair** as the authoritative ingestion-auth shape C26 binds against, and annotated
the §1 FAITHFUL-FILL + §3.1 with **OTLP/HTTP (no gRPC at the LangFuse seam)** — tagged LangFuse-native,
exact path/version header deferred to sweep-2/OQ-1. No new capability/custom code (documents stock
LangFuse behaviour) → applied.

### RC27-03 — major — Mis-citation: the G37 secrets store is "parked as FE-3," but FE-3 is the signing/key-model enhancement, not a secrets store; no FE entry is the secrets store. (FIXED — CONFIRMED by D-14)

> **CONFIRMED by D-14 (integrator pass 2026-05-31).** G37 (secrets/credential-storage gap, owned by C03) ≠ FE-3 (graduated-mandatory signing, blocked on G37 but a distinct deferred enhancement). The RC27-03 fix is binding; specs deferring secrets cite **G37**, not FE-3. C27 §1/§6/§7/§9-OQ-4 already state the distinction.
**Claim.** §6, §7, OQ-4 (and plan T3 / Risk 3) all state a real secrets-management layer "is parked
as **FE-3**" / "that is FE-3, gated on a chosen store." (The prior review pass explicitly *blessed*
this as "exactly the faithful move" — a fidelity miss this pass corrects.)
**Evidence/reasoning.** FUTURE-ENHANCEMENTS.md **FE-3** is **"Graduated-mandatory signing + per-actor
key model"** (deferred from C41 DELTA-01/06). It is *blocked on* G37 ("no secrets store; plaintext keys
make signing theater") but is **not itself** the deferred secrets store; **no** FE entry is (FE-1 judge
family, FE-2 substrate portability, FE-4 seat pool, FE-5 enumerated DoD). The home of the
unbuilt-secrets-store question is the **open gap G37 itself**, whose canonical resolution OQ-4 already
correctly assigns to **C03** (the config owner). Citing FE-3 as the parking lot is a fill mislabeled as
a cross-reference fact, repeated 4× across the two docs.
**Fix (applied).** Replaced every "parked as FE-3 / that is FE-3, gated on a chosen store" with the
faithful statement: the secrets-store gap is **tracked as the open gap G37 (canonical resolution owned
by C03 per OQ-4); FE-3 (signing) is itself blocked on G37**. The (correct) note-and-defer / build-no-
secrets-layer posture is unchanged.

### RC27-04 — minor — OQ-4's "shared across C03/C24/C26/C27/C41/C43" over-claims which components carry G37 as a key gap. (FIXED)
**Claim.** OQ-4 says "G37 is shared across **C03/C24/C26/C27/C41/C43**."
**Evidence/reasoning.** The inventory's key-gap column lists **G37** only on **C03, C27, C43**.
C24/C26 carry **G33** (OSS-stack failure), not G37; C41 carries none of G37/G33 as a key gap. The
narrative point (many components *touch* plaintext creds) is fine, but conflating "touches credentials"
with "carries G37 as a key gap" mis-states the inventory. Minor, non-load-bearing.
**Fix (applied).** Softened OQ-4 to "G37 is a key gap on **C03 (config owner), C27, C43**, and the
plaintext-credential surface it names is touched by the OTel/Max/judge paths too" — matching the
inventory's gap assignment while keeping the cross-cutting note.

### RC27-05 — minor — G33 attribution overstated: §6/OQ-6 say the inventory assigns G33 to "C24/C26"; it assigns G33 to C24 (not C26). (FIXED)
**Claim.** §6 (LangFuse-down row + trailing FAITHFUL-FILL) and OQ-6 say availability/retention "fall
under G33, assigned by the inventory to **C24/C26**."
**Evidence/reasoning.** Inventory G33 owners: **C21, C24, C36, C37, C40, C57** — **not** C26 (C26's
only key gap is G04). C26's spec elects to *discuss* G33, but the inventory does not assign it there.
Minor — C27's disposition (build no buffer; defer the OSS-stack failure story) is correct regardless.
**Fix (applied).** Tightened the "C24/C26" attributions to **C24 (the integration-hardening budget)**,
keeping "shared with C26" only where C27 genuinely co-defers the *exporter*-side behaviour (a C26
concern). Matches the inventory.

### RC27-06 — minor — INV-4 / §3.1 name only `session.id`; the upstream correlation contract C26 forwards is a set — mirror it so the two specs' correlation story is visibly one contract. (FIXED)
**Claim.** §3.1/§4/INV-4 lean on `session.id` (and name `user.account_uuid`, `organization.id` for
sensitivity) citing AIC:178. C26 §3.4 INV-4 enumerates the full pass-through set (`prompt.id`,
`session.id`, `user.account_uuid`, `organization.id`, `terminal.type`) at the same source.
**Evidence/reasoning.** Not a fidelity error (the cite is right; `session.id` IS the grouping key) — a
completeness gap. Naming only `session.id` understates that INV-4 depends on the *upstream* set
arriving intact (C26 INV-4 pass-through).
**Fix (applied).** Added a half-line to INV-4 and the §3.1 Correlation row: the dependency is on the
full upstream correlation set C26 forwards unaltered (C26 INV-4), with `session.id` as the grouping
key. Faithful, non-architectural → applied.

### RC27-07 — minor — Operator auth (§3.2) should be explicitly LangFuse-native, so the "no custom code" boundary is airtight on the auth axis too. (FIXED)
**Claim.** §3.2 says the operator "authenticates and browses"; §3.3/§4 list an "initial admin"
credential — a natural spot for a builder to bolt on SSO.
**Evidence/reasoning.** No violation found — the spec already frames the UI as off-the-shelf and
credentials as LangFuse's. A belt-and-suspenders nit to pre-empt a custom auth/SSO story (passes the
bar — LangFuse ships its own login/RBAC).
**Fix (applied).** Added a clause to §3.2: operator authentication is **LangFuse-native (its own
login/RBAC); C27 authors no auth/SSO layer** — same INV-3 posture.

### RC27-08 — minor — §6 G37 row reads co-located secrets (OTel mTLS, Max OAuth) as if C27-adjacent state; clarify they are owned elsewhere. (FIXED)
**Claim.** §6 G37 row lists "the co-located OTel mTLS certs / Max OAuth tokens" alongside LangFuse's
own creds.
**Evidence/reasoning.** Accurate per G37's enumeration, but those are C25/C41/C04 secrets, not C27's;
reading them as "co-located with C27" risks implying C27 touches them. Trivial hygiene.
**Fix (applied).** Reworded so co-located secrets read as "alongside, owned elsewhere," not C27-owned.

### RC27-09 — minor (no defect) — Off-the-shelf / config-only posture, terminal-sink, and availability/retention deferral all pass the bar. Verified.
**Claim/Evidence.** INV-3 + the §1 NOT-list + every plan task forbid a custom store/UI/receiver/
retention/HA/secrets layer; §6/OQ-5/OQ-6 DEFER availability/retention/HA to LangFuse-native + ops and
build nothing (adding any of them would be the exact stack-hardening the bar drops). Terminal-sink /
two-sinks (INV-1/INV-2, AC-6) is asserted with **no C27→CXDB crossing**, consistent with C26 §3.4
INV-1/INV-2 (single LangFuse sink + Collector✗→CXDB anti-edge) and C25 INV-1/AC-6; the "weak L4
fallback" reading (AIC:326/374) is correctly **not** adopted and routed to OQ-2 (CXDB is L4, LangFuse
browsing-only). License paraphrase (§1) checked against README:294 — faithful; the README-"MIT" vs
AIC-"Apache 2.0" tension is real and correctly flagged with OQ-3 routing the SPDX pin to deploy time.
**No fix.** Two-sinks hoist question **RESOLVED by D-12:** the rule stays as **cross-referenced per-spec
notes** (fork stated at C25, anti-edge at C26, C24/C27 cross-referencing) — **no new shared
Observability-subsystem doc** (avoids scope creep). C27 INV-2 carries the D-12 cross-reference note.

## Seam-consistency verdict (C26 ↔ C27)

**Consistent on mechanism; mismatched on signal set.** Both specs name the **same** seam (LangFuse's
native OTLP-trace ingestion endpoint, OTLP/HTTP, ingestion-key/Basic-auth header, exact path deferred
to a **joint** sweep-2 resolution under shared OQ-1) — that half aligns, and RC27-02 sharpens it. The
unresolved half: **C26 forwards metrics + logs + traces to LangFuse, but LangFuse ingests traces
only** (RC27-01), and C26 AC-5 ("metrics+events appear in LangFuse") conflicts with C27's browse ACs.
Faithful seam = **traces-only at C27**; the metrics/logs disposition is a C26-pipeline decision
**DEFERRED** to the orchestrator (edits C26 §3.3/AC-5, out of bounds here). C27 remains a **terminal
sink** — no C27→CXDB crossing — so the two-sink rule (G04) is not violated by either side.

## Verdict
**accept-with-fixes.** C27 is a faithful, bar-compliant spec: off-the-shelf self-hosted LangFuse
(deploy + config, near-zero custom-code budget), inventing **no** custom store/UI/receiver/HA/buffer/
retention/secrets machinery (every red flag the brief names is cleanly avoided), with terminal-sink/
two-sinks asserted consistently with C26 and C25. Applied fixes are cite-hygiene + contract-sharpening:
the **G37→FE-3 mis-citation** (RC27-03, a fidelity error the prior pass missed), the grounded
LangFuse ingestion auth/transport shape (RC27-02), the traces-only sharpening of the seam on the C27
side (RC27-01), the G37/G33 ownership cites (RC27-04/05), and three completeness nits (RC27-06/07/08).
**One architecturally-significant item is DEFERRED to joint orchestrator resolution: the C26↔C27
metrics/logs signal-set mismatch** (RC27-01) — its corrective edit lands in C26's pipeline and must be
ruled as one contract. No fidelity blockers; the only non-applied item is the genuinely cross-component
seam, correctly left for the integrator.
