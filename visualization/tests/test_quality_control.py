import pytest
import os
from streamlit.testing.v1 import AppTest

def test_quality_control_page_loads():
    """Test that the Quality Control page loads without errors."""
    os.environ["BRIEFLOW_ANALYSIS_ROOT"] = "tests/fixtures/analysis_root"
    at = AppTest.from_file("pages/1_Quality_Control.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered the title
    assert len(at.markdown) > 0
    assert "Review the quality control metrics" in at.markdown[0].value 