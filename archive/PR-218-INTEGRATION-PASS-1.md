# Integration Pass 1 — applying adopted rulings D-1…D-5 across the Batch-1 foundation

Integrator pass. Surgical, cross-component edits realizing the binding decisions in
`review-log.md` (D-1…D-5) and `FUTURE-ENHANCEMENTS.md` (FE-1), across both tracks
(`spec/`, `spec-optimized/`). No `.review.md` files touched; no git run.

Conventions:
- **Faithful (Track A):** rulings recorded as `> [AMBIGUITY ... — RESOLVED by D-n]` resolutions
  citing the decision id; no design changes, structure/`[FAITHFUL-FILL]` marks preserved.
- **Optimized (Track B):** rulings folded into the existing `[DELTA-NN]` framing as RESOLVED,
  delta index/header updated where the delta text asserted the now-settled value.

---

## D-2 — Bundle-id namespace (one factory-owned root + per-store sub-bundles)

Canonical: `softwarefactory.v4.beads` (bead types), `softwarefactory.v4.trajectory` (CXDB turn
types), `softwarefactory.v4.packs` (pack ids). Vendor `strongdm.*` and the merged-single-bundle
option dropped.

| File | Change |
|---|---|
| `spec-optimized/C20-bead-schema.md` | DELTA-07 binding + §4.4 DEFERRED block + OQ3 rewritten to RESOLVED; bead bundle = `softwarefactory.v4.beads`. |
| `spec-optimized/C21-cxdb-trajectory-store.md` | DELTA-03 + §4 type-bundle pin + G17 row + §8 AC: trajectory bundle = `softwarefactory.v4.trajectory`; collision notes → RESOLVED. |
| `spec-optimized/C22-cxdb-type-registry.md` | DELTA-01/04 header, §1, §4 data model (bundle file names, `bundle_id`/`type` examples, concrete-types table split by bundle), §5/§7/§8: trajectory bundle named, bead rows tagged C20-authored. |
| `spec-optimized/C02-pack-extension-abi.md` | OQ5 rewritten to RESOLVED; pack-id namespace = `softwarefactory.v4.packs`. |
| `spec/C21-cxdb-trajectory-store.md` | I7 type-registry row: canonical namespace ruled, trajectory bundle = `softwarefactory.v4.trajectory`. |
| `spec/C22-cxdb-type-registry.md` | XC-4 note → AMBIGUITY-RESOLVED; all `softwarefactory.v4` literals → `softwarefactory.v4.trajectory` (§1, §4 triple/bundle, AC1). |
| `spec/C19-bead-work-graph.md` | OQ-C19-5 rewritten to RESOLVED (namespace + ownership). |

C02-faithful, C20-faithful: no divergent bundle-id present → no edit needed (faithful C20 already
treats beads as a separate type space and asserts no bundle string).

## D-3 — Bead-schema ownership (C20 authors; C22 registers)

C20 authors bead-type payload schemas; C22 owns the registration mechanism + CXDB-turn types only,
registering C20's bead types via a documented seam. C22's claim to author bead schemas removed.

| File | Change |
|---|---|
| `spec-optimized/C22-cxdb-type-registry.md` | DELTA-04 reframed (registration mechanism, two namespaces, bead schemas C20-owned); §1 "NOT" bullet, §2 consumer line (C20 supplies schemas via seam), §4 RegisteredType/table notes; flow §5.1 cold-start clarified Phase-0 no-CXDB. |
| `spec-optimized/C20-bead-schema.md` | DELTA-07 RESOLVED block + OQ3: "two registries, one mapping" confirmed canonical. |
| `spec/C22-cxdb-type-registry.md` | OQ2 → RESOLVED by D-3 (ownership split upheld; faithful C22 already declared C20/C22 separate so only the OQ needed resolving). |

Faithful C22/C20 already held the correct "separate registries / C20 owns bead types" reading;
D-3 only required converting the open cross-track OQ to a RESOLVED note.

## D-4 — C19↔C20 direction (C20 depends on C19; co-foundational; M1 freeze + no-op `validate` stub)

