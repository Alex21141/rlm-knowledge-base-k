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
- **Максимум:** 913 символ
- **В межах 500–1000:** 244/244 (100%)
- **Коротших за 500:** 0/244
- **Довших за 1000:** 0/244
- **Унікальних секцій:** 103
- **Placeholder-ів:** 0

## Висновки

### Що вдалося

1. **Вірність першоджерел:** 10 документів з офіційних джерел — MIT GitHub, arXiv, Prime Intellect блог, Context Labs, Alex Zhang. Фактична точність термінів, API та експериментальних чисел.

2. **Комплексне покриття:** 10 документів — теорія (блог), основні дослідження (стаття + GitHub), production (HALO), експерименти (ablations + folding), порівняння (RLM vs RAG), foundational RAG (NeurIPS 2020, failure points, survey).

3. **Семантична цілісність:** Чанки зберігають межі параграфів та code blocks. Таблиці CLI options, tips середовищ залишені цілими — критично для research-асистента.

4. **Багаті метадані:** Domain-теги (`machine_learning`, `agent-engineering`, `experimental-ml`, `ml-theory`, `analysis`, `survey`) для фільтрування. Напр. "install HALO" → `halo_agent_optimizer`; "RAG failure points" → `rag_failure_points`.

5. **Zero undersized:** Всі 244 чанків ≥ 531 символів — жодних <500, що забезпечує стабільні embedding quality.

6. **Zero oversized:** Всі 244 чанків ≤ 913 символів — жодних >1000, що погіршували б embedding quality.

### Що потребує покращення

1. **Крос-посилання:** Чанки посилаються на концепти з інших документів. `related_chunks` в метаданих покращило б multi-document retrieval.

2. **Темпоральні метадані:** `publication_date` + `last_verified` для попередження про застарілу інформацію.

3. **Візуальний контент:** Діаграми оригіналів (RLM flowchart, HALO engine) втрачені. Image URLs або описи допомогли б.

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
│       └── chunks.jsonl                      # 244 чанків
└── scripts/
    └── prepare_knowledge_base.py             # Chunking pipeline
```

## Використання

```bash
python scripts/prepare_knowledge_base.py
```

Скрипт читає всі Markdown файли з `data/raw/` і генерує `data/processed/chunks.jsonl`.