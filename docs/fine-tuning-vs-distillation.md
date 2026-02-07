# Exactus: Fine-Tuning & Distillation Strategy Guide

**Version:** 1.2

**Last Updated:** 2026-02-08

**Repository:** [mlim-usfca/exactus](https://github.com/mlim-usfca/exactus)

**Status:** **Approved** (Incorporating Attention Distillation & Grammar Constraints)

---

## Executive Summary

Exactus prioritizes **accuracy over creativity** through zero-hallucination structured extraction optimized for CPU-efficient inference. This guide defines the transition from large-scale reasoning to specialized, constrained execution on edge-tier hardware.

---

## 1. Fine-Tuning Strategies

### 1.1 Instruction Tuning with Negative Constraints

*Focus: Training the model to say "I don't know."*

* **Negative Constraint Training**: 15–20% of training samples must feature "distractor" prompts where the requested entity is absent. The model is penalized if it "guesses" and rewarded for returning `null` or `N/A` (preferably empty structure).
* **Source-Grounded SFT**: Input-output pairs must include a `source_span` index, forcing the model to learn that every generated token must have a corresponding coordinate in the input text.

### 1.2 Targeted Layer & Attention Tuning

*Focus: Anchoring structure without losing linguistics.*

* **Output Projection Focus**: Focus weight updates on the final layers and embeddings. This "freezes" the core logic while specializing the vocabulary for structural tokens (JSON keys, brackets, CSV delimiters).
* **Attention Map Alignment**: During fine-tuning, enforce a "sparsity constraint" where the model’s attention must peak on source tokens that match the target extraction, discouraging "hallucinatory" attention drift to empty latent space.

---

## 2. Distillation Architecture

### 2.1 Teacher-Student Configuration

| Role | Recommended Models | Rationale |
| --- | --- | --- |
| **Teacher** | Qwen2.5-72B / GPT-4o | Deep reasoning for complex schema mapping. |
| **Student** | Qwen3-0.6B / Qwen3-4B | Optimized for 4-bit CPU inference (ONNX/OpenVINO). |

### 2.2 Sequence-Level & Feature Distillation

*Focus: Transferring "Extraction Logic" rather than "General Knowledge".*

* **Primary (Sequence-Level)**: Use the Teacher to generate a "Gold Standard" dataset. Filter this data through the `training-data-validator` to ensure 100% schema adherence before the Student ever sees it.
* **Secondary (Attention Distillation)**: Force the Student’s attention heads to mimic the Teacher’s. If the Teacher looks at "Price: $50" to extract a value, the Student is trained to align its attention weights to those same coordinates.
* **Recursive Extraction Logic**: For the 0.6B model, the distillation process should include **"Task Decomposition"**. If a schema has >10 fields, train the student to handle it in "chunks" rather than a single massive JSON blob.

---

## 3. Inference-Time Constraint Mechanisms

### 3.1 Grammar-Constrained Decoding (The "Safety Rail")

Regardless of training, the inference engine must enforce syntax.

* **FSM-Based Constraints**: Integrate libraries like `Outlines` or `Guidance`. Use a Finite State Machine (FSM) to ensure that if the model generates a `{`, the only valid next tokens are `"`, whitespace, or `}`.
* **Regex-Guided Extraction**: For specific fields (dates, phone numbers, IDs), the decoding process should restrict the model's vocabulary to tokens that match the target Regex pattern.
* **Source-Vocabulary Restriction**: Dynamically restrict the model's output logit space so it can only choose tokens present in the source document + structural syntax tokens.

### 3.2 Deterministic Sampling

* **Temperature = 0**: Strictly enforced.
* **Greedy Decoding**: Favored over Beam Search to minimize CPU overhead while ensuring the most probable (factual) token is selected.

---

## 4. CPU-First Optimization

### 4.1 Quantization-Aware Training (QAT)

Traditional post-training quantization often breaks small models' ability to follow complex JSON.

* **Action**: Apply QAT during the final 10% of the fine-tuning phase. This "pre-adapts" the model to the rounding errors of 4-bit (INT4) precision.

### 4.2 Targeted Runtimes

* **ONNX Runtime**: Primary target for cross-platform CPU.
* **OpenVINO**: Specialized optimization for Intel-based server environments.

---

## 5. Implementation Roadmap

### Phase 1: Data Generation (Teacher-Led)

* [ ] Generate 500k samples with 20% "Absent Data" scenarios.
* [ ] Implement **Cross-Format Consistency**: One source text generates JSON, XML, and CSV versions to ensure format-agnostic extraction.

### Phase 2: Training (Student-Led)

* [ ] Execute **QLoRA** on Qwen3-0.6B using the Attention Alignment loss.
* [ ] Perform **QAT** to prepare for INT4 deployment.

### Phase 3: Validation (System-Level)

* [ ] Benchmark **Model + Grammar Constraints** against NuExtract-2.0.
* [ ] **SLA Check**: Ensure 500-token processing in <100ms on 4-core CPU.

---

## Appendix A: Quality Metrics

| Metric | Target | Description |
| --- | --- | --- |
| **Schema Fidelity** | 100% | Guaranteed by Grammar-Constrained Decoding. |
| **Hallucination Rate** | <0.1% | Measured by token-traceability to source document. |
| **Recovery Rate** | >95% | Ability to correctly return `null` when data is missing. |
| **Inference Latency** | <100ms | P90 target for standard CPU environments. |

---

**Next Step:** Would you like me to create the **Phase 1 Python script** that utilizes a Teacher model to generate these "negative constraint" samples and validates them against a JSON schema?