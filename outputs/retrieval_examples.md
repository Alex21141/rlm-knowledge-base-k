# HW2: Semantic Retrieval — Test Results

**Embedding model:** sentence-transformers/all-MiniLM-L6-v2
**FAISS index:** IndexFlatIP, 467 vectors
**Chunks:** 467
**Queries:** 10
**Top-k:** 5

---

Query: How does the RLM REPL architecture process user prompts that exceed the base model's fixed context window?

Top-1: rlm_comprehensive_guide_chunk_026 | score: 0.7659
  Text: r context for certain problems. LMs can more efficiently solve problems when only looking locally at  certain parts of their input. The REPL environment provides a programmatic way for the model to pe
  Source: data/raw/rlm_comprehensive_guide.md

Top-2: rlm_comprehensive_guide_chunk_008 | score: 0.7175
  Text: too large. The recursion bottoms out when chunks fit comfortably in the base model's context window.  ### Three Design Choices That Make RLMs Different from "Just Using Agents"  The paper identifies t
  Source: data/raw/rlm_comprehensive_guide.md

Top-3: rlm_comprehensive_guide_chunk_005 | score: 0.7101
  Text: 2. **Provide metadata, not content.** The root model receives only constant-size metadata about P: its length, a short prefix, how to access slices of it. The full text of P never enters the model's c
  Source: data/raw/rlm_comprehensive_guide.md

Top-4: llm_reasoning_paradigms_evolution_chunk_019 | score: 0.693
  Text: esent a fundamental rethinking of how language models interact with information. Instead of treating  the prompt as a fixed token sequence, RLMs treat context as a variable in an external environment 
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-5: alexzhang_blog_context_rot_chunk_007 | score: 0.6695
  Text: ar-infinite context lengths. An RLM allows a language model to interact with an environment (in this  instance, a REPL environment) that stores the (potentially huge) context, where it can recursively
  Source: data/raw/alexzhang_blog_context_rot.md

---

Query: What is context rot in recursive language models and how does it affect performance on long-context tasks?

