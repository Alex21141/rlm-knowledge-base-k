# RLM.md — Comprehensive Guide to Recursive Language Models
**Source:** https://rlm.md

**Authors:** Community-curated from rlm.md (based on MIT OASYS Lab research by Alex L. Zhang, Tim Kraska, Omar Khattab)
**Paper:** "Recursive Language Models" — arXiv:2512.24601, Accepted at ICML 2025

---

## INDEX: 6 Sections

1. Fundamentals — The decompose-recurse-aggregate pattern
2. Techniques — REPL, decomposition, sub-calls, post-training
3. Research — Paper deep dive, benchmark results, ablations
4. Applications — Code analysis, legal, deep research, books
5. Comparison: LLM vs RLM — Two fundamentally different approaches
6. Summary — When to use RLMs

---

## 1. FUNDAMENTALS

### The Core Insight: Why Shoving Everything into Context Doesn't Work

Every LLM has a context window — a maximum number of tokens it can process at once. The industry keeps making these bigger: 128K, 272K, 1M. But size isn't the issue. **Quality is.**
Even within their stated limits, models exhibit *context rot*: performance degrades as prompts get longer, especially on tasks that require reasoning over the entire input rather than just locating a specific fact. GPT-5 handles needle-in-a-haystack fine at 200K tokens. Ask it to aggregate information from every paragraph in a 200K-token document, and it falls apart.
The degradation gets worse as task complexity increases:
- **Constant-complexity tasks** (find one thing) survive longer contexts
- **Linear-complexity tasks** (process every chunk) degrade faster
- **Quadratic-complexity tasks** (reason about pairs of chunks) collapse almost immediately
RLMs sidestep this entirely. The neural network never sees the full prompt. It only sees metadata about it — length, a short prefix, type information — and writes code to interact with it piece by piece.

### How an RLM Actually Works

An RLM wraps any base language model with an inference-time scaffold. The flow:
1. **Initialize a REPL.** Given an arbitrary-length prompt P, the RLM starts a persistent programming environment (Python REPL). P is stored as a string variable inside this environment. The model also gets a function for invoking sub-RLM calls.
2. **Provide metadata, not content.** The root model receives only constant-size metadata about P: its length, a short prefix, how to access slices of it. The full text of P never enters the model's context window.
3. **Model writes code.** The model generates code that peeks into P, slices it, transforms it, and launches sub-RLM calls on the slices. These sub-calls are themselves full RLMs that can recurse further.
4. **Execute and observe.** The REPL runs the code, updates state, and returns only metadata about stdout back to the model. Intermediate results live as variables in the REPL, not in the model's context.
5. **Aggregate and return.** When the model sets a special "Final" variable in the REPL, iteration stops and that value becomes the response.
The key: at every level of recursion, the model's context window only contains constant-size turns. All the heavy data lives in REPL variables. This is what makes unbounded input processing possible.

### The Recursive Call Pattern

```
User Prompt P (e.g., 10M tokens)
 |
 v
[RLM Root] -- sees: len(P)=10M, P[:200]="The first"
 |
 |-- writes: chunks = [P[i:i+8000] for i in range(0, len(P), 8000)]
 |-- writes: results = [sub_rlm(f"Summarize: {c}") for c in chunks]
 | |
 | +--[Sub-RLM 1] processes chunk 1 (8K tokens)
 | +--[Sub-RLM 2] processes chunk 2 (8K tokens)
 | +--[Sub-RLM 3] processes chunk 3 (8K tokens)
 | +-- (1,250 sub-calls for 10M tokens)
 |
 |-- writes: combined = "\n".join(results)
 |-- writes: Final = sub_rlm(f"Given these summaries: {combined}, answer: ")
 |
 v
Response Y
```
Each sub-RLM is itself a full RLM that can recurse further if its input is still too large. The recursion bottoms out when chunks fit comfortably in the base model's context window.

### Three Design Choices That Make RLMs Different from "Just Using Agents"

