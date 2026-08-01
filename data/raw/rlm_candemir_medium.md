# Recursive Language Models: How LLMs Learned to Stop Memorizing and Start Searching

**Source:** 
**Author:** Can Demir
**Date:** February 18, 2026
**Tags:** RLM, context rot, beginner guide, out-of-core algorithms, inference paradigm

---

_A beginner-friendly guide to the inference paradigm that lets AI process 100x more context — no retraining required_

## Part 1: The Problem That Needed Solving

## Your Brain Doesn't Work Like an LLM

Imagine I hand you a 500-page novel and ask: "What color was the hat the shopkeeper was wearing in Chapter 3?" You wouldn't try to memorize the entire book first. You'd flip to Chapter 3, scan for the relevant scene, and find the answer.

Now imagine I told you: "No flipping allowed. Read the entire book once, front to back, and _then_ answer my question."

That's essentially what we ask LLMs to do. When you paste a long document into ChatGPT or Claude, the model processes every single token in one pass. It has to hold the entire context in its "working memory" simultaneously. For short inputs, this works beautifully. For long inputs, things start to fall apart.

## What Is Context Rot, Really?

The term "context rot" describes a well-documented but somewhat mysterious phenomenon: as the amount of text you feed into a language model grows, the model's ability to recall and reason about that text degrades — sometimes dramatically.

This isn't just a theoretical concern. Practitioners encounter it constantly. If you've used an AI coding assistant for a long session, you might have noticed the model getting "dumber" as the conversation history grows. If you've asked an LLM to analyze a long legal document, you might have found it missing critical clauses. These are manifestations of context rot.

The research backs this up. Studies using "needle in a haystack" tests — where a specific fact is hidden somewhere in a long document — consistently show that models struggle to find information placed in the middle of long contexts. Even models that technically support 100K or 200K token windows often show meaningful performance degradation well before hitting those limits. In some evaluations, the effective context length where performance remains reliable is only about half of the advertised window — or less.

## Why "Just Make the Window Bigger" Doesn't Work

The natural response is: why not just make context windows larger? And indeed, the industry has been racing to do exactly that. We've gone from 4K tokens to 32K, then 128K, 200K, even 1 million tokens.

But this approach runs into three stubborn problems.

**First, attention is expensive.** The core mechanism of modern LLMs — the Transformer's self-attention — scales quadratically with sequence length. Double the context, and the computation roughly quadruples. This means longer contexts are dramatically slower and more expensive.

**Second, more context doesn't mean better understanding.** This is the counterintuitive part. Even when a model technically has enough room for your entire document, it doesn't mean it can effectively use all that information. The model still processes everything in one pass, and its ability to attend to relevant details degrades as the haystack grows.

**Third, there's an information-theoretic argument.** As Alex Zhang, the lead author of the RLM paper, has pointed out: there's a fundamental entropy argument suggesting you need exponentially more training data as you increase the effective context window. Simply making the window bigger is fighting an uphill battle.

The deeper issue is architectural. We're trying to solve a _systems problem_ with a _model problem_. And that distinction is exactly where RLMs come in.

## Part 2: The Key Insight — From Memorizing to Searching

## The Librarian, Not the Speed Reader

This is where it gets interesting. The RLM paper's core insight draws from a concept in classical computer science called **out-of-core algorithms**.

Here's the idea. In traditional computing, when a dataset is too large to fit into a computer's main memory (RAM), you don't try to load it all at once. Instead, you keep the data on disk and fetch only the chunks you need, when you need them. This is how databases have worked for decades. It's how your operating system handles files larger than your available memory.

The RLM researchers asked: why don't we do the same thing with LLMs?

Think of it this way. A standard LLM is like a speed reader who tries to memorize an entire encyclopedia before answering your question. An RLM is like a **librarian**. The librarian doesn't memorize every book in the library. Instead, she knows how to navigate the catalog, find the right shelf, pull the relevant book, and look up exactly what you need. She might even delegate — asking an assistant to check one section while she checks another.

The librarian doesn't need a bigger brain. She needs a better _system_.

