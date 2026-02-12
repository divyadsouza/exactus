# Exactus: Fine-Tuning & Distillation Strategy Guide

**Version:** 1.3

**Last Updated:** 2026-02-08

**Repository:** [mlim-usfca/exactus](https://github.com/mlim-usfca/exactus)

**Target:** **Absolute Zero Hallucination (0% Extrinsic Hallucination)**

---

## 1. The Zero-Hallucination Architecture

To achieve a 0% rate, Exactus uses a **"Verify-then-Generate"** pipeline. The model is no longer just predicting the next token; it is navigating a map of the source text.

### 1.1 Self-Interruption & Abstention Training

*Focus: Structural refusal.*

* **Learned Policy Refusal**: Unlike a prompt-level instruction, we fine-tune the model's internal "concept vectors" (using techniques like **Activation Steering**) to trigger a hard stop if the attention mechanism cannot find a high-confidence match in the source text.
* **Abstention Tokens**: We introduce a dedicated `[ABSENT]` token. The model is trained to favor this token over any parametric "guess" when the probability of a source match falls below a specific threshold (e.g., ).

### 1.2 Attention-Anchored SFT

*Focus: Mathematical grounding.*

* **Grounding Loss**: We implement a custom loss function that penalizes the model if it generates a non-structural token (like a name or date) while its attention is not primarily focused on the corresponding coordinates in the source document.
* **Coordinate-Aware Distillation**: The Teacher model (GPT-4o/Qwen-72B) provides not just the extraction, but the **character-level offsets** of where it found the data. The Student (Exactus) is trained to predict these offsets as a "thinking" step before outputting the text.

---

## 2. Deterministic Inference Mechanisms

Training alone cannot guarantee 0%. We use **Hard Constraints** at the engine level to bridge the final gap.

### 2.1 Grammar-Constrained Decoding (FSM)

* **State Machine Enforcement**: We use a Finite State Machine (FSM) to restrict the model's vocabulary at every step. If the schema expects an `integer`, the model's output logit for letters is mathematically set to zero.
* **System-Level Syntax Guarantees**: This ensures 100% schema adherence (JSON/XML/YAML) by making "malformed output" physically impossible for the model to generate.

### 2.2 Source-Vocabulary Masking

* **Dynamic Token Masking**: During generation, the inference engine builds a "valid token list" from the source document. For any value-extraction field, the model is **masked**—it can only pick tokens that actually appear in the input text.
* **Result**: Extrinsic hallucinations (inventing new facts) are eliminated because the model's "keyboard" only contains words from the source.

---

## 3. Distillation for Absolute Fidelity

### 3.1 Teacher Consensus (Voting)

To ensure the "Gold Standard" training data is actually 100% accurate:

* **Ensemble Labeling**: We use three Teachers (e.g., Qwen-72B, GPT-4o, Claude 3.5). A sample is only added to the Exactus training set if all three models reach a consensus on the extraction.
* **Cross-Format Verification**: The same source is extracted into JSON and XML. If the values don't match between formats, the sample is discarded.

### 3.2 Recursive Task Decomposition

For ultra-small models (0.6B), complex schemas increase hallucination risk.

* **The "Split-Extract-Merge" Pattern**: The Exactus API automatically breaks large schemas into "Micro-Tasks." The 0.6B model only extracts 2-3 fields at a time, keeping its context window clean and focus sharp.

---

## 4. Optimization & Deployment

| Requirement | Strategy | Tooling |
| --- | --- | --- |
| **0% Formatting Error** | FSM / Grammar Constraints | Outlines / Guidance |
| **0% Extrinsic Hallucination** | Source-Vocab Masking | Custom Logit Processor |
| **<100ms Latency** | INT4 Quantization + QAT | OpenVINO / ONNX |
| **High Recall** | Multi-Pass Recursive Logic | Exactus Orchestrator |

---

## Appendix A: Updated Quality Metrics

| Metric | Target | Verification Mechanism |
| --- | --- | --- |
| **Hallucination Rate** | **0.0%** | Automated token-source alignment check |
| **Schema Compliance** | **100%** | Forced FSM-based decoding |
| **Null Accuracy** | **>99%** | Negative constraint testing (Absent Data) |
| **Inference Latency** | **<50ms** | Per-token profiling on 4-core CPU |
