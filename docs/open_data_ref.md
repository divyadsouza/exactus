# Open Data References for Exactus

This document outlines open-source datasets identified for potential use in the Exactus project. These datasets are suitable for structured information extraction and output generation tasks, aligning with Exactus's goals of zero-hallucination, factual extraction, and schema-driven outputs. They can be leveraged for training, validation, testing, or benchmarking against baseline models like NuExtract.

Datasets were selected based on their factual nature, diversity in domains, adaptability to JSON/XML/CSV formats, and relevance to pure extraction without hallucinations. All are publicly available on platforms like Hugging Face or Kaggle, with open licensing (e.g., MIT, CC-BY-SA).

## Dataset Overview

| Dataset | Platform | Size | Format | Domain | Relevance to Exactus |
|---------|----------|------|--------|--------|----------------------|
| Vital Articles Synthetic Information Extraction | Hugging Face (`nicpopovic/vital_articles_synthetic_information_extraction`) | ~5,010 samples | JSONL/Parquet | Wikipedia | High - Synthetic extraction pairs; direct analog to NuExtract's training data |
| DocRED | Hugging Face (`thunlp/docred`) | ~5,000 documents | JSON | Wikipedia | High - Document-level relations; long-context extraction |
| TACRED | Hugging Face (`dfki-nlp/tacred`) | ~106,000 examples | JSON/CSV | General web | High - Relation triples; factual and diverse |
| CoNLL-2003 | Hugging Face (`eriktks/conll2003`) | ~20,000 sentences | Text + tags | News | Medium - Entity extraction; convertible to JSON |
| MultiWOZ | Hugging Face (`pfb30/multi_woz_v22`) | ~10,000 dialogues | JSON | Dialogues | Medium - Slot-value structures; schema-driven |
| SROIE | Kaggle (`urbikn/sroie-datasetv2`) | ~1,000 receipts | Text + XML/JSON | Receipts | Medium - Key-value extraction; real-world domain |
| WikiTableQuestions | Hugging Face (`stanfordnlp/wikitablequestions`) | ~22,000 questions | Text + tables | Tables | Medium - Table-based outputs; hybrid tasks |

## Detailed Justifications and Use Cases

### 1. Vital Articles Synthetic Information Extraction
- **Description**: Synthetically generated from Wikipedia abstracts using an LLM pipeline. Provides text inputs with structured JSON outputs (entities and relation triples, ~59k entities, ~30k triples).
- **Justification**: Highly relevant as it's synthetic and designed for in-context learning without hallucinations—directly analogous to NuExtract's synthetic training approach. Factual base (Wikipedia) ensures no fabrications.
- **Potential Use**:
  - **Training**: Primary data for structured extraction; ready for JSON schema training with minimal preprocessing.
  - **Testing**: Validate zero-hallucination on synthetic pairs.
  - **Benchmarking**: Compare against NuExtract for extraction accuracy on similar data.

### 2. DocRED
- **Description**: Full Wikipedia documents with intra-document entity relations (triples). Inputs are long texts; outputs are JSON-like structures with entities and relation graphs.
- **Justification**: Excellent for long-document extraction, matching NuExtract's capabilities. Factual, diverse, and high-complexity; ideal for zero-hallucination training.
- **Potential Use**:
  - **Training**: Complex structured generation; filter/augment for schema-driven outputs.
  - **Testing**: End-to-end model testing on document-level tasks.
  - **Benchmarking**: Baseline against NuExtract for long-context performance.

### 3. TACRED
- **Description**: Sentences with annotated subject-object relations (e.g., triples like `{"subject": "John", "relation": "works_for", "object": "Google"}`).
- **Justification**: Strong for relation extraction tasks. Factual web text ensures no hallucinations; aligns with NuExtract's focus on pure extraction.
- **Potential Use**:
  - **Training**: Fine-tuning for relation-based structured outputs.
  - **Testing**: Hallucination resistance on diverse relations.
  - **Benchmarking**: Compare extraction precision/recall against NuExtract.

### 4. CoNLL-2003
- **Description**: News sentences with BIO-tagged entities (e.g., PER, LOC, ORG). Easily convertible to JSON structures.
- **Justification**: High for entity extraction without hallucinations. Suitable for training on factual, non-synthetic data; low-to-medium complexity.
- **Potential Use**:
  - **Training**: Basic structured outputs; convert to JSONL pairs.
  - **Testing**: Validation for simple entity tasks.
  - **Benchmarking**: Factual accuracy baseline against NuExtract.

### 5. MultiWOZ
- **Description**: Multi-turn dialogues with structured slot-value outputs (e.g., `{"restaurant": {"food": "Italian", "price": "cheap"}}`).
- **Justification**: Aligns with schema-driven outputs. Factual dialogues ensure no hallucinations; medium complexity.
- **Potential Use**:
  - **Training**: Dynamic structured generation in dialogues.
  - **Testing**: Adaptive structuring on conversational data.
  - **Benchmarking**: Consistency in format switching against NuExtract.

### 6. SROIE
- **Description**: Receipt images with OCR text and annotated key-value pairs (adaptable to JSON).
- **Justification**: Good for real-world structured output (e.g., invoices). Factual and domain-specific; useful for diverse applications.
- **Potential Use**:
  - **Training**: OCR-to-structured data; convert annotations to JSON.
  - **Testing**: Edge cases like missing data.
  - **Benchmarking**: Domain-specific accuracy against NuExtract.

### 7. WikiTableQuestions
- **Description**: Wikipedia tables with natural language questions and structured answers (SQL-like or JSON paths).
- **Justification**: Useful for factual, table-driven structured outputs. Diverse and non-hallucinatory; medium complexity.
- **Potential Use**:
  - **Training**: Hybrid text-structured tasks; generate JSON schemas from tables.
  - **Testing**: Complex schema adherence.
  - **Benchmarking**: Table extraction performance vs. NuExtract.

## General Notes
- **Licensing and Access**: All datasets are open-source. Download via Hugging Face Datasets library (`datasets.load_dataset()`) or direct links. Verify for commercial use.
- **Preprocessing Needs**: Most require conversion to JSONL (text input + JSON output) for Exactus training. Use tools like LLMs for augmentation if needed.
- **Integration with Exactus**: Supplement existing synthetic JSONL files (e.g., `training_data_sample1.jsonl`). Create validation/test sets in `data/validation/` and `data/test/` directories.
- **Benchmarking Against NuExtract**: Use these for comparative evaluation on accuracy, speed, and hallucination rates. Start with Vital Articles and DocRED for direct relevance.
- **Limitations**: Some (e.g., CoNLL-2003) need tag-to-JSON conversion. Synthetic datasets may require real-data mixing for generalization.

For implementation, refer to the `training-data-validator` skill for quality checks. If needed, we can generate code to load and convert these datasets.