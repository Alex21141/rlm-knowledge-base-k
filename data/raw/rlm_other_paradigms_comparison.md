# Chain-of-Thought (CoT)

CoT models reason step-by-step within a single forward pass. RLMs extend this by allowing the model to delegate reasoning steps to sub-calls, effectively creating a tree of thought rather than a linear chain.

# ReAct (Reasoning + Acting)

ReAct models interleave reasoning and action. RLMs can be seen as a generalization where the "action" space includes recursive sub-calls to other LMs, making the action space much more powerful.

# Tree of Thoughts (ToT)

ToT explores multiple reasoning paths in parallel. RLMs naturally implement a form of ToT where each sub-call can explore a different branch of reasoning, and the root LM selects or merges the results.

# Retrieval-Augmented Generation (RAG)

Traditional RAG retrieves relevant documents before generation. RLMs dynamically decide what to retrieve and when, and can perform multi-hop retrieval through recursive calls.

# Agentic RL

Agentic RL learns policies for NLP tasks via reinforcement learning. RLMs can be seen as a constrained agent framework where the action space is restricted to language model calls with specific function signatures.

# Mixture of Experts (MoE)

MoE activates sparse subsets of model parameters per token. RLMs activate different models/spaces conditionally, achieving similar parameter efficiency at the architecture level rather than the parameter level.

# Fine-tuning / LoRA

LoRA adapts weights via low-rank updates. RLMs achieve adaptation through execution rather than weight modification — the root model dynamically composes sub-calls based on task characteristics.

# Prompt Chaining

Prompt chaining links independent LLM calls. RLMs generalize this by allowing hierarchical composition where sub-calls can themselves invoke further sub-calls, forming a tree structure.
