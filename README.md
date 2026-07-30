# Домашнє завдання №3 — Покращення retrieval pipeline

## 1. Опис проєкту

Покращення retrieval pipeline з HW2. Baseline vs Improved порівняння на 10 RLM-запитах.

**Покращення:**
1. Metadata filtering (document_type, domain, source_file)
2. Query rewriting (pattern-based expansion for RLM domain)
3. Hybrid scoring (semantic MiniLM + keyword BM25-like)

---

## 2. Knowledge base

| Метрика | Значення |
|---------|----------|
| Документів | **10** |
| Чанків | **467** |
| Vectors в index | **467** |
| Середній розмір чанку | **697 chars** |

---

## 3. Retrieval pipeline

**Baseline (HW2):** Semantic search only (MiniLM + FAISS)
**Improved:** Metadata filtering + Query rewriting + Hybrid scoring

**Config:**

| Параметр | Baseline | Improved |
|----------|----------|----------|
| Embedding model | all-MiniLM-L6-v2 | all-MiniLM-L6-v2 |
| FAISS index | IndexFlatIP | IndexFlatIP |
| Query rewriting | ❌ | ✅ (10 patterns for RLM domain) |
| Metadata filtering | ❌ | ✅ (topic-based) |
| Hybrid scoring | ❌ | ✅ (0.20 keyword weight) |
| Top-k | 5 | 5 |

---

## 4. Тестові запити (10)

Ті самі 10 запитів з HW2 — RLM-focused:

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

## 5. Результати (baseline vs improved)

| Query | Baseline top-1 | Improved top-1 | Що змінилось |
|-------|---------------|----------------|-------------|
| 1. Long prompts | \`rlm_original_paper_chunk_002\` (0.701) | \`rlm_original_paper_chunk_027\` (0.828) | ✅ Better chunk (query rewrite): 0.8280 vs 0.7010 |
| 2. Context rot | \`rlm_candemir_medium_chunk_003\` (0.694) | \`rlm_original_paper_chunk_004\` (0.702) | ✅ Better chunk (query rewrite): 0.7020 vs 0.6940 |
| 3. Python REPL | \`alexzhang_blog_context_rot_chunk_013\` (0.660) | \`alexzhang_blog_context_rot_chunk_013\` (0.742) | ✅ Score improved: +0.082 (hybrid) |
| 4. Benchmarks | \`rlm_original_paper_chunk_036\` (0.597) | \`rlm_original_paper_chunk_036\` (0.651) | ✅ Score improved: +0.054 (hybrid) |
| 5. RLM vs base LLMs | \`rlm_comprehensive_guide_chunk_002\` (0.747) | \`rlm_original_paper_chunk_035\` (0.828) | ✅ Better chunk (query rewrite): 0.8280 vs 0.7470 |
| 6. RLM vs RAG | \`rlm_candemir_medium_chunk_022\` (0.660) | \`rlm_candemir_medium_chunk_022\` (0.752) | ✅ Score improved: +0.092 (hybrid) |
| 7. Context folding | \`prime_intellect_ablations_chunk_007\` (0.776) | \`prime_intellect_ablations_chunk_007\` (0.686) | ⚠️ Score degraded: -0.090 |
| 8. Ablation results | \`prime_intellect_ablations_chunk_057\` (0.601) | \`rlm_comprehensive_guide_chunk_002\` (0.635) | ✅ Better chunk (query rewrite): 0.6350 vs 0.6010 |
| 9. HALO agent | \`halo_agent_optimizer_chunk_001\` (0.762) | \`halo_agent_optimizer_chunk_001\` (0.868) | ✅ Score improved: +0.106 (hybrid) |
| 10. RL fine-tuning | \`rlm_rl_training_alphaxiv_chunk_002\` (0.666) | \`rlm_rl_training_alphaxiv_chunk_002\` (0.739) | ✅ Score improved: +0.073 (hybrid) |

**Aggregate:**

| Метрика | Baseline | Improved | Δ |
|---------|----------|----------|---|
| Average score | 0.686 | 0.743 | +0.057 |
| Queries improved | — | 9/10 | ✅ |
| Queries degraded | — | 1/10 | ⚠️ |

**Note:** Q7 (Context folding) має score degradation (-0.089) тому що rewritten query `context folding agentic context engineering AgentFold...` семантично віддалений від оригінального chunk. Це trade-off query rewriting — іноді знаходить кращий chunk, іноді погіршує match.

---

## 6. Висновок

### ✅ Що вийшло добре

1. **8/10 queries improved** — 8 запитів отримали кращі результати (4 через query rewriting, 4 через hybrid scoring)
2. **Query rewriting знайшов кращі chunks** — Q1 (0.701→0.828), Q5 (0.747→0.828), Q8 (0.601→0.635) — значне покращення
3. **Hybrid scoring стабільний boost** — avg +0.074 для 4 query (HALO +0.107, RLM vs RAG +0.092, Python REPL +0.082, RL fine-tuning +0.073)

### ⚠️ Trade-offs

1. **Q7 (Context folding) degraded** — rewritten embedding далі від оригінального chunk (0.776→0.686), тому що rewriting додав зайві терміни (AgentFold, agentic, delegation)
2. **Query rewriting не завжди покращує** — для точних, специфічних запитів rewriting може "розмити" семантичний фокус
3. **Metadata filtering мало використано** — 0 query отримали improvement через filter (filter часто повертає 0 chunks)

*Ці обмеження будуть частково вирішені в HW4 (RAG Answer Generation).*
