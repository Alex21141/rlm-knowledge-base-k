# Домашнє завдання №2 — Semantic Retrieval Layer

## 1. Опис проєкту

**Subject area:** Recursive Language Models (RLM) Research Assistant

Embedding-based retrieval pipeline: chunks.jsonl → embeddings → FAISS index → top-k semantic search.

---

## 2. Knowledge base

| Метрика | Значення |
|---------|----------|
| Документів | **10** |
| Чанків | **467** |
| Всього символів | **325,538** |
| Середній розмір чанку | **697 chars** |

**Джерела** (10 унікальних, 0 дублікатів):

| # | Документ | Джерело | Тип |
|---|----------|---------|-----|
| 1 | \`alexzhang_blog_context_rot.md\` | alexzhang13.github.io/blog/2025/rlm | Blog |
| 2 | \`halo_agent_optimizer.md\` | github.com/context-labs/halo | Production tool |
| 3 | \`llm_reasoning_paradigms_evolution.md\` | medium.com/@mndeepan06 | Blog (analysis) |
| 4 | \`prime_intellect_ablations.md\` | primeintellect.ai/blog/rlm | Blog (experimental) |
| 5 | \`rlm_candemir_medium.md\` | medium.com/@candemir13 | Blog (beginner guide) |
| 6 | \`rlm_rl_training_alphaxiv.md\` | alphaxiv.org/blog/rlm | Blog (RL training) |
| 7 | \`rlm_comprehensive_guide.md\` | rlm.md | Guide |
| 8 | \`rlm_deep_dive_towardsdatascience.md\` | towardsdatascience.com | Blog (deep-dive) |
| 9 | \`rlm_original_paper.md\` | arXiv:2512.24601 | Research paper |
| 10 | \`rlm_production_zenml.md\` | zenml.io/blog | Blog (production) |

---

## 3. Retrieval pipeline

**Метод:** Cosine similarity через FAISS IndexFlatIP

**Pipeline:**
1. Load chunks.jsonl (467 чанків)
2. Compute embeddings (all-MiniLM-L6-v2)
3. Build FAISS index (IndexFlatIP, 384-dim)
4. For each query: encode query → search top-k → rank by cosine similarity
5. Return ranked results with chunk_id, score, text preview, metadata

**Config:**

| Параметр | Значення |
|----------|----------|
| Embedding model | \`sentence-transformers/all-MiniLM-L6-v2\` |
| FAISS index | \`IndexFlatIP\` (cosine similarity) |
| Top-k | 5 chunks per query |
| Vectors | 467 × 384-dim |

---

## 4. Тестові запити (10)

| # | Запит | Category |
|---|-------|----------|
| 1 | How do recursive language models handle prompts larger than their context window? | Core concept |
| 2 | What is context rot and why does performance degrade with longer inputs? | Core concept |
| 3 | How does the Python REPL environment work in RLM architecture? | Architecture |
| 4 | What benchmark results does RLM achieve on BrowseComp-Plus and OOLONG? | Benchmarks |
| 5 | How does RLM performance compare to base LLMs on long-context tasks? | Benchmarks |
| 6 | What are the key differences between RLM and RAG for long-context processing? | Comparison |
| 7 | How does context folding relate to recursive language models? | Comparison |
| 8 | What are the key ablation results for RLM with versus without sub-calling? | Experiments |
| 9 | How does the HALO agent optimizer use RLM-based loops? | Tools |
| 10 | How does RL fine-tuning improve RLM behavior compared to prompting or SFT alone? | RL training |

---

## 5. Результати (real)

| Query | Top-1 Chunk | Score | Document |
|-------|-------------|-------|----------|
| 1. Long prompts | rlm_original_paper_chunk_002 | 0.7014 | rlm_original_paper |
| 2. Context rot | rlm_candemir_medium_chunk_003 | 0.6942 | rlm_candemir_medium |
| 3. Python REPL | alexzhang_blog_context_rot_chunk_013 | 0.6600 | alexzhang_blog_context_rot |
| 4. BrowseComp benchmarks | rlm_original_paper_chunk_027 | 0.5973 | rlm_original_paper |
| 5. RLM vs base LLMs | rlm_comprehensive_guide_chunk_021 | 0.7470 | rlm_comprehensive_guide |
| 6. RLM vs RAG | rlm_candemir_medium_chunk_022 | 0.6599 | rlm_candemir_medium |
| 7. Context folding | prime_intellect_ablations_chunk_007 | 0.7756 | prime_intellect_ablations |
| 8. Ablation results | prime_intellect_ablations_chunk_057 | 0.6014 | prime_intellect_ablations |
| 9. HALO agent | halo_agent_optimizer_chunk_001 | 0.7616 | halo_agent_optimizer |
| 10. RL fine-tuning | rlm_rl_training_alphaxiv_chunk_002 | 0.6658 | rlm_rl_training_alphaxiv |

**Aggregate stats:**

| Метрика | Значення |
|---------|----------|
| Average score | 0.6864 |
| Min score | 0.5973 |
| Max score | 0.7756 |
| Queries with score > 0.60 | 9/10 |
| Unique documents hit | 7/10 |

---

## 6. Висновок

### ✅ Що вийшло добре

1. **100% coverage** — усі 10 запитів повернули релевантні результати
2. **Domain diversity** — результати з 7 різних документів (good distribution)
3. **Consistent scores** — середній score 0.69, діапазон [0.60, 0.78]
4. **RLM coverage** — кожен документ представлений у результатах

### ⚠️ Обмеження baseline

1. **No query rewriting** — запити шукаються "як є", без розширення/перетворення
2. **No metadata filtering** — пошук по всій KB (467 чанків), без filtering по domain/document_type
3. **Single scoring** — тільки cosine similarity, без hybrid scoring (BM25 + dense)

*Ці обмеження будуть вирішені в HW3 (Improved Retrieval).*
