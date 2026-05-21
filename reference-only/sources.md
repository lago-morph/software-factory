# Source catalog — browse view

Auto-generated from `reference-only/sources.json` by `.claude/skills/research-pipeline/scripts/render-sources-md.py`.
Do not edit by hand — your changes will be overwritten on next push to `main`.

**Records:** 214 · **Generated:** 2026-05-21 08:31 UTC

## Table of contents

- [🔴 Manual fetch needed](#manual-fetch-needed)
- [By category](#by-category)
  - [dark-factory](#cat-dark-factory) *(39)*
  - [intent-driven-architecture](#cat-intent-driven-architecture) *(9)*
  - [spec-authorship](#cat-spec-authorship) *(4)*
  - [willison-canon](#cat-willison-canon) *(26)*
  - [compound-engineering](#cat-compound-engineering) *(11)*
  - [anthropic-substrate](#cat-anthropic-substrate) *(10)*
  - [openai-substrate](#cat-openai-substrate) *(8)*
  - [other-vendor-substrate](#cat-other-vendor-substrate) *(75)*
  - [skills-composition](#cat-skills-composition) *(10)*
  - [evals-and-benchmarks](#cat-evals-and-benchmarks) *(28)*
  - [academic-foundations](#cat-academic-foundations) *(9)*
  - [security-primitives](#cat-security-primitives) *(4)*
  - [governance-and-legal](#cat-governance-and-legal) *(7)*
  - [ai-engineering-culture](#cat-ai-engineering-culture) *(23)*
  - [meta-synthesis](#cat-meta-synthesis) *(2)*
- [By status (cross-cutting view)](#by-status)
  - [§ 1 — Complete](#status-complete) *(196)*
  - [§ 2 — Partial](#status-partial) *(11)*
  - [§ 3a — Wanted (URL known)](#status-wanted-url) *(5)*
  - [§ 3b — Wanted (title only)](#status-wanted-title) *(0)*
  - [§ 4 — Superseded](#status-superseded) *(2)*

<a id="manual-fetch-needed"></a>
## 🔴 Manual fetch needed

**1 record(s)** have `ingestion_status=want` file entries — the fetch action couldn't get them automatically (Cloudflare challenge, JS-rendered SPA, paywall, or 404 with no successor).

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

| Record | Title | Source URL | Reason want | Drop as |
|---|---|---|---|---|
| `992e4f88b6` | Agentic Engineering Book (Jaymin West) | [Source URL](https://www.jayminwest.com/agentic-engineering-book) | Not yet fetched | `research/manual/992e4f88b6.mhtml` |


<a id="by-category"></a>
## By category

<a id="cat-dark-factory"></a>

<details>
<summary><b>dark-factory</b> — 39 records — <em>Dark-Factory canon — Shapiro / El Kaim / StrongDM foundational essays on AI-built software as paradigm.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="43e68409a4"></a>[`43e68409a4`](43e68409a4/) | **2389-research/coven: Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming** | [Source URL](https://github.com/2389-research/coven) | [Local Source](43e68409a4/2389-research_coven_%20Rust%20platform%20for%20orchestrating%20AI%20agents%20with%20tool%20capabilities%20and%20gRPC%20streaming.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="42500eb134"></a>[`42500eb134`](42500eb134/) | **2389-research/dotpowers: a superpowers implementation for attractors** | [Source URL](https://github.com/2389-research/dotpowers) | [Local Source](42500eb134/2389-research_dotpowers_%20a%20superpowers%20implementation%20for%20attractors.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(3)* |
| <a id="c317a03b84"></a>[`c317a03b84`](c317a03b84/) | **2389-research/mammoth** | [Source URL](https://github.com/2389-research/mammoth) | [Local Source](c317a03b84/2389-research_mammoth.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="8f251bd57a"></a>[`8f251bd57a`](8f251bd57a/) | **2389-research/smasher: A builder** | [Source URL](https://github.com/2389-ai/smasher) | [Local Source](8f251bd57a/2389-research_smasher_%20A%20builder.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="f79769ac6c"></a>[`f79769ac6c`](f79769ac6c/) | **2389-research/tracker** | [Source URL](https://github.com/2389-research/tracker) | [Local Source](f79769ac6c/2389-research_tracker.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="3703e782c0"></a>[`3703e782c0`](3703e782c0/) | **=?utf-8?Q?You=20Don=E2=80=99t=20Write=20the=20Code.=20You=20Don=E2=80=99t?=** | [Source URL](https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code) | [Local Source](3703e782c0/171372634d_www.danshapiro.com__blog__2026__02__you-dont-write-the-code.html) | html ✓ · md ✓ · mhtml ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/01-shapiro-five-levels.md`](../research/followup/01-shapiro-five-levels.md) *(2)* |
| <a id="2e49bcd671"></a>[`2e49bcd671`](2e49bcd671/) | **About assigning tasks to Copilot (file contains saved 2389-research/dotpowers GitHub page instead)** | [Source URL](https://docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot) | [Local Source](2e49bcd671/7c5f3e46f0_docs.github.com__en__copilot__how-tos__agents__about-assigning-tasks-to-copilot.html) | html ✓ | — |
| <a id="d6bf9e3a7e"></a>[`d6bf9e3a7e`](d6bf9e3a7e/) | **Completion, Chat, Agent, Claw – Dan Shapiro's Blog** | [Source URL](https://www.danshapiro.com/blog/2026/05/completion-chat-agent-claw) | [Local Source](d6bf9e3a7e/Completion%2C%20Chat%2C%20Agent%2C%20Claw%20%E2%80%93%20Dan%20Shapiro%27s%20Blog.mhtml) | mhtml ✓ | [`research/32-shapiro-completion-chat-agent-claw.md`](../research/32-shapiro-completion-chat-agent-claw.md) · [`research/followup/01-shapiro-five-levels.md`](../research/followup/01-shapiro-five-levels.md) *(2)* |
| <a id="708f29cb35"></a>[`708f29cb35`](708f29cb35/) | **Coven — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/coven) | [Local Source](708f29cb35/Coven%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="3af462fa75"></a>[`3af462fa75`](3af462fa75/) | **danshapiro/kilroy** | [Source URL](https://github.com/danshapiro/kilroy) | [Local Source](3af462fa75/danshapiro_kilroy.txt) | txt ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/01-shapiro-five-levels.md`](../research/followup/01-shapiro-five-levels.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(5)* |
| <a id="f908e4d494"></a>[`f908e4d494`](f908e4d494/) | **dotpowers — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/dotpowers) | [Local Source](f908e4d494/dotpowers%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="fe423b2a50"></a>[`fe423b2a50`](fe423b2a50/) | **dotpowers/dotpowers.dot at main · 2389-research/dotpowers** | [Source URL](https://github.com/2389-research/dotpowers/blob/main/dotpowers.dot) | [Local Source](fe423b2a50/dotpowers_dotpowers.dot%20at%20main%20%C2%B7%202389-research_dotpowers.txt) | txt ✓ | [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) *(1)* |
| <a id="c94a94f2d3"></a>[`c94a94f2d3`](c94a94f2d3/) | **El Kaim Book — Chapter 3: Intent-Driven Architecture** | — | [Local Source](c94a94f2d3/Chapter%203%20Intent-Driven%20Architectur.txt) | txt ✓ | — |
| <a id="b2e8ea6df7"></a>[`b2e8ea6df7`](b2e8ea6df7/) | **Factory (StrongDM) — Attractor** | [Source URL](https://factory.strongdm.ai/products/attractor) | [Local Source](b2e8ea6df7/factory.strongdm.ai__products__attractor.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) *(3)* |
| <a id="d93e59de67"></a>[`d93e59de67`](d93e59de67/) | **Factory (StrongDM) — CXDB** | [Source URL](https://factory.strongdm.ai/products/cxdb) | [Local Source](d93e59de67/factory.strongdm.ai__products__cxdb.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="f2abe271f9"></a>[`f2abe271f9`](f2abe271f9/) | **Factory (StrongDM) — DTU** | [Source URL](https://factory.strongdm.ai/techniques/dtu) | [Local Source](f2abe271f9/factory.strongdm.ai__techniques__dtu.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="1f8e6329d5"></a>[`1f8e6329d5`](1f8e6329d5/) | **Factory (StrongDM) — Gene Transfusion** | [Source URL](https://factory.strongdm.ai/techniques/gene-transfusion) | [Local Source](1f8e6329d5/factory.strongdm.ai__techniques__gene-transfusion.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="6e7fbc4124"></a>[`6e7fbc4124`](6e7fbc4124/) | **Factory (StrongDM) — Home** | [Source URL](https://factory.strongdm.ai/) | [Local Source](6e7fbc4124/factory.strongdm.ai.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/03-every-compound-engineering.md`](../research/03-every-compound-engineering.md) · [`research/05-simon-willison.md`](../research/05-simon-willison.md) · [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(+1 more)* *(6)* |
| <a id="a1032841ba"></a>[`a1032841ba`](a1032841ba/) | **Factory (StrongDM) — Principles** | [Source URL](https://factory.strongdm.ai/principles) | [Local Source](a1032841ba/factory.strongdm.ai__principles.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(2)* |
| <a id="b7e946fa1b"></a>[`b7e946fa1b`](b7e946fa1b/) | **Factory (StrongDM) — Products** | [Source URL](https://factory.strongdm.ai/products) | [Local Source](b7e946fa1b/factory.strongdm.ai__products.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="2e46f64134"></a>[`2e46f64134`](2e46f64134/) | **Factory (StrongDM) — Pyramid Summaries** | [Source URL](https://factory.strongdm.ai/techniques/pyramid-summaries) | [Local Source](2e46f64134/factory.strongdm.ai__techniques__pyramid-summaries.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="76447f23b5"></a>[`76447f23b5`](76447f23b5/) | **Factory (StrongDM) — Semport** | [Source URL](https://factory.strongdm.ai/techniques/semport) | [Local Source](76447f23b5/factory.strongdm.ai__techniques__semport.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="39c9037a8c"></a>[`39c9037a8c`](39c9037a8c/) | **Factory (StrongDM) — Techniques** | [Source URL](https://factory.strongdm.ai/techniques) | [Local Source](39c9037a8c/factory.strongdm.ai__techniques.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(2)* |
| <a id="e7eab5a353"></a>[`e7eab5a353`](e7eab5a353/) | **Mammoth — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/mammoth) | [Local Source](e7eab5a353/Mammoth%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="59d633b2c6"></a>[`59d633b2c6`](59d633b2c6/) | **Smasher — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/smasher) | [Local Source](59d633b2c6/Smasher%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="8282baf1e4"></a>[`8282baf1e4`](8282baf1e4/) | **Software factories and the agentic moment (Hacker News)** | [Source URL](https://news.ycombinator.com/item?id=46924426) | [Local Source](8282baf1e4/news.ycombinator.com__item__q__id_eq_46924426.html) | html ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) *(1)* |
| <a id="e951bbc27e"></a>[`e951bbc27e`](e951bbc27e/) | **strongdm/attractorbench: NLSpec instruction following benchmark** | [Source URL](https://github.com/strongdm/attractorbench) | [Local Source](e951bbc27e/strongdm_attractorbench_%20NLSpec%20instruction%20following%20benchmark%20for%20https___factory.strongdm.ai_products_attractor.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(3)* |
| <a id="7c5da8e730"></a>[`7c5da8e730`](7c5da8e730/) | **The Dark Factory Is a .dot file — 2389 Research, Inc.** | [Source URL](https://2389.ai/posts/the-dark-factory-is-a-dot-file) | [Local Source](7c5da8e730/The%20Dark%20Factory%20Is%20a%20.dot%20file%20%E2%80%94%202389%20Research%2C%20Inc.mhtml) | mhtml ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/04-gastown-beads.md`](../research/followup/04-gastown-beads.md) *(3)* |
| <a id="f675af7d98"></a>[`f675af7d98`](f675af7d98/) | **The Dark Factory: How Software Is Learning to Build Itself** | [Source URL](https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e) | [Local Source](f675af7d98/dark-factory-article.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(1)* |
| <a id="3a16af6be1"></a>[`3a16af6be1`](3a16af6be1/) | **The Dark Software Factory (BCG Platinion)** | [Source URL](https://www.bcgplatinion.com/insights/the-dark-software-factory) | [Local Source](3a16af6be1/0257d222ac_www.bcgplatinion.com__insights__the-dark-software-factory.html) | html ✓ · md ✓ | — |
| <a id="99b58be420"></a>[`99b58be420`](99b58be420/) | **The Five Levels: From Spicy Autocomplete to the Software Factory (Dan Shapiro)** | [Source URL](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory) | [Local Source](99b58be420/c62a32953d_danshapiro.com__blog__2026__01__the-five-levels-from-spicy-autocomplete-to-the-s.html) | html ✓ · md ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/01-shapiro-five-levels.md`](../research/followup/01-shapiro-five-levels.md) *(3)* |
| <a id="11086c2305"></a>[`11086c2305`](11086c2305/) | **The Road Runner Economy (Noah Radford)** | [Source URL](https://nraford7.github.io/road-runner-economy) | — | *(none registered)* | [`research/followup/01-shapiro-five-levels.md`](../research/followup/01-shapiro-five-levels.md) *(1)* |
| <a id="44d4c1be80"></a>[`44d4c1be80`](44d4c1be80/) | **The Software Factory** | [Source URL](https://lukepm.com/blog/the-software-factory) | [Local Source](44d4c1be80/The%20Software%20Factory%20_%20LukePM.com.txt) | txt ✓ | — |
| <a id="400f0c3c0a"></a>[`400f0c3c0a`](400f0c3c0a/) | **The Software Factory: When No Human Writes or Reviews the Code** | [Source URL](https://www.thepragmaticcto.com/p/the-software-factory-when-no-human) | [Local Source](400f0c3c0a/cb3fefb852_www.thepragmaticcto.com__p__the-software-factory-when-no-human.html) | html ✓ · md ✓ | — |
| <a id="4d0de0d106"></a>[`4d0de0d106`](4d0de0d106/) | **Tracker — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/tracker) | [Local Source](4d0de0d106/Tracker%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="97f2036966"></a>[`97f2036966`](97f2036966/) | **Untitled Webflow-hosted PDF (no /Title metadata)** | [Source URL](https://cdn.prod.website-files.com/655cded084fee2e958faaffc/69b8331d6141dc7278866f9c_D) | [Local Source](97f2036966/1af176f305_cdn.prod.website-files.com__655cded084fee2e958faaffc__69b8331d6141dc7278866f9c_D.html) | html ✓ · md ✓ | — |
| <a id="d9e1bd997d"></a>[`d9e1bd997d`](d9e1bd997d/) | **When AI Agents Write Your Code, Does Language Choice Matter?** | [Source URL](https://www.thepragmaticcto.com/p/when-ai-agents-write-your-code-does) | [Local Source](d9e1bd997d/When%20AI%20Agents%20Write%20Your%20Code%2C%20Does%20Language%20Choice%20Matter_.txt) | txt ✓ | [`research/33-language-choice-as-harness.md`](../research/33-language-choice-as-harness.md) *(1)* |
| <a id="60fbea1689"></a>[`60fbea1689`](60fbea1689/) | **William El Kaim — About (Medium)** | [Source URL](https://medium.com/@welkaim/about) | [Local Source](60fbea1689/medium.com-welkaim-about.txt) | txt ✓ · html ✓ · html ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(1)* |
| <a id="7dbf96d872"></a>[`7dbf96d872`](7dbf96d872/) | **William El Kaim — Medium** | [Source URL](https://welkaim.medium.com/) | [Local Source](7dbf96d872/welkaim.medium.com) | other ✓ · html ✓ · html ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(1)* |

</details>

<a id="cat-intent-driven-architecture"></a>

<details>
<summary><b>intent-driven-architecture</b> — 9 records — <em>Intent-driven / continuous enterprise architecture, RISE-style automation, product-line variability.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="8c295c7ecf"></a>[`8c295c7ecf`](8c295c7ecf/) | **El Kaim Book — Chapter 1: The Limits of Traditional Enterprise Architecture** | — | [Local Source](8c295c7ecf/Chapter%201%20The%20Limits%20of%20Traditional.txt) | txt ✓ | — |
| <a id="12ddb278e4"></a>[`12ddb278e4`](12ddb278e4/) | **El Kaim Book — Chapter 2: Continuous Enterprise Architecture** | — | [Local Source](12ddb278e4/Chapter%202%20Continuous%20Enterprise%20Arc.txt) | txt ✓ | — |
| <a id="c94a94f2d3"></a>[`c94a94f2d3`](c94a94f2d3/) | **El Kaim Book — Chapter 3: Intent-Driven Architecture** | — | [Local Source](c94a94f2d3/Chapter%203%20Intent-Driven%20Architectur.txt) | txt ✓ | — |
| <a id="a37637a130"></a>[`a37637a130`](a37637a130/) | **El Kaim Book — Chapter 4: Why AI and Automation Change Everything** | — | [Local Source](a37637a130/Chapter%204%20Why%20AI%20and%20Automation%20Cha.txt) | txt ✓ | — |
| <a id="9e3537481f"></a>[`9e3537481f`](9e3537481f/) | **El Kaim Book — Chapter 5: Automating RISE with SAP** | — | [Local Source](9e3537481f/Chapter%205%20Automating%20RISE%20with%20SAP.txt) | txt ✓ | — |
| <a id="49a055f96d"></a>[`49a055f96d`](49a055f96d/) | **El Kaim Book — Chapter 6: The Enterprise Architecture Function** | — | [Local Source](49a055f96d/Chapter%206%20The%20Enterprise%20Architectu.txt) | txt ✓ | — |
| <a id="e78ab8b5d2"></a>[`e78ab8b5d2`](e78ab8b5d2/) | **El Kaim Book — Chapter 7: Automating Enterprise Architecture** | — | [Local Source](e78ab8b5d2/Chapter%207%20Automating%20Enterprise%20Arc.txt) | txt ✓ | — |
| <a id="b59dfbed79"></a>[`b59dfbed79`](b59dfbed79/) | **El Kaim Book — Chapter 8: From Intent to Specification** | — | [Local Source](b59dfbed79/Chapter%208%20From%20Intent%20to%20Specificat.txt) | txt ✓ | — |
| <a id="f52a2d4098"></a>[`f52a2d4098`](f52a2d4098/) | **El Kaim Book — Chapter 9: Software Product Line and Variability** | — | [Local Source](f52a2d4098/Chapter%209%20Software%20Product%20Line%20and.txt) | txt ✓ | — |

</details>

<a id="cat-spec-authorship"></a>

<details>
<summary><b>spec-authorship</b> — 4 records — <em>Requirements engineering, BMAD, scenario testing, INCOSE primer, spec-as-prompt practice.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="34b7fdd99d"></a>[`34b7fdd99d`](34b7fdd99d/) | **Requirements Writing Guide \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/opinions/requirements-writing-guide) | [Local Source](34b7fdd99d/Requirements%20Writing%20Guide%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="95265c651d"></a>[`95265c651d`](95265c651d/) | **Spec-driven development: The AI engineering workflow (Lenny's Newsletter)** | [Source URL](https://www.lennysnewsletter.com/p/spec-driven-development-the-ai-engineering) | [Local Source](95265c651d/lenny-spec-driven-development.txt) | txt ✓ | [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../research/35-lenny-howiai-spec-driven-and-team-ops.md) *(1)* |
| <a id="3592091691"></a>[`3592091691`](3592091691/) | **Specification-Driven Agentic Development System: A Methodology for Iterative Specification Refinement Using AI Agents**<br><em>User-authored layered-spec / 5-failure-mode / revelation-cycle methodology</em> | [Source URL](https://github.com/jonathanmanton) | [Local Source](3592091691/spec-driven-ai-dev.md) | md ✓ | — |
| <a id="292ea05299"></a>[`292ea05299`](292ea05299/) | **Work Order Writing Guide \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/opinions/work-order-writing-guide) | [Local Source](292ea05299/Work%20Order%20Writing%20Guide%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |

</details>

<a id="cat-willison-canon"></a>

<details>
<summary><b>willison-canon</b> — 26 records — <em>Simon Willison's collected writings + interviews.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="08be49ea7d"></a>[`08be49ea7d`](08be49ea7d/) | **Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns) | [Local Source](08be49ea7d/simonwillison.net__guides__agentic-engineering-patterns.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) · [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) *(2)* |
| <a id="2263d13b18"></a>[`2263d13b18`](2263d13b18/) | **Agentic manual testing - Agentic Engineering Patterns** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing) | [Local Source](2263d13b18/simonwillison.net__guides__agentic-engineering-patterns__agentic-manual-testing.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="23efb53da9"></a>[`23efb53da9`](23efb53da9/) | **Agents are models using tools in a loop** | [Source URL](https://simonwillison.net/2025/May/22/tools-in-a-loop) | [Local Source](23efb53da9/simonwillison.net__2025__May__22__tools-in-a-loop.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="f8007cc630"></a>[`f8007cc630`](f8007cc630/) | **An AI State of the Union \| Simon Willison (Lenny's Newsletter)** | [Source URL](https://www.lennysnewsletter.com/p/an-ai-state-of-the-union) | [Local Source](f8007cc630/www.lennysnewsletter.com__p__an-ai-state-of-the-union.html) | html ✓ · html ✓ · txt ✓ · txt ✓ · md ✓ · txt ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) *(1)* |
| <a id="86f58b89a9"></a>[`86f58b89a9`](86f58b89a9/) | **Anti-patterns: things to avoid - Agentic Engineering Patterns** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns) | [Local Source](86f58b89a9/simonwillison.net__guides__agentic-engineering-patterns__anti-patterns.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="cad3fa5db1"></a>[`cad3fa5db1`](cad3fa5db1/) | **Claude Code: Best practices for agentic coding** | [Source URL](https://simonwillison.net/2025/Apr/19/claude-code-best-practices) | [Local Source](cad3fa5db1/simonwillison.net__2025__Apr__19__claude-code-best-practices.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="875b882ad1"></a>[`875b882ad1`](875b882ad1/) | **Designing agentic loops** | [Source URL](https://simonwillison.net/2025/Sep/30/designing-agentic-loops) | [Local Source](875b882ad1/simonwillison.net__2025__Sep__30__designing-agentic-loops.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="1b74bb31e3"></a>[`1b74bb31e3`](1b74bb31e3/) | **Embracing the parallel coding agent lifestyle** | [Source URL](https://simonwillison.net/2025/Oct/5/parallel-coding-agents) | [Local Source](1b74bb31e3/simonwillison.net__2025__Oct__5__parallel-coding-agents.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="c6074ee6d6"></a>[`c6074ee6d6`](c6074ee6d6/) | **First run the tests - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests) | [Local Source](c6074ee6d6/simonwillison.net__guides__agentic-engineering-patterns__first-run-the-tests.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="4c98a39ea9"></a>[`4c98a39ea9`](4c98a39ea9/) | **Hoard things you know how to do - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do) | [Local Source](4c98a39ea9/simonwillison.net__guides__agentic-engineering-patterns__hoard-things-you-know-how-to-do.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="53b4490fe8"></a>[`53b4490fe8`](53b4490fe8/) | **How coding agents work - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work) | [Local Source](53b4490fe8/simonwillison.net__guides__agentic-engineering-patterns__how-coding-agents-work.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="303c8ff4e8"></a>[`303c8ff4e8`](303c8ff4e8/) | **How StrongDM's AI team build serious software without even looking at the code** | [Source URL](https://simonwillison.net/2026/Feb/7/software-factory) | [Local Source](303c8ff4e8/simonwillison.net__2026__Feb__7__software-factory.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) · [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(3)* |
| <a id="95ba3accbc"></a>[`95ba3accbc`](95ba3accbc/) | **I think "agent" may finally have a widely enough agreed upon definition to be useful jargon now** | [Source URL](https://simonwillison.net/2025/Sep/18/agents) | [Local Source](95ba3accbc/simonwillison.net__2025__Sep__18__agents.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="dbc37326e4"></a>[`dbc37326e4`](dbc37326e4/) | **Interactive explanations - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations) | [Local Source](dbc37326e4/simonwillison.net__guides__agentic-engineering-patterns__interactive-explanations.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="d95bf55a39"></a>[`d95bf55a39`](d95bf55a39/) | **Linear walkthroughs - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs) | [Local Source](d95bf55a39/simonwillison.net__guides__agentic-engineering-patterns__linear-walkthroughs.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="1e8169decc"></a>[`1e8169decc`](1e8169decc/) | **Prompts I use - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/prompts) | [Local Source](1e8169decc/simonwillison.net__guides__agentic-engineering-patterns__prompts.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="b4b5b2e638"></a>[`b4b5b2e638`](b4b5b2e638/) | **Red/green TDD - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd) | [Local Source](b4b5b2e638/simonwillison.net__guides__agentic-engineering-patterns__red-green-tdd.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) · [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) *(2)* |
| <a id="11ae110ddb"></a>[`11ae110ddb`](11ae110ddb/) | **Simon Willison on agentic-engineering** | [Source URL](https://simonwillison.net/tags/agentic-engineering) | [Local Source](11ae110ddb/simonwillison.net__tags__agentic-engineering.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="67dfba1ed6"></a>[`67dfba1ed6`](67dfba1ed6/) | **Simon Willison on evals** | [Source URL](https://simonwillison.net/tags/evals) | [Local Source](67dfba1ed6/simonwillison.net__tags__evals.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="53ed6e363d"></a>[`53ed6e363d`](53ed6e363d/) | **Simon Willison — CaMeL paper writeup**<br><em>Willison summary of the CaMeL prompt-injection defense paper</em> | [Source URL](https://simonwillison.net/2025/Apr/11/camel) | [Local Source](53ed6e363d/2ab9a1ab38_simonwillison.net__2025__Apr__11__camel.html) | html ✓ · md ✓ · mhtml ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/followup/08-security-primitives.md`](../research/followup/08-security-primitives.md) *(2)* |
| <a id="3262892c6c"></a>[`3262892c6c`](3262892c6c/) | **Subagents - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/subagents) | [Local Source](3262892c6c/simonwillison.net__guides__agentic-engineering-patterns__subagents.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="9c9554d27e"></a>[`9c9554d27e`](9c9554d27e/) | **The lethal trifecta for AI agents: private data, untrusted content, and external communication** | [Source URL](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta) | [Local Source](9c9554d27e/65eac5afb6_simonwillison.net__2025__Jun__16__the-lethal-trifecta.html) | html ✓ · md ✓ · mhtml ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/followup/08-security-primitives.md`](../research/followup/08-security-primitives.md) *(2)* |
| <a id="a811ab37e6"></a>[`a811ab37e6`](a811ab37e6/) | **Vibe coding and agentic engineering are getting closer than I'd like** | [Source URL](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering) | [Local Source](a811ab37e6/simonwillison.net__2026__May__6__vibe-coding-and-agentic-engineering.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="4ccc7d8083"></a>[`4ccc7d8083`](4ccc7d8083/) | **What is agentic engineering? - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering) | [Local Source](4ccc7d8083/simonwillison.net__guides__agentic-engineering-patterns__what-is-agentic-engineering.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="4d44956ef1"></a>[`4d44956ef1`](4d44956ef1/) | **Writing about Agentic Engineering Patterns** | [Source URL](https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns) | [Local Source](4d44956ef1/simonwillison.net__2026__Feb__23__agentic-engineering-patterns.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="470703acd9"></a>[`470703acd9`](470703acd9/) | **Writing code is cheap now - Agentic Engineering Patterns - Simon Willison's Weblog** | [Source URL](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap) | [Local Source](470703acd9/simonwillison.net__guides__agentic-engineering-patterns__code-is-cheap.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |

</details>

<a id="cat-compound-engineering"></a>

<details>
<summary><b>compound-engineering</b> — 11 records — <em>Compound-engineering workflows, personal harnesses, practitioner accounts (Klaassen / Reed / How I AI).</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="ac5b4f8018"></a>[`ac5b4f8018`](ac5b4f8018/) | **Build your own AI developer tools with Claude Code (How I AI, Lenny's Newsletter)** | [Source URL](https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build) | [Local Source](ac5b4f8018/lenny-build-your-own-ai-developer-tools-with-claude-code.txt) | txt ✓ | [`research/34-lenny-howiai-personal-harnesses.md`](../research/34-lenny-howiai-personal-harnesses.md) *(1)* |
| <a id="4b1f62e4fc"></a>[`4b1f62e4fc`](4b1f62e4fc/) | **Compound Engineering** | [Source URL](https://every.to/guides/compound-engineering) | [Local Source](4b1f62e4fc/every.to__guides__compound-engineering.html) | html ✓ · txt ✓ | [`research/03-every-compound-engineering.md`](../research/03-every-compound-engineering.md) · [`research/followup/05-klaassen-siblings.md`](../research/followup/05-klaassen-siblings.md) *(2)* |
| <a id="8fa24c4cd3"></a>[`8fa24c4cd3`](8fa24c4cd3/) | **Compound Engineering: How Every Codes With Agents** | [Source URL](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents) | [Local Source](8fa24c4cd3/every.to__chain-of-thought__compound-engineering-how-every-codes-with-agents.html) | html ✓ · txt ✓ | [`research/03-every-compound-engineering.md`](../research/03-every-compound-engineering.md) · [`research/followup/05-klaassen-siblings.md`](../research/followup/05-klaassen-siblings.md) *(2)* |
| <a id="67b1f7d3a3"></a>[`67b1f7d3a3`](67b1f7d3a3/) | **Culture of AI Engineering** | [Source URL](https://every.to/source-code/the-culture-of-ai-engineering) | [Local Source](67b1f7d3a3/brier-culture-of-ai-engineering.txt) | txt ✓ | — |
| <a id="a747576e0f"></a>[`a747576e0f`](a747576e0f/) | **How I AI: CJ Hess on Building Custom AI Tools (Lenny's Newsletter)** | [Source URL](https://www.lennysnewsletter.com/p/how-i-ai-cj-hess) | [Local Source](a747576e0f/How%20I%20AI%20CJ%20Hess%20on%20Building%20Custom.txt) | txt ✓ | — |
| <a id="b0d89f5419"></a>[`b0d89f5419`](b0d89f5419/) | **How to Work and Compound with AI** | [Source URL](https://eugeneyan.com/writing/working-with-ai) | [Local Source](b0d89f5419/How%20to%20Work%20and%20Compound%20with%20AI.mhtml) | mhtml ✓ | — |
| <a id="243a228bd1"></a>[`243a228bd1`](243a228bd1/) | **My AI Had Already Fixed the Code Before I Saw It** | [Source URL](https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it) | [Local Source](243a228bd1/cb749911cb_every.to__source-code__my-ai-had-already-fixed-the-code-before-i-saw-it.html) | html ✓ · html ✓ · txt ✓ · txt ✓ | [`research/03-every-compound-engineering.md`](../research/03-every-compound-engineering.md) *(1)* |
| <a id="516e66f9f7"></a>[`516e66f9f7`](516e66f9f7/) | **Quests, token leaderboards, and a skills marketplace: The elite AI adoption playbook \| John Kim (Sendbird)** | [Source URL](https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation) | [Local Source](516e66f9f7/Quests%20token%20leaderboards%20and%20a%20s.txt) | txt ✓ | [`research/36-sendbird-quests-token-tiers.md`](../research/36-sendbird-quests-token-tiers.md) *(1)* |
| <a id="95265c651d"></a>[`95265c651d`](95265c651d/) | **Spec-driven development: The AI engineering workflow (Lenny's Newsletter)** | [Source URL](https://www.lennysnewsletter.com/p/spec-driven-development-the-ai-engineering) | [Local Source](95265c651d/lenny-spec-driven-development.txt) | txt ✓ | [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../research/35-lenny-howiai-spec-driven-and-team-ops.md) *(1)* |
| <a id="5b2ed8c57e"></a>[`5b2ed8c57e`](5b2ed8c57e/) | **Spec-driven development: The AI engineering workflow at Notion \| Ryan Nystrom** | [Source URL](https://www.chatprd.ai/how-i-ai/ryan-nystrom-notion-workflows-for-engineering-velocity) | [Local Source](5b2ed8c57e/The%20AI%20engineering%20workflow%20at%20Noti.txt) | txt ✓ | [`research/35-lenny-howiai-spec-driven-and-team-ops.md`](../research/35-lenny-howiai-spec-driven-and-team-ops.md) *(1)* |
| <a id="0ee794b3a3"></a>[`0ee794b3a3`](0ee794b3a3/) | **The Agent That Saved My Brain** | [Source URL](https://every.to/p/the-agent-that-saved-my-brain) | [Local Source](0ee794b3a3/every.to__p__the-agent-that-saved-my-brain.html) | html ✓ · txt ✓ | [`research/03-every-compound-engineering.md`](../research/03-every-compound-engineering.md) *(1)* |

</details>

<a id="cat-anthropic-substrate"></a>

<details>
<summary><b>anthropic-substrate</b> — 10 records — <em>Claude Code substrate, Anthropic engineering posts, Cherny interviews.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="a3afc1e8c7"></a>[`a3afc1e8c7`](a3afc1e8c7/) | **(unknown)** | [Source URL](https://www.anthropic.com/engineering/multi-agent-research-system) | [Local Source](a3afc1e8c7/37ed91c908_www.anthropic.com__engineering__multi-agent-research-system.html) | html ✓ · md ✓ | [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(1)* |
| <a id="bdba59d7ee"></a>[`bdba59d7ee`](bdba59d7ee/) | **Agent Skills — Best Practices (Claude docs)** | [Source URL](https://platform.claude.com/docs/en/agent-skills/best-practices) | [Local Source](bdba59d7ee/f789a44863_platform.claude.com__docs__en__agent-skills__best-practices.html) | html ✓ · md ✓ | — |
| <a id="9d696416cb"></a>[`9d696416cb`](9d696416cb/) | **Anthropic Agent Skills — Overview (Platform docs)** | [Source URL](https://platform.claude.com/docs/en/agent-skills/overview) | [Local Source](9d696416cb/platform-claude-com-agent-skills-overview.txt) | txt ✓ | — |
| <a id="ac5b4f8018"></a>[`ac5b4f8018`](ac5b4f8018/) | **Build your own AI developer tools with Claude Code (How I AI, Lenny's Newsletter)** | [Source URL](https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build) | [Local Source](ac5b4f8018/lenny-build-your-own-ai-developer-tools-with-claude-code.txt) | txt ✓ | [`research/34-lenny-howiai-personal-harnesses.md`](../research/34-lenny-howiai-personal-harnesses.md) *(1)* |
| <a id="ffc229d838"></a>[`ffc229d838`](ffc229d838/) | **Building Effective Agents**<br><em>Anthropic engineering — orchestrator-worker, evaluator-optimizer, augmented LLM patterns</em> | [Source URL](https://www.anthropic.com/engineering/building-effective-agents) | [Local Source](ffc229d838/7d24e5faa2_www.anthropic.com__engineering__building-effective-agents.html) | html ✓ · md ✓ | — |
| <a id="cad3fa5db1"></a>[`cad3fa5db1`](cad3fa5db1/) | **Claude Code: Best practices for agentic coding** | [Source URL](https://simonwillison.net/2025/Apr/19/claude-code-best-practices) | [Local Source](cad3fa5db1/simonwillison.net__2025__Apr__19__claude-code-best-practices.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="586cb02137"></a>[`586cb02137`](586cb02137/) | **Head of Claude Code: What happens when AI does 90% of the coding** | [Source URL](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens) | [Local Source](586cb02137/9f57e8bf80_www.lennysnewsletter.com__p__head-of-claude-code-what-happens.html) | html ✓ · txt ✓ · txt ✓ · txt ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/followup/03-cherny-interview.md`](../research/followup/03-cherny-interview.md) *(2)* |
| <a id="ee885bfc4c"></a>[`ee885bfc4c`](ee885bfc4c/) | **Skill authoring best practices - Claude API Docs** | [Source URL](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | [Local Source](ee885bfc4c/Skill%20authoring%20best%20practices%20-%20Claude%20API%20Docs.mhtml) | mhtml ✓ | — |
| <a id="26035151aa"></a>[`26035151aa`](26035151aa/) | **The Complete Guide to Building Skills for Claude** | [Source URL](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | [Local Source](26035151aa/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | pdf ✓ | — |
| <a id="3643d46af4"></a>[`3643d46af4`](3643d46af4/) | **What are Skills? (Anthropic support)** | [Source URL](https://support.claude.com/en/articles/what-are-skills) | [Local Source](3643d46af4/support-claude-com-what-are-skills.txt) | txt ✓ | — |

</details>

<a id="cat-openai-substrate"></a>

<details>
<summary><b>openai-substrate</b> — 8 records — <em>Codex substrate, OpenAI cookbook, running-codex-safely docs.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="dccefbfc62"></a>[`dccefbfc62`](dccefbfc62/) | **=?utf-8?Q?Agent=20approvals=20&=20security=20=E2=80=93=20Codex=20\|=20Open?=** | [Source URL](https://developers.openai.com/codex/agent-approvals-security) | [Local Source](dccefbfc62/ed3b262d33_developers.openai.com__codex__agent-approvals-security.html) | html ✓ · md ✓ · mhtml ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="175cba9347"></a>[`175cba9347`](175cba9347/) | **=?utf-8?Q?Custom=20instructions=20with=20AGENTS.md=20=E2=80=93=20Codex=20?=** | [Source URL](https://developers.openai.com/codex/guides/agents-md) | [Local Source](175cba9347/77457a7169_developers.openai.com__codex__guides__agents-md.html) | html ✓ · md ✓ · mhtml ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="8334be0240"></a>[`8334be0240`](8334be0240/) | **=?utf-8?Q?Subagents=20=E2=80=93=20Codex=20\|=20OpenAI=20Developers?=** | [Source URL](https://developers.openai.com/codex/subagents) | [Local Source](8334be0240/d179e7b09d_developers.openai.com__codex__subagents.html) | html ✓ · md ✓ · mhtml ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="f6b9330226"></a>[`f6b9330226`](f6b9330226/) | **Harness engineering: leveraging Codex in an agent-first world** | [Source URL](https://openai.com/index/harness-engineering) | [Local Source](f6b9330226/Harness%20engineering_%20leveraging%20Codex%20in%20an%20agent-first%20world%20_%20OpenAI.txt) | txt ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="10b59b402b"></a>[`10b59b402b`](10b59b402b/) | **Introducing SWE-bench Verified** | [Source URL](https://openai.com/index/introducing-swe-bench-verified) | [Local Source](10b59b402b/Introducing%20SWE-bench%20Verified%20_%20OpenAI.txt) | txt ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="c35a5146b7"></a>[`c35a5146b7`](c35a5146b7/) | **Rules – Codex \| OpenAI Developers** | [Source URL](https://developers.openai.com/codex/rules) | [Local Source](c35a5146b7/Rules%20%E2%80%93%20Codex%20_%20OpenAI%20Developers.txt) | txt ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="66be122077"></a>[`66be122077`](66be122077/) | **Running Codex safely at OpenAI** | [Source URL](https://openai.com/index/running-codex-safely) | [Local Source](66be122077/Running%20Codex%20safely%20at%20OpenAI%20_%20OpenAI.txt) | txt ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="e205ffac9d"></a>[`e205ffac9d`](e205ffac9d/) | **Unlocking the Codex harness: how we built the App Server** | [Source URL](https://openai.com/index/unlocking-the-codex-harness) | [Local Source](e205ffac9d/Unlocking%20the%20Codex%20harness_%20how%20we%20built%20the%20App%20Server%20_%20OpenAI.txt) | txt ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |

</details>

<a id="cat-other-vendor-substrate"></a>

<details>
<summary><b>other-vendor-substrate</b> — 75 records — <em>GitHub Copilot, Replit Agent, Devin, Factory.ai, Tabnine, OpenHands, etc.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="43e68409a4"></a>[`43e68409a4`](43e68409a4/) | **2389-research/coven: Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming** | [Source URL](https://github.com/2389-research/coven) | [Local Source](43e68409a4/2389-research_coven_%20Rust%20platform%20for%20orchestrating%20AI%20agents%20with%20tool%20capabilities%20and%20gRPC%20streaming.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="42500eb134"></a>[`42500eb134`](42500eb134/) | **2389-research/dotpowers: a superpowers implementation for attractors** | [Source URL](https://github.com/2389-research/dotpowers) | [Local Source](42500eb134/2389-research_dotpowers_%20a%20superpowers%20implementation%20for%20attractors.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(3)* |
| <a id="c317a03b84"></a>[`c317a03b84`](c317a03b84/) | **2389-research/mammoth** | [Source URL](https://github.com/2389-research/mammoth) | [Local Source](c317a03b84/2389-research_mammoth.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="8f251bd57a"></a>[`8f251bd57a`](8f251bd57a/) | **2389-research/smasher: A builder** | [Source URL](https://github.com/2389-ai/smasher) | [Local Source](8f251bd57a/2389-research_smasher_%20A%20builder.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="f79769ac6c"></a>[`f79769ac6c`](f79769ac6c/) | **2389-research/tracker** | [Source URL](https://github.com/2389-research/tracker) | [Local Source](f79769ac6c/2389-research_tracker.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="5c785e88b3"></a>[`5c785e88b3`](5c785e88b3/) | **404 - GitHub Docs** | [Source URL](https://docs.github.com/en/copilot/concepts/agents/about-coding-agent) | [Local Source](5c785e88b3/04f58c2152_docs.github.com__en__copilot__concepts__agents__about-coding-agent.html) | html ✓ | — |
| <a id="85cdf07ac2"></a>[`85cdf07ac2`](85cdf07ac2/) | **8090 Inc Blog** | [Source URL](https://www.8090.inc/blog) | [Local Source](85cdf07ac2/c2eb1a9d1b_www.8090.inc__blog.html) | html ✓ | — |
| <a id="5cc5a296b6"></a>[`5cc5a296b6`](5cc5a296b6/) | **=?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Agent=203:=20Our=20Most=20Au?=** | [Source URL](https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet) | [Local Source](5cc5a296b6/e1dffb38b4_blog.replit.com__introducing-agent-3-our-most-autonomous-agent-yet.html) | html ✓ · md ✓ · mhtml ✓ | [`research/20-replit-agent.md`](../research/20-replit-agent.md) *(1)* |
| <a id="73dc7199ce"></a>[`73dc7199ce`](73dc7199ce/) | **=?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Replit=20Agent=204:=20Built?=** | [Source URL](https://blog.replit.com/introducing-agent-4-built-for-creativity) | [Local Source](73dc7199ce/ff906146e8_blog.replit.com__introducing-agent-4-built-for-creativity.html) | html ✓ · md ✓ · mhtml ✓ | [`research/20-replit-agent.md`](../research/20-replit-agent.md) *(1)* |
| <a id="23b7d51d69"></a>[`23b7d51d69`](23b7d51d69/) | **[2511.03690] The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents** | [Source URL](https://arxiv.org/abs/2511.03690) | [Local Source](23b7d51d69/7342918a91_arxiv.org__abs__2511.03690.html) | html ✓ · md ✓ | [`research/11-openhands-substrate-audit.md`](../research/11-openhands-substrate-audit.md) *(1)* |
| <a id="2e49bcd671"></a>[`2e49bcd671`](2e49bcd671/) | **About assigning tasks to Copilot (file contains saved 2389-research/dotpowers GitHub page instead)** | [Source URL](https://docs.github.com/en/copilot/how-tos/agents/about-assigning-tasks-to-copilot) | [Local Source](2e49bcd671/7c5f3e46f0_docs.github.com__en__copilot__how-tos__agents__about-assigning-tasks-to-copilot.html) | html ✓ | — |
| <a id="991f3bf0f6"></a>[`991f3bf0f6`](991f3bf0f6/) | **About Copilot Workspace (GitHub Docs)** | [Source URL](https://docs.github.com/en/copilot/copilot-workspace/about-copilot-workspace) | — | html (skip) | [`research/19-github-copilot-cloud-agent.md`](../research/19-github-copilot-cloud-agent.md) *(1)* |
| <a id="325d8c1018"></a>[`325d8c1018`](325d8c1018/) | **About extensions for Copilot (capture is a PNG image, not the docs page)** | [Source URL](https://docs.github.com/en/copilot/concepts/copilot-extensions/about-extensions-for) | [Local Source](325d8c1018/676c1dcdf1_docs.github.com__en__copilot__concepts__copilot-extensions__about-extensions-for.html) | html ✓ | — |
| <a id="ebc17186b3"></a>[`ebc17186b3`](ebc17186b3/) | **About GitHub Copilot cloud agent - GitHub Docs** | [Source URL](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) | [Local Source](ebc17186b3/About%20GitHub%20Copilot%20cloud%20agent%20-%20GitHub%20Docs.mhtml) | mhtml ✓ | [`research/19-github-copilot-cloud-agent.md`](../research/19-github-copilot-cloud-agent.md) *(1)* |
| <a id="1b03040a1b"></a>[`1b03040a1b`](1b03040a1b/) | **Agent Guidelines \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/agent-guidelines) | [Local Source](1b03040a1b/66f27b480b_docs.tabnine.com__main__administering-tabnine__managing-your-team__settings__age.html) | html ✓ · md ✓ | — |
| <a id="8962e872bd"></a>[`8962e872bd`](8962e872bd/) | **Agentic Engineering (IBM Think Topics)** | [Source URL](https://www.ibm.com/think/topics/agentic-engineering) | [Local Source](8962e872bd/ab2e549306_www.ibm.com__think__topics__agentic-engineering.html) | html ✓ · md ✓ | [`research/12-adjacent-ecosystem.md`](../research/12-adjacent-ecosystem.md) *(1)* |
| <a id="39405fa555"></a>[`39405fa555`](39405fa555/) | **Agentic Engineering: Redefining Software Engineering (LangChain)** | [Source URL](https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering) | [Local Source](39405fa555/9ae3d72c5a_www.langchain.com__blog__agentic-engineering-redefining-software-engineering.html) | html ✓ · md ✓ | [`research/12-adjacent-ecosystem.md`](../research/12-adjacent-ecosystem.md) *(1)* |
| <a id="f313f7845c"></a>[`f313f7845c`](f313f7845c/) | **Artifacts \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/raw-materials/artifacts) | [Local Source](f313f7845c/Artifacts%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="83fcd19c73"></a>[`83fcd19c73`](83fcd19c73/) | **Blueprint Writing Guide \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/opinions/blueprint-writing-guide) | [Local Source](83fcd19c73/Blueprint%20Writing%20Guide%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="e36b18df01"></a>[`e36b18df01`](e36b18df01/) | **Blueprints \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/modules/blueprints) | [Local Source](e36b18df01/Blueprints%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="dcc5c900a1"></a>[`dcc5c900a1`](dcc5c900a1/) | **Changelog \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/resources/changelog) | [Local Source](dcc5c900a1/Changelog%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="8e651f5fda"></a>[`8e651f5fda`](8e651f5fda/) | **Coaching Guidelines \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/getting-started/context-engine/admin-console/coaching) | [Local Source](8e651f5fda/90835867bb_docs.tabnine.com__main__getting-started__context-engine__admin-console__coaching.html) | html ✓ · md ✓ | — |
| <a id="d9aa0e7ad5"></a>[`d9aa0e7ad5`](d9aa0e7ad5/) | **Codebase Connection \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/raw-materials/codebase) | [Local Source](d9aa0e7ad5/Codebase%20Connection%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="54629e12fe"></a>[`54629e12fe`](54629e12fe/) | **Context Engine \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/getting-started/context-engine) | [Local Source](54629e12fe/c11b58a296_docs.tabnine.com__main__getting-started__context-engine.html) | html ✓ · md ✓ | — |
| <a id="708f29cb35"></a>[`708f29cb35`](708f29cb35/) | **Coven — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/coven) | [Local Source](708f29cb35/Coven%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="265e444ae9"></a>[`265e444ae9`](265e444ae9/) | **Deployment Options \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/welcome/readme/architecture/deployment-options) | [Local Source](265e444ae9/c099219973_docs.tabnine.com__main__welcome__readme__architecture__deployment-options.html) | html ✓ · md ✓ | — |
| <a id="3274cc670c"></a>[`3274cc670c`](3274cc670c/) | **Devin (Cognition AI)** | [Source URL](https://www.cognition.ai/blog/devin) | [Local Source](3274cc670c/461d7478ae_www.cognition.ai__blog__devin.html) | html ✓ | — |
| <a id="f908e4d494"></a>[`f908e4d494`](f908e4d494/) | **dotpowers — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/dotpowers) | [Local Source](f908e4d494/dotpowers%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="fe423b2a50"></a>[`fe423b2a50`](fe423b2a50/) | **dotpowers/dotpowers.dot at main · 2389-research/dotpowers** | [Source URL](https://github.com/2389-research/dotpowers/blob/main/dotpowers.dot) | [Local Source](fe423b2a50/dotpowers_dotpowers.dot%20at%20main%20%C2%B7%202389-research_dotpowers.txt) | txt ✓ | [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) *(1)* |
| <a id="b2e8ea6df7"></a>[`b2e8ea6df7`](b2e8ea6df7/) | **Factory (StrongDM) — Attractor** | [Source URL](https://factory.strongdm.ai/products/attractor) | [Local Source](b2e8ea6df7/factory.strongdm.ai__products__attractor.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) *(3)* |
| <a id="d93e59de67"></a>[`d93e59de67`](d93e59de67/) | **Factory (StrongDM) — CXDB** | [Source URL](https://factory.strongdm.ai/products/cxdb) | [Local Source](d93e59de67/factory.strongdm.ai__products__cxdb.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="f2abe271f9"></a>[`f2abe271f9`](f2abe271f9/) | **Factory (StrongDM) — DTU** | [Source URL](https://factory.strongdm.ai/techniques/dtu) | [Local Source](f2abe271f9/factory.strongdm.ai__techniques__dtu.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="1f8e6329d5"></a>[`1f8e6329d5`](1f8e6329d5/) | **Factory (StrongDM) — Gene Transfusion** | [Source URL](https://factory.strongdm.ai/techniques/gene-transfusion) | [Local Source](1f8e6329d5/factory.strongdm.ai__techniques__gene-transfusion.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="6e7fbc4124"></a>[`6e7fbc4124`](6e7fbc4124/) | **Factory (StrongDM) — Home** | [Source URL](https://factory.strongdm.ai/) | [Local Source](6e7fbc4124/factory.strongdm.ai.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/03-every-compound-engineering.md`](../research/03-every-compound-engineering.md) · [`research/05-simon-willison.md`](../research/05-simon-willison.md) · [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(+1 more)* *(6)* |
| <a id="a1032841ba"></a>[`a1032841ba`](a1032841ba/) | **Factory (StrongDM) — Principles** | [Source URL](https://factory.strongdm.ai/principles) | [Local Source](a1032841ba/factory.strongdm.ai__principles.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(2)* |
| <a id="b7e946fa1b"></a>[`b7e946fa1b`](b7e946fa1b/) | **Factory (StrongDM) — Products** | [Source URL](https://factory.strongdm.ai/products) | [Local Source](b7e946fa1b/factory.strongdm.ai__products.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="2e46f64134"></a>[`2e46f64134`](2e46f64134/) | **Factory (StrongDM) — Pyramid Summaries** | [Source URL](https://factory.strongdm.ai/techniques/pyramid-summaries) | [Local Source](2e46f64134/factory.strongdm.ai__techniques__pyramid-summaries.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="76447f23b5"></a>[`76447f23b5`](76447f23b5/) | **Factory (StrongDM) — Semport** | [Source URL](https://factory.strongdm.ai/techniques/semport) | [Local Source](76447f23b5/factory.strongdm.ai__techniques__semport.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) *(1)* |
| <a id="39c9037a8c"></a>[`39c9037a8c`](39c9037a8c/) | **Factory (StrongDM) — Techniques** | [Source URL](https://factory.strongdm.ai/techniques) | [Local Source](39c9037a8c/factory.strongdm.ai__techniques.html) | html ✓ | [`research/01-strongdm-factory.md`](../research/01-strongdm-factory.md) · [`research/07-dark-factory.md`](../research/07-dark-factory.md) *(2)* |
| <a id="109582ff1a"></a>[`109582ff1a`](109582ff1a/) | **Factory AI – Product** | [Source URL](https://www.factory.ai/product) | [Local Source](109582ff1a/d376d7dbe6_www.factory.ai__product.html) | html ✓ | — |
| <a id="c6f235b88d"></a>[`c6f235b88d`](c6f235b88d/) | **gascity (gastownhall) — Gas City repository** | [Source URL](https://github.com/gastownhall/gascity) | — | *(none registered)* | [`research/38-gas-systems-substrate.md`](../research/38-gas-systems-substrate.md) · [`research/followup/13-gas-city-deep-dive.md`](../research/followup/13-gas-city-deep-dive.md) *(2)* |
| <a id="d7921179bf"></a>[`d7921179bf`](d7921179bf/) | **gastown (gastownhall) — Gas Town repository** | [Source URL](https://github.com/gastownhall/gastown) | — | *(none registered)* | [`research/38-gas-systems-substrate.md`](../research/38-gas-systems-substrate.md) · [`research/followup/14-gas-town-deep-dive.md`](../research/followup/14-gas-town-deep-dive.md) *(2)* |
| <a id="974abcda96"></a>[`974abcda96`](974abcda96/) | **gastownhall/gascity issue #586** | [Source URL](https://github.com/gastownhall/gascity/issues/586) | — | *(none registered)* | [`research/followup/13-gas-city-deep-dive.md`](../research/followup/13-gas-city-deep-dive.md) *(1)* |
| <a id="5f4b04494f"></a>[`5f4b04494f`](5f4b04494f/) | **GitHub Actions CI/CD Pipeline \| All-Hands-AI/OpenHands \| DeepWiki** | [Source URL](https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes) | [Local Source](5f4b04494f/0397796935_deepwiki.com__All-Hands-AI__OpenHands__11.3-cli-and-deployment-modes.html) | html ✓ · md ✓ | [`research/11-openhands-substrate-audit.md`](../research/11-openhands-substrate-audit.md) · [`research/12-adjacent-ecosystem.md`](../research/12-adjacent-ecosystem.md) *(2)* |
| <a id="1069d4d757"></a>[`1069d4d757`](1069d4d757/) | **Guidelines \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/getting-started/tabnine-agent/guidelines) | [Local Source](1069d4d757/a6d57df443_docs.tabnine.com__main__getting-started__tabnine-agent__guidelines.html) | html ✓ · md ✓ | — |
| <a id="78717fec1f"></a>[`78717fec1f`](78717fec1f/) | **Headless Mode - OpenHands Docs** | [Source URL](https://docs.all-hands.dev/usage/how-to/headless-mode) | [Local Source](78717fec1f/c7fa1c9c87_docs.all-hands.dev__usage__how-to__headless-mode.html) | html ✓ · md ✓ | [`research/11-openhands-substrate-audit.md`](../research/11-openhands-substrate-audit.md) *(1)* |
| <a id="8778ec392c"></a>[`8778ec392c`](8778ec392c/) | **Introduction - OpenHands Docs** | [Source URL](https://docs.all-hands.dev/) | [Local Source](8778ec392c/3f22b50dcc_docs.all-hands.dev__.html) | html ✓ · md ✓ | [`research/11-openhands-substrate-audit.md`](../research/11-openhands-substrate-audit.md) *(1)* |
| <a id="9ad71cb019"></a>[`9ad71cb019`](9ad71cb019/) | **Introduction \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/general/introduction) | [Local Source](9ad71cb019/Introduction%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="af38d390c2"></a>[`af38d390c2`](af38d390c2/) | **Kiro** | [Source URL](https://kiro.dev/) | [Local Source](af38d390c2/7dbc434e46_kiro.dev__.html) | html ✓ · md ✓ | [`research/12-adjacent-ecosystem.md`](../research/12-adjacent-ecosystem.md) *(1)* |
| <a id="e7eab5a353"></a>[`e7eab5a353`](e7eab5a353/) | **Mammoth — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/mammoth) | [Local Source](e7eab5a353/Mammoth%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="b973e0e535"></a>[`b973e0e535`](b973e0e535/) | **Managing code scanning alerts (capture is a PNG image, not the docs page)** | [Source URL](https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts) | [Local Source](b973e0e535/dc284c4243_docs.github.com__en__code-security__code-scanning__managing-code-scanning-alerts.html) | html ✓ | — |
| <a id="8e89b0d8e5"></a>[`8e89b0d8e5`](8e89b0d8e5/) | **Migrating from Jira \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/opinions/jira-migration) | [Local Source](8e89b0d8e5/Migrating%20from%20Jira%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="a5209cf735"></a>[`a5209cf735`](a5209cf735/) | **OpenHands AI Action · Actions · GitHub Marketplace** | [Source URL](https://github.com/marketplace/actions/openhands-ai-action) | [Local Source](a5209cf735/910b8cc08e_github.com__marketplace__actions__openhands-ai-action.html) | html ✓ · md ✓ | [`research/11-openhands-substrate-audit.md`](../research/11-openhands-substrate-audit.md) *(1)* |
| <a id="d77d04c052"></a>[`d77d04c052`](d77d04c052/) | **Privacy \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/welcome/readme/privacy) | [Local Source](d77d04c052/0e83235cbd_docs.tabnine.com__main__welcome__readme__privacy.html) | html ✓ · md ✓ | — |
| <a id="271feb61a7"></a>[`271feb61a7`](271feb61a7/) | **Private Installation \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/administering-tabnine/private-installation) | [Local Source](271feb61a7/0fb7fa1792_docs.tabnine.com__main__administering-tabnine__private-installation.html) | html ✓ · md ✓ | — |
| <a id="bdb0d1357f"></a>[`bdb0d1357f`](bdb0d1357f/) | **Provenance and Attribution \| Tabnine Docs** | [Source URL](https://docs.tabnine.com/main/welcome/readme/protection/provenance-and-attribution) | [Local Source](bdb0d1357f/5ac91b779a_docs.tabnine.com__main__welcome__readme__protection__provenance-and-attribution.html) | html ✓ · md ✓ | — |
| <a id="607f6af312"></a>[`607f6af312`](607f6af312/) | **Quickstart \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/general/quickstart) | [Local Source](607f6af312/Quickstart%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="12d3cc73b8"></a>[`12d3cc73b8`](12d3cc73b8/) | **Replit — Introducing Replit App Monitoring** | [Source URL](https://blog.replit.com/app-monitoring) | [Local Source](12d3cc73b8/Replit%20%E2%80%94%20Introducing%20Replit%20App%20Monitoring.mhtml) | mhtml ✓ | [`research/20-replit-agent.md`](../research/20-replit-agent.md) *(1)* |
| <a id="34b7fdd99d"></a>[`34b7fdd99d`](34b7fdd99d/) | **Requirements Writing Guide \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/opinions/requirements-writing-guide) | [Local Source](34b7fdd99d/Requirements%20Writing%20Guide%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="f3e4b69e8c"></a>[`f3e4b69e8c`](f3e4b69e8c/) | **Requirements \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/modules/requirements) | [Local Source](f3e4b69e8c/Requirements%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="59d633b2c6"></a>[`59d633b2c6`](59d633b2c6/) | **Smasher — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/smasher) | [Local Source](59d633b2c6/Smasher%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="a03c2b3502"></a>[`a03c2b3502`](a03c2b3502/) | **Software Factory Roadmap 2026 — 8090** | [Source URL](https://www.8090.ai/docs/resources/roadmap) | [Local Source](a03c2b3502/software_factory_roadmap_8090.mmd) | other ✓ | — |
| <a id="e951bbc27e"></a>[`e951bbc27e`](e951bbc27e/) | **strongdm/attractorbench: NLSpec instruction following benchmark** | [Source URL](https://github.com/strongdm/attractorbench) | [Local Source](e951bbc27e/strongdm_attractorbench_%20NLSpec%20instruction%20following%20benchmark%20for%20https___factory.strongdm.ai_products_attractor.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(3)* |
| <a id="b5fc7f9df9"></a>[`b5fc7f9df9`](b5fc7f9df9/) | **Superconductor** | [Source URL](https://www.superconductor.com/) | [Local Source](b5fc7f9df9/9f8a2de096_www.superconductor.com__.html) | html ✓ · md ✓ | — |
| <a id="be4a3756f4"></a>[`be4a3756f4`](be4a3756f4/) | **SWE-agent documentation** | [Source URL](https://swe-agent.com/latest) | [Local Source](be4a3756f4/792a008f65_swe-agent.com__latest__.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="cd9714d14e"></a>[`cd9714d14e`](cd9714d14e/) | **SWE-agent: Agent-Computer Interfaces (ACI)** | [Source URL](https://swe-agent.com/latest/background/aci) | [Local Source](cd9714d14e/768037f6d2_swe-agent.com__latest__background__aci__.html) | html ✓ · md ✓ | — |
| <a id="5492497a11"></a>[`5492497a11`](5492497a11/) | **Tabnine Docs (Server Setup Guide)** | [Source URL](https://docs.tabnine.com/main/administering-tabnine/private-installation/server-setup-guide) | [Local Source](5492497a11/63a0647181_docs.tabnine.com__main__administering-tabnine__private-installation__server-setu.html) | html ✓ | — |
| <a id="dafe463e94"></a>[`dafe463e94`](dafe463e94/) | **Tabnine Docs (Tabnine's Private and Protect)** | [Source URL](https://docs.tabnine.com/main/welcome/readme/ai-models/tabnines-private-and-protect) | [Local Source](dafe463e94/e4d2aaccbf_docs.tabnine.com__main__welcome__readme__ai-models__tabnines-private-and-protect.html) | html ✓ | — |
| <a id="7c5da8e730"></a>[`7c5da8e730`](7c5da8e730/) | **The Dark Factory Is a .dot file — 2389 Research, Inc.** | [Source URL](https://2389.ai/posts/the-dark-factory-is-a-dot-file) | [Local Source](7c5da8e730/The%20Dark%20Factory%20Is%20a%20.dot%20file%20%E2%80%94%202389%20Research%2C%20Inc.mhtml) | mhtml ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/04-gastown-beads.md`](../research/followup/04-gastown-beads.md) *(3)* |
| <a id="1175dde05f"></a>[`1175dde05f`](1175dde05f/) | **The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents (arXiv 2511.03690 PDF)** | [Source URL](https://arxiv.org/pdf/2511.03690) | [Local Source](1175dde05f/2823d15a84_arxiv.org__pdf__2511.03690.html) | html ✓ · md ✓ | [`research/11-openhands-substrate-audit.md`](../research/11-openhands-substrate-audit.md) *(1)* |
| <a id="4d0de0d106"></a>[`4d0de0d106`](4d0de0d106/) | **Tracker — 2389 Research, Inc.** | [Source URL](https://2389.ai/products/tracker) | [Local Source](4d0de0d106/Tracker%20%E2%80%94%202389%20Research%2C%20Inc.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/followup/02-attractor-implementations.md`](../research/followup/02-attractor-implementations.md) *(2)* |
| <a id="8508964c2a"></a>[`8508964c2a`](8508964c2a/) | **Validator \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/modules/validator) | [Local Source](8508964c2a/Validator%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="a112fe3b90"></a>[`a112fe3b90`](a112fe3b90/) | **What is agentic coding? How it works and use cases \| Google Cloud** | [Source URL](https://cloud.google.com/discover/what-is-agentic-coding) | [Local Source](a112fe3b90/5d7510eda5_cloud.google.com__discover__what-is-agentic-coding.html) | html ✓ · md ✓ | [`research/12-adjacent-ecosystem.md`](../research/12-adjacent-ecosystem.md) *(1)* |
| <a id="292ea05299"></a>[`292ea05299`](292ea05299/) | **Work Order Writing Guide \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/opinions/work-order-writing-guide) | [Local Source](292ea05299/Work%20Order%20Writing%20Guide%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |
| <a id="2f73d1a742"></a>[`2f73d1a742`](2f73d1a742/) | **Work Orders \| Docs \| 8090** | [Source URL](https://www.8090.ai/docs/modules/work-orders) | [Local Source](2f73d1a742/Work%20Orders%20_%20Docs%20_%208090.mhtml) | mhtml ✓ | — |

</details>

<a id="cat-skills-composition"></a>

<details>
<summary><b>skills-composition</b> — 10 records — <em>Skills as a composition primitive — agentskills.io, Anthropic Agent Skills, MCP.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="1c3b30521c"></a>[`1c3b30521c`](1c3b30521c/) | **Agent Skills Cookbook 01 — Introduction** | [Source URL](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/01_skills_introduction.ipynb) | [Local Source](1c3b30521c/01_skills_introduction.ipynb) | ipynb ✓ | — |
| <a id="1f7e1ebaf3"></a>[`1f7e1ebaf3`](1f7e1ebaf3/) | **Agent Skills Cookbook 02 — Financial Applications** | [Source URL](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/02_skills_financial_applications.ipynb) | [Local Source](1f7e1ebaf3/02_skills_financial_applications.ipynb) | ipynb ✓ | — |
| <a id="b1b49c4c3d"></a>[`b1b49c4c3d`](b1b49c4c3d/) | **Agent Skills Cookbook 03 — Custom Development** | [Source URL](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/03_skills_custom_development.ipynb) | [Local Source](b1b49c4c3d/03_skills_custom_development.ipynb) | ipynb ✓ | — |
| <a id="bdba59d7ee"></a>[`bdba59d7ee`](bdba59d7ee/) | **Agent Skills — Best Practices (Claude docs)** | [Source URL](https://platform.claude.com/docs/en/agent-skills/best-practices) | [Local Source](bdba59d7ee/f789a44863_platform.claude.com__docs__en__agent-skills__best-practices.html) | html ✓ · md ✓ | — |
| <a id="5a9f63821f"></a>[`5a9f63821f`](5a9f63821f/) | **Agent Skills: Security** | [Source URL](https://platform.claude.com/docs/en/agent-skills/security) | [Local Source](5a9f63821f/f3a634c400_platform.claude.com__docs__en__agent-skills__security.html) | html ✓ · md ✓ | — |
| <a id="9d696416cb"></a>[`9d696416cb`](9d696416cb/) | **Anthropic Agent Skills — Overview (Platform docs)** | [Source URL](https://platform.claude.com/docs/en/agent-skills/overview) | [Local Source](9d696416cb/platform-claude-com-agent-skills-overview.txt) | txt ✓ | — |
| <a id="516e66f9f7"></a>[`516e66f9f7`](516e66f9f7/) | **Quests, token leaderboards, and a skills marketplace: The elite AI adoption playbook \| John Kim (Sendbird)** | [Source URL](https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation) | [Local Source](516e66f9f7/Quests%20token%20leaderboards%20and%20a%20s.txt) | txt ✓ | [`research/36-sendbird-quests-token-tiers.md`](../research/36-sendbird-quests-token-tiers.md) *(1)* |
| <a id="ee885bfc4c"></a>[`ee885bfc4c`](ee885bfc4c/) | **Skill authoring best practices - Claude API Docs** | [Source URL](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | [Local Source](ee885bfc4c/Skill%20authoring%20best%20practices%20-%20Claude%20API%20Docs.mhtml) | mhtml ✓ | — |
| <a id="26035151aa"></a>[`26035151aa`](26035151aa/) | **The Complete Guide to Building Skills for Claude** | [Source URL](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | [Local Source](26035151aa/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) | pdf ✓ | — |
| <a id="3643d46af4"></a>[`3643d46af4`](3643d46af4/) | **What are Skills? (Anthropic support)** | [Source URL](https://support.claude.com/en/articles/what-are-skills) | [Local Source](3643d46af4/support-claude-com-what-are-skills.txt) | txt ✓ | — |

</details>

<a id="cat-evals-and-benchmarks"></a>

<details>
<summary><b>evals-and-benchmarks</b> — 28 records — <em>SWE-bench, SWE-agent, AlphaCode, CodeGen, evals primers (Husain, Yan, Shankar).</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="366927b32e"></a>[`366927b32e`](366927b32e/) | **(unknown)** | [Source URL](https://eugeneyan.com/404.html) | [Local Source](366927b32e/975ebfc0d7_eugeneyan.com__writing__llm-evaluator.html) | html ✓ | — |
| <a id="2137eaa69f"></a>[`2137eaa69f`](2137eaa69f/) | **[2203.07814] Competition-Level Code Generation with AlphaCode** | [Source URL](https://arxiv.org/abs/2203.07814) | [Local Source](2137eaa69f/f5ef9048e2_arxiv.org__abs__2203.07814.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="bee5963dd8"></a>[`bee5963dd8`](bee5963dd8/) | **[2203.07814] Competition-Level Code Generation with AlphaCode (ar5iv HTML)** | [Source URL](https://ar5iv.labs.arxiv.org/html/2203.07814) | [Local Source](bee5963dd8/e46fc62bac_ar5iv.labs.arxiv.org__html__2203.07814.html) | html ✓ · md ✓ | — |
| <a id="5b36476e30"></a>[`5b36476e30`](5b36476e30/) | **[2203.13474] CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis** | [Source URL](https://arxiv.org/abs/2203.13474) | [Local Source](5b36476e30/0ddbf74275_arxiv.org__abs__2203.13474.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="3e4a5dea3a"></a>[`3e4a5dea3a`](3e4a5dea3a/) | **[2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** | [Source URL](https://arxiv.org/abs/2310.06770) | [Local Source](3e4a5dea3a/e0cb42ccf2_arxiv.org__abs__2310.06770.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="54b1ddaabf"></a>[`54b1ddaabf`](54b1ddaabf/) | **[2405.15793] SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** | [Source URL](https://arxiv.org/abs/2405.15793) | [Local Source](54b1ddaabf/58fb7d3580_arxiv.org__abs__2405.15793.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="71d2de09c6"></a>[`71d2de09c6`](71d2de09c6/) | **A Field Guide to Rapidly Improving AI Products**<br><em>Hamel Husain — experiments-not-features roadmap reframe + NurtureBoss case study</em> | [Source URL](https://hamel.dev/blog/posts/field-guide) | [Local Source](71d2de09c6/307762ff25_hamel.dev__blog__posts__field-guide.html) | html ✓ · md ✓ · mhtml ✓ | [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(1)* |
| <a id="49a54313c7"></a>[`49a54313c7`](49a54313c7/) | **Competitive programming with AlphaCode — Google DeepMind** | [Source URL](https://deepmind.google/discover/blog/competitive-programming-with-alphacode) | [Local Source](49a54313c7/ccdac16687_deepmind.google__discover__blog__competitive-programming-with-alphacode__.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="0c4bb49f75"></a>[`0c4bb49f75`](0c4bb49f75/) | **Creating an LLM-as-a-Judge**<br><em>Hamel Husain — operational manual for LLM judges (Critique Shadowing pattern)</em> | [Source URL](https://hamel.dev/blog/posts/llm-judge) | [Local Source](0c4bb49f75/b979c76d0b_hamel.dev__blog__posts__llm-judge.html) | html ✓ · md ✓ | [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(1)* |
| <a id="caad3c1702"></a>[`caad3c1702`](caad3c1702/) | ~~Eugene Yan — LLM Evaluator~~ → [`ade5ef8d76`](#ade5ef8d76) | — | — | — | — |
| <a id="ade5ef8d76"></a>[`ade5ef8d76`](ade5ef8d76/) | **Eugene Yan — LLM Evaluators**<br><em>Third core eval source (with Husain and Anthropic multi-agent)</em> | [Source URL](https://eugeneyan.com/writing/llm-evaluators) | [Local Source](ade5ef8d76/Evaluating%20the%20Effectiveness%20of%20LLM-Evaluators%20%28aka%20LLM-as-Judge%29.mhtml) | mhtml ✓ | — |
| <a id="18856eb4cf"></a>[`18856eb4cf`](18856eb4cf/) | **FAQs About AI Evals**<br><em>Husain & Shankar — 60-80% of dev time on error analysis</em> | [Source URL](https://hamel.dev/blog/posts/evals-faq) | [Local Source](18856eb4cf/b8fcb74562_hamel.dev__blog__posts__evals-faq.html) | html ✓ · md ✓ · mhtml ✓ | [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(1)* |
| <a id="8cc1f9afc8"></a>[`8cc1f9afc8`](8cc1f9afc8/) | **Hamel Husain’s Blog** | [Source URL](https://hamel.dev/) | [Local Source](8cc1f9afc8/Hamel%20Husain%E2%80%99s%20Blog%20%E2%80%93%20Hamel%27s%20Blog%20-%20Hamel%20Husain.mhtml) | mhtml ✓ | — |
| <a id="10b59b402b"></a>[`10b59b402b`](10b59b402b/) | **Introducing SWE-bench Verified** | [Source URL](https://openai.com/index/introducing-swe-bench-verified) | [Local Source](10b59b402b/Introducing%20SWE-bench%20Verified%20_%20OpenAI.txt) | txt ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="6ea6e28334"></a>[`6ea6e28334`](6ea6e28334/) | **Langfuse Blog (index of posts)** | [Source URL](https://langfuse.com/blog) | [Local Source](6ea6e28334/Langfuse%20blog%20posts%20available.mhtml) | mhtml ✓ | — |
| <a id="da116da1a4"></a>[`da116da1a4`](da116da1a4/) | **Quality, Not Speed: Building a Production Evaluation Framework for AI-Assisted Medical Document Authoring — 8090 Blog** | [Source URL](https://www.8090.ai/blog/quality-not-speed-building-a-production-evaluation-framework-for-ai-assisted-medical-document-authoring) | [Local Source](da116da1a4/Quality%2C%20Not%20Speed_%20Building%20a%20Production%20Evaluation%20Framework%20for%20AI-Assisted%20Medical%20Document%20Authoring%20%E2%80%94%208090%20Blog.mhtml) | mhtml ✓ | — |
| <a id="67dfba1ed6"></a>[`67dfba1ed6`](67dfba1ed6/) | **Simon Willison on evals** | [Source URL](https://simonwillison.net/tags/evals) | [Local Source](67dfba1ed6/simonwillison.net__tags__evals.html) | html ✓ | [`research/05-simon-willison.md`](../research/05-simon-willison.md) *(1)* |
| <a id="e951bbc27e"></a>[`e951bbc27e`](e951bbc27e/) | **strongdm/attractorbench: NLSpec instruction following benchmark** | [Source URL](https://github.com/strongdm/attractorbench) | [Local Source](e951bbc27e/strongdm_attractorbench_%20NLSpec%20instruction%20following%20benchmark%20for%20https___factory.strongdm.ai_products_attractor.txt) | txt ✓ | [`research/07-dark-factory.md`](../research/07-dark-factory.md) · [`research/27-dotfile-pipelines-as-product.md`](../research/27-dotfile-pipelines-as-product.md) · [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(3)* |
| <a id="be4a3756f4"></a>[`be4a3756f4`](be4a3756f4/) | **SWE-agent documentation** | [Source URL](https://swe-agent.com/latest) | [Local Source](be4a3756f4/792a008f65_swe-agent.com__latest__.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="cd9714d14e"></a>[`cd9714d14e`](cd9714d14e/) | **SWE-agent: Agent-Computer Interfaces (ACI)** | [Source URL](https://swe-agent.com/latest/background/aci) | [Local Source](cd9714d14e/768037f6d2_swe-agent.com__latest__background__aci__.html) | html ✓ · md ✓ | — |
| <a id="2ffe813975"></a>[`2ffe813975`](2ffe813975/) | **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (OpenReview, NeurIPS 2024)** | [Source URL](https://openreview.net/forum?id=mXpq6ut8J3) | [Local Source](2ffe813975/fab9b6461c_openreview.net__forum_id_mXpq6ut8J3.html) | html ✓ · md ✓ | — |
| <a id="433a37bad4"></a>[`433a37bad4`](433a37bad4/) | **SWE-bench** | [Source URL](https://www.swebench.com/) | [Local Source](433a37bad4/cf42ebe435_www.swebench.com__.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="ec39dd30f2"></a>[`ec39dd30f2`](ec39dd30f2/) | **SWE-bench (original)** | [Source URL](https://www.swebench.com/original.html) | [Local Source](ec39dd30f2/feaf516c14_www.swebench.com__original.html.html) | html ✓ · md ✓ | — |
| <a id="16ed58023e"></a>[`16ed58023e`](16ed58023e/) | **SWE-bench Lite** | [Source URL](https://www.swebench.com/lite.html) | [Local Source](16ed58023e/031a17f559_www.swebench.com__lite.html.html) | html ✓ · md ✓ | — |
| <a id="af47372f0f"></a>[`af47372f0f`](af47372f0f/) | **SWE-bench Verified** | [Source URL](https://www.swebench.com/verified.html) | [Local Source](af47372f0f/374353fbb7_www.swebench.com__verified.html.html) | html ✓ · md ✓ | — |
| <a id="f9d207b032"></a>[`f9d207b032`](f9d207b032/) | **SWE-bench: Can Language Models Resolve Real-World GitHub Issues? \| Princeton Language and Intelligence** | [Source URL](https://pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-github-issues) | [Local Source](f9d207b032/SWE-bench_%20Can%20Language%20Models%20Resolve%20Real-World%20GitHub%20Issues_%20_%20Princeton%20Language%20and%20Intelligence.mhtml) | mhtml ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="eb69cbdcba"></a>[`eb69cbdcba`](eb69cbdcba/) | **Writing • Eugene Yan** | [Source URL](https://eugeneyan.com/writing) | [Local Source](eb69cbdcba/Writing%20%E2%80%A2%20Eugene%20Yan.mhtml) | mhtml ✓ | — |
| <a id="faa604dace"></a>[`faa604dace`](faa604dace/) | **Your AI Product Needs Evals**<br><em>Hamel Husain — the philosophical root of LLM eval discipline</em> | [Source URL](https://hamel.dev/blog/posts/evals) | [Local Source](faa604dace/your-ai-product-needs-evals.html) | html ✓ | [`research/followup/07-evals-deepdive.md`](../research/followup/07-evals-deepdive.md) *(1)* |

</details>

<a id="cat-academic-foundations"></a>

<details>
<summary><b>academic-foundations</b> — 9 records — <em>Academic methodology papers: underspecification, multi-task benchmarks, CHI/ICSE studies.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="6bea7182f9"></a>[`6bea7182f9`](6bea7182f9/) | **(unknown)** | [Source URL](https://arxiv.org/html/2505.13360v3) | [Local Source](6bea7182f9/2662e841a3_arxiv.org__html__2505.13360v3.html) | html ✓ · md ✓ | [`research/26-prompt-underspecification-academic.md`](../research/26-prompt-underspecification-academic.md) *(1)* |
| <a id="7beb3bc828"></a>[`7beb3bc828`](7beb3bc828/) | **(unknown)** | [Source URL](https://arxiv.org/html/2507.20439v1) | [Local Source](7beb3bc828/4d499d46a4_arxiv.org__html__2507.20439v1.html) | html ✓ · md ✓ | [`research/26-prompt-underspecification-academic.md`](../research/26-prompt-underspecification-academic.md) *(1)* |
| <a id="bee5963dd8"></a>[`bee5963dd8`](bee5963dd8/) | **[2203.07814] Competition-Level Code Generation with AlphaCode (ar5iv HTML)** | [Source URL](https://ar5iv.labs.arxiv.org/html/2203.07814) | [Local Source](bee5963dd8/e46fc62bac_ar5iv.labs.arxiv.org__html__2203.07814.html) | html ✓ · md ✓ | — |
| <a id="7ff9a0b608"></a>[`7ff9a0b608`](7ff9a0b608/) | **CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis (OpenReview, ICLR 2023)** | [Source URL](https://openreview.net/forum?id=iaYcJKpY2B_) | [Local Source](7ff9a0b608/d7c124e7b6_openreview.net__forum_id_iaYcJKpY2B_.html) | html ✓ · md ✓ | [`research/22-academic-foundations.md`](../research/22-academic-foundations.md) *(1)* |
| <a id="24ca29ee98"></a>[`24ca29ee98`](24ca29ee98/) | **Defeating Prompt Injections by Design** | [Source URL](https://arxiv.org/abs/2503.18813) | [Local Source](24ca29ee98/91a944142c_arxiv.org__abs__2503.18813.html) | html ✓ · md ✓ · other ✓ · other ✓ · other ✓ · pdf ✓ | [`research/followup/08-security-primitives.md`](../research/followup/08-security-primitives.md) *(1)* |
| <a id="e588b9bb1a"></a>[`e588b9bb1a`](e588b9bb1a/) | ~~Defeating Prompt Injections by Design (arXiv:2503.18813v2)~~ → [`24ca29ee98`](#24ca29ee98) | — | — | — | — |
| <a id="fa20be05d7"></a>[`fa20be05d7`](fa20be05d7/) | **Neves-Bussmann (Stanford Computational Antitrust, Vol. 6, 2026)** | [Source URL](https://law.stanford.edu/publications) | [Local Source](fa20be05d7/Neves-Bussmann.pdf) | pdf ✓ | — |
| <a id="2ffe813975"></a>[`2ffe813975`](2ffe813975/) | **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (OpenReview, NeurIPS 2024)** | [Source URL](https://openreview.net/forum?id=mXpq6ut8J3) | [Local Source](2ffe813975/fab9b6461c_openreview.net__forum_id_mXpq6ut8J3.html) | html ✓ · md ✓ | — |
| <a id="b4907c87f4"></a>[`b4907c87f4`](b4907c87f4/) | **The Prompt Report: A Systematic Survey of Prompt Engineering Techniques** | [Source URL](https://arxiv.org/html/2406.06608v6) | [Local Source](b4907c87f4/The%20Prompt%20Report_%20A%20Systematic%20Survey%20of%20Prompt%20Engineering%20Techniques.mhtml) | mhtml ✓ | [`research/29-prompt-engineering-survey.md`](../research/29-prompt-engineering-survey.md) *(1)* |

</details>

<a id="cat-security-primitives"></a>

<details>
<summary><b>security-primitives</b> — 4 records — <em>Threat models, prompt-injection defenses, capability/data-flow security (CaMeL, AgentDojo).</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="24ca29ee98"></a>[`24ca29ee98`](24ca29ee98/) | **Defeating Prompt Injections by Design** | [Source URL](https://arxiv.org/abs/2503.18813) | [Local Source](24ca29ee98/91a944142c_arxiv.org__abs__2503.18813.html) | html ✓ · md ✓ · other ✓ · other ✓ · other ✓ · pdf ✓ | [`research/followup/08-security-primitives.md`](../research/followup/08-security-primitives.md) *(1)* |
| <a id="d30b9fbd12"></a>[`d30b9fbd12`](d30b9fbd12/) | **Defeating Prompt Injections by Design (arXiv 2503.18813 PDF)** | [Source URL](https://arxiv.org/pdf/2503.18813) | [Local Source](d30b9fbd12/6a6cc551c7_arxiv.org__pdf__2503.18813.html) | html ✓ · md ✓ | — |
| <a id="e588b9bb1a"></a>[`e588b9bb1a`](e588b9bb1a/) | ~~Defeating Prompt Injections by Design (arXiv:2503.18813v2)~~ → [`24ca29ee98`](#24ca29ee98) | — | — | — | — |
| <a id="53ed6e363d"></a>[`53ed6e363d`](53ed6e363d/) | **Simon Willison — CaMeL paper writeup**<br><em>Willison summary of the CaMeL prompt-injection defense paper</em> | [Source URL](https://simonwillison.net/2025/Apr/11/camel) | [Local Source](53ed6e363d/2ab9a1ab38_simonwillison.net__2025__Apr__11__camel.html) | html ✓ · md ✓ · mhtml ✓ | [`research/06-hn-and-lenny.md`](../research/06-hn-and-lenny.md) · [`research/followup/08-security-primitives.md`](../research/followup/08-security-primitives.md) *(2)* |

</details>

<a id="cat-governance-and-legal"></a>

<details>
<summary><b>governance-and-legal</b> — 7 records — <em>Stanford CodeX, Caremark / RSI board exposure, NHTSA levels, AUTOSAR, ISO 42010.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="0d2f8d5810"></a>[`0d2f8d5810`](0d2f8d5810/) | **AI Life Cycle Core Principles - CodeX - Stanford Law School** | [Source URL](https://law.stanford.edu/2023/03/17/ai-life-cycle-core-principles) | [Local Source](0d2f8d5810/AI%20Life%20Cycle%20Core%20Principles%20-%20CodeX%20-%20Stanford%20Law%20School.txt) | txt ✓ | — |
| <a id="a4a2c507c6"></a>[`a4a2c507c6`](a4a2c507c6/) | **Built by Agents, Tested by Agents, Trusted by Whom? - CodeX - Stanford Law School** | [Source URL](https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom) | [Local Source](a4a2c507c6/2c631ecd45_law.stanford.edu__2026__02__08__built-by-agents-tested-by-agents-trusted-by-whom.html) | html ✓ · md ✓ | — |
| <a id="d01c58d1d5"></a>[`d01c58d1d5`](d01c58d1d5/) | **Cognitive Escrow: The Human-Centered Principle Has a Blind Spot - CodeX - Stanford Law School** | [Source URL](https://law.stanford.edu/2026/03/07/cognitive-escrow-the-human-centered-principle-has-a-blind-spot) | [Local Source](d01c58d1d5/Cognitive%20Escrow_%20The%20Human-Centered%20Principle%20Has%20a%20Blind%20Spot%20-%20CodeX%20-%20Stanford%20Law%20School.txt) | txt ✓ | [`research/30-cognitive-escrow.md`](../research/30-cognitive-escrow.md) *(1)* |
| <a id="0d8acce129"></a>[`0d8acce129`](0d8acce129/) | **From Principles to Practice: The 48 Controls That Make Responsible AI Auditable, Defensible, and Real - CodeX - Stanford Law School** | [Source URL](https://law.stanford.edu/2026/02/16/from-principles-to-practice-the-48-controls-that-make-responsible-ai-auditable-defensible-and-real) | [Local Source](0d8acce129/From%20Principles%20to%20Practice_%20The%2048%20Controls%20That%20Make%20Responsible%20AI%20Auditable%2C%20Defensible%2C%20and%20Real%20-%20CodeX%20-%20Stanford%20Law%20School.txt) | txt ✓ | — |
| <a id="fa20be05d7"></a>[`fa20be05d7`](fa20be05d7/) | **Neves-Bussmann (Stanford Computational Antitrust, Vol. 6, 2026)** | [Source URL](https://law.stanford.edu/publications) | [Local Source](fa20be05d7/Neves-Bussmann.pdf) | pdf ✓ | — |
| <a id="b366ba8741"></a>[`b366ba8741`](b366ba8741/) | **The Ungovernable Machine** | [Source URL](https://law.stanford.edu/2026/03/17/the-ungovernable-machine) | [Local Source](b366ba8741/The%20Ungovernable%20Machine%20-%20CodeX%20-%20Stanford%20Law%20School.txt) | txt ✓ | [`research/31-caremark-rsi-board-exposure.md`](../research/31-caremark-rsi-board-exposure.md) *(1)* |
| <a id="71e8193f07"></a>[`71e8193f07`](71e8193f07/) | **Turning AI Governance Into Operational Infrastructure** | [Source URL](https://law.stanford.edu/2026/04/05/turning-ai-governance-into-operational-infrastructure) | [Local Source](71e8193f07/Turning%20AI%20Governance%20Into%20Operational%20Infrastructure%20-%20CodeX%20-%20Stanford%20Law%20School.txt) | txt ✓ | — |

</details>

<a id="cat-ai-engineering-culture"></a>

<details>
<summary><b>ai-engineering-culture</b> — 23 records — <em>Team-level dynamics, organisational culture, the social/operational side.</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="e6f77b9e81"></a>[`e6f77b9e81`](e6f77b9e81/) | **A Manifesto for Agentic Development** | [Source URL](https://jayminwest.substack.com/p/a-manifesto-for-agentic-development) | [Local Source](e6f77b9e81/5b9538c4e3_jayminwest.substack.com__p__a-manifesto-for-agentic-development.html) | html ✓ · mhtml ✓ | — |
| <a id="80735d97d3"></a>[`80735d97d3`](80735d97d3/) | **AddyOsmani.com - Agentic Engineering** | [Source URL](https://addyosmani.com/blog/agentic-engineering) | [Local Source](80735d97d3/b6ee58bd76_addyosmani.com__blog__agentic-engineering__.html) | html ✓ · md ✓ | [`research/12-adjacent-ecosystem.md`](../research/12-adjacent-ecosystem.md) *(1)* |
| <a id="992e4f88b6"></a>[`992e4f88b6`](992e4f88b6/) | **Agentic Engineering Book (Jaymin West)** | [Source URL](https://www.jayminwest.com/agentic-engineering-book) | [Local Source](992e4f88b6/96bb6edd45_www.jayminwest.com__agentic-engineering-book.html) | html ✓ · md ✓ · youtube-transcript (want) · youtube-transcript (want) · youtube-transcript (want) | — |
| <a id="35b057067e"></a>[`35b057067e`](35b057067e/) | **Agentic Engineering Book – Chapter 6: Harnesses (Jaymin West)** | [Source URL](https://www.jayminwest.com/agentic-engineering-book/6-harnesses) | [Local Source](35b057067e/8569c92993_www.jayminwest.com__agentic-engineering-book__6-harnesses.html) | html ✓ · md ✓ | — |
| <a id="8484aea116"></a>[`8484aea116`](8484aea116/) | **AI and the marshmallow test - by Sam Schillace** | [Source URL](https://sundaylettersfromsam.substack.com/p/ai-and-the-marshmallow-test) | [Local Source](8484aea116/AI%20and%20the%20marshmallow%20test%20-%20by%20Sam%20Schillace.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="4dae4e40d9"></a>[`4dae4e40d9`](4dae4e40d9/) | **Artisans and Factory Lines - by Sam Schillace** | [Source URL](https://sundaylettersfromsam.substack.com/p/artisans-and-factory-lines) | [Local Source](4dae4e40d9/Artisans%20and%20Factory%20Lines%20-%20by%20Sam%20Schillace.mhtml) | mhtml ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="384a19285c"></a>[`384a19285c`](384a19285c/) | **Attention and collaboration in the AI world** | [Source URL](https://sundaylettersfromsam.substack.com/p/attention-and-collaboration-in-the) | [Local Source](384a19285c/Attention%20and%20collaboration%20in%20the%20AI%20world.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="890af05bff"></a>[`890af05bff`](890af05bff/) | **Attention is all ya got - by Sam Schillace - Sunday Letters** | [Source URL](https://sundaylettersfromsam.substack.com/p/attention-is-all-ya-got) | [Local Source](890af05bff/Attention%20is%20all%20ya%20got%20-%20by%20Sam%20Schillace%20-%20Sunday%20Letters.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="67b1f7d3a3"></a>[`67b1f7d3a3`](67b1f7d3a3/) | **Culture of AI Engineering** | [Source URL](https://every.to/source-code/the-culture-of-ai-engineering) | [Local Source](67b1f7d3a3/brier-culture-of-ai-engineering.txt) | txt ✓ | — |
| <a id="f6b9330226"></a>[`f6b9330226`](f6b9330226/) | **Harness engineering: leveraging Codex in an agent-first world** | [Source URL](https://openai.com/index/harness-engineering) | [Local Source](f6b9330226/Harness%20engineering_%20leveraging%20Codex%20in%20an%20agent-first%20world%20_%20OpenAI.txt) | txt ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="226e141838"></a>[`226e141838`](226e141838/) | **How it will happen - by Sam Schillace - Sunday Letters** | [Source URL](https://sundaylettersfromsam.substack.com/p/how-it-will-happen) | [Local Source](226e141838/How%20it%20will%20happen%20-%20by%20Sam%20Schillace%20-%20Sunday%20Letters.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="83fdf58ee6"></a>[`83fdf58ee6`](83fdf58ee6/) | **I have seen the compounding teams - by Sam Schillace** | [Source URL](https://sundaylettersfromsam.substack.com/p/i-have-seen-the-compounding-teams) | [Local Source](83fdf58ee6/I%20have%20seen%20the%20compounding%20teams%20-%20by%20Sam%20Schillace.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="accca79ad1"></a>[`accca79ad1`](accca79ad1/) | **Machine with Concrete - by Sam Schillace - Sunday Letters** | [Source URL](https://sundaylettersfromsam.substack.com/p/machine-with-concrete) | [Local Source](accca79ad1/Machine%20with%20Concrete%20-%20by%20Sam%20Schillace%20-%20Sunday%20Letters.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="ecc055b160"></a>[`ecc055b160`](ecc055b160/) | **Part 1: Why Building Fast Is Not Enough — 8090 Blog** | [Source URL](https://www.8090.ai/blog/part-1-why-building-fast-is-not-enough) | [Local Source](ecc055b160/Part%201_%20Why%20Building%20Fast%20Is%20Not%20Enough%20%E2%80%94%208090%20Blog.mhtml) | mhtml ✓ | — |
| <a id="4ccd0104d2"></a>[`4ccd0104d2`](4ccd0104d2/) | **Part 2: What Alignment Actually Is — 8090 Blog** | [Source URL](https://www.8090.ai/blog/part-2-what-alignment-actually-is) | [Local Source](4ccd0104d2/Part%202_%20What%20Alignment%20Actually%20Is%20%E2%80%94%208090%20Blog.mhtml) | mhtml ✓ | — |
| <a id="388198d08f"></a>[`388198d08f`](388198d08f/) | **Part 3: Seven Properties of an Aligned System — 8090 Blog** | [Source URL](https://www.8090.ai/blog/part-3-seven-properties-of-an-aligned-system) | [Local Source](388198d08f/Part%203_%20Seven%20Properties%20of%20an%20Aligned%20System%20%E2%80%94%208090%20Blog.mhtml) | mhtml ✓ | — |
| <a id="5a214ded33"></a>[`5a214ded33`](5a214ded33/) | **Part 4: How Alignment Compounds — 8090 Blog** | [Source URL](https://www.8090.ai/blog/part-4-how-alignment-compounds-) | [Local Source](5a214ded33/Part%204_%20How%20Alignment%20Compounds%20%E2%80%94%208090%20Blog.mhtml) | mhtml ✓ | — |
| <a id="da116da1a4"></a>[`da116da1a4`](da116da1a4/) | **Quality, Not Speed: Building a Production Evaluation Framework for AI-Assisted Medical Document Authoring — 8090 Blog** | [Source URL](https://www.8090.ai/blog/quality-not-speed-building-a-production-evaluation-framework-for-ai-assisted-medical-document-authoring) | [Local Source](da116da1a4/Quality%2C%20Not%20Speed_%20Building%20a%20Production%20Evaluation%20Framework%20for%20AI-Assisted%20Medical%20Document%20Authoring%20%E2%80%94%208090%20Blog.mhtml) | mhtml ✓ | — |
| <a id="7839068ee6"></a>[`7839068ee6`](7839068ee6/) | **The agent-shaped world - by Sam Schillace - Sunday Letters** | [Source URL](https://sundaylettersfromsam.substack.com/p/the-agent-shaped-world) | [Local Source](7839068ee6/The%20agent-shaped%20world%20-%20by%20Sam%20Schillace%20-%20Sunday%20Letters.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="16aabc3cfe"></a>[`16aabc3cfe`](16aabc3cfe/) | **The hard part isn't doing the work now; it's choosing the work.** | [Source URL](https://sundaylettersfromsam.substack.com/p/the-hard-part-isnt-doing-the-work) | [Local Source](16aabc3cfe/The%20hard%20part%20isn%27t%20doing%20the%20work%20now%3B%20it%27s%20choosing%20the%20work..txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="19fba72517"></a>[`19fba72517`](19fba72517/) | **The one scarce resource AI can't replace - by Sam Schillace** | [Source URL](https://sundaylettersfromsam.substack.com/p/laundry-lists-and-building-blocks) | [Local Source](19fba72517/The%20one%20scarce%20resource%20AI%20can%27t%20replace%20-%20by%20Sam%20Schillace.txt) | txt ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |
| <a id="e205ffac9d"></a>[`e205ffac9d`](e205ffac9d/) | **Unlocking the Codex harness: how we built the App Server** | [Source URL](https://openai.com/index/unlocking-the-codex-harness) | [Local Source](e205ffac9d/Unlocking%20the%20Codex%20harness_%20how%20we%20built%20the%20App%20Server%20_%20OpenAI.txt) | txt ✓ | [`research/18-openai-codex-substrate.md`](../research/18-openai-codex-substrate.md) *(1)* |
| <a id="375a9386eb"></a>[`375a9386eb`](375a9386eb/) | **What is a harness and why do I care? - by Sam Schillace** | [Source URL](https://sundaylettersfromsam.substack.com/p/what-is-a-harness-and-why-do-i-care) | [Local Source](375a9386eb/What%20is%20a%20harness%20and%20why%20do%20I%20care_%20-%20by%20Sam%20Schillace.mhtml) | mhtml ✓ | [`research/28-schillace-sunday-letters.md`](../research/28-schillace-sunday-letters.md) *(1)* |

</details>

<a id="cat-meta-synthesis"></a>

<details>
<summary><b>meta-synthesis</b> — 2 records — <em>Derived syntheses over the corpus (counterfactual deep-research, QC re-reads).</em></summary>

| ID | Title / Summary | Source URL | Local Source | Files | Cited in |
|---|---|---|---|---|---|
| <a id="1e18da4d24"></a>[`1e18da4d24`](1e18da4d24/) | **ChatGPT Deep Research synthesis (2026-05-11) — report** | — | [Local Source](1e18da4d24/report.md) | md ✓ | — |
| <a id="c2cdaebb34"></a>[`c2cdaebb34`](c2cdaebb34/) | **ChatGPT Deep Research synthesis (2026-05-11) — sources list** | — | [Local Source](c2cdaebb34/sources.md) | md ✓ | — |

</details>

<a id="by-status"></a>
## By status (cross-cutting view)

<a id="status-complete"></a>
### § 1 — Complete *(196 records)*

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
- [`dccefbfc62` — =?utf-8?Q?Agent=20approvals=20&=20security=20=E2=80=93=20Codex=20|=20Open?=](#dccefbfc62)
- [`175cba9347` — =?utf-8?Q?Custom=20instructions=20with=20AGENTS.md=20=E2=80=93=20Codex=20?=](#175cba9347)
- [`5cc5a296b6` — =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Agent=203:=20Our=20Most=20Au?=](#5cc5a296b6)
- [`73dc7199ce` — =?utf-8?Q?Replit=20=E2=80=94=20Introducing=20Replit=20Agent=204:=20Built?=](#73dc7199ce)
- [`8334be0240` — =?utf-8?Q?Subagents=20=E2=80=93=20Codex=20|=20OpenAI=20Developers?=](#8334be0240)
- [`3703e782c0` — =?utf-8?Q?You=20Don=E2=80=99t=20Write=20the=20Code.=20You=20Don=E2=80=99t?=](#3703e782c0)
- [`2137eaa69f` — [2203.07814] Competition-Level Code Generation with AlphaCode](#2137eaa69f)
- [`bee5963dd8` — [2203.07814] Competition-Level Code Generation with AlphaCode (ar5iv HTML)](#bee5963dd8)
- [`5b36476e30` — [2203.13474] CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis](#5b36476e30)
- [`3e4a5dea3a` — [2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](#3e4a5dea3a)
- [`54b1ddaabf` — [2405.15793] SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](#54b1ddaabf)
- [`23b7d51d69` — [2511.03690] The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents](#23b7d51d69)
- [`71d2de09c6` — A Field Guide to Rapidly Improving AI Products](#71d2de09c6)
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
- [`24ca29ee98` — Defeating Prompt Injections by Design](#24ca29ee98)
- [`d30b9fbd12` — Defeating Prompt Injections by Design (arXiv 2503.18813 PDF)](#d30b9fbd12)
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
- [`ade5ef8d76` — Eugene Yan — LLM Evaluators](#ade5ef8d76)
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
- [`18856eb4cf` — FAQs About AI Evals](#18856eb4cf)
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
- [`53ed6e363d` — Simon Willison — CaMeL paper writeup](#53ed6e363d)
- [`ee885bfc4c` — Skill authoring best practices - Claude API Docs](#ee885bfc4c)
- [`59d633b2c6` — Smasher — 2389 Research, Inc.](#59d633b2c6)
- [`8282baf1e4` — Software factories and the agentic moment (Hacker News)](#8282baf1e4)
- [`a03c2b3502` — Software Factory Roadmap 2026 — 8090](#a03c2b3502)
- [`95265c651d` — Spec-driven development: The AI engineering workflow (Lenny's Newsletter)](#95265c651d)
- [`5b2ed8c57e` — Spec-driven development: The AI engineering workflow at Notion | Ryan Nystrom](#5b2ed8c57e)
- [`3592091691` — Specification-Driven Agentic Development System: A Methodology for Iterative Specification Refinement Using AI Agents](#3592091691)
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
- [`9c9554d27e` — The lethal trifecta for AI agents: private data, untrusted content, and external communication](#9c9554d27e)
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

<a id="status-partial"></a>
### § 2 — Partial *(11 records)*

*Has some content, but also files that are wanted, partial, or had fetch errors.*

- [`5c785e88b3` — 404 - GitHub Docs](#5c785e88b3)
- [`85cdf07ac2` — 8090 Inc Blog](#85cdf07ac2)
- [`e6f77b9e81` — A Manifesto for Agentic Development](#e6f77b9e81)
- [`5a9f63821f` — Agent Skills: Security](#5a9f63821f)
- [`992e4f88b6` — Agentic Engineering Book (Jaymin West)](#992e4f88b6)
- [`f8007cc630` — An AI State of the Union | Simon Willison (Lenny's Newsletter)](#f8007cc630)
- [`3274cc670c` — Devin (Cognition AI)](#3274cc670c)
- [`586cb02137` — Head of Claude Code: What happens when AI does 90% of the coding](#586cb02137)
- [`5492497a11` — Tabnine Docs (Server Setup Guide)](#5492497a11)
- [`dafe463e94` — Tabnine Docs (Tabnine's Private and Protect)](#dafe463e94)
- [`60fbea1689` — William El Kaim — About (Medium)](#60fbea1689)

<a id="status-wanted-url"></a>
### § 3a — Wanted (URL known) *(5 records)*

*URL is known but no content acquired yet.*

- [`991f3bf0f6` — About Copilot Workspace (GitHub Docs)](#991f3bf0f6)
- [`c6f235b88d` — gascity (gastownhall) — Gas City repository](#c6f235b88d)
- [`d7921179bf` — gastown (gastownhall) — Gas Town repository](#d7921179bf)
- [`974abcda96` — gastownhall/gascity issue #586](#974abcda96)
- [`11086c2305` — The Road Runner Economy (Noah Radford)](#11086c2305)

<a id="status-wanted-title"></a>
### § 3b — Wanted (title only) *(0 records)*

*Title + search hints only; no URL yet.*

*(none)*

<a id="status-superseded"></a>
### § 4 — Superseded *(2 records)*

*Records replaced by another; `pointer_to` is set.*

- `e588b9bb1a` ~~Defeating Prompt Injections by Design (arXiv:2503.18813v2)~~ → [`24ca29ee98`](#24ca29ee98)
- `caad3c1702` ~~Eugene Yan — LLM Evaluator~~ → [`ade5ef8d76`](#ade5ef8d76)

