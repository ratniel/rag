import os
from pathlib import Path
from src.preprocessing_utils import save_clean_html, delete_files_except_html, delete_empty_dirs
import pickle
#load list from a pickle file
with open('file_paths.pkl', 'rb') as f:
    file_paths = pickle.load(f)


delete_files_except_html(path="data/raw_data")
delete_empty_dirs(path="data/raw_data")

#append raw_data to file_paths
file_paths = ["data/raw_data/"+file_path for file_path in file_paths]
error_files = []

for file_path in file_paths:
    try:
        save_clean_html(Path(file_path))
    except Exception as e:
        error_files.append(file_path)
        print(f"Error processing {file_path}: {e}")