| File | Change |
|---|---|
| `spec/C19-bead-work-graph.md` | §2 dependency row + OQ-C19-1 rewritten to RESOLVED: canonical C20→C19, cycle broken by M1 interface freeze + no-op `validate` stub. |
| `spec-optimized/C19-bead-work-graph.md` | §2 C20 dependency made explicit (co-foundational, C20 depends on C19, M1 freeze + no-op stub). |
| `spec-optimized/C20-bead-schema.md` | §2 C19 dependency annotated with D-4 (direction + stub seam). |

Faithful C20 already stated "C20 depends on C19" (inventory direction) — left as-is, no contradiction.

## D-5 — C41↔C23 tamper-evidence (C41 owns the hash-chain over C23 ordered `event_id`s)

| File | Change |
|---|---|
| `spec-optimized/C41-identity-attribution.md` | DELTA-04 header, §3 invariant, §3 outbound C23 line, §4.4 RC41B-01 ownership note, §6 G36 caveat (2): all → RESOLVED — C41 owns chain over C23-provided ordered gap-free `event_id`s. |
| `spec-optimized/C23-event-bus.md` | §6 P9 F-mode row, §7 security, OQ3: C23 provides ordered gap-free `event_id`s only; chain is C41's (OQ3 RESOLVED). |
| `spec/C41-identity-attribution.md` | §6 G36 AMBIGUITY block: appended D-5 chain-ownership resolution (orthogonal to the optional/mandatory question, which stays Track-A faithful). |
| `spec/C23-event-bus.md` | §7 security: appended `> [AMBIGUITY] D-5` — C23 provides ordered ids only, chain is C41's. |

## D-1 / FE-1 — Judge (same-provider baseline; cross-family/cross-provider = FE-1, future)

| File | Change |
|---|---|
| `spec-optimized/C29-model-floor-stylesheet.md` | DELTA-02 header note; §3c policy table (L2/L3 marked FE-1) + post-table D-1/FE-1 ruling block confirming L1 Phase-0 default; OQ-1/OQ-2 rewritten (Phase-0 resolved; FE-1 residual). |
| `spec/C29-model-floor-stylesheet.md` | §6 tension: added `> [AMBIGUITY] D-1/FE-1` resolution so cross-family is no longer an unsatisfiable blocker; I2 invariant, §5 step 4, §8 A2, §6 F27/F46 rows, and G08/G20 OQs annotated to the same-provider Phase-0 baseline with cross-provider = FE-1. |

---

## Residual conflicts / notes for a human

- **Granularity sub-question (under D-2):** whether `softwarefactory.v4.beads` is one shared bundle
  or per-type bundles is left as a sweep-2 detail in C20-opt OQ3 — not a foundational blocker.
- **G37 key-storage (XC-6) still open:** D-5 fixes *chain ownership*, but C41-opt's `signed`/
  `attested` assurance remains security-effective only once G37 (secrets store) lands. Untouched
  here (out of the five rulings' scope); flagged in C41-opt §6 caveat (1) as before.
- **FE-1 judge-seat (DELTA-03 in C29-opt):** retained as the FE-1 seam, not deleted — correct per
  FE-1 ("leave a clean `judge_family` hook"). No Phase-0 obligation.
- **Open DECISION-NEEDED items in review-log** (signing mandatory-vs-optional; the now-superseded
  cross-family-credential critical-path item) were NOT in the five adopted rulings; the
  cross-family one is effectively closed by D-1/FE-1, but I left the review-log entry itself
  untouched (not a spec doc; not in my edit scope).

## Foundation consistency verdict

**Consistent.** After this pass the Batch-1 foundation speaks with one voice on the four
contested seams: one bundle-id namespace (D-2), one bead-schema author with a clean registration
seam (D-3), one dependency direction with a freeze/stub that breaks the build cycle (D-4), and one
owner for the tamper-evident provenance chain (D-5). The judge critical-path blocker is removed:
Phase-0 builds against a same-provider judge (D-1), with cross-family/cross-provider parked as FE-1
behind an existing policy seam. No residual cross-track contradiction remains among C02/C19/C20/
C21/C22/C23/C29/C41; the two open items above (G37, bundle granularity) are scoped sweep-2/security
work, not foundational inconsistencies.
