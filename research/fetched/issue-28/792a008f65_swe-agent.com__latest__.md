Skip to content 

📣 We now recommend [mini-swe-agent](https://mini-swe-agent.com) instead of SWE-agent: Same performance, much more simple & flexible 

[ ](. "SWE-agent documentation")

SWE-agent documentation 

Getting Started 

Initializing search 




[ SWE-agent/SWE-agent  ](https://github.com/SWE-agent/SWE-agent "Go to repository")

  * [ Getting Started ](.)
  * [ User Guides ](usage/)
  * [ API Reference ](reference/)



[ ](. "SWE-agent documentation") SWE-agent documentation 

[ SWE-agent/SWE-agent  ](https://github.com/SWE-agent/SWE-agent "Go to repository")

  * [ Getting Started  ](.)

Getting Started 
    * [ Installation  ](installation/)

Installation 
      * [ From source  ](installation/source/)
      * [ In browser  ](installation/codespaces/)
      * [ Models and keys  ](installation/keys/)
      * [ 1.0 migration  ](installation/migration/)
      * [ Troubleshooting  ](installation/tips/)
      * [ Changelog  ](installation/changelog/)
    * Tutorials  Tutorials 
      * [ Hello world  ](usage/hello_world/)
      * [ Command line basics  ](usage/cl_tutorial/)
      * [ Solving coding challenges  ](usage/coding_challenges/)
      * [ Trajectory inspector  ](usage/inspector/)
      * [ Batch mode  ](usage/batch_mode/)
      * [ Competitive runs  ](usage/competitive_runs/)
      * [ Adding custom tools  ](usage/adding_custom_tools/)
      * [ What's next?  ](usage/whats_next/)
    * [ FAQ  ](faq/)
  * [ User Guides  ](usage/)

User Guides 
    * [ Project overview  ](background/)

Project overview 
      * [ Architecture  ](background/architecture/)
      * [ Agent tools  ](background/aci/)
    * [ Command line interface  ](usage/cli/)
    * [ Output files  ](usage/trajectories/)
    * [ Configuration  ](config/)

Configuration 
      * [ Config files  ](config/config/)
      * [ Templates  ](config/templates/)
      * [ Models  ](config/models/)
      * [ Demonstrations  ](config/demonstrations/)
      * [ Tools  ](config/tools/)
      * [ Environments  ](config/environments/)
    * Development  Development 
      * [ Contribution guide  ](dev/contribute/)
      * [ Formatting conflicts  ](dev/formatting_conflicts/)
  * [ API Reference  ](reference/)

API Reference 
    * Run config  Run config 
      * [ Run single  ](reference/run_single_config/)
      * [ Run batch  ](reference/run_batch_config/)
    * Instance config  Instance config 
      * [ Problem statements  ](reference/problem_statements/)
      * [ Repository  ](reference/repo/)
      * [ Batch instances  ](reference/batch_instances/)
    * Agent config  Agent config 
      * [ Agent config  ](reference/agent_config/)
      * [ Model config  ](reference/model_config/)
      * [ Templates  ](reference/template_config/)
      * [ Tools  ](reference/tools_config/)
      * [ History processors  ](reference/history_processor_config/)
      * [ Action parsers  ](reference/parsers/)
    * [ Environment config  ](reference/env_config/)
    * [ Tool bundle config  ](reference/bundle_config/)
    * Classes  Classes 
      * [ Agent class  ](reference/agent/)
      * [ Environment class  ](reference/env/)
      * [ Exceptions  ](reference/exceptions/)



Table of contents 

  * 📣 News 
  * ✍️ Doc updates 



[ ](https://github.com/SWE-agent/SWE-agent/edit/main/docs/index.md "Edit this page")

# Getting Started

[](assets/readme_assets/swe-agent-banner-light.svg) [](assets/readme_assets/swe-agent-banner-dark.svg)

We recommend mini-swe-agent instead of SWE-agent

Most of our current development effort is on [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent/), which has superseded SWE-agent. It matches the performance of SWE-agent, while being much simpler. See the [FAQ](https://mini-swe-agent.com/latest/faq/) for more details about the differences.

SWE-agent enables your language model of choice (e.g. GPT-4o or Claude Sonnet 4) to autonomously use tools to [fix issues in real GitHub repositories](https://swe-agent.com/latest/usage/hello_world), [find cybersecurity vulnerabilities](https://enigma-agent.com/), or [perform any custom task](https://swe-agent.com/latest/usage/coding_challenges).

  * ✅ **State of the art** on SWE-bench among open-source projects
  * ✅ **Free-flowing & generalizable**: Leaves maximal agency to the LM
  * ✅ **Configurable & fully documented**: Governed by a single `yaml` file
  * ✅ **Made for research** : Simple & hackable by design



SWE-agent is built and maintained by researchers from Princeton University and Stanford University.

[ download Installation Installing SWE-agent. ](installation/) [ settings Hello world Solve a GitHub issue with SWE-agent. ](usage/hello_world/) [ lightbulb User guides Dive deeper into SWE-agent's features and goals. ](usage/) [ book Background & goals Learn more about the project goals and academic research. ](background/)

## 📣 News

  * July 24: [Mini-SWE-Agent](https://github.com/SWE-agent/mini-SWE-agent) achieves 65% on SWE-bench verified in 100 lines of python!
  * July 9: [Multimodal support for SWE-agent](usage/multimodal/) \- Process images from GitHub issues with vision-capable AI models
  * May 2: [SWE-agent-LM-32b](https://swesmith.com) achieves open-weights SOTA on SWE-bench
  * Feb 28: [SWE-agent 1.0 + Claude 3.7 is SoTA on SWE-Bench full](https://x.com/KLieret/status/1895487966409298067)
  * Feb 25: [SWE-agent 1.0 + Claude 3.7 is SoTA on SWE-bench verified](https://x.com/KLieret/status/1894408819670733158)
  * Feb 13: [Releasing SWE-agent 1.0: SoTA on SWE-bench light & tons of new features](https://x.com/KLieret/status/1890048205448220849)
  * Dec 7: [An interview with the SWE-agent & SWE-bench team](https://www.youtube.com/watch?v=fcr8WzeEXyk)



## ✍️ Doc updates

  * June 26: [Adding custom tools](usage/adding_custom_tools/)
  * Apr 8: [Running SWE-agent competitively](usage/competitive_runs/)
  * Mar 7: [Updated SWE-agent architecture diagram of 1.0](background/architecture/)



SWE-agent has been superseded by **mini-swe-agent**.

mini-swe-agent is simpler & more flexible while still being as performant.

See the [FAQ](https://mini-swe-agent.com/latest/faq/) for more details about why you should switch.   
SWE-agent is now in maintenance-only mode.

[ Check out mini-swe-agent ](https://mini-swe-agent.com) Continue to SWE-agent 

Our projects

[ Mini-SWE-Agent ](https://mini-swe-agent.com/ "Mini-SWE-Agent") [ SWE-ReX ](https://swe-rex.com/ "SWE-rex") [ SWE-smith ](https://swesmith.com "SWE-smith") [ SWE-bench ](https://swebench.com "SWE-bench") [ sb-cli ](https://www.swebench.com/sb-cli/ "sb-cli")

Back to top  [ Next  Setting up SWE-agent  ](installation/)

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
