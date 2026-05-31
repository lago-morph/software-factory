# Adversarial review — C17 Tool-Node Abstraction (Track A, sweep 1)

Reviewer persona: Subsystem Adversary (C08/C17)
Target: spec/C17-tool-node-abstraction.md

Track A attacks **fidelity & completeness only** — not the design. The question is never "should C17 be
a registry with a typed descriptor and a cache" (that is Track B / DELTA territory) but "does the faithful
spec invent only what v4 unambiguously implies, label every fill honestly, and stay consistent with C02
(the ABI it layers on) and the rest of the inventory."

## Findings

### RC17A-01 — major — The C17↔C02 declaration-ownership split (§3.2 [AMBIGUITY: G29]) is a genuine architectural assignment, but it is asserted as resolved here while C02-faithful resolves the *same* seam without granting C17 any "declaration ownership."
- **Claim.** §3.2's [AMBIGUITY: G29] picks "Reading A's wire ownership + Reading B's declaration ownership":
  the *bytes* are C02's, but "the *workflow-level declaration* of which inputs/outputs a node exposes is
  C17's." However C02-faithful §3.2 already enumerates `Input channel` / `Output channel` / declared
  `args`/files as C02's own ABI elements, and C02 §1 cedes to C17 only "the tool-node *abstraction* as a
  workflow concept," not an input/output *declaration* layer. Nothing in C02-faithful reserves a
  "declared-inputs/outputs owned by C17, distinct from the ABI" surface. So C17 invents a third ownership
  band ("workflow-level declaration") that v4 never names and that C02 does not leave vacant.
- **Evidence/reasoning.** Charter A rule 1 (no architectural changes beyond what v4 states/implies) + the
  brief's explicit instruction to verify C17 "layers cleanly on C02's wire ABI (no duplication/contradiction
  of the tool-node seam, G29)." The faithful-faithful pair should agree on who owns the I/O declaration. As
  written, C02 says "args/files/exit-code + optional stdin-JSON is *the* I/O contract (mine)"; C17 says "the
  *declaration* of which inputs/outputs is mine." These are reconcilable only if "declaration" means purely
  "which context placeholder keys a formula node fills" — which is actually **C12's** formula-node schema,
  not a new C17-owned layer. The faithful floor should be: C17 owns *node-kind + determinism semantics +
  the uniform by-name reference*; it does **not** own an inputs/outputs declaration distinct from C02's ABI
  and C12's node entry.
- **Suggested fix (APPLIED).** Narrow §3.2's pick to: C17 adds only node-kind + determinism + the
  by-name/uniform-reference contract; the input/output *declaration* is the C02 `[[tool]]` block (bytes) as
  surfaced into the C12 formula node (which placeholders it fills) — C17 does not introduce a third
  ownership band. Cross-reference C02-faithful §3.2. Keeps G29 resolved in C02, keeps C17 thin (consistent
  with the §4/§8 "no new on-disk artifact / view-only" stance the spec already commits to).

### RC17A-02 — major — C17's dependency table lists C12/C13 as *downstream* ("places nodes"), but C17 has no inventory dependency on C12/C13 at all and the inventory direction is the reverse — fidelity to the dependency graph is fine, but §2 over-claims C17 as a guarantor to C18 ("safe re-run") on a determinism property v4 never promises at runtime.
- **Claim.** §2 + §3.3 + §5.6 state C17 *guarantees* to C18 that "re-running a deterministic node on the
  same inputs is safe … the property C18's convergence loop and C40's crash-survival rely on." But v4 only
  asserts tool nodes are "cheap and reproducible" (README:154) as a *design intent*; it never specifies a
  runtime determinism/idempotency guarantee, and §6 + OQ-3 of this very spec concede "v4 asserts
  reproducibility but specifies no runtime determinism check." So C17 cannot *guarantee* safe re-run to C18
  as an outbound contract; it can only *declare* the determinism contract and rely on C16/test enforcement.
  Presenting it as a guarantee C18/C40 "rely on" overstates fidelity.
- **Evidence/reasoning.** This is a completeness/honesty issue: an outbound *guarantee* (§3.3) is stated
  with more strength than the spec's own failure-mode section (§6, "enforcement deferred to C16/test") and
  OQ-3 support. The faithful reading is "declared invariant + safe-re-run *intent*," not a guarantee.
- **Suggested fix (APPLIED).** Downgrade §3.3 / §5.6 wording from "guarantees safe re-run" to "declares the
  determinism contract; safe re-run is the *intended* P4 payoff, enforced by the contract + C16/test, not a
  runtime-checked guarantee" — consistent with §6 and OQ-3.

