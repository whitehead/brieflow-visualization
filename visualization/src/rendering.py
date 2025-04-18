import os
import uuid
import pandas as pd
import streamlit as st

class VisualizationRenderer:
    @staticmethod
    def display_plots_and_tables(filtered_df, root_dir):
        # Group by directory and basename
        grouped = filtered_df.groupby(['dir', 'basename'])
        # Iterate through each group
        for (dir_name, base_name), group_df in grouped:
            with st.container():
                st.markdown(f"### Group: {dir_name} - {base_name}")

                # Count only the items we'll actually display
                display_items = []
                for _, row in group_df.iterrows():
                    has_png = any(r['ext'] == 'png' for _, r in group_df.iterrows())
                    if row['ext'] == 'png' or (row['ext'] == 'tsv' and not has_png):
                        display_items.append(row)

                # Create columns based on actual display items
                cols = st.columns(min(3, len(display_items)))

                for idx, row in enumerate(display_items):
                    col_idx = idx % len(cols)
                    with cols[col_idx]:
                        # Check if this group has both PNG and TSV
                        has_png = any(r['ext'] == 'png' for _, r in group_df.iterrows())
                        has_tsv = any(r['ext'] == 'tsv' for _, r in group_df.iterrows())

                        if row['ext'] == 'png':
                            # Always show PNG if it exists
                            try:
                                st.image(os.path.join(root_dir, row['file_path']),
                                         caption=f"{row['metric_name']} - {row['well_id']}")
                            except Exception as e:
                                st.error(f"Could not load image: {row['file_path']}")
                                st.error(str(e))

                            # If there's a corresponding TSV, add download link
                            if has_tsv:
                                tsv_row = group_df[group_df['ext'] == 'tsv'].iloc[0]
                                tsv_path = os.path.join(root_dir, tsv_row['file_path'])
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
                                tsv_data = pd.read_csv(os.path.join(root_dir, row['file_path']), sep='\t')
                                st.dataframe(tsv_data)
                            except Exception as e:
                                st.error(f"Error reading TSV file: {e}")

                st.markdown("---")  # Add a separator between groups
