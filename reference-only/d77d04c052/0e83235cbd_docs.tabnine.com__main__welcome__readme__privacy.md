bars[](/main)

search

circle-xmark

`⌘Ctrl``k`

[Tabnine websitechevron-down](https://www.tabnine.com/)[Contact Sales](https://www.tabnine.com/contact-us/?utm_source=docs&utm_medium=organic&utm_campaign=docs)

Moreellipsischevron-down

[](/main)

  * Welcomechevron-right

    * [Overviewchevron-right](/main)

      * [Architecturechevron-right](/main/welcome/readme/architecture)
      * [Security](/main/welcome/readme/security)
      * [Privacy](/main/welcome/readme/privacy)
      * [Protectionchevron-right](/main/welcome/readme/protection)
      * [Personalizationchevron-right](/main/welcome/readme/personalization)
      * [AI Models](/main/welcome/readme/ai-models)
      * [Integrationschevron-right](/main/welcome/readme/integrations)
      * [System & Hardware Requirementschevron-right](/main/welcome/readme/system-requirements)
      * [Supported Languages](/main/welcome/readme/supported-languages)
      * [Supported IDEs](/main/welcome/readme/supported-ides)
      * [Tabnine Subscription Planschevron-right](/main/welcome/readme/tabnine-subscription-plans)

    * [Support & Feedback](/main/welcome/support-and-feedback)

  * Getting startedchevron-right

    * [Installchevron-right](/main/getting-started/install)
    * [Quickstart Guidechevron-right](/main/getting-started/quickstart)
    * [Context Enginechevron-right](/main/getting-started/context-engine)
    * [Tabnine Agentchevron-right](/main/getting-started/tabnine-agent)
    * [Tabnine Chatchevron-right](/main/getting-started/tabnine-chat)
    * [Tabnine Testingchevron-right](/main/getting-started/tabnine-testing)
    * [Tabnine CLIchevron-right](/main/getting-started/tabnine-cli)
    * [Code Completionschevron-right](/main/getting-started/code-completion)
    * [Inline Actions](/main/getting-started/inline-actions)

  * Administering Tabninechevron-right

    * [Private Installationchevron-right](/main/administering-tabnine/managing-your-team)
    * [memo-padRelease Notes](/main/administering-tabnine/release-notes)




chevron-upchevron-down

[gitbookPowered by GitBook](https://www.gitbook.com/?utm_source=content&utm_medium=trademark&utm_campaign=Y2qxVf5VTm3fmwP4B4Gx&utm_content=site_AIYf2)[gitbook](https://www.gitbook.com/?utm_source=content&utm_medium=trademark&utm_campaign=Y2qxVf5VTm3fmwP4B4Gx&utm_content=site_AIYf2)

xmark

block-quote On this pagexmark

xmark

copyCopychevron-down

block-quoteOn this pageblock-quote

  1. [Welcome](/main/welcome)chevron-right
  2. [Overview](/main)



# Privacy

Tabnine AI code assistant: Privacy

## 

hashtag

Code Privacy

**When using Tabnine models, your code remains private. Tabnine NEVER retains or shares any of your code with third parties.**

Tabnine has a _no-train-no-retain_ policy. This is in place regardless which model is being used.

### 

hashtag

Querying the Tabnine AI Model for AI Coding Assistance

As you code, the Tabnine client (plugin) requests AI assistance from the Tabnine cluster.

For code suggestions, the process occurs in the background as you code. For chat, this request process occurs once the user asks a question.

These requests include **some code from the local project as context** (the **“context window”** as described below) to allow Tabnine to return the most relevant and accurate answers. This context window **may include elements from your local environment, such as** :

  * Chat history (for chat)

  * Lines of code

  * Variables

  * Type declarations

  * Functions

  * Objects

  * Related imports from the current file

  * Related files

  * Syntactic and semantic error reports




This context is deleted **immediately** after the server returns the answer to the client.

**Tabnine doesn’t retain any user code beyond the immediate time frame** required for inferencing the model. This is what we call ephemeral processing.

The sole purpose of the **context window** is to facilitate the most accurate answers possible. The moment that output is generated, the code is discarded and is never stored.

This is true even for [Tabnine Enterprise’sarrow-up-right](https://www.tabnine.com/enterprise) private deployment options (on-premises and VPC).

#### 

hashtag

**With Tabnine models, your code is not shared with third parties**

We develop our AI models based on our own pioneering experience and the best-of-breed, permissive, open source technologies in the market.

No third-party APIs are used.

#### 

hashtag

**Tabnine does not train its models on your code**

**Tabnine’s code completion model and Tabnine Protected chat model are only trained on open source code with permissive licenses.**

Private fine-tuned AI models are pretrained on private code by Tabnine and are only accessible by your team members and stored on your private setup.

Learn more about [Tabnine’s AI models](/main/welcome/readme/ai-models).

circle-info

**Clarification regarding the Magic Moments feature**

The code completion examples in the Tabnine Hub (in the IDE) under the **Magic Moments** tab are saved locally on the user's machine and never leave the computer.

### 

hashtag

Personalization

Tabnine's personalization capabilities — including **context** through local code awareness and **connection** to software repository for global code awareness — require creating a RAG index of your code. The computation for vector embeddings for the chat [RAG index](/main/welcome/readme/personalization/tabnines-personalization-in-depth#the-rag-index) requires a lot of resources, and cannot be done locally without stressing the user’s machine. Tabnine performs this computation on the server GPU while keeping the same principles:

  * Your code remains private; Tabnine never stores your code.

  * Tabnine does not share any of your code with third parties.

  * Tabnine does not train on your code.




[Learn more](/main/welcome/readme/personalization#personalization-and-code-privacy)

### 

hashtag

**Data Plane in Self-Hosted / Air-Gapped Deployment**

The Tabnine cluster collects operational metrics and logs to ensure system health and quality of service.

In an air-gapped deployment, metrics can be sent to a Prometheus server and logs can be sent to your log aggregator. In a self-hosted deployment, the Tabnine cluster sends operational metrics and logs to Tabnine’s servers to allow improved support when required. **No code or PII data is ever sent to Tabnine’s servers**.

### 

hashtag

**Tabnine Cluster**

The Tabnine cluster sends operational metrics and logs (every 1 second) to Tabnine’s servers. Metrics and logs data are retained for a week. This includes:

  * GPU and CPU utilization

  * GPU and CPU memory

  * Server throughput

  * Server latency




### 

hashtag

**Tabnine Client**

The Tabnine client sends telemetry to Tabnine’s self-hosted server (which is then streamed to Tabnine’s servers) on various user interactions. This includes:

  * Plugin and binary configurations

  * User machine details, including CPU type, available processors, and memory

  * One-way hashed, nonidentifiable data, including user email, hostname, and IP

  * IDE details, including type and version

  * Statistical data: Aggregated number of suggestions/completions per programming language




Last updated 9 months ago

Was this helpful?

  * Code Privacy
  * Querying the Tabnine AI Model for AI Coding Assistance
  * Personalization
  * Data Plane in Self-Hosted / Air-Gapped Deployment
  * Tabnine Cluster
  * Tabnine Client



Was this helpful?
