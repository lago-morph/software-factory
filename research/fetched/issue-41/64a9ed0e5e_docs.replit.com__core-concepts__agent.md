Skip to main content

[Replit home page](/getting-started/intro-replit)

English

  * [Docs](/getting-started/intro-replit)
  * [Tutorials](/tutorials/effective-prompting)
  * [Trust & Billing](/category/billing)
  * [Enterprise](/category/teams)
  * [Changelog](/updates/2026/05/08/changelog)
  * [Learn](https://learn.replit.com)



Search...

⌘K

  * [Start Building](https://replit.com?ref=docs)



[Replit home page](/getting-started/intro-replit)

Search or ask...

Navigation

Agent

Replit Agent




##### Getting Started

  * [Overview](/getting-started/intro-replit)
  * Quickstarts

  * [Build in ChatGPT](/getting-started/quickstarts/build-in-chatgpt)
  * Import




##### Core Concepts

  * [How Replit works](/core-concepts/how-replit-works)
  * [Overview](/category/replit-apps)
  * [Overview](/category/cloud-services)
  * Agent

    * [Overview](/core-concepts/agent)
    * [Build in Parallel](/core-concepts/agent/task-system)
    * [Efficient Prompting](/core-concepts/agent/best-practices)
    * Autonomy & validation

    * Features

  * Workspaces

  * Project Editor

  * Security

  * Design

  * Projects

  * Storage

  * Integrations

  * Monetization




##### Platforms

  * [Mobile App](/platforms/mobile-app)
  * [ChatGPT](/platforms/chatgpt)



##### Additional Resources

  * [CLUI](/additional-resources/clui-graphical-cli)
  * [Cheat Sheet](/additional-resources/cheat-sheet)
  * [Shared responsibility model](/additional-resources/shared-responsibility-model)
  * [Google Authentication in Python and Flask](/additional-resources/google-auth-in-flask)
  * [Streaming native graphics using VNC](/additional-resources/streaming-native-graphics-vnc)
  * [FAQ](/faq)



Agent

# Replit Agent

Copy page

Replit Agent turns your ideas into apps, designs, slides, and more, all from plain language. No coding required.

Copy page

> ## Documentation Index
> 
> Fetch the complete documentation index at: <https://docs.replit.com/llms.txt>
> 
> Use this file to discover all available pages before exploring further.

## 

​

What is Replit Agent?

Agent is your creative partner. Agent takes your ideas, helps you refine them, and then makes them real. Unlike a chatbot that only answers questions, Agent takes action: it sets up your project, creates applications, checks its work, and fixes problems along the way. Describe what you want in everyday language. No code or technical knowledge required. Agent handles the rest, from planning to deployment.

## 

​

How to use Replit Agent

### 

​

Getting started

1

Describe what you want

In the [Project Editor](/core-concepts/project-editor), just start chatting. Describe an app you want to build, ask a question, research a topic, or pull data from [connected services](/core-concepts/agent/general-agent) like BigQuery, Slack, or Notion. There are no constraints. Replit Agent handles whatever you throw at it.

2

Choose what to build

Optionally, select a project type: web app, mobile app, slides, design, data visualization, and more. If you already described what you want in step 1, Agent figures out the right setup automatically.

3

Agent builds it

Agent writes code, sets up infrastructure, and tests the result. Once you’re in your project, you can switch between Agent modes to control how it builds.

4

Iterate, test, deploy

Chat with Agent to refine your project, then publish when you’re ready. All artifacts deploy together.

You’re not locked into one type. Start with a web app and add a mobile app, slides, or a video later — all in the same project.

### 

​

Plan mode

Enable Plan mode to brainstorm, ask questions, and map out your project before Agent changes any code or data. In Plan mode, Agent will:

  * **Break down complex projects** into ordered task lists
  * **Explore different approaches** and weigh trade-offs
  * **Review and refine** before any code is written

Click “Plan” in the chat input — or simply ask Agent — to switch to Plan mode. Example: “Create a plan to build a project tracker for my team” Agent creates an ordered task list you can review and refine. When you’re happy with the plan, approve it and Agent starts building.

Learn more in the [Plan mode guide](/core-concepts/agent/plan-mode).

### 

​

Agent modes

Choose how Agent builds your project:

  * **Lite** : Make lightweight, inexpensive changes quickly. Lite mode is ideal for visual tweaks, bug fixes, and scoped features.
  * **Economy** : Use Agent’s cost-optimized models for everyday tasks. Expand **Advanced settings** to manage features like App Testing and Code Optimizations.
  * **Power** : Use Agent’s most capable models for harder problems, larger changes, and longer builds. In **Advanced settings** , you can also turn on **Turbo** for up to 2.5x faster builds at higher cost (Pro only).



Tip: You can also enable **[Plan mode](/core-concepts/agent/plan-mode)** to review and iterate on Agent’s plan before building begins. Max mode is no longer available; use Power for the most capable standard builds.

## 

​

What you can build with the Replit Agent

  * **Web apps, mobile apps, data dashboards, and AI-powered tools**
  * **Visual designs and prototypes** — explore mockups on the [Design Canvas](/replitai/canvas) before committing to code
  * **Multiple outputs in one project** — web apps, mobile apps, slides, and videos sharing the same backend
  * **Files and documents** — CSVs, PDFs, PowerPoint files, Markdown docs
  * **Connected service queries** — pull data from BigQuery, Linear, Slack, Notion, and more directly from chat



## Start building now

Describe your idea and let Agent bring it to life — no setup required.

## 

​

Frequently asked questions

Do I need to know how to code?

No. Agent handles all the technical work — writing code, setting up infrastructure, configuring databases. You describe what you want in plain language and Agent builds it.

What's the difference between Lite, Economy, and Power?

**Lite** is for quick, targeted changes (10-60 seconds) such as visual tweaks, bug fixes, and scoped features. **Economy** is the best default for most builds when you want to balance cost and quality. **Power** uses the most capable models for harder tasks, and **Turbo** is an optional Power-only toggle in Advanced settings when you need the fastest runs.

Can I build more than one thing in a project?

Yes. You can add web apps, mobile apps, slides, videos, and data visualizations to the [same project](/replitai/artifacts#multiple-artifacts-in-one-project) — all sharing the same backend and data.

What happens if Agent makes a mistake?

Agent tests its own work on a regular basis. Agent also creates checkpoints as it works, so you can roll back to any previous state. You can also chat with Agent to describe what went wrong and it will fix the issue.

## 

​

Availability

Capability| Core| Pro  
---|---|---  
Agent chat and building| ✅| ✅  
Lite mode| ✅| ✅  
Economy mode| ✅| ✅  
Power mode| ✅| ✅  
Design Canvas| ✅| ✅  
Multi-Artifacts| ✅| ✅  
Active background tasks| 1| 10  
Turbo| ❌| ✅  
  
For detailed pricing, see [Agent billing](/billing/ai-billing#agent-billing).

## 

​

Next steps

## Agent Skills

Teach Agent specialized knowledge — use pre-built skills or create your own.

## Build in parallel

Kanban planning, background tasks, and changes applied back to the main version.

## Design Canvas

Visual mockups and the hands-on visual editor.

## Connectors

Connect BigQuery, Linear, Slack, Notion, and more.

## Billing

Agent pricing, plan comparison, and spending management.

## Vibe coding guide

Tips for effective prompting and building with AI.

Was this page helpful?

YesNo

[Cloud ServicesPrevious](/category/cloud-services)[Build in ParallelNext](/core-concepts/agent/task-system)

⌘I

[x](https://x.com/replit)[linkedin](https://www.linkedin.com/company/repl-it)[youtube](https://www.youtube.com/@replit)

On this page

  * What is Replit Agent?
  * How to use Replit Agent
  * Getting started
  * Plan mode
  * Agent modes
  * What you can build with the Replit Agent
  * Frequently asked questions
  * Availability
  * Next steps


