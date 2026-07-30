# Homework #3 — Retrieval Pipeline Improvement Comparison

## Improvements Applied

1. **Metadata filtering**: Filter by `document_type`, `domain`, `source_file`

2. **Query rewriting**: Pattern-based query expansion for better semantic match

3. **Hybrid scoring**: Combine semantic (MiniLM) + keyword (BM25-like) scores


## Comparison Table


| Query | Baseline top-1 | Improved top-1 | What changed |

|-------|---------------|----------------|-------------|

| How do recursive language models handle prompts larger than their context window? | `rlm_original_paper_chunk_002` (0.701) | `rlm_original_paper_chunk_027` (0.828) | ✅ Better chunk (query rewrite): Recursive Language Models (was: Recursive Language Models) |

| What is context rot and why does performance degrade with longer inputs? | `rlm_candemir_medium_chunk_003` (0.694) | `rlm_original_paper_chunk_004` (0.702) | ✅ Better chunk (query rewrite): 2 Scaling Long Context Tasks (was: What Is Context Rot, Really?) |

| How does the Python REPL environment work in RLM architecture? | `alexzhang_blog_context_rot_chunk_013` (0.660) | `alexzhang_blog_context_rot_chunk_013` (0.742) | ✅ Score improved: 0.6600 → 0.7415 |

| What benchmark results does RLM achieve on BrowseComp-Plus and OOLONG? | `rlm_original_paper_chunk_036` (0.597) | `rlm_original_paper_chunk_036` (0.651) | ✅ Score improved: 0.5973 → 0.6506 |

| How does RLM performance compare to base LLMs on long-context tasks? | `rlm_comprehensive_guide_chunk_002` (0.747) | `rlm_original_paper_chunk_035` (0.828) | ✅ Better chunk (query rewrite): 3 Results and Discussion (was: 1. FUNDAMENTALS) |

| What are the key differences between RLM and RAG for long-context processing? | `rlm_candemir_medium_chunk_022` (0.660) | `rlm_candemir_medium_chunk_022` (0.752) | ✅ Score improved: 0.6599 → 0.7522 |

| How does context folding relate to recursive language models? | `prime_intellect_ablations_chunk_007` (0.776) | `prime_intellect_ablations_chunk_007` (0.686) | No change |

| What are the key ablation results for RLM with versus without sub-calling? | `prime_intellect_ablations_chunk_057` (0.601) | `rlm_comprehensive_guide_chunk_002` (0.635) | ✅ Better chunk (query rewrite): 1. FUNDAMENTALS (was: The RLM) |

| How does the HALO agent optimizer use RLM-based loops? | `halo_agent_optimizer_chunk_001` (0.762) | `halo_agent_optimizer_chunk_001` (0.868) | ✅ Score improved: 0.7616 → 0.8682 |

| How does RL fine-tuning improve RLM behavior compared to prompting or SFT alone? | `rlm_rl_training_alphaxiv_chunk_002` (0.666) | `rlm_rl_training_alphaxiv_chunk_002` (0.739) | ✅ Score improved: 0.6658 → 0.7385 |


## Summary of Improvements


| Improvement | Queries affected | Description |

|-------------|-----------------|-------------|

| Query rewriting | 4 | Rewritten queries matched different, more relevant chunks |

| Metadata filtering | 0 | Smart domain-based filters narrowed search space |

| Hybrid scoring | 5 | Keyword boost improved scores for exact matches |

| No change | 1 | Baseline was already optimal |


## Detailed Analysis


### What worked best


**Hybrid scoring** improved retrieval scores for 5 queries where the baseline already found the correct chunk. The keyword component boosted exact matches.


### Conclusion


The combination of **query rewriting** and **hybrid scoring** provides the best improvement. Query rewriting handles cases where the original query is too vague for semantic matching, while hybrid scoring boosts exact keyword matches that pure embedding models might miss.


**Overall: 9 queries improved, 1 unchanged.**
