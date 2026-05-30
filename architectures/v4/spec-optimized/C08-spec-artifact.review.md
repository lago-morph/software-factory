# Adversarial review — C08 Spec artifact & format (Track B, sweep 1)

Reviewer persona: Subsystem Adversary (C08/C17)
Target: spec-optimized/C08-spec-artifact.md

Track B attacks the **design**: correctness, hidden coupling, failure handling, cost, simplicity,
scalability, security — and whether each [DELTA] is justified against a concrete force or is unsupported
taste. The optimized C08 carries six deltas (DELTA-01..06); each gets attacked on its merits.

## Findings

### RC08B-01 — major — DELTA-04 (`spec_id` = BLAKE3 over the bundle) creates a satisfaction-history *invalidation cliff*: any edit to any bundle file mints a new `spec_id`, so a one-word fix to `spec.md` or a clarifying edit to `DoD.md` discards all prior satisfaction/meta-metric history keyed on the old id. The spec names this in OQ3 but ships the whole-bundle hash as the design.
- **Claim.** §3/§4/§7 make `spec_id` the join key for C33 satisfaction, C46 meta-metrics, and C49 replay,
  and INV-3 says "any edit yields a new `spec_id`." OQ3 concedes per-file addressing "is more precise" but
  defers it. With whole-bundle addressing, the *common* operation — refine the DoD, fix a typo in the Goal —
  breaks the measurement continuity DELTA-04 exists to protect. The delta's stated benefit ("satisfaction-
  over-time doesn't silently mix spec revisions") is undermined by its own granularity choice: it doesn't
  *mix* revisions, it *severs* the time series at every edit, which is arguably worse for "satisfaction over
  time" (you get a forest of single-point series).
- **Reasoning / cheaper alternative.** A spec identity needs two levels, not one: a stable **`spec_lineage_id`**
  (identity of "this spec across revisions" — e.g. content-address of the manifest's `name` + first-commit,
  or a UUID minted at creation) plus the per-revision **`spec_id`** (content-address of the bundle). C33/C46
  series key on `(spec_lineage_id)` and *annotate* each point with the `spec_id` it was measured at, so a
  revision is a visible step-change in one continuous series, not a new series. This is the standard
  "entity id + version id" split and costs one extra field. It also resolves OQ3 (per-file is unnecessary
  once you have lineage + revision).
- **Suggested fix (APPLIED — additive, low-risk).** Add `spec_lineage_id` to the manifest (DELTA-04) and
  state C33/C46 key time-series on lineage, annotated by `spec_id`; reframe OQ3 as "lineage+revision
  resolves it; per-file addressing is a further optimization, deferred." This is a clarifying refinement of
  DELTA-04, not a new architectural commitment, so applied in place.

### RC08B-02 — major — DELTA-03 (mandatory machine-checkable DoD) is the load-bearing claim against F18, but the spec never establishes that a DoD *can* be machine-checkable for the general case; OQ2 admits most criteria may need the LLM judge (C32) — in which case the DoD is "satisfaction prose with ids" and the F18 rigor gain is asserted, not earned.
- **Claim.** §6 F18 row claims the DoD is "the deterministic anchor" that makes the spec "materially stronger
  than faithful's Partial — prose ambiguity remains." But §3.3 only requires each DoD criterion have "a
  stable id and a boolean/scored evaluation"; *who* evaluates is open, and OQ2 concedes the evaluator may be
  the C32 LLM judge for most criteria. An LLM-judge-scored criterion is exactly as prose-ambiguous as the
  prose it replaced (the judge re-interprets it); the id buys traceability, not rigor. So DELTA-03's F18
  claim is over-stated: it converts prose into *enumerated, addressable* prose, which helps C33 aggregation
  but does not by itself defeat F18's ambiguity.
