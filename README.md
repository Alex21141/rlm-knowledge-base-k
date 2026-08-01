# Домашнє завдання №2 — Semantic Retrieval

## 1. Опис проєкту

Semantic retrieval поверх knowledge base з HW1. Використовуємо MiniLM embeddings + FAISS index для пошуку релевантних чанків.

**Ціль:** відповісти на 10 RLM-запитів через semantic search.

---

## 2. Knowledge base

| Метрика | Значення |
|---------|----------|
| Документів | **10** |
| Чанків | **467** |
| Vectors в index | **467** |
| Embedding model | all-MiniLM-L6-v2 (384-dim) |
| FAISS index | IndexFlatIP |
| CHUNK_SIZE | 600 |
| OVERLAP | 100 |

---

## 3. Retrieval pipeline

1. **Load chunks** — read `data/processed/chunks.jsonl` (467 chunks)
2. **Build/load FAISS index** — `index/faiss.index` + `index/metadata.json`
3. **Embed query** — MiniLM → 384-dim vector
4. **Search** — FAISS inner product, top-k=5
5. **Return results** — chunk_id, score, text preview, metadata

---

## 4. Тестові запити (10)

| # | Запит | Category |
|---|-------|----------|
| 1 | How does the RLM REPL architecture process user prompts that exceed the base model's fixed context window? | Core concept |
| 2 | What is context rot in recursive language models and how does it affect performance on long-context tasks? | Core concept |
| 3 | How does the Python REPL environment function within the RLM agent architecture for recursive code execution? | Architecture |
| 4 | How does RLM recursive reasoning compare to retrieval-augmented generation? | Comparison |
| 5 | How does RLM performance scale on long-context tasks like S-NIAH compared to non-recursive base LLMs? | Benchmarks |
| 6 | What are the architectural trade-offs between RLM recursive decomposition and retrieval-augmented generation for multi-hop reasoning? | Comparison |
| 7 | How does the evolution from flat prompting to recursive execution relate to context management in language models? | Comparison |
| 8 | What are the ablation results for RLM with and without sub-calling on information-dense tasks? | Experiments |
| 9 | How does the HALO agent optimizer implement RLM-based recursive loops for tool use? | Tools |
| 10 | How does reinforcement learning fine-tuning improve RLM recursive behavior compared to supervised fine-tuning? | RL training |

---

## 5. Результати (real)

| Query | Top-1 Chunk | Score | Document |
|-------|-------------|-------|----------|
| 1. RLM REPL architecture | \`rlm_comprehensive_guide_chunk_026\` | 0.7659 | rlm_comprehensive_guide |
| 2. Context rot | \`rlm_original_paper_chunk_004\` | 0.8503 | rlm_original_paper |
| 3. Python REPL in RLM | \`rlm_rl_training_alphaxiv_chunk_005\` | 0.7492 | rlm_rl_training_alphaxiv |
| 4. RLM recursive reasoning vs RAG | \`rlm_candemir_medium_chunk_021\` | 0.6711 | rlm_candemir_medium |
| 5. S-NIAH scaling | \`llm_reasoning_paradigms_evolution_chunk_023\` | 0.7168 | llm_reasoning_paradigms_evolution |
| 6. RLM vs RAG trade-offs | \`llm_reasoning_paradigms_evolution_chunk_025\` | 0.6391 | llm_reasoning_paradigms_evolution |
| 7. Flat prompting → recursive | \`rlm_original_paper_chunk_004\` | 0.6691 | rlm_original_paper |
| 8. Ablation (sub-calling) | \`prime_intellect_ablations_chunk_057\` | 0.5685 | prime_intellect_ablations |
| 9. HALO optimizer | \`halo_agent_optimizer_chunk_001\` | 0.8091 | halo_agent_optimizer |
| 10. RL fine-tuning vs SFT | \`rlm_comprehensive_guide_chunk_018\` | 0.6229 | rlm_comprehensive_guide |

**Stats:**

| Метрика | Значення |
|---------|----------|
| Average score | 0.7062 |
| Min score | 0.5685 |
| Max score | 0.8503 |
| Queries with score > 0.60 | 9/10 |

---

## 6. Висновок

### ✅ Що вийшло добре

1. **High-quality retrieval** — середній score 0.71, 9/10 запитів >0.60
2. **RLM-документи домінують** — 6/10 результатів з RLM-фокусних документів (rlm_original_paper, rlm_comprehensive_guide, rlm_rl_training_alphaxiv, rlm_candemir_medium)
3. **Consistent scores** — діапазон [0.57, 0.85], немає outlier'ів

### ⚠️ Обмеження

1. **No evaluation metrics** — немає автоматичної оцінки релевантності (Rouge/BERTScore)
2. **Single embedding model** — MiniLM, не порівняно з іншими моделями (e.g., E5, bge)
3. **Pure semantic search** — без keyword boosting або metadata filtering (буде в HW3)

*Ці обмеження будуть частково вирішені в HW3 (Improved Retrieval) та HW4 (RAG Answer Generation).*
