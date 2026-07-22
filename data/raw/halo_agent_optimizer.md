# HALO: Hierarchical Agent Loop Optimizer

**Repository:** https://github.com/context-labs/halo  
**PyPI:** `halo-engine`  
**Tagline:** RLM-based agent optimizer using production traces

## What is HALO?

HALO is a methodology for building recursively self-improving agent harnesses using RLMs. This repository contains:

- The HALO Desktop App for running HALO locally on your machine
- Information on HALO methodology
- A Python package that implements the core HALO-RLM engine (View on PyPI)
- A demo project showing how to build HALO loops for your agents using the Python package
- Benchmarking examples applying HALO to popular agent benchmarks (View AppWorld)

## HALO Loop

The core HALO loop is surprisingly simple:

1. **Collect execution traces** from your agent harness. HALO uses OpenTelemetry-compatible tracing.
2. **Feed traces into HALO-RLM engine.**
3. **The engine decomposes the traces** to understand common failure modes across harness executions and produces a report with its findings.
4. **This report is fed into a coding agent** like Cursor or Claude Code to generate and apply a set of changes to your harness.
5. **The harness is then re-deployed**, more traces are gathered, and the cycle repeats.

HALO is great at finding issues in production agent deployments. We find high-traffic environments tend to generate more data with higher variance across executions, creating the type of issues that HALO is great at identifying.

## Why an RLM?

A general-purpose harness like Claude Code is the wrong tool for trace analysis. This isn't because the model isn't smart, but because traces can get extremely long, and you need a specialized toolkit in order to make observations about systemic agentic behavior. We noticed in our testing that harnesses like CC would often overfit to an error present in a single/few traces rather than generalize to harness-level problems. This led us to creating a specialized form of a RLM.

## HALO Engine Architecture

The HALO Engine implements bounded recursion, per-depth parallelism, and persistent context items.

### Key Components

- **RLM (Root LLM, depth=0):** The root agent that orchestrates the analysis.
- **Subagents (depth=1):** Parallel subagents that analyze specific trace subsets.
- **Grandchild Subagent (depth=2, terminal):** The deepest level of recursion, with no `call_subagent` tool available.
- **Per-depth semaphore:** Controls `max_parallel_subagents` (default 4).
- **Compaction model:** Summarizes context items to manage memory.
- **Context-item store:** Persistent storage for intermediate results.

### Available Tools for Root LM

The root LM has access to these tools:
- `get_dataset_overview`: Overview of the trace dataset
- `query_traces`: Query specific traces
- `count_traces`: Count traces matching criteria
- `view_trace`: View a single trace in detail
- `search_trace`: Search within a trace
- `get_context_item`: Retrieve a stored context item
- `synthesis`: Synthesize findings across traces
- `run_code` (sandboxed): Execute analysis code
- `call_subagent`: Launch a subagent for deeper analysis

### Subagent Tools

Tools are only usable by sub-LLMs, not the root RLM. This decision was made because many tools produce a lot of tokens. Now, the main RLM doesn't have to see those tokens, and can instead delegate the work that requires tools.

## Installation and Usage

Install the HALO engine + CLI from PyPI:

```
pip install halo-engine

# Verify installation
halo --help
```

### CLI Usage

```
export OPENAI_API_KEY=...
# Optional: point HALO at another OpenAI-compatible provider.
export OPENAI_BASE_URL=https://openrouter.ai/api/v1

halo path_to_your_traces.jsonl -p "Diagnose errors you find and suggest fixes"
```

