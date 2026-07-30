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
| 3 | `llm_reasoning_paradigms_evolution.md` | medium.com/@mndeepan06 | Blog (analysis) |
| 4 | `prime_intellect_ablations.md` | primeintellect.ai/blog/rlm | Blog (experimental) |
| 5 | `rlm_candemir_medium.md` | medium.com/@candemir13 | Blog (beginner guide) |
| 6 | `rlm_rl_training_alphaxiv.md` | alphaxiv.org/blog/rlm | Blog (RL training) |
| 7 | `rlm_comprehensive_guide.md` | rlm.md | Guide |
| 8 | `rlm_deep_dive_towardsdatascience.md` | towardsdatascience.com (Avishek Biswas) | Blog (deep-dive) |
| 9 | `rlm_original_paper.md` | arXiv:2512.24601 (Zhang, Kraska, Khattab) | Research paper |
| 10 | `rlm_production_zenml.md` | zenml.io/blog (ZenML) | Blog (production) |

**Домени:** recursive-language-models, ml-reasoning, agent-optimization, context-engineering

---

## 3. Структура метаданих

Кожен chunk містить:

| Поле | Тип | Опис |
|------|-----|------|
| `chunk_id` | string | `docid_chunk_NNN` (напр. `rlm_original_paper_chunk_001`) |
| `document_id` | string | Ідентифікатор документа |
| `source_file` | string | `data/raw/rlm_original_paper.md` |
| `chunk_index` | int | Порядковий номер (0-based) |
| `title` | string | Назва документа |
| `section` | string | Назва розділу |
| `language` | string | Мова (en/uk) |
| `domain` | string | Доменна область |
| `document_type` | string | research-paper / guide / tool / blog / analysis |
| `source_type` | string | markdown |

---

## 4. Стратегія chunking

| Параметр | Значення | Обґрунтування |
|----------|----------|---------------|
| `chunk_size` | 600 chars | Баланс: достатньо контексту, не занадто велико |
| `overlap` | 100 chars | Зберігає перехід між сусідніми чанками |
| `метод` | Paragraph-aware splitting | Спочатку розбиття по абзацах, потім merge до target size |
| `min_size` | 500 chars | Чанки <500 об'єднуються з сусідом |

**Pipeline:** `raw markdown → normalize → paragraph split → merge to 600 → add metadata → chunks.jsonl`

---

## 5. Статистика

| Метрика | Значення |
|---------|----------|
| Вихідних документів | 10 |
| Всього чанків | 467 |
| Всього символів | 325,538 |
| Чанків 500-1000 chars | 458 (98.1%) ✅ |
| Undersized (<500) | 6 (1.3%) |
| Oversized (>1000) | 3 (0.6%) |
| Середній розмір | 697 chars |

**Per-document breakdown:**

| Документ | Chunks | Chars | Avg |
|----------|--------|-------|-----|
| alexzhang_blog_context_rot | 73 | 48,575 | 665 |
| halo_agent_optimizer | 14 | 9,180 | 655 |
| llm_reasoning_paradigms_evolution | 27 | 17,661 | 654 |
| prime_intellect_ablations | 80 | 53,620 | 670 |
| rlm_candemir_medium | 36 | 23,824 | 661 |
| rlm_comprehensive_guide | 32 | 20,823 | 650 |
| rlm_deep_dive_towardsdatascience | 62 | 41,060 | 662 |
| rlm_original_paper | 54 | 51,814 | 959 |
| rlm_production_zenml | 35 | 23,567 | 673 |
| rlm_rl_training_alphaxiv | 54 | 35,414 | 655 |

---

## 6. Приклади chunks

### RLM original paper (chunk 1)
```json
{"chunk_id": "rlm_original_paper_chunk_001", "text": "# Recursive Language Models -- Original Paper (MIT CSAIL)\n\n**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab...", "metadata": {"document_id": "rlm_original_paper", "section": "Introduction", "domain": "recursive-language-models", "document_type": "research-paper"}}
```

### RL training for RLMs (chunk 1)
```json
{"chunk_id": "rlm_rl_training_alphaxiv_chunk_001", "text": "# Reinforcing Recursive Language Models — alphaXiv Blog\n\n**Source:** https://www.alphaxiv.org/blog/reinforcement-learning-for-rlms\n**Platform:** alphaXiv / NovaSky AI (SkyRL)...", "metadata": {"document_id": "rlm_rl_training_alphaxiv", "section": "RL Training", "domain": "recursive-language-models", "document_type": "blog"}}
```

### TDS deep-dive (chunk 10)
```json
{"chunk_id": "rlm_deep_dive_towardsdatascience_chunk_010", "text": "Let's trace through a concrete example. The RLM receives a user query about analyzing a long document...", "metadata": {"document_id": "rlm_deep_dive_towardsdatascience", "section": "Concrete Example", "domain": "recursive-language-models"}}
```

### ZenML production (chunk 5)
```json
{"chunk_id": "rlm_production_zenml_chunk_005", "text": "RLMs can handle inputs up to two orders of magnitude beyond model context windows. The RLM-Qwen3-8B improves median performance by 28.3%...", "metadata": {"document_id": "rlm_production_zenml", "section": "Key Results from the Paper", "domain": "recursive-language-models"}}
```

### HALO tool (chunk 1)
```json
{"chunk_id": "halo_agent_optimizer_chunk_001", "text": "# HALO: Hierarchical Agent Loop Optimizer\n\n**Repository:** https://github.com/context-labs/halo\n**Tagline:** RLM-based agent optimizer...", "metadata": {"document_id": "halo_agent_optimizer", "section": "HALO Overview", "domain": "agent-optimization", "document_type": "tool"}}
```

---

## 7. Висновок

### ✅ Що вийшло добре

1. **Унікальні джерела** — 10 документів, 0 семантичних дублікатів (Jaccard <0.05 між усіма парами)
2. **Якість чанків** — 98.1% у цільовому range 500-1000 chars, 3 oversized (0.6%)
3. **Метадані** — повна структура (10 полів), ready для filtering по domain / document_type
4. **Покриття** — 4 домени: RLM теорія + agent optimization + reasoning + production
5. **Повні оригінали** — 3 ключові документи повні (alexzhang 43KB, prime_intellect 47KB, arXiv paper 128KB)

### ⚠️ Що покращити

1. **Undersized chunks** — 6 чанків (<500 chars). Короткі розділи, де merge руйнує семантику.
2. **Нерівномірність** — `prime_intellect_ablations` (80 chunks) vs `halo_agent_optimizer` (14 chunks) — різниця в 6x.
3. **Domain filtering** — `document_type` та `domain` можуть бути використані для precision filtering на HW2/HW3.