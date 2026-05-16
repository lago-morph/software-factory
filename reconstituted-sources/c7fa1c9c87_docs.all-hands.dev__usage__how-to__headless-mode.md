Skip to main content

[OpenHands Docs home page](/)

Search...

⌘KAsk AI

  * [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands "OpenHands/OpenHands")
  * [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands "OpenHands/OpenHands")



Search...

Navigation

Ways to Run

Headless Mode

[Documentation](/overview/introduction)[Use Cases](/openhands/usage/use-cases/overview)[SDK](/sdk)[CLI](/openhands/usage/cli/installation)[Cloud](/openhands/usage/cloud/openhands-cloud)[Enterprise](/enterprise)

##### Getting Started

  * [Installation](/openhands/usage/cli/installation)
  * [Quick Start](/openhands/usage/cli/quick-start)



##### Ways to Run

  * [Terminal (CLI)](/openhands/usage/cli/terminal)
  * [Headless Mode](/openhands/usage/cli/headless)
  * [Web Interface](/openhands/usage/cli/web-interface)
  * [GUI Server](/openhands/usage/cli/gui-server)
  * IDE Integration (ACP)




##### Cloud

  * [OpenHands Cloud](/openhands/usage/cli/cloud)



##### Extensions

  * [MCP Servers](/openhands/usage/cli/mcp-servers)
  * [Critic (Experimental)](/openhands/usage/cli/critic)



##### Reference

  * [Command Reference](/openhands/usage/cli/command-reference)
  * [Resume Conversations](/openhands/usage/cli/resume)



On this page

  * Overview
  * Requirements
  * Basic Usage
  * JSON Output Mode
  * Use Cases for JSON Output
  * Example: Capture Output to File
  * See Also



Ways to Run

# Headless Mode

Copy page

Run OpenHands without UI for scripting, automation, and CI/CD pipelines

Copy page

> ## Documentation Index
> 
> Fetch the complete documentation index at: <https://docs.openhands.dev/llms.txt>
> 
> Use this file to discover all available pages before exploring further.

## 

​

Overview

Headless mode runs OpenHands without the interactive terminal UI, making it ideal for:

  * CI/CD pipelines
  * Automated scripting
  * Integration with other tools
  * Batch processing


    
    
    openhands --headless -t "Your task here"
    

## 

​

Requirements

  * Must specify a task with `--task` or `--file`



**Headless mode always runs in`always-approve` mode.** The agent will execute all actions without any confirmation. This cannot be changed—`--llm-approve` is not available in headless mode.

## 

​

Basic Usage
    
    
    # Run a task in headless mode
    openhands --headless -t "Write a Python script that prints hello world"
    
    # Load task from a file
    openhands --headless -f task.txt
    

## 

​

JSON Output Mode

The `--json` flag enables structured JSONL (JSON Lines) output, streaming events as they occur:
    
    
    openhands --headless --json -t "Create a simple Flask app"
    

Each line is a JSON object representing an agent event:
    
    
    {"type": "action", "action": "write", "path": "app.py", ...}
    {"type": "observation", "content": "File created successfully", ...}
    {"type": "action", "action": "run", "command": "python app.py", ...}
    

### 

​

Use Cases for JSON Output

  * **CI/CD pipelines** : Parse events to determine success/failure
  * **Automated processing** : Feed output to other tools
  * **Logging** : Capture structured logs for analysis
  * **Integration** : Connect OpenHands with other systems



### 

​

Example: Capture Output to File
    
    
    openhands --headless --json -t "Add unit tests" > output.jsonl
    

## 

​

See Also

  * [Terminal Mode](/openhands/usage/cli/terminal) \- Interactive CLI usage
  * [Command Reference](/openhands/usage/cli/command-reference) \- All CLI options



Was this page helpful?

YesNo

[Terminal (CLI)](/openhands/usage/cli/terminal)[Web Interface](/openhands/usage/cli/web-interface)

⌘I

[OpenHands Docs home page](/)

[slack](https://openhands.dev/joinslack)[github](https://github.com/OpenHands/OpenHands)

[Company](https://openhands.dev/)[Blog](https://openhands.dev/blog)[Cloud](https://app.all-hands.dev)[Enterprise](https://openhands.dev/enterprise)

[slack](https://openhands.dev/joinslack)[github](https://github.com/OpenHands/OpenHands)

[Powered byThis documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=allhandsai)

Assistant

Responses are generated using AI and may contain mistakes.

[Contact support](mailto:contact@openhands.dev)
