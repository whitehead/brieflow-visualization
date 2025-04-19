import streamlit as st
import pandas as pd
import os
from src.filesystem import FileSystem
from src.rendering import VisualizationRenderer
from src.filtering import create_filter_radio, apply_filter

st.set_page_config(
    page_title="Montages - Brieflow Analysis",
    page_icon=":microscope:",
    layout="wide",
)

st.title("Montages")
st.markdown("View and analyze montages from the brieflow pipeline")

@st.cache_data
def load_data(root_dir):
    # Find all montage files
    files = FileSystem.find_files(
        root_dir,
        include_all=['montages'],
        extensions=['png']
    )
    
    # Extract features from the file paths
    filtered_df = FileSystem.extract_features(root_dir, files)
    
    # Add additional columns based on the file path structure
    filtered_df['gene'] = filtered_df['file_path'].apply(lambda x: x.split('/')[-3])
    filtered_df['guide'] = filtered_df['file_path'].apply(lambda x: x.split('/')[-2])
    filtered_df['channel'] = filtered_df['file_path'].apply(lambda x: x.split('/')[-1].split('__')[0])
    
    return filtered_df

# Configuration
ROOT_DIR = os.getenv('BRIEFLOW_ANALYSIS_ROOT', '../analysis_root')

# Load the data
filtered_df = load_data(ROOT_DIR)

st.sidebar.title("Filters")

# Create gene filter with search functionality
all_genes = sorted(filtered_df['gene'].unique())
selected_genes = st.sidebar.multiselect(
    "Select Genes",
    all_genes,
    default=[],
    help="Search and select one or more genes"
)

# Apply gene filter
if selected_genes:
    filtered_df = filtered_df[filtered_df['gene'].isin(selected_genes)]

# Create other filters using the helper function (TOo many!)
#selected_guide = create_filter_radio(filtered_df, 'guide', st.sidebar, "Guide")
#filtered_df = apply_filter(filtered_df, 'guide', selected_guide)

selected_channel = create_filter_radio(filtered_df, 'channel', st.sidebar, "Channel")
filtered_df = apply_filter(filtered_df, 'channel', selected_channel)

# Display the filtered dataframe (debug)
# st.dataframe(filtered_df)

if selected_genes: 
    # We cannot show the unflitered list. You must pick at least one gene.j
    VisualizationRenderer.display_plots_and_tables(filtered_df, ROOT_DIR) 