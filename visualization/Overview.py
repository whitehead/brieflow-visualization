import streamlit as st
from pathlib import Path

# Render the README.md file
readme_path = Path("../README.md")
if readme_path.exists():
    content = readme_path.read_text()
    st.markdown(content, unsafe_allow_html=True)
else:
    st.warning(f"{readme_path} file not found")
