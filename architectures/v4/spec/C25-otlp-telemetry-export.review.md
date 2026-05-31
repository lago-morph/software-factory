# Adversarial review — C25 OTLP telemetry export (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Observability (C25/C26/C27 + the C24 seam)
Target: spec/C25-otlp-telemetry-export.md (+ plan-faithful/C25-otlp-telemetry-export.md)
Charter: single canonical track; Track-A posture → attack FIDELITY + COMPLETENESS (not the design),
PLUS the capability-for-principle bar (flag hardening-on-existing-stack-capability that isn't new
capability tied to a 12-principle; when in doubt → DROP). Gap in scope: **G04**.
Note: C25 is the EXEMPLAR the C26/C27 builders matched — reviewed at least as hard as the rest.

## Summary of the attack surface checked
- **Two-sink (G04 / INV-1)** vs the source docs and the sibling specs.
- **The BAR**: is C25 kept to *config + the topology fact*, or does it re-grow the dropped daemon /
  fail-safe / single-endpoint-hardcode / raw-bodies machinery?
- **Citations** to AI-CONTEXT / README (every load-bearing line spot-checked against source).
- **Cross-consistency** with C28 (emitter), C24 (raw-bodies consumer), C26 (collector anti-edge).
- **Binding decisions D-1..D-5**: does C25 violate any? (No — see verdict.)

## Findings

### RC25-01 — minor — the rejected OTLP→CXDB path is mis-cited as "AI-CONTEXT §11.3 / line 210"
**Claim.** §6 (G04 F-mode row) and §9 (OQ-1) cite the explicitly-rejected OTLP→CXDB path as
"AI-CONTEXT §11.3 / line 210." **Evidence.** Line 210 is in **§5.2** ("**no native OTLP receiver**…
positioned *against* OTel"), not §11.3. §11.3 ("Considered and rejected") runs lines 490–502, and the
relevant row — "OTLP path for Claude Code → CXDB … Span tree vs turn DAG impedance" — is **line 497**;
the made-decision twin is §11.1 **line 466** ("Skip OTLP → CXDB path: Yes"). So the compound cite
"§11.3 / line 210" pins §11.3 to a line that belongs to §5.2 — two different facts welded into one
wrong locator. The matched sibling C26 cites these correctly and *separately* ("AI-CONTEXT:466, 497"
for the rejection; ":210" for the no-receiver fact). Because C25 is the exemplar, the sloppy locator is
worth correcting even though the *substance* (CXDB has no OTLP receiver; the OTLP→CXDB path is rejected)
is right and did not propagate the error to C26. **Fix (applied).** Split the cite everywhere it
appears: "no OTLP receiver" → AI-CONTEXT:210 (§5.2); "OTLP→CXDB rejected" → AI-CONTEXT §11.1:466 + §11.3:497.

### RC25-02 — minor — stale "C26/C27 specs not yet written" + a missed cross-reference to C26's anti-edge (INV-2)
**Claim.** §1 source header parenthesises the "downstream C26 collector / C27 LangFuse specs (**not yet
written at this sweep**)." **Evidence.** Both `spec/C26-otel-collector.md` and `spec/C27-langfuse-traces.md`
exist (authored this wave). More substantively: C25's own OQ-1 commits to "state the split in C25 (the
source) and **cross-reference from C24/C26**," and C26 OQ-2 mirrors it ("state the *split* at C25, the
*anti-edge* at C26"). The G04 *enforcement* edge — "Collector ✗→ CXDB" — is C26 **INV-2**; C25 asserts the
split but never points at where the anti-edge is actually enforced, so the promised cross-reference is
half-built. **Fix (applied).** Updated the parenthetical to "authored this wave" and added a one-line
cross-reference from INV-1 to C26 INV-2 (the anti-edge) and C24 INV-6 (no-spans-to-CXDB), so the three
specs visibly assert one boundary.

