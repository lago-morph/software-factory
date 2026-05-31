# Adversarial review — C30 Scenario Authoring & Store (canonical track, sweep 1)

Reviewer persona: Adversary / critic-fixer — Evaluation & Judge (C30)
Target: spec/C30-scenario-store.md (+ plan-faithful/C30-scenario-store.md)
Posture: canonical / faithful — attack FIDELITY + COMPLETENESS, plus the HANDOFF §2
capability-for-principle bar (flag hardening on existing-stack capability, not new capability tied to a
12-principle). Binding decisions D-1..D-14 flagged only if violated.

## Findings

### RC30-01 — major — "Day-0 scenario signing" is a D-14 violation + premature hardening; git content-addressing + isolation already give Phase-0 tamper-evidence. **DEFER.**
**Claim.** §1 (Responsibilities bullet 4) keeps day-0 signing as "the one genuine low-effort custom artifact
C30 adds beyond Inspect AI … the bar: KEEP — serves P5/P6 holdout integrity, no off-the-shelf piece provides
it." It is hardened into a load-bearing **invariant** (INV-4 "every scenario is signed at authoring time"),
an **interface** (I5), a **data-model row** (Day-0 signatures), an **acceptance criterion** (AC-5), a **plan
task** (T5), and a **freeze milestone** (M4).
**Evidence (four independent problems).**
1. **Violates D-14 (binding).** D-14 settled the *materially identical* signing question for C41:
   signing is **optional/deferred → FE-3, blocked on G37** ("Signing stays deferred (Bet 2 → FE-3) …
   resolves the old 'signing mandatory vs optional' → optional/deferred (README:229)"). XC-6 (the C41/C03
   finding D-14 resolves) is explicit: "plaintext keys in `city.toml` collapse the ladder. **Signing is a
   mechanism, not yet a control, until C03's SecretResolver lands.**" C30 re-introduces *mandatory* day-0
   signing as a KEEP and an invariant — exactly the posture D-14 retired. The brief lists D-14 as a binding
   decision to flag if violated; it is violated.
2. **Fails the capability-for-principle bar (HANDOFF §2).** The scenarios live in a **separate git repo**
   (INV-1). Git's object store is content-addressed (AI-CONTEXT:404), and v4 *itself* establishes
   content-addressing ⇒ tamper-evidence as the recognized pattern (AI-CONTEXT:236, BLAKE3 →
   "tamper-evidence"). So at Phase-0/2 the **git commit history over the scenario repo** (immutable,
   content-addressed, attributable to the committing `scenario_authoring` rig) **plus** the
   `scenarios`-partition / `scenario_authoring`-rig isolation **already** deliver tamper-evidence + provenance
   for the corpus. A custom signature adds **no new capability the git+isolation stack does not already
   provide at Phase-0**. The one capability a signature *would* add beyond git — cryptographic
   non-repudiation against an attacker who can rewrite git history — **requires a key**, and there is **no
   secrets store** (G37 open, owned by C03). A plaintext key collapses precisely that assurance (XC-6/D-14).
   So signing is hardening-on-existing-stack-capability, not new capability tied to a principle → **DROP/DEFER
   per the bar.**
3. **Fidelity overreach on the F9 source.** The *only* v4 source for "day-0 signing" is the
   F-MODE-COVERAGE F9 cell. The spec quotes it as `F9 "Cryptographically signed scenarios at day-0"` but the
   actual cell reads **"Cryptographically signed scenarios at day-0 *(gene transfusion from GF-C pattern)*"**
   — i.e. v4 scopes it as a **Phase-3+ gene-transfusion artifact**, not a Phase-2 storage primitive. The spec
   silently drops the `(gene transfusion from GF-C pattern)` qualifier and promotes a transfused Phase-3+
   pattern into a Phase-2 storage-layer invariant. Worse, the spec's *primary* source — the README Principle-5
   section — names signing **nowhere**; its placement summary says holdout enforcement is "filesystem
   permissions + agent-prompt discipline + audit logging" (README:177). "Day-0 signing" is therefore a
   single-cell, mis-scoped citation elevated to a KEEP.
