# C03 — Layered config / feature-flag model  (Spec, Track B)

> Source: AI-CONTEXT §3.2 (concept 4 "Config: Layered TOML; section presence = feature flag"), §3.4 (smallest viable install / explicitly-off list), §13.1–13.3 (`pack.toml`/`city.toml` examples), §3.1 (coverage map), §11.1 (decisions); README Part 6 Phase 0/Phase 1 (`[formulas]` on/off, env block), §3.1 coverage; _meta gaps G03, G37; F-MODE-COVERAGE F13.
> Inventory ID: C03   Kind: data-store   Status: sweep-1
> Deltas: DELTA-01 (resolution layering + explicit precedence), DELTA-02 (capability descriptor registry replaces implicit section-presence), DELTA-03 (secret-reference indirection — no plaintext secrets in TOML), DELTA-04 (config validation/lint gate at load), DELTA-05 (Phase-0 native-count corrected to 5; `[formulas]`-gated P3 made explicit), DELTA-06 (config provenance + change attribution into C23/C41).

## 1. Purpose & responsibility

C03 is the **config substrate**: the layered TOML that the Gas City runtime (C01) loads at startup and on reload, in which **the presence of a section enables a capability**. It is the single mechanism by which every other component is feature-gated — turning `[formulas]` on activates the workflow engine (C12), adding `[[rig]]` blocks activates partitioning (C42), adding `[[service]]` blocks wires CXDB/LangFuse/OTel (C21/C27/C26), etc. C03 owns: the **layer stack** (defaults → pack → city → agent-env → runtime override), the **resolution/precedence rules** that flatten that stack into one effective config, the **capability descriptor registry** that maps a section to the capability it gates and that capability's dependencies, the **load-time validation gate**, and the **secret-reference indirection** that keeps credentials out of version-controlled TOML.

