# Adversarial review — C20 Bead schema registry (Track A, sweep 1)

Reviewer persona: Subsystem Adversary (Persistence & Memory)
Target: spec-faithful/C20-bead-schema.md (+ plan-faithful/C20-bead-schema.md)

Track A attacks **fidelity and completeness only** — not the design.

## Findings

### RC20A-01 — major — Cold-start procedure systematically mis-cited to "AI-CONTEXT §13" (14 occurrences); the rest of the subsystem cites the identical lines (694–699) as "§16"
Evidence: C20-A cited the cold-start recipe (`gc bd find --type factory_build_in_progress`, `transfused_from`,
`gc converge resume <bead_id>`, lines 694–699) to **§13** throughout. C19-A/C21-A/C22 cite the *same line
numbers* to **§16**. Line numbers are the authoritative anchor and agree everywhere; only C20-A's section
label was wrong.
Reasoning: Track A rule 5 — every claim traces to a v4 source. A wrong section number on the most load-bearing
citation in the doc (the cold-start procedure C20 exists to make resolvable) is a fidelity defect.
Suggested fix: `§13` → `§16` for the cold-start procedure. **Applied** — all 14 occurrences corrected.

### RC20A-02 — major — G18 is *relocated to C39*, not *resolved here* — honestly stated in §4.3/§6 but §8 AC-4 could read as closure
Evidence: §4.3 AMBIGUITY block correctly picks "Reading B for the *schema*, Reading A for the *policy*" and §6
lists G18 "**Partially addressed** (schema slots only)" — both correct. But §8 AC-4 phrased the chain
"carries the … fields — so C39 *can* express a bound," which is relocation, not closure; a reader of §8 alone
could think G18 is closed at C20.
Reasoning: The brief asks whether G18 is "truly resolved vs merely relocated." Faithful answer: **relocated**.
C20-A states this correctly elsewhere; the acceptance criterion must not be misreadable as closure.
Suggested fix: Add a "G18 *relocated to C39*, not closed here" marker to AC-4. **Applied**.

### RC20A-03 — major — Three bead types (`anomaly`/`diagnosis`/`resolution`) registered under FAITHFUL-FILL; the live alternative is they are CXDB turns, not beads
Evidence: §4.2 FAITHFUL-FILL registered them as bead types ("a chain cannot be a bead chain unless its links
are beads"). OQ-C20-2 itself concedes they may be CXDB turns with only `fix_task` as a bead — and the §5
corpus puts fine-grained trajectory content in CXDB (C21/C22), not the work-graph. This is the doc's largest
inference; v4 names only `fix_task` by string for the chain.
Reasoning: Defensible (README P11 says "Custom **bead** chain") but not settled. Registering them as frozen
types risks committing the work-graph to content that may belong in CXDB.
Suggested fix: Downgrade the three to *provisional* chain-node types pending the C20↔C21/C22 boundary ruling.
**Applied** — marked provisional in §4.2 with the CXDB-turn alternative spelled out and cross-linked OQ-C20-2.

### RC20A-04 — major — Cross-track divergence on the §16 query not flagged: C20-A keeps `factory_build_in_progress` as a literal type; C20-B folds it into state + needs a shim (XC-2)
Evidence: C20-A §4.2 keeps the verbatim type (so the §16 `--type factory_build_in_progress` query resolves
literally — the *correct* faithful choice). C20-B DELTA-02 makes it `factory_build` + `state=in_progress` and
needs an OQ1 compat shim (XC-2 in review-log). C20-A's §4.1 AMBIGUITY block raised the dual representation but
did not connect it to the §16 query-resolution contract or note the optimized divergence.
Reasoning: Completeness + diffability (track charters) — the faithful spec should note that its verbatim-type
choice is what keeps §16 literal and that the optimized track diverges (XC-2).
Suggested fix: Add an XC-2 cross-reference to §4.1. **Applied**.

### RC20A-05 — minor — `created_by` mislabelled as the override chain's "only edge"
Evidence: §4.3 "Override-discipline chain… its only edge is `created_by` + a reference to the overridden
action." `created_by` is the envelope attribution field (§4.1), not a dependency edge.
Suggested fix: Reword — `created_by` is envelope attribution; the only dependency *link* is the reference to
the overridden action. **Applied**.

### RC20A-06 — minor — Closure-chain edge names (`diagnosed_by`/`produces`/`resolved_by`) invented and incompatible with the optimized track's taxonomy
Evidence: §4.3 diagram invents three edge names; v4 names none ("Tasks with dependencies", untyped). The
optimized track (C19-B/C20-B) independently chose `caused_by`/`closes`/`child_of`/`blocks`. Two tracks, two
incompatible edge vocabularies, neither from v4.
Suggested fix: Mark the edge names FAITHFUL-FILL and note the optimized track's divergent set + that the
canonical edge taxonomy is a cross-track integrator decision. **Applied**.

### RC20A-07 — minor — "Registry closed" invariant presupposes Gas City enforces a closed type set (G11, unverified) — already flagged as OQ-C20-4 but the §3/§5/§8 invariants assert it as fact
Evidence: §3 invariant + §8 AC-5 assert writing an unregistered type "is rejected." OQ-C20-4 concedes Gas
City's actual enforcement is unverified (G11) — the substrate may accept free-form `type` strings.
Reasoning: The closed-registry invariant is the heart of C20's G17 closure; it rests on unverified substrate
behavior. C20-A flags this in OQ-C20-4 but states the invariant unconditionally in §3/§8.
Suggested fix: Cross-reference OQ-C20-4/G11 at the invariant ("rejection presupposes Gas City enforces a
closed type set; if not, enforcement is pack work, C02"). **Not applied** (OQ-C20-4 already carries it) —
flagged so the integrator sees the invariant is G11-gated.

## Cross-component resolutions recommended to the integrator
- **Bundle-id (XC-4):** C20-A correctly does **not** name a bead `bundle_id` (faithfully separates bead types
  from CXDB turns, OQ2). The collision is on the optimized track. Recommended canonical:
  `softwarefactory.v4.beads`, with **C20 authoring bead-type schemas** and C22 hosting the registration
  mechanism — reject C22-B's claim to *own* bead-type schemas (see C20-B / C22 reviews).
- **C19↔C20 direction (XC-1):** **C20 depends on C19** (inventory); co-foundational, broken by the envelope
  freeze. C20-A states this correctly.
- **G18 ownership (XC-3):** C20 owns the *schema slots*; **C39 owns the numeric policy**. G18 is *relocated*
  to C39, not closed at C20. Confirm C39 (C20-A OQ-C20-1).

## Verdict
**accept-with-fixes.** C20-A is faithful and handles G17/G18 honestly (slots here, policy in C39 — explicitly
relocation, not closure). The one real fidelity defect (the systematic §13/§16 mis-citation, RC20A-01) is
fixed. Applied fixes also mark the invented chain-node types and edge names as provisional/FAITHFUL-FILL
(RC20A-03/06), connect the verbatim `factory_build_in_progress` type to the §16 contract (RC20A-04), and
correct the `created_by`-as-edge slip (RC20A-05). No blockers; G18-is-relocated and the bundle-id ownership
fork are DEFERRED to the integrator.
</content>
