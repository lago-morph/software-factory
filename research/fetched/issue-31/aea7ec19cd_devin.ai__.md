[ ](/)

  * [ Enterprise ](/enterprise)
  * [ Pricing ](/pricing)
  * [ Customers ](/customers)
  * Resources

    * [ Blog ](https://www.cognition.ai/blog/1)
    * [ Docs ](https://docs.devin.ai/)
    * [ Careers ](https://cognition.ai/careers)
    * [ About us ](https://www.cognition.ai/)
    * [ Contact ](https://www.cognition.ai/get-started#company)
    * [ Community ](/community)
    * [ Devin for Security ](/security)




[ Login ](https://app.devin.ai/login?prompt=empty) [ Contact sales ](https://www.cognition.ai/get-started#company) [ Sign up ](https://app.devin.ai/signup)

  * [ Enterprise ](/enterprise)
  * [ Pricing ](/pricing)
  * [ Customers ](/customers)
  * [ Community ](/community)
  * [ Devin for Security ](/security)


  * [ Blog ](https://www.cognition.ai/blog/1)
  * [ Docs ](https://docs.devin.ai/)
  * [ Careers ](https://cognition.ai/careers)
  * [ About us ](https://www.cognition.ai/)
  * [ Contact ](https://www.cognition.ai/get-started#company)

[ Sign up ](https://app.devin.ai/signup) [ Login ](https://app.devin.ai/login?prompt=empty)

## How Nubank refactors millions of lines of code to improve engineering efficiency with Devin

8x

engineering time efficiency gain

20x

cost savings

## Overview

One of Nubank’s most critical, company-wide projects for 2023-2024 was a migration of their core ETL — an 8 year old, multi-million lines of code monolith — to sub-modules. To handle such a large refactor, their only option was a multi-year effort that distributed repetitive refactoring work across over one thousand of their engineers. With Devin, however, this changed: engineers were able to delegate Devin to handle their migrations and achieve a 12x efficiency improvement in terms of engineering hours saved, and over 20x cost savings. Among others, Data, Collections, and Risk business units verified and completed their migrations in weeks instead of months or years.

## The Problem

Nubank was born into the tradition of centralized ETL FinServ architectures. To date, the monolith architecture had worked well for Nubank — it enabled the developer autonomy and flexibility that carried them through their hypergrowth phases. After 8 years, however, Nubank’s sheer volume of customer growth, as well as geographic and product expansion beyond their original credit card business, led to an entangled, behemoth ETL with countless cross-dependencies and no clear path to continuing to scale.

For Nubankers, business critical data transformations started taking increasingly long to run, with chains of dependencies as deep as 70 and insufficient formal agreements on who was responsible for maintaining what. As the company continued to grow, it became clear that the ETL would be a primary bottleneck to scale.

> Nubank concluded that there was an urgent need to split up their monolithic ETL repository, amassing over 6 million lines of code, into smaller, more flexible sub-modules.

Nubank’s code migration was filled with the monotonous, repetitive work that engineers dread. Moving each data class implementation from one architecture to another while tracing imports correctly, performing multiple delicate refactoring steps, and accounting for any number of edge cases was highly tedious, even to do just once or twice. At Nubank’s scale, however, the total migration scope involved more than 1,000 engineers moving ~100,000 data class implementations over an expected timeline of 18 months.

In a world where engineering resources are scarce, such large-scale migrations and modernizations become massively expensive, time-consuming projects that distract from any engineering team’s core mission: building better products for customers. Unfortunately, this is the reality for many of the world’s largest organizations.

## The Decision: an army of Devins to tackle subtasks in parallel

At project outset in 2023, Nubank had no choice but to rely on their engineers to perform code changes manually. Migrating one data class was a highly discretionary task, with multiple variations, edge cases, and ad hoc decision-making — far too complex to be scriptable, but high-volume enough to be a significant manual effort.

Within weeks of Devin’s launch, Nubank identified a clear opportunity to accelerate their refactor at a fraction of the engineering hours. Migration or large refactoring tasks are often fantastic projects for Devin: after investing a small, fixed cost to teach Devin how to approach sub-tasks, Devin can go and complete the migration autonomously. A human is kept in the loop just to manage the project and approve Devin’s changes.

## The Solution: Custom ETL Migration Devin

A task of this magnitude, with the vast number of variations that it had, was a ripe opportunity for fine-tuning. The Nubank team helped to collect examples of previous migrations their engineers had done manually, some of which were fed to Devin for fine-tuning. The rest were used to create a [benchmark evaluation set.](https://cognition.ai/blog/evaluating-coding-agents) Against this evaluation set, we observed a **doubling of Devin’s task completion scores after fine-tuning, as well as a 4x improvement in task speed. Roughly 40 minutes per sub-task dropped to 10,** which made the whole migration start to look much cheaper and less time-consuming, allowing the company to devote more energy to new business and new value creation instead.

Devin contributed to its own speed improvements by building itself classical tools and scripts it would later use on the most common, mechanical components of the migration. For instance, detecting the country extension of a data class (either ‘br’, ‘co’, or ‘mx’) based on its file path was a few-step process for each sub-task. Devin’s script automatically turned this into a single step executable — improvements from which added up immensely across all tens of thousands of sub-tasks.

There is also a compounding advantage on Devin’s learning. In the first weeks, it was common to see outstanding errors to fix, or small things Devin wasn’t sure how to solve. But as Devin saw more examples and gained familiarity with the task, it started to avoid rabbit holes more often and find faster solutions to previously-seen errors and edge cases. Much like a human engineer, we observed obvious speed and reliability improvements with every day Devin worked on the migration.

Results: Delivering an 8-12x faster migration, lifting a burden from every engineer, and slashing migration costs by 20x.

> “Devin provided an easy way to reduce the number of engineering hours for the migration, in a way that was more stable and less prone to human error. Rather than engineers having to work across several files and complete an entire migration task 100%, they could just review Devin’s changes, make minor adjustments, then merge their PR”
> 
> Jose Carlos Castro, Senior Product Manager

8-12x efficiency gains This is calculated by comparing the typical engineering hours required to complete a data class migration task against the total engineering hours spent prompting and reviewing Devin’s work on the same task.

Over 20x cost savings on scope of the migration delegated to Devin This is calculated by comparing the cost of running Devin versus the hourly cost of an engineer completing that task. The significant savings are heavily driven by speed of task execution and cost effectiveness of Devin relative to human engineering time – it does not even consider the value captured by completing the entire project months ahead of schedule!

Fewer dreaded migration tasks for Nubank engineers

[ New Introducing Devin for Terminal ](/terminal)

#  Devin, the AI  
software engineer 

##### Industry leaders choose to

##  Build with Devin

[ Hear from our customers ](/customers)

## Use cases

Use Devin to plan and execute complex engineering tasks, from code migrations to on-call incident resolution.

### PR review & visual QA

  * - Automatically identify and resolve bugs
  * - Visual QA with full browser and desktop use
  * - Intelligently organize code diffs for review

[ Learn about Devin Review ](https://app.devin.ai/review)

### Documentation

  * - Auto-generate documentation and system diagrams for legacy codebases.
  * - Comprehensive visibility into systems that your team hasn't built.

[ Learn more about DeepWiki > ](https://deepwiki.com)

### Code migration + refactors

  * - Assign a fleet of agents to migrate all repos in parallel
  * - Accelerate all modernizations — COBOL, .NET, Talend, legacy ETL, and more.
  * - Complete audibility at each step.



### Scheduled chores and application development

  * - Schedule daily QA and release notes
  * - Continuously review and address user feedback
  * - Maintain documentation



### Issue triage + bug fixing

  * - Investigate Datadog incidents immediately
  * - Intelligently route Slack bug reports
  * - Automatically fix CI failures



### And many others

  * - Automated ticket resolution
  * - Unit and E2E testing
  * - Performance optimization
  * - Web research and scraping
  * - Repetitive browser task automation



## Learn & work  
together

Devin is built for engineering teams with complex, multi-repo projects.

Use when

When working in the backend repo

Approved new knowledge: When working in the backend repo

Rejected new knowledge: When working in the backend repo

### Learns your codebase &   
picks up tribal knowledge

Collaborate

### Works where your team works

Ask Devin to triage Datadog incidents, route Slack messages, and tackle Linear tickets. Or automate entirely using the Devin API and Devin Automations.

### Multi-week, multi-repo projects

Devin can spin up a team of Devins for large tasks. Devin gets better over time by reading past session trajectories.

##  Able to work with hundreds of tools

Build together with

Confluence

Build together with

Airtable

Build together with

Segment

Build together with

Asana

Build together with

Notion

Build together with

Stripe

Build together with

AWS

Build together with

GitHub

Build together with

Datadog

Build together with

Linear

Build together with

Databricks

Build together with

Slack

Build together with

Google Drive

Build together with

Sentry

Build together with

gg 

gg 

PostgreSQL

Build together with

Azure

Build together with

Snowflake

Build together with

MongoDB

#### 

GitHub

Devin ships PRs the way your team does — picking up reviewfeedback and CI results to get each PR approved and merged.

#### 

Linear

Assign Devin tickets directly in Linear, or add a Devin label.

#### 

Slack and Teams

Tag Devin in any conversation to surface relevant context, dig intoissues, or turn discussions directly into PRs.

#### 

Linear

Assign Devin tickets directly in Linear, or add a Devin label.

gg 

gg 

GitHub

Devin ships PRs the way your team does — picking up review feedback and CI results to get each PR approved and merged.

Linear

Assign Devin tickets directly in Linear, or add a Devin label.

Slack and Teams

Tag Devin in any conversation to surface relevant context, dig into issues, or turn discussions directly into PRs.

### Build more with  
Devin

[ Get started ](https://app.devin.ai/signup)

#### Need Devin for your enterprise?

#### Get started with Devin Enterprise

Devin Enterprise provides additional capabilities, security and control for your organization.

[Learn about Devin Enterprise](/enterprise) [ Contact us ](https://www.cognition.ai/get-started#company)

[Privacy policy](https://www.cognition.ai/pages/privacy-policy) [Terms of service](https://www.cognition.ai/pages/terms-of-service) [Your privacy choices](/privacy-choices)

[ Linkedin ](https://www.linkedin.com/company/cognition-ai-labs/) [ X (Twitter) ](https://x.com/cognition)
