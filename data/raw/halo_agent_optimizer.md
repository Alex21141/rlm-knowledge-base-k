# HALO: Hierarchical Agent Loop Optimizer

**Source:** https://github.com/context-labs/halo
**PyPI:** https://pypi.org/project/halo-engine/
**Tagline:** RLM-based agent optimizer using production traces

## Benchmarks

### AppWorld

HALO was applied to the AppWorld benchmark, a set of agentic tasks that assess the LLM's ability to use multi-app services like Spotify, Venmo, file systems, and phone contacts. We tested HALO's ability to improve harnesses for both Gemini 3 Flash and Sonnet 4.6. We iterated on the harness using the `dev` split, and then used the `test_normal` split as a proxy to verify that improvements did not come from overfitting.
The feedback from HALO Engine surfaced failures in the harnesses such as hallucinated tool calls, redundant arguments in tools, refusal loops, and semantic correctness issues. Each issue mapped cleanly to a direct prompt edit. HALO's claims were independently verified from the source trace files with the findings holding up under scrutiny.
**Results:**
| Model | Split | Baseline SGC | Peak SGC after HALO | Improvement |
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
