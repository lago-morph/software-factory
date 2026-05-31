# Adversarial review — C46 Meta-Metric Stream (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Optimization / Cost
Target: spec/C46-meta-metrics.md (+ plan-faithful/C46-meta-metrics.md)
Charter: single canonical track → attack FIDELITY + COMPLETENESS (not design), **plus** THE BAR
(flag any custom metrics/time-series engine; the keep = the cost MODEL definition (G32) + the
meta-metric stream defs). Assigned gaps: **G09, G32**. Binding in force: D-6, D-15, D-19.

## Findings

### RC46-01 — major — the cost/usage signal (C46's core G32 input) is sourced from the wrong telemetry path and the wrong side of the bridge
**Claim.** Across §1, §2, §3 (I2), §4, §5 (record step 2) and §6 the spec asserts C46 reads "per-run usage
(tokens, latency)" from "the telemetry path (**C24**/CXDB)" and names **C24** as the usage source / read seam.
**Evidence (two coupled fidelity errors).**
(a) **Token usage + cost are native OTLP *metrics*, not C24's payload.** AI-CONTEXT:172 lists the OTLP metric
set as "session count, lines of code, PRs, commits, **costs, token usage**, edit decisions, **active time**";
spec/C25 §3.3 (line 70) repeats it. That metrics stream flows **C25 (emit) → C26 (OTel Collector)** on a 60s
cadence (per D-11, LangFuse takes traces; metrics are best-effort). The **C24 raw-API-bodies→CXDB bridge**
carries *untruncated conversation bodies* (AI-CONTEXT:176 "Conversation-shaped, ideal for CXDB ingestion"),
**not** the metrics stream. Token counts are *recoverable* from the body JSON, but the spec presents C24/CXDB
as the authoritative usage feed and never reconciles that cost/tokens natively live on the OTLP-metrics path.
(b) **C24 is the *write* bridge; the CXDB *read* seam is C21.** spec/C24 §1 (line 65) states verbatim:
"**C36/C37/C38/C49 read from C21, not from C24**." The sibling metric-reader C36 follows this exactly (C36
review:79 "read from **C21** … provenance **C24**"). C46 instead names C24 as the thing it *reads*, which is
the wrong side of the bridge.
**Why major (not blocker).** C46's *cost MODEL* (I1, the G32 deliverable) is correct and unaffected — only
*where its raw token/cost inputs come from* is mis-specified; and the inventory pins C46's dep as **C24**, so
the prose drifted from the surrounding telemetry topology even though §4/§6 already hint at C25/C26/C21.
**Fix (applied + deferred).** Applied in spec §1 (NOT-source bullet), §2 (split the dep row; added C25/C26
metrics row + C21 read-seam row), §3 I2, §4 data-model row, §5 step 2, §6 G32 attribution clause — all now
say token/cost is natively an OTLP metric (C25→C26) and the CXDB read seam is **C21** (C24 = writer/
provenance), mirroring C36. Mirrored into the plan (T4, dep-graph C24 line, §6 OQ roster). The
**architecturally-significant** residual — does C46 read the metrics path (C25/C26) or the CXDB bodies (C21),
and should the **pinned dep edge** read C21/C25 rather than/in addition to C24 — is **DEFERRED** as new
**OQ-6** (spec §1/§9, plan §6) → **needs integrator decision** (touches the inventory dep edge).

### RC46-02 — minor — "wall-clock time" cost-dimension conflated with the time-to-threshold metric's cross-run clock
**Claim.** §6 (old line 266) said the cost-vector's "**wall-clock time**" is "**the basis for
time-to-threshold**." **Evidence.** Two different clocks: the cost-vector's wall-clock time is *one run's
elapsed duration* (a cost — how long a unit of work took; AI-CONTEXT:172 "active time"), whereas
time-to-threshold (§1 line 46, §5 step 3) is *cumulative elapsed time/run-count **across** the run-sequence*
for satisfaction to cross a cutline — a trend over many runs. Calling the per-run cost dimension the "basis
for" the cross-run metric muddles the cost model. **Fix (applied).** Reworded the cost-vector bullet to
define wall-clock time as each run's *elapsed duration* and added an explicit note distinguishing it from
time-to-threshold's cumulative cross-run clock.

### RC46-03 — minor — source-header line citation off-by-two (README:263 vs 265)
**Claim.** The §-source header cited "**line 263** 'The system measures its own meta-performance…'."
**Evidence.** README:263 is the `### Principle 12 — Self-optimization` **header**; the quoted sentence is on
README:**265**. (All other header citations verified exact: README:269 definition row, :270 tracking/MLflow,
:278 "Build last", :470 Phase 3d; AI-CONTEXT:353/378/516.) **Fix (applied).** Header now reads "line 263
§-header; line 265 '…measures its own meta-performance…'."

### RC46-04 — minor (no-op / confirm) — OQ-1 title names only the dollar dimension though it also carries the shared-cutline (G09) deferral
**Claim.** OQ-1's header is titled "G32 cost-model **dollar dimension** + price reference," but the §6
[AMBIGUITY: G09] block also routes the **time-to-threshold cutline value** through "OQ-1, shared with
C33:OQ-1." **Evidence.** C33:OQ-1 (review-log:209) is indeed the shared G09 cutline-value question, and C46's
sharing of it is correct; both the dollar-dimension and the cutline-value deferrals are explicitly flagged —
the only nit is that they ride one OQ whose title names just the dollar dimension. Nothing is lost.
**Fix.** None needed — left as-is (cosmetic; both deferrals are visible and correctly routed).

## Verdict
**accept-with-fixes.** This is a strong, faithful, well-traced spec that nails its mandate: it is **the bar's
poster child** — it explicitly refuses a custom time-series/metrics engine (INV-6/AC-7), a significance engine
(→C48, D-19), a promotion gate (→C50), token metering (→C24/C25/C26), and per-criterion meta-metrics (FE-5/
D-15), keeping only the two pieces v4 names as "your work": the **cost-model definition** (G32) and the
meta-metric **stream defs + cross-stack glue**. **G32 is genuinely resolved**: cost = vector {tokens, $, time}
÷ the C33 satisfaction term, with the dollar nuance handled *honestly* — tokens/time exact, $ = modelled
tokens×reference-price = operator policy, explicitly **not** claimed exact under flat-rate Max (§6 "What stays
open", OQ-1, AC-2). **G09** is correctly an *input* duty: satisfaction consumed from C33 (D-15 holistic), and
time-to-threshold *consumes* a cutline owned by C50/C53/C39 (reading (b), INV-4/AC-6) — no anti-P6 verdict
re-introduced. Citations to README/AI-CONTEXT/F-MODE (F47/F60/F40/F48) and the cross-spec deferrals (C29/C28/
C32/C37/C38/C55 → C46) all verify. One **major** fidelity fix applied (cost signal mis-routed to C24's
bodies-path instead of the OTLP-metrics path, and to the C24 writer instead of the C21 read seam) with the
dep-edge correction **deferred to the integrator as OQ-6**; two minor clarity fixes applied; one cosmetic
no-op. No bar violation, no invented capability — the one architecturally-significant item (OQ-6) is left
flagged, not silently changed.
