"""
Run this on the remote machine to check which dependencies are already installed.
Usage: python check_dependencies.py
"""

import importlib
import sys

packages = {
    # Core ML
    "torch":            "torch",
    "torchvision":      "torchvision",
    "transformers":     "transformers",
    "accelerate":       "accelerate",
    "pydantic":         "pydantic",
    # HuggingFace
    "huggingface_hub":  "huggingface_hub",
    "datasets":         "datasets",
    # Data handling
    "pyarrow":          "pyarrow",
    "jsonlines":        "jsonlines",
    "yaml":             "pyyaml",
    "dotenv":           "python-dotenv",
    # Notebook & tracking
    "jupyter":          "jupyter",
    "mlflow":           "mlflow",
    "tensorboard":      "tensorboard",
    "tqdm":             "tqdm",
    # Model optimization
    "onnx":             "onnx",
    "onnxruntime":      "onnxruntime-gpu",
    # Code quality
    "black":            "black",
    "ruff":             "ruff",
    "mypy":             "mypy",
    "isort":            "isort",
    "pytest":           "pytest",
    "pytest_cov":       "pytest-cov",
}

installed = []
missing = []

for import_name, pip_name in packages.items():
    try:
        mod = importlib.import_module(import_name)
        version = getattr(mod, "__version__", "unknown version")
        installed.append((pip_name, version))
    except ImportError:
        missing.append(pip_name)

print(f"\n{'='*50}")
print(f"Python: {sys.version}")
print(f"{'='*50}")

print(f"\n✅ INSTALLED ({len(installed)}):")
for name, version in installed:
    print(f"  {name:<25} {version}")

print(f"\n❌ MISSING ({len(missing)}):")
for name in missing:
    print(f"  {name}")

# Extra: check if torch can see the GPUs
if any(n == "torch" for n, _ in installed):
    import torch
    print(f"\n🔍 TORCH CUDA CHECK:")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    print(f"  GPU count:      {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")

print()
