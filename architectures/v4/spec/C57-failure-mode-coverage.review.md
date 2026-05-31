# Adversarial review — C57 Failure-mode coverage map & residual-risk register (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Security & Governance (the capstone register's honesty is load-bearing)
Target: [`spec/C57-failure-mode-coverage.md`](./C57-failure-mode-coverage.md) + [`plan-faithful/C57-failure-mode-coverage.md`](../plan-faithful/C57-failure-mode-coverage.md)
Charter: single canonical track → attack FIDELITY + COMPLETENESS (+ the capability-for-principle bar), not design.

## Summary of the attack

C57 is the v4 capstone register; its load-bearing property is **honesty** (no over-claimed "Addressed", a
complete and reconciled mode map, every gap/caution named). I verified the spec's central honesty claims
**against the actual catalog by mechanical tally**, and they hold with precision:

- **G38 (F15 missing).** Extracted all `| F\d+ |` rows from [`F-MODE-COVERAGE.md`](../F-MODE-COVERAGE.md):
  **exactly 60 distinct F-numbers; F15 is the only one absent** from F1–F61. The spec's "60 distinct, not
  61" is exact. ✓
- **G40 (double-counts).** F32, F35, F47 each appear in **exactly two** rows. F32 = **Addressed/Addressed**
  (two mechanisms, same status → an owner-duplication, not a status conflict); F35 + F47 = **Partial + §8
  Caution** (genuine status conflict). The spec's tie-break (Partial+Caution → `caution`; F32 → one owner
  C41) matches `ambiguities-and-gaps.md` G40 verbatim and is a faithful editorial rule. ✓
- **G39 (counts ≠ 61).** §10 headline literally reads 24+20+11+4 = **59**; the raw rows pre-dedup read 30
  "Addressed" + 18 "Partial". The spec's "59 ≠ 61" is exact (see RC57-03 for a completeness nit). ✓
- **F54 / G35 (the brief's over-claim trap).** Catalog status for F54 is **Partial** (CXDB history + Healer
  anomaly detection — a real but weak mechanism); the spec registers G35/F54 as `partial`/`caution` and
  registers the multi-cycle objective-drift **audit-pack as UNBUILT, homed at C57**. **It is NOT
  over-claimed "addressed."** The brief's "must be registered UNBUILT/gap, not addressed" bar is met. ✓
- **G31 (lethal-trifecta).** Registered `addressed`-with-caveat + the XC-8/D-18 exposure window, flagged as
  the run's loudest "no bare Addressed" entry; F12/F44/F56 link to it. Faithful to D-18 (boundary-typing →
  Phase-2 entry precondition; twin half → Phase-3c) and XC-8 (detection-only). ✓
- **G19 / C49** ("largely unsolved", "most significant invention", zero contract) — faithful. **FE-1..FE-5**
  — all five match `FUTURE-ENHANCEMENTS.md` (incl. FE-3 blocked on G37, FE-4 on Max ToS). ✓
- **Owners.** Every cited owning C-ID (C04/C05/C24/C28/C29/C39/C40/C41/C44/C46/C49/C50/C51/C54/C56) exists in
  the inventory; attributions (C41→F32 attribution, C46→cost-model gap, C50→F47 Goodhart) are plausible. ✓
- **The bar (over-build).** No CI gate, no SBOM/license scanner, no residual-risk service, no
  coverage-enforcement engine — the spec/plan explicitly DROP all of these and keep a hand-maintained
  Markdown artifact under git review. Correct. ✓
- **Scope.** C57 does **not** touch, mirror, or reference the repo-level `architectures/failure-modes.md`
  (grepped: zero C57 references there). Correct. ✓
- **Bindings.** D-1 (same-provider judge / cross-family = FE-1; F48 stays Partial), D-13, D-18, XC-8, and the
  prevent-vs-detect cross-component OQ (C43:OQ-C43-1 ≡ C34:OQ-C34-1) are all cited faithfully. No binding
  violated.

**No blockers. The register is honest and complete at sweep-1 altitude.** Findings are minor
fidelity-of-citation / completeness polish; one architecturally-significant item is correctly DEFERRED.

## Findings

### RC57-01 — minor — "F-MODE-COVERAGE §0 legend" cites a section number that does not exist
**Claim.** §4.1 table header and the §4.1 [FAITHFUL-FILL] both attribute the status enum to
"F-MODE-COVERAGE §0." **Evidence.** F-MODE-COVERAGE has **no §0** — its sections run §1–§12; the four status
definitions live in the **unnumbered preamble (lines 6–9)**. The definitions themselves are verbatim-faithful
(matched word-for-word against lines 6–9, modulo "doesn't"→"does not", which is why "verbatim *intent*" is
the right tag). So the *content* is faithful but the *locator* is invented — exactly the "mislabel a
locator" fidelity defect a capstone must avoid. **Fix (applied).** Re-cited both occurrences to
"F-MODE-COVERAGE's preamble legend (lines 6–9)" and noted the doc has no numbered §0 (sections §1–§12).

