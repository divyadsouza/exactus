# Glossary

Key terms and concepts used throughout the project. New contributors are encouraged to research these terms to build foundational knowledge.

- **Baseline Model**: A reference model (e.g., NuExtract) used for comparison and validation of Exactus's performance.
- **Distillation**: The process of training a smaller "student" model to replicate the behavior of a larger "teacher" model, preserving accuracy while reducing size.
- **Fine-Tuning**: Adapting a pre-trained model to a specific task by training on task-specific data.
- **Hallucinations**: When a model generates information not present in the input, such as fabricated facts or interpretations.
- **Hugging Face**: An open-source platform and library for NLP models, providing tools like Transformers for model loading and inference.
- **Inference**: The process of using a trained model to make predictions or generate outputs on new data.
- **JSONL**: JSON Lines format, where each line is a valid JSON object, commonly used for training data in machine learning.
- **LoRA/QLoRA**: Parameter-efficient fine-tuning methods that update only a small subset of model parameters.
- **Structured Output**: Data formatted in schemas like JSON, XML, CSV, or YAML, ensuring consistent and parseable results.
- **Transformers**: A library by Hugging Face for working with transformer-based models, including loading, training, and inference.
- **Attention Distillation**: Training a student model to replicate the attention patterns of a teacher model, ensuring focus on relevant source tokens.
- **Deterministic Sampling**: Generation with temperature=0 and greedy decoding to ensure reproducible, factual outputs.
- **FSM-Based Constraints**: Finite State Machine constraints that enforce valid token sequences during decoding.
- **Grammar-Constrained Decoding**: Inference-time mechanisms using FSMs and regex to ensure syntactically correct outputs.
- **Hallucination Rate**: Percentage of outputs containing fabricated information not present in the source.
- **Inference Latency**: Time required to process input and generate output, targeted at <100ms for CPU deployment.
- **ONNX Runtime**: Cross-platform runtime for optimized model inference on CPUs.
- **OpenVINO**: Intel's toolkit for optimizing neural network inference on Intel hardware.
- **QAT (Quantization-Aware Training)**: Training that simulates quantization effects to maintain accuracy at low precision.
- **Recovery Rate**: Ability to correctly return null or empty values when data is missing from source.
- **Recursive Extraction Logic**: Processing complex schemas in chunks rather than monolithic structures.
- **Regex-Guided Extraction**: Restricting output vocabulary for specific fields to match predefined patterns.
- **Schema Fidelity**: Guarantee that outputs conform 100% to specified schemas.
- **Source-Vocabulary Restriction**: Limiting output tokens to those present in the source document plus structural syntax.
- **Zero-Hallucination**: The principle that outputs must contain only information explicitly present in the input, with no fabrication.