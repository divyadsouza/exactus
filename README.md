# Exactus: Data-Accurate Structured Output Model

## Overview

**Exactus** is a specialized language model designed to generate precise, structured outputs without hallucinations. The project focuses on training, fine-tuning, and distilling models that prioritize factual accuracy, exact formatting, and efficient inference—particularly on CPU environments.

For learning objectives, see [docs/learning_outcomes.md](docs/learning_outcomes.md). For key concepts, see [docs/key_concepts.md](docs/key_concepts.md). For a glossary of terms, see [docs/glossary.md](docs/glossary.md).

## Project Goals

The primary goal of Exactus is to create a high-quality language model optimized for structured output generation, designed to be served via standard inference servers such as Transformers, vLLM, Llama.cpp, and similar frameworks.

A secondary, future goal is to develop APIs for Exactus, including both server-type APIs (e.g., RESTful services) and client-based APIs for easier integration into applications. Key advantages of API development include:

1. **URL as source material**: Enable processing of web content directly via URLs
2. **File path as source material**: Support local file processing through file system paths  
3. **Memory / Cache**: Investigate adding memory or caching capabilities to the model or API for handling summaries or structural changes that reference the same source material(s)
4. **Scalability & Concurrency**: Handle multiple simultaneous requests, enabling parallel processing of large document batches
5. **Authentication & Security**: Built-in API keys, OAuth, and rate limiting to control access and prevent abuse
6. **Standardized Interface**: RESTful design provides consistent endpoints for different operations (extract, summarize, validate)
7. **Monitoring & Analytics**: Built-in logging, metrics, and error tracking for production deployment
8. **Batch Processing**: Accept multiple URLs/files in a single request for efficient bulk operations
9. **Streaming Responses**: Stream structured output as it's generated for large documents rather than waiting for completion
10. **Cross-Platform Integration**: Any programming language can call the API, enabling broader adoption
11. **Database Integration**: Connect to relational databases, NoSQL databases, and vector databases with schema/data dictionary definitions, enabling the AI to intelligently extract and structure data according to specified formats for RAG workflows and data transformation

**Example API Usage:**
```json
{
  "database": {
    "type": "mongodb",
    "connection": "mongodb://...",
    "collection": "products"
  },
  "schema": {
    "name": "string",
    "price": "number", 
    "features": ["string"],
    "category": "string"
  },
  "query": {"category": "electronics"},
  "output_format": "json"
}
```

## The Problem

Modern large language models (LLMs) are powerful but often unreliable for production data tasks:

- **Hallucinations**: Models frequently generate plausible-sounding but fabricated information
- **Inconsistent Structure**: Output formats vary unpredictably, breaking downstream pipelines
- **Resource Heavy**: Many models require expensive GPU infrastructure for inference
- **Slow Inference**: Large models have slow inference speeds, making them unsuitable for processing large volumes of data efficiently, especially on CPU or with limited GPU resources
- **Over-Creative**: Models add interpretations or embellishments not present in source data

For applications requiring **exact data extraction**, **faithful summarization**, **structured output generation**, and **efficient high-throughput processing**, these issues are deal-breakers.

## The Solution

Exactus addresses these challenges by developing a model that:

1. **Never fabricates** — Only outputs information explicitly present in the input
2. **Follows structure precisely** — Adheres to user-specified schemas or generates intelligent defaults
3. **Runs efficiently and fast** — Optimized for CPU inference without GPU dependency, delivering quick inference speeds for large data processing
4. **Stays small and fast** — Distilled from larger reasoning models while preserving accuracy

## Baseline Reference Model

