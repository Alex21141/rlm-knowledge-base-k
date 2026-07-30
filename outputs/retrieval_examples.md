# HW2: Semantic Retrieval — Test Results

**Embedding model:** sentence-transformers/all-MiniLM-L6-v2
**FAISS index:** IndexFlatIP, 467 vectors
**Chunks:** 467
**Queries:** 10
**Top-k:** 5

---

Query: How do recursive language models handle prompts larger than their context window?

Top-1: rlm_original_paper_chunk_002 | score: 0.7014
  Text: s through the lens of inference-time scaling. We propose Recursive Language Models (RLMs), a general  inference strategy that treats long prompts as part of an external environment and allows the LLM 
  Source: data/raw/rlm_original_paper.md

Top-2: llm_reasoning_paradigms_evolution_chunk_019 | score: 0.6977
  Text: esent a fundamental rethinking of how language models interact with information. Instead of treating  the prompt as a fixed token sequence, RLMs treat context as a variable in an external environment 
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-3: llm_reasoning_paradigms_evolution_chunk_005 | score: 0.6847
  Text: ems, inference-time scaling, and more recently, Recursive Language Models (RLMs). Rather than asking  "How do we fit everything into the prompt?", these approaches ask a deeper question: How should a 
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-4: rlm_original_paper_chunk_008 | score: 0.6794
  Text: n is rarely expressive enough for tasks that require dense access to many parts of the prompt, as it  presumes in effect that some details that appear early in the prompt can safely be forgotten to ma
  Source: data/raw/rlm_original_paper.md

Top-5: alexzhang_blog_context_rot_chunk_003 | score: 0.6496
  Text: We propose **Recursive Language Models**, or **RLM**s, a general inference strategy where language models can decompose and recursively interact with their input context as a variable. We design a spe
  Source: data/raw/alexzhang_blog_context_rot.md

---

Query: What is context rot and why does performance degrade with longer inputs?

Top-1: rlm_candemir_medium_chunk_003 | score: 0.6942
  Text: ken in one pass. It has to hold the entire context in its "working memory" simultaneously. For short  inputs, this works beautifully. For long inputs, things start to fall apart.  ## What Is Context R
  Source: data/raw/rlm_candemir_medium.md

