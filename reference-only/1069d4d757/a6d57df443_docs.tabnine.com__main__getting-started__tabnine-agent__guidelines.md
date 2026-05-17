bars[](/main)

search

circle-xmark

`⌘Ctrl``k`

[Tabnine websitechevron-down](https://www.tabnine.com/)[Contact Sales](https://www.tabnine.com/contact-us/?utm_source=docs&utm_medium=organic&utm_campaign=docs)

Moreellipsischevron-down

[](/main)

  * Welcomechevron-right

    * [Overviewchevron-right](/main)
    * [Support & Feedback](/main/welcome/support-and-feedback)

  * Getting startedchevron-right

    * [Installchevron-right](/main/getting-started/install)
    * [Quickstart Guidechevron-right](/main/getting-started/quickstart)
    * [Context Enginechevron-right](/main/getting-started/context-engine)
    * [Tabnine Agentchevron-right](/main/getting-started/tabnine-agent)

      * [How to Use Tabnine Agent](/main/getting-started/tabnine-agent/how-to-use-tabnine-agent)
      * [Guidelines](/main/getting-started/tabnine-agent/guidelines)
      * [mcpModel Context Protocol servers (MCP)](/main/getting-started/tabnine-agent/mcp-intro-and-setup)
      * [In-IDE Agent Settings](/main/getting-started/tabnine-agent/agent-settings)
      * [Agents in Action](/main/getting-started/tabnine-agent/agents-in-action)
      * [Admin Console](/main/getting-started/tabnine-agent/admin-console)

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

  1. [Getting started](/main/getting-started)chevron-right
  2. [Tabnine Agent](/main/getting-started/tabnine-agent)



# Guidelines

## 

hashtag

Guidelines Overview

Guidelines are a powerful feature of Tabnine Agents that allow you to define custom behaviors, workflow rules, and system prompts through simple Markdown files. Think of guidelines as custom instructions that shape how your agent behaves and operates within your specific development environment.

### 

hashtag

What are Guidelines?

Guidelines are Markdown files stored in your project’s `/.tabnine/guidelines/` directory that act as:

  * **Custom System Prompts** : Define how the agent should behave

  * **Workflow Rules** : Specify procedures and processes to follow

  * **Tool Instructions** : Control how and when tools should be used

  * **Team Standards** : Encode your team’s coding practices and conventions




### 

hashtag

Creating Guidelines

To add custom guidelines for use by Tabnine Agent, create a new directory called `.tabnine`.

This directory will either reside either 1) in your home directory or 2) on a per-project basis within your project directory.

After that, create a `/guidelines/` folder in the `/tabnine/` directory either in your Terminal or manually.

Once in the `.tabnine/guidelines/` directory, save a markdown file (`.md`) with written instructions in natural language. Tabnine Agent will interpret the text.

There is no _real_ structural requirement, but it is still a best practice to list the various guidelines in a _hierarchical structure_ for easy interpretation, both by Agents and other users.

Your location will resemble `$PROJECT_FOLDER/.tabnine/guidelines/appguidelines.md`.

As noted above, you can save multiple guideline files.

circle-info

Think of these in a similar fashion to the `agents.md` file that other agentic tools use.

Here is a common example of a `guidelines.md` file with hierarchical structure:

circle-info

It is recommended to keep your `guidelines.md` file to 500 lines or less.

### 

hashtag

Governance for Agentic Guidelines

(Released [5.26.0](/main/administering-tabnine/release-notes#v5.26.0))

In the Admin UI, navigate over to Agent Guidelines on the left-hand side of the page.

Beneath the **General Guideline** title, you can add your natural language guideline description. They will also be applicable to all your organization’s users and projects.

Guidelines that are input here will have the same effect as guidelines listed in your `guidelines.md` file, but they will take precedence over personal guidelines that exist in the `guidelines.md` file.

Last updated 1 month ago

Was this helpful?

  * Guidelines Overview
  * What are Guidelines?
  * Creating Guidelines
  * Governance for Agentic Guidelines



Was this helpful?

Copy
    
    
    # Team Coding Standards
    ## Overview
    This guideline defines our team's coding standards and practices for consistent code quality.
    ## Instructions
    ### Code Style- Use meaningful variable and function names
    - Follow language-specific naming conventions (camelCase for JavaScript, snake_case for Python)
    - Keep functions small and focused (max 20-30 lines)
    - Add comments for complex business logic
    ### Error Handling- Always handle errors gracefully
    - Use try-catch blocks for operations that might fail
    - Log errors with appropriate context
    - Provide user-friendly error messages
    ### Testing- Write unit tests for all new functions
    - Maintain minimum 80% code coverage
    - Include integration tests for API endpoints
    - Use descriptive test names that explain the scenario
    ## Examples
    Good variable naming:
    userAuthenticationToken = generateToken(user);
    const isValidEmail = validateEmailAddress(email);
    Bad variable naming:
    const t = generateToken(user);  // Too generic
    const flag = validateEmailAddress(email);  // Unclear purpose
