# Домашнє завдання №2 — Семантичний пошук

## 1. Опис проєкту

Семантичний пошук поверх бази знань з ДЗ №1. Використовуємо MiniLM embeddings + FAISS index для пошуку релевантних фрагментів.

**Ціль:** відповісти на 10 RLM-запитів через семантичний пошук.

---

## 2. База знань

| Метрика | Значення |
|---------|----------|
| Документів | **10** |
| Фрагментів (чанків) | **467** |
| Векторів в індексі | **467** |
| Embedding-модель | all-MiniLM-L6-v2 (384-вимірний) |
| FAISS-індекс | IndexFlatIP |
| CHUNK_SIZE | 600 |
| OVERLAP | 100 |

---

## 3. Процес пошуку

1. **Завантаження чанків** — читання `data/processed/chunks.jsonl` (467 чанків)
2. **Побудова/завантаження FAISS-індексу** — `index/faiss.index` + `index/metadata.json`
3. **Ембедінг запиту** — MiniLM → 384-вимірний вектор
4. **Пошук** — FAISS скалярний добуток, top-k=5
5. **Повернення результатів** — chunk_id, оцінка, передогляд тексту, метадані

---

## 4. Тестові запити (10)

| # | Запит | Категорія |
|---|-------|----------|
| 1 | How does the RLM REPL architecture process user prompts that exceed the base model's fixed context window? | Ключова концепція |
| 2 | What is context rot in recursive language models and how does it affect performance on long-context tasks? | Ключова концепція |
| 3 | How does the Python REPL environment function within the RLM agent architecture for recursive code execution? | Архітектура |
| 4 | How does RLM recursive reasoning compare to retrieval-augmented generation? | Порівняння |
| 5 | How does RLM performance scale on long-context tasks like S-NIAH compared to non-recursive base LLMs? | Бенчмарки |
| 6 | What are the architectural trade-offs between RLM recursive decomposition and retrieval-augmented generation for multi-hop reasoning? | Порівняння |
| 7 | How does the evolution from flat prompting to recursive execution relate to context management in language models? | Порівняння |
| 8 | What are the ablation results for RLM with and without sub-calling on information-dense tasks? | Експерименти |
| 9 | How does the HALO agent optimizer implement RLM-based recursive loops for tool use? | Інструменти |
| 10 | How does reinforcement learning fine-tuning improve RLM recursive behavior compared to supervised fine-tuning? | RL-тренування |

---

## 5. Результати