Top-1: rlm_original_paper_chunk_004 | score: 0.8503
  Text: ndles them effectively. Additional experiments across other models, methods, and benchmarks are in §  [2](https://arxiv.org/html/2512.24601v1#S2 "2 Scaling Long Context Tasks ‣ Recursive Language Mode
  Source: data/raw/rlm_original_paper.md

Top-2: rlm_candemir_medium_chunk_003 | score: 0.7385
  Text: ken in one pass. It has to hold the entire context in its "working memory" simultaneously. For short  inputs, this works beautifully. For long inputs, things start to fall apart.  ## What Is Context R
  Source: data/raw/rlm_candemir_medium.md

Top-3: alexzhang_blog_context_rot_chunk_062 | score: 0.7234
  Text: ce sampling methods over a set of candidate responses.  ## What We’re Thinking Now & for the Future.  Long-context capabilities in language models used to be a model architecture problem (think ALiBi,
  Source: data/raw/alexzhang_blog_context_rot.md

Top-4: alexzhang_blog_context_rot_chunk_007 | score: 0.7087
  Text: ar-infinite context lengths. An RLM allows a language model to interact with an environment (in this  instance, a REPL environment) that stores the (potentially huge) context, where it can recursively
  Source: data/raw/alexzhang_blog_context_rot.md

Top-5: rlm_production_zenml_chunk_005 | score: 0.7
  Text: ecause they reward lexical matching](https://arxiv.org/abs/2502.05167). When lexical cues disappear,  performance drops sharply with longer inputs, even for models marketed as long-context. Chroma’s [
  Source: data/raw/rlm_production_zenml.md

---

Query: How does the Python REPL environment function within the RLM agent architecture for recursive code execution?

Top-1: rlm_rl_training_alphaxiv_chunk_005 | score: 0.7492
  Text: by recursively calling itself with the ultimate goal of answering some user query about the context.  Like the original RLM paper, we use a Python Read-Eval-Print-Loop (REPL) as our environment. Rathe
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-2: rlm_deep_dive_towardsdatascience_chunk_023 | score: 0.6984
  Text: subtasks. The subagent responses do not get automatically loaded into the parent agent’s context, it  **_gets returned as symbols or variables inside the parent’s REPL_** - RLM agents can return respo
  Source: data/raw/rlm_deep_dive_towardsdatascience.md

Top-3: alexzhang_blog_context_rot_chunk_013 | score: 0.6956
  Text: *. **Figure 3** shows an example of how the RLM with a REPL **environment** produces a final answer.  **Figure 3.** Our instantiation of the RLM framework provides the root LM the ability to analyze t
  Source: data/raw/alexzhang_blog_context_rot.md

Top-4: rlm_comprehensive_guide_chunk_012 | score: 0.6305
  Text: dow expansion will help a model that needs to do O(n^2) semantic work in a single forward pass.  ---  ## 2. TECHNIQUES  ### The REPL  The REPL (Read-Eval-Print Loop) is where the magic happens. When a
  Source: data/raw/rlm_comprehensive_guide.md

Top-5: rlm_deep_dive_towardsdatascience_chunk_003 | score: 0.629
  Text: _Side note: Unless specified, all images used in this article were produced by the author. Free licensing._  The main reason Recursive Language Models feel inaccessible to a lot of the audience is tha
  Source: data/raw/rlm_deep_dive_towardsdatascience.md

---

Query: What benchmark scores does RLM achieve on BrowseComp-Plus and OOLONG compared to GPT-5 and Qwen3-Coder?

Top-1: rlm_rl_training_alphaxiv_chunk_044 | score: 0.6237
  Text: t 4.6Qwen3.5-4B(ours)Gemini-3-FlashGPT-5.4-minimodel0.100.200.300.400.500.600.700.6070.5830.5660.533  Average rubric eval score on the multi-paper evidence-selection task. The RL fine-tuned Qwen3.5-4B
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-2: rlm_original_paper_chunk_036 | score: 0.6069
  Text: costs. Notably, RLMs scale well to the theoretical costs of extending a base model’s context window  -  on BrowseComp-Plus (1K), the cost of GPT-5-mini ingesting 6-11M input tokens is $​1.50−$​2.75\\m
  Source: data/raw/rlm_original_paper.md

Top-3: prime_intellect_ablations_chunk_073 | score: 0.6019
  Text: ### INTELLECT-3: Oolong  `uv run environments/oolong/plot_results.py -m prime-intellect/intellect-3`  Like with GPT-5-mini, the RLM performs better than the pure LLM, though INTELLECT-3 benefits from 
  Source: data/raw/prime_intellect_ablations.md

Top-4: prime_intellect_ablations_chunk_044 | score: 0.5877
  Text: ts.py -m gpt-5-mini -I lift`):  The RLM tends to increase final reward. The exceptions are two-fold:  For math-python, the reward is significantly lower with than without the RLM. Because the RLM allo
  Source: data/raw/prime_intellect_ablations.md

Top-5: rlm_production_zenml_chunk_008 | score: 0.5848
  Text: scaffold, across the paper’s four long-context evaluation tasks. - On three tasks where the paper reports a meaningful direct GPT-5 baseline (CodeQA, OOLONG, OOLONG-Pairs), RLM-Qwen3-8B closes much of
  Source: data/raw/rlm_production_zenml.md

---

Query: How does RLM performance scale on long-context tasks like S-NIAH compared to non-recursive base LLMs?

Top-1: llm_reasoning_paradigms_evolution_chunk_023 | score: 0.7168
  Text: , tool calls, retrieved chunks. RLMs complete this evolution by treating reasoning as a system-level  property  --  how a model orchestrates its interaction with information across time and recursive 
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-2: rlm_original_paper_chunk_035 | score: 0.7017
  Text: $0.85) | 58.00($0.33 ±\\pm $0.20) | | RLM (no sub-calls) | 58.00 ($0.18 ±\\pm $0.56) | 88.00 ($0.44  ±\\pm $0.90) | 36.00 ($0.37 ±\\pm $0.42) | 43.93 ($0.69 ±\\pm $1.16) |  Observation 1: RLMs can sca
  Source: data/raw/rlm_original_paper.md

Top-3: rlm_comprehensive_guide_chunk_002 | score: 0.692
  Text: alls, post-training 3. [Research](#3-research)  --  Paper deep dive, benchmark results, ablations 4.  [Applications](#4-applications)  --  Code analysis, legal, deep research, books 5. [Comparison: LL
  Source: data/raw/rlm_comprehensive_guide.md

Top-4: prime_intellect_ablations_chunk_045 | score: 0.6662
  Text: the RLM is worse than the LLM, except when it is told a strategy for solving Deep Research problems:  split the question up into multiple, smaller research problems, and let sub-LLMs solve them, then 
  Source: data/raw/prime_intellect_ablations.md

Top-5: alexzhang_blog_context_rot_chunk_066 | score: 0.6662
  Text: ted to see how we can apply these ideas to improve the performance of RLMs as another axis of scale.  **RLMs improve as LMs improve.** Finally, the performance, speed, and cost of RLM calls correlate 
  Source: data/raw/alexzhang_blog_context_rot.md

---

Query: What are the architectural trade-offs between RLM recursive decomposition and retrieval-augmented generation for multi-hop reasoning?

Top-1: llm_reasoning_paradigms_evolution_chunk_025 | score: 0.6391
  Text: ing where each paradigm breaks  --  and choosing accordingly.  ## Open Questions & Future Directions  Several open questions remain: How should RLMs be trained? Current approaches rely on prompt engin
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-2: alexzhang_blog_context_rot_chunk_005 | score: 0.624
  Text: haddam, Y. Li, H. Hong, X. Shi, X. Liu, N. Thakur, C. Zhang, L. Gao, W. Chen, J. Lin.  2025\.  \[2\]  . On it, we observe that RLMs outperform other methods like ReAct + test-time indexing and retriev
  Source: data/raw/alexzhang_blog_context_rot.md

Top-3: rlm_comprehensive_guide_chunk_015 | score: 0.6113
  Text: document. True recursion, not just one level of delegation.  **Targeted probing**  --  for search-like tasks, the model might use BM25-style keyword matching in the REPL to identify relevant sections,
  Source: data/raw/rlm_comprehensive_guide.md

Top-4: alexzhang_blog_context_rot_chunk_010 | score: 0.6107
  Text: his intuition as the basis for a recursive language model.  ## **Recursive Language Models (RLMs).**  A recursive language model is a thin wrapper around a LM that can spawn (recursive) LM calls for i
  Source: data/raw/alexzhang_blog_context_rot.md

Top-5: rlm_candemir_medium_chunk_036 | score: 0.6056
  Text: nching and folding sub-trajectories. - **Prime Intellect's RLM implementation**  --  their blog post  "Recursive Language Models: the paradigm of 2026" provides practical insights from implementing an
  Source: data/raw/rlm_candemir_medium.md

---

Query: How does the evolution from flat prompting to recursive execution relate to context management in language models?

Top-1: rlm_original_paper_chunk_004 | score: 0.6691
  Text: ndles them effectively. Additional experiments across other models, methods, and benchmarks are in §  [2](https://arxiv.org/html/2512.24601v1#S2 "2 Scaling Long Context Tasks ‣ Recursive Language Mode
  Source: data/raw/rlm_original_paper.md

Top-2: llm_reasoning_paradigms_evolution_chunk_019 | score: 0.6574
  Text: esent a fundamental rethinking of how language models interact with information. Instead of treating  the prompt as a fixed token sequence, RLMs treat context as a variable in an external environment 
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-3: alexzhang_blog_context_rot_chunk_011 | score: 0.6533
  Text: view that we want a system that can answer a particular **query** over some associated **context**:  **Figure 2.** A recursive language model call replaces a language model call. It provides the user 
  Source: data/raw/alexzhang_blog_context_rot.md

Top-4: llm_reasoning_paradigms_evolution_chunk_001 | score: 0.6515
  Text: # LLM Reasoning Paradigms Evolution: From Prompting to Recursive Systems (Deepan MN, Medium Jan 2026)  **Source:** https://medium.com/@mndeepan06/recursive-language-models-rlms-from-prompting-to-recur
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-5: llm_reasoning_paradigms_evolution_chunk_026 | score: 0.6437
  Text: tions point to a future where reasoning paradigms are composed rather than competing.  ## Conclusion  The evolution of LLM reasoning is not just about bigger models or longer context windows. It is ab
  Source: data/raw/llm_reasoning_paradigms_evolution.md

---

Query: What are the ablation results for RLM with and without sub-calling on information-dense tasks?

Top-1: prime_intellect_ablations_chunk_057 | score: 0.5685
  Text: tested on the same 50 prompts.  Below, we plot the most important statistics about these ablations:  `uv run environments/math_python/plot_results.py -m gpt-5-mini -I ablation`  We quickly see three r
  Source: data/raw/prime_intellect_ablations.md

Top-2: rlm_rl_training_alphaxiv_chunk_045 | score: 0.512
  Text: not share the same prefix. Additionally, we maintain lengthy prompts that describe the strategy in detail. While this was necessary to get good results for models out-of-the-box that were not trained 
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-3: prime_intellect_ablations_chunk_040 | score: 0.5048
  Text: tim-copy  - `content_type = "all"` - `target_length = 500` - `mean_fragment_length = 20`  ### Models  We run our main ablations with GPT-5-mini. The reason is that initial experiments show that it is 
  Source: data/raw/prime_intellect_ablations.md

Top-4: prime_intellect_ablations_chunk_067 | score: 0.504
  Text: What this plot shows is that there is no clear relationship between fragment length and reward; this  modification seems to not make a big difference; at least not for the RLM! For the standard LLM, f
  Source: data/raw/prime_intellect_ablations.md

Top-5: rlm_comprehensive_guide_chunk_021 | score: 0.4904
  Text: they put the user prompt directly into the model's context. They inherit all the limitations of the  base model's context window. Adding BM25 retrieval helps for search tasks but doesn't address aggre
  Source: data/raw/rlm_comprehensive_guide.md

---

Query: How does the HALO agent optimizer implement RLM-based recursive loops for tool use?

Top-1: halo_agent_optimizer_chunk_001 | score: 0.8091
  Text: # HALO: Hierarchical Agent Loop Optimizer  **Repository:** https://github.com/context-labs/halo **PyPI:** `halo-engine` **Tagline:** RLM-based agent optimizer using production traces  ## What is HALO?
  Source: data/raw/halo_agent_optimizer.md

Top-2: halo_agent_optimizer_chunk_004 | score: 0.7202
  Text: c agentic behavior. We noticed in our testing that harnesses like CC would often overfit to an error  present in a single/few traces rather than generalize to harness-level problems. This led us to cr
  Source: data/raw/halo_agent_optimizer.md

Top-3: halo_agent_optimizer_chunk_002 | score: 0.691
  Text: examples applying HALO to popular agent benchmarks (View AppWorld)  ## HALO Loop  The core HALO loop is surprisingly simple:  1. **Collect execution traces** from your agent harness. HALO uses OpenTel
  Source: data/raw/halo_agent_optimizer.md

Top-4: rlm_production_zenml_chunk_019 | score: 0.6575
  Text: soning Pattern  Each `process_chunk` step runs a bounded iterative loop. Here’s the simplified flow:  Each plan+reflect iteration costs 2 LLM calls. The final summarize costs 1. So `max_iterations=6` 
  Source: data/raw/rlm_production_zenml.md

Top-5: rlm_rl_training_alphaxiv_chunk_005 | score: 0.6044
  Text: by recursively calling itself with the ultimate goal of answering some user query about the context.  Like the original RLM paper, we use a Python Read-Eval-Print-Loop (REPL) as our environment. Rathe
  Source: data/raw/rlm_rl_training_alphaxiv.md

---

Query: How does reinforcement learning fine-tuning improve RLM recursive behavior compared to supervised fine-tuning?

Top-1: rlm_comprehensive_guide_chunk_018 | score: 0.6229
  Text: r's most surprising result might be how little training it takes to make a model natively recursive.  RLM-Qwen3-8B was created by fine-tuning Qwen3-8B on just **1,000 filtered trajectories**. These tr
  Source: data/raw/rlm_comprehensive_guide.md

Top-2: rlm_rl_training_alphaxiv_chunk_001 | score: 0.6176
  Text: # Reinforcing Recursive Language Models  --  alphaXiv Blog  **Source:** https://www.alphaxiv.org/blog/reinforcement-learning-for-rlms **Platform:** alphaXiv / NovaSky AI (SkyRL) **Date:** 2026 **Autho
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-3: rlm_rl_training_alphaxiv_chunk_003 | score: 0.6097
  Text: separate policy models for parent and child RLMs, we train one model to play both roles of a parent  decomposer and child sub-agent. We use a simple RL training setup where rollouts from children RLMs
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-4: rlm_rl_training_alphaxiv_chunk_046 | score: 0.5986
  Text: d  Avg raw reward (EMA) when training the multi-paper RLM with a significantly reduced system prompt  Training with this setup converges slightly below the original run and is generally more unstable 
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-5: rlm_rl_training_alphaxiv_chunk_021 | score: 0.5857
  Text: xiv.org/blog/reinforcement-learning-for-rlms\#rlm-no-sub-calls "Jump to section") RLM (no sub-calls)  Before considering the recursive element of RLMs, we want to first confirm we can RL fine-tune Qwe
  Source: data/raw/rlm_rl_training_alphaxiv.md

---

