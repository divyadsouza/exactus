# Exactus: Data-Accurate Structured Output Model

## Overview

**Exactus** is a specialized language model designed to generate precise, structured outputs without hallucinations. The project focuses on training, fine-tuning, and distilling models that prioritize factual accuracy, exact formatting, and efficient inference—particularly on CPU environments.

## The Problem

Modern large language models (LLMs) are powerful but often unreliable for production data tasks:

- **Hallucinations**: Models frequently generate plausible-sounding but fabricated information
- **Inconsistent Structure**: Output formats vary unpredictably, breaking downstream pipelines
- **Resource Heavy**: Many models require expensive GPU infrastructure for inference
- **Over-Creative**: Models add interpretations or embellishments not present in source data

For applications requiring **exact data extraction**, **faithful summarization**, and **structured output generation**, these issues are deal-breakers.

## The Solution

Exactus addresses these challenges by developing a model that:

1. **Never fabricates** — Only outputs information explicitly present in the input
2. **Follows structure precisely** — Adheres to user-specified schemas or generates intelligent defaults
3. **Runs efficiently** — Optimized for CPU inference without GPU dependency
4. **Stays small and fast** — Distilled from larger reasoning models while preserving accuracy

## Baseline Reference Model

Exactus draws inspiration from and will be validated against [**NuExtract**](https://huggingface.co/numind/NuExtract) by NuMind—a state-of-the-art structured extraction model that closely aligns with our project objectives.

### Why NuExtract as Baseline?

| Alignment Area | NuExtract Feature | Exactus Relevance |
|----------------|-------------------|-------------------|
| **Pure Extraction** | Model outputs only text present in the source document | Matches our zero-hallucination requirement |
| **Schema-Driven** | Uses JSON templates to define extraction structure | Aligns with our structured output objective |
| **Compact Size** | Available in 0.5B (tiny), 4B, and 7B variants | Validates small model viability |
| **Fine-Tuned Focus** | Specialized fine-tuning on synthetic extraction data | Supports our fine-tuning approach |

### NuExtract Model Family

| Version | Base Model | Parameters | Key Features |
|---------|------------|------------|---------------|
| [NuExtract](https://huggingface.co/numind/NuExtract) | Phi-3-mini-4k-instruct | 4B | Original version, JSON extraction |
| [NuExtract-v1.5](https://huggingface.co/numind/NuExtract-v1.5) | Phi-3.5-mini-instruct | 4B | Multilingual, long document support (10-20k tokens) |
| [NuExtract-2.0](https://huggingface.co/numind/NuExtract-2.0-4B) | Qwen2.5-VL family | 2B/4B/8B | Multimodal (text + images), typed schemas |
| [NuExtract-tiny](https://huggingface.co/numind/NuExtract-tiny-v1.5) | Qwen2.5-0.5B | 0.5B | Ultra-compact for resource-constrained environments |

### Key Takeaways for Exactus

1. **Extraction-First Training**: NuExtract demonstrates that fine-tuning on high-quality synthetic extraction data produces models that avoid hallucination
2. **Template-Based Prompting**: JSON schema templates effectively guide structured output generation
3. **Size vs. Accuracy Trade-off**: The tiny (0.5B) to large (7B) variants show that smaller models can achieve extraction accuracy
4. **Temperature Matters**: NuExtract recommends temperature ≈ 0 for extraction—creativity is the enemy of accuracy

> 📖 **Reference**: Exactus will benchmark against NuExtract to validate our training approach and measure improvement in areas like additional output formats (CSV, XML, YAML), CPU optimization, and adaptive structuring.

---

## Core Objectives

### Output Requirements

| Requirement | Description |
|-------------|-------------|
| **Exact Summary Generation** | Faithful reproduction of source information—no additions, no omissions |
| **Zero Hallucinations** | Never generate facts, data, or information not explicitly present in the input |
| **Structured Data Output** | Support for JSON, CSV, XML, YAML with proper syntax and schema adherence |
| **Adaptive Structuring** | Follow user-specified schemas exactly, or generate intelligent structures when not specified |

### Performance Requirements

| Requirement | Description |
|-------------|-------------|
| **Small Model Size** | Compact footprint optimized for efficient deployment |
| **Fast Inference** | Low-latency generation suitable for production workloads |
| **CPU-First Design** | Full functionality without GPU; GPU acceleration optional |
| **Resource-Efficient** | Minimal memory and compute requirements |

## Project Structure

```
project/
├── data/
│   ├── training/          # Training datasets
│   ├── validation/        # Validation datasets
│   └── test/             # Test datasets
├── models/
│   ├── parent_model/     # Original reasoning model
│   ├── distilled/        # Distilled model versions
│   └── fine_tuned/       # Fine-tuned model versions
├── training/
│   ├── distillation/     # Distillation scripts
│   ├── fine_tuning/     # Fine-tuning scripts
│   └── data_prep/       # Dataset preparation
├── evaluation/
│   ├── hallucination/    # Hallucination detection tests
│   ├── structure/        # Format compliance tests
│   └── accuracy/         # Content accuracy tests
├── inference/
│   └── deployment/       # Deployment scripts and configs
└── docs/
    └── specifications/   # Detailed model specs
```

## Training Approach

Exactus can be created through two primary paths, depending on requirements:

### Path A: Model Distillation
Distill from a larger parent reasoning model to create a smaller, efficient version:
- Transfer factual accuracy capabilities from teacher to student model
- Preserve structural output understanding while reducing parameters
- Optimize for CPU inference from the start

### Path B: Fine-Tuning
Fine-tune an existing small model on curated datasets:
- **Dataset Curation**: Clean, factual data with clear source attribution
- **Loss Functions**: Specialized objectives for hallucination prevention
- **Format Training**: Explicit training on structured output generation
- **Constraint Learning**: Teach model to recognize and respect output boundaries

### Key Training Techniques (Both Paths)
- **Constrained Decoding**: Limit generation to source-only information
- **Format Enforcement**: Explicit format token training
- **Schema Adherence**: Training with JSON Schema, XML DTD, etc.
- **Uncertainty Calibration**: Teach model to recognize knowledge boundaries

## Evaluation Metrics

### Accuracy Metrics
- **Factual Fidelity**: Percentage of output facts present in source
- **Hallucination Rate**: Count of unsourced information
- **Omission Rate**: Important information missed from source

### Structure Metrics
- **Format Compliance**: Syntax correctness for each output format
- **Schema Adherence**: Compliance with user-specified schemas
- **Consistency**: Uniform structure when no schema provided

### Performance Metrics
- **Inference Speed**: Tokens/second on CPU
- **Memory Usage**: RAM consumption during inference
- **Model Size**: Disk footprint

## Usage Examples

### Explicit Structure Request
```
Input: "Summarize the following product specifications as JSON with 'name', 'price', and 'features' array: [spec text]"
Output: {
  "name": "Exact product name from spec",
  "price": "Exact price from spec",
  "features": ["Feature 1 from spec", "Feature 2 from spec"]
}
```

### Intelligent Structure Generation
```
Input: "Summarize this meeting transcript"
Output: {
  "participants": ["Name1", "Name2"],
  "date": "Date from transcript",
  "key_decisions": ["Decision 1", "Decision 2"],
  "action_items": [
    {"task": "Task from transcript", "assignee": "Name from transcript"}
  ]
}
```

## Deployment Requirements

### Hardware
- CPU-only operation
- Minimum 4GB RAM (recommended 8GB+)
- Multi-core support for faster inference

### Software Dependencies
- PyTorch/TensorFlow with CPU optimizations
- ONNX Runtime for potential optimization
- Format libraries (json, xml, csv, yaml parsers)

## Development Roadmap

### Phase 1: Data Foundation
- [ ] Curate hallucination-free training data with source attribution
- [ ] Create diverse structured output examples (JSON, CSV, XML, YAML)
- [ ] Develop data augmentation pipelines for format variations
- [ ] Build validation datasets for accuracy testing

### Phase 2: Model Training
- [ ] Evaluate NuExtract variants as potential base/reference models
- [ ] Select base models for distillation/fine-tuning (e.g., Phi-3.5, Qwen2.5)
- [ ] Implement constrained training with anti-hallucination objectives
- [ ] Develop format-specific output modules (extend beyond JSON to CSV, XML, YAML)
- [ ] Train initial Exactus model versions

### Phase 3: Validation & Benchmarking
- [ ] Create comprehensive hallucination detection test suite
- [ ] Develop format compliance and schema adherence tests
- [ ] Benchmark Exactus against NuExtract (accuracy, speed, size)
- [ ] Compare performance on NuExtract's published benchmarks
- [ ] Conduct adversarial testing for edge cases

### Phase 4: Optimization & Deployment
- [ ] Apply model quantization for CPU efficiency
- [ ] Optimize inference speed (target: production-ready latency)
- [ ] Reduce memory footprint for resource-constrained environments
- [ ] Package for easy deployment and integration

## Getting Started

> 🚧 **Project Status**: Exactus is currently in the planning and data preparation phase. Code and pre-trained models are not yet available.

### Prerequisites (Planned)
- Python 3.11+
- PyTorch with CPU optimizations
- 4GB+ RAM (8GB+ recommended)

### Installation (Coming Soon)
```bash
# Clone the repository
git clone https://github.com/mlim-usfca/exactus.git
cd exactus

# Install dependencies
pip install -r requirements.txt
```

### Quick Start (Coming Soon)
```python
from exactus import ExactusModel

model = ExactusModel.load("exactus-base")
result = model.extract(
    source="Your source text here...",
    format="json",
    schema={"name": str, "value": float}
)
```

## Contributing

We welcome contributions to Exactus!

### Data Contributions
- Provide clean, factual text with clear source attribution
- Include varied structured output examples across formats
- Add edge cases for hallucination testing

### Code Contributions
- Optimization techniques for CPU inference
- New format support modules
- Improved constraint enforcement methods
- Evaluation and benchmarking tools

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> **Philosophy**: Exactus prioritizes **accuracy over creativity**. It is designed to be a reliable, factual data extraction and structuring tool—not a creative writing assistant. When in doubt, Exactus omits rather than invents.