## The Fundamental Shift

Here's the key conceptual shift, and I want you to sit with this for a moment because it's genuinely important:

**Standard LLM:** The prompt goes _into_ the model. The model processes everything internally.

**Recursive LLM:** The prompt stays _outside_ the model. The model reaches out to examine it as needed.

In a standard LLM call, your entire input becomes part of the model's context window. It's all loaded into the neural network's attention mechanism at once.

In an RLM, your input is stored as a variable in an external environment — specifically, a Python programming environment (called a REPL). The model never sees the full text directly. Instead, it writes code to inspect, search, partition, and analyze the text programmatically. When it needs to understand a specific section, it sends that section — and only that section — to a sub-model for processing.

This is a profound change in how we think about the relationship between a model and its input. The input isn't something to be consumed. It's an **environment** to be explored.

## Part 3: How RLMs Actually Work

## The Architecture (No Code Required)

Let me walk you through the RLM architecture using our librarian analogy, and then we'll see what each part maps to in the actual system.

**The Library** = Your long document or prompt. It sits on the shelves (stored as a Python variable), available for inspection but not loaded into anyone's brain all at once.

**The Head Librarian** = The "root" language model. This is typically a powerful model (like GPT-5 or Claude) that orchestrates the entire operation. It decides what to look for, how to break up the work, and how to combine the findings.

**The Library Catalog System** = The Python REPL (Read-Eval-Print Loop) environment. This is where the head librarian can write code to search, slice, grep, and manipulate the text. Think of it as the card catalog and computer system that lets you find things without reading every book.

**The Assistant Librarians** = Sub-LLM calls. When the head librarian identifies a specific section that needs understanding, she dispatches an assistant to read _just that section_ and report back. These assistants are often smaller, cheaper models — they don't need to be geniuses, they just need to read a specific passage and answer a specific question about it.

## A Concrete Example

Let's make this tangible. Imagine you have a 500-page corporate report (let's say 2 million characters) and you ask: "What were the revenue figures for the Asia-Pacific region in Q3?"

**What a standard LLM does:** Load the entire 2 million characters into the context window. Hope the model can find and focus on the relevant section. Often fails because the relevant numbers are buried in the middle somewhere.

**What an RLM does:**

**Step 1 — Survey.** The root model gets told: "You have a document stored in a variable called `context`. It's 2 million characters long. Here's the query." The root model never sees the actual text yet.

**Step 2 — Strategize.** The root model writes code to explore the document. It might start by peeking at the first 1,000 characters to understand the structure, then search for section headers or keywords like "Asia-Pacific" and "Q3" and "revenue."

**Step 3 — Locate.** The code finds that the relevant section starts at character 847,000. The root model extracts, say, a 5,000-character window around that section.

**Step 4 — Delegate.** The root model sends this focused excerpt to a sub-LLM with the specific question: "Based on this text, what were the Q3 revenue figures for Asia-Pacific?"

**Step 5 — Synthesize.** The sub-LLM returns the answer. The root model might verify it by checking another section, then returns the final answer to you.

Notice what happened: no single model call ever had to process 2 million characters. The root model worked with short code snippets and metadata. The sub-model worked with a focused 5,000-character excerpt. The full document was accessible the entire time, but only the relevant pieces were ever loaded into any model's context window.

## Why "Recursive"?

The "recursive" in Recursive Language Models refers to the fact that a language model can call _other_ language models (or even itself) as part of its processing. The root model decomposes a problem, delegates sub-problems to other model calls, and those sub-calls could theoretically do the same — creating a tree of language model invocations, each handling a manageable chunk of the problem.

In practice, the current implementations mostly use a single level of recursion — the root calls sub-models, but those sub-models don't call further sub-models. The researchers found that for most current benchmarks, one level of depth is sufficient. But the framework is designed to go deeper when needed, and this is where things get exciting for future development.

Think of it like delegation in an organization. The CEO doesn't read every email. She asks department heads, who ask their teams, who examine the actual data. Each level only handles what's appropriate for its scope.

## Part 4: What Makes This Actually Work?

