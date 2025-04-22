import pytest
import os
import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

# Add the visualization directory to the Python path
visualization_dir = str(Path(__file__).parent.parent)
if visualization_dir not in sys.path:
    sys.path.insert(0, visualization_dir)

def test_overview_page_loads():
    """Test that the Overview page loads without errors."""
    at = AppTest.from_file("../Overview.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered something
    assert len(at.markdown) > 0