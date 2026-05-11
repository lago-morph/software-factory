Skip to content 

📣 We now recommend [mini-swe-agent](https://mini-swe-agent.com) instead of SWE-agent: Same performance, much more simple & flexible 

[ ](../.. "SWE-agent documentation")

SWE-agent documentation 

Agent tools 

Initializing search 




[ SWE-agent/SWE-agent  ](https://github.com/SWE-agent/SWE-agent "Go to repository")

  * [ Getting Started ](../..)
  * [ User Guides ](../../usage/)
  * [ API Reference ](../../reference/)



[ ](../.. "SWE-agent documentation") SWE-agent documentation 

[ SWE-agent/SWE-agent  ](https://github.com/SWE-agent/SWE-agent "Go to repository")

  * [ Getting Started  ](../..)

Getting Started 
    * [ Installation  ](../../installation/)

Installation 
      * [ From source  ](../../installation/source/)
      * [ In browser  ](../../installation/codespaces/)
      * [ Models and keys  ](../../installation/keys/)
      * [ 1.0 migration  ](../../installation/migration/)
      * [ Troubleshooting  ](../../installation/tips/)
      * [ Changelog  ](../../installation/changelog/)
    * Tutorials  Tutorials 
      * [ Hello world  ](../../usage/hello_world/)
      * [ Command line basics  ](../../usage/cl_tutorial/)
      * [ Solving coding challenges  ](../../usage/coding_challenges/)
      * [ Trajectory inspector  ](../../usage/inspector/)
      * [ Batch mode  ](../../usage/batch_mode/)
      * [ Competitive runs  ](../../usage/competitive_runs/)
      * [ Adding custom tools  ](../../usage/adding_custom_tools/)
      * [ What's next?  ](../../usage/whats_next/)
    * [ FAQ  ](../../faq/)
  * [ User Guides  ](../../usage/)

User Guides 
    * [ Project overview  ](../)

Project overview 
      * [ Architecture  ](../architecture/)
      * [ Agent tools  ](./)
    * [ Command line interface  ](../../usage/cli/)
    * [ Output files  ](../../usage/trajectories/)
    * [ Configuration  ](../../config/)

Configuration 
      * [ Config files  ](../../config/config/)
      * [ Templates  ](../../config/templates/)
      * [ Models  ](../../config/models/)
      * [ Demonstrations  ](../../config/demonstrations/)
      * [ Tools  ](../../config/tools/)
      * [ Environments  ](../../config/environments/)
    * Development  Development 
      * [ Contribution guide  ](../../dev/contribute/)
      * [ Formatting conflicts  ](../../dev/formatting_conflicts/)
  * [ API Reference  ](../../reference/)

API Reference 
    * Run config  Run config 
      * [ Run single  ](../../reference/run_single_config/)
      * [ Run batch  ](../../reference/run_batch_config/)
    * Instance config  Instance config 
      * [ Problem statements  ](../../reference/problem_statements/)
      * [ Repository  ](../../reference/repo/)
      * [ Batch instances  ](../../reference/batch_instances/)
    * Agent config  Agent config 
      * [ Agent config  ](../../reference/agent_config/)
      * [ Model config  ](../../reference/model_config/)
      * [ Templates  ](../../reference/template_config/)
      * [ Tools  ](../../reference/tools_config/)
      * [ History processors  ](../../reference/history_processor_config/)
      * [ Action parsers  ](../../reference/parsers/)
    * [ Environment config  ](../../reference/env_config/)
    * [ Tool bundle config  ](../../reference/bundle_config/)
    * Classes  Classes 
      * [ Agent class  ](../../reference/agent/)
      * [ Environment class  ](../../reference/env/)
      * [ Exceptions  ](../../reference/exceptions/)



[ ](https://github.com/SWE-agent/SWE-agent/edit/main/docs/background/aci.md "Edit this page")

# Agent Computer Interface (ACI)

SWE-agent is built on the idea of an **Agent-Computer Interface** (ACI). An ACI is essentially an a set of tools and interaction format that allows an agent to interact with a computer-based environment, to perform tasks, such as software engineering. The SWE-agent repository is built to make it easy to invent new ACIs for agents to solve various tasks.

Just like how typical language models requires good prompt engineering, **good ACI design leads to much better results when using agents**. As we show in the SWE-agent [paper](https://arxiv.org/abs/2405.15793), a baseline agent without a well-tuned ACI does much worse than SWE-agent.

SWE-agent contains features that we discovered to be immensely helpful during the agent-computer interface design process:

  1. We add a **linter** that runs when an edit command is issued, and do not let the edit command go through if the code isn't syntactically correct.
  2. We supply the agent with a **special-built file viewer** , instead of having it just `cat` files. We found that this file viewer works best when displaying just 100 lines in each turn. The **file editor** that we built has commands for scrolling up and down and for performing a search within the file.
  3. We supply the agent with a special-built full-directory string **searching command**. We found that it was important for this tool to succinctly list the matches- we simply list each file that had at least one match. Showing the model more context about each match proved to be too confusing for the model.
  4. When commands have an empty output we return a message saying "Your command ran successfully and did not produce any output."



Read our paper for more details [here](https://arxiv.org/abs/2405.15793).

SWE-agent has been superseded by **mini-swe-agent**.

mini-swe-agent is simpler & more flexible while still being as performant.

See the [FAQ](https://mini-swe-agent.com/latest/faq/) for more details about why you should switch.   
SWE-agent is now in maintenance-only mode.

[ Check out mini-swe-agent ](https://mini-swe-agent.com) Continue to SWE-agent 

Our projects

[ Mini-SWE-Agent ](https://mini-swe-agent.com/ "Mini-SWE-Agent") [ SWE-ReX ](https://swe-rex.com/ "SWE-rex") [ SWE-smith ](https://swesmith.com "SWE-smith") [ SWE-bench ](https://swebench.com "SWE-bench") [ sb-cli ](https://www.swebench.com/sb-cli/ "sb-cli")

Back to top  [ Previous  Architecture  ](../architecture/) [ Next  Command line interface  ](../../usage/cli/)

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
