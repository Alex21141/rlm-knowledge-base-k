# Alex Zhang Blog: Recursive Language Models (Oct 2025)

**Source:** https://alexzhang13.github.io/blog/2025/rlm/  
**Full Paper:** https://arxiv.org/abs/2512.24601  
**Code:** https://github.com/alexzhang13/rlm  
**Minimal Implementation:** https://github.com/alexzhang13/rlm-minimal

## tl;dr

We explore language models that recursively call themselves or other LLMs before providing a final answer. Our goal is to enable the processing of essentially unbounded input context length and output length and to mitigate degradation "context rot".

We propose Recursive Language Models, or RLMs, a general inference strategy where language models can decompose and recursively interact with their input context as a variable. We design a specific instantiation where GPT-5 or GPT-5-mini is queried in a Python REPL environment that stores the user's prompt in a variable.

We demonstrate that an RLM using GPT-5-mini outperforms GPT-5 on a split of the most difficult long-context benchmark (OOLONG) by more than double the number of correct answers, and is cheaper per query on average. We also construct a new long-context Deep Research task from BrowseComp-Plus. On it, we observe that RLMs outperform other methods like ReAct + test-time indexing and retrieval over the prompt. Surprisingly, we find that RLMs also do not degrade in performance when given 10M+ tokens at inference time.

We are excited to share these very early results, and argue that RLMs will be a powerful paradigm very soon. We think that RLMs trained explicitly to recursively reason are likely to represent the next milestone in general-purpose inference-time scaling after CoT-style reasoning models and ReAct-style agent models.

## Prelude: Why is "Long-Context" Research So Unsatisfactory?

There is this well-known but difficult to characterize phenomenon in language models known as "context rot". Anthropic defines context rot as "when the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases", but many researchers in the community know this definition doesn't fully hit the mark.

For example, if we look at popular needle-in-the-haystack benchmarks like RULER, most frontier models actually do extremely well (90%+ on 1-year old models). But people have noticed that context rot is this weird thing that happens when your Claude Code history gets bloated, or you chat with ChatGPT for a long time — it's almost like, as the conversation goes on, the model gets dumber.

It's sort of this well-known but hard to describe failure mode that we don't talk about in our papers because we can't benchmark it. The natural solution is something along the lines of, "well maybe if I split the context into two model calls, then combine them in a third model call, I'd avoid this degradation issue". We take this intuition as the basis for a recursive language model.

## Recursive Language Models (RLMs)

A recursive language model is a thin wrapper around a LM that can spawn (recursive) LM calls for intermediate computation. From the perspective of the user or programmer, it is the same as a model call. In other words, you query a RLM as an "API" like you would a LM, i.e. `rlm.completion(messages)` is a direct replacement for `gpt5.completion(messages)`.

We take a **context-centric view** rather than a **problem-centric view** of input decomposition. This framing retains the functional view that we want a system that can answer a particular **query** over some associated **context**.

### From the User/API Perspective

From the outside, an RLM looks identical to a standard LM call:
- Input: context + query
- Output: response

The user sees no difference. Under the hood, a RLM provides only the **query** to the LM (which we call the **root LM**, or LM with depth=0), and allows this LM to interact with an **environment**, which stores the (potentially huge) **context**.

### The REPL Environment

We choose the **environment** to be a loop where the LM can write to and read the output of cells of a Python REPL Notebook (similar to a Jupyter Notebook environment) that is pre-loaded with the **context** as a variable in memory.

The **root LM** has the ability to call a recursive LM (or LM with depth=1) inside the REPL **environment** as if it were a function in code, allowing it to naturally peek at, partition, grep through, and launch recursive sub-queries over the **context**.

### Example RLM Workflow

1. The root LM receives the query and knows the context is available as a variable in the REPL
2. The root LM writes Python code to examine the context: `print(context[:2000])` to peek at structure
3. The root LM identifies relevant sections and launches sub-LM calls via `llm_query()` or `llm_batch()`
4. Each sub-LM processes its assigned snippet and returns a sub-response
5. The root LM aggregates sub-responses and produces the final answer

## Key Results

### OOLONG Benchmark

RLM using GPT-5-mini outperforms GPT-5 on OOLONG by more than double the number of correct answers, and is cheaper per query on average.

### BrowseComp-Plus Deep Research

We construct a new long-context Deep Research task from BrowseComp-Plus. RLMs outperform ReAct + test-time indexing and retrieval over the prompt.

### 10M+ Token Contexts

Surprisingly, RLMs do not degrade in performance when given 10M+ tokens at inference time. This is two orders of magnitude beyond typical model context windows.

## The Bigger Vision

RLMs are not just a long-context hack. They are a step toward models that actively manage their cognition — decomposing problems, verifying steps, delegating subtasks, and scaling to video, lifelong memory, or complex agents.

Teaching models to manage their own context end-to-end through reinforcement learning will be the next major breakthrough, enabling agents to solve long-horizon tasks spanning weeks to months.

In 2026, we might stop bragging about context-window size and start asking: "How recursively smart is your model?"

## Comparison with Other Paradigms

### Chain-of-Thought (CoT)

CoT models reason step-by-step within a single forward pass. RLMs extend this by allowing the model to delegate reasoning steps to sub-calls, effectively creating a tree of thought rather than a linear chain.

### ReAct (Reasoning + Acting)

ReAct models interleave reasoning and action. RLMs can be seen as a generalization where the "action" space includes recursive sub-calls to other LMs, making the action space much more powerful.

### Tree of Thoughts (ToT)

ToT explores multiple reasoning paths in parallel. RLMs naturally implement a form of ToT where each sub-call can explore a different branch of reasoning, and the root LM selects or merges the results.

### Retrieval-Augmented Generation (RAG)

Traditional RAG retrieves relevant documents before generation. RLMs dynamically decide what to retrieve and when, and can perform multi-hop retrieval through recursive calls.

## Future Directions

- Training models natively for recursive behavior through RL
- Scaling to video and multimodal contexts
- Lifelong memory integration
- Complex multi-agent systems with recursive delegation
- Context folding as an alternative to explicit file-based scaffolding

## Citation

```
@misc{zhang2026recursivelanguagemodels,
      title={Recursive Language Models},
      author={Alex L. Zhang and Tim Kraska and Omar Khattab},
      year={2026},
      eprint={2512.24601},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2512.24601},
}
```
