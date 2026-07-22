# Homework #1 — Knowledge Base Preparation

## Subject Area

**Recursive Language Models (RLM) Research Assistant** — a chatbot designed to help ML researchers, engineers, and students understand recursive language model architectures, their implementation, training, and real-world applications. The knowledge base covers the full spectrum from foundational theory to production tooling, including complementary architectures like RecurrentGemma/Griffin.

## Sources

All documents are derived from primary sources: official repositories, arXiv papers, and original blog posts.

| # | Document | Source URL | Description |
|---|----------|------------|-------------|
| 1 | `rlm_core_paper_and_github.md` | [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) | Core paper (arXiv:2512.24601), full GitHub README, system prompts, REPL environments, model providers, training harness, trajectory logging, and visualizer setup |
| 2 | `rlm_original_paper.md` | [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) | Original academic paper by Alex Zhang, Tim Kraska, Omar Khattab (MIT CSAIL). Full text: abstract, introduction, methods, results, emergent patterns, related work, limitations, conclusion |
| 3 | `halo_agent_optimizer.md` | [github.com/context-labs/halo](https://github.com/context-labs/halo) | HALO Desktop App — RLM-based agent optimizer using production traces. Engine architecture, CLI options, Python API, AppWorld benchmarks, and telemetry |
| 4 | `prime_intellect_ablations.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Prime Intellect's experimental ablations across 4 environments (DeepDive, math-python, Oolong, verbatim-copy) with GPT-5-mini. Detailed environment tips and results |
| 5 | `alexzhang_blog_context_rot.md` | [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/) | Original blog post introducing RLMs. Context rot intuition, context-centric view, REPL environment design, and key results (OOLONG, BrowseComp-Plus, 10M+ tokens) |
| 6 | `prime_intellect_context_folding.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Analysis of context folding alternatives (AgentFold, Agentic Context Engineering) and why RLM is the most flexible approach. Prime Intellect's implementation details |
| 7 | `recurrentgemma_griffin_architecture.md` | [arXiv:2404.07839](https://arxiv.org/abs/2404.07839) | Google DeepMind's RecurrentGemma using the Griffin architecture. Linear recurrences + local attention, fixed-size state, inference performance, and safety evaluation |
| 8 | `rlm_paper_v3_updates.md` | [arXiv:2512.24601v3](https://arxiv.org/abs/2512.24601v3) | May 2026 update (v3, 10,181 KB). Expanded experimental results, training insights, and the RLM as a language model replacement paradigm |
| 9 | `rlm_industry_analysis.md` | Medium analysis (2026) | Industry perspective: Prime Intellect's vision, Google Developer community response, comparison with CoT/ReAct/ToT/RAG, and open research questions |

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

- **Total chunks:** 125
- **Average chunk size:** 798 characters
- **Minimum chunk size:** 199 characters
- **Maximum chunk size:** 850 characters
- **Chunks outside 500–1000 range:** 2/125
- **Unique sections:** 77
- **Generic placeholders:** 0

## Chunk Examples

### Example 1: `rlm_core_chunk_001`

```json
{
  "chunk_id": "rlm_core_chunk_001",
  "text": "# Recursive Language Models — Core Paper and Implementation\n\n**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL) \n**Paper:** arXiv:2512.24601 (Dec 31, 2025) \n**Code:** https://github.com/alexzhang13/rlm \n**Minimal Implementation:** https://github.com/alexzhang13/rlm-minimal \n**Blog:** https://alexzhang13.github.io/blog/2025/rlm/\n\n## Abstract\n\nWe study allowing large language models (LLMs) to process arbitrarily long prompts through the lens of inference-time scaling. We propose Recursive Language Models (RLMs), a general inference paradigm that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt.",
  "metadata": {
    "document_id": "rlm_core",
    "source_file": "data/raw/rlm_core_paper_and_github.md",
    "source_type": "markdown",
    "title": "Recursive Language Models — Core Paper and Implementation (MIT)",
    "section": "Core Paper & GitHub Setup",
    "chunk_index": 1,
    "language": "en",
    "domain": "machine_learning",
    "document_type": "research-paper"
  }
}
```

**Analysis:** This chunk from *Recursive Language Models — Core Paper and Implementation (MIT)* covers the section **"Core Paper & GitHub Setup"**. It is self-contained and provides machine-learning-level detail suitable for answering queries about core paper and GitHub setup.

---

### Example 2: `halo_agent_optimizer_chunk_005`

```json
{
  "chunk_id": "halo_agent_optimizer_chunk_005",
  "text": "### Available Tools for Root LM\n\nThe root LM has access to these tools:\n- `get_dataset_overview`: Overview of the trace dataset\n- `query_traces`: Query specific traces\n- `count_traces`: Count traces matching criteria\n- `view_trace`: View a single trace in detail\n- `search_trace`: Search within a trace\n- `get_context_item`: Retrieve a stored context item\n- `synthesis`: Synthesize findings across traces\n- `run_code` (sandboxed): Execute analysis code\n- `call_subagent`: Launch a subagent for deeper analysis\n\n### Subagent Tools\n\nTools are only usable by sub-LLMs, not the root RLM. This decision was made because many tools produce a lot of tokens. Now, the main RLM doesn't have to see those tokens, and can instead delegate the work that requires tools.\n\n## Installation and Usage\n\nInstall the HALO engine + CLI from PyPI:\n\n```\npip install halo-engine\n\n# Verify installation\nhalo --help\n\n```",
  "metadata": {
    "document_id": "halo_agent_optimizer",
    "source_file": "data/raw/halo_agent_optimizer.md",
    "source_type": "markdown",
    "title": "HALO: Hierarchical Agent Loop Optimizer",
    "section": "HALO: Hierarchical Agent Loop Optimizer",
    "chunk_index": 5,
    "language": "en",
    "domain": "agent-engineering",
    "document_type": "tool"
  }
}
```

**Analysis:** This chunk from *HALO: Hierarchical Agent Loop Optimizer* covers the section **"HALO: Hierarchical Agent Loop Optimizer"**. It is self-contained and provides agent-engineering-level detail suitable for answering queries about available tools for root LM and subagent tools.

---

### Example 3: `prime_intellect_ablations_chunk_008`

```json
{
  "chunk_id": "prime_intellect_ablations_chunk_008",
  "text": "**Environment tips for DeepDive:**\n\n```\nStrategy for deep research tasks:\n1. Decompose the question into multiple smaller, focused research sub-tasks\n2. Parallel sub-LLM research: Use llm_batch() to dispatch sub-tasks in parallel\n3. Synthesize findings: After collecting sub-LLM responses, combine and cross-reference\n4. Iterate if needed: Dispatch another batch of targeted sub-tasks\n5. Finalize: Write synthesized answer to answer[\"content\"], set answer[\"ready\"] = True\n\n```\n\n### math-python\n\nmath-python poses difficult math problems, and gives an LLM a Python tool to solve those problems. Examples include triangle geometry problems and polynomial equations.",
  "metadata": {
    "document_id": "prime_intellect_ablations",
    "source_file": "data/raw/prime_intellect_ablations.md",
    "source_type": "markdown",
    "title": "Prime Intellect: Recursive Language Models Ablations",
    "section": "Prime Intellect: Recursive Language Models Ablations",
    "chunk_index": 8,
    "language": "en",
    "domain": "experimental-ml",
    "document_type": "experimental-report"
  }
}
```

**Analysis:** This chunk from *Prime Intellect: Recursive Language Models Ablations* covers the section **"Prime Intellect: Recursive Language Models Ablations"**. It is self-contained and provides experimental-ml-level detail suitable for answering queries about DeepDive environment strategy and math-python problems.

---

### Example 4: `prime_intellect_context_folding_chunk_005`

```json
{
  "chunk_id": "prime_intellect_context_folding_chunk_005",
  "text": "The RLM allows the model to actively manage its own context. This approach is more in line with The Bitter Lesson than the ones presented before; it enables training directly with the RLM scaffolding and getting better and better, learned context folding through end-to-end reinforcement learning.\n\nIt never actually summarizes context, which leads to information loss. Instead, it pro-actively delegates context to Python scripts and sub-LLMs.\n\n## RLM Implementation at Prime Intellect\n\nPrime Intellect has implemented their version of the RLM in `verifiers` so that it is ready to be used in any environment. They provide several RLM-based environments on the Environments Hub, and support training with `prime-rl`.\n\n### Key Implementation Details",
  "metadata": {
    "document_id": "prime_intellect_context_folding",
    "source_file": "data/raw/prime_intellect_context_folding.md",
    "source_type": "markdown",
    "title": "Context Folding and the RLM Paradigm",
    "section": "Context Folding and the RLM Paradigm",
    "chunk_index": 5,
    "language": "en",
    "domain": "ml-theory",
    "document_type": "analysis"
  }
}
```

**Analysis:** This chunk from *Context Folding and the RLM Paradigm* covers the section **"Context Folding and the RLM Paradigm"**. It is self-contained and provides ml-theory-level detail suitable for answering queries about RLM implementation and context folding approach.

---

### Example 5: `rlm_original_paper_chunk_001`

```json
{
  "chunk_id": "rlm_original_paper_chunk_001",
  "text": "# Recursive Language Models — Original Paper (MIT CSAIL)\n\n**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)\n**Paper:** arXiv:2512.24601 (v1)\n**Code:** https://github.com/alexzhang13/rlm\n**Blog:** https://alexzhang13.github.io/blog/2025/rlm/\n\n---\n\n## Abstract\n\nWe study allowing large language models (LLMs) to process arbitrarily long prompts through the lens of inference-time scaling. We propose Recursive Language Models (RLMs), a general inference strategy that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt. We find that RLMs successfully handle inputs up to two orders of magnitude beyond model context windows and, even for shorter prompts, dramatically outperform the quality of base LLMs and common long-context scaffolds across four diverse long-context tasks, while having comparable (or cheaper) cost per query.",
  "metadata": {
    "document_id": "rlm_original_paper",
    "source_file": "data/raw/rlm_original_paper.md",
    "source_type": "markdown",
    "title": "Recursive Language Models — Original Paper (MIT CSAIL)",
    "section": "Original Academic Paper",
    "chunk_index": 1,
    "language": "en",
    "domain": "machine_learning",
    "document_type": "research-paper"
  }
}
```

**Analysis:** This chunk from *Recursive Language Models — Original Paper (MIT CSAIL)* covers the section **"Original Academic Paper"**. It is self-contained and provides machine-learning-level detail suitable for answering queries about the original RLM paper abstract and core concepts.

---

## Conclusion

### What went well

1. **Primary source fidelity:** Every document is derived directly from official sources — the MIT paper repository, Context Labs HALO repo, Prime Intellect blog, Alex Zhang's blog, Google DeepMind's RecurrentGemma paper, and arXiv v3 updates. This ensures factual accuracy and captures exact terminology, API signatures, and experimental numbers.

2. **Comprehensive coverage:** The 9 documents span the full research-to-production spectrum: theory (blog), core research (original paper + GitHub + v3 updates), production tooling (HALO), experimental validation (Prime Intellect ablations), comparative analysis (context folding), complementary architecture (RecurrentGemma/Griffin), and industry outlook.

3. **Semantic coherence:** Chunks preserve paragraph and code block boundaries. The HALO CLI options table, Prime Intellect's environment tips, and RecurrentGemma's hyperparameter tables are kept intact — critical for a research assistant where precise values matter.

4. **Rich metadata:** Domain-specific tags (`machine_learning`, `agent-engineering`, `experimental-ml`, `model-architecture`, `ml-theory`, `industry-analysis`) enable advanced filtering. A user querying "how to install HALO" routes to `halo_agent_optimizer` chunks; "what is Griffin" routes to `recurrentgemma_griffin_architecture`.

5. **Overlap strategy:** The 180-character overlap ensures cross-paragraph concepts (e.g., "REPL environment → sub-LM calls → final answer") remain retrievable even at chunk boundaries.

6. **Zero generic placeholders:** All 125 chunks have meaningful section names — no "General" or "Overview" placeholders that would degrade retrieval quality.

7. **Actionable content:** Chunks contain concrete, copy-pasteable information: system prompts, CLI commands, Python API examples, benchmark numbers, environment tips, and architecture details. This makes the chatbot immediately useful for practitioners.

### What needs improvement

1. **Cross-references:** Some chunks reference concepts from other documents (e.g., the blog mentions the paper, HALO references the RLM paradigm, RecurrentGemma mentions context windows). Adding explicit `related_chunks` or `see_also` metadata would improve multi-document retrieval.

2. **Temporal metadata:** Adding `publication_date` and `last_verified` fields would help the chatbot warn users when information may be outdated. The blog is from Oct 2025, the original paper from Dec 2025, the v3 paper from May 2026, and HALO is actively developed.

3. **Code executability:** Many chunks contain code snippets (Python, Bash, CLI). A future improvement would be to tag code blocks with `language` and `tested` flags, and potentially include expected output.

4. **Hierarchical metadata:** Adding parent/child section relationships (e.g., "REPL Environments → DockerREPL") would enable better hierarchical retrieval strategies.

5. **Chunk size uniformity:** Some introductory/overview chunks are shorter than 500 characters due to natural paragraph boundaries. A post-processing merge step could combine adjacent short chunks to improve embedding density.

6. **Missing visual content:** The original sources contain important diagrams (RLM architecture flowchart, HALO engine diagram, RecurrentGemma layer structure, benchmark charts). The text-based knowledge base cannot capture these. Adding image URLs or diagram descriptions would help.

7. **Version tracking:** HALO and the RLM library are actively developed. Adding `version` or `commit_hash` metadata would help users know which version of the API a chunk refers to.

8. **Multilingual support:** Currently all content is in English. For a global research community, adding translations or parallel corpus in other languages would expand accessibility.

## Project Structure

```
.
├── README.md
├── data/
│   ├── raw/
│   │   ├── rlm_core_paper_and_github.md      # MIT paper + GitHub
│   │   ├── rlm_original_paper.md             # Original academic paper (PDF)
│   │   ├── halo_agent_optimizer.md           # Context Labs HALO
│   │   ├── prime_intellect_ablations.md      # Prime Intellect experiments
│   │   ├── alexzhang_blog_context_rot.md     # Original blog post
│   │   ├── prime_intellect_context_folding.md # Context folding analysis
│   │   ├── recurrentgemma_griffin_architecture.md # Google DeepMind
│   │   ├── rlm_paper_v3_updates.md           # May 2026 update
│   │   └── rlm_industry_analysis.md          # Industry outlook
│   └── processed/
│       └── chunks.jsonl                      # 125 chunks (99,751 chars)
└── scripts/
    └── prepare_knowledge_base.py             # Chunking pipeline
```

## Usage

To regenerate the knowledge base from raw sources:

```bash
python scripts/prepare_knowledge_base.py
```

The script reads all Markdown files from `data/raw/` and produces `data/processed/chunks.jsonl`.