import streamlit as st
import pandas as pd
import glob
import os

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from src.filesystem import FileSystem
from src.rendering import VisualizationRenderer
from src.filtering import create_filter_radio, apply_filter

# =====================
# CONSTANTS
ANALYSIS_ROOT = os.getenv('BRIEFLOW_ANALYSIS_ROOT', '../analysis_root')

# Common hover data columns
HOVER_COLUMNS = ['gene_symbol_0', 'cluster', 'Gene Names', 'source']

# Indices for accessing customdata array
GENE_SYMBOL_INDEX = 0
CLUSTER_INDEX = 1
GENE_NAMES_INDEX = 2
SOURCE_INDEX = 3

# =====================
# FUNCTIONS



# Load and merge cluster TSV files
@st.cache_data
def load_cluster_data():
    # Find all relevant TSV files
    tsv_files = glob.glob(f"{ANALYSIS_ROOT}/cluster/**/*__phate_leiden_uniprot.tsv", recursive=True)
    
    # Read each file and add source attribute
    dfs = []
    for file_path in tsv_files:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        df = pd.read_csv(file_path, sep='\t')
        df['source'] = base_name
        dfs.append(df)
    
    # Concatenate all dataframes
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# Create a scatter plot with consistent settings
def create_scatter_plot(data, color_column, color_discrete_sequence, color_discrete_map=None):
    fig = px.scatter(
        data,
        x='PHATE_0',
        y='PHATE_1',
        color=color_column,
        hover_data=HOVER_COLUMNS,
        title='PHATE Visualization',
        width=1000,
        height=800,
        color_discrete_sequence=color_discrete_sequence,
        color_discrete_map=color_discrete_map or {}
    )
    
    # Apply hover template to all traces
    for trace in fig.data:
        trace.hovertemplate = (
            "PHATE_0=%{x}<br>"
            "PHATE_1=%{y}<br>"
            f"gene_symbol_0=%{{customdata[{GENE_SYMBOL_INDEX}]}}<br>"
            f"cluster=%{{customdata[{CLUSTER_INDEX}]}}<br>"
            f"Gene Names=%{{customdata[{GENE_NAMES_INDEX}]}}<br>"
            f"source=%{{customdata[{SOURCE_INDEX}]}}<br>"
            "<extra></extra>"
        )
    
    return fig

# Extract item value from selected point
def get_item_value_from_point(selected_point, groupby_column):
    # Get value from customdata which contains the hover_data values
    if 'customdata' in selected_point and len(selected_point['customdata']) > 0:
        if groupby_column in HOVER_COLUMNS:
            col_index = HOVER_COLUMNS.index(groupby_column)
            if col_index < len(selected_point['customdata']):
                return str(selected_point['customdata'][col_index])
    
    # Fallback to legendgroup as a last resort (for compatibility)
    if 'legendgroup' in selected_point:
        return selected_point['legendgroup']
        
    return None

# Helper function to create a scatter trace
def make_scatter_trace(x, y, marker, text, customdata, name, showlegend, color=None):
    hovertemplate = (
        "PHATE_0=%{x}<br>"
        "PHATE_1=%{y}<br>"
        f"gene_symbol_0=%{{customdata[{GENE_SYMBOL_INDEX}]}}<br>"
        f"cluster=%{{customdata[{CLUSTER_INDEX}]}}<br>"
        f"Gene Names=%{{customdata[{GENE_NAMES_INDEX}]}}<br>"
        f"source=%{{customdata[{SOURCE_INDEX}]}}<br>"
        "<extra></extra>"
    )
    # Optionally override color in marker
    if color is not None:
        marker = dict(marker, color=color)
    return go.Scattergl(
        x=x,
        y=y,
        mode='markers',
        marker=marker,
        text=text,
        customdata=customdata,
        name=name,
        hovertemplate=hovertemplate,
        showlegend=showlegend,
    )

# =====================
# MAIN CODE

st.set_page_config(
    page_title="Cluster Analysis - Brieflow Analysis",
    layout="wide"
)

st.title("Cluster Analysis")

# Initialize session state for selected item and grouping column if they don't exist
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

if 'groupby_column' not in st.session_state:
    st.session_state.groupby_column = 'cluster'

# Load the data
cluster_data = load_cluster_data()

