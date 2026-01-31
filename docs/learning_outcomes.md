# Learning Outcomes for Exactus: Data-Accurate Structured Output Model

## Overview

This project provides a comprehensive learning experience for ML/AI students interested in building **specialized language models for structured data extraction without hallucinations**. Through hands-on implementation, students will explore modern techniques for training, fine-tuning, and distilling models that prioritize **factual accuracy**, **schema adherence**, and **CPU-efficient inference**—skills essential for production AI systems where reliability matters.

Exactus focuses on creating models that **never fabricate information**, follow output structures precisely, and run efficiently without GPU dependency. This contrasts with general-purpose LLMs by emphasizing **accuracy over creativity**.

## Learning Outcomes

By the end of this project, students will be able to:

1. **Understand Structured Extraction Models**: Gain deep understanding of models designed for information extraction, including how they differ from general-purpose LLMs in their focus on faithful reproduction of source information without creative additions.

2. **Master Parameter-Efficient Fine-Tuning**: Learn to adapt pre-trained models using LoRA (Low-Rank Adaptation) and QLoRA techniques, which freeze pre-trained weights and inject trainable low-rank matrices—crucial for CPU deployment and resource-constrained environments.

3. **Implement Knowledge Distillation Pipelines**: Develop skills in transferring capabilities from larger "teacher" models to smaller "student" models, preserving accuracy while reducing parameters for efficient inference.

4. **Apply Anti-Hallucination Techniques**: Understand and implement strategies to prevent model hallucinations, including constrained decoding, refusal-aware instruction tuning (R-Tuning), and uncertainty calibration.

5. **Handle Structured Data Formats**: Learn to generate valid outputs in multiple formats (JSON, CSV, XML, YAML) with proper syntax and schema adherence, including handling edge cases like missing data and null values.

6. **Curate Zero-Hallucination Training Data**: Master the creation and validation of synthetic training data where outputs contain only information explicitly present in inputs—the foundation of accurate extraction models.

7. **Optimize for CPU Inference**: Understand quantization techniques (INT8, INT4, GPTQ, AWQ), ONNX/OpenVINO conversion, and other optimizations for production deployment without GPU dependency.

8. **Evaluate Extraction Accuracy**: Master specialized evaluation metrics including factual fidelity, hallucination rate, omission rate, schema adherence, and format compliance.

9. **Benchmark Against Reference Models**: Learn to compare model performance against baselines like NuExtract, using established evaluation datasets and reproducible methodology.

10. **Apply Responsible AI Practices**: Understand the ethical importance of factual accuracy in AI systems, recognizing that hallucinations can cause real-world harm in production applications.

## Key Concepts

### Structured Extraction vs. General LLMs

Structured extraction models like Exactus and NuExtract are fundamentally different from general-purpose LLMs. While ChatGPT or Claude excel at creative tasks and open-ended conversations, extraction models are designed to:

- **Output only information present in the source** — No creative additions or interpolations
- **Follow schemas precisely** — Adhere to user-specified JSON schemas, XML DTDs, or format templates
- **Prefer omission over fabrication** — When data is missing, leave fields empty rather than guess
- **Use low temperature** — NuExtract recommends temperature ≈ 0 because creativity is the enemy of accuracy

**Key Distinction**: General LLMs ask "What's a plausible response?" Extraction models ask "What's explicitly stated in the source?"

### Knowledge Distillation

Knowledge distillation is the process of transferring knowledge from a large "teacher" model to a smaller "student" model. Originally introduced by Hinton, Vinyals, and Dean (2015), this technique enables deploying capable models in resource-constrained environments.

**Key Components:**
- **Teacher Model**: Large, accurate model that provides training signals
- **Student Model**: Smaller model that learns to mimic teacher outputs
- **Soft Labels**: Teacher's probability distributions (not just hard predictions)
- **Temperature Scaling**: Controls softness of probability distributions during training
- **Knowledge Transfer**: Student learns the teacher's "dark knowledge" in output distributions

**Relevance to Exactus**: Distillation allows creating CPU-efficient models that retain the factual accuracy of larger reasoning models.

### Parameter-Efficient Fine-Tuning (LoRA/QLoRA)

Rather than updating all model parameters (expensive and resource-intensive), parameter-efficient methods freeze pre-trained weights and add small trainable components.

