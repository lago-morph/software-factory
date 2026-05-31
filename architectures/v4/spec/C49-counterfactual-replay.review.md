# Adversarial review — C49 Counterfactual Replay Driver (canonical track, sweep 1)

Reviewer persona: Adversary / critic-fixer — Self-Optimization (C49)
Target: spec/C49-counterfactual-replay.md + plan-faithful/C49-counterfactual-replay.md
Posture: post-convergence single track (D-6). Attack FIDELITY + COMPLETENESS, not design; PLUS the
capability-for-principle bar (HANDOFF §2). Sole gap owned: **G19**. Bindings checked: D-6, D-13.

This is v4's hardest, admittedly-unsolved invention. The central question is the **HONESTY of the G19
framing** — does C49 pretend to solve what v4 concedes is unsolved? Verdict up front: **no, it does not**.
The tractable/deferred partition is sound, the fidelity-labeling contract is the correct minimal honest
move, and AC-7 explicitly refuses to assert reproduction for the LLM slice. The findings below are
precision/fidelity fixes around an honest core, not a challenge to the framing.

## Findings

### RC49-01 — minor (fidelity / mis-citation) — "Bridge + driver" mis-parsed: "Bridge" = the C24 bridge pack, not "the CXDB primitive"
**Claim.** §1 (lines 13–15) reads README:274's Implementation column "**Bridge + driver**" as "the
**bridge/primitive** — content-addressed turns + O(1) branching — is owned by C21 … C49 is the driver."
i.e. it glosses "Bridge" as the CXDB branching *primitive*. **Evidence.** v4's Implementation column uses
"**Bridge pack**" with a specific referent: README:241 tags the CXDB trajectory store itself as
"Bridge pack", and README:408 names that pack "**raw-bodies → CXDB bridge pack**" — i.e. the
telemetry→CXDB **bridge is C24** (inventory C24 "Telemetry → CXDB ingestion bridge"), *not* the O(1)
branching primitive. So "Bridge + driver" most faithfully decomposes as **C24 (the bridge that lands
trajectories in CXDB) + C49 (the driver)**, both sitting over the **C21** store/primitive — not "C21 is
the bridge." The *architectural conclusion C49 draws is still correct* (C49 = driver; the O(1) branch
primitive + store = C21, which C49 depends on and must not duplicate); only the gloss on the word
"Bridge" is wrong, and it slightly muddies the C21-vs-C24 boundary. **Fix (applied).** Reworded §1 to
stop equating "Bridge" with the C21 primitive: "Bridge + driver" = the trajectory-landing **bridge pack
(C24)** + the **driver (C49)**, both over **C21**'s store + O(1)-branch primitive (C21 I5/I6, INV-3) — and
kept the (correct) point that C49 owns only the driver and reuses C21's primitive.

### RC49-02 — minor (fidelity / over-precise word) — INV-5 / AC-3 "reproduces" conflates the no-change control re-run with the variant re-run
**Claim.** INV-5 and AC-3 state the deterministic-tool slice "**reproduces** the original post-T outcome"
*and* "a variant change produces a clean diff." **Evidence.** A *variant* re-run on a deterministic node
changes the output **by design** — it does not "reproduce" the original; only the **no-change control**
re-run reproduces it. The two are run together (control + variant) and the claim is fine for the control
leg, but stating "reproduces" as the headline property of the *variant* path is loose and could be read as
"the variant also reproduces," which is self-contradictory. The intent (deterministic ⇒ the control
re-execution is byte-reproducible, so any variant difference is *attributable* rather than noise) is
correct and is the real load-bearing property. **Fix (applied).** Split the claim in INV-5 and AC-3:
the **control re-execution reproduces** the original post-T outcome (the reproducibility property), and
**because** the control is reproducible, a variant's difference is **clean/attributable** (not confounded
by re-execution noise). No semantic change — just stops "reproduces" from attaching to the variant leg.

### RC49-03 — minor (completeness / borrowed classifier not attributed) — the deterministic-vs-LLM "step classification" that the whole partition rests on is not assigned an owner
**Claim.** The entire G19 partition (tractable `deterministic-tool-replay` vs deferred
`counterfactual-reexecution`) hinges on a binary: does a post-T continuation "touch **only deterministic
tool nodes / twin-served deps**" or "involve **LLM steps / non-twinned effects**"? **Evidence.** C49
treats "deterministic tool node" as a clean, available class but never says **who classifies a node as
deterministic**. v4 locates deterministic-vs-LLM node discipline in **C16** (discipline-linter,
"LLM-where-tool") over **C12**'s formula node-kinds (`{agent, tool, gate, sub_formula}`, review-log D-7) —
that taxonomy is the source of truth for "is this step deterministic." C49 should *consume* that
classification, not silently assert its own. The spec defers "the deterministic-vs-LLM step classification
rule" to sweep-2 (§5) — good — but doesn't name where the rule *comes from*, so it reads as a C49-owned
invention (which would tip toward over-build / a parallel classifier). **Fix (applied).** Added a one-line
note at I6/§6 and the §5 sweep-2 deferral that the deterministic/LLM **node classification is C12's
node-kind taxonomy + C16's discipline check** (D-7), which C49 *consumes* to pick the fidelity class — it
does not define a classifier of its own. Keeps the partition; attributes its hinge.

