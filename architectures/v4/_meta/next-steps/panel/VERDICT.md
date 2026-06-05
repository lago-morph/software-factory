# Panel verdict + adopted amendments

The [unified plan](../10-unified-plan.md) went before a 6-person adversarial panel (real subagent
dispatches, per the repo's adversarial-review rule). **Every reviewer returned
`accept-with-named-amendments`** — the macro-shape (*calibrate the instrument → drive one trustworthy
nail → widen only behind the fence*) was accepted by all six; none rejected it. The amendments below
are the changes the panel required, de-duplicated and adopted into the
[final plain-language report](../../../../../next-steps-plain-english.md).

| # | Reviewer verdict | Headline |
|---|---|---|
| [01 architect/methodology](./01-architect-methodology.md) | accept-with-amendments | calibration has a chicken-and-egg; holdout is logically prior |
| [02 safety/security](./02-safety-security.md) | accept-with-amendments | fence = hard PREVENT per D-30; Term-4 integrity unowned; leak probe must cover writes |
| [03 eval/measurement](./03-eval-measurement.md) | accept-with-amendments | calibration is statistically non-falsifiable as written |
| [04 delivery/SRE](./04-delivery-sre.md) | accept-with-amendments | scope too big; "clusterless line" isn't clusterless; parallel rigs ≠ throughput on one seat |
| [05 bootstrap-skeptic](./05-bootstrap-skeptic.md) | accept-with-amendments | architecture-spec→buildable-spec is human-authored; `[PROPOSED]` holes drive spec-corner no-go loops; no transfusion exemplar |
| [06 operator/product](./06-operator-product.md) | accept-with-amendments | open plainly; surface the operator's decisions; name the felt-progress gap |

## Adopted amendments (folded into the final report)

**AM-1 — Make judge calibration buildable, statistically honest, and independent.** (R1+R3+R4)
- Resolve the chicken-and-egg: seed the calibration set with **synthetic/fixture trajectories** for the
  `system`/`scenario` corners (which don't exist before the first build), and **split** the gate into
  *design-now* / *populate-after-first-build*.
- Gate on a **statistical upper bound** on the false-green rate with a **per-corner minimum sample
  size**, not a point estimate on a tiny matrix.
- Use **≥2 human labellers + an inter-rater agreement check**; exclude contested trajectories.
- Keep the **cross-family judge** (a same-family judge's errors correlate with the coder's).
- **Time-box it** (fixed small N, coarse bar) so it doesn't consume week 1.

**AM-2 — Put holdout integrity first, and cover the *write* path.** (R1+R2+R3)
- Run the holdout-integrity check **before/with** calibration — calibrating over leakable scenarios
  calibrates against a lie.
- The leak probe must test the **authoring/write path** (a worker weakening a spec or scenario until its
  own output passes), not just reads — per [C34 §1.2 / D-44/D-45](../../../spec/C34-holdout-integrity.md).
- Author held-out scenarios in an **independent rig/role**, not solely from the component's own
  acceptance criteria (own-AC scenarios aren't independently held out).

**AM-3 — Honor the binding fence rule (D-30).** (R2)
- If the substrate is **detect-only**, unattended operation is **blocked at human-in-the-loop** until
  prevention is established — per [C43 / D-30](../../../spec/C43-isolation-boundary.md), this is binding,
  not a "trust annotation." The final report makes a detect-only result a hard block on any unattended
  widening.

**AM-4 — Stand up a real Term-4 integrity + rollback harness.** (R2)
- Make a minimal **post-deploy factory-integrity check + rollback** an explicit exit of the first-build
  gate, or C53's Term 4 is paper on a self-modifying system
  ([C53 §3.2 Term 4](../../../spec/C53-bootstrap-validation.md)).

**AM-5 — Name the real recursion seam: the spec-completion pass.** (R5)
- agent-os specs are *architecture-of-record* with deliberate `[PROPOSED — not in source]` holes; those
  holes are what held-out scenarios score, so a raw agent-os spec drives `root_cause = spec` no-go loops.
- Add an explicit **human-or-factory spec-completion pass** that closes the `[PROPOSED]` holes into a
  complete buildable spec **before** dispatch; state that the C11→C08 step is **human-authored** (C11
  enforces field presence, not quality); put the named-behavior list in the gate's evidence bundle.
- The "needs more substrate" fallback does **not** fit this failure (the fix is a spec pass, not a
  component) — name a distinct "complete the spec and re-run" branch.

**AM-6 — Provide a named, license-cleared gene-transfusion exemplar for the first build.** (R5)
- [C51](../../../spec/C51-gene-transfusion.md) requires ≥1 external exemplar and **excludes adopted OSS**
  (CloudEvents/JSON-Schema) from transfusion. Name + license-clear B12's exemplar before dispatch, or
  choose a first build whose exemplar is real and permissive.

**AM-7 — Right-size the window to one operator + one Max seat.** (R4+R5)
- The four-component "clusterless line" (B3→B16→B6→B9) is **not** clusterless — B16/B6/B9 depend on A1
  (LiteLLM). Even B12 has a runtime half; score only its **clusterless core** for the first `go`.
- "Multiple rigs" is **config partitioning, not added compute** — on one Max seat, rigs **serialize**;
  do the cost back-of-envelope at Gate 0, not after the topology is set.
- While the judge is uncalibrated, C53 forces `oversight_level = full`, so the widening phase is
  **serial human-gated builds**, not a batched line. Realistic in-window yield is **B22 (design) +
  B12-core (code)**, with the production line as horizon.

**AM-8 — Make it legible and decision-forward for the operator.** (R6)
- Open in plain language; **surface the calibration bar + sample size as an explicit operator
  decision** with a recommended default; **name the felt-progress gap** (no agent-os *code* ships until
  the first real build); reframe twin-starvation as a **planned milestone** that exits on a "twins are
  next" decision brief, not a risk that ambushes.

## Preserved (consensus — do not weaken)

Calibration as a **hard precondition** (all six named it); **prevent-vs-detect** as the near-zero-cost
first action; the **corner-routed defect ledger** + corner-rate **Goodhart tripwire**; the **100% floor
as a boolean** with the satisfaction distribution as *diagnostic evidence*; the **cross-family judge**;
`no_go` as a **first-class, shipping-blocked terminal**; **cost measured before fan-out**; the **twin
gap surfaced empirically** as the next factory-build; and the genuine, non-decorative **agent-os**
connection with honest "unproven by construction" candor and gates-not-day-counts.