**LoRA (Low-Rank Adaptation)**:
- Freezes pre-trained model weights
- Injects trainable rank decomposition matrices into transformer layers
- Reduces trainable parameters by 10,000x compared to full fine-tuning
- No additional inference latency (adapters merge with base model)

**QLoRA (Quantized LoRA)**:
- Combines 4-bit quantization with LoRA
- Enables fine-tuning 65B models on a single 48GB GPU
- Introduces NF4 (4-bit NormalFloat) data type for optimal quantization
- Uses double quantization and paged optimizers for memory efficiency

**Why This Matters**: CPU-first deployment requires small model footprints. LoRA/QLoRA enables fine-tuning without massive GPU infrastructure.

### Anti-Hallucination Techniques

Hallucinations occur when models generate content that diverges from input, contradicts context, or misaligns with world knowledge. For extraction tasks, any fabricated data is unacceptable.

**Key Strategies:**

- **Constrained Decoding**: Limit generation vocabulary to tokens present in source text
- **Refusal-Aware Instruction Tuning (R-Tuning)**: Train models to say "I don't know" when information isn't available, rather than fabricating
- **Temperature Control**: Use temperature ≈ 0 to minimize sampling randomness
- **Schema Enforcement**: Validate outputs against schemas and reject invalid structures
- **Uncertainty Calibration**: Teach models to recognize when they lack knowledge

**Hallucination Types to Prevent:**
- **Fabrication**: Generating facts not in the source
- **Distortion**: Misrepresenting source information
- **Omission**: Missing important data (acceptable when uncertain, problematic when systematic)

### Quantization for CPU Deployment

Quantization reduces model precision from 32-bit floating-point to lower precision formats, enabling efficient CPU inference. This is essential for Exactus's goal of GPU-free deployment.

**Quantization Methods:**

| Method | Precision | Description |
|--------|-----------|-------------|
| INT8 | 8-bit integer | Standard quantization, widely supported |
| INT4 | 4-bit integer | Aggressive compression, requires careful calibration |
| GPTQ | 4-bit | Post-training quantization using layer-wise optimization |
| AWQ | 4-bit | Activation-aware quantization, preserves important weights |

**Types:**
- **Post-Training Quantization (PTQ)**: Applied after training; fast but may lose accuracy
- **Quantization-Aware Training (QAT)**: Simulates quantization during training; better accuracy
- **Dynamic Quantization**: Quantizes at runtime; flexible but slower
- **Static Quantization**: Quantizes at compile time; faster inference

**CPU Optimization Targets:**
- ONNX Runtime for cross-platform deployment
- OpenVINO for Intel hardware optimization
- llama.cpp for edge/embedded deployment
- Target: < 100ms for 500-token input on 4-core CPU

### Structured Output Formats

Exactus supports multiple structured output formats, each with specific use cases and validation requirements:

**JSON (Primary Focus)**:
- Schema-driven with JSON Schema validation
- Most common format for API responses and data interchange
- Supports nested objects, arrays, and typed values

**XML**:
- Document-centric structure with DTD/XSD validation
- Common in enterprise systems and legacy integrations
- Verbose but self-describing

**CSV**:
- Tabular data for spreadsheets and databases
- Simple but limited to flat structures
- Requires header row handling

**YAML**:
- Human-readable configuration format
- Superset of JSON with additional features
- Common in DevOps and configuration management

### Training Data for Zero-Hallucination Models

Creating effective training data for extraction models requires different principles than general LLM training:

**Key Principles:**
- **Explicit Source Attribution**: Every output element must trace to specific source text
- **No Interpolation**: Don't fill gaps with "reasonable" assumptions
- **Null Handling**: Explicitly train on missing data scenarios
- **Edge Cases**: Include empty results, partial data, and error states
- **Format Variety**: Same content across JSON/XML/CSV/YAML for consistency

**Data Quality Checks:**
- Structural validity (parseable JSON, well-formed XML)
- Semantic accuracy (output matches source exactly)
- Schema compliance (follows specified structure)
- No fabrication (automated and human review)

See [docs/open_data_ref.md](open_data_ref.md) for open datasets suitable for training and validation.

### Additional Concepts to Explore

