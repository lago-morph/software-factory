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

Features

replit.md




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

      * [Agent Skills](/core-concepts/agent/skills)
      * [Agents & Automations](/core-concepts/agent/agents-and-automations)
      * [Automation examples](/core-concepts/agent/automation-examples)
      * [General Agent](/core-concepts/agent/general-agent)
      * [Image Generation](/core-concepts/agent/image-generation)
      * [Message Queue](/core-concepts/agent/message-queue)
      * [replit.md](/core-concepts/agent/replit-dot-md)
      * [Web Search](/core-concepts/agent/web-search)
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



Features

# replit.md

Copy page

Learn how to use replit.md to customize Agent’s behavior, coding style, and project context.

Copy page

> ## Documentation Index
> 
> Fetch the complete documentation index at: <https://docs.replit.com/llms.txt>
> 
> Use this file to discover all available pages before exploring further.

Agent automatically creates this file in your project’s root directory using proven best practices. Agent includes its contents in the context to help it understand your preferences, project structure, and coding style.

## 

​

How `replit.md` works

Agent first creates a `replit.md` file in your project’s root directory using proven best practices. This file includes:

  * Basic project information
  * Recommended coding patterns
  * Common preferences for your project type

When Agent processes your requests, it automatically reads your `replit.md` file and uses its contents to:

  * Understand your project’s architecture and conventions
  * Follow your preferred coding patterns and style
  * Use your specified package managers and dependencies

Agent can also update your `replit.md` file as it learns more about your project and makes changes to your application.

You can edit the `replit.md` file to customize Agent’s behavior.

## 

​

Setting up `replit.md`

### 

​

Automatic generation

When you create a new project with Agent, it automatically generates a `replit.md` file using proven best practices. This file appears in your project’s root directory and includes:

  * Basic project information
  * Recommended coding patterns
  * Common preferences for your project type



### 

​

Manual creation

You can create your own `replit.md` file by adding a new file named `replit.md` in your project’s root directory. Agent will automatically detect and use this file in future conversations.

`replit.md` must be located in your project’s root directory to work properly.

### 

​

Regenerating `replit.md`

If your `replit.md` file becomes corrupted or you want to start fresh:

  1. Delete the existing `replit.md` file from your project root
  2. Start a new conversation with Agent
  3. Agent will automatically generate a new `replit.md` file based on your current project



## 

​

Best practices

### 

​

Be specific and clear

Write clear, specific instructions that help Agent understand exactly what you want:
    
    
    ## Coding Style
    
    - Use TypeScript for all new JavaScript files
    - Prefer functional components with hooks over class components
    - Use Tailwind CSS for styling, avoid inline styles
    - Always include TypeScript types for function parameters and return values
    

For a more detailed guide on prompt formatting, check out the [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags).

### 

​

Use examples

