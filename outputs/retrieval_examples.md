# Retrieval Test Results

**Model:** sentence-transformers/all-MiniLM-L6-v2

**Index:** FAISS (Inner Product, dim=384)

**Chunks indexed:** 84

**Top-k:** 3


---

## Query 1: How do RLMs handle arbitrarily long prompts?

**Expected:** context-centric view, recursive decomposition, REPL environment


Top-1: prime_intellect_ablations_chunk_005 | score: 0.6126
  Text: This setup allows the model to generate its final answer via a form of diffusion, which occurs over the course of its reasoning chain.

### Input Data Handling

Both a prompt and extra input data can ...
  Source: data/raw/prime_intellect_ablations.md | Section: Input Data Handling



Top-2: rlm_core_paper_and_github_chunk_001 | score: 0.5235
  Text: # Recursive Language Models  --  Core Paper and Implementation

**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)
**Paper:** arXiv:2512.24601 (Dec 31, 2025)
**Code:** https://github.com...
  Source: data/raw/rlm_core_paper_and_github.md | Section: Recursive Language Models  --  Core Paper and Implementation



Top-3: rlm_core_paper_and_github_chunk_007 | score: 0.4859
  Text: RLMs support configurable max recursion depths:
- **Depth 0:** RLM without sub-calling capabilities (standard LM behavior).
- **Depth 1:** Allows sub-calling LLMs on specific context snippets.
- **Dep...
  Source: data/raw/rlm_core_paper_and_github.md | Section: Experimental Results



**Comment:** partially relevant


---

## Query 2: What is context rot and why does it happen?

**Expected:** degradation of context quality with increasing length


Top-1: rlm_core_paper_and_github_chunk_004 | score: 0.6233
  Text: icult to characterize phenomenon in language models known as "context rot". Anthropic defines context rot as "when the number of tokens in the context

window increases, the model's ability to accurat...
  Source: data/raw/rlm_core_paper_and_github.md | Section: The Problem: Context Rot



Top-2: alexzhang_blog_context_rot_chunk_004 | score: 0.6137
  Text: tokens in the context window increases, the model's ability to accurately recall information from that context decreases", but many researchers in the

community know this definition doesn't fully hit...
  Source: data/raw/alexzhang_blog_context_rot.md | Section: Prelude: Why is "Long-Context" Research So Unsatisfactory?



Top-3: rlm_core_paper_and_github_chunk_003 | score: 0.5004
  Text: ## Core Concept: Context-Centric View

A recursive language model is a thin wrapper around a LM that can spawn (recursive) LM calls for intermediate

computation. From the perspective of the user or p...
  Source: data/raw/rlm_core_paper_and_github.md | Section: Core Concept: Context-Centric View



**Comment:** relevant


---

## Query 3: How does HALO optimize agent loops?

**Expected:** hierarchical agent loop, root LM + sub-LMs, trace analysis


Top-1: halo_agent_optimizer_chunk_001 | score: 0.8106
  Text: # HALO: Hierarchical Agent Loop Optimizer

**Repository:** https://github.com/context-labs/halo
**PyPI:** `halo-engine`
**Tagline:** RLM-based agent optimizer using production traces

## What is HALO?...
  Source: data/raw/halo_agent_optimizer.md | Section: HALO: Hierarchical Agent Loop Optimizer



Top-2: halo_agent_optimizer_chunk_002 | score: 0.6022
  Text: 1. **Collect execution traces** from your agent harness. HALO uses OpenTelemetry-compatible tracing.
2. **Feed traces into HALO-RLM engine.**
3. **The engine decomposes the traces** to understand comm...
  Source: data/raw/halo_agent_optimizer.md | Section: Telemetry



Top-3: halo_agent_optimizer_chunk_003 | score: 0.5495
  Text: traffic environments tend to generate more data with higher variance across executions, creating the type of issues that HALO is great at identifying.

## Why an RLM?

A general-purpose harness like C...
  Source: data/raw/halo_agent_optimizer.md | Section: HALO Engine Architecture



**Comment:** partially relevant


---

## Query 4: What are the key differences between RLM and ReAct?

**Expected:** RLM is recursive, ReAct is reasoning+acting with tools


Top-1: rlm_industry_analysis_chunk_003 | score: 0.5649
  Text: Developers are exploring how to integrate RLM concepts into existing agent frameworks, particularly for applications requiring extremely long context lengths (10M+ tokens) and information-dense tasks....
  Source: data/raw/rlm_industry_analysis.md | Section: Comparison with Other Paradigms



