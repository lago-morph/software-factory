# Adversarial review — C15 Workflow linter (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Workflow Engine (critic-fixer)
Target: spec/C15-workflow-linter.md + plan-faithful/C15-workflow-linter.md
Charter: canonical / Track-A posture → attack FIDELITY and COMPLETENESS only, not the
design; PLUS the capability-for-principle bar (flag hardening that is not tied to a 12-principle)
and the C10-shape minimality bar from the dispatch.

## Findings

### RC15-01 — minor — G30 is mis-scoped as if its headline target were Mammoth; the gap's actual subject is the Tracker/diagnosis-agent (C38) seam, with Mammoth named only as Tracker's *wrapper*
**Claim.** §6 G30 note opens "G30's headline target is the Healer's Tracker transfusion (C38); the
same finding lands on C15 because C15's 21 rules are transfused from Mammoth." The §1 Source header
likewise leans on G30 as a C15-relevant gap.
**Evidence.** The actual G30 text (ambiguities-and-gaps:77) is titled **"Diagnosis agent ↔ Tracker
transfusion seam"** and is entirely about P11's diagnosis agent transfusing from *Tracker's*
`Diagnose`/`Audit`/`Doctor` APIs; Mammoth appears only as the thing that *wraps* Tracker
("Tracker (library Mammoth wraps)", README:292). G30 never mentions the 21-rule DOT linter or C15.
The inventory C15 gap column does say "G30", so C15 is *assigned* the gap — but the gap's literal
subject is the Tracker code-vs-pattern boundary, not Mammoth's. The spec's move — "the same
code-port-vs-pattern-reimplement boundary problem applies to C15's Mammoth transfusion" — is a sound
and useful *extension* of G30's principle to C15's situation, exactly what the inventory assignment
asks for. The only fidelity defect is calling it G30's "headline target" framing without flagging
that C15 is *applying G30's boundary principle to a sibling transfusion*, not closing G30's own
Tracker case. **Fix (applied).** Reworded the §6 G30 opener and the §1 Source note to state that
G30's literal subject is the Tracker transfusion (C38) and that C15 *inherits the same
code-port-vs-pattern boundary obligation* for its Mammoth transfusion — so the extension reads as a
deliberate generalization, not a misread of what G30 says.

### RC15-02 — minor — README's two license statements for Mammoth (134 "MIT" vs 301/§508/§551 "verify") are both cited, but §6 leans on "MIT per README" as the default in a way that slightly under-weights the verify caveat
**Claim.** §6 G30 resolution: "the faithful default is **MIT, code-transfusable** *pending the
README:551/§508 license-verification step*"; the wording foregrounds "README:134 *already* states
Mammoth's license as MIT" before the caveat.
**Evidence.** README:134 inline does say "(Go, MIT)" and License col "MIT (Mammoth)". But the master
license table (README:301) says "**MIT (verify; 2389 research convention)**", AI-CONTEXT §6.4 says
"**License: verify; 2389 convention is MIT**", and README:508/535/551 all list Mammoth among
projects that "need license verification before adoption." The weight of the corpus is
*verify-before-adopt, likely-MIT-by-convention* — i.e. **unverified**, which is precisely why G30/the
inventory flag it. Defaulting the spec to "MIT, code-transfusable" as the primary disposition (with
verification as a footnote) inverts the corpus's own emphasis. The spec is not wrong (it does cite
both and provides the pattern-reimplement fallback), but the faithful default should foreground the
*unverified* status, not the convention-MIT optimistic reading. **Fix (applied).** Re-balanced the §6
G30 resolution to lead with "license is **unverified — likely MIT by 2389 convention but flagged
'verify' (README:301, AI-CONTEXT §6.4, README:551)**" and frame **code-port as the outcome IF
verification confirms MIT**, pattern-reimplement otherwise — so neither branch is pre-selected as the
"default" ahead of the verification v4 itself mandates. OQ-3 and plan T0-license already carry the
verification-first ordering, so this is purely a wording re-balance, not a design change.

