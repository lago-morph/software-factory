# Panel Sweep-2 — 03 · Substrate Realist (G11)

**Reviewer angle.** Everything in the 25-component spine rests on Gas City "native"
claims. My only question: are those claims honestly flagged as unverified-against-a-real-`gc`,
or are load-bearing ones silently assumed? And is the spine buildable TODAY, or is it a house
on sand until the D-23 spike runs?

**Sources read (targeted):** `gascity-config-anchor.md` (§3 key table, §4 native-claim table,
§5 prevent-vs-detect), `gascity-conformance-check.md` (Tests A–G + Outcome Routing),
`gascity-integration-runbook.md` (§3 city.toml, §7 conformance gate, needs-G11 summary),
`C01-gas-city-substrate.md` (§4.2 native-claim status, §6 G11/G03, §8.1 AC gate),
`C28-claude-code-agent-loop.md` (§3.3 RCM-SEAM-01 env-forwarding seam), and review-log
**D-23 / D-30 / D-31 / D-32 / D-34** + the substrate harvest (F1–F12) and spike protocol.

---

## VERDICT: `right-idea-change-X-before-building`

The substrate-honesty discipline is **genuinely good** — markedly better than the typical
"assume the dependency works" spec. The harvest grounds 6 of ~10 native claims in real
prototype evidence (F1–F12), and the four highest-risk claims I was sent to check are **all
honestly flagged, none silently assumed** (see Finding 1). That is the "right idea."

The change-before-building is narrow but hard: **one empirical run — D-23 Test A — gates the
entire P2/P3b security shape, and it has never executed.** The spine is buildable as specced
*for the Phase-0 / attended slice* TODAY; it is **NOT** buildable for any unattended (P2) or
self-modification (P3b) claim until Test A returns a verdict. The docs say this, but the
framing ("spec-now / verify-at-build") under-rates how much rework a DETECT-ONLY/SILENT result
forces. See the explicit call at the end.

---

## FINDINGS

### Finding 1 — The four highest-risk claims are honestly flagged. Verified, not assumed.

I checked each of the four the brief named. All four are flagged `needs-pinned-gc-run (G11)`
or `prevent-vs-detect-OPEN` consistently across anchor + spec + runbook. None is presented as
a verified fact:

| Risk | Status in corpus | Honestly flagged? |
|---|---|---|
| `[[rig]]` vs `[[rigs]]` city.toml spelling (D-32) | anchor §3 spelling note + key table = `needs-pinned-gc-run (G11)`; C01 §3.3 box; runbook §3 D-32 rule; D-32 in review-log | **YES** — and the *invariant that survives either spelling* (`path` ONLY in `.gc/site.toml`) is correctly isolated, so a build can proceed against the invariant even before the spelling resolves. This is the model the rest should follow. |
| `command` vs `cmd` tool-node key (D-34) | anchor §3 `[[tool]]` row = G11; C28 §3.4 cites D-34 verbatim and extends it to `[[hook]] command`; D-34 in review-log | **YES** — D-34 explicitly forbids claiming either spelling verified. C28 correctly propagates the same uncertainty to the hook field (good seam hygiene). |
| `CLAUDE_CODE_OAUTH_TOKEN` env-forwarding seam | C28 §3.3 **RCM-SEAM-01**, OPEN SEAM box: two readings (explicit `[[agent]] env` vs container-env inheritance), with the `gc internal/execenv` strip-risk named | **YES** — and this is the *best-written* uncertainty in the corpus: it names the concrete 401 failure both readings can produce and gives the operator a belt-and-suspenders mitigation. |
| prevent-vs-detect (D-30) | anchor §4 + §5 = `prevent-vs-detect-OPEN`; C01 §4.2/§8.1; conformance Test A KEYSTONE; runbook §7 | **YES** — flagged as the keystone everywhere, with the worst-case composite (A1∧A2) routing rule (RC01-S2-02) correctly applied. |

**This is the headline: the substrate honesty holds.** A 5/5-panel G11 flag has not been
papered over. The `[inferred — needs G11]` vocabulary (anchor §line 23) is used precisely
(e.g. `created_by` is NOT claimed as a verbatim field — anchor §4 / C01 §4.2 correctly say the
literal field name is inferred and `From`/`Assignee`/`session.id` are what the deep-dive
actually shows).

### Finding 2 — The conformance check is *necessary* but I can name three things it would miss.

The conformance check (the owed D-23 spike, operationalized) is well-built: exact commands,
PASS/FAIL/SILENT criteria, the composite-verdict rule, and an honest "Protocol Ambiguities"
section (§"Unrunnable Items") that pre-flags `bd create --prefix`, `gc events --since`,
`gc session list --json`, the dolt SQL port, and tmux pane-title fragility as
possibly-unrunnable-as-written. That self-awareness is exactly right.

What it would still miss — gaps that matter before building:

