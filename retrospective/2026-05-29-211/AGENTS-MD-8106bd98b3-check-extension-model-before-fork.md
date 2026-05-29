# agent instruction

**Check the project's documented extension model before recommending fork.** "Before recommending forking or vendoring an OSS dependency, identify the project's documented extension model (packs, plugins, config, etc.) and verify whether the proposed extension can be achieved within that model. Reach for fork only when source-level modification is genuinely required (new core interface, modified internal behavior, urgent bug fix not yet upstream)."

*Grounded in: incorrectly recommending Gas City fork+vendor when the pack model handles all v4 extension needs.*

# justification

I recommended forking Gas City + vendoring its `internal/` paths into the v4 docs. The recommendation was wrong because Gas City's whole extension model is packs, which don't require Go library imports. The user caught it explicitly: "I thought its whole thing was you could extend with packs." Forking commits the team to maintaining a fork forever; pack-based extension just means writing TOML and tool-node binaries. The cost of forking when not needed is heavy and ongoing (rebase pain, migration tail, divergence risk); the marginal cost of checking the extension model is one repo README pass. The asymmetry is dramatic — recommend fork without checking and you bake in months of unnecessary fork-maintenance overhead.
