# Домашнє завдання №2 — Базовий semantic retrieval layer

## 1. Опис проєкту

**Subject area:** Recursive Language Models (RLM) Research Assistant

Побудовано базовий retrieval layer для knowledge base з 10 документів (237 чанків). Pipeline: `chunks.jsonl → embeddings → FAISS index → top-k semantic search → retrieved chunks`.

---

## 2. Embedding model

| Параметр | Значення |
|----------|----------|
| Модель | `sentence-transformers/all-MiniLM-L6-v2` |
| Вимірність | 384 |
| Normalization | L2 (cosine similarity via inner product) |

---

## 3. Vector storage

| Параметр | Значення |
|----------|----------|
| Тип індексу | FAISS Inner Product (`IndexIP`) |
| Кількість векторів | 237 |
| Вимірність | 384 |
| Збереження | `index/faiss.index` + `index/embeddings.npy` + `index/metadata.json` |

---

## 4. Retrieval implementation

Script: `scripts/retrieval.py`

**Pipeline:**
1. Load chunks from `data/processed/chunks.jsonl`
2. Encode all chunk texts with MiniLM → 384-dim embeddings
3. Build FAISS IndexIP + save to disk
4. For each query: encode → search top-k=3 → return (chunk_id, score, text_preview, metadata)

**Usage:**
```bash
# Build index
python scripts/retrieval.py build

# Search
python scripts/retrieval.py search "How do RLMs handle long context?"
```

---

## 5. Тестові запити (10 queries)

### Query 1: How do RLMs handle arbitrarily long prompts?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `rlm_original_paper_chunk_006` | 0.620 | rlm_original_paper.md | Introduction |
| Top-2 | `prime_intellect_ablations_chunk_005` | 0.613 | prime_intellect_ablations.md | Input Data Handling |
| Top-3 | `rlm_original_paper_chunk_031` | 0.555 | rlm_original_paper.md | Limitations and Future Work |

**Comment:** ✅ **relevant** — Top-1 прямо відповідає на питання про рекурсивну декомпозицію контексту.

---

### Query 2: What is context rot and why does it happen?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `rlm_core_paper_and_github_chunk_004` | 0.623 | rlm_core_paper_and_github.md | The Problem: Context Rot |
| Top-2 | `alexzhang_blog_context_rot_chunk_004` | 0.614 | alexzhang_blog_context_rot.md | Prelude: Why Long-Context Research So Unsatisfactory |
| Top-3 | `rlm_core_paper_and_github_chunk_003` | 0.500 | rlm_core_paper_and_github.md | Core Concept: Context-Centric View |

**Comment:** ✅ **relevant** — Чудове покриття з двох джерел (paper + blog).

---

### Query 3: How does HALO optimize agent loops?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `halo_agent_optimizer_chunk_001` | 0.811 | halo_agent_optimizer.md | HALO Overview |
| Top-2 | `halo_agent_optimizer_chunk_002` | 0.602 | halo_agent_optimizer.md | Telemetry |
| Top-3 | `halo_agent_optimizer_chunk_003` | 0.550 | halo_agent_optimizer.md | HALO Engine Architecture |

**Comment:** ✅ **relevant** — Найвищий score (0.811), все з одного документа.

---

### Query 4: What are the key differences between RLM and ReAct?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `alexzhang_blog_context_rot_chunk_010` | 0.525 | alexzhang_blog_context_rot.md | ReAct (Reasoning + Acting) |
| Top-2 | `rlm_core_paper_and_github_chunk_016` | 0.465 | rlm_core_paper_and_github.md | RLMs in the Wild |
| Top-3 | `rlm_original_paper_chunk_017` | 0.430 | rlm_original_paper.md | Results and Discussion |

**Comment:** ⚠️ **partially relevant** — Top-1 містить порівняння, але score низький (0.525). Top-2-3 слабко релевантні.

---

### Query 5: What are the seven failure points when engineering a RAG system?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `rag_failure_points_arxiv2024_chunk_007` | 0.696 | rag_failure_points_arxiv2024.md | INTRODUCTION |
| Top-2 | `rag_failure_points_arxiv2024_chunk_003` | 0.567 | rag_failure_points_arxiv2024.md | INTRODUCTION |
| Top-3 | `rag_survey_arxiv2024_chunk_007` | 0.544 | rag_survey_arxiv2024.md | General |

**Comment:** ⚠️ **partially relevant** — Знайшов документ, але Top-1 — інтро, а не перелік 7 failure points.

---

### Query 6: How does Prime Intellect implement RLM ablations?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `prime_intellect_ablations_chunk_001` | 0.576 | prime_intellect_ablations.md | Prime Intellect: RLM Ablations |
| Top-2 | `rlm_original_paper_chunk_021` | 0.495 | rlm_original_paper.md | Emergent Patterns in RLM Trajectories |
| Top-3 | `prime_intellect_ablations_chunk_003` | 0.465 | prime_intellect_ablations.md | Implementation Details |