4. **F7 baselining does not need C30-owned signing.** §6/AC-5 lean on F7 ("periodic baselining against
   signed scenarios"). F7 is a *Healer* (C36/C39) behaviour over the corpus; baselining can verify the corpus
   against its **git revision** (the Phase-0-available content-addressed identity) without a C30-authored
   cryptographic signature. F7 does not establish a C30 signing obligation.
**Fix (APPLIED — DEFER, not a fresh architectural call: applying the existing D-14 ruling).** Throughout
spec + plan, demote day-0 signing from KEEP/invariant/AC to **DEFERRED → FE-3 (blocked on G37, per D-14)**,
and name **git commit history over the separate scenario repo as the Phase-0/2 tamper-evidence + provenance
mechanism** (consistent with AI-CONTEXT:236/404 and INV-1). Specifically: §1 bullet 4 rewritten as a
DEFER-with-rationale; INV-4 replaced by a git-revision-integrity invariant; I5 / §4 row / AC-5 / T5 / M4 /
the §5 author-flow step / §7 security / OQ-3 re-pointed to "git content-addressing now; cryptographic signing
= FE-3 when G37 lands." F9 re-cited *with* its `(gene transfusion from GF-C pattern)` qualifier and marked
Phase-3+. This is a confident apply because D-14 already dictates the outcome — C30 is the one component that
re-opened a settled question.

### RC30-02 — minor — F9 is mis-quoted (qualifier dropped) wherever it appears.
**Claim.** §1, §3 (I5), §6 (F-mode table, INV-4 note), and AC-5 all cite F9 as "Cryptographically signed
scenarios at day-0" with no qualifier. **Evidence.** The F-MODE-COVERAGE F9 row is "… at day-0 **(gene
transfusion from GF-C pattern)**" and its sibling F7/F55 rows treat "signed scenarios" as the same
transfused mechanism — none of them a Phase-2 storage primitive. Quoting the cell without the qualifier
mislabels a Phase-3+ transfused pattern as a v4-mandated storage-layer fact. **Fix (APPLIED).** Folded into
RC30-01's apply: every F9 citation now carries the `(gene transfusion from GF-C pattern)` qualifier and the
Phase-3+ scoping. (Severity minor as a standalone citation-hygiene issue; the load-bearing consequence is
RC30-01.)

### RC30-03 — minor — INV-5 / AC-1 assert "valid Inspect AI `Task`" as a property C30 enforces, but C30 is an adopter of an unverified upstream (G11-class).
**Claim.** INV-5 "scenarios are valid Inspect AI `Task` artifacts; C30 stores no bespoke scenario format,"
AC-1 "scenarios are authored as Inspect AI `Task` artifacts." **Evidence.** Inspect AI is an *adopted,
unverified* third-party (G11 — every "Native"/adopted-OSS claim is unverified; no version run). "Valid
`Task`" is whatever the pinned Inspect AI accepts — a property C30 *inherits from the upstream*, not one the
C30 spec independently defines or enforces. Asserting it as a C30 invariant slightly overstates, the same
adopted-property pattern RC23A-03 flagged for C23. **Fix (APPLIED).** Qualified INV-5/AC-1 to "valid against
the *pinned* Inspect AI `Task` schema (an adopted-upstream property verified by the conformance pack /
version pin, G11), not a C30-defined format" — keeps the no-bespoke-DSL point (correct, README:170) without
claiming C30 owns Task validity.

### RC30-04 — minor — D-13 boundary is honoured, but two "addresses Gxx" claims over-reach into enforcement language.
**Claim.** §8 AC-7 header reads "AC-7 … addresses G10/G21/G28"; §6 G21 says C30 "addresses G21 … at the
storage/authoring altitude." **Evidence.** This is *almost* right and the spec is careful elsewhere (it
repeatedly and correctly routes enforcement to C34, partition to C42, per D-13 — verified against C42 §1/§2
and review-log D-13, no contradiction found). But "C30 addresses G21" overstates: per D-13 + the C42 spec,
**G21 is not C30's to address at all** — C30's stored-corpus placement merely makes the boundary
*well-defined*; G21 (enforcement has no mechanism) is wholly C34's (enforcement) + C43's (blast radius).
C30 *contributes to the precondition*; it does not "address" G21. **Fix (APPLIED).** Softened to "C30
**makes G10/G28 resolvable at the storage altitude and supplies the well-defined boundary G21's
C34/C43 resolution needs**; C30 does not itself address G21" — matches the D-13 split the rest of the spec
already states. (No change to the substantive, correct routing.)

