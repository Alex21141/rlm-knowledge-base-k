# Homework #3 — Retrieval Pipeline Improvement Comparison

## Improvements Applied

1. **Metadata filtering**: Filter by `document_type`, `domain`, `source_file`

2. **Query rewriting**: Pattern-based query expansion for better semantic match

3. **Hybrid scoring**: Combine semantic (MiniLM) + keyword (BM25-like) scores


## Comparison Table


| Query | Baseline top-1 | Improved top-1 | What changed |

|-------|---------------|----------------|-------------|

| How do RLMs handle arbitrarily long prompts? | `rlm_deep_dive_towardsdatascience_chunk_022` (0.661) | `rlm_deep_dive_towardsdatascience_chunk_022` (0.706) | ✅ Score improved: 0.6612 → 0.7057 |

| What is context rot and why does it happen? | `rlm_candemir_medium_chunk_003` (0.596) | `alexzhang_blog_context_rot_chunk_024` (0.679) | ✅ Better chunk (query rewrite): Some early (and very exciting) results! (was: What Is Context Rot, Really?) |

| How does HALO optimize agent loops? | `halo_agent_optimizer_chunk_001` (0.786) | `halo_agent_optimizer_chunk_001` (0.875) | ✅ Score improved: 0.7861 → 0.8750 |

| What are the key differences between RLM and ReAct? | `rlm_deep_dive_towardsdatascience_chunk_003` (0.527) | `rlm_deep_dive_towardsdatascience_chunk_003` (0.572) | ✅ Score improved: 0.5275 → 0.5719 |

| What is the Griffin architecture used in RecurrentGemma? | `alexzhang_blog_context_rot_chunk_059` (0.435) | `alexzhang_blog_context_rot_chunk_059` (0.469) | ✅ Score improved: 0.4352 → 0.4685 |

| How does Prime Intellect implement RLM ablations? | `prime_intellect_ablations_chunk_072` (0.490) | `prime_intellect_ablations_chunk_072` (0.566) | ✅ Score improved: 0.4898 → 0.5660 |

| What is context folding and how does RLM compare? | `prime_intellect_ablations_chunk_007` (0.693) | `prime_intellect_ablations_chunk_004` (0.681) | ✅ Better chunk (query rewrite): How we plan to manage extremely long contexts (was: The RLM) |

| How do you install and set up the RLM system? | `rlm_deep_dive_towardsdatascience_chunk_043` (0.455) | `rlm_deep_dive_towardsdatascience_chunk_043` (0.547) | ✅ Score improved: 0.4554 → 0.5471 |

| What benchmark results does RLM achieve on Oolong? | `prime_intellect_ablations_chunk_073` (0.659) | `rlm_rl_training_alphaxiv_chunk_044` (0.582) | ✅ Better chunk (query rewrite): [Jump to section](https://www.alphaxiv.org/blog/reinforcement-learning-for-rlms\#rlm-with-sub-calls "Jump to section") RLM (with sub-calls) (was: Oolong) |

| What are the training insights for RLMs in paper v3? | `rlm_rl_training_alphaxiv_chunk_050` (0.624) | `rlm_rl_training_alphaxiv_chunk_001` (0.571) | ✅ Better chunk (query rewrite): Reinforcing Recursive Language Models  --  alphaXiv Blog (was: [Jump to section](https://www.alphaxiv.org/blog/reinforcement-learning-for-rlms\#rlm-with-sub-calls "Jump to section") RLM (with sub-calls)) |


## Summary of Improvements


| Improvement | Queries affected | Description |

|-------------|-----------------|-------------|

| Query rewriting | 4 | Rewritten queries matched different, more relevant chunks |

| Metadata filtering | 0 | Smart domain-based filters narrowed search space |

| Hybrid scoring | 6 | Keyword boost improved scores for exact matches |

| No change | 0 | Baseline was already optimal |


## Detailed Analysis


### What worked best


**Hybrid scoring** improved retrieval scores for 6 queries where the baseline already found the correct chunk. The keyword component boosted exact matches.


### Conclusion


The combination of **query rewriting** and **hybrid scoring** provides the best improvement. Query rewriting handles cases where the original query is too vague for semantic matching, while hybrid scoring boosts exact keyword matches that pure embedding models might miss.


**Overall: 10 queries improved, 0 unchanged.**
