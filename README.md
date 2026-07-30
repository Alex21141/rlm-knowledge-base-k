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
| 1 | How do RLMs handle arbitrarily long prompts? | simple | Відповідь з цитатами |
| 2 | What causes context rot in language models? | rephrased | Знайде context rot контекст |
| 3 | What is the difference between RLM and standard LLM? | simple | Порівняльна відповідь |
| 4 | How does HALO optimize agent loops using RLMs? | simple | Tool-specific відповідь |
| 5 | How does RLM compare to context folding? | simple | Порівняння |
| 6 | How does RL fine-tuning improve RLM behavior? | simple | RL training відповідь |
| 7 | What is the stock price of Apple Inc in 2025? | insufficient | Fallback — не знаю |
| 8 | How much does the RLM system cost in production? | insufficient | Fallback / partial |
| 9 | What are the key ablation results for RLM? | simple | Експериментальні результати |
| 10 | Who invented the internet? | insufficient | Fallback — не знаю |

---

## 5. Результати (real LLM output)

| Q# | Питання | Тип | Результат |
|----|---------|-----|----------|
| 1 | Long prompts | simple | ✅ PASS — цитати [rlm_original_paper_chunk_009] тощо |
| 2 | Context rot | rephrased | ✅ PASS — знайшло релевантний контекст |
| 3 | RLM vs standard | simple | ✅ PASS — порівняльна відповідь з цитатами |
| 4 | HALO agent loops | simple | ✅ PASS — детальна відповідь з HALO chunk |
| 5 | RLM vs context folding | simple | ✅ PASS — цитати з prime_intellect |
| 6 | RL fine-tuning | simple | ✅ PASS — цитати з rlm_rl_training_alphaxiv |
| 7 | Apple stock price | insufficient | ✅ PASS — fallback "не маю інформації" |
| 8 | Production cost | insufficient | ⚠️ WARN — часткова відповідь (знайшла benchmark cost) |
| 9 | Ablation results | simple | ✅ PASS — цитати з prime_intellect_ablations |
| 10 | Who invented internet | insufficient | ✅ PASS — fallback "не маю інформації" |

**Stats:**

| Метрика | Значення |
|---------|----------|
| Total questions | 10 |
| PASS | 9 (90%) |
| WARN | 1 (10%) |
| Fallback triggered (insufficient) | 2/3 ✅ |
| Citations in answers | 7/7 simple queries ✅ |

---

## 6. Prompt improvements

### V1 → V2: Added grounding rules

**V1 (basic):** "Answer the question using the context below."
- **Проблема:** Модель додавала загальні знання, не згадувала джерела

**V2 (grounded):** Додано правила "ONLY use context" + fallback phrase
- **Результат:** Модель почала дотримуватися grounding, але не цитувала chunk IDs

### V2 → V3: Added citation requirement

**V3 (final):** Додано "Cite every factual claim: [chunk_id]"
- **Результат:** 90% PASS, цитати [chunk_id] у кожній відповіді, fallback працює для 2/3 insufficient

### V3 lesson: Production cost question (Q8)

**Проблема:** Для питання про вартість production model знайшла частково релевантний chunk і дала часткову відповідь замість fallback.
- **Лекція:** Context може містити частково релевантну інформацію — модель повинна розрізняти "повна відповідь" vs "часткові дані"

---

## 7. Висновок

### ✅ Що вийшло добре

1. **90% pass rate** — 9/10 питань оброблено коректно
2. **Citations working** — модель цитує chunk IDs у форматі [chunk_id]
3. **Fallback working** — 2/3 out-of-scope питань отримали правильний fallback
4. **Grounded answers** — відповіді базуються на retrieved context, не на загальних знаннях

### ⚠️ Обмеження

1. **Partial relevance** — Q8 (production cost) знайшла частково релевантний chunk і дала відповідь замість fallback
2. **No evaluation metrics** — немає автоматичної оцінки quality (Rouge/BERTScore)
3. **Single LLM** — тестування тільки на qwen36-27b-awq, не порівняно з іншими моделями
