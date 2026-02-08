# Exactus Scripts

This folder contains the core orchestration scripts for the Exactus project, designed to enable zero-hallucination data extraction using small AI models (0.6B-4B parameters).

## Scripts Overview

### 1. `orchestrate_v1.py`

**Purpose**: Implements the Exactus Orchestrator, a data preprocessing system that prepares text for small AI models to achieve accurate, hallucination-free extractions.

**Key Features**:
- Recursive schema decomposition for complex field sets
- Relevant segment identification via sliding window search
- Data quality validation to detect missing information
- Performance benchmarking and metrics collection

**Architecture**:
- **Schema Profiler**: Splits schemas with >8 fields into smaller sub-tasks
- **Segment Finder**: Isolates 300-500 character windows containing relevant keywords
- **Data Validator**: Flags unextractable information to prevent hallucinations

**Usage**:
```bash
# Run built-in test case (demonstrates schema splitting and validation)
python orchestrate_v1.py

# Test with custom text and schema file
python orchestrate_v1.py "Your text here" path/to/schema.json

# Read JSON input from stdin
echo '{"text": "Your text", "schema": {"field": "type"}}' | python orchestrate_v1.py -
```

**Output**: Performance report showing model calls, latency, extraction status, and data quality alerts (warnings when requested fields aren't found in the text).

**When to Use**:
- **Data Research Phase**: Test orchestration logic on sample data
- **Model Evaluation Phase**: Benchmark before/after model integration
- **Production Phase**: Import as the front-end processor for API requests

### 2. `test_research.py`

**Purpose**: Validation harness for testing the orchestrator against training data samples.

**Features**:
- Loads JSONL training files with instruction-input-output triples
- Extracts schemas from expected outputs
- Runs benchmarks on each sample to validate logic
- Reports relevance finder accuracy and data quality detection

**Usage**:
```bash
# Test with default sample file
python test_research.py

# Test with specific file
python test_research.py ../data/training/training_data_sample1.jsonl

# Test edge cases
python test_research.py ../data/training/training_data_sample5_edgecase.jsonl
```

**Input Format**: JSONL files where each line contains:
```json
{
  "instruction": "Parse this email...",
  "input": "From: alice@company.com...",
  "output": "{\"sender\": \"alice@company.com\", ...}"
}
```

**Output**: Individual benchmark reports for each training sample, including data quality alerts for missing information.

**When to Use**:
- **Data Research Phase**: Validate orchestration on real training data
- **Debugging**: Identify cases where segment finding or validation fails
- **Quality Assurance**: Ensure no hallucinations on known datasets

## Development Workflow

1. **Research Phase**: Use `test_research.py` or `test_with_training.py` with training samples to refine logic
2. **Integration Phase**: Replace placeholder in `orchestrate_v1.py` with actual model calls
3. **Production Phase**: Deploy `orchestrate_v1.py` as API preprocessor

### 3. `test_with_training.py`

**Purpose**: Demonstrates calling `orchestrate_v1.py` as an external subprocess with embedded training data samples.

**Features**:
- Contains sample training data directly in the script
- Calls `orchestrate_v1.py` as a separate process
- Shows how to use the command-line interface programmatically
- Creates temporary schema files automatically

**Usage**:
```bash
python test_with_training.py
```

**Output**: Benchmark report from `orchestrate_v1.py` for the embedded training sample.

**When to Use**:
- **Learning**: Understand how to call `orchestrate_v1.py` from other scripts
- **Testing**: Quick validation without external data files
- **Examples**: Reference for integrating orchestrator into larger systems

## Requirements

- Python 3.10+
- Training data in `../data/training/` (JSONL format)

## Key Metrics

- **Model Calls**: Number of inference operations (lower is better)
- **Latency**: Processing time (<100ms target for CPU efficiency)
- **Data Quality**: Percentage of samples with verified segments
- **Extraction Status**: Fields found vs. expected

## Notes

- Both scripts include comprehensive comments for maintainability
- The orchestrator assumes small models; adjust `field_threshold` and `window_size` as needed
- Data quality alerts indicate potential hallucination risks in production