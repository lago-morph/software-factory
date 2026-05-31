# Adversarial review — C37 Trajectory Embedding & Clustering (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Healing Loop (P11)
Target: `spec/C37-trajectory-clustering.md` (+ `plan-faithful/C37-trajectory-clustering.md`)
Posture: canonical track (D-6) → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (flag any addition that hardens existing stack capability rather than
delivering new capability tied to a 12-principle).

## Findings

### RC37-01 — major — `[AMBIGUITY: G32]` fabricates an inventory quote for the C46 deferral target
**Claim.** §6 G32 routes the cost-per-satisfaction model to **C46** and cites it as
`(C46, inventory \`C29:G32 — cost-per-satisfaction model deferred to C46\`)`. **Evidence.** No such
string exists in `_meta/component-inventory.md`. The inventory carries G32 on **C29, C37, C46, C48,
C57** rows; C46's row reads "Meta-metric stream … Records **cost-per-satisfaction**, time-to-threshold,
judge-FP-rate over time; **needs a defined cost model**". So routing the cost model to C46 is
**well-supported** by the actual inventory text — but the *quoted* inventory fragment is invented, which
is exactly the "mislabel a fill as a cited fact" failure the bar targets. **Fix (applied).** Replaced the
fabricated quote with the real basis: C46 is the meta-metric stream whose own inventory row names
"cost-per-satisfaction … needs a defined cost model", and C46 carries G32 in the inventory alongside
C37. The (b) reading and the C46 routing are sound and kept.

### RC37-02 — major — README:499 ("ensure its clusters match") is the **Healer's** scenario line, cited as C37's own adversarial check
**Claim.** §8 (test strategy) and plan T10/R-2/R-5 cite README:499 — "feed it failure trajectories the
team manually clustered, ensure its clusters match" — as **C37's** headline adversarial acceptance check.
**Evidence.** README:499 reads in full: "**The Healer agent's scenarios** are adversarial — feed it
failure trajectories that the team has manually clustered, ensure its clusters match." The sentence
attributes the scenario set to **the Healer agent** (the C38 diagnosis surface), and **C38's** spec cites
the *same* line (C38 §6 G07, AC2) as *its* held-out acceptance. So README:499 is a **shared** citation
whose grammatical owner is the Healer, not the clustering stage. The behaviour it describes (a clustering
that matches human-assigned clusters) *is* legitimately a clustering-quality check, so the check itself is
faithful to C37's job — but presenting README:499 as *C37's* line, unqualified, overstates the citation
and silently double-claims a v4 sentence already claimed by C38. **Fix (applied).** Re-tagged both C37
citations of README:499 as the **shared Healer-evaluation** line it is: C37 surfaces the *clusters-match*
property as its own AC (legitimate, since the clustering is what the Healer's "clusters match" rests on),
while noting README:499's grammatical owner is the Healer scenario set (C38), so the citation is not read
as a C37-exclusive v4 directive. The AC content (known-similar failures co-cluster) is correct and kept.

### RC37-03 — minor — C36↔C37 population seam: the two specs agree on the *direction* but not the *unit*, and only C37 flags it
**Claim.** §1/§2/OQ-1 treat the C36→C37 hand-off as open (does C36 select the population, or does C37
cluster a broader set?). **Evidence.** Cross-checking C36: C36 §1 states plainly "**C36 *feeds* C37**";
C36 I3 emits an `anomaly` signal carrying "the **pointer back to the offending trajectory in C21**" —
i.e. C36's natural output granularity is **per-anomalous-trajectory (or per-value)**, whereas C37's I1
input is a **set/window** of trajectories to cluster. The two specs are **consistent on direction**
(C36→C37, anomaly→cluster) and both **defer the exact contract**, but C36's OQ-2 frames the signal
**carrier** (C20 bead vs C23 event) without naming the *aggregation* into the set C37 consumes, and C36
does **not** list the C36→C37 hand-off as a top OQ. So the seam is genuinely two-sided-open, but the
**granularity mismatch** (per-trajectory signal vs population-to-cluster) is implicit. This is a
completeness gap, not a contradiction. **Fix (applied).** Sharpened OQ-1 to name the *granularity*
question explicitly — whether C37's I1 input is the **aggregated anomalous window** (C37 batches the
individual C36 signals into a population) or whether C36 emits a window directly — and noted the seam is
co-owned with **C36 OQ-2** (the signal carrier), so the sweep-2 freeze is joint with C36. No design
change; the direction (C36 feeds C37) is preserved.

### RC37-04 — minor — cluster output (I5) is silent on attribution/provenance, where the sibling C38 record is explicitly attributed
**Claim.** I5 / the data-model "Cluster set (output)" defines the per-cluster record as members + size +
representative + noise set, with no provenance/attribution field. **Evidence.** The downstream sibling
C38 stamps **`created_by`** (C41) on every `Diagnosis` (C38 I4 "attributed, no silent diagnosis") and
records `transfused_from`. v4 does **not** state an attribution requirement for C37's *clustering* output
specifically (P9/C41 `created_by` is "on every action", README:229, but C37 is a derived view, and the
spec already binds C37 to own no source-of-truth, INV-5). So this is **not** a fidelity violation — v4
imposes no C37-specific attribution clause — but the loop-auditability story (F54 objective-drift audit,
which §6 says C37 "underwrites") is cleaner if the emitted clustering carries the config-pin/run identity
that produced it (so a re-derived view is traceable to the models/params that made it, INV-5). **Fix
(applied).** Added one clause to I5/the cluster-set state noting that the emitted clustering is *labelled
with the run's pinned config identity* (embedding-model id + HDBSCAN param-set + population selector) so
the derived view is reproducibly traceable (INV-5/§7 observability) — framed as an observability/trace
property, **not** a new `created_by` attribution mechanism (which stays C41's and is not asserted as a v4
requirement on C37). Left as the minimal trace; no new capability.

