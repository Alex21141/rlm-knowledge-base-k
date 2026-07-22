# Recursive Language Models — Paper Updates (May 2026)

**Source:** arXiv:2512.24601v3 (May 11, 2026)  
**Authors:** Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)  
**Code:** https://github.com/alexzhang13/rlm

## Paper Evolution

The Recursive Language Models paper has evolved through three versions:
- **v1:** December 31, 2025 (7,933 KB)
- **v2:** January 28, 2026 (7,976 KB)
- **v3:** May 11, 2026 (10,181 KB)

The v3 update significantly expands the paper by approximately 2.2 MB, suggesting substantial new experimental results, additional benchmarks, or expanded theoretical analysis.

## Core Claims (Reinforced in v3)

RLMs can successfully process inputs up to two orders of magnitude beyond model context windows. Even for shorter prompts, RLMs dramatically outperform vanilla frontier LLMs and common long-context and coding scaffolds:
- **26%** improvement over compaction agents (median across benchmarks)
- **130%** improvement over CodeAct with sub-calls
- **13%** improvement over Claude Code

All while maintaining comparable or cheaper cost per query.

## RLM-Qwen3-8B Fine-tuning

At a small scale, researchers post-trained the first model natively around the RLM paradigm. RLM-Qwen3-8B:
- Outperforms the underlying Qwen3-8B model by **28.3%** on average
- Approaches the quality of vanilla GPT-5 on three long-context tasks
- Was trained on 1,000 filtered trajectories of Qwen3-Coder-480B-A35B as an RLM with Qwen3-8B sub-calls on LongBenchPro tasks

## Key Insight for Training

Being an effective sub-call model is roughly similar to being a general purpose reasoning model. Training can be made much more tractable at small scale by focusing on improving the root model's ability to:
1. Manipulate the REPL environment
2. Launch recursive calls appropriately
3. Parse and aggregate sub-call results
4. Know when to stop recursing and provide a final answer

## The RLM as a Language Model Replacement

RLMs replace the canonical `llm.completion(prompt, model)` call with a `rlm.completion(prompt, model)` call. They act as a "language model" from the user's perspective, but under the hood they offload the context as a variable in a REPL environment that the LM can interact with and launch sub-LM calls inside of.

This is a bet on future "language model" design choices. The authors argue for a CodeAct-style harness (all language models should have access to a code environment) with sub-(R)LM calls as functions in code, and context/prompts as objects in code. They want to move away from the JSON tool-calling standard for both sub-agents and generic tool calls.

## Training Environment

The repository now includes a verifiers training environment based on Prime Intellect's `prime-rl` in the `training/` folder. Users can train their own RLMs, which directly plug into the inference engine.

The training harness uses subprocess-isolated local REPL execution (no cloud sandboxes for simplicity), matching the `local` environment above. An ideal setup would use sandboxes for safety.

## Citation

```
@misc{zhang2026recursivelanguagemodels,
      title={Recursive Language Models},
      author={Alex L. Zhang and Tim Kraska and Omar Khattab},
      year={2026},
      eprint={2512.24601},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2512.24601},
}
```
