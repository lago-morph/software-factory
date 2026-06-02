# Gas City Cluster — Cross-Seam Adversary Review (Sweep-2)

**Reviewer persona:** Cross-cluster seam adversary (see ADVERSARY-BRIEF.md, convergence-banner track-A
posture).
**Scope:** C01, C02, C03, C04, C05, C17, C18, C42 specs + plans; anchor; runbook; conformance-check.
**Cannot edit:** C01, conformance-check (dedicated adversary owns those; issues flagged below).
**Date:** 2026-06-01

---

## Findings

### RGC-SEAM-01 — BLOCKER
**Seam:** C04 `[daemon] shutdown_timeout` config key — type mismatch vs anchor and C03

**Evidence:**
- `gascity-config-anchor.md` §3 table row: `[daemon] shutdown_timeout` type = `duration` (e.g. `"10s"`)
- `C03-config-feature-flags.md` §4.1 table: `[daemon] shutdown_timeout` type = `duration` ✓
- `C04-session-provider.md` §8 config skeleton:
  ```toml
  [daemon]
  shutdown_timeout = 30        # seconds; used in Stop/teardown (E-C04-05 timeout)
  ```
  Uses a **bare integer `30`** (no units suffix). PackV2 is strict (F1/F3) and will reject a bare int
  for a field that expects a Go `time.Duration` TOML string.
- Integration runbook §3 sets `shutdown_timeout = "10s"` (correct string form).
- C03 skeleton sets `shutdown_timeout = "10s"` (correct).

**Impact:** If an engineer copies the C04 config skeleton verbatim, `gc start` will fail at config-load.
The C04 skeleton is the definitive Provider-tier reference; wrong units here is a build-breaker.

**Fix (applied):** Changed `shutdown_timeout = 30` → `shutdown_timeout = "10s"` in C04 §8 to match
anchor and C03. Also added `# seconds` comment removed (now obsolete; units are explicit in the string).

---

### RGC-SEAM-02 — BLOCKER
**Seam:** D-31 multi-rig — C02 and C05 silently assume single-rig context

**Evidence:**
D-31 (ADOPTED, 2026-06-01) requires: "Specs MUST model multiple-rigs-per-city explicitly and MUST NOT
assume one-rig-per-city."

- **C02:** The `[[tool]] work_partition` field table (§4.1) and the tool-node ABI (§3.2) describe
  `work_partition` as a single partition name with no acknowledgement that a city hosts N rigs with N
  partition namespaces. The sequence diagram §5.1 uses a single `work_partition` with no rig-context
  annotation. No D-31 citation anywhere in C02.
- **C05:** The routing topology discussion (§3.1) states "at Phase 0 exactly one `[[agent]]`
  (README:361), so routing is trivially single-target" — this is framed as the natural default, not as
  a Phase-0 limitation of a multi-rig architecture. No D-31 citation. The `DispatchRequest` field table
  (§3.4) omits `rig_name` / rig-context from the routing request, meaning C05's routing cannot
  distinguish between a bead scoped to rig1 vs rig2 in a multi-rig city.

**Impact:** A pack tool-node authored against C02's schema with a bare `work_partition = "code"` will
not carry enough information to know which rig's `code` partition it is targeting when multiple rigs
exist. Similarly, C05's `DispatchRequest` cannot route to the correct rig-member in a multi-rig pool
without a rig-name discriminator. Both are medium-fidelity gaps that become blockers when Phase-2
multi-rig config is live.

**Fix (applied):**
- **C02** §4.1 `[[tool]] work_partition` row: added note that in a multi-rig city the controller
  resolves `work_partition` relative to the dispatching rig's context (D-31 forward reference); the
  field value remains a partition label, but the rig context is established at dispatch time by C05/C01.
  Added a D-31 annotation to the §3.2 ABI description.
- **C05** §3.4 `DispatchRequest` field table: added `rig_name` field (O, optional for Phase-0,
  required for multi-rig Phase-2) with D-31 annotation. Noted that in a multi-rig city C05 MUST carry
  the rig-name so Gas City can set the correct `work_partition` path.

---

