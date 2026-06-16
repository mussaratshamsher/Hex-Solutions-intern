import os
from pathlib import Path
import streamlit as st

@st.cache_resource
def find_file(filename):
    """Deep searches for a file in the project directory."""
    # Project root is 3 levels up from this file (src/utils/file_locator.py)
    root = Path(__file__).resolve().parent.parent.parent
    
    # Perform the search
    for root_dir, dirs, files in os.walk(root):
        if filename in files:
            return Path(root_dir) / filename
            
    # Diagnostic logging if not found
    error_msg = f"File '{filename}' not found. Current CWD: {Path.cwd()}\n"
    error_msg += f"Project Root Searched: {root}\n"
    error_msg += "Partial Directory Tree:\n"
    
    # List top-level directories to understand structure
    for item in root.iterdir():
        if item.is_dir():
            error_msg += f"  DIR: {item.name}\n"
        else:
            error_msg += f"  FILE: {item.name}\n"
            
    st.error(error_msg)
    return None