### RC15-03 — minor — the C14↔C15 seam (loop-construct marker on the DOT surface) is consistent, but C15 should name C14:OQ-2 as the shared blocker, not only C12:OQ-2 / its own OQ-2
**Claim.** §3.3 rule 1 + plan T3 require C14's DOT export to carry **loop-construct markers** ("a
bounded loop is distinguishable from a raw back-edge"); C15's OQ-2 pins "does the DOT surface carry
the node-kind tag, loop-construct markers, and node ids C15's structural rules need?"
**Evidence.** This is the correct and load-bearing seam, and it is **consistent** with C14: C14 §3.4
explicitly makes the loop primitive "a first-class entry in the §3.3 exclusion/mapping catalog" and
flags it as **C14:OQ-2**, stating it "gates C15's ability to lint loops"; C14 §3.1 emits node ids
(1:1, "ids must survive the round trip"), a `kind=` attr, and directed edges = dependency direction —
exactly the surface C15's structural rules read. So the two specs agree on the contract and both
flag the same unresolved item. The minor fidelity gap: C15 attributes the loop-marker uncertainty to
**C12:OQ-2** (the formula's loop primitive) and its own OQ-2, but the *DOT-encoding* of that
primitive — the thing C15's cycle rule actually consumes — is tracked as **C14:OQ-2** in the C14
spec. C15 should cite C14:OQ-2 as the shared seam OQ so the dependency is traceable from both sides.
**Fix (applied).** Added a cross-reference in §3.1/OQ-2 and the dependency table noting that the
loop-construct DOT encoding C15 needs is the subject of **C14:OQ-2** (which itself defers to
C12:OQ-2 for the primitive), so the seam is named identically from both ends.

### RC15-04 — minor — §1/§2 assert C14 "has no spec at this sweep"; C14 is in fact specced (spec/C14-formula-dot-translator.md exists), which strengthens C15 but the stale "named-but-unbuilt upstream" framing should be corrected
**Claim.** §1 Source: "C14 … *named-but-unbuilt upstream*"; §2 table + footprint note:
"**C14 has no spec at this sweep** (no C14 spec yet)"; OQ-2: "C14 has no spec yet."
**Evidence.** `spec/C14-formula-dot-translator.md` exists and is a full sweep-1 spec that defines the
`export(formula)→dot` surface (§3.1), node ids, kind attr, edges, and the loop-primitive caveat
(§3.4) — precisely the DOT surface C15 depends on. C15's repeated "C14 has no spec yet" is therefore
**stale/inaccurate** as written. This *helps* C15 (the contract it needs is now pinnable against a
real C14 spec rather than a hypothetical), so it is a fidelity-improving correction, not a downgrade.
The plan T3 ("C14 is unbuilt — this is a contract negotiation") and the dependency-graph "C14 has no
spec yet" carry the same stale claim. **Fix (applied).** Updated §1, §2 (table + footprint note),
§3.1, OQ-2, and plan T3 / §2 / §5 to say C14 is **specced at sweep-1** (cite
`spec/C14-formula-dot-translator.md`) but its **exact DOT-attribute surface is deferred to C14
sweep-2** (C14 §3.1 names the mapping but not attribute-level encoding; loop encoding is C14:OQ-2) —
so the real residual uncertainty (attribute-level DOT contract, not "C14 doesn't exist") is stated
accurately. This is the load-bearing correction in this review.

### RC15-05 — minor — D-7 conformance is correct (kind referenced, not redefined) but §1's "barely needs it" aside undersells that C15 *does* read kind=gate to avoid false cycle findings on sanctioned loops
**Claim.** §2 table: C15 "*references*, never redefines [the node-kind set] (and barely needs it:
structure, not kind)." §3.3 rule 1 distinguishes a raw back-edge from "a sanctioned bounded-loop
construct."
**Evidence.** D-7 (node-kind taxonomy home = C12; references-not-redefines) is **satisfied** — C15
nowhere redefines `{agent,tool,gate,sub_formula}` and §1/§3 explicitly defer the set to C12. Good.
But "barely needs it" is in mild tension with the spec's own cycle rule: to flag "a graph cycle that
is *not* a sanctioned bounded-loop construct" (§3.3 rule 1), C15 must recognize the loop/gate
construct on the DOT surface — i.e. it *does* consume the kind/loop-marker, which is exactly the
seam in RC15-03. The claim that C15 "barely needs" the kind is slightly self-undercutting. This is a
fidelity-of-self-description nit, not a D-7 violation. **Fix (applied).** Softened "barely needs it"
to note C15 reads kind/loop-construct markers **only** to tell a sanctioned bounded loop from a raw
back-edge (the §3.3 rule-1 distinction) — it consumes the value, never defines it (D-7) — which is
consistent with RC15-03's seam.

