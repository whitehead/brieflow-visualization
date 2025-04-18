# Brieflow Streamlit Visualization

This project provides a Streamlit-based interface for interactive exploration of analysis results.

## Structure

- `setup-venv.sh` — Configures a venv and installs dependencies
- `run-visualization.sh` — Script to run the visualization app normally
- `analysis_root/` — Symlink to analysis data (We expect this to contain sbs, phenotype, merge, and cluster folders)
- `visualization/` — The streamlit application
  - `Home.py` — The entry point for the streamlit application
  - `pages/` — Additional Streamlit pages
    - `1_Quality_Control.py` — Interactive visualization of pipeline QC metrics and filtering
    - `2_Cluster.py` — PHATE and Leiden clustering analysis visualization
    - `3_Config.py` — System configuration and git repository information

## Setup

1. Create virtual environment and install dependencies
   ```sh
   ./setup-venv.sh
   ```
2. Configure the analysis root directory:
   - Option 1: Set the `BRIEFLOW_ANALYSIS_ROOT` environment variable
     ```sh
     export BRIEFLOW_ANALYSIS_ROOT=/path/to/analysis_root
     ```
   - Option 2: Create a symlink (if environment variable is not set)
     ```sh
     ln -s /path/to/analysis_root analysis_root
     ```

## Running
4. Run the app:
   ```
   ./run-visualization.sh
   ```
