# Adversarial review — C02 Pack & Tool-Node ABI (Tracks A + B, sweep 1)

Reviewer persona: Subsystem Adversary (Runtime Substrate)
Targets: spec-faithful/C02-pack-extension-abi.md, plan-faithful/C02-pack-extension-abi.md,
spec-optimized/C02-pack-extension-abi.md, plan-optimized/C02-pack-extension-abi.md

## Findings — Track A (faithful: attack fidelity/completeness)

### RC02-01 — minor — Reading-A vs Reading-B choice silently sets the cross-track ABI shape
Claim: spec-A §3.2 picks **Reading A** (args + partition files + exit code) as the *mandatory floor* and
relegates stdin/stdout-JSON (Reading B) to an optional sweep-2 profile.
Evidence: This is a faithful, well-argued AMBIGUITY resolution (only Reading A is shown in §13.3). BUT the
Track-B spec (C02-B DELTA-01/03) makes **stdin-JSON the primary path** and demotes argv/`{placeholder}` to
a *compat shim*. The two tracks therefore land on opposite primary I/O channels. That is *permitted* (Track
B improves freely), but the faithful doc should note that its Reading-B "optional profile" is exactly what
the optimized track promotes, so a reader diffing the two tracks understands the divergence is deliberate.
Fix (APPLIED): added a one-line cross-track note to the §3.2 AMBIGUITY block pointing at C02-B DELTA-01/03.

### RC02-02 — minor — Downstream fan-out list cites a component range without C40/C45
Claim: spec-A §2 "Downstream (every 'your work' pack)" lists C10, C14–C16, C24, C30–C33, C35, C36–C39,
C44, C46–C50.
Evidence: Faithful to the README placement tables, but C40 (durable Orders — "Gas City Orders" but Temporal
optional, i.e. a pack-shaped integration) and C45 (twin fidelity, a tool node over C44) are arguably also
pack-realized; conversely C46 (meta-metric *stream*, a data-flow) is not obviously a pack. This is a
completeness nit, not a fidelity error — the list is illustrative ("~25 components") and the inventory is
the authority. Fix (DEFERRED): left as-is; the "~25" hedge already signals non-exhaustiveness. Flagged so
sweep-2 can reconcile the exact pack-vs-not set against the inventory `Kind` column.

### RC02-03 — minor — "stateless per call" FAITHFUL-FILL is sound but collides with C02-B OQ4 / C17 OQ4
Claim: spec-A §3.2(3) invariant: tool-node invocation is "stateless per call … one process per node
execution," with long-lived work pushed to `[[service]]`.
Evidence: Faithful and minimal. But the same boundary (tool-node vs `[[service]]` for the C24 directory-
watch bridge and the C44 twin) is an *open* question in C02-B OQ4 and C17 OQ4 — i.e. the optimized tracks
concede the boundary is undrawn in the corpus. The faithful doc asserts it as settled. Since v4 genuinely
only shows `type="subprocess"` spawn-per-step, the faithful assertion is defensible, but it should cross-
reference that C24/C44 may not fit. Fix (APPLIED): added a pointer from the "stateless per call" invariant
to the open tool-node↔service boundary (OQ5 already raises it; tightened the wording).

## Findings — Track B (optimized: attack the design)

