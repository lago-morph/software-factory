[SWE-bench](/) __

[SWE-bench](/) __

  * [Leaderboards](index.html)
  * Benchmarks
  * [SWE-bench](original.html)
  * [SWE-bench Verified](verified.html)
  * [SWE-bench Multilingual](multilingual-leaderboard.html)
  * [SWE-bench Multimodal](multimodal.html)
  * [SWE-bench Lite](lite.html)
  * About
  * [Paper __](https://openreview.net/pdf?id=VTF8yNQM66)
  * [Docs __](https://swebench.com/SWE-bench/)
  * [Blog](blog.html)
  * [Contact](contact.html)
  * [Citations](citations.html)
  * [Press](press.html)
  * [Submit](submit.html)
  * SWE-bench Family
  * [mini-SWE-agent __](https://mini-swe-agent.com/)
  * [ SWE-smith __](https://swesmith.com/)
  * [ CodeClash __](https://codeclash.ai/)
  * [ SWE-ReX __](https://swe-rex.com/latest/)
  * [ SWE-bench CLI __](https://swebench.com/sb-cli/)
  * [ SWE-agent (legacy) __](https://swe-agent.com/latest/)



[ __](https://github.com/swe-bench/SWE-bench)   [ __](https://www.youtube.com/@SWE-bench)   [ __](https://twitter.com/SWEbench)   [ __](https://join.slack.com/t/swe-bench/shared_invite/zt-3rljl10bn-WED_gNRuFQu6YcILJMgeSw) __

# SWE-bench

Can Language Models Resolve Real-world Github Issues?

Carlos E. Jimenez*, John Yang*, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik R Narasimhan   
*Equal contribution

  


[Paper](https://arxiv.org/abs/2310.06770) [GitHub](https://github.com/SWE-bench/SWE-bench) [Dataset](https://huggingface.co/datasets/SWE-bench/SWE-bench)

## Overview

SWE-bench tests AI systems' ability to solve GitHub issues.

We collect 2,294 task instances by crawling Pull Requests and Issues from 12 popular Python repositories. Each instance is based on a pull request that (1) is associated with an issue, and (2) modified 1+ testing related files. 

Per instance, we construct an execution environment (Docker Image) with the repository successfully installed at the commit that the Pull Request is based on. Without the Pull Request's changes, a number of test(s) fail. After the Pull Request is merged, the same set of test(s) pass. These "Fail-to-Pass" tests are the primary signal for evaluation. 

SWE-bench evaluation works as follows. Per task instance, an AI system is given the issue text. The AI system should then modify the codebase in order to resolve the described issues. When the AI system is finished, we run the aforementioned Fail-to-Pass tests to check if the issue was successfully resolved. 

SWE-bench was released in October 2023, where our initial Retrieval Augmented Generation (RAG) baseline scored just 1.96%. Our follow up work, [SWE-agent](https://swe-agent.com/latest/), was the first agent-based AI system ever introduced for performing software engineering tasks, achieving a score of 12.47% on SWE-bench. You can train your own agentic software engineering models using our [SWE-smith](https://swesmith.com/) dataset. 

* * *

## Resources

In the original SWE-bench work, we fine-tuned CodeLlama ([Rozière et al. 2023](https://arxiv.org/abs/2308.12950)) to directly generate patches given 1+ files along with the issue text. We provide all assets, including the training data and model weights, for the SWE-Llama models. 

Base and pre-processed datasets (Oracle, 13K, 27K, 40K, 50K Llama) are available on HuggingFace.

[🤗 SWE-bench](https://huggingface.co/datasets/princeton-nlp/SWE-bench) [🤗 "Oracle" Retrieval](https://huggingface.co/datasets/princeton-nlp/SWE-bench_oracle) [🤗 BM25 Retrieval 13K](https://huggingface.co/datasets/princeton-nlp/SWE-bench_bm25_13K) [🤗 BM25 Retrieval 27K](https://huggingface.co/datasets/princeton-nlp/SWE-bench_bm25_27K) [🤗 BM25 Retrieval 40K](https://huggingface.co/datasets/princeton-nlp/SWE-bench_bm25_40K) [🤗 BM25 Retrieval 50K (Llama)](https://huggingface.co/datasets/princeton-nlp/SWE-bench_bm25_50k_llama)

SWE-Llama model weights:

[SWE-Llama 13b](https://huggingface.co/princeton-nlp/SWE-Llama-13b) [SWE-Llama 13b (PEFT)](https://huggingface.co/princeton-nlp/SWE-Llama-13b-peft) [SWE-Llama 7b](https://huggingface.co/princeton-nlp/SWE-Llama-7b) [SWE-Llama 7b (PEFT)](https://huggingface.co/princeton-nlp/SWE-Llama-7b-peft)

* * *

## Citation

If you use SWE-bench in your research, please cite our paper:

BibTeX APA MLA

Copy
    
    
    @inproceedings{
        jimenez2024swebench,
        title={{SWE}-bench: Can Language Models Resolve Real-world Github Issues?},
        author={Carlos E Jimenez and John Yang and Alexander Wettig and Shunyu Yao and Kexin Pei and Ofir Press and Karthik R Narasimhan},
        booktitle={The Twelfth International Conference on Learning Representations},
        year={2024},
        url={https://openreview.net/forum?id=VTF8yNQM66}
    }

Copy
    
    
    Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. R. (2024). SWE-bench: Can Language Models Resolve Real-world Github Issues? In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=VTF8yNQM66

Copy
    
    
    Jimenez, Carlos E., et al. "SWE-bench: Can Language Models Resolve Real-world Github Issues?" The Twelfth International Conference on Learning Representations, 2024.

(C) 2025 SWE-bench Team. All rights reserved. 

[GitHub](https://github.com/swe-bench/SWE-bench) [HuggingFace](https://huggingface.co/collections/SWE-bench/benchmarks-68113bc99eb3a64a91ea33c9) [Paper](https://arxiv.org/abs/2310.06770)
