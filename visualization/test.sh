#!/bin/bash
# Change to script directory
cd "$(dirname "$0")"

# Source the virtual environment
source ../venv/bin/activate

# Run pytest from this directory
pytest tests/ -v
