# RLM vs RAG: Two Approaches to the Long-Context Problem

**Source:** https://rlm.md/blog/rlm-vs-rag-retrieval-augmented-generation.html
**Date:** February 2026
**Published by:** rlm.md (RLM community blog)

---

## Abstract

Retrieval-Augmented Generation dominated the long-context conversation for three years. RLMs take a fundamentally different path. This article provides a clear-eyed comparison of two architectures that solve the long-context problem in fundamentally different ways, with different strengths.

---

## How RAG works, and where it shines

RAG operates on a straightforward principle: instead of feeding the entire corpus to the model, retrieve only the parts that are likely relevant to the current query. A typical RAG pipeline has four stages: document ingestion (chunking and embedding), indexing (storing embeddings in a vector database), retrieval (finding the top-k most similar chunks to the query), and generation (feeding the retrieved chunks to the LLM along with the query).

This architecture excels at **factoid retrieval over large knowledge bases**. If you have ten million documents and need to answer "What was the revenue for Q3 2024?", RAG is the right tool. The question has a clear answer that lives in a specific location. The embedding model can usually find the right chunk. The LLM can generate a clear response from that chunk. The pipeline is fast, the cost is low, and the accuracy is high.

RAG also handles well the scenario where knowledge changes frequently. Because the retrieval layer is separate from the model, you can update the index without retraining. New documents get chunked, embedded, and indexed. The model immediately has access to the updated information. This is a significant operational advantage in domains like news, compliance, and customer support.

## Where RAG breaks down

The problems with RAG become apparent when tasks require more than retrieval. Three failure modes are particularly common in practice.

**The relevance gap.** RAG assumes that the most semantically similar chunks are the most relevant to the query. This assumption fails for multi-hop reasoning tasks where the answer depends on connecting information from chunks that are not individually similar to the query. A question like "Compare the indemnification clauses across all three vendor contracts" requires chunks from different documents that would not individually score highly against the query embedding. The retrieval step misses them, and the generation step cannot reason about information it never received.

**The aggregation gap.** Even when all relevant chunks are retrieved, RAG provides no mechanism for structured reasoning across those chunks. The LLM receives a bag of text snippets and must somehow synthesize them in a single forward pass. For simple tasks -- summarization, extraction, comparison of two items -- this works. For tasks requiring systematic processing of dozens of chunks with specific logical operations (counting, cross-referencing, finding contradictions), the single-pass approach degrades rapidly.

**The completeness gap.** RAG fundamentally cannot guarantee that all relevant information has been retrieved. A top-k retrieval with k=10 might miss the 11th most relevant chunk, which happens to contain a critical exception clause. Increasing k helps but increases cost and dilutes the signal. For tasks where completeness matters -- legal review, audit, compliance checking -- this is a serious limitation. You cannot certify that you have reviewed all relevant material if your retrieval pipeline makes no completeness guarantees.

## How RLMs differ

RLMs approach the same problem from a different direction. Instead of pre-selecting chunks based on similarity, the model has access to the entire corpus as an external variable and programmatically decides what to examine, in what order, and with what logic.

This difference is fundamental, not incremental. In a RAG pipeline, the retrieval step is a fixed function: embed the query, find the nearest neighbors, return the top k. The model has no control over this process and no ability to adapt it. In an RLM, the model writes its own retrieval logic. It can scan the input for structural markers, read specific sections based on what it finds, backtrack when it discovers cross-references, and systematically ensure it has examined every relevant section.

Consider the indemnification clause comparison from earlier. An RLM would approach it roughly as follows: first, scan the input to identify all three contracts and their locations within the corpus. Second, for each contract, find the indemnification section (by scanning section headers or searching for keywords). Third, extract the key terms from each section via recursive sub-calls. Fourth, compare the extracted terms and produce a structured analysis.