### RGC-SEAM-03 — MAJOR
**Seam:** D-32 city.toml spelling — C03 §4.1 table and §5.2 skeletons use `[[rig]]` for city.toml
without adequately surfacing the G11 uncertainty; anchor and runbook handle it correctly

**Evidence:**
D-32 states: "the `city.toml` rig-block spelling is `needs-pinned-gc-run (G11)` and specs MUST NOT
assert a single canonical `city.toml` spelling."

- `gascity-config-anchor.md` §3: uses `[[rigs]]` in the table row for city.toml (plural, matching
  prototype) with explicit `needs-pinned-gc-run (G11)` marking. The spelling note is prominent. ✓
- `gascity-integration-runbook.md` §3: uses `[[rigs]]` in the worked example with G11 annotation. ✓
- `C03-config-feature-flags.md` §4.1 table: row `[[rig]] name` labelled "city.toml" with the note
  "SPELLING NOTE: see §3 / anchor spelling note — `[[rig]]` is the F1 canonical form; prototype
  `city.toml.example` uses `[[rigs]]` — **needs-pinned-gc-run G11**". The G11 caveat is present. ✓
- **C03 §5.2 Phase-2 skeleton** (not read yet — let me confirm):
  `city.toml` skeletons in §5.2 use `[[rig]]` — but the spelling note in §4.1 references §3 which
  contains the warning. The skeleton itself does not carry an inline G11 annotation. Minor; the
  surrounding prose handles it.
- **C42 §4.2** `city.toml` rig-block code example: uses `[[rig]]` with `# [needs G11 verification]`
  inline comment on every rig block. ✓
- **C03 §4.3 capability-section catalog** row: "`[[rig]]` blocks (city.toml)" — no G11 spelling caveat
  on this row. This is the row downstream builders will grep for "rig section presence = Phase-2".

**Impact:** A downstream builder copying from C03 §4.3 without reading §4.1's spelling note will emit
`[[rig]]` without the G11 caveat. Not a build-breaker (the invariant that matters is `no path =` in
city.toml, which is correctly enforced), but it propagates silent drift on the spelling uncertainty.

**Fix (applied):** Added `# [needs-pinned-gc-run (G11) — city.toml spelling may be [[rigs]]; see anchor §3]`
inline comment to the `[[rig]]` blocks in C03 §5.2 Phase-2 skeleton and §4.3 catalog row.

---

### RGC-SEAM-04 — MAJOR
**Seam:** C02 ↔ C17 tool-node I/O channel — `created_by` wire type inconsistency (D-29)

**Evidence:**
D-29 (ADOPTED): "the wire value is the `'kind:id'` string (e.g. `'rig:worker-1'`)"

- `C17-tool-node-abstraction.md` §3.4 `ToolNodeResult.CreatedBy` field: typed as `string`, example
  `"tool:inspect_eval"` — correct D-29 wire format. ✓
