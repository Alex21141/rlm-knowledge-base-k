# RAG Answer Generation -- Test Results

**Prompt version:** v3 (grounded + citation + fallback)

**LLM:** qwen36-27b-awq via vLLM

**Embedding:** sentence-transformers/all-MiniLM-L6-v2

**Index:** FAISS FlatIP, 467 chunks

**Top-k:** 3

---

## Question 1: How do RLMs handle arbitrarily long prompts?

**Type:** simple (Core RLM concept — answer clearly in context)

**Retrieved chunks:**

  - rlm_deep_dive_towardsdatascience_chunk_022 (score: 0.6612)
  - rlm_comprehensive_guide_chunk_004 (score: 0.6438)
  - rlm_original_paper_chunk_009 (score: 0.6084)

**Answer:**



RLMs handle arbitrarily long prompts by treating them as part of an external environment rather than feeding them directly into the neural network [rlm_original_paper_chunk_009]. Instead, the model interacts with the prompt through an external programmable environment or REPL [rlm_deep_dive_towardsdatascience_chunk_022]. The neural network never sees the full prompt; it only receives metadata such as the prompt's length, a short prefix, and type information [rlm_comprehensive_guide_chunk_004]. Using this metadata, the LLM writes code to interact with the prompt piece by piece [rlm_comprehensive_guide_chunk_004]. This process begins by initializing a persistent programming environment (REPL) for the arbitrary-length prompt [rlm_comprehensive_guide_chunk_004].

**Sources:** data/raw/rlm_deep_dive_towardsdatascience.md, data/raw/rlm_comprehensive_guide.md, data/raw/rlm_original_paper.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 2: What causes context rot in language models?

**Type:** rephrased (Rephrased: what is context rot?)

**Retrieved chunks:**

  - rlm_original_paper_chunk_004 (score: 0.7307)
  - rlm_candemir_medium_chunk_003 (score: 0.7082)
  - alexzhang_blog_context_rot_chunk_062 (score: 0.6693)

**Answer:**



Context rot occurs because language models must hold the entire input context in their "working memory" simultaneously, causing recall and reasoning abilities to degrade as the text length increases [rlm_candemir_medium_chunk_003]. Additionally, the underlying bottlenecks contributing to these long-context limitations are described as a combination of model architecture challenges, systems constraints due to quadratic attention, and Mixture-of-Experts (MoE) layer bottlenecks [alexzhang_blog_context_rot_chunk_062].

**Sources:** data/raw/rlm_candemir_medium.md, data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_original_paper.md

**Comment:** PASS - Rephrased question handled - model found relevant context.

---

## Question 3: What is the difference between RLM and standard LLM for long-context tasks?

**Type:** simple (Simple conceptual comparison)

**Retrieved chunks:**

  - rlm_comprehensive_guide_chunk_002 (score: 0.7152)
  - prime_intellect_ablations_chunk_015 (score: 0.6980)
  - llm_reasoning_paradigms_evolution_chunk_023 (score: 0.6868)

**Answer:**



For long-context tasks, RLMs and standard LLMs represent two fundamentally different approaches [rlm_comprehensive_guide_chunk_002]. Standard LLMs are constrained by a context window (a maximum number of tokens they can process), making it ineffective to simply shove all data into the context [rlm_comprehensive_guide_chunk_002]. In contrast, RLMs function as powerful long-context agents that are highly flexible and strong at tool-use, making them ideal for environments where context is a sparse resource [prime_intellect_ablations_chunk_015]. Instead of relying on expanding context windows or model parameters, RLMs treat reasoning as a system-level property, focusing on how the model orchestrates information across time and recursive calls [llm_reasoning_paradigms_evolution_chunk_023]. This shifts the primary bottleneck for long-context tasks from the model's context window to the overall system design [llm_reasoning_paradigms_evolution_chunk_023].

**Sources:** data/raw/prime_intellect_ablations.md, data/raw/rlm_comprehensive_guide.md, data/raw/llm_reasoning_paradigms_evolution.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 4: How does HALO optimize agent loops using RLMs?

**Type:** simple (Tool-specific question — HALO + RLM)

**Retrieved chunks:**

  - halo_agent_optimizer_chunk_001 (score: 0.8104)
  - halo_agent_optimizer_chunk_002 (score: 0.7249)
  - halo_agent_optimizer_chunk_004 (score: 0.6684)

**Answer:**



HALO optimizes agent loops by implementing a methodology for building recursively self-improving agent harnesses using RLMs [halo_agent_optimizer_chunk_001]. The process follows a four-step loop:

1. Execution traces are collected from the agent harness using OpenTelemetry-compatible tracing [halo_agent_optimizer_chunk_002].
2. The traces are fed into the HALO-RLM engine [halo_agent_optimizer_chunk_002].
3. The engine decomposes the traces to identify common failure modes across harness executions and produces a findings report [halo_agent_optimizer_chunk_002].
4. The report is fed into a coding agent like Cursor or Claude Code [halo_agent_optimizer_chunk_002].

The HALO Engine utilizes a specialized RLM architecture that implements bounded recursion, per-depth parallelism, and persistent context items. This design prevents the system from overfitting to errors in individual traces and instead allows it to generalize to harness-level problems [halo_agent_optimizer_chunk_004].

**Sources:** data/raw/halo_agent_optimizer.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 5: How does RLM compare to context folding for long-context processing?

**Type:** simple (Comparison: RLM vs context folding)

