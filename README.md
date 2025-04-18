# Brieflow Streamlit Visualization

This project provides a Streamlit-based interface for interactive exploration of analysis results.

## Structure

- `setup-venv.sh` — Configures a venv and installs dependencies
- `run-visualization.sh` — Script to run the visualization app normally
- `analysis_root/` — Symlink to analysis data (We expect this to contain sbs, phenotype, merge, and cluster folders)
- `visualization/` — The streamlit application
  - `Home.py` — The entry point for the streamlit application
  - `pages/` — (Optional) Additional Streamlit pages

## Setup

1. Create and activate a virtual environment
   ```sh
   ./setup-venv.sh
   ```
2. Ensure `analysis_root/` points to your analysis results
   ```sh
   ln -s /path/to/analysis_root analysis_root
   ```

## Running
4. Run the app:
   ```sh
   ./run-visualization.sh
   ```
