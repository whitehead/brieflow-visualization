# Brieflow Visualization App - Page Data Summary

This document provides a summary of the pages in the Brieflow Visualization application, including the data files used and fields accessed by each page.

## Pages Overview

### Home.py
**Data Files Used:**
- `../README.md`

**Fields Used:**
- Text content

### 1_Quality_Control.py
**Data Files Used:**
- PNG and TSV files from analysis_root
- Files filtered by: 'phenotype', 'merge', 'sbs', 'aggregate' and 'eval'

**Fields Used:**
- `dir_level_0` (Phase): Extracted from the first level of the directory path by splitting the path and indexing
- `dir_level_2` (Subgroup): Extracted from the third level of the directory path by splitting the path and indexing
- `plate_id`: Extracted using regex pattern `r'(P-\d+)'` to find plate IDs in format "P-123" from the file path
- `well_id`: Extracted using regex pattern `r'(W-[A-Z]\d+)'` to find well IDs in format "W-A1", "W-B12", etc. from the file path
- `metric_name`: Extracted from the file basename by splitting on "__" and taking the last part (e.g., "image__metric_name.png")
- `file_path`: Stores the relative path of the file from the root directory

### 2_Cluster.py
**Data Files Used:**
- TSV files: `*__phate_leiden_uniprot.tsv`
- PNG and TSV files from 'cluster/plots'

**Fields Used:**
- `PHATE_0`, `PHATE_1` (coordinates)
- `gene_symbol_0`
- `cluster`
- `Gene Names`
- `source`
- `dir_level_0`, `dir_level_1`
- `metric_name`

### 3_Config.py
**Data Files Used:**
- Git repository information
- `requirements.in`
- `requirements.txt`

**Fields Used:**
- Repository URL
- Commit hash
- Package dependencies

### 4_Montages.py
**Data Files Used:**
- PNG files from 'montages' directory

**Fields Used:**
- `gene` (extracted from file path directory structure)
- `guide` (extracted from file path directory structure)
- `channel` (extracted from file path directory structure)
- `file_path`

These fields are extracted from the directory structure of the file paths. For example:

Real path example:
`analysis_root/montages/BRCA1/sgRNA_1234/GFP__cell_image.png`

The same path with placeholder variables:
`analysis_root/montages/{gene}/{guide}/{channel}__filename.png`

Where:
- `gene` = "BRCA1" (third-to-last directory component)
- `guide` = "sgRNA_1234" (second-to-last directory component)
- `channel` = "GFP" (first part of the filename before "__")