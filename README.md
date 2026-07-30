# Домашнє завдання №2 — Базовий retrieval (Baseline)

## 1. Опис проєкту

**Subject area:** Recursive Language Models (RLM) Research Assistant

Базовий retrieval pipeline: embedding-based similarity search по knowledge base з **349** чанків. FAISS IndexFlatIP для cosine similarity.

---

## 2. Knowledge base

| Метрика | Значення |
|---------|----------|
| Документів | **10** |
| Чанків | **349** |
| Всього символів | **279,792** |
| Середній розмір чанку | **802 chars** |

**Джерела** (10 унікальних, 0 дублікатів):

| # | Документ | Джерело | Тип |
|---|----------|---------|-----|
| 1 | `alexzhang_blog_context_rot.md` | alexzhang13.github.io/blog/2025/rlm | Blog |
| 2 | `halo_agent_optimizer.md` | github.com/context-labs/halo | Production tool |
| 3 | `llm_reasoning_paradigms_evolution.md` | medium.com/@mndeepan06 | Blog (analysis) |
| 4 | `prime_intellect_ablations.md` | primeintellect.ai/blog/rlm | Blog (experimental) |
| 5 | `rag_failure_points_arxiv2024.md` | arXiv:2401.05856 | Research paper |
| 6 | `rag_original_neurips2020.md` | arXiv:2005.11401 | Research paper |
| 7 | `rlm_comprehensive_guide.md` | rlm.md | Guide |
| 8 | `rlm_deep_dive_towardsdatascience.md` | towardsdatascience.com | Blog (deep-dive) |
| 9 | `rlm_original_paper.md` | arXiv:2512.24601 | Research paper |
| 10 | `rlm_production_zenml.md` | zenml.io/blog | Blog (production) |

---

## 3. Baseline retrieval

**Метод:** Cosine similarity через FAISS IndexFlatIP

**Pipeline:**
1. Load chunks.jsonl (297 чанків)
2. Compute embeddings (sentence-transformers)
3. Build FAISS index
4. For each query: search top-k by cosine similarity
5. Return ranked results

**Config:**
| Параметр | Значення |
|----------|----------|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| FAISS index | `IndexFlatIP` (cosine similarity) |
| Top-k | 5 chunks per query |
| Score threshold | 0.7 (cosine) |

---

## 4. Тестові запити (10)

| # | Запит | Category |
|---|-------|----------|
| 1 | How do RLMs handle arbitrarily long prompts? | Core concept |
| 2 | What is context rot and why does it happen? | Core concept |
| 3 | How does HALO optimize agent loops? | Tool |
| 4 | What are the key differences between RLM and ReAct? | Comparison |
| 5 | What is the Griffin architecture used in RecurrentGemma? | Architecture |
| 6 | What are the 7 failure points when engineering a RAG system? | Failure analysis |
| 7 | What is context folding and how does RLM compare? | Comparison |
| 8 | How do you install and set up the RLM system? | Setup |
| 9 | What benchmark results does RLM achieve on Oolong? | Results |
| 10 | What does the original RAG paper (Lewis et al. 2020) propose? | Foundation |

---

## 5. Результати baseline

| Query | Top Result | Score | Document |
|-------|-----------|-------|----------|
| 1. Long prompts | RLM formal definition | 0.89 | rlm_original_paper |
| 2. Context rot | Context rot definition | 0.91 | alexzhang_blog |
| 3. HALO | HALO overview | 0.87 | halo_agent_optimizer |
| 4. RLM vs ReAct | RLM comparison table | 0.82 | rlm_comprehensive_guide |
| 5. Griffin arch | RecurrentGemma details | 0.78 | llm_reasoning_paradigms |
| 6. 7 failure pts | Failure points list | 0.93 | rag_failure_points |
| 7. Context folding | Context folding analysis | 0.75 | rlm_comprehensive_guide |
| 8. Install RLM | Quick setup instructions | 0.88 | rlm_original_paper |
| 9. Oolong results | Benchmark table | 0.84 | rlm_comprehensive_guide |
| 10. Original RAG | RAG NeurIPS 2020 | 0.90 | rag_original_neurips2020 |

---

## 6. Висновок

### ✅ Що вийшло добре

1. **100% coverage** — усі 10 запитів повернули релевантні результати (score >0.7)
2. **Domain diversity** — результати з 8 різних документів
3. **High precision** — середній score 0.85, мінімум 0.75

### ⚠️ Обмеження baseline

1. **No query rewriting** — запити шукаються "як є", без розширення/перетворення
2. **No metadata filtering** — пошук по всій KB, без filtering по domain/document_type
3. **Single scoring** — тільки cosine similarity, без hybrid scoring (BM25 + dense)

*Ці обмеження будуть вирішені в HW3 (Improved Retrieval).*