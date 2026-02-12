"""
Exactus Orchestrator v1

This script implements the core orchestration logic for the Exactus system.
It prepares data for small AI models (0.6B-4B parameters) to achieve zero hallucination
by decomposing complex extraction tasks into smaller, focused operations.

Key features:
- Recursive schema splitting for large field sets
- Relevant segment identification via sliding window search
- Data quality validation to detect unextractable information
- Performance benchmarking and metrics collection

Used in Data Research Phase to test logic before model integration.
"""

import json
import time
import re
from typing import Dict, Any, List

class ExactusOrchestrator:
    """
    Orchestrates data extraction for small AI models using a three-layer approach:
    1. Schema Profiler: Splits complex schemas recursively
    2. Relevant Segment Finder: Isolates key text windows
    3. Model & Decoder: Processes clean snippets (placeholder here)
    """
    
    def __init__(self, field_threshold=8, window_size=500, validate_quality=True):
        """
        Initialize the orchestrator.
        
        Args:
            field_threshold: Max fields before splitting schema (prevents model choke)
            window_size: Character window for segment search (balances context vs efficiency)
            validate_quality: Enable data quality checks for missing information
        """
        self.field_threshold = field_threshold
        self.window_size = window_size
        self.validate_quality = validate_quality
        self.metrics = {"calls": 0, "quality_warnings": []}

    def find_relevant_segment(self, text: str, schema: Dict) -> str:
        """
        Isolates the most relevant part of the text for a given schema.
        
        Uses keyword matching to find text windows containing schema field names.
        For short texts, returns the whole text. For long texts, uses sliding window
        to find the segment with highest keyword density.
        
        Args:
            text: The input text to search
            schema: Dict of fields to extract (keys used as keywords)
            
        Returns:
            The most relevant text segment
        """
        keywords = [k.lower() for k in schema.keys()]
        if len(text) <= self.window_size:
            segment = text
        else:
            best_segment = ""
            max_score = -1
            
            # Sliding window search with 50% overlap for comprehensive coverage
            step = self.window_size // 2
            for i in range(0, len(text), step):
                segment = text[i : i + self.window_size]
                score = sum(1 for kw in keywords if kw in segment.lower())
                if score > max_score:
                    max_score = score
                    best_segment = segment
            segment = best_segment
        
        # DATA QUALITY VALIDATOR: Alert if keywords are missing from the source
        # This prevents the model from hallucinating missing information
        score = sum(1 for kw in keywords if kw in segment.lower())
        if self.validate_quality and score == 0:
            msg = f"WARNING: No keywords found for sub-schema: {list(schema.keys())}"
            self.metrics["quality_warnings"].append(msg)
            
        return segment

    def extract(self, text: str, schema: Dict) -> Dict:
        """
        Recursive extraction loop that decomposes complex schemas.
        
        If schema has too many fields, splits into smaller sub-tasks to prevent
        model overload. Each sub-task gets its own relevant segment, ensuring
        the model operates in its "high-certainty zone."
        
        Args:
            text: Input text to extract from
            schema: Target schema structure (nested dicts supported)
            
        Returns:
            Dict with extracted values (placeholder "verified_val" for now)
        """
        if len(schema) > self.field_threshold:
            # Split large schemas to avoid model choke on complex tasks
            items = list(schema.items())
            midpoint = len(items) // 2
            s1, s2 = dict(items[:midpoint]), dict(items[midpoint:])
            merged = {}
            merged.update(self.extract(text, s1))
            merged.update(self.extract(text, s2))
            return merged
        else:
            self.metrics["calls"] += 1
            segment = self.find_relevant_segment(text, schema)
            # Placeholder for actual model inference (ONNX/OpenVINO)
            # In production, replace with: model.generate(segment, schema)
            return {field: "verified_val" for field in schema.keys()}

def run_benchmark(text, schema):
    """
    Runs a performance benchmark on the orchestrator.
    
    Tests the extraction logic and reports key metrics:
    - Model calls (indicates task decomposition)
    - Latency (should be <100ms for CPU efficiency)
    - Extraction status (fields found vs expected)
    - Data quality alerts (missing information detection)
    
    Args:
        text: Input text for extraction
        schema: Target schema to extract
    """
    orchestrator = ExactusOrchestrator(validate_quality=True)
    print(f"🚀 Initializing Exactus Benchmark (Text Length: {len(text)} chars)")
    
    start = time.time()
    results = orchestrator.extract(text, schema)
    end = time.time()

    print("\n" + "="*40)
    print("EXACTUS PERFORMANCE REPORT")
    print("-" * 40)
    print(f"Total Model Calls:   {orchestrator.metrics['calls']}")
    print(f"Total Latency:       {end - start:.4f}s")
    print(f"Extraction Status:   {len(results)}/{len(schema)} fields found")
    
    if orchestrator.metrics["quality_warnings"]:
        print("\n❌ DATA QUALITY ALERTS:")
        for warning in orchestrator.metrics["quality_warnings"]:
            print(f"  - {warning}")
    else:
        print("\n✅ DATA QUALITY: All segments verified.")
    print("="*40)

if __name__ == "__main__":
    """
    Command-line interface for testing the Exactus Orchestrator.
    
    Usage:
        python orchestrate_v1.py                          # Run default test case
        python orchestrate_v1.py "your text here" schema.json  # Custom text and schema file
        python orchestrate_v1.py -                       # Read JSON from stdin
    
    The default test case demonstrates schema splitting and data quality validation.
    """
    import sys
    
    if len(sys.argv) == 1:
        # Default test case: 12 fields (triggers recursion) + missing data field (triggers validator)
        # Demonstrates schema splitting and data quality detection
        sample_text = "The contract was signed on 2025-01-01 by Alice and Bob."
        sample_schema = {}
        for i in range(12):
            sample_schema[f"field_{i}"] = "string"
        sample_schema["missing_data_field"] = "string"
        run_benchmark(sample_text, sample_schema)
    
    elif len(sys.argv) == 2 and sys.argv[1] == "-":
        # Read JSON from stdin
        try:
            import json
            data = json.load(sys.stdin)
            text = data.get("text", "")
            schema = data.get("schema", {})
            run_benchmark(text, schema)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading JSON from stdin: {e}")
            print("Expected format: {'text': 'your text', 'schema': {'field': 'type', ...}}")
            sys.exit(1)
    
    elif len(sys.argv) == 3:
        # Custom text and schema file
        text = sys.argv[1]
        schema_file = sys.argv[2]
        try:
            import json
            with open(schema_file, 'r') as f:
                schema = json.load(f)
            run_benchmark(text, schema)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading schema file '{schema_file}': {e}")
            sys.exit(1)
    
    else:
        print("Usage:")
        print("  python orchestrate_v1.py                          # Default test case")
        print("  python orchestrate_v1.py 'text' schema.json       # Custom text and schema file")
        print("  python orchestrate_v1.py -                        # Read JSON from stdin")
        sys.exit(1)