import pytest
import os
import pandas as pd
import numpy as np
import random
import string
from streamlit.testing.v1 import AppTest

# Set the analysis root directory for testing
os.environ["BRIEFLOW_ANALYSIS_ROOT"] = "test/fixtures/analysis_root"

def generate_random_gene_name():
    """Generate a random gene name that looks like a real one."""
    prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{prefix}{suffix}"

def generate_random_function():
    """Generate a random function description."""
    functions = [
        "FUNCTION: Regulates cellular processes through protein-protein interactions.",
        "FUNCTION: Catalyzes biochemical reactions in metabolic pathways.",
        "FUNCTION: Involved in signal transduction and cellular communication.",
        "FUNCTION: Plays a role in DNA replication and repair mechanisms.",
        "FUNCTION: Participates in protein synthesis and degradation.",
        "FUNCTION: Modulates gene expression through chromatin remodeling.",
        "FUNCTION: Mediates intracellular transport and vesicle trafficking.",
        "FUNCTION: Contributes to cell cycle regulation and apoptosis.",
        "FUNCTION: Facilitates ion transport across cellular membranes.",
        "FUNCTION: Regulates immune response and inflammation."
    ]
    return random.choice(functions)

def generate_test_cluster_data(n_rows=100):
    """Generate a test DataFrame with fake cluster data."""
    # Generate random PHATE coordinates
    phate_0 = np.random.uniform(-0.02, 0.02, n_rows)
    phate_1 = np.random.uniform(-0.01, 0.01, n_rows)
    
    # Generate random clusters (0-5)
    clusters = np.random.randint(0, 6, n_rows)
    
    # Generate gene symbols (mix of nontargeting and gene names)
    gene_symbols = []
    gene_names = []
    functions = []
    kegg_ids = []
    complex_portal = []
    string_ids = []
    
    for i in range(n_rows):
        if random.random() < 0.3:  # 30% chance of being nontargeting
            gene_symbols.append(f"nontargeting_{random.randint(1, 200)}")
            gene_names.append("")
            functions.append("")
            kegg_ids.append("")
            complex_portal.append("")
            string_ids.append("")
        else:
            gene_symbol = generate_random_gene_name()
            gene_symbols.append(gene_symbol)
            gene_names.append(f"{gene_symbol} {''.join(random.choices(string.ascii_uppercase, k=2))}{random.randint(100, 999)}")
            functions.append(generate_random_function())
            kegg_ids.append(f"hsa:{random.randint(10000, 99999)}")
            if random.random() < 0.3:  # 30% chance of having complex portal
                complex_portal.append(f"CPX-{random.randint(1000, 9999)}")
            else:
                complex_portal.append("")
            string_ids.append(f"9606.ENSP{random.randint(100000000, 999999999)}")
    
    data = {
        'gene_symbol_0': gene_symbols,
        'PHATE_0': phate_0,
        'PHATE_1': phate_1,
        'cluster': clusters,
        'Gene Names': gene_names,
        'Function': functions,
        'KEGG': kegg_ids,
        'ComplexPortal': complex_portal,
        'STRING': string_ids
    }
    
    return pd.DataFrame(data)

def write_test_cluster_data(n_rows=100, output_dir="test/fixtures/analysis_root"):
    """Generate and write test cluster data to a file."""
    # Create the cluster directory structure
    cluster_dir = os.path.join(output_dir, "cluster")
    os.makedirs(cluster_dir, exist_ok=True)
    
    # Generate the test data
    df = generate_test_cluster_data(n_rows)
    
    # Write to TSV file with the required naming convention
    output_file = os.path.join(cluster_dir, "test_data__phate_leiden_uniprot.tsv")
    df.to_csv(output_file, sep='\t', index=False)
    
    return output_file

def test_cluster_page_loads():
    """Test that the Cluster Analysis page loads without errors."""
    # Generate and write test data
    test_data_file = write_test_cluster_data()
    
    at = AppTest.from_file("pages/4_Cluster.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered the title
    assert len(at.markdown) > 0
    assert "Cluster Data Overview" in at.markdown[0].value 