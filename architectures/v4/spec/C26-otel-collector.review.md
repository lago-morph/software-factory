# Adversarial review — C26 OTel Collector (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Observability (C26 collector; the C25→C26 and C26→C27 seams)
Target: spec/C26-otel-collector.md (+ plan-faithful/C26-otel-collector.md)
Charter: single canonical track; Track-A posture → attack FIDELITY + COMPLETENESS (not the design),
PLUS the capability-for-principle bar (flag hardening-on-existing-stack-capability that isn't new
capability tied to a 12-principle; when in doubt → DROP). Gap in scope: **G04**.
THE BAR for C26: it IS the off-the-shelf OpenTelemetry Collector (config + pipeline YAML, no custom code).

## Summary of the attack surface checked
- **THE BAR**: is C26 kept to *config + topology + invariants*, or does it re-grow a custom
  buffer / retry / back-pressure / queue / processor duplicating native Collector features?
- **Two-sink (G04)**: INV-1 (single LangFuse sink) + INV-2 (Collector ✗→ CXDB anti-edge), and their
  cross-consistency with C25 INV-1 and C24's framing.
- **The C26→C27 export seam (OQ-1)**: is C26's described exporter (type/endpoint/auth + **signal set**)
  consistent with how C27 describes its OTLP ingestion? Including non-trace (metrics/events) handling.
- **Citations** to AI-CONTEXT / README (every load-bearing line spot-checked against source).
- **Binding decisions D-1..D-5**: does C26 violate any? (No — see verdict.)

## Findings

### RC26-01 — major — RESOLVED by D-11 — C26 routes metrics+events to LangFuse and asserts they "appear in LangFuse" (AC-5); C27's ingestion is trace-only, so the C26→C27 seam is inconsistent on signal coverage

> **RESOLVED by D-11 (integrator pass 2026-05-31).** LangFuse ingests **TRACES only** (verified vs LangFuse OTel docs). C26 exports the trace signal to C27/LangFuse; metrics/events received by C26 are **not asserted to appear in LangFuse** (forwarded best-effort, or not routed) and **never** to CXDB (two-sink anti-edge holds). Seam transport = OTLP/HTTP + HTTP Basic auth (base64 `public:secret`); only the path/headers remain for sweep-2. Applied to C26 §3.2/§3.3/§5/AC-5/OQ-1.
**Claim.** C26 §3.3 wires **three** pipelines — metrics, logs/events, and beta traces — each terminating
at `otlphttp → LangFuse (C27)`, and **AC-5** asserts "the metric set and event set C25 emits … traverse
the pipeline and **appear in LangFuse**." §5 ("Export (single sink)") says "every signal accepted at the
receiver … is delivered to LangFuse." **Evidence.** The downstream spec C27 describes its ingestion as
**trace-only**: §3.1 Payload = "OTLP **traces** (LangFuse ingests OTLP-trace spans)"; §1 FAITHFUL-FILL
names LangFuse's **native OTLP-*trace* ingestion endpoint** (`/api/public/otel`); and C27's own **OQ-1**
explicitly flags "what happens to metrics/events vs traces — LangFuse is **trace-oriented**, so non-trace
OTLP signals **may not be browsable there**." So C26 promises metrics/events land *and appear* in LangFuse
while C27 (and LangFuse natively) only commits to traces. This is a real seam mismatch (OQ-1 is shared
between the two specs but the two specs currently make **different** claims about it): C26's AC-5 is an
over-claim relative to what C27 supports, and a builder following C26 verbatim would write a fixture
assertion ("metrics appear in LangFuse") that C27 cannot satisfy. **Fix (applied).** Qualified C26 §3.3
(metrics + logs/events rows and the post-table note), §3.2 postcondition, §5 export note, and AC-5 so
that: traces are the signal LangFuse browses; whether LangFuse **ingests/exposes** non-trace OTLP
(metrics/events) is the **open seam item (OQ-1, shared with C27)** — C26 forwards what it receives, but
the spec no longer *asserts* metrics/events are browsable in LangFuse. Tightened OQ-1 to name the
non-trace-signal question explicitly and point at C27 OQ-1 so the two specs resolve **one** seam. The
architecturally-significant half (does the pipeline drop/route non-trace signals elsewhere, or does
LangFuse ingest them?) is **DEFERRED — needs orchestrator decision** (see DEFERRED note below); only the
over-claim wording is fixed in place.

