# Source catalog — browse view

Auto-generated from `reference-only/sources.json` by `scripts/render-sources-md.py`.
Do not edit by hand — your changes will be overwritten on next push to `main`.

**Records:** 209 · **Generated:** 2026-05-17 22:02 UTC

## 🔴 Manual fetch needed

**14 record(s)** have `ingestion_status=want` file entries — the fetch action couldn't get them automatically (Cloudflare challenge, JS-rendered SPA, paywall, or 404 with no successor).

### How to fetch manually

1. Open the URL in your browser (signed in if needed for paywalled content).
2. **File → Save Page As → Webpage, Complete** (saves as MHTML — preserves embedded images + CSS). Chrome/Edge call this *"Save as MHTML"*; Firefox calls it *"Webpage, single file"* via an extension.
3. Save the file with the suggested name from the **Drop as** column below into `research/manual/`.
4. After all manual fetches are dropped, run:
   ```bash
   python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py --all
   ```
   This will register each file into its catalog record (matching by sha256 + filename) and flip the status to `have`.

### Records to fetch

| Record | Title | URL | Reason want | Drop as |
|---|---|---|---|---|
| `175cba9347` | =?utf-8?Q?Custom=20instructions=20with=20AGENTS.md=20=E2=80= | [https://developers.openai.com/codex/guides/agents-md](https://developers.openai.com/codex/guides/agents-md) | Not yet fetched | `research/manual/175cba9347.mhtml` |
| `18856eb4cf` | FAQs About AI Evals | [https://hamel.dev/blog/posts/evals-faq](https://hamel.dev/blog/posts/evals-faq) | Not yet fetched | `research/manual/18856eb4cf.mhtml` |
| `24ca29ee98` | (unknown) | [https://arxiv.org/abs/2503.18813](https://arxiv.org/abs/2503.18813) | Not yet fetched | `research/manual/24ca29ee98.mhtml` |
| `3703e782c0` | =?utf-8?Q?You=20Don=E2=80=99t=20Write=20the=20Code.=20You=20 | [https://www.danshapiro.com/blog/2026/02/you-dont-write-the-c](https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code) | Not yet fetched | `research/manual/3703e782c0.mhtml` |
| `53ed6e363d` | Simon Willison — CaMeL paper writeup | [https://simonwillison.net/2025/Apr/11/camel](https://simonwillison.net/2025/Apr/11/camel) | Not yet fetched | `research/manual/53ed6e363d.mhtml` |
| `5a9f63821f` | Agent Skills: Security | [https://platform.claude.com/docs/en/agent-skills/security](https://platform.claude.com/docs/en/agent-skills/security) | Refetch — current capture is a JS-rendered shell | `research/manual/5a9f63821f.mhtml` |
| `5cc5a296b6` | =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Agent=203:=20Ou | [https://blog.replit.com/introducing-agent-3-our-most-autonom](https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet) | Not yet fetched | `research/manual/5cc5a296b6.mhtml` |
| `71d2de09c6` | A Field Guide to Rapidly Improving AI Products | [https://hamel.dev/blog/posts/field-guide](https://hamel.dev/blog/posts/field-guide) | Not yet fetched | `research/manual/71d2de09c6.mhtml` |
| `73dc7199ce` | =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Replit=20Agent= | [https://blog.replit.com/introducing-agent-4-built-for-creati](https://blog.replit.com/introducing-agent-4-built-for-creativity) | Not yet fetched | `research/manual/73dc7199ce.mhtml` |
| `8334be0240` | =?utf-8?Q?Subagents=20=E2=80=93=20Codex=20\|=20OpenAI=20Deve | [https://developers.openai.com/codex/subagents](https://developers.openai.com/codex/subagents) | Not yet fetched | `research/manual/8334be0240.mhtml` |
| `9c9554d27e` | The lethal trifecta for AI agents: private data, untrusted c | [https://simonwillison.net/2025/Jun/16/the-lethal-trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta) | Not yet fetched | `research/manual/9c9554d27e.mhtml` |
| `ade5ef8d76` | Eugene Yan — LLM Evaluators | [https://eugeneyan.com/writing/llm-evaluators](https://eugeneyan.com/writing/llm-evaluators) | Correct URL is plural 'evaluators'; original record had singular which 404'd | `research/manual/ade5ef8d76.mhtml` |
| `dccefbfc62` | =?utf-8?Q?Agent=20approvals=20&=20security=20=E2=80=93=20Cod | [https://developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security) | Not yet fetched | `research/manual/dccefbfc62.mhtml` |
| `f8007cc630` | An AI State of the Union \| Simon Willison (Lenny's Newslett | [https://www.lennysnewsletter.com/p/an-ai-state-of-the-union](https://www.lennysnewsletter.com/p/an-ai-state-of-the-union) | Refetch — only partial transcript currently | `research/manual/f8007cc630.mhtml` |


## By category

### dark-factory *(38 records)*

*Dark-Factory canon — Shapiro / El Kaim / StrongDM foundational essays on AI-built software as paradigm.*

### 43e68409a4 — 2389-research/coven: Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming <a id="43e68409a4"></a>

<https://github.com/2389-research/coven>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 42500eb134 — 2389-research/dotpowers: a superpowers implementation for attractors <a id="42500eb134"></a>

<https://github.com/2389-research/dotpowers>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/02-attractor-implementations.md` *(3)*

### c317a03b84 — 2389-research/mammoth <a id="c317a03b84"></a>

<https://github.com/2389-research/mammoth>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 8f251bd57a — 2389-research/smasher: A builder <a id="8f251bd57a"></a>

<https://github.com/2389-ai/smasher>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### f79769ac6c — 2389-research/tracker <a id="f79769ac6c"></a>

<https://github.com/2389-research/tracker>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 3703e782c0 — =?utf-8?Q?You=20Don=E2=80=99t=20Write=20the=20Code.=20You=20Don=E2=80=99t?= <a id="3703e782c0"></a>

<https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/01-shapiro-five-levels.md` *(2)*

### 2e49bcd671 — About assigning tasks to Copilot (file contains saved 2389-research/dotpowers GitHub page instead) <a id="2e49bcd671"></a>

<https://docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`

### d6bf9e3a7e — Completion, Chat, Agent, Claw – Dan Shapiro's Blog <a id="d6bf9e3a7e"></a>

<https://www.danshapiro.com/blog/2026/05/completion-chat-agent-claw>

- **Files:** mhtml ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/32-shapiro-completion-chat-agent-claw.md` · `research/followup/01-shapiro-five-levels.md` *(2)*

### 708f29cb35 — Coven — 2389 Research, Inc. <a id="708f29cb35"></a>

<https://2389.ai/products/coven>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 3af462fa75 — danshapiro/kilroy <a id="3af462fa75"></a>

<https://github.com/danshapiro/kilroy>

- **Files:** txt ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/06-hn-and-lenny.md` · `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/01-shapiro-five-levels.md` · `research/followup/02-attractor-implementations.md` *(5)*

### f908e4d494 — dotpowers — 2389 Research, Inc. <a id="f908e4d494"></a>

<https://2389.ai/products/dotpowers>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### fe423b2a50 — dotpowers/dotpowers.dot at main · 2389-research/dotpowers <a id="fe423b2a50"></a>

<https://github.com/2389-research/dotpowers/blob/main/dotpowers.dot>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/27-dotfile-pipelines-as-product.md` *(1)*

### c94a94f2d3 — El Kaim Book — Chapter 3: Intent-Driven Architecture <a id="c94a94f2d3"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `dark-factory` · `intent-driven-architecture`

### b2e8ea6df7 — Factory (StrongDM) — Attractor <a id="b2e8ea6df7"></a>

<https://factory.strongdm.ai/products/attractor>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` *(3)*

### d93e59de67 — Factory (StrongDM) — CXDB <a id="d93e59de67"></a>

<https://factory.strongdm.ai/products/cxdb>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### f2abe271f9 — Factory (StrongDM) — DTU <a id="f2abe271f9"></a>

<https://factory.strongdm.ai/techniques/dtu>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 1f8e6329d5 — Factory (StrongDM) — Gene Transfusion <a id="1f8e6329d5"></a>

<https://factory.strongdm.ai/techniques/gene-transfusion>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 6e7fbc4124 — Factory (StrongDM) — Home <a id="6e7fbc4124"></a>

<https://factory.strongdm.ai/>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/03-every-compound-engineering.md` · `research/05-simon-willison.md` · `research/06-hn-and-lenny.md` · `research/07-dark-factory.md` *(+1 more)* *(6)*

### a1032841ba — Factory (StrongDM) — Principles <a id="a1032841ba"></a>

<https://factory.strongdm.ai/principles>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/07-dark-factory.md` *(2)*

### b7e946fa1b — Factory (StrongDM) — Products <a id="b7e946fa1b"></a>

<https://factory.strongdm.ai/products>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 2e46f64134 — Factory (StrongDM) — Pyramid Summaries <a id="2e46f64134"></a>

<https://factory.strongdm.ai/techniques/pyramid-summaries>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 76447f23b5 — Factory (StrongDM) — Semport <a id="76447f23b5"></a>

<https://factory.strongdm.ai/techniques/semport>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 39c9037a8c — Factory (StrongDM) — Techniques <a id="39c9037a8c"></a>

<https://factory.strongdm.ai/techniques>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/07-dark-factory.md` *(2)*

### e7eab5a353 — Mammoth — 2389 Research, Inc. <a id="e7eab5a353"></a>

<https://2389.ai/products/mammoth>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 59d633b2c6 — Smasher — 2389 Research, Inc. <a id="59d633b2c6"></a>

<https://2389.ai/products/smasher>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 8282baf1e4 — Software factories and the agentic moment (Hacker News) <a id="8282baf1e4"></a>

<https://news.ycombinator.com/item?id=46924426>

- **Files:** html ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/06-hn-and-lenny.md` *(1)*

### e951bbc27e — strongdm/attractorbench: NLSpec instruction following benchmark <a id="e951bbc27e"></a>

<https://github.com/strongdm/attractorbench>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `evals-and-benchmarks` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/07-evals-deepdive.md` *(3)*

### 7c5da8e730 — The Dark Factory Is a .dot file — 2389 Research, Inc. <a id="7c5da8e730"></a>

<https://2389.ai/posts/the-dark-factory-is-a-dot-file>

- **Files:** mhtml ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/04-gastown-beads.md` *(3)*

### f675af7d98 — The Dark Factory: How Software Is Learning to Build Itself <a id="f675af7d98"></a>

<https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e>

- **Files:** txt ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/07-dark-factory.md` *(1)*

### 3a16af6be1 — The Dark Software Factory (BCG Platinion) <a id="3a16af6be1"></a>

<https://www.bcgplatinion.com/insights/the-dark-software-factory>

- **Files:** html ✓ · md ✓
- **Tags:** `dark-factory`

### 99b58be420 — The Five Levels: From Spicy Autocomplete to the Software Factory (Dan Shapiro) <a id="99b58be420"></a>

<https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory>

- **Files:** html ✓ · md ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/05-simon-willison.md` · `research/07-dark-factory.md` · `research/followup/01-shapiro-five-levels.md` *(3)*

### 44d4c1be80 — The Software Factory <a id="44d4c1be80"></a>

<https://lukepm.com/blog/the-software-factory>

- **Files:** txt ✓
- **Tags:** `dark-factory`

### 400f0c3c0a — The Software Factory: When No Human Writes or Reviews the Code <a id="400f0c3c0a"></a>

<https://www.thepragmaticcto.com/p/the-software-factory-when-no-human>

- **Files:** html ✓ · md ✓
- **Tags:** `dark-factory`

### 4d0de0d106 — Tracker — 2389 Research, Inc. <a id="4d0de0d106"></a>

<https://2389.ai/products/tracker>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 97f2036966 — Untitled Webflow-hosted PDF (no /Title metadata) <a id="97f2036966"></a>

<https://cdn.prod.website-files.com/655cded084fee2e958faaffc/69b8331d6141dc7278866f9c_D>

- **Files:** html ✓ · md ✓
- **Tags:** `dark-factory`

### d9e1bd997d — When AI Agents Write Your Code, Does Language Choice Matter? <a id="d9e1bd997d"></a>

<https://www.thepragmaticcto.com/p/when-ai-agents-write-your-code-does>

- **Files:** txt ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/33-language-choice-as-harness.md` *(1)*

### 60fbea1689 — William El Kaim — About (Medium) <a id="60fbea1689"></a>

<https://medium.com/@welkaim/about>

- **Files:** txt ✓ · html ✓ · html ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/07-dark-factory.md` *(1)*

### 7dbf96d872 — William El Kaim — Medium <a id="7dbf96d872"></a>

<https://welkaim.medium.com/>

- **Files:** other ✓ · html ✓ · html ✓
- **Tags:** `dark-factory`
- **Cited in:** `research/07-dark-factory.md` *(1)*


### intent-driven-architecture *(9 records)*

*Intent-driven / continuous enterprise architecture, RISE-style automation, product-line variability.*

### 8c295c7ecf — El Kaim Book — Chapter 1: The Limits of Traditional Enterprise Architecture <a id="8c295c7ecf"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### 12ddb278e4 — El Kaim Book — Chapter 2: Continuous Enterprise Architecture <a id="12ddb278e4"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### c94a94f2d3 — El Kaim Book — Chapter 3: Intent-Driven Architecture <a id="c94a94f2d3"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `dark-factory` · `intent-driven-architecture`

### a37637a130 — El Kaim Book — Chapter 4: Why AI and Automation Change Everything <a id="a37637a130"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### 9e3537481f — El Kaim Book — Chapter 5: Automating RISE with SAP <a id="9e3537481f"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### 49a055f96d — El Kaim Book — Chapter 6: The Enterprise Architecture Function <a id="49a055f96d"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### e78ab8b5d2 — El Kaim Book — Chapter 7: Automating Enterprise Architecture <a id="e78ab8b5d2"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### b59dfbed79 — El Kaim Book — Chapter 8: From Intent to Specification <a id="b59dfbed79"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`

### f52a2d4098 — El Kaim Book — Chapter 9: Software Product Line and Variability <a id="f52a2d4098"></a>

*(no canonical URL)*

- **Files:** txt ✓
- **Tags:** `intent-driven-architecture`


### spec-authorship *(3 records)*

*Requirements engineering, BMAD, scenario testing, INCOSE primer, spec-as-prompt practice.*

### 34b7fdd99d — Requirements Writing Guide | Docs | 8090 <a id="34b7fdd99d"></a>

<https://www.8090.ai/docs/opinions/requirements-writing-guide>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate` · `spec-authorship`

### 95265c651d — Spec-driven development: The AI engineering workflow (Lenny's Newsletter) <a id="95265c651d"></a>

<https://www.lennysnewsletter.com/p/spec-driven-development-the-ai-engineering>

- **Files:** txt ✓
- **Tags:** `compound-engineering` · `spec-authorship`
- **Cited in:** `research/35-lenny-howiai-spec-driven-and-team-ops.md` *(1)*

### 292ea05299 — Work Order Writing Guide | Docs | 8090 <a id="292ea05299"></a>

<https://www.8090.ai/docs/opinions/work-order-writing-guide>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate` · `spec-authorship`


### willison-canon *(26 records)*

*Simon Willison's collected writings + interviews.*

### 08be49ea7d — Agentic Engineering Patterns - Simon Willison's Weblog <a id="08be49ea7d"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` · `research/06-hn-and-lenny.md` *(2)*

### 2263d13b18 — Agentic manual testing - Agentic Engineering Patterns <a id="2263d13b18"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 23efb53da9 — Agents are models using tools in a loop <a id="23efb53da9"></a>

<https://simonwillison.net/2025/May/22/tools-in-a-loop>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### f8007cc630 — An AI State of the Union | Simon Willison (Lenny's Newsletter) <a id="f8007cc630"></a>

<https://www.lennysnewsletter.com/p/an-ai-state-of-the-union>

- **Files:** html ✓ · html ✓ · txt ✓ · txt ✓ · html (want) · md ✓ · txt ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/06-hn-and-lenny.md` *(1)*

### 86f58b89a9 — Anti-patterns: things to avoid - Agentic Engineering Patterns <a id="86f58b89a9"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### cad3fa5db1 — Claude Code: Best practices for agentic coding <a id="cad3fa5db1"></a>

<https://simonwillison.net/2025/Apr/19/claude-code-best-practices>

- **Files:** html ✓
- **Tags:** `anthropic-substrate` · `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 875b882ad1 — Designing agentic loops <a id="875b882ad1"></a>

<https://simonwillison.net/2025/Sep/30/designing-agentic-loops>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 1b74bb31e3 — Embracing the parallel coding agent lifestyle <a id="1b74bb31e3"></a>

<https://simonwillison.net/2025/Oct/5/parallel-coding-agents>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### c6074ee6d6 — First run the tests - Agentic Engineering Patterns - Simon Willison's Weblog <a id="c6074ee6d6"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 4c98a39ea9 — Hoard things you know how to do - Agentic Engineering Patterns - Simon Willison's Weblog <a id="4c98a39ea9"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 53b4490fe8 — How coding agents work - Agentic Engineering Patterns - Simon Willison's Weblog <a id="53b4490fe8"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 303c8ff4e8 — How StrongDM's AI team build serious software without even looking at the code <a id="303c8ff4e8"></a>

<https://simonwillison.net/2026/Feb/7/software-factory>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` · `research/06-hn-and-lenny.md` · `research/07-dark-factory.md` *(3)*

### 95ba3accbc — I think "agent" may finally have a widely enough agreed upon definition to be useful jargon now <a id="95ba3accbc"></a>

<https://simonwillison.net/2025/Sep/18/agents>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### dbc37326e4 — Interactive explanations - Agentic Engineering Patterns - Simon Willison's Weblog <a id="dbc37326e4"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### d95bf55a39 — Linear walkthroughs - Agentic Engineering Patterns - Simon Willison's Weblog <a id="d95bf55a39"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 1e8169decc — Prompts I use - Agentic Engineering Patterns - Simon Willison's Weblog <a id="1e8169decc"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/prompts>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### b4b5b2e638 — Red/green TDD - Agentic Engineering Patterns - Simon Willison's Weblog <a id="b4b5b2e638"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` · `research/06-hn-and-lenny.md` *(2)*

### 11ae110ddb — Simon Willison on agentic-engineering <a id="11ae110ddb"></a>

<https://simonwillison.net/tags/agentic-engineering>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 67dfba1ed6 — Simon Willison on evals <a id="67dfba1ed6"></a>

<https://simonwillison.net/tags/evals>

- **Files:** html ✓
- **Tags:** `evals-and-benchmarks` · `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 53ed6e363d — Simon Willison — CaMeL paper writeup <a id="53ed6e363d"></a>

<https://simonwillison.net/2025/Apr/11/camel>

*Willison summary of the CaMeL prompt-injection defense paper*

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `security-primitives` · `willison-canon`
- **Cited in:** `research/06-hn-and-lenny.md` · `research/followup/08-security-primitives.md` *(2)*

### 3262892c6c — Subagents - Agentic Engineering Patterns - Simon Willison's Weblog <a id="3262892c6c"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/subagents>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 9c9554d27e — The lethal trifecta for AI agents: private data, untrusted content, and external communication <a id="9c9554d27e"></a>

<https://simonwillison.net/2025/Jun/16/the-lethal-trifecta>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/06-hn-and-lenny.md` · `research/followup/08-security-primitives.md` *(2)*

### a811ab37e6 — Vibe coding and agentic engineering are getting closer than I'd like <a id="a811ab37e6"></a>

<https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 4ccc7d8083 — What is agentic engineering? - Agentic Engineering Patterns - Simon Willison's Weblog <a id="4ccc7d8083"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 4d44956ef1 — Writing about Agentic Engineering Patterns <a id="4d44956ef1"></a>

<https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 470703acd9 — Writing code is cheap now - Agentic Engineering Patterns - Simon Willison's Weblog <a id="470703acd9"></a>

<https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap>

- **Files:** html ✓
- **Tags:** `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*


### compound-engineering *(11 records)*

*Compound-engineering workflows, personal harnesses, practitioner accounts (Klaassen / Reed / How I AI).*

### ac5b4f8018 — Build your own AI developer tools with Claude Code (How I AI, Lenny's Newsletter) <a id="ac5b4f8018"></a>

<https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build>

- **Files:** txt ✓
- **Tags:** `anthropic-substrate` · `compound-engineering`
- **Cited in:** `research/34-lenny-howiai-personal-harnesses.md` *(1)*

### 4b1f62e4fc — Compound Engineering <a id="4b1f62e4fc"></a>

<https://every.to/guides/compound-engineering>

- **Files:** html ✓ · txt ✓
- **Tags:** `compound-engineering`
- **Cited in:** `research/03-every-compound-engineering.md` · `research/followup/05-klaassen-siblings.md` *(2)*

### 8fa24c4cd3 — Compound Engineering: How Every Codes With Agents <a id="8fa24c4cd3"></a>

<https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents>

- **Files:** html ✓ · txt ✓
- **Tags:** `compound-engineering`
- **Cited in:** `research/03-every-compound-engineering.md` · `research/followup/05-klaassen-siblings.md` *(2)*

### 67b1f7d3a3 — Culture of AI Engineering <a id="67b1f7d3a3"></a>

<https://every.to/source-code/the-culture-of-ai-engineering>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture` · `compound-engineering`

### a747576e0f — How I AI: CJ Hess on Building Custom AI Tools (Lenny's Newsletter) <a id="a747576e0f"></a>

<https://www.lennysnewsletter.com/p/how-i-ai-cj-hess>

- **Files:** txt ✓
- **Tags:** `compound-engineering`

### b0d89f5419 — How to Work and Compound with AI <a id="b0d89f5419"></a>

<https://eugeneyan.com/writing/working-with-ai>

- **Files:** mhtml ✓
- **Tags:** `compound-engineering`

### 243a228bd1 — My AI Had Already Fixed the Code Before I Saw It <a id="243a228bd1"></a>

<https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it>

- **Files:** html ✓ · html ✓ · txt ✓ · txt ✓
- **Tags:** `compound-engineering`
- **Cited in:** `research/03-every-compound-engineering.md` *(1)*

### 516e66f9f7 — Quests, token leaderboards, and a skills marketplace: The elite AI adoption playbook | John Kim (Sendbird) <a id="516e66f9f7"></a>

<https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation>

- **Files:** txt ✓
- **Tags:** `compound-engineering` · `skills-composition`
- **Cited in:** `research/36-sendbird-quests-token-tiers.md` *(1)*

### 95265c651d — Spec-driven development: The AI engineering workflow (Lenny's Newsletter) <a id="95265c651d"></a>

<https://www.lennysnewsletter.com/p/spec-driven-development-the-ai-engineering>

- **Files:** txt ✓
- **Tags:** `compound-engineering` · `spec-authorship`
- **Cited in:** `research/35-lenny-howiai-spec-driven-and-team-ops.md` *(1)*

### 5b2ed8c57e — Spec-driven development: The AI engineering workflow at Notion | Ryan Nystrom <a id="5b2ed8c57e"></a>

<https://www.chatprd.ai/how-i-ai/ryan-nystrom-notion-workflows-for-engineering-velocity>

- **Files:** txt ✓
- **Tags:** `compound-engineering`
- **Cited in:** `research/35-lenny-howiai-spec-driven-and-team-ops.md` *(1)*

### 0ee794b3a3 — The Agent That Saved My Brain <a id="0ee794b3a3"></a>

<https://every.to/p/the-agent-that-saved-my-brain>

- **Files:** html ✓ · txt ✓
- **Tags:** `compound-engineering`
- **Cited in:** `research/03-every-compound-engineering.md` *(1)*


### anthropic-substrate *(10 records)*

*Claude Code substrate, Anthropic engineering posts, Cherny interviews.*

### a3afc1e8c7 — (unknown) <a id="a3afc1e8c7"></a>

<https://www.anthropic.com/engineering/multi-agent-research-system>

- **Files:** html ✓ · md ✓
- **Tags:** `anthropic-substrate`
- **Cited in:** `research/followup/07-evals-deepdive.md` *(1)*

### bdba59d7ee — Agent Skills — Best Practices (Claude docs) <a id="bdba59d7ee"></a>

<https://platform.claude.com/docs/en/agent-skills/best-practices>

- **Files:** html ✓ · md ✓
- **Tags:** `anthropic-substrate` · `skills-composition`
- **Cited in:** `research/PLAN.md` *(1)*

### 9d696416cb — Anthropic Agent Skills — Overview (Platform docs) <a id="9d696416cb"></a>

<https://platform.claude.com/docs/en/agent-skills/overview>

- **Files:** txt ✓
- **Tags:** `anthropic-substrate` · `skills-composition`

### ac5b4f8018 — Build your own AI developer tools with Claude Code (How I AI, Lenny's Newsletter) <a id="ac5b4f8018"></a>

<https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build>

- **Files:** txt ✓
- **Tags:** `anthropic-substrate` · `compound-engineering`
- **Cited in:** `research/34-lenny-howiai-personal-harnesses.md` *(1)*

### ffc229d838 — Building Effective Agents <a id="ffc229d838"></a>

<https://www.anthropic.com/engineering/building-effective-agents>

*Anthropic engineering — orchestrator-worker, evaluator-optimizer, augmented LLM patterns*

- **Files:** html ✓ · md ✓
- **Tags:** `anthropic-substrate`

### cad3fa5db1 — Claude Code: Best practices for agentic coding <a id="cad3fa5db1"></a>

<https://simonwillison.net/2025/Apr/19/claude-code-best-practices>

- **Files:** html ✓
- **Tags:** `anthropic-substrate` · `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### 586cb02137 — Head of Claude Code: What happens when AI does 90% of the coding <a id="586cb02137"></a>

<https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens>

- **Files:** html ✓ · txt ✓ · txt ✓ · txt ✓
- **Tags:** `anthropic-substrate`
- **Cited in:** `research/06-hn-and-lenny.md` · `research/followup/03-cherny-interview.md` *(2)*

### ee885bfc4c — Skill authoring best practices - Claude API Docs <a id="ee885bfc4c"></a>

<https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>

- **Files:** mhtml ✓
- **Tags:** `anthropic-substrate` · `skills-composition`

### 26035151aa — The Complete Guide to Building Skills for Claude <a id="26035151aa"></a>

<https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf>

- **Files:** pdf ✓
- **Tags:** `anthropic-substrate` · `skills-composition`

### 3643d46af4 — What are Skills? (Anthropic support) <a id="3643d46af4"></a>

<https://support.claude.com/en/articles/what-are-skills>

- **Files:** txt ✓
- **Tags:** `anthropic-substrate` · `skills-composition`


### openai-substrate *(8 records)*

*Codex substrate, OpenAI cookbook, running-codex-safely docs.*

### dccefbfc62 — =?utf-8?Q?Agent=20approvals=20&=20security=20=E2=80=93=20Codex=20|=20Open?= <a id="dccefbfc62"></a>

<https://developers.openai.com/codex/agent-approvals-security>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*

### 175cba9347 — =?utf-8?Q?Custom=20instructions=20with=20AGENTS.md=20=E2=80=93=20Codex=20?= <a id="175cba9347"></a>

<https://developers.openai.com/codex/guides/agents-md>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*

### 8334be0240 — =?utf-8?Q?Subagents=20=E2=80=93=20Codex=20|=20OpenAI=20Developers?= <a id="8334be0240"></a>

<https://developers.openai.com/codex/subagents>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*

### f6b9330226 — Harness engineering: leveraging Codex in an agent-first world <a id="f6b9330226"></a>

<https://openai.com/index/harness-engineering>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture` · `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*

### 10b59b402b — Introducing SWE-bench Verified <a id="10b59b402b"></a>

<https://openai.com/index/introducing-swe-bench-verified>

- **Files:** txt ✓
- **Tags:** `evals-and-benchmarks` · `openai-substrate`
- **Cited in:** `research/22-academic-foundations.md` · `research/plan-sync.md` *(2)*

### c35a5146b7 — Rules – Codex | OpenAI Developers <a id="c35a5146b7"></a>

<https://developers.openai.com/codex/rules>

- **Files:** txt ✓
- **Tags:** `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` *(1)*

### 66be122077 — Running Codex safely at OpenAI <a id="66be122077"></a>

<https://openai.com/index/running-codex-safely>

- **Files:** txt ✓
- **Tags:** `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` *(1)*

### e205ffac9d — Unlocking the Codex harness: how we built the App Server <a id="e205ffac9d"></a>

<https://openai.com/index/unlocking-the-codex-harness>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture` · `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*


### other-vendor-substrate *(72 records)*

*GitHub Copilot, Replit Agent, Devin, Factory.ai, Tabnine, OpenHands, etc.*

### 43e68409a4 — 2389-research/coven: Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming <a id="43e68409a4"></a>

<https://github.com/2389-research/coven>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 42500eb134 — 2389-research/dotpowers: a superpowers implementation for attractors <a id="42500eb134"></a>

<https://github.com/2389-research/dotpowers>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/02-attractor-implementations.md` *(3)*

### c317a03b84 — 2389-research/mammoth <a id="c317a03b84"></a>

<https://github.com/2389-research/mammoth>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 8f251bd57a — 2389-research/smasher: A builder <a id="8f251bd57a"></a>

<https://github.com/2389-ai/smasher>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### f79769ac6c — 2389-research/tracker <a id="f79769ac6c"></a>

<https://github.com/2389-research/tracker>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 5c785e88b3 — 404 - GitHub Docs <a id="5c785e88b3"></a>

<https://docs.github.com/en/copilot/concepts/agents/about-coding-agent>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### 85cdf07ac2 — 8090 Inc Blog <a id="85cdf07ac2"></a>

<https://www.8090.inc/blog>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### 5cc5a296b6 — =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Agent=203:=20Our=20Most=20Au?= <a id="5cc5a296b6"></a>

<https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/20-replit-agent.md` · `research/plan-sync.md` *(2)*

### 73dc7199ce — =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Replit=20Agent=204:=20Built?= <a id="73dc7199ce"></a>

<https://blog.replit.com/introducing-agent-4-built-for-creativity>

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/20-replit-agent.md` · `research/plan-sync.md` *(2)*

### 23b7d51d69 — [2511.03690] The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents <a id="23b7d51d69"></a>

<https://arxiv.org/abs/2511.03690>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/11-openhands-substrate-audit.md` *(1)*

### 2e49bcd671 — About assigning tasks to Copilot (file contains saved 2389-research/dotpowers GitHub page instead) <a id="2e49bcd671"></a>

<https://docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`

### 991f3bf0f6 — About Copilot Workspace (GitHub Docs) <a id="991f3bf0f6"></a>

<https://docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace>

- **Files:** html (skip)
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/19-github-copilot-cloud-agent.md` *(1)*

### 325d8c1018 — About extensions for Copilot (capture is a PNG image, not the docs page) <a id="325d8c1018"></a>

<https://docs.github.com/en/copilot/concepts/copilot-extensions/about-extensions-for>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### ebc17186b3 — About GitHub Copilot cloud agent - GitHub Docs <a id="ebc17186b3"></a>

<https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/19-github-copilot-cloud-agent.md` *(1)*

### 1b03040a1b — Agent Guidelines | Tabnine Docs <a id="1b03040a1b"></a>

<https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/agent-guidelines>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### 8962e872bd — Agentic Engineering (IBM Think Topics) <a id="8962e872bd"></a>

<https://www.ibm.com/think/topics/agentic-engineering>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/12-adjacent-ecosystem.md` *(1)*

### 39405fa555 — Agentic Engineering: Redefining Software Engineering (LangChain) <a id="39405fa555"></a>

<https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/12-adjacent-ecosystem.md` *(1)*

### f313f7845c — Artifacts | Docs | 8090 <a id="f313f7845c"></a>

<https://www.8090.ai/docs/raw-materials/artifacts>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### 83fcd19c73 — Blueprint Writing Guide | Docs | 8090 <a id="83fcd19c73"></a>

<https://www.8090.ai/docs/opinions/blueprint-writing-guide>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### e36b18df01 — Blueprints | Docs | 8090 <a id="e36b18df01"></a>

<https://www.8090.ai/docs/modules/blueprints>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### dcc5c900a1 — Changelog | Docs | 8090 <a id="dcc5c900a1"></a>

<https://www.8090.ai/docs/resources/changelog>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### 8e651f5fda — Coaching Guidelines | Tabnine Docs <a id="8e651f5fda"></a>

<https://docs.tabnine.com/main/getting-started/context-engine/admin-console/coaching>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### d9aa0e7ad5 — Codebase Connection | Docs | 8090 <a id="d9aa0e7ad5"></a>

<https://www.8090.ai/docs/raw-materials/codebase>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### 54629e12fe — Context Engine | Tabnine Docs <a id="54629e12fe"></a>

<https://docs.tabnine.com/main/getting-started/context-engine>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### 708f29cb35 — Coven — 2389 Research, Inc. <a id="708f29cb35"></a>

<https://2389.ai/products/coven>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 265e444ae9 — Deployment Options | Tabnine Docs <a id="265e444ae9"></a>

<https://docs.tabnine.com/main/welcome/readme/architecture/deployment-options>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### 3274cc670c — Devin (Cognition AI) <a id="3274cc670c"></a>

<https://www.cognition.ai/blog/devin>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### f908e4d494 — dotpowers — 2389 Research, Inc. <a id="f908e4d494"></a>

<https://2389.ai/products/dotpowers>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### fe423b2a50 — dotpowers/dotpowers.dot at main · 2389-research/dotpowers <a id="fe423b2a50"></a>

<https://github.com/2389-research/dotpowers/blob/main/dotpowers.dot>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/27-dotfile-pipelines-as-product.md` *(1)*

### b2e8ea6df7 — Factory (StrongDM) — Attractor <a id="b2e8ea6df7"></a>

<https://factory.strongdm.ai/products/attractor>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` *(3)*

### d93e59de67 — Factory (StrongDM) — CXDB <a id="d93e59de67"></a>

<https://factory.strongdm.ai/products/cxdb>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### f2abe271f9 — Factory (StrongDM) — DTU <a id="f2abe271f9"></a>

<https://factory.strongdm.ai/techniques/dtu>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 1f8e6329d5 — Factory (StrongDM) — Gene Transfusion <a id="1f8e6329d5"></a>

<https://factory.strongdm.ai/techniques/gene-transfusion>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 6e7fbc4124 — Factory (StrongDM) — Home <a id="6e7fbc4124"></a>

<https://factory.strongdm.ai/>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/03-every-compound-engineering.md` · `research/05-simon-willison.md` · `research/06-hn-and-lenny.md` · `research/07-dark-factory.md` *(+1 more)* *(6)*

### a1032841ba — Factory (StrongDM) — Principles <a id="a1032841ba"></a>

<https://factory.strongdm.ai/principles>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/07-dark-factory.md` *(2)*

### b7e946fa1b — Factory (StrongDM) — Products <a id="b7e946fa1b"></a>

<https://factory.strongdm.ai/products>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 2e46f64134 — Factory (StrongDM) — Pyramid Summaries <a id="2e46f64134"></a>

<https://factory.strongdm.ai/techniques/pyramid-summaries>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 76447f23b5 — Factory (StrongDM) — Semport <a id="76447f23b5"></a>

<https://factory.strongdm.ai/techniques/semport>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` *(1)*

### 39c9037a8c — Factory (StrongDM) — Techniques <a id="39c9037a8c"></a>

<https://factory.strongdm.ai/techniques>

- **Files:** html ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/01-strongdm-factory.md` · `research/07-dark-factory.md` *(2)*

### 109582ff1a — Factory AI – Product <a id="109582ff1a"></a>

<https://www.factory.ai/product>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### 5f4b04494f — GitHub Actions CI/CD Pipeline | All-Hands-AI/OpenHands | DeepWiki <a id="5f4b04494f"></a>

<https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/11-openhands-substrate-audit.md` · `research/12-adjacent-ecosystem.md` *(2)*

### 1069d4d757 — Guidelines | Tabnine Docs <a id="1069d4d757"></a>

<https://docs.tabnine.com/main/getting-started/tabnine-agent/guidelines>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### 78717fec1f — Headless Mode - OpenHands Docs <a id="78717fec1f"></a>

<https://docs.all-hands.dev/usage/how-to/headless-mode>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/11-openhands-substrate-audit.md` *(1)*

### 8778ec392c — Introduction - OpenHands Docs <a id="8778ec392c"></a>

<https://docs.all-hands.dev/>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/11-openhands-substrate-audit.md` *(1)*

### 9ad71cb019 — Introduction | Docs | 8090 <a id="9ad71cb019"></a>

<https://www.8090.ai/docs/general/introduction>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### af38d390c2 — Kiro <a id="af38d390c2"></a>

<https://kiro.dev/>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/12-adjacent-ecosystem.md` *(1)*

### e7eab5a353 — Mammoth — 2389 Research, Inc. <a id="e7eab5a353"></a>

<https://2389.ai/products/mammoth>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### b973e0e535 — Managing code scanning alerts (capture is a PNG image, not the docs page) <a id="b973e0e535"></a>

<https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### 8e89b0d8e5 — Migrating from Jira | Docs | 8090 <a id="8e89b0d8e5"></a>

<https://www.8090.ai/docs/opinions/jira-migration>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### a5209cf735 — OpenHands AI Action · Actions · GitHub Marketplace <a id="a5209cf735"></a>

<https://github.com/marketplace/actions/openhands-ai-action>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/11-openhands-substrate-audit.md` *(1)*

### d77d04c052 — Privacy | Tabnine Docs <a id="d77d04c052"></a>

<https://docs.tabnine.com/main/welcome/readme/privacy>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### 271feb61a7 — Private Installation | Tabnine Docs <a id="271feb61a7"></a>

<https://docs.tabnine.com/main/administering-tabnine/private-installation>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### bdb0d1357f — Provenance and Attribution | Tabnine Docs <a id="bdb0d1357f"></a>

<https://docs.tabnine.com/main/welcome/readme/protection/provenance-and-attribution>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### 607f6af312 — Quickstart | Docs | 8090 <a id="607f6af312"></a>

<https://www.8090.ai/docs/general/quickstart>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### 12d3cc73b8 — Replit — Introducing Replit App Monitoring <a id="12d3cc73b8"></a>

<https://blog.replit.com/app-monitoring>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/20-replit-agent.md` *(1)*

### 34b7fdd99d — Requirements Writing Guide | Docs | 8090 <a id="34b7fdd99d"></a>

<https://www.8090.ai/docs/opinions/requirements-writing-guide>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate` · `spec-authorship`

### f3e4b69e8c — Requirements | Docs | 8090 <a id="f3e4b69e8c"></a>

<https://www.8090.ai/docs/modules/requirements>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### 59d633b2c6 — Smasher — 2389 Research, Inc. <a id="59d633b2c6"></a>

<https://2389.ai/products/smasher>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### a03c2b3502 — Software Factory Roadmap 2026 — 8090 <a id="a03c2b3502"></a>

<https://www.8090.ai/docs/resources/roadmap>

- **Files:** other ✓
- **Tags:** `other-vendor-substrate`

### e951bbc27e — strongdm/attractorbench: NLSpec instruction following benchmark <a id="e951bbc27e"></a>

<https://github.com/strongdm/attractorbench>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `evals-and-benchmarks` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/07-evals-deepdive.md` *(3)*

### b5fc7f9df9 — Superconductor <a id="b5fc7f9df9"></a>

<https://www.superconductor.com/>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`

### be4a3756f4 — SWE-agent documentation <a id="be4a3756f4"></a>

<https://swe-agent.com/latest>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks` · `other-vendor-substrate`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### cd9714d14e — SWE-agent: Agent-Computer Interfaces (ACI) <a id="cd9714d14e"></a>

<https://swe-agent.com/latest/background/aci>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks` · `other-vendor-substrate`

### 5492497a11 — Tabnine Docs (Server Setup Guide) <a id="5492497a11"></a>

<https://docs.tabnine.com/main/administering-tabnine/private-installation/server-setup-guide>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### dafe463e94 — Tabnine Docs (Tabnine's Private and Protect) <a id="dafe463e94"></a>

<https://docs.tabnine.com/main/welcome/readme/ai-models/tabnines-private-and-protect>

- **Files:** html ✓
- **Tags:** `other-vendor-substrate`

### 7c5da8e730 — The Dark Factory Is a .dot file — 2389 Research, Inc. <a id="7c5da8e730"></a>

<https://2389.ai/posts/the-dark-factory-is-a-dot-file>

- **Files:** mhtml ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/04-gastown-beads.md` *(3)*

### 1175dde05f — The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents (arXiv 2511.03690 PDF) <a id="1175dde05f"></a>

<https://arxiv.org/pdf/2511.03690>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/11-openhands-substrate-audit.md` *(1)*

### 4d0de0d106 — Tracker — 2389 Research, Inc. <a id="4d0de0d106"></a>

<https://2389.ai/products/tracker>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/followup/02-attractor-implementations.md` *(2)*

### 8508964c2a — Validator | Docs | 8090 <a id="8508964c2a"></a>

<https://www.8090.ai/docs/modules/validator>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`

### a112fe3b90 — What is agentic coding? How it works and use cases | Google Cloud <a id="a112fe3b90"></a>

<https://cloud.google.com/discover/what-is-agentic-coding>

- **Files:** html ✓ · md ✓
- **Tags:** `other-vendor-substrate`
- **Cited in:** `research/12-adjacent-ecosystem.md` *(1)*

### 292ea05299 — Work Order Writing Guide | Docs | 8090 <a id="292ea05299"></a>

<https://www.8090.ai/docs/opinions/work-order-writing-guide>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate` · `spec-authorship`

### 2f73d1a742 — Work Orders | Docs | 8090 <a id="2f73d1a742"></a>

<https://www.8090.ai/docs/modules/work-orders>

- **Files:** mhtml ✓
- **Tags:** `other-vendor-substrate`


### skills-composition *(10 records)*

*Skills as a composition primitive — agentskills.io, Anthropic Agent Skills, MCP.*

### 1c3b30521c — Agent Skills Cookbook 01 — Introduction <a id="1c3b30521c"></a>

<https://github.com/anthropics/anthropic-cookbook/blob/main/skills/01_skills_introduction.ipynb>

- **Files:** ipynb ✓
- **Tags:** `skills-composition`

### 1f7e1ebaf3 — Agent Skills Cookbook 02 — Financial Applications <a id="1f7e1ebaf3"></a>

<https://github.com/anthropics/anthropic-cookbook/blob/main/skills/02_skills_financial_applications.ipynb>

- **Files:** ipynb ✓
- **Tags:** `skills-composition`

### b1b49c4c3d — Agent Skills Cookbook 03 — Custom Development <a id="b1b49c4c3d"></a>

<https://github.com/anthropics/anthropic-cookbook/blob/main/skills/03_skills_custom_development.ipynb>

- **Files:** ipynb ✓
- **Tags:** `skills-composition`

### bdba59d7ee — Agent Skills — Best Practices (Claude docs) <a id="bdba59d7ee"></a>

<https://platform.claude.com/docs/en/agent-skills/best-practices>

- **Files:** html ✓ · md ✓
- **Tags:** `anthropic-substrate` · `skills-composition`
- **Cited in:** `research/PLAN.md` *(1)*

### 5a9f63821f — Agent Skills: Security <a id="5a9f63821f"></a>

<https://platform.claude.com/docs/en/agent-skills/security>

- **Files:** html ✓ · md ✓ · html (want)
- **Tags:** `skills-composition`
- **Cited in:** `research/PLAN.md` *(1)*

### 9d696416cb — Anthropic Agent Skills — Overview (Platform docs) <a id="9d696416cb"></a>

<https://platform.claude.com/docs/en/agent-skills/overview>

- **Files:** txt ✓
- **Tags:** `anthropic-substrate` · `skills-composition`

### 516e66f9f7 — Quests, token leaderboards, and a skills marketplace: The elite AI adoption playbook | John Kim (Sendbird) <a id="516e66f9f7"></a>

<https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation>

- **Files:** txt ✓
- **Tags:** `compound-engineering` · `skills-composition`
- **Cited in:** `research/36-sendbird-quests-token-tiers.md` *(1)*

### ee885bfc4c — Skill authoring best practices - Claude API Docs <a id="ee885bfc4c"></a>

<https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>

- **Files:** mhtml ✓
- **Tags:** `anthropic-substrate` · `skills-composition`

### 26035151aa — The Complete Guide to Building Skills for Claude <a id="26035151aa"></a>

<https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf>

- **Files:** pdf ✓
- **Tags:** `anthropic-substrate` · `skills-composition`

### 3643d46af4 — What are Skills? (Anthropic support) <a id="3643d46af4"></a>

<https://support.claude.com/en/articles/what-are-skills>

- **Files:** txt ✓
- **Tags:** `anthropic-substrate` · `skills-composition`


### evals-and-benchmarks *(28 records)*

*SWE-bench, SWE-agent, AlphaCode, CodeGen, evals primers (Husain, Yan, Shankar).*

### 366927b32e — (unknown) <a id="366927b32e"></a>

<https://eugeneyan.com/404.html>

- **Files:** html ✓
- **Tags:** `evals-and-benchmarks`

### 2137eaa69f — [2203.07814] Competition-Level Code Generation with AlphaCode <a id="2137eaa69f"></a>

<https://arxiv.org/abs/2203.07814>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### bee5963dd8 — [2203.07814] Competition-Level Code Generation with AlphaCode (ar5iv HTML) <a id="bee5963dd8"></a>

<https://ar5iv.labs.arxiv.org/html/2203.07814>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations` · `evals-and-benchmarks`

### 5b36476e30 — [2203.13474] CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis <a id="5b36476e30"></a>

<https://arxiv.org/abs/2203.13474>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### 3e4a5dea3a — [2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues? <a id="3e4a5dea3a"></a>

<https://arxiv.org/abs/2310.06770>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### 54b1ddaabf — [2405.15793] SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering <a id="54b1ddaabf"></a>

<https://arxiv.org/abs/2405.15793>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### 71d2de09c6 — A Field Guide to Rapidly Improving AI Products <a id="71d2de09c6"></a>

<https://hamel.dev/blog/posts/field-guide>

*Hamel Husain — experiments-not-features roadmap reframe + NurtureBoss case study*

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/followup/07-evals-deepdive.md` *(1)*

### 49a54313c7 — Competitive programming with AlphaCode — Google DeepMind <a id="49a54313c7"></a>

<https://deepmind.google/discover/blog/competitive-programming-with-alphacode>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### 0c4bb49f75 — Creating an LLM-as-a-Judge <a id="0c4bb49f75"></a>

<https://hamel.dev/blog/posts/llm-judge>

*Hamel Husain — operational manual for LLM judges (Critique Shadowing pattern)*

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/followup/07-evals-deepdive.md` *(1)*

### caad3c1702 ~~Eugene Yan — LLM Evaluator~~ → see [ade5ef8d76](#ade5ef8d76)

### ade5ef8d76 — Eugene Yan — LLM Evaluators <a id="ade5ef8d76"></a>

<https://eugeneyan.com/writing/llm-evaluators>

*Third core eval source (with Husain and Anthropic multi-agent)*

- **Files:** html (want) · mhtml ✓
- **Tags:** `evals-and-benchmarks`

### 18856eb4cf — FAQs About AI Evals <a id="18856eb4cf"></a>

<https://hamel.dev/blog/posts/evals-faq>

*Husain & Shankar — 60-80% of dev time on error analysis*

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/followup/07-evals-deepdive.md` *(1)*

### 8cc1f9afc8 — Hamel Husain’s Blog <a id="8cc1f9afc8"></a>

<https://hamel.dev/>

- **Files:** mhtml ✓
- **Tags:** `evals-and-benchmarks`

### 10b59b402b — Introducing SWE-bench Verified <a id="10b59b402b"></a>

<https://openai.com/index/introducing-swe-bench-verified>

- **Files:** txt ✓
- **Tags:** `evals-and-benchmarks` · `openai-substrate`
- **Cited in:** `research/22-academic-foundations.md` · `research/plan-sync.md` *(2)*

### 6ea6e28334 — Langfuse Blog (index of posts) <a id="6ea6e28334"></a>

<https://langfuse.com/blog>

- **Files:** mhtml ✓
- **Tags:** `evals-and-benchmarks`

### da116da1a4 — Quality, Not Speed: Building a Production Evaluation Framework for AI-Assisted Medical Document Authoring — 8090 Blog <a id="da116da1a4"></a>

<https://www.8090.ai/blog/quality-not-speed-building-a-production-evaluation-framework-for-ai-assisted-medical-document-authoring>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture` · `evals-and-benchmarks`

### 67dfba1ed6 — Simon Willison on evals <a id="67dfba1ed6"></a>

<https://simonwillison.net/tags/evals>

- **Files:** html ✓
- **Tags:** `evals-and-benchmarks` · `willison-canon`
- **Cited in:** `research/05-simon-willison.md` *(1)*

### e951bbc27e — strongdm/attractorbench: NLSpec instruction following benchmark <a id="e951bbc27e"></a>

<https://github.com/strongdm/attractorbench>

- **Files:** txt ✓
- **Tags:** `dark-factory` · `evals-and-benchmarks` · `other-vendor-substrate`
- **Cited in:** `research/07-dark-factory.md` · `research/27-dotfile-pipelines-as-product.md` · `research/followup/07-evals-deepdive.md` *(3)*

### be4a3756f4 — SWE-agent documentation <a id="be4a3756f4"></a>

<https://swe-agent.com/latest>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks` · `other-vendor-substrate`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### cd9714d14e — SWE-agent: Agent-Computer Interfaces (ACI) <a id="cd9714d14e"></a>

<https://swe-agent.com/latest/background/aci>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks` · `other-vendor-substrate`

### 2ffe813975 — SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (OpenReview, NeurIPS 2024) <a id="2ffe813975"></a>

<https://openreview.net/forum?id=mXpq6ut8J3>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations` · `evals-and-benchmarks`

### 433a37bad4 — SWE-bench <a id="433a37bad4"></a>

<https://www.swebench.com/>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### ec39dd30f2 — SWE-bench (original) <a id="ec39dd30f2"></a>

<https://www.swebench.com/original.html>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`

### 16ed58023e — SWE-bench Lite <a id="16ed58023e"></a>

<https://www.swebench.com/lite.html>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`

### af47372f0f — SWE-bench Verified <a id="af47372f0f"></a>

<https://www.swebench.com/verified.html>

- **Files:** html ✓ · md ✓
- **Tags:** `evals-and-benchmarks`

### f9d207b032 — SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Princeton Language and Intelligence <a id="f9d207b032"></a>

<https://pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-github-issues>

- **Files:** mhtml ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/22-academic-foundations.md` · `research/plan-sync.md` *(2)*

### eb69cbdcba — Writing • Eugene Yan <a id="eb69cbdcba"></a>

<https://eugeneyan.com/writing>

- **Files:** mhtml ✓
- **Tags:** `evals-and-benchmarks`

### faa604dace — Your AI Product Needs Evals <a id="faa604dace"></a>

<https://hamel.dev/blog/posts/evals>

*Hamel Husain — the philosophical root of LLM eval discipline*

- **Files:** html ✓
- **Tags:** `evals-and-benchmarks`
- **Cited in:** `research/followup/07-evals-deepdive.md` *(1)*


### academic-foundations *(9 records)*

*Academic methodology papers: underspecification, multi-task benchmarks, CHI/ICSE studies.*

### 24ca29ee98 — (unknown) <a id="24ca29ee98"></a>

<https://arxiv.org/abs/2503.18813>

- **Files:** html (want) · html ✓ · md ✓ · other ✓ · other ✓ · other ✓
- **Tags:** `academic-foundations` · `security-primitives`
- **Cited in:** `research/followup/08-security-primitives.md` *(1)*

### 6bea7182f9 — (unknown) <a id="6bea7182f9"></a>

<https://arxiv.org/html/2505.13360v3>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations`
- **Cited in:** `research/26-prompt-underspecification-academic.md` *(1)*

### 7beb3bc828 — (unknown) <a id="7beb3bc828"></a>

<https://arxiv.org/html/2507.20439v1>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations`
- **Cited in:** `research/26-prompt-underspecification-academic.md` *(1)*

### bee5963dd8 — [2203.07814] Competition-Level Code Generation with AlphaCode (ar5iv HTML) <a id="bee5963dd8"></a>

<https://ar5iv.labs.arxiv.org/html/2203.07814>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations` · `evals-and-benchmarks`

### 7ff9a0b608 — CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis (OpenReview, ICLR 2023) <a id="7ff9a0b608"></a>

<https://openreview.net/forum?id=iaYcJKpY2B_>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations`
- **Cited in:** `research/22-academic-foundations.md` *(1)*

### e588b9bb1a — Defeating Prompt Injections by Design (arXiv:2503.18813v2) <a id="e588b9bb1a"></a>

<https://github.com/google-research/camel-prompt-injection>

- **Files:** pdf ✓
- **Tags:** `security-primitives` · `academic-foundations`

### fa20be05d7 — Neves-Bussmann (Stanford Computational Antitrust, Vol. 6, 2026) <a id="fa20be05d7"></a>

<https://law.stanford.edu/publications>

- **Files:** pdf ✓
- **Tags:** `academic-foundations` · `governance-and-legal`

### 2ffe813975 — SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (OpenReview, NeurIPS 2024) <a id="2ffe813975"></a>

<https://openreview.net/forum?id=mXpq6ut8J3>

- **Files:** html ✓ · md ✓
- **Tags:** `academic-foundations` · `evals-and-benchmarks`

### b4907c87f4 — The Prompt Report: A Systematic Survey of Prompt Engineering Techniques <a id="b4907c87f4"></a>

<https://arxiv.org/html/2406.06608v6>

- **Files:** mhtml ✓
- **Tags:** `academic-foundations`
- **Cited in:** `research/29-prompt-engineering-survey.md` *(1)*


### security-primitives *(4 records)*

*Threat models, prompt-injection defenses, capability/data-flow security (CaMeL, AgentDojo).*

### 24ca29ee98 — (unknown) <a id="24ca29ee98"></a>

<https://arxiv.org/abs/2503.18813>

- **Files:** html (want) · html ✓ · md ✓ · other ✓ · other ✓ · other ✓
- **Tags:** `academic-foundations` · `security-primitives`
- **Cited in:** `research/followup/08-security-primitives.md` *(1)*

### d30b9fbd12 — Defeating Prompt Injections by Design (arXiv 2503.18813 PDF) <a id="d30b9fbd12"></a>

<https://arxiv.org/pdf/2503.18813>

- **Files:** html ✓ · md ✓
- **Tags:** `security-primitives`

### e588b9bb1a — Defeating Prompt Injections by Design (arXiv:2503.18813v2) <a id="e588b9bb1a"></a>

<https://github.com/google-research/camel-prompt-injection>

- **Files:** pdf ✓
- **Tags:** `security-primitives` · `academic-foundations`

### 53ed6e363d — Simon Willison — CaMeL paper writeup <a id="53ed6e363d"></a>

<https://simonwillison.net/2025/Apr/11/camel>

*Willison summary of the CaMeL prompt-injection defense paper*

- **Files:** html (want) · html ✓ · md ✓ · mhtml ✓
- **Tags:** `security-primitives` · `willison-canon`
- **Cited in:** `research/06-hn-and-lenny.md` · `research/followup/08-security-primitives.md` *(2)*


### governance-and-legal *(7 records)*

*Stanford CodeX, Caremark / RSI board exposure, NHTSA levels, AUTOSAR, ISO 42010.*

### 0d2f8d5810 — AI Life Cycle Core Principles - CodeX - Stanford Law School <a id="0d2f8d5810"></a>

<https://law.stanford.edu/2023/03/17/ai-life-cycle-core-principles>

- **Files:** txt ✓
- **Tags:** `governance-and-legal`

### a4a2c507c6 — Built by Agents, Tested by Agents, Trusted by Whom? - CodeX - Stanford Law School <a id="a4a2c507c6"></a>

<https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom>

- **Files:** html ✓ · md ✓
- **Tags:** `governance-and-legal`

### d01c58d1d5 — Cognitive Escrow: The Human-Centered Principle Has a Blind Spot - CodeX - Stanford Law School <a id="d01c58d1d5"></a>

<https://law.stanford.edu/2026/03/07/cognitive-escrow-the-human-centered-principle-has-a-blind-spot>

- **Files:** txt ✓
- **Tags:** `governance-and-legal`
- **Cited in:** `research/30-cognitive-escrow.md` *(1)*

### 0d8acce129 — From Principles to Practice: The 48 Controls That Make Responsible AI Auditable, Defensible, and Real - CodeX - Stanford Law School <a id="0d8acce129"></a>

<https://law.stanford.edu/2026/02/16/from-principles-to-practice-the-48-controls-that-make-responsible-ai-auditable-defensible-and-real>

- **Files:** txt ✓
- **Tags:** `governance-and-legal`

### fa20be05d7 — Neves-Bussmann (Stanford Computational Antitrust, Vol. 6, 2026) <a id="fa20be05d7"></a>

<https://law.stanford.edu/publications>

- **Files:** pdf ✓
- **Tags:** `academic-foundations` · `governance-and-legal`

### b366ba8741 — The Ungovernable Machine <a id="b366ba8741"></a>

<https://law.stanford.edu/2026/03/17/the-ungovernable-machine>

- **Files:** txt ✓
- **Tags:** `governance-and-legal`
- **Cited in:** `research/31-caremark-rsi-board-exposure.md` *(1)*

### 71e8193f07 — Turning AI Governance Into Operational Infrastructure <a id="71e8193f07"></a>

<https://law.stanford.edu/2026/04/05/turning-ai-governance-into-operational-infrastructure>

- **Files:** txt ✓
- **Tags:** `governance-and-legal`


### ai-engineering-culture *(23 records)*

*Team-level dynamics, organisational culture, the social/operational side.*

### e6f77b9e81 — A Manifesto for Agentic Development <a id="e6f77b9e81"></a>

<https://jayminwest.substack.com/p/a-manifesto-for-agentic-development>

- **Files:** html ✓ · mhtml ✓
- **Tags:** `ai-engineering-culture`

### 80735d97d3 — AddyOsmani.com - Agentic Engineering <a id="80735d97d3"></a>

<https://addyosmani.com/blog/agentic-engineering>

- **Files:** html ✓ · md ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/12-adjacent-ecosystem.md` *(1)*

### 992e4f88b6 — Agentic Engineering Book (Jaymin West) <a id="992e4f88b6"></a>

<https://www.jayminwest.com/agentic-engineering-book>

- **Files:** html ✓ · md ✓
- **Tags:** `ai-engineering-culture`

### 35b057067e — Agentic Engineering Book – Chapter 6: Harnesses (Jaymin West) <a id="35b057067e"></a>

<https://www.jayminwest.com/agentic-engineering-book/6-harnesses>

- **Files:** html ✓ · md ✓
- **Tags:** `ai-engineering-culture`

### 8484aea116 — AI and the marshmallow test - by Sam Schillace <a id="8484aea116"></a>

<https://sundaylettersfromsam.substack.com/p/ai-and-the-marshmallow-test>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 4dae4e40d9 — Artisans and Factory Lines - by Sam Schillace <a id="4dae4e40d9"></a>

<https://sundaylettersfromsam.substack.com/p/artisans-and-factory-lines>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 384a19285c — Attention and collaboration in the AI world <a id="384a19285c"></a>

<https://sundaylettersfromsam.substack.com/p/attention-and-collaboration-in-the>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 890af05bff — Attention is all ya got - by Sam Schillace - Sunday Letters <a id="890af05bff"></a>

<https://sundaylettersfromsam.substack.com/p/attention-is-all-ya-got>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 67b1f7d3a3 — Culture of AI Engineering <a id="67b1f7d3a3"></a>

<https://every.to/source-code/the-culture-of-ai-engineering>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture` · `compound-engineering`

### f6b9330226 — Harness engineering: leveraging Codex in an agent-first world <a id="f6b9330226"></a>

<https://openai.com/index/harness-engineering>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture` · `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*

### 226e141838 — How it will happen - by Sam Schillace - Sunday Letters <a id="226e141838"></a>

<https://sundaylettersfromsam.substack.com/p/how-it-will-happen>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 83fdf58ee6 — I have seen the compounding teams - by Sam Schillace <a id="83fdf58ee6"></a>

<https://sundaylettersfromsam.substack.com/p/i-have-seen-the-compounding-teams>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### accca79ad1 — Machine with Concrete - by Sam Schillace - Sunday Letters <a id="accca79ad1"></a>

<https://sundaylettersfromsam.substack.com/p/machine-with-concrete>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### ecc055b160 — Part 1: Why Building Fast Is Not Enough — 8090 Blog <a id="ecc055b160"></a>

<https://www.8090.ai/blog/part-1-why-building-fast-is-not-enough>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture`

### 4ccd0104d2 — Part 2: What Alignment Actually Is — 8090 Blog <a id="4ccd0104d2"></a>

<https://www.8090.ai/blog/part-2-what-alignment-actually-is>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture`

### 388198d08f — Part 3: Seven Properties of an Aligned System — 8090 Blog <a id="388198d08f"></a>

<https://www.8090.ai/blog/part-3-seven-properties-of-an-aligned-system>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture`

### 5a214ded33 — Part 4: How Alignment Compounds — 8090 Blog <a id="5a214ded33"></a>

<https://www.8090.ai/blog/part-4-how-alignment-compounds->

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture`

### da116da1a4 — Quality, Not Speed: Building a Production Evaluation Framework for AI-Assisted Medical Document Authoring — 8090 Blog <a id="da116da1a4"></a>

<https://www.8090.ai/blog/quality-not-speed-building-a-production-evaluation-framework-for-ai-assisted-medical-document-authoring>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture` · `evals-and-benchmarks`

### 7839068ee6 — The agent-shaped world - by Sam Schillace - Sunday Letters <a id="7839068ee6"></a>

<https://sundaylettersfromsam.substack.com/p/the-agent-shaped-world>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 16aabc3cfe — The hard part isn't doing the work now; it's choosing the work. <a id="16aabc3cfe"></a>

<https://sundaylettersfromsam.substack.com/p/the-hard-part-isnt-doing-the-work>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### 19fba72517 — The one scarce resource AI can't replace - by Sam Schillace <a id="19fba72517"></a>

<https://sundaylettersfromsam.substack.com/p/laundry-lists-and-building-blocks>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*

### e205ffac9d — Unlocking the Codex harness: how we built the App Server <a id="e205ffac9d"></a>

<https://openai.com/index/unlocking-the-codex-harness>

- **Files:** txt ✓
- **Tags:** `ai-engineering-culture` · `openai-substrate`
- **Cited in:** `research/18-openai-codex-substrate.md` · `research/plan-sync.md` *(2)*

### 375a9386eb — What is a harness and why do I care? - by Sam Schillace <a id="375a9386eb"></a>

<https://sundaylettersfromsam.substack.com/p/what-is-a-harness-and-why-do-i-care>

- **Files:** mhtml ✓
- **Tags:** `ai-engineering-culture`
- **Cited in:** `research/28-schillace-sunday-letters.md` *(1)*


### meta-synthesis *(2 records)*

*Derived syntheses over the corpus (counterfactual deep-research, QC re-reads).*

### 1e18da4d24 — ChatGPT Deep Research synthesis (2026-05-11) — report <a id="1e18da4d24"></a>

*(no canonical URL)*

- **Files:** md ✓
- **Tags:** `meta-synthesis`

### c2cdaebb34 — ChatGPT Deep Research synthesis (2026-05-11) — sources list <a id="c2cdaebb34"></a>

*(no canonical URL)*

- **Files:** md ✓
- **Tags:** `meta-synthesis`


## By status (cross-cutting view)

### § 1 — Complete *(185 records)*

*Every registered file is present and complete.*

- [`366927b32e` — (unknown)](#366927b32e)
- [`6bea7182f9` — (unknown)](#6bea7182f9)
- [`7beb3bc828` — (unknown)](#7beb3bc828)
- [`a3afc1e8c7` — (unknown)](#a3afc1e8c7)
- [`43e68409a4` — 2389-research/coven: Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming](#43e68409a4)
- [`42500eb134` — 2389-research/dotpowers: a superpowers implementation for attractors](#42500eb134)
- [`c317a03b84` — 2389-research/mammoth](#c317a03b84)
- [`8f251bd57a` — 2389-research/smasher: A builder](#8f251bd57a)
- [`f79769ac6c` — 2389-research/tracker](#f79769ac6c)
- [`2137eaa69f` — [2203.07814] Competition-Level Code Generation with AlphaCode](#2137eaa69f)
- [`bee5963dd8` — [2203.07814] Competition-Level Code Generation with AlphaCode (ar5iv HTML)](#bee5963dd8)
- [`5b36476e30` — [2203.13474] CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis](#5b36476e30)
- [`3e4a5dea3a` — [2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](#3e4a5dea3a)
- [`54b1ddaabf` — [2405.15793] SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](#54b1ddaabf)
- [`23b7d51d69` — [2511.03690] The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents](#23b7d51d69)
- [`2e49bcd671` — About assigning tasks to Copilot (file contains saved 2389-research/dotpowers GitHub page instead)](#2e49bcd671)
- [`325d8c1018` — About extensions for Copilot (capture is a PNG image, not the docs page)](#325d8c1018)
- [`ebc17186b3` — About GitHub Copilot cloud agent - GitHub Docs](#ebc17186b3)
- [`80735d97d3` — AddyOsmani.com - Agentic Engineering](#80735d97d3)
- [`1b03040a1b` — Agent Guidelines | Tabnine Docs](#1b03040a1b)
- [`1c3b30521c` — Agent Skills Cookbook 01 — Introduction](#1c3b30521c)
- [`1f7e1ebaf3` — Agent Skills Cookbook 02 — Financial Applications](#1f7e1ebaf3)
- [`b1b49c4c3d` — Agent Skills Cookbook 03 — Custom Development](#b1b49c4c3d)
- [`bdba59d7ee` — Agent Skills — Best Practices (Claude docs)](#bdba59d7ee)
- [`8962e872bd` — Agentic Engineering (IBM Think Topics)](#8962e872bd)
- [`992e4f88b6` — Agentic Engineering Book (Jaymin West)](#992e4f88b6)
- [`35b057067e` — Agentic Engineering Book – Chapter 6: Harnesses (Jaymin West)](#35b057067e)
- [`08be49ea7d` — Agentic Engineering Patterns - Simon Willison's Weblog](#08be49ea7d)
- [`39405fa555` — Agentic Engineering: Redefining Software Engineering (LangChain)](#39405fa555)
- [`2263d13b18` — Agentic manual testing - Agentic Engineering Patterns](#2263d13b18)
- [`23efb53da9` — Agents are models using tools in a loop](#23efb53da9)
- [`8484aea116` — AI and the marshmallow test - by Sam Schillace](#8484aea116)
- [`0d2f8d5810` — AI Life Cycle Core Principles - CodeX - Stanford Law School](#0d2f8d5810)
- [`9d696416cb` — Anthropic Agent Skills — Overview (Platform docs)](#9d696416cb)
- [`86f58b89a9` — Anti-patterns: things to avoid - Agentic Engineering Patterns](#86f58b89a9)
- [`f313f7845c` — Artifacts | Docs | 8090](#f313f7845c)
- [`4dae4e40d9` — Artisans and Factory Lines - by Sam Schillace](#4dae4e40d9)
- [`384a19285c` — Attention and collaboration in the AI world](#384a19285c)
- [`890af05bff` — Attention is all ya got - by Sam Schillace - Sunday Letters](#890af05bff)
- [`83fcd19c73` — Blueprint Writing Guide | Docs | 8090](#83fcd19c73)
- [`e36b18df01` — Blueprints | Docs | 8090](#e36b18df01)
- [`ac5b4f8018` — Build your own AI developer tools with Claude Code (How I AI, Lenny's Newsletter)](#ac5b4f8018)
- [`ffc229d838` — Building Effective Agents](#ffc229d838)
- [`a4a2c507c6` — Built by Agents, Tested by Agents, Trusted by Whom? - CodeX - Stanford Law School](#a4a2c507c6)
- [`dcc5c900a1` — Changelog | Docs | 8090](#dcc5c900a1)
- [`1e18da4d24` — ChatGPT Deep Research synthesis (2026-05-11) — report](#1e18da4d24)
- [`c2cdaebb34` — ChatGPT Deep Research synthesis (2026-05-11) — sources list](#c2cdaebb34)
- [`cad3fa5db1` — Claude Code: Best practices for agentic coding](#cad3fa5db1)
- [`8e651f5fda` — Coaching Guidelines | Tabnine Docs](#8e651f5fda)
- [`d9aa0e7ad5` — Codebase Connection | Docs | 8090](#d9aa0e7ad5)
- [`7ff9a0b608` — CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis (OpenReview, ICLR 2023)](#7ff9a0b608)
- [`d01c58d1d5` — Cognitive Escrow: The Human-Centered Principle Has a Blind Spot - CodeX - Stanford Law School](#d01c58d1d5)
- [`49a54313c7` — Competitive programming with AlphaCode — Google DeepMind](#49a54313c7)
- [`d6bf9e3a7e` — Completion, Chat, Agent, Claw – Dan Shapiro's Blog](#d6bf9e3a7e)
- [`4b1f62e4fc` — Compound Engineering](#4b1f62e4fc)
- [`8fa24c4cd3` — Compound Engineering: How Every Codes With Agents](#8fa24c4cd3)
- [`54629e12fe` — Context Engine | Tabnine Docs](#54629e12fe)
- [`708f29cb35` — Coven — 2389 Research, Inc.](#708f29cb35)
- [`0c4bb49f75` — Creating an LLM-as-a-Judge](#0c4bb49f75)
- [`67b1f7d3a3` — Culture of AI Engineering](#67b1f7d3a3)
- [`3af462fa75` — danshapiro/kilroy](#3af462fa75)
- [`d30b9fbd12` — Defeating Prompt Injections by Design (arXiv 2503.18813 PDF)](#d30b9fbd12)
- [`e588b9bb1a` — Defeating Prompt Injections by Design (arXiv:2503.18813v2)](#e588b9bb1a)
- [`265e444ae9` — Deployment Options | Tabnine Docs](#265e444ae9)
- [`875b882ad1` — Designing agentic loops](#875b882ad1)
- [`f908e4d494` — dotpowers — 2389 Research, Inc.](#f908e4d494)
- [`fe423b2a50` — dotpowers/dotpowers.dot at main · 2389-research/dotpowers](#fe423b2a50)
- [`8c295c7ecf` — El Kaim Book — Chapter 1: The Limits of Traditional Enterprise Architecture](#8c295c7ecf)
- [`12ddb278e4` — El Kaim Book — Chapter 2: Continuous Enterprise Architecture](#12ddb278e4)
- [`c94a94f2d3` — El Kaim Book — Chapter 3: Intent-Driven Architecture](#c94a94f2d3)
- [`a37637a130` — El Kaim Book — Chapter 4: Why AI and Automation Change Everything](#a37637a130)
- [`9e3537481f` — El Kaim Book — Chapter 5: Automating RISE with SAP](#9e3537481f)
- [`49a055f96d` — El Kaim Book — Chapter 6: The Enterprise Architecture Function](#49a055f96d)
- [`e78ab8b5d2` — El Kaim Book — Chapter 7: Automating Enterprise Architecture](#e78ab8b5d2)
- [`b59dfbed79` — El Kaim Book — Chapter 8: From Intent to Specification](#b59dfbed79)
- [`f52a2d4098` — El Kaim Book — Chapter 9: Software Product Line and Variability](#f52a2d4098)
- [`1b74bb31e3` — Embracing the parallel coding agent lifestyle](#1b74bb31e3)
- [`b2e8ea6df7` — Factory (StrongDM) — Attractor](#b2e8ea6df7)
- [`d93e59de67` — Factory (StrongDM) — CXDB](#d93e59de67)
- [`f2abe271f9` — Factory (StrongDM) — DTU](#f2abe271f9)
- [`1f8e6329d5` — Factory (StrongDM) — Gene Transfusion](#1f8e6329d5)
- [`6e7fbc4124` — Factory (StrongDM) — Home](#6e7fbc4124)
- [`a1032841ba` — Factory (StrongDM) — Principles](#a1032841ba)
- [`b7e946fa1b` — Factory (StrongDM) — Products](#b7e946fa1b)
- [`2e46f64134` — Factory (StrongDM) — Pyramid Summaries](#2e46f64134)
- [`76447f23b5` — Factory (StrongDM) — Semport](#76447f23b5)
- [`39c9037a8c` — Factory (StrongDM) — Techniques](#39c9037a8c)
- [`109582ff1a` — Factory AI – Product](#109582ff1a)
- [`c6074ee6d6` — First run the tests - Agentic Engineering Patterns - Simon Willison's Weblog](#c6074ee6d6)
- [`0d8acce129` — From Principles to Practice: The 48 Controls That Make Responsible AI Auditable, Defensible, and Real - CodeX - Stanford Law School](#0d8acce129)
- [`5f4b04494f` — GitHub Actions CI/CD Pipeline | All-Hands-AI/OpenHands | DeepWiki](#5f4b04494f)
- [`1069d4d757` — Guidelines | Tabnine Docs](#1069d4d757)
- [`8cc1f9afc8` — Hamel Husain’s Blog](#8cc1f9afc8)
- [`f6b9330226` — Harness engineering: leveraging Codex in an agent-first world](#f6b9330226)
- [`78717fec1f` — Headless Mode - OpenHands Docs](#78717fec1f)
- [`4c98a39ea9` — Hoard things you know how to do - Agentic Engineering Patterns - Simon Willison's Weblog](#4c98a39ea9)
- [`53b4490fe8` — How coding agents work - Agentic Engineering Patterns - Simon Willison's Weblog](#53b4490fe8)
- [`a747576e0f` — How I AI: CJ Hess on Building Custom AI Tools (Lenny's Newsletter)](#a747576e0f)
- [`226e141838` — How it will happen - by Sam Schillace - Sunday Letters](#226e141838)
- [`303c8ff4e8` — How StrongDM's AI team build serious software without even looking at the code](#303c8ff4e8)
- [`b0d89f5419` — How to Work and Compound with AI](#b0d89f5419)
- [`83fdf58ee6` — I have seen the compounding teams - by Sam Schillace](#83fdf58ee6)
- [`95ba3accbc` — I think "agent" may finally have a widely enough agreed upon definition to be useful jargon now](#95ba3accbc)
- [`dbc37326e4` — Interactive explanations - Agentic Engineering Patterns - Simon Willison's Weblog](#dbc37326e4)
- [`10b59b402b` — Introducing SWE-bench Verified](#10b59b402b)
- [`8778ec392c` — Introduction - OpenHands Docs](#8778ec392c)
- [`9ad71cb019` — Introduction | Docs | 8090](#9ad71cb019)
- [`af38d390c2` — Kiro](#af38d390c2)
- [`6ea6e28334` — Langfuse Blog (index of posts)](#6ea6e28334)
- [`d95bf55a39` — Linear walkthroughs - Agentic Engineering Patterns - Simon Willison's Weblog](#d95bf55a39)
- [`accca79ad1` — Machine with Concrete - by Sam Schillace - Sunday Letters](#accca79ad1)
- [`e7eab5a353` — Mammoth — 2389 Research, Inc.](#e7eab5a353)
- [`b973e0e535` — Managing code scanning alerts (capture is a PNG image, not the docs page)](#b973e0e535)
- [`8e89b0d8e5` — Migrating from Jira | Docs | 8090](#8e89b0d8e5)
- [`243a228bd1` — My AI Had Already Fixed the Code Before I Saw It](#243a228bd1)
- [`fa20be05d7` — Neves-Bussmann (Stanford Computational Antitrust, Vol. 6, 2026)](#fa20be05d7)
- [`a5209cf735` — OpenHands AI Action · Actions · GitHub Marketplace](#a5209cf735)
- [`ecc055b160` — Part 1: Why Building Fast Is Not Enough — 8090 Blog](#ecc055b160)
- [`4ccd0104d2` — Part 2: What Alignment Actually Is — 8090 Blog](#4ccd0104d2)
- [`388198d08f` — Part 3: Seven Properties of an Aligned System — 8090 Blog](#388198d08f)
- [`5a214ded33` — Part 4: How Alignment Compounds — 8090 Blog](#5a214ded33)
- [`d77d04c052` — Privacy | Tabnine Docs](#d77d04c052)
- [`271feb61a7` — Private Installation | Tabnine Docs](#271feb61a7)
- [`1e8169decc` — Prompts I use - Agentic Engineering Patterns - Simon Willison's Weblog](#1e8169decc)
- [`bdb0d1357f` — Provenance and Attribution | Tabnine Docs](#bdb0d1357f)
- [`da116da1a4` — Quality, Not Speed: Building a Production Evaluation Framework for AI-Assisted Medical Document Authoring — 8090 Blog](#da116da1a4)
- [`516e66f9f7` — Quests, token leaderboards, and a skills marketplace: The elite AI adoption playbook | John Kim (Sendbird)](#516e66f9f7)
- [`607f6af312` — Quickstart | Docs | 8090](#607f6af312)
- [`b4b5b2e638` — Red/green TDD - Agentic Engineering Patterns - Simon Willison's Weblog](#b4b5b2e638)
- [`12d3cc73b8` — Replit — Introducing Replit App Monitoring](#12d3cc73b8)
- [`34b7fdd99d` — Requirements Writing Guide | Docs | 8090](#34b7fdd99d)
- [`f3e4b69e8c` — Requirements | Docs | 8090](#f3e4b69e8c)
- [`c35a5146b7` — Rules – Codex | OpenAI Developers](#c35a5146b7)
- [`66be122077` — Running Codex safely at OpenAI](#66be122077)
- [`11ae110ddb` — Simon Willison on agentic-engineering](#11ae110ddb)
- [`67dfba1ed6` — Simon Willison on evals](#67dfba1ed6)
- [`ee885bfc4c` — Skill authoring best practices - Claude API Docs](#ee885bfc4c)
- [`59d633b2c6` — Smasher — 2389 Research, Inc.](#59d633b2c6)
- [`8282baf1e4` — Software factories and the agentic moment (Hacker News)](#8282baf1e4)
- [`a03c2b3502` — Software Factory Roadmap 2026 — 8090](#a03c2b3502)
- [`95265c651d` — Spec-driven development: The AI engineering workflow (Lenny's Newsletter)](#95265c651d)
- [`5b2ed8c57e` — Spec-driven development: The AI engineering workflow at Notion | Ryan Nystrom](#5b2ed8c57e)
- [`e951bbc27e` — strongdm/attractorbench: NLSpec instruction following benchmark](#e951bbc27e)
- [`3262892c6c` — Subagents - Agentic Engineering Patterns - Simon Willison's Weblog](#3262892c6c)
- [`b5fc7f9df9` — Superconductor](#b5fc7f9df9)
- [`be4a3756f4` — SWE-agent documentation](#be4a3756f4)
- [`cd9714d14e` — SWE-agent: Agent-Computer Interfaces (ACI)](#cd9714d14e)
- [`2ffe813975` — SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (OpenReview, NeurIPS 2024)](#2ffe813975)
- [`433a37bad4` — SWE-bench](#433a37bad4)
- [`ec39dd30f2` — SWE-bench (original)](#ec39dd30f2)
- [`16ed58023e` — SWE-bench Lite](#16ed58023e)
- [`af47372f0f` — SWE-bench Verified](#af47372f0f)
- [`f9d207b032` — SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Princeton Language and Intelligence](#f9d207b032)
- [`0ee794b3a3` — The Agent That Saved My Brain](#0ee794b3a3)
- [`7839068ee6` — The agent-shaped world - by Sam Schillace - Sunday Letters](#7839068ee6)
- [`26035151aa` — The Complete Guide to Building Skills for Claude](#26035151aa)
- [`7c5da8e730` — The Dark Factory Is a .dot file — 2389 Research, Inc.](#7c5da8e730)
- [`f675af7d98` — The Dark Factory: How Software Is Learning to Build Itself](#f675af7d98)
- [`3a16af6be1` — The Dark Software Factory (BCG Platinion)](#3a16af6be1)
- [`99b58be420` — The Five Levels: From Spicy Autocomplete to the Software Factory (Dan Shapiro)](#99b58be420)
- [`16aabc3cfe` — The hard part isn't doing the work now; it's choosing the work.](#16aabc3cfe)
- [`19fba72517` — The one scarce resource AI can't replace - by Sam Schillace](#19fba72517)
- [`1175dde05f` — The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents (arXiv 2511.03690 PDF)](#1175dde05f)
- [`b4907c87f4` — The Prompt Report: A Systematic Survey of Prompt Engineering Techniques](#b4907c87f4)
- [`44d4c1be80` — The Software Factory](#44d4c1be80)
- [`400f0c3c0a` — The Software Factory: When No Human Writes or Reviews the Code](#400f0c3c0a)
- [`b366ba8741` — The Ungovernable Machine](#b366ba8741)
- [`4d0de0d106` — Tracker — 2389 Research, Inc.](#4d0de0d106)
- [`71e8193f07` — Turning AI Governance Into Operational Infrastructure](#71e8193f07)
- [`e205ffac9d` — Unlocking the Codex harness: how we built the App Server](#e205ffac9d)
- [`97f2036966` — Untitled Webflow-hosted PDF (no /Title metadata)](#97f2036966)
- [`8508964c2a` — Validator | Docs | 8090](#8508964c2a)
- [`a811ab37e6` — Vibe coding and agentic engineering are getting closer than I'd like](#a811ab37e6)
- [`3643d46af4` — What are Skills? (Anthropic support)](#3643d46af4)
- [`375a9386eb` — What is a harness and why do I care? - by Sam Schillace](#375a9386eb)
- [`a112fe3b90` — What is agentic coding? How it works and use cases | Google Cloud](#a112fe3b90)
- [`4ccc7d8083` — What is agentic engineering? - Agentic Engineering Patterns - Simon Willison's Weblog](#4ccc7d8083)
- [`d9e1bd997d` — When AI Agents Write Your Code, Does Language Choice Matter?](#d9e1bd997d)
- [`7dbf96d872` — William El Kaim — Medium](#7dbf96d872)
- [`292ea05299` — Work Order Writing Guide | Docs | 8090](#292ea05299)
- [`2f73d1a742` — Work Orders | Docs | 8090](#2f73d1a742)
- [`4d44956ef1` — Writing about Agentic Engineering Patterns](#4d44956ef1)
- [`470703acd9` — Writing code is cheap now - Agentic Engineering Patterns - Simon Willison's Weblog](#470703acd9)
- [`eb69cbdcba` — Writing • Eugene Yan](#eb69cbdcba)
- [`faa604dace` — Your AI Product Needs Evals](#faa604dace)

### § 2 — Partial *(22 records)*

*Has some content, but also files that are wanted, partial, or had fetch errors.*

- [`24ca29ee98` — (unknown)](#24ca29ee98)
- [`5c785e88b3` — 404 - GitHub Docs](#5c785e88b3)
- [`85cdf07ac2` — 8090 Inc Blog](#85cdf07ac2)
- [`dccefbfc62` — =?utf-8?Q?Agent=20approvals=20&=20security=20=E2=80=93=20Codex=20|=20Open?=](#dccefbfc62)
- [`175cba9347` — =?utf-8?Q?Custom=20instructions=20with=20AGENTS.md=20=E2=80=93=20Codex=20?=](#175cba9347)
- [`5cc5a296b6` — =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Agent=203:=20Our=20Most=20Au?=](#5cc5a296b6)
- [`73dc7199ce` — =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Replit=20Agent=204:=20Built?=](#73dc7199ce)
- [`8334be0240` — =?utf-8?Q?Subagents=20=E2=80=93=20Codex=20|=20OpenAI=20Developers?=](#8334be0240)
- [`3703e782c0` — =?utf-8?Q?You=20Don=E2=80=99t=20Write=20the=20Code.=20You=20Don=E2=80=99t?=](#3703e782c0)
- [`71d2de09c6` — A Field Guide to Rapidly Improving AI Products](#71d2de09c6)
- [`e6f77b9e81` — A Manifesto for Agentic Development](#e6f77b9e81)
- [`5a9f63821f` — Agent Skills: Security](#5a9f63821f)
- [`f8007cc630` — An AI State of the Union | Simon Willison (Lenny's Newsletter)](#f8007cc630)
- [`3274cc670c` — Devin (Cognition AI)](#3274cc670c)
- [`ade5ef8d76` — Eugene Yan — LLM Evaluators](#ade5ef8d76)
- [`18856eb4cf` — FAQs About AI Evals](#18856eb4cf)
- [`586cb02137` — Head of Claude Code: What happens when AI does 90% of the coding](#586cb02137)
- [`53ed6e363d` — Simon Willison — CaMeL paper writeup](#53ed6e363d)
- [`5492497a11` — Tabnine Docs (Server Setup Guide)](#5492497a11)
- [`dafe463e94` — Tabnine Docs (Tabnine's Private and Protect)](#dafe463e94)
- [`9c9554d27e` — The lethal trifecta for AI agents: private data, untrusted content, and external communication](#9c9554d27e)
- [`60fbea1689` — William El Kaim — About (Medium)](#60fbea1689)

### § 3a — Wanted (URL known) *(1 record)*

*URL is known but no content acquired yet.*

- [`991f3bf0f6` — About Copilot Workspace (GitHub Docs)](#991f3bf0f6)

### § 3b — Wanted (title only) *(0 records)*

*Title + search hints only; no URL yet.*

*(none)*

### § 4 — Superseded *(1 record)*

*Records replaced by another; `pointer_to` is set.*

- `caad3c1702` ~~Eugene Yan — LLM Evaluator~~ → [ade5ef8d76](#ade5ef8d76)