At no point does the model rely on embedding similarity to find the right sections. It uses structural understanding of the document to navigate directly to what it needs. This is closer to how a human lawyer would approach the task -- and it avoids the failure modes that plague RAG on this type of work.

## The completeness advantage

For tasks where completeness matters, RLMs have a structural advantage. Because the model has programmatic access to the entire input, it can implement exhaustive processing strategies. It can iterate over every section of a document, every file in a codebase, every row in a dataset. It can verify that it has processed everything by checking counts, comparing against a known structure, or simply scanning from start to end.

RAG cannot do this. By design, it selects a subset of the available information based on a heuristic (embedding similarity). For many tasks, this is perfectly fine -- you do not need to review every paragraph of a 10,000-page corpus to answer a specific factual question. But for tasks like regulatory compliance review, contract due diligence, or codebase-wide refactoring, partial coverage is not acceptable. The risk is not that the model gives a wrong answer about the information it received -- it is that it never received the information that would change the answer.

## Cost and latency trade-offs

RAG has a clear cost advantage for simple retrieval tasks. A single embedding lookup plus one LLM call is cheap and fast. An RLM that recursively processes an entire document will make multiple LLM calls, consuming more tokens and taking more time.

However, the cost comparison is more nuanced than it appears. The MIT paper found that for frontier models (GPT-5), the median cost of RLM processing is actually comparable to or lower than a single long-context call. This is because the RLM selectively examines only the parts of the input that matter, while a long-context call pays the quadratic attention cost over the entire input. The relevant comparison is not "RLM vs RAG" but "RLM vs the alternative approach you would use without RLM."

For latency-sensitive applications, RAG remains superior when the task is genuinely a retrieval task. A well-tuned RAG pipeline can return results in under a second. An RLM processing the same corpus will take longer, because it involves multiple sequential LLM calls. Parallel sub-calls help, but the recursive structure imposes some inherent serialization.

## When to use which

**Use RAG when:** The task is primarily retrieval (finding specific facts in a large corpus). The query maps cleanly to a specific document or passage. Latency is critical. The corpus changes frequently and needs to stay current without model changes. The questions are diverse and unpredictable, making pre-processing impractical.

**Use RLMs when:** The task requires reasoning across multiple sections or documents. Completeness matters (legal, compliance, audit). The task has O(n) or O(n^2) complexity (comparisons, cross-referencing, aggregation). The input has known structure that the model can navigate. A wrong answer due to missing context is worse than a slower response.

**Consider combining them:** RAG for initial candidate retrieval, RLM for deep processing of the retrieved set. This hybrid approach uses RAG's efficiency to narrow the search space and RLM's thoroughness to ensure complete processing of the relevant subset. Several production systems are already exploring this pattern, and it is likely to become a standard architecture for complex enterprise workflows.

## The bigger picture

RAG was the right solution for 2023. It addressed the most pressing limitation (context window size) with the tools available (vector databases, embedding models). It remains the right solution for a large class of tasks.

But the long-context problem has multiple facets, and retrieval-based approaches address only one of them. RLMs address a different facet: the ability to reason deeply and completely over large inputs. As both technologies mature, practitioners will need to understand the strengths and limitations of each to make informed architectural decisions. The answer to "should I use RAG or RLMs?" is increasingly "it depends on the task" -- which is the right answer for any mature engineering discipline.

### References

1. Zhang, A., Kraska, T., & Khattab, O. (2025). Recursive Language Models. arXiv:2512.24601. MIT OASYS Lab.
2. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020.
3. Gao, Y., et al. (2024). Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv:2312.10997.
4. Barnett, S., et al. (2024). Seven Failure Points When Engineering a Retrieval Augmented Generation System. arXiv:2401.05856.
5. Shi, W., et al. (2023). Large Language Models Can Be Easily Distracted by Irrelevant Context. ICML 2023.
6. Xu, F., et al. (2024). Retrieval Meets Long Context Language Models. NAACL 2024.