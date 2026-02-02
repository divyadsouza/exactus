# Learning Outcomes and Glossary for Exactus: Data-Accurate Structured Output Model

*Last updated: February 1, 2026*

## Overview

This project provides a comprehensive learning experience for ML/AI students interested in building **specialized language models for structured data extraction without hallucinations**. Through hands-on implementation, students will explore modern techniques for training, fine-tuning, and distilling models that prioritize **factual accuracy**, **schema adherence**, and **CPU-efficient inference**—skills essential for production AI systems where reliability matters.

Exactus focuses on creating models that **never fabricate information**, follow output structures precisely, and run efficiently without GPU dependency. This contrasts with general-purpose LLMs by emphasizing **accuracy over creativity**.

## Table of Contents

- [Overview](#overview)
- [Learning Outcomes](#learning-outcomes)
- [Glossary](glossary.md)
- [Key Concepts](key_concepts.md)
- [Getting Started](getting_started.md)
- [Resources](resources.md)

## Learning Outcomes

By the end of this project, students will be able to:

1. **Understand Structured Extraction Models**: Gain deep understanding of models designed for information extraction, including how they differ from general-purpose LLMs in their focus on faithful reproduction of source information without creative additions.  
   *Checkpoint*: Compare Exactus outputs with a general LLM on the same input and document differences.

2. **Master Parameter-Efficient Fine-Tuning**: Learn to adapt pre-trained models using LoRA (Low-Rank Adaptation) and QLoRA techniques, which freeze pre-trained weights and inject trainable low-rank matrices—crucial for CPU deployment and resource-constrained environments.  
   *Checkpoint*: Fine-tune a small model using LoRA on a sample dataset and measure parameter reduction.

3. **Implement Knowledge Distillation Pipelines**: Develop skills in transferring capabilities from larger "teacher" models to smaller "student" models, preserving accuracy while reducing parameters for efficient inference.  
   *Checkpoint*: Distill a teacher model to a student and compare inference speeds.

4. **Apply Anti-Hallucination Techniques**: Understand and implement strategies to prevent model hallucinations, including constrained decoding, refusal-aware instruction tuning (R-Tuning), and uncertainty calibration.  
   *Checkpoint*: Test a model on adversarial inputs and apply one anti-hallucination technique.

5. **Handle Structured Data Formats**: Learn to generate valid outputs in multiple formats (JSON, CSV, XML, YAML) with proper syntax and schema adherence, including handling edge cases like missing data and null values.  
   *Checkpoint*: Generate outputs in JSON and XML from the same input, ensuring schema compliance.

6. **Curate Zero-Hallucination Training Data**: Master the creation and validation of synthetic training data where outputs contain only information explicitly present in inputs—the foundation of accurate extraction models.  
   *Checkpoint*: Create and validate a small JSONL dataset using the training-data-validator skill.

7. **Optimize for CPU Inference**: Understand quantization techniques (INT8, INT4, GPTQ, AWQ), ONNX/OpenVINO conversion, and other optimizations for production deployment without GPU dependency.  
   *Checkpoint*: Quantize a model and benchmark CPU inference time.

8. **Evaluate Extraction Accuracy**: Master specialized evaluation metrics including factual fidelity, hallucination rate, omission rate, schema adherence, and format compliance.  
   *Checkpoint*: Evaluate a model on a benchmark dataset and calculate key metrics.

9. **Benchmark Against Reference Models**: Learn to compare model performance against baselines like NuExtract, using established evaluation datasets and reproducible methodology.  
   *Checkpoint*: Run a comparison with NuExtract on a shared task.

10. **Apply Responsible AI Practices**: Understand the ethical importance of factual accuracy in AI systems, recognizing that hallucinations can cause real-world harm in production applications.  
    *Checkpoint*: Document a case study on hallucination risks in a real-world scenario.

---

> **Philosophy**: Exactus prioritizes **accuracy over creativity**. When learning these concepts, always ask: "Does this help produce more accurate outputs, or does it add risk of fabrication?" The best way to learn is through hands-on experimentation—but in extraction tasks, measure success by what the model *doesn't* make up, not just what it gets right.