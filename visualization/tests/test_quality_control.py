import pytest
import os
import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

# Add the visualization directory to the Python path
visualization_dir = str(Path(__file__).parent.parent)
if visualization_dir not in sys.path:
    sys.path.insert(0, visualization_dir)

def test_quality_control_page_loads():
    """Test that the Quality Control page loads without errors."""
    os.environ["BRIEFLOW_ANALYSIS_ROOT"] = "tests/fixtures/analysis_root"
    at = AppTest.from_file("../pages/3_Quality_Control.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered the title
    assert len(at.markdown) > 0
    assert "Review the quality control metrics" in at.markdown[0].value 