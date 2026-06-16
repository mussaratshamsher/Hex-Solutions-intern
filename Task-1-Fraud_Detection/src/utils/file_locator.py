import os
from pathlib import Path
import streamlit as st

@st.cache_resource
def find_file(filename):
    """Deep searches for a file in the project directory."""
    root = Path.cwd()
    for root_dir, dirs, files in os.walk(root):
        if filename in files:
            return Path(root_dir) / filename
    return None