### RC30-05 — minor — `created_by` scenario-attribution fill cites C41/README:226–231, which is the *identity* model, not a scenario-corpus attribution mandate.
**Claim.** §4 [FAITHFUL-FILL] adds `created_by` to the stored scenario record, "mirrors the corpus-wide
attribution requirement (C41; README:226–231)." **Evidence.** README:226–231 is the P9 identity/attribution
table ("Every action carries identity … beads, events native `created_by`"). Scenario *files in a git repo*
are not beads/events, so `created_by` on a scenario record is a reasonable *faithful inference* (attribution
is P9-native and the `scenario_authoring` rig is the actor) — but it is an **inference**, not a v4
requirement that scenario *files* carry `created_by`; git already records the committing actor. The fill is
defensible and minimal; it is just labelled slightly too strongly. **Fix (APPLIED).** Re-tagged the
`created_by` element as a faithful inference whose Phase-0 realization is **the git commit author**
(the rig), with an explicit `created_by` field deferred to the sweep-2 record decision (OQ-1) — keeps P9
attribution without asserting a v4 mandate or a second attribution mechanism alongside git.

### RC30-06 — minor — Plan T5 / M4 / DoD still gate seams on a signing artifact now deferred; left consistent by the RC30-01 apply.
**Claim.** plan §1 T5 ("Day-0 signing"), §4 M4 ("scenario-path feed + signature frozen"), §5 risk 4, §6 DoD
("scenarios are day-0 signed") all treat signing as build/freeze scope. **Evidence.** With RC30-01 deferring
signing, these would dangle. **Fix (APPLIED).** T5 retitled "Corpus integrity via git revision (signing
deferred → FE-3/G37)"; M4 drops the signature-format freeze (git-revision identity only); risk 4 and DoD
re-pointed to git-revision integrity with cryptographic signing as the FE-3 trigger. Plan and spec now agree.

## Verdict
**accept-with-fixes.** The spec is strong on the load-bearing axis the orchestrator cares about — the **D-13
storage/enforcement seam is correct and consistently held** (C30 stores/authors, C42 provides the partition,
C34 enforces+audits; no OPA, no custom DSL, Inspect AI adopted verbatim) and the G10/G28 storage-side
resolutions are honest (held-out = policy intent verified after-the-fact by C34, not a C30 guarantee). The
one real defect is **day-0 signing**, which is simultaneously a D-14 violation, a capability-for-principle-bar
failure (git content-addressing + isolation already give Phase-0 tamper-evidence; the delta needs a key that
G37 hasn't provided), and a mis-scoped F9 citation (a Phase-3+ gene-transfusion pattern promoted to a Phase-2
storage invariant). Because **D-14 already dictates the outcome** (signing optional/deferred → FE-3), the fix
is applied confidently rather than deferred. All six findings fixed in place; **nothing left
`DEFERRED — needs orchestrator decision`** — the signing question was already decided by D-14, so applying it
is fidelity, not a new architectural call.
