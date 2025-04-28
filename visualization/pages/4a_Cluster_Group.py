import streamlit as st
import pandas as pd
import glob
import os
import uuid

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
HOVER_COLUMNS = ['gene_symbol_0', 'cluster', 'cell_count', 'source']

# Indices for accessing customdata array
GENE_SYMBOL_INDEX = 0
CLUSTER_INDEX = 1
CELL_COUNT_INDEX = 2
SOURCE_INDEX = 3

# =====================
# FUNCTIONS



# Load and merge cluster TSV files
@st.cache_data
def load_cluster_data():
    # Find all relevant TSV files
    cluster_root = os.path.join(ANALYSIS_ROOT, 'cluster')
    tsv_files = glob.glob(f"{cluster_root}/**/*__phate_leiden_clustering.tsv", recursive=True)

    # Read each file and add source attribute
    dfs = []
    for file_path in tsv_files:
        rel_path = os.path.relpath(file_path, cluster_root)
        dirname = os.path.dirname(rel_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        df = pd.read_csv(file_path, sep='\t')
        df['source'] = base_name
        df['leiden_resolution'] = FileSystem.extract_leiden_resolution(rel_path)
        parts = dirname.split(os.sep)
        for i, part in enumerate(parts):
            df[f'dir_level_{i}'] = part
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
            f"cell_count=%{{customdata[{CELL_COUNT_INDEX}]}}<br>"
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
        f"cell_count=%{{customdata[{CELL_COUNT_INDEX}]}}<br>"
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

@st.cache_data
def load_montage_data(root_dir, gene_name):
    # Find all montage files
    files = FileSystem.find_files(
        root_dir + "/" + gene_name,
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

def display_gene_montages(gene_montages_root, gene):
    gene_dir = os.path.join(gene_montages_root, gene)
    if not os.path.exists(gene_dir):
        st.warning(f"No montage directory found for gene {gene}")
    else:
        montage_data = load_montage_data(gene_montages_root, gene)
        if montage_data.empty:
            st.write(f"No montage data found for gene {gene}")
        else:
            # Add filters for guide and channel
            available_guides = sorted(montage_data['guide'].unique())
            
            # Initialize session state for selected guide if it doesn't exist
            if f'selected_guide_{gene}' not in st.session_state:
                st.session_state[f'selected_guide_{gene}'] = None
            
            # Define a callback for when the guide dropdown changes
            def on_guide_select():
                st.session_state[f'selected_guide_{gene}'] = st.session_state[f"guide_dropdown_{gene}"]
            
            # Determine the index of the selected guide in the dropdown
            selected_index = 0
            selected_guide = st.session_state.get(f"selected_guide_{gene}", None)
            
            if selected_guide in available_guides:
                selected_index = available_guides.index(selected_guide)
            elif available_guides:
                # If no guide is selected yet or the previously selected guide is not available, select the first one
                selected_guide = available_guides[0]
                st.session_state[f'selected_guide_{gene}'] = selected_guide
            
            # Create a dropdown to select a guide
            selected_guide = st.selectbox(
                "Select Guide",
                available_guides,
                index=selected_index,
                key=f"guide_dropdown_{gene}",  # Use a stable key based on the selected gene
                on_change=on_guide_select
            )

            # Filter the data based on selections
            filtered_montage_data = montage_data[
                (montage_data['guide'] == selected_guide)
                ]

            if len(filtered_montage_data) > 0:
                # Display each image in the filtered data
                for _, row in filtered_montage_data.iterrows():
                    # Construct the full path including the montages directory
                    image_path = os.path.join(gene_montages_root, row['file_path'])

                    try:
                        if os.path.exists(image_path):
                            st.image(image_path, caption=f"{gene} - {selected_guide} - {row['channel']}")
                        else:
                            st.error(f"Image file not found: {image_path}")
                    except Exception as e:
                        st.error(f"Error displaying image: {str(e)}")

                # Add download button for overlay TIFF
                overlay_tiff_path = os.path.join(
                    gene_montages_root,
                    gene,
                    selected_guide,
                    f"overlay_montage.tiff"
                )

                if os.path.exists(overlay_tiff_path):
                    with open(overlay_tiff_path, 'rb') as f:
                        st.download_button(
                            label="Download Overlay TIFF",
                            data=f,
                            file_name=f"{gene}_{selected_guide}_{row['channel']}_overlay.tiff",
                            key=f"download_{gene}_{selected_guide}_{row['channel']}_{uuid.uuid4()}"
                        )
                else:
                    st.warning(f"No overlay tiff found: {overlay_tiff_path}")
            else:
                st.warning(f"No image found for {gene} - {selected_guide}")

# =====================
# MAIN CODE

st.set_page_config(
    page_title="Cluster Analysis - Brieflow Analysis",
    layout="wide"
)

# Initialize session state for selected item and grouping column if they don't exist
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

if 'groupby_column' not in st.session_state:
    st.session_state.groupby_column = 'cluster'

# Initialize session state for selected gene if it doesn't exist
if 'selected_gene' not in st.session_state:
    st.session_state.selected_gene = None

# Initialize session state for selected guide if it doesn't exist
if 'selected_guide' not in st.session_state:
    st.session_state.selected_guide = None

# Initialize session state for zoom coordinates if they don't exist
if 'zoom_xrange' not in st.session_state:
    st.session_state.zoom_xrange = None
if 'zoom_yrange' not in st.session_state:
    st.session_state.zoom_yrange = None

def display_cluster(cluster_data, container=st.container()):
    r'''
    :param cluster_data: a dataframe from load_cluster_data
    :param container: an st.container or equivalent that UI elements will be added to
    '''
    global st
    # Display the data
    if not cluster_data.empty:
        # Create a sidebar with controls
        with st.sidebar:
            # Dropdown to select the grouping column
            available_columns = ['source', 'cluster']
            # Add any other numeric or categorical columns that might be useful for grouping
            # for col in cluster_data.columns:
            #     if col not in available_columns and cluster_data[col].nunique() < 30:
            #         available_columns.append(col)

            selected_column = st.selectbox(
                "Group by column",
                available_columns,
                index=available_columns.index(st.session_state.groupby_column)
            )

            # Update session state if the grouping column has changed
            if selected_column != st.session_state.groupby_column:
                st.session_state.groupby_column = selected_column
                st.session_state.selected_item = None  # Reset selection when changing grouping
                st.session_state.selected_gene = None  # Reset selected gene when changing grouping
                st.rerun()

            # Show selected item and clear button if an item is selected
            if st.session_state.selected_item:
                st.write(f"Selected {st.session_state.groupby_column}: {st.session_state.selected_item}")
                if st.button("Clear Selection"):
                    st.session_state.selected_item = None
                    st.session_state.selected_gene = None
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
                    
                    # Get the selected gene if any
                    selected_gene = st.session_state.get("selected_gene", None)
                    
                    # Split the dataframe into selected gene and other genes
                    selected_gene_df = group_df[group_df['gene_symbol_0'] == selected_gene] if selected_gene else pd.DataFrame()
                    other_genes_df = group_df[group_df['gene_symbol_0'] != selected_gene] if selected_gene else group_df
                    
                    # Add other genes in the selected group
                    if not other_genes_df.empty:
                        marker = dict(
                            color=color_map[group],
                            size=10,
                            opacity=1.0,
                            line=dict(width=2, color='black')
                        )
                        fig.add_trace(make_scatter_trace(
                            x=other_genes_df['PHATE_0'],
                            y=other_genes_df['PHATE_1'],
                            marker=marker,
                            text=other_genes_df['gene_symbol_0'],
                            customdata=other_genes_df[HOVER_COLUMNS],
                            name=str(group),
                            showlegend=True,
                        ))
                    
                    # Add the selected gene with special highlighting
                    if not selected_gene_df.empty:
                        marker = dict(
                            color=color_map[group],  # Use the cluster's color instead of red
                            size=15,      # Larger size
                            opacity=1.0,
                            symbol='circle',  # Filled circle
                            line=dict(width=3, color='white')  # White border for contrast
                        )
                        fig.add_trace(make_scatter_trace(
                            x=selected_gene_df['PHATE_0'],
                            y=selected_gene_df['PHATE_1'],
                            marker=marker,
                            text=selected_gene_df['gene_symbol_0'],
                            customdata=selected_gene_df[HOVER_COLUMNS],
                            name=f"{selected_gene} (Selected)",
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
        
        # Apply saved zoom coordinates if they exist
        if st.session_state.zoom_xrange is not None and st.session_state.zoom_yrange is not None:
            fig.update_layout(
                xaxis=dict(range=st.session_state.zoom_xrange),
                yaxis=dict(range=st.session_state.zoom_yrange)
            )

        # Display the plot with click event handling
        event = st.plotly_chart(fig, use_container_width=True, key="cluster_plot", on_select="rerun")

        # Handle click events
        if event.selection and event.selection.points:
            selected_point = event.selection.points[0]

            # Get the item value from the selected point
            item_value = get_item_value_from_point(selected_point, st.session_state.groupby_column)
            
            # Get the gene value from the selected point
            gene_value = None
            if 'customdata' in selected_point and len(selected_point['customdata']) > 0:
                if GENE_SYMBOL_INDEX < len(selected_point['customdata']):
                    gene_value = str(selected_point['customdata'][GENE_SYMBOL_INDEX])

            # Update session state if the item has changed
            if item_value and (st.session_state.selected_item != item_value or st.session_state.selected_gene != gene_value):
                st.session_state.selected_item = item_value
                st.session_state.selected_gene = gene_value
                
                # Store current zoom state before rerunning
                if hasattr(event, 'relayoutData') and event.relayoutData:
                    if 'xaxis.range[0]' in event.relayoutData and 'xaxis.range[1]' in event.relayoutData:
                        st.session_state.zoom_xrange = [
                            event.relayoutData['xaxis.range[0]'],
                            event.relayoutData['xaxis.range[1]']
                        ]
                    if 'yaxis.range[0]' in event.relayoutData and 'yaxis.range[1]' in event.relayoutData:
                        st.session_state.zoom_yrange = [
                            event.relayoutData['yaxis.range[0]'],
                            event.relayoutData['yaxis.range[1]']
                        ]
                
                st.rerun()
        
        # Save zoom coordinates from the event if available
        if hasattr(event, 'relayoutData') and event.relayoutData:
            if 'xaxis.range[0]' in event.relayoutData and 'xaxis.range[1]' in event.relayoutData:
                st.session_state.zoom_xrange = [
                    event.relayoutData['xaxis.range[0]'],
                    event.relayoutData['xaxis.range[1]']
                ]
            if 'yaxis.range[0]' in event.relayoutData and 'yaxis.range[1]' in event.relayoutData:
                st.session_state.zoom_yrange = [
                    event.relayoutData['yaxis.range[0]'],
                    event.relayoutData['yaxis.range[1]']
                ]

        # Display data overview
        st.write("Cluster Data Overview")

        # If an item is selected, filter the dataframe
        if st.session_state.selected_item:
            filtered_data = cluster_data[
                cluster_data[st.session_state.groupby_column] == st.session_state.selected_item]
            st.dataframe(filtered_data)
        else:
            st.dataframe(cluster_data)
    else:
        st.write("No cluster data files found.")

# Load cluster data
cluster_data = load_cluster_data()

# Initialize cell_class in session state if it doesn't exist
if 'cell_class' not in st.session_state:
    st.session_state.cell_class = 'all'

# Set up the page layout with two columns
st.title("Cluster Analysis")

# Add cell class filter in the sidebar
st.sidebar.title("Filters")
cell_class_options = ['all', 'mitotic', 'interphase']  # Add default options
selected_cell_class = st.sidebar.radio(
    "Cell Class",
    cell_class_options,
    index=cell_class_options.index(st.session_state.cell_class) if st.session_state.cell_class in cell_class_options else 0
)
cluster_data = apply_filter(cluster_data, 'dir_level_1', selected_cell_class)
st.session_state.cell_class = selected_cell_class

selected_lr = create_filter_radio(cluster_data, 'leiden_resolution', st.sidebar, "Leiden Resolution", include_all=False)
cluster_data = apply_filter(cluster_data, 'leiden_resolution', selected_lr)

# Create two columns for the main content
col1, col2 = st.columns([1,1])

with col1:
    # Display cluster data in the left column
    display_cluster(cluster_data)

with col2:
    # Selected Gene info
    cell_class = st.session_state.get("cell_class", 'all')

    if 'selected_item' in st.session_state:
        selected_item = st.session_state.get("selected_item", None)
        selected_gene = st.session_state.get("selected_gene", None)
        groupby_column = st.session_state.get("groupby_column", None)
        
        if selected_item:
            selected_gene_info_df = cluster_data[cluster_data[groupby_column] == selected_item]
            gene_montages_root = os.path.join(ANALYSIS_ROOT, "aggregate", 'montages', f"{cell_class}__montages")
            
            # Check if gene_montages_root directory exists
            if os.path.exists(gene_montages_root):
                genes = selected_gene_info_df['gene_symbol_0'].tolist()
                
                # Display a dropdown to select a gene
                st.write(f"### Cluster ({len(genes)} genes)")
                
                # Define a callback for when the dropdown changes
                def on_gene_select():
                    st.session_state.selected_gene = st.session_state[f"gene_dropdown_{selected_item}"]
                
                # Determine the index of the selected gene in the dropdown
                selected_index = 0
                if selected_gene in genes:
                    selected_index = genes.index(selected_gene)
                
                # Create a dropdown to select a gene
                st.selectbox(
                    "Select a gene to view",
                    options=genes,
                    index=selected_index,
                    key=f"gene_dropdown_{selected_item}",  # Use a stable key based on the selected cluster
                    on_change=on_gene_select
                )
                
                # Display montages only for the selected gene
                if selected_gene:
                    display_gene_montages(gene_montages_root, selected_gene)
                else:
                    # If no gene is selected yet, select the first one
                    if genes:
                        st.session_state.selected_gene = genes[0]
                        st.rerun()
                    else:
                        st.write("No genes found in this cluster.")
            else:
                st.warning(f"⚠️ WARNING: Gene montages root directory does not exist: {gene_montages_root}")
        else:
            st.write("No group selected.")
    else:
        st.write("No group selected.")