### RC17A-03 — minor — Mis-citation: §1 and §3.3/§8 attribute the EARS spec linter to "C32" in several places, but C32 is the LLM-as-judge harness; the EARS/INCOSE spec linter is **C10**.
- **Claim.** §1 ("the EARS spec linter C32"), §6, and the §1 NOT-list / §2 "instances" rows reference "C32
  EARS spec linter" / route the spec linter through C17 as C32. Per the canonical inventory C10 = "Spec
  linter (EARS / INCOSE)"; C32 = "LLM-as-judge harness." The EARS linter is C10. (C17's §2 also lists "C32
  EARS spec linter" in the downstream-instances row.)
- **Evidence/reasoning.** Direct inventory mis-cite (Charter A rule 5: every claim traces to a source; here
  the source ID is wrong). It does not change the architecture but corrupts the dependency picture and the
  cross-reference for any reader.
- **Suggested fix (APPLIED).** Replace the EARS-linter references from C32 → C10 throughout C17-faithful;
  keep C32 only where the LLM-judge is actually meant (it is not, in C17 — C17's tool-node instances are
  deterministic, so the judge is not one of them; remove C32 from the instance list).

### RC17A-04 — minor — §3.1 sources the `kind = deterministic` tag as a [FAITHFUL-FILL] (correct), but C02-faithful §3.2 already carries a `deterministic` invariant on the tool node; the two fills name the same concept with different shapes and neither cross-references the other.
- **Claim.** C17 §3.1 invents a `kind = deterministic` node-kind tag (fill); C02-faithful §3.2 invariant 1
  states "a tool node is deterministic-first … LLM nodes are a different node kind owned by C28." Both fills
  assert the same deterministic-vs-model distinction but at different layers, with no statement of whether
  the tag lives in the C02 `[[tool]]` block, the C12 formula node, or a C17 view — leaving OQ-2 ("node-kind
  tag name/shape … must be reconciled with C16 and C12") to carry the whole burden.
- **Evidence/reasoning.** Completeness/consistency: two foundational faithful specs introduce the same
  invented field independently; a reader cannot tell which is canonical. Minor because OQ-2 already flags
  the reconciliation — but the spec should point at it from §3.1.
- **Suggested fix (APPLIED).** Add a one-line note to §3.1's [FAITHFUL-FILL] cross-referencing C02-faithful's
  deterministic-first invariant and OQ-2, stating the tag's *home* (C12 formula node vs C02 block) is the
  open reconciliation, not a C17-owned new file.

### RC17A-05 — minor — G29 is labelled "minor … owned and resolved by C02" (correct), but §6's final [FAITHFUL-FILL] says "C17 addresses G29 only by consuming C02's resolution and pinning the workflow-level split (3.2)" — which re-opens the §3.2 over-claim flagged in RC17A-01.
- **Suggested fix (APPLIED via RC17A-01).** Once §3.2 is narrowed (RC17A-01), align §6's G29 note to say
  C17 consumes C02's resolution and adds only node-kind + determinism semantics; it does not pin a separate
  "workflow-level I/O split."

## Verdict

**accept-with-fixes.** The faithful C17 is fundamentally sound: it correctly scopes C17 as a thin
workflow-engine *view* over C02's ABI + C12's formula nodes, adds no new on-disk artifact, labels its fills
honestly, and its F51/F52 coverage maps cleanly to the deterministic-first principle. Its real fidelity
weaknesses are (1) RC17A-01 — it carves out a "workflow-level I/O declaration" ownership band that v4 never
names and that C02-faithful does not leave vacant, mildly contradicting the C02 seam the brief asks me to
verify; and (2) RC17A-03 — a repeated C10→C32 mis-cite of the EARS linter. Both fixed in place, along with
the over-stated C18 "guarantee" (RC17A-02) and the cross-reference gaps (RC17A-04/05). No architectural
change required — the deferred question is purely OQ-2's tag-home reconciliation with C12/C16, which is
correctly left open.

**Integrator note (C17/C02 seam, faithful):** After the RC17A-01 fix the faithful pair is consistent — C02
owns the wire bytes + the `[[tool]]` I/O contract (G29 resolved there), C17 owns node-kind + determinism +
the uniform by-name reference, C12 owns which placeholders a node fills. No duplication or contradiction of
the tool-node seam remains. The only residual is the tag-home (C12 vs C02 block), deferred to OQ-2.
