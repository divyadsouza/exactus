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
- **Zero-Hallucination**: The principle that outputs must contain only information explicitly present in the input, with no fabrication.