# Anthropic Agent Skills — Primary Source Material

Anthropic's official Agent Skills documentation + cookbook notebooks. These are the canonical implementation references and security guidance. Kept on disk for re-quoting (the platform.claude.com docs page is a JS-rendered SPA that the action-fetch route cannot retrieve; this Path B export is the only practical primary source).

## Files

- **`platform-claude-com-agent-skills-overview.txt`** — Anthropic developer overview of Agent Skills (`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`). The Path B export of the JS-rendered SPA page that round-7 issue #36 couldn't fetch via the action.
- **`support-claude-com-what-are-skills.txt`** — Anthropic user-facing explainer of Skills (`support.claude.com`). Cross-product availability + open-standard claim (`agentskills.io`).
- **`01_skills_introduction.ipynb`** — Anthropic cookbook: introduction to Skills. Schema constraints, three-tier disclosure, multi-skill composition.
- **`02_skills_financial_applications.ipynb`** — Anthropic cookbook: financial domain skills example. Real worked example.
- **`03_skills_custom_development.ipynb`** — Anthropic cookbook: custom skill development. Authoring discipline, testing, versioning.

All five drained 2026-05-13 into `research/23-anthropic-engineering-trilogy.md` (the §3 attribution-gap close from round 6 + cookbook findings + concrete schema constraints + cross-references flagged for `research/04-every-skill-libraries.md`).
