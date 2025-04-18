import streamlit as st
import pandas as pd
import glob

st.markdown("Review the quality control metrics from the brieflow pipeline")


def find_eval_files(root_dir):
    """
    Find all PNG and TSV files in the directory tree that contain 'eval' in their path.

    Args:
        root_dir: The root directory to search in

    Returns:
        A list of file paths that contain 'eval' in their path
    """
    # Find all PNG and TSV files in the directory tree
    png_files = glob.glob(f"{root_dir}/**/*.png", recursive=True)
    tsv_files = glob.glob(f"{root_dir}/**/*.tsv", recursive=True)

    # Combine the lists
    all_files = png_files + tsv_files

    # Filter for files containing "eval" in their path (not just basename)
    eval_files = [f for f in all_files if "eval" in f]

    # Return the array of matching file paths
    return eval_files

ROOT_DIR = "../analysis_root"
files = find_eval_files(ROOT_DIR)

files