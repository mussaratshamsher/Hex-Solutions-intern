import os
from pathlib import Path

def find_file(filename):
    print(f"Searching for {filename}...")
    # Start search from the repository root (often CWD in Streamlit Cloud)
    root = Path.cwd()
    
    for root_dir, dirs, files in os.walk(root):
        if filename in files:
            path = Path(root_dir) / filename
            print(f"FOUND: {path}")
            return path
            
    print("FILE NOT FOUND")
    return None

if __name__ == "__main__":
    find_file("fraud_model.pkl")
    find_file("transactions.csv")
