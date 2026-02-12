# Key Concepts

## Structured Extraction vs. General LLMs

Structured extraction models like Exactus and NuExtract are fundamentally different from general-purpose LLMs. While ChatGPT or Claude excel at creative tasks and open-ended conversations, extraction models are designed to:

- **Output only information present in the source** — No creative additions or interpolations
- **Follow schemas precisely** — Adhere to user-specified JSON schemas, XML DTDs, or format templates
- **Prefer omission over fabrication** — When data is missing, leave fields empty rather than guess
- **Use low temperature** — NuExtract recommends temperature ≈ 0 because creativity is the enemy of accuracy

**Key Distinction**: General LLMs ask "What's a plausible response?" Extraction models ask "What's explicitly stated in the source?"

## Knowledge Distillation

Knowledge distillation is the process of transferring knowledge from a large "teacher" model to a smaller "student" model. Originally introduced by Hinton, Vinyals, and Dean (2015), this technique enables deploying capable models in resource-constrained environments.

**Key Components:**
- **Teacher Model**: Large, accurate model that provides training signals
- **Student Model**: Smaller model that learns to mimic teacher outputs
- **Soft Labels**: Teacher's probability distributions (not just hard predictions)
- **Temperature Scaling**: Controls softness of probability distributions during training
- **Knowledge Transfer**: Student learns the teacher's "dark knowledge" in output distributions

**Relevance to Exactus**: Distillation allows creating CPU-efficient models that retain the factual accuracy of larger reasoning models.

## Fine-Tuning for Absolute Zero Hallucination

Exactus employs specialized fine-tuning techniques to achieve 0% extrinsic hallucination through a "Verify-then-Generate" pipeline.

### Self-Interruption & Abstention Training

Training models to trigger internal hard stops when source matches are uncertain.

**Key Components:**
- **Learned Policy Refusal**: Fine-tune concept vectors using Activation Steering to enforce abstention from parametric guesses
- **Abstention Tokens**: Introduce `[ABSENT]` token favored when attention confidence falls below threshold
- **Structural Refusal**: Reward returning empty structures over fabrication

### Attention-Anchored SFT

Mathematical grounding ensuring every token traces to source coordinates.

**Techniques:**
- **Grounding Loss**: Penalize outputs where attention isn't peaked on corresponding source spans
- **Coordinate-Aware Distillation**: Teacher provides character-level offsets for precise mapping
- **Sparsity Constraints**: Prevent attention drift to latent space

## Distillation for Absolute Fidelity

Advanced distillation methods ensure 100% accurate training data through consensus and verification.

### Teacher Consensus Configuration

Using ensemble agreement to guarantee gold-standard data.

| Role | Recommended Models | Rationale |
| --- | --- | --- |
| **Teachers** | Qwen2.5-72B, GPT-4o, Claude 3.5 | Ensemble voting for consensus on extractions |
| **Student** | Qwen3-0.6B / Qwen3-4B | Optimized for 4-bit CPU inference |

### Sequence-Level Distillation with Verification

**Ensemble Labeling**: Only include samples where all teachers agree on extraction.

**Cross-Format Verification**: Validate by extracting same source into JSON and XML, discarding mismatches.

**Recursive Task Decomposition**: For small models, break complex schemas into "Split-Extract-Merge" micro-tasks.

## Grammar-Constrained Decoding

Inference-time mechanisms that enforce syntactic correctness and source grounding.

**Key Methods:**
- **FSM-Based Constraints**: Finite State Machines ensure valid token sequences (e.g., `{` must be followed by valid JSON tokens)
- **Source-Vocabulary Masking**: Dynamically restrict logits to tokens present in source document
- **Regex-Guided Extraction**: Restrict vocabulary for specific fields (dates, phone numbers) to match patterns

## Deterministic Sampling

Eliminating randomness in generation to ensure reproducible, factual outputs.

**Requirements:**
- **Temperature = 0**: Strictly enforced to prevent creative deviations
- **Greedy Decoding**: Select most probable token for CPU efficiency and accuracy
- **No Beam Search**: Avoids complexity while maintaining factual generation

## Quantization-Aware Training (QAT)

Integrating quantization simulation during training to maintain accuracy at low precision.

**Benefits:**
- Pre-adapts models to 4-bit (INT4) rounding errors
- Applied in final 10% of fine-tuning phase
- Prevents accuracy degradation from post-training quantization

**Target Runtimes:**
- **ONNX Runtime**: Cross-platform CPU inference
- **OpenVINO**: Intel-optimized performance

## Parameter-Efficient Fine-Tuning (LoRA/QLoRA)

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

## Anti-Hallucination Techniques

Hallucinations occur when models generate content that diverges from input, contradicts context, or misaligns with world knowledge. For extraction tasks, any fabricated data is unacceptable.

**Key Strategies:**

- **Verify-then-Generate Pipeline**: Two-phase approach with coordinate verification before output
- **Source-Vocabulary Masking**: Limit generation to tokens in source document
- **Grammar-Constrained Decoding**: Use FSM-based constraints and regex patterns to enforce syntactic validity
- **Self-Interruption Training**: Train models to abstain when attention confidence is low
- **Teacher Consensus**: Use ensemble agreement for training data validation
- **Temperature Control**: Use temperature = 0 to minimize sampling randomness
- **Schema Enforcement**: Validate outputs against schemas and reject invalid structures
- **Uncertainty Calibration**: Teach models to recognize when they lack knowledge

**Hallucination Types to Prevent:**
- **Fabrication**: Generating facts not in the source
- **Distortion**: Misrepresenting source information
- **Omission**: Missing important data (acceptable when uncertain, problematic when systematic)

## Quantization for CPU Deployment

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
- **Quantization-Aware Training (QAT)**: Simulates quantization during training; better accuracy for low-precision deployment
- **Dynamic Quantization**: Quantizes at runtime; flexible but slower
- **Static Quantization**: Quantizes at compile time; faster inference

**CPU Optimization Targets:**
- ONNX Runtime for cross-platform deployment
- OpenVINO for Intel hardware optimization
- llama.cpp for edge/embedded deployment
- Target: < 50ms for 500-token input on 4-core CPU

## Structured Output Formats

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

## Training Data for Zero-Hallucination Models

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

See [open_data_ref.md](open_data_ref.md) for open datasets suitable for training and validation.

## Additional Concepts to Explore

- **Constrained Beam Search**: Limit decoding to valid tokens only
- **Contrastive Learning**: Train models to distinguish correct from fabricated outputs
- **Synthetic Data Generation**: Use teacher models to create extraction training pairs
- **Multi-Format Consistency**: Same extraction across different output formats
- **Adversarial Testing**: Deliberately misleading inputs to test hallucination resistance
- **Calibration**: Align model confidence with actual accuracy
- **Retrieval-Augmented Generation (RAG)**: Ground outputs in retrieved source documents