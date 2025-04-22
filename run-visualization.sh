#!/usr/bin/env bash

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Default port and config
export STREAMLIT_CONFIG=".streamlit/config.toml"

# Start Streamlit server, force bind to 0.0.0.0
cd visualization
exec streamlit run Overview.py --server.address=0.0.0.0 "$@"
