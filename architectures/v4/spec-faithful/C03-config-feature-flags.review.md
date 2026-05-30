# Adversarial review — C03 Layered config / feature-flag model (Tracks A + B, sweep 1)

Reviewer persona: Subsystem Adversary (Runtime Substrate)
Targets: spec-faithful/C03-config-feature-flags.md, plan-faithful/C03-config-feature-flags.md,
spec-optimized/C03-config-feature-flags.md, plan-optimized/C03-config-feature-flags.md

## Findings — Track A (faithful: attack fidelity/completeness)

### RC03-01 — minor — `[rigs]` vs `[[rig]]` spelling inconsistency (mirrors C01 RC01-03)
Claim: spec-A §4 capability table and the Phase-0 "off-by-omission" set both write **`[rigs]`**; but the
same table's rig row and §13.3 use **`[[rig]]`** (array-of-tables).
Evidence: AI-CONTEXT §3.4's explicit-off list literally says "rigs"; AI-CONTEXT §13.3 / C42 use `[[rig]]`.
The faithful doc is citing §3.4 verbatim, so it is not *wrong*, but it uses both spellings within one doc
for the same section, which is a drift hazard for the linters that key off section names.
Fix (APPLIED): footnoted the Phase-0 "off-by-omission" `[rigs]` to note the canonical array form is
`[[rig]]` (§13.3 / C42) and that §3.4's "rigs" is the prose form; one spelling (`[[rig]]`) recommended for
sweep-2 schema. Same disposition as C01 RC01-03; flagged for C01/C03/C42 convergence.

### RC03-02 — minor — G03 native-count resolution is correct and consistent with C01 — but the two specs must not both "own" the fix
Claim: spec-A §6 + AMBIGUITY[G03] resolves the count as phase-relative (5 at Phase 0, 6 at Phase 1) and
says C03 "owns the very flag (`[formulas]`) the miscount turns on."
Evidence: This is faithful and matches C01-A §6 AMBIGUITY[G03] and C01-A AC-2 exactly (both pick Reading B,
both defer the corpus-wide headline to C57). GOOD — no contradiction. The only risk is double-ownership of
the *resolution*: C01 asserts the count via its conformance manifest; C03 asserts it via the section-
presence derivation. They are complementary (C03 = "which sections present → count"; C01 = "verify the
capability is actually native"), not conflicting. Fix (APPLIED): added a one-line note to §6 clarifying the
split (C03 derives the count from present sections; C01 verifies each native claim; C57 reconciles the
corpus headline) so no reader thinks two specs independently re-litigate G03.

### RC03-03 — minor — "data-store" Kind vs "no mutable runtime state" is a faithful tension worth flagging
Claim: Inventory lists C03 `Kind: data-store`; spec-A §4 says "No mutable runtime state of its own."
Evidence: The inventory classifies C03 as a data-store but the config is a version-controlled *file set*
read at load, not a live store — the faithful doc correctly describes it as definitional/load-time state.
This is a (minor) inventory-vs-spec classification mismatch, not a defect in the spec. Fix (DEFERRED):
the spec's framing is the more accurate one; the `Kind: data-store` label is the inventory's and out of
C03's edit scope. Flagged for the integrator (cf. C07 which has the analogous cross-cutting-vs-artifact
question). No spec change.

## Findings — Track B (optimized: attack the design)