### RC57-02 — minor — the G35 build-vs-register ambiguity should quote C56:OQ-3's literal "+ mechanism" wording (it is the source of the tension)
**Claim.** The [AMBIGUITY: G35] block (§6) frames Reading B ("C57 builds the audit") as something C57 "could
be read as," then picks Reading A (register-only). **Evidence.** Reading B is not merely a loose possibility:
review-log **C56:OQ-3 literally says "C57 = objective-drift audit register *+ mechanism* (unbuilt, Batch
5)"** — the "+ mechanism" clause is the exact wording that creates the build-vs-register tension. The spec's
Reading-A pick is correct and faithful (the bar DROPS a running audit; the brief requires F54 registered
unbuilt), but the resolution is stronger when it quotes the contested phrase rather than paraphrasing it, so
the OQ-C57-3 deferral is grounded in the literal source. **Fix (applied).** Quoted C56:OQ-3's "+ mechanism"
wording in the [AMBIGUITY: G35] Reading-B clause, and added an explicit `DEFERRED — needs orchestrator
decision` marker to OQ-C57-3 pinned to that exact phrase. **The substantive build-vs-register decision stays
DEFERRED (OQ-C57-3, top OQ) — it is an architectural scheduling call above the register's altitude.**

### RC57-03 — minor — §4.3 G39 row cites only the §10 headline (59); the pre-dedup row reality (30/18) is the actual re-tally base
**Claim.** §4.3's G39 row states the defect as "24+20+11+4 = 59" (the §10 headline) and commits to a
re-tally to 61. **Evidence.** `ambiguities-and-gaps.md` G39 is more precise: the **raw rows pre-dedup read 30
"Addressed" + 18 "Partial"** (the §7 "overlap" row and the F32/F35/F47 double-counts inflate the row tally
over the headline). My own tally confirms 30/18 raw. The Reading-A re-tally (the spec's committed sweep-2
deliverable) must reconcile *both* the 59-headline and the 30/18 raw-row reality, or it re-imports the same
ambiguity it exists to fix. Citing only the headline understates the evidence the re-tally must reconcile.
**Fix (applied).** Added the 30/18 pre-dedup figure (with the §7-overlap + double-count explanation) to the
§4.3 G39 row, and noted the re-tally must reconcile both numbers.

### RC57-04 — minor — bare-text internal references in the spec's Source header (AGENTS.md violation)
**Claim.** The spec's Source/`> [...]` header refers to "F-MODE-COVERAGE.md", "FUTURE-ENHANCEMENTS.md",
"README", "AI-CONTEXT", "component-inventory", and the various OQs as **bare text**, not as relative markdown
links. **Evidence.** [`AGENTS.md`](../../../AGENTS.md) "Internal document references" requires every
cross-doc reference to be a descriptive **relative markdown link** ("see synthesis/00" is named as
not-acceptable). The C57 *plan* correctly uses a relative link for its spec ref; the spec's header does not.
**Fix (NOT applied — flagged).** This is the prevailing source-header style across the v4 corpus (every
component spec's `> Source:` block is bare-text), so unilaterally re-linking only C57's header would diverge
from the corpus without fixing the systemic issue; the header carries dense line-anchored citations whose
relative-link conversion is a corpus-wide editorial pass, not a single-component sweep-1 fix. **Flagged for
the integrator** as a corpus-style item (sibling to OQ-C57-5's "integrator edit pass" routing). Not a
fidelity defect in the claims themselves.

### RC57-05 — minor (note, no fix needed) — "Addressed-with-caveat" is a presentation of `addressed`, not a 5th enum value — verify it never breaks the single-status invariant
**Claim.** G31's register entry uses "status `addressed`-with-caveat", and §3/§4.1 define a closed 4-value
enum {addressed, partial, gap, caution}. **Evidence.** This is internally consistent — "addressed-with-
caveat" is `addressed` + a mandatory `residual`-column caveat (the "no bare Addressed" invariant), not a
fifth status — and the spec is explicit that the enum is closed at four. I checked it does not silently
introduce a 5th value: it does not. **No fix.** Recording it so a sweep-2 author does not mistake
"addressed-with-caveat" for a separate enum member when building the on-disk status encoding (§4.2). The
single-status invariant holds.

## Verdict

**accept-with-fixes.** The capstone register is **honest and complete** at sweep-1 altitude: every honesty
claim the brief flagged was mechanically verified against the catalog and holds — F15-missing (G38),
F32/F35/F47 double-counts (G40), 59≠61 (G39), F54 registered UNBUILT-not-addressed, G31 addressed-with-caveat
+ XC-8/D-18 exposure window, G19/C49 unsolved, FE-1..FE-5, and no over-build into an enforcement engine /
SBOM scanner / residual-risk service. C57 does not touch the repo-level `failure-modes.md`. All findings are
minor fidelity-of-citation / completeness polish; four are **fixed in place** (RC57-01 invented "§0";
RC57-02 quote C56:OQ-3's "+ mechanism" + DEFERRED marker; RC57-03 add the 30/18 pre-dedup re-tally base) and
**one architecturally-significant item is correctly DEFERRED** (OQ-C57-3 / F54-objective-drift ownership →
orchestrator). RC57-04 (bare-text Source-header refs) is **flagged for the integrator** as a corpus-wide
style item, not unilaterally changed. Nothing dishonest; nothing over-claimed; no binding violated.
