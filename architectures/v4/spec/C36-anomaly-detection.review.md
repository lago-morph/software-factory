# Adversarial review — C36 Anomaly Detection (numeric) (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Healing Loop
Target: spec/C36-anomaly-detection.md (+ plan-faithful/C36-anomaly-detection.md)
Charter: canonical single-track → attack FIDELITY and COMPLETENESS (not design), PLUS the
capability-for-principle bar (HANDOFF §2): flag any addition hardening existing stack capability rather
than new capability tied to a 12-principle. Gap in scope: **G33** only.

## Findings

### RC36-01 — major — the C36↔C37 population seam is asserted as settled (C36 selects the set C37 clusters) but is an open question; it silently contradicts C37's own OQ-1
**Claim.** §2 (downstream row) states C37 "Consumes C36's anomaly signal — embeds + clusters **the flagged
failures**" and "the **anomaly→cluster trigger seam is C36's signal (I3)**"; I3 calls itself "the **trigger**
C37/C38 consume." This presents, as fact, that C36 *selects* the trajectory population C37 clusters.
**Evidence.** The sibling spec **spec/C37-trajectory-clustering.md** raises exactly this as its **OQ-1**
(lines 357–360): *"Does **C36** (anomaly detection) **select** the trajectory population C37 clusters … or does
C37 cluster a broader trajectory set with C36 scoring numerically in parallel? The exact hand-off (what C36
passes C37) is unspecified in v4 … freeze at sweep-2 **with C36**."* The inventory has **C37 `depends on` C21**,
not C36 (component-inventory:49) — i.e. C37 reads trajectories from C21 directly, so "C36 selects C37's input"
is *not* forced by the dependency graph. v4 itself only states the ordering "Observability → anomaly →
diagnosis" (README:248); it never says the anomaly detector hands the clustering step its population. So C36's
spec takes one side of a two-sided, explicitly-open seam and states it as established — the precise "silently
assumed instead of named as an OQ" failure this review is charged to catch. (The brief's SEAM check.)
**Fix (applied).** (a) Added **OQ-5** to §9 naming the C36↔C37 population seam and cross-referencing C37 OQ-1
("freeze jointly at sweep-2"). (b) Softened the §2 downstream-C37 row and the I3 description from asserting
C37 clusters "the flagged failures" to "C37 consumes C36's anomaly signal; **whether C36's flagged set
*selects* C37's clustering population or C37 reads a broader set from C21 in parallel is OQ-5 (= C37 OQ-1)**."
The *signal contract* (I3 carries what/score/provenance) is unchanged and kept — only the unstated claim that
the signal **scopes C37's input** is demoted to the OQ it is.

### RC36-02 — minor — §10 license-table line citations (310/311) point at the wrong rows
**Claim.** The §"Source" header cites "§10 license table (line 310 'PyOD | BSD-2-Clause | Clean'; line 311
'Anomalib | Apache 2.0 | Clean')."
**Evidence.** AI-CONTEXT:310 is `LLM instrumentation | OpenLLMetry, OpenInference | Apache 2.0 | Mature` and
:311 is `Claude Code instrumentation | Native OTLP via env vars | n/a (Anthropic) | Native` — neither is the
PyOD/Anomalib license row. The license *values* (PyOD BSD-2, Anomalib Apache-2.0) are nonetheless correct and
are supported by the rows that the spec **does** cite accurately (README:253 "BSD / Apache 2.0"; AI-CONTEXT:327
"BSD-2/Apache 2.0"). So this is a stray wrong line-number, not a wrong fact.
**Fix (applied).** Replaced the bogus "line 310/311" parenthetical with the correct supporting cites
(README:253; AI-CONTEXT:327) so the license claim is traceable and no citation points at an unrelated row.

### RC36-03 — minor — "a future-track item" (line 86) lightly resurrects the retired Track-A/B vocabulary (D-6)
**Claim.** §1 boundary: the LLM-trajectory/semantic anomaly layer "is a later P11 surface (**a future-track
item**; it composes *on* C36, OQ-3)."
**Evidence.** Post-convergence there is one canonical track and **D-6** directs specs not to frame against a
live alternate track. "future-track" is not the dead Track-A/B split in substance (it means "a deferred later
surface"), but the word needlessly reintroduces "track" framing a careful reader could misread.
**Fix (applied).** Reworded to "a **later/deferred P11 surface**" — same meaning, no track vocabulary;
consistent with D-6 and with OQ-3's own "separate later P11 surface" phrasing.

### RC36-04 — minor — F22 is marked "Addressed" (not Partial) in F-MODE-COVERAGE; the spec's "underwrites the numeric-detection half" framing is correct but worth an explicit half-ownership note
**Claim.** §6 lists C36 as underwriting "**F22** (zombie agents …) — the mode most directly named to C36" and
groups it with the Partial drift modes.
**Evidence.** F-MODE-COVERAGE:44 marks F22 **Addressed** (full), with the row spanning *both* "anomaly
detection on session liveness (PyOD on telemetry)" **and** "Tracker-style diagnosis." The spec is in fact
faithful — it explicitly says C36 owns only the *numeric-detection half* and routes diagnosis to C38, and
C38's spec concurs (spec/C38:235 "detection is C36, diagnosis is C38 | Addressed (diagnosis half is C38)"). The
only risk is a skim reading C36 as owning F22 wholesale and inheriting its "Addressed" status.
**Fix (applied).** Tightened the §6 F-mode note to say C36 underwrites the **PyOD-on-telemetry detection half**
of F22 (status "Addressed" is **joint with C38's diagnosis half**), so the half-ownership is explicit and the
status is not mis-attributed to C36 alone. No substantive change; clarity only.

## Verdict
**accept-with-fixes.** Strong, faithful, and unusually disciplined on **the bar** — INV-1, the §6 DROP list,
and INV-4 each explicitly refuse the two textbook traps (a custom anomaly estimator; a C36-side durable
buffer), keeping the *only* custom surface as the watched-metric wiring + the anomaly-signal contract, exactly
as charged. The metric-stream read seam is handled correctly and consistently with both deps (read from **C21**
I6, provenance **C24** — spec/C24:65; named at OQ-1), and **G33** is honestly discharged as a read-side
inheritance (fail-open / skip-and-re-derive; durability deferred to C24/C21 with the inbox/disk ceiling
acknowledged). AC-1…AC-9 are testable. The one real defect is **RC36-01**: C36 stated as settled a
cross-component population seam that its own consumer (C37) flags as open — fixed in place by demoting it to a
cross-referenced OQ-5 and softening the two assertions, with the signal contract itself preserved. Remaining
fixes are citation/vocabulary hygiene. **Nothing architecturally significant left deferred** — the seam
resolution itself (which side wins) is correctly an orchestrator/sweep-2 call, now recorded as OQ-5 rather than
silently decided.
