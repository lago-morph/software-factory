# Adversarial review — C37 Trajectory Embedding & Clustering (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Healing Loop (P11)
Target: `spec/C37-trajectory-clustering.md` (+ `plan-faithful/C37-trajectory-clustering.md`)
Posture: canonical track (D-6) → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (flag any addition that hardens existing stack capability rather than
delivering new capability tied to a 12-principle). Assigned gaps: **G32, G33** only. Binding: D-1..D-17
(relevant D-6 — satisfied; docs say "canonical track").

> **Note on a prior review pass.** An earlier `C37-…review.md` existed whose findings were sound in spirit
> but (a) mis-diagnosed RC37-01 below as a *fabricated* quote ("no such string exists") — it is in fact a
> **mis-attributed real** quote (lives in review-log:154, not the inventory), so the correct severity is
> **minor**, not major; and (b) marked its fixes "applied" when **none had actually landed** in the spec/plan
> (verified: the original builder text was unchanged at every cited line). This pass re-grounds the findings
> and **actually applies** the confident fixes.

## What holds (the bar)
The bar is held cleanly. INV-1/AC-3 forbid any custom embedder/distance/clusterer; §6 "what got DROPPED"
enumerates the refusals (no custom algorithm; cost model → C46; in-stage HA → C40+C21; quality/auto-tune →
sweep-2) — exemplary capability-for-principle discipline. The "transfusion from sentence-transformers +
HDBSCAN" framing mirrors README:461 *verbatim* (v4 itself uses "transfusion" loosely for wrapping these
mature libs, exactly as "transfusion from PyOD" for C36), and the spec correctly treats them as off-the-shelf
wraps, **not** as C51-gated gene-transfusion exemplars. G32 (reading (b): bound to the supplied/anomalous
population; cost figure → C46) and G33 (reading (b): fail-isolated, best-effort loop; durability = C40+C21)
are both **ADDRESSED-with-reason**, consistent with the C21/C24/C36/C38 siblings. C37's "sole dep = C21"
claim is faithful (inventory: C37 depends on C21 only; C36 is a seam, not a dep edge — correct, not
challenged). All load-bearing README (248/254/255/256/261/312–313/461/466/499) and AI-CONTEXT
(327/329/330/406/649–650) citations verified exact against `architectures/v4/{README,AI-CONTEXT}.md`.

## Findings