## The Power of Code as a Thinking Tool

One design decision in RLMs deserves special attention: the use of a Python REPL as the model's environment for interacting with context.

This isn't an arbitrary choice. Code gives the model capabilities that natural language reasoning simply can't match:

**Precise slicing.** The model can extract exactly characters 847,000 through 852,000 from a document. Try doing that with a natural language instruction.

**Pattern matching.** Regular expressions let the model search for specific patterns — dates, numbers, section headers, keywords — across millions of characters almost instantly.

**Programmatic decomposition.** The model can write a loop that processes a document chapter by chapter, or splits a CSV file into rows, or identifies all email addresses in a corpus. This kind of systematic processing is natural in code but nearly impossible through pure language.

**Adaptive strategy.** Here's the elegant part: the model decides _at inference time_ how to approach the problem. For a needle-in-a-haystack task, it might do a targeted search. For a summarization task, it might systematically process chunks. For a comparison task, it might extract relevant sections and align them. The strategy adapts to the problem.

## Why Not Just Use RAG?

If you're familiar with Retrieval-Augmented Generation (RAG), you might be wondering: isn't this just a fancy version of RAG?

There's a meaningful distinction. RAG systems use pre-built indexes (often vector embeddings) to retrieve relevant chunks before feeding them to the model. The retrieval strategy is designed by engineers ahead of time and applied uniformly.

RLMs are more flexible. The model itself decides how to explore the context, and it can use any strategy that can be expressed in code — not just similarity search. It can grep for patterns, analyze document structure, cross-reference sections, and adapt its approach based on what it discovers.

That said, the RLM authors have noted that RLMs and RAG are complementary, not competing. They can be used together, with RAG handling initial broad retrieval and RLMs doing deeper, more adaptive analysis of the retrieved content.

## Part 5: The Results — Does It Actually Work?

## The Numbers

The empirical results are compelling. When tested on challenging long-context benchmarks, RLMs showed dramatic improvements:

On long-context tasks, an RLM built on GPT-5-mini outperformed the base GPT-5 model — a smaller model with the RLM framework beat a larger model without it. On the most difficult configurations, the RLM achieved more than double the correct answers of the base model.

The framework successfully handled inputs up to **100 times beyond** the base model's context window. A model with a 128K token window could effectively process inputs of 10 million tokens or more.

Perhaps most surprisingly, the cost was often comparable or even lower than baseline approaches. On some benchmarks, the RLM was up to three times cheaper than summarization-based alternatives, because it processed only the relevant sections rather than the entire document.

A natively trained version, called RLM-Qwen3–8B (a relatively small model fine-tuned to use the RLM framework), outperformed its base model by over 28% on average across long-context tasks — and even approached the quality of vanilla GPT-5, a much larger model.

## Where RLMs Shine

The framework is particularly effective for:

**Needle-in-a-haystack tasks** — finding specific information in massive documents. This is where standard LLMs suffer most from context rot, and where the RLM's targeted search capability provides the biggest advantage.

**Long-input, long-output tasks** — situations where both the input and the expected output are very large. For example, processing a long git history and outputting the final state of a file. RLMs can iteratively construct outputs through the REPL, building them piece by piece rather than trying to generate everything in one shot.

**Structured data processing** — tasks like extracting information from large tables, processing CSV files, or analyzing structured documents where programmatic access is naturally more efficient than language-based reasoning.

**Long chat histories** — as conversations extend over many turns, the RLM framework can help models maintain coherence by treating the history as a searchable environment rather than a monolithic context.

## Part 6: The Honest Assessment — Limitations and Open Questions

No tutorial from me would be complete without an honest look at what doesn't work yet. And there's plenty to be candid about.

## Where RLMs Struggle

**Mathematical reasoning.** Current results show that RLMs underperform on math tasks by 15–25% compared to standard approaches. The researchers attribute this to models not yet being trained to effectively use the RLM scaffolding for mathematical problem-solving. Math requires tight, sequential reasoning that doesn't decompose as naturally into independent sub-problems.

