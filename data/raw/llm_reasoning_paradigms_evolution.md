# LLM Reasoning Paradigms Evolution: From Prompting to Recursive Systems (Deepan MN, Medium Jan 2026)

**Source:** https://medium.com/@mndeepan06/recursive-language-models-rlms-from-prompting-to-recursive-systems
**Author:** Deepan MN (AI Engineer, Zoho)
**Date:** January 20, 2026

## Single-Prompt Reasoning: The Starting Point

Single-prompt reasoning is the most basic way we interact with Large Language Models: one prompt in, one answer out. All reasoning — if it happens at all — is implicit and compressed into a single generation. The model does not break the problem into steps, verify intermediate results, or store any state beyond the given prompt. This approach works well for simple questions, pattern completion, and shallow reasoning tasks. However, it becomes brittle as task complexity increases. Because there is no explicit decomposition, the model must solve everything in one pass. Multi-step problems, long inputs, and information-dense tasks often lead to confident but incorrect answers. Single-prompt reasoning established the baseline capabilities of LLMs — but it also exposed a key limitation: Good language modeling does not automatically imply good reasoning. This limitation motivated the next evolution: making reasoning explicit through chains.

## Chain-of-Thought & Chain-of-Prompting

Chain-of-Thought (CoT) and Chain-of-Prompting emerged to address a key weakness of single-prompt reasoning: the lack of explicit reasoning steps. Instead of forcing the model to solve everything in one pass, these approaches encourage the model to reason step by step, either within a single prompt or across multiple prompts. By making intermediate reasoning explicit, LLMs show significant improvements on mathematical reasoning, logical inference, and multi-step problem solving. This was a major breakthrough. It demonstrated that how a model reasons can matter as much as model size.
However, these methods still share an important constraint. All reasoning happens inside the token context. As chains grow longer: token usage increases, attention degrades, and earlier reasoning steps become less influential. This leads to context rot, where longer chains do not reliably produce better answers. Chain-of-Prompting improves how models think, but not how much they can reason over. As tasks grow longer and more information-dense, a new question emerges: What happens when reasoning itself no longer fits inside the context window? Answering that question led to the next shift — tool-augmented reasoning.

## Tool-Augmented Reasoning (ReAct, Code-Calling)

Tool-augmented reasoning extends chain-of-thought by allowing LLMs to act, not just think. Instead of relying solely on natural language reasoning, the model can invoke external tools such as code execution, calculators, search APIs, and databases. Frameworks like ReAct combine reasoning and action in a loop: the model thinks, uses a tool, observes the result, and continues reasoning. This significantly improves performance on tasks that require precise computation, external knowledge access, and verification of intermediate results.
However, despite this added power, a core limitation remains. The reasoning trajectory still lives in tokens. Each thought, tool call, and observation accumulates context. As tasks grow longer or require many steps, token usage increases, attention weakens, and the system becomes harder to control. Tool use improves capability, but not scalability. Tools help LLMs act better, but they don't solve long-context reasoning. To address large knowledge and long inputs more directly, the next paradigm focused on retrieval.

## Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) was introduced to address a practical limitation of LLMs: they cannot reliably store or recall all relevant knowledge. Instead of placing all information inside the prompt, RAG retrieves a small set of relevant documents or chunks from an external knowledge base and injects them into the model's context at inference time. This works well when information is sparse, relevant facts can be retrieved independently, and the task depends on a few key passages. RAG significantly reduces hallucinations and improves factual accuracy, making it a popular choice for enterprise and production systems.
However, RAG introduces a different kind of bottleneck. Because only a subset of the data is retrieved, RAG struggles when answers depend on global structure, reasoning requires aggregating information across many chunks, or important details are distributed throughout the input. In these cases, retrieval becomes lossy. What is not retrieved is effectively invisible to the model. RAG optimizes what to read, not how to reason over everything. As tasks began requiring long-horizon planning, aggregation, and decision-making, systems evolved again — this time toward agent-based reasoning.

## Agent-Based Systems

Agent-based systems extend LLMs beyond single interactions by giving them goals, memory, tools, and autonomy. Instead of answering a single prompt, an agent can plan multiple steps, decide what tools to use, store intermediate results, and execute long-running tasks. This makes agents well-suited for workflows like research, coding assistance, and task automation.
However, autonomy introduces new challenges. As agents operate over many steps, their reasoning trajectories grow longer. Each decision adds tokens, increasing the risk of drift, compounding errors, and loss of earlier context. Memory mechanisms often rely on summarization, which can discard important details. In practice, agents are powerful but fragile. Agents add autonomy, but not guaranteed scalability in reasoning. To address these limitations, many turned to a seemingly straightforward solution: making context windows larger.

## Context Window Scaling

The most direct response to long-context limitations has been scaling context windows. Modern models now support 128K, 200K, and even 1M+ token windows. On the surface, this seems like the perfect solution: simply give the model more room. And for certain tasks, it works. Needle-in-a-haystack benchmarks show models can retrieve specific facts from very long contexts.
However, this approach has fundamental limits. Context rot — the degradation of performance with increasing input length — becomes more pronounced. The cost of processing longer contexts grows super-linearly with attention mechanisms. And crucially, giving the model more room doesn't change how it reasons within that space. A model that struggles to reason over 32K tokens will not suddenly become better at reasoning over 1M tokens — it will just have more context to struggle with. Context window scaling addresses the quantity of information, but not the quality of reasoning over that information. This led researchers to explore a different axis: scaling compute at inference time rather than scaling parameters or context.