Top-2: rlm_original_paper_chunk_004 | score: 0.6717
  Text: ndles them effectively. Additional experiments across other models, methods, and benchmarks are in §  [2](https://arxiv.org/html/2512.24601v1#S2 "2 Scaling Long Context Tasks ‣ Recursive Language Mode
  Source: data/raw/rlm_original_paper.md

Top-3: rlm_production_zenml_chunk_005 | score: 0.6482
  Text: ecause they reward lexical matching](https://arxiv.org/abs/2502.05167). When lexical cues disappear,  performance drops sharply with longer inputs, even for models marketed as long-context. Chroma’s [
  Source: data/raw/rlm_production_zenml.md

Top-4: alexzhang_blog_context_rot_chunk_062 | score: 0.6313
  Text: ce sampling methods over a set of candidate responses.  ## What We’re Thinking Now & for the Future.  Long-context capabilities in language models used to be a model architecture problem (think ALiBi,
  Source: data/raw/alexzhang_blog_context_rot.md

Top-5: rlm_production_zenml_chunk_004 | score: 0.604
  Text: e heard the buzz but haven’t read the paper, here’s the short version.  ### The Problem: Context Rot  When you stuff massive documents into an LLM’s context window, performance degrades. Even models w
  Source: data/raw/rlm_production_zenml.md

---

Query: How does the Python REPL environment work in RLM architecture?

Top-1: alexzhang_blog_context_rot_chunk_013 | score: 0.66
  Text: *. **Figure 3** shows an example of how the RLM with a REPL **environment** produces a final answer.  **Figure 3.** Our instantiation of the RLM framework provides the root LM the ability to analyze t
  Source: data/raw/alexzhang_blog_context_rot.md

Top-2: rlm_comprehensive_guide_chunk_005 | score: 0.6525
  Text: 2. **Provide metadata, not content.** The root model receives only constant-size metadata about P: its length, a short prefix, how to access slices of it. The full text of P never enters the model's c
  Source: data/raw/rlm_comprehensive_guide.md

Top-3: rlm_rl_training_alphaxiv_chunk_005 | score: 0.6516
  Text: by recursively calling itself with the ultimate goal of answering some user query about the context.  Like the original RLM paper, we use a Python Read-Eval-Print-Loop (REPL) as our environment. Rathe
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-4: rlm_deep_dive_towardsdatascience_chunk_023 | score: 0.6141
  Text: subtasks. The subagent responses do not get automatically loaded into the parent agent’s context, it  **_gets returned as symbols or variables inside the parent’s REPL_** - RLM agents can return respo
  Source: data/raw/rlm_deep_dive_towardsdatascience.md

Top-5: rlm_candemir_medium_chunk_018 | score: 0.6084
  Text: is designed to go deeper when needed, and this is where things get exciting for future development.  Think of it like delegation in an organization. The CEO doesn't read every email. She asks departme
  Source: data/raw/rlm_candemir_medium.md

---

Query: What benchmark results does RLM achieve on BrowseComp-Plus and OOLONG?

Top-1: rlm_original_paper_chunk_036 | score: 0.5973
  Text: costs. Notably, RLMs scale well to the theoretical costs of extending a base model’s context window  -  on BrowseComp-Plus (1K), the cost of GPT-5-mini ingesting 6-11M input tokens is $​1.50−$​2.75\\m
  Source: data/raw/rlm_original_paper.md

Top-2: rlm_production_zenml_chunk_009 | score: 0.5848
  Text: The paper’s evaluation includes tasks where base models cannot even fit the input. BrowseComp+ at 1K documents is in the multi-million token range. RLM variants can still operate.  ### How RLMs Differ
  Source: data/raw/rlm_production_zenml.md

Top-3: prime_intellect_ablations_chunk_068 | score: 0.575
  Text: DISCLAIMER: we must stress again that this is not a measurement of any model's absolute performance  on any benchmark. Again, we put no effort into optimizing the models' benchmark scores by hyperpara
  Source: data/raw/prime_intellect_ablations.md

Top-4: alexzhang_blog_context_rot_chunk_057 | score: 0.5637
  Text: query to range from a few seconds to several minutes. Furthermore, while we can control the length /  “thinking time” of an RLM by increasing the maximum number of iterations, we do not currently have
  Source: data/raw/alexzhang_blog_context_rot.md

Top-5: prime_intellect_ablations_chunk_073 | score: 0.5581
  Text: ### INTELLECT-3: Oolong  `uv run environments/oolong/plot_results.py -m prime-intellect/intellect-3`  Like with GPT-5-mini, the RLM performs better than the pure LLM, though INTELLECT-3 benefits from 
  Source: data/raw/prime_intellect_ablations.md

---

Query: How does RLM performance compare to base LLMs on long-context tasks?

Top-1: rlm_comprehensive_guide_chunk_002 | score: 0.747
  Text: alls, post-training 3. [Research](#3-research)  --  Paper deep dive, benchmark results, ablations 4.  [Applications](#4-applications)  --  Code analysis, legal, deep research, books 5. [Comparison: LL
  Source: data/raw/rlm_comprehensive_guide.md

Top-2: llm_reasoning_paradigms_evolution_chunk_023 | score: 0.7433
  Text: , tool calls, retrieved chunks. RLMs complete this evolution by treating reasoning as a system-level  property  --  how a model orchestrates its interaction with information across time and recursive 
  Source: data/raw/llm_reasoning_paradigms_evolution.md

Top-3: rlm_original_paper_chunk_035 | score: 0.7342
  Text: $0.85) | 58.00($0.33 ±\\pm $0.20) | | RLM (no sub-calls) | 58.00 ($0.18 ±\\pm $0.56) | 88.00 ($0.44  ±\\pm $0.90) | 36.00 ($0.37 ±\\pm $0.42) | 43.93 ($0.69 ±\\pm $1.16) |  Observation 1: RLMs can sca
  Source: data/raw/rlm_original_paper.md

Top-4: prime_intellect_ablations_chunk_061 | score: 0.7305
  Text: hs for the RLM. For the most important, real data, the RLM is significantly better than the LLM at a  context length of around 1.5M characters (~300-400k tokens). Beyond that, no model can succeed.  F
  Source: data/raw/prime_intellect_ablations.md

Top-5: prime_intellect_ablations_chunk_053 | score: 0.7203
  Text: strongly the context window of the RLM is compressed, while retaining performance - math-python: the  presence of the RLM harness, despite enabling the exact same behavior as the default LLM harness, 
  Source: data/raw/prime_intellect_ablations.md

---

Query: What are the key differences between RLM and RAG for long-context processing?

Top-1: rlm_candemir_medium_chunk_022 | score: 0.6599
  Text: yze document structure, cross-reference sections, and adapt its approach based on what it discovers.  That said, the RLM authors have noted that RLMs and RAG are complementary, not competing. They can
  Source: data/raw/rlm_candemir_medium.md

Top-2: rlm_production_zenml_chunk_010 | score: 0.5987
  Text: rch for, and what to delegate. It's a research assistant with a filing system, not a keyword search.  RAG retrieves. RLMs investigate.  RLMs are also part of a broader pattern: systems that treat “wha
  Source: data/raw/rlm_production_zenml.md

Top-3: rlm_rl_training_alphaxiv_chunk_019 | score: 0.5788
  Text: input papers is generated from a PDF parsing library and included in the dataset to be passed in as  context to the root RLM. Highlighted papers are the ground-truth supporting papers.  Another point 
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-4: rlm_candemir_medium_chunk_021 | score: 0.5774
  Text: etrieval-Augmented Generation (RAG), you might be wondering: isn't this just a fancy version of RAG?  There's a meaningful distinction. RAG systems use pre-built indexes (often vector embeddings) to r
  Source: data/raw/rlm_candemir_medium.md

Top-5: prime_intellect_ablations_chunk_053 | score: 0.5696
  Text: strongly the context window of the RLM is compressed, while retaining performance - math-python: the  presence of the RLM harness, despite enabling the exact same behavior as the default LLM harness, 
  Source: data/raw/prime_intellect_ablations.md

---

Query: How does context folding relate to recursive language models?

Top-1: prime_intellect_ablations_chunk_007 | score: 0.7756
  Text: context folding is the Recursive Language Model (RLM), introduced by Alex Zhang in October 2025 as a  [blog post](https://alexzhang13.github.io/blog/2025/rlm/), and now available as a full paper: [htt
  Source: data/raw/prime_intellect_ablations.md

Top-2: rlm_candemir_medium_chunk_035 | score: 0.7521
  Text: trick to a native capability.  ## Further Reading  If you want to go deeper, here's where to start:  - **The original paper:** Zhang, Kraska, and Khattab  --  "Recursive Language Models" (arXiv:2512.2
  Source: data/raw/rlm_candemir_medium.md

Top-3: rlm_original_paper_chunk_004 | score: 0.7001
  Text: ndles them effectively. Additional experiments across other models, methods, and benchmarks are in §  [2](https://arxiv.org/html/2512.24601v1#S2 "2 Scaling Long Context Tasks ‣ Recursive Language Mode
  Source: data/raw/rlm_original_paper.md

Top-4: alexzhang_blog_context_rot_chunk_002 | score: 0.6967
  Text: hors  ### Affiliations  Alex Zhang  MIT CSAIL  Omar Khattab  MIT CSAIL  ### Published  Oct. 15, 2025  _The full paper is now available here: https://www.alphaxiv.org/abs/2512.24601 https://www.alphaxi
  Source: data/raw/alexzhang_blog_context_rot.md

Top-5: prime_intellect_ablations_chunk_006 | score: 0.6576
  Text: g per-action summaries - [Agentic Context Engineering: Evolving Contexts for Self-Improving Language  Models](http://arxiv.org/abs/2510.04618): a three-agent system with a Generator that uses the curr
  Source: data/raw/prime_intellect_ablations.md

---

Query: What are the key ablation results for RLM with versus without sub-calling?

Top-1: prime_intellect_ablations_chunk_057 | score: 0.6014
  Text: tested on the same 50 prompts.  Below, we plot the most important statistics about these ablations:  `uv run environments/math_python/plot_results.py -m gpt-5-mini -I ablation`  We quickly see three r
  Source: data/raw/prime_intellect_ablations.md

Top-2: prime_intellect_ablations_chunk_056 | score: 0.511
  Text: hen, we run the same ablations as before (with the same random seed leading to the same data order),  but vary the timeout of each of the LLM's commands: 120 seconds (the default used for all other ex
  Source: data/raw/prime_intellect_ablations.md

Top-3: rlm_rl_training_alphaxiv_chunk_045 | score: 0.4971
  Text: not share the same prefix. Additionally, we maintain lengthy prompts that describe the strategy in detail. While this was necessary to get good results for models out-of-the-box that were not trained 
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-4: prime_intellect_ablations_chunk_067 | score: 0.4923
  Text: What this plot shows is that there is no clear relationship between fragment length and reward; this  modification seems to not make a big difference; at least not for the RLM! For the standard LLM, f
  Source: data/raw/prime_intellect_ablations.md

Top-5: prime_intellect_ablations_chunk_040 | score: 0.4353
  Text: tim-copy  - `content_type = "all"` - `target_length = 500` - `mean_fragment_length = 20`  ### Models  We run our main ablations with GPT-5-mini. The reason is that initial experiments show that it is 
  Source: data/raw/prime_intellect_ablations.md

---

Query: How does the HALO agent optimizer use RLM-based loops?

Top-1: halo_agent_optimizer_chunk_001 | score: 0.7616
  Text: # HALO: Hierarchical Agent Loop Optimizer  **Repository:** https://github.com/context-labs/halo **PyPI:** `halo-engine` **Tagline:** RLM-based agent optimizer using production traces  ## What is HALO?
  Source: data/raw/halo_agent_optimizer.md

Top-2: halo_agent_optimizer_chunk_002 | score: 0.6824
  Text: examples applying HALO to popular agent benchmarks (View AppWorld)  ## HALO Loop  The core HALO loop is surprisingly simple:  1. **Collect execution traces** from your agent harness. HALO uses OpenTel
  Source: data/raw/halo_agent_optimizer.md

Top-3: halo_agent_optimizer_chunk_004 | score: 0.613
  Text: c agentic behavior. We noticed in our testing that harnesses like CC would often overfit to an error  present in a single/few traces rather than generalize to harness-level problems. This led us to cr
  Source: data/raw/halo_agent_optimizer.md

Top-4: halo_agent_optimizer_chunk_003 | score: 0.5615
  Text: ur harness. 5. **The harness is then re-deployed**, more traces are gathered, and the cycle repeats.  HALO is great at finding issues in production agent deployments. We find high-traffic environments
  Source: data/raw/halo_agent_optimizer.md

Top-5: rlm_production_zenml_chunk_019 | score: 0.5118
  Text: soning Pattern  Each `process_chunk` step runs a bounded iterative loop. Here’s the simplified flow:  Each plan+reflect iteration costs 2 LLM calls. The final summarize costs 1. So `max_iterations=6` 
  Source: data/raw/rlm_production_zenml.md

---

Query: How does RL fine-tuning improve RLM behavior compared to prompting or SFT alone?

Top-1: rlm_rl_training_alphaxiv_chunk_002 | score: 0.6658
  Text: sk-specific, RLM behavior that cannot be elicited through prompting or even SFT. This blog assumes a  basic level of familiarity with RLMs. A great resource for learning about them is the [original RL
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-2: rlm_rl_training_alphaxiv_chunk_020 | score: 0.6373
  Text: der-480B-A35B-Instruct. The purpose of SFT is to teach the model how to navigate a REPL environment,  including RLM-specific syntax for submitting an answer and making sub-LM calls. However, SFT was n
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-3: rlm_rl_training_alphaxiv_chunk_023 | score: 0.6046
  Text: ve 0 pass@16 scores. RLM-based tasks are outside the edge of competence \[3\] for most small models.  When training without an SFT phase, we observed many of the same failure modes observed in the ori
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-4: rlm_rl_training_alphaxiv_chunk_047 | score: 0.5887
  Text: **Task Exploration.** We've chosen this particular task selfishly for our own production needs. Beyond evidence selection, there's a whole world of tasks worth exploring with RLM training. If RLMs are
  Source: data/raw/rlm_rl_training_alphaxiv.md

Top-5: rlm_rl_training_alphaxiv_chunk_045 | score: 0.5859
  Text: not share the same prefix. Additionally, we maintain lengthy prompts that describe the strategy in detail. While this was necessary to get good results for models out-of-the-box that were not trained 
  Source: data/raw/rlm_rl_training_alphaxiv.md

---