### RC37-05 — minor — "(spec/C21 §8)" conformance-gate citation is leaned on heavily; confirm the cited clause actually enumerates C37
**Claim.** §2, §5, §8, and the plan repeatedly gate C37 on "C21's conformance suite **must pass before …
C36–C38 … build on C21** (spec/C21 §8)". **Evidence.** This is a load-bearing sequencing claim cited
five-plus times. The *quoted* clause "must pass before C22, C24, C36–C38 … build on C21" appears in the
C37 source header itself and in C36's spec identically, so the two siblings agree — but the review's
scope forbids editing C21, and I cannot fully re-verify C21 §8's exact enumeration from C37's files alone.
The claim is **internally consistent** across C36/C37 and is the natural reading of a conformance gate.
**Fix (not applied — verification note only).** No edit; flagging that the "spec/C21 §8 enumerates
C36–C38" citation should be spot-checked against C21's actual §8 text at integration (it is asserted
consistently by both P11 siblings, so low risk). Not a DEFERRED architectural item — a citation-audit
note.

### RC37-06 — minor — "local/CPU-capable … no judge-provider tokens" embedder claim is a reasonable fill but stated with more certainty than v4 backs
**Claim.** §6 G32 and §7 (cost/security) assert the sentence-transformers embedder is
**"local/CPU-capable"**, needs "**no judge-provider tokens**", and that D-1 (judge provider) is therefore
"irrelevant to C37". **Evidence.** This is **true of sentence-transformers as a library** (it runs local
models), and it is the correct *capability-for-principle* reading (the embed step is compute, not LLM
spend — materially distinct from the C32 judge / C38 diagnosis token cost). v4 itself does not *state*
"local/CPU" for the embedder; it states the library + "standard recipe" (AI-CONTEXT:406). So this is a
**faithful inference about the named library**, not a v4 fact — currently phrased as flat assertion.
**Fix (applied).** Lightly qualified the "local/CPU" claim as the property of the **named library**
(sentence-transformers runs local embedding models) rather than an unattributed v4 statement, so it is not
read as a v4 directive. The cost conclusion (compute, not provider tokens; cheaper than judge/diagnosis)
is sound and kept; the D-1-irrelevance point is correct and kept.

### RC37-07 — minor — G33 reading-(b) leans on "spec/C21 chose the same fail-open reading" and "C40 durable Orders" — confirm both cross-refs
**Claim.** §6 G33 grounds C37's fail-isolation in "spec/C21 chose the same fail-open reading for
CXDB-down" and "the durability seam is **C40 (Orders)**". **Evidence.** Cross-checking siblings: **C36**
§6 makes the identical move ("C21 fails *open* on outage, spec/C21 §6 reading (a)"; "durability is C24's
inbox-spool + C21's fail-open"), and C38 §1/§6 routes durable re-launch to **C40** ("C40 = durable
carrier; C38 = content"). So C37's G33 posture is **consistent with all three P11 siblings** and with the
capability-for-principle bar (no in-stage HA — that's C40 + C21). The C21 §6 "reading (a) fail-open" and
C40-as-durable-carrier citations are asserted consistently across C36/C37/C38; same caveat as RC37-05 (I
cannot re-verify C21 §6 / C40 from C37's files). **Fix (not applied — verification note only).** No edit;
the G33 reading is faithful and sibling-consistent. Flag for integration spot-check that C21 §6 is indeed
"fail-open reading (a)" (C36 cites it identically, so low risk).

## Verdict

**accept-with-fixes.** The spec is strong, faithful, and correctly minimal: it holds C37 to the
off-the-shelf **sentence-transformers + HDBSCAN** recipe (INV-1, AC-3), keeps the genuine custom surface
to the three load-bearing seams the brief names — the **wiring** (read C21 → embed → cluster → emit), the
**representation choice** (I2/G32, defaulted minimally to trajectory-as-text), and the **per-cluster
contract handed to C38** (I5/INV-2) — and introduces **no** custom embedding/distance/clustering algorithm
and **no** in-stage HA (the capability-for-principle bar is respected; the §6 "what got DROPPED" list is
exemplary). G32 (cost) and G33 (partial-failure) are both **ADDRESSED-with-reason**, not merely deferred,
with the cost model correctly routed to C46 and durability to C40 + C21. The C36↔C37 population seam is
consistent in direction with C36's side and the residual (granularity) is now explicitly OQ'd.

No blockers. Two **major** fidelity fixes applied in place — a fabricated inventory quote (RC37-01) and a
double-claimed/mis-attributed README:499 citation (RC37-02) — plus three minor qualify-the-inference /
sharpen-the-seam fixes (RC37-03/04/06). Two minor items (RC37-05, RC37-07) are **citation-audit notes**
against C21 §6/§8 and C40 that cannot be re-verified from C37's own files (asserted consistently by the
C36/C38 siblings, so low risk) — these are verification notes, not DEFERRED architectural decisions.
**Nothing architecturally significant is deferred**; the OQ-1 granularity sharpening and the I5 trace
clause are faithful tightenings, not design changes.