1. **The env-forwarding seam (RCM-SEAM-01) is NOT a conformance test.** Test A–G cover
   partition/twin/orders/attribution/reconcile/prefix — but there is **no test that boots a
   `claude` pane and asserts `CLAUDE_CODE_OAUTH_TOKEN` actually reached the process** (i.e.
   that `gc`'s `internal/execenv` did not strip it). This is the single most likely *first-boot*
   failure (Finding 4) and it is invisible to the current battery. The minimal stand-up
   (`gc status` green) can pass while every agent's API call 401s. **Add an A0/pre-flight test:
   inside a worker pane, `env | grep CLAUDE_CODE_OAUTH_TOKEN` returns the token.**

2. **Test A is run on the `gastown`/prefix partition, but D-31 + D-38 require a *worker-rig ≠
   judge-rig* two-rig city, and the holdout read-surface (worker MUST NOT read scenarios) is the
   real face D-30 protects.** The protocol probes rig1→rig2 and rig1→city reads — a reasonable
   proxy — but it never instantiates the actual `read_partition`/`write_partition` grammar
   (itself G11) or the scenarios partition. So a PREVENT verdict on the generic rig1/rig2 probe
   does **not** fully discharge C34's holdout boundary unless `read_partition` is wired and
   probed. The conformance check's Test A would report PREVENT while the holdout-specific config
   (still G11) remains unexercised.

3. **`[[service]]` / twin (Test B) targets C44 — which is OUT of the 25-component spine** (D-20
   split: C43 boundary-typing in-spine NOW, the twin half C44 *deferred*; HANDOFF §"backbone").
   So Test B is de-risking a component the spine does not build this pass. Not wrong to keep it
   (it's cheap to run in the same Docker session), but the conformance gate should not *block*
   the spine on Test B's outcome. The runbook §7 "Do not skip this gate" wording is slightly
   over-broad here.

### Finding 3 — "Buildable today" is true for the attended slice, false for the unattended claim.

The Phase-0 install (C01 §3.3 ~30-line skeleton) is grounded almost entirely in harvest-verified
facts: `gc start --foreground` (F6), tmux provider (F7), `bd`/Dolt (F8/F9), `IS_SANDBOX=1` (F12),
prefix mechanism (F10), pack-import strictness (F3), the `gc init`-bypass authoring path (F4).
An engineer can stand up a single-rig, attended, human-in-the-loop factory from the runbook
**today** with high confidence — the unverified items there (`[mail]`, `[formulas]`, `[events]`,
`[[service]]`, non-tmux providers) are all Phase-1+ and correctly fenced off by section-absence
(INV-4 fail-safe-to-off).

But the spine's *reason for being* is the safe **self-build** — which is P3b (self-modification)
and trends toward P2 (unattended). D-30 is binding: those require **prevent**, and prevent is
`OPEN`. So the precise truth is: **the spine is buildable today up to the D-30 gate, and the
gate is closed.** Calling the whole spine "buildable, verify-at-build" blurs the line between
"build the Phase-0 substrate now" (true) and "build the unattended self-build loop now" (false
until Test A). The corpus mostly respects this (C01 §7 keeps P2/P3b human-in-the-loop), but the
*sequencing* needs to be stated as a hard ordering, not a caveat.

### Finding 4 — Single highest-probability first-deploy failure: the OAuth env-forwarding seam (E-C28-03), not the prevent gate.

The prevent gate is the highest-*architectural*-risk unknown. But the highest-*probability
first-deploy* failure is mundane and upstream of everything: **`CLAUDE_CODE_OAUTH_TOKEN` not
reaching the `claude` pane process → 401 on the first API call → every agent stalls** (C28
E-C28-03; RCM-SEAM-01 Reading A vs B). Why this is #1:

- It fires at the very first agent turn, before any partition/order/twin behavior is exercised.
- Both readings of the seam can produce it (token absent from `[[agent]] env`, OR `gc` strips
  token-bearing vars before spawning) — and **which reading is correct is itself G11**, so the
  operator cannot pre-empt it from the spec alone.
- It is **not covered by the conformance battery** (Finding 2.1), so the current gate would wave
  the install through (`gc status` green, panes spawned) and the failure surfaces only when work
  is dispatched.
- Runner-up is **E-C01-06 misplaced-key startup refusal** (PackV2 is strict — F1/F3; a `path` in
  a `city.toml` rig block, or a duplicate transitive `maintenance` import, refuses startup). But
  that fails *loud and early* at boot with a clear error, so it is lower-severity than the silent
  401 stall. The dolt `DOLT_REF=refs/heads/dolt-data` proxy requirement (F9, E-C01-10) is third —
  also loud, and already harvest-verified.

---

## SHARPEST OBJECTION

**The conformance check is written as a one-shot PASS/FAIL gate, but its keystone (Test A) has a
prerequisite the corpus treats as already-built — and it is also G11.** Test A's PREVENT verdict
is only meaningful if the *thing being prevented* is configured: the worker-rig/judge-rig split
(D-31/D-38) and the `read_partition`/`write_partition` grammar (anchor §3, C42:OQ — **G11**). The
spike protocol §3 probes a generic rig1→rig2 read, which is a reasonable smoke test, but it does
**not** wire the holdout partition. So there is a circularity the docs don't surface: *we need a
pinned `gc` run to learn the `read_partition` grammar; we need the `read_partition` grammar wired
to truly test whether the holdout is prevented.* A PREVENT result on the generic probe could be
read as "D-30 satisfied, build unattended" when the holdout-specific surface — the one that
actually matters for D-17/C34 — was never exercised. **Test A as written can return a
false-green for the holdout boundary.** The fix is small: make Test A's setup explicitly include
a scenarios partition and the (G11-discovered) partition grammar as a second probe, and state
that the generic-prefix PREVENT result discharges C43 boundary-typing but **not** C34 holdout
until the scenarios-partition probe also passes.

---

## CHANGE-BEFORE-BUILDING

1. **Add an env-forwarding pre-flight to the conformance check** (new Test A0, ahead of the
   battery): boot one `claude` pane, assert `CLAUDE_CODE_OAUTH_TOKEN` is present in the pane
   process env AND a trivial API call returns 200. This closes the #1 first-deploy failure
   (Finding 4) and resolves RCM-SEAM-01's two readings empirically in the same run. Cheap; high
   value; currently missing.

2. **Split Test A's discharge: C43 (boundary-typing) vs C34 (holdout).** State that the generic
   rig1/rig2 PREVENT result discharges C43 only; C34's holdout boundary additionally requires a
   scenarios-partition probe with the (G11-discovered) `read_partition` grammar wired. Prevents
   the false-green in my sharpest objection.

3. **State the build ordering as a hard gate, not a caveat.** "Phase-0 attended substrate:
   build now. Unattended (P2) / self-modification (P3b) loop: BLOCKED on Test A overall-PREVENT
   (or the D-30 watcher landing)." The corpus has all the pieces (C01 §7, D-30); it needs to be
   one unambiguous ordering sentence in the runbook §7 so no builder reads "spec-now/verify-at-
   build" as license to wire the unattended loop before the spike runs.

4. **Decouple the spine gate from Test B (C44/twins).** C44 is deferred out of the spine (D-20);
   Test B should be marked "run opportunistically, does NOT block spine components." Tightens
   runbook §7's "do not skip this gate."

---

## EXPLICIT CALL — must the empirical D-23 spike run before ANY implementation starts?

**No — and forcing it to would be the wrong call. But a hard *partial* gate is required.**

- **Spec-now is fully acceptable, and is already done well.** Writing the spine to implementation
  depth against the unverified substrate is sound *because* the corpus flags every unverified
  claim with `needs-pinned-gc-run (G11)` and isolates the spelling-independent invariants (the
  `[[rig]]`/`path` split is the template). Authoring is not blocked.

- **Building the Phase-0 / attended substrate is acceptable BEFORE the spike** — every claim it
  rests on is harvest-verified (F1–F12). The spike de-risks; it is not a precondition for the
  attended install. (This matches HANDOFF §0.3.5: "the spike is owed … it does not block defining
  the components.")

- **The spike IS a hard precondition for two specific things, and these must not be built first:**
  (a) **any unattended (P2) or self-modification (P3b) loop** — D-30 binding, gated on Test A
  overall-PREVENT; and (b) **any spec text or code that assumes the bead prefix *enforces*** —
  anchor §5 builder-rule. Build-order must therefore be: author + build attended Phase-0 →
  **run the spike the moment Docker exists** → only then wire the unattended self-build face
  (and the D-30 watcher if Test A is DETECT/SILENT).

- **One correction to the "verify-at-build" framing:** a DETECT-ONLY or SILENT Test A result does
  not just annotate a spec — it *mandates building a new component* (the D-30 blocking watcher,
  at the OS level if A2 is SILENT). That is not a caveat absorbed at build time; it is a branch
  that reshapes the security architecture and adds scope. So "verify-at-build" is fine *for the
  attended slice* but is the wrong mental model *for the unattended slice* — there, it is
  "verify-before-you-can-even-scope." The spike should run as early as a Docker env is available,
  not deferred to whenever the unattended components come up in build order.

**Bottom line:** Honest substrate discipline (verdict: right-idea). Build the attended Phase-0
now; do not let any builder wire the unattended/self-modifying face until Test A returns
overall-PREVENT or the watcher lands; and add the OAuth pre-flight before the first real deploy,
because that 401 — not the prevent gate — is what kills the first boot.

---

*Authored 2026-06-01 by the Substrate Realist (G11), Sweep-2 depth panel. Grounded against
gascity-prototype@b14c278 harvest (F1–F12), D-23 spike protocol, conformance check, and
decisions D-23/D-30/D-31/D-32/D-34. No `gc` was run (live-run still OWED — needs Docker).*