**Comment:** ⚠️ **partially relevant** — Top-1 — overview, Top-3 кращий (Implementation Details).

---

### Query 7: What is context folding and how does RLM compare?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `prime_intellect_context_folding_chunk_005` | 0.560 | prime_intellect_context_folding.md | RLM Implementation at Prime Intellect |
| Top-2 | `rlm_core_paper_and_github_chunk_003` | 0.556 | rlm_core_paper_and_github.md | Core Concept: Context-Centric View |
| Top-3 | `rlm_core_paper_and_github_chunk_007` | 0.537 | rlm_core_paper_and_github.md | Experimental Results |

**Comment:** ⚠️ **partially relevant** — Знайшов релевантний документ, але не точний розділ про AgentFold.

---

### Query 8: How do you install and set up the RLM system?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `rlm_core_paper_and_github_chunk_016` | 0.458 | rlm_core_paper_and_github.md | RLMs in the Wild |
| Top-2 | `prime_intellect_context_folding_chunk_006` | 0.431 | prime_intellect_context_folding.md | Experimental Results Summary |
| Top-3 | `rlm_core_paper_and_github_chunk_011` | 0.337 | rlm_core_paper_and_github.md | REPL Environments |

**Comment:** ❌ **not relevant** — Top-1 не про install. Top-3 містить `pip install rlms`, але score занадто низький (0.337).

---

### Query 9: What benchmark results does RLM achieve on Oolong?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `prime_intellect_ablations_chunk_013` | 0.623 | prime_intellect_ablations.md | Verbatim Copy |
| Top-2 | `rlm_original_paper_chunk_021` | 0.603 | rlm_original_paper.md | Emergent Patterns in RLM Trajectories |
| Top-3 | `rlm_original_paper_chunk_019` | 0.597 | rlm_original_paper.md | Results and Discussion |

**Comment:** ⚠️ **partially relevant** — Top-1 про Verbatim Copy, не Oolong. Top-3 (Results and Discussion) ближче.

---

### Query 10: What is the original RAG approach from NeurIPS 2020?

| Rank | Chunk | Score | Source | Section |
|------|-------|-------|--------|---------|
| Top-1 | `rag_survey_arxiv2024_chunk_011` | 0.461 | rag_survey_arxiv2024.md | General |
| Top-2 | `rag_survey_arxiv2024_chunk_009` | 0.440 | rag_survey_arxiv2024.md | General |
| Top-3 | `rag_survey_arxiv2024_chunk_007` | 0.422 | rag_survey_arxiv2024.md | General |

**Comment:** ❌ **not relevant** — Survey згадує RAG, але не оригінальну роботу NeurIPS 2020. Чанки з `rag_original_neurips2020.md` взагалі не потрапили в top-3.

---

## 6. Аналіз результатів

### Статистика релевантності

| Релевантність | Кількість | Queries |
|---------------|-----------|---------|
| ✅ **Relevant** | 2 | Q1 (RLM long prompts), Q2 (context rot) |
| ⚠️ **Partially relevant** | 6 | Q3-Q9 |
| ❌ **Not relevant** | 2 | Q8 (install RLM), Q10 (RAG NeurIPS 2020) |

### Що retrieval робить добре

1. **Концептуальні запити:** Чудова робота з core RLM concepts (Q1, Q2). MiniLM добре кодує семантику RLM-термінології.
2. **Назви проектів:** HALO (Q3) — найвищий score (0.811), тому що назва проекту є сильним семантичним маркером.
3. **Поширені концепції:** Context rot, RLM ablations, context folding — добре знаходяться через cross-document coverage.

### Де retrieval слабкий

1. **Setup/install запити:** Q8 повернув нерелевантні результати. Проблема: `pip install` — дуже коротка фраза, яка не має достатньо семантики для embedding.
2. **Конкретні цитування:** Q10 (NeurIPS 2020 RAG) — запит занадто специфічний, embedding не містить семантики "який саме папер".
3. **Низькі score для порівнянь:** Q4 (RLM vs ReAct) — score 0.525, що вказує на слабку семантичну схожість між "RLM" та "ReAct" у embedding space.

### Висновок

Baseline retrieval з MiniLM + FAISS показує **прийнятну якість для концептуальних запитів** (2/10 fully relevant, 6/10 partially relevant). Але **слабкий для запитів про конкретні інструкції/цитати** (2/10 not relevant).

**Рекомендація:** Для покращення — додати metadata filtering (по domain/document_type), query rewriting для розширення специфічних запитів, та hybrid scoring (semantic + keyword) для покриття випадків, де чистий embedding слабкий.