import os
from pathlib import Path
import streamlit as st

@st.cache_resource
def find_file(filename):
    """Deterministically searches for a file in the project directory."""
    # Project root is 3 levels up from this file (src/utils/file_locator.py)
    root = Path(__file__).resolve().parent.parent.parent
    
    # 1. Direct path lookup for known directories
    known_paths = [
        root / "models" / filename,
        root / "data" / filename,
    ]
    
    for path in known_paths:
        if path.exists():
            return path
            
    # 2. Fallback: Perform a search
    for root_dir, dirs, files in os.walk(root):
        if filename in files:
            return Path(root_dir) / filename
            
    # Diagnostic logging if not found
    error_msg = f"File '{filename}' not found. Searched known paths: {known_paths}\n"
    error_msg += f"Project Root: {root}\n"
    
    st.error(error_msg)
    return None
