# AI model and hardware selection (MVP policy)

Last reviewed: 2026-10-18. This is a maintenance policy and conservative capacity-based estimate, not live market research. No web research was performed in this firing: no browser/search tool is available in session tools and repository instructions prohibit initiating network/download activity. Prices, stock and product rankings are therefore not current or verified.

## Current prototype facts

- The opt-in setup script selects **Qwen2.5-Coder-1.5B-Instruct Q4_K_M**, about 1.12 GB GGUF.
- `setup-ai-cpu.sh` clones llama.cpp and downloads this model only when explicitly run; it checks a pinned SHA-256 before moving the file into its final name.
- Actual download/inference, RAM peak, throughput and output quality are not covered by the current automated suite. AI tests use a mocked HTTP server.
- READY works without a model. AI is optional. Generation/proposal, review/approval and explicit execution remain distinct.

## Capacity-based purchasing guidance

Provisional thresholds for the current small CPU model, not universal minimum requirements:

| Profile | Indicative configuration | Rationale/limit |
|---|---|---|
| Console without AI | Distro-supported x86-64, 4 GB RAM | BASIC/Python needs no GGUF; project storage separate |
| Short CPU-AI trials | Recent x86-64 CPU, 4+ cores, 16 GB RAM, SSD with 10+ GB free | Headroom for OS, model and short context; no latency guarantee |
| More comfortable CPU-AI | Modern 6–8 core CPU, 32 GB RAM, 256+ GB SSD | More context/multitasking headroom; no guaranteed scaling |
| Larger models/long context later | Reassess from 64 GB RAM; consider GPU only after benchmarking the selected model | Outside tested profile; no verified recommendation today |

Before buying, check current single-/multi-thread CPU benchmarks, upgradeable dual-channel RAM, storage, noise, power, Linux/driver support and warranty. No brand, SKU, price or retailer is recommended. Verify compatibility and returns with the seller. Update only with dated research and reproducible benchmarks. GGUF file size is not RAM demand: runtime and context need additional memory.

## Requirements for selectable model catalog

Record for each entry: exact model/repository and immutable revision, quantization, license/redistribution terms, size/verified digest, runtime compatibility, expected RAM for stated context, CPU/GPU requirements, source URL, research date, download method, offline import and rollback/removal steps. Selection must be opt-in: never download on startup. Validate artifacts before activation; preserve existing verified models if download/checksum fails.

## Validation plan (not performed)

1. Test a local catalog/schema with fixtures only; no network.
2. Test selection, unavailable model, wrong digest, interrupted staging and rollback in a temporary directory using a fake HTTP server.
3. On a consenting Linux host, explicitly provision the pinned model, verify digest and record llama.cpp revision/build flags.
4. Benchmark fixed prompts/tokens/context with warm-up/repeats; record tokens/s, time-to-first-token, peak RSS, CPU/temperature. Separate mock tests from real inference results.
5. Refresh purchase guidance only with dated sources and measurements; state region/date and avoid unsupported pricing claims.
