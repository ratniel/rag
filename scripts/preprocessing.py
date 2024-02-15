from src.preprocessing_utils import delete_files_except_html, delete_empty_dirs, save_clean_html, save_clean_txt
import pickle
from pathlib import Path

dir_path = "./data/raw_data"
delete_files_except_html(path=dir_path)
delete_empty_dirs(path=dir_path)

# file_paths = [str(file_path) for file_path in Path("data/processed_html_data").rglob('*') if file_path.is_file()]

#load the file_paths list from file_paths.pkl
with open("ref/file_paths.pkl", "rb") as f:
    file_paths = pickle.load(f)

#append the file paths
file_paths = [dir_path + "/" + file for file in file_paths]


#save the clean html files and clean text files
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    try:
        save_clean_html(filepath=file_path, save_location="./data/clean_html", dir_path="data/raw_data")
    except Exception as e:
        print(f"Error occurred while saving clean HTML file: {file_path}")
        print(e)

    try:
        save_clean_txt(filepath=file_path, save_location="./data/clean_text", dir_path="data/raw_data")
    except Exception as e:
        print(f"Error occurred while saving clean text file: {file_path}")
        print(e)