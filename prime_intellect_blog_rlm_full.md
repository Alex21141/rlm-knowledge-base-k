# Prime Intellect: Recursive Language Models — Full Blog Post

**URL:** https://www.primeintellect.ai/blog/rlm  
**Date:** 2025-2026  
**Status:** Experimental work-in-progress, major focus of research

---

## Introduction: The Context Problem

LLM agents have become significantly more useful over the course of this year. They are now capable of implementing complex changes in large codebases autonomously, often reading and editing dozens of files, searching the web, and maintaining context even over the course of multiple such complex requests.

These capabilities require the use of vast numbers of tokens. But that, in turn, is difficult for current LLMs: per-token costs rise linearly with the context length, while the performance of even the best models drops with it. A well-known phenomenon at this point is context rot, the reduction of LLM capabilities as contexts grow in size.

## Existing Approaches: File-Based Scaffolding

Claude Code, OpenAI's Codex, and similar TUI systems tend to use file-systems and context compression by LLM summarization at regular intervals as the basis of their scaffolding. This effectively leads to a succession of agents, all connected to each other by a prompt and the state of some set of files.

## Context Folding Alternatives

A different approach to the context problem is "context folding". Its goal is to have a continual, growing rollout, while managing the context window itself (instead of external files) in order to keep it short. This is compatible with the file-based scaffolding, as an LLM using context folding looks just like a normal LLM from the outside.

### Scaling Long-Horizon LLM Agent via Context-Folding

The agent can actively "branch" its rollout, and "return" from the branch. Within the branch, it retains the full previous context, but after returning, only a self-chosen summary of the branch remains in the context window.

### AgentFold: Long-Horizon Web Agents with Proactive Context Management

Every one of the agent's actions produces both a result, and a summary of the action and the reasoning that led to it. These summaries can be hierarchical, consolidating the lessons from multiple actions into a single point, or retaining per-action summaries.

### Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

A three-agent system is proposed:
1. **Generator:** Uses the current knowledge base for creating the rollout
2. **Reflector:** Takes lessons and information about the generation and about the current state of the knowledge base
3. **Curator:** Takes the Reflector's lessons and adapts the knowledge base with them in a structured manner

## Why RLM is the Best Approach

Prime Intellect believes that the simplest, most flexible method for context folding is the Recursive Language Model (RLM), introduced by Alex Zhang in October 2025 as a blog post, and now available as a full paper.

The RLM allows the model to actively manage its own context. This approach is more in line with The Bitter Lesson than the ones presented before; it enables training directly with the RLM scaffolding and getting better and better, learned context folding through end-to-end reinforcement learning.

It never actually summarizes context, which leads to information loss. Instead, it pro-actively delegates context to Python scripts and sub-LLMs.

## How the RLM Works

Rather than directly ingesting its (potentially large) input data, the RLM allows an LLM to use a persistent Python REPL to inspect and transform its input data, and to call sub-LLMs from within that Python REPL.

This enables several nice capabilities:

- Potentially huge input data, like PDFs or Datasets or videos, doesn't have to be loaded directly into a model's context, which makes the LLM leaner and avoids context rot
- The LLM can search, filter, and transform the context using Python functionality, avoiding the need to process redundant input
- It can use sub-LLMs — fresh instances of itself — to perform work for it, and programmatically pipe parts of the input data into them

These skills combined make it a great candidate for situations that typically require large context sizes.

## Prime Intellect's Implementation Details

### Parallel Sub-LLM Calls

The model has an `llm_batch` function available in the REPL, through which it can process a batch of prompts in parallel.

### Sub-LLM Tools

Any tools given to the environment will only be usable by the sub-LLMs. This decision was made because many tools produce a lot of tokens. Now, the main RLM doesn't have to see those tokens, and can instead delegate the work that requires tools.

### Package Installation

Any pip package can be installed. The RLM is made aware of which packages are installed. In math-python, for example, `numpy`, `scipy`, and `sympy` were installed. The standard library is always available. Code execution happens in isolated Sandboxes.

### Answer Variable