- **Reasoning.** The honest, defensible claim is narrower and still valuable: the DoD makes "what counts as
  done" *enumerated and per-criterion scoreable* (a real gain for C33/satisfaction and for partial credit),
  and *some* criteria are deterministically checkable (test-pass, lint, scenario), which is where the F18
  rigor gain actually lives. The over-claim is treating the whole DoD as "deterministic."
- **Suggested fix (APPLIED).** Soften §6 F18 + §1's DELTA-03 framing to: the DoD attacks F18 *to the extent
  a criterion is deterministically or scenario-checkable*; judge-only criteria inherit residual prose
  ambiguity (now *localized and labelled* per criterion rather than diffuse). Require the DoD criterion
  taxonomy (deterministic | scenario-backed | judge-only) that OQ2 defers — promote it from OQ to a
  sweep-2 acceptance item so the F18 claim is earned, not assumed. Applied as wording + an AC note; the
  taxonomy *design* stays deferred to sweep-2 (DEFERRED).

### RC08B-03 — major — DELTA-01 (decouple spec from `prompt.template.md`) is well-justified by the corpus, but it silently re-scopes the C08↔C09 *and* C08↔C11 boundaries, and the spec asserts the new ownership ("seam owned by C08") as a recommendation while building the whole interface section on it. This is the one delta that must not be applied unilaterally.
- **Claim.** DELTA-01 + §2 + OQ1 move the reference seam to C08 (C09 resolves a `spec_id`) and make C11
  "emit a C08 bundle." Both are *re-scopes of neighboring components' contracts*, decided inside C08. OQ1
  honestly flags the C08↔C09 ownership as needing "cross-component reconciliation with the C09 author," but
  §3.3/§4/INV-2 already commit to "renderability is now C09's concern, not C08's" — i.e. the spec removes a
  responsibility (INV-2 renderable, in faithful) from C08 and hands it to C09 before C09 has agreed.
- **Reasoning.** The decoupling is the right call (the corpus evidence — StrongDM 3 files, Kilroy
  `spec.md`+`DoD.md`+`.dot`, Gas-City-ships-formulas-not-specs — is strong and concrete; this is force-
  justified, not taste). But "who owns the reference seam" is an architectural boundary decision that
  changes C09's and C11's specs, so it is exactly the class the brief says to **defer**, not apply.
- **Suggested fix (DEFERRED — architectural).** Keep DELTA-01's decoupling (justified) but flag the
  **C08↔C09 seam ownership** and the **C11→C08 emission contract** as DEFERRED for integrator/cross-author
  reconciliation. Do not let C08 unilaterally strip C09's renderability obligation; state both readings (seam
  in C08 vs. seam in C09) and recommend C08 per OQ1, pending the C09 author. Left as-is in the spec body
  (already hedged in OQ1) + recorded here as the top deferred item.

### RC08B-04 — minor — DELTA-05 (four required sections) and DELTA-06 (`detail_level: vague` is legitimate) are in direct tension: a `vague` spec by definition may not be able to fill Constraints / Out-of-scope, yet INV-2 rejects a bundle missing a required section before any run.
- **Claim.** §3.2 makes Goal/Constraints/DoD/Out-of-scope MUST-have (INV-2 rejects on absence); §5/§6 make
  `detail_level: vague` a "legitimate, safe state" whose under-specification is remediated *later* by the
  clarification hook. But if a vague spec must still contain all four sections to pass INV-2, either (a) the
  sections are present-but-empty (so the gate checks presence, not content, weakening DELTA-05), or (b) a
  genuinely thin intent can't be committed at all (defeating DELTA-06). The spec doesn't say which.
- **Reasoning.** Cheaper/cleaner: make the *gate* `detail_level`-aware — `vague` requires Goal only;
  `moderate`/`complete` require all four. The clarification hook (DELTA-06) is precisely what fills the
  missing sections before build tokens are spent. This makes the two deltas compose instead of conflict.
