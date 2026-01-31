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
                # Check for hallucinations: output should only contain info from input
                # This is hard to automate perfectly, but check if output has words not in input
                input_text = entry['input'].lower()
                output_text = output.lower()
                # Simple check: if output has numbers or strings not in input, but this is approximate
                # For now, just structural validation
            except json.JSONDecodeError:
                errors.append(f"Line {line_num}: Invalid JSONL entry")
    return errors

# Check all files
data_dir = Path('./data/training')
for file in data_dir.glob('*.jsonl'):
    print(f"Checking {file.name}")
    errs = check_file(file)
    if errs:
        for err in errs:
            print(f"  {err}")
    else:
        print("  All good")

print("Validation complete.")