HALO uses the canonical OpenAI env vars: `OPENAI_API_KEY` for credentials and `OPENAI_BASE_URL` for OpenAI-compatible providers. If `OPENAI_BASE_URL` is unset, HALO uses `https://api.openai.com/v1`.

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `TRACE_PATH` | required | JSONL trace file |
| `--prompt`, `-p` | required | User prompt sent to the root agent |
| `--model`, `-m` | `gpt-5.4-mini` | Model name for root and subagent calls |
| `--synthesis-model` | `--model` | Model for synthesis calls (trace summarization). A small, cheap model is recommended |
| `--compaction-model` | `--model` | Model for compaction calls (context summarization) — the biggest token consumer |
| `--max-depth` | `2` | Max subagent recursion depth |
| `--max-turns` | `20` | Max turns per agent |
| `--max-parallel` | `10` | Max concurrent subagents |
| `--base-url` | `OPENAI_BASE_URL` | OpenAI-compatible API base URL |
| `--api-key` | `OPENAI_API_KEY` | Provider API key |
| `--temperature` | provider default | Sampling temperature |
| `--max-output-tokens` | provider default | Maximum output tokens |
| `--parallel-tool-calls` | enabled | Allow models to issue parallel tool calls |
| `--refusal-retries` | `0` | Retry an agent model request when the model refuses |
| `--reasoning-effort` | model default | Reasoning effort for root and subagent calls |
| `--telemetry` | off | Emit OpenInference traces of HALO's own activity |

### Python API

The engine exposes four entry points from `engine.main`:

| Function | Sync/async | Returns | When to use |
|----------|-----------|---------|-------------|
| `stream_engine_async` | async | `AsyncIterator[AgentOutputItem | AgentTextDelta]` | Live UI, custom rendering |
| `stream_engine_output_async` | async | `AsyncIterator[AgentOutputItem]` | Log/persist each completed step |
| `run_engine_async` | async | `list[AgentOutputItem]` | Final list only |
| `stream_engine` | sync | `Iterator[AgentOutputItem | AgentTextDelta]` | Sync generator; yields every event |
| `stream_engine_output` | sync | `Iterator[AgentOutputItem]` | Sync generator; yields completed items |
| `run_engine` | sync | `list[AgentOutputItem]` | Sync, collects to a list |

```python
from engine.main import stream_engine_output_async

async for item in stream_engine_output_async(messages, cfg, trace_path):
    logger.info("step", extra={"sequence": item.sequence, "agent": item.agent_name})
```

## Benchmarks

### AppWorld

HALO was applied to the AppWorld benchmark, a set of agentic tasks that assess the LLM's ability to use multi-app services like Spotify, Venmo, file systems, and phone contacts. We tested HALO's ability to improve harnesses for both Gemini 3 Flash and Sonnet 4.6. We iterated on the harness using the `dev` split, and then used the `test_normal` split as a proxy to verify that improvements did not come from overfitting.

The feedback from HALO Engine surfaced failures in the harnesses such as hallucinated tool calls, redundant arguments in tools, refusal loops, and semantic correctness issues. Each issue mapped cleanly to a direct prompt edit. HALO's claims were independently verified from the source trace files with the findings holding up under scrutiny.

**Results:**

| Model | Split | Baseline SGC | Peak SGC after HALO | Improvement |
|-------|-------|-------------|---------------------|-------------|
| gemini-3-flash | dev | 36.8 | 52.6 | +15.8 |
| gemini-3-flash | test_normal | 37.5 | 48.2 | +10.7 |
| claude-sonnet-4.6 | dev | 73.7 | 89.5 | +15.8 |
| claude-sonnet-4.6 | test_normal | 62.5 | 73.2 | +10.7 |

## Telemetry

HALO can emit OpenInference-shaped traces of its own LLM, tool, and agent activity. It is off by default; nothing is emitted unless you pass `--telemetry`.

When telemetry is enabled, `CATALYST_OTLP_TOKEN` uploads spans to inference.net Catalyst over OTLP. If it is unset, spans are written to a local JSONL file at `./halo-telemetry-{run_id}.jsonl`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `CATALYST_OTLP_TOKEN` | unset | If set, uploads to Catalyst over OTLP |
| `CATALYST_OTLP_ENDPOINT` | catalyst-tracing default | OTLP endpoint base URL |
| `CATALYST_DEBUG` | unset | Set to `1` to surface OTLP export errors |
| `CATALYST_TRACING_RUN_ID` | unset | Uses this HALO run id instead of a generated uuid |
| `HALO_TELEMETRY_PATH` | `./halo-telemetry-{run_id}.jsonl` | Local fallback file path |
