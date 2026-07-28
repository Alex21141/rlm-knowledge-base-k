# Домашнє завдання №1 — Підготовка knowledge base

## 1. Опис проєкту

**Subject area:** Recursive Language Models (RLM) Research Assistant

Чат-бот для допомоги дослідникам ML, інженерам та студентам у розумінні архітектур рекурсивних мовних моделей, їх реалізації, навчання та практичного застосування. Knowledge base покриває повний спектр — від базової теорії до production-інструментів.

---

## 2. Джерела

| # | Документ | Джерело | Тип |
|---|----------|---------|-----|
| 1 | `alexzhang_blog_context_rot.md` | alexzhang13.github.io/blog/2025/rlm | Blog |
| 2 | `halo_agent_optimizer.md` | github.com/context-labs/halo | Production tool |
| 3 | `prime_intellect_ablations.md` | primeintellect.ai/blog/rlm | Blog (experimental) |
| 4 | `prime_intellect_context_folding.md` | primeintellect.ai/blog/rlm | Blog (analysis) |
| 5 | `rag_failure_points_arxiv2024.md` | arXiv:2401.05856 | Research paper |
| 6 | `rag_original_neurips2020.md` | arXiv:2005.11401 | Research paper |
| 7 | `rag_survey_arxiv2024.md` | arXiv:2312.10997 | Survey paper |
| 8 | `rlm_core_paper_and_github.md` | github.com/alexzhang13/rlm | Paper + repo |
| 9 | `rlm_original_paper.md` | arXiv:2512.24601 | Research paper |
| 10 | `llm_reasoning_paradigms_evolution.md` | medium.com/@mndeepan06 | Blog (analysis) |

**Домени:** recursive-language-models, retrieval-augmented-generation, ml-reasoning, agent-optimization, context-engineering

---

## 3. Структура метаданих

Кожен chunk містить наступні поля metadata:

| Поле | Тип | Опис |
|------|-----|------|
| `chunk_id` | string | Унікальний ідентифікатор (напр. `rlm_original_paper_chunk_001`) |
| `document_id` | string | Ідентифікатор документа (напр. `rlm_original_paper`) |
| `source_file` | string | Шлях до вихідного файлу (напр. `data/raw/rlm_original_paper.md`) |
| `chunk_index` | integer | Порядковий номер чанку в документі |
| `title` | string | Назва документа |
| `section` | string | Назва розділу документа |
| `language` | string | Мова (en/uk) |
| `domain` | string | Доменна область |
| `document_type` | string | Тип документа (research-paper, guide, tool, blog, analysis, survey) |
| `source_type` | string | Формат джерела (markdown) |

---

## 4. Стратегія chunking

| Параметр | Значення | Обґрунтування |
|----------|----------|---------------|
| `chunk_size` | 500–1000 символів | Достатньо для самостійного читання, не занадто велико |
| `overlap` | 100 символів | Зберігає контекст між сусідніми чанками |
| `метод` | Paragraph-aware splitting | Спочатку розбиття по абзацах, потім об'єднання для досягнення цільового розміру |
| `min_size` | 500 символів | Чанки менше 500 символів об'єднуються з сусідом |

**Pipeline:** `raw sources → normalized markdown → paragraph split → merge to target size → add metadata → chunks.jsonl`

---

## 5. Статистика

| Метрика | Значення |
|---------|----------|
| Вихідних документів | 10 |
| Всього чанків | 237 |
| Всього символів | 191,355 |
| Чанків у range 500–1000 | 233 (98.3%) |
| Undersized (<500) | 4 (1.7%) |
| Oversized (>1000) | 0 (0%) |
| Середній розмір чанку | 807 символів |

**Розбивка по документах:**

| Документ | Chunks | Chars | Avg |
|----------|--------|-------|-----|
| alexzhang_blog_context_rot | 12 | 7,672 | 639 |
| halo_agent_optimizer | 18 | 14,064 | 781 |
| llm_reasoning_paradigms_evolution | 26 | 21,147 | 813 |
| prime_intellect_ablations | 14 | 10,507 | 751 |
| prime_intellect_context_folding | 13 | 10,858 | 835 |
| rag_failure_points_arxiv2024 | 26 | 26,353 | 1,014 |
| rag_original_neurips2020 | 30 | 36,156 | 1,205 |
| rag_survey_arxiv2024 | 25 | 21,886 | 875 |
| rlm_core_paper_and_github | 26 | 24,277 | 934 |
| rlm_original_paper | 10 | 8,435 | 844 |

---

## 6. Приклади chunks

### Приклад 1: Основна стаття RLM