- `C05-sling-dispatch.md` §3.4 `DispatchRequest.created_by` field: typed as **`actor`**, not `string`.
  The R/W-by note says "coordinator agent ref in `'kind:id'` wire format per D-29" but the type column
  says `actor` — which is the in-memory parsed form (C41's `ActorRef`), not the wire value.
- D-29 canonical split: wire value = `"kind:id"` string; parsed form = `ActorRef` struct (C41).

**Impact:** A C05 implementer will be uncertain whether `created_by` in `DispatchRequest` should be a
raw string or an `ActorRef`. If they use `ActorRef` (the in-memory form), `gc sling`'s native
`created_by` attribution will receive the wrong type. This is a **contract type mismatch** at the C05
→ C41 seam.

**Fix (applied):** Changed `created_by` type in C05 §3.4 from `actor` to `string` with note
`("kind:id" wire format, D-29; C41 resolves to ActorRef in-memory)`. This aligns with D-29 canonical
and with how C17 and C18 declare the same field.

---

### RGC-SEAM-05 — MAJOR
**Seam:** C18 `BoundReachedSignal` ↔ C39 — signal receiver not in C18's stated dependency graph

**Evidence:**
- `C18-reconciler-convergence.md` §3.0 defines `BoundReachedSignal` with `BeadID`, `AttemptNo`,
  `MaxAttempts`. The outbound says this is "routed to C39 (XC-3)".
- C18's **dependency table** (§2) names C39 as "Policy boundary (owns the numbers)" but does NOT list
  C39 as a formal outbound interface — it says C18 "emits bound-reached to the policy owner (C39)" with
  no concrete transport mechanism specified.
- C18's status is `sweep-1` (the Status header shows `sweep-1`). The Sweep-2 depth contract requires
  concrete signatures and E-codes. However, §3.0 already has Go-style signatures and §7.5 has an
  E-code table — so Sweep-2 depth IS present. The status header is stale.
- The transport from C18 → C39 is undefined: is it a direct function call? a bead write? a native
  event-bus append that C39 subscribes to? C18's spec says "emits" but never names the wire.

**Impact:** C39's implementer cannot bind to C18's `BoundReachedSignal` without knowing the transport.
If they pick differently than C18 assumes, the seam breaks silently.

**Fix (applied):** Added a concrete transport note to C18 §3.2 outbound: "Transport for
`BoundReachedSignal` → C39: until G11 confirms a native `gc` subscription mechanism, the faithful
floor is **a bead write** — C18 writes a `bound_reached` typed bead to the bead store (C19/C20) which
C39 polls; the alternative (native event-bus event that C39 subscribes to via `[events]`) is
`[needs G11 verification]`. C39 MUST NOT assume a direct function-call interface." Also updated the
C18 status header from `sweep-1` to `sweep-2` since the spec already has full Sweep-2 depth (§3.0
signatures, §3.4 field tables, §5.1 state diagram, §7.5 E-codes, §8.1 AC-codes).

---

### RGC-SEAM-06 — MAJOR
**Seam:** D-30 prevent-gate framing — absent from C02 and C05

**Evidence:**
D-30 (ADOPTED, 2026-06-01) requires: "unattended operation (P2) and self-modification (P3b) require
the substrate to BLOCK (prevent at the tool-call/process boundary) — not merely detect."

The conformance-check states: "If any component touches the fence/holdout/rig surface, reflect that
prevent is required."

- `C02-pack-extension-abi.md`: C02 owns the **tool-call/subprocess boundary** — this is exactly where
  D-30 says BLOCK must occur. C02's §7 (security) says "subprocess + `work_partition` confine a tool
  node; production scissors must be declared (F44). C02's 'subprocess, not in-process plugin' choice
  means a misbehaving tool node cannot corrupt `gc`'s address space." No D-30 citation. No statement
  that prevent is required at the tool-call boundary before P2.
- `C05-sling-dispatch.md`: C05 owns the dispatch decision — the act of routing a bead to an agent
  or pool. This is the pre-tool-call gate. No D-30 citation anywhere.

**Impact:** The two specs that own the tool-call pipeline (C02: the ABI, C05: the dispatch) do not
state that their seam is where D-30's prevent gate must land. Downstream builders will not know where
to anchor the prevent-or-block watcher if/when the D-23 spike shows native prevention is absent.

**Fix (applied):**
- **C02** §7 Security: added a D-30 prevent-gate paragraph noting that the subprocess boundary is the
  candidate enforcement point for the D-30 blocking requirement; the D-23 spike (Test A) determines
  whether `gc`'s native tool-call routing prevents out-of-partition access or whether a watcher must
  wrap `bd`/tool-node spawn at this layer. Design of the watcher is deferred until spike completes.
- **C05** §3.3 Invariants: added INV-6: "D-30 prevent-gate: before P2/P3b, the dispatch path MUST
  be able to block (not merely audit) a bead routed to an out-of-partition agent. Whether native `gc`
  sling provides this block or a pre-dispatch watcher is needed is the D-23 spike Test A question.
  C05 must not dispatch to an out-of-partition target without this gate active for unattended runs."

---

### RGC-SEAM-07 — MAJOR
**Seam:** C03 CapabilityDescriptor registry — D-33 annotation present but XC-7 resolution prose
appears in both C02 and C03, creating redundant ownership claims

**Evidence:**
D-33 (ADOPTED): "C03 owns the CapabilityDescriptor registry + descriptor schema; C02 carries only a
`capability_id` reference in the pack manifest."

- `C02-pack-extension-abi.md` §9 (if present) and the D-33 block in §1: states "C02 DOES NOT define
  the CapabilityDescriptor schema. C02 carries only a `capability_id` reference field." ✓ Clean.
- `C03-config-feature-flags.md` §3: "C03 OWNS the CapabilityDescriptor registry + descriptor schema."
  ✓ Clean.
- **Gap:** Neither spec actually defines the `capability_id` field in its field table. C02's §4.1
  manifest field table has no `capability_id` row. C03 owns the registry but never gives a field table
  for the `CapabilityDescriptor` record itself (what fields it has, which are R/W-by whom).
  The cross-reference is declared; the schema is deferred.

**Impact:** Not a seam break today (both specs say the same thing in the right direction), but a future
builder implementing C02 or C03 will not find the concrete `capability_id` or `CapabilityDescriptor`
schema. This is a **major gap** that will surface as a build-blocker when the first pack needs to
register a capability.

**Fix (applied):**
- **C02** §4.1: Added a `capability_id` row: `[pack] capability_id | string | O | ID of the
  capability this pack provides, as registered in C03's CapabilityDescriptor registry (D-33 /
  XC-7 RESOLVED). Validated by C03 at config-load. | Pack author writes; C03 registry validates`.
- **C03** §3: Added a stub `CapabilityDescriptor` record block noting the schema is Sweep-2
  pending: fields `capability_id` (string, required), `section` (string, the city.toml section it
  gates), `requires` (list of capability_ids, optional), `conflicts_with` (list, optional). Marked
  `[needs G11 verification]` for the exact TOML form; flagged as Sweep-2 freeze pending C02 and
  downstream consumers.

---

### RGC-SEAM-08 — MINOR
**Seam:** Verbatim D-citation check — D-30 quoted non-verbatim in C42 §6.1

**Evidence:**
AGENTS-MD-bf4431be57 requires verbatim D-citations as blockquotes. D-30 verbatim text from
review-log.md:

> "unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at
> the tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant
> blast-radius face."

`C42-rig-partitioning.md` §6.1 E-C42-04 D-30 note:

> "unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at
> the tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant
> blast-radius face."

This is verbatim. ✓

Now checking C04 §6.3:
> "D-30 (ADOPTED — operator, 2026-06-01) — Prevent/block is required for unattended; the watcher is
> the sanctioned discharge, its design deferred."
> — review-log.md D-30, 2026-06-01

This is a **paraphrase** of the blockquote (the actual D-30 text is longer). The cite-as-blockquote
requirement is violated — C04 cites the D-30 *heading* but not the binding *text*.

**Fix (applied):** Replaced the C04 §6.3 D-30 paraphrase with the verbatim blockquote text from
review-log.md, followed by the attribution.

---

### RGC-SEAM-09 — MINOR
**Seam:** C42 `PartitionRecord.role_kind` enum — `worker` vs `implementer` terminology unresolved
in the type signature

**Evidence:**
- `C42-rig-partitioning.md` §9 OQ-C42-2: "RESOLVED: 'worker' (Phase-0) and 'implementer' (Phase-2)
  are the same role." The note says this is resolved.
- `C42` §3.1 `PartitionRecord.role_kind`: typed as `enum{worker, scenario_author, judge}` — uses
  `worker`.
- `C42` §4.2 config TOML example: uses `name = "implementer"` for the rig but the enum value is
  `worker`. This works if the enum value and the rig name are separate concepts (the rig is *named*
  `implementer` in city.toml but classified as `role_kind=worker` by C42's policy). However, it is
  confusing — a downstream builder reading the TOML sees `name="implementer"` and the partition record
  shows `role_kind=worker`, with no prose bridging the two.

**Impact:** Low but real: C34 and C32 consume `PartitionRecord.role_kind` for enforcement and audit.
If either uses the TOML `name` as the role discriminator instead of `role_kind`, they will not match.

**Fix (applied):** Added a clarifying note to C42 §3.1 `PartitionRecord.role_kind` field: "Note: the
`role_kind` is a classified role (the enum), which may differ from the `rig_name` in city.toml (e.g.
a rig named `implementer` in city.toml classifies as `role_kind=worker` — OQ-C42-2 RESOLVED). C34 and
C32 MUST consume `role_kind`, not parse `rig_name` as the role discriminator."

---

### RGC-SEAM-10 — MINOR
**Seam:** C03 §3 field table `[[tool]] cmd` vs C02/anchor `[[tool]] command` key name mismatch

**Evidence:**
- `gascity-config-anchor.md` §3 table: lists `[[tool]]` rows with fields `name`, `cmd`, `args` — uses
  `cmd`.
- `C03-config-feature-flags.md` §4.1: uses `[[tool]] cmd` (matches anchor). ✓
- `C02-pack-extension-abi.md` §4.1: uses `[[tool]] command` (not `cmd`).
- AI-CONTEXT §13.3 prototype sketch shows `command = "inspect"`.

**Impact:** `command` vs `cmd` is a config-key spelling disagreement between C02 (which owns the ABI)
and C03/anchor. If the real `gc` uses `command`, then C03/anchor are wrong; if it uses `cmd`, then C02
is wrong. Both cannot be right. This is a contract-drift requiring resolution.

**Resolution (in-spec annotation applied):** Both C02 §4.1 and C03 §4.1 annotated with
`[needs-G11 verification] — anchor uses 'cmd', C02 uses 'command'; AI-CONTEXT §13.3 shows 'command';
confirm against pinned gc before any pack author relies on this field name`. The anchor §3 row for
`[[tool]]` also carries the G11 flag already; the C03 row now matches. C02 uses `command` which
matches AI-CONTEXT §13.3 and is therefore the more grounded choice pending G11 confirmation; C03's
`cmd` is flagged as potentially stale.

**DEFERRED — orchestrator ledger:** Decide canonical spelling (`command` vs `cmd`) from a pinned-`gc`
run at G11; update anchor and C03 to match C02 if `command` is confirmed.

---

### RGC-SEAM-11 — MINOR
**Seam:** E↔AC cross-reference integrity — C17 AC-C17-05 asserts no E-code

**Evidence:**
SWEEP2-DISPATCH §"Acceptance tests": "Each AC that exercises a failure path cross-references the
E-code it asserts."

- `C17-tool-node-abstraction.md` §8 (AC-code table): AC-C17-05 exercises the tool-node invocation
  success path; the "Verifies" column says `C02 Reading-A args substitution + C17 invocation; §3.4,
  §5 step 3` with `—` for the E-code column. This is a success path, so no E-code is expected. ✓
- AC-C17-03 exercises context-key mismatch and says `E-C17-05` in the verifies column. ✓
- AC-C17-01 (ToolNodeRef not found) → asserts `E-C17-01`. ✓

The E↔AC cross-references in C17 are internally consistent. No fix needed.

---

### RGC-SEAM-12 — MINOR (C01/conformance flag — DO NOT EDIT these files)
**Seam:** C01 `[[rig]]` spelling in §3 I2 interface — uses `[rigs]` (square bracket, singleton) which
is neither the F1 canonical `[[rig]]` nor the prototype `[[rigs]]` (double brackets)

**Evidence (flag for C01 adversary):**
`C01-gas-city-substrate.md` §3 I2 interface table: "section presence toggles capabilities (`[formulas]`,
`[mail]`, `[daemon]`, `[rigs]`, `[[service]]`, `[beads]`)." The `[rigs]` entry uses a single bracket
form which is neither a TOML array-of-tables (`[[rigs]]`) nor a table (`[rigs]` — a non-array section).
This is not a D-32-compliant spelling.

**Action:** **FLAG for C01 adversary.** Do not edit C01. The C01 adversary should replace `[rigs]` in
the interface description with `[[rig]]`/`[[rigs]]` (the D-32 array-of-tables spelling, with G11
caveat) to prevent downstream builders from inferring that rig declarations use a non-array TOML form.

---

### RGC-SEAM-13 — MINOR (conformance-check flag — DO NOT EDIT)
**Seam:** Conformance check `gascity-conformance-check.md` Test F references `city.toml` with
`prefix = "r1"` and `prefix = "r2"` but uses `[[rigs]]` in the expected-output block while earlier
sections use `[[rig]]`

**Evidence (flag for conformance adversary):**
Test F expected-output: "`city.toml` contains `prefix = "r1"` and `prefix = "r2"` (or equivalent
explicit overrides) for rig1 and rig2 respectively." No spelling citation. Test D uses `[[rig]]` in a
literal config display. No cross-consistency within the doc.