The RLM only ever provides an answer in a Python variable. An `answer` variable is initialized at the start of each Sandbox running the Python code; it's a dictionary with two keys:

- `"content"`: The LLM can write into this as often as it wants, and it can delete or edit the content over multiple turns
- `"ready"`: Only when this is set to `True` will the rollout end, and the answer be extracted from `"content"`

At the start of each rollout, `answer = {"content": "", ready: False}`.

This setup allows the model to generate its final answer via a form of diffusion, which occurs over the course of its reasoning chain.

### Input Data Handling

Both a prompt and extra input data can be given. The prompt is put directly into the RLM's context window, while the extra input data is available only programmatically. The only way for the RLM to view that data is to print it in the REPL. Since we limit the number of output characters from the REPL output that will be shown to the RLM in each turn (to 8192 by default, user-adjustable), the RLM is forced to make use of Python and sub-LLMs to work with input data.

## Experimental Setup

The basic setup of all experiments is to compare three scaffolds for the same environment:

1. A standard LLM with whatever tools the environment normally provides
2. The RLM
3. The RLM with environment-specific tips

This tells us how a normal LLM compares to an RLM, and to an RLM that knows how its scaffold is best used in the given environment. We directly compare to an LLM because at its core, an RLM is an abstraction around a single LLM call.

The RLM is limited in its per-REPL-call timeout, which we set to 120 seconds unless stated otherwise. This helps when the RLM writes inefficient code, but also limits its use of sub-LLM calls.

## Environments Tested

### DeepDive

DeepDive is a method for gathering data for Deep Research tasks by walking open knowledge graphs to create complex questions and verifiable answers, then obfuscating the questions via LLM re-formulation.

To solve such problems, the models have three tools available:
- `search(query: str)`: use Google via Serper. Returns an enumerated list of Google results and the corresponding URL
- `click(index: int)`: "click" on one of the results from the previous search
- `open(url: str)`: open the given URL

