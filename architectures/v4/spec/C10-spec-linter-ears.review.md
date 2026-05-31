# Adversarial review — C10 Spec linter (EARS / INCOSE) (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Spec Intake (fidelity + completeness + the capability bar)
Target: spec/C10-spec-linter-ears.md (+ plan-faithful/C10-spec-linter-ears.md)
Charter: single-track. Track-A posture → attack FIDELITY and COMPLETENESS, not the design; PLUS the
capability-for-principle bar (HANDOFF §2 / SURVIVOR-PASS): flag any addition that hardens existing-stack
capability rather than delivering new capability tied to a 12-principle, and flag any survivor-pass DROP
that has been reintroduced.

## Summary

The faithful C10 is a strong, well-traced spec. Every load-bearing v4 citation I spot-checked is exact
(README:102/108/111/154; F-MODE:20/74/76; one-shot Part 2 lines 86–122; component-inventory Batch-2 line
109; the C07 "Consumed by C10" row; the C17 instances row). The two most-defensive survivor-pass DROPs —
**#05 versioned configurable rule registry** and **#06 0–1 score + threshold gate** — are correctly
**absent** (zero reintroduction; the rule set is explicitly an in-pack table that "introduces no new shared
on-disk artifact", and the disposition is advisory/blocking, not a score-threshold). Good.

The one substantive issue is survivor-pass DROP **#04 (vocab-lint wired to C07 / F38)**, which the faithful
spec reintroduces as a co-owner responsibility — but that DROP is in genuine tension with two direct v4
statements (F-MODE:74 assigns F38 to the spec linter; C07's own spec names C10 the F38 owner). That makes
it an orchestrator reconciliation, not a unilateral strip — deferred (RC10-01). The rest are minor
qualify-the-inference / tighten-the-citation fixes, applied in place.

## Findings

### RC10-01 — major — Survivor-pass DROP #04 (vocab-lint wired to C07) is reintroduced as a co-owner responsibility, but it directly contradicts F-MODE:74 + C07's doc — needs orchestrator reconciliation, not a unilateral strip
**Claim.** SURVIVOR-PASS C10 row #04 is **DROP — "Vocab-lint wired to C07 — No C07 machinery."** The
faithful spec nonetheless elevates the F38 vocabulary-lint rule to a **co-equal reason-to-exist and owned
responsibility**, threaded throughout: §1 ("C10 is the **owner** of F38"; "Run the vocabulary-lint rule
against the C07 term registry"), §3.1 (C07 term registry as a named **input**), §3.3 rule 3, §4, §5, §6
(F38 row + stale-registry degrade), §8 AC-4, and plan T6 / Workstream C. **Evidence (both sides).**
*Against the spec:* the bar's worked verdict drops exactly this wiring; the kept-minimal capability is the
report shape + advisory/blocking over C08, not a C07-keyed vocab rule. *For the spec (the fidelity
counter-argument that makes this a DEFER, not a strip):* F-MODE-COVERAGE:74 literally states F38
("Vocabulary lint debt") is handled by "EARS-style spec linter (P1 component); deterministically detectable
— **Addressed**" — i.e. v4 itself assigns F38 to *this* component; the component-inventory C10 one-liner is
"addresses prose-rigor / **vocab-lint debt**"; and C07's *own* survivor spec says F38 is "owned by C10's
EARS linter … C07 is the data; the linters are the consumers" (C07 §1, §3.3, line 49 "Consumed by C10",
§6 F38 row). So C07 and C10 are mutually consistent, and both trace F38 to C10 — which is the opposite of
what DROP #04 implies. The likeliest intent of DROP #04 is narrower than it reads: it drops the *elaborate
C07 `CanonicalTermSet` content-hash machinery* (because survivor-C07's registry is itself a
`[FAITHFUL-FILL]` TOML assumption, OQ-C07-2 "format … needs deciding"), **not** the existence of an F38
vocab rule in C10. The faithful spec already softens to that reading (C07 is a *soft data* dependency for
*one* rule; vocab-lint **degrades to skip-with-warning** if the registry is absent, §6; the registry format
is routed to C07/OQ, not asserted). **Why deferred (not applied).** Resolving this either way is
architecturally significant and cross-component: stripping F38/vocab-lint from C10 would put C10 in direct
conflict with F-MODE:74 and with C07's already-frozen doc (a fidelity regression and a cross-dependency
break); keeping it as-is leaves a standing contradiction with the survivor-pass row. This is precisely the
"ambiguous / architecturally-significant" class the brief says to leave UNapplied. **Fix (DEFERRED — needs
orchestrator decision).** Orchestrator to reconcile SURVIVOR-PASS C10 #04 against F-MODE:74 + C07 §1/§3.3/
§6. Recommended resolution (for the integrator, not applied here): **keep the F38 vocab rule in C10** (so
F-MODE:74 and C07 stay coherent) but **scope DROP #04 explicitly to the C07-machinery elaboration** — no
`CanonicalTermSet` content-hash contract, no versioned term-set pinning, registry treated as the existing
soft TOML data the linter best-effort loads — which is already how the faithful spec reads. If the
orchestrator instead upholds DROP #04 literally, then F-MODE:74 and C07's "owned by C10" statements must be
amended in the same pass (out of C10's edit scope). A `DEFERRED` marker has been added at spec §3.3 / §1 and
in plan T6.

### RC10-02 — minor — §6 F51 handling over-claims: F-MODE:76 assigns F51 to "deterministic boundary typing" generally, not to the spec linter specifically
**Claim.** §6 lists F51 ("Ashby-deficient probabilistic guard") as a mode C10 handles, calling C10 "the
**primary** kind P4 wants" and "exactly the deterministic boundary-typing guard F51 favors over an LLM
check (F-MODE:76)." §7 repeats "the F51 reason deterministic guards are primary." **Evidence.** F-MODE:76
reads: "F51 … P4 (deterministic-first) — **deterministic boundary typing** is the primary guard; LLM-judge
is secondary — Addressed." It credits *deterministic-first / boundary typing* as a class; it does **not**
name the spec linter, and "boundary typing" is the isolation/typing posture owned by C43 (isolation
boundary) + C17, not specifically a spec linter. C10 *is* a deterministic no-model guard (true, and a fair
P4 exemplar), but "C10 is exactly the deterministic boundary-typing guard F51 favors" reads C10 into a
v4 statement that is about a category. **Fix (applied).** Softened §6/§7 to: C10 is *an instance of* the
deterministic-first posture F51 credits (no-model, reproducible) — it is **not** the boundary-typing guard
F51 names (that is C17/C43); reworded so F-MODE:76 is cited as category support, not a C10-specific claim.

### RC10-03 — minor — Dependency footprint asserted in §2 is broader than the inventory's `Depends on` for C10 (C08 only); should be flagged as derived, not inventory-stated
**Claim.** §2 and the plan's "Must precede C10" assert C10 depends on **C08, C07, C17/C02, and C03** all
being frozen first. **Evidence.** The component-inventory C10 row's formal `Depends on` column is **C08
only** (line 22). The other four are real upstreams, but C10 reaches them transitively (via C08's lint
contract, via C17's tool-node abstraction, via C03's "optional" config) rather than by a stated inventory
edge. The §2 narrative mostly cites them correctly through the *other* components' docs, but the dependency
table and the plan present a four-way Batch-1 prerequisite as if it were the inventory's dependency record.
Combined with RC10-01 (the C07 edge is the contested one), this matters: C07 in particular is **not** an
inventory dependency of C10. **Fix (applied).** Added a one-line note at §2 that C08 is C10's sole *formal*
inventory dependency; C07 (vocab data), C17/C02 (built-as), and C03 (optional-enable) are *derived/soft*
upstreams the faithful reading introduces — keeping the table honest about which edge the inventory states.

### RC10-04 — minor — §3.2 / OQ-4 lean toward SARIF as "the natural transfusion-friendly choice"; harmless but is a sweep-2 design lean a faithful sweep-1 should not pre-bias
**Claim.** The [FAITHFUL-FILL] at §3.2 and OQ-4 both say "SARIF is the natural transfusion-friendly
choice." **Evidence.** v4 names *no* serialization (correctly stated). Naming JSON/SARIF/text as the
candidate set is fine and faithful; editorialising that SARIF is "natural / the choice" is a mild
sweep-2 design lean (and a Track-B-flavoured optimisation) inside a Track-A sweep-1 fill whose own text
says "v4 names none." Low stakes — the fill defers the pick to sweep 2 and constrains it to the C02 ABI —
but the lean should not read as a decision. **Fix (applied).** Reworded to list JSON/SARIF/text as equal
candidates and dropped the "natural choice" editorialising; the pick stays a sweep-2 deliverable
constrained by the C02 output ABI.

### RC10-05 — minor — Citation style mixes "§<line-number>" with real section numbers (C07 §49, C17 §64); substantively correct but reads as a section that doesn't exist
**Claim.** §2 cites "C07 §3.2, §3.3, **§49** 'Consumed by C10'" and "C17 §1 … **§64** lists C10 as an
instance." **Evidence.** C07 has sections §1–§9 (no §49); line **49** is the "Consumed by C10/C15/C16"
dependency row. C17 has §1–§9 (no §64); line **64** is the downstream-instances row naming C10. The targets
are right; the "§<n>" form points at a line as if it were a section, which a reader will fail to find.
**Fix (applied).** Changed the two mixed cites to name the section + clarify it is a line ("C07 §2 deps
table, line 49 'Consumed by C10'"; "C17 §2 instances row, line 64") so the reference resolves.

### RC10-06 — minor — §1 asserts C10 "owns exactly the *detectable* portion" of F18 in a way that slightly outruns F-MODE:20's wording — acceptable but tag the boundary as inference
**Claim.** §1 (F18 bullet) states C10 "owns exactly the *detectable* portion, not the residual semantic
ambiguity (F-MODE:20)." **Evidence.** F-MODE:20 says F18 is "EARS-style spec linter (P1 component) +
satisfaction-not-test-pass (P6) — **Partial — fundamental prose ambiguity remains**." It establishes the
linter is the structural half and the residue is conceded; the precise phrase "owns exactly the detectable
portion" is C10's (fair) gloss, not v4's words. This is a *reasonable* faithful inference and is already
hedged elsewhere ("C10 does not claim to close F18"), so it is not a misattribution — only the word
"exactly" risks reading as a v4 guarantee of a clean detectable/undetectable partition. **Fix (applied).**
Softened "owns exactly the detectable portion" → "owns the deterministically-detectable subset (the
residual semantic ambiguity is conceded, per F-MODE:20's *Partial*)", so the partition reads as the
faithful framing it is.

## Verdict

**accept-with-fixes.** Faithful, well-cited, and correctly disciplined on the two defensive survivor-pass
DROPs (#05 versioned rule registry, #06 score+threshold gate are absent). Five minor fidelity/citation
tightenings applied in place (F51 over-claim, derived-dependency honesty, SARIF lean, mixed §/line cites,
the F18 "exactly" gloss). The one consequential item — RC10-01, the reintroduction of DROP #04 (vocab-lint
/ F38) — is **DEFERRED to the orchestrator**, because the survivor-pass row that drops it is itself in
direct tension with F-MODE:74 and with C07's already-frozen "owned by C10" statements; choosing either way
is architecturally significant and edits the cross-component contract, which is out of a Track-A reviewer's
authority. No fidelity blocker; nothing else architectural outstanding.