### RC15-06 — minor — D-9 conformance is exemplary; no F38/vocab claim. (No fix; recorded as a positive to bank the verification.)
**Claim.** Dispatch requires verifying C15 makes **no** F38/vocabulary-lint claim (owned by C10,
D-9). **Evidence.** §1 "What C15 is NOT" bullet 4, INV-4, AC-4, and the §9 DROP note all explicitly
disclaim F38/vocab/undefined-term linting and cite D-9 + "owned by C10"; AC-4 even makes the
boundary *testable* (structurally-sound-but-wrong-kind → zero C15 findings). C15 reads no C07
glossary. This is fully conformant with D-9 and the minimality bar. **No fix needed.**

### RC15-07 — minor — the minimality / capability-for-principle bar is met; the three named DROPs (pluggable registry, 0–1 quality score, vocab-lint) are correctly rejected. (No fix; recorded.)
**Claim.** Dispatch's BAR: flag over-build (configurable/pluggable rule registry, a 0–1 workflow
quality score / Goodhart, any vocab/F38 linting). **Evidence.** §1 NOT-bullet 7, §4 (fixed table not
a registry), INV-4, and the §9 "What the bar dropped" note explicitly drop all three and tie the
fixed-21-rule + findings-report + advisory-status shape to the C10 sibling and Principle 3. The
report shape is the minimal `{rule_id,severity,location,message}` taken from C10 §3.2. C15 is
correctly MINIMAL like C10. **No fix needed** — this is the desired posture; recorded so the bar
check is on the record.

## Verdict
**accept-with-fixes.** C15 is a strong, faithful, genuinely-minimal sweep-1 spec+plan: it nails the
C10-shape mandate (fixed 21 rules, findings report, advisory-by-default), is exemplary on **D-9** (no
F38/vocab claim, boundary made testable in AC-4) and **D-7** (kind referenced, never redefined), and
the **C14↔C15 seam is consistent** — both specs name the loop-construct DOT encoding as the
load-bearing, still-open contract (C15 OQ-2 ↔ C14:OQ-2 ↔ C12:OQ-2) and C14's `export` surface (node
ids, kind attr, directed edges) is exactly what C15's structural rules consume. All six applied
fixes are fidelity polish, not design change: (1) frame G30 as a *principle inherited* for the
Mammoth transfusion rather than G30's own Tracker headline; (2) re-balance the Mammoth license to
lead with "unverified (verify), likely-MIT" rather than optimistic-MIT-default; (3) name C14:OQ-2 as
the shared seam OQ; (4) **correct the stale "C14 has no spec yet" to "C14 is specced; its
DOT-attribute surface is sweep-2"** (the one load-bearing correction); (5) soften "barely needs the
kind"; (6/7) banked the D-9 + minimality verifications as positives. **Nothing architecturally
significant is deferred** — the residual unknowns (exact DOT attribute encoding, loop encoding,
license verification, blocking-vs-advisory default, serialization) are all already correctly pinned
as OQ-1..OQ-4 and plan tasks T0-license/T3, which is the right sweep-1 disposition.
