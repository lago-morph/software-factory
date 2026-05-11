Toggle navigation[**OpenReview**.net](/)

  * [Login](/login)



[Go to **ICLR 2023 Conference** homepage](/group?id=ICLR.cc/2023/Conference "Venue Homepage")

## CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis[](/pdf?id=iaYcJKpY2B_ "Download PDF")

### [Erik Nijkamp](/profile?id=~Erik_Nijkamp2 "~Erik_Nijkamp2"), [Bo Pang](/profile?id=~Bo_Pang4 "~Bo_Pang4"), [Hiroaki Hayashi](/profile?id=~Hiroaki_Hayashi1 "~Hiroaki_Hayashi1"), [Lifu Tu](/profile?id=~Lifu_Tu1 "~Lifu_Tu1"), [Huan Wang](/profile?id=~Huan_Wang1 "~Huan_Wang1"), [Yingbo Zhou](/profile?id=~Yingbo_Zhou1 "~Yingbo_Zhou1"), [Silvio Savarese](/profile?id=~Silvio_Savarese1 "~Silvio_Savarese1"), [Caiming Xiong](/profile?id=~Caiming_Xiong1 "~Caiming_Xiong1")

Published: 01 Feb 2023, Last Modified: 27 Feb 2023ICLR 2023 notable top 25%Readers:  Everyone

**Keywords :** Program synthesis, multi-turn generation, code generation, large language models, generative models

**TL;DR :** We open-source a large language models, CodeGen, for program synthesis and propose a multi-turn program synthesis benchmark for evaluation.

**Abstract :** Program synthesis strives to generate a computer program as a solution to a given problem specification, expressed with input-output examples or natural language descriptions. The prevalence of large language models advances the state-of-the-art for program synthesis, though limited training resources and data impede open access to such models. To democratize this, we train and release a family of large language models up to 16.1B parameters, called CODEGEN, on natural language and programming language data, and open source the training library JAXFORMER. We show the utility of the trained model by demonstrating that it is competitive with the previous state-of-the-art on zero-shot Python code generation on HumanEval. We further investigate the multi-step paradigm for program synthesis, where a single program is factorized into multiple prompts specifying subproblems. To this end, we construct an open benchmark, Multi-Turn Programming Benchmark (MTPB), consisting of 115 diverse problem sets that are factorized into multi-turn prompts. Our analysis on MTPB shows that the same intent provided to CODEGEN in multi-turn fashion significantly improves program synthesis over that provided as a single turn. We make the training library JAXFORMER and model checkpoints available as open source contribution: https://github.com/salesforce/CodeGen.

**Anonymous Url :** I certify that there is no URL (e.g., github page) that could be used to find authors’ identity.

**No Acknowledgement Section :** I certify that there is no acknowledgement section in this submission for double blind review.

**Code Of Ethics :** I acknowledge that I and all co-authors of this work have read and commit to adhering to the ICLR Code of Ethics

**Submission Guidelines :** Yes

**Please Choose The Closest Area That Your Submission Falls Into :** Deep Learning and representational learning

23 Replies

* * *

Loading

  * [About OpenReview](/about)
  * [Hosting a Venue](/group?id=OpenReview.net/Support)
  * [All Venues](/venues)



  * [Contact](/contact)
  * [Sponsors](/sponsors)
  * [**Donate**](/donate)



  * [FAQ](https://docs.openreview.net/getting-started/frequently-asked-questions)
  * [Terms of Use](/legal/terms) / [Privacy Policy](/legal/privacy)
  * [News](/group?id=OpenReview.net/News&referrer=\[Homepage\]\(/\))



  * [About OpenReview](/about)
  * [Hosting a Venue](/group?id=OpenReview.net/Support)
  * [All Venues](/venues)
  * [Sponsors](/sponsors)
  * [News](/group?id=OpenReview.net/News&referrer=\[Homepage\]\(/\))



  * [FAQ](https://docs.openreview.net/getting-started/frequently-asked-questions)
  * [Contact](/contact)
  * [**Donate**](/donate)
  * [Terms of Use](/legal/terms)
  * [Privacy Policy](/legal/privacy)



[OpenReview](/about) is a long-term project to advance science through improved peer review with legal nonprofit status. We gratefully acknowledge the support of the [OpenReview Sponsors](/sponsors). © 2026 OpenReview
