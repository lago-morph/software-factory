# C22 — CXDB type registry & viewpoint tagging  (Build Plan, canonical track)

> Source / Spec ref: spec/C22-cxdb-type-registry.md

## 1. Work breakdown

| id | description | size | prereqs |
|---|---|---|---|
| T1 | Freeze the **type-identity triple** contract `{bundle_id, type, version}` + `viewpoint` as the per-payload metadata writers must attach (spec §3 `tag_payload`, §4). Pure contract artifact. | S | C21 turn/payload model |
| T2 | Define the **viewpoint enumeration** `{architecture, spec, implementation}` and the totality invariant I3 (spec §4). | S | — |
| T3 | Define the **bundle document format** (`bundle_id`, `version`, `types` map, `viewpoints`) stored in CXDB `registry/` (spec §4; AI-CONTEXT §5.3). | S | T1, T2 |
| T4 | Author the **`softwarefactory.v4.trajectory` bundle skeleton** — bundle identity + viewpoint set + placeholder type slots — the concrete artifact that closes G17 for the CXDB side. Per-type schemas are stubs at this sweep. | M | T3 |
| T5 | Specify the **resolution + validation gate** (`resolve_type`, I1 resolvability, I2 version immutability) that runs on the C21 write path. | M | T1, T3 |
| T6 | Specify **type-aware projection** (`project`) + **viewpoint filtering** (`filter_by_viewpoint`) read interfaces (spec §3; AI-CONTEXT §5.5; F50). | M | T1, T3 |
| T7 | Specify **schema-evolution rules** (additive new `version`, immutability of published versions) and replay-safety guarantees for C49. | S | T5 |
| T8 | Write **acceptance tests** AC1–AC6 (spec §8), incl. the F50 separation test (AC4) and version-replay test (AC5). | M | T4, T5, T6, T7 |

## 2. Dependency graph

- **Hard upstream:** C21 (CXDB store) — C22 *is* C21's `registry/` + type layer; cannot land before C21's
  turn/payload model and `registry/` directory exist.
- **Internal critical path:** T1 → T3 → T4 → T5 → T8. The triple contract (T1) gates the bundle format
  (T3), which gates the v4 bundle (T4) and the validation gate (T5); acceptance (T8) closes everything.
- **Downstream waiting on C22's contracts:** C24 (must tag-on-ingest), C36/C37/C38 (read typed payloads),
  C49 (version-aware replay), CXDB UI (projection). They build against the **T1/T2 contract** as stubs.
- **No cycle:** C22 depends only on C21 (lower in Batch 1); it is depended-on by Batch 2+ consumers.

## 3. Parallelization

Within C22, after the **T1+T2 contract is frozen** (smallest, do first), three workstreams run concurrently:
- **WS-A (write side):** T5 validation/resolution gate + T7 evolution rules.
- **WS-B (read side):** T6 projection + viewpoint filtering.
- **WS-C (artifact):** T3 bundle format → T4 the `softwarefactory.v4.trajectory` bundle.

T8 (acceptance) joins all three. WS-B and WS-C have no interdependency; WS-A depends on T3 (from WS-C)
for the schema it validates against, so start T3 early in WS-C to unblock WS-A.

## 4. Interfaces-first / contract milestones

Freeze **earliest** so dependents can build against stubs:
1. **M1 — the triple + viewpoint metadata contract (T1+T2).** This is the single most-shared artifact:
   C24 stamps it, C36–C38/C49 read it, the UI projects it. Freeze before any internal work.
2. **M2 — bundle document format (T3).** Lets the C21 team wire the `registry/` directory.
3. **M3 — `softwarefactory.v4.trajectory` bundle identity + viewpoint enum (T4 skeleton).** Lets downstream pick
   their `type`/`viewpoint` values even before per-type schemas are filled in at sweep 2.

## 5. Risks & de-risking order

Prototype/spike in this order to retire the most uncertainty:
1. **G17 closure (highest value):** confirm the `softwarefactory.v4.trajectory` bundle (T4) actually covers the
   payload types v4 stores in CXDB. Spike against C24's intended raw-body payload shape (G26 seam) to
   avoid defining a bundle that doesn't fit real ingest.
2. **F50 enforceability (OQ1):** validate that mandatory tag (I3) + `filter_by_viewpoint` genuinely
   separates architecture/spec assertions — and surface, honestly, that it does *not* prevent mis-tagging
   (detect-vs-prevent, → review-log).
3. **Version-replay safety (I2/T7):** prove a schema version bump leaves older turns resolvable, since
   C49 counterfactual replay depends on it. Highest correctness risk on the read path.

## 6. Definition of done

- All of T1–T8 complete; spec §8 AC1–AC6 satisfied.
- **Per-component:** the `softwarefactory.v4.trajectory` bundle exists and is registrable under CXDB `registry/`
  (closes G17 for the CXDB type side); every CXDB payload carries a resolvable triple + exactly one
  viewpoint; F50 separation demonstrated (AC4); version evolution is replay-safe (AC5); typed payloads
  project structurally (AC6).
- **Contracts frozen** (M1–M3) and published so C24/C36/C37/C38/C49/UI can build against them.
- Open questions OQ1–OQ3 mirrored into `_meta/review-log.md`.