Top-2: alexzhang_blog_context_rot_chunk_010 | score: 0.5253
  Text: the model to delegate reasoning steps to sub-calls, effectively creating a tree of thought rather than a linear chain.

### ReAct (Reasoning + Acting)

ReAct models interleave reasoning and action. RL...
  Source: data/raw/alexzhang_blog_context_rot.md | Section: ReAct (Reasoning + Acting)



Top-3: rlm_core_paper_and_github_chunk_016 | score: 0.4652
  Text: e many amazing demos and production-ready use cases of RLMs. Notable examples that explicitly use RLMs as a central piece of their design include HALO

(Context Labs) and various agent optimization to...
  Source: data/raw/rlm_core_paper_and_github.md | Section: RLMs in the Wild



**Comment:** partially relevant


---

## Query 5: What is the Griffin architecture used in RecurrentGemma?

**Expected:** linear recurrences, fixed-size state, local attention


Top-1: recurrentgemma_griffin_architecture_chunk_002 | score: 0.5325
  Text: We provide two sizes of models, containing 2B and 9B parameters, and provide pre-trained and instruction tuned variants for both. Our models achieve comparable performance to similarly-sized Gemma bas...
  Source: data/raw/recurrentgemma_griffin_architecture.md | Section: The Griffin Architecture



Top-2: recurrentgemma_griffin_architecture_chunk_001 | score: 0.5223
  Text: # RecurrentGemma: Moving Past Transformers for Efficient Open Language Models

**Authors:** Griffin, RLHF, and Gemma Teams (Google DeepMind)
**Paper:** arXiv:2404.07839 (Apr 11, 2024)
**Code:** https:...
  Source: data/raw/recurrentgemma_griffin_architecture.md | Section: RecurrentGemma: Moving Past Transformers for Efficient Open Language Models



Top-3: recurrentgemma_griffin_architecture_chunk_004 | score: 0.4596
  Text: ----------------|-------------------|
| Total params | 2.68B | 8.58B |
| Non-Embedding params | 2.03B | 7.53B |
| Embedding params | 0.65B | 1.05B |
|

Vocabulary size | 256k | 256k |
| Model width | ...
  Source: data/raw/recurrentgemma_griffin_architecture.md | Section: Architecture Modifications



**Comment:** partially relevant


---

## Query 6: How does Prime Intellect implement RLM ablations?

**Expected:** DeepDive, math-python, Oolong, verbatim-copy environments


Top-1: prime_intellect_ablations_chunk_001 | score: 0.5763
  Text: # Prime Intellect: Recursive Language Models Ablations

**Source:** https://www.primeintellect.ai/blog/rlm
**Status:** Experimental work-in-progress, major focus of research

## The RLM Paradigm

Prim...
  Source: data/raw/prime_intellect_ablations.md | Section: Prime Intellect: Recursive Language Models Ablations



Top-2: prime_intellect_ablations_chunk_003 | score: 0.4649
  Text: nt input
- It can use sub-LLMs  --  fresh instances of itself  --  to perform work for it, and programmatically pipe parts of the input data into them

These skills combined make it a great candidate ...
  Source: data/raw/prime_intellect_ablations.md | Section: Prime Intellect's Implementation Details



Top-3: prime_intellect_context_folding_chunk_006 | score: 0.4563
  Text: it is ready to be used in any environment. They provide several RLM-based environments on the Environments Hub, and support training with `prime-rl`.

### Key Implementation Details

- **Sub-LLM calls...
  Source: data/raw/prime_intellect_context_folding.md | Section: Experimental Results Summary



**Comment:** partially relevant


---

## Query 7: What is context folding and how does RLM compare?

**Expected:** agentic context engineering, AgentFold vs RLM delegation


Top-1: prime_intellect_context_folding_chunk_005 | score: 0.5596
  Text: The RLM allows the model to actively manage its own context. This approach is more in line with The Bitter Lesson than the ones presented before; it enables training directly with the RLM scaffolding ...
  Source: data/raw/prime_intellect_context_folding.md | Section: RLM Implementation at Prime Intellect



Top-2: rlm_core_paper_and_github_chunk_003 | score: 0.5557
  Text: ## Core Concept: Context-Centric View

A recursive language model is a thin wrapper around a LM that can spawn (recursive) LM calls for intermediate