Exactus draws inspiration from and will be validated against [**NuExtract-2.0**](https://huggingface.co/collections/numind/nuextract-20) by NuMind—a state-of-the-art structured extraction model that closely aligns with our project objectives.

### Why NuExtract as Baseline?

| Alignment Area | NuExtract Feature | Exactus Relevance |
|----------------|-------------------|-------------------|
| **Pure Extraction** | Model outputs only text present in the source document | Matches our zero-hallucination requirement |
| **Schema-Driven** | Uses JSON templates to define extraction structure | Aligns with our structured output objective |
| **Compact Size** | Available in 0.5B (tiny), 2B, 4B, and 8B variants | Validates small model viability |
| **Fine-Tuned Focus** | Specialized fine-tuning on synthetic extraction data | Supports our fine-tuning approach |

### NuExtract Model Family

| Version | Base Model | Parameters | Key Features |
|---------|------------|------------|---------------|
| [NuExtract](https://huggingface.co/numind/NuExtract) | Phi-3-mini-4k-instruct | 4B | Original version, JSON extraction |
| [NuExtract-v1.5](https://huggingface.co/numind/NuExtract-v1.5) | Phi-3.5-mini-instruct | 4B | Multilingual, long document support (10-20k tokens) |
| [NuExtract-2.0](https://huggingface.co/collections/numind/nuextract-20) | Qwen2.5-VL family | 2B/4B/8B (with GPTQ and GGUF variants) | Multimodal (text + images), typed schemas |
| [NuExtract-tiny](https://huggingface.co/numind/NuExtract-tiny-v1.5) | Qwen2.5-0.5B | 0.5B | Ultra-compact for resource-constrained environments |

### Key Takeaways for Exactus

1. **Extraction-First Training**: NuExtract demonstrates that fine-tuning on high-quality synthetic extraction data produces models that avoid hallucination
2. **Template-Based Prompting**: JSON schema templates effectively guide structured output generation
3. **Size vs. Accuracy Trade-off**: The tiny (0.5B) to large (8B) variants show that smaller models can achieve extraction accuracy
4. **Temperature Matters**: NuExtract recommends temperature ≈ 0 for extraction—creativity is the enemy of accuracy

> 📖 **Reference**: Exactus will benchmark against NuExtract-2.0 to validate our training approach and measure improvement in areas like additional output formats (CSV, XML, YAML), CPU optimization, and adaptive structuring.

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

**Note**: Some directories (e.g., `models/`, `validation/`, `test/`) are planned for future phases and not yet present in the current workspace.

## Training Data

The `data/training/` directory contains synthetic JSONL datasets designed to train models for accurate structured output generation. Each sample file represents different variations and complexity levels of extraction tasks.

### Dataset Files

| File | Description | Focus Areas |
|------|-------------|-------------|
| `training_data_sample1.jsonl` | Basic structured extraction examples | Simple JSON objects, arrays, nested structures for common domains like emails, vehicles, and recipes |
| `training_data_sample2.jsonl` | Multi-format extraction with varied domains | JSON and XML outputs across diverse scenarios: orders, flights, products, meetings, patient records, reviews, shipping policies, sensor readings, contracts, and product specifications |
| `training_data_sample3.jsonl` | Exact format specification with templates | Strict adherence to user-provided schemas, covering employee data, products, invoices, events, patient visits, configurations, orders, API responses, and property details |
| `training_data_sample4.jsonl` | Complex nested structures | Advanced JSON/XML with deep nesting: project management, restaurant menus, system monitoring, and scientific experiments |
| `training_data_sample5_edgecase.jsonl` | Edge cases with missing/null data | Handling scenarios where expected data is absent or null, such as successful operations (no errors), empty search results, and anonymous users with minimal information |

### Data Characteristics

- **Zero Hallucinations**: All outputs contain only information explicitly present in the input text
- **Format Variety**: Supports JSON, XML, and structured text outputs
- **Domain Diversity**: Covers business, healthcare, technology, scientific, and consumer domains
- **Complexity Progression**: Files build from basic to advanced extraction scenarios
- **Edge Case Coverage**: Includes handling of missing data, empty results, and null values
- **Schema Adherence**: Emphasizes exact matching to specified output formats and structures

### Open Datasets for Reference and Augmentation

For additional training, validation, and benchmarking data, refer to [docs/open_data_ref.md](docs/open_data_ref.md), which documents publicly available open-source datasets suitable for structured extraction tasks. These can supplement the synthetic data and provide real-world examples for testing against baselines like NuExtract.

In addition to these open datasets, we may need to generate additional synthetic datasets using AI tools to cover specific domains, edge cases, or to increase dataset diversity. These AI-generated datasets should be validated using the `training-data-validator` skill to ensure they maintain zero hallucinations and structural accuracy.

## AI Agents and Skills

For guidance on using AI coding assistants to help with project development, data validation, and creating new skills (including for synthetic dataset generation), see [docs/ai_agents_guide.md](docs/ai_agents_guide.md).

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

### Phase 0: Project Setup 🆕
> Foundational infrastructure before training begins

- [ ] **Set up development environment** — Create `requirements.txt`, `pyproject.toml`
- [ ] **Establish coding standards** — Configure linting, formatting, type hints
- [ ] **Set up CI/CD pipeline** — Automated testing on PRs
- [ ] **Configure experiment tracking** — MLflow, Weights & Biases, or similar
- [ ] **Generate AGENTS.md** — Use `agents-md-generator` skill
- [ ] **Create documentation structure** — Initial project docs setup

### Phase 1: Data Foundation
- [ ] **Curate hallucination-free training data** — Include source attribution for all examples
- [ ] **Create diverse structured output examples** — JSON, CSV, XML, YAML formats
- [ ] **Develop data augmentation pipelines** — Generate format variations programmatically
- [ ] **Build validation datasets** — Separate data for accuracy testing
- [ ] **Add negative examples dataset** — Train model to recognize when extraction isn't possible
- [ ] **Create cross-format consistency tests** — Same source → JSON/XML/CSV/YAML semantic equivalence
- [ ] **Build adversarial examples** — Deliberately misleading inputs to test hallucination resistance
- [ ] **Consider multilingual extraction samples** — Evaluate if Exactus needs multilingual support
- [ ] **Bootstrap data with open datasets** — Use datasets from `docs/open_data_ref.md` + `training-data-validator` to generate verified training data

### Phase 2: Model Training
- [ ] **Evaluate NuExtract variants** — Assess as potential base/reference models (different variants: 4B and 2B models)
- [ ] **Select base models** — Choose for distillation/fine-tuning (e.g., Phi-4-instruct, Qwen3-4B, Qwen3-2B, and Qwen3-0.6B)
- [ ] **Implement constrained training** — Anti-hallucination objectives
- [ ] **Develop format-specific output modules** — Extend beyond JSON to CSV, XML, YAML
- [ ] **Train initial Exactus model versions** — First training runs and evaluation
- [ ] **Define base model selection criteria** — Quantitative thresholds before fine-tuning proceeds
- [ ] **Specify anti-hallucination loss function** — Contrastive loss, constrained beam search, or custom objective
- [ ] **Evaluate LoRA/QLoRA fine-tuning** — Parameter-efficient training crucial for CPU deployment
- [ ] **Implement incremental training checkpoints** — Enable rollback and A/B testing
- [ ] **Design synthetic data generation loop** — Teacher-student self-improvement cycle

#### Base Model Candidates

| Model | Parameters | Pros | Cons |
|-------|------------|------|------|
| Qwen3-0.6B | 0.6B | Ultra-small, advanced reasoning with thinking mode, Apache 2.0 | May lack capacity for complex schemas |
| Qwen3-4B | 4B | Balanced size, strong reasoning and multilingual support, Apache 2.0 | Larger footprint |
| Phi-4-mini-instruct | 3.8B | Strong reasoning, especially math and logic, MIT license | Larger footprint |

### Phase 3: Validation & Benchmarking
- [ ] **Create hallucination detection test suite** — Comprehensive coverage of fabrication scenarios
- [ ] **Develop format compliance tests** — Schema adherence validation
- [ ] **Benchmark against NuExtract** — Compare accuracy, speed, size
- [ ] **Compare on published benchmarks** — Use NuExtract's evaluation datasets
- [ ] **Conduct adversarial testing** — Edge cases and stress tests
- [ ] **Define specific benchmark datasets** — SQuAD, NQ, TriviaQA extraction variants
- [ ] **Create hallucination scoring rubric** — Quantify fabrication, distortion, omission separately
- [ ] **Build regression test suite** — Automated tests on every training checkpoint
- [ ] **Add human evaluation component** — Sample-based review for nuanced hallucination detection
- [ ] **Create format edge case tests** — Malformed schemas, deep nesting, Unicode handling
- [ ] **Implement latency profiling** — Per-token timing on Intel, ARM, Apple Silicon

#### Expanded Evaluation Metrics

| Category | Metric | Description |
|----------|--------|-------------|
| Accuracy | Schema Coverage Score | % of schema fields correctly populated |
| Accuracy | Extraction Precision/Recall | Information retrieval framing |
| Accuracy | Null Handling Accuracy | Correct behavior when data is missing |
| Consistency | Format Switching Accuracy | Same content, different output formats |

### Phase 4: Optimization & Deployment
- [ ] **Apply model quantization** — Optimize for CPU efficiency
- [ ] **Optimize inference speed** — Target production-ready latency
- [ ] **Reduce memory footprint** — Support resource-constrained environments
- [ ] **Package for deployment** — Easy integration and distribution
- [ ] **Evaluate quantization methods** — INT8, INT4, GPTQ, AWQ benchmarking
- [ ] **Implement ONNX/OpenVINO conversion** — Critical for CPU inference optimization
- [ ] **Define target latency SLA** — e.g., "< 100ms for 500-token input on 4-core CPU"
- [ ] **Add batch inference support** — Production systems often batch requests
- [ ] **Create Docker deployment** — Containerized inference server
- [ ] **Implement API server** — FastAPI wrapper with OpenAPI spec
- [ ] **Evaluate edge deployment** — llama.cpp or similar for embedded/mobile

### Phase 5: Continuous Improvement 🆕
> Post-deployment lifecycle management

- [ ] **Implement user feedback loop** — Collect hallucination reports from users
- [ ] **Create automated retraining pipeline** — Incorporate new validated data
- [ ] **Establish semantic versioning** — Version model releases consistently
- [ ] **Set up production monitoring** — Track latency, accuracy drift, error rates
- [ ] **Document update procedures** — Model update and rollback workflows

---

## Key Gaps to Address

| Category | Gap | Priority |
|----------|-----|----------|
| Infrastructure | No `pyproject.toml` or dev setup | 🔴 High |
| Data | Missing `validation/` and `test/` directories | 🔴 High |
| Specificity | Vague targets ("production-ready latency") | 🟡 Medium |
| Tooling | No experiment tracking configured | 🟡 Medium |
| Testing | No automated CI/CD for training validation | 🟡 Medium |

## Getting Started

> 🚧 **Project Status**: Exactus is currently in the planning and data preparation phase. Code and pre-trained models are not yet available.

### Immediate Next Steps

1. Review the learning outcomes in [docs/learning_outcomes.md](docs/learning_outcomes.md), key concepts in [docs/key_concepts.md](docs/key_concepts.md), and glossary in [docs/glossary.md](docs/glossary.md) to understand key concepts.
2. Explore the training data samples in `data/training/` to see examples of zero-hallucination data.
3. Familiarize yourself with AI agents and skills via [docs/ai_agents_guide.md](docs/ai_agents_guide.md).
4. Start with Phase 0 tasks in the roadmap, such as setting up the development environment.

### Prerequisites (Planned)
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- PyTorch with CPU optimizations
- 4GB+ RAM (8GB+ recommended)

### Installation (Coming Soon)
```bash
# Clone the repository
git clone https://github.com/mlim-usfca/exactus.git
cd exactus

# Sync dependencies using uv (installs from pyproject.toml)
uv sync
```

### Quick Start (Coming Soon)
```python
# Example using Transformers library (once Exactus model is released on Hugging Face)
from transformers import pipeline

extractor = pipeline("text-generation", model="usfca/exactus-base")
result = extractor("Extract structured data as JSON from: [your source text here]")
print(result)
```

## Contributing

We welcome contributions to Exactus! For assistance with contributions, use AI agents as described in [docs/ai_agents_guide.md](docs/ai_agents_guide.md) to help with coding, validation, and automation tasks.

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