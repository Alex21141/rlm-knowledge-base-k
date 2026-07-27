# Домашнє завдання №1 — Підготовка knowledge base

## Тема

**Recursive Language Models (RLM) Research Assistant** — чат-бот для допомоги дослідникам ML, інженерам та студентам у розумінні архітектур рекурсивних мовних моделей, їх реалізації, навчання та практичного застосування. Knowledge base покриває повний спектр — від базової теорії до production-інструментів.

## Джерела

Всі документи отримані з першоджерел: офіційних репозиторіїв, статей на arXiv та оригінальних блог-постів.

| # | Документ | URL джерела | Опис |
|---|----------|-------------|------|
| 1 | `alexzhang_blog_context_rot.md` | [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/) | Оригінальний блог-пост Alex Zhang. Інтуїція context rot, REPL design, ключові результати (OOLONG, BrowseComp-Plus, 10M+ tokens) |
| 2 | `halo_agent_optimizer.md` | [github.com/context-labs/halo](https://github.com/context-labs/halo) | HALO — RLM-базований оптимізатор агентів. Архітектура engine, CLI options, Python API, AppWorld benchmarks |
| 3 | `prime_intellect_ablations.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Експериментальні абляції Prime Intellect у 4 середовищах (DeepDive, math-python, Oolong, verbatim-copy) з GPT-5-mini |
| 4 | `prime_intellect_context_folding.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Аналіз context folding альтернатив (AgentFold, Agentic Context Engineering) та чому RLM — найбільш гнучкий підхід |
| 5 | `rag_failure_points_arxiv2024.md` | [arXiv:2401.05856](https://arxiv.org/abs/2401.05856) | Seven Failure Points of RAG (Barnett et al., 2024). Indexing, querying, chunking, scoring, reranking, generation, evaluation |
| 6 | `rag_original_neurips2020.md` | [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) | Original RAG paper (Lewis et al., NeurIPS 2020). Knowledge-intensive NLP: retrieval + generation, dense retrieval DPR, grounded dialogue |
| 7 | `rag_survey_arxiv2024.md` | [arXiv:2312.10997](https://arxiv.org/abs/2312.10997) | RAG Survey (Gao et al., 2024). Taxonomy, methods, benchmarks, open challenges |
| 8 | `rlm_core_paper_and_github.md` | [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) | Основна стаття (arXiv:2512.24601), GitHub README, system prompts, REPL environments, model providers, training harness |
| 9 | `rlm_original_paper.md` | [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) | Оригінальна академічна стаття MIT CSAIL (Zhang, Kraska, Khattab). Abstract, intro, methods, results, limitations |
| 10 | `rlm_vs_rag_comparison.md` | [rlm.md/blog](https://rlm.md/blog/rlm-vs-rag-retrieval-augmented-generation.html) | Детальне порівняння RLM vs RAG: failure modes RAG, completeness advantage RLM, cost/latency trade-offs, when to use each |

## Структура метаданих

| Поле | Тип | Опис |
|------|-----|------|
| `chunk_id` | string | Унікальний ідентифікатор: `{document_id}_chunk_{index}` |
| `text` | string | Фактичний вміст чанку |
| `metadata.document_id` | string | Ідентифікатор вихідного документа |
| `metadata.source_file` | string | Шлях до raw-джерела |
| `metadata.source_type` | string | Формат джерела (`markdown`) |
| `metadata.title` | string | Людський заголовок документа |
| `metadata.section` | string | Найближчий заголовок секції для контексту |
| `metadata.chunk_index` | integer | Послідовний індекс в межах документа |
| `metadata.language` | string | Мова контенту (`en`) |
| `metadata.domain` | string | Тема домену (напр. `machine_learning`, `agent-engineering`) |
| `metadata.document_type` | string | Категорія документа (`research-paper`, `tool`, `blog`, `experimental-report`, `analysis`, `survey`) |

## Стратегія chunking

- **Метод:** Параграфний sliding window зі збереженням семантичних меж
- **Розмір чанку:** ~900 символів (в межах 500–1000)
- **Overlap:** ~180 символів між сусідніми чанками (в межах 100–200)
- **Спеціальна обробка:** Code blocks, таблиці, діаграми (як текст) зберігаються цілими
- **Правила меж:** Чанки розриваються на межах параграфів; великі параграфи — на межах речень

### Статистика розміру чанків

- **Всього чанків:** 244
- **Середній розмір:** 812 символів
- **Мінімум:** 531 символ
- **Максимум:** 913 символів
- **В межах 500–1000:** 244/244 (100%)
- **Коротших за 500:** 0/244
- **Довших за 1000:** 0/244
- **Унікальних секцій:** 103
- **Placeholder-ів:** 0

## Приклади chunks

### Приклад 1: Блог-пост (теорія)

```json
{
  "chunk_id": "alexzhang_blog_context_rot_chunk_001",
  "text": "# Alex Zhang Blog: Recursive Language Models (Oct 2025)\n\n**Source:** https://alexzhang13.github.io/blog/2025/rlm/\n**Full Paper:** https://arxiv.org/abs/2512.24601\n**Code:** https://github.com/alexzhang13/rlm\n\n## tl;dr\n\nWe explore language models that recursively call themselves or other LLMs before providing a final answer. Our goal is to enable the processing of essentially unbounded input context length and output length and to mitigate degradation \"context rot\"...",
  "metadata": {
    "document_id": "alexzhang_blog_context_rot",
    "source_file": "data/raw/alexzhang_blog_context_rot.md",
    "source_type": "markdown",
    "title": "Alex Zhang Blog: Recursive Language Models (Oct 2025)",
    "section": "Alex Zhang Blog: Recursive Language Models (Oct 2025)",
    "chunk_index": 1,
    "language": "en",
    "domain": "ml-theory",
    "document_type": "blog"
  }
}
```

### Приклад 2: Оригінальна стаття (дослідження)

```json
{
  "chunk_id": "rlm_original_paper_chunk_002",
  "text": "the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt. We find that RLMs successfully handle inputs up to two orders of magnitude beyond model context windows and, even for shorter prompts, dramatically outperform the quality of base LLMs and common long-context scaffolds across four diverse long-context tasks, while having comparable (or cheaper) cost per query.\n\n---\n\n## Introduction\n\nDespite rapid progress in reasoning and tool use, modern language models still have limited context lengths and, even within these limits, appear to inevitably exhibit context rot...",
  "metadata": {
    "document_id": "rlm_original_paper",
    "source_file": "data/raw/rlm_original_paper.md",
    "source_type": "markdown",
    "title": "Recursive Language Models — Original Paper (MIT CSAIL)",
    "section": "Introduction",
    "chunk_index": 2,
    "language": "en",
    "domain": "machine_learning",
    "document_type": "research-paper"
  }
}
```

### Приклад 3: RAG Survey (огляд літератури)

```json
{
  "chunk_id": "rag_survey_arxiv2024_chunk_019",
  "text": "ng structure and the original query. The goal of optimizing indexing is to enhance the quality of the content being indexed. This involves strategies: enhancing data granularity, optimizing index structures, adding metadata, alignment optimization, and mixed retrieval. While the goal of query optimization is to make the user's original question clearer and more suitable for the retrieval task...",
  "metadata": {
    "document_id": "rag_survey_arxiv2024",
    "source_file": "data/raw/rag_survey_arxiv2024.md",
    "source_type": "markdown",
    "title": "Retrieval-Augmented Generation for Large Language Models: A Survey (Gao et al., 2024)",
    "section": "General",
    "chunk_index": 19,
    "language": "en",
    "domain": "machine_learning",
    "document_type": "survey"
  }
}
```

### Приклад 4: HALO (production-інструмент)

```json
{
  "chunk_id": "halo_agent_optimizer_chunk_001",
  "text": "# HALO: Hierarchical Agent Loop Optimizer\n\n**Repository:** https://github.com/context-labs/halo\n**PyPI:** `halo-engine`\n**Tagline:** RLM-based agent optimizer using production traces\n\n## What is HALO?\n\nHALO is a hierarchical agent loop optimizer built on top of the Recursive Language Model (RLM) paradigm. It analyzes production agent execution traces, identifies inefficiencies, and rewrites agent loops to improve performance...",
  "metadata": {
    "document_id": "halo_agent_optimizer",
    "source_file": "data/raw/halo_agent_optimizer.md",
    "source_type": "markdown",
    "title": "HALO: Hierarchical Agent Loop Optimizer (Context Labs)",
    "section": "HALO Engine & Benchmarks",
    "chunk_index": 1,
    "language": "en",
    "domain": "agent-engineering",
    "document_type": "tool"
  }
}
```

## Висновки

### Що вдалося

1. **Вірність першоджерел:** 10 документів з офіційних джерел — MIT GitHub, arXiv, Prime Intellect блог, Context Labs, Alex Zhang. Фактична точність термінів, API та експериментальних чисел.

2. **Комплексне покриття:** 10 документів — теорія (блог), основні дослідження (стаття + GitHub), production (HALO), експерименти (ablations + folding), порівняння (RLM vs RAG), foundational RAG (NeurIPS 2020, failure points, survey).

3. **Семантична цілісність:** Чанки зберігають межі параграфів та code blocks. Таблиці CLI options, tips середовищ залишені цілими — критично для research-асистента.

4. **Багаті метадані:** Domain-теги (`machine_learning`, `agent-engineering`, `experimental-ml`, `ml-theory`, `analysis`, `survey`) для фільтрування. Напр. "install HALO" → `halo_agent_optimizer`; "RAG failure points" → `rag_failure_points`.

5. **Zero oversized:** Всі 244 чанки ≤ 913 символів — жодних >1000, що погіршували б embedding quality.

### Що потребує покращення

1. **Крос-посилання:** Чанки посилаються на концепти з інших документів. `related_chunks` в метадани покращило б multi-document retrieval.

2. **Темпоральні метадані:** `publication_date` + `last_verified` для попередження про застарілу інформацію.

3. **Рівномірність розміру:** 4 чанків <500 символів. Merge сусідніх коротких покращив би embedding density.

4. **Візуальний контент:** Діаграми оригіналів (RLM flowchart, HALO engine) втрачені. Image URLs або описи допомогли б.

## Структура проєкту

```
.
├── README.md
├── data/
│   ├── raw/
│   │   ├── alexzhang_blog_context_rot.md
│   │   ├── halo_agent_optimizer.md
│   │   ├── prime_intellect_ablations.md
│   │   ├── prime_intellect_context_folding.md
│   │   ├── rag_failure_points_arxiv2024.md
│   │   ├── rag_original_neurips2020.md
│   │   ├── rag_survey_arxiv2024.md
│   │   ├── rlm_core_paper_and_github.md
│   │   ├── rlm_original_paper.md
│   │   └── rlm_vs_rag_comparison.md
│   └── processed/
│       └── chunks.jsonl
├── index/
│   ├── faiss.index
│   ├── embeddings.npy
│   └── metadata.json
├── outputs/
│   └── retrieval_examples.md
├── scripts/
│   ├── prepare_knowledge_base.py
│   └── retrieval.py
└── prime_intellect_blog_rlm_full.md
```

## Використання

```bash
python scripts/prepare_knowledge_base.py
```

Скрипт читає всі Markdown файли з `data/raw/` і генерує `data/processed/chunks.jsonl`.

---

## Домашнє завдання №2 — Базовий semantic retrieval layer

### Архітектура

- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Vector storage:** FAISS (Inner Product, L2-normalized) + embeddings.npy
- **Chunks indexed:** 244
- **Top-k:** 3

### Використання

```bash
python scripts/retrieval.py build     # Build FAISS index
python scripts/retrieval.py test      # Run test queries
python scripts/retrieval.py search "query"  # Search
```

### Тестові запити та результати

| # | Query | Top-1 Chunk | Score | Relevance |
|---|-------|-------------|-------|-----------|
| 1 | How do RLMs handle arbitrarily long prompts? | rlm_original_paper_chunk_006 | 0.6195 | relevant |
| 2 | What is context rot and why does it happen? | rlm_core_paper_and_github_chunk_004 | 0.6233 | relevant |
| 3 | How does HALO optimize agent loops? | halo_agent_optimizer_chunk_001 | 0.8106 | partially relevant |
| 4 | What are the key differences between RLM and ReAct? | alexzhang_blog_context_rot_chunk_010 | 0.5253 | partially relevant |
| 5 | What are the seven failure points when engineering a RAG system? | rag_failure_points_arxiv2024_chunk_008 | 0.6125 | partially relevant |
| 6 | How does Prime Intellect implement RLM ablations? | prime_intellect_ablations_chunk_001 | 0.5763 | partially relevant |
| 7 | What is context folding and how does RLM compare? | prime_intellect_context_folding_chunk_005 | 0.5596 | partially relevant |
| 8 | How do you install and set up the RLM system? | prime_intellect_context_folding_chunk_006 | 0.4307 | partially relevant |
| 9 | What benchmark results does RLM achieve on Oolong? | prime_intellect_ablations_chunk_013 | 0.6232 | partially relevant |
| 10 | What is the original RAG approach from NeurIPS 2020? | rag_survey_arxiv2024_chunk_011 | 0.4613 | partially relevant |

### Аналіз

- **Релевантні (top-1 correct):** 2/10 — queries 1, 2
- **Частково релевантні:** 8/10
- **Не релевантних:** 0/10
- **Avg Top-1 score:** 0.55
- **Best:** Query 3 (HALO) — score 0.81

### Висновки

- ✅ FAISS index працює з 244 чанками
- ✅ MiniLM дає прийнятну якість для ML/RLM домену
- ⚠️ Базовий semantic retrieval без metadata filtering має partial relevance
- ⚠️ Рекомендація: для підвищення релевантності розглянути metadata filtering, query rewriting або reranking
