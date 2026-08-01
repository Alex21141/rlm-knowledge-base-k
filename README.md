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

### 📊 Детальний аналіз за запитами

| # | Запит | Score | Документ | Вердикт | Коментар |
|---|-------|-------|----------|---------|----------|
| 1 | RLM REPL architecture | 0.7659 | rlm_comprehensive_guide | ✅ Влучив | Top-1 чанк містить ключову інформацію про REPL-архітектуру |
| 2 | Context rot | 0.8503 | rlm_original_paper | ✅ Влучив | Найвищий score — семантичний match з оригінальною працею |
| 3 | Python REPL in RLM | 0.7492 | rlm_rl_training_alphaxiv | ✅ Влучив | Коректно знайшов секцію про REPL-environment для code execution |
| 4 | RLM vs RAG comparison | 0.6711 | rlm_candemir_medium | ✅ Влучив | Порівняльний запит — знайшов чанк про RLM vs RAG відмінність |
| 5 | S-NIAH scaling | 0.7168 | llm_reasoning_paradigms_evolution | ✅ Влучив | Знайшов long-context benchmark results, хоча й не в RLM-фокусному документі |
| 6 | RLM vs RAG trade-offs | 0.6391 | llm_reasoning_paradigms_evolution | ⚠️ Пограничний | Score <0.65 — semantична близькість зменшується для порівняльних запитів |
| 7 | Flat prompting → recursive | 0.6691 | rlm_original_paper | ✅ Влучив | Коректно, але score на межі — концептуальний запит |
| 8 | Ablation (sub-calling) | 0.5685 | prime_intellect_ablations | ❌ Низький | Найнижчий score — специфічний запит на ablation results |
| 9 | HALO optimizer | 0.8091 | halo_agent_optimizer | ✅ Влучив | Другий найвищий score — точний документ-матч |
| 10 | RL fine-tuning vs SFT | 0.6229 | rlm_comprehensive_guide | ⚠️ Пограничний | Score <0.65 — порівняльний запит між методами fine-tuning |

### 📈 Aggregate metrics

| Метрика | Значення |
|---------|----------|
| Average score | **0.7062** |
| Min score | 0.5685 (Q8: ablation) |
| Max score | 0.8503 (Q2: context rot) |
| Queries > 0.65 (strong) | **7/10** |
| Queries > 0.60 (acceptable) | **9/10** |
| Queries < 0.60 (weak) | **1/10** |

### ✅ Дивіденди semantic retrieval

1. **Концептуальні запити працюють чудово** — Q1 (0.77), Q2 (0.85), Q3 (0.75) отримали високі scores. MiniLM добре захоплює семантику RLM-концептів.
2. **Specific entity matching** — Q9 (HALO, 0.81) та Q2 (context rot, 0.85) демонструють, що коли запит містить унікальну назву/термін, retrieval влучає точно.
3. **Cross-document coverage** — Top-1 результати розподілені по 8 унікальних документах (10 doc total), що свідчить про добре покриття KB.
4. **Документна релевантність** — 6/10 топ-1 результатів з RLM-фокусних документів (rlm_original_paper, rlm_comprehensive_guide, rlm_rl_training_alphaxiv, rlm_candemir_medium).

### ⚠️ Де retrieval слабкий

1. **Ablation/експериментальні запити** — Q8 (0.57) значно нижчий порогового 0.60. Абляція sub-calling — це вузький експериментальний результат, який погано семантично кодується MiniLM.
2. **Порівняльні запити** — Q6 (0.64) та Q10 (0.62) мають scores <0.65. Запити типу "X vs Y" або "X compare to Y" втрачають семантичну специфічність.
3. **Conceptual evolution queries** — Q7 (0.67) на межі. Запити про еволюцію парадигм (flat prompting → recursive) складні для pure semantic search.
4. **Pattern:** низькі scores корелюють із запитами що містять *порівняння* або *вузькі експериментальні деталі* — саме те, що потребує keyword boosting або hybrid search (буде в HW3).

### 🎯 Висновок

Semantic retrieval на MiniLM + FAISS показує solid базову продуктивність (avg 0.71, 9/10 >0.60). Найкраще працює для концептуальних запитів та запитів з унікальними термінами. Найслабші місця — порівняльні запити та вузькі експериментальні деталі. Ці обмеження очікувані для pure semantic search та будуть вирішені в HW3 (hybrid retrieval + metadata filtering) та HW4 (RAG answer generation).