**Synthetic vs. real data.** Interestingly, RLMs tend to underperform on synthetic benchmarks but excel on realistic, complex data. This suggests the approach works best when the data has natural structure that the model can exploit — chapters, sections, patterns — rather than randomly arranged information.

**Cost unpredictability.** While median costs are reasonable, RLM trajectories can be "long-tailed." Sometimes the model gets stuck in loops or performs redundant verifications, causing individual queries to become expensive. Controlling this behavior reliably is still an open challenge.

**Model dependency.** Not all models are equally good at using the RLM scaffolding. GPT-5 was notably better at it than many open-source alternatives. Some models attempted thousands of sub-calls for simple tasks, while others couldn't even use the correct function-calling format. The framework is model-agnostic in principle, but model capability matters enormously in practice.

## The Bigger Picture

RLMs represent an inference-time strategy — a way of _using_ existing models more effectively, not a new model architecture. This is both a strength and a limitation. The strength is that you can apply RLMs to any existing model without retraining. The limitation is that the model wasn't specifically trained to work this way, so it's not always efficient.

This is exactly why several research groups, including Prime Intellect, are now working on **training** models natively with RLM scaffolding, using reinforcement learning. The idea is to teach models to manage their own context end-to-end — deciding when to search, when to delegate, and when to synthesize — as a learned behavior rather than a prompted one.

If this succeeds, it could be transformative. Instead of context windows growing ever larger (with diminishing returns), models would learn to be _smart_ about context — just like that librarian who never needs to memorize the library, only navigate it expertly.

## Where This Is Heading

We're at an inflection point in how the AI field thinks about context.

For years, the approach was straightforward: make the window bigger. More tokens, more memory, more compute. RLMs represent a philosophical shift — from brute-force memorization to intelligent navigation. From "how do we make the model remember more?" to "how do we make the model _search_ better?"

This shift resonates with something deeper. Human cognition doesn't work by loading everything into working memory. We externalize knowledge — in books, databases, notes, libraries — and develop sophisticated strategies for retrieving what we need, when we need it. RLMs give language models a primitive version of this same capability.

The next milestone to watch for is RL-trained RLMs: models that have learned to manage their own context through reinforcement learning, getting better and better at deciding when and how to explore their environment. Several groups have predicted this will be a defining development of 2026.

Whether or not that specific prediction holds, the underlying insight is here to stay: the smartest approach to processing vast amounts of information isn't always to process _all_ of it. Sometimes, the wisest thing a model can do is decide what _not_ to read.

## Key Takeaways

1. **Context rot is real and fundamental.** Even models with massive context windows degrade on long inputs. Bigger windows help, but don't solve the core problem.
2. **RLMs reframe the problem.** Instead of feeding the entire input into the model, RLMs treat the input as an external environment the model can explore programmatically.
3. **The architecture is simple but powerful.** A root model orchestrates the process, writing code to inspect and partition the input, then delegating focused sub-tasks to smaller model calls.
4. **Results are impressive.** RLMs handle inputs 100x beyond model context windows, often outperforming larger models at comparable or lower cost.
5. **Limitations exist.** Math tasks, cost unpredictability, and model dependency are real challenges. This is early-stage technology with enormous potential but open questions.
6. **The future is learned context management.** The most exciting direction is training models to manage their own context via reinforcement learning — moving from a prompted inference trick to a native capability.

## Further Reading

If you want to go deeper, here's where to start:

- **The original paper:** Zhang, Kraska, and Khattab — "Recursive Language Models" (arXiv:2512.24601). The paper is well-written and surprisingly accessible.
- **The original blog post by Alex Zhang** (October 2025) — provides excellent intuition and was the initial introduction of the concept before the formal paper.
- **Context-Folding** (Sun et al., arXiv:2510.11967) — a related approach that uses reinforcement learning to train agents to manage their working context through branching and folding sub-trajectories.
- **Prime Intellect's RLM implementation** — their blog post "Recursive Language Models: the paradigm of 2026" provides practical insights from implementing and ablating the framework across multiple models.
- **The official RLM GitHub repository** — contains the inference library for running RLMs with various model providers and sandbox environments.
