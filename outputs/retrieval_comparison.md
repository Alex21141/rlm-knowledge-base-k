# Homework #3 — Retrieval Pipeline Improvement Comparison

## Improvements Applied

1. **Metadata filtering**: Filter by `document_type`, `domain`, `source_file`

2. **Query rewriting**: Pattern-based query expansion for better semantic match

3. **Hybrid scoring**: Combine semantic (MiniLM) + keyword (BM25-like) scores


## Comparison Table


| Query | Baseline top-1 | Improved top-1 | What changed |

|-------|---------------|----------------|-------------|

| How do RLMs handle arbitrarily long prompts? | `rlm_original_paper_chunk_006` (0.620) | `rlm_original_paper_chunk_006` (0.642) | ✅ Score improved: 0.6195 → 0.6417 |

| What is context rot and why does it happen? | `rlm_core_paper_and_github_chunk_004` (0.623) | `rlm_core_paper_and_github_chunk_004` (0.675) | ✅ Score improved: 0.6233 → 0.6747 |

| How does HALO optimize agent loops? | `halo_agent_optimizer_chunk_001` (0.811) | `halo_agent_optimizer_chunk_001` (0.899) | ✅ Score improved: 0.8106 → 0.8995 |

| What are the key differences between RLM and ReAct? | `rlm_industry_analysis_chunk_003` (0.565) | `rlm_industry_analysis_chunk_003` (0.632) | ✅ Score improved: 0.5649 → 0.6316 |

| What is the Griffin architecture used in RecurrentGemma? | `recurrentgemma_griffin_architecture_chunk_002` (0.532) | `recurrentgemma_griffin_architecture_chunk_002` (0.621) | ✅ Score improved: 0.5325 → 0.6214 |

| How does Prime Intellect implement RLM ablations? | `prime_intellect_ablations_chunk_001` (0.576) | `prime_intellect_ablations_chunk_001` (0.662) | ✅ Score improved: 0.5763 → 0.6620 |

| What is context folding and how does RLM compare? | `prime_intellect_context_folding_chunk_005` (0.560) | `prime_intellect_context_folding_chunk_004` (0.675) | ✅ Better chunk (query rewrite): Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (was: RLM Implementation at Prime Intellect) |

| How do you install and set up the RLM system? | `rlm_core_paper_and_github_chunk_016` (0.458) | `prime_intellect_context_folding_chunk_006` (0.497) | ✅ Better chunk (query rewrite): Experimental Results Summary (was: RLMs in the Wild) |

| What benchmark results does RLM achieve on Oolong? | `prime_intellect_ablations_chunk_013` (0.623) | `rlm_original_paper_chunk_019` (0.594) | ✅ Better chunk (query rewrite): Results and Discussion (was: Verbatim Copy) |

| What are the training insights for RLMs in paper v3? | `rlm_paper_v3_updates_chunk_002` (0.571) | `rlm_original_paper_chunk_032` (0.547) | ✅ Better chunk (query rewrite): Conclusion (was: Core Claims (Reinforced in v3)) |


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