computation. From the perspective of the user or p...
  Source: data/raw/rlm_core_paper_and_github.md | Section: Core Concept: Context-Centric View



Top-3: rlm_core_paper_and_github_chunk_007 | score: 0.5371
  Text: RLMs support configurable max recursion depths:
- **Depth 0:** RLM without sub-calling capabilities (standard LM behavior).
- **Depth 1:** Allows sub-calling LLMs on specific context snippets.
- **Dep...
  Source: data/raw/rlm_core_paper_and_github.md | Section: Experimental Results



**Comment:** partially relevant


---

## Query 8: How do you install and set up the RLM system?

**Expected:** pip install, REPL environments, Docker setup


Top-1: rlm_core_paper_and_github_chunk_016 | score: 0.4581
  Text: e many amazing demos and production-ready use cases of RLMs. Notable examples that explicitly use RLMs as a central piece of their design include HALO

(Context Labs) and various agent optimization to...
  Source: data/raw/rlm_core_paper_and_github.md | Section: RLMs in the Wild



Top-2: prime_intellect_context_folding_chunk_006 | score: 0.4307
  Text: it is ready to be used in any environment. They provide several RLM-based environments on the Environments Hub, and support training with `prime-rl`.

### Key Implementation Details

- **Sub-LLM calls...
  Source: data/raw/prime_intellect_context_folding.md | Section: Experimental Results Summary



Top-3: rlm_paper_v3_updates_chunk_002 | score: 0.3536
  Text: y 2.2 MB, suggesting substantial new experimental results, additional benchmarks, or expanded theoretical analysis.

## Core Claims (Reinforced in v3)

RLMs can successfully process inputs up to two o...
  Source: data/raw/rlm_paper_v3_updates.md | Section: Core Claims (Reinforced in v3)



**Comment:** partially relevant


---

## Query 9: What benchmark results does RLM achieve on Oolong?

**Expected:** Oolong benchmark, multi-step reasoning, accuracy


Top-1: prime_intellect_ablations_chunk_013 | score: 0.6232
  Text: mation retrieval)
- RLM performs best on Verbatim Copy (precise text reproduction)
- Math Python shows RLM underperforming, suggesting the overhead of

scaffolding may not be worth it for simple math ...
  Source: data/raw/prime_intellect_ablations.md | Section: Verbatim Copy



Top-2: rlm_paper_v3_updates_chunk_002 | score: 0.5836
  Text: y 2.2 MB, suggesting substantial new experimental results, additional benchmarks, or expanded theoretical analysis.

## Core Claims (Reinforced in v3)

RLMs can successfully process inputs up to two o...
  Source: data/raw/rlm_paper_v3_updates.md | Section: Core Claims (Reinforced in v3)



Top-3: prime_intellect_ablations_chunk_010 | score: 0.5268
  Text: sessions that were recorded and from which some information was extracted.

Oolong is a complex, long-context eval that many models struggle with. The RLM has much promise because the long context is ...
  Source: data/raw/prime_intellect_ablations.md | Section: Oolong



**Comment:** partially relevant


---

## Query 10: What are the training insights for RLMs in paper v3?

**Expected:** training environment, reinforcement learning, scaling


Top-1: rlm_paper_v3_updates_chunk_002 | score: 0.5705
  Text: y 2.2 MB, suggesting substantial new experimental results, additional benchmarks, or expanded theoretical analysis.

## Core Claims (Reinforced in v3)

RLMs can successfully process inputs up to two o...
  Source: data/raw/rlm_paper_v3_updates.md | Section: Core Claims (Reinforced in v3)



Top-2: rlm_paper_v3_updates_chunk_003 | score: 0.5501
  Text: round the RLM paradigm. RLM-Qwen3-8B:
- Outperforms the underlying Qwen3-8B model by **28.3%** on average
- Approaches the quality of vanilla GPT-5 on

three long-context tasks
- Was trained on 1,000 ...
  Source: data/raw/rlm_paper_v3_updates.md | Section: Key Insight for Training



Top-3: rlm_core_paper_and_github_chunk_008 | score: 0.5244
  Text: text Deep Research task constructed from BrowseComp-Plus, RLMs outperform other methods like ReAct + test-time indexing and retrieval over the prompt.

Surprisingly, RLMs do not degrade in performance...
  Source: data/raw/rlm_core_paper_and_github.md | Section: Cost Comparison



**Comment:** partially relevant


---