### RC26-02 — minor — §3.2 / pipeline table assert the exporter type is `otlphttp` as if v4 stated it; it is a [FAITHFUL-FILL], and the bare-prose assertions aren't tagged
**Claim.** §3.2 states "the Collector's `otlphttp` exporter targets that endpoint" and the §3.3 pipeline
table names `otlphttp → LangFuse` in every row, in the same register as the v4-sourced facts. **Evidence.**
v4 says only "point the OTel Collector at [LangFuse]" (README:540) and `OTel --> LF` (README:412) — it
names **neither** the exporter type (`otlphttp` vs `otlp`/gRPC) nor the transport. C26 §3.2 *does*
parenthetically call the path "a C27-side detail resolved at sweep 2" and the §3.3 FAITHFUL-FILL covers
"per-signal pipelines / processors," but the **exporter-type choice itself** (`otlphttp`) is presented as
settled fact in the table and §3.2 prose, not flagged as the inference it is. This mirrors the exemplar
defect the C25 review corrected (RC25-03: qualify an inferred/native property as such, don't assert it as
v4 fact). It is consistent with C27's reading (HTTP ingestion), so substance is fine — only the labeling
overstates certainty. **Fix (applied).** Reworded §3.2 and the §3.3 note to mark `otlphttp` (HTTP
transport to LangFuse) as the **faithful-fill default** consistent with C27's HTTP ingestion, with the
exact exporter block + transport co-frozen at sweep 2 (OQ-1) — so the type is no longer read as a v4-stated
fact. No scope change.