| № | Запит | Чанк (найкращий) | Оцінка | Документ |
|---|-------|-------------|--------|----------|
| 1 | RLM REPL архітектура | \`rlm_comprehensive_guide_chunk_026\` | 0.7659 | rlm_comprehensive_guide |
| 2 | Контекстна деградація | \`rlm_original_paper_chunk_004\` | 0.8503 | rlm_original_paper |
| 3 | Python REPL в RLM | \`rlm_rl_training_alphaxiv_chunk_005\` | 0.7492 | rlm_rl_training_alphaxiv |
| 4 | RLM vs RAG порівняння | \`rlm_candemir_medium_chunk_021\` | 0.6711 | rlm_candemir_medium |
| 5 | S-NIAH масштабування | \`llm_reasoning_paradigms_evolution_chunk_023\` | 0.7168 | llm_reasoning_paradigms_evolution |
| 6 | RLM vs RAG компроміси | \`llm_reasoning_paradigms_evolution_chunk_025\` | 0.6391 | llm_reasoning_paradigms_evolution |
| 7 | Плоске промптування → рекурсія | \`rlm_original_paper_chunk_004\` | 0.6691 | rlm_original_paper |
| 8 | Абляція (підвиклики) | \`prime_intellect_ablations_chunk_057\` | 0.5685 | prime_intellect_ablations |
| 9 | HALO оптимізатор | \`halo_agent_optimizer_chunk_001\` | 0.8091 | halo_agent_optimizer |
| 10 | RL-донавчання проти SFT | \`rlm_comprehensive_guide_chunk_018\` | 0.6229 | rlm_comprehensive_guide |

**Статистика:**

| Метрика | Значення |
|---------|----------|
| Середня оцінка | 0.7062 |
| Мінімальна | 0.5685 |
| Максимальна | 0.8503 |
| Запитів з оцінкою > 0.60 | 9/10 |

---

## 6. Висновок

### 📊 Детальний аналіз за запитами

| # | Запит | Оцінка | Документ | Вердикт | Коментар |
|---|-------|--------|----------|---------|----------|
| 1 | RLM REPL архітектура | 0.7659 | rlm_comprehensive_guide | ✅ Влучив | Перший чанк містить ключову інформацію про REPL-архітектуру |
| 2 | Контекстна деградація | 0.8503 | rlm_original_paper | ✅ Влучив | Найвища оцінка — семантичний збіг з оригінальною працею |
| 3 | Python REPL в RLM | 0.7492 | rlm_rl_training_alphaxiv | ✅ Влучив | Коректно знайшов секцію про REPL-середовище для виконання коду |
| 4 | RLM vs RAG порівняння | 0.6711 | rlm_candemir_medium | ✅ Влучив | Порівняльний запит — знайшов чанк про RLM vs RAG відмінність |
| 5 | S-NIAH масштабування | 0.7168 | llm_reasoning_paradigms_evolution | ✅ Влучив | Знайшов результати довгоконтекстних тестів, хоча й не в RLM-фокусному документі |
| 6 | RLM vs RAG компроміси | 0.6391 | llm_reasoning_paradigms_evolution | ⚠️ Пограничний | Оцінка <0.65 — семантична близькість зменшується для порівняльних запитів |
| 7 | Плоске промптування → рекурсія | 0.6691 | rlm_original_paper | ✅ Влучив | Коректно, але оцінка на межі — концептуальний запит |
| 8 | Абляція (підвиклики) | 0.5685 | prime_intellect_ablations | ❌ Низький | Найнижча оцінка — специфічний запит на результати абляції |
| 9 | HALO оптимізатор | 0.8091 | halo_agent_optimizer | ✅ Влучив | Друга найвища оцінка — точний документ-збіг |
| 10 | RL-донавчання проти SFT | 0.6229 | rlm_comprehensive_guide | ⚠️ Пограничний | Оцінка <0.65 — порівняльний запит між методами тонкого налаштування |

### 📈 Агреговані метрики

| Метрика | Значення |
|---------|----------|
| Середня оцінка | **0.7062** |
| Мінімальна | 0.5685 (Q8: абляція) |
| Максимальна | 0.8503 (Q2: контекстна деградація) |
| Запитів > 0.65 (сильні) | **7/10** |
| Запитів > 0.60 (прийнятні) | **9/10** |
| Запитів < 0.60 (слабкі) | **1/10** |

### ✅ Сильні сторони

1. **Концептуальні запити працюють чудово** — Q1 (0.77), Q2 (0.85), Q3 (0.75) отримали високі оцінки. MiniLM добре захоплює семантику RLM-концептів.
2. **Точне впізнавання сутностей** — Q9 (HALO, 0.81) та Q2 (контекстна деградація, 0.85) демонструють, що коли запит містить унікальну назву чи термін, пошук влучає точно.
3. **Міждокументне покриття** — перші результати розподілені по 8 унікальних документах (з 10 в базі), що свідчить про добре покриття.
4. **Документна релевантність** — 6/10 перших результатів з RLM-орієнтованих документів (rlm_original_paper, rlm_comprehensive_guide, rlm_rl_training_alphaxiv, rlm_candemir_medium).

### ⚠️ Де пошук слабший

1. **Абляційні/експериментальні запити** — Q8 (0.57) значно нижчий порогового 0.60. Абляція підвикликів — це вузький експериментальний результат, який погано семантично кодується MiniLM.
2. **Порівняльні запити** — Q6 (0.64) та Q10 (0.62) мають оцінки <0.65. Запити типу "X проти Y" втрачають семантичну специфічність.
3. **Запити про еволюцію концепцій** — Q7 (0.67) на межі. Запити про еволюцію парадигм складні для чистого семантичного пошуку.
4. **Закономірність:** низькі оцінки корелюють із запитами, що містять порівняння або вузькі експериментальні деталі.

### 🎯 Висновок

Семантичний пошук на MiniLM + FAISS показує стабільну базову продуктивність (середній показник 0.71, 9/10 >0.60). Найкраще працює для концептуальних запитів та запитів з унікальними термінами. Найслабші місця — порівняльні запити та вузькі експериментальні деталі. Ці обмеження є очікуваними для чистого семантичного пошуку.