### RC25-03 — minor — INV-3 / §3.3 say C25 "must guarantee" `session.id`; a config-only interface can only assert a native property
**Claim.** §3.3 ("C25 **must guarantee** it is present on the raw bodies / signals"), §5 ("carrying the
`session.id` correlation key (INV-3)"), and INV-3 ("C25's contract **guarantees** the correlation
attributes are emitted") frame `session.id` emission as something C25 enforces. **Evidence.** The
correlation attributes are **Anthropic-native** — emitted by Claude Code's built-in exporter
(AI-CONTEXT:178), and C25's own §1/INV-2 are emphatic that C25 "**is not** an OTLP exporter
implementation… does not implement OTLP; it configures Claude Code's built-in exporter." A config-only
interface cannot *guarantee* the binary emits a field; it can only **assert/rely on** the native property
and **verify** it in the fixture (AC-5). This is exactly the exemplar defect the C23 review already
corrected (RC23A-03: "qualify an *adopted* property as such rather than asserting it as a guarantee the
spec independently enforces"). Asserting a guarantee here slightly overstates C25's reach and is the kind
of wording that, in the exemplar, downstream builders copy. **Fix (applied).** Reworded INV-3 and the
§3.3 line to: C25 **relies on / asserts** the native exporter emits the correlation attributes (incl.
`session.id`) and the Phase-1 fixture **verifies** it (AC-5); the *mapping rule* to CXDB's parent pointer
remains C24's (G26). No scope added; the claim is now sized to what a config interface can hold.

### RC25-04 — minor — "first stage of the observability pipeline" elides that the two sinks diverge at the *emitter*, not at a later stage
**Claim.** §1 calls C25 "the **first stage** of the observability pipeline C25 → C26 → C27, and it
simultaneously feeds C24." **Evidence.** Correct and consistent with README:411–413 (the diagram forks at
**CC** — the emitter — into `OTLP| OTel` and `raw bodies| Bridge`). The sibling C26 spec leans on this
precise fact ("the two sinks **diverge at C25, not at C26**"). C25 states the fork but never says, in so
many words, that the *divergence point is C25 itself* — which is the load-bearing half of G04 (a naive
integrator who thinks the split happens "downstream" is exactly who wires OTLP→CXDB at the collector).
The fact is *implied* by the §5 Mermaid (two edges leave `CC`) but not stated in prose. **Fix (applied).**
Added a half-sentence to §1/INV-1 making explicit that the two sinks **fork at the emitter (C25/C28),
not at any later stage** — matching C26's "diverge at C25" framing so the two specs are word-for-word
aligned on the divergence point.

### RC25-05 — minor (no change; recorded) — `README §13.1` section label is asserted, not verified; line numbers are exact
**Claim.** The §1 header and §5/§9 cite "README §13.1 Phase 1." **Evidence.** Every *line number* C25
cites in README (386, 411–413, 539–541) is exact (verified against source). The *section number* "§13.1"
is a label C25 and C26 both use; I could not confirm the README's own heading is numbered "13.1" (README
uses prose Part/Phase headings around these lines). Because (a) the line numbers — the load-bearing part —
are correct, and (b) C26 uses the identical "§13.1" label (shared convention, not a unique C25 slip),
this is below the fix bar. **No fix; recorded for the sweep-2 citation-normalisation pass** (decide one
canonical README section-label scheme across the Observability specs).

## Non-findings explicitly checked (held up under attack)
- **Two-sink INV-1 is correct and cross-consistent.** OTLP terminates at C26; CXDB is fed *only* via
  raw-bodies→C24; OTLP→CXDB is never wired (§1, §2, §3.2, INV-1, §5 diagram's severed `…x` edge, §6, AC-6).
  Consistent with **C26 INV-1** (single LangFuse sink) + **C26 INV-2** (anti-edge Collector ✗→ CXDB) and
  with **C24** (§1 "OTLP → CXDB explicitly rejected… C24 never sends spans to CXDB"; C24 **INV-6**). The
  division of labour — C25 owns the *split*, C26 owns the *anti-edge enforcement* — is coherent and
  matched by C26 OQ-2. No contradiction across the three.
- **THE BAR is respected — no over-build.** INV-2 is config-only activation; the dropped pieces stay
  dropped: no mandatory-on/fail-safe operator policy (C25 says off = unset the var, AC-7), no
  single-endpoint hard-coding (endpoint is the `OTEL_EXPORTER_OTLP_ENDPOINT` var, three protocols named),
  no raw-bodies escape-hatch *machinery* (file protocol/retention explicitly deferred to C24, §4 + OQ-2),
  and OQ-3 **declines to add** an emit-side buffer v4 doesn't name. This is the correct posture under the
  bar (native stack already provides the exporter; adding custom code would be hardening, → DROP).
- **Env-var contract is faithful.** §3.1 matches AI-CONTEXT:161–180 + §13.2:575–579 exactly; the
  five-required / rest-optional [FAITHFUL-FILL] is a sound minimal reading (575–579 is the block v4 ships).
- **C28 consistency.** C28 §1 ("NOT the telemetry exporter… C25 owns the export config"), I/F #5
  ("Consumed by C25"), and the §13.2 env block all agree with C25's "C25 configures C28's native exporter."
- **G04 is addressed** (INV-1 + AC-6 + OQ-1), which is the only gap in C25's row.
- **D-1..D-5 not violated.** C25 touches none of: judge provider (D-1), bundle-id namespace (D-2),
  bead-type ownership (D-3), C19↔C20 direction (D-4), C41↔C23 hash-chain (D-5).
- **Plan** mirrors the spec faithfully (T1–T8 are config-and-verify only; T5 = the G04 two-sinks proof;
  the de-risking order leads with G04 and the `session.id` guarantee). The same RC25-03 "guarantee"
  wording recurs in plan T2/DoD and §5; fixed there too for consistency.

## Verdict
**accept-with-fixes.** C25 is a solid exemplar: the two-sink boundary (the whole point of G04) is correct
and cross-consistent with C26's anti-edge and C24's framing, the config-not-daemon bar is held with no
over-build, and the env-var/signal contract is faithful to source. All five findings are **minor** and
fidelity/hygiene-class, not architectural: one mis-cited locator (RC25-01), one stale "not-yet-written"
note + missed cross-reference (RC25-02), one over-stated "guarantee" of a native property (RC25-03, the
same correction the C23 exemplar already took), and one prose gap on the divergence point (RC25-04) — all
**fixed in place**. RC25-05 (README section-label) is recorded for the sweep-2 citation pass, not fixed.
**Nothing deferred to the orchestrator; no blockers; no majors.**