# Display the data
if not cluster_data.empty:
    # Create a sidebar with controls
    with st.sidebar:
        # Dropdown to select the grouping column
        available_columns = ['source', 'cluster']
        # Add any other numeric or categorical columns that might be useful for grouping
        for col in cluster_data.columns:
            if col not in available_columns and cluster_data[col].nunique() < 30:
                available_columns.append(col)
        
        selected_column = st.selectbox(
            "Group by column", 
            available_columns, 
            index=available_columns.index(st.session_state.groupby_column)
        )
        
        # Update session state if the grouping column has changed
        if selected_column != st.session_state.groupby_column:
            st.session_state.groupby_column = selected_column
            st.session_state.selected_item = None  # Reset selection when changing grouping
            st.rerun()
        
        # Show selected item and clear button if an item is selected
        if st.session_state.selected_item:
            st.write(f"Selected {st.session_state.groupby_column}: {st.session_state.selected_item}")
            if st.button("Clear Selection"):
                st.session_state.selected_item = None
                st.rerun()
    
    # Always treat grouping column as categorical for discrete color maps
    if st.session_state.groupby_column in cluster_data.columns:
        cluster_data[st.session_state.groupby_column] = cluster_data[st.session_state.groupby_column].astype(str)
    
    # Build a color map using the group names and the color palette
    group_names = cluster_data[st.session_state.groupby_column].unique()
    
    # Create a color palette optimized for visibility on a black background
    def get_optimized_color_palette(num_colors):
        
        # Use a perceptually uniform colormap that works well on dark backgrounds
        # Options: 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
        colormap_name = 'turbo'  # Good visibility on dark backgrounds
        
        # Get evenly spaced colors from the colormap
        cmap = plt.get_cmap(colormap_name)
        colors = [mcolors.rgb2hex(cmap(i / (num_colors - 1 if num_colors > 1 else 1))) 
                 for i in range(num_colors)]
        
        return colors
    
    # Get enough colors for all groups
    optimized_palette = get_optimized_color_palette(len(group_names))
    color_map = {group: optimized_palette[i] for i, group in enumerate(group_names)}
    
    # Always compute selected_data and other_data
    selected_item = st.session_state.get("selected_item", None)
    groupby_column = st.session_state.groupby_column
    selected_data = cluster_data[cluster_data[groupby_column].astype(str) == str(selected_item)]
    other_data = cluster_data[cluster_data[groupby_column].astype(str) != str(selected_item)]

    # Use plotly.graph_objects for full control
    fig = go.Figure()

    # Plot each group as its own trace so all appear in the legend
    # First phase: Add unselected points (all in gray)
    if selected_item is not None:
        for group in group_names:
            if group != selected_item:
                group_df = cluster_data[cluster_data[groupby_column] == group]
                marker = dict(
                    color='gray',  # All unselected points are gray
                    size=8,
                    opacity=0.3,
                )
                fig.add_trace(make_scatter_trace(
                    x=group_df['PHATE_0'],
                    y=group_df['PHATE_1'],
                    marker=marker,
                    text=group_df['gene_symbol_0'],
                    customdata=group_df[HOVER_COLUMNS],
                    name=str(group),
                    showlegend=True,
                ))
        
        # Second phase: Add selected points on top
        for group in group_names:
            if group == selected_item:
                group_df = cluster_data[cluster_data[groupby_column] == group]
                marker = dict(
                    color=color_map[group],
                    size=10,
                    opacity=1.0,
                    line=dict(width=2, color='black')
                )
                fig.add_trace(make_scatter_trace(
                    x=group_df['PHATE_0'],
                    y=group_df['PHATE_1'],
                    marker=marker,
                    text=group_df['gene_symbol_0'],
                    customdata=group_df[HOVER_COLUMNS],
                    name=str(group),
                    showlegend=True,
                ))
    else:
        # No selection: add all points with their original colors
        for group in group_names:
            group_df = cluster_data[cluster_data[groupby_column] == group]
            marker = dict(
                color=color_map[group],
                size=8,
                opacity=1.0,
            )
            fig.add_trace(make_scatter_trace(
                x=group_df['PHATE_0'],
                y=group_df['PHATE_1'],
                marker=marker,
                text=group_df['gene_symbol_0'],
                customdata=group_df[HOVER_COLUMNS],
                name=str(group),
                showlegend=True,
            ))
    
    # Update layout
    fig.update_layout(
        hovermode='closest',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title='',
        width=1000,
        height=800,
    )

    # Display the plot with click event handling
    event = st.plotly_chart(fig, use_container_width=True, key="cluster_plot", on_select="rerun")
    
    # Handle click events
    if event.selection and event.selection.points:
        selected_point = event.selection.points[0]
        
        # Get the item value from the selected point
        item_value = get_item_value_from_point(selected_point, st.session_state.groupby_column)
        
        # Update session state if the item has changed
        if item_value and st.session_state.selected_item != item_value:
            st.session_state.selected_item = item_value
            st.rerun()
    
    # Display data overview
    st.write("Cluster Data Overview")
    
    # If an item is selected, filter the dataframe
    if st.session_state.selected_item:
        filtered_data = cluster_data[cluster_data[st.session_state.groupby_column] == st.session_state.selected_item]
        st.dataframe(filtered_data)
    else:
        st.dataframe(cluster_data)
else:
    st.write("No cluster data files found.")

# Plots and tables
st.write("Plots and Tables")
st.sidebar.title("Filters")

@st.cache_data
def load_plots_and_tables_data():
    cluster_plots_dir = os.path.join(ANALYSIS_ROOT,'cluster')
    cluster_plot_files = FileSystem.find_files(cluster_plots_dir, include_all=['plots'], extensions=['png', 'tsv'])

    filtered_df = FileSystem.extract_features(cluster_plots_dir, cluster_plot_files)
    return filtered_df, cluster_plots_dir

filtered_df, cluster_plots_dir = load_plots_and_tables_data()

selected_dir_level_0 = create_filter_radio(filtered_df, 'dir_level_0', st.sidebar, "A")
filtered_df = apply_filter(filtered_df, 'dir_level_0', selected_dir_level_0)

selected_dir_level_1 = create_filter_radio(filtered_df, 'dir_level_1', st.sidebar, "B", include_all=False)
filtered_df = apply_filter(filtered_df, 'dir_level_1', selected_dir_level_1)

#selected_dir_level_2 = create_filter_radio(filtered_df, 'dir_level_2', st.sidebar, "C")
#filtered_df = apply_filter(filtered_df, 'dir_level_2', selected_dir_level_2)

selected_metric = create_filter_radio(filtered_df, 'metric_name', st.sidebar, "Metric")
filtered_df = apply_filter(filtered_df, 'metric_name', selected_metric)

VisualizationRenderer.display_plots_and_tables(filtered_df, cluster_plots_dir)
