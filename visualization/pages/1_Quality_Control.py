import streamlit as st
import pandas as pd
import glob
import os
import re
import uuid

st.set_page_config(
    page_title="Quality Control - Brieflow Analysis",
    page_icon=":microscope:",
    layout="wide",
)

st.title("Quality Control")
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


def extract_well_id(file_path):
    r"""
    Extract well identifier (format: W-[A-Z]\d+) from a file path.

    Args:
        file_path: Path to the file

    Returns:
        Well ID if found, None otherwise
    """
    match = re.search(r'(W-[A-Z]\d+)', file_path)
    return match.group(1) if match else None


def extract_plate_id(file_path):
    r"""
    Extract plate identifier (format: P-\d+) from a file path.

    Args:
        file_path: Path to the file

    Returns:
        Plate ID if found, None otherwise
    """
    match = re.search(r'(P-\d+)', file_path)
    return match.group(1) if match else None


def extract_metric_name(file_path):
    """
    Extract metric name from the basename (the part after the last "__").

    Args:
        file_path: Path to the file

    Returns:
        Metric name if found, None otherwise
    """
    base = os.path.splitext(os.path.basename(file_path))[0]
    if "__" in base:
        return base.split("__")[-1]
    return None


def extract_features(root_dir, files, omit_folders=None):
    """
    Extract features from PNG and TSV files including path information.

    Args:
        root_dir: Root directory to use as base for relative paths
        files: List of file paths to process
        omit_folders: Set of folder names to omit from directory levels (default: {'eval'})

    Returns:
        DataFrame containing extracted features and path information
    """
    if omit_folders is None:
        omit_folders = {'eval'}

    features = []

    for file in files:
        # Convert to relative path
        rel_path = os.path.relpath(file, root_dir)
        dirname = os.path.dirname(rel_path)
        basename = os.path.basename(file)
        name, ext = os.path.splitext(basename)

        # Basic feature dictionary with new fields
        feature = {
            'file_path': rel_path,
            'dir': dirname,
            'basename': name,
            'ext': ext.lstrip('.')  # Remove the leading dot from extension
        }

        # Extract identifiers and metadata from file path
        feature['well_id'] = extract_well_id(rel_path)
        feature['plate_id'] = extract_plate_id(rel_path)
        feature['metric_name'] = extract_metric_name(rel_path)

        # Add directory levels, skipping omitted folders
        parts = dirname.split(os.sep)
        parts = [part for part in parts if part not in omit_folders]  # Filter out omitted parts
        for i, part in enumerate(parts):
            feature[f'dir_level_{i}'] = part
        features.append(feature)

    return pd.DataFrame(features)


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
SIDE_BAR_FILTERS = True

# Load the data
files = find_eval_files(ROOT_DIR)
df = extract_features(ROOT_DIR, files)  # Uses default omit_folders={'eval'}

# Apply filters to the dataframe
filtered_df = df.copy()

# Filter for valid dir_level_0 values
valid_level_0 = ['phenotype', 'merge', 'sbs']
filtered_df = filtered_df[filtered_df['dir_level_0'].isin(valid_level_0)]


# Create columns for filters
if SIDE_BAR_FILTERS:
    st.sidebar.title("Filters")
    col1 = st.sidebar
    col2 = st.sidebar
    col3 = st.sidebar
    col4 = st.sidebar
    col5 = st.sidebar
else:
    col1, col2, col3, col4, col5 = st.columns(5)

# Create filters using the helper function
selected_dir_level_0 = create_filter_radio(filtered_df, 'dir_level_0', col1)
filtered_df = apply_filter(filtered_df, 'dir_level_0', selected_dir_level_0)

selected_dir_level_1 = create_filter_radio(filtered_df, 'dir_level_1', col2)
filtered_df = apply_filter(filtered_df, 'dir_level_1', selected_dir_level_1)

selected_plate = create_filter_radio(filtered_df, 'plate_id', col3, "Filter by plate")
filtered_df = apply_filter(filtered_df, 'plate_id', selected_plate)

selected_well = create_filter_radio(filtered_df, 'well_id', col4, "Filter by well")
filtered_df = apply_filter(filtered_df, 'well_id', selected_well)

selected_metric = create_filter_radio(filtered_df, 'metric_name', col5, "Filter by metric")
filtered_df = apply_filter(filtered_df, 'metric_name', selected_metric)

# Display the filtered dataframe (debug)
# st.dataframe(filtered_df)

# Group by directory and basename
grouped = filtered_df.groupby(['dir', 'basename'])

# Iterate through each group
for (dir_name, base_name), group_df in grouped:
    with st.container():
        st.markdown(f"### Group: {dir_name} - {base_name}")
        
        # Count only the items we'll actually display
        display_items = []
        for _, row in group_df.iterrows():
            has_png = any(row['ext'] == 'png' for _, row in group_df.iterrows())
            if row['ext'] == 'png' or (row['ext'] == 'tsv' and not has_png):
                display_items.append(row)
        
        # Create columns based on actual display items
        cols = st.columns(min(3, len(display_items)))
        
        for idx, row in enumerate(display_items):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                # Check if this group has both PNG and TSV
                has_png = any(row['ext'] == 'png' for _, row in group_df.iterrows())
                has_tsv = any(row['ext'] == 'tsv' for _, row in group_df.iterrows())
                
                if row['ext'] == 'png':
                    # Always show PNG if it exists
                    try:
                        st.image(os.path.join(ROOT_DIR, row['file_path']), 
                                caption=f"{row['metric_name']} - {row['well_id']}")
                    except Exception as e:
                        st.error(f"Could not load image: {row['file_path']}")
                        st.error(str(e))
                    
                    # If there's a corresponding TSV, add download link
                    if has_tsv:
                        tsv_row = group_df[group_df['ext'] == 'tsv'].iloc[0]
                        tsv_path = os.path.join(ROOT_DIR, tsv_row['file_path'])
                        with open(tsv_path, 'rb') as f:
                            st.download_button(
                                label="Download TSV data",
                                data=f,
                                file_name=os.path.basename(tsv_path),
                                key=f"download_{str(uuid.uuid4())}"
                            )
                
                elif row['ext'] == 'tsv' and not has_png:
                    # Only show TSV if there's no PNG
                    try:
                        tsv_data = pd.read_csv(os.path.join(ROOT_DIR, row['file_path']), sep='\t')
                        st.dataframe(tsv_data)
                    except Exception as e:
                        st.error(f"Error reading TSV file: {e}")
        
        st.markdown("---")  # Add a separator between groups


