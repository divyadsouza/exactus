---
name: training-data-validator
description: 'Validates synthetic training data for structured output models, checking structural validity and semantic accuracy to ensure zero hallucinations. Use when verifying JSONL training data files, assessing data quality, or confirming AI-generated datasets contain only factual extractions without fabrications.'
---

# Training Data Validator

This skill validates synthetic training data used for fine-tuning structured output models like Exactus. It performs two levels of validation:

1. **Structural Validation**: Uses a Python script to verify JSON/XML syntax and format compliance
2. **Semantic Validation**: AI-powered reasoning to check for factual accuracy and absence of hallucinations

## When to Use This Skill

- Verifying JSONL training data files for accuracy
- Checking synthetic datasets for hallucinations or fabricated content
- Assessing data quality before model training
- Validating extraction-based training data (instruction-input-output triplets)
- When users mention "validate training data", "check data accuracy", or "verify no hallucinations"

## Prerequisites

- Python 3.x with `json` and `xml.etree.ElementTree` modules (standard library)
- Access to JSONL files containing training data with `instruction`, `input`, and `output` fields

## Usage

### Running Validation

The skill can validate all training data files or specific ones:

**Validate all files:**
```
Please validate all the training data files in data/training/
```

**Validate specific files:**
```
Validate training_data_sample1.jsonl and training_data_sample2.jsonl
```

### Validation Process

1. **Structural Check**: Python script validates JSON/XML syntax and schema adherence
2. **Semantic Check**: AI analysis ensures outputs contain only information from inputs, with no hallucinations

### Output Format

The skill provides:
- Structural validation results (pass/fail with error details)
- Semantic validation summary (hallucination detection, accuracy assessment)
- Detailed reasoning for each entry if issues are found

## Bundled Resources

### validate_data.py

The Python validation script performs automated structural checks:

```python
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def validate_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def validate_xml(xml_str):
    try:
        ET.fromstring(xml_str)
        return True
    except ET.ParseError:
        return False

def check_file(file_path):
    errors = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line.strip())
                output = entry['output']
                if output.startswith('{') or output.startswith('['):
                    if not validate_json(output):
                        errors.append(f"Line {line_num}: Invalid JSON in output")
                elif output.startswith('<'):
                    if not validate_xml(output):
                        errors.append(f"Line {line_num}: Invalid XML in output")
            except json.JSONDecodeError:
                errors.append(f"Line {line_num}: Invalid JSONL entry")
    return errors

# Check all files
data_dir = Path('/Users/mlim/Projects/mlim-usfca/exactus/data/training')
for file in data_dir.glob('*.jsonl'):
    print(f"Checking {file.name}")
    errs = check_file(file)
    if errs:
        for err in errs:
            print(f"  {err}")
    else:
        print("  All good")

print("Validation complete.")
```

## Examples

### Example 1: Full Validation
**User:** "Verify the accuracy of all training data files"

**Skill Response:** 
- Runs Python script for structural validation
- Performs semantic analysis on all 32 entries
- Reports: "All files passed structural validation. Semantic analysis confirms zero hallucinations across all entries."

### Example 2: Specific File Check
**User:** "Check training_data_sample1.jsonl for correctness"

**Skill Response:**
- Validates the 3 entries in sample1
- Confirms email parsing, vehicle extraction, and recipe data are accurate
- Notes any potential issues (none found in this case)

## Error Handling

- **Structural Errors**: Reports specific line numbers and error types
- **Semantic Issues**: Describes hallucinated content or missing information
- **File Not Found**: Suggests checking file paths and permissions

## Limitations

- Semantic validation relies on AI reasoning and may have edge cases
- Does not validate against external truth sources (only input-output consistency)
- Assumes standard JSONL format with instruction/input/output fields

## Future Enhancements

- Add support for CSV/YAML output validation
- Implement automated hallucination scoring
- Add batch processing for large datasets