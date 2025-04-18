import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

st.set_page_config(
    page_title="Cluster Analysis - Brieflow Analysis",
    layout="wide"
)

st.title("Cluster Analysis")

# Load and merge cluster TSV files
@st.cache_data
def load_cluster_data():
    # Find all relevant TSV files
    analysis_root = os.getenv('BRIEFLOW_ANALYSIS_ROOT', '../analysis_root')
    tsv_files = glob.glob(f"{analysis_root}/cluster/**/*__phate_leiden_uniprot.tsv", recursive=True)
    
    # Initialize empty list to store dataframes
    dfs = []
    
    # Read each file and add source attribute
    for file_path in tsv_files:
        # Get the base name of the file (without extension)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Read the TSV file
        df = pd.read_csv(file_path, sep='\t')
        
        # Add source column
        df['source'] = base_name
        
        dfs.append(df)
    
    # Concatenate all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()

# Load the data
cluster_data = load_cluster_data()

# Display the data
if not cluster_data.empty:
    # Create scatter plot
    fig = px.scatter(
        cluster_data,
        x='PHATE_0',
        y='PHATE_1',
        color='source',
        hover_data=['gene_symbol_0', 'cluster', 'Gene Names'],
        title='PHATE Visualization',
        width=1000,
        height=800
    )
    
    # Update layout for better visualization
    fig.update_layout(
        hovermode='closest',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("Cluster Data Overview")
    st.dataframe(cluster_data)
else:
    st.write("No cluster data files found.") 
