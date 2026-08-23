# Running Small Language Models Locally

## Why Small Models?

This project deliberately uses models around or below 0.5 billion parameters, such as SmolLM 360M, Qwen2 0.5B, or a similarly compact TinyLlama checkpoint. They are large enough to demonstrate tokenization, prompting, fine-tuning, decoding, and model–solver integration, but small enough to run on an ordinary laptop with less than 16 GB of RAM.

The model weights are only part of memory use. A rough weight-memory calculation is:

`number of parameters × bytes per parameter`

A 360M-parameter model needs about 1.44 GB in FP32, 0.72 GB in FP16, 0.36 GB in INT8, and roughly 0.18–0.25 GB in practical 4-bit formats. A 500M model needs about 2.0 GB in FP32 or 1.0 GB in FP16. Runtime also needs memory for activations, the key-value cache, tokenizer data, temporary buffers, and Python itself. Training adds gradients and optimizer states, often several times the weight memory.

## Precision and Quantization

**FP32** offers wide numerical range and maximum compatibility, but uses four bytes per weight. **FP16** or **BF16** uses two bytes and is often faster on supported GPUs. **INT8** stores weights in one byte and dequantizes during computation; it reduces RAM but can add CPU overhead. Four-bit quantization compresses further, although quality and kernel support must be tested rather than assumed.

Quantization is not automatically better. On some CPUs, an optimized INT8 or 4-bit runtime is much faster; on others, unsupported operations cause slow fallback paths. Measure both latency and Wordle win rate after changing precision.

## CPU and GPU Inference

CPU inference is the universal baseline. Small models can produce usable interactive output locally, but tokens per second depend heavily on architecture, quantization, thread count, memory bandwidth, context length, and decoding strategy. Do not copy a speed number from another machine and treat it as yours. Record model loading time, prompt-processing time, generated tokens, and generation time, then compute tokens per second.

A local GPU can improve throughput if the model and runtime fit in video memory, but it is optional. Integrated GPUs and platform-specific accelerators may also help. Always preserve a CPU path so the experiment remains reproducible on common hardware.

## Local-Only Reproducibility

After downloading an openly available checkpoint once, run experiments without API calls or paid services. Pin package versions, record the exact checkpoint revision and quantization, cache model files locally, and save configuration files alongside results. Set random seeds for Python, NumPy, and the model framework where applicable. Avoid silently switching model revisions between experiments.

Local execution improves privacy and removes network variability, but it does not guarantee reproducibility. Thread scheduling, numerical kernels, hardware, and sampling can still differ. Document operating system, processor, RAM, accelerator, library versions, and thread settings.

## Measuring Local Cost

For each benchmark, collect:

- wall-clock seconds per game and per generated token;
- peak resident memory (RAM) and, if used, peak GPU memory;
- total generated tokens and model calls;
- CPU-hours: elapsed hours multiplied by average utilized CPU cores;
- energy only if your operating system exposes a reliable measurement.

Run a warm-up before timing so model loading and kernel initialization do not distort steady-state measurements. Separate one-time load cost from repeated game cost. Tools such as `/usr/bin/time -v`, Python's `time.perf_counter`, framework memory counters, and OS process monitors are sufficient.

## The Engineering Tradeoff

A larger model may improve guess quality but increase latency and RAM. More sampled candidates may raise win rate but multiply decoding cost. Quantization may make a model fit while slightly changing rankings. Plot win rate against seconds per game and peak RAM instead of declaring one configuration universally best. The goal is a strong **local system**, not the largest model you can download.