## Inference-Time Scaling

Inference-time scaling represents a paradigm shift: instead of making models bigger or giving them more context, allocate more computation during inference. Chain-of-thought reasoning was an early form of this — the model spends more tokens generating intermediate steps rather than jumping to an answer. Recent developments have systematized this approach through methods like self-consistency (sampling multiple reasoning paths and voting), tree-of-thought (exploring branches with backtracking), and reinforcement learning from feedback.
OpenAI's o1 and DeepSeek-R1 demonstrate the power of this approach. These models allocate significant compute at test time — generating long chains of reasoning, self-verifying, and correcting errors — to achieve dramatically better performance on complex reasoning tasks. The key insight is that reasoning quality can scale with inference-time compute, even for fixed-size models.
However, inference-time scaling alone has limits. When the information itself exceeds what fits in context, no amount of extra thinking helps. The model cannot reason over information it cannot see. This reveals a deeper structural issue: the assumption that all reasoning must happen within a single model call with bounded context. Recursive Language Models propose to break this assumption entirely.

## Recursive Language Models (RLMs): The Core Shift

Recursive Language Models (RLMs) represent a fundamental rethinking of how language models interact with information. Instead of treating the prompt as a fixed token sequence, RLMs treat context as a variable in an external environment that the model can interact with programmatically. The model does not receive the entire context as tokens. Instead, it receives a query and can write code to explore, filter, and partition the context stored as a variable in a REPL environment.
This design choice has profound implications. The root model's context window stays small — it never sees the entire input at once. It can recursively call itself or other models on partitions of the context. Each recursive call also operates on a small context window, processing a subset of the input. The model orchestrates its own reasoning over arbitrarily large inputs by decomposing and composing, rather than trying to fit everything into one context window.
This shift from tokens to state to systems is what distinguishes RLMs from all previous approaches. Every prior paradigm tried to make reasoning better within a single context window. RLMs change the question from "how to reason in context" to "how to interact with information to reason."

## RLMs vs Other Reasoning Paradigms

| Paradigm | Strengths | Limitations | RLM advantage |
| Single-prompt | Simple, fast | No decomposition, brittle | Recursive decomposition |
| CoT | Explicit steps | All reasoning in context | Context as external variable |
| Tool-augmented | External tools | Trajectory accumulates tokens | Programmatic exploration |
| RAG | Factual accuracy | Lossy retrieval | Adaptive, non-lossy search |
| GraphRAG | Entity relationships | Expensive indexing | No upfront indexing |
| Agents | Autonomous, flexible | Fragile over many steps | Guaranteed scalability |
| Context scaling | Simple solution | Context rot | No context degradation |
| Inference-time | Better reasoning | Bounded by context | Context-independent |

## Mental Model Shift: Tokens → State → Systems

The evolution of LLM reasoning paradigms reveals a deeper pattern: a shift from tokens to state to systems. Early approaches treated reasoning as a property of text generation — how to generate better tokens. Later approaches added state — intermediate steps, tool calls, retrieved chunks. RLMs complete this evolution by treating reasoning as a system-level property — how a model orchestrates its interaction with information across time and recursive calls.
This mental model shift is critical. It means the bottleneck is not the model's parameters or context window — it's the system design. As LLMs move into production, the winners will not be those with the biggest models or longest context windows. They will be those who design the best systems for how models interact with information.

## Practical Implications: When and Where RLMs Matter

RLMs are particularly valuable when: the input is very large (beyond context window), answers depend on global structure, reasoning requires aggregation across many parts, or the task requires adaptive exploration. They are less critical for simple lookups, tasks that fit in context, or when retrieval-based approaches suffice.
The practical recommendation: use the right tool for the task. RAG for factual QA over knowledge bases. RLMs for deep analysis of large documents. Agents for autonomous workflows. The key is understanding where each paradigm breaks — and choosing accordingly.

## Open Questions & Future Directions

Several open questions remain: How should RLMs be trained? Current approaches rely on prompt engineering and zero-shot reasoning — explicit RL training for recursive reasoning is unexplored. What is the optimal recursion depth? Current experiments use depth=1 — deeper recursion may enable stronger reasoning but introduces complexity. How do RLMs integrate with other paradigms? Can RAG be used within RLM sub-calls? Can agents use RLMs as their reasoning engine? These questions point to a future where reasoning paradigms are composed rather than competing.

## Conclusion

The evolution of LLM reasoning is not just about bigger models or longer context windows. It is about how models reason and interact with information. Early approaches relied on prompts and token-based reasoning. Later methods added chains, tools, retrieval, and agents — but many of them still struggled with long, information-dense tasks. Recursive Language Models introduce a different idea: treat context as state, not tokens, and treat reasoning as interaction, not generation. This shift shows that many limitations of LLMs are system-level issues, not model-level ones. As LLMs move into real-world, long-horizon applications, progress will depend less on prompt engineering and more on system design and orchestration. The future of LLM reasoning lies beyond prompts — in systems.
