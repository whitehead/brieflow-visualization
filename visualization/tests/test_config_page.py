import pytest
from streamlit.testing.v1 import AppTest

def test_config_page_loads():
    """Test that the Config page loads without errors."""
    at = AppTest.from_file("pages/2_Config.py")
    at.run(timeout=10)
    
    # Verify no exceptions occurred
    assert not at.exception
    
    # Verify the page rendered something
    assert len(at.markdown) > 0 