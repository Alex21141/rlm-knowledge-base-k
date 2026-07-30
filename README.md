# Домашнє завдання №4 — Генерація відповіді поверх retrieval

## 1. Опис проєкту

Будівництво QA pipeline: question → retrieval → prompt → LLM answer → grounded response with citations.

**Ціль:** модель відповідає тільки на основі retrieved context і чесно каже "не знаю" при недостатньому context.

---

## 2. Knowledge base

| Метрика | Значення |
|---------|----------|
| Документів | **10** |
| Чанків | **467** |
| Vectors | **467 × 384-dim** |

---

## 3. Prompt template (V3 — фінальний)

```
You are a research assistant specializing in Recursive Language Models (RLM), Retrieval-Augmented Generation (RAG), and LLM reasoning paradigms.

INSTRUCTIONS:
1. Answer the user question using ONLY the information in the provided context below.
2. If the context does not contain sufficient information, respond with: "I do not have enough information in the available documents to answer this question."
3. Do NOT use general knowledge or assumptions.
4. Cite every factual claim using the format: [chunk_id] (e.g., [rlm_original_paper_chunk_006]).
5. If multiple chunks support different parts, cite each separately.
6. Keep the answer concise and focused.

Context:
{retrieved_context}

Question:
{user_question}

Answer:
```

---

## 4. Тестові питання (10)

| # | Питання | Тип | Очікувана поведінка |
|---|---------|-----|---------------------|
| 1 | How do recursive language models handle prompts larger than their context window? | simple | Відповідь з цитатами |
| 2 | What is context rot and why does performance degrade with longer inputs? | simple | Відповідь з цитатами |
| 3 | How does the Python REPL environment work in RLM architecture? | simple | Відповідь з цитатами |
| 4 | What benchmark results does RLM achieve on BrowseComp-Plus and OOLONG? | simple | Відповідь з цитатами |
| 5 | What are the key differences between RLM and RAG for long-context processing? | simple | Відповідь з цитатами |
| 6 | What are the key ablation results for RLM with versus without sub-calling? | simple | Відповідь з цитатами |
| 7 | How does RL fine-tuning improve RLM behavior compared to prompting or SFT alone? | simple | Відповідь з цитатами |
| 8 | What is the stock price of Apple Inc in 2025? | insufficient | Fallback — не знаю |
| 9 | How much does the RLM system cost to run in production? | insufficient | Fallback — не знаю |
| 10 | Who invented the internet? | insufficient | Fallback — не знаю |

---

## 5. Результати (real LLM output)

| Q# | Питання | Тип | Результат |
|----|---------|-----|----------|
| 1 | RLM long prompts | simple | ✅ PASS — цитати present, grounded |
| 2 | Context rot | simple | ✅ PASS — цитати present, grounded |
| 3 | Python REPL | simple | ✅ PASS — цитати present, grounded |
| 4 | Benchmarks | simple | ✅ PASS — цитати present, grounded |
| 5 | RLM vs RAG | simple | ✅ PASS — цитати present, grounded |
| 6 | Ablation | simple | ✅ PASS — цитати present, grounded |
| 7 | RL fine-tuning | simple | ✅ PASS — цитати present, grounded |
| 8 | Apple stock | insufficient | ✅ PASS — fallback "не маю інформації" |
| 9 | Production cost | insufficient | ✅ PASS — fallback "не маю інформації" |
| 10 | Internet origin | insufficient | ✅ PASS — fallback "не маю інформації" |

**Stats:**

| Метрика | Значення |
|---------|----------|
| Total questions | 10 |
| PASS | 10 (100%) |
| WARN | 0 (0%) |
| Fallback triggered (insufficient) | 3/3 ✅ |
| Citations in simple answers | 7/7 ✅ |

---

## 6. Prompt improvements

### V1 → V2: Added grounding rules

**V1 (basic):** "Answer the question using the context below."
- **Проблема:** Модель додавала загальні знання, не згадувала джерела

**V2 (grounded):** Додано правила "ONLY use context" + fallback phrase
- **Результат:** Модель почала дотримуватися grounding, але не цитувала chunk IDs

### V2 → V3: Added citation requirement

**V3 (final):** Додано "Cite every factual claim: [chunk_id]"
- **Результат:** 100% PASS, цитати [chunk_id] у кожній відповіді, fallback працює для 3/3 insufficient

---

## 7. Висновок

### ✅ Що вийшло добре

1. **100% pass rate** — 10/10 питань оброблено коректно
2. **Citations working** — модель цитує chunk IDs у форматі [chunk_id] у всіх 7 simple-відповідях
3. **Fallback working** — 3/3 out-of-scope питань отримали правильний fallback (раніше було 2/3)
4. **Grounded answers** — відповіді базуються на retrieved context, не на загальних знаннях
5. **Q9 (production cost)** — тепер fallback працює! (раніше був WARN)

### ⚠️ Обмеження

1. **No evaluation metrics** — немає автоматичної оцінки quality (Rouge/BERTScore)
2. **Single LLM** — тестування тільки на qwen36-27b-awq, не порівняно з іншими моделями
3. **Top-k=3** — лише 3 чанки, більше context могло б покращити відповіді