Examples help Agent understand your preferences better than abstract descriptions:
    
    
    ## API Error Handling
    
    When creating API endpoints, always use this error handling pattern:
    
    ```javascript
    app.get('/api/users', async (req, res) => {
      try {
        const users = await getUsersFromDatabase();
        res.json({ success: true, data: users });
      } catch (error) {
        console.error('Error fetching users:', error);
        res.status(500).json({ 
          success: false, 
          error: 'Failed to fetch users' 
        });
      }
    });
    

### 

​

Define communication preferences

Tell Agent how you prefer to receive information and updates:
    
    
    ## Communication Style
    
    - Before implementing changes, explain what you're going to do and why
    - Break down complex tasks into clear steps
    - Ask for clarification if requirements are unclear
    - Provide brief explanations for technical decisions
    

### 

​

Specify project context

Help Agent understand your project’s purpose and constraints:
    
    
    ## Project Context
    
    This is a social media app for book lovers where users can:
    - Create reading lists and share book recommendations
    - Follow other readers and see their updates
    - Rate and review books they've read
    
    Target audience: Casual readers aged 25-45
    Tech stack: React frontend, Node.js backend, PostgreSQL database
    

## 

​

Example `replit.md` configurations

### 

​

Web application project
    
    
    # MyApp Project Guidelines
    
    ## Project Overview
    A task management web application built with React and Express.js.
    
    ## Technology Preferences
    - Frontend: React with TypeScript, Tailwind CSS
    - Backend: Express.js with TypeScript
    - Database: Neon PostgreSQL with Drizzle ORM
    - Package Manager: npm (not yarn or pnpm)
    
    ## Coding Standards
    - Use functional components with hooks
    - Implement proper error boundaries
    - Follow REST API conventions for endpoints
    - Use descriptive variable and function names
    
    ## Communication Style
    - Explain your approach before making changes
    - Provide code comments for complex logic
    - Ask questions if requirements are ambiguous
    

### 

​

Data analysis project
    
    
    # Data Analysis Project Guidelines
    
    ## Project Context
    Analyzing customer behavior data to identify trends and insights.
    
    ## Technology Preferences
    - Python with Streamlit for interactive web applications
    - pandas, numpy, and matplotlib for data analysis
    
    ## Analysis Standards
    - Include clear documentation for all analysis steps
    - Create interactive visualizations with Streamlit components
    - Validate data quality before analysis
    - Export results to CSV format and display in Streamlit tables
    
    ## Communication Style
    - Explain statistical methods and assumptions
    - Provide context for findings and recommendations
    - Use clear, non-technical language for business insights
    - Create interactive dashboards for stakeholder presentations
    

### 

​

API development project
    
    
    # API Development Guidelines
    
    ## Project Overview
    Building a RESTful API for a mobile app backend.
    
    ## Technology Stack
    - Node.js with Express.js
    - MongoDB with Mongoose
    - JWT for authentication
    - Package manager: npm
    
    ## API Standards
    - Use semantic HTTP status codes
    - Implement proper input validation
    - Include rate limiting on public endpoints
    - Follow OpenAPI specification for documentation
    
    ## Security Requirements
    - Validate all user inputs
    - Use environment variables for sensitive data
    - Implement proper CORS policies
    - Include request logging for debugging
    
    ## Testing Approach
    - Write unit tests for all endpoints
    - Include integration tests for critical flows
    - Use Jest as the testing framework
    

## 

​

Advanced usage

### 

​

Dynamic project guidance

Update your `replit.md` file as your project evolves to provide current context:
    
    
    ## Current Development Phase
    The team is currently focused on implementing user authentication.
    Priority features:
    1. User registration and login
    2. Password reset functionality  
    3. Email verification
    
    ## Recent Decisions
    - Switched from local authentication to OAuth with Google
    - Added Redux for state management
    - Decided to use Material-UI for consistent styling
    

### 

​

Integration with external tools

Reference external documentation and tools in your `replit.md`:
    
    
    ## External Resources
    - Design system: Follow the Figma design system at [link]
    - API documentation: Reference our internal API docs
    - Coding standards: Follow the team style guide in our wiki
    
    ## Deployment Process
    - Test changes in development environment first
    - Use the CI/CD pipeline for staging published apps
    - Require code review before production releases
    

## 

​

Combining web search with `replit.md`

Agent can perform web searches to find current information, libraries, and solutions. When combined with your `replit.md` file, you get both up-to-date knowledge and project-specific guidance.

### 

​

Best practices for web search integration

**Be specific about what you want Agent to research:**
    
    
    ## Research Preferences
    - Always check for the latest versions of dependencies before suggesting updates
    - Research current best practices for security implementations
    - Look up recent performance optimization techniques for our tech stack
    

**Guide Agent on how to apply external knowledge:**
    
    
    ## External Research Guidelines
    - When suggesting new libraries, ensure compatibility with our existing stack
    - Adapt external examples to match our coding standards and project structure  
    - Verify that suggested solutions work with our publishing environment
    

**Example request that leverages both:** “Research the latest React 18 performance optimization techniques and implement them following the component patterns defined in `replit.md`” This approach gives you solutions that are both current and tailored to your specific project needs.

## 

​

Limitations

### 

​

File size and content limits

While there’s no strict character limit for `replit.md`, extremely large files may not be fully processed. Keep your `replit.md` focused and concise for best results.

### 

​

Root directory requirement

`replit.md` must exist in your project’s root directory. Agent won’t automatically detect files in subdirectories.

### 

​

Context scope

`replit.md` provides context for Agent conversations but doesn’t automatically apply to other AI tools.

## 

​

Next steps

Ready to customize Agent for your project?

  1. **Start simple** : Create a basic `replit.md` with your key preferences
  2. **Iterate and improve** : Update your `replit.md` as you work with Agent
  3. **Share patterns** : Use successful `replit.md` configurations across similar projects
  4. **Monitor effectiveness** : Pay attention to how well Agent follows your guidelines and adjust accordingly

Learn more about [working with Agent](/core-concepts/agent) or explore other [AI tools](/core-concepts/how-replit-works). **Enterprise** : Pre-configure `replit.md` in [custom templates](/teams/custom-templates) to give every builder in your organization a consistent starting context. For design-specific guidance, see [setting up a design system](/teams/custom-design-system).

Was this page helpful?

YesNo

[Message QueuePrevious](/core-concepts/agent/message-queue)[Web SearchNext](/core-concepts/agent/web-search)

⌘I

[x](https://x.com/replit)[linkedin](https://www.linkedin.com/company/repl-it)[youtube](https://www.youtube.com/@replit)

On this page

  * How replit.md works
  * Setting up replit.md
  * Automatic generation
  * Manual creation
  * Regenerating replit.md
  * Best practices
  * Be specific and clear
  * Use examples
  * Define communication preferences
  * Specify project context
  * Example replit.md configurations
  * Web application project
  * Data analysis project
  * API development project
  * Advanced usage
  * Dynamic project guidance
  * Integration with external tools
  * Combining web search with replit.md
  * Best practices for web search integration
  * Limitations
  * File size and content limits
  * Root directory requirement
  * Context scope
  * Next steps


