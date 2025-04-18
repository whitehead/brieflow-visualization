import streamlit as st
import git
import os

st.set_page_config(
    page_title="Configuration - Brieflow Analysis",
    layout="wide",
)

st.title("Configuration")

# Get git repository information
try:
    repo = git.Repo(search_parent_directories=True)
    commit_hash = repo.head.commit.hexsha
    
    st.header("Git Repository Information")
    
    # Check if there are any remotes
    if repo.remotes:
        # Get the first remote's URL if origin doesn't exist
        remote_url = repo.remotes[0].url if not hasattr(repo.remotes, 'origin') else repo.remotes.origin.url
        st.write(f"**Repository URL:** {remote_url}")
    else:
        st.write("**Repository URL:** No remote repositories configured")
    
    st.write(f"**Current Commit Hash:** {commit_hash}")
except Exception as e:
    st.error(f"Error retrieving git information: {str(e)}")

# Read and display requirements.in
st.header("Requirements.in Contents")
st.write("""
**requirements.in** contains the direct dependencies of the project. 
We use **pip-tools** to manage dependencies:
- Add direct dependencies to requirements.in
- Run `pip-compile requirements.in` to generate requirements.txt with all transitive dependencies
- Run `pip install -r requirements.txt` to install all dependencies
""")
try:
    requirements_in_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.in")
    with open(requirements_in_path, 'r') as file:
        requirements_in_content = file.read()

    st.code(requirements_in_content, language="text")
except Exception as e:
    st.error(f"Error reading requirements.in: {str(e)}")

# Read and display requirements.txt
st.header("Requirements.txt Contents")
try:
    requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt")
    with open(requirements_path, 'r') as file:
        requirements_content = file.read()

    st.code(requirements_content, language="text")
except Exception as e:
    st.error(f"Error reading requirements.txt: {str(e)}")