### RC49-04 — minor (fidelity precision) — "deterministic tool node ⇒ pure function of branched state" omits the wall-clock/RNG/ambient-input caveat
**Claim.** §6 partition table and INV-5 assert that with "only deterministic tool nodes + twin-served
deps … re-execution is a *pure* function of the branched state." **Evidence.** A node labeled
"deterministic" can still read wall-clock time, a random seed, or ambient process state and thereby fail to
reproduce even with no LLM and a perfect twin. The reproducibility guarantee is really "deterministic
**and** input-closed over (branched state ⊕ twin-served deps)" — the un-stated assumption is that a
deterministic tool node has *no* hidden ambient inputs. This is a faithful-fill assumption, not a v4
statement, and it is exactly the kind of thing the deterministic-replay analogs (Temporal replay) handle
explicitly (Temporal forbids non-deterministic API calls in replayed code). **Fix (applied).** Qualified
INV-5 / the §6 table to "deterministic **and input-closed** (no wall-clock/RNG/ambient reads) tool nodes,"
flagged as a [FAITHFUL-FILL] borrowing the Temporal-replay determinism constraint (AI-CONTEXT:423), and
routed "which nodes qualify as input-closed" to the C12/C16 classification seam (RC49-03) at sweep-2.

### RC49-05 — minor (fidelity) — "reproduction CLAIMED for the tractable slice" should be scoped to the CONTROL, consistent with the inventory wording
**Claim.** The dispatch framing and spec say the tractable slice has "reproduction **claimed**" while the
LLM slice has "reproduction **NOT claimed**." **Evidence.** This is the right partition, but as written
(esp. AC-3 pre-fix, RC49-02) "reproduction claimed" can be misread as "the counterfactual reproduces,"
when what is claimed is that the **deterministic control re-execution** reproduces and therefore the
*comparison* is sound. The inventory itself only ever claims the *primitive* ("Re-runs a trajectory from a
midpoint via CXDB O(1) branching", inventory C49) — never that re-execution reproduces. So the honest
claim is narrower than "reproduction": it is **"the deterministic control re-execution is byte-reproducible,
so deterministic-node variant comparisons are attributable."** **Fix (applied).** Tightened §6 partition
"Fidelity" cell and §8 AC-3 to claim **reproducible control + attributable variant diff** for the tractable
slice (not bare "reproduction"), keeping the LLM slice's explicit no-reproduction stance unchanged. This
is purely a scoping tightening of an already-honest claim.

### RC49-06 — observation (no fix) — G19 framing, the capability-bar, D-6, and D-13 all PASS
**Claim / evidence (all verified, recorded so the integrator can see the attack landed):**
- **G19 honesty — PASS.** §1 box + §6 explicitly pick reading (b) (framed open problem), refuse reading (a)
  (claimed solution) as contradicting AI-CONTEXT:515, and AC-7 verifies the LLM slice is "**labeled and
  bounded**" and "explicitly **does NOT** assert reproduction." The deferred slice is routed to OQ-1 and the
  "heaviest human review" posture (README:470). The plan does **not** schedule a "solve G19" task
  (plan §1 header). This is the correct, non-over-claiming partition.
- **Capability-for-principle bar (HANDOFF §2) — PASS.** Drop-check (plan §6) drops trajectory store, custom
  branch impl, variant authoring (C47), stats (C48), twin/isolation engine (C44/C43); the **sole KEEP** is
  the branch-from-midpoint driver + the fidelity-labeled honest contract. New capability tied to P12, not
  hardening of an existing stack capability. No over-build flagged.
- **D-13 — PASS.** §1 boundary + INV-4 + the §2 table correctly place blast-radius/twin isolation on **C43**
  and the twin on **C44**; C49 "runs behind C43, against C44 twins," fail-closed on non-twinnable effects.
- **D-6 — PASS.** Header is "Track: canonical (single-track per D-6)"; no live "Track A/B" framing.
- **C21 citations — PASS.** I5 (O(1) branch), I6 (replay), INV-3 (no history copy) all match spec/C21
  exactly; C21 §1/§2 already name C49 as the downstream consumer. No contradiction with C21.
- **Twin-fidelity honesty (G22) — PASS.** §6 force (2) + OQ-5 correctly bound external-state mitigation by
  twin fidelity and defer the bar to **C45** (verified: C45 owns the "how close is close enough" bar, G22).
- **README/AI-CONTEXT quotes — PASS** (spot-checked: README:274/278/397/470/500; AI-CONTEXT:237/357/359/
  375/423/515 — all verbatim-accurate), except the "Bridge" gloss in RC49-01.

## Verdict
**accept-with-fixes.** This is a genuinely honest treatment of v4's single admitted-unsolved invention: it
names the capability, names *why* it is hard (LLM non-determinism + external-dependency state, the latter
mitigated-not-solved by C43/C44 and bounded by twin fidelity G22/C45), and partitions a real tractable-now
slice (deterministic-tool replay over C21's O(1) branch) from an explicitly-deferred research bet (full
LLM-step counterfactual, best-effort + variance-bounded + human-reviewed, **reproduction NOT claimed**).
The capability-bar, D-6, and D-13 all hold; the sole KEEP is correctly the driver + honest contract. All
five fixes are applied in place and are precision tightenings (mis-parsed "Bridge" label; "reproduces"
scoped to the control leg not the variant; the deterministic/LLM classifier attributed to C12/C16 rather
than C49-owned; the input-closed caveat on "deterministic ⇒ pure"). **Nothing architecturally significant
is deferred** — the one big open item (OQ-1, when an LLM-counterfactual is trustworthy enough) is *already*
correctly framed-not-closed by the spec and routed to the heaviest-human-review posture, which is the
faithful outcome, not a reviewer deferral.