- **Suggested fix (APPLIED).** Add a clause to INV-2 / §3.2: required-section enforcement is graded by
  `detail_level` (`vague` ⇒ Goal required, others advisory-until-clarified; `complete` ⇒ all four). Resolves
  the tension without weakening either delta. Applied.

### RC08B-05 — minor — DELTA-04's content-addressing reuses C21/CXDB's BLAKE3 primitive and lists C21 as a build-time dependency, but the inventory gives C08 only `Depends on: C03`; this adds a foundational→foundational dependency edge (C08→C21) that the batch/parallelism plan doesn't account for, and BLAKE3 canonicalization of a *directory bundle* is non-trivial (file ordering, manifest self-reference).
- **Claim.** §2 adds C21 as upstream; §4 says `spec_id` = "BLAKE3 over the canonicalized bundle." Two issues:
  (1) it introduces a new Batch-1↔Batch-1 dependency the inventory/parallel-build story doesn't list, which
  the plan's parallelism claim should acknowledge; (2) "canonicalized bundle" hides real work — directory
  hashing needs a defined file-ordering + handling of the manifest hashing itself (the manifest can't
  contain the hash of a bundle that includes the manifest without a fixed exclusion rule).
- **Suggested fix (APPLIED — note only).** Add a one-line §3/§4 note that `spec_id` canonicalization needs a
  defined bundle-hash rule (sorted relative paths; `spec_id` field excluded from the manifest's own hashed
  bytes — a Merkle-over-files scheme), and that C08→C21 is a *primitive reuse* (C08 can stub BLAKE3 and is
  not blocked on C21's store). Keeps the parallel-build story honest. The canonicalization *spec* is
  sweep-2 (DEFERRED).

### RC08B-06 — minor — Security: §7 says "lint can flag obvious secret-shaped tokens," but the DoD is the most likely place a criterion encodes an environment-specific endpoint/credential (e.g. "connects to https://prod-…"), and the spec bundle is plaintext in a git pack read by the *implementer* agent — a held-out-integrity (C34) concern if a DoD criterion leaks the very target a scenario is meant to hold out.
- **Suggested fix (NOT APPLIED — cross-component, noted).** Optional sweep-2: state that DoD criteria must
  not encode holdout-sensitive targets, cross-ref C34. Left for the C34/holdout reconciliation; flagged, not
  applied (architecturally touches C34).

## Verdict

**accept-with-fixes.** This is a strong optimized spec — the deltas are mostly force-justified, not taste:
DELTA-01 (decouple from the prompt template) is backed by concrete corpus evidence and is the right call;
DELTA-03/05/06 (DoD + required sections + graded detail) form a coherent attack on F18/F3/F25. The design's
real weaknesses are **correctness of the identity model** (RC08B-01: whole-bundle hashing severs
satisfaction history at every edit — needs a lineage+revision split) and **an over-claimed F18 win**
(RC08B-02: a judge-scored DoD is still prose; the rigor gain is real only for the deterministic/scenario
subset). Both fixed in place by narrowing the claims and adding the lineage id. DELTA-01's boundary
re-scope (RC08B-03) is correct but must be reconciled with the C09/C11 authors — DEFERRED. The
DELTA-05↔DELTA-06 gate tension (RC08B-04) fixed by grading enforcement on `detail_level`.

**Integrator call (C08 spec-vs-template):** DELTA-01 is the defensible answer — the spec is a standalone
target-system bundle the prompt template *references*, not the template itself. The corpus is unambiguous
(every real dark-factory separates them; Gas City itself ships formulas/molecules, not standalone specs),
so Track B's decoupling is better engineering than Track A's faithful collapse, and the two tracks are a
clean faithful-vs-optimized split rather than a faithful error. **The boundary re-scope the integrator must
rule on is C08↔C09 seam ownership** (identity exposed by C08 vs. reference owned by C09) — recommend
C08-owns-identity, C09-consumes — **and** the C11→C08 emission contract. Both DEFERRED to cross-author
reconciliation.