**Retrieved chunks:**

  - prime_intellect_ablations_chunk_078 (score: 0.7256)
  - prime_intellect_ablations_chunk_007 (score: 0.7002)
  - rlm_original_paper_chunk_014 (score: 0.6945)

**Answer:**



Based on the provided context, context folding is not a separate method to compare against the RLM; rather, context folding is the Recursive Language Model (RLM) itself [prime_intellect_ablations_chunk_007]. For long-context processing, the RLM (context folding) demonstrates extremely strong performance, effectively handling scales of 10M+ tokens while exhibiting far less severe degradation for longer contexts compared to other approaches [rlm_original_paper_chunk_014].

**Sources:** data/raw/prime_intellect_ablations.md, data/raw/rlm_original_paper.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 6: How does RL fine-tuning improve RLM behavior compared to prompting alone?

**Type:** simple (RL training for RLMs)

**Retrieved chunks:**

  - rlm_rl_training_alphaxiv_chunk_002 (score: 0.6396)
  - rlm_rl_training_alphaxiv_chunk_045 (score: 0.6200)
  - rlm_rl_training_alphaxiv_chunk_047 (score: 0.6157)

**Answer:**



Based on the provided context, RL fine-tuning improves RLM behavior compared to prompting alone by:
- Enabling RLM behaviors that cannot be elicited through prompting or even supervised fine-tuning (SFT) [rlm_rl_training_alphaxiv_chunk_002].
- Eliminating the need for extensive prompt tuning and lengthy system prompts (e.g., 1500 tokens) that are otherwise required to elicit consistent behavior from out-of-the-box models [rlm_rl_training_alphaxiv_chunk_002][rlm_rl_training_alphaxiv_chunk_045].
- Acting as the ultimately necessary training method for inference scaling techniques, as prompting alone only yields limited improvements compared to the performance and training story driven by RL fine-tuning [rlm_rl_training_alphaxiv_chunk_047].

**Sources:** data/raw/rlm_rl_training_alphaxiv.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 7: What is the stock price of Apple Inc in 2025?

**Type:** insufficient (Insufficient context — should trigger fallback)

**Retrieved chunks:**

  - rlm_candemir_medium_chunk_015 (score: 0.1768)
  - rlm_original_paper_chunk_034 (score: 0.1528)
  - alexzhang_blog_context_rot_chunk_053 (score: 0.1487)

**Answer:**



I do not have enough information in the available documents to answer this question.

**Sources:** data/raw/rlm_candemir_medium.md, data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_original_paper.md

**Comment:** PASS - Fallback triggered correctly - model says it does not know.

---

## Question 8: How much does the RLM system cost to run in production?

**Type:** insufficient (Insufficient context — no pricing info in KB)

**Retrieved chunks:**

  - rlm_original_paper_chunk_036 (score: 0.4347)
  - rlm_production_zenml_chunk_011 (score: 0.4271)
  - alexzhang_blog_context_rot_chunk_066 (score: 0.4124)

**Answer:**



The provided context does not specify a fixed cost for running the RLM system in production. It reports an average benchmark cost of $0.99 per call for RLM(GPT-5) on BrowseComp-Plus [rlm_original_paper_chunk_036]. For production deployments, costs are managed via configuration knobs like `max_iterations` and `max_llm_calls` [rlm_production_zenml_chunk_011], but tracking exact per-chunk costs and overall spending is presented as an open challenge rather than a defined figure [rlm_production_zenml_chunk_011].

**Sources:** data/raw/rlm_production_zenml.md, data/raw/rlm_original_paper.md, data/raw/alexzhang_blog_context_rot.md

**Comment:** WARN - Model did not trigger fallback - may be hallucinating.

---

## Question 9: What are the key ablation results for RLM with versus without sub-calling?

**Type:** simple (Experimental results — Prime Intellect ablations)

**Retrieved chunks:**

  - prime_intellect_ablations_chunk_057 (score: 0.6014)
  - prime_intellect_ablations_chunk_056 (score: 0.5110)
  - rlm_rl_training_alphaxiv_chunk_045 (score: 0.4971)

**Answer:**



Based on the provided context, the key ablation results for RLM with sub-calling (sub-LLMs) are:
- **Performance:** Using sub-LLMs for math tasks makes the GPT-5-mini model weaker [prime_intellect_ablations_chunk_057].
- **Main Model Token Usage:** The approach barely reduces the main model's token usage, which remains significantly higher than that of a standard LLM [prime_intellect_ablations_chunk_057].
- **Sub-LLM Token Overhead:** It adds sub-LLM tokens, but only minimally, because the GPT-5-mini RLM utilizes sub-LLMs very sparsely even with extra prompting [prime_intellect_ablations_chunk_057].

**Sources:** data/raw/prime_intellect_ablations.md, data/raw/rlm_rl_training_alphaxiv.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 10: Who invented the internet?

**Type:** insufficient (Completely out of scope — should trigger fallback)

**Retrieved chunks:**

  - alexzhang_blog_context_rot_chunk_073 (score: 0.2375)
  - prime_intellect_ablations_chunk_020 (score: 0.2052)
  - rlm_rl_training_alphaxiv_chunk_054 (score: 0.1922)

**Answer:**



I do not have enough information in the available documents to answer this question.

**Sources:** data/raw/prime_intellect_ablations.md, data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_rl_training_alphaxiv.md

**Comment:** PASS - Fallback triggered correctly - model says it does not know.

---
