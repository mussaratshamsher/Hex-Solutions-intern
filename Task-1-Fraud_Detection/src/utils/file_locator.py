import os
from pathlib import Path
import streamlit as st

@st.cache_resource
def find_file(filename):
    """Deep searches for a file in the project directory."""
    root = Path.cwd()
    
    # Perform the search
    for root_dir, dirs, files in os.walk(root):
        if filename in files:
            return Path(root_dir) / filename
            
    # Diagnostic logging if not found
    error_msg = f"File '{filename}' not found. Current CWD: {root}\n"
    error_msg += "Partial Directory Tree:\n"
    
    # List top-level directories to understand structure
    for item in root.iterdir():
        if item.is_dir():
            error_msg += f"  DIR: {item.name}\n"
        else:
            error_msg += f"  FILE: {item.name}\n"
            
    st.error(error_msg)
    return None