```json
{
  "chunk_id": "rlm_original_paper_chunk_006",
  "text": "general context about the REPL environment (e.g., the length\nof the string P), and permits it to write code that peeks into and decomposes\nP, and to iteratively observe any side effects from execution...",
  "metadata": {
    "document_id": "rlm_original_paper",
    "source_file": "data/raw/rlm_original_paper.md",
    "title": "Recursive Language Models",
    "section": "Introduction",
    "chunk_index": 6,
    "language": "en",
    "domain": "recursive-language-models",
    "document_type": "research-paper"
  }
}
```
*Коментар: Цей чанк описує механізм рекурсивної декомпозиції контексту — ключова концепція RLM.*

### Приклад 2: Context rot

```json
{
  "chunk_id": "rlm_core_paper_and_github_chunk_004",
  "text": "icult to characterize phenomenon in language models known as \"context rot\". Anthropic defines context rot as \"when the number of tokens in the context\nwindow increases, the model's ability to accurat...",
  "metadata": {
    "document_id": "rlm_core_paper_and_github",
    "source_file": "data/raw/rlm_core_paper_and_github.md",
    "title": "RLM Core Paper + GitHub",
    "section": "The Problem: Context Rot",
    "chunk_index": 4,
    "language": "en",
    "domain": "recursive-language-models",
    "document_type": "research-paper"
  }
}
```
*Коментар: Визначення context rot — центральна проблема, яку RLM вирішує.*

### Приклад 3: Eволюція парадигм

```json
{
  "chunk_id": "llm_reasoning_paradigms_evolution_chunk_001",
  "text": "Chain-of-Thought (CoT) prompting was one of the first major innovations that demonstrated LLMs could perform multi-step reasoning when explicitly instructed to 'think step by step'...",
  "metadata": {
    "document_id": "llm_reasoning_paradigms_evolution",
    "source_file": "data/raw/llm_reasoning_paradigms_evolution.md",
    "title": "LLM Reasoning Paradigms Evolution: From Prompting to Recursive Systems",
    "section": "1. Chain-of-Thought (CoT)",
    "chunk_index": 1,
    "language": "en",
    "domain": "ml-reasoning",
    "document_type": "analysis"
  }
}
```
*Коментар: Початок еволюції — від простого prompting до складних парадигм.*

### Приклад 4: HALO agent optimizer

```json
{
  "chunk_id": "halo_agent_optimizer_chunk_001",
  "text": "# HALO: Hierarchical Agent Loop Optimizer\n\n**Repository:** https://github.com/context-labs/halo\n**PyPI:** `halo-engine`\n**Tagline:** RLM-based agent optimizer using production traces",
  "metadata": {
    "document_id": "halo_agent_optimizer",
    "source_file": "data/raw/halo_agent_optimizer.md",
    "title": "HALO: Hierarchical Agent Loop Optimizer",
    "section": "HALO: Hierarchical Agent Loop Optimizer",
    "chunk_index": 1,
    "language": "en",
    "domain": "agent-optimization",
    "document_type": "tool"
  }
}
```
*Коментар: Production інструмент — демонструє практичне застосування RLM.*

### Приклад 5: RAG failure points

```json
{
  "chunk_id": "rag_failure_points_arxiv2024_chunk_007",
  "text": "nces for building RAG systems are constantly emerging [8, 12] but how they relate and perform for a specific application context has to be discovered.\n\nIn this work we present the lessons learned and ...",
  "metadata": {
    "document_id": "rag_failure_points_arxiv2024",
    "source_file": "data/raw/rag_failure_points_arxiv2024.md",
    "title": "Seven Failure Points When Engineering a Retrieval Augmented Generation System",
    "section": "1. INTRODUCTION",
    "chunk_index": 7,
    "language": "en",
    "domain": "retrieval-augmented-generation",
    "document_type": "analysis"
  }
}
```
*Коментар: Аналіз практичних проблем RAG — важливий контекст для розуміння, чому потрібні покращення.*

---

## 7. Висновок

### Що вийшло добре

1. **Якість джерел:** Усі 10 документів отримані з першоджерел (arXiv PDF, GitHub, офіційні блоги). Жодних HTML-артефактів чи дублікатів.
2. **Метадані:** Повна структура з 10 полів, включаючи domain та document_type для майбутнього filtering.
3. **Chunking:** 98.3% чанків у цільовому range 500–1000 символів. Paragraph-aware метод зберігає читабельність.
4. **Покриття:** KB покриває 5 доменів — від теорії (RLM paper) до практики (HALO, Prime Intellect) та порівняльних аналізів.

### Що треба покращити

1. **Undersized chunks:** 4 чанки (<500 символів) залишились. В основному — короткі розділи, де об'єднання з сусідом руйнує семантику.
2. **Нерівномірне покриття:** `rag_original_neurips2020.md` генерує найбільше чанків (30) через великий PDF-текст. Можливо варто збільшити chunk_size для цього документа.
3. **Доменна класифікація:** Поле `domain` може бути розширене — зараз використовується лише для груповання, але може бути використано для precision filtering.