### RC37-01 — major — the C36↔C37 population seam is under-committed on C37's side relative to what C36 already commits; C37 never names C36's `anomaly` signal (C36 I3) as the carrier of its population selector
**Claim.** C37 framed the entire C36→C37 hand-off as open (OQ-1: "does C36 select the population, or does C37
cluster a broader set?") and described C36 only as a "population selector … *Seam, not a dep edge* … exact
hand-off is OQ-1" (§2 row; I1), naming **no** concrete carrier. **Evidence.** spec/C36 commits definitely on
its side: C36 I3 emits a typed **`anomaly` signal** carrying "the **pointer back to the offending trajectory
in C21**" (C36 §3 I3; INV-3), and C36 §2 states "the **anomaly→cluster trigger seam is C36's signal (I3)**"
with C37 "Consumes C36's anomaly signal — embeds + clusters the flagged failures" (C36 §1, lines 73–75; §2
line 108). C36's data-model further co-freezes "the `anomaly`-signal record shape … with C37/C38, the
principal consumers". So C36 has already declared (a) C37 consumes C36's `anomaly` signal as the trigger, and
(b) the signal shape is co-frozen *with C37* — yet C37 acknowledged neither, leaving the seam asymmetric (one
side committed, the other treating it as wholly unresolved). The **carrier** (C36 I3) is settled and should be
named; the genuinely-open residual is narrower — the **granularity/aggregation** (does C37 batch the
individual per-anomaly C36 signals into the population, or does C36 hand a window directly; does C37 cluster
exactly the flagged set or a broader one). This is the SEAM the brief specifically flags, and the most serious
finding. **Fix (applied).** Named **C36's `anomaly` signal (C36 I3)** as the I1 selector carrier in the §2
C36 row, I1, and (sharpened) OQ-1; recorded the record-shape co-freeze with C36; recast OQ-1 to the
granularity question and bound it to **C36 OQ-2** (carrier + record shape) for a joint sweep-2 freeze. Plan
risk-3 updated to match. Additive only — **no** dependency-graph change (C21 stays C37's sole dep edge).

### RC37-02 — minor — README:499 ("ensure its clusters match") is framed in v4 as *the Healer agent's* scenarios; C37 presented it as unambiguously C37's adversarial check (and C38 also claims it)
**Claim.** C37 invoked README:499 ("feed it failure trajectories the team manually clustered, ensure its
clusters match") as *C37's* headline adversarial validation in §8 (test strategy) and plan T10/risk-2/DoD-T10.
**Evidence.** README:499 reads in full: "**The Healer agent's scenarios** are adversarial — feed it failure
trajectories that the team has manually clustered, ensure its clusters match." The pronoun "its" refers to the
**Healer** (the C38 diagnosis agent); spec/C38 indeed claims the *same* line as **its** G07 acceptance (C38
AC2: "On the adversarial Healer scenario set — README:499 — C38's root-cause diagnoses match the human-assigned
root cause"). So one v4 sentence is cited by two components as their own. The reading is defensible (the
*clusters-match* half most naturally exercises the *clustering* stage, C37; the *diagnoses-match* half
exercises C38) — not a contradiction — but C37 overstated by presenting the check as solely its own.
**Fix (applied).** Recast both spec and plan README:499 references as v4's **Healer-scenario** set (shared
with C38, which owns the diagnosis-match half); C37 owns the **clustering-match / clustering-fidelity** half it
rests on — so the cross-component attribution is explicit and consistent with C38 AC2. AC content (known-
similar failures co-cluster) unchanged.

### RC37-03 — minor — the `C29:G32 — cost-per-satisfaction model deferred to C46` citation was attributed to "inventory" but is from review-log:154
**Claim.** §6 [AMBIGUITY: G32] grounded the "cost-per-satisfaction model lives at C46" reading by citing
`inventory \`C29:G32 — cost-per-satisfaction model deferred to C46\``. **Evidence.** That exact string is
**not** in component-inventory.md; it is verbatim in `_meta/review-log.md:154` ("C29:G32 — cost-per-
satisfaction model deferred to C46 (C29 is cost-aware only)"). (This corrects the prior pass, which called the
quote *fabricated* after searching only the inventory.) The *conclusion* is independently well-grounded — the
inventory's C46 row (line 58) reads "Records cost-per-satisfaction … **needs a defined cost model**" and C46
carries G32 — so only the **source label** is wrong (review-log, not inventory). A mis-attributed source is a
Track-A fidelity defect even when the claim is true. **Fix (applied).** Re-attributed the citation to
**review-log:154** (its real home) and added the supporting inventory C46-row evidence.

### RC37-04 — minor — C38 expects a per-cluster "shared-failure signal" feature that C37's I5 cluster record does not provide
**Claim.** C37's emitted cluster record (I5 / §4) is {member ids, size, representative/exemplar, noise set} —
structural fields only. **Evidence.** spec/C38 §3 inbound-contract-1 enumerates what it reads from a C37
cluster as "its id, its member trajectories …, and whatever cluster-level features C37 attaches (size,
centroid/exemplar, **the shared-failure signal**)". The "shared-failure signal" — some per-cluster
characterization of *what* the members share — is on C38's wishlist but in **no** C37 interface/data-model
field. C38 rightly defers ("Concrete cluster schema is C37's (sweep-2 seam)"), so this is a seam-completeness
gap to reconcile at the sweep-2 cluster-record freeze, not a present contradiction. **Fix (applied).** Added a
seam note at I5 flagging C38 §3.1's expectation and routing the reconcile to the **sweep-2 cluster-record
freeze (joint with C38, M2)** — surfacing the asymmetric expectation now rather than silently shipping a
narrower record.

### RC37-05 — minor — "local/CPU-capable … no judge-provider tokens" embedder claim was stated as fact with more certainty than v4 backs
**Claim.** §6 G32 (and §7) asserted the sentence-transformers embedder is "**local/CPU-capable**" and needs
"**no judge-provider tokens**". **Evidence.** This is **true of sentence-transformers as a library** (it runs
local models) and is the correct capability-for-principle reading (the embed step is compute, not LLM spend —
distinct from the C32 judge / C38 diagnosis token cost). But v4 states only the library + "standard recipe"
(AI-CONTEXT:406); "local/CPU" is a **faithful inference about the named library**, not a v4 statement, and was
phrased as a flat assertion. **Fix (applied).** Qualified the §6 claim as a property of the **named library**
(sentence-transformers runs local embedding models) rather than an unattributed v4 fact. The cost conclusion
(compute, not provider tokens; cheaper than judge/diagnosis) and the D-1-irrelevance point are sound and kept.
(The §7 one-liner "A local/CPU sentence-transformers embedding" is brief, derives from the now-qualified §6,
and reads as a cost-note rather than a cited v4 fact — left as-is to avoid churn.)

### RC37-06 — minor — verification note: the "spec/C21 §8 / §6" and "C40 durable Orders" cross-refs are leaned on heavily and cannot be re-verified from C37's files (edit scope = C37 only)
**Claim.** §2/§5/§8/plan gate C37 on "C21's conformance suite must pass before … C36–C38 … build on C21
(spec/C21 §8)" (5+ times), and §6 G33 grounds fail-isolation in "spec/C21 chose the same fail-open reading
(spec/C21 §6)" + "durability seam is **C40 (Orders)**". **Evidence.** These are internally consistent across
the P11 siblings: spec/C36 cites C21 §8's "must pass before … C36–C38" and C21 §6 fail-open **identically**,
and spec/C38 §1/§6 routes durable re-launch to C40 ("C40 = durable carrier; C38 = content"). So the citations
are sibling-corroborated and low-risk, but the brief restricts edits to C37's files and I cannot re-verify
C21 §6/§8 or C40's text directly. **Fix (not applied — verification note).** No edit; flag for an integration
spot-check that C21 §8 actually enumerates C36–C38 and C21 §6 is the "fail-open reading (a)". Not a DEFERRED
architectural item — a citation-audit note.

### Considered and declined (not applied, by design)
- **Adding a config-pin "trace identity" clause to the I5 output contract.** Tempting (so a re-derived
  clustering is traceable to the models/params that made it), but the spec **already** carries this via
  **INV-5** (same population + pinned models/params ⇒ same clustering) and **§7 Observability/Ops** ("pin the
  embedding-model id + versions … reproducible"; health events worth emitting). Enlarging the *cross-component*
  I5 contract with a field neither v4 requires nor C38 asked for is exactly the hardening-beyond-the-principle
  the bar cautions against — declined deliberately (not a deferral). The reproducibility/trace property stands
  on INV-5 + §7 without growing the contract.

## Verdict
**accept-with-fixes.** Faithful, well-traced, and correctly minimal: the off-the-shelf
**sentence-transformers + HDBSCAN** recipe is held (INV-1/AC-3), the keep is exactly the three load-bearing
seams the brief names — **wiring** (read C21 → embed → cluster → emit), the **G32 representation choice**
(I2, defaulted to trajectory-as-text), and the **per-cluster contract to C38** (I5/INV-2) — with **no** custom
algorithm and **no** in-stage HA. G32 and G33 are ADDRESSED-with-reason (cost → C46, durability → C40+C21).
No blockers. One **major** seam fix applied (RC37-01 — C37 now names C36's committed `anomaly`-signal carrier
and the granularity residual is jointly OQ'd with C36); four **minor** fidelity fixes applied in place (RC37-02
Healer-scenario attribution, RC37-03 review-log re-attribution, RC37-04 cluster-record seam note, RC37-05
qualify the local/CPU inference). RC37-06 is a citation-audit verification note (C21 §6/§8, C40) that cannot
be re-verified from C37's files — sibling-corroborated, low-risk, **not** a DEFERRED decision. **Nothing
architecturally significant is deferred**; every applied fix is additive or a citation correction and changes
no dependency edge, no chosen G32/G33 reading, and no design decision. OQ-1..OQ-4 remain the correctly-open
items (OQ-1 now sharpened to the granularity question).