### RC26-03 — minor — INV-1 "All received OTLP terminates at LangFuse" reads as a delivery guarantee a config-only forwarder can't make; reconcile with the native best-effort semantics stated two sections later
**Claim.** INV-1 (§3.4): "**All** received OTLP terminates at LangFuse and nowhere else." §3.2
postcondition: "**Every** signal accepted at the receiver … **is delivered** to LangFuse." **Evidence.**
§4 (Consistency) and §6 (LangFuse-down) correctly state delivery is **best-effort per the Collector's
native export semantics** — on a down sink the Collector queues/retries and **drops when the queue is
exhausted** (INV-3). So "every received signal **is delivered**" overstates: under the very failure mode
C26 itself documents, some signals are dropped, not delivered. The *routing* invariant (terminates at
LangFuse **and nowhere else** — no second/CXDB sink) is the load-bearing, correct part; the *delivery*
phrasing is what overreaches. This is the same "config-only interface can only assert a native property,
not guarantee an outcome" correction the C25 exemplar took (RC25-03). **Fix (applied).** Reworded INV-1
and the §3.2 postcondition to scope the invariant to **routing** ("the only terminal sink on the pipeline
is LangFuse; nothing is routed anywhere else") and made the *delivery* clause explicitly best-effort /
native-queue-and-retry (cross-ref INV-3 / §6), so the strong word ("every … delivered") no longer
contradicts §6. The single-sink claim — the half that matters for G04 — is unchanged and kept strong.

### RC26-04 — minor — INV-2 / AC-3 cite the rejected OTLP→CXDB path but weld two distinct AI-CONTEXT facts; keep them split (the exemplar's RC25-01 correction)
**Claim.** INV-2, §2 (anti-dependency row), §6 (G04 row), and AC-3 cite the CXDB anti-edge as, e.g.,
"AI-CONTEXT:210, 466, 497" as a bundle. **Evidence.** These are **two** different facts and C26 already
mostly keeps them apart, which is good — but the bundling in a couple of spots risks the exact conflation
the C25 review fixed (RC25-01): line **210** is §5.2 "**no native OTLP receiver** … positioned *against*
OTel"; the **rejection** decision is §11.1 line **466** ("Skip OTLP → CXDB path: Yes") + §11.3 line **497**
("OTLP path for Claude Code → CXDB … Span tree vs turn DAG impedance"). All three lines verified exact
against source. C26's substance is correct and it cites more carefully than C25 originally did; this is a
hygiene nit, not a factual error. **Fix (applied).** Where the three were bundled, annotated the split
inline (210 = no-receiver fact; 466/497 = the rejected-path decision) so C26 matches the corrected C25
locator convention. Substance unchanged.

### RC26-05 — minor (no change; recorded) — `README §13.1` / `Part-4` section labels are asserted but the README uses prose Part/Phase headings; line numbers are exact
**Claim.** The §1 header cites "README §13.1 Phase 1" and "README Part-4 OSS table (line 297)."
**Evidence.** Every **line number** C26 cites in README (297, 386, 411–412, 539–540) is **exact** (verified
against source: 297 = the `OpenTelemetry Collector | Apache 2.0 | Clean` row; 411–412 = `CC -->|OTLP| OTel`
/ `OTel --> LF`; 539–540 = the install checklist). The **section labels** "§13.1"/"Part-4" are a shared
convention C25/C26/C27 all use; the README's own headings are prose, not numbered "13.1." Because the
load-bearing line numbers are correct and the label is a corpus-wide convention (identical to the C25
exemplar — RC25-05 recorded the same), this is below the fix bar. **No fix; recorded for the sweep-2
citation-normalisation pass** (one canonical README section-label scheme across the Observability specs).

## Non-findings explicitly checked (held up under attack)
- **THE BAR is respected — no over-build.** C26 authors **no** custom collector code: §1 ("not custom
  software, a buffering layer, or a retry/back-pressure engine"), INV-3 (verbatim OSS, config-only), §4
  (no custom buffer; only the Collector's native queue), §6 (LangFuse-down → **native** sending-queue +
  retry, "adds none"), AC-6/AC-7, and plan T-tasks (all "config-and-verify only"; risk #3 names the
  over-build trap and DROPs it). The dropped pieces stay dropped — no bespoke buffer, retry, or processor.
  This is the correct posture under the bar and mirrors C25.
- **Two-sink (G04) is correct and cross-consistent.** C26 INV-1 (single LangFuse sink) + INV-2 (anti-edge
  Collector ✗→ CXDB) match **C25 INV-1** (split asserted at the emitter) and **C24** (raw-bodies→CXDB is
  the separate sink; C24 never sends spans to CXDB). The division of labour — C25 owns the *split*, C26
  owns the *anti-edge enforcement* where a naive integrator would physically add the CXDB exporter, C24 is
  the *other* sink — is coherent and matched by C26 OQ-2 ↔ C25 OQ-1. The §5 diagram's severed `…x` edge to
  CXDB and AC-3 (the G04 anti-edge check) make the rejected path explicit. G04 is the only gap in C26's
  row and it is addressed (INV-1 + INV-2 + AC-3 + OQ-2).
- **Receiver side is faithful.** §3.1's `:4317` gRPC default + optional `:4318` HTTP matches AI-CONTEXT:164,
  167, 578; the three-signal set (metrics / events-logs / beta traces) matches AI-CONTEXT:172–174; the
  `[[service]] otel_collector type="external" endpoint=:4317` declaration matches AI-CONTEXT:563–566; the
  C25→C26 `OTEL_EXPORTER_OTLP_ENDPOINT` pointing matches AI-CONTEXT:575–579. mTLS option matches
  AI-CONTEXT:169. Correlation attributes (INV-4) match AI-CONTEXT:178.
- **D-1..D-5 not violated.** C26 touches none of: judge provider (D-1), bundle-id namespace (D-2),
  bead-type ownership (D-3), C19↔C20 direction (D-4), C41↔C23 hash-chain (D-5).
- **Plan mirrors the spec faithfully.** T1–T9 are config-and-verify only; T5 is the G04 single-sink +
  anti-edge proof; the de-risking order leads with G04 (#1) and the over-build trap (#3); the C26→C27 seam
  is flagged as the shared fan-out coordination (T3 / OQ-1). The AC-5 signal-coverage over-claim (RC26-01)
  recurs in plan T4 DoD ("signal coverage … traverses to LangFuse"); qualified there too for consistency.

## Verdict
**accept-with-fixes.** C26 is a faithful, well-traced match to the C25 exemplar: the config-not-code bar
is held with zero over-build (the standing trap for this component — a custom buffer/retry — is explicitly
refused), the G04 two-sink boundary + CXDB anti-edge are correct and cross-consistent with C25/C24, and
every load-bearing citation is exact. **One major (RC26-01):** the C26→C27 seam is inconsistent on
**non-trace signal coverage** — C26 asserts metrics/events "appear in LangFuse" while C27 (trace-oriented)
does not commit to ingesting/browsing them; the over-claim wording is **fixed in place**, but the
substantive question (does LangFuse ingest non-trace OTLP, or are metrics/events dropped/routed elsewhere?)
is **DEFERRED** to the orchestrator as it needs **joint C26↔C27 resolution** at the seam (OQ-1) — it is
exactly the kind of architecturally-significant, cross-component item the charter says to defer. The four
minors (exporter-type fill labeling RC26-02, INV-1 delivery-vs-routing RC26-03, the split-cite hygiene
RC26-04) are fidelity/hygiene-class and **fixed in place**; RC26-05 (README section-label) is recorded for
the sweep-2 citation pass, not fixed.

### RESOLVED by D-11 (was: DEFERRED — RC26-01, the C26↔C27 seam)
The C26→C27 seam's **signal-coverage** half is now settled: **D-11 — LangFuse ingests TRACES only** (verified
vs LangFuse OTel docs). C26 exports the trace signal to C27/LangFuse; the metrics/events pipelines are
**forwarded best-effort or not routed** and are **not asserted to appear in LangFuse**, and **never** routed
to CXDB (INV-2 holds — the two-sink anti-edge). Of the orchestrator's two options this is **(A)**. Seam
transport is also settled (OTLP/HTTP + HTTP Basic auth, base64 `public:secret`; no gRPC); only the exact
ingestion path + `x-langfuse-ingestion-version` header remain a sweep-2 exporter-mechanics detail. Applied to
C26 §3.2/§3.3/§5/AC-5/§9 OQ-1; C27 already states traces-only (RC27-01).
