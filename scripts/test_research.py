"""
Test Research Script for Exactus Orchestrator

This script validates the Exactus Orchestrator logic using training data samples.
It loads JSONL files containing instruction-input-output triples, extracts schemas
from the expected outputs, and runs benchmarks to test:

- Relevance finder accuracy (segment identification)
- Data quality validation (detecting missing information)
- Performance metrics (calls, latency, extraction status)

Used in Data Research Phase to ensure orchestration works before model integration.
Run with: python test_research.py [path/to/training_data.jsonl]
"""

import json
from orchestrate_v1 import ExactusOrchestrator, run_benchmark

def load_jsonl(file_path):
    """
    Load a JSONL (JSON Lines) file into a list of dictionaries.
    
    Each line in the file should be a valid JSON object representing
    a training sample with 'instruction', 'input', and 'output' fields.
    
    Args:
        file_path: Path to the JSONL file
        
    Returns:
        List of dicts, one per line
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def extract_schema_from_output(output_str):
    """
    Extract the schema structure from the expected output string.
    
    Parses the JSON output to get the target schema for extraction.
    Handles cases where output might not be JSON (e.g., XML samples).
    
    Args:
        output_str: The expected output string from training data
        
    Returns:
        Dict representing the schema structure, or empty dict if invalid
    """
    try:
        return json.loads(output_str)
    except json.JSONDecodeError:
        # Skip non-JSON outputs (e.g., XML in edgecase samples)
        return {}

def test_with_training_data(jsonl_path):
    """
    Run the orchestrator benchmark on all samples in a training data file.
    
    For each sample, extracts the schema from the expected output and tests
    how well the orchestrator can find relevant segments and validate data quality.
    
    Args:
        jsonl_path: Path to the JSONL training data file
    """
    data = load_jsonl(jsonl_path)
    print(f"Loaded {len(data)} samples from {jsonl_path}\n")

    for i, entry in enumerate(data, 1):
        print(f"--- Sample {i} ---")
        text = entry["input"]
        schema = extract_schema_from_output(entry["output"])
        
        if not schema:
            print("Skipping non-JSON output sample.\n")
            continue
        
        print(f"Instruction: {entry['instruction']}")
        print(f"Text: {text[:100]}...")  # Truncate long texts for readability
        print(f"Schema keys: {list(schema.keys())}\n")
        
        # Run the benchmark and show results
        run_benchmark(text, schema)
        print("\n")

if __name__ == "__main__":
    # Command-line interface for testing with training data
    # Usage: python test_research.py [path/to/data.jsonl]
    # If no path provided, uses default sample1 file
    import sys
    if len(sys.argv) > 1:
        jsonl_file = sys.argv[1]
    else:
        jsonl_file = "../data/training/training_data_sample1.jsonl"  # Default test file
    
    test_with_training_data(jsonl_file)