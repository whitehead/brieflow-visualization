import streamlit as st
import pandas as pd
import os
import uuid
from src.filesystem import FileSystem
from src.rendering import VisualizationRenderer

st.set_page_config(
    page_title="Quality Control - Brieflow Analysis",
    page_icon=":microscope:",
    layout="wide",
)

st.title("Quality Control")
st.markdown("Review the quality control metrics from the brieflow pipeline")

@st.cache_data
def load_data(root_dir):
    global filtered_df
    # Apply filters directly during file discovery for better performance
    # Filter for dir_level_0 in ['phenotype', 'merge', 'sbs', 'aggregate'] and dir_level_1 == 'eval'
    files = FileSystem.find_files(
        root_dir, 
        include_any=['phenotype', 'merge', 'sbs', 'aggregate'],
        include_all=['eval'],
        extensions=['png', 'tsv']
    )
    filtered_df = FileSystem.extract_features(root_dir, files)
    return filtered_df


def create_filter_radio(df, column, container, label=None):
    """
    Create a radio button for filtering based on a column.

    Args:
        df: DataFrame containing the data
        column: Column name to filter on
        container: Streamlit container to place the radio button in
        label: Label for the radio button (defaults to "Filter by {column}")

    Returns:
        Selected value from the radio button
    """
    if label is None:
        label = f"Filter by {column}"

    selected_value = "All"
    if column in df.columns:
        values = df[column].dropna().unique().tolist()
        values.sort()  # Sort alphabetically
        if values:
            selected_value = container.radio(label, ["All"] + values)

    return selected_value

def apply_filter(df, column, selected_value):
    """
    Apply a filter to the dataframe based on the selected value.

    Args:
        df: DataFrame to filter
        column: Column name to filter on
        selected_value: Value to filter for

    Returns:
        Filtered DataFrame
    """
    if selected_value != "All" and column in df.columns:
        return df[df[column] == selected_value]
    return df



# Configuration
ROOT_DIR = os.getenv('BRIEFLOW_ANALYSIS_ROOT', '../analysis_root')

# Load the data
filtered_df = load_data(ROOT_DIR)

st.sidebar.title("Filters")

# Create filters using the helper function
selected_dir_level_0 = create_filter_radio(filtered_df, 'dir_level_0', st.sidebar, "Phase")
filtered_df = apply_filter(filtered_df, 'dir_level_0', selected_dir_level_0)

# dir_level_1 is always "eval", so we don't need to create a filter

selected_dir_level_2 = create_filter_radio(filtered_df, 'dir_level_2', st.sidebar, "Subgroup")
filtered_df = apply_filter(filtered_df, 'dir_level_2', selected_dir_level_2)

selected_plate = create_filter_radio(filtered_df, 'plate_id', st.sidebar, "Plate")
filtered_df = apply_filter(filtered_df, 'plate_id', selected_plate)

selected_well = create_filter_radio(filtered_df, 'well_id', st.sidebar, "Well")
filtered_df = apply_filter(filtered_df, 'well_id', selected_well)

selected_metric = create_filter_radio(filtered_df, 'metric_name', st.sidebar, "Metric")
filtered_df = apply_filter(filtered_df, 'metric_name', selected_metric)

# Display the filtered dataframe (debug)
# st.dataframe(filtered_df)

VisualizationRenderer.display_plots_and_tables(filtered_df, ROOT_DIR)