DeepDive requires strong tool-use. Its tools also produce many tokens; `open` can produce tens of thousands of tokens (and that is with truncation, without that we've seen 1.5 million tokens and more). The tasks also often involve many subsequent tool-calls. Therefore, DeepDive tests how well the model using the RLM harness can make use of sub-LLMs with tools, how strongly that impacts the main RLM's context length, and at what cost in parallel sub-LLMs calls.

**Environment tips for DeepDive:**
```
Strategy for deep research tasks:
1. Decompose the question into multiple smaller, focused research sub-tasks
2. Parallel sub-LLM research: Use llm_batch() to dispatch sub-tasks in parallel
3. Synthesize findings: After collecting sub-LLM responses, combine and cross-reference
4. Iterate if needed: Dispatch another batch of targeted sub-tasks
5. Finalize: Write synthesized answer to answer["content"], set answer["ready"] = True
```

### math-python

math-python poses difficult math problems, and gives an LLM a Python tool to solve those problems. Examples include triangle geometry problems and polynomial equations.

The Python REPL is very similar to the Python tool that the standard LLM gets. However, the RLM has sub-LLMs available and can break the task down into subtasks, or let sub-LLMs evaluate its work. The RLM has to manage much more complicated scaffolding.

**Environment tips for math-python:**
```
Use Python for calculations. The sympy library is available for symbolic math.
```

### Oolong

Oolong is a long-context eval with synth, synth-with-labels, and real subsets. The real dataset is constructed from real D&D playing sessions that were recorded and from which some information was extracted.

Oolong is a complex, long-context eval that many models struggle with. The RLM has much promise because the long context is accessible only through the Python REPL, where sub-LLMs can help with classification of parts of the context, while the RLM aggregates the results.

**Environment tips for Oolong:**
```
Strategy for long-context information retrieval:
1. Split the context into chunks (e.g., by paragraphs or fixed character windows with some overlap)
2. Write a prompt describing what to look for, then append it to each chunk
3. Call llm_batch() once with all prompts to scan chunks in parallel
4. Aggregate the relevant findings from the responses
```

### Verbatim Copy

LLMs often struggle to repeat complex texts verbatim. This environment auto-generates data for the model to copy, with knobs for content_type (words, json, csv, codes, mixed, all), target_length, and mean_fragment_length.

The RLM could theoretically help here: the model can write its best attempt into `answer["content"]`, without setting `answer["ready"]` to True, print it out, and then edit any errors with targeted Python functions.

**Environment tips for verbatim copy:**
```
Strategy for verbatim copying:
1. Write your initial attempt to answer["content"]
2. Print answer["content"] to see exactly what you wrote
3. Compare carefully with the original text
4. Fix any errors using string operations
5. Only set answer["ready"] = True after you have verified correctness
```

## Results Across Environments

Using GPT-5-mini as the main model:

**Mean reward by environment:**
- DeepDive: LLM ~0.58, RLM ~0.54, RLM+tips ~0.62
- Math Python: LLM ~0.44, RLM ~0.35, RLM+tips ~0.36
- Oolong: LLM ~0.43, RLM ~0.55, RLM+tips ~0.51
- Verbatim Copy: LLM ~0.83, RLM ~0.91, RLM+tips ~0.88

Key observations:
- RLM+tips performs best on DeepDive (deep research with tool use)
- RLM performs best on Oolong (long-context information retrieval)
- RLM performs best on Verbatim Copy (precise text reproduction)
- Math Python shows RLM underperforming, suggesting the overhead of scaffolding may not be worth it for simple math problems

## Models Ablated

Main ablations run with GPT-5-mini. Open source models tested through OpenRouter include GLM 4.6, GLM 4.5 Air, and INTELLECT-3. DeepSeek-v3.2 had issues with wrong function calling format. Xiaomi's Mimo-v2-flash had rate limits too strict for meaningful results.

It is very important to note that this is not meant to find out any model's absolute performance on a benchmark. We put no effort into tuning hyperparameters or optimizing individual model performance. The comparison we care about is that between the LLM and the RLM; absolute performance doesn't matter, only relative.

## RLM Implementation at Prime Intellect

Prime Intellect has implemented their version of the RLM in `verifiers` so that it is ready to be used in any environment. They provide several RLM-based environments on the Environments Hub, and support training with `prime-rl`.

### Key Implementation Details

- **Sub-LLM calls can be parallelized** via `llm_batch()` function in the REPL
- **Sub-LLMs can be given tools** — any tools given to the environment will only be usable by the sub-LLMs
- **Any pip package can be installed** — the RLM is made aware of which packages are installed
- **Code execution happens in isolated Sandboxes**
- **The RLM only ever provides an answer in a Python variable** — an `answer` dictionary with `"content"` and `"ready"` keys

## The RLM Paradigm: Why It Matters

Prime Intellect is calling RLM "the paradigm of 2026". They are building production tools around RLMs (RLMEnv) and betting big on training models natively for recursive behavior.

They believe that teaching models to manage their own context end-to-end through reinforcement learning will be the next major breakthrough, enabling agents to solve long-horizon tasks spanning weeks to months.

## Key Insight: When RLMs Help vs. Hurt

RLMs are most beneficial when:
- Contexts are extremely large (10M+ tokens)
- Tasks require complex multi-hop reasoning across documents
- Tool-use produces many tokens that would bloat the main model's context
- Tasks involve many subsequent tool-calls
- Precise text reproduction is required

RLMs may not be worth the overhead when:
- Tasks are simple and can be solved with a single tool call
- The context fits comfortably within the model's window
- The task does not require decomposition or parallel processing

## Future Work

Prime Intellect plans to scale the training of the RLM on environments that reward effective very long-horizon reasoning. They believe that teaching models to manage their own context end-to-end through reinforcement learning will be the next major breakthrough, enabling agents to solve long-horizon tasks spanning weeks to months.

## Related Resources

- **RLM Paper:** https://arxiv.org/abs/2512.24601
- **RLM Code:** https://github.com/alexzhang13/rlm
- **Prime Intellect Environments:** https://www.primeintellect.ai/environments
- **prime-rl:** https://github.com/primeintellect/prime-rl
- **verifiers:** https://github.com/primeintellect/verifiers