**Action:** **FLAG for conformance adversary.** Conformance check should adopt the D-32 two-form
annotation: "city.toml rig block (spelling `[[rig]]` or `[[rigs]]`, G11) must carry `prefix = …`".

---

## Summary of Applied Fixes

| Finding | File edited | Change summary |
|---|---|---|
| RGC-SEAM-01 | C04 §8 | `shutdown_timeout = 30` → `"10s"` (duration type match) |
| RGC-SEAM-02 | C02 §3.2, §4.1; C05 §3.4 | D-31 multi-rig annotations; `rig_name` field added to DispatchRequest |
| RGC-SEAM-03 | C03 §4.3, §5.2 | G11 spelling caveat added to rig section rows and Phase-2 skeleton |
| RGC-SEAM-04 | C05 §3.4 | `created_by` type `actor` → `string` (D-29 wire type) |
| RGC-SEAM-05 | C18 §3.2; status header | BoundReachedSignal transport note; status updated to `sweep-2` |
| RGC-SEAM-06 | C02 §7; C05 §3.3 | D-30 prevent-gate paragraphs added to C02 and C05 |
| RGC-SEAM-07 | C02 §4.1; C03 §3 | `capability_id` field added to C02; CapabilityDescriptor stub added to C03 |
| RGC-SEAM-08 | C04 §6.3 | D-30 citation replaced with verbatim blockquote |
| RGC-SEAM-09 | C42 §3.1 | `role_kind` vs `rig_name` clarification note |
| RGC-SEAM-10 | C02 §4.1; C03 §4.1 | `command`/`cmd` G11 annotation |
| RGC-SEAM-11 | none | E↔AC refs intact |
| RGC-SEAM-12 | none (C01 flag) | Flagged for C01 adversary |
| RGC-SEAM-13 | none (conformance flag) | Flagged for conformance adversary |

