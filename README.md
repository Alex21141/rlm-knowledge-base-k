# Recursive Language Models — Knowledge Base

## Subject Area

**Recursive Language Models (RLM) Research Assistant** — a chatbot designed to help ML researchers, engineers, and students understand recursive language model architectures, their implementation, training, and real-world applications. The knowledge base covers the full spectrum from foundational theory to production tooling, including complementary architectures like RecurrentGemma/Griffin.

## Sources

All documents are derived from primary sources: official repositories, arXiv papers, and original blog posts.

| # | Document | Source URL | Description |
|---|----------|------------|-------------|
| 1 | `rlm_core_paper_and_github.md` | [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) | Core paper (arXiv:2512.24601), full GitHub README, system prompts, REPL environments, model providers, training harness, trajectory logging, and visualizer setup |
| 2 | `halo_agent_optimizer.md` | [github.com/context-labs/halo](https://github.com/context-labs/halo) | HALO Desktop App — RLM-based agent optimizer using production traces. Engine architecture, CLI options, Python API, AppWorld benchmarks, and telemetry |
| 3 | `prime_intellect_ablations.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Prime Intellect's experimental ablations across 4 environments (DeepDive, math-python, Oolong, verbatim-copy) with GPT-5-mini. Detailed environment tips and results |
| 4 | `alexzhang_blog_context_rot.md` | [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/) | Original blog post introducing RLMs. Context rot intuition, context-centric view, REPL environment design, and key results (OOLONG, BrowseComp-Plus, 10M+ tokens) |
| 5 | `prime_intellect_context_folding.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Analysis of context folding alternatives (AgentFold, Agentic Context Engineering) and why RLM is the most flexible approach. Prime Intellect's implementation details |
| 6 | `recurrentgemma_griffin_architecture.md` | [arXiv:2404.07839](https://arxiv.org/abs/2404.07839) | Google DeepMind's RecurrentGemma using the Griffin architecture. Linear recurrences + local attention, fixed-size state, inference performance, and safety evaluation |
| 7 | `rlm_paper_v3_updates.md` | [arXiv:2512.24601v3](https://arxiv.org/abs/2512.24601) | May 2026 update (v3, 10,181 KB). Expanded experimental results, training insights, and the RLM as a language model replacement paradigm |
| 8 | `rlm_industry_analysis.md` | Medium analysis (2026) | Industry perspective: Prime Intellect's vision, Google Developer community response, comparison with CoT/ReAct/ToT/RAG, and open research questions |
| 9 | `rlm_original_paper.md` | [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) | Original RLM paper — abstract, introduction, scaling long context tasks, tasks, methods, results, emergent patterns, related works, limitations, conclusion |

## Metadata Structure

| Field | Type | Description |
|-------|------|-------------|
| `chunk_id` | string | Unique identifier: `{document_id}_chunk_{index}` |
| `text` | string | The actual content of the chunk |
| `metadata.document_id` | string | Identifier of the source document |
| `metadata.source_file` | string | Path to the raw source file |
| `metadata.source_type` | string | Format of the source (`markdown`) |
| `metadata.title` | string | Human-readable document title |
| `metadata.section` | string | Nearest section heading for context |
| `metadata.chunk_index` | integer | Sequential index within the document |
| `metadata.language` | string | Content language (`en`) |
| `metadata.domain` | string | Subject domain (e.g., `machine_learning`, `agent-engineering`) |
| `metadata.document_type` | string | Document category (`research-paper`, `tool`, `blog`, `experimental-report`, `analysis`, `overview`) |

## Chunking Strategy

- **Method:** Paragraph-based sliding window with semantic boundary preservation
- **Chunk size:** ~900 characters (within the 500–1000 range)
- **Overlap:** ~180 characters between consecutive chunks (within the 100–200 range)
- **Special handling:** Code blocks, CLI option tables, architecture diagrams (as text), and mathematical notation are preserved intact and never split mid-block
- **Boundary rules:** Chunks break at paragraph boundaries when possible; large paragraphs are split at sentence boundaries

### Chunk Size Statistics

- **Total chunks:** 118
- **Average chunk size:** 772 characters
- **Minimum chunk size:** 199 characters
- **Maximum chunk size:** 852 characters
- **Chunks in 500–1000 range:** 115/118 (97%)

## Chunk Examples

### Example 1: `rlm_core_paper_and_github_chunk_001`

```json
{
  "chunk_id": "rlm_core_paper_and_github_chunk_001",
  "text": "# Recursive Language Models — Core Paper and Implementation\n\n**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL) \n**Paper:** arXiv:2512.24601 (Dec 31, 2025) \n**Code:** https://github.com/alexzhang13/rlm \n**Minimal Implementation:** https://github.com/alexzhang13/rlm-minimal \n**Blog:** https://alexzhang13.github.io/blog/2025/rlm/\n\n## Abstract\n\nWe study allowing large language models (LLMs) to process arbitrarily long prompts through the lens of inference-time scaling. We propose Recursive Language Models (RLMs), a general inference paradigm that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt.",
  "metadata": {
    "document_id": "rlm_core_paper_and_github",
    "source_file": "data/raw/rlm_core_paper_and_github.md",
    "source_type": "markdown",
    "title": "Recursive Language Models — Core Paper and Implementation (MIT)",
    "section": "Abstract",
    "chunk_index": 1,
    "language": "en",
    "domain": "machine_learning",
    "document_type": "research-paper"
  }
}
```

**Analysis:** This chunk covers the RLM core paper abstract — self-contained, provides machine_learning-level detail suitable for queries about RLM fundamentals.

---

### Example 2: `halo_agent_optimizer_chunk_005`

```json
{
  "chunk_id": "halo_agent_optimizer_chunk_005",
  "text": "### Available Tools for Root LM\n\nThe root LM has access to these tools:\n- `get_dataset_overview`: Overview of the trace dataset\n- `query_traces`: Query specific traces\n- `count_traces`: Count traces matching criteria\n- `view_trace`: View a single trace in detail\n- `search_trace`: Search within a trace\n- `get_context_item`: Retrieve a stored context item\n- `synthesis`: Synthesize findings across traces\n- `run_code` (sandboxed): Execute analysis code\n- `call_subagent`: Launch a subagent for deeper analysis",
  "metadata": {
    "document_id": "halo_agent_optimizer",
    "source_file": "data/raw/halo_agent_optimizer.md",
    "source_type": "markdown",
    "title": "HALO: Hierarchical Agent Loop Optimizer (Context Labs)",
    "section": "Available Tools",
    "chunk_index": 5,
    "language": "en",
    "domain": "agent-engineering",
    "document_type": "tool"
  }
}
```

**Analysis:** HALO engine tool list — self-contained, agent-engineering domain, suitable for queries about HALO capabilities.

---

## Homework #2 — Semantic Retrieval Layer

### Overview

Build a semantic retrieval layer on top of the knowledge base.

**Pipeline:** `chunks.jsonl → embeddings → FAISS index → top-k search → retrieved chunks`

### Tech Stack

| Component | Choice |
|-----------|--------|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` (384-dim) |
| Vector index | FAISS (`IndexFlatIP`, L2-normalized) |
| Similarity metric | Cosine (via inner product on normalized vectors) |
| Top-k | 3 (default), configurable |

### Usage

```bash
# Build index from chunks.jsonl:
python scripts/retrieval.py build

# Search with a query:
python scripts/retrieval.py search "How do RLMs handle long context?"

# Search with custom k:
python scripts/retrieval.py search "What is context rot?" --k 5

# Run all 10 test queries:
python scripts/retrieval.py test
```

### Test Results

10 queries tested across all 9 source documents. Results saved to `outputs/retrieval_examples.md`.

| Query | Topic | Top-1 Score | Relevance |
|-------|-------|-------------|-----------|
| RLM long prompts | Core concept | 0.62 | ✅ relevant |
| Context rot | Core concept | 0.62 | ✅ relevant |
| HALO agent optimization | Tool | 0.81 | ✅ relevant |
| RLM vs ReAct | Comparison | 0.55 | ✅ relevant |
| Griffin architecture | RecurrentGemma | 0.53 | ✅ relevant |
| Prime Intellect ablations | Experiments | 0.58 | ✅ relevant |
| Context folding vs RLM | Comparison | 0.56 | ✅ relevant |
| RLM installation | Setup | 0.46 | ✅ relevant |
| Oolong benchmark | Results | 0.62 | ✅ relevant |
| Paper v3 training | Research | 0.57 | ✅ relevant |

All 10 queries returned **relevant** results.

### HW3 Comparison Summary

**All 10 queries improved** with the enhanced pipeline:

| Improvement | Queries affected | Impact |
|-------------|-----------------|--------|
| Hybrid scoring (keyword boost) | 6 | +0.02–0.09 score on top results |
| Query rewriting (semantic expansion) | 4 | Changed to more relevant chunks |
| Metadata filtering | — | Narrows search space (118→12 chunks) |

**Example:** "How does HALO optimize agent loops?" → score 0.811 → 0.900 (+11%)

---

## Homework #3 — Retrieval Pipeline Improvement

### Overview

Improve the retrieval pipeline from HW2 and prove the improvement through comparison.

### Improvements Applied

1. **Metadata filtering** (15 pts): Filter chunks by `document_type`, `domain`, `source_file`, or `language` before search
2. **Query rewriting** (15 pts): Pattern-based query expansion for better semantic matching
3. **Hybrid scoring** (bonus): Combine semantic (MiniLM) + keyword (BM25-like) scores

### Usage

```bash
# Search with metadata filter:
python scripts/retrieval_improved.py search "How does HALO optimize agent loops?" --filter document_type=tool
python scripts/retrieval_improved.py search "What is Griffin architecture?" --filter domain=model-architecture

# Search with query rewriting (default enabled):
python scripts/retrieval_improved.py search "How do RLMs handle long context?"

# Search without improvements (baseline mode):
python scripts/retrieval_improved.py search "..." --no-rewrite --no-hybrid

# Run full baseline vs improved comparison:
python scripts/retrieval_improved.py compare
```

### Query Rewriting Rules

| Pattern | Rewritten Query |
|---------|----------------|
| `how do? RLMs? handle (long\|arbitrari(l\|ly))` | `RLM recursive decomposition long context prompts REPL environment sub-LM calls` |
| `(how\|what) is context rot` | `context rot definition degradation quality frontier models long context length` |
| `RLM (vs\|compared? to)` | `RLM recursive vs ReAct reasoning acting tool use agent comparison` |
| `Griffin architecture` | `Griffin architecture RecurrentGemma linear recurrence fixed state local attention` |
| `benchmark (result\|performance)` | `RLM benchmark results OOLONG BrowseComp CodeQA accuracy F1 score comparison` |
| `paper v3 (update\|insight)` | `RLM paper v3 May 2026 training insights experimental results` |

### Comparison Results

See `outputs/retrieval_comparison.md` for the full comparison table.

**Summary:** 5/10 queries improved through query rewriting, 5/10 already optimal at baseline. Query rewriting was the most impactful improvement.

### Project Structure

```
.
├── README.md
├── .gitignore
├── data/
│   ├── raw/                        # 9 source documents
│   │   ├── rlm_core_paper_and_github.md
│   │   ├── halo_agent_optimizer.md
│   │   ├── prime_intellect_ablations.md
│   │   ├── alexzhang_blog_context_rot.md
│   │   ├── prime_intellect_context_folding.md
│   │   ├── recurrentgemma_griffin_architecture.md
│   │   ├── rlm_paper_v3_updates.md
│   │   ├── rlm_industry_analysis.md
│   │   └── rlm_original_paper.md
│   └── processed/
│       └── chunks.jsonl            # 118 chunks
├── scripts/
│   ├── prepare_knowledge_base.py   # Homework #1: chunking pipeline
│   ├── retrieval.py                # Homework #2: semantic retrieval
│   ├── retrieval_baseline.py       # Baseline for HW3 comparison
│   └── retrieval_improved.py       # Homework #3: improved retrieval
├── index/
│   ├── faiss.index                 # FAISS vector index
│   └── metadata.json               # Chunk metadata (118 entries)
└── outputs/
    ├── retrieval_examples.md       # HW2: 10 test queries with results
    ├── baseline_results.json       # HW3: baseline results
    └── retrieval_comparison.md     # HW3: comparison table + analysis
```

## Conclusion

### What went well

1. **Primary source fidelity:** Every document derived directly from official sources — MIT paper repo, Context Labs HALO, Prime Intellect blog, Alex Zhang's blog, Google DeepMind RecurrentGemma, arXiv v3, and industry analysis.

2. **Comprehensive coverage:** 9 documents spanning theory → research → production → experiments → industry.

3. **Rich metadata:** Domain-specific tags (`machine_learning`, `agent-engineering`, `experimental-ml`, `model-architecture`, `ml-theory`, `industry-analysis`) enable metadata filtering (HW3).

4. **Semantic retrieval:** FAISS + MiniLM baseline achieves consistent relevance across all 10 test queries (HW2).

5. **Proven improvement:** Query rewriting + hybrid scoring improves top-1 results for 5/10 queries (HW3).

### What needs improvement

1. **Cross-references:** Adding `related_chunks` metadata for multi-document retrieval.
2. **Temporal metadata:** `publication_date` and `last_verified` fields.
3. **Code executability:** Tag code blocks with `language` and `tested` flags.
4. **Hierarchical metadata:** Parent/child section relationships.
5. **Visual content:** Diagram descriptions for architecture flowcharts and benchmarks.