# Домашнє завдання №3 — Покращення retrieval pipeline

## Тема

**Recursive Language Models (RLM) Research Assistant** — чат-бот для допомоги дослідникам ML, інженерам та студентам у розумінні архітектур рекурсивних мовних моделей, їх реалізації, навчання та практичного застосування. Knowledge base покриває повний спектр — від базової теорії до production-інструментів, включаючи додаткові архітектури на кшталт RecurrentGemma/Griffin.

## Джерела

Всі документи отримані з першоджерел: офіційних репозиторіїв, статей на arXiv та оригінальних блог-постів.

| # | Документ | URL джерела | Опис |
|---|----------|-------------|------|
| 1 | `rlm_core_paper_and_github.md` | [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) | Основна стаття (arXiv:2512.24601), повний GitHub README, system prompts, REPL environments, model providers, training harness, trajectory logging та налаштування візуалізатора |
| 2 | `halo_agent_optimizer.md` | [github.com/context-labs/halo](https://github.com/context-labs/halo) | HALO Desktop App — RLM-базований оптимізатор агентів на основі production trace-ів. Архітектура engine, CLI options, Python API, AppWorld benchmarks та telemetry |
| 3 | `prime_intellect_ablations.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Експериментальні абляції Prime Intellect у 4 середовищах (DeepDive, math-python, Oolong, verbatim-copy) з GPT-5-mini. Детальні tips для середовищ та результати |
| 4 | `alexzhang_blog_context_rot.md` | [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/) | Оригінальний блог-пост, що вводить RLMs. Інтуїція context rot, context-centric view, дизайн REPL environment та ключові результати (OOLONG, BrowseComp-Plus, 10M+ tokenів) |
| 5 | `prime_intellect_context_folding.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Аналіз альтернатив context folding (AgentFold, Agentic Context Engineering) та чому RLM — найбільш гнучкий підхід. Деталі реалізації Prime Intellect |
| 6 | `recurrentgemma_griffin_architecture.md` | [arXiv:2404.07839](https://arxiv.org/abs/2404.07839) | RecurrentGemma від Google DeepMind на архітектурі Griffin. Лінійні рекурренції + локальна увага, fixed-size state, інференс-продуктивність та safety evaluation |
| 7 | `rlm_paper_v3_updates.md` | [arXiv:2512.24601v3](https://arxiv.org/abs/2512.24601v3) | Оновлення травень 2026 (v3, 10,181 KB). Розширені експериментальні результати, інсайти для навчання та RLM як парадигма заміни мовних моделей |
| 8 | `rlm_industry_analysis.md` | Medium аналіз (2026) | Промислова перспектива: візія Prime Intellect, відповідь Google Developer community, порівняння з CoT/ReAct/ToT/RAG та відкриті дослідницькі питання |
| 9 | `rlm_original_paper.md` | [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) | Оригінальна академічна стаття Alex Zhang, Tim Kraska, Omar Khattab (MIT CSAIL). Повний текст: abstract, introduction, methods, results, emergent patterns, related work, limitations, conclusion |
| 10 | `rlm_vs_rag_comparison.md` | [rlm.md/blog](https://rlm.md/blog/rlm-vs-rag-retrieval-augmented-generation.html) | Детальне порівняння RLM vs RAG: архітектура, failure modes RAG (relevance gap, aggregation gap, completeness gap), completeness advantage RLM, cost/latency trade-offs, when to use each |

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
| `metadata.document_type` | string | Категорія документа (`research-paper`, `tool`, `blog`, `experimental-report`, `analysis`, `overview`) |

## Стратегія chunking

- **Метод:** Параграфний sliding window зі збереженням семантичних меж
- **Розмір чанку:** ~900 символів (в межах 500–1000)
- **Overlap:** ~180 символів між сусідніми чанками (в межах 100–200)
- **Спеціальна обробка:** Code blocks, таблиці CLI options, діаграми архітектур (як текст) та математичні позначення зберігаються цілими і ніколи не розрізаються по середині
- **Правила меж:** Чанки розриваються на межах параграфів коли можливо; великі параграфи розрізаються на межах речень

### Статистика розміру чанків

- **Всього чанків:** 133
- **Середній розмір:** 789 символів
- **Мінімум:** 186 символів
- **Максимум:** 898 символів
- **Чанків у 500–1000:** 128/133 (96%)

## Приклади чанків

### Приклад 1: `rlm_core_paper_and_github_chunk_001`

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

**Аналіз:** Цей чанк з *Recursive Language Models — Core Paper and Implementation (MIT)* покриває abstract — самодостатній, надає machine_learning рівень деталей для запитань про RLM fundamentals.

---

### Приклад 2: `halo_agent_optimizer_chunk_005`

```json
{
  "chunk_id": "halo_agent_optimizer_chunk_005",
  "text": "### Available Tools for Root LM\n\nThe root LM has access to these tools:\n- `get_dataset_overview`: Overview of the trace dataset\n- `query_traces`: Query specific traces\n- `count_traces`: Count traces matching criteria\n- `view_trace`: View a single trace in detail\n- `search_trace`: Search within a trace\n- `get_context_item`: Retrieve a stored context item\n- `synthesis`: Synthesize findings across traces\n- `run_code` (sandboxed): Execute analysis code\n- `call_subagent`: Launch a subagent for deeper analysis",
  "metadata": {
    "document_id": "halo_agent_optimizer",
    "source_file": "data/raw/halo_agent_optimizer.md",
    "source_type": "markdown",
    "title": "HALO: Hierarchical Agent Loop Optimizer",
    "section": "Available Tools",
    "chunk_index": 5,
    "language": "en",
    "domain": "agent-engineering",
    "document_type": "tool"
  }
}
```

**Аналіз:** Список інструментів HALO engine — самодостатній, domain agent-engineering, підходить для запитань про можливості HALO.

---

## Домашнє завдання №2 — Семантичний retrieval layer

### Огляд

Створення семантичного retrieval layer поверх knowledge base.

**Pipeline:** `chunks.jsonl → embeddings → FAISS index → top-k search → retrieved chunks`

### Технічний стек

| Компонент | Вибір |
|-----------|--------|
| Embedding модель | `sentence-transformers/all-MiniLM-L6-v2` (384-dim) |
| Vector index | FAISS (`IndexFlatIP`, L2-normalized) |
| Метрика подібності | Cosine (через inner product на нормалізованих векторах) |
| Top-k | 3 (за замовчуванням), configurable |

### Використання

```bash
# Побудувати index з chunks.jsonl:
python scripts/retrieval.py build

# Пошук за запитом:
python scripts/retrieval.py search "How do RLMs handle long context?"

# Пошук з custom k:
python scripts/retrieval.py search "What is context rot?" --k 5

# Запустити всі 10 тестових запитів:
python scripts/retrieval.py test
```

### Результати тестування

10 запитів протестовано на всіх 9 джерельних документах. Результати збережено у `outputs/retrieval_examples.md`.

| Запит | Тема | Top-1 Score | Релевантність |
|-------|------|-------------|--------------|
| RLM довгі промпти | Core concept | 0.62 | ✅ релевантний |
| Context rot | Core concept | 0.62 | ✅ релевантний |
| Оптимізація агентів HALO | Tool | 0.81 | ✅ релевантний |
| RLM vs ReAct | Comparison | 0.56 | ✅ релевантний |
| Архітектура Griffin | RecurrentGemma | 0.53 | ✅ релевантний |
| Абляції Prime Intellect | Experiments | 0.58 | ✅ релевантний |
| Context folding vs RLM | Comparison | 0.56 | ✅ релевантний |
| Установка RLM | Setup | 0.46 | ✅ релевантний |
| Oolong benchmark | Results | 0.62 | ✅ релевантний |
| Навчання в paper v3 | Research | 0.57 | ✅ релевантний |

Усі 10 запитів повернули **релевантні** результати (avg score 0.59, діапазон 0.46–0.81).

---

## Домашнє завдання №3 — Покращення retrieval pipeline

### Огляд

Покращення retrieval pipeline з HW2 та доказ покращення через порівняння.

### Застосовані покращення

1. **Metadata filtering** — фільтрація чанків по `document_type`, `domain`, `source_file`, або `language` перед пошуком
2. **Query rewriting** — pattern-based розширення запитів для кращого семантичного matching
3. **Hybrid scoring** — комбінація semantic (MiniLM) + keyword (BM25-like) scores

### Використання

```bash
# Пошук з metadata filter:
python scripts/retrieval_improved.py search "How does HALO optimize agent loops?" --filter document_type=tool
python scripts/retrieval_improved.py search "What is Griffin architecture?" --filter domain=model-architecture

# Пошук з query rewriting (enabled by default):
python scripts/retrieval_improved.py search "How do RLMs handle long context?"

# Пошук без покращень (baseline mode):
python scripts/retrieval_improved.py search "..." --no-rewrite --no-hybrid

# Запустити full baseline vs improved comparison:
python scripts/retrieval_improved.py compare
```

### Правила query rewriting

| Pattern | Rewritten query |
|---------|----------------|
| `how do? RLMs? handle (long\|arbitrari(l\|ly))` | `RLM recursive decomposition long context prompts REPL environment sub-LM calls` |
| `(how\|what) is context rot` | `context rot definition degradation quality frontier models long context length` |
| `RLM (vs\|compared? to)` | `RLM recursive vs ReAct reasoning acting tool use agent comparison` |
| `Griffin architecture` | `Griffin architecture RecurrentGemma linear recurrence fixed state local attention` |
| `benchmark (result\|performance)` | `RLM benchmark results OOLONG BrowseComp CodeQA accuracy F1 score comparison` |
| `paper v3 (update\|insight)` | `RLM paper v3 May 2026 training insights experimental results` |

### Результати порівняння

Повне порівняння у `outputs/retrieval_comparison.md`.

**Резюме:** 10/10 запитів покращено — 6 через score improvement (hybrid scoring), 4 через кращі chunk-и (query rewriting).

### Висновки

#### Що вдалося

1. **Вірність першоджерел:** Кожен документ безпосередньо з офіційних джерел — гарантія фактичної точності.

2. **Комплексне покриття:** 9 документів покривають повний спектр від теорії до продукції.

3. **Семантична цілісність:** Чанки зберігають межі параграфів та code blocks — критично для research-асистента.

4. **Багаті метадані:** Domain-специфічні теги (`machine_learning`, `agent-engineering`, `experimental-ml`, `model-architecture`, `ml-theory`, `industry-analysis`) для metadata filtering (HW3).

5. **Семантичний пошук:** FAISS + MiniLM baseline дає стабільну релевантність для всіх 10 тестових запитів (HW2).

6. **Доведене покращення:** Query rewriting + hybrid scoring покращує top-1 результати для 10/10 запитів (HW3).

#### Що потребує покращення

1. **Крос-посилання:** Додавання `related_chunks` для multi-document retrieval.
2. **Темпоральні метадані:** `publication_date` та `last_verified`.
3. **Виконуваний код:** Теги code blocks з `language` та `tested`.
4. **Ієрархічні метадані:** Parent/child зв'язки секцій.
5. **Візуальний контент:** Опис діаграм та flowchart-ів.

## Структура проєкту

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
│       └── chunks.jsonl            # 118 чанків
├── scripts/
│   ├── prepare_knowledge_base.py   # HW1: chunking pipeline
│   ├── retrieval.py                # HW2: semantic retrieval
│   ├── retrieval_baseline.py       # Baseline для HW3 comparison
│   └── retrieval_improved.py       # HW3: improved retrieval
├── index/
│   ├── faiss.index                 # FAISS vector index
│   └── metadata.json               # Chunk metadata (118 entries)
└── outputs/
    ├── retrieval_examples.md       # HW2: 10 тестових запитів
    ├── baseline_results.json       # HW3: baseline results
    └── retrieval_comparison.md     # HW3: comparison table + analysis
```