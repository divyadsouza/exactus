# Glossary

Key terms and concepts used throughout the project. New contributors are encouraged to research these terms to build foundational knowledge.

- **Baseline Model**: A reference model (e.g., NuExtract) used for comparison and validation of Exactus's performance.
- **Distillation**: The process of training a smaller "student" model to replicate the behavior of a larger "teacher" model, preserving accuracy while reducing size.
- **Fine-Tuning**: Adapting a pre-trained model to a specific task by training on task-specific data.
- **Hallucinations**: When a model generates information not present in the input, such as fabricated facts or interpretations.
- **Extrinsic Hallucination**: Generating facts or entities not present in the source document.
- **Hugging Face**: An open-source platform and library for NLP models, providing tools like Transformers for model loading and inference.
- **Inference**: The process of using a trained model to make predictions or generate outputs on new data.
- **JSONL**: JSON Lines format, where each line is a valid JSON object, commonly used for training data in machine learning.
- **LoRA/QLoRA**: Parameter-efficient fine-tuning methods that update only a small subset of model parameters.
- **Structured Output**: Data formatted in schemas like JSON, XML, CSV, or YAML, ensuring consistent and parseable results.
- **Transformers**: A library by Hugging Face for working with transformer-based models, including loading, training, and inference.
- **Verify-then-Generate Pipeline**: A two-phase approach where the model first verifies source coordinates before generating output, ensuring zero extrinsic hallucinations.
- **Self-Interruption & Abstention Training**: Training the model to trigger internal "hard stops" when attention cannot find high-confidence source matches.
- **Learned Policy Refusal**: Fine-tuning concept vectors using techniques like Activation Steering to enforce abstention from guesses.
- **Activation Steering**: A technique to modify model activations during training to steer behavior towards desired policies.
- **Abstention Tokens**: Special tokens (e.g., `[ABSENT]`) trained to favor when source matches fall below confidence thresholds.
- **Attention-Anchored SFT**: Supervised fine-tuning that penalizes outputs where attention is not focused on corresponding source coordinates.
- **Grounding Loss**: A custom loss function ensuring generated tokens have matching attention peaks in the source document.
- **Coordinate-Aware Distillation**: Teacher models provide character-level offsets alongside extractions for precise grounding.
- **Grammar-Constrained Decoding (FSM)**: Using Finite State Machines to restrict token sequences, ensuring 100% schema compliance.
- **Source-Vocabulary Masking**: Dynamically masking the model's output logits to only allow tokens present in the source document.
- **Teacher Consensus (Voting)**: Using multiple teacher models and requiring agreement for training sample inclusion.
- **Cross-Format Verification**: Validating extractions by comparing outputs across different formats (JSON/XML) for consistency.
- **Recursive Task Decomposition**: Breaking complex schemas into micro-tasks for small models to process in chunks.
- **Split-Extract-Merge Pattern**: Automatically decomposing large schemas into smaller subtasks for efficient processing.
- **Deterministic Sampling**: Generation with temperature=0 and greedy decoding to ensure reproducible, factual outputs.
- **FSM-Based Constraints**: Finite State Machine constraints that enforce valid token sequences during decoding.
- **Hallucination Rate**: Percentage of outputs containing fabricated information not present in the source. Target: 0.0%.
- **Inference Latency**: Time required to process input and generate output, targeted at <50ms for CPU deployment.
- **Null Accuracy**: Ability to correctly return null or empty values when data is missing from source. Target: >99%.
- **Schema Compliance**: Guarantee that outputs conform 100% to specified schemas.
- **ONNX Runtime**: Cross-platform runtime for optimized model inference on CPUs.
- **OpenVINO**: Intel's toolkit for optimizing neural network inference on Intel hardware.
- **QAT (Quantization-Aware Training)**: Training that simulates quantization effects to maintain accuracy at low precision.
- **Zero-Hallucination**: The principle that outputs must contain only information explicitly present in the input, with no fabrication.