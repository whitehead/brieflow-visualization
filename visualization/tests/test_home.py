import pytest
from streamlit.testing.v1 import AppTest

def test_home_page_loads():
    """Test that the Home page loads without errors."""
    at = AppTest.from_file("Home.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered something
    assert len(at.markdown) > 0 

def test_quality_control_page_loads():
    """Test that the Quality Control page loads without errors."""
    at = AppTest.from_file("pages/1_Quality_Control.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered the title
    assert len(at.markdown) > 0
    assert "Review the quality control metrics" in at.markdown[0].value 

def test_cluster_page_loads():
    """Test that the Cluster Analysis page loads without errors."""
    at = AppTest.from_file("pages/2_Cluster.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered the title
    assert len(at.markdown) > 0
    assert "Cluster Data Overview" in at.markdown[0].value 