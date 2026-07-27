# Домашнє завдання №1 — Підготовка knowledge base

## Тема

**Recursive Language Models (RLM) Research Assistant** — чат-бот для допомоги дослідникам ML, інженерам та студентам у розумінні архітектур рекурсивних мовних моделей, їх реалізації, навчання та практичного застосування. Knowledge base покриває повний спектр — від базової теорії до production-інструментів.

## Джерела

Всі документи отримані з першоджерел: офіційних репозиторіїв, статей на arXiv та оригінальних блог-постів.

| # | Документ | URL джерела | Опис |
|---|----------|-------------|------|
| 1 | `rlm_core_paper_and_github.md` | [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) | Основна стаття (arXiv:2512.24601), повний GitHub README, system prompts, REPL environments, model providers, training harness, trajectory logging та налаштування візуалізатора |
| 2 | `rlm_original_paper.md` | [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) | Оригінальна академічна стаття Alex Zhang, Tim Kraska, Omar Khattab (MIT CSAIL). Повний текст: abstract, introduction, methods, results, emergent patterns, related work, limitations, conclusion |
| 3 | `halo_agent_optimizer.md` | [github.com/context-labs/halo](https://github.com/context-labs/halo) | HALO Desktop App — RLM-базований оптимізатор агентів на основі production trace-ів. Архітектура engine, CLI options, Python API, AppWorld benchmarks та telemetry |
| 4 | `prime_intellect_ablations.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Експериментальні абляції Prime Intellect у 4 середовищах (DeepDive, math-python, Oolong, verbatim-copy) з GPT-5-mini. Детальні tips для середовищ та результати |
| 5 | `alexzhang_blog_context_rot.md` | [alexzhang13.github.io/blog/2025/rlm](https://alexzhang13.github.io/blog/2025/rlm/) | Оригінальний блог-пост, що вводить RLMs. Інтуїція context rot, context-centric view, дизайн REPL environment та ключові результати (OOLONG, BrowseComp-Plus, 10M+ tokenів) |
| 6 | `prime_intellect_context_folding.md` | [primeintellect.ai/blog/rlm](https://www.primeintellect.ai/blog/rlm) | Аналіз альтернатив context folding (AgentFold, Agentic Context Engineering) та чому RLM — найбільш гнучкий підхід. Деталі реалізації Prime Intellect |
| 7 | `recurrentgemma_griffin_architecture.md` | [arXiv:2404.07839](https://arxiv.org/abs/2404.07839) | RecurrentGemma від Google DeepMind на архітектурі Griffin. Лінійні рекурренції + локальна увага, fixed-size state, інференс-продуктивність та safety evaluation |
| 8 | `rlm_paper_v3_updates.md` | [arXiv:2512.24601v3](https://arxiv.org/abs/2512.24601v3) | Оновлення травень 2026 (v3, 10,181 KB). Розширені експериментальні результати, інсайти для навчання та RLM як парадигма заміни мовних моделей |
| 9 | `rlm_industry_analysis.md` | Medium аналіз (2026) | Промислова перспектива: візія Prime Intellect, відповідь Google Developer community, порівняння з CoT/ReAct/ToT/RAG та відкриті дослідницькі питання |
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
- **Чанків поза межами 500–1000:** 5/133
- **Унікальних секцій:** 88
- **Placeholder-ів:** 0

## Приклади чанків

### Приклад 1: `rlm_core_chunk_001`

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

**Аналіз:** Цей чанк з *Recursive Language Models — Core Paper and Implementation (MIT)* покриває секцію **"Core Paper & GitHub Setup"**. Він самодостатній і надає детальний опис для відповіді на запитання про основну статтю та налаштування GitHub.

---

### Приклад 2: `halo_agent_optimizer_chunk_005`

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

**Аналіз:** Цей чанк з *HALO: Hierarchical Agent Loop Optimizer* покриває секцію **"HALO: Hierarchical Agent Loop Optimizer"**. Він самодостатній і надає детальний опис для відповіді на запитання про доступні інструменти root LM та subagent tools.

---

### Приклад 3: `prime_intellect_ablations_chunk_008`

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

**Аналіз:** Цей чанк з *Prime Intellect: Recursive Language Models Ablations* покриває секцію **"Prime Intellect: Recursive Language Models Ablations"**. Він самодостатній і надає детальний опис для відповіді на запитання про стратегію DeepDive та math-python проблеми.

---

### Приклад 4: `prime_intellect_context_folding_chunk_005`

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

**Аналіз:** Цей чанк з *Context Folding and the RLM Paradigm* покриває секцію **"Context Folding and the RLM Paradigm"**. Він самодостатній і надає детальний опис для відповіді на запитання про реалізацію RLM та підхід context folding.

---

### Приклад 5: `rlm_original_paper_chunk_001`

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

**Аналіз:** Цей чанк з *Recursive Language Models — Original Paper (MIT CSAIL)* покриває секцію **"Original Academic Paper"**. Він самодостатній і надає детальний опис для відповіді на запитання про abstract оригінальної статті RLM та ключові концепції.

---

## Висновки

### Що вдалося

1. **Вірність першоджерел:** Кожен документ отримано безпосередньо з офіційних джерел — репозиторій статті MIT, репозиторій HALO Context Labs, блог Prime Intellect, блог Alex Zhang, стаття RecurrentGemma Google DeepMind та оновлення arXiv v3. Це гарантує фактичну точність та точні терміни, API сигнатури та експериментальні числа.

2. **Комплексне покриття:** 9 документів покривають повний спектр від дослідження до продукції: теорія (блог), основні дослідження (оригінальна стаття + GitHub + v3 оновлення), production-інструменти (HALO), експериментальна валідація (Prime Intellect ablations), порівняльний аналіз (context folding), додаткова архітектура (RecurrentGemma/Griffin) та промисловий огляд.

3. **Семантична цілісність:** Чанки зберігають межі параграфів та code blocks. Таблиця CLI options HALO, tips середовищ Prime Intellect та таблиці гіперпараметрів RecurrentGemma залишені цілими — критично важливо для research-асистента, де точні значення мають значення.

4. **Багаті метадані:** Domain-специфічні теги (`machine_learning`, `agent-engineering`, `experimental-ml`, `model-architecture`, `ml-theory`, `industry-analysis`) дозволяють розширене фільтрування. Користувач, який запитує "how to install HALO" отримує чанки з `halo_agent_optimizer`; "what is Griffin" → `recurrentgemma_griffin_architecture`.

5. **Стратегія overlap:** 180-символьний overlap гарантує, що cross-paragraph концепти (напр. "REPL environment → sub-LM calls → final answer") залишаються retrievable навіть на межах чанків.

6. **Нуль placeholder-ів:** Всі 125 чанків мають змістовні назви секцій — жодних "General" чи "Overview" placeholder-ів, які б погіршили якість retrieval.

7. **Практичний контент:** Чанки містять конкретну, копіювану інформацію: system prompts, CLI команди, приклади Python API, benchmark-числа, tips середовищ та деталі архітектур. Це робить чат-бота миттєво корисним для практиків.

### Що потребує покращення

1. **Крос-посилання:** Деякі чанки посилаються на концепти з інших документів (напр. блог згадує статтю, HALO посилається на RLM парадигму, RecurrentGemma згадує context windows). Додавання експліцитних `related_chunks` або `see_also` в метадані покращило б multi-document retrieval.

2. **Темпоральні метадані:** Додавання `publication_date` та `last_verified` полів допомогло б чат-боту попереджати користувачів, коли інформація може бути застарілою. Блог від жовтня 2025, оригінальна стаття від грудня 2025, v3 стаття від травня 2026, HALO активно розробляється.

3. **Виконуваний код:** Багато чанків містять code snippets (Python, Bash, CLI). Майбутнє покращення — теги code blocks з `language` та `tested` прапорцями, потенційно з очікуваним output-ом.

4. **Ієрархічні метадані:** Додавання parent/child зв'язків секцій (напр. "REPL Environments → DockerREPL") дозволило б кращі ієрархічні стратегії retrieval.

5. **Рівномірність розміру чанків:** Деякі introductory/overview чанки коротші за 500 символів через природні межі параграфів. Post-processing merge крок міг би об'єднати сусідні короткі чанки для покращення embedding density.

6. **Відсутній візуальний контент:** Оригінальні джерела містять важливі діаграми (архітектура RLM flowchart, діаграма HALO engine, структура шарів RecurrentGemma, benchmark charts). Text-based knowledge base не може їх зберегти. Додавання image URLs або описів діаграм допомогло б.

7. **Версійний трекінг:** HALO та RLM library активно розробляються. Додавання `version` або `commit_hash` в метадані допомогло б користувачам знати, яка версія API в чанку.

8. **Мульти-мовна підтримка:** Наразі весь контент англійською. Для глобальної дослідницької спільноти додавання перекладів або паралельних корпусів іншими мовами розширило б доступність.

## Структура проєкту

```
.
├── README.md
├── data/
│   ├── raw/
│   │   ├── rlm_core_paper_and_github.md      # MIT стаття + GitHub
│   │   ├── rlm_original_paper.md             # Оригінальна академічна стаття (PDF)
│   │   ├── halo_agent_optimizer.md           # Context Labs HALO
│   │   ├── prime_intellect_ablations.md      # Prime Intellect експерименти
│   │   ├── alexzhang_blog_context_rot.md     # Оригінальний блог-пост
│   │   ├── prime_intellect_context_folding.md # Аналіз context folding
│   │   ├── recurrentgemma_griffin_architecture.md # Google DeepMind
│   │   ├── rlm_paper_v3_updates.md           # Оновлення травень 2026
│   │   ├── rlm_industry_analysis.md          # Промисловий огляд
│   │   └── rlm_vs_rag_comparison.md          # RLM vs RAG порівняння
│   └── processed/
│       └── chunks.jsonl                      # 133 чанків (104,994 chars)
└── scripts/
    └── prepare_knowledge_base.py             # Chunking pipeline
```

## Використання

Для регенерації knowledge base з raw-джерел:

```bash
python scripts/prepare_knowledge_base.py
```

Скрипт читає всі Markdown файли з `data/raw/` і генерує `data/processed/chunks.jsonl`.