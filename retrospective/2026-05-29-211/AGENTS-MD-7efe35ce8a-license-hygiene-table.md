# agent instruction

**License hygiene table for multi-OSS plans.** "Any architectural plan involving multiple OSS components must include a license hygiene table that lists every project, its license, and specific cautions for restrictive or unusual licenses. Especially flag the Elastic License (restrictive on hosted services), source-available licenses, and Go projects with internal/ paths that block module import."

*Grounded in: v4 README license hygiene table (PR #209) caught Phoenix's Elastic License as restrictive on hosted services, redirecting to LangFuse as the cleaner alternative.*

# justification

License surprises after committing to an OSS dependency are expensive. The v4 license hygiene table caught Phoenix's Elastic License before adopting it — Elastic License restricts hosted-service operation, which would have prevented operating the v4 factory as a service downstream. Pivoted to LangFuse (Apache 2.0). The marginal cost of building the table is one row per dependency (a few minutes of license checking); the cost of license surprise downstream is migrations, re-architecture, and potential commercial deadlock. The asymmetry favors the table overwhelmingly. The table also serves as ongoing documentation — future contributors can see at a glance whether a new dependency is license-clean.
