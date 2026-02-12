#!/usr/bin/env python3
import json, subprocess, tempfile, os

text = "From: alice@company.com\nTo: bob@client.com\nDate: March 10, 2024"
schema = {"sender": "string", "recipient": "string", "date": "string"}

print("Testing orchestrate_v1.py with training data:")
print("Text:", text)
print("Schema:", schema)

with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(schema, f)
    schema_file = f.name

try:
    result = subprocess.run(["python", "orchestrate_v1.py", text, schema_file], capture_output=True, text=True)
    print("\nOutput:")
    print(result.stdout)
finally:
    os.unlink(schema_file)
