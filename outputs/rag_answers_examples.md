# RAG Answer Generation -- Test Results

**Prompt version:** v3 (grounded + citation + fallback)

**LLM:** qwen36-27b-awq via vLLM

**Embedding:** sentence-transformers/all-MiniLM-L6-v2

**Index:** FAISS FlatIP, 467 chunks

**Top-k:** 3

---

## Question 1: How do recursive language models handle prompts larger than their context window?

**Type:** simple (Core RLM concept — how RLMs decompose long prompts)

**Retrieved chunks:**

  - rlm_original_paper_chunk_002 (score: 0.7014)
  - llm_reasoning_paradigms_evolution_chunk_019 (score: 0.6977)
  - llm_reasoning_paradigms_evolution_chunk_005 (score: 0.6847)

**Answer:**



Recursive Language Models (RLMs) handle prompts larger than their context window by treating the context as a variable in an external environment rather than a fixed token sequence [llm_reasoning_paradigms_evolution_chunk_019]. Instead of receiving the entire context as tokens, the model receives a query and writes code to programmatically explore, filter, partition, examine, and decompose the context stored in a REPL environment [rlm_original_paper_chunk_002][llm_reasoning_paradigms_evolution_chunk_019]. It then recursively calls itself over snippets of the prompt [rlm_original_paper_chunk_002]. This strategy enables RLMs to successfully process inputs up to two orders of magnitude beyond their model context windows [rlm_original_paper_chunk_002].

**Sources:** data/raw/rlm_original_paper.md, data/raw/llm_reasoning_paradigms_evolution.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 2: What is context rot and why does performance degrade with longer inputs?

**Type:** simple (Context rot definition and causes)

**Retrieved chunks:**

  - rlm_candemir_medium_chunk_003 (score: 0.6942)
  - rlm_original_paper_chunk_004 (score: 0.6717)
  - rlm_production_zenml_chunk_005 (score: 0.6482)

**Answer:**



Context rot is a phenomenon where a language model's ability to recall and reason about text degrades, sometimes dramatically, as the amount of input text grows [rlm_candemir_medium_chunk_003]. Performance degrades with longer inputs because the model must hold the entire context in its "working memory" simultaneously, which becomes difficult to manage as text length increases [rlm_candemir_medium_chunk_003]. Additionally, many evaluation benchmarks reward lexical matching; when these lexical cues disappear in longer inputs, performance drops sharply [rlm_production_zenml_chunk_005].

**Sources:** data/raw/rlm_original_paper.md, data/raw/rlm_candemir_medium.md, data/raw/rlm_production_zenml.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 3: How does the Python REPL environment work in RLM architecture?

**Type:** simple (REPL architecture in RLM)

**Retrieved chunks:**

  - alexzhang_blog_context_rot_chunk_013 (score: 0.6600)
  - rlm_comprehensive_guide_chunk_005 (score: 0.6525)
  - rlm_rl_training_alphaxiv_chunk_005 (score: 0.6516)

**Answer:**



In the RLM architecture, the Python REPL environment serves as the primary interface for the model to inspect and transform data [rlm_rl_training_alphaxiv_chunk_005]. Rather than loading the full context into its window, the root model receives only constant-size metadata, such as the context's length, a short prefix, and instructions for accessing slices [rlm_comprehensive_guide_chunk_005]. During each turn, the model outputs code blocks to peek into, slice, or transform the context data [alexzhang_blog_context_rot_chunk_013][rlm_comprehensive_guide_chunk_005]. The REPL executes this code, updates the environment state, and returns a truncated version of the output back to the model's context [alexzhang_blog_context_rot_chunk_013][rlm_comprehensive_guide_chunk_005][rlm_rl_training_alphaxiv_chunk_005]. The model can also use the REPL to launch recursive sub-RLM calls on specific string slices or variables stored in the environment [alexzhang_blog_context_rot_chunk_013][rlm_comprehensive_guide_chunk_005]. Once the analysis is complete, the model outputs its final answer using `FINAL(…)` tags [alexzhang_blog_context_rot_chunk_013].

**Sources:** data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_rl_training_alphaxiv.md, data/raw/rlm_comprehensive_guide.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 4: What benchmark results does RLM achieve on BrowseComp-Plus and OOLONG?

**Type:** simple (RLM benchmark results)

**Retrieved chunks:**

  - rlm_original_paper_chunk_036 (score: 0.5973)
  - rlm_production_zenml_chunk_009 (score: 0.5848)
  - prime_intellect_ablations_chunk_068 (score: 0.5750)

**Answer:**



For BrowseComp-Plus, RLM(GPT-5) has an average cost of $0.99 and outperforms both summarization and retrieval baselines by over 29% [rlm_original_paper_chunk_036]. The provided context does not contain any benchmark results for OOLONG.

**Sources:** data/raw/rlm_original_paper.md, data/raw/rlm_production_zenml.md, data/raw/prime_intellect_ablations.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 5: What are the key differences between RLM and RAG for long-context processing?

**Type:** simple (RLM vs RAG comparison)

**Retrieved chunks:**

  - rlm_candemir_medium_chunk_022 (score: 0.6599)
  - rlm_production_zenml_chunk_010 (score: 0.5987)
  - rlm_rl_training_alphaxiv_chunk_019 (score: 0.5788)