### RC03-04 — major — DELTA-03 SecretRef has no resolver baseline, so "no plaintext secrets" is a lint, not a guarantee, at Phase 0
Claim: spec-B DELTA-03 + invariant: "No secret literal is ever present in a `LayerSource` payload that is
version-controlled (lint-enforced)"; §7 "DELTA-03 is the core security improvement — secrets out of git."
Evidence/reasoning: The *seam* (`SecretRef` syntax + `SecretResolver` interface) is well-specified, but
OQ1 concedes the **provider is unchosen** ("env-injection only, or a Vault/SOPS-shaped backend?"). Until a
resolver provider exists, the only enforced thing is a *lint that rejects secret-shaped literals* — which
is detection, and trivially defeated (a base64'd or split secret passes a regex lint). The plan (T9) ships
"env-injection baseline," but env-injection still means the secret is in the process environment, sourced
from *somewhere* — and if that somewhere is `${ENV:NAME}` resolved from a `.env` file or the `city.toml`
`env = {}` block (AI-CONTEXT §13.2, the exact G37 surface), the secret is still adjacent to version
control. The delta claims "secrets out of git" as achieved; at the Phase-0/baseline reality it is "secrets
*referenced* indirectly, with the actual storage unspecified." This is the same over-claim pattern as the
C01/C02 portability/enforcement deltas.
Fix (APPLIED): qualified DELTA-03 / §7 to state "secrets out of *version-controlled TOML*" (the achievable
claim) rather than "secrets out of git", and noted that the resolver-provider choice (OQ1) determines
whether the secret material itself is actually protected or merely relocated to an unspecified `env`
source. The lint is detection-of-literals, not a storage guarantee.

### RC03-05 — major — DELTA-02 capability descriptors + transitive `requires` create a cross-component coupling the corpus never had, with no cycle-handling
Claim: spec-B DELTA-02 + invariant: "`requires` is transitively satisfied or load fails — you cannot enable
C42 rigs without the substrate they assume."
Evidence/reasoning: Promoting section-presence to a dependency-resolved capability graph is a real
improvement (it kills the F13 silent-missing-config trap). BUT: (a) there is **no statement of what happens
on a `requires` cycle** (A requires B, B requires A) — a real risk once packs (C02) self-declare descriptors
(OQ3); the load-time flatten would either loop or fail opaquely. (b) The descriptor graph now encodes
inter-component dependency *in config*, duplicating the inventory's `Depends on` edges — two sources of
truth for "what needs what," which can drift. (c) `conflicts_with` is named but its semantics (mutual?
directional? transitive?) are undefined. For a foundational fail-closed gate, undefined cycle/conflict
semantics is a correctness hole.
Fix (APPLIED): added to §3 invariants + §6 that the `requires`/`conflicts_with` graph MUST be a DAG
(cycle = load-time error with a typed diagnostic, not a hang), and noted the descriptor graph should be
*derived from / checked against* the inventory dependency edges rather than a second independent source of
truth (DEFERRED: whether descriptors are authored or generated from the inventory is an architectural call
for the integrator — flagged, not resolved).

### RC03-06 — minor — DELTA-05 "phase profiles" reintroduce the very thing C03 says it is NOT (a runtime feature-flag service)
Claim: spec-B §1 "Not a runtime feature-flag service with live per-request flips … Flags are install/phase-
scoped." DELTA-05 / §4: "Phase 0/1/2 are *named layer presets* … optional named overlays."
Evidence/reasoning: No real contradiction (presets are load-time, not per-request), but "named overlays"
that an operator selects is a small step toward a profile/environment system; the spec should be explicit
that selecting a profile is still a *load/reload* event (immutable generation), not a live flip, so the
"no live per-request flags" boundary is not quietly eroded. Fix (APPLIED): one-line clarification in the
DELTA-05 / phase-profiles bullet that profile selection is a load/reload generation switch, preserving the
stated non-goal.

### RC03-07 — minor — Six deltas, all defensible; DELTA-06 config-provenance-to-C23 is a clean cross-component win but assumes C23/C41 shape not yet frozen
Claim: spec-B DELTA-06 emits a `ConfigProvenance` event to C23 with C41 attribution on every (re)load.
Evidence: Good design (makes "what config produced this satisfaction number" answerable for C46). The plan
(T10) correctly gates this on C23/C41 availability and stubs the sink. The only risk is the event *shape*
being co-frozen with C23 — which plan §4 milestone 5 already calls out. No over-claim. Fix: none needed;
noted as a correctly-handled cross-component dependency.

## Cross-component notes
- **G03 native-count is consistent across C01 and C03** (RC03-02): both pick phase-relative 5/6, both defer
  the corpus headline to C57. Clean. The C03 derivation and C01 conformance check are complementary halves.
- **`[rigs]`/`[[rig]]` spelling** (RC03-01) needs one canonical form across C01/C03/C42 — mirror to the
  same OQ raised in C01 RC01-03.
- **Capability-descriptor ownership** (RC03-05 / OQ3) straddles C02↔C03: C02-B's `CapabilityDescriptor`
  (in `PackManifest`) and C03-B's `CapabilityDescriptor` (in the registry) are the *same* concept declared
  in two specs. They are consistent in intent (C02 carries it in the bundle, C03 validates/registers it),
  but the authoritative schema owner must be ruled (C02 OQ3 + C03 OQ3 both raise it). Mirror to review-log.
- **SecretRef seam** (RC03-04) is referenced by C02-B (§7 "secrets reach nodes only as resolved values via
  env keys their manifest declares … aligns with C03 DELTA-03") — the two specs agree, but both depend on
  the unchosen resolver provider (G37). One ruling needed; mirror to review-log (already seeded as C03 OQ).

## Verdict
- **Track A: accept-with-fixes** — faithful, correctly defers G37, and its G03 resolution matches C01. The
  `[rigs]`/`[[rig]]` and data-store-Kind nits are flagged; only the spelling footnote applied.
- **Track B: accept-with-fixes** — strong design (descriptors + validation gate + secret indirection +
  provenance), but DELTA-03 over-claimed "secrets out of git" (now "out of version-controlled TOML") and
  DELTA-02's `requires`/`conflicts_with` graph lacked cycle/conflict semantics (now DAG-required, with the
  authored-vs-derived descriptor question deferred). Core model is sound and well-sequenced.
