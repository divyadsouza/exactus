## Activate venv
  cd /raid/dmdsouza/exactus
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
## Install dependencies
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
  pip install -e .
## Run with 
jupyter nbconvert --to notebook --execute nuextract_benchmark.ipynb \
--output nuextract_benchmark_output.ipynb \
--ExecutePreprocessor.timeout=86400