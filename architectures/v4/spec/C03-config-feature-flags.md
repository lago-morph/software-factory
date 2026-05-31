# C03 — Layered config / feature-flag model  (Spec, canonical track)

> Source: AI-CONTEXT §3.2 ("nine concepts" #4 — "Config: Layered TOML; section presence = feature flag"); AI-CONTEXT §3.4 (smallest viable install / "Explicitly off" list); AI-CONTEXT §3.1 (coverage map — "Strong when `[formulas]` enabled"); AI-CONTEXT §13.1/§13.2/§13.3 (concrete `pack.toml`/`city.toml` skeletons per phase); AI-CONTEXT §11.1 ("6 of 12 principles natively"); README Part 6 Phase 0/Phase 1 ("Turn on `[formulas]`", "What you do NOT install"); component-inventory C03 row (`A26`, `B70`; depends on C01; gaps G03, G37).
> Inventory ID: C03   Kind: data-store   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C03 is the **layered TOML configuration model** in which **the presence of a section enables a
capability** and its absence leaves the capability off. It is the single mechanism through which every
other component is feature-gated: `[formulas]` present ⇒ formula DAG composition on; `[mail]` present ⇒
messaging on; `[[rig]]` blocks present ⇒ rig partitioning on; and so on. The config files (`pack.toml`,
`city.toml`, and per-agent template references) are the version-controlled source of truth for *which
parts of the substrate are live in a given install* and for *the parameters those parts run with*.

**Responsibilities**
- Define the **layered config files** v4 uses — `pack.toml` (imports) and `city.toml` (workspace, agents,
  beads, services, rigs, tools, formulas, mail, daemon …) — and the rule that **section presence = the
  feature flag** (AI-CONTEXT §3.2 #4).
- Own the **enablement semantics**: a capability is *off* unless its section is present; turning a
  capability on is "add the section" (README Phase 1: "Turn on `[formulas]`").
- Own the **layering/merge order** by which `pack.toml` imports compose with the local `city.toml`
  (the "layered" in "layered TOML") and per-agent `env = { … }` overrides apply.
- Be the gate that drives the **per-phase install surface**: Phase 0 minimum (the "Explicitly off" set),
  Phase 1 additions, Phase 2 additions (AI-CONTEXT §13.1–§13.3).

**Explicitly NOT**
- NOT the substrate runtime itself (C01) — C03 is the *config data model* C01 reads; C01 is what acts on it.
- NOT the formula/pipeline-file format (C12). `[formulas]` *presence* is C03's flag; the *content* of a
  formula DAG is C12. C03 owns the on/off switch, not the workflow grammar.
- NOT the pack ABI / tool-node protocol (C02). C03 describes `[imports.*]` and `[[tool]]` *declarations*;
  the subprocess tool-node wire protocol is C02.
- NOT a secrets manager. C03 records that credentials appear in `env = { … }` / `[[service]]` blocks
  (AI-CONTEXT §13.2) but defines no secret storage, rotation, or encryption (see G37, §6/§9).
- NOT the phase-delivery plan (C54). C03 supplies the flags each phase toggles; C54 owns the phase ordering.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | C03 is Gas City concept #4 ("Config"); the substrate parses and acts on these TOML files. C03 has no meaning without C01. |
| Downstream (gated by) | **C12** Formula format | `[formulas]` section presence enables C12 (AI-CONTEXT §3.1, README Phase 1). |
| Downstream (gated by) | **C08** Spec artifact | inventory: C08 `depends on C03`; spec/template wiring is config-declared (`agents/<name>/prompt.template.md`). |
| Downstream (gated by) | **C06** Messaging, **C42** Rig partitioning, **C04** Session/provider, **C40** Orders, **C44**/services | `[mail]`, `[[rig]]`, `[[agent]] provider`, `[daemon]`/orders, `[[service]]` sections each gate their component. |
| Downstream (consumes) | **C02** Pack ABI | `[imports.core]` / pack imports are the layering inputs C03 composes. |

C03 is **foundational** (inventory: yes), in **Batch 1**, authored in parallel with C01/C02/C07 — it is a
load-bearing schema everything references for "is feature X on, and with what parameters."

## 3. Interfaces / contracts

Sweep 1 — interfaces named and described (signatures/schemas deferred to sweep 2).

1. **Config-file set** — the ordered layers C03 defines:
   - `pack.toml` — declares imports (`[imports.core]`, future `[imports.<name>]`); the *outer* layer.
   - `city.toml` — the workspace install: `[workspace]`, `[[agent]]`, `[beads]`, and the optional
     capability sections (`[formulas]`, `[mail]`, `[daemon]`, `[[rig]]`, `[[service]]`, `[[tool]]`).
   - per-agent `env = { … }` inline tables — the *innermost* override layer (e.g. Claude Code OTEL vars,
     AI-CONTEXT §13.2).
2. **Feature-flag predicate** — "is capability C enabled?" answered by **section presence**: `present ⇒ on`,
   `absent ⇒ off`. This is the contract every gated component queries (directly or via C01).
3. **Layer-merge interface** — "compose imported pack config + local `city.toml` + per-agent env into one
   effective config." Defines precedence (described in §4; concrete merge algebra deferred to sweep 2).
4. **Capability-parameter accessor** — for an enabled section, read its keys (e.g. `[[service]]
   endpoint = …`, `[beads] provider = "file"`). Presence enables; keys parameterize.

**Invariants**
- **Presence-is-the-flag**: no separate `enabled = true` boolean exists for the substrate-native
  capabilities; the *only* on/off signal is whether the section is written. (Faithful to AI-CONTEXT §3.2
  #4 and README "Turn on `[formulas]`" / "Explicitly off".)
- **Absent ⇒ inert**: a capability whose section is absent contributes nothing at runtime (Phase 0's
  "What you do NOT install" is achieved purely by *omitting* sections, not by disabling them).
- **Version-controlled**: config files live in git alongside packs (README:107 "packs are git-versioned");
  the effective feature set of an install is fully reconstructable from committed TOML.

## 4. Data model / state

C03 owns the **config files as a layered, version-controlled artifact**. No mutable runtime state of its
own; the substrate (C01) is what loads it each run.

**Layering (outer → inner; inner overrides outer):**

1. `pack.toml` imports (`[imports.core]`, …) — bring in pack-provided defaults/sections.
2. local `city.toml` — the install's own sections; this is where most capability flags are written.
3. per-`[[agent]]` `env = { … }` — innermost per-agent parameter overrides.

> [FAITHFUL-FILL] v4 says the config is "**layered** TOML" (AI-CONTEXT §3.2 #4) and shows imports
> (`pack.toml [imports.core]`) plus a local `city.toml` plus per-agent `env`, but never states the
> precedence rule explicitly. The minimal consistent choice is the conventional outer-to-inner override
> (imports = defaults, local `city.toml` overrides, per-agent `env` most specific) — it is the only
> ordering under which the §13.1–§13.3 skeletons compose without contradiction. Concrete merge algebra
> (deep-merge vs replace per key/array) is deferred to sweep 2.

**Capability sections (faithful enumeration from v4):**

| Section | Capability gated | On at phase | Source |
|---|---|---|---|
| `[workspace]` | the install/workspace identity | Phase 0 (always) | AI-CONTEXT §13.1 |
| `[[agent]] provider = "claude"` | an agent worker backed by a provider | Phase 0 (always) | AI-CONTEXT §13.1 |
| `[beads] provider = "file"` | bead store (file backend) | Phase 0 (always) | AI-CONTEXT §13.1 |
| `[imports.core]` (`pack.toml`) | core pack import layer | Phase 0 (always) | AI-CONTEXT §13.1 |
| `[formulas]` | formula DAG composition (C12) | Phase 1 (on) | AI-CONTEXT §3.1/§13.2; README Phase 1 |
| `[[service]]` (langfuse/cxdb/otel) | external service wiring | Phase 1 | AI-CONTEXT §13.2 |
| `[[agent]] env = { … }` | Claude Code OTEL/telemetry params | Phase 1 | AI-CONTEXT §13.2 |
| `[[rig]] read_partition/write_partition` | rig/agent-role partitioning (C42) | Phase 2 | AI-CONTEXT §13.3 |
| `[[tool]] type = "subprocess"` | tool-node declaration (e.g. `inspect_eval`) | Phase 2 | AI-CONTEXT §13.3 |
| `[mail]`, `[daemon]`, Dolt server, orders | messaging / daemon / Dolt / Orders | **off** at Phase 0 | AI-CONTEXT §3.4 ("Explicitly off") |

**Phase-0 "off-by-omission" set** (the explicit faithful list): `[daemon]`, `[mail]`, `[formulas]`,
`[rigs]`†, Dolt server, `[[service]]` blocks, orders (AI-CONTEXT §3.4). All off purely because their
sections are absent.

> † **Spelling note.** AI-CONTEXT §3.4 writes the prose form "rigs"; the canonical *section* form is the
> array-of-tables `[[rig]]` (AI-CONTEXT §13.3 / C42). One spelling (`[[rig]]`) should be adopted in the
> sweep-2 schema so the C10/C15 vocabulary linters key off a single section name. Mirror of C01 RC01-03;
> reconcile across C01/C03/C42.

## 5. Behavior

C03 has no control loop; its behavior is **load-time** and **authoring-time**:

- **Authoring**: enabling a capability = adding its section (and its parameter keys) to `city.toml`
  (or importing a pack that provides it). Disabling = removing the section.
- **Load-time composition**: at substrate startup, C01 reads `pack.toml` imports, merges them under the
  local `city.toml`, applies per-agent `env`, and yields the **effective config**; section presence in the
  effective config is the enablement signal each component checks.
- **Phase progression**: moving Phase 0 → 1 → 2 is, at the config layer, exactly the act of adding the
  Phase-1 and Phase-2 sections from §13.2/§13.3 to the Phase-0 skeleton.

(Sequence/state diagrams for the load/merge flow deferred to sweep 2 per BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C03 (faithful) |
|---|---|---|
| **G03** — "6 of 12 native" is unsupported because P3 is "Strong **when `[formulas]` enabled**" but Phase 0 turns `[formulas]` **off** | C03 *owns the very flag* (`[formulas]`) the miscount turns on. | See AMBIGUITY block below. Faithful resolution: the native count is **phase-relative** — 5 at Phase 0 (formulas off), 6 once `[formulas]` is added in Phase 1. C03's job is to make that gating explicit so the count is unambiguous per phase. **Ownership split (consistent with C01-A §6):** C03 *derives* the count from which sections are present; C01 *verifies* each native capability against the pinned `gc` (conformance manifest); C57 *reconciles* the corpus-wide headline. The three are complementary, not three independent fixes of the same number. |
| **G37** — secrets/credentials appear in `city.toml`/`env` as plaintext with no secrets story | OAuth/CXDB/LangFuse/OTel mTLS creds live in `[[service]]` endpoints and `env = { … }` (AI-CONTEXT §13.2), i.e. *inside C03's files*. | Noted + deferred (faithful): v4 specifies no secrets manager, so C03 faithfully records that secrets ride in version-controlled TOML/env and flags it as residual risk (§9). Inventing encryption/rotation would exceed v4. |
| Misconfiguration (typo'd / missing section) | A capability silently stays off if its section is absent or misnamed. | Faithful posture: absence is *intentional* off (Phase 0 relies on it), so "missing section" is indistinguishable from "deliberately off." Detection of *unintended* omission is not specified by v4; flagged as open question (§9). |
| Layer-merge ambiguity | Imported pack and local `city.toml` could set the same key. | Handled by the precedence FAITHFUL-FILL in §4 (inner overrides outer); concrete conflict rules → sweep 2. |

> [AMBIGUITY: G03] **What is the native principle count at the smallest install — 5 or 6?**
> Reading A (literal headline): AI-CONTEXT §11.1/§3.6 assert "6 of 12 native" and count P1,P2,P3,P4,P9,P10.
> Reading B (gated): §3.1 rates P3 "Strong **when `[formulas]` enabled**" and §3.4 + README Phase 0 turn
> `[formulas]` **off** at the smallest install, and README Phase 0 itself says P3 is "full when formulas
> turn on in Phase 1." Under Reading B the smallest install delivers **5** (P3 not yet on).
> **Pick: Reading B**, as most consistent with the rest of v4 — the §3.1 coverage map, the §3.4 explicit-off
> list, and the README Phase-0 "full when formulas turn on" note all agree P3 is `[formulas]`-gated, and
> C03's whole premise (section presence = capability) makes the count *necessarily phase-relative*. The
> "6 of 12" headline is faithful only as a Phase-1 (formulas-on) statement; at Phase 0 it is 5. C03
> records the count as a function of which sections are present, not a fixed scalar.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security**: C03 is the locus of G37 — `[[service]]` endpoints and per-agent `env = { … }` carry
  endpoints and (implicitly) credentials in plaintext version-controlled TOML. v4 gives no secrets story;
  C03 surfaces this as residual risk (§9) rather than resolving it (Canonical-track faithfulness).
- **Cost**: negligible direct cost; config is small (~30 lines at Phase 0, AI-CONTEXT §13.1). Its cost
  leverage is indirect — it gates which (costly) services are wired in.
- **Scale**: config is human-authored and small; no scale concern of its own. It bounds runtime scale by
  which sections (services, rigs, tools) are present.
- **Observability**: the effective config *is* the observability surface for "what is on in this install";
  it is fully reconstructable from committed files.
- **Ops**: changes flow through normal git review (README:107). AI-CONTEXT §3.5 warns of 1–2 breaking
  pack-schema / formula-format changes per quarter — schema-version drift is an ops concern C03 must track
  (sweep 2: a config schema version pin).

## 8. Acceptance criteria & test strategy

1. **Presence-is-flag**: enabling a capability requires *only* adding its section; with the section absent,
   the capability is provably inert (Phase-0 "Explicitly off" set verified to contribute nothing).
2. **Phase skeletons compose**: the §13.1 Phase-0 skeleton + §13.2 Phase-1 additions + §13.3 Phase-2
   additions merge into a valid effective config with deterministic precedence (no key collisions
   silently dropped).
3. **Phase-relative native count**: a check derives the native-principle count from present sections and
   yields 5 at the Phase-0 skeleton (formulas off) and 6 once `[formulas]` is added — making G03 explicit
   rather than a fixed headline.
4. **Round-trip**: the effective feature set of an install is reconstructable from committed `pack.toml` +
   `city.toml` alone (version-control invariant).
5. **Secrets surfaced**: a lint/audit flags any credential-bearing key in `env`/`[[service]]` as a G37
   residual-risk item (detection only; v4 prescribes no mitigation).
(Concrete TOML schema, merge-precedence test vectors, and a config validator are sweep-2 deliverables.)

## 9. Open questions

- **OQ-C03-1** (→ review-log): **G37 secrets.** v4 puts OAuth/CXDB/LangFuse/OTel-mTLS credentials in
  version-controlled `city.toml`/`env` with no secrets manager. Faithful spec records the risk and defers;
  is even a minimal faithful elaboration (e.g. `env` values referencing an external secret source) in
  scope, or is that an architectural change deferred as a future enhancement? Flagged, not silently resolved.
  **Wrap-up decision (D-25, ADOPTED 2026-05-31):** posture is settled — **keep config/env now**, and adopt a **minimal off-the-shelf secrets approach (env-injection or SOPS-encrypted files) at the first real credential**; no premature secrets build. This is the **G37** posture (G37 ≠ FE-3 signing, per D-14). See [the decision ledger](../_meta/review-log.md#wrap-up-operator-decisions-2026-05-31--d-20d-25).
- **OQ-C03-2** (→ review-log): **Layer-merge precedence is inferred** (§4 FAITHFUL-FILL). v4 never states
  whether imported-pack config deep-merges or is replaced by local `city.toml`, nor array-section
  (`[[service]]`, `[[rig]]`) merge semantics. Needs the actual Gas City precedence rule (G11 — Gas City
  behavior is unverified) before sweep-2 schema can be authoritative.
- **OQ-C03-3** (→ review-log): **Off-by-omission vs unintended-omission.** Because absence *is* the off
  signal, a misnamed/forgotten section is indistinguishable from a deliberate disable. v4 specifies no
  guard; is a faithful "expected-sections manifest" warranted, or does that contradict the
  presence-is-the-only-signal invariant?