What it is **NOT**:
- Not the workflow/DAG format — that is C12 (`[formulas]` *turns C12 on*; the formula files themselves are C12's artifact).
- Not the pack ABI — packs (C02) *contribute a config layer* and declare capability descriptors, but C03 defines the merge/precedence semantics, not the bundle format.
- Not a runtime feature-flag service with live per-request flips (no Unleash/LaunchDarkly). Flags are **install/phase-scoped**, resolved at load and on explicit reload, not per-trajectory.
- Not the secrets store — C03 defines the *reference* syntax and resolution seam; the actual secret material lives in an external provider (env/file/Vault-shaped), out of scope for the value but in scope for the seam (DELTA-03).
- Not identity/attribution (C41) — but every effective-config change emits a provenance record *to* C23/C41 (DELTA-06).

## 2. Context & dependencies

- **Depends on:** C01 (Gas City loads and owns the TOML reader; C03 specifies the layering/validation contract Gas City's loader must honor).
- **Consumed by (foundational fan-out):** essentially everything. Direct gating relationships: C12 (`[formulas]`), C04 (`[[agent]]`/session env), C42 (`[[rig]]`), C06 (`[mail]`), C40 (`[daemon]`/orders), C17/C44 (`[[service]]`, `[[tool]]`), C19 (`[beads] provider`), C28/C25 (agent `env` OTLP block), C29 (model-stylesheet routing config). C08 (spec artifact) lists C03 as a dependency for format/version config.
- **Sits at:** the bottom of the Runtime Substrate, immediately above C01. It is read before any capability initializes; its correctness is a precondition for every other component's activation.

## 3. Interfaces / contracts

Named-and-described (sweep 1; signatures in sweep 2).

**Inbound**
- `LayerSource` — a contributor of a config layer (defaults baked into Gas City; a pack's `pack.toml`+packaged TOML; the project `city.toml`; per-agent `env`; an ephemeral runtime override). Each declares its precedence rank.
- `CapabilityDescriptor` (DELTA-02) — registered by core + each pack: `{ capability_id, gating_section (e.g. "[formulas]"), requires (capability_ids), conflicts_with, schema_ref, default_state }`. Makes "section X enables capability Y, which needs Y'" explicit and machine-checkable instead of folklore.
- `SecretRef` (DELTA-03) — a value of form `secret://<provider>/<key>` (or `${ENV:NAME}` / `file://`) that C03 resolves through a `SecretResolver` seam at load; the literal secret never appears in the TOML layer.

**Outbound**
- `EffectiveConfig` — the flattened, validated, secret-resolved view: the set of enabled capabilities + their resolved parameters. Queryable by capability_id and by section path. This is the *only* config surface other components read; nobody re-parses raw TOML.
- `ConfigValidationReport` — result of the load-time gate (DELTA-04): unknown sections, unsatisfied `requires`, conflicts, schema violations, dangling `SecretRef`s, deprecated keys. Fail-closed for `requires`/conflict/schema errors; warn for deprecations.
- `ConfigProvenance` event (DELTA-06) — on each (re)load: which layers contributed, effective hash, who/what triggered the change → emitted to C23 (event bus) with C41 attribution.

**Invariants**
- Determinism: same ordered layer set + same secret-resolver state ⇒ identical `EffectiveConfig` (and identical effective hash).
- A capability is enabled **iff** its gating section is present in the flattened config **and** validation passed; partial/invalid enablement is impossible (fail-closed).
- `requires` is transitively satisfied or load fails — you cannot enable C42 rigs without the substrate they assume. The `requires`/`conflicts_with` relation MUST form a **DAG**; a dependency cycle is a load-time error with a typed `DescriptorCycle` diagnostic, never a hang or opaque failure. (`conflicts_with` is mutual and non-transitive.)
- No secret literal is ever present in a version-controlled `LayerSource` payload (lint-enforced, DELTA-03). Note this is *detection of secret-shaped literals*, not a storage guarantee — the actual protection depends on the resolver provider (OQ1).

## 4. Data model / state

- **Layer stack (ordered, low→high precedence):** `core-defaults` → `pack` (in pack-import order) → `city.toml` → `agent.env` → `runtime-override`. (DELTA-01 makes this order explicit; v4 only ever shows examples, never states precedence.)
- **Merge semantics:** tables deep-merge by key; arrays-of-tables (`[[agent]]`, `[[rig]]`, `[[service]]`) merge by a declared identity key (`name`) — same-name entries override, new names append. Scalars: higher layer wins.
- **Capability registry:** the set of `CapabilityDescriptor`s, keyed by `capability_id`. Lives in core + packs; assembled at load.
- **Effective config:** in-memory, immutable per generation; carries a content hash (effective-config hash) for provenance and for C46 meta-metrics keying ("which config produced this satisfaction number").
- **Phase profiles** (DELTA-05 framing): Phase 0 / Phase 1 / Phase 2 are *named layer presets* (which sections are present). They are documentation + optional named overlays, not new mechanism. Selecting a profile is a **load/reload generation switch** (immutable generation), never a live per-request flip — preserving the §1 non-goal ("not a runtime feature-flag service").
- Persistence: the source layers are version-controlled files (Gas City owns them); the effective config + provenance are derived, logged to C23, not separately persisted.

## 5. Behavior

Load/reload flow (sweep-2 will add a Mermaid sequence diagram):

1. Gas City discovers layer sources (core defaults, imported packs, `city.toml`, agent env, any runtime override).
2. C03 collects `CapabilityDescriptor`s from core + packs.
3. Flatten layers by precedence (DELTA-01) → raw effective TOML.
4. Determine enabled set = sections present whose descriptor exists.
5. Validate (DELTA-04): schema per section, `requires`/`conflicts_with` over the enabled set, unknown-section detection, deprecation scan.
6. Resolve `SecretRef`s through the resolver seam (DELTA-03); dangling refs = validation error.
7. On success: publish immutable `EffectiveConfig` + emit `ConfigProvenance` to C23/C41 (DELTA-06). On failure: fail-closed, refuse to start (or refuse the reload, keeping the prior generation live).

Reload is the same flow producing a new generation; capabilities observe a generation switch rather than mutating in place.

## 6. Failure modes & handling

- **F13 (Missing-config blindspot)** — *primary.* Implicit section-presence means a forgotten section silently disables a capability with no signal. Mitigation (DELTA-02/04): capability descriptors make the *intended* set declarable, and the validation gate reports enabled-vs-expected and unsatisfied `requires`, converting silent absence into a load-time report. Residual: the universe of unspecified environment beyond declared descriptors (acknowledged in F-MODE-COVERAGE F13 as a residual gap).
- **G37 / secret leakage** — plaintext OAuth/CXDB/LangFuse/mTLS creds in version-controlled TOML. Mitigation: `SecretRef` indirection + lint that rejects secret-shaped literals in versioned layers (DELTA-03). See Open Questions for resolver-provider choice.
- **Misconfiguration / phantom-enable** — a typo'd section name silently does nothing. Mitigation: unknown-section detection is an error, not ignored (DELTA-04).
- **Config drift across layers (F34/F7 flavor)** — pack layer and city layer disagree. Mitigation: deterministic precedence (DELTA-01) + provenance hash so drift is observable and attributable (DELTA-06).
- **Descriptor-graph cycle / dual source of truth (DELTA-02)** — `requires`/`conflicts_with` must be a DAG; a cycle fails load with `DescriptorCycle` rather than looping. Open architectural question (DEFERRED): the descriptor dependency edges duplicate the inventory's `Depends on` edges — whether descriptors are *authored* or *generated from / checked against* the inventory is a single-source-of-truth call for the integrator (see OQ3, and C02 OQ3 for the C02↔C03 ownership straddle).
- **Reload corruption** — bad reload must not take down a running factory. Mitigation: immutable generations; failed validation keeps the prior generation live (fail-closed-to-last-good).

## 7. Cross-cutting

- **Security:** DELTA-03 is the core security improvement — secrets out of *version-controlled TOML* (the G37 surface). The achievable guarantee is "no secret literal in a versioned layer"; whether the secret *material* is actually protected vs merely relocated to an unspecified `env`/`${ENV:NAME}` source depends on the resolver-provider choice (OQ1) — env-injection still places the secret in the process environment from *somewhere*. Validation fail-closed prevents half-enabled capabilities crossing trust boundaries (relevant to C43 isolation).
- **Cost/scale:** flags are install-scoped; resolution is O(layers); no per-request cost. Effective-config hash lets C46 attribute cost/satisfaction to a config generation.
- **Observability:** every (re)load is an attributed event (DELTA-06); the effective config + its hash are introspectable, satisfying "what is actually turned on right now?".
- **Ops:** phase profiles (DELTA-05) give operators a named, validated path Phase 0→1→2 instead of hand-editing and hoping.

## 8. Acceptance criteria & test strategy

1. **Determinism:** identical ordered layers ⇒ byte-identical effective hash (golden test).
2. **Gating:** removing `[formulas]` disables C12 and *reports* it via the expected-set check; adding it (with `requires` met) enables it. Same for `[[rig]]`→C42, `[[service]]`→C21/C26/C27.
3. **Precedence:** agent-env overriding a city scalar resolves to the agent value; arrays-of-tables merge by `name` (override vs append) per DELTA-01.
4. **Fail-closed:** unsatisfied `requires`, unknown section, schema violation, or dangling `SecretRef` each refuse load; a bad *reload* leaves the prior generation serving.
5. **No-plaintext-secret lint:** a secret-shaped literal in a versioned layer fails the lint (DELTA-03).
6. **Provenance:** each load emits exactly one attributed `ConfigProvenance` to C23 with the effective hash (DELTA-06).
7. **Phase-0 honesty (G03/DELTA-05):** a Phase-0 profile reports P3 as *gated-off* (native count 5), and turning `[formulas]` on flips P3 to delivered.

## 9. Open questions

- **OQ1 (→ review-log):** Which `SecretResolver` provider is the v4 baseline under Max — env-injection only, or a Vault/SOPS-shaped backend? G37 names the problem but the corpus offers no secrets story; the choice affects C28 OAuth handling and C25 mTLS certs. *Top open question.*
- **OQ2:** Does Gas City's existing TOML loader already define a precedence order C03 must match (DELTA-01 may be describing, not changing, behavior)? Needs upstream confirmation; if it conflicts, DELTA-01 becomes a fork-or-conform decision touching C01.
- **OQ3:** Are capability descriptors authored centrally (core registry) or self-declared per pack (C02 ABI extension)? Affects the C02↔C03 seam.
