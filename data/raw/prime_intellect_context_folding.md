# Context Folding and the RLM Paradigm

**Source:** https://www.primeintellect.ai/blog/rlm  
**Authors:** Prime Intellect Research Team

## The Context Problem

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

## RLM Implementation at Prime Intellect

Prime Intellect has implemented their version of the RLM in `verifiers` so that it is ready to be used in any environment. They provide several RLM-based environments on the Environments Hub, and support training with `prime-rl`.

### Key Implementation Details

- **Sub-LLM calls can be parallelized** via `llm_batch()` function in the REPL
- **Sub-LLMs can be given tools** — any tools given to the environment will only be usable by the sub-LLMs
- **Any pip package can be installed** — the RLM is made aware of which packages are installed
- **Code execution happens in isolated Sandboxes**
- **The RLM only ever provides an answer in a Python variable** — an `answer` dictionary with `"content"` and `"ready"` keys

## Experimental Results Summary

### DeepDive Results

RLM+tips performs best on DeepDive (deep research with tool use), achieving ~0.62 mean reward vs ~0.58 for standard LLM. This demonstrates that RLMs excel when tool-use produces many tokens and tasks involve many subsequent tool-calls.

### Oolong Results

RLM performs best on Oolong (long-context information retrieval), achieving ~0.55 mean reward vs ~0.43 for standard LLM. This confirms that RLMs are particularly effective when the long context is accessible only through the Python REPL, where sub-LLMs can help with classification while the RLM aggregates results.

### Verbatim Copy Results

RLM performs best on Verbatim Copy (precise text reproduction), achieving ~0.91 mean reward vs ~0.83 for standard LLM. This shows that the ability to iteratively edit answers via Python string operations is valuable.

### math-python Results

RLM underperforms on math-python (~0.35 vs ~0.44 for standard LLM), suggesting the overhead of scaffolding may not be worth it for simple math problems where a single Python REPL call suffices.

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