- **Constrained Beam Search**: Limit decoding to valid tokens only
- **Contrastive Learning**: Train models to distinguish correct from fabricated outputs
- **Synthetic Data Generation**: Use teacher models to create extraction training pairs
- **Multi-Format Consistency**: Same extraction across different output formats
- **Adversarial Testing**: Deliberately misleading inputs to test hallucination resistance
- **Calibration**: Align model confidence with actual accuracy
- **Retrieval-Augmented Generation (RAG)**: Ground outputs in retrieved source documents

## Getting Started

1. Review the project structure and baseline model information in the [README](../README.md)
2. Examine the sample training files in `data/training/` to understand zero-hallucination data formats
3. Study the NuExtract model family as the reference baseline for structured extraction
4. Explore open datasets in [docs/open_data_ref.md](open_data_ref.md) for training augmentation
5. Start with simple extraction tasks before moving to complex nested schemas
6. Experiment with different quantization techniques for CPU optimization
7. Document your learning journey, especially hallucination edge cases encountered

## Resources

### Core Papers

- [Attention is All You Need](https://arxiv.org/abs/1706.03762) - Original transformer architecture (Vaswani et al., 2017)
- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) - Knowledge distillation foundations (Hinton, Vinyals, Dean, 2015)
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) - Parameter-efficient fine-tuning (Hu et al., 2021)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) - Memory-efficient fine-tuning with 4-bit quantization (Dettmers et al., 2023)

### Hallucination Research

- [Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models](https://arxiv.org/abs/2309.01219) - Comprehensive survey on hallucination detection, explanation, and mitigation (Zhang et al., 2023)
- [R-Tuning: Instructing Large Language Models to Say 'I Don't Know'](https://arxiv.org/abs/2311.09677) - Refusal-aware instruction tuning to prevent fabrication (Zhang et al., 2023)

### Reference Models

- [NuExtract-2.0](https://huggingface.co/collections/numind/nuextract-20) - State-of-the-art structured extraction model family (NuMind)
- [NuExtract Blog Post](https://numind.ai/blog/nuextract-a-foundation-model-for-structured-extraction) - NuMind's approach to zero-hallucination extraction
- [Qwen2.5 Model Family](https://huggingface.co/Qwen) - Base models for NuExtract and Exactus candidates
- [Qwen3 Model Family](https://huggingface.co/collections/Qwen/qwen3) - Latest Qwen models with advanced reasoning capabilities and thinking mode
- [Phi-4](https://huggingface.co/microsoft/phi-4) - Microsoft's efficient reasoning model

### Practical Tutorials

- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/index) - Parameter-efficient fine-tuning library
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index) - Core library for working with LLMs
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/) - Cross-platform inference optimization
- [OpenVINO Toolkit](https://docs.openvino.ai/) - Intel's toolkit for CPU inference optimization
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - CPU/edge deployment for LLMs

### Evaluation & Benchmarking

- [SQuAD (Stanford Question Answering Dataset)](https://rajpurkar.github.io/SQuAD-explorer/) - Reading comprehension benchmark
- [TruthfulQA](https://github.com/sylinrl/TruthfulQA) - Benchmark for measuring model truthfulness
- [HaluEval](https://github.com/RUCAIBox/HaluEval) - Hallucination evaluation benchmark

### Courses & Learning Paths

- [Deep Learning Specialization](https://www.deeplearning.ai/courses/deep-learning-specialization/) - Andrew Ng's foundational course (alternative access)
- [Fast.ai Practical Deep Learning](https://course.fast.ai/) - Hands-on practical approach
- [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course) - Free course on NLP with transformers
- [LLM University by Cohere](https://cohere.com/llmu) - Comprehensive LLM fundamentals

### Project-Specific Resources

- [Open Data References](open_data_ref.md) - Curated datasets for training and validation
- [Training Data Samples](../data/training/) - Example JSONL files demonstrating data formats
- [training-data-validator Skill](.github/skills/training-data-validator/) - Tool for validating synthetic training data

---

> **Philosophy**: Exactus prioritizes **accuracy over creativity**. When learning these concepts, always ask: "Does this help produce more accurate outputs, or does it add risk of fabrication?" The best way to learn is through hands-on experimentation—but in extraction tasks, measure success by what the model *doesn't* make up, not just what it gets right.