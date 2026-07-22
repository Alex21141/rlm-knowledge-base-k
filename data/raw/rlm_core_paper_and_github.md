# Recursive Language Models — Core Paper and Implementation

**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)  
**Paper:** arXiv:2512.24601 (Dec 31, 2025)  
**Code:** https://github.com/alexzhang13/rlm  
**Minimal Implementation:** https://github.com/alexzhang13/rlm-minimal  
**Blog:** https://alexzhang13.github.io/blog/2025/rlm/

## Abstract

We study allowing large language models (LLMs) to process arbitrarily long prompts through the lens of inference-time scaling. We propose Recursive Language Models (RLMs), a general inference paradigm that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt.

We find that RLMs can successfully process inputs up to two orders of magnitude beyond model context windows and, even for shorter prompts, dramatically outperform the quality of vanilla frontier LLMs and common long-context and coding scaffolds across four diverse long-context tasks while having comparable cost.

At a small scale, we post-train the first model around the RLM. Our model, RLM-Qwen3-8B, outperforms the underlying Qwen3-8B model by 28.3% on average and even approaches the quality of vanilla GPT-5 on three long-context tasks.

## Core Concept: Context-Centric View

A recursive language model is a thin wrapper around a LM that can spawn (recursive) LM calls for intermediate computation. From the perspective of the user or programmer, it is the same as a model call. In other words, you query a RLM as an "API" like you would a LM, i.e. `rlm.completion(messages)` is a direct replacement for `gpt5.completion(messages)`.

We take a **context-centric view** rather than a **problem-centric view** of input decomposition. This framing retains the functional view that we want a system that can answer a particular **query** over some associated **context**.

## The Problem: Context Rot

There is a well-known but difficult to characterize phenomenon in language models known as "context rot". Anthropic defines context rot as "when the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases", but many researchers know this definition doesn't fully hit the mark.

For example, if we look at popular needle-in-the-haystack benchmarks like RULER, most frontier models actually do extremely well (90%+ on 1-year old models). But people have noticed that context rot is this weird thing that happens when your Claude Code history gets bloated, or you chat with ChatGPT for a long time — it's almost like, as the conversation goes on, the model gets dumber.

It's sort of this well-known but hard to describe failure mode that we don't talk about in our papers because we can't benchmark it. The natural solution is something along the lines of, "well maybe if I split the context into two model calls, then combine them in a third model call, I'd avoid this degradation issue". We take this intuition as the basis for a recursive language model.

## RLM Architecture with REPL Environment

An RLM acts as a mapping from text → text, but is more flexible than a standard language model call and can scale to near-infinite context lengths. An RLM allows a language model to interact with an environment (in this instance, a Python REPL environment) that stores the (potentially huge) context, where it can recursively sub-query "itself", other LM calls, or other RLM calls, to efficiently parse this context and provide a final response.

The user prompt is stored in a variable within the REPL environment. The root LM can then programmatically examine, decompose, and recursively call itself over snippets of the prompt.

### Key Components

1. **Root LM (depth=0):** The primary language model that receives the user query and orchestrates the recursive process.
2. **Sub-LM / Recursive LM (depth=1):** Smaller or same-sized models called by the root to process specific sub-tasks or context snippets.
3. **REPL Environment:** A Python environment where the prompt is stored as a variable, enabling programmatic manipulation.
4. **Sub-call Module:** A module loaded in the REPL that allows querying sub-LMs.

### Recursion Depth

RLMs support configurable max recursion depths:
- **Depth 0:** RLM without sub-calling capabilities (standard LM behavior).
- **Depth 1:** Allows sub-calling LLMs on specific context snippets.
- **Depth >1:** Allows sub-calling RLMs, enabling nested recursive reasoning.

Notation: RLM(model, depth=N), e.g., RLM(GPT-5, depth=2).

## Experimental Results

### Long Context Benchmarks

RLMs using GPT-5-mini outperform GPT-5 on a split of the most difficult long-context benchmark (OOLONG) by more than double the number of correct answers, and are cheaper per query on average.

On a new long-context Deep Research task constructed from BrowseComp-Plus, RLMs outperform other methods like ReAct + test-time indexing and retrieval over the prompt.

Surprisingly, RLMs do not degrade in performance when given 10M+ tokens at inference time.

### Cost Comparison

RLMs achieve comparable cost to vanilla models while dramatically outperforming them on quality. The cost savings come from delegating sub-tasks to smaller models (e.g., GPT-5-mini for recursive calls) rather than processing the full context with the largest model.

### Fine-tuning Results

RLM-Qwen3-8B was created by fine-tuning Qwen3-8B on 1,000 filtered trajectories of Qwen3-Coder-480B-A35B as an RLM with Qwen3-8B sub-calls on LongBenchPro tasks.

The key insight for training is that being an effective sub-call model is roughly similar to being a general purpose reasoning model, so training can be made much more tractable at small scale by focusing on improving the root model's ability to manipulate the REPL and to launch recursive calls.

## System Prompt for RLM with REPL

The RLM operates in a Python REPL environment with the following system prompt structure:

```
You are operating in a Python REPL environment. The user's prompt has been stored in a variable.
You have access to a sub-LM querying module.

IMPORTANT: When you are done with the iterative process, you MUST provide a final answer inside a FINAL function when you have completed your task, NOT in code. Do not use these tags unless you have completed your task. You have two options:

1. Use FINAL(your final answer here) to provide the answer directly
2. Use FINAL_VAR(variable_name) to return a variable you have created in the REPL environment as your final output

Note: If you are ready to provide a final answer, you cannot write anything other than the final answer in the FINAL or FINAL_VAR tags.

Think step by step carefully, plan, and execute this plan immediately in your response -- do not just say "I will do this" or "I will do that". Output to the REPL environment as much as possible. Remember to explicitly answer the original query in your final answer.
```

## Quick Setup

`rlms` requires Python 3.11 or later. Install from PyPI:

```
pip install rlms
```

The default RLM client uses a REPL environment that runs on the host process through Python `exec` calls. It uses the same virtual environment as the host process, but with some limitations in its available global modules.

Example usage with GPT-5-nano:

```python
from rlm import RLM

rlm = RLM(
    backend="openai",
    backend_kwargs={"model_name": "gpt-5-nano"},
    verbose=True,
)

print(rlm.completion("Print me the first 100 powers of two, each on a newline.").response)
```

## REPL Environments

We support two types of REPL environments — isolated, and non-isolated.

### Non-Isolated (Default)

Non-isolated environments run code execution on the same machine as the RLM (e.g. through `exec`), which is reasonable for some local low-risk tasks, like simple benchmarking, but can be problematic if the prompts or tool calls can interact with malicious users.

Supported non-isolated environments:
- **local** (default): `LocalREPL` runs in the same process as the RLM itself, with specified global and local namespaces for minimal security.
- **ipython**: `IPythonREPL` runs cells inside a real IPython session — either in-process (default) or in a separate `ipykernel` subprocess. Subprocess mode adds hard `cell_timeout` enforcement and full namespace isolation from the RLM host.
- **docker**: `DockerREPL` launches the REPL environment as a Docker image. By default, we use the `python:3.11-slim` image. The container runs fully isolated from the host; a lightweight host-side proxy bridges LM access back into the container.

### Isolated (Cloud)

Fully isolated environments use cloud-based sandboxes to run code generated by the RLM, ensuring complete isolation from the host process. Whenever a recursive sub-call is made in these instances, it is requested from the host process.

Supported isolated environments:
- **modal**: Modal Sandboxes
- **prime**: Prime Intellect Sandboxes (currently beta)
- **daytona**: Daytona Sandboxes
- **e2b**: E2B Sandboxes

## Model Providers

We currently support most major clients (OpenAI, Anthropic), as well as the router platforms (OpenRouter, Portkey). For local models, we recommend using vLLM (which interfaces with the OpenAI client).

## Training

We provide a simple RL training harness for training RLMs used in this repo (specifically the `local` REPL). The implementation uses no sandboxes for simplicity. Training logic is isolated to the `training/` folder, which exposes `rlm.RLM` as a `verifiers` `Environment` and plugs straight into `prime-rl`.

A worked example with an example `.toml` lives in `training/environments/oolong/` (OOLONG long-context QA). New training environments can be added the same way — author a `verifiers` env that wraps your task.

## Trajectory Logging and Visualizer

`RLMChatCompletion` has an optional `metadata` field that holds the full trajectory (run config + all iterations and sub-calls) so you can reconstruct the run. Pass an `RLMLogger` to capture it:

- **In-memory only:** `logger=RLMLogger()` (no `log_dir`)
- **Also save to disk:** `logger=RLMLogger(log_dir="./logs")` (JSONL for the visualizer)

To run the visualizer locally, we use Node.js and shadcn/ui:

```
cd visualizer/
npm run dev        # default localhost:3001
```

## RLMs in the Wild

There are many amazing demos and production-ready use cases of RLMs. Notable examples that explicitly use RLMs as a central piece of their design include HALO (Context Labs) and various agent optimization tools.