### RC02-04 — major — DELTA-02 pack signing names no key-management / trust-root owner (supply-chain gap on a self-modifying factory)
Claim: spec-B DELTA-02 makes the bundle "signed, versioned, dependency-declaring," and §6 cites it as the
mitigation for the self-bootstrap (C52) RSI supply-chain risk: "an unsigned/unverified pack entering the
load path is an RSI risk … signature + fail-closed verify."
Evidence/reasoning: Signature *verification* is specified, but **who holds the signing key, what the trust
root is, and how a factory-generated pack (C52) gets signed without the factory also holding the key** are
unspecified. On a self-modifying factory this is the crux: if the factory can sign its own emitted packs,
the signature proves provenance but NOT that a human reviewed it — it does not actually gate RSI (G35), it
only authenticates the author (which may be the factory itself). The delta as written presents signing as a
supply-chain *control* when, absent a human-held trust root, it is only an *audit stamp* (the same
over-claim pattern flagged in C01 RC01-04 for DELTA-01). OQ3 correctly flags the C02↔C41↔C51 ownership
straddle but does not surface the key-custody / human-gate question.
Fix (APPLIED): qualified DELTA-02 in §6 to state that signing provides *authenticated provenance*, and that
gating RSI requires the signing trust-root to be **human-held or human-gated at the C52/C53 review point**
(not factory-held) — otherwise it is audit, not prevention. Cross-ref added to C52/C53 and G35. The full
key-management design is DEFERRED to C41 (attribution/provenance) + C51 (transfusion) + C57.