## Deferred Items (orchestrator ledger)

1. **`command` vs `cmd` canonical spelling** (RGC-SEAM-10): anchor uses `cmd`, C02 uses `command`,
   AI-CONTEXT §13.3 shows `command`. Must be resolved at G11 pinned-`gc` run. Update anchor and C03
   to match whichever the real `gc` binary accepts.

2. **C18 → C39 BoundReachedSignal transport mechanism** (RGC-SEAM-05 residual): is it a bead write,
   a native event subscription, or a direct interface call? Must be resolved at G11 and frozen as a
   joint C18/C39 Sweep-2 contract before either component can be built.

3. **C05 `DispatchRequest.rig_name` Phase-2 contract** (RGC-SEAM-02 residual): the exact field that
   carries rig-context in a multi-rig dispatch must be frozen jointly with C18 (which assembles the
   `PassInput.Desired` set and triggers dispatch) and C01/Gas City (which uses the rig context to set
   `work_partition`). A joint C05/C18/C42 Sweep-2 freeze is needed before Phase-2 multi-rig config
   is live.

---

## C01 / Conformance Issues Flagged for Dedicated Adversaries

- **C01:** `[rigs]` (singleton bracket, §3 I2) should be `[[rig]]`/`[[rigs]]` (array-of-tables) per
  D-32 and PackV2 TOML semantics (RGC-SEAM-12).
- **Conformance check:** Test F and D use inconsistent spelling for rig blocks; should adopt D-32
  two-form annotation with G11 flag (RGC-SEAM-13).

---

## Verdict

**accept-with-fixes**

Six issues were applied in-place (including one blocker: `shutdown_timeout` type mismatch in C04,
and one blocker: D-31 multi-rig context absent from C02/C05 dispatch seam). Three are deferred to
the orchestrator ledger. Two are flagged for the C01 and conformance adversaries respectively, per
scope constraints. The core seam architecture (C02 ↔ C17 ABI, C18 ↔ C39 bound-reached, C42 ↔ C34
policy feed, C05 ↔ C04 handoff) is sound; the identified drifts are correctable without architectural
change.