**Answer:**



Based on the provided context, the key differences between RLM and RAG for long-context processing are:

- **Core Function:** RAG handles initial broad retrieval, whereas RLMs perform deeper, more adaptive analysis of the retrieved content [rlm_candemir_medium_chunk_022]. This is summarized as "RAG retrieves. RLMs investigate." [rlm_production_zenml_chunk_010].
- **Context Management:** RLMs treat "what’s in context" as a first-class design problem, enabling the model to programmatically explore externalized context [rlm_production_zenml_chunk_010].
- **Retrieval Flexibility:** RAG typically relies on a fixed-size top-k retrieval, while RLMs can dynamically return verbatim spans of varying lengths and counts [rlm_rl_training_alphaxiv_chunk_019].

Despite these distinctions, the context emphasizes that RLMs and RAG are complementary rather than competing, and can be used together [rlm_candemir_medium_chunk_022], [rlm_rl_training_alphaxiv_chunk_019].

**Sources:** data/raw/rlm_rl_training_alphaxiv.md, data/raw/rlm_candemir_medium.md, data/raw/rlm_production_zenml.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 6: What are the key ablation results for RLM with versus without sub-calling?

**Type:** simple (RLM ablation experiments)

**Retrieved chunks:**

  - prime_intellect_ablations_chunk_057 (score: 0.6014)
  - prime_intellect_ablations_chunk_056 (score: 0.5110)
  - rlm_rl_training_alphaxiv_chunk_045 (score: 0.4971)

**Answer:**



Based on the provided context, the key ablation results for RLMs utilizing sub-calling (sub-LLMs) are:
- Using sub-LLMs for math tasks makes the model weaker [prime_intellect_ablations_chunk_057].
- It barely reduces the main model's token usage [prime_intellect_ablations_chunk_057].
- It adds sub-LLM tokens, but only minimally, because the RLM uses sub-LLMs very sparsely even with additional prompting [prime_intellect_ablations_chunk_057].

**Sources:** data/raw/rlm_rl_training_alphaxiv.md, data/raw/prime_intellect_ablations.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 7: How does RL fine-tuning improve RLM behavior compared to prompting or SFT alone?

**Type:** simple (RL training for RLMs)

**Retrieved chunks:**

  - rlm_rl_training_alphaxiv_chunk_002 (score: 0.6658)
  - rlm_rl_training_alphaxiv_chunk_020 (score: 0.6373)
  - rlm_rl_training_alphaxiv_chunk_023 (score: 0.6046)

**Answer:**



RL fine-tuning can elicit RLM-specific behavior that cannot be achieved through prompting or even SFT alone [rlm_rl_training_alphaxiv_chunk_002]. While RLMs typically require extensive prompt tuning to elicit consistent behavior and can suffer from unpredictable latency, RL fine-tuning provides a robust method to improve model capabilities for specific tasks without the catastrophic forgetting associated with pure SFT-based approaches [rlm_rl_training_alphaxiv_chunk_002][rlm_rl_training_alphaxiv_chunk_020]. Additionally, SFT is primarily used to teach REPL navigation and RLM-specific syntax rather than training for specific tasks or datasets, making RL fine-tuning more effective for task-specific optimization [rlm_rl_training_alphaxiv_chunk_020].

**Sources:** data/raw/rlm_rl_training_alphaxiv.md

**Comment:** PASS - Citations present - answer is grounded.

---

## Question 8: What is the stock price of Apple Inc in 2025?

**Type:** insufficient (Insufficient context — should trigger fallback)

**Retrieved chunks:**

  - rlm_candemir_medium_chunk_015 (score: 0.1768)
  - rlm_original_paper_chunk_034 (score: 0.1528)
  - alexzhang_blog_context_rot_chunk_053 (score: 0.1487)

**Answer:**



I do not have enough information in the available documents to answer this question.

**Sources:** data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_original_paper.md, data/raw/rlm_candemir_medium.md

**Comment:** PASS - Fallback triggered correctly - model says it does not know.

---

## Question 9: How much does the RLM system cost to run in production?

**Type:** insufficient (Insufficient context — no pricing info in KB)

**Retrieved chunks:**

  - rlm_original_paper_chunk_036 (score: 0.4347)
  - rlm_production_zenml_chunk_011 (score: 0.4271)
  - alexzhang_blog_context_rot_chunk_066 (score: 0.4124)

**Answer:**



I do not have enough information in the available documents to answer this question.

**Sources:** data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_original_paper.md, data/raw/rlm_production_zenml.md

**Comment:** PASS - Fallback triggered correctly - model says it does not know.

---

## Question 10: Who invented the internet?

**Type:** insufficient (Completely out of scope — should trigger fallback)

**Retrieved chunks:**

  - alexzhang_blog_context_rot_chunk_073 (score: 0.2375)
  - prime_intellect_ablations_chunk_020 (score: 0.2052)
  - rlm_rl_training_alphaxiv_chunk_054 (score: 0.1922)

**Answer:**



I do not have enough information in the available documents to answer this question.

**Sources:** data/raw/alexzhang_blog_context_rot.md, data/raw/rlm_rl_training_alphaxiv.md, data/raw/prime_intellect_ablations.md

**Comment:** PASS - Fallback triggered correctly - model says it does not know.

---
