# agent instruction

**`[defaults.rig.imports]` is a `gc rig add` template, not an apply-to-all.** In Gas City, `[defaults.rig.imports]` is only copied into a rig by `gc rig add` at registration time; for rigs declared statically (in `city.toml`/`site.toml` without running `gc rig add`), give each `[[rigs]]` its own `[rigs.imports.<pack>]` or its rig-scoped agents will never expand.

*Grounded in: gastown witness/refinery/polecat roles never appeared until per-rig imports were added.*

# justification

Native dispatch silently did nothing because the gastown rig roles (witness/refinery/polecat) never expanded. The config declared `[defaults.rig.imports.gastown]` and assumed it applied to every rig — but in Gas City that block is a template that `gc rig add` consumes at registration, and the prototype declares its rigs statically and never runs `gc rig add`, so no rig ever imported the pack. The fix was to give each `[[rigs]]` its own `[rigs.imports.gastown]`. The cost of not knowing this is a system that boots cleanly, reports no error, and simply never routes work — the most expensive kind of failure to diagnose, because nothing is broken, the pipeline just isn't there. The marginal cost of the rule is one import block per statically-declared rig. Encoding this gc-specific semantic (defaults are a `rig add` template, not a global default) saves the next agent from re-deriving it by live-booting and inspecting `gc agent list`.