### RC02-05 — major — DELTA-04 capability enforcement is claimed at the ABI layer but has no teeth without C43 (the G21 detection-vs-prevention trap)
Claim: spec-B DELTA-04 + §3b: "A node touching outside its grant is killed (exit ≥124) … converts F44's
broad access from implicit to declared-and-bounded." Invariant "Capability grant/enforcement."
Evidence/reasoning: The spec is honest in §6 ("enforcement strength depends on C43's mechanism … C02
declares and threads the grant but does not itself implement the sandbox") and OQ2 raises exactly the G21
risk. GOOD. But the spec *body* (DELTA-04 header, §3b "is killed", §7 "the deterministic-layer half of the
C43 posture") repeatedly states enforcement as a fact, while the kill mechanism (who detects an out-of-
partition `open()`? the OS? Gas City? a seccomp profile?) is undefined. If C43's mechanism is config-level
`work_partition` only (which §13.3 shows and whose enforcement strength C02-B OQ2 itself calls "unproven"),
then "killed on breach" is aspirational. This is the single most important security claim in C02 and it
rests on an unbuilt downstream (G31/G21).
Fix (APPLIED): softened DELTA-04 / §3b from "is killed" to "is killed **if C43 supplies OS-level
enforcement; absent that, the breach is detected-and-attributed only (G21) — see OQ2**." Keeps the design
intent, makes the guarantee conditional on the C43 seam rather than asserted at the ABI.

### RC02-06 — major — Seven deltas on a foundational interface; DELTA-01 (the wire protocol) is contradicted by its own OQ1 and may be a soft fork-trigger
Claim: DELTA-01/03 *define* a `ToolNodeRequest`/`ToolNodeResponse` stdin/stdout-JSON protocol as "the core
G29 resolution."
Evidence/reasoning: OQ1 concedes that Gas City may *already* fix a different I/O convention, in which case
"DELTA-01/03 become conform-or-shim rather than define — and a divergence wide enough to need shimming is
itself a soft fork-trigger." This is the load-bearing risk of the whole optimization: C02-B's thesis is
"packs cover all extension → no fork," yet if v4's actual `gc` tool-node protocol differs from the invented
envelope, C02 must either shim (glue ≈ fork-by-another-name, which DELTA-06 itself calls out for the
language case) or conform (and then DELTA-01/03 are describing, not designing). The delta presents a clean
*designed* protocol where the honest artifact may be *a protocol we must reverse-engineer and match*. This
is acceptable as a Track-B bet but the header over-states certainty.
Fix (APPLIED): reframed the DELTA-01 header from "specify the actual tool-node wire protocol" to "specify
the tool-node wire protocol **(define-if-greenfield; conform-or-shim if `gc` already fixes one — OQ1/G11)**"
so the central uncertainty is in the delta index, not buried in OQ1. The plan (T1 spike) already orders this
correctly; no plan change needed.

### RC02-07 — minor — Exit-code taxonomy reserves `>=124` but does not reconcile with C18/C40 retry semantics it claims to serve
Claim: §3b exit-code taxonomy: `3 = transient/retryable (node asks runtime to retry per C18/C40 policy)`;
`>=124 = runtime-imposed kill`.
Evidence/reasoning: The taxonomy is good and the intent (let C18/C40 distinguish retry/branch/abort
deterministically) is sound. But C18 (reconciler) owns the *convergence-gate / retry-budget* policy and C40
owns *durable retry across crashes*; C02 here asserts a node can "ask the runtime to retry" (exit 3) without
stating whether the node's request is advisory or binding, or how it interacts with C18's per-node iteration
cap (C01-B DELTA-05 / the F52 bound). A node that always returns exit-3 could defeat the substrate's
bounded-tick guarantee. Fix (APPLIED): added a note to the exit-3 row that retry is **advisory — the C18
iteration cap / C40 retry budget is authoritative; a node cannot force unbounded retries (F52, C01-B
DELTA-05)**. Pins the seam so the three-owner retry story (C02 signal / C18 budget / C40 durability) is
explicit.

### RC02-08 — minor — DELTA-02 `transfused_from` and pack `pack_id` introduce a fourth namespace into the unresolved bundle-id mess (XC-4)
Claim: §3a `PackManifest` carries `{ pack_id, version, abi_version, … transfused_from }`; §4 "the bundle's
identity is `{pack_id, version, content-hash}`."
Evidence/reasoning: This is a *separate* namespace from the CXDB/bead bundle-id collision (review-log XC-4:
C20 `v4.beads.v1` vs C22 `strongdm.factory.v4` vs C21 `softwarefactory.trajectory.v1`). C02's `pack_id` is
fine on its own, but the corpus now has FOUR independent reverse-DNS-ish identity schemes
(pack_id, bead bundle, CXDB trajectory bundle, type-registry bundle) with no single naming authority. C02
is not wrong, but as the *supply-chain root* it is the natural place to note that pack identity and the
CXDB/bead bundle namespaces need one ruling. Fix (APPLIED): added a cross-component note to §9 / OQ flagging
that `pack_id` should be reconciled with the XC-4 bundle-id namespace ruling so the factory has one identity
convention, not four. Cross-ref to review-log XC-4.

## Cross-component notes
- **Tool-node ABI ownership is clean** across C01/C02/C17: C01-B DELTA-04 ("seam exists, conformance-
  tested"), C02-B DELTA-01 ("owns the wire format"), C17-B DELTA-01/02 ("typed catalog/facade ON TOP of
  C02, never redefines the wire"). No duplication or contradiction. C17-B §1 even quotes C02 ceding the
  catalog to C17. This is the best-aligned seam in the subsystem.
- **Primary I/O channel diverges by track** (RC02-01): faithful = args+files+exit (Reading A); optimized =
  stdin-JSON envelope (DELTA-01/03). Deliberate and in-charter, now cross-noted.
- **XC-4 bundle-id namespace** (RC02-08): C02 adds `pack_id` as a fourth identity scheme; the C20/C21/C22
  collision still needs the integrator ruling. C02 is outside that collision but should adopt whatever
  convention wins. Mirror to review-log XC-4.
- **Capability-enforcement teeth** (RC02-05) and **wire-protocol define-vs-conform** (RC02-06) both reduce
  to the same two unbuilt/unverified dependencies — C43 (G31) and the real `gc` (G11). C02's plan T1 spike
  + OQ2 joint-spike-with-C43 are the right de-risking actions; no plan change needed.

## Verdict
- **Track A: accept-with-fixes** — faithful, well-cited, the G29 ABI elaboration is the right minimal fill;
  the Reading-A/B and stateless-per-call assertions now cross-reference the optimized-track divergence and
  the undrawn service boundary.
- **Track B: accept-with-fixes** — the seven deltas are individually forced and the C17 seam is exemplary,
  but DELTA-02 (signing-as-RSI-control), DELTA-04 (capability enforcement), and DELTA-01 (define-vs-conform)
  each over-claimed a guarantee that depends on an unbuilt/unverified downstream (C43/G31, C52 trust-root,
  real `gc`/G11). All three softened to conditional claims; the underlying design is sound and the plan
  de-risks them in the right order.
