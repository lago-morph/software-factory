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

Autonomy & validation

App Testing




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

      * [Agent Modes](/core-concepts/agent/agent-modes)
      * [App Testing](/core-concepts/agent/app-testing)
      * [Code Optimizations](/core-concepts/agent/code-optimizations)
      * [Checkpoints](/core-concepts/agent/checkpoints-and-rollbacks)
      * [Plan Mode](/core-concepts/agent/plan-mode)
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



Autonomy & validation

# App Testing

Copy page

Learn how Agent tests your app in a real browser and automatically fixes issues it finds.

Copy page

> ## Documentation Index
> 
> Fetch the complete documentation index at: <https://docs.replit.com/llms.txt>
> 
> Use this file to discover all available pages before exploring further.

App Testing lets Agent test the apps it builds using an actual browser. Agent navigates through your application like a real user would, clicking around and validating functionality. This self-testing capability helps ensure your app works correctly and allows Agent to catch and fix issues automatically.

## 

​

How App Testing works

Watch App Testing in action as Agent navigates through your app:

When App Testing is enabled, Agent will periodically decide to test itself when it thinks enough has changed to deem it necessary. Agent doesn’t test after 100% of user messages, but intelligently determines when testing would be most valuable.

At this time, App Testing is available for Full Stack JavaScript and Streamlit Python web applications.

### 

​

Key Benefits

  * **Extended Autonomy** : Enables Agent to work for longer periods without requiring human intervention
  * **Higher Quality** : Produces apps with fewer mistakes by identifying and addressing issues early
  * **Cost Efficiency** : Prevents the need for additional debugging sessions by catching problems during development
  * **Interactive Review** : Provides video replays and section-by-section navigation for thorough result analysis



### 

​

The Testing Process

When Agent decides to test itself, here’s what happens:

  1. **Browser Preview** : You’ll see a browser preview within the Agent pane
  2. **Visual Testing** : Watch Agent’s cursor as it clicks around your app, testing functionality
  3. **Real User Simulation** : Agent navigates through your application just like a real user would, entering mock data when necessary
  4. **Automatic Analysis** : Agent analyzes the test results and identifies any issues
  5. **Self-Correction** : Agent reports back with a summary of its tests and automatically fixes any issues that crop up



## 

​

Key capabilities

Agent intelligently tests your application by navigating through it like a real user would, covering:

  * **User interface validation** : Buttons, forms, navigation, and visual elements
  * **Functionality verification** : Core features and user workflows
  * **Integration testing** : API calls, database interactions, and third-party services
  * **Performance and accessibility** : Load times, responsiveness, and accessibility standards



## 

​

Usage

App Testing lives in **Advanced settings** inside the Agent settings dropdown in your chat input. Turn it on when you’re using Economy or Power mode. Lite mode keeps App Testing off.

App Testing is part of Agent’s autonomous capabilities. Learn more about [Code Optimizations](/core-concepts/agent/code-optimizations) and other [Agent features](/core-concepts/agent).

## 

​

Take over

Sometimes the Agent will encounter a roadblock during testing that it needs your help with to continue. Most commonly this involves logging in to a user account (e.g. Gmail). In these cases, the Agent will pop up with a button to “Begin take over.”

Pressing “Begin take over” enables you to click into the testing preview, complete the requisite steps, then allow the Agent to continue. You can also press “Skip” to skip take over, ending the App Testing if the Agent cannot proceed without your help. If you do not respond within 10 minutes, the Agent will continue as if you pressed “Skip.”

### 

​

What to expect

  * **Skip option** : Use the skip button to bypass testing if needed and continue with development
  * **Interactive video replay** : After testing, click the video to replay the entire testing session
  * **Section navigation** : Use the sliders at the bottom to jump to specific sections of the test

The interactive replay interface allows you to review the complete testing session:

## 

​

Troubleshooting

**Tests failing unexpectedly**

  * Try skipping then prompting again to test
  * Check for dynamic content that might affect test timing
  * Review test scenarios for accuracy

**Missing test coverage**

  * Provide more detailed descriptions of your app’s functionality
  * Explicitly mention critical user flows that should be tested

**App Testing not working at all?**

  * App Testing only works with web applications* at this time



## 

​

Pricing and usage

App Testing is included as part of Agent’s effort-based pricing model with important cost considerations:

  * **Usage-based** : Testing is charged based on the effort spent (simpler tests are less expensive)
  * **Cost vs. Benefit** : While testing costs money, it can save costs by avoiding additional prompts and extra work from Agent by catching mistakes earlier
  * **Efficient Development** : Automated approach reduces the need for manual debugging and rework



**Cost-Effective Testing** : Although App Testing adds to your usage costs, it often saves money overall by preventing the need for additional Agent sessions to fix issues that could have been caught during testing.

## 

​

Next steps

Ready to use App Testing with your projects?

  1. **Start Building** : Create an app with Agent and let testing activate automatically
  2. **Review Results** : Examine test reports and implement suggested improvements
  3. **Iterate** : Use test feedback to refine your application
  4. **Scale Up** : Apply App Testing to larger, more complex projects

Learn more about [Replit Agent](/core-concepts/agent) and its full capabilities.

Was this page helpful?

YesNo

[Agent ModesPrevious](/core-concepts/agent/agent-modes)[Code OptimizationsNext](/core-concepts/agent/code-optimizations)

⌘I

[x](https://x.com/replit)[linkedin](https://www.linkedin.com/company/repl-it)[youtube](https://www.youtube.com/@replit)

On this page

  * How App Testing works
  * Key Benefits
  * The Testing Process
  * Key capabilities
  * Usage
  * Take over
  * What to expect
  * Troubleshooting
  * Pricing and usage
  * Next steps


