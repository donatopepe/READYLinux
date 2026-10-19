# AI model and hardware selection (MVP policy)

Last reviewed: 2026-10-18. This is a maintenance policy and a conservative, capacity-based estimate, not a live market survey. No web research was performed in this firing: no browser/search tool is available in the session and repository instructions prohibit starting network/downloads. Do not treat SKU prices, stock or benchmark rankings as current.

## Current prototype facts

- README's opt-in installer selects `Qwen2.5-Coder-1.5B-Instruct Q4_K_M`, approximately 1.12 GB GGUF.
- `setup-ai-cpu.sh` clones llama.cpp and downloads that file only when explicitly run; it checks a pinned SHA-256 before moving the model to its final name.
- Actual model download, runtime inference, throughput, RAM peak and output quality are not verified by the present automated suite. Current AI tests use an HTTP mock.
- READY can run without the model; the AI backend is optional. Generation/proposal, review/approval and explicit execution remain distinct.

## Capacity-based shopping guidance

Use these as provisional tiers for the current small CPU model, not universal minimum requirements:

| Profile | Provisional target | Notes |
|---|---|---|
| Console/BASIC only | Supported x86-64 Linux, 4 GB RAM | No GGUF required |
| Short CPU-AI trials | Recent 4+ core CPU, 16 GB RAM, SSD with 10+ GB free | Limited context; response latency is hardware-dependent |
| More comfortable CPU-AI use | Modern 6–8 core CPU, 32 GB RAM, 256+ GB SSD | More context/multitasking headroom; not a measured performance promise |
| Larger models/long context | Reassess memory and GPU only after selecting/benchmarking a model | No current tested recommendation |

No brand, product SKU, price, GPU or retailer recommendation is made here. Before purchase, check live manufacturer specifications, independent benchmarks for the exact quantization/runtime, Linux driver support, RAM upgradeability, noise, power, warranty and local prices. Never infer suitable RAM from GGUF file size alone: runtime plus context need additional memory.

## Requirements before calling a model selectable/recommended

For each catalog entry record: exact model/repository and immutable revision, quantization, license/redistribution terms, artifact size and verified digest, runtime compatibility, expected RAM for specified context, CPU/GPU requirements, source URL, research date, supported download method, offline import option, and rollback/removal instructions. Default selection remains opt-in; never auto-download merely by launching READY. Validate model files before activation and preserve existing verified models on failed download/checksum.

## Validation plan (not yet performed)

1. Add a model catalog/schema test using local fixtures only; no network.
2. Test selection, unavailable model, invalid digest, interrupted staging and safe activation/rollback with a temporary directory and fake HTTP server.
3. On a consenting Linux host, explicitly provision the pinned model, verify digest and capture llama.cpp revision/build flags.
4. Benchmark prompts of fixed tokens/context with warm-up and repeat runs; record tokens/s, time-to-first-token, peak RSS, CPU and temperatures. Keep mock tests separate from real inference results.
5. Refresh purchase guidance only from dated sources and test results; note region/date and avoid unsupported price claims.