The paper identifies three specific design decisions that separate RLMs from existing agent scaffolds:
**1. The prompt is a variable, not context.** Coding agents and retrieval agents put the user prompt directly into the LLM's context window. An RLM stores it externally. This sounds trivial but it's the entire game — it means the model is never bounded by its context window with respect to user input.
**2. Output is symbolic, not autoregressive.** Standard scaffolds ask the model to generate its final answer token-by-token into the context window, which means outputs are also bounded by the window. RLMs build up the response in REPL variables, enabling unbounded output length.
**3. Recursion is programmatic, not verbal.** Previous self-delegation approaches (like Anthropic's sub-agent patterns) let models invoke themselves, but the sub-calls are generated autoregressively — one at a time, limited by output length. RLMs write *programs* that launch sub-calls inside loops, enabling the model to invoke itself O(|P|) or even O(|P|^2) times through a few lines of code.
Point 3 is the killer. A standard agent might verbalize "now process chunk 1 now process chunk 2" and run out of context after a dozen chunks. An RLM writes `for chunk in chunks: results.append(sub_rlm(chunk)` and processes thousands.

### Complexity Classes

Not all long-context tasks are created equal. The paper categorizes them by how processing complexity scales with input length:
**Constant complexity** — tasks like needle-in-a-haystack where you're looking for one thing regardless of input size. Frontier models handle these reasonably well even at long contexts. RLMs help but the gap is smaller.
**Linear complexity** — tasks like OOLONG where the answer depends on processing every chunk of the input. These break standard models quickly. RLMs with GPT-5 outperform vanilla GPT-5 by 28.4% here.
**Quadratic complexity** — tasks like OOLONG-Pairs where you need to reason about *pairs* of chunks. Vanilla GPT-5 scores below 0.1% F1. RLM(GPT-5) scores 58% F1. The gap is comical.
This hierarchy is the real insight. Context windows aren't just too small — they're the wrong abstraction for information-dense tasks. No amount of window expansion will help a model that needs to do O(n^2) semantic work in a single forward pass.

---

## 2. TECHNIQUES

### The REPL

The REPL (Read-Eval-Print Loop) is where the magic happens. When an RLM receives a prompt P, it initializes a persistent Python environment with:
- **P as a string variable** — the full prompt text, accessible by indexing/slicing
- **A sub_rlm() function** — invokes a fresh RLM on any string, returns the response
- **Standard Python** — loops, string operations, data structures, everything you'd expect
The model then generates code in iterative turns. Each turn: write code, execute it, observe metadata about the result (not the full stdout — just its length and a prefix). This forces the model to keep heavy data in REPL variables rather than polluting its own context window.
If each turn is trimmed to c tokens, you get at most K/c root iterations (where K is the context window), each of which can launch arbitrarily many sub-calls. In practice, the model self-terminates by setting a "Final" variable when it has its answer.

### Decomposition: How Models Slice Their Inputs

The model decides its own decomposition strategy. Nobody hardcodes chunk sizes or overlap windows. The model examines metadata about P (length, prefix, type) and writes appropriate slicing code. Common patterns observed in the paper:
**Fixed-size chunking** — the simplest approach. Split P into N-token chunks, process each with a sub-RLM, aggregate results. Used for straightforward aggregation tasks.
**Semantic chunking** — the model peeks at P to find natural boundaries (document separators, paragraph breaks, function definitions in code) and splits on those.
**Hierarchical decomposition** — for tasks requiring deep reasoning, the model might first chunk at a coarse level (documents), then have sub-RLMs further decompose within each document. True recursion, not just one level of delegation.
**Targeted probing** — for search-like tasks, the model might use BM25-style keyword matching in the REPL to identify relevant sections, then only launch sub-RLMs on those sections. This is why RLMs can be *cheaper* than base model calls — selective context access.
The key difference from RAG or sliding-window approaches: the model is in control. It writes the decomposition logic itself, adapting to the specific task and input structure. No one-size-fits-all chunking strategy imposed from outside.

### Sub-calls: Recursive Self-Invocation

The sub_rlm() function is what gives RLMs their recursive power. When the root model writes:
```python
results = [sub_rlm(f"Classify this text: {chunk}") for chunk in chunks]
```
Each sub_rlm() call spins up a fresh RLM instance. That instance gets its own REPL, its own context window, its own ability to recurse further. The sub-model can be the same model or a smaller/cheaper one.
In the paper's GPT-5 experiments, the root model is GPT-5 while sub-calls use GPT-5-mini — striking a balance between capability and cost. For the Qwen3-Coder experiments, the same model is used throughout.
This is fundamentally different from autoregressive sub-agent delegation. When Anthropic's agent patterns or similar scaffolds "delegate" to a sub-agent, they verbalize the delegation in their output stream — one sub-call per generated token sequence. An RLM writes a *for loop* that launches thousands of sub-calls through a few tokens of code. The semantic work scales with the program, not with the output length.

### Post-Training: Making RLM-Qwen3-8B

The paper's most surprising result might be how little training it takes to make a model natively recursive.
RLM-Qwen3-8B was created by fine-tuning Qwen3-8B on just **1,000 filtered trajectories**. These trajectories were generated by running Qwen3-Coder-480B as an RLM with Qwen3-8B sub-calls on tasks from LongBenchPro — so the training data shows what good RLM behavior looks like from a stronger model.
The clever insight: training a good sub-call model is roughly the same as training a good general-purpose reasoning model. You don't need to teach the model recursion at both levels simultaneously. Focus on teaching the root model how to manipulate the REPL and launch sub-calls effectively. The sub-call model just needs to be a competent reasoner, which smaller models already are.
The training domains were deliberately unrelated to the evaluation tasks. No overlap. Yet the model improved by a median of 28.3% across four benchmarks. The RLM scaffold is genuinely task-agnostic — learning to be recursive in one domain transfers to others.

### RLMs vs Everything Else

**vs RAG (Retrieval-Augmented Generation)** — RAG retrieves a fixed number of relevant chunks and feeds them to the model. Great for lookup tasks, terrible for aggregation. If the answer requires reasoning across every chunk in a corpus, RAG can't help you. RLMs can.
**vs Sliding Window / Context Compaction** — Summarization agents iteratively compress context as it fills up. This works okay for shallow tasks but presumes you can safely forget early details to make room for new ones. For dense reasoning tasks, that assumption is fatal. On BrowseComp-Plus, RLMs outperform the summarization baseline by over 29%.
**vs CodeAct / ReAct Agents** — These agents can execute code in a loop, but they put the user prompt directly into the model's context. They inherit all the limitations of the base model's context window. Adding BM25 retrieval helps for search tasks but doesn't address aggregation.
**vs CodeAct with Sub-calls** — The closest baseline. This gives the agent both code execution and the ability to invoke sub-LM calls. But because the prompt is in-context rather than in a variable, it still hits the wall on long inputs. The paper tests this ablation directly: on information-dense tasks, RLMs outperform by 10-59%.
**vs Bigger Context Windows** — This is the elephant in the room. Why not just wait for 10M-token context windows? Because context rot isn't a scaling problem. It's an attention problem. Bigger windows don't help if the model can't maintain quality across them. RLMs solve the quality problem, not the size problem.

### Sandbox Options

The reference implementation supports multiple REPL environments:
- **Local (default)** — Python exec in the same process. Fine for benchmarking and trusted inputs.
- **Docker** — Runs the REPL in a Docker container for isolation. Uses python:3.11-slim by default.
- **Modal Sandboxes** — Cloud-based isolated execution via Modal. Full isolation from the host process.
- **Prime Intellect Sandboxes** — Another cloud sandbox option, currently in beta.
For production use with untrusted inputs, isolated environments are non-negotiable — the model is writing and executing arbitrary code. But for research and controlled settings, the local REPL is fast and simple.

### Framework Support

**DSPy (v3.1.2+)** — Stanford's programmatic LLM framework has built-in RLM support. You can initialize an RLM with `dspy.RLM('articles, question -> trends: list[str]')` and it handles the REPL, sub-calls, and aggregation transparently. It supports using a smaller model for sub-calls via the `sub_lm` parameter to reduce costs.
**Google ADK** — Liam Connell (Google Cloud) published an enterprise-ready reimplementation of RLMs using Google's Agent Development Kit. The ADK version extends the original paper with two notable innovations: **lazy file loading** (the context object references files on disk or in GCS buckets rather than loading everything into memory) and **parallelism** (sub-calls can run concurrently rather than sequentially).
**Coding agents** — Tools like Claude Code and Gemini CLI already use sub-agent patterns that resemble RLMs. The difference is that these tools don't externalize the user prompt as a REPL variable, so they're still bounded by context limits on the input side. But the conceptual overlap suggests RLMs may become the default inference pattern for coding agents.

### The Bitter Lesson

Alex Zhang described RLMs as a "bitter-lesson-pilled approach" on X. The reference is to Rich Sutton's famous essay arguing that general methods leveraging computation always win over clever domain-specific tricks.
The insight Zhang emphasized: "LMs can often ignore most of their context for certain problems. LMs can more efficiently solve problems when only looking locally at certain parts of their input. The REPL environment provides a programmatic way for the model to peek at and infer long contexts without the model ever actually viewing it. It's a partially observable problem that you're giving the LM, where it can make logical decisions based on the structure of the task and context."
This framing matters. RLMs aren't a workaround for insufficient context windows. They're an argument that the model shouldn't see the full context in the first place — that treating the input as a partially observable environment you interact with programmatically is fundamentally more expressive than attention over a flat token sequence.

---

## 3. RESEARCH

### The Paper

"Recursive Language Models" by Alex L. Zhang, Tim Kraska, and Omar Khattab. MIT OASYS Lab. arXiv:2512.24601. Accepted at ICML 2025. This is the paper that introduced RLMs as a general inference paradigm.
The central claim: you can dramatically scale the effective input and output lengths of any LLM, at inference time, by treating the prompt as an external environment and enabling symbolic recursion.
This isn't another "we made the context window bigger" paper. It's an argument that the entire paradigm of stuffing tokens into a Transformer is wrong for information-dense tasks, and that the right abstraction is recursive self-invocation over programmatic slices of the input.
The evidence is strong. Four diverse benchmarks, two frontier models (GPT-5 and Qwen3-Coder-480B), multiple baselines (vanilla LLM, CodeAct, CodeAct+BM25, summary agents, CodeAct with sub-calls), and a small-scale post-training experiment. The results are consistent across all of them.

### Four Tasks, Four Complexity Levels

**S-NIAH (Single Needle in a Haystack)** — Find a specific phrase or number in a large body of unrelated text. 50 tasks. Complexity: O(1) with respect to input length. This is the easy case — frontier models already handle it well at moderate lengths.
**BrowseComp-Plus (1K documents)** — Multi-hop question answering over 1,000 documents. Requires piecing together information from several gold/evidence documents buried in hard negatives. 150 instances. Harder than S-NIAH because it requires finding and connecting multiple documents.
**OOLONG (trec_coarse)** — Transform every chunk of input semantically, then aggregate to form a final answer. 50 tasks. Complexity: O(n) — the answer depends on nearly every entry in the dataset. This is where standard models start breaking hard.
**OOLONG-Pairs** — A modified version requiring aggregation over *pairs* of chunks. 20 tasks. Complexity: O(n^2). The worst case for standard models. Frontier models essentially can't solve this at all.

### Benchmark Results

| Method | S-NIAH | BrowseComp+ | OOLONG | OOLONG-Pairs |
| GPT-5 (vanilla) | 92.0 | * | 41.1 | <0.1 |
| **RLM(GPT-5)** | **98.0** | **47.3** | **69.5** | **58.0** |
| Summary Agent (GPT-5) | — | 18.0 | 48.8 | 1.5 |
| CodeAct+BM25 (GPT-5) | 98.0 | 41.3 | 24.5 | <0.1 |
| Qwen3-8B (vanilla) | * | * | low | low |
| **RLM-Qwen3-8B** | **+28.3% avg improvement over base** | | | |
* indicates input exceeded context limits.
The standout: OOLONG-Pairs. GPT-5 scores essentially zero. The RLM version scores 58% F1. This is a task that is mathematically impossible to solve well in a single forward pass because it requires O(n^2) semantic operations. The RLM writes a nested loop that compares every pair of entries — exactly the kind of thing no amount of attention mechanism improvement will achieve.

### Performance vs Input Length Scaling

Figure 1 of the paper plots performance on S-NIAH, OOLONG, and OOLONG-Pairs as input length scales from 2^13 (8K) to 2^18 (262K) tokens.
- **S-NIAH (constant complexity):** GPT-5 holds steady, the RLM holds steady. Not much difference at shorter lengths — the gap appears beyond 2^14 tokens.
- **OOLONG (linear complexity):** GPT-5 degrades steadily. The RLM maintains strong performance throughout. The crossover happens around 2^14 tokens.
- **OOLONG-Pairs (quadratic complexity):** GPT-5 collapses immediately. Even at 2^13 tokens (the shortest tested), it's already struggling. The RLM maintains reasonable performance across the entire range.
Beyond 2^18 tokens (past GPT-5's 272K context window), the base model simply can't run. The RLM keeps going.
The paper also tested at the 10M+ token scale on BrowseComp-Plus, where input corpora are 6-11M tokens. A linearly extrapolated cost for GPT-5-mini ingesting that much would be $1.50-$2.75. The RLM averaged $0.99 while outperforming all baselines by 29%+.

### Cost Analysis

One of the more counterintuitive findings: RLMs are often *cheaper* than base model calls. At the 50th percentile, RLM(GPT-5) costs less than vanilla GPT-5 across most benchmarks.
Why? Because the RLM selectively examines context. Instead of ingesting a full 200K-token prompt, it might only look at 30K tokens total across its sub-calls. You pay for what you use.
The catch: high variance. At the 95th percentile, some RLM runs are significantly more expensive due to long trajectories. The model sometimes explores more paths than necessary. Compared to the summarization agent (which always ingests everything), RLMs are up to 3x cheaper at comparable performance levels.

### Ablations: What Actually Matters

The paper runs careful ablations:
**REPL without sub-calls:** Just having the prompt as an external variable (without recursive self-invocation) already helps a lot. It beats most baselines and scales beyond context limits. But on information-dense tasks (OOLONG, OOLONG-Pairs), sub-calls provide an additional 10-59% improvement.
**CodeAct with sub-calls (but prompt in context):** Giving an agent sub-call ability without externalizing the prompt doesn't close the gap. The prompt-in-context bottleneck is real.
**Different root/sub models:** Using a cheaper model for sub-calls (GPT-5-mini for subs, GPT-5 for root) works well and reduces cost. The sub-call model doesn't need to be as capable as the root.
The takeaway: both the REPL (prompt as variable) and symbolic recursion (programmatic sub-calls) contribute independently, and their combination is greater than either alone.

### Where RLMs Sit in the Literature

RLMs draw on and improve several existing lines of research:
**Inference-time compute scaling** — the reasoning model paradigm (OpenAI o-series, DeepSeek-R1) showed that spending more compute at inference improves results. RLMs apply the same idea to context length rather than reasoning depth.
**Coding agents** (CodeAct, SWE-agent) — these treat external files as an environment, but can't handle arbitrarily long user prompts because the prompt still goes into context.
**Self-delegation** (Anthropic sub-agents, Sentient AI) — these let models invoke themselves, but autoregressively rather than programmatically, limiting the scale of delegation.
**Context compaction** (DSPy, OpenAI context condensation) — useful for agent trajectories but lossy for dense reasoning tasks.
The theoretical contribution: RLMs show that with symbolic recursion and external prompt storage, you can achieve effectively unbounded input tokens, unbounded output tokens, and unbounded semantic horizon.

---

## 4. APPLICATIONS

### Deep Research: Reasoning Over Massive Document Corpora

The paper benchmarks RLMs on BrowseComp-Plus, a deep research task that requires reasoning over 1,000 documents to answer multi-hop questions. The documents contain gold evidence, supporting evidence, and hard negatives — mimicking real-world research scenarios where you have a huge corpus and need to find and connect the relevant pieces.
At 6-11 million tokens of input, no standard model can even fit this in context. RAG helps for simple lookups but fails when the answer requires synthesizing information across multiple documents that wouldn't all appear in a top-k retrieval. The RLM approach lets the model systematically examine the corpus, identify relevant documents, and recursively reason over their connections.
Any organization sitting on thousands of reports, memos, research papers, or technical documents could use RLMs to answer questions that span their entire knowledge base. Not retrieval — actual dense reasoning across everything.

### Code: Understanding Entire Repositories

The LongBench-v2 CodeQA benchmark tests exactly this: given a code repository, answer questions that require understanding the relationships between multiple files. This is the kind of task that developers do every day when onboarding to a new codebase or debugging cross-module issues.
Current AI coding assistants typically work file-by-file or with a handful of files in context. RLMs can process an entire repository as a single prompt, recursively examining files, tracing dependencies, and building up an understanding of the codebase structure before answering specific questions about it.
The model writes code to explore the repo — listing files, reading specific functions, tracing imports — using the same kind of systematic exploration a human developer would. But it does it across the entire codebase simultaneously, with sub-RLMs processing individual files in parallel.

### Legal: Contract Analysis at Scale

Consider a due diligence review: hundreds of contracts, each dozens of pages, and you need to identify every instance of a specific clause type, compare terms across all agreements, and flag inconsistencies. This is O(n) or O(n^2) work depending on whether you need cross-document comparison.
Standard models can summarize individual contracts fine. But "find every non-compete clause across 500 employment agreements and identify which ones have terms inconsistent with the master agreement" requires dense processing of every document and comparison across all of them. That's exactly the pattern RLMs excel at — decompose into individual documents, extract relevant clauses via sub-RLMs, then aggregate and compare.
The OOLONG benchmark results are directly relevant here. OOLONG requires transforming each chunk of input semantically and then aggregating — precisely what contract analysis demands. RLMs outperform vanilla GPT-5 by 28.4% on this class of task.

### Books and Long-Form: Processing Book-Length Texts

A typical novel is 80,000-100,000 words, roughly 100K-130K tokens. That fits (barely) in some context windows. But actually reasoning over an entire book — tracking character arcs, identifying thematic patterns, cross-referencing plot points across chapters — degrades rapidly even within window limits.
RLMs make book-length analysis practical. The model can recursively process chapters, extract structured information from each, and then reason over the extracted data. For literary analysis, this means genuine engagement with the full text rather than a lossy summary. For nonfiction, it means synthesizing arguments and evidence across an entire work.
Scale this up to multiple books — comparative literature analysis, regulatory code spanning thousands of pages, historical archives — and you're in territory where no other approach comes close.

### Integration with Agent Frameworks

RLMs are designed as a drop-in replacement for standard LLM completion calls. The API surface is identical: `rlm.completion(prompt, model)` instead of `llm.completion(prompt, model)`. This makes integration with existing agent frameworks straightforward.
The Google ADK (Agent Development Kit) community has already started discussing RLM integration for building agents that need to process long contexts. Any ADK agent that currently hits context limits on long inputs could swap in an RLM completion call and immediately gain the ability to handle 10M+ token inputs.
Liam Connell's ADK implementation introduced **lazy file loading** — instead of loading all context into memory, the RLM holds references to files on disk or in GCS/Sharepoint. The model calls methods to read metadata and contents on demand. This is a practical extension that makes RLMs viable for enterprise document stores where downloading everything upfront is impossible.

### Task Decomposition

A subtlety that the community coverage has surfaced: RLMs don't just decompose context. They decompose *tasks*.
When an agent invokes sub_rlm(), it sets both the query (task definition) and the context that the child agent receives. This means RLMs can tackle reasoning problems that exceed a single model's capacity — not because the input is too long, but because the reasoning chain itself is too complex for one context window.
This opens up a second axis of scaling beyond context length: reasoning depth. The root model can delegate sub-problems that themselves require extended reasoning, each in their own fresh context window.

### When to Reach for an RLM

RLMs are not always the right tool. The paper is honest about this: for short inputs within the model's effective context window, vanilla LLM calls are simpler and sometimes better. There's a crossover point around 2^14 tokens (16K) where RLMs start outperforming.
**Use an RLM when:**
- Your input exceeds the model's context window
- Your input fits in context but the task requires dense reasoning over most of it (not just finding one thing)
- The task involves cross-referencing or comparing multiple sections of the input
- You need to scale to millions of tokens
**Don't bother with an RLM when:**
- Your input is short and the task is straightforward
- You just need to find one specific piece of information (RAG is cheaper)
- Latency is more important than quality (RLMs add wall-clock time from multiple calls)

---

## 5. COMPARISON: LLM vs RLM

Two fundamentally different approaches to processing long inputs.
| Feature | Large Language Model | Recursive Language Model |
| Context window | 272K tokens (fixed) | 10M+ tokens (stored as env variable) |
| Input handling | Entire input at once | Decompose → chunk → recurse → aggregate |
| Processing | Single forward pass over ALL tokens | REPL environment with sub-RLM calls |
| Attention | Over ALL tokens simultaneously | Only on current turn (constant size) |
| Output quality on long inputs | Degrades with length | Maintains quality — unbounded |
| Context rot | Yes — inevitable at scale | No — model never sees full context |
| Scalability | Bounded by context window | Limited only by compute budget |
| Cost at scale | Proportional to input size | Often cheaper (selective examination) |

### The Problem: Context Windows Are a Lie

GPT-5 advertises a 272K token context window. Sounds generous. But feed it a task that requires dense reasoning over all 272K tokens — not just finding a needle, but actually processing every line — and performance falls off a cliff. This is called **context rot**, and every model suffers from it.
The industry response has been to make windows bigger. 1M tokens. 10M tokens. But bigger windows don't solve the fundamental issue: Transformers degrade on long, information-dense inputs regardless of what fits technically.
RLMs take a different approach. Instead of forcing the entire prompt through the neural network at once, they let the model **programmatically examine, decompose, and recursively call itself** over pieces of the input. The prompt lives in a REPL environment as a variable. The model writes code to slice it, process the slices, and aggregate results.
The result: effective processing of 10M+ token inputs. Not with summarization hacks or retrieval tricks. With actual dense semantic work across the entire input.

---

## 6. SUMMARY

### Headline Numbers

RLM-Qwen3-8B — an 8-billion parameter model post-trained on just 1,000 samples — outperforms the base Qwen3-8B by **28.3% on average** across four diverse long-context benchmarks. It approaches the quality of vanilla GPT-5 on three of them.
At the frontier scale, RLM(GPT-5) maintains strong performance on inputs up to 2^18 tokens (262K+), while vanilla GPT-5 degrades sharply as inputs grow. On OOLONG-Pairs — a task requiring quadratic-complexity reasoning — GPT-5 scores less than 0.1% F1. The RLM version scores 58%.
The cost? Comparable. At the median, RLM runs are actually *cheaper* than base model calls on GPT-5, because the model selectively examines context rather than ingesting everything at once.

### Two Key Takeaways

1. **Validation of a RAG system is only feasible during operation** — robustness evolves rather than being designed in at the start
2. **RLMs treat the prompt as a variable, not context** — the model writes code to interact with it piece by piece, enabling unbounded input processing
> "It's a partially observable problem that you're giving the LM, where it can make logical decisions based on the structure of the task and context." — Alex Zhang, MIT CSAIL

### The Ecosystem Is Moving

DSPy (v3.1.2+) ships with built-in RLM support. Google's Agent Development Kit has an enterprise-ready implementation with lazy file loading and parallel sub-calls. VentureBeat, InfoQ, and Towards Data Science have all published deep dives. This isn't a paper that got filed away — it's being adopted.

---

**Full Paper:** arXiv:2512.24601 ()
**Website:**
**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab
**Affiliation:** MIT OASYS Lab
**Venue:** ICML